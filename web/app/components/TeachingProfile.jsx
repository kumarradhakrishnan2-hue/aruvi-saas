"use client";
import { useEffect, useRef, useState } from "react";
import { getJSON, pretty, ROMAN, projectReadiness, API, withUser } from "../lib/format";
import { pushSectionState } from "../lib/sectionState";
import { RollWheel, PickWheel } from "./wheels";

/* ───────── TeachingProfile — Settings → "Your teaching profile" (rebuilt 2026-07-02) ─────────
 * The ONE profile editor, reached through the header settings gear.
 *
 * Founder spec (this iteration):
 *   • ACCORDION — subjects are collapsible rows; ONLY ONE subject (and its classes) is open
 *     at a time, so the page never shows more than one subject's tree. Tap a header to open.
 *   • MASTER EDIT — a single Edit toggle reveals ALL mutation controls at once: red dustbins
 *     (delete a subject / a class / a section chip), "edit →" on the numbers line, and the
 *     green add buttons (+ section · + add a class · + add a subject). View mode is clean —
 *     nothing but her data.
 *   • STRUCTURE vs VALUES — things in her tree (subjects/classes/sections) are added/removed
 *     in place; numbers about a thing (duration · periods/week · annual budget) open the same
 *     single-question wheel screens from day one, prefilled, Save and back. One editing idiom.
 *   • NO whole-profile actions — "Delete profile" and "Redo whole profile" are gone. The
 *     profile is only ever edited at a point.
 *
 * Every dustbin gets ONE scoped confirm naming exactly what goes (a section names one card;
 * a class names its sections; a subject names its classes) and always ends with: lessons stay
 * in the library. Removals cascade upward (last section takes its class; last class takes its
 * subject) and clear the removed sections' local state (lu_pointer_*, current_chapter_*).
 *
 * Adding a subject runs that ONE subject through the conversational loop (classes → per class:
 * sections → duration → periods/week → the 4-method annual-budget estimator), with the
 * "subject saved ✓ — continue / finish for now" checkpoint between subjects when several are
 * added at once. Adding a class runs ONLY the new class(es) through the per-class questions —
 * existing classes are never re-asked. All time-facts remain NUMBERS (no day schedule, ever —
 * the calendar purge, MEMORY.md 2026-07-02); grids[] ships all -1 for shape-compat.
 *
 * Props: readiness (projection carrying canonical .subjects[]), onChange(projection).
 */

const SECTION_LETTERS = Array.from({ length: 26 }, (_, i) => String.fromCharCode(65 + i)); // A…Z
const DURATION_CHOICES = Array.from({ length: 21 }, (_, i) => 20 + i * 5); // 20,25,…120 min
const PPW_CHOICES = Array.from({ length: 14 }, (_, i) => i + 1);           // 1…14 periods/week
const DAYS_IN_WEEK = 6;
const ESTIMATE_WEEKS = 30;
const DEFAULT_DURATION = 40;
const DEFAULT_PPW = 6;

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

const classNum = (g) => {
  const idx = ROMAN.indexOf((g || "").toLowerCase());
  return idx >= 0 ? idx + 3 : g;
};

/* ── periods/week is now stored PER DURATION TYPE (ppw_by_duration: { [minutes]: count }) ──
 * We no longer ask a single "periods per week" number: where a class has >1 duration type,
 * the teacher gives the weekly count for EACH duration and the total is their sum (the ratio
 * that will split a chapter's periods at generation — see MEMORY.md 2026-07-05). `periods_per_week`
 * is kept on the record as that DERIVED sum, so every existing consumer (budget estimator, view
 * totals, format.projectReadiness) is unchanged. */
const ppwMapSum = (m) => Object.keys(m || {}).reduce((a, k) => a + (Number(m[k]) || 0), 0);
// Reconcile a per-duration weekly-count map to the CURRENT set of durations: keep the count for
// each surviving duration; a duration with no count yet defaults to the whole total when there's
// only one type (single-duration = the old single number), else to 1 (a real type teaches ≥1/wk).
const normPpw = (durations, map, fallbackPpw) => {
  const durs = (durations && durations.length) ? durations : [DEFAULT_DURATION];
  const out = {};
  durs.forEach((d) => {
    const v = Number((map || {})[d] ?? (map || {})[String(d)]);
    out[d] = v > 0 ? v : (durs.length === 1 ? (Number(fallbackPpw) || DEFAULT_PPW) : 1);
  });
  return out;
};

/* Per-duration periods/week capture — ONE selection idiom, two shapes:
 *   • single duration → the same large periods/week wheel as before (no visible change);
 *   • >1 duration     → a two-column table (Duration · Periods/week stepper), one row per type
 *     (up to three), with the running weekly total shown live. Total is NEVER asked directly. */
function PpwCapture({ durations, map, onSet }) {
  const durs = (durations && durations.length) ? durations : [DEFAULT_DURATION];
  if (durs.length === 1) {
    const d = durs[0];
    const val = Number(map[d] ?? map[String(d)]) || DEFAULT_PPW;
    return (
      <RollWheel ariaLabel="Periods per week" large value={String(val)}
        onChange={(v) => onSet(d, Number(v))}
        items={PPW_CHOICES.map((p) => ({ id: String(p), chip: p, label: p === 1 ? "period a week" : "periods a week" }))} />
    );
  }
  const total = durs.reduce((a, d) => a + (Number(map[d] ?? map[String(d)]) || 0), 0);
  return (
    <div className="tp-ppw-table">
      <div className="tp-ppw-row tp-ppw-head">
        <span className="tp-ppw-dur">Duration</span>
        <span className="tp-ppw-ct">Periods / week</span>
      </div>
      {durs.map((d) => {
        const val = Number(map[d] ?? map[String(d)]) || 1;
        return (
          <div className="tp-ppw-row" key={d}>
            <span className="tp-ppw-dur">{d} min</span>
            <span className="tp-ppw-stepper">
              <button type="button" className="tp-val-btn" aria-label={`Fewer ${d}-minute periods`} onClick={() => onSet(d, Math.max(1, val - 1))}>−</button>
              <input type="number" className="tp-val-input tp-ppw-input" min="1" value={val}
                onChange={(e) => onSet(d, Math.max(1, parseInt(e.target.value, 10) || 1))}
                aria-label={`Periods per week for ${d}-minute classes`} />
              <button type="button" className="tp-val-btn" aria-label={`More ${d}-minute periods`} onClick={() => onSet(d, val + 1)}>+</button>
            </span>
          </div>
        );
      })}
      <p className="tp-ppw-total">= {total} periods a week</p>
    </div>
  );
}

const subjectSlugOf = (name) => (name || "").toLowerCase().replace(/ /g, "_");
const deepCopy = (x) => JSON.parse(JSON.stringify(x));
const secLetter = (s) => (typeof s === "string" ? s : s.sec);
const byRoman = (a, b) => ROMAN.indexOf(a.toLowerCase()) - ROMAN.indexOf(b.toLowerCase());

// red dustbin (stroke inherits color — .tp-bin sets the red)
const Bin = () => (
  <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor"
    strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M3.5 6.5h17M9.5 6.5V4.4h5v2.1M18.8 6.5l-1 14h-11.6l-1-14M10 11v6M14 11v6" />
  </svg>
);

// pencil (edit) — stroke inherits color via .tp-icon-btn
const Pencil = ({ size = 14 }) => (
  <svg viewBox="0 0 24 24" width={size} height={size} fill="none" stroke="currentColor"
    strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M4 20h4L18.5 9.5a1.5 1.5 0 0 0 0-2.12l-1.88-1.88a1.5 1.5 0 0 0-2.12 0L4 16v4z" />
    <path d="M13.5 6.5l4 4" />
  </svg>
);

