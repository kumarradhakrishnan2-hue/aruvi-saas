"use client";
import { useState, useEffect } from "react";
import { API, withUser, projectReadiness } from "../lib/format";

/* ───────── MyClasses — the editable teaching-profile drill-down (2026-06-28) ─────────
 * Replaces the old "wizard-as-profile" pattern (re-launching Readiness to edit). This is a
 * focused, view-first drill: Subject → Grade → Section, with editing gated behind an explicit
 * Edit toggle so nothing changes by accident. Ported from docs/mockups/editable-profile-tree.html
 * after several rounds of design iteration.
 *
 * DATA — operates directly on the CANONICAL readiness profile (`readiness.subjects[]`), the
 * exact shape Readiness.jsx persists (CLOUD_DATA_MODEL.md §2.1):
 *   subjects[] → { name, grades[]→{grade, sections[]→{tag}, durations[]}, grids, budget }
 *     • per-section weekly days live in grids[gradeIdx][sectionIdx][dayIdx] = durationIndex | -1
 *       (NOT a schema change — the readiness grid was always per-section)
 *     • budget[gradeIdx] = { method, value }; we edit raw period counts as {method:"periods", value}
 * On any edit we deep-clone, mutate, POST /readiness {subjects} (full replace, same as
 * onReadyComplete), and re-project so the parent's consumers (MyPlans, Allocate) stay in sync.
 *
 * DESIGN — "scholarly planner on warm paper" (globals.css). Single green accent (no per-subject
 * colour), no logos, hover-spotlight rows, grade screen = 3 tabs (Annual budget · Duration ·
 * Sections →) styled like the top tabs. Switching tabs cancels an in-progress edit. Mobile:
 * the day grid + cards reflow; verify at ~390px (CLAUDE.md mobile requirement).
 *
 * Props:
 *   readiness  — the projection from page.jsx (carries .subjects[] canonical)
 *   onChange(payload) — called after a successful local edit with the re-projected readiness,
 *                       so the parent updates its state (mirrors onReadyComplete's setReadiness)
 */

const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const ALL_SUBJECTS = ["Science", "Mathematics", "Social Sciences", "English", "The World Around Us"];
const ALL_GRADES = ["III", "IV", "V", "VI", "VII", "VIII", "IX", "X"];
const SECTION_CHOICES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
const DURATION_CHOICES = Array.from({ length: 25 }, (_, i) => 30 + i * 5); // 30,35,…150
const SECTION_PAGE = 3;
const DURATION_PAGE = 4;
const GRADE_PAGE = 4;
const MIN_FALLBACK = 45;

const clone = (o) => JSON.parse(JSON.stringify(o));
// budget[gradeIdx] -> raw period count (we only edit the "periods" method here)
const budgetPeriods = (subj, gi) => {
  const b = (subj.budget && (subj.budget[gi] ?? subj.budget[String(gi)])) || null;
  if (!b) return 0;
  if (b.method === "periods") return b.value || 0;
  return b.value || 0; // other methods: surface the stored value; editing rewrites as periods
};
// grids[gi][secIdx] is a row of 6 cells (durationIndex | -1). Helpers read/write it.
const sectionRow = (subj, gi, secIdx) => {
  const g = (subj.grids && subj.grids[gi]) || [];
  return g[secIdx] || DAYS.map(() => -1);
};
const daysOfRow = (row) => DAYS.filter((_, c) => (row[c] ?? -1) >= 0);
const avgMin = (durs) => (durs && durs.length ? Math.round(durs.reduce((a, b) => a + b, 0) / durs.length) : MIN_FALLBACK);

