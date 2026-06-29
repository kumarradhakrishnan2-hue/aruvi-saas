"use client";
import { useEffect, useMemo, useState } from "react";
import { getJSON, pad, pretty, gradeUp } from "../lib/format";
import LessonView from "./LessonView";
import SectionProgress from "./SectionProgress";

/* ───────── MyLessonPlans — the technical resource library (2026-06-29) ─────────
 * Mirrors the LESSON VIEWER hierarchy: subject → grade → chapter. This is the teacher's
 * direct view into her made plans as resources — NOT a here-and-now teaching status view
 * (that lives in My Week, which is section/pointer aware). So there is deliberately no
 * section or learning-unit pointer here.
 *
 * Structure:
 *   • Subject pills — only the subjects she actually teaches (from readiness.subjects[]).
 *     Hidden entirely if she teaches just one subject (nothing to choose).
 *   • Grade tabs — the grades she teaches under the chosen subject, as collapsible panels.
 *     If she teaches only ONE grade, its plans show open directly (no collapse chrome).
 *   • Chapter rows — the saved plans for that subject·grade; each opens in LessonView.
 *   • Per-grade "Need a chapter you don't have yet?" → onAllocate(subjectSlug, gradeSlug),
 *     which jumps to Generate with the allocation table pre-scoped to that combo.
 *
 * Data: readiness stores subject as DISPLAY NAME ("Science") and grade as UPPERCASE ROMAN
 * ("VII"); the plans API + the rest of the app use SLUGS ("science", "vii"). We convert at
 * the boundary: subjectSlug = name.toLowerCase().replace(/ /g,"_"); gradeSlug = grade.toLowerCase().
 *
 * Pointer rule (2026-06-29): GRADE-LEVEL READS, SECTION-LEVEL ACTS. Opening a chapter here is
 * PREVIEW ONLY — LessonView gets `preview` so no teaching pointer moves (the library has no
 * section in scope; a pointer here would write a phantom non-section key). Moving a section's
 * pointer happens in My Week. Track's section rows therefore hand off via onOpenSection().
 *
 * Props:
 *   readiness     — page projection carrying .subjects[] (canonical).
 *   onAllocate    — (subjectSlug, gradeSlug) => void; opens Generate allocation for that combo.
 *   onOpenSection — (subjectSlug, gradeSlug, sectionTag, plan) => void; deep-links into My Week
 *                   to open that section's pointer-enabled plan (passed through to Track).
 */

const subjectSlug = (name) => (name || "").toLowerCase().replace(/ /g, "_");
const gradeSlug = (g) => (g || "").toLowerCase();

