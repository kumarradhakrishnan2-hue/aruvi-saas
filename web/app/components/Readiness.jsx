"use client";
import { useState } from "react";
import useSupportedGrades from "../lib/useSupportedGrades";

/* ───────── Readiness setup (Phase 2) ─────────
 * Conversational, one-question-per-screen setup. Two halves:
 *
 *   PART A — "Tell us what you teach" (steps 1–4, added 2026-06-27):
 *     1. subjects          → which subjects do you teach
 *     2. grades            → which grades, per subject
 *     3. sections          → which sections, per subject·grade
 *     4. durations         → which class durations exist, per subject·grade
 *
 *   PART B — the weekly reality (ported from docs/mockups/readiness-grid-flow.html):
 *     5. grid              → tap/hold weekly grid (sections × days) per subject·grade
 *     6. budget            → annual budget per subject·grade (weeks / periods / days / estimate)
 *
 * Parts B steps loop per grade WITHIN each subject, and the whole thing loops per subject.
 * On finish it calls onComplete(payload) so the shell can flip `ready` and unlock Generate.
 *
 * ───────── CLOUD / SUPABASE PORTABILITY (Phase 4) ─────────
 * The object this component emits via onComplete() — `readiness` — IS the per-user/tenant
 * "teaching profile". Today it lives only in front-end React state + (downstream) localStorage.
 * Phase 4 moves it verbatim into Supabase, keyed by user/tenant. To make that a drop-in:
 *   • The canonical shape is the `subjects[]` array (see buildPayload below). Each element is a
 *     fully self-contained per-subject record — subject, its grades, each grade's sections,
 *     the subject's durations, the per-grade weekly grid, and the per-grade annual budget.
 *     That array maps 1:1 to a `readiness_subjects` table (one row per subject, JSONB columns
 *     for grids/budget) OR to normalized child tables (subjects → grades → sections → grids).
 *   • The TOP-LEVEL keys (subject / grades / grids / durations / budget) are a DENORMALIZED
 *     "active subject" projection kept ONLY for backward compatibility with the current
 *     consumers (MyPlans.classesFromReadiness, Allocate.weeklyRatioFromReadiness). They are
 *     NOT the source of truth and should NOT be persisted as their own table — derive them
 *     from subjects[] at read time. See the DB-MAPPING block on buildPayload().
 * No persistence calls live in this file by design: the seam is onComplete(payload) → shell.
 */

const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const WORK_WEEK = 6;        // 6-day week → days ÷ 6 = weeks
const ESTIMATE_WEEKS = 30;  // "not sure" estimate

const METHODS = {
  weeks:   { label: "I know my teaching weeks", unit: "weeks",         step: 1 },
  periods: { label: "I know my period count",   unit: "periods / year", step: 1 },
  days:    { label: "I know my working days",   unit: "working days",  step: 6 },
  auto:    { label: "I’m not sure — estimate it", unit: "",            step: 0 },
};
const METHOD_ORDER = ["weeks", "periods", "days", "auto"];

// Picklists for the conversational collection steps.
const SUBJECT_CHOICES = ["Science", "Mathematics", "Social Sciences", "English", "The World Around Us"];
// Grade choices are NOT a fixed list here — they come per-subject from useSupportedGrades (shared
// with My Class), so the grade step only offers grades Aruvi has chapters for.
// Sections paged 3 at a time; extended A–Z so a teacher can keep asking for "more" indefinitely.
const SECTION_CHOICES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
const SECTION_PAGE = 3;
// Durations paged 4 at a time: from 30 min upward in 5-min steps; teacher asks for "more" as needed.
const DURATION_CHOICES = Array.from({ length: 25 }, (_, i) => 30 + i * 5); // 30,35,…150
const DURATION_PAGE = 4;
// Roman grade → arabic, for building section tags like "6A".
const GRADE_ARABIC = { III: 3, IV: 4, V: 5, VI: 6, VII: 7, VIII: 8, IX: 9, X: 10 };
const sectionTag = (gradeRoman, sec) => `${GRADE_ARABIC[gradeRoman] || gradeRoman}${sec}`;

// Total step count for the "Step N of M" progress line: 4 collection steps + grid + budget.
const TOTAL_STEPS = 6;

/* Reverse buildPayload(): turn a saved readiness `subjects[]` record back into the internal
 * authoring shape this component edits — sections as plain strings, plus the grids/budgets
 * maps keyed the way PART B reads them. Used only for the edit-mode pre-fill. */