export default function MyClasses({ readiness, onChange }) {
  // local working copy of the canonical subjects[]; edits mutate a clone then persist
  const initSubjects = (readiness && readiness.subjects) || [];
  const [subjects, setSubjects] = useState(initSubjects);
  const [path, setPath] = useState([]);           // [] | [si] | [si,gi] | [si,gi,secIdx]
  const [editing, setEditing] = useState(false);
  const [gradeTab, setGradeTab] = useState("budget");
  const [toast, setToast] = useState("");
  const [modal, setModal] = useState(null);       // {type, ...} or null
  const [saving, setSaving] = useState(false);

  // Adopt a new upstream readiness (e.g. after sign-in / a different user) ONLY when idle at the
  // root and not editing — never clobber an in-progress edit. Effect-based (not render-phase) so
  // React doesn't warn about setting state during render. Keyed on the subjects[] reference.
  const upstream = readiness && readiness.subjects;
  useEffect(() => {
    if (!upstream) return;
    if (path.length !== 0 || editing || modal) return;
    if (upstream !== subjects && JSON.stringify(upstream) !== JSON.stringify(subjects)) {
      setSubjects(upstream);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [upstream]);

  const flash = (m) => { setToast(m); window.clearTimeout(flash._t); flash._t = window.setTimeout(() => setToast(""), 1900); };

  // ── persist: deep-clone-mutate pattern. `mutate(draft)` edits a clone; we save + re-project. ──
  const commit = (mutate, msg) => {
    const draft = clone(subjects);
    mutate(draft);
    setSubjects(draft);
    if (onChange) onChange(projectReadiness({ subjects: draft }, Math.max(0, path[0] || 0)));
    setSaving(true);
    fetch(`${API}/readiness`, withUser({
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ subjects: draft }),
    })).catch(() => {}).finally(() => setSaving(false));
    if (msg) flash(msg);
  };

  // ── navigation (always land in view mode) ──
  const goUp = () => { setPath((p) => p.slice(0, -1)); setEditing(false); };
  const drill = (i) => {
    // Drilling grade → section (len 2 → 3) PRESERVES edit mode, so the single grade-level Edit
    // carries into the section's day grid (you can pick weekly days without re-pressing Edit).
    // Every other drill lands in view mode.
    setPath((p) => {
      const np = [...p, i];
      if (np.length === 2) { setGradeTab("budget"); setEditing(false); }
      else if (np.length !== 3) setEditing(false);
      return np;
    });
  };
  const toggleEdit = () => setEditing((e) => !e);
  // switching grade tabs KEEPS the in-progress edit: one Edit on the grade screen makes all
  // three tabs (budget / duration / sections) editable at once; Done confirms across them.
  const switchTab = (t) => {
    if (t === gradeTab) return;
    setGradeTab(t);
  };

  const subj = path.length >= 1 ? subjects[path[0]] : null;
  const grade = path.length >= 2 ? subj.grades[path[1]] : null;

  // ════════════════════ edits ════════════════════
  const stepBudget = (d) => { if (!editing) return; const gi = path[1];
    commit((dr) => { const cur = budgetPeriods(dr[path[0]], gi); setBudgetRaw(dr[path[0]], gi, Math.max(0, cur + d)); }); };
  const setBudget = (v) => { if (!editing) return; const gi = path[1]; const n = Math.max(0, Math.round(+String(v).replace(/[^0-9]/g, "") || 0));
    commit((dr) => setBudgetRaw(dr[path[0]], gi, n)); };
  const addDuration = (d) => { if (!editing) return; const gi = path[1];
    commit((dr) => { const g = dr[path[0]].grades[gi]; g.durations = [...(g.durations || []), d].sort((a, b) => a - b); }, `${d} min added`); };
  const dropDuration = (di) => { if (!editing) return; const gi = path[1];
    commit((dr) => { dr[path[0]].grades[gi].durations.splice(di, 1); }, "Duration removed"); };
  const tapCell = (dayIdx) => { if (!editing) return; const [si, gi, secIdx] = path;
    commit((dr) => {
      const s = dr[si]; ensureGrid(s, gi, secIdx);
      const row = s.grids[gi][secIdx]; const cur = row[dayIdx];
      const ndur = (s.grades[gi].durations || []).length;
      if (cur < 0) row[dayIdx] = 0;
      else if (cur < ndur - 1) row[dayIdx] = cur + 1;
      else row[dayIdx] = -1;
    });
  };
  // adding a section is handled by AddSectionModal (asks which letter(s) via commit directly).
  const deleteSubject = (i) => commit((dr) => dr.splice(i, 1), "Subject deleted");
  const deleteGrade = (gi) => commit((dr) => { dr[path[0]].grades.splice(gi, 1); (dr[path[0]].grids || []).splice(gi, 1); deleteBudgetKey(dr[path[0]], gi); }, "Grade deleted");
  const deleteSection = (secIdx) => commit((dr) => { dr[path[0]].grades[path[1]].sections.splice(secIdx, 1); (dr[path[0]].grids[path[1]] || []).splice(secIdx, 1); }, "Section deleted");

  // ── render ──
  return (
    <div className={`myclasses ${path.length === 0 ? "at-root" : ""}`}>
      {path.length > 0 && <button className="back" onClick={goUp}>← Back</button>}
      {/* No breadcrumb on any screen — each title names its place and "← Back" handles
          up-navigation, so the small-text subject/grade crumb only duplicated the title. */}

      <div className="lvl-head">
        <div>
          <h1 className="lvl-title">{headTitle(path, subj, grade)}</h1>
          {/* Every screen's Edit button spells out its own action, so the generic "use the Edit
              button" hint is dropped everywhere. */}
          <p className="lvl-sub">{headSub(path, editing)}</p>
        </div>
        <button className={`edit-toggle ${editing ? "on" : ""}`} onClick={toggleEdit}>
          {editing ? "Done" : (path.length === 0 ? "Edit to add/delete subjects" : path.length === 1 ? "Edit to add/delete grades" : path.length === 2 ? "Edit budget, duration & sections" : "Edit days of the week")}
        </button>
      </div>

      {path.length !== 2 && (
        <div className="section-kicker"><span className="kicker">{kickerFor(path)}</span><span className="rule" /></div>
      )}

      <div className={editing ? "mc-body editing" : "mc-body"}>
        {path.length === 0 && <Subjects subjects={subjects} editing={editing} onDrill={drill} onAdd={() => setModal({ type: "addSubject" })} onDel={(i) => setModal({ type: "delSubject", i })} />}
        {path.length === 1 && <Grades subj={subj} editing={editing} onDrill={drill} onAdd={() => setModal({ type: "addGrade" })} onDel={(gi) => setModal({ type: "delGrade", gi })} />}
        {path.length === 2 && (
          <GradeDetail subj={subj} grade={grade} gi={path[1]} tab={gradeTab} editing={editing}
            onTab={switchTab} onStepBudget={stepBudget} onSetBudget={setBudget}
            onAddDur={addDuration} onDropDur={dropDuration} onDrillSec={drill}
            onAddSec={() => setModal({ type: "addSection" })} onDelSec={(secIdx) => setModal({ type: "delSection", secIdx })} />
        )}
        {path.length === 3 && <SectionGrid subj={subj} grade={grade} gi={path[1]} secIdx={path[2]} editing={editing} onTap={tapCell} />}
      </div>

      {saving && <div className="tip"><span className="bulb">◔</span><span>Saving…</span></div>}

      {modal && <Modal modal={modal} subjects={subjects} path={path}
        onClose={() => setModal(null)} flash={flash} commit={commit}
        onDeleteSubject={deleteSubject} onDeleteGrade={deleteGrade} onDeleteSection={deleteSection} />}
      {toast && <div className="mc-toast show">{toast}</div>}
    </div>
  );
}

