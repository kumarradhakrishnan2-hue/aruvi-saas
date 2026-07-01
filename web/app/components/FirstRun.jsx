"use client";
import { useEffect, useState } from "react";
import { getJSON, pretty, gradeUp, ROMAN } from "../lib/format";
import ViewModelView from "./ViewModelView";

/* ───────── FirstRun — shell-less Guided First Experience (Phase 1, 2026-07-01) ─────────
 * The mobile-first, progressive-acquisition entry point (CLAUDE.md §0). Until the teacher has
 * generated one lesson and attached it to a section, there is NO app shell — no header, no
 * tabs, no sidebar. She just completes one meaningful task. This component owns that whole
 * pre-activation surface and renders full-screen on its own.
 *
 * Principle: benefit first, data second. We ask ONE subject, ONE grade, ONE chapter — the
 * minimum to generate a first lesson — with NCF defaults (40 min / 12 periods) pre-filled and
 * only revealed for editing if the teacher taps "Want to change?". Each answer quietly becomes
 * part of the profile later; she never feels she is "building a profile."
 *
 * Steps: welcome → subject → grade → chapter (+duration). On "Generate Lesson Plan" we hand the
 * selection up via onComplete(); the generate → preview → section-cards → arrange-week sequence
 * is wired in the next increment. Design: warm-paper system (§4), authored mobile-first.
 *
 * Props:
 *   user        — signed-in id (for the greeting line, optional)
 *   onComplete(selection) — { subject, grade, chapter, durationMin, periods }; advances the flow
 *   onExit()    — optional: back out to sign-in (from the welcome step)
 */

const DEFAULT_DURATION = 40;   // NCF starting point (minutes per class)
const DEFAULT_PERIODS = 12;    // NCF starting point (teaching periods for the chapter)
const DURATION_CHOICES = [30, 35, 40, 45, 50, 55, 60];