function hydrateFromReadiness(readiness) {
  const src = (readiness && readiness.subjects) || [];
  const profile = {
    subjects: src.map((s) => ({
      name: s.name,
      grades: (s.grades || []).map((g) => ({
        grade: g.grade,
        sections: (g.sections || []).map((sec) => (typeof sec === "string" ? sec : sec.sec)),
        durations: [...(g.durations || [])],
      })),
    })),
  };
  const grids = {};
  const budgets = {};
  src.forEach((s, sIdx) => {
    if (Array.isArray(s.grids)) grids[sIdx] = s.grids;
    const b = s.budget || {};
    (s.grades || []).forEach((_, gIdx) => {
      const entry = b[gIdx] ?? b[String(gIdx)];
      if (entry) budgets[`${sIdx}:${gIdx}`] = entry;
    });
  });
  // Seed the default method from the first grade that has one, so the budget step opens on it.
  const firstBudget = budgets["0:0"];
  return { profile, grids, budgets, defaultMethod: (firstBudget && firstBudget.method) || "weeks" };
}

export default function Readiness({ subject: subjectProp, onComplete, initialReadiness = null, startPhase = "subjects", calendarOnly = false }) {
  // Edit-mode pre-fill: when an existing profile is handed in, reverse it into the authoring
  // shape so every step shows the teacher's real answers instead of blanks. One-time seed.
  const seed = initialReadiness ? hydrateFromReadiness(initialReadiness) : null;

  /* ───────── PART A collected state ─────────
   * `profile` is the authoritative collected structure during setup:
   *   profile.subjects: [{ name, grades: [{ grade, sections: ["A","B"], durations: [45,60] }] }]
   * Starts EMPTY for first-time setup; pre-filled in edit mode (seed above).
   * (`subjectProp` is no longer used to seed a default; kept for API compatibility.) */
  const [profile, setProfile] = useState(() => (seed ? seed.profile : { subjects: [] }));

  // Where we are. Phases A1..A4 are global; "grid"/"budget" loop per (subject, grade).
  // startPhase lets an edit link drop the teacher straight onto the relevant screen
  // ("subjects" for profile edits, "durations" for calendar edits).
  const [phase, setPhase] = useState(startPhase); // subjects | grades | sections | durations | grid | budget
  const [si, setSi] = useState(0);   // active subject index (grades/sections/durations/grid/budget)
  const [gi, setGi] = useState(0);   // active grade index within current subject (grid loop)
  const [bi, setBi] = useState(0);   // active grade index within current subject (budget loop)

  // Durations are collected PER SUBJECT·GRADE (in step 4, like sections) and stored on each
  // grade as grade.durations. The grid/budget read the active grade's durations (curDur below).

  // PART B working state (built lazily once collection is done; pre-seeded in edit mode).
  const [grids, setGrids] = useState(() => (seed ? seed.grids : {}));   // { `${si}` : [grade][section][day] = durIdx|-1 }
  const [budgets, setBudgets] = useState(() => (seed ? seed.budgets : {})); // { `${si}:${gradeIdx}` : { method, value } }
  const [defaultMethod, setDefaultMethod] = useState(() => (seed ? seed.defaultMethod : "weeks"));
  const [showAlt, setShowAlt] = useState(false);

  const subjects = profile.subjects;
  // Safe fallback so derived render-time reads (curSubject.grades/.durations below) never throw
  // while no subject is chosen yet (the subjects step doesn't use these values).
  const EMPTY_SUBJECT = { name: "", grades: [] };
  const curSubject = subjects[si] || subjects[0] || EMPTY_SUBJECT;

  // Grade choices restricted to what this subject actually supports — via the SHARED hook so the
  // rule is identical to My Class's editor (one source of truth in lib/useSupportedGrades).
  const gradeChoicesForSubject = useSupportedGrades(curSubject.name);

  // Per-subject pass marker (2a/2b/3a/3b…): only when the teacher has more than one subject.
  const multiSubject = subjects.length > 1;
  const passSuffix = multiSubject ? String.fromCharCode(97 + si) : "";   // 0→"a", 1→"b"…
  const passSubjectName = multiSubject ? curSubject.name : "";

  /* ════════════════════ helpers — PART A mutation ════════════════════ */
  const updateProfile = (mut) => setProfile((p) => {
    const next = { subjects: p.subjects.map((s) => ({ ...s, grades: s.grades.map((g) => ({ ...g, sections: [...g.sections], durations: [...(g.durations || [])] })) })) };
    mut(next);
    return next;
  });

  // step 1 — subjects (none pre-selected; teacher may select/deselect any, including the last)
  const toggleSubject = (name) => updateProfile((p) => {
    const idx = p.subjects.findIndex((s) => s.name === name);
    if (idx >= 0) p.subjects.splice(idx, 1);
    else p.subjects.push({ name, grades: [] });
  });

  // step 2 — grades (for current subject)
  const toggleGrade = (g) => updateProfile((p) => {
    const sub = p.subjects[si];
    const idx = sub.grades.findIndex((x) => x.grade === g);
    if (idx >= 0) sub.grades.splice(idx, 1);
    else sub.grades.push({ grade: g, sections: [], durations: [] });
    sub.grades.sort((a, b) => (GRADE_ARABIC[a.grade] || 0) - (GRADE_ARABIC[b.grade] || 0));
  });

  // step 3 — sections (per grade of current subject)
  const toggleSection = (gradeRoman, sec) => updateProfile((p) => {
    const sub = p.subjects[si];
    const gr = sub.grades.find((x) => x.grade === gradeRoman);
    if (!gr) return;
    const idx = gr.sections.indexOf(sec);
    if (idx >= 0) gr.sections.splice(idx, 1);   // allow unclicking down to zero
    else gr.sections.push(sec);
    gr.sections.sort();
  });

  // step 4 — durations (per subject·grade, like sections)
  const toggleDuration = (gradeRoman, d) => updateProfile((p) => {
    const sub = p.subjects[si];
    const gr = sub.grades.find((x) => x.grade === gradeRoman);
    if (!gr) return;
    if (!gr.durations) gr.durations = [];
    const idx = gr.durations.indexOf(d);
    if (idx >= 0) gr.durations.splice(idx, 1);     // allow unclicking down to zero
    else gr.durations.push(d);
    gr.durations.sort((a, b) => a - b);
  });

  /* ════════════════════ helpers — PART B (grid + budget) ════════════════════ */
  // Lazily ensure a grid exists for subject si shaped [grade][section][day].
  const ensureGrid = (sIdx) => {
    setGrids((all) => {
      if (all[sIdx]) return all;
      const sub = subjects[sIdx];
      const g = sub.grades.map((gr) => gr.sections.map(() => DAYS.map(() => -1)));
      return { ...all, [sIdx]: g };
    });
  };
  const curGridSubject = grids[si] || (curSubject.grades.map((gr) => gr.sections.map(() => DAYS.map(() => -1))));
  const curGrade = curSubject.grades[gi] || curSubject.grades[0];
  const curDur = (curGrade && curGrade.durations && curGrade.durations.length) ? curGrade.durations : [45];

  const setCell = (r, c, val) => setGrids((all) => {
    const base = all[si] || curSubject.grades.map((gr) => gr.sections.map(() => DAYS.map(() => -1)));
    const next = { ...all, [si]: base.map((g) => g.map((row) => [...row])) };
    next[si][gi][r][c] = val;
    return next;
  });
  const cellVal = (r, c) => (curGridSubject[gi] && curGridSubject[gi][r] ? curGridSubject[gi][r][c] : -1);
  // Tap cycles through the grade's durations, then back to empty:
  //   single duration  → empty ↔ 45
  //   two durations    → empty → 45 → 60 → empty
  const tapCell = (r, c) => {
    const v = cellVal(r, c);
    const n = curDur.length;
    setCell(r, c, v < 0 ? 0 : (v + 1 >= n ? -1 : v + 1));
  };
  // (right-click also advances, as a shortcut)
  const holdCell = (r, c) => {
    const v = cellVal(r, c);
    setCell(r, c, v < 0 ? 0 : (v + 1) % curDur.length);
  };

  const sectionCount = (gradeIdx) => (curSubject.grades[gradeIdx]?.sections.length || 1);
  const weeklyPeriods = (gradeIdx) => {
    const g = curGridSubject[gradeIdx]; if (!g) return 0;
    let n = 0; g.forEach((row) => row.forEach((v) => { if (v >= 0) n++; }));
    return Math.round(n / sectionCount(gradeIdx));
  };
  const weeklyMinutes = (gradeIdx) => {
    const g = curGridSubject[gradeIdx]; if (!g) return 0;
    let m = 0; g.forEach((row) => row.forEach((v) => { if (v >= 0) m += curDur[v]; }));
    return Math.round(m / sectionCount(gradeIdx));
  };

  /* ---------- budget math ---------- */
  const defaultValueFor = (gradeIdx, method) => {
    if (method === "weeks") return 36;
    if (method === "periods") return weeklyPeriods(gradeIdx) * 36;
    if (method === "days") return 180;
    return 0;
  };
  const computeBudget = (gradeIdx, method, value) => {
    const wp = weeklyPeriods(gradeIdx);
    if (method === "weeks")   return { periods: wp * value, weeks: value };
    if (method === "periods") return { periods: value, weeks: wp ? value / wp : null };
    if (method === "days")    { const w = value / WORK_WEEK; return { periods: Math.round(wp * w), weeks: w }; }
    return { periods: wp * ESTIMATE_WEEKS, weeks: ESTIMATE_WEEKS };
  };
  const annualHours = (gradeIdx, weeks) => (weeks == null ? null : Math.round(weeklyMinutes(gradeIdx) * weeks / 60));

  const budKey = `${si}:${bi}`;
  const curBudget = budgets[budKey] || { method: defaultMethod, value: defaultValueFor(bi, defaultMethod) };
  const setBudgetMethod = (m) => {
    setBudgets((b) => ({ ...b, [budKey]: { method: m, value: defaultValueFor(bi, m) } }));
    if (si === 0 && bi === 0) setDefaultMethod(m);
  };
  const stepBudget = (delta) => setBudgets((b) => {
    const cur = b[budKey] || { method: defaultMethod, value: defaultValueFor(bi, defaultMethod) };
    return { ...b, [budKey]: { ...cur, value: Math.max(0, cur.value + delta) } };
  });

  /* ════════════════════ build final payload ════════════════════ */
  /* DB-MAPPING (Phase 4 / Supabase): the `subjects[]` array below is the CANONICAL,
   * fully-normalizable teaching profile. Persist THIS. The top-level active-subject
   * projection (grades/grids/durations/budget) is derived sugar for current consumers —
   * regenerate it on read, do not store it as its own table. */
  const buildPayload = () => {
    const subjectsOut = subjects.map((sub, sIdx) => {
      const grid = grids[sIdx] || sub.grades.map((gr) => gr.sections.map(() => DAYS.map(() => -1)));
      const perGradeBudget = {};
      sub.grades.forEach((_, gIdx) => {
        perGradeBudget[gIdx] = budgets[`${sIdx}:${gIdx}`] || { method: defaultMethod, value: defaultValueFor(gIdx, defaultMethod) };
      });
      return {
        name: sub.name,
        grades: sub.grades.map((gr) => ({
          grade: gr.grade,
          sections: gr.sections.map((sec) => ({ tag: sectionTag(gr.grade, sec), sec })),
          durations: [...(gr.durations || [])],   // per-grade class durations (minutes)
        })),
        grids: grid,                 // [grade][section][day] = durationIndex | -1
        budget: perGradeBudget,      // { gradeIdx: { method, value } }
      };
    });

    // Active-subject projection (backward compat with MyPlans / Allocate consumers).
    const active = subjectsOut[si] || subjectsOut[0];
    return {
      // canonical (persist this):
      subjects: subjectsOut,
      activeSubjectIndex: si,
      // derived active-subject projection (do NOT persist as source of truth):
      subject: active.name,
      grades: active.grades,
      durations: active.grades.map((gr) => gr.durations), // per-grade durations for legacy weeklyRatio/idx use
      grids: active.grids,
      budget: active.budget,
    };
  };

  /* ════════════════════ navigation ════════════════════
   * SUBJECT-MAJOR (2026-06-29): each subject runs its FULL setup before the next starts —
   * grades → sections → durations → weekly grid (all grades) → budget (all grades) → then the
   * NEXT subject's grades. Within a subject the phases run in order; only the budget step (the
   * subject's last) advances `si` to the next subject. `gi`/`bi` walk grades within the subject. */
  const lastSubject = si >= subjects.length - 1;

  const goFromSubjects = () => { if (subjects.length) { setSi(0); setPhase("grades"); } };

  // grades → sections (same subject)
  const goFromGrades = () => {
    if (!curSubject.grades.length) return;       // need ≥1 grade for this subject
    setPhase("sections");
  };

  // sections → durations (same subject)
  const sectionsComplete = curSubject.grades.every((gr) => gr.sections.length > 0);
  const goFromSections = () => {
    if (!sectionsComplete) return;
    setPhase("durations");
  };

  // durations → weekly grid (same subject, first grade)
  const durationsComplete = curSubject.grades.every((gr) => (gr.durations || []).length > 0);
  const goFromDurations = () => {
    if (!durationsComplete) return;
    setGi(0); ensureGrid(si); setPhase("grid");
  };

  // weekly grid → walk this subject's grades, then THIS subject's budget.
  const gridNext = () => {
    if (gi < curSubject.grades.length - 1) { setGi(gi + 1); return; }  // next grade, same subject
    setBi(0); setShowAlt(true); setPhase("budget");                   // this subject's grids done → its budget
  };
  const gridBack = () => {
    if (gi > 0) { setGi(gi - 1); return; }
    setPhase("durations");                                            // back to this subject's durations
  };

  // budget → walk this subject's grades; after the last grade, move to the NEXT subject's grades
  // (or finish). This is the single point where the flow advances from one subject to the next.
  const budBack = () => {
    if (bi > 0) { setBi(bi - 1); return; }
    setGi(curSubject.grades.length - 1); setPhase("grid");           // back to this subject's last grid
  };
  const budNext = () => {
    if (bi < curSubject.grades.length - 1) { setBi(bi + 1); setShowAlt(false); return; }  // next grade, same subject
    if (!lastSubject) {                                              // → next subject, start at its grades
      const ns = si + 1; setSi(ns); setGi(0); setBi(0); setShowAlt(false); setPhase("grades"); return;
    }
    onComplete && onComplete(buildPayload());                        // all subjects done → finish
  };

  /* ════════════════════ render ════════════════════ */

  // ---- Step 1: subjects ----
  if (phase === "subjects") {
    const chosen = subjects.map((s) => s.name);
    return (
      <div className="rd">
        <StepProgress n={1} />
        <div className="rd-hd">
          <div className="kicker">Let’s set up your year</div>
          <h2 className="rd-q">Tell us what you teach.</h2>
          <p className="rd-ask">Pick every subject you plan with Aruvi. You’ll only do this once.</p>
        </div>
        <MultiDropdown
          choices={SUBJECT_CHOICES}
          selected={chosen}
          onToggle={toggleSubject}
          placeholder="Choose your subjects"
        />
        <div className="rd-btns">
          <button className="primary" style={{ flex: 1 }} disabled={!chosen.length} onClick={goFromSubjects}>
            Continue →
          </button>
        </div>
      </div>
    );
  }

  // ---- Step 2: grades (per subject) ----
  if (phase === "grades") {
    const chosen = curSubject.grades.map((g) => g.grade);
    return (
      <div className="rd">
        <StepProgress n={2} suffix={passSuffix} subjectName={passSubjectName} />
        <div className="rd-hd">
          <div className="kicker">{curSubject.name}</div>
          <h2 className="rd-q">Which grades do you teach in {curSubject.name}?</h2>
          <p className="rd-ask">Choose each grade you take this subject for.</p>
        </div>
        <MultiDropdown
          choices={gradeChoicesForSubject}
          selected={chosen}
          onToggle={toggleGrade}
          render={(g) => `Grade ${g}`}
          placeholder="Choose your grades"
        />
        <div className="rd-btns">
          <button className="ghost" onClick={() => { if (si === 0) setPhase("subjects"); else { const ps = si - 1; setSi(ps); setBi(subjects[ps].grades.length - 1); setShowAlt(false); setPhase("budget"); } }}>
            {si === 0 ? "← subjects" : `← ${subjects[si - 1].name}`}
          </button>
          <button className="primary" style={{ flex: 1 }} disabled={!chosen.length} onClick={goFromGrades}>
            Continue →
          </button>
        </div>
      </div>
    );
  }

  // ---- Step 3: sections (per grade of subject) ----
  if (phase === "sections") {
    return (
      <div className="rd">
        <StepProgress n={3} suffix={passSuffix} subjectName={passSubjectName} />
        <div className="rd-hd">
          <h2 className="rd-q">Which sections do you teach in {curSubject.name}?</h2>
          <p className="rd-ask">Choose the sections you take for each grade. Three show at a time — tap “list more sections” for the next set.</p>
        </div>
        <div className="sec-groups">
          {curSubject.grades.map((gr) => (
            <div className="sec-group" key={gr.grade}>
              <div className="kicker sec-group-h">Grade {gr.grade}</div>
              <PagedDropdown
                choices={SECTION_CHOICES}
                pageSize={SECTION_PAGE}
                selected={gr.sections}
                onToggle={(sec) => toggleSection(gr.grade, sec)}
                placeholder="Choose your sections"
                moreLabel="list more sections"
              />
            </div>
          ))}
        </div>
        <div className="rd-btns">
          <button className="ghost" onClick={() => setPhase("grades")}>← grades</button>
          <button className="primary" style={{ flex: 1 }} disabled={!sectionsComplete} onClick={goFromSections}>
            Continue →
          </button>
        </div>
      </div>
    );
  }

  // ---- Step 4: durations (per subject·grade, like sections; 4a/4b per subject) ----
  if (phase === "durations") {
    return (
      <div className="rd">
        <StepProgress n={4} suffix={passSuffix} subjectName={passSubjectName} />
        <div className="rd-hd">
          <h2 className="rd-q">What is the duration of your classes in {curSubject.name}?</h2>
          <p className="rd-ask">Most teachers have just one. Add another only if some classes run longer. Three show at a time — tap “list more durations” for the next set.</p>
        </div>
        <div className="sec-groups">
          {curSubject.grades.map((gr) => (
            <div className="sec-group" key={gr.grade}>
              <div className="kicker sec-group-h">Grade {gr.grade}</div>
              <PagedDropdown
                choices={DURATION_CHOICES}
                pageSize={DURATION_PAGE}
                selected={gr.durations || []}
                onToggle={(d) => toggleDuration(gr.grade, d)}
                render={(d) => `${d} minutes`}
                placeholder="Choose your class durations"
                moreLabel="list more durations"
              />
            </div>
          ))}
        </div>
        <div className="rd-btns">
          {/* In calendar-edit mode durations is the entry screen — no back into sections. */}
          {!(calendarOnly && si === 0) && (
            <button className="ghost" onClick={() => setPhase("sections")}>← sections</button>
          )}
          <button className="primary" style={{ flex: 1 }} disabled={!durationsComplete} onClick={goFromDurations}>
            Continue to the weekly grid →
          </button>
        </div>
      </div>
    );
  }

  // ---- Step 5: weekly grid (per subject·grade) ----
  if (phase === "grid") {
    const ds = curDur;
    const lab = ds.length === 1 ? `${ds[0]}-min periods` : `${ds.join(" & ")}-min periods`;
    const lastGrade = gi === curSubject.grades.length - 1;
    const secs = curGrade?.sections || [];
    return (
      <div className="rd">
        <StepProgress n={5} suffix={passSuffix} subjectName={passSubjectName} />
        <div className="rd-hd">
          <div className="kicker">{curSubject.name} · Grade {curGrade.grade} · {lab}</div>
          <h2 className="rd-q">When do you teach {curSubject.name} to Grade {curGrade.grade} each week?</h2>
          <p className="rd-ask">{curDur.length > 1
            ? `Tap a day to mark the class. Tap again to cycle through your periods (${curDur.join(", ")} min), and once more to clear it.`
            : "Tap the days you teach each section. Tap again to clear."}</p>
        </div>
        <table className="wk">
          <thead><tr><th className="rowhd">Section</th>{DAYS.map((d) => <th key={d}>{d}</th>)}</tr></thead>
          <tbody>
            {secs.map((sec, r) => {
              const tag = sectionTag(curGrade.grade, sec);
              const ci = r % 4;  // cycle the 4 section colours by row, so any letter (A–Z) is coloured
              return (
                <tr key={tag} data-sec={ci}>
                  <th className="rowhd"><span className="rowtag">{tag}</span></th>
                  {DAYS.map((d, c) => {
                    const v = cellVal(r, c);
                    return (
                      <td key={d}>
                        <div
                          className={`cell ${v >= 0 ? "on" : ""}`}
                          data-sec={v >= 0 ? ci : undefined}
                          onClick={() => tapCell(r, c)}
                          onContextMenu={(e) => { e.preventDefault(); holdCell(r, c); }}
                        >{v >= 0 ? curDur[v] : ""}</div>
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
        <div className="rd-btns">
          <button className="ghost" onClick={gridBack}>← {gi === 0 ? "durations" : `Grade ${curSubject.grades[gi - 1].grade}`}</button>
          <button className="primary" style={{ flex: 1 }} onClick={gridNext}>
            {!lastGrade
              ? `Continue to ${curSubject.name} Grade ${curSubject.grades[gi + 1].grade} →`
              : "Ready to estimate your annual teaching time? →"}
          </button>
        </div>
      </div>
    );
  }

  // ---- Step 6: annual budget (per subject·grade) ----
  const bGrade = curSubject.grades[bi];
  const res = computeBudget(bi, curBudget.method, curBudget.value);
  const hrs = annualHours(bi, res.weeks);
  const lastGrade = bi === curSubject.grades.length - 1;
  // (lastSubject is declared once in the navigation section above and reused here)
  const methodList = ((si === 0 && bi === 0) || showAlt) ? METHOD_ORDER : [curBudget.method];
  let line2;
  if (curBudget.method === "periods") line2 = `Entered directly — ${weeklyPeriods(bi)} periods/week in your timetable.`;
  else if (curBudget.method === "weeks") line2 = `${curBudget.value} weeks × ${weeklyPeriods(bi)} periods/week.`;
  else if (curBudget.method === "days") line2 = `${curBudget.value} working days ÷ ${WORK_WEEK} = ${Math.round(res.weeks * 10) / 10} weeks × ${weeklyPeriods(bi)} periods/week.`;
  else line2 = `Estimated ${ESTIMATE_WEEKS} weeks × ${weeklyPeriods(bi)} periods/week.`;

  // Hours formula: periods × minutes-per-period ÷ 60. avgMin is the period length (or the
  // average when a grade mixes durations, e.g. 45 & 60).
  const wp = weeklyPeriods(bi);
  const avgMin = wp ? Math.round(weeklyMinutes(bi) / wp) : 0;
  const hoursFormula = (hrs != null && res.periods)
    ? `${res.periods} periods × ${avgMin} min ÷ 60 = ${hrs} hours.`
    : null;

  const editing = !!initialReadiness;
  const finishLabel = lastGrade
    ? (lastSubject ? (editing ? "Save changes →" : "Confirm — continue to Generate →") : `Continue to ${subjects[si + 1].name} →`)
    : `Continue to Grade ${curSubject.grades[bi + 1].grade} →`;

  return (
    <div className="rd">
      <StepProgress n={6} suffix={passSuffix} subjectName={passSubjectName} />
      <div className="rd-hd">
        <div className="kicker">{curSubject.name} · Grade {bGrade.grade} · annual budget</div>
        <h2 className="rd-q">How many periods do you expect to teach {curSubject.name} to Grade {bGrade.grade} this year?</h2>
        <p className="rd-ask">{(si === 0 && bi === 0)
          ? "There are many ways to know this number including Aruvi’s own estimation. Choose the option that suits you below."
          : "Same method as before. Enter this grade’s number — or tap below to use a different method."}</p>
      </div>

      {!(si === 0 && bi === 0) && <div className="kicker rd-method-label">YOUR PREFERRED METHOD</div>}
      <div className="methodrow">
        {methodList.map((m) => {
          const meta = METHODS[m];
          const open = m === curBudget.method;
          return (
            <div className={`method ${open ? "open sel" : ""}`} key={m}>
              <div className="mt" onClick={() => !open && setBudgetMethod(m)}>
                <span>{meta.label}</span><span className="chev">▾</span>
              </div>
              <div className="mbody">
                {m === "auto" ? (
                  <div className="md">Schools typically have between 28–33 working weeks. Aruvi uses <b>{ESTIMATE_WEEKS} weeks</b> as the estimate — adjust later if you like.</div>
                ) : (
                  <div className="inrow">
                    <span className="steppermini">
                      <button onClick={(e) => { e.stopPropagation(); stepBudget(-meta.step); }}>–</button>
                      <span className="v">{curBudget.value}</span>
                      <button onClick={(e) => { e.stopPropagation(); stepBudget(meta.step); }}>+</button>
                    </span>
                    <span className="unitlab">{meta.unit}</span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {!(si === 0 && bi === 0) && (
        <div className="gc-switch" onClick={() => setShowAlt(!showAlt)}>
          {showAlt ? "keep this method ▴" : "use a different method ▾"}
        </div>
      )}

      <div className="budgetsum">
        <div className="bsk">{curSubject.name} Grade {bGrade.grade} · annual budget</div>
        <div className="bsv">{res.periods} periods <small>≈ {hrs != null ? `${hrs} teaching hours` : "—"}</small></div>
        <div className="bsn">{line2}{hoursFormula ? `  ${hoursFormula}` : ""}</div>
      </div>

      <div className="rd-btns">
        <button className="ghost" onClick={budBack}>{bi === 0 ? "← back to grids" : `← Grade ${curSubject.grades[bi - 1].grade}`}</button>
        <button className="primary" style={{ flex: 1 }} onClick={budNext}>{finishLabel}</button>
      </div>
    </div>
  );
}

/* ───────── presentational helpers ───────── */

/* Collapsed multi-select dropdown. Click the control to reveal the option list; tap options to
 * toggle (stays open for multi-select). Collapsed, it summarizes what's chosen — so the screen
 * stays uncluttered. `render` labels options/summary (e.g. "Grade VI"). */
function MultiDropdown({ choices, selected, onToggle, render, label, placeholder = "Choose…" }) {
  const [open, setOpen] = useState(false);
  const isSel = (c) => selected.includes(c);
  const summary = selected.length
    ? selected.map((c) => (render ? render(c) : c)).join(", ")
    : placeholder;
  return (
    <div className="mdd">
      {label && <div className="kicker mdd-h">{label}</div>}
      <button type="button" className={`mdd-control ${open ? "open" : ""}`} onClick={() => setOpen((o) => !o)}>
        <span className={`mdd-summary ${selected.length ? "" : "ph"}`}>{summary}</span>
        <span className="mdd-chev">▾</span>
      </button>
      {open && (
        <div className="mdd-menu">
          {choices.map((c) => (
            <button
              type="button"
              key={c}
              className={`mdd-opt ${isSel(c) ? "on" : ""}`}
              onClick={() => onToggle(c)}
            >
              <span className="mdd-mark">{isSel(c) ? "✓" : ""}</span>
              <span className="mdd-lbl">{render ? render(c) : c}</span>
            </button>
          ))}
          <div className="mdd-pager">
            <div className="mdd-pager-l" />
            <button type="button" className="mdd-pg done" onClick={() => setOpen(false)}>Done</button>
          </div>
        </div>
      )}
    </div>
  );
}

/* Collapsed multi-select dropdown that PAGES its options in groups of `pageSize`. Only one
 * page of options is visible at a time; "list more sections →" swaps to the next group and
 * "← back" returns. Selections persist across pages (a teacher can tap A, page forward, and
 * tap I). Collapsed, it summarizes everything chosen across all pages. */
function PagedDropdown({ choices, pageSize = 3, selected, onToggle, render, placeholder = "Choose…", moreLabel = "list more", showDone = true }) {
  const [open, setOpen] = useState(false);
  const [page, setPage] = useState(0);
  const isSel = (c) => selected.includes(c);
  const pageCount = Math.ceil(choices.length / pageSize);
  const start = page * pageSize;
  const pageItems = choices.slice(start, start + pageSize);
  const summary = selected.length
    ? selected.map((c) => (render ? render(c) : c)).join(", ")
    : placeholder;
  return (
    <div className="mdd">
      <button type="button" className={`mdd-control ${open ? "open" : ""}`} onClick={() => setOpen((o) => !o)}>
        <span className={`mdd-summary ${selected.length ? "" : "ph"}`}>{summary}</span>
        <span className="mdd-chev">▾</span>
      </button>
      {open && (
        <div className="mdd-menu">
          {pageItems.map((c) => (
            <button type="button" key={c} className={`mdd-opt ${isSel(c) ? "on" : ""}`} onClick={() => onToggle(c)}>
              <span className="mdd-mark">{isSel(c) ? "✓" : ""}</span>
              <span className="mdd-lbl">{render ? render(c) : c}</span>
            </button>
          ))}
          <div className="mdd-pager">
            <div className="mdd-pager-l">
              {page > 0 && <button type="button" className="mdd-pg" onClick={() => setPage((p) => Math.max(0, p - 1))}>← back</button>}
              {page < pageCount - 1 && <button type="button" className="mdd-pg" onClick={() => setPage((p) => Math.min(pageCount - 1, p + 1))}>{moreLabel} →</button>}
            </div>
            {showDone && <button type="button" className="mdd-pg done" onClick={() => setOpen(false)}>Done</button>}
          </div>
        </div>
      )}
    </div>
  );
}

// A tap-to-toggle pick list. `inline` lays chips in a wrap row; otherwise a stacked list.
function PickList({ choices, selected, onToggle, render, label, inline }) {
  const isSel = (c) => selected.includes(c);
  return (
    <div className={inline ? "picklist inline" : "picklist"}>
      {label && <div className="kicker picklist-h">{label}</div>}
      <div className={inline ? "pickrow" : "pickcol"}>
        {choices.map((c) => (
          <button
            type="button"
            key={c}
            className={`pickchip ${isSel(c) ? "on" : ""}`}
            onClick={() => onToggle(c)}
          >
            <span className="pickmark">{isSel(c) ? "✓" : "+"}</span>
            <span className="picklbl">{render ? render(c) : c}</span>
          </button>
        ))}
      </div>
    </div>
  );
}

/* `suffix` (e.g. "a","b") marks which subject's pass this is, shown only when a teacher has
 * more than one subject. Flow is SUBJECT-MAJOR: each subject runs steps 2→6 in full before the
 * next subject begins, so the pips advance 2→6 within a subject and the suffix flips (…6a → 2b)
 * when the next subject's pass starts. */
function StepProgress({ n, suffix, subjectName }) {
  return (
    <div className="rd-prog">
      <span className="pk">Step {n}{suffix || ""} · of {TOTAL_STEPS}{subjectName ? ` ${subjectName}` : ""}</span>
      <div className="pips">
        {Array.from({ length: TOTAL_STEPS }).map((_, i) => (
          <span key={i} className={`pip ${i < n ? "on" : ""}`} />
        ))}
      </div>
    </div>
  );
}
