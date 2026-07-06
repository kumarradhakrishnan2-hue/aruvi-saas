"use client";
import { useEffect, useState } from "react";
import { getJSON, markPrepared, pretty, gradeUp, ROMAN } from "../lib/format";
import { pushSectionState } from "../lib/sectionState";
import { RollWheel, PickWheel, PpwCapture, normPpw, ppwMapSum, DEFAULT_PPW } from "./wheels";

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
 * Steps: welcome → subject → grade → chapter (+duration) → preview (screen 4, "Lesson plan
 * ready!" — a FACTS TEASER, not the plan itself) → FULL-PROFILE ACQUISITION (2026-07-05:
 * sections → durations → periods/week per duration → annual budget, for this subject·grade;
 * generation is a one-way street, no back to chapter) → creatingCards (reward beat) → DIRECT
 * handoff: page.jsx opens the real workspace shell (two tabs + settings header) and she lands on
 * the My Classes home. No interstitial — an earlier "Go to my classes →" button was removed
 * (2026-07-02): she can't know what "my classes" means before she has ever seen the shell.
 *
 * UNATTACHED cards (2026-07-05): the handoff deposits the lesson in My Lessons (markPrepared) but
 * does NOT bind it to any section — the home cards land in the "pick a chapter" state, and she
 * taps "+" on a card to attach the waiting lesson. Auto-binding is what used to make the first
 * class look "done" and leave the profile orphaned (see MEMORY.md 2026-07-05).
 *
 * NO DAY SCHEDULE (2026-07-02): the weekly-arrangement step is GONE. Aruvi organizes by the
 * section pointer ("where did I stop?"), not by days — the calendar was a category error
 * against that model (see MEMORY.md 2026-07-02). First run never asks which days she teaches;
 * the canonical payload still carries a grids[] field for shape-compat, but it is always
 * all -1 ("no schedule"). Design: warm-paper system (§4), authored mobile-first.
 *
 * The preview step deliberately does NOT render the full lesson plan (ViewModelView) — a saved
 * plan currently stands in for it, and a REAL generated plan will later live in the exact same
 * saved-plans folder, but either way showing the whole document before she's attached it to a
 * class works against the guided flow. Instead it shows a teaser of common fields (subject,
 * class, chapter title, period count, assessment item count) pulled from that plan's view model.
 *
 * Props:
 *   user        — signed-in id (for the greeting line, optional)
 *   onComplete(payload) — payload = { subjects: [subjectRecord] }, the CANONICAL readiness
 *     shape (same one Readiness.jsx's buildPayload()/onReadyComplete produce) built from
 *     everything the teacher picked: subject, grade, one section-per-fan-out. The grids[]
 *     field ships all -1 (day schedules are never collected). The caller (page.jsx) persists
 *     it via POST /readiness and flips ready — that's the real activation moment, not a flag.
 *   onExit()    — optional: back out to sign-in (from the welcome step)
 */

const DEFAULT_DURATION = 40;   // NCF starting point (minutes per class)
const DEFAULT_PERIODS = 12;    // NCF starting point (teaching periods for the chapter)
// Duration wheel: 20–120 minutes in 5-minute steps. Periods wheel: 1–60 periods, 1 at a time.
const DURATION_CHOICES = Array.from({ length: 21 }, (_, i) => 20 + i * 5); // 20,25,…120
const PERIOD_CHOICES = Array.from({ length: 60 }, (_, i) => i + 1);        // 1,2,…60
// DAYS exists ONLY to shape the all--1 grids[] in the activation payload (readiness shape
// compat) — no day schedule is ever collected or shown. Section letters run the full A–Z
// range so a school with many parallel sections can scroll ("wheel") past the first few and
// pick any of them.
const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const SECTION_LETTERS = Array.from({ length: 26 }, (_, i) => String.fromCharCode(65 + i)); // A…Z
// The four steps of the post-lesson class set-up, shown as a progress rail so she can see the
// whole run and that it ends soon.
const ACQ_STEPS = ["Sections", "Durations", "Periods", "Budget"];

// Annual-budget estimator — mirrors TeachingProfile's (duplicated to keep first run self-contained;
// the 4-method estimator is the same one the Settings profile uses).
const DAYS_IN_WEEK = 6;
const ESTIMATE_WEEKS = 30;
const METHODS = {
  weeks:   { label: "I know my teaching weeks",   unit: "weeks",          step: 1 },
  periods: { label: "I know my period count",     unit: "periods / year", step: 1 },
  days:    { label: "I know my working days",     unit: "working days",   step: 1 },
  auto:    { label: "I’m not sure — estimate it", unit: "",               step: 0 },
};
const METHOD_ORDER = ["weeks", "periods", "days", "auto"];
const defaultValueFor = (method, ppw) =>
  method === "weeks" ? 30 : method === "periods" ? ppw * 30 : method === "days" ? 180 : 0;
const budgetPeriods = (ppw, b) => {
  if (!b) return null;
  if (b.method === "weeks") return ppw * b.value;
  if (b.method === "periods") return b.value;
  if (b.method === "days") return Math.round(ppw * b.value / DAYS_IN_WEEK);
  return b.value ? b.value : ppw * ESTIMATE_WEEKS; // auto: NCF total when resolved, else flat fallback
};

// Teachers say "Class 7", not "Grade VII" — convert the Roman grade slug to its number
// for display (ROMAN starts at "iii" → 3). Falls back to the Roman form if unmapped.
const classNum = (g) => {
  const idx = ROMAN.indexOf(gradeUp(g).toLowerCase());
  return idx >= 0 ? idx + 3 : gradeUp(g);
};

// RollWheel + PickWheel live in wheels.jsx (extracted 2026-07-02) — the SAME selection UI
// is reused by the Settings profile redo, per the one-UI rule.

/* SectionPicker — the multi-select overlay behind "Change section" (screen 5, picking from the
 * full A–Z letter list, opened from the suggested-class Add/Edit button). `allowEmpty` is kept
 * for callers that don't require a minimum of one. */
function SectionPicker({ letters, selected, tagFor, title, allowEmpty, onDone, onClose }) {
  // Every time this picker opens it starts fully unticked — no section pre-checked, even if
  // some were picked last time — so she always makes a fresh, deliberate choice.
  const [picked, setPicked] = useState([]);
  const toggle = (s) => setPicked((a) => (a.includes(s) ? a.filter((x) => x !== s) : [...a, s].sort()));

  return (
    <div className="fr-modal-bg" onClick={(e) => { if (e.currentTarget === e.target) onClose(); }}>
      <div className="fr-modal">
        <h2 className="fr-q">{title || "Select sections"}</h2>
        <p className="fr-hint">
          Choose all the sections you will teach this lesson to.
          {letters.length > 4 ? " Wheel up or down, or use the arrows, for more." : ""}
        </p>
        <PickWheel options={letters} selected={picked} onToggle={toggle} ariaLabel={title || "Select sections"}
          labelFor={(s) => (tagFor ? `Section ${tagFor(s)}` : s)}>
          <button type="button" className="primary fr-cta" disabled={!allowEmpty && picked.length === 0}
            onClick={() => onDone(picked)}>
            Done
          </button>
        </PickWheel>
      </div>
    </div>
  );
}

export default function FirstRun({ user, onComplete, onExit, onSignOut }) {
  const [step, setStep] = useState("welcome");
  // welcome | subject | grade | chapter | preview | acqSections | acqDurations | acqPpw | acqBudget | creatingCards

  const [subjects, setSubjects] = useState([]);
  const [subject, setSubject] = useState("");   // slug

  const [grades, setGrades] = useState([]);
  const [grade, setGrade] = useState("");       // slug

  const [chapters, setChapters] = useState([]);
  const [chapterNo, setChapterNo] = useState(""); // chapter_number as string

  const [durationMin, setDurationMin] = useState(DEFAULT_DURATION);
  const [periods, setPeriods] = useState(DEFAULT_PERIODS);
  // Estimated periods' recommendation is chapter-specific (NCF period-norms × effort index),
  // so it's tracked separately from the live `periods` value — the "NCF recommended" tag
  // compares the CURRENT value against this, live, on every wheel move: land back on the
  // recommended number and the tag reappears, move off it and the tag drops. Duration's
  // recommendation is the flat DEFAULT_DURATION constant, so no extra state is needed there.
  const [defaultPeriods, setDefaultPeriods] = useState(DEFAULT_PERIODS);
  // Both fields sit grey/read-only showing their default until "Change" is pressed, which
  // opens that field's wheel picker (the other field's wheel, if open, closes — only one
  // edit box open at a time).
  const [editingField, setEditingField] = useState(null); // null | "duration" | "periods"

  // Section fan-out. `sections` is the letters she's teaching this lesson to (default one,
  // "A", matching the mockup's default "VI A" before she changes it).
  const [sections, setSections] = useState(["A"]);
  const [sectionPickerOpen, setSectionPickerOpen] = useState(false);
  const [activating, setActivating] = useState(false);      // busy state for the final handoff

  // FULL-PROFILE acquisition (2026-07-05) — after the lesson is generated, first run now collects
  // the whole teaching profile for this subject·grade (sections → durations → periods/week per
  // duration → annual budget) instead of just naming a section. This is the ONE moment she's
  // motivated (desperate to see the lesson), so we acquire everything now rather than leave the
  // first class profile-orphaned. Cards then land UNATTACHED and she taps "+" to attach the lesson.
  const [durations, setDurations] = useState([DEFAULT_DURATION]);       // acquisition durations (multi)
  const [ppwByDur, setPpwByDur] = useState({ [DEFAULT_DURATION]: DEFAULT_PPW }); // { [minutes]: count }
  const [budget, setBudget] = useState(null);                           // { method, value }
  const [ncfTotal, setNcfTotal] = useState(null);                       // NCF annual periods for the budget "estimate"

  // Preview step — live generation is deferred, so "Generate Lesson Plan" pulls the closest
  // matching SAVED plan for this subject·grade·chapter and reads its view model for the teaser
  // facts (periods, assessment items) — see the "preview" step below, not the full document.
  const [previewBusy, setPreviewBusy] = useState(false);
  const [previewView, setPreviewView] = useState(null);
  const [previewNote, setPreviewNote] = useState("");
  const [previewError, setPreviewError] = useState("");
  // Which saved plan the preview used — deposited in My Lessons at handoff (markPrepared), but
  // NOT bound to any section; she attaches it herself via "+" on a card.
  const [previewPlanFile, setPreviewPlanFile] = useState(null);

  // Load the subject catalogue once (used on the subject step).
  useEffect(() => {
    getJSON("/subjects").then((d) => setSubjects(d.subjects || [])).catch(() => setSubjects([]));
  }, []);

  // Stepping away from the chapter step and back (← Change class, ← Back to chapter, etc.)
  // should never re-open a duration/periods wheel the teacher left open — every fresh arrival
  // on the chapter step starts with both boxes closed.
  useEffect(() => {
    if (step === "chapter") setEditingField(null);
  }, [step]);

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
    const rec = c.ncf_estimated_periods != null ? Math.round(c.ncf_estimated_periods) : DEFAULT_PERIODS;
    setDefaultPeriods(rec);
    setPeriods(rec);
    setEditingField((f) => (f === "periods" ? null : f)); // close a stale edit box, if open
  }, [chapterNo, chapters]);

  const chosenChapter = chapters.find((c) => String(c.chapter_number) === String(chapterNo));

  // Section tag matches the app-wide convention (MyClasses.jsx / Readiness.jsx): arabic grade
  // number + letter, e.g. "6A" — displayed everywhere else as "Section 6A".
  const tagFor = (letter) => `${classNum(grade)}${letter}`;

  // ── acquisition handlers ──
  const startAcquisition = () => {
    setDurations([durationMin]);                 // seed durations from the chapter-step choice
    setPpwByDur({ [durationMin]: DEFAULT_PPW });
    setBudget(null);
    setStep("acqSections");
  };
  const toggleSection = (s) =>
    setSections((a) => (a.includes(s) ? a.filter((x) => x !== s) : [...a, s].sort()));
  const toggleDuration = (d) =>
    setDurations((a) => (a.includes(d)
      ? (a.length > 1 ? a.filter((x) => x !== d) : a)   // keep at least one
      : [...a, d].sort((x, y) => x - y)));
  const goDurToPpw = () => {
    const next = normPpw(durations, ppwByDur, DEFAULT_PPW);  // reconcile counts to current durations
    setPpwByDur(next);
    setStep("acqPpw");
  };
  const setPpwCount = (d, v) => setPpwByDur((m) => {
    const base = normPpw(durations, m, DEFAULT_PPW);
    return { ...base, [d]: Math.max(1, Number(v) || 1) };
  });

  // NCF annual-periods figure for the budget "estimate" method (only while that screen shows).
  useEffect(() => {
    if (step !== "acqBudget" || !subject || !grade) return;
    let live = true;
    setNcfTotal(null);
    getJSON(`/subjects/${subject}/${grade}/ncf-periods`)
      .then((d) => { if (live) setNcfTotal(d && d.ncf_total_periods != null ? d.ncf_total_periods : null); })
      .catch(() => { if (live) setNcfTotal(null); });
    return () => { live = false; };
  }, [step, subject, grade]);

  // Build the CANONICAL readiness payload — the FULL profile for this one subject·grade: every
  // chosen section, the durations, the per-duration weekly counts (+ derived periods_per_week),
  // and the annual budget keyed by grade index 0. grids[] ships all -1 (no day schedule, ever).
  const buildActivationPayload = () => {
    const secObjs = sections.map((s) => ({ tag: tagFor(s), sec: s }));
    const grid = sections.map(() => DAYS.map(() => -1));
    const ppwMap = normPpw(durations, ppwByDur, DEFAULT_PPW);
    const subjectRecord = {
      name: pretty(subject),
      grades: [{
        grade: gradeUp(grade),
        sections: secObjs,
        durations: [...durations],
        ppw_by_duration: ppwMap,
        periods_per_week: ppwMapSum(ppwMap),
      }],
      grids: [grid],
      budget: { 0: budget || { method: "auto", value: 0 } },
    };
    return { subjects: [subjectRecord] };
  };

  // "Create teaching cards" (screen 4) fires this: hold on a short "Section Cards are being
  // created…" beat (screen "creatingCards") so the moment reads as something being built for
  // her, then hand off DIRECTLY into the shell — no interstitial, no "go to…" button naming a
  // destination she has never seen. The My Classes home she lands on IS the reward payoff:
  // her section cards (unattached), ready for her to tap "+" and attach the waiting lesson.
  const goCreateCards = () => {
    setStep("creatingCards");
    setTimeout(finishActivation, 1800);
  };

  // Finalize: deposit the previewed plan in My Lessons (NOT bound to any section) and hand the
  // full-profile canonical readiness payload to onComplete. Persistence (POST /readiness) is
  // page.jsx's job, same as the old upfront wizard.
  const finishActivation = () => {
    setActivating(true);
    try {
      if (previewPlanFile) {
        // Deposit the lesson in My Lessons — but DELIBERATELY do not bind it to any section.
        // Cards land UNATTACHED so she taps "+" on a card to attach the waiting lesson. Binding it
        // here is what used to make the first class look "done" and leave the profile orphaned.
        markPrepared(subject, grade, previewPlanFile);
      }
      // Guarantee every card lands UNATTACHED: clear any stale binding for these exact section
      // keys, both locally AND on the server. A reused section key (e.g. english_iii_3A left over
      // from an earlier run) otherwise resurrects its old chapter via pullSectionState, so a
      // "fresh" card shows already attached. First run only runs for an empty profile, so a clear
      // here is always safe.
      sections.forEach((s) => {
        const secKey = `${subject}_${grade}_${tagFor(s)}`;
        try {
          window.localStorage.removeItem(`current_chapter_${secKey}`);
          window.localStorage.removeItem(`lu_pointer_${secKey}`);
          window.localStorage.removeItem(`lu_done_${secKey}`);
        } catch {}
        pushSectionState(secKey);   // no chapter in localStorage now → deletes the server row
      });
    } catch {}
    onComplete && onComplete(buildActivationPayload());
  };

  // "Generate Lesson Plan" — live generation is deferred (see api/main.py's /generate stub),
  // so we pull a SAVED plan's real facts (periods, assessment item count) for the teaser
  // summary, same pattern Allocate.jsx's G7 spoke uses to serve saved-plan previews. We no
  // longer render the plan itself here — see screen 4a "preview" below: showing the full
  // document before she's attached it to a class got in the way of the guided flow, and a
  // REAL generated plan will live in this same saved-plans folder later, so this fetch already
  // works unchanged once live generation lands. Try the exact chosen chapter first; if this
  // subject·grade has no saved plan for it yet, fall back to whichever saved plan IS available
  // so testing isn't blocked (the disclosure note below stays honest about that substitution).
  const generate = async () => {
    if (!chosenChapter) return;
    setStep("preview");
    setPreviewBusy(true);
    setPreviewError("");
    setPreviewNote("");
    setPreviewView(null);
    setPreviewPlanFile(null);
    try {
      const plansRes = await getJSON(`/plans/${subject}/${grade}`);
      const plans = plansRes.plans || [];
      let match = plans.find((p) => String(p.chapter_number) === String(chapterNo));
      if (!match && plans.length) {
        match = plans[0];
        setPreviewNote(
          `Live generation isn’t on yet, and there’s no saved test plan for Chapter ${chapterNo} — so Chapter ${match.chapter_number} (“${match.chapter_title}”) is standing in. This stand-in is the lesson that lands in My Lessons.`
        );
      }
      if (!match) {
        setPreviewError(`No saved test plans available yet for ${pretty(subject)} · Class ${classNum(grade)}.`);
        return;
      }
      const viewRes = await getJSON(`/plans/${subject}/${grade}/${match.filename}/view`);
      setPreviewView(viewRes.view);
      setPreviewPlanFile(match.filename);
    } catch (e) {
      setPreviewError("Couldn't load a saved plan right now. Try again in a moment.");
    } finally {
      setPreviewBusy(false);
    }
  };

  /* ── shared: three-step progress rail (Subject · Grade · Chapter) ── */
  const Progress = ({ active, steps = ["Subject", "Class", "Chapter"] }) => {
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
          <button className="primary fr-cta prepare-cta" onClick={() => setStep("subject")}>Prepare my first lesson →</button>
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
          <h1 className="fr-q">What do you teach?</h1>
          <p className="fr-hint">Let’s start with one subject. Roll the box or use the arrows — the subject shown is your pick.</p>
          {subjects.length === 0 && <div className="fr-loading">Loading subjects…</div>}
          {subjects.length > 0 && (
            <RollWheel ariaLabel="Subject" value={subject} onChange={setSubject} large
              items={subjects.map((s) => ({ id: s, chip: pretty(s).charAt(0), label: pretty(s) }))} />
          )}
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
        <Progress active="Class" />
        <div className="fr-step-body">
          <h1 className="fr-q">Which class do you teach {pretty(subject)} to?</h1>
          <p className="fr-hint">You can add more classes later. Roll the box or use the arrows — the class shown is your pick.</p>
          {grades.length === 0 && <div className="fr-loading">Loading classes…</div>}
          {grades.length > 0 && (
            <RollWheel ariaLabel="Class" value={grade} onChange={setGrade} large
              items={grades.map((g) => ({ id: g, chip: classNum(g), label: `Class ${classNum(g)}` }))} />
          )}
        </div>
        <div className="fr-foot">
          <button className="primary fr-cta" disabled={!grade} onClick={() => setStep("chapter")}>Continue</button>
          <button className="fr-link" onClick={() => setStep("subject")}>← Change subject</button>
        </div>
      </div>
    );
  }

  /* ── STEP 4 · LESSON PLAN READY — facts teaser + "teach this lesson" + suggested class, all
   * one screen (mockup: "Lesson generated" screen 1). Generation is a one-way street from here
   * — no back-to-chapter escape hatch; the only way forward is "Create teaching cards". Screen
   * 5's section picker is the modal at the bottom, opened from the suggested-class Add/Edit. ── */
  if (step === "preview") {
    const assessmentCount = previewView
      ? (previewView.assessment?.groups || []).reduce((sum, g) => sum + (g.items ? g.items.length : 0), 0)
      : null;
    return (
      <div className="fr-wrap">
        <Brand />
        <div className="fr-step-body">
          {previewBusy && <div className="fr-loading">Building your lesson plan…</div>}
          {!previewBusy && previewError && <div className="empty">{previewError}</div>}
          {!previewBusy && !previewError && previewView && (
            <>
              <div className="fr-plan-ready">
                <div className="fr-plan-ready-head">
                  <span className="fr-plan-ready-check" aria-hidden="true">✓</span>
                  <h1 className="fr-plan-ready-title">Lesson plan ready!</h1>
                </div>
                <p className="fr-plan-ready-sub">Your lesson has been generated successfully.</p>
              </div>

              {/* UNMISSABLE stand-in disclosure (founder's call 2026-07-06): when the chosen
                  chapter has no saved test plan, the substitution must be said out loud HERE —
                  the note used to be set but never rendered on this teaser, while the card
                  showed the CHOSEN chapter's title over the stand-in's numbers ("I picked
                  chapter 5 but the system shows 9"). The teaser now always names the plan
                  actually being deposited. */}
              {previewNote && <div className="fr-standin" role="note">{previewNote}</div>}

              <div className="fr-teaser-card">
                <h2 className="fr-teaser-title">{previewNote ? previewView.lesson_plan.chapter_title : (chosenChapter ? chosenChapter.chapter_title : previewView.lesson_plan.chapter_title)}</h2>
                <p className="fr-teaser-sub">{pretty(subject)} · Class {classNum(grade)}</p>
                <div className="fr-teaser-stats">
                  <div className="fr-teaser-stat">
                    <span className="fr-teaser-stat-num">{previewView.lesson_plan.total_periods}</span>
                    <span className="fr-teaser-stat-label">periods</span>
                  </div>
                  <div className="fr-teaser-stat">
                    <span className="fr-teaser-stat-num">{assessmentCount}</span>
                    <span className="fr-teaser-stat-label">assessment items</span>
                  </div>
                </div>
              </div>

              <p className="fr-hint">Your lesson plan needs a home. Help us set up your class to receive the plan.</p>
              <h2 className="fr-teach-heading">Now let’s set up your class</h2>
            </>
          )}
        </div>
        <div className="fr-foot">
          <button className="primary fr-cta" disabled={previewBusy || !previewView} onClick={startAcquisition}>
            Set up my class →
          </button>
          <p className="fr-secure">Your lesson is safe in My Lessons.</p>
        </div>
      </div>
    );
  }

  /* ── PROFILE ACQUISITION (after the lesson is ready) — sections → durations → periods/week →
   * annual budget, for this one subject·grade. Reuses the shared wheels + PpwCapture. On finish,
   * cards are created UNATTACHED and the lesson waits in My Lessons for her to tap "+". ── */
  if (step === "acqSections") {
    return (
      <div className="fr-wrap">
        <Brand />
        <Progress steps={ACQ_STEPS} active="Sections" />
        <div className="fr-step-body">
          <h1 className="fr-q">Which sections of Class {classNum(grade)} do you teach {pretty(subject)} to?</h1>
          <p className="fr-hint">Each section gets its own class card. Pick all the sections you teach.</p>
          <PickWheel options={SECTION_LETTERS} selected={sections} onToggle={toggleSection}
            ariaLabel="Sections" labelFor={(s) => `Section ${tagFor(s)}`}>
            <button type="button" className="primary fr-cta" disabled={!sections.length}
              onClick={() => setStep("acqDurations")}>Continue</button>
          </PickWheel>
        </div>
        <div className="fr-foot">
          <button className="fr-link" onClick={() => setStep("preview")}>← Back</button>
        </div>
      </div>
    );
  }

  if (step === "acqDurations") {
    return (
      <div className="fr-wrap">
        <Brand />
        <Progress steps={ACQ_STEPS} active="Durations" />
        <div className="fr-step-body">
          <h1 className="fr-q">How long are your {pretty(subject)} periods for Class {classNum(grade)}?</h1>
          <p className="fr-hint">Most classes are one length. Add another only if some run longer.</p>
          <PickWheel options={DURATION_CHOICES} selected={durations} onToggle={toggleDuration}
            ariaLabel="Period durations" labelFor={(d) => `${d} min`} initialScrollTo={durationMin}>
            <button type="button" className="primary fr-cta" disabled={!durations.length}
              onClick={goDurToPpw}>Continue</button>
          </PickWheel>
        </div>
        <div className="fr-foot">
          <button className="fr-link" onClick={() => setStep("acqSections")}>← Back</button>
        </div>
      </div>
    );
  }

  if (step === "acqPpw") {
    const map = normPpw(durations, ppwByDur, DEFAULT_PPW);
    const multi = durations.length > 1;
    return (
      <div className="fr-wrap">
        <Brand />
        <Progress steps={ACQ_STEPS} active="Periods" />
        <div className="fr-step-body">
          <h1 className="fr-q">{multi
            ? `How many periods a week does Class ${classNum(grade)} get for ${pretty(subject)} for each duration?`
            : `How many periods a week does Class ${classNum(grade)} get for ${pretty(subject)}?`}</h1>
          <p className="fr-hint">{multi
            ? "This would help us suggest NCF aligned periods needed for a chapter and implement a lesson plan that mirrors your period structure."
            : "This would help us suggest NCF aligned periods needed for a chapter."}</p>
          <PpwCapture durations={durations} map={map} onSet={setPpwCount} />
        </div>
        <div className="fr-foot">
          <button type="button" className="primary fr-cta" onClick={() => setStep("acqBudget")}>Continue</button>
          <button className="fr-link" onClick={() => setStep("acqDurations")}>← Back</button>
        </div>
      </div>
    );
  }

  if (step === "acqBudget") {
    const ppw = ppwMapSum(normPpw(durations, ppwByDur, DEFAULT_PPW));
    const picked = !!budget;                                   // no method selected until she taps one
    const bSel = budget && budget.method === "auto"
      ? { method: "auto", value: ppw * ESTIMATE_WEEKS } : budget;
    const setMethod = (m) => setBudget({ method: m, value: defaultValueFor(m, ppw) });
    const stepValue = (delta) => setBudget({ ...bSel, value: Math.max(0, bSel.value + delta) });
    const setValue = (v) => setBudget({ ...bSel, value: Math.max(0, v) });
    return (
      <div className="fr-wrap">
        <Brand />
        <Progress steps={ACQ_STEPS} active="Budget" />
        <div className="fr-step-body">
          <h1 className="fr-q">How long is your teaching year for Class {classNum(grade)}?</h1>
          <p className="fr-hint">Pick one method below based on what you know.</p>
          {/* Each method carries its OWN result below it, so tapping a choice shows the period
              number right where she chose — and once she's picked, the other methods dim to keep
              her focused on the one she selected. */}
          <div className="tp-methods">
            {METHOD_ORDER.map((m) => {
              const on = picked && budget.method === m;
              const dim = picked && !on;
              return (
                <div key={m} className="fr-bud-row">
                  <button type="button" className={`tp-method ${on ? "on" : ""} ${dim ? "fr-dim" : ""}`}
                    onClick={() => setMethod(m)}>
                    {METHODS[m].label}
                  </button>
                  {on && (
                    <div className="fr-bud-detail">
                      {m !== "auto" && (
                        <div className="tp-val-row">
                          <button type="button" className="tp-val-btn" onClick={() => stepValue(-METHODS[m].step)} aria-label="Less">−</button>
                          <input type="number" className="tp-val-input" min="0" value={bSel.value}
                            onChange={(e) => setValue(parseInt(e.target.value, 10) || 0)} aria-label={METHODS[m].unit} />
                          <button type="button" className="tp-val-btn" onClick={() => stepValue(METHODS[m].step)} aria-label="More">+</button>
                          <span className="tp-val-unit">{METHODS[m].unit}</span>
                        </div>
                      )}
                      <p className="tp-total">≈ {budgetPeriods(ppw, bSel)} periods for the year, at {ppw} a week</p>
                      {m === "auto" && (
                        <p className="tp-estimate-sub">{ncfTotal != null
                          ? `(based on a 30-week year. Please note however that as per NCF, this class requires ${ncfTotal} periods.)`
                          : "(based on a 30-week year.)"}</p>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
        <div className="fr-foot">
          <button type="button" className="primary fr-cta" disabled={!picked} onClick={goCreateCards}>
            Set up my class ✓
          </button>
          <button className="fr-link" onClick={() => setStep("acqPpw")}>← Back</button>
        </div>
      </div>
    );
  }

  /* ── STEP · CREATING CARDS — the reward beat, then a DIRECT handoff into the shell.
   * The My Classes home she lands on shows the cards themselves (with the lesson bound),
   * so no interstitial screen re-describes them or asks her to "go" anywhere. ── */
  if (step === "creatingCards") {
    return (
      <div className="fr-wrap fr-celebrate">
        <Brand />
        <div className="fr-celebrate-body">
          <span className="fr-celebrate-spin" aria-hidden="true" />
          <h1 className="fr-celebrate-title">{activating ? "Setting up your classes…" : "Section Cards are being created…"}</h1>
          <p className="fr-hint">Just a moment while Aruvi sets up your class.</p>
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
        <h1 className="fr-q">Choose the chapter to teach</h1>
        <p className="fr-hint">Roll the box or use arrows to pick one chapter.</p>

        {chapters.length === 0 && <div className="fr-loading">Loading chapters…</div>}
        {chapters.length > 0 && (
          <RollWheel ariaLabel="Chapter" value={chapterNo} onChange={setChapterNo} rowPx={92}
            items={chapters.map((c) => ({ id: String(c.chapter_number), chip: c.chapter_number, label: c.chapter_title }))} />
        )}

        <div className="fr-defaults">
          <div className={`fr-default ${editingField === "duration" ? "fr-default-editing" : ""}`}>
            <span className="fr-default-kicker-row">
              <span className="fr-default-kicker">Class duration</span>
              {durationMin === DEFAULT_DURATION && <span className="fr-tag-recommended">NCF recommended</span>}
            </span>
            {editingField !== "duration" ? (
              <div className="fr-default-row">
                <span className="fr-default-val fr-default-val-muted">{durationMin}-minute classes</span>
                <button type="button" className="fr-change-btn" onClick={() => setEditingField("duration")}>
                  Change
                </button>
              </div>
            ) : (
              <div className="fr-default-wheel-wrap">
                <RollWheel ariaLabel="Class duration" value={String(durationMin)}
                  onChange={(v) => setDurationMin(Number(v))}
                  items={DURATION_CHOICES.map((m) => ({ id: String(m), chip: m, label: "minute classes" }))} />
                {/* Interim (2026-07-05): first run collects a SINGLE duration on purpose — the
                    mixed-duration case (per-week count per type → count-multiset at generation)
                    lands later in gradual profile acquisition, not here (avoids a schema change +
                    keeps first run benefit-first). This note just reassures her the mix isn't lost. */}
                <p className="fr-hint fr-dur-note">
                  Some classes run longer than others. Let’s keep to one duration for now — you can add more later.
                </p>
                <button type="button" className="fr-done-btn" onClick={() => setEditingField(null)}>Done</button>
              </div>
            )}
          </div>
          <div className={`fr-default ${editingField === "periods" ? "fr-default-editing" : ""}`}>
            <span className="fr-default-kicker-row">
              <span className="fr-default-kicker">Estimated periods</span>
              {periods === defaultPeriods && <span className="fr-tag-recommended">NCF recommended</span>}
            </span>
            {editingField !== "periods" ? (
              <div className="fr-default-row">
                <span className="fr-default-val fr-default-val-muted">{periods} periods</span>
                <button type="button" className="fr-change-btn" onClick={() => setEditingField("periods")}>
                  Change
                </button>
              </div>
            ) : (
              <div className="fr-default-wheel-wrap">
                <RollWheel ariaLabel="Estimated periods" value={String(periods)}
                  onChange={(v) => setPeriods(Number(v))}
                  items={PERIOD_CHOICES.map((p) => ({ id: String(p), chip: p, label: p === 1 ? "period" : "periods" }))} />
                <button type="button" className="fr-done-btn" onClick={() => setEditingField(null)}>Done</button>
              </div>
            )}
          </div>
        </div>
      </div>
      <div className="fr-foot">
        <button className="primary fr-cta prepare-cta" disabled={!chosenChapter} onClick={generate}>Prepare the lesson →</button>
        <button className="fr-link" onClick={() => setStep("grade")}>← Change class</button>
      </div>
    </div>
  );
}
