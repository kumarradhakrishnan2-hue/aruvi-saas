"use client";
import { useEffect, useMemo, useState } from "react";
import { getJSON, markPrepared, pad, pretty, ROMAN, annualBudgetPeriods } from "../lib/format";
import { RollWheel } from "./wheels";
import ViewModelView from "./ViewModelView";

/* ───────── PrepareLesson — the everyday, single-chapter generate flow (2026-07-03) ─────────
 * The bottom-up utilization path: the teacher prepares ONE chapter at a time, sets that
 * chapter's periods, and generates its lesson plan + assessment. Her actual consumption
 * accrues from these individual acts — no annual plan is required, and this flow NEVER calls
 * the allocator or touches the allocation register.
 *
 * This is deliberately decoupled from the top-down annual-budget allocator (Allocate.jsx +
 * PDF report), which stays as its own independent capability answering "how do I spread my
 * 180 periods across the whole year?" — a strategic overview a teacher may follow fully,
 * partly, or not at all. The two never gate each other.
 *
 * Flow: pick chapter → set periods (effort-index SUGGESTION default, editable) → Generate.
 * The screen also shows how this chapter sits inside the teacher's annual budget: what her
 * already-prepared lessons (the My Lessons list for this class) have committed, plus what the
 * proposed periods add. Live generation is still deferred (see api/main.py's /generate stub),
 * so "Generate" opens the closest saved plan's view as a preview.
 *
 * Props: subject (slug) · grade (slug) · readiness (for the annual budget) · onNavigate.
 */

const DEFAULT_PERIODS = 12; // fallback when neither a budget-based suggestion nor an NCF figure exists

// Teachers say "Class 7", not "Grade VII" — ROMAN starts at "iii" → 3.
const classNum = (g) => {
  const idx = ROMAN.indexOf((g || "").toLowerCase());
  return idx >= 0 ? idx + 3 : (g || "").toUpperCase();
};