/* ─────────── helpers for budget/grid mutation on a draft ─────────── */
function setBudgetRaw(subj, gi, periods) {
  if (!subj.budget) subj.budget = {};
  subj.budget[gi] = { method: "periods", value: periods };
}
function deleteBudgetKey(subj, gi) {
  if (!subj.budget) return;
  // budget is keyed by grade index; re-key the trailing entries down by one
  const out = {};
  Object.keys(subj.budget).forEach((k) => {
    const idx = +k;
    if (idx < gi) out[idx] = subj.budget[k];
    else if (idx > gi) out[idx - 1] = subj.budget[k];
  });
  subj.budget = out;
}
function ensureGrid(subj, gi, secIdx) {
  if (!subj.grids) subj.grids = [];
  if (!subj.grids[gi]) subj.grids[gi] = [];
  if (!subj.grids[gi][secIdx]) subj.grids[gi][secIdx] = DAYS.map(() => -1);
}
const ROMANS = { III: 3, IV: 4, V: 5, VI: 6, VII: 7, VIII: 8, IX: 9, X: 10 };
function romanToArabic(g) { return ROMANS[g] || g; }

/* ─────────── headings ─────────── */
function headTitle(path, subj, grade) {
  if (path.length === 0) return "My Class";
  if (path.length === 1) return subj.name;
  if (path.length === 2) return `${subj.name} · Grade ${grade.grade}`;
  return `Grade ${grade.grade} · Section ${subj.grades[path[1]].sections[path[2]].tag}`;
}
function headSub(path, editing) {
  if (path.length === 0) return "What you teach — tap a subject to open its grades.";
  if (path.length === 1) return "Grades you teach — tap one for its budget, durations & sections.";
  if (path.length === 2) return "Budget, durations and sections for this class.";
  return editing ? "Tap a day to set its period." : "When this section meets. Tap Edit to change.";
}
function kickerFor(path) {
  if (path.length === 0) return "Subjects";
  if (path.length === 1) return "Grades";
  return "Weekly days";
}