export default function MyLessonPlans({ readiness, onAllocate, onOpenSection }) {
  const subjects = useMemo(() => (readiness && readiness.subjects) || [], [readiness]);

  // The subject in focus (by display name). Default to the first taught subject.
  const [activeSubject, setActiveSubject] = useState(() => (subjects[0] ? subjects[0].name : ""));
  // Plans keyed `${subjectSlug}/${gradeSlug}` -> array (or undefined while loading).
  const [plansByKey, setPlansByKey] = useState({});
  // Which grade panels are expanded (key = gradeSlug). Single-grade subjects ignore this.
  const [openGrades, setOpenGrades] = useState({});
  // Open plan in the viewer.
  const [openPlan, setOpenPlan] = useState(null);   // { view }
  const [opening, setOpening] = useState(false);
  // Track per-section progress for one chapter: { subjectSlug, gradeSlug, sections[], plan }.
  const [tracking, setTracking] = useState(null);

  // Keep activeSubject valid as the profile changes.
  useEffect(() => {
    if (!subjects.length) return;
    if (!subjects.some((s) => s.name === activeSubject)) setActiveSubject(subjects[0].name);
  }, [subjects, activeSubject]);

  const current = subjects.find((s) => s.name === activeSubject) || subjects[0] || null;
  const grades = useMemo(() => (current && current.grades) || [], [current]);
  const singleGrade = grades.length === 1;

  // Fetch plans for every grade of the active subject (a handful of small calls).
  useEffect(() => {
    if (!current) return;
    const sSlug = subjectSlug(current.name);
    grades.forEach((g) => {
      const gSlug = gradeSlug(g.grade);
      const key = `${sSlug}/${gSlug}`;
      setPlansByKey((prev) => (key in prev ? prev : { ...prev, [key]: undefined }));
      getJSON(`/plans/${sSlug}/${gSlug}`)
        .then((d) => setPlansByKey((prev) => ({ ...prev, [key]: d.plans || [] })))
        .catch(() => setPlansByKey((prev) => ({ ...prev, [key]: [] })));
    });
    // Single-grade subject opens its only grade automatically.
    if (singleGrade && grades[0]) setOpenGrades({ [gradeSlug(grades[0].grade)]: true });
  }, [current, grades, singleGrade]);

  const openLesson = async (sSlug, gSlug, p) => {
    setOpening(true);
    try {
      const view = (await getJSON(`/plans/${sSlug}/${gSlug}/${p.filename}/view`)).view;
      setOpenPlan({ view });
    } finally { setOpening(false); }
  };

  if (opening) return <div className="spin">Opening plan…</div>;
  if (openPlan) return <LessonView view={openPlan.view} onExit={() => setOpenPlan(null)} preview />;
  if (tracking) return (
    <SectionProgress
      subjectSlug={tracking.subjectSlug}
      gradeSlug={tracking.gradeSlug}
      grade={tracking.grade}
      sections={tracking.sections}
      plan={tracking.plan}
      onExit={() => setTracking(null)}
      onOpenSection={onOpenSection}
    />
  );

  if (!current) {
    return <div className="mlp-empty">No subjects set up yet. Finish setup in My Plans to see your lesson plans here.</div>;
  }

  const sSlug = subjectSlug(current.name);

  const renderGradeBody = (g) => {
    const gSlug = gradeSlug(g.grade);
    const key = `${sSlug}/${gSlug}`;
    const plans = plansByKey[key];
    const sections = (g.sections || []).map((s) => s.tag).filter(Boolean);
    return (
      <div className="mlp-gradebody">
        {plans === undefined ? (
          <div className="mlp-loading">Loading plans…</div>
        ) : plans.length === 0 ? (
          <div className="mlp-noplans">No plans for this grade yet.</div>
        ) : (
          plans.map((p) => (
            <div key={p.filename} className="mlp-row">
              <button className="mlp-row-open" onClick={() => openLesson(sSlug, gSlug, p)}>
                <span className="mlp-row-ch">CH {pad(p.chapter_number)}</span>
                <span className="mlp-row-title">{p.chapter_title}</span>
              </button>
              <button className="mlp-row-track"
                onClick={() => setTracking({ subjectSlug: sSlug, gradeSlug: gSlug, grade: g.grade, sections, plan: p })}>
                Track
              </button>
            </div>
          ))
        )}
        <div className="mlp-allocate">
          <span className="mlp-allocate-q">Need a chapter you don&rsquo;t have yet?</span>
          <button className="mlp-allocate-btn" onClick={() => onAllocate && onAllocate(sSlug, gSlug)}>
            Generate · Grade {gradeUp(g.grade)} →
          </button>
        </div>
      </div>
    );
  };

  return (
    <div className="mlp">
      <div className="lvl-head">
        <div>
          <div className="kicker kicker-ochre">My lesson plans</div>
          <h1 className="lvl-title">Your plans, by subject and grade</h1>
          <p className="lvl-sub">Every plan you&rsquo;ve made — open one to read, or build a new one.</p>
        </div>
      </div>

      {subjects.length > 1 && (
        <div className="mlp-subjects">
          <span className="mlp-subjects-lbl">Subject</span>
          {subjects.map((s) => (
            <button key={s.name}
              className={`mlp-subj-pill ${s.name === current.name ? "on" : ""}`}
              onClick={() => setActiveSubject(s.name)}>
              {pretty(subjectSlug(s.name))}
            </button>
          ))}
        </div>
      )}

      {singleGrade ? (
        // One grade → show its plans directly, no collapse chrome.
        <div className="mlp-single">
          <div className="mlp-grade-head plain">
            <span className="mlp-grade-name">Grade {gradeUp(grades[0].grade)}</span>
            <span className="mlp-grade-meta">{pretty(sSlug).toUpperCase()}</span>
          </div>
          {renderGradeBody(grades[0])}
        </div>
      ) : (
        grades.map((g) => {
          const gSlug = gradeSlug(g.grade);
          const key = `${sSlug}/${gSlug}`;
          const plans = plansByKey[key];
          const count = Array.isArray(plans) ? plans.length : null;
          const isOpen = !!openGrades[gSlug];
          return (
            <div className="mlp-panel" key={g.grade}>
              <button className="mlp-grade-head" onClick={() => setOpenGrades((p) => ({ ...p, [gSlug]: !p[gSlug] }))}>
                <span className={`mlp-caret ${isOpen ? "open" : ""}`} aria-hidden="true">›</span>
                <span className="mlp-grade-name">Grade {gradeUp(g.grade)}</span>
                <span className="mlp-grade-meta">{pretty(sSlug).toUpperCase()}{count != null ? ` · ${count} plan${count !== 1 ? "s" : ""}` : ""}</span>
              </button>
              {isOpen && renderGradeBody(g)}
            </div>
          );
        })
      )}
    </div>
  );
}