// clear the local teaching state (bookmark + chapter binding) of one removed section
const clearSectionState = (subjName, gradeRoman, tag) => {
  const key = `${subjectSlugOf(subjName)}_${(gradeRoman || "").toLowerCase()}_${tag}`;
  try {
    window.localStorage.removeItem(`lu_pointer_${key}`);
    window.localStorage.removeItem(`current_chapter_${key}`);
    window.localStorage.removeItem(`lu_done_${key}`);
  } catch {}
  pushSectionState(key);   // chapter gone → the server drops this section's row too
};

// budget maps are keyed by grade INDEX — re-key whenever the grade list changes shape
const rekeyBudget = (oldGrades, oldBudget, newGrades) => {
  const byGrade = {};
  (oldGrades || []).forEach((g, i) => {
    const b = (oldBudget || {})[i] ?? (oldBudget || {})[String(i)];
    if (b) byGrade[g.grade] = b;
  });
  const out = {};
  newGrades.forEach((g, i) => { if (byGrade[g.grade]) out[i] = byGrade[g.grade]; });
  return out;
};

// per-grade draft used inside the conversational screens: sections as plain letters
const gradeDraftFrom = (rec) => {
  const durations = (rec.durations && rec.durations.length) ? [...rec.durations] : [DEFAULT_DURATION];
  const ppw_by_duration = normPpw(durations, rec.ppw_by_duration, rec.periods_per_week);
  return {
    grade: rec.grade,
    sections: (rec.sections || []).map(secLetter),
    durations,
    ppw_by_duration,
    periods_per_week: ppwMapSum(ppw_by_duration),
    budget: null,
  };
};

