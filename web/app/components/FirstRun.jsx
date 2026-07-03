"use client";
import { useEffect, useState } from "react";
import { getJSON, pretty, gradeUp, ROMAN } from "../lib/format";
import { pushSectionState } from "../lib/sectionState";
import { RollWheel, PickWheel } from "./wheels";

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
 * ready!" — a FACTS TEASER, not the plan itself, PLUS "teach this lesson" + suggested class;
 * screen 5's section picker is a modal over it; generation is a one-way street, no back button)
 * → creatingCards (reward beat) → DIRECT handoff: page.jsx opens the real workspace shell
 * (two tabs + settings header) and she lands on the My Classes home, where the cards just
 * created ARE the screen. No interstitial in between — an earlier "Go to my classes →"
 * button was removed (2026-07-02): she can't know what "my classes" means before she has
 * ever seen the shell, so naming the destination only added confusion. The handoff also
 * writes each section's current_chapter_* binding so the home cards show the lesson she
 * just attached, not an empty "pick a chapter" state.
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
  // welcome | subject | grade | chapter | preview | creatingCards

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

  // Preview step — live generation is deferred, so "Generate Lesson Plan" pulls the closest
  // matching SAVED plan for this subject·grade·chapter and reads its view model for the teaser
  // facts (periods, assessment items) — see the "preview" step below, not the full document.
  const [previewBusy, setPreviewBusy] = useState(false);
  const [previewView, setPreviewView] = useState(null);
  const [previewNote, setPreviewNote] = useState("");
  const [previewError, setPreviewError] = useState("");
  // Which saved plan the preview actually used — bound to each section at handoff
  // (current_chapter_*), so the My Classes home opens on the lesson she just attached.
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

  // Her single chapter-step duration — the only duration the first run collects.
  const durOptions = [durationMin];

  // Build the CANONICAL readiness payload from everything picked across the whole flow. One
  // subject record, one grade, one section per fan-out choice. grids[] ships all -1 — day
  // schedules are never collected (see the header note).
  const buildActivationPayload = () => {
    const secObjs = sections.map((s) => ({ tag: tagFor(s), sec: s }));
    const grid = sections.map(() => DAYS.map(() => -1));
    const subjectRecord = {
      name: pretty(subject),
      grades: [{
        grade: gradeUp(grade),
        sections: secObjs,
        durations: durOptions,
      }],
      grids: [grid],
      budget: {},
    };
    return { subjects: [subjectRecord] };
  };

  // "Create teaching cards" (screen 4) fires this: hold on a short "Section Cards are being
  // created…" beat (screen "creatingCards") so the moment reads as something being built for
  // her, then hand off DIRECTLY into the shell — no interstitial, no "go to…" button naming a
  // destination she has never seen. The My Classes home she lands on IS the reward payoff:
  // her cards, already showing the lesson she just attached.
  const goCreateCards = () => {
    setStep("creatingCards");
    setTimeout(finishActivation, 1800);
  };

  // Finalize: bind the previewed plan to every fan-out section (current_chapter_* is what the
  // My Classes home reads to show the chapter on each card — without it she'd land on empty
  // "pick a chapter" cards), then hand the canonical readiness payload to onComplete.
  // Persistence itself (POST /readiness) is page.jsx's job, same as the old upfront wizard.
  const finishActivation = () => {
    setActivating(true);
    try {
      if (previewPlanFile) {
        sections.forEach((s) => {
          const secKey = `${subject}_${grade}_${tagFor(s)}`;
          window.localStorage.setItem(`current_chapter_${secKey}`, previewPlanFile);
          pushSectionState(secKey);   // sync the first binding to the server (cross-device)
        });
      }
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
          `No saved test plan for Chapter ${chapterNo} yet — showing Chapter ${match.chapter_number} (${match.chapter_title}) as a stand-in preview.`
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
  const Progress = ({ active }) => {
    const steps = ["Subject", "Class", "Chapter"];
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

              <div className="fr-teaser-card">
                <h2 className="fr-teaser-title">{chosenChapter ? chosenChapter.chapter_title : previewView.lesson_plan.chapter_title}</h2>
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

              <h2 className="fr-teach-heading">Teach this lesson to your class</h2>
              <p className="fr-hint">We'll create one teaching card for each class so each can progress independently.</p>

              <span className="fr-default-kicker">{sections.length > 1 ? "Classes" : "Class"}</span>
              <div className="fr-suggested-class fr-suggested-class-tap" onClick={() => setSectionPickerOpen(true)}>
                <span className={`fr-default-val ${sections.length > 2 ? "fr-default-val-compact" : ""}`}>
                  {sections.length ? sections.map((s) => tagFor(s)).join(", ") : "—"}
                </span>
                <button type="button" className="fr-change-btn fr-change-btn-primary"
                  onClick={(e) => { e.stopPropagation(); setSectionPickerOpen(true); }}>
                  Add/Edit
                </button>
              </div>
            </>
          )}
        </div>
        <div className="fr-foot">
          <button className="primary fr-cta" disabled={previewBusy || !sections.length} onClick={goCreateCards}>
            Create teaching cards →
          </button>
          <p className="fr-secure">You can change this anytime.</p>
        </div>
        {sectionPickerOpen && (
          <SectionPicker letters={SECTION_LETTERS} selected={sections} tagFor={tagFor}
            onDone={(picked) => { setSections(picked); setSectionPickerOpen(false); }}
            onClose={() => setSectionPickerOpen(false)} />
        )}
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
          <RollWheel ariaLabel="Chapter" value={chapterNo} onChange={setChapterNo}
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