/* ─────────── level: subjects ─────────── */
function Subjects({ subjects, editing, onDrill, onAdd, onDel }) {
  return (
    <div className="nodes">
      {subjects.map((s, i) => {
        const secs = (s.grades || []).reduce((a, g) => a + (g.sections || []).length, 0);
        return (
          <div className="node" key={s.name} onClick={() => onDrill(i)}>
            <div className="node-body"><div className="node-name">{s.name}</div>
              <div className="node-meta">{(s.grades || []).length} grades · {secs} sections</div></div>
            {editing && <button className="node-del" onClick={(e) => { e.stopPropagation(); onDel(i); }}>Delete</button>}
            <span className="node-go">›</span>
          </div>
        );
      })}
      {editing && <div className="add-node" onClick={onAdd}><span className="add-plus">＋</span> Add a subject</div>}
    </div>
  );
}

/* ─────────── level: grades ─────────── */
function Grades({ subj, editing, onDrill, onAdd, onDel }) {
  return (
    <div className="nodes">
      {subj.grades.map((g, i) => (
        <div className="node" key={g.grade} onClick={() => onDrill(i)}>
          <div className="node-body"><div className="node-name">Grade {g.grade}</div>
            <div className="node-meta">{(g.sections || []).length} section{(g.sections || []).length !== 1 ? "s" : ""} · {(g.durations || []).map((d) => d + " min").join(" · ") || "no durations"} · {budgetPeriods(subj, i)} periods/yr</div></div>
          {editing && <button className="node-del" onClick={(e) => { e.stopPropagation(); onDel(i); }}>Delete</button>}
          <span className="node-go">›</span>
        </div>
      ))}
      {editing && <div className="add-node" onClick={onAdd}><span className="add-plus">＋</span> Add a grade to {subj.name}</div>}
    </div>
  );
}

/* ─────────── level: grade detail ───────────
 * Sections come FIRST (each a collapsible row drilling into its weekly days), then the two tabs
 * (Annual budget · Duration) toggling their panel BELOW it. */
function GradeDetail({ subj, grade, gi, tab, editing, onTab, onStepBudget, onSetBudget, onAddDur, onDropDur, onDrillSec, onAddSec, onDelSec }) {
  const showDuration = tab === "duration";
  return (
    <div>
      <div className="grade-sections">
        <div className="section-kicker"><span className="kicker">Sections</span><span className="rule" /></div>
        <SectionsPanel subj={subj} grade={grade} gi={gi} editing={editing} onDrill={onDrillSec} onAdd={onAddSec} onDel={onDelSec} />
      </div>

      <div className="gtabs">
        <button className={`gtab ${!showDuration ? "on" : ""}`} onClick={() => onTab("budget")}>Annual budget</button>
        <button className={`gtab ${showDuration ? "on" : ""}`} onClick={() => onTab("duration")}>Duration</button>
      </div>
      {showDuration
        ? <DurationPanel grade={grade} editing={editing} onAdd={onAddDur} onDrop={onDropDur} />
        : <BudgetPanel subj={subj} grade={grade} gi={gi} editing={editing} onStep={onStepBudget} onSet={onSetBudget} />}
    </div>
  );
}

function BudgetPanel({ subj, grade, gi, editing, onStep, onSet }) {
  const periods = budgetPeriods(subj, gi);
  const m = avgMin(grade.durations);
  const hrs = Math.round(periods * m / 60);
  const fresh = periods === 0;
  return (
    <div className="budgetsum">
      <div className="bsk">Grade {grade.grade} · annual budget</div>
      {editing && fresh && <div className="budget-prompt">Enter the annual budget</div>}
      <div className="budget-stepline">
        {editing ? (
          <span className="steppermini">
            <button onClick={() => onStep(-1)}>–</button>
            <input className="budget-num" type="text" inputMode="numeric" value={periods}
              onChange={(e) => onSet(e.target.value)} />
            <button onClick={() => onStep(1)}>+</button>
          </span>
        ) : (
          <span className="budget-ro">{periods}</span>
        )}
        <span className="budget-unit">periods / year</span>
        <span className="budget-hours">≈ {hrs} teaching hours</span>
      </div>
      <div className="bsn">{periods} periods × {m} min ÷ 60 = {hrs} hours.</div>
    </div>
  );
}

