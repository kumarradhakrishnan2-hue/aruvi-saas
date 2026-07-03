"use client";
import { useEffect, useMemo, useRef, useState } from "react";
import { getJSON, pad, pretty } from "../lib/format";
import { pullSectionState, readLocalSection } from "../lib/sectionState";
import useSupportedGrades from "../lib/useSupportedGrades";
import LessonView from "./LessonView";
import { RollWheel } from "./wheels";

/* ───────── MyLessonPlans — the lesson library, one class at a time (redesigned 2026-07-03) ─────────
 * A teacher comes here with ONE class in mind ("what's left to prepare for VI Science"), so the
 * tab scopes to a single subject·grade and gives the whole body to that list. It mirrors My
 * Classes structurally: "Your lessons" at the dash-title size, then Subject + Grade as the two
 * first-run RollWheels (only what she teaches), pinned in a frozen header while the lesson list
 * scrolls beneath. Cards reuse the .sc-card sizing so the two tabs read as one family.
 *
 * Card colour = teaching lifecycle, lifted from section to lesson (the basis chosen 2026-07-03):
 *   • sage rail  — no section has taken this chapter yet ("ready to teach", on the shelf)
 *   • green (st-going) — ANY section is mid-chapter on it ("teaching now" wins — it's live)
 *   • clay (st-done)   — every engaged section has finished and none is live
 * The status line is EXHAUSTIVE and single-colour: "Completed 6A, 6C · Teaching now 6B, 6D"
 * (completed first). No per-section drill-down here — that's the section card's job; tapping a
 * card just opens the READ-ONLY lesson plan (PDF attachment later). Per-section state is read
 * from the same server-backed section cache My Classes writes (readLocalSection), so the two
 * tabs always agree.
 *
 * Data: readiness stores subject as DISPLAY NAME ("Science") and grade as UPPERCASE ROMAN ("VI");
 * the plans API uses SLUGS. We convert at the boundary. Section tags are already stored as "6A".
 *
 * Props:
 *   readiness  — page projection carrying .subjects[] (canonical).
 *   onAllocate — (subjectSlug, gradeSlug) => void; opens Generate to prepare a new lesson.
 */

const subjectSlug = (name) => (name || "").toLowerCase().replace(/ /g, "_");
const gradeSlug = (g) => (g || "").toLowerCase();
// The teacher's word is "Class", shown as a plain number — never "Grade", never Roman numerals.
// Readiness still STORES the grade as Roman ("VI"); we convert to the display number only here.
const CLASS_NUM = { iii: 3, iv: 4, v: 5, vi: 6, vii: 7, viii: 8, ix: 9, x: 10 };
const classNum = (g) => CLASS_NUM[(g || "").toLowerCase()] ?? (g || "");

// Persist the chosen Subject + Class so the tab REMEMBERS where she was when she toggles over to
// My Classes and back (she flips between the two to pick chapters — resetting to the first
// subject/class each time is exactly the annoyance to avoid). localStorage → survives the
// unmount/remount on tab switch AND a full refresh.
const LS_SUBJECT = "mylessons_subject";
const LS_CLASS = "mylessons_class";
const lsGet = (k) => { if (typeof window === "undefined") return null; try { return window.localStorage.getItem(k); } catch { return null; } };
const lsSet = (k, v) => { if (typeof window === "undefined") return; try { window.localStorage.setItem(k, v); } catch {} };

