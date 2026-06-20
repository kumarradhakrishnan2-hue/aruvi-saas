"use client";
import { useEffect, useState } from "react";

const API = "http://localhost:8000";
const ROMAN = ["iii", "iv", "v", "vi", "vii", "viii", "ix", "x"];

const pretty = (s) => (s || "").split("_").map((w) => w.charAt(0).toUpperCase() + w.slice(1)).join(" ");
const gradeUp = (g) => (g || "").replace(/grade/i, "").trim().toUpperCase();

async function getJSON(path, opts) {
  const r = await fetch(API + path, opts);
  if (!r.ok) throw new Error(`${r.status}`);
  return r.json();
}

/* ───────────────────────── view-model renderer (on-screen) ───────────────────────── */
function Stimulus({ vs }) {
  if (!vs || vs.type === "none" || !vs.content) return null;
  if (vs.type === "svg") return <div className="vs" dangerouslySetInnerHTML={{ __html: vs.content }} />;
  if (vs.type === "table") {
    const rows = vs.content.split("\n").filter((l) => l.trim()).map((l) => l.split("|").map((c) => c.trim()));
    return (
      <div className="vs"><table className="vt">
        <thead><tr>{rows[0].map((c, i) => <th key={i}>{c}</th>)}</tr></thead>
        <tbody>{rows.slice(1).map((r, i) => <tr key={i}>{r.map((c, j) => <td key={j}>{c}</td>)}</tr>)}</tbody>
      </table></div>
    );
  }
  return <div className="vs prose">{vs.content}</div>;
}

function Chips({ meta }) {
  const keep = ["weight", "implied_lo", "stage_number", "description", "spine_code", "section_id", "section_anchor"];
  const chips = keep.filter((k) => meta && meta[k] !== undefined && meta[k] !== "" && meta[k] !== null)
    .map((k) => <span className="chip" key={k}><b>{k}</b> {String(meta[k])}</span>);
  return chips.length ? <div className="chips">{chips}</div> : null;
}

function PeriodCard({ p }) {
  return (
    <div className="card">
      <div className="card-hd"><span className="pnum">P{p.number}</span>{p.title}
        {p.meta?.duration_minutes ? <span className="dur">{p.meta.duration_minutes} min</span> : null}</div>
      {p.activities?.length ? <ul className="acts">{p.activities.map((a, i) => <li key={i}>{a}</li>)}</ul> : null}
      {p.learning_outcomes?.length ? <div className="sub"><b>LO:</b> {p.learning_outcomes.join("; ")}</div> : null}
      {p.meta?.pedagogical_method || p.meta?.pedagogical_approach ?
        <div className="sub"><b>Pedagogy:</b> {p.meta.pedagogical_method || p.meta.pedagogical_approach}</div> : null}
      {p.teacher_notes?.length ? <div className="sub"><b>Teacher notes:</b> {p.teacher_notes.join(" ")}</div> : null}
      {p.homework ? <div className="sub"><b>Homework:</b> {p.homework}</div> : null}
    </div>
  );
}

function GroupBlock({ g }) {
  return (
    <section className="grp">
      <div className="grp-hd"><span className="gtype">{g.type}</span><span className="glabel">{g.label}</span></div>
      <Chips meta={g.meta} />
      {g.periods?.map((p, i) => <PeriodCard key={i} p={p} />)}
      {g.children?.map((c, i) => <GroupBlock key={i} g={c} />)}
    </section>
  );
}

function AItem({ it }) {
  return (
    <div className="card">
      <div className="card-hd"><span className="qtype">{it.item_type}</span>{it.prompt}</div>
      <Stimulus vs={it.visual_stimulus} />
      {it.options?.length ? <ol className="opts" type="A">{it.options.map((o, i) => <li key={i}>{o}</li>)}</ol> : null}
      {it.answer ? <div className="ans">Answer: {it.answer}</div> : null}
      {it.implied_lo ? <div className="sub"><b>Implied LO:</b> {it.implied_lo}</div> : null}
      {it.teacher_guide?.length ? <div className="sub"><b>Teacher guide:</b> {it.teacher_guide.join(" · ")}</div> : null}
    </div>
  );
}

function ViewModelView({ view }) {
  const lp = view.lesson_plan, a = view.assessment;
  return (
    <div className="vm">
      <h3>Lesson Plan — {lp.chapter_title} <small>({pretty(lp.subject)}, grade {gradeUp(lp.grade)}, {lp.total_periods} periods)</small></h3>
      {lp.groups.map((g, i) => <GroupBlock key={i} g={g} />)}
      <h3>Assessment — {a.chapter_title}</h3>
      {a.groups.map((g, i) => (
        <section className="grp" key={i}>
          <div className="grp-hd"><span className="gtype">{g.type}</span><span className="glabel">{g.label}</span></div>
          <Chips meta={g.meta} />
          {g.items.map((it, j) => <AItem key={j} it={it} />)}
        </section>
      ))}
    </div>
  );
}