function DurationPanel({ grade, editing, onAdd, onDrop }) {
  const durs = grade.durations || [];
  const [menuOpen, setMenuOpen] = useState(false);
  const [page, setPage] = useState(0);
  const avail = DURATION_CHOICES.filter((d) => !durs.includes(d));
  const pageCount = Math.ceil(avail.length / DURATION_PAGE);
  const items = avail.slice(page * DURATION_PAGE, page * DURATION_PAGE + DURATION_PAGE);
  return (
    <div className="detail-card">
      <div className="detail-label">Duration types <span className="move">(grade-level — all sections share these)</span></div>
      {!durs.length && <div className="dur-empty">No durations set{editing ? " — add one to begin." : "."}</div>}
      <div className="dur-chips">
        {durs.map((d, di) => (
          <span className={`dur-chip ${di === 1 ? "alt" : ""}`} key={d}>{d} min{editing && <span className="x" onClick={() => onDrop(di)}>✕</span>}</span>
        ))}
        {editing && <button className="dur-add" onClick={() => { setMenuOpen((o) => !o); setPage(0); }}><span className="add-plus-sm">＋</span> Add duration</button>}
      </div>
      {editing && menuOpen && (
        <div className="mdd"><div className="mdd-menu">
          {items.map((d) => (
            <button className="mdd-opt" key={d} onClick={() => { onAdd(d); }}><span className="mdd-mark" /><span className="mdd-lbl">{d} minutes</span></button>
          ))}
          <div className="mdd-pager"><div className="mdd-pager-l">
            {page > 0 && <button className="mdd-pg" onClick={() => setPage((p) => p - 1)}>← back</button>}
            {page < pageCount - 1 && <button className="mdd-pg" onClick={() => setPage((p) => p + 1)}>list more →</button>}
          </div><button className="mdd-pg done" onClick={() => setMenuOpen(false)}>Done</button></div>
        </div></div>
      )}
    </div>
  );
}

function SectionsPanel({ subj, grade, gi, editing, onDrill, onAdd, onDel }) {
  return (
    <div>
      <div className="nodes">
        {grade.sections.map((x, secIdx) => {
          const ds = daysOfRow(sectionRow(subj, gi, secIdx));
          return (
            <div className="node" key={x.tag} onClick={() => onDrill(secIdx)}>
              <div className="node-body"><div className="node-name">Section {x.tag}</div>
                <div className="node-meta">{ds.length ? ds.join(" · ") : <span className="needs">Needs weekly days →</span>}</div></div>
              {editing && <button className="node-del" onClick={(e) => { e.stopPropagation(); onDel(secIdx); }}>Delete</button>}
              <span className="node-go">›</span>
            </div>
          );
        })}
        {editing && <div className="add-node" onClick={onAdd}><span className="add-plus">＋</span> Add a section</div>}
      </div>
    </div>
  );
}

/* ─────────── level: section day grid ─────────── */
function SectionGrid({ subj, grade, gi, secIdx, editing, onTap }) {
  const row = sectionRow(subj, gi, secIdx);
  const durs = grade.durations || [];
  const ds = daysOfRow(row);
  let note;
  if (!editing) {
    note = ds.length === 0
      ? <div className="daycal-note daycal-empty">No days set yet — tap Edit to schedule.</div>
      : null;
  } else {
    note = ds.length === 0
      ? <div className="daycal-note daycal-empty">No days yet — tap to add them.</div>
      : (durs.length > 1
        ? <div className="daycal-note">Tap a day to mark it; tap again to cycle {durs.join(", ")} min; once more to clear.</div>
        : <div className="daycal-note">Tap the days this section meets. Tap again to clear.</div>);
  }
  // data-sec colours the cell's "on" state (CSS keys backgrounds off [data-sec]); without it the
  // toggled-on cell painted white text on an unfilled cell and looked like nothing happened.
  const sec = secIdx % 4;
  return (
    <div className="daycal">
      <table className="wk"><thead><tr>{DAYS.map((d) => <th key={d}>{d}</th>)}</tr></thead>
        <tbody><tr data-sec={sec}>{DAYS.map((d, c) => {
          const v = row[c] ?? -1; const on = v >= 0;
          return <td key={d}><div data-sec={sec} className={`cell ${on ? "on" : ""} ${editing ? "" : "ro"}`} onClick={editing ? () => onTap(c) : undefined}>{on ? <>{durs[v]}<br />min</> : ""}</div></td>;
        })}</tr></tbody></table>
      {note}
    </div>
  );
}