export default function MyLessonPlans({ readiness, onAllocate }) {
  const subjects = useMemo(() => (readiness && readiness.subjects) || [], [readiness]);

  // Subject in focus (by display name); class in focus (uppercase Roman). RESTORE the last choice
  // from localStorage (see LS_* above); fall back to the first taught subject/class on first ever
  // visit. A stale saved class is harmless — the RollWheel self-corrects if it isn't offered.
  const [activeSubject, setActiveSubject] = useState(() => {
    const saved = lsGet(LS_SUBJECT);
    if (saved && subjects.some((s) => s.name === saved)) return saved;
    return subjects[0] ? subjects[0].name : "";
  });
  const [activeGrade, setActiveGrade] = useState(() => {
    const saved = lsGet(LS_CLASS);
    if (saved) return saved;
    const g = subjects[0] && subjects[0].grades && subjects[0].grades[0];
    return g ? g.grade : "";
  });
  // Plans keyed `${subjectSlug}/${gradeSlug}` -> array (or undefined while loading).
  const [plansByKey, setPlansByKey] = useState({});
  const [openPlan, setOpenPlan] = useState(null);   // { view }
  const [opening, setOpening] = useState(false);
  const [, setTick] = useState(0);                  // bumped after a section-state sync → re-read

  const current = subjects.find((s) => s.name === activeSubject) || subjects[0] || null;
  const grades = useMemo(() => (current && current.grades) || [], [current]);   // HER taught classes
  // Class is NOT restricted to what she teaches: the wheel offers every class Aruvi has content
  // for in this subject (a superset of hers). Picking a class with no prepared LPs falls through
  // to the empty message + Prepare CTA. Her taught class (if this IS one) still supplies the
  // sections that drive the per-section status; a non-taught class simply has no sections.
  const supportedGrades = useSupportedGrades(activeSubject);   // Roman, ordered; superset of hers
  const taughtGradeObj = grades.find((g) => g.grade === activeGrade) || null;

  const sSlug = current ? subjectSlug(current.name) : "";
  const gSlug = gradeSlug(activeGrade);
  const key = sSlug && gSlug ? `${sSlug}/${gSlug}` : "";
  const plans = key ? plansByKey[key] : undefined;

  // Keep the active subject/grade valid as the profile changes.
  useEffect(() => {
    if (!subjects.length) return;
    if (!subjects.some((s) => s.name === activeSubject)) {
      const s0 = subjects[0];
      const g0 = s0.grades && s0.grades[0] ? s0.grades[0].grade : "";
      setActiveSubject(s0.name); lsSet(LS_SUBJECT, s0.name);
      setActiveGrade(g0); lsSet(LS_CLASS, g0);
    }
  }, [subjects, activeSubject]);

  // Fetch the saved plans for the scoped subject·grade (a single small call per combo, cached).
  useEffect(() => {
    if (!key) return;
    setPlansByKey((prev) => (key in prev ? prev : { ...prev, [key]: undefined }));
    getJSON(`/plans/${sSlug}/${gSlug}`)
      .then((d) => setPlansByKey((prev) => ({ ...prev, [key]: d.plans || [] })))
      .catch(() => setPlansByKey((prev) => ({ ...prev, [key]: [] })));
  }, [key, sSlug, gSlug]);

  // Reconcile this grade's section teaching-state from the server into the localStorage cache so
  // the status lines match what the teacher set on My Classes / another device. Re-syncs on load,
  // on tab focus/visibility, and on a light interval — same pattern as My Classes. Skipped while a
  // plan is open so an in-flight read is never interrupted.
  const busyRef = useRef(false);
  busyRef.current = !!openPlan;
  useEffect(() => {
    const keys = (taughtGradeObj ? taughtGradeObj.sections || [] : [])
      .map((s) => `${sSlug}_${gSlug}_${s.tag}`).filter(Boolean);
    if (!keys.length) return;
    let live = true;
    const sync = () => {
      if (!live || busyRef.current) return;
      pullSectionState(keys).then(() => { if (live) setTick((t) => t + 1); });
    };
    sync();
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
  }, [sSlug, gSlug]);

  const onSubject = (name) => {
    setActiveSubject(name);
    lsSet(LS_SUBJECT, name);
    const s = subjects.find((x) => x.name === name);
    const g = s && s.grades && s.grades[0] ? s.grades[0].grade : "";
    setActiveGrade(g);
    lsSet(LS_CLASS, g);
  };
  const onGrade = (g) => { setActiveGrade(g); lsSet(LS_CLASS, g); };

  const openLesson = async (p) => {
    setOpening(true);
    try {
      const view = (await getJSON(`/plans/${sSlug}/${gSlug}/${p.filename}/view`)).view;
      setOpenPlan({ view });
    } finally { setOpening(false); }
  };

  // Exhaustive per-section state for one chapter: which sections completed it, which are on it now.
  // A section counts only if it's currently tracking THIS chapter (current_chapter === filename).
  const statusFor = (plan) => {
    const completed = [];
    const live = [];
    (taughtGradeObj ? taughtGradeObj.sections || [] : []).forEach((s) => {
      const st = readLocalSection(`${sSlug}_${gSlug}_${s.tag}`);
      if (st.chapter && st.chapter === plan.filename) (st.done ? completed : live).push(s.tag);
    });
    return { completed, live };
  };

  if (opening) return <div className="spin">Opening plan…</div>;
  if (openPlan) return <LessonView view={openPlan.view} onExit={() => setOpenPlan(null)} preview />;

  if (!current) {
    return <div className="mlp-empty">No subjects set up yet. Finish setup in My Classes to see your lessons here.</div>;
  }

  const subjectItems = subjects.map((s) => ({ id: s.name, label: s.name }));
  // Every supported class for this subject (superset of hers) — not just what she teaches.
  const gradeItems = supportedGrades.map((g) => ({ id: g, label: `${classNum(g)}` }));

  const prepareCTA = (
    <div className="mlp-allocate">
      <span className="mlp-allocate-q">Need a chapter you don&rsquo;t have yet?</span>
      <button className="mlp-allocate-btn prepare-cta" onClick={() => onAllocate && onAllocate(sSlug, gSlug)}>
        Prepare a new lesson →
      </button>
    </div>
  );

  return (
    <div className="mlp2">
      <div className="mlp2-frozen">
        <h1 className="mlp2-title">Your lessons</h1>
        <div className="mlp2-wheels">
          <div className="mlp2-wcol">
            <span className="mlp2-wlbl">Subject</span>
            {subjectItems.length > 1 ? (
              <RollWheel items={subjectItems} value={activeSubject} onChange={onSubject} ariaLabel="Subject" large rowPx={48} fit />
            ) : (
              <div className="mlp2-static">{current.name}</div>
            )}
          </div>
          <div className="mlp2-wcol">
            <span className="mlp2-wlbl">Class</span>
            {gradeItems.length > 1 ? (
              <RollWheel items={gradeItems} value={activeGrade} onChange={onGrade} ariaLabel="Class" large rowPx={48} />
            ) : (
              <div className="mlp2-static">Class {classNum(activeGrade)}</div>
            )}
          </div>
        </div>
      </div>

      {plans === undefined ? (
        <div className="mlp-loading">Loading plans…</div>
      ) : plans.length === 0 ? (
        <div className="mlp2-emptybody">
          There are no lesson plans prepared for {pretty(sSlug)} · Class {classNum(activeGrade)} yet.
        </div>
      ) : (
        <div className="sc-list">
          {plans.map((p) => {
            const { completed, live } = statusFor(p);
            const cls = live.length ? "st-going" : completed.length ? "st-done" : "mlp2-shelf";
            return (
              <div className={`sc-card ${cls}`} key={p.filename} onClick={() => openLesson(p)}>
                <div className="sc-tag">{pad(p.chapter_number)}</div>
                <div className="sc-body">
                  <div className="sc-title">{p.chapter_title}</div>
                  {completed.length || live.length ? (
                    <div className="mlp2-status">
                      {completed.length > 0 && <span>Completed {completed.join(", ")}</span>}
                      {completed.length > 0 && live.length > 0 && <span className="sep">·</span>}
                      {live.length > 0 && <span>Teaching now {live.join(", ")}</span>}
                    </div>
                  ) : (
                    <div className="mlp2-ready">Ready to teach</div>
                  )}
                </div>
                <span className="mlp2-open" aria-hidden="true">›</span>
              </div>
            );
          })}
        </div>
      )}

      {prepareCTA}
    </div>
  );
}