export default function TeachingProfile({ readiness, onChange, onBack, autoAddClassSubject, onConsumeAutoAdd, portalIntent, onConsumePortal }) {
  // SINGLE SOURCE OF TRUTH: the profile lives in the parent's `readiness` prop. Derive the
  // canonical subjects[] straight from it — no mirrored local copy. That way an edit (which
  // routes through persist → onChange → setReadiness) re-renders THIS view and every other
  // consumer from the exact same object, so edits reflect live the instant they save, exactly
  // like adds do. `canon` is READ-only here; every mutation deep-copies before touching it, so
  // deriving (not copying into state) is safe and removes the mirror-state desync.
  const canon = (readiness && readiness.subjects) || [];

  /* view state */
  const [openSubject, setOpenSubject] = useState(null);  // accordion: name of the ONE open subject
  const [editing, setEditing] = useState(false);         // master edit toggle
  const [confirm, setConfirm] = useState(null);          // { kind:"subject"|"grade"|"section", si, gi?, sec? }

  /* flow state (conversational screens) */
  // screen: view | pickSubjects | classes | class | subjectDone | addSection | editNums
  //         | editSections | portalSubject | portalClass
  const [screen, setScreen] = useState("view");
  // "add" (the gear's + buttons: only NEW options offered) vs "manage" (the My Classes "+"
  // portal: enrolled options shown pre-ticked; unticking one = removal behind the same scoped
  // warning the dustbins use — warned, never blocked, since mid-year reassignments are real).
  const [pickMode, setPickMode] = useState("add");      // pickSubjects screen
  const [classMode, setClassMode] = useState("add");    // classes screen
  const [portalGoal, setPortalGoal] = useState(null);   // "class" | "section" — what the portal pick leads to
  const [portalSi, setPortalSi] = useState(null);       // portal: chosen subject index (section goal)
  const [subConfirm, setSubConfirm] = useState(null);   // { removes:[names], adds:[names] } — manage-subjects warning
  const [classConfirm, setClassConfirm] = useState(null); // { removes:[romans], adds:[romans] } — manage-classes warning
  const [fromPortal, setFromPortal] = useState(false);  // visit began at My Classes' "+" → every exit returns there
  // Back links still route through setScreen("view"); on a portal visit the bounce effect
  // (below) forwards that to My Classes, so the label says where she'll actually land.
  const backLabel = fromPortal ? "← Back to My Classes" : "← Back to profile";
  const [catalogue, setCatalogue] = useState([]);        // all offerable subject display names
  const [queue, setQueue] = useState([]); const [qi, setQi] = useState(0); // addSubject queue
  const [picked, setPicked] = useState([]);              // generic multi-pick buffer
  const [gradeOptions, setGradeOptions] = useState([]);  // roman uppercase, current subject
  const [draft, setDraft] = useState(null);              // { name, grades:[gradeDraft], existingCount }
  const [pendingIdxs, setPendingIdxs] = useState([]);    // draft.grades indices still to be asked
  const [pi, setPi] = useState(0);                       // position inside pendingIdxs
  const [classStep, setClassStep] = useState("sections"); // sections | durations | ppw | budget
  const [numCtx, setNumCtx] = useState(null);            // editNums: { si, gi, g(draft), step }
  const [ncfTotal, setNcfTotal] = useState(null);        // NCF recommended annual periods for the budget "estimate"
  const [secConfirm, setSecConfirm] = useState(null);    // { removed:[tags] } — warn before an edit-sections save drops sections

  // pin the top block just below the app's sticky header — measure the header so the offset
  // is exact across desktop/mobile rather than a guessed pixel value
  const rootRef = useRef(null);
  useEffect(() => {
    const setTop = () => {
      const el = rootRef.current;
      if (!el) return;
      const h = (typeof document !== "undefined" && document.querySelector(".hdr")?.offsetHeight) || 60;
      el.style.setProperty("--tp-sticky-top", `${h}px`);
      const sticky = el.querySelector(".tp-sticky");
      const sh = sticky ? sticky.offsetHeight : 0;
      el.style.setProperty("--tp-sub-top", `${h + sh}px`); // open subject header pins just below the top block
    };
    setTop();
    window.addEventListener("resize", setTop);
    return () => window.removeEventListener("resize", setTop);
  }, [canon, editing]);

  useEffect(() => {
    getJSON("/subjects").then((d) => setCatalogue((d.subjects || []).map(pretty))).catch(() => setCatalogue([]));
  }, []);
  // keep the accordion pointing at a real subject
  useEffect(() => {
    if (!canon.length) { setOpenSubject(null); return; }
    if (!canon.some((s) => s.name === openSubject)) setOpenSubject(canon[0].name);
  }, [canon]); // eslint-disable-line react-hooks/exhaustive-deps

  // Arrived from the My Classes "add more classes in this subject" prompt: open that subject
  // and launch the SAME add-a-class flow the "+ add a class" button uses, then tell the parent
  // to clear the directive. Guarded to run once (a re-render must not relaunch it).
  const autoAddDoneRef = useRef(false);
  useEffect(() => {
    if (!autoAddClassSubject || autoAddDoneRef.current) return;
    const si = canon.findIndex((s) => s.name === autoAddClassSubject);
    if (si < 0) return; // wait until canon carries the subject
    autoAddDoneRef.current = true;
    setOpenSubject(autoAddClassSubject);
    startAddClass(si);
    onConsumeAutoAdd && onConsumeAutoAdd();
  }, [autoAddClassSubject, canon]); // eslint-disable-line react-hooks/exhaustive-deps

  // Arrived from My Classes' standing "+" portal (founder, 2026-07-06): launch the manage
  // screen for the chosen level — Subject straight in; Class/Section via a subject (and class)
  // pick first, skipped when there is only one. Same one-shot guard as the auto-add directive.
  const portalDoneRef = useRef(false);
  useEffect(() => {
    if (!portalIntent || portalDoneRef.current || !canon.length) return;
    portalDoneRef.current = true;
    setFromPortal(true);
    if (portalIntent === "subject") startManageSubjects();
    else if (portalIntent === "class") {
      if (canon.length === 1) startManageClasses(0);
      else { setPortalGoal("class"); setScreen("portalSubject"); }
    } else if (portalIntent === "section") {
      if (canon.length === 1) portalPickClass(0);
      else { setPortalGoal("section"); setScreen("portalSubject"); }
    }
    onConsumePortal && onConsumePortal();
  }, [portalIntent, canon]); // eslint-disable-line react-hooks/exhaustive-deps

  // A portal-initiated visit ALWAYS ends in My Classes, never on the profile accordion
  // (founder, 2026-07-06): she came from her cards, so every exit — completing the flow,
  // cancelling, or any "back" link — returns her there. Every flow ending funnels through
  // setScreen("view"), so this one bounce covers them all. onBack is page.jsx's goClasses.
  useEffect(() => {
    if (fromPortal && screen === "view") onBack && onBack();
  }, [fromPortal, screen]); // eslint-disable-line react-hooks/exhaustive-deps

  const persist = (subjectsOut) => {
    // Optimistic: push straight to the parent so the view reflects instantly — no local mirror
    // to keep in step. setReadiness re-renders this component with the new subjects[] (which
    // `canon` derives from) and every consumer.
    onChange && onChange(projectReadiness({ subjects: subjectsOut }));
    // Persist to the server. cascade:true is REQUIRED for any removal (deleting a subject /
    // class / section, or unticking a section): every destructive edit here is ALREADY behind a
    // scoped confirm modal, and without cascade the server refuses removals with HTTP 409 and
    // the write silently fails — so the edit reverts on the next login. Additive / value-only
    // edits carry nothing to cascade, so the flag is a harmless no-op for them. Surface any
    // failure rather than swallowing it, so a broken save is never invisible again.
    fetch(`${API}/readiness`, withUser({
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ subjects: subjectsOut, cascade: true }),
    }))
      .then((res) => { if (!res.ok) console.error("Aruvi: readiness save failed", res.status); })
      .catch((e) => console.error("Aruvi: readiness save error", e));
  };

  /* ── granular removals (each behind its scoped confirm) ── */
  const doRemove = () => {
    const { kind, si, gi, sec } = confirm;
    const next = deepCopy(canon);
    const sub = next[si];
    if (kind === "section") {
      const g = sub.grades[gi];
      clearSectionState(sub.name, g.grade, `${classNum(g.grade)}${sec}`);
      g.sections = g.sections.filter((x) => secLetter(x) !== sec);
      if (!g.sections.length) {              // cascade: last section takes the class
        const oldGrades = sub.grades;
        sub.grades = sub.grades.filter((_, i) => i !== gi);
        sub.budget = rekeyBudget(oldGrades, sub.budget, sub.grades);
        sub.grids = sub.grades.map((gr) => gr.sections.map(() => Array(DAYS_IN_WEEK).fill(-1)));
      } else {
        sub.grids = sub.grades.map((gr) => gr.sections.map(() => Array(DAYS_IN_WEEK).fill(-1)));
      }
    }
    if (kind === "grade") {
      const g = sub.grades[gi];
      g.sections.forEach((x) => clearSectionState(sub.name, g.grade, `${classNum(g.grade)}${secLetter(x)}`));
      const oldGrades = sub.grades;
      sub.grades = sub.grades.filter((_, i) => i !== gi);
      sub.budget = rekeyBudget(oldGrades, sub.budget, sub.grades);
      sub.grids = sub.grades.map((gr) => gr.sections.map(() => Array(DAYS_IN_WEEK).fill(-1)));
    }
    if (kind === "subject") {
      sub.grades.forEach((g) => g.sections.forEach((x) =>
        clearSectionState(sub.name, g.grade, `${classNum(g.grade)}${secLetter(x)}`)));
    }
    const out = (kind === "subject" || !next[si].grades.length)
      ? next.filter((_, i) => i !== si)      // cascade: last class takes the subject
      : next;
    persist(out);
    setConfirm(null);
  };

  // scoped confirm copy: name exactly what goes, promise what stays
  const confirmCopy = () => {
    const { kind, si, gi, sec } = confirm;
    const sub = canon[si];
    if (kind === "section") {
      const g = sub.grades[gi];
      const tag = `${classNum(g.grade)}${sec}`;
      const last = g.sections.length === 1;
      return {
        title: `Remove Section ${tag}?`,
        body: `Its card and bookmark will be removed.${last ? ` It is the last section — Class ${classNum(g.grade)} goes with it.` : ""} Your lessons stay in the library.`,
        cta: `Yes, remove ${tag}`,
      };
    }
    if (kind === "grade") {
      const g = sub.grades[gi];
      const tags = g.sections.map((x) => `${classNum(g.grade)}${secLetter(x)}`).join(", ");
      const last = sub.grades.length === 1;
      return {
        title: `Remove Class ${classNum(g.grade)} from ${sub.name}?`,
        body: `${tags} — their cards and bookmarks — will be removed.${last ? ` It is the last class — ${sub.name} goes with it.` : ""} Your lessons stay in the library.`,
        cta: `Yes, remove Class ${classNum(g.grade)}`,
      };
    }
    const classes = sub.grades.map((g) => `Class ${classNum(g.grade)}`).join(", ");
    return {
      title: `Remove ${sub.name}?`,
      body: `${classes || "Its classes"} — all cards and bookmarks — will be removed. Your lessons stay in the library.`,
      cta: `Yes, remove ${sub.name}`,
    };
  };

  /* ── add flows ── */
  const startAddSubject = () => { setPicked([]); setPickMode("add"); setClassMode("add"); setScreen("pickSubjects"); };

  /* ── manage flows (the My Classes "+" portal) — same screens, enrolled options pre-ticked;
     unticking removes behind ONE scoped warning. Warned, never blocked. ── */
  const startManageSubjects = () => {
    setPicked(canon.map((s) => s.name));
    setPickMode("manage"); setClassMode("add");
    setScreen("pickSubjects");
  };
  const startManageClasses = (si) => {
    setClassMode("manage");
    setQueue([canon[si].name]); setQi(0);
    beginSubjectRun(canon[si].name);
    setPicked((canon[si].grades || []).map((g) => g.grade)); // pre-tick enrolled (beginSubjectRun clears picked)
  };
  // Section goal: subject chosen → straight to editSections when the subject has one class,
  // else ask which class first.
  const portalPickClass = (si) => {
    const sub = canon[si];
    if ((sub.grades || []).length === 1) startEditSections(si, 0);
    else { setPortalSi(si); setScreen("portalClass"); }
  };

  const startSubjectAdds = (adds) => { setClassMode("add"); setQueue(adds); setQi(0); beginSubjectRun(adds[0]); };
  const onManageSubjectsContinue = () => {
    const enrolled = canon.map((s) => s.name);
    const adds = picked.filter((n) => !enrolled.includes(n));
    const removes = enrolled.filter((n) => !picked.includes(n));
    if (!adds.length && !removes.length) { setScreen("view"); return; }
    if (removes.length) setSubConfirm({ removes, adds });
    else startSubjectAdds(adds);
  };
  const applySubjectChanges = () => {
    const { removes, adds } = subConfirm;
    const next = deepCopy(canon).filter((s) => {
      if (!removes.includes(s.name)) return true;
      s.grades.forEach((g) => g.sections.forEach((x) =>
        clearSectionState(s.name, g.grade, `${classNum(g.grade)}${secLetter(x)}`)));
      return false;
    });
    persist(next);
    setSubConfirm(null);
    if (adds.length) startSubjectAdds(adds);
    else setScreen("view");
  };

  // seed the conversational run for ONE subject; pending = which grades still get questions
  const beginSubjectRun = (name) => {
    const existing = canon.find((s) => s.name === name);
    const grades = existing ? (existing.grades || []).map(gradeDraftFrom) : [];
    if (existing && existing.budget) {
      grades.forEach((g, i) => {
        const b = existing.budget[i] ?? existing.budget[String(i)];
        if (b) g.budget = { ...b };
      });
    }
    setDraft({ name, grades });
    setPicked([]);
    setGradeOptions([]);
    getJSON(`/subjects/${subjectSlugOf(name)}/grades`).then((d) => {
      const gs = [...(d.grades || [])].sort((a, b) => ROMAN.indexOf(a) - ROMAN.indexOf(b));
      setGradeOptions(gs.map((g) => g.toUpperCase()));
    }).catch(() => setGradeOptions([]));
    setScreen("classes");
  };

  const onSubjectsPicked = () => {
    const q = [...picked];
    setQueue(q); setQi(0);
    beginSubjectRun(q[0]);
  };

  const startAddClass = (si) => {
    setClassMode("add");
    setQueue([canon[si].name]); setQi(0);
    beginSubjectRun(canon[si].name);
  };

  // classes step continue: NEW grades only get questions; existing ones keep their answers.
  // Shared by the add path (base = current draft grades) and the manage path (base = the
  // grades KEPT after a removal confirm).
  const continueWithGrades = (baseGrades, addedRomans) => {
    const all = [...baseGrades, ...addedRomans.map((roman) => ({
      grade: roman, sections: [], durations: [DEFAULT_DURATION],
      ppw_by_duration: { [DEFAULT_DURATION]: DEFAULT_PPW },
      periods_per_week: DEFAULT_PPW, budget: null,
    }))].sort((a, b) => byRoman(a.grade, b.grade));
    const pend = all.map((g, i) => (addedRomans.includes(g.grade) ? i : -1)).filter((i) => i >= 0);
    setDraft((d) => ({ ...d, grades: all }));
    setPendingIdxs(pend); setPi(0); setClassStep("sections");
    setScreen("class");
  };
  const onClassesContinue = () => {
    const have = draft.grades.map((g) => g.grade);
    continueWithGrades(draft.grades, picked.filter((g) => !have.includes(g)));
  };
  // Manage-classes continue: unticked enrolled classes = removals (warned first); newly ticked
  // ones queue the usual per-class questions afterwards.
  const onManageClassesContinue = () => {
    const have = draft.grades.map((g) => g.grade);
    const adds = picked.filter((g) => !have.includes(g));
    const removes = have.filter((g) => !picked.includes(g));
    if (!adds.length && !removes.length) { setScreen("view"); return; }
    if (removes.length) setClassConfirm({ removes, adds });
    else continueWithGrades(draft.grades, adds);
  };
  const applyClassChanges = () => {
    const { removes, adds } = classConfirm;
    // Removed classes lose their section bookmarks (draft grade sections are letters).
    draft.grades.forEach((g) => {
      if (removes.includes(g.grade)) g.sections.forEach((sec) =>
        clearSectionState(draft.name, g.grade, `${classNum(g.grade)}${sec}`));
    });
    const keep = draft.grades.filter((g) => !removes.includes(g.grade));
    setClassConfirm(null);
    if (adds.length) continueWithGrades(keep, adds);
    else if (keep.length) { finalizeSubject({ ...draft, grades: keep }); setScreen("view"); }
    else {
      // last class taken away and nothing added — the subject goes with it (warned in the confirm)
      persist(deepCopy(canon).filter((s) => s.name !== draft.name));
      setScreen("view");
    }
  };

  const gIdx = pendingIdxs[pi];
  const updGrade = (patch) => setDraft((d) => ({
    ...d, grades: d.grades.map((g, i) => (i === gIdx ? { ...g, ...patch } : g)),
  }));

  // fetch the NCF-recommended annual periods whenever a budget screen is showing, so the
  // "estimate" option reflects the National Curricular Framework figure for this subject·grade
  const inClassBudget = screen === "class" && classStep === "budget";
  const inEditBudget = screen === "editNums" && numCtx && numCtx.step === "budget";
  const budgetSubject = inClassBudget ? (draft && draft.name)
    : inEditBudget ? (canon[numCtx.si] && canon[numCtx.si].name) : null;
  const budgetGrade = inClassBudget ? (draft && draft.grades[gIdx] && draft.grades[gIdx].grade)
    : inEditBudget ? (numCtx.g && numCtx.g.grade) : null;
  useEffect(() => {
    if (!budgetSubject || !budgetGrade) return;
    let live = true;
    setNcfTotal(null);
    getJSON(`/subjects/${subjectSlugOf(budgetSubject)}/${budgetGrade.toLowerCase()}/ncf-periods`)
      .then((d) => { if (live) setNcfTotal(d && d.ncf_total_periods != null ? d.ncf_total_periods : null); })
      .catch(() => { if (live) setNcfTotal(null); });
    return () => { live = false; };
  }, [budgetSubject, budgetGrade]);

  // finalize the draft into a canonical record and persist (upsert by name)
  const finalizeSubject = (d) => {
    const budget = {};
    d.grades.forEach((g, i) => { budget[i] = g.budget || { method: "auto", value: 0 }; });
    const rec = {
      name: d.name,
      grades: d.grades.map((g) => {
        const ppwMap = normPpw(g.durations, g.ppw_by_duration, g.periods_per_week);
        return {
          grade: g.grade,
          sections: g.sections.map((sec) => ({ tag: `${classNum(g.grade)}${sec}`, sec })),
          durations: [...g.durations],
          ppw_by_duration: ppwMap,
          periods_per_week: ppwMapSum(ppwMap),
        };
      }),
      grids: d.grades.map((g) => g.sections.map(() => Array(DAYS_IN_WEEK).fill(-1))), // shape-compat only
      budget,
    };
    const idx = canon.findIndex((s) => s.name === rec.name);
    persist(idx >= 0 ? canon.map((s, i) => (i === idx ? rec : s)) : [...canon, rec]);
    setOpenSubject(rec.name);
  };

  const onClassDone = () => {
    if (pi + 1 < pendingIdxs.length) { setPi(pi + 1); setClassStep("sections"); return; }
    finalizeSubject(draft);
    if (qi + 1 < queue.length) setScreen("subjectDone");  // checkpoint between added subjects
    else setScreen("view");
  };

  /* ── spot edits ── */
  const startAddSection = (si, gi) => { setNumCtx({ si, gi }); setPicked([]); setScreen("addSection"); };

  // pencil next to the sections → one screen to add AND remove (keep ≥1; whole-class delete stays on the basket)
  const startEditSections = (si, gi) => {
    setNumCtx({ si, gi });
    setPicked(canon[si].grades[gi].sections.map(secLetter));
    setScreen("editSections");
  };
  // Save intent: if the edit drops any existing sections, warn first (same as the basket removals);
  // pure additions save straight through.
  const requestEditSections = () => {
    const { si, gi } = numCtx;
    const g = canon[si].grades[gi];
    const removed = g.sections.map(secLetter).filter((s) => !picked.includes(s));
    if (removed.length) setSecConfirm({ removed: removed.map((sec) => `${classNum(g.grade)}${sec}`) });
    else applyEditSections();
  };
  const applyEditSections = () => {
    const { si, gi } = numCtx;
    const next = deepCopy(canon);
    const sub = next[si]; const g = sub.grades[gi];
    const before = g.sections.map(secLetter);
    const after = [...picked].sort();
    before.filter((s) => !after.includes(s)).forEach((sec) =>
      clearSectionState(sub.name, g.grade, `${classNum(g.grade)}${sec}`));
    g.sections = after.map((sec) => ({ tag: `${classNum(g.grade)}${sec}`, sec }));
    sub.grids = sub.grades.map((gr) => gr.sections.map(() => Array(DAYS_IN_WEEK).fill(-1)));
    persist(next);
    setSecConfirm(null);
    setScreen("view");
  };
  const saveAddSection = () => {
    const { si, gi } = numCtx;
    const next = deepCopy(canon);
    const g = next[si].grades[gi];
    const have = g.sections.map(secLetter);
    [...picked].sort().forEach((sec) => {
      if (!have.includes(sec)) g.sections.push({ tag: `${classNum(g.grade)}${sec}`, sec });
    });
    g.sections.sort((a, b) => (secLetter(a) < secLetter(b) ? -1 : 1));
    next[si].grids = next[si].grades.map((gr) => gr.sections.map(() => Array(DAYS_IN_WEEK).fill(-1)));
    persist(next);
    setScreen("view");
  };

  const startEditNums = (si, gi, step = "duration") => {
    const sub = canon[si];
    const g = gradeDraftFrom(sub.grades[gi]);
    const b = (sub.budget || {})[gi] ?? (sub.budget || {})[String(gi)];
    if (b) g.budget = { ...b };
    setNumCtx({ si, gi, g, step });
    setScreen("editNums");
  };
  const updNum = (patch) => setNumCtx((c) => ({ ...c, g: { ...c.g, ...patch } }));
  // save from ANY single field-edit screen; unedited fields keep their loaded values
  const saveEditNums = (finalBudget) => {
    const { si, gi, g } = numCtx;
    const next = deepCopy(canon);
    const rec = next[si].grades[gi];
    const ppwMap = normPpw(g.durations, g.ppw_by_duration, g.periods_per_week);
    rec.durations = [...g.durations];
    rec.ppw_by_duration = ppwMap;
    rec.periods_per_week = ppwMapSum(ppwMap);
    const budget = finalBudget || g.budget
      || (next[si].budget || {})[gi] || (next[si].budget || {})[String(gi)]
      || { method: "auto", value: 0 };
    next[si].budget = { ...(next[si].budget || {}), [gi]: budget };
    persist(next);
    setScreen("view");
  };

  /* ════════════════════ conversational screens ════════════════════ */

  // Portal pick screens — the "+" chose Class or Section; ask which subject (and class) first.
  if (screen === "portalSubject") {
    return (
      <div className="tp">
        <div className="kicker kicker-ochre">Your teaching · {portalGoal === "class" ? "classes" : "sections"}</div>
        <h1 className="fr-q">In which subject?</h1>
        <p className="fr-hint">{portalGoal === "class"
          ? "Pick the subject whose classes you want to change."
          : "Pick the subject, then the class whose sections you want to change."}</p>
        <div className="tp-portal-list">
          {canon.map((s, si) => (
            <button key={s.name} type="button" className="tp-portal-row"
              onClick={() => (portalGoal === "class" ? startManageClasses(si) : portalPickClass(si))}>
              <span>{s.name}</span><span className="tp-portal-go" aria-hidden="true">›</span>
            </button>
          ))}
        </div>
        <button className="fr-link" onClick={() => setScreen("view")}>{backLabel}</button>
      </div>
    );
  }

  if (screen === "portalClass") {
    const sub = canon[portalSi];
    if (!sub) return null;
    return (
      <div className="tp">
        <div className="kicker kicker-ochre">{sub.name} · sections</div>
        <h1 className="fr-q">Which class?</h1>
        <p className="fr-hint">Pick the class whose sections you want to change.</p>
        <div className="tp-portal-list">
          {sub.grades.map((g, gi) => (
            <button key={g.grade} type="button" className="tp-portal-row"
              onClick={() => startEditSections(portalSi, gi)}>
              <span>Class {classNum(g.grade)}</span><span className="tp-portal-go" aria-hidden="true">›</span>
            </button>
          ))}
        </div>
        <button className="fr-link" onClick={() => setScreen("view")}>{backLabel}</button>
      </div>
    );
  }

  if (screen === "pickSubjects") {
    const manage = pickMode === "manage";
    const enrolled = canon.map((s) => s.name);
    const options = manage ? catalogue : catalogue.filter((n) => !enrolled.includes(n));
    const toggle = (n) => setPicked((a) => (a.includes(n) ? a.filter((x) => x !== n) : [...a, n]));
    return (
      <div className="tp">
        <div className="kicker kicker-ochre">{manage ? "Your teaching · subjects" : "Teaching profile · add a subject"}</div>
        <h1 className="fr-q">{manage ? "What do you teach?" : "What else do you teach?"}</h1>
        <p className="fr-hint">{manage
          ? "Tick a subject to add it — untick one to remove it. Keep at least one."
          : "Pick the subject — or several — to add."}</p>
        {options.length === 0 && <p className="fr-hint">Every subject Aruvi offers is already in your profile.</p>}
        {options.length > 0 && (
          <PickWheel options={options} selected={picked} onToggle={toggle}
            ariaLabel={manage ? "Your subjects" : "Subjects to add"}>
            <button type="button" className="primary fr-cta" disabled={!picked.length}
              onClick={manage ? onManageSubjectsContinue : onSubjectsPicked}>
              Continue
            </button>
          </PickWheel>
        )}
        <button className="fr-link" onClick={() => setScreen("view")}>{backLabel}</button>

        {/* Manage-mode removal warning — one scoped confirm naming exactly what goes, same
            voice as the dustbins'. Confirming applies removals, then queues any adds. */}
        {subConfirm && (() => {
          const names = subConfirm.removes.join(", ");
          const classesOf = subConfirm.removes.map((n) => {
            const s = canon.find((x) => x.name === n);
            return s ? (s.grades || []).map((g) => `Class ${classNum(g.grade)}`).join(", ") : "";
          }).filter(Boolean).join(" · ");
          return (
            <div className="fr-modal-bg" onClick={(e) => { if (e.currentTarget === e.target) setSubConfirm(null); }}>
              <div className="fr-modal">
                <h2 className="fr-q">Remove {names}?</h2>
                <p className="fr-hint">{classesOf || "Its classes"} — all cards and bookmarks — will be removed. Your lessons stay in the library.</p>
                <button type="button" className="tp-remove-confirm" onClick={applySubjectChanges}>Yes, remove {names}</button>
                <button type="button" className="fr-link fr-center" onClick={() => setSubConfirm(null)}>Keep {subConfirm.removes.length === 1 ? "it" : "them"}</button>
              </div>
            </div>
          );
        })()}
      </div>
    );
  }

  if (screen === "classes") {
    const manageC = classMode === "manage";
    const have = draft.grades.map((g) => g.grade);
    const options = manageC ? gradeOptions : gradeOptions.filter((g) => !have.includes(g));
    const toggle = (roman) => setPicked((a) => (a.includes(roman) ? a.filter((x) => x !== roman) : [...a, roman]));
    const adding = have.length > 0; // add-a-class on an existing subject vs a brand-new subject
    return (
      <div className="tp">
        <div className="kicker kicker-ochre">{manageC ? `${draft.name} · classes` : `${draft.name}${queue.length > 1 ? ` · subject ${qi + 1} of ${queue.length}` : ""}`}</div>
        <h1 className="fr-q">{manageC ? `Which classes do you teach ${draft.name} to?`
          : adding ? `Which classes are you adding for ${draft.name}?` : `Which classes do you teach ${draft.name} to?`}</h1>
        {manageC && <p className="fr-hint">Tick a class to add it — untick one to remove it.</p>}
        {!manageC && adding && <p className="fr-hint">Your current classes stay as they are — pick only the new ones.</p>}
        {gradeOptions.length === 0 && <div className="fr-loading">Loading classes…</div>}
        {gradeOptions.length > 0 && options.length === 0 && (
          <p className="fr-hint">Every class Aruvi offers for {draft.name} is already in your profile.</p>
        )}
        {options.length > 0 && (
          <PickWheel options={options} selected={picked} onToggle={toggle}
            ariaLabel={`Classes for ${draft.name}`} labelFor={(g) => `Class ${classNum(g)}`}>
            <button type="button" className="primary fr-cta" disabled={manageC ? false : !picked.length}
              onClick={manageC ? onManageClassesContinue : onClassesContinue}>
              Continue
            </button>
          </PickWheel>
        )}

        {/* Manage-mode removal warning — names the classes AND their section cards; if nothing
            is left the subject goes with them (warned, never blocked). */}
        {classConfirm && (() => {
          const names = classConfirm.removes.map((r) => `Class ${classNum(r)}`).join(", ");
          const tags = classConfirm.removes.map((roman) => {
            const g = draft.grades.find((x) => x.grade === roman);
            return g && g.sections.length ? g.sections.map((sec) => `${classNum(roman)}${sec}`).join(", ") : `Class ${classNum(roman)}`;
          }).join(", ");
          const allGone = classConfirm.removes.length === draft.grades.length && !classConfirm.adds.length;
          return (
            <div className="fr-modal-bg" onClick={(e) => { if (e.currentTarget === e.target) setClassConfirm(null); }}>
              <div className="fr-modal">
                <h2 className="fr-q">Remove {names} from {draft.name}?</h2>
                <p className="fr-hint">{tags} — their cards and bookmarks — will be removed.{allGone ? ` No class is left — ${draft.name} goes with it.` : ""} Your lessons stay in the library.</p>
                <button type="button" className="tp-remove-confirm" onClick={applyClassChanges}>Yes, remove {names}</button>
                <button type="button" className="fr-link fr-center" onClick={() => setClassConfirm(null)}>Keep {classConfirm.removes.length === 1 ? "it" : "them"}</button>
              </div>
            </div>
          );
        })()}
        <button className="fr-link" onClick={() => setScreen("view")}>{backLabel}</button>
      </div>
    );
  }

  if (screen === "class") {
    const g = draft.grades[gIdx];
    const kicker = `${draft.name} · Class ${classNum(g.grade)} · ${pi + 1} of ${pendingIdxs.length}`;

    if (classStep === "sections") {
      const toggle = (s) => updGrade({
        sections: g.sections.includes(s) ? g.sections.filter((x) => x !== s) : [...g.sections, s].sort(),
      });
      return (
        <div className="tp">
          <div className="kicker kicker-ochre">{kicker}</div>
          <h1 className="fr-q">Which sections of Class {classNum(g.grade)}?</h1>
          <p className="fr-hint">Every ticked section gets its own class card and its own bookmark.</p>
          <PickWheel options={SECTION_LETTERS} selected={g.sections} onToggle={toggle}
            ariaLabel={`Sections of Class ${classNum(g.grade)}`} labelFor={(s) => `Section ${classNum(g.grade)}${s}`}>
            <button type="button" className="primary fr-cta" disabled={!g.sections.length}
              onClick={() => setClassStep("durations")}>
              Continue
            </button>
          </PickWheel>
          <button className="fr-link" onClick={() => setScreen("view")}>{backLabel}</button>
        </div>
      );
    }

    if (classStep === "durations") {
      const toggle = (d) => updGrade({
        durations: g.durations.includes(d)
          ? (g.durations.length > 1 ? g.durations.filter((x) => x !== d) : g.durations)
          : [...g.durations, d].sort((x, y) => x - y),
      });
      return (
        <div className="tp">
          <div className="kicker kicker-ochre">{kicker}</div>
          <h1 className="fr-q">How long are your {draft.name} periods for Class {classNum(g.grade)}?</h1>
          <p className="fr-hint">If more than one duration, select multiple.</p>
          <PickWheel options={DURATION_CHOICES} selected={g.durations} onToggle={toggle}
            ariaLabel="Period durations" labelFor={(d) => `${d} min`} initialScrollTo={DEFAULT_DURATION}>
            <button type="button" className="primary fr-cta" onClick={() => {
              // Reconcile the per-duration weekly-count map to whatever durations she just chose,
              // so the next screen (and the budget total) reflect the current set immediately.
              const nextMap = normPpw(g.durations, g.ppw_by_duration, g.periods_per_week);
              updGrade({ ppw_by_duration: nextMap, periods_per_week: ppwMapSum(nextMap) });
              setClassStep("ppw");
            }}>Continue</button>
          </PickWheel>
          <button className="fr-link" onClick={() => setClassStep("sections")}>← Back</button>
        </div>
      );
    }

    if (classStep === "ppw") {
      const map = normPpw(g.durations, g.ppw_by_duration, g.periods_per_week);
      const multi = (g.durations || []).length > 1;
      const setCount = (d, v) => {
        const next = { ...map, [d]: Math.max(1, Number(v) || 1) };
        updGrade({ ppw_by_duration: next, periods_per_week: ppwMapSum(next) });
      };
      return (
        <div className="tp">
          <div className="kicker kicker-ochre">{kicker}</div>
          <h1 className="fr-q">{multi
            ? `How many periods a week for each duration?`
            : `How many periods a week does Class ${classNum(g.grade)} get for ${draft.name}?`}</h1>
          <p className="fr-hint">{multi
            ? "One row per duration — Aruvi adds them up. No timetable, just counts."
            : "A number, not a timetable — Aruvi never asks which days."}</p>
          <PpwCapture durations={g.durations} map={map} onSet={setCount} />
          <div className="fr-foot">
            <button className="primary fr-cta" onClick={() => setClassStep("budget")}>Continue</button>
            <button className="fr-link" onClick={() => setClassStep("durations")}>← Back</button>
          </div>
        </div>
      );
    }

    /* budget */
    const ppw = g.periods_per_week || DEFAULT_PPW;
    const rawB = g.budget || { method: "weeks", value: defaultValueFor("weeks", ppw) };
    const b = rawB.method === "auto"
      ? { method: "auto", value: ppw * ESTIMATE_WEEKS }
      : rawB;
    const setMethod = (m) => updGrade({ budget: { method: m, value: defaultValueFor(m, ppw) } });
    const stepValue = (delta) => updGrade({ budget: { ...b, value: Math.max(0, b.value + delta) } });
    const setValue = (v) => updGrade({ budget: { ...b, value: Math.max(0, v) } });
    const isLast = pi + 1 >= pendingIdxs.length;
    return (
      <div className="tp">
        <div className="kicker kicker-ochre">{kicker}</div>
        <h1 className="fr-q">How long is your teaching year for Class {classNum(g.grade)}?</h1>
        <p className="fr-hint">Pick one method below based on what you know.</p>
        <div className="tp-methods">
          {METHOD_ORDER.map((m) => (
            <button type="button" key={m} className={`tp-method ${b.method === m ? "on" : ""}`} onClick={() => setMethod(m)}>
              {METHODS[m].label}
            </button>
          ))}
        </div>
        {b.method !== "auto" && (
          <div className="tp-val-row">
            <button type="button" className="tp-val-btn" onClick={() => stepValue(-METHODS[b.method].step)} aria-label="Less">−</button>
            <input type="number" className="tp-val-input" min="0" value={b.value}
              onChange={(e) => setValue(parseInt(e.target.value, 10) || 0)} aria-label={METHODS[b.method].unit} />
            <button type="button" className="tp-val-btn" onClick={() => stepValue(METHODS[b.method].step)} aria-label="More">+</button>
            <span className="tp-val-unit">{METHODS[b.method].unit}</span>
          </div>
        )}
        {b.method === "auto" && (
          <p className="tp-estimate-tag">{ncfTotal != null ? `As per NCF, this class is ${ncfTotal} periods` : "No NCF figure for this class"}</p>
        )}
        <p className="tp-total">≈ {budgetPeriods(ppw, b)} periods for the year, at {ppw} a week</p>
        {b.method === "auto" && (
          <p className="tp-estimate-sub">(based on a 30-week year)</p>
        )}
        <div className="fr-foot">
          <button className="primary fr-cta" onClick={() => { updGrade({ budget: b }); onClassDone(); }}>
            {isLast ? "Save ✓" : "Next class →"}
          </button>
          <button className="fr-link" onClick={() => setClassStep("ppw")}>← Back</button>
        </div>
      </div>
    );
  }

  if (screen === "subjectDone") {
    return (
      <div className="tp">
        <div className="kicker kicker-ochre">Teaching profile</div>
        <div className="fr-ready-note">
          <span className="fr-ready-check">✓</span>
          <div className="fr-ready-text">
            <strong>{draft.name} saved.</strong>
            <span>You can continue now, or come back for the rest later.</span>
          </div>
        </div>
        <div className="fr-foot">
          <button className="primary fr-cta" onClick={() => { const n = qi + 1; setQi(n); beginSubjectRun(queue[n]); }}>
            Continue to {queue[qi + 1]} →
          </button>
          <button className="fr-link fr-center" onClick={() => setScreen("view")}>Finish for now</button>
        </div>
      </div>
    );
  }

  if (screen === "addSection") {
    const { si, gi } = numCtx;
    const sub = canon[si]; const g = sub.grades[gi];
    const have = g.sections.map(secLetter);
    const options = SECTION_LETTERS.filter((s) => !have.includes(s));
    const toggle = (s) => setPicked((a) => (a.includes(s) ? a.filter((x) => x !== s) : [...a, s]));
    return (
      <div className="tp">
        <div className="kicker kicker-ochre">{sub.name} · Class {classNum(g.grade)} · sections</div>
        <h1 className="fr-q">Add sections to Class {classNum(g.grade)}</h1>
        <p className="fr-hint">You already have {have.map((s) => `${classNum(g.grade)}${s}`).join(", ")}. Tick the new ones.</p>
        <PickWheel options={options} selected={picked} onToggle={toggle}
          ariaLabel="Sections to add" labelFor={(s) => `Section ${classNum(g.grade)}${s}`}>
          <button type="button" className="primary fr-cta" disabled={!picked.length} onClick={saveAddSection}>Save</button>
        </PickWheel>
        <button className="fr-link" onClick={() => setScreen("view")}>{backLabel}</button>
      </div>
    );
  }

  if (screen === "editSections") {
    const { si, gi } = numCtx;
    const sub = canon[si]; const g = sub.grades[gi];
    const toggle = (s) => setPicked((a) => (a.includes(s) ? a.filter((x) => x !== s) : [...a, s]));
    return (
      <div className="tp">
        <div className="kicker kicker-ochre">{sub.name} · Class {classNum(g.grade)} · sections</div>
        <h1 className="fr-q">Edit sections of Class {classNum(g.grade)}</h1>
        <p className="fr-hint">Tick to keep or add a section, untick to remove one. A removed section loses its bookmark — your lessons stay in the library. To remove the whole class, use the basket on the class.</p>
        <PickWheel options={SECTION_LETTERS} selected={picked} onToggle={toggle}
          ariaLabel="Sections" labelFor={(s) => `Section ${classNum(g.grade)}${s}`}>
          <button type="button" className="primary fr-cta" disabled={!picked.length} onClick={requestEditSections}>Save</button>
        </PickWheel>
        <button className="fr-link" onClick={() => setScreen("view")}>{backLabel}</button>

        {secConfirm && (
          <div className="fr-modal-bg" onClick={(e) => { if (e.currentTarget === e.target) setSecConfirm(null); }}>
            <div className="fr-modal">
              <h2 className="fr-q">Remove {secConfirm.removed.join(", ")}?</h2>
              <p className="fr-hint">{secConfirm.removed.length === 1 ? "Its card and bookmark" : "Their cards and bookmarks"} will be removed. Your lessons stay in the library.</p>
              <button type="button" className="tp-remove-confirm" onClick={applyEditSections}>Yes, remove {secConfirm.removed.join(", ")}</button>
              <button type="button" className="fr-link fr-center" onClick={() => setSecConfirm(null)}>Keep {secConfirm.removed.length === 1 ? "it" : "them"}</button>
            </div>
          </div>
        )}
      </div>
    );
  }

  if (screen === "editNums") {
    const { si, gi, g, step } = numCtx;
    const sub = canon[si];
    const kicker = `${sub.name} · Class ${classNum(g.grade)}`;

    if (step === "duration") {
      const toggle = (d) => updNum({
        durations: g.durations.includes(d)
          ? (g.durations.length > 1 ? g.durations.filter((x) => x !== d) : g.durations)
          : [...g.durations, d].sort((x, y) => x - y),
      });
      const multi = g.durations.length > 1;
      return (
        <div className="tp">
          <div className="kicker kicker-ochre">{kicker} · duration</div>
          <h1 className="fr-q">How long are the periods?</h1>
          <p className="fr-hint">If more than one duration, select multiple.</p>
          <PickWheel options={DURATION_CHOICES} selected={g.durations} onToggle={toggle}
            ariaLabel="Period durations" labelFor={(d) => `${d} min`} initialScrollTo={g.durations[0]}>
            {multi ? (
              // >1 duration → go on to ask the weekly count per type (reconcile the map first)
              <button type="button" className="primary fr-cta" onClick={() => {
                const nextMap = normPpw(g.durations, g.ppw_by_duration, g.periods_per_week);
                setNumCtx((c) => ({ ...c, g: { ...c.g, ppw_by_duration: nextMap, periods_per_week: ppwMapSum(nextMap) }, step: "ppw" }));
              }}>Continue</button>
            ) : (
              <button type="button" className="primary fr-cta" onClick={() => saveEditNums()}>Save</button>
            )}
          </PickWheel>
          <button className="fr-link" onClick={() => setScreen("view")}>Cancel</button>
        </div>
      );
    }

    if (step === "ppw") {
      const map = normPpw(g.durations, g.ppw_by_duration, g.periods_per_week);
      const multi = (g.durations || []).length > 1;
      const setCount = (d, v) => {
        const next = { ...map, [d]: Math.max(1, Number(v) || 1) };
        updNum({ ppw_by_duration: next, periods_per_week: ppwMapSum(next) });
      };
      return (
        <div className="tp">
          <div className="kicker kicker-ochre">{kicker} · periods / week</div>
          <h1 className="fr-q">{multi ? "How many periods a week for each duration?" : "How many periods a week?"}</h1>
          {multi && <p className="fr-hint">One row per duration — Aruvi adds them up.</p>}
          <PpwCapture durations={g.durations} map={map} onSet={setCount} />
          <div className="fr-foot">
            <button className="primary fr-cta" onClick={() => saveEditNums()}>Save</button>
            <button className="fr-link" onClick={() => setScreen("view")}>Cancel</button>
          </div>
        </div>
      );
    }

    const ppw = g.periods_per_week || DEFAULT_PPW;
    const rawB = g.budget || { method: "weeks", value: defaultValueFor("weeks", ppw) };
    const b = rawB.method === "auto"
      ? { method: "auto", value: ppw * ESTIMATE_WEEKS }
      : rawB;
    const setMethod = (m) => updNum({ budget: { method: m, value: defaultValueFor(m, ppw) } });
    const stepValue = (delta) => updNum({ budget: { ...b, value: Math.max(0, b.value + delta) } });
    const setValue = (v) => updNum({ budget: { ...b, value: Math.max(0, v) } });
    return (
      <div className="tp">
        <div className="kicker kicker-ochre">{kicker} · annual budget</div>
        <h1 className="fr-q">How long is the teaching year?</h1>
        <p className="fr-hint">Pick one method below based on what you know.</p>
        <div className="tp-methods">
          {METHOD_ORDER.map((m) => (
            <button type="button" key={m} className={`tp-method ${b.method === m ? "on" : ""}`} onClick={() => setMethod(m)}>
              {METHODS[m].label}
            </button>
          ))}
        </div>
        {b.method !== "auto" && (
          <div className="tp-val-row">
            <button type="button" className="tp-val-btn" onClick={() => stepValue(-METHODS[b.method].step)} aria-label="Less">−</button>
            <input type="number" className="tp-val-input" min="0" value={b.value}
              onChange={(e) => setValue(parseInt(e.target.value, 10) || 0)} aria-label={METHODS[b.method].unit} />
            <button type="button" className="tp-val-btn" onClick={() => stepValue(METHODS[b.method].step)} aria-label="More">+</button>
            <span className="tp-val-unit">{METHODS[b.method].unit}</span>
          </div>
        )}
        {b.method === "auto" && (
          <p className="tp-estimate-tag">{ncfTotal != null ? `As per NCF, this class is ${ncfTotal} periods` : "No NCF figure for this class"}</p>
        )}
        <p className="tp-total">≈ {budgetPeriods(ppw, b)} periods for the year, at {ppw} a week</p>
        {b.method === "auto" && (
          <p className="tp-estimate-sub">(based on a 30-week year)</p>
        )}
        <div className="fr-foot">
          <button className="primary fr-cta" onClick={() => saveEditNums(b)}>Save</button>
          <button className="fr-link" onClick={() => setScreen("view")}>Cancel</button>
        </div>
      </div>
    );
  }

  /* ════════════════════ VIEW — the accordion ════════════════════ */
  // headline totals across the whole profile
  const stats = (() => {
    const classSet = new Set(); const secSet = new Set(); let ppw = 0;
    canon.forEach((s) => (s.grades || []).forEach((g) => {
      classSet.add(classNum(g.grade));
      (g.sections || []).forEach((x) => secSet.add(`${classNum(g.grade)}${secLetter(x)}`));
      ppw += g.periods_per_week || 0;
    }));
    return { subjects: canon.length, classes: classSet.size, sections: secSet.size, ppw };
  })();

  return (
    <div className="tp" ref={rootRef}>
      <div className="tp-sticky">
        {onBack && (
          <button className="tp-back" onClick={onBack}>← Back to My Classes</button>
        )}
        <div className="tp-hd">
          <div>
            <h1 className="lvl-title">Your teaching profile</h1>
            <div className="tp-hd-spacer" aria-hidden="true"></div>
          </div>
          {canon.length > 0 && (
            editing ? (
              <button className="tp-edit-toggle on" onClick={() => setEditing(false)} aria-label="Done editing">Done</button>
            ) : (
              <button className="tp-edit-pencil" onClick={() => setEditing(true)} aria-label="Edit profile" title="Edit profile">
                <Pencil size={22} />
              </button>
            )
          )}
        </div>

        {canon.length === 0 && (
          <p className="tp-empty">No profile yet — add a subject to begin.</p>
        )}

        {canon.length > 0 && (
          <div className="tp-stats">
            <div className="tp-stat"><span className="tp-stat-n">{stats.subjects}</span><span className="tp-stat-l">Subjects</span></div>
            <div className="tp-stat"><span className="tp-stat-n">{stats.classes}</span><span className="tp-stat-l">Classes</span></div>
            <div className="tp-stat"><span className="tp-stat-n">{stats.sections}</span><span className="tp-stat-l">Sections</span></div>
            <div className="tp-stat"><span className="tp-stat-n">{stats.ppw}</span><span className="tp-stat-l">Periods / week</span></div>
          </div>
        )}
      </div>

      {canon.map((s, si) => {
        const open = s.name === openSubject;
        const subPpw = (s.grades || []).reduce((a, g) => a + (g.periods_per_week || 0), 0);
        return (
          <div className={`tp-sub ${open ? "open" : ""}`} key={s.name}>
            <div className="tp-sub-hd" onClick={() => setOpenSubject(open ? null : s.name)}>
              <span className="tp-sub-left">
                <span className="tp-sub-name">{s.name}</span>
                {editing && open && (
                  <button className="tp-bin" aria-label={`Remove ${s.name}`}
                    onClick={(e) => { e.stopPropagation(); setConfirm({ kind: "subject", si }); }}><Bin /></button>
                )}
              </span>
              <span className="tp-sub-side">
                <span className="tp-sub-ppw">{subPpw} periods / week</span>
                <span className="tp-caret">{open ? "▾" : "▸"}</span>
              </span>
            </div>

            {open && (s.grades || []).map((g, gi) => {
              const ppw = g.periods_per_week;
              const b = (s.budget || {})[gi] ?? (s.budget || {})[String(gi)];
              const total = ppw && b ? budgetPeriods(ppw, b) : null;
              // Periods/week: total-forward number, with the per-duration split as a caption right
              // below it ("6×40 · 1×50"). The caption is ABSOLUTELY positioned (.tp-cc-col-cap) so
              // it sits in the card's bottom padding instead of making the centre column taller than
              // Duration/Budget — that height difference was what left an empty row under the card.
              // Single-duration classes show just the number, no caption.
              const durs = g.durations || [];
              const pmap = g.ppw_by_duration || {};
              const perWeekBreakdown = durs.length > 1
                ? durs.map((d) => `${pmap[d] ?? pmap[String(d)] ?? "—"}×${d}`).join(" · ")
                : null;
              return (
                <div className="tp-classcard" key={g.grade}>
                  <div className="tp-cc-hd">
                    <span className="tp-cc-left">
                      <span className="tp-cc-name">Class {classNum(g.grade)}</span>
                      {editing && (
                        <button className="tp-bin" aria-label={`Remove Class ${classNum(g.grade)}`}
                          onClick={() => setConfirm({ kind: "grade", si, gi })}><Bin /></button>
                      )}
                    </span>
                    <div className="tp-cc-right">
                      <span className="tp-cc-seclbl">Sections</span>
                      <div className="tp-chips">
                        {(g.sections || []).map((x) => {
                          const sec = secLetter(x);
                          return (
                            <span className="tp-chip" key={sec}>{classNum(g.grade)}{sec}</span>
                          );
                        })}
                      </div>
                      {editing && (
                        <button className="tp-icon-btn" aria-label={`Edit sections of Class ${classNum(g.grade)}`}
                          onClick={() => startEditSections(si, gi)}><Pencil /></button>
                      )}
                    </div>
                  </div>
                  <div className="tp-cc-cols">
                    <div className="tp-cc-col">
                      <div className="tp-cc-col-l">Duration
                        {editing && (
                          <button className="tp-icon-btn tp-icon-xs" aria-label={`Edit duration of Class ${classNum(g.grade)}`}
                            onClick={() => startEditNums(si, gi, "duration")}><Pencil size={12} /></button>
                        )}
                      </div>
                      <div className="tp-cc-col-v">{(g.durations || []).join("/")} min</div>
                    </div>
                    <div className="tp-cc-col tp-cc-col--center">
                      <div className="tp-cc-col-l">Periods / week
                        {editing && (
                          <button className="tp-icon-btn tp-icon-xs" aria-label={`Edit periods per week of Class ${classNum(g.grade)}`}
                            onClick={() => startEditNums(si, gi, "ppw")}><Pencil size={12} /></button>
                        )}
                      </div>
                      <div className="tp-cc-col-v">{ppw || "—"}</div>
                      {perWeekBreakdown && <div className="tp-cc-col-cap">{perWeekBreakdown}</div>}
                    </div>
                    <div className="tp-cc-col">
                      <div className="tp-cc-col-l">Annual budget
                        {editing && (
                          <button className="tp-icon-btn tp-icon-xs" aria-label={`Edit annual budget of Class ${classNum(g.grade)}`}
                            onClick={() => startEditNums(si, gi, "budget")}><Pencil size={12} /></button>
                        )}
                      </div>
                      <div className="tp-cc-col-v">{total ? `${total} periods` : "—"}</div>
                    </div>
                  </div>
                </div>
              );
            })}

            {open && editing && (
              <button className="tp-add" onClick={() => startAddClass(si)}>+ add a class</button>
            )}
          </div>
        );
      })}

      {(editing || canon.length === 0) && (
        <button className="tp-add tp-add-subject" onClick={startAddSubject}>+ add a subject</button>
      )}

      {confirm && (() => {
        const c = confirmCopy();
        return (
          <div className="fr-modal-bg" onClick={(e) => { if (e.currentTarget === e.target) setConfirm(null); }}>
            <div className="fr-modal">
              <h2 className="fr-q">{c.title}</h2>
              <p className="fr-hint">{c.body}</p>
              <button type="button" className="tp-remove-confirm" onClick={doRemove}>{c.cta}</button>
              <button type="button" className="fr-link fr-center" onClick={() => setConfirm(null)}>Keep it</button>
            </div>
          </div>
        );
      })()}
    </div>
  );
}