/* ─────────── modals: delete-confirm + guided add ─────────── */
function Modal({ modal, subjects, path, onClose, flash, commit, onDeleteSubject, onDeleteGrade, onDeleteSection }) {
  if (modal.type === "delSubject" || modal.type === "delGrade" || modal.type === "delSection") {
    return <DeleteModal modal={modal} subjects={subjects} path={path} onClose={onClose}
      onDeleteSubject={onDeleteSubject} onDeleteGrade={onDeleteGrade} onDeleteSection={onDeleteSection} />;
  }
  if (modal.type === "addSubject") return <AddSubjectModal subjects={subjects} onClose={onClose} commit={commit} flash={flash} />;
  if (modal.type === "addGrade") return <AddGradeModal subj={subjects[path[0]]} si={path[0]} onClose={onClose} commit={commit} flash={flash} />;
  if (modal.type === "addSection") return <AddSectionModal subj={subjects[path[0]]} si={path[0]} gi={path[1]} onClose={onClose} commit={commit} flash={flash} />;
  return null;
}

function DeleteModal({ modal, subjects, path, onClose, onDeleteSubject, onDeleteGrade, onDeleteSection }) {
  let title, body, onYes;
  if (modal.type === "delSubject") {
    const s = subjects[modal.i]; const secs = (s.grades || []).reduce((a, g) => a + (g.sections || []).length, 0);
    title = `Delete ${s.name}?`;
    body = <>This removes the whole subject and everything under it:<ul><li>{(s.grades || []).length} grades</li><li>{secs} sections and their weekly days</li><li>durations &amp; annual budgets</li></ul>This can't be undone.</>;
    onYes = () => { onDeleteSubject(modal.i); onClose(); };
  } else if (modal.type === "delGrade") {
    const s = subjects[path[0]]; const g = s.grades[modal.gi];
    title = `Delete ${s.name} · Grade ${g.grade}?`;
    body = <>This grade has <b>{(g.sections || []).length} section{(g.sections || []).length !== 1 ? "s" : ""}</b>, each with its own weekly days, plus durations and an annual budget. Deleting removes all of it.</>;
    onYes = () => { onDeleteGrade(modal.gi); onClose(); };
  } else {
    const g = subjects[path[0]].grades[path[1]];
    if ((g.sections || []).length <= 1) { return <Backdrop onClose={onClose}><div className="mc-modal"><p className="modal-body">A grade needs at least one section.</p><div className="modal-bar"><button className="btn btn-cancel" onClick={onClose}>OK</button></div></div></Backdrop>; }
    const x = g.sections[modal.secIdx];
    title = `Delete Section ${x.tag}?`;
    body = <>Section {x.tag} and its weekly schedule will be removed.</>;
    onYes = () => { onDeleteSection(modal.secIdx); onClose(); };
  }
  return (
    <Backdrop onClose={onClose}>
      <div className="mc-modal">
        <div className="modal-kicker danger">⚠ Confirm delete</div>
        <h3 className="modal-title">{title}</h3>
        <p className="modal-body">{body}</p>
        <div className="modal-bar"><button className="btn btn-cancel" onClick={onClose}>Keep it</button><button className="btn btn-danger" onClick={onYes}>Delete</button></div>
      </div>
    </Backdrop>
  );
}