export default function FirstRun({ user, onComplete, onExit, onSignOut }) {
  const [step, setStep] = useState("welcome");  // welcome | subject | grade | chapter | preview

  const [subjects, setSubjects] = useState([]);
  const [subject, setSubject] = useState("");   // slug

  const [grades, setGrades] = useState([]);
  const [grade, setGrade] = useState("");       // slug

  const [chapters, setChapters] = useState([]);
  const [chapterNo, setChapterNo] = useState(""); // chapter_number as string

  const [durationMin, setDurationMin] = useState(DEFAULT_DURATION);
  const [periods, setPeriods] = useState(DEFAULT_PERIODS);
  const [customizing, setCustomizing] = useState(false);

  // Preview step — live generation is deferred, so "Generate Lesson Plan" pulls the closest
  // matching SAVED plan for this subject·grade·chapter and renders it through the same
  // ViewModelView used everywhere else. This lets the whole first-run flow be exercised
  // end-to-end on real data ahead of the actual generate → preview wiring.
  const [previewBusy, setPreviewBusy] = useState(false);
  const [previewView, setPreviewView] = useState(null);
  const [previewNote, setPreviewNote] = useState("");
  const [previewError, setPreviewError] = useState("");

  // Load the subject catalogue once (used on the subject step).
  useEffect(() => {
    getJSON("/subjects").then((d) => setSubjects(d.subjects || [])).catch(() => setSubjects([]));
  }, []);

  // Grades for the chosen subject.
  useEffect(() => {
    if (!subject) { setGrades([]); return; }
    getJSON(`/subjects/${subject}/grades`).then((d) => {
      const gs = [...(d.grades || [])].sort((a, b) => ROMAN.indexOf(a) - ROMAN.indexOf(b));
      setGrades(gs);
    }).catch(() => setGrades([]));
  }, [subject]);

  // Chapters for the chosen subject·grade.
  useEffect(() => {
    if (!subject || !grade) { setChapters([]); return; }
    getJSON(`/subjects/${subject}/${grade}/chapters`).then((d) => {
      setChapters(d.chapters || []);
    }).catch(() => setChapters([]));
  }, [subject, grade]);

  // Estimated teaching periods for the chosen chapter — sourced from the NCF period-norms
  // table (data/content/allocation_norms/ncf_period_norms.json), distributed across this
  // grade's chapters by effort index (api's /chapters endpoint does the maths, same allocator
  // Allocate.jsx uses). Falls back to the flat NCF_DEFAULT_PERIODS placeholder only when the
  // norm table has no figure for this subject·stage (e.g. Science·preparatory).
  useEffect(() => {
    const c = chapters.find((x) => String(x.chapter_number) === String(chapterNo));
    if (!c) return;
    setPeriods(c.ncf_estimated_periods != null ? Math.round(c.ncf_estimated_periods) : DEFAULT_PERIODS);
  }, [chapterNo, chapters]);

  const chosenChapter = chapters.find((c) => String(c.chapter_number) === String(chapterNo));

  const selection = () => ({
    subject, grade,
    chapter: chosenChapter,
    durationMin: Number(durationMin) || DEFAULT_DURATION,
    periods: Number(periods) || DEFAULT_PERIODS,
  });

  // "Generate Lesson Plan" — live generation is deferred (see api/main.py's /generate stub),
  // so we serve a SAVED plan as the preview, same pattern Allocate.jsx's G7 spoke already
  // uses. Try the exact chosen chapter first; if this subject·grade has no saved plan for
  // it yet, fall back to whichever saved plan IS available so testing isn't blocked.
  const generate = async () => {
    if (!chosenChapter) return;
    setStep("preview");
    setPreviewBusy(true);
    setPreviewError("");
    setPreviewNote("");
    setPreviewView(null);
    try {
      const plansRes = await getJSON(`/plans/${subject}/${grade}`);
      const plans = plansRes.plans || [];
      let match = plans.find((p) => String(p.chapter_number) === String(chapterNo));
      if (!match && plans.length) {
        match = plans[0];
        setPreviewNote(
          `No saved test plan for Chapter ${chapterNo} yet — showing Chapter ${match.chapter_number} (${match.chapter_title}) as a stand-in preview.`
        );
      }
      if (!match) {
        setPreviewError(`No saved test plans available yet for ${pretty(subject)} · Class ${gradeUp(grade)}.`);
        return;
      }
      const viewRes = await getJSON(`/plans/${subject}/${grade}/${match.filename}/view`);
      setPreviewView(viewRes.view);
    } catch (e) {
      setPreviewError("Couldn't load a saved plan right now. Try again in a moment.");
    } finally {
      setPreviewBusy(false);
    }
  };

  /* ── shared: three-step progress rail (Subject · Grade · Chapter) ── */
  const Progress = ({ active }) => {
    const steps = ["Subject", "Grade", "Chapter"];
    const idx = steps.indexOf(active);
    return (
      <ol className="fr-prog" aria-label="Setup progress">
        {steps.map((label, i) => (
          <li key={label} className={`fr-prog-step ${i < idx ? "done" : ""} ${i === idx ? "current" : ""}`}>
            <span className="fr-prog-dot">{i < idx ? "✓" : i + 1}</span>
            <span className="fr-prog-label">{label}</span>
          </li>
        ))}
      </ol>
    );
  };

  const Brand = () => (
    <div className="fr-brand">
      {user && (
        <div className="fr-user">
          <span className="fr-user-name">{user}</span>
          {onSignOut && <button className="fr-user-logout" onClick={onSignOut}>Log out</button>}
        </div>
      )}
      <span className="brand-row">Aruvi<em>.</em></span>
      <span className="fr-brand-tag">lesson studio</span>
    </div>
  );

  /* ── WELCOME ── */
  if (step === "welcome") {
    return (
      <div className="fr-wrap fr-welcome">
        <Brand />
        <div className="fr-welcome-body">
          <h1 className="fr-welcome-title">Welcome to Aruvi</h1>
          <p className="fr-welcome-sub">
            We help you teach engaging, NCF-aligned lessons while saving you time.
          </p>
          <ul className="fr-pain-list">
            <li><span className="fr-pain-tick">✓</span><span>Lesson plan in minutes, not hours</span></li>
            <li><span className="fr-pain-tick">✓</span><span>NCF / NCERT aligned</span></li>
            <li><span className="fr-pain-tick">✓</span><span>Assessment built in</span></li>
            <li><span className="fr-pain-tick">✓</span><span>Every section's status at one glance</span></li>
          </ul>
          <h2 className="fr-welcome-h2">Let’s get started</h2>
          <p className="fr-welcome-sub">
            Answer three quick questions and Aruvi will create your first lesson plan.
          </p>
        </div>
        <div className="fr-foot">
          <button className="primary fr-cta" onClick={() => setStep("subject")}>Prepare my first lesson →</button>
          <p className="fr-secure">🛡 Your data is private and secure</p>
        </div>
      </div>
    );
  }

  /* ── STEP 1 · SUBJECT ── */
  if (step === "subject") {
    return (
      <div className="fr-wrap">
        <Brand />
        <Progress active="Subject" />
        <div className="fr-step-body">
          <h1 className="fr-q">What would you like to teach?</h1>
          <p className="fr-hint">Let’s start with one subject.</p>
          <div className="fr-list" role="radiogroup" aria-label="Subject">
            {subjects.length === 0 && <div className="fr-loading">Loading subjects…</div>}
            {subjects.map((s) => (
              <button key={s} role="radio" aria-checked={subject === s}
                className={`fr-opt ${subject === s ? "sel" : ""}`}
                onClick={() => setSubject(s)}>
                <span className="fr-opt-chip">{pretty(s).charAt(0)}</span>
                <span className="fr-opt-label">{pretty(s)}</span>
                {subject === s && <span className="fr-opt-tick" aria-hidden="true">✓</span>}
              </button>
            ))}
          </div>
        </div>
        <div className="fr-foot">
          <button className="primary fr-cta" disabled={!subject} onClick={() => setStep("grade")}>Continue</button>
          <button className="fr-link" onClick={() => setStep("welcome")}>← Back</button>
        </div>
      </div>
    );
  }

  /* ── STEP 2 · GRADE ── */
  if (step === "grade") {
    return (
      <div className="fr-wrap">
        <Brand />
        <Progress active="Grade" />
        <div className="fr-step-body">
          <p className="fr-eyebrow">Selected subject</p>
          <p className="fr-eyebrow-val">{pretty(subject)}</p>
          <h1 className="fr-q">Which grade do you want to teach {pretty(subject)} to?</h1>
          <p className="fr-hint">You can add more grades later.</p>
          <div className="fr-list" role="radiogroup" aria-label="Grade">
            {grades.length === 0 && <div className="fr-loading">Loading grades…</div>}
            {grades.map((g) => (
              <button key={g} role="radio" aria-checked={grade === g}
                className={`fr-opt ${grade === g ? "sel" : ""}`}
                onClick={() => setGrade(g)}>
                <span className="fr-opt-label">Class {gradeUp(g)}</span>
                {grade === g && <span className="fr-opt-tick" aria-hidden="true">✓</span>}
              </button>
            ))}
          </div>
        </div>
        <div className="fr-foot">
          <button className="primary fr-cta" disabled={!grade} onClick={() => setStep("chapter")}>Continue</button>
          <button className="fr-link" onClick={() => setStep("subject")}>← Change subject</button>
        </div>
      </div>
    );
  }

  /* ── STEP 4 · PREVIEW (saved-plan stand-in; live generation deferred) ── */
  if (step === "preview") {
    return (
      <div className="fr-wrap">
        <Brand />
        <div className="fr-step-body">
          <p className="fr-crumb">
            <span>Subject <strong>{pretty(subject)}</strong></span>
            <span className="fr-crumb-dot">·</span>
            <span>Grade <strong>Class {gradeUp(grade)}</strong></span>
            <span className="fr-crumb-dot">·</span>
            <span>Chapter <strong>{chosenChapter ? chosenChapter.chapter_number : chapterNo}</strong></span>
          </p>
          {previewBusy && <div className="fr-loading">Building your lesson preview…</div>}
          {!previewBusy && previewError && <div className="empty">{previewError}</div>}
          {!previewBusy && !previewError && (
            <>
              <div className="fr-note">
                <span className="fr-note-kicker">Testing preview</span>
                <span className="fr-note-body">
                  Live generation is coming soon — this is a saved plan standing in so you can try
                  the full flow. {previewNote}
                </span>
              </div>
              {previewView && <ViewModelView view={previewView} />}
            </>
          )}
        </div>
        <div className="fr-foot">
          <button className="primary fr-cta" disabled={previewBusy} onClick={() => onComplete && onComplete(selection())}>
            Continue →
          </button>
          <button className="fr-link" onClick={() => { setStep("chapter"); setPreviewView(null); setPreviewError(""); setPreviewNote(""); }}>
            ← Back to chapter
          </button>
        </div>
      </div>
    );
  }

  /* ── STEP 3 · CHAPTER (+ NCF default duration/periods) ── */
  return (
    <div className="fr-wrap">
      <Brand />
      <Progress active="Chapter" />
      <div className="fr-step-body">
        <p className="fr-crumb">
          <span>Subject <strong>{pretty(subject)}</strong></span>
          <span className="fr-crumb-dot">·</span>
          <span>Grade <strong>Class {gradeUp(grade)}</strong></span>
        </p>
        <h1 className="fr-q">Which chapter do you want to teach?</h1>

        <label className="fr-select-wrap">
          <span className="fr-select-kicker">Chapter</span>
          <select className="fr-select" value={chapterNo} onChange={(e) => setChapterNo(e.target.value)}>
            <option value="">Choose a chapter…</option>
            {chapters.map((c) => (
              <option key={c.chapter_number} value={c.chapter_number}>
                Chapter {c.chapter_number} — {c.chapter_title}
              </option>
            ))}
          </select>
        </label>

        <div className="fr-defaults">
          <div className="fr-default">
            <span className="fr-default-kicker">Class duration <em>(NCF recommended)</em></span>
            <span className="fr-default-val">{durationMin}-minute classes</span>
            {!customizing && <button className="fr-link fr-default-change" onClick={() => setCustomizing(true)}>Change?</button>}
          </div>
          <div className="fr-default">
            <span className="fr-default-kicker">Estimated teaching periods</span>
            <span className="fr-default-val">{periods} periods</span>
            {!customizing && <button className="fr-link fr-default-change" onClick={() => setCustomizing(true)}>Change?</button>}
          </div>

          {customizing && (
            <div className="fr-custom">
              <label className="fr-select-wrap">
                <span className="fr-select-kicker">Class duration</span>
                <select className="fr-select" value={durationMin} onChange={(e) => setDurationMin(Number(e.target.value))}>
                  {DURATION_CHOICES.map((m) => <option key={m} value={m}>{m} minutes</option>)}
                </select>
              </label>
              <label className="fr-select-wrap">
                <span className="fr-select-kicker">Estimated teaching periods</span>
                <input className="fr-num" type="number" min={1} max={60} value={periods}
                  onChange={(e) => setPeriods(e.target.value)} />
              </label>
              <button className="fr-link fr-center" onClick={() => setCustomizing(false)}>Use NCF defaults</button>
            </div>
          )}
        </div>
      </div>
      <div className="fr-foot">
        <button className="primary fr-cta" disabled={!chosenChapter} onClick={generate}>Generate Lesson Plan</button>
        <button className="fr-link" onClick={() => setStep("grade")}>← Change grade</button>
      </div>
    </div>
  );
}