export default function PrepareLesson({ subject, grade, readiness, onNavigate, onPrepared }) {
  const [chapters, setChapters] = useState([]);
  const [chapterNo, setChapterNo] = useState("");          // chapter_number as string
  const [periods, setPeriods] = useState(DEFAULT_PERIODS);
  const [step, setStep] = useState("chapter");             // "chapter" | "preview"
  const [plans, setPlans] = useState([]);                  // saved plans (preview source + committed budget)
  const [busy, setBusy] = useState(false);
  const [view, setView] = useState(null);
  const [error, setError] = useState("");
  const [note, setNote] = useState("");
  const [showInfo, setShowInfo] = useState(false);         // effort-index explainer popover
  const [showBreakdown, setShowBreakdown] = useState(false); // committed-chapters popup
  const [warnRegen, setWarnRegen] = useState(false);       // re-preparing an already-prepared chapter

  // Load chapters (+ effort weight + NCF estimate) and saved plans for the scope.
  useEffect(() => {
    setStep("chapter"); setChapterNo(""); setView(null); setError(""); setNote("");
    setChapters([]); setPlans([]); setShowInfo(false); setShowBreakdown(false); setWarnRegen(false);
    getJSON(`/subjects/${subject}/${grade}/chapters`)
      .then((d) => setChapters(d.chapters || [])).catch(() => setChapters([]));
    getJSON(`/plans/${subject}/${grade}`)
      .then((d) => setPlans(d.plans || [])).catch(() => setPlans([]));
  }, [subject, grade]);

  // Annual budget (periods) for this subject·grade, from the canonical readiness profile.
  const annualBudget = useMemo(
    () => annualBudgetPeriods(readiness, subject, grade),
    [readiness, subject, grade]
  );

  // Total effort weight across all chapters — the denominator of each chapter's budget share.
  const sumW = useMemo(
    () => chapters.reduce((s, c) => s + (Number(c.weight) || 0), 0),
    [chapters]
  );

  // Aruvi's suggested periods for a chapter: its effort-index SHARE of the teacher's OWN annual
  // budget (weight_c / Σweights × budget) — the same basis Allocate uses. NCF is deliberately NOT
  // used here (2026-07-08): by the time this route runs the class has been created and its annual
  // budget collected, so the suggestion keys off her real budget. A flat default is the only
  // fallback (e.g. a chapter with no effort weight); NCF never drives the number.
  const suggestionFor = (c) => {
    if (!c) return DEFAULT_PERIODS;
    if (annualBudget != null && sumW > 0 && c.weight != null) {
      const v = Math.round(((Number(c.weight) || 0) / sumW) * annualBudget);
      return v > 0 ? v : 1;
    }
    return DEFAULT_PERIODS;
  };

  const chosen = chapters.find((c) => String(c.chapter_number) === String(chapterNo));
  const suggestion = suggestionFor(chosen);
  const planFor = (cn) => plans.find((p) => String(p.chapter_number) === String(cn));

  // The suggestion becomes the default value when a chapter is chosen (still editable).
  useEffect(() => {
    const c = chapters.find((x) => String(x.chapter_number) === String(chapterNo));
    if (!c) return;
    setPeriods(suggestionFor(c));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [chapterNo, chapters, annualBudget, sumW]);

  // Files currently ATTACHED to a section of this class (localStorage bindings) — so a chapter a
  // class is actively teaching counts toward the budget even if its `prepared` write was lost
  // (mirrors My Lessons' `p.prepared || isAttached(p)`).
  const attachedFiles = useMemo(() => {
    const set = new Set();
    if (typeof window === "undefined") return set;
    const subs = (readiness && readiness.subjects) || [];
    const slugify = (n) => (n || "").toLowerCase().replace(/ /g, "_");
    const sub = subs.find((s) => slugify(s.name) === subject);
    const g = sub && (sub.grades || []).find((x) => (x.grade || "").toLowerCase() === grade);
    ((g && g.sections) || []).forEach((sec) => {
      try {
        const f = window.localStorage.getItem(`current_chapter_${subject}_${grade}_${sec.tag}`);
        if (f) set.add(f);
      } catch {}
    });
    return set;
  }, [readiness, subject, grade]);

  // Chapters the teacher has already prepared for THIS class (the My Lessons list) — one row per
  // chapter, each contributing its lesson plan's period count (total_units). Excludes the chapter
  // she's preparing now (that's the "proposed" segment, not yet committed) and any archived plan.
  const committed = useMemo(() => {
    const arr = (plans || []).filter(
      (p) => (p.prepared || attachedFiles.has(p.filename)) && !p.archived
        && String(p.chapter_number) !== String(chapterNo)
    );
    const byCh = {};
    arr.forEach((p) => {
      const k = String(p.chapter_number);
      const prev = byCh[k];
      if (!prev || String(p.prepared_at || "") > String(prev.prepared_at || "")) byCh[k] = p;
    });
    return Object.values(byCh)
      .map((p) => ({
        filename: p.filename,
        chapter_number: p.chapter_number,
        chapter_title: p.chapter_title,
        // Track the teacher's CHOSEN periods (what she allocated). Fall back to the served plan's
        // authored learning-unit count only when no chosen count was stored (e.g. first-run).
        periods: (p.prepared_periods != null ? Number(p.prepared_periods) : Number(p.total_units)) || 0,
      }))
      .sort((a, b) => (Number(a.chapter_number) || 0) - (Number(b.chapter_number) || 0));
  }, [plans, attachedFiles, chapterNo]);

  // Has the chosen chapter already been prepared (it's in her generated list / attached to a
  // section)? Re-preparing is allowed, but warned — and for budget tracking only the LATEST
  // generation counts (the `committed` dedupe above keeps the newest prepared_at per chapter).
  const chosenAlreadyPrepared = useMemo(
    () => !!chapterNo && (plans || []).some(
      (p) => String(p.chapter_number) === String(chapterNo) && (p.prepared || attachedFiles.has(p.filename))
    ),
    [plans, chapterNo, attachedFiles]
  );

  const committedTotal = committed.reduce((s, c) => s + c.periods, 0);
  // "Used" / "Available" reflect only what's ACTUALLY committed (already-prepared chapters),
  // NOT the chapter she's proposing now — that lives in the Suggestion box.
  const left = annualBudget != null ? annualBudget - committedTotal : null;
  const over = left != null && left < 0;

  // "Prepare the lesson" — records the chapter as prepared, then RETURNS to where she came from
  // (the section's attach popup, or My Lessons) with the new chapter now listed — it does NOT
  // open the lesson plan. Attaching/teaching is a separate, deliberate step done from there.
  // Live gen is still deferred, so "prepared" means the chapter's saved plan becomes hers; we
  // await the mark so the popup's refetch sees `prepared` immediately. A chapter with no saved
  // plan yet can't be prepared — a stand-in preview is shown instead so testing isn't blocked.
  // Click handler: if this chapter is already prepared, warn first (re-preparing replaces the
  // tracked version); otherwise prepare straight away.
  const onPrepareClick = () => {
    if (!chosen) return;
    if (chosenAlreadyPrepared) { setWarnRegen(true); return; }
    doGenerate();
  };

  const doGenerate = async () => {
    if (!chosen) return;
    const exact = planFor(chapterNo);            // the plan for the chapter she actually chose
    if (exact) {
      setBusy(true);
      try {
        await markPrepared(subject, grade, exact.filename, periods);
        if (onPrepared) { onPrepared({ subject, grade, filename: exact.filename, chapterNo }); return; }
      } finally {
        setBusy(false);
      }
    }
    // No exact saved plan (or no return handler) → fall back to the stand-in preview.
    setStep("preview"); setBusy(true); setError(""); setNote(""); setView(null);
    try {
      let match = exact;
      if (!match && plans.length) {
        match = plans[0];
        setNote(`No saved plan for Chapter ${chapterNo} yet — showing Chapter ${match.chapter_number} (${match.chapter_title}) as a stand-in preview.`);
      }
      if (!match) {
        setError(`No saved plan available yet for ${pretty(subject)} · Class ${classNum(grade)}.`);
        return;
      }
      setView((await getJSON(`/plans/${subject}/${grade}/${match.filename}/view`)).view);
    } catch {
      setError("Couldn't load a plan right now. Try again in a moment.");
    } finally {
      setBusy(false);
    }
  };

  // ── preview: the generated (saved-plan) lesson ──
  if (step === "preview") {
    return (
      <div>
        <button className="back" onClick={() => { setStep("chapter"); setView(null); }}>← back to chapter</button>
        {busy && <div className="empty">Building your lesson plan…</div>}
        {!busy && error && <div className="empty">{error}</div>}
        {!busy && !error && note && <p className="h2-sub">{note}</p>}
        {!busy && !error && view && <ViewModelView view={view} />}
      </div>
    );
  }

  // ── chapter + periods ──
  const setP = (n) => setPeriods(Number.isFinite(n) && n >= 0 ? n : 0);
  return (
    <div>
      <div className="prep-hdr-row">
        <p className="h2">Prepare a lesson plan</p>
        <button className="back back-tr" onClick={() => onNavigate && onNavigate("myplans")}>← back</button>
      </div>
      <div className="ap-kicker prep-scope">{pretty(subject)} · Class {classNum(grade)}</div>
      <p className="h2-sub prep-instr">
        Pick one chapter and enter the periods you plan to spend teaching it.
      </p>

      {!chapters.length ? (
        <div className="empty">No chapter mappings for this subject &amp; grade yet.</div>
      ) : (
        <>
          <RollWheel ariaLabel="Chapter" value={chapterNo} onChange={setChapterNo} rowPx={92}
            items={chapters.map((c) => ({ id: String(c.chapter_number), chip: c.chapter_number, label: c.chapter_title }))} />

          <div className="prep-block">
            <div className="prep-left">
              <p className="prep-fieldlab">Periods for this chapter</p>
              <span className="steppermini prep-stepper">
                <button type="button" onClick={() => setP((Number(periods) || 0) - 1)} aria-label="fewer periods">–</button>
                <input type="number" min="0" className="v g4-vinput" value={periods}
                  onChange={(e) => setP(parseInt(e.target.value, 10))} aria-label="Periods for this chapter" />
                <button type="button" onClick={() => setP((Number(periods) || 0) + 1)} aria-label="more periods">+</button>
              </span>
            </div>

            {chosen ? (
              <div className="prep-right">
                <div className="prep-box prep-sugg2">
                  <div className="prep-sugg-hd">
                    <span className="prep-sugg-k">Suggestion</span>
                    <button type="button" className="prep-info" aria-label="How the suggestion is made"
                      onClick={() => setShowInfo((v) => !v)}>i</button>
                  </div>
                  <div className="prep-sugg-body">
                    <span className="prep-sugg-val">{suggestion}</span>
                    {periods === suggestion
                      ? <span className="prep-sugg-ok" aria-label="matches the suggestion">✓</span>
                      : <button type="button" className="prep-use" onClick={() => setPeriods(suggestion)}>use</button>}
                  </div>
                  {showInfo && (
                    <div className="prep-tip" role="note">
                      Aruvi shares your annual budget for this class across its chapters by each
                      chapter&rsquo;s effort index — heavier chapters get more periods. It&rsquo;s a
                      starting point, so you can change it freely.
                    </div>
                  )}
                </div>

                {annualBudget != null ? (
                  <div className="prep-box prep-budget2">
                    <div className="prep-brow">
                      <span className="prep-brow-k">Total periods</span>
                      <span className="prep-brow-v pine">{annualBudget}</span>
                    </div>
                    <button type="button" className="prep-brow prep-brow-btn" disabled={!committed.length}
                      onClick={() => setShowBreakdown(true)}
                      aria-label={`Used ${committedTotal} periods${committed.length ? " — view breakdown" : ""}`}>
                      <span className="prep-brow-k">Used{committed.length ? <span className="prep-brow-info" aria-hidden="true"> ⓘ</span> : null}</span>
                      <span className="prep-brow-v clay">{committedTotal}</span>
                    </button>
                    <div className="prep-brow">
                      <span className="prep-brow-k">Available</span>
                      <span className={`prep-brow-v${over ? " clay" : ""}`}>{over ? `−${-left}` : left}</span>
                    </div>
                  </div>
                ) : null}
              </div>
            ) : null}
          </div>

          <div className="savebar savebar-prep">
            <button className="primary prepare-cta" disabled={!chosen} onClick={onPrepareClick}>
              {chosenAlreadyPrepared ? "Prepare again →" : "Prepare the lesson →"}
            </button>
            {!chosen
              ? <span className="savebar-hint">Pick a chapter to continue.</span>
              : chosenAlreadyPrepared
                ? <span className="savebar-hint">Already prepared — preparing again replaces the tracked version.</span>
                : null}
          </div>
        </>
      )}

      {warnRegen && chosen ? (
        <div className="ap-overlay" onClick={() => setWarnRegen(false)}>
          <div className="ap-modal ap-confirm" onClick={(e) => e.stopPropagation()}>
            <button className="ap-close" aria-label="Close" onClick={() => setWarnRegen(false)}>✕</button>
            <div className="ap-head">
              <div className="ap-kicker">{pretty(subject)} · Class {classNum(grade)}</div>
              <div className="ap-title">Prepare this chapter again?</div>
              <div className="ap-sub">
                You&rsquo;ve already prepared &ldquo;{chosen.chapter_title}&rdquo; for this class.
                Preparing it again makes a fresh lesson plan — and for budget tracking, only this
                latest version will count.
              </div>
            </div>
            <div className="ap-confirm-actions">
              <button className="ap-btn-ghost" onClick={() => setWarnRegen(false)}>Cancel</button>
              <button className="ap-btn-danger" onClick={() => { setWarnRegen(false); doGenerate(); }}>Prepare again</button>
            </div>
          </div>
        </div>
      ) : null}

      {showBreakdown ? (
        <div className="ap-overlay" onClick={() => setShowBreakdown(false)}>
          <div className="ap-modal" onClick={(e) => e.stopPropagation()}>
            <button className="ap-close" aria-label="Close" onClick={() => setShowBreakdown(false)}>✕</button>
            <div className="ap-head">
              <div className="ap-kicker">{pretty(subject)} · Class {classNum(grade)}</div>
              <div className="ap-title">Committed so far</div>
              <div className="ap-sub">Periods already taken by the lessons you&rsquo;ve prepared for this class.</div>
            </div>
            <div className="ap-list">
              {committed.map((c) => (
                <div className="prep-brk-row" key={c.filename}>
                  <span className="prep-brk-ch">Ch {pad(c.chapter_number)}</span>
                  <span className="prep-brk-name" title={c.chapter_title}>{c.chapter_title}</span>
                  <span className="prep-brk-p">{c.periods}</span>
                </div>
              ))}
              <div className="prep-brk-total">
                <span>Total committed</span>
                <span>{committedTotal} periods</span>
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}
