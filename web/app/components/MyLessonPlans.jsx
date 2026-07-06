"use client";
import { useEffect, useMemo, useRef, useState } from "react";
import { API, getJSON, pad, pretty, withUser } from "../lib/format";
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

/* Line-icons, currentColor stroke so they inherit the warm-paper palette. */
const ArchiveIcon = ({ size = 18 }) => (
  <svg viewBox="0 0 24 24" width={size} height={size} fill="none" stroke="currentColor"
       strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <rect x="3" y="4" width="18" height="4" rx="1" />
    <path d="M5 8v11a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8" />
    <path d="M10 12h4" />
  </svg>
);
// The SAME archive box, but OPEN — the lid swung a full 90° UP so it stands vertical, hinged at
// the box's back corner. Shown when you're inside the archive so the icon reads as "the box is
// open, you're in it"; tapping it closes it back to your lessons.
const OpenArchiveIcon = ({ size = 18 }) => (
  <svg viewBox="0 0 24 24" width={size} height={size} fill="none" stroke="currentColor"
       strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <rect x="6.4" y="12" width="12.2" height="8" rx="1.4" />
    <rect x="3.4" y="2.6" width="3.2" height="9.4" rx="1" />
    <path d="M10.8 16h4" />
  </svg>
);

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
  // Active vs Archived view over the SAME list. Archive is a per-tenant FLAG the server sets
  // (plan.archived); there is no hard delete. "active" is the default — a teacher lives here.
  const [view, setView] = useState("active");
  const [toast, setToast] = useState(null);         // { kind:"ok"|"block", text } | null

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

  // A plan is "attached" if any section is currently teaching or has completed it — the same
  // signal that colours the card. Attached plans are BLOCKED from archiving (the teacher would
  // lose the class's pointer/context), so archive is only ever offered on detached plans.
  const isAttached = (plan) => {
    const { completed, live } = statusFor(plan);
    return completed.length > 0 || live.length > 0;
  };

  // Flip a plan's archived flag in local state (optimistic) so it moves between the two views
  // instantly, before the server round-trip resolves.
  const setArchivedFlag = (filename, val) => {
    setPlansByKey((prev) => {
      const arr = prev[key];
      if (!Array.isArray(arr)) return prev;
      return {
        ...prev,
        [key]: arr.map((p) =>
          p.filename === filename
            ? { ...p, archived: val, archived_at: val ? new Date().toISOString() : null }
            : p),
      };
    });
  };

  const body = (p) => ({ subject: sSlug, grade: gSlug, filename: p.filename });

  const archivePlan = (p, e) => {
    if (e) e.stopPropagation();
    // Safety only — the archive icon is never rendered for an attached plan, so this can't be
    // reached from the UI. No warning path: attachment simply removes the affordance.
    if (isAttached(p)) return;
    setArchivedFlag(p.filename, true);
    setToast({ kind: "ok", text: "Moved to Archive — find it in the box above." });
    fetch(`${API}/plan-archive`, withUser({
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body(p)),
    })).then((r) => { if (!r.ok) throw new Error(); }).catch(() => {
      setArchivedFlag(p.filename, false);   // revert the optimistic move
      setToast({ kind: "block", text: "Couldn't archive just now — please try again." });
    });
  };

  const restorePlan = (p, e) => {
    if (e) e.stopPropagation();
    setArchivedFlag(p.filename, false);
    setToast({ kind: "ok", text: "Restored to your lessons." });
    fetch(`${API}/plan-archive`, withUser({
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body(p)),
    })).then((r) => { if (!r.ok) throw new Error(); }).catch(() => {
      setArchivedFlag(p.filename, true);
      setToast({ kind: "block", text: "Couldn't restore just now — please try again." });
    });
  };

  // Auto-dismiss the toast after a few seconds.
  useEffect(() => {
    if (!toast) return;
    const t = setTimeout(() => setToast(null), 3200);
    return () => clearTimeout(t);
  }, [toast]);

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

  // My Lessons shows ONLY what this teacher has prepared — never the whole shared sample library
  // (live gen is deferred, so the saved-plan content is identical for every teacher). The server
  // sets `prepared` per tenant; a plan any section is attached to counts as prepared too, so a
  // lesson a class is actively teaching can never vanish from the repository even if its prepared
  // write was lost. Un-prepared sample plans are hidden entirely (the empty-state copy already
  // reads "no lesson plans prepared … yet").
  const preparedPlans = (Array.isArray(plans) ? plans : []).filter((p) => p.prepared || isAttached(p));
  // Split the prepared list into the two views by the server-set archived flag (archive is a
  // flag, not a separate fetch). Chips only appear once something is archived — no clutter before.
  const allPlans = preparedPlans;
  const activePlans = allPlans.filter((p) => !p.archived);
  const archivedPlans = allPlans.filter((p) => p.archived);
  const hasArchived = archivedPlans.length > 0;
  const effView = hasArchived ? view : "active";   // auto-fall-back when nothing's archived
  const shown = effView === "archived" ? archivedPlans : activePlans;

  return (
    <div className="mlp2">
      <div className="mlp2-frozen">
        <div className="mlp2-titlerow">
          <h1 className="mlp2-title">{effView === "archived" ? "Archive" : "Your lessons"}</h1>
          {effView === "archived" ? (
            // Open box = you're inside the archive; tapping it closes the box and drops you back
            // to your lessons (the one, symmetric way in and out).
            <button className="mlp2-archfolder open" onClick={() => setView("active")}
              aria-label="Close archive, back to your lessons" title="Back to your lessons">
              <OpenArchiveIcon size={22} />
              <span className="mlp2-archcount">{archivedPlans.length}</span>
            </button>
          ) : hasArchived ? (
            <button className="mlp2-archfolder" onClick={() => setView("archived")}
              aria-label={`Open archive (${archivedPlans.length})`} title="Archived lessons">
              <ArchiveIcon size={22} />
              <span className="mlp2-archcount">{archivedPlans.length}</span>
            </button>
          ) : null}
        </div>
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
      ) : shown.length === 0 ? (
        <div className="mlp2-emptybody">
          {effView === "archived"
            ? "Nothing archived here."
            : hasArchived
              ? `Every prepared lesson for ${pretty(sSlug)} · Class ${classNum(activeGrade)} is archived.`
              : `There are no lesson plans prepared for ${pretty(sSlug)} · Class ${classNum(activeGrade)} yet.`}
        </div>
      ) : (
        <div className="sc-list">
          {shown.map((p) => {
            const { completed, live } = statusFor(p);
            const cls = effView === "archived"
              ? "mlp2-arch"
              : live.length ? "st-going" : completed.length ? "st-done" : "mlp2-shelf";
            return (
              <div className={`sc-card ${cls}`} key={p.filename} onClick={() => openLesson(p)}>
                <div className="sc-tag">{pad(p.chapter_number)}</div>
                <div className="sc-body">
                  <div className="sc-title">{p.chapter_title}</div>
                  {effView === "archived" ? (
                    <div className="mlp2-ready">Archived</div>
                  ) : completed.length || live.length ? (
                    <div className="mlp2-status">
                      {completed.length > 0 && <span>Completed {completed.join(", ")}</span>}
                      {completed.length > 0 && live.length > 0 && <span className="sep">·</span>}
                      {live.length > 0 && <span>Teaching now {live.join(", ")}</span>}
                    </div>
                  ) : (
                    <div className="mlp2-ready">Ready to teach</div>
                  )}
                </div>
                {effView === "archived" ? (
                  <button className="mlp2-restore-btn" onClick={(e) => restorePlan(p, e)}
                    aria-label={`Restore ${p.chapter_title}`}>Restore</button>
                ) : !isAttached(p) ? (
                  // No archive affordance on a plan a class is on — attached plans can't be
                  // archived, so showing (and then blocking) the control would be inconsistent.
                  <button className="mlp2-iconbtn archive" onClick={(e) => archivePlan(p, e)}
                    aria-label={`Archive ${p.chapter_title}`} title="Archive">
                    <ArchiveIcon />
                  </button>
                ) : null}
              </div>
            );
          })}
        </div>
      )}

      {prepareCTA}

      {toast && (
        <div className={`mlp2-toast ${toast.kind}`} role="status">{toast.text}</div>
      )}
    </div>
  );
}
