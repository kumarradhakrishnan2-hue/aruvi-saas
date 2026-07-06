"use client";
import { useEffect, useRef, useState } from "react";
import { getJSON, pretty, pad, gradeUp } from "../lib/format";
import { pushSectionState, pullSectionState } from "../lib/sectionState";
import { readHistory, recordHistory, hasHistory } from "../lib/sectionHistory";
import Readiness from "./Readiness";
import LessonView from "./LessonView";

const subjectSlug = (name) => (name || "").toLowerCase().replace(/ /g, "_");
const gradeSlug = (g) => (g || "").toLowerCase();

// Small "history" glyph (clock + counter-clockwise arrow) for the section card's history button.
const HistoryIcon = (
  <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor"
    strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M3 3v5h5" />
    <path d="M3.05 13A9 9 0 1 0 6 5.3L3 8" />
    <path d="M12 7v5l3 2" />
  </svg>
);
// History-status → the label shown on the popup pill.
const HISTORY_LABEL = { ongoing: "Ongoing", completed: "Completed", untracked: "Untracked" };
// Back-compat: an earlier build stored the untracked status as "set_aside". Normalize legacy
// localStorage entries so they still render with a label + slate pill instead of a blank status.
const normStatus = (s) => (s === "set_aside" ? "untracked" : s);

/* ONE CARD PER subject·grade·section the teacher handles — across ALL subjects (walks the
 * canonical readiness.subjects[], not the single active projection). NO day derivation
 * (2026-07-02): My Classes is pointer-organized ("where did I stop?"), never day-organized —
 * the calendar was a category error against the section-pointer model (MEMORY.md). Each entry
 * carries the slugs + section tag so the card can look up that class's plans and pointer. */
function classesFromReadiness(readiness) {
  const subjects = (readiness && readiness.subjects) || [];
  const out = [];
  subjects.forEach((s) => {
    const sSlug = subjectSlug(s.name);
    (s.grades || []).forEach((g) => {
      const gSlug = gradeSlug(g.grade);
      (g.sections || []).forEach((sec) => {
        out.push({
          subjectName: s.name, subjectSlug: sSlug, grade: g.grade, gradeSlug: gSlug,
          sectionTag: sec.tag,
        });
      });
    });
  });
  return out;
}

