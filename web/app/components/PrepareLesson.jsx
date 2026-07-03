"use client";
import { useEffect, useState } from "react";
import { getJSON, pad, pretty, ROMAN } from "../lib/format";
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
 * Flow: pick chapter → set periods (NCF-suggested default, editable) → Generate. Live
 * generation is still deferred (see api/main.py's /generate stub), so "Generate" opens the
 * closest saved plan's view as a preview — the SAME source FirstRun's preview and the old
 * Allocate generate spoke used. A real generated plan will land in the same saved-plans
 * folder later, so this fetch works unchanged once live generation is wired.
 *
 * Props: subject (slug) · grade (slug) · onNavigate — rendered by GenerateTab for a scoped
 * subject·grade (the readiness gate + subject/grade picker live in GenerateTab).
 */

const DEFAULT_PERIODS = 12; // NCF fallback when the norm table has no figure for this subject·stage

// Teachers say "Class 7", not "Grade VII" — ROMAN starts at "iii" → 3.
const classNum = (g) => {
  const idx = ROMAN.indexOf((g || "").toLowerCase());
  return idx >= 0 ? idx + 3 : (g || "").toUpperCase();
};

export default function PrepareLesson({ subject, grade, onNavigate }) {
  const [chapters, setChapters] = useState([]);
  const [chapterNo, setChapterNo] = useState("");          // chapter_number as string
  const [periods, setPeriods] = useState(DEFAULT_PERIODS);
  const [defaultPeriods, setDefaultPeriods] = useState(DEFAULT_PERIODS); // NCF suggestion for the chosen chapter
  const [step, setStep] = useState("chapter");             // "chapter" | "preview"
  const [plans, setPlans] = useState([]);                  // saved plans (preview source)
  const [busy, setBusy] = useState(false);
  const [view, setView] = useState(null);
  const [error, setError] = useState("");
  const [note, setNote] = useState("");

  // Load chapters (+ NCF estimate + effort weight) and saved plans for the scope.
  useEffect(() => {
    setStep("chapter"); setChapterNo(""); setView(null); setError(""); setNote("");
    setChapters([]); setPlans([]);
    getJSON(`/subjects/${subject}/${grade}/chapters`)
      .then((d) => setChapters(d.chapters || [])).catch(() => setChapters([]));
    getJSON(`/plans/${subject}/${grade}`)
      .then((d) => setPlans(d.plans || [])).catch(() => setPlans([]));
  }, [subject, grade]);

  // The NCF-suggested periods for the chosen chapter become the default value (still editable).
  useEffect(() => {
    const c = chapters.find((x) => String(x.chapter_number) === String(chapterNo));
    if (!c) return;
    const rec = c.ncf_estimated_periods != null ? Math.round(c.ncf_estimated_periods) : DEFAULT_PERIODS;
    setDefaultPeriods(rec);
    setPeriods(rec);
  }, [chapterNo, chapters]);

  const chosen = chapters.find((c) => String(c.chapter_number) === String(chapterNo));
  const planFor = (cn) => plans.find((p) => String(p.chapter_number) === String(cn));

  // "Generate Lesson Plan" — live gen deferred, so open the matching saved plan's view as a
  // preview. Falls back to whatever saved plan exists so testing isn't blocked (with an honest
  // stand-in note), mirroring FirstRun's preview substitution.
  const generate = async () => {
    if (!chosen) return;
    setStep("preview"); setBusy(true); setError(""); setNote(""); setView(null);
    try {
      let match = planFor(chapterNo);
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
      <p className="h2">Prepare a lesson — {pretty(subject)} · Class {classNum(grade)}</p>
      <p className="h2-sub">
        Pick one chapter and the periods you plan to spend on it. Aruvi builds the lesson plan and
        its assessment for that chapter — no yearly plan needed.
      </p>

      {!chapters.length ? (
        <div className="empty">No chapter mappings for this subject &amp; grade yet.</div>
      ) : (
        <>
          <RollWheel ariaLabel="Chapter" value={chapterNo} onChange={setChapterNo}
            items={chapters.map((c) => ({ id: String(c.chapter_number), chip: c.chapter_number, label: c.chapter_title }))} />

          <div className="g4-midrow">
            <div className="g4-inrow">
              <span className="steppermini">
                <button type="button" onClick={() => setP((Number(periods) || 0) - 1)} aria-label="fewer periods">–</button>
                <input type="number" min="0" className="v g4-vinput" value={periods}
                  onChange={(e) => setP(parseInt(e.target.value, 10))} aria-label="Periods for this chapter" />
                <button type="button" onClick={() => setP((Number(periods) || 0) + 1)} aria-label="more periods">+</button>
              </span>
              <span className="unitlab">periods</span>
            </div>
          </div>
          {chosen ? (
            <p className="h2-sub">
              {periods === defaultPeriods
                ? "NCF-recommended for this chapter."
                : `NCF suggests ${defaultPeriods} for this chapter.`}
            </p>
          ) : null}

          <div className="savebar">
            <button className="primary prepare-cta" disabled={!chosen} onClick={generate}>Prepare the lesson →</button>
            {!chosen ? <span className="savebar-hint">Pick a chapter to continue.</span> : null}
          </div>
        </>
      )}
    </div>
  );
}