// guided add subject: subject → grades (multi) → sections per grade (multi, paged)
function AddSubjectModal({ subjects, onClose, commit, flash }) {
  const avail = ALL_SUBJECTS.filter((s) => !subjects.some((d) => d.name === s));
  const [step, setStep] = useState(1);
  const [name, setName] = useState(avail[0] || "");
  const [grades, setGrades] = useState([]);
  const [gPage, setGPage] = useState(0);
  const [secByGrade, setSecByGrade] = useState({});
  const [sPage, setSPage] = useState({});

  const toggleGrade = (g) => setGrades((a) => a.includes(g) ? a.filter((x) => x !== g) : [...a, g].sort((x, y) => ALL_GRADES.indexOf(x) - ALL_GRADES.indexOf(y)));
  const goSections = () => { const init = {}; const sp = {}; grades.forEach((g) => { init[g] = ["A", "B"]; sp[g] = 0; }); setSecByGrade(init); setSPage(sp); setStep(3); };
  const toggleSec = (g, s) => setSecByGrade((m) => { const a = m[g] || []; return { ...m, [g]: a.includes(s) ? a.filter((x) => x !== s) : [...a, s].sort() }; });
  const ready3 = grades.every((g) => (secByGrade[g] || []).length > 0);

  const finish = () => {
    commit((dr) => {
      const newGrades = grades.map((g) => ({
        grade: g,
        sections: (secByGrade[g] || []).map((t) => ({ tag: `${romanToArabic(g)}${t}`, sec: t })),
        durations: [],
      }));
      const grids = newGrades.map((ng) => ng.sections.map(() => DAYS.map(() => -1)));
      dr.push({ name, grades: newGrades, grids, budget: {} });
    }, `${name} added — set duration & budget per grade`);
    onClose();
  };

  return (
    <Backdrop onClose={onClose}>
      <div className="mc-modal">
        {step === 1 && (<>
          <div className="modal-kicker add">Add subject · step 1 of 3</div>
          <h3 className="modal-title">Which subject?</h3>
          <p className="modal-ask">Choose the subject you want to add.</p>
          <div className="modal-field"><label>Subject</label>
            <select value={name} onChange={(e) => setName(e.target.value)}>{avail.map((s) => <option key={s}>{s}</option>)}</select></div>
          <div className="modal-bar"><button className="btn btn-cancel" onClick={onClose}>Cancel</button><button className="btn btn-go" onClick={() => setStep(2)}>Next →</button></div>
        </>)}
        {step === 2 && (<>
          <div className="modal-kicker add">Add {name} · step 2 of 3</div>
          <h3 className="modal-title">Which grades?</h3>
          <p className="modal-ask">Pick every grade you teach {name} to — choose as many as you like.</p>
          <PagedPicker choices={ALL_GRADES} page={gPage} setPage={setGPage} pageSize={GRADE_PAGE}
            selected={grades} onToggle={toggleGrade} render={(g) => "Grade " + g} />
          <div className="modal-bar"><button className="btn btn-cancel" onClick={onClose}>Cancel</button>
            <button className="btn btn-go" disabled={!grades.length} onClick={goSections}>Next →</button></div>
        </>)}
        {step === 3 && (<>
          <div className="modal-kicker add">Add {name} · step 3 of 3</div>
          <h3 className="modal-title">Which sections?</h3>
          <p className="modal-ask">Choose the sections for each grade. Three show at a time — tap "list more" for the next set.</p>
          {grades.map((g) => (
            <div key={g} className="addsec-group">
              <div className="kicker">Grade {g}</div>
              <PagedPicker choices={SECTION_CHOICES} page={sPage[g] || 0} setPage={(fn) => setSPage((m) => ({ ...m, [g]: typeof fn === "function" ? fn(m[g] || 0) : fn }))}
                pageSize={SECTION_PAGE} selected={secByGrade[g] || []} onToggle={(s) => toggleSec(g, s)} render={(s) => "Section " + s} />
            </div>
          ))}
          <p className="modal-fine">After this, open each grade to set its duration and annual budget — nothing is pre-filled.</p>
          <div className="modal-bar"><button className="btn btn-cancel" onClick={onClose}>Cancel</button>
            <button className="btn btn-go" disabled={!ready3} onClick={finish}>Add {name}</button></div>
        </>)}
      </div>
    </Backdrop>
  );
}

function AddGradeModal({ subj, si, onClose, commit, flash }) {
  const avail = ALL_GRADES.filter((g) => !subj.grades.some((x) => x.grade === g));
  const [gPage, setGPage] = useState(0);
  const [picked, setPicked] = useState(null);
  const [secs, setSecs] = useState([]);   // no sections pre-selected — teacher chooses
  const [sPage, setSPage] = useState(0);
  const toggleSec = (s) => setSecs((a) => a.includes(s) ? a.filter((x) => x !== s) : [...a, s].sort());

  const finish = () => {
    commit((dr) => {
      const s = dr[si];
      s.grades.push({ grade: picked, sections: secs.map((t) => ({ tag: `${romanToArabic(picked)}${t}`, sec: t })), durations: [] });
      if (!s.grids) s.grids = [];
      s.grids.push(secs.map(() => DAYS.map(() => -1)));
    }, `Grade ${picked} added — set its duration & budget`);
    onClose();
  };

  return (
    <Backdrop onClose={onClose}>
      <div className="mc-modal">
        {!picked ? (<>
          <div className="modal-kicker add">Add grade to {subj.name}</div>
          <h3 className="modal-title">Which grade?</h3>
          <p className="modal-ask">Pick the grade to add.</p>
          <PagedPicker choices={avail} page={gPage} setPage={setGPage} pageSize={GRADE_PAGE}
            selected={[]} onToggle={(g) => setPicked(g)} render={(g) => "Grade " + g} single />
          <div className="modal-bar"><button className="btn btn-cancel" onClick={onClose}>Cancel</button></div>
        </>) : (<>
          <div className="modal-kicker add">Add Grade {picked} to {subj.name}</div>
          <h3 className="modal-title">Which sections?</h3>
          <p className="modal-ask">Choose the sections you take. Three show at a time — tap "list more" for the next set.</p>
          <PagedPicker choices={SECTION_CHOICES} page={sPage} setPage={setSPage} pageSize={SECTION_PAGE}
            selected={secs} onToggle={toggleSec} render={(s) => "Section " + s} />
          <p className="modal-fine">Then set this grade's duration and budget — nothing is pre-filled.</p>
          <div className="modal-bar"><button className="btn btn-cancel" onClick={onClose}>Cancel</button>
            <button className="btn btn-go" disabled={!secs.length} onClick={finish}>Add grade</button></div>
        </>)}
      </div>
    </Backdrop>
  );
}