export default function MyPlans({ subject, grade, ready, readiness, onReady, onNavigate, onEnterGenerate, user, onSignOut, pendingOpen, onConsumePending }) {
  const [openPlan, setOpenPlan] = useState(null);  // { view, sectionKey } for LessonView
  const [loading, setLoading] = useState(false);
  const [setupStarted, setSetupStarted] = useState(false); // 2a welcome → grid flow gate
  const [attachFor, setAttachFor] = useState(null); // { c, sectionKey } — "+" track-a-chapter picker
  const [untrackFor, setUntrackFor] = useState(null); // { c, sectionKey, plan } — "−" untrack confirm
  const [historyFor, setHistoryFor] = useState(null); // { c, sectionKey } — chapter-history popup
  const [, setSyncTick] = useState(0); // bumped after a server pull so cards re-read the refreshed cache
  // plans for EVERY subject·grade the teacher handles, keyed `${subjectSlug}/${gradeSlug}`.
  const [plansByKey, setPlansByKey] = useState({});

  // All classes across all subjects (one card per subject·grade·section).
  const classes = ready ? classesFromReadiness(readiness) : [];

  // Fetch saved plans once per distinct subject·grade the teacher handles.
  useEffect(() => { setOpenPlan(null);
    if (!ready) return;
    const seen = new Set();
    classes.forEach((c) => {
      const key = `${c.subjectSlug}/${c.gradeSlug}`;
      if (seen.has(key)) return; seen.add(key);
      setPlansByKey((prev) => (key in prev ? prev : { ...prev, [key]: undefined }));
      getJSON(`/plans/${c.subjectSlug}/${c.gradeSlug}`)
        .then((d) => setPlansByKey((prev) => ({ ...prev, [key]: d.plans || [] })))
        .catch(() => setPlansByKey((prev) => ({ ...prev, [key]: [] })));
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ready, readiness]);

  // Reconcile section teaching-state (tracked chapter + pointer + done) from the SERVER into the
  // localStorage cache, so a device shows the same tracking/progress the teacher set elsewhere
  // (fixes the Chrome-vs-iPhone divergence). localStorage stays the optimistic cache; the server
  // row is authoritative here. Bump syncTick when done so the cards re-read the cache.
  //
  // Re-syncs WITHOUT a manual refresh: on load, whenever the tab regains focus / becomes visible
  // (the "I just switched to my iPhone" moment), and on a light interval while visible. We skip a
  // sync while a modal or the lesson view is open so an in-flight action is never clobbered.
  const uiBusyRef = useRef(false);
  uiBusyRef.current = !!(attachFor || untrackFor || openPlan || historyFor);
  useEffect(() => {
    if (!ready) return;
    const keys = classesFromReadiness(readiness)
      .map((c) => `${c.subjectSlug}_${c.gradeSlug}_${c.sectionTag}`);
    if (!keys.length) return;
    let live = true;
    const sync = () => {
      if (!live || uiBusyRef.current) return;
      pullSectionState(keys).then(() => { if (live) setSyncTick((t) => t + 1); });
    };
    sync(); // initial reconcile
    const onVis = () => { if (document.visibilityState === "visible") sync(); };
    document.addEventListener("visibilitychange", onVis);
    window.addEventListener("focus", sync);
    const iv = setInterval(() => { if (document.visibilityState === "visible") sync(); }, 20000);
    return () => {
      live = false;
      document.removeEventListener("visibilitychange", onVis);
      window.removeEventListener("focus", sync);
      clearInterval(iv);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ready, readiness, user]);

  // Deep-link from Track (My Lesson Plans): open a specific SECTION's plan, pointer-enabled.
  // Uses the request's OWN subject/grade (My Week is no longer scoped to one subject·grade).
  useEffect(() => {
    if (!pendingOpen || !ready) return;
    const { subject: pSub, grade: pGrade, sectionTag, filename } = pendingOpen;
    if (!pSub || !pGrade || !filename) { onConsumePending && onConsumePending(); return; }
    const sectionKey = `${pSub}_${pGrade}_${sectionTag}`;
    let live = true;
    setLoading(true);
    getJSON(`/plans/${pSub}/${pGrade}/${filename}/view`)
      .then((d) => { if (live) setOpenPlan({ view: d.view, sectionKey }); })
      .catch(() => {})
      .finally(() => { if (live) { setLoading(false); onConsumePending && onConsumePending(); } });
    return () => { live = false; };
  }, [pendingOpen, ready, onConsumePending]);

  // Readiness incomplete → first the 2a welcome landing, then the readiness grid flow.
  if (!ready) {
    if (!setupStarted) {
      // Screen 2a — welcome / readiness-incomplete empty state.
      return (
        <div className="welcome">
          <div className="kicker kicker-ochre welcome-kicker">Welcome to Aruvi</div>
          <div className="welcome-title">Let&rsquo;s get your week set up</div>
          <div className="welcome-sub">Aruvi needs two quick things before it can plan with you — your weekly grid of classes, and how long your teaching year is.</div>
          <div className="welcome-sub">This only takes a few minutes, and you&rsquo;ll only do it once.</div>
          <button className="welcome-begin" onClick={() => setSetupStarted(true)}>Let&rsquo;s begin →</button>
        </div>
      );
    }
    // Readiness grid flow (ported from readiness-grid-flow.html). Completing it unlocks Generate.
    return (
      <Readiness
        subject={pretty(subject)}
        onComplete={(payload) => { onReady && onReady(payload); /* stay in My Plans → 2b welcome */ }}
      />
    );
  }

  const openLesson = async (sSlug, gSlug, p, sectionKey) => {
    setLoading(true);
    try {
      const view = (await getJSON(`/plans/${sSlug}/${gSlug}/${p.filename}/view`)).view;
      setOpenPlan({ view, sectionKey });
    } finally { setLoading(false); }
  };

  // current-LU pointer (per section) from localStorage, for the "On: Learning Unit N" line
  const pointerFor = (sectionKey) => {
    if (typeof window === "undefined") return null;
    const n = Number(window.localStorage.getItem(`lu_pointer_${sectionKey}`));
    return Number.isFinite(n) && n >= 0 ? n + 1 : null;
  };
  // How many learning units this section has marked complete (= the raw pointer index; 0 when
  // untouched). This is the anti-noise gate for history: a chapter only enters the log if ≥1 unit
  // was completed before it left the current slot (teacher's rule — track/untrack is used casually).
  const unitsDoneFor = (sectionKey) => {
    if (typeof window === "undefined") return 0;
    const n = Number(window.localStorage.getItem(`lu_pointer_${sectionKey}`));
    return Number.isFinite(n) && n > 0 ? n : 0;
  };
  // Which chapter (filename) a section is currently tracking. Written when a chapter is bound to
  // a class; absent = nothing started yet ("pick a chapter to begin tracking").
  const currentChapterFile = (sectionKey) => {
    if (typeof window === "undefined") return null;
    try { return window.localStorage.getItem(`current_chapter_${sectionKey}`) || null; } catch { return null; }
  };
  // Completion flag written by LessonView when the last learning unit is marked complete.
  const isDone = (sectionKey) => {
    if (typeof window === "undefined") return false;
    try { return window.localStorage.getItem(`lu_done_${sectionKey}`) === "1"; } catch { return false; }
  };
  // Bind an already-prepared chapter to a section and return to the cards view — the originating
  // section card now shows this chapter (closing the modal re-renders it). We deliberately do NOT
  // open the lesson: the teacher lands back on My Classes, where she tapped "+", not inside the plan.
  // The pointer + done flag are PER-SECTION, so switching to a new chapter (e.g. from a completed
  // one) resets them — the new chapter starts fresh at its first learning unit.
  const attachChapter = (c, sectionKey, plan) => {
    try {
      window.localStorage.setItem(`current_chapter_${sectionKey}`, plan.filename);
      window.localStorage.removeItem(`lu_pointer_${sectionKey}`);
      window.localStorage.removeItem(`lu_done_${sectionKey}`);
    } catch {}
    pushSectionState(sectionKey);   // sync the new binding to the server (cross-device)
    setAttachFor(null);
  };

  // Clear a section's chapter binding + pointer + done. The chapter itself is untouched (still in
  // My Lessons); the card returns to the unstarted "Pick a chapter" (grey) state.
  const clearBinding = (sectionKey) => {
    try {
      window.localStorage.removeItem(`current_chapter_${sectionKey}`);
      window.localStorage.removeItem(`lu_pointer_${sectionKey}`);
      window.localStorage.removeItem(`lu_done_${sectionKey}`);
    } catch {}
    pushSectionState(sectionKey);   // no chapter now → the server row is deleted (untrack)
  };
  // Untrack (ongoing/started cards) — the reversal of tracking, via a confirm window. Logs an
  // "untracked" history entry ONLY when ≥1 unit was completed (the anti-noise gate); a casual
  // attach→untrack with no progress leaves no trace. We stamp the progress reached (units done /
  // total) so the history row can say how far the section got before untracking.
  const untrackChapter = (sectionKey, plan) => {
    if (plan && unitsDoneFor(sectionKey) >= 1) {
      recordHistory(sectionKey, {
        file: plan.filename, chapter_number: plan.chapter_number, chapter_title: plan.chapter_title,
        status: "untracked", units_done: unitsDoneFor(sectionKey), total_units: plan.total_units || null,
        ts: Date.now(),
      });
    }
    clearBinding(sectionKey); setUntrackFor(null);
  };
  // Move on from a COMPLETED chapter: one click frees it (card reverts to unstarted grey) and opens
  // the picker to track the next chapter — no confirm, since a finished chapter has no place to lose.
  // A completed chapter always earns its history row (all units done).
  const moveOnFromCompleted = (c, sectionKey, plan) => {
    if (plan) {
      recordHistory(sectionKey, {
        file: plan.filename, chapter_number: plan.chapter_number, chapter_title: plan.chapter_title,
        status: "completed", units_done: plan.total_units || null, total_units: plan.total_units || null,
        ts: Date.now(),
      });
    }
    clearBinding(sectionKey); setAttachFor({ c, sectionKey });
  };

  if (loading) return <div className="spin">Opening plan…</div>;
  if (openPlan) return <LessonView view={openPlan.view} sectionKey={openPlan.sectionKey} onExit={() => setOpenPlan(null)} />;

  // "+" attach-a-lesson picker — a focused MODAL layered over the cards (not a separate screen),
  // scoped to ONE subject·class. Lists chapters already prepared for that subject·grade (tap =
  // attach + open) and offers to prepare a brand-new one. Rendered at the bottom of the main
  // cards view; see attachModal below.
  const attachModal = attachFor ? (() => {
    const { c, sectionKey } = attachFor;
    const gradePlans = plansByKey[`${c.subjectSlug}/${c.gradeSlug}`];
    // Exclude the chapter already bound to this section (e.g. the just-completed one) — she's here
    // to pick a DIFFERENT chapter, so it should not appear in the list.
    const boundFile = currentChapterFile(sectionKey);
    const listPlans = Array.isArray(gradePlans) ? gradePlans.filter((p) => p.filename !== boundFile) : gradePlans;
    return (
      <div className="ap-overlay" onClick={() => setAttachFor(null)}>
        <div className="ap-modal" onClick={(e) => e.stopPropagation()}>
          <button className="ap-close" aria-label="Close" onClick={() => setAttachFor(null)}>✕</button>
          <div className="ap-head">
            <div className="ap-kicker">{pretty(c.subjectSlug)} · Grade {gradeUp(c.grade)} · {c.sectionTag}</div>
            <div className="ap-title">Track a chapter for this section</div>
            <div className="ap-sub">Pick a chapter you&rsquo;ve already prepared to track for this section, or build a new one.</div>
          </div>
          <div className="ap-list">
            {listPlans === undefined ? (
              <div className="ap-loading">Loading lessons…</div>
            ) : listPlans.length === 0 ? (
              <div className="ap-none">No other lessons prepared for this section yet.</div>
            ) : (
              listPlans.map((p) => (
                <button key={p.filename} className="ap-row" onClick={() => attachChapter(c, sectionKey, p)}>
                  <span className="ch-meta">
                    <span className="ch-meta-tx"><b>Ch {pad(p.chapter_number)}</b></span>
                    <span className="ch-go" aria-hidden="true">›</span>
                  </span>
                  <span className="ch-name" title={p.chapter_title}>{p.chapter_title}</span>
                </button>
              ))
            )}
          </div>
          <div className="mlp-allocate">
            <span className="mlp-allocate-q">Need a chapter you don&rsquo;t have yet?</span>
            <button className="mlp-allocate-btn prepare-cta"
              onClick={() => onEnterGenerate && onEnterGenerate({ subject: c.subjectSlug, grade: c.gradeSlug, single: true })}>
              Prepare a new lesson →
            </button>
          </div>
        </div>
      </div>
    );
  })() : null;

  // Untrack confirmation — a deliberate window so she's sure. Reversal of tracking; makes the plan
  // available to track again and clears her place in it.
  const untrackModal = untrackFor ? (() => {
    const { c, sectionKey, plan } = untrackFor;
    const chLabel = `${plan.chapter_number ? `Ch ${plan.chapter_number} — ` : ""}${plan.chapter_title}`;
    return (
      <div className="ap-overlay" onClick={() => setUntrackFor(null)}>
        <div className="ap-modal ap-confirm" onClick={(e) => e.stopPropagation()}>
          <button className="ap-close" aria-label="Close" onClick={() => setUntrackFor(null)}>✕</button>
          <div className="ap-head">
            <div className="ap-kicker">{pretty(c.subjectSlug)} · Grade {gradeUp(c.grade)} · {c.sectionTag}</div>
            <div className="ap-title">Stop tracking this chapter?</div>
            <div className="ap-sub">{c.sectionTag} will stop tracking &ldquo;{chLabel}&rdquo;. It will be available to track again for this section.</div>
          </div>
          <div className="ap-confirm-actions">
            <button className="ap-btn-ghost" onClick={() => setUntrackFor(null)}>Keep tracking</button>
            <button className="ap-btn-danger" onClick={() => untrackChapter(sectionKey, plan)}>Stop tracking</button>
          </div>
        </div>
      </div>
    );
  })() : null;

  // Chapter-history popup — an instant in/out list (a function, not a screen). Shows ONE row per
  // chapter (the log is keyed by file → latest action wins), newest first. The still-bound current
  // chapter is overlaid live as "Ongoing"/"Completed" ONLY when it has progress (≥1 unit), so a
  // freshly-attached, untouched chapter never appears (matches the anti-noise gate).
  const historyModal = historyFor ? (() => {
    const { c, sectionKey } = historyFor;
    const gradePlans = plansByKey[`${c.subjectSlug}/${c.gradeSlug}`];
    const byFile = {};
    readHistory(sectionKey).forEach((h) => { byFile[h.file] = { ...h }; });
    const curFile = currentChapterFile(sectionKey);
    if (curFile) {
      const done = isDone(sectionKey);
      if (done || unitsDoneFor(sectionKey) >= 1) {
        const cp = Array.isArray(gradePlans) ? gradePlans.find((p) => p.filename === curFile) : null;
        const prev = byFile[curFile];
        const total = cp ? (cp.total_units || null) : (prev ? prev.total_units : null);
        byFile[curFile] = {
          file: curFile,
          chapter_number: cp ? cp.chapter_number : (prev ? prev.chapter_number : null),
          chapter_title: cp ? cp.chapter_title : (prev ? prev.chapter_title : ""),
          status: done ? "completed" : "ongoing",
          units_done: done ? total : unitsDoneFor(sectionKey),
          total_units: total,
          ts: Date.now() + 1,   // current action sorts to the top
        };
      }
    }
    const rows = Object.values(byFile).sort((a, b) => (b.ts || 0) - (a.ts || 0));
    return (
      <div className="ap-overlay" onClick={() => setHistoryFor(null)}>
        <div className="ap-modal" onClick={(e) => e.stopPropagation()}>
          <button className="ap-close" aria-label="Close" onClick={() => setHistoryFor(null)}>✕</button>
          <div className="ap-head">
            <div className="ap-kicker">{pretty(c.subjectSlug)} · Grade {gradeUp(c.grade)} · {c.sectionTag}</div>
            <div className="ap-title">Section history</div>
            <div className="ap-sub">Where each chapter stands for this section.</div>
          </div>
          <div className="ap-list">
            {rows.length === 0 ? (
              <div className="ap-none">No chapters taught yet.</div>
            ) : (
              rows.map((r) => {
                const st = normStatus(r.status);
                return (
                <div className="ch-row" key={r.file}>
                  <div className="ch-meta">
                    <span className="ch-meta-tx"><b>Ch {r.chapter_number ? pad(r.chapter_number) : "—"}</b></span>
                    <span className={`ch-pill ch-${st}`}>{HISTORY_LABEL[st] || "Untracked"}</span>
                  </div>
                  <div className="ch-name" title={r.chapter_title}>{r.chapter_title}</div>
                  {r.total_units ? (
                    <div className="sc-rail ch-rail"
                      aria-label={`${r.units_done || 0} of ${r.total_units} learning units completed`}>
                      {Array.from({ length: r.total_units }).map((_, t) => (
                        <span key={t} className={`sc-tick ${t < (r.units_done || 0) ? "done" : (st === "ongoing" && t === r.units_done ? "cur" : "")}`} />
                      ))}
                    </div>
                  ) : null}
                </div>
                );
              })
            )}
          </div>
        </div>
      </div>
    );
  })() : null;

  // Home header: time-of-day greeting (repeat view only — see below).
  const hour = new Date().getHours();
  const greeting = hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";
  const firstName = (user || "").trim();

  // Ready but the teacher has no classes at all (empty profile).
  if (!classes.length) {
    return (
      <div>
        <div className="dash-hd">
          <div>
            <div className="dash-title">{greeting}{firstName ? `, ${firstName}` : ""}!</div>
          </div>
        </div>
        <div className="slotcard slot-empty">
          <div className="slotrail dim" />
          <div className="slotbody">
            <div className="slot-title muted">No classes set up yet</div>
            <div className="slot-meta">Set up your teaching profile from the settings gear above to start planning.</div>
          </div>
        </div>
      </div>
    );
  }

  // Nothing planned yet? The class cards still show — each as "Pick a chapter to begin" —
  // with a welcome CTA banner ABOVE them. Cards are never hidden.
  const anyBound = classes.some((c) => currentChapterFile(`${c.subjectSlug}_${c.gradeSlug}_${c.sectionTag}`));
  // Any lesson already prepared for one of her classes? After first-gen this is TRUE (the lesson
  // was deposited but left unattached), so the welcome nudge points her at the "+" to attach it.
  const anyPlans = Object.values(plansByKey).some((v) => Array.isArray(v) && v.length > 0);

  /* My Classes home: a FLAT list of section cards — no day buckets, no "today", no pace pills.
   * Each card answers one question — "where did I stop with this class?" — via the LU progress
   * rail and a status shade (grey=not started, green=ongoing, gold=completed) carried on a
   * left-edge accent bar. FIRST-TIME view (no chapter bound anywhere) drops the greeting and
   * shows the welcome banner; REPEAT view shows the greeting + "continue where you left off". */
  return (
    <div>
      {anyBound && (
        <div className="dash-hd">
          <div>
            <div className="dash-title">{greeting}{firstName ? `, ${firstName}` : ""}!</div>
            <div className="dash-sub">Continue where you left off with every class.</div>
          </div>
        </div>
      )}

      {!anyBound && (
        <div className="dash-welcome">
          <div className="dash-welcome-text">
            <div className="dash-welcome-title">Your classes are ready</div>
            <div className="dash-welcome-sub">{anyPlans
              ? <>Your lesson is waiting in My Lessons — tap <b>+</b> on a class to start teaching it.</>
              : <>Tap <b>+</b> on a class to prepare its first lesson.</>}</div>
          </div>
        </div>
      )}

      <div className="sc-list">
        {classes.map((c, i) => {
          const sectionKey = `${c.subjectSlug}_${c.gradeSlug}_${c.sectionTag}`;
          const gradePlans = plansByKey[`${c.subjectSlug}/${c.gradeSlug}`];
          const file = currentChapterFile(sectionKey);
          const plan = file && Array.isArray(gradePlans) ? gradePlans.find((p) => p.filename === file) : null;
          const hist = hasHistory(sectionKey);   // any PAST chapters logged → show the history glyph

          // No chapter bound to this class yet → "pick a chapter to begin" (grey / not started).
          // The card is NOT tappable-to-generate anymore; the "+" opens the attach picker instead.
          if (!plan) {
            return (
              <div className="sc-card st-new" key={i}>
                <div className="sc-tag muted">{c.sectionTag}</div>
                <div className="sc-body">
                  <span className="sc-kicker">{pretty(c.subjectSlug)}</span>
                  <div className="sc-title muted">Pick a chapter to begin</div>
                </div>
                <div className="sc-right">
                  <button className="sc-add" aria-label="Attach a lesson to this section"
                    onClick={() => setAttachFor({ c, sectionKey })}>+</button>
                  {hist && (
                    <button className="sc-hist" aria-label="Section history for this section"
                      onClick={() => setHistoryFor({ c, sectionKey })}>{HistoryIcon}</button>
                  )}
                </div>
              </div>
            );
          }

          const lu = pointerFor(sectionKey);          // current LU, 1-based (null = untouched)
          const done = isDone(sectionKey);
          const total = plan.total_units || null;      // LU count from the plans listing
          const ticks = total ? Array.from({ length: total }) : null;
          const status = done ? "st-done" : lu ? "st-going" : "st-new";
          return (
            <div className={`sc-card ${status}`} key={i}
              onClick={() => openLesson(c.subjectSlug, c.gradeSlug, plan, sectionKey)}>
              <div className="sc-tag">{c.sectionTag}</div>
              <div className="sc-body">
                <span className="sc-kicker">{pretty(c.subjectSlug)}{plan.chapter_number ? ` · Ch ${plan.chapter_number}` : ""}</span>
                <div className="sc-title" title={plan.chapter_title}>{plan.chapter_title}</div>
                {ticks && (
                  <div className="sc-rail" aria-label={done ? `${total} learning units, completed` : lu ? `Learning Unit ${lu} of ${total}` : `${total} learning units, not started`}>
                    {ticks.map((_, t) => (
                      <span key={t} className={`sc-tick ${done || (lu && t < lu - 1) ? "done" : lu && t === lu - 1 ? "cur" : ""}`} />
                    ))}
                  </div>
                )}
              </div>
              {/* Right-slot actions. COMPLETED → a "Complete" label + "+"; clicking "+" frees the
                  finished chapter (card reverts to unstarted) and opens the picker for the next one.
                  STILL TRACKING → "−" untrack, the deliberate reversal via a confirm window.
                  stopPropagation so neither opens the lesson. */}
              {done ? (
                <div className="sc-actions sc-actions-col">
                  <span className="sc-status-done">Complete</span>
                  <button className="sc-add" aria-label="Finish with this chapter and track the next"
                    onClick={(e) => { e.stopPropagation(); moveOnFromCompleted(c, sectionKey, plan); }}>+</button>
                  {hist && (
                    <button className="sc-hist" aria-label="Section history for this section"
                      onClick={(e) => { e.stopPropagation(); setHistoryFor({ c, sectionKey }); }}>{HistoryIcon}</button>
                  )}
                </div>
              ) : (
                <div className="sc-right">
                  <button className="sc-remove" aria-label="Stop tracking this chapter"
                    onClick={(e) => { e.stopPropagation(); setUntrackFor({ c, sectionKey, plan }); }}>−</button>
                  {hist && (
                    <button className="sc-hist" aria-label="Section history for this section"
                      onClick={(e) => { e.stopPropagation(); setHistoryFor({ c, sectionKey }); }}>{HistoryIcon}</button>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      <div className="dash-foot">Tap any class to open its lesson. Your place only moves when you tell it to.</div>

      {attachModal}
      {untrackModal}
      {historyModal}
    </div>
  );
}