/* ───────────────────────── tabs ───────────────────────── */
function Allocate({ subject, grade }) {
  const [chapters, setChapters] = useState([]);
  const [total, setTotal] = useState(50);
  const [alloc, setAlloc] = useState(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => { setAlloc(null);
    getJSON(`/subjects/${subject}/${grade}/chapters`).then((d) => setChapters(d.chapters)).catch(() => setChapters([]));
  }, [subject, grade]);

  const run = async () => {
    setBusy(true);
    try { setAlloc((await getJSON(`/subjects/${subject}/${grade}/allocate`,
      { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ total_periods: Number(total) }) })).allocations); }
    finally { setBusy(false); }
  };

  const rows = alloc || chapters.map((c) => ({ ...c, periods: null }));
  const maxP = Math.max(1, ...rows.map((r) => r.periods || r.weight || 0));
  return (
    <div>
      <p className="h2">Allocate the year across {chapters.length} chapters by weight.</p>
      <div style={{ display: "flex", gap: 12, alignItems: "flex-end", marginBottom: 18 }}>
        <label className="fld">Total periods
          <input type="number" min="1" value={total} onChange={(e) => setTotal(e.target.value)} style={{ width: 110 }} /></label>
        <button className="primary" onClick={run} disabled={busy || !chapters.length}>{busy ? "Allocating…" : "Allocate"}</button>
      </div>
      {rows.map((r) => (
        <div className="alloc-bar" key={r.chapter_number}>
          <div className="alloc-name"><b>Ch {r.chapter_number}</b>{r.chapter_title}</div>
          <div className="bar-track"><div className="bar-fill" style={{ width: `${((r.periods ?? r.weight) / maxP) * 100}%` }} /></div>
          <div className="alloc-p">{r.periods != null ? <><b>{r.periods}</b> periods</> : <span className="chipw">w {r.weight}</span>}</div>
        </div>
      ))}
      {!chapters.length && <div className="empty">No chapter mappings for this subject/grade.</div>}
    </div>
  );
}

function MyPlans({ subject, grade }) {
  const [plans, setPlans] = useState([]);
  const [view, setView] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => { setView(null);
    getJSON(`/plans/${subject}/${grade}`).then((d) => setPlans(d.plans)).catch(() => setPlans([]));
  }, [subject, grade]);

  const open = async (fn) => { setLoading(true);
    try { setView((await getJSON(`/plans/${subject}/${grade}/${fn}/view`)).view); } finally { setLoading(false); }
  };

  if (loading) return <div className="spin">Loading plan…</div>;
  if (view) return (<div><button className="primary" onClick={() => setView(null)} style={{ marginBottom: 14 }}>← Back to plans</button><ViewModelView view={view} /></div>);
  return (
    <div>
      <p className="h2">{plans.length} saved plan{plans.length === 1 ? "" : "s"}.</p>
      {plans.map((p) => (
        <div className="plan-row" key={p.filename} onClick={() => open(p.filename)}>
          <span className="plan-num">Ch {p.chapter_number}</span>
          <span>{p.chapter_title}</span>
          <span className="plan-date">{(p.saved_at || "").slice(0, 10)}</span>
        </div>
      ))}
      {!plans.length && <div className="empty">No saved plans for this subject/grade yet.</div>}
    </div>
  );
}

function Generate() {
  return (
    <div className="empty">
      <div style={{ fontSize: 17, fontWeight: 600, color: "var(--ink)", marginBottom: 6 }}>Generate — coming soon</div>
      Live generation is wired but intentionally deferred for now.<br />
      Meanwhile, open <b>My Plans</b> to view real generated lesson plans &amp; assessments.
    </div>
  );
}

/* ───────────────────────── app shell ───────────────────────── */
export default function Home() {
  const [subjects, setSubjects] = useState([]);
  const [subject, setSubject] = useState("");
  const [grades, setGrades] = useState([]);
  const [grade, setGrade] = useState("");
  const [tab, setTab] = useState("allocate");

  useEffect(() => { getJSON("/subjects").then((d) => { setSubjects(d.subjects); setSubject(d.subjects.includes("science") ? "science" : d.subjects[0]); }).catch(() => {}); }, []);
  useEffect(() => { if (!subject) return;
    getJSON(`/subjects/${subject}/grades`).then((d) => {
      const gs = [...d.grades].sort((a, b) => ROMAN.indexOf(a) - ROMAN.indexOf(b));
      setGrades(gs); setGrade(gs.includes("vii") ? "vii" : gs[0] || "");
    }).catch(() => setGrades([]));
  }, [subject]);

  return (
    <>
      <header className="hdr">
        <div className="brand">Aruvi <span>· lesson planner</span></div>
        <div className="sel">
          <label className="fld">Subject
            <select value={subject} onChange={(e) => setSubject(e.target.value)}>
              {subjects.map((s) => <option key={s} value={s}>{pretty(s)}</option>)}
            </select></label>
          <label className="fld">Grade
            <select value={grade} onChange={(e) => setGrade(e.target.value)}>
              {grades.map((g) => <option key={g} value={g}>{gradeUp(g)}</option>)}
            </select></label>
        </div>
      </header>
      <div className="tabs">
        {["allocate", "generate", "myplans"].map((t) => (
          <button key={t} className={`tab ${tab === t ? "active" : ""}`} onClick={() => setTab(t)}>
            {t === "myplans" ? "My Plans" : pretty(t)}
          </button>
        ))}
      </div>
      <main>
        {!subject ? <div className="empty">Connecting to the Aruvi API…</div> :
          tab === "allocate" ? <Allocate subject={subject} grade={grade} /> :
          tab === "generate" ? <Generate /> :
          <MyPlans subject={subject} grade={grade} />}
      </main>
    </>
  );
}