// guided add section(s) to an existing grade — asks WHICH letters (multi), same paged picker
// the grade flow uses, instead of silently defaulting to the next free letter.
function AddSectionModal({ subj, si, gi, onClose, commit, flash }) {
  const grade = subj.grades[gi];
  const used = new Set((grade.sections || []).map((x) => (x.sec || x.tag.slice(-1)).toUpperCase()));
  const avail = SECTION_CHOICES.filter((s) => !used.has(s));
  const [secs, setSecs] = useState([]);   // nothing pre-selected — teacher chooses
  const [sPage, setSPage] = useState(0);
  const toggleSec = (s) => setSecs((a) => a.includes(s) ? a.filter((x) => x !== s) : [...a, s].sort());

  const finish = () => {
    commit((dr) => {
      const g = dr[si].grades[gi];
      const arabic = (g.grade.match(/^[IVX]+/) ? romanToArabic(g.grade) : g.grade);
      secs.forEach((t) => {
        g.sections = [...g.sections, { tag: `${arabic}${t}`, sec: t }];
        ensureGrid(dr[si], gi, g.sections.length - 1);
      });
    }, secs.length > 1 ? `${secs.length} sections added` : "Section added");
    onClose();
  };

  return (
    <Backdrop onClose={onClose}>
      <div className="mc-modal">
        <div className="modal-kicker add">Add section to {subj.name} · Grade {grade.grade}</div>
        <h3 className="modal-title">Which sections?</h3>
        <p className="modal-ask">Choose the section(s) to add. Three show at a time — tap "list more" for the next set.</p>
        <PagedPicker choices={avail} page={sPage} setPage={setSPage} pageSize={SECTION_PAGE}
          selected={secs} onToggle={toggleSec} render={(s) => "Section " + s} />
        <div className="modal-bar"><button className="btn btn-cancel" onClick={onClose}>Cancel</button>
          <button className="btn btn-go" disabled={!secs.length} onClick={finish}>Add section</button></div>
      </div>
    </Backdrop>
  );
}

// paged multi/single picker (3 or 4 at a time + "list more")
function PagedPicker({ choices, page, setPage, pageSize, selected, onToggle, render, single }) {
  const pageCount = Math.ceil(choices.length / pageSize);
  const items = choices.slice(page * pageSize, page * pageSize + pageSize);
  const sel = (c) => selected.includes(c);
  return (
    <div className="mdd">
      <div className="mdd-menu">
        {items.map((c) => (
          <button key={c} className={`mdd-opt ${sel(c) ? "on" : ""}`} onClick={() => onToggle(c)}>
            <span className="mdd-mark">{!single && sel(c) ? "✓" : ""}</span><span className="mdd-lbl">{render ? render(c) : c}</span>
          </button>
        ))}
        <div className="mdd-pager"><div className="mdd-pager-l">
          {page > 0 && <button className="mdd-pg" onClick={() => setPage((p) => p - 1)}>← back</button>}
          {page < pageCount - 1 && <button className="mdd-pg" onClick={() => setPage((p) => p + 1)}>list more →</button>}
        </div></div>
      </div>
    </div>
  );
}

function Backdrop({ children, onClose }) {
  return <div className="mc-modal-bg" onClick={(e) => { if (e.currentTarget === e.target) onClose(); }}>{children}</div>;
}
