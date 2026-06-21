"use client";
import { useEffect, useState } from "react";

const API = "http://localhost:8000";
const ROMAN = ["iii", "iv", "v", "vi", "vii", "viii", "ix", "x"];

const pretty = (s) => (s || "").split("_").map((w) => w.charAt(0).toUpperCase() + w.slice(1)).join(" ");
const gradeUp = (g) => (g || "").replace(/grade/i, "").trim().toUpperCase();
const kickerOf = (t) => (t || "").replace(/_/g, " ").toUpperCase();
const pad = (n) => String(n ?? "").padStart(2, "0");

async function getJSON(path, opts) {
  const r = await fetch(API + path, opts);
  if (!r.ok) throw new Error(`${r.status}`);
  return r.json();
}

/* ───────── view-model renderer (the document) ───────── */
function Stimulus({ vs }) {
  if (!vs || vs.type === "none" || !vs.content) return null;
  if (vs.type === "svg") return <div className="vs"><div className="vs-svg" dangerouslySetInnerHTML={{ __html: vs.content }} /></div>;
  if (vs.type === "table") {
    const rows = vs.content.split("\n").filter((l) => l.trim()).map((l) => l.split("|").map((c) => c.trim()));
    return (
      <div className="vs"><table className="vt">
        <thead><tr>{rows[0].map((c, i) => <th key={i}>{c}</th>)}</tr></thead>
        <tbody>{rows.slice(1).map((r, i) => <tr key={i}>{r.map((c, j) => <td key={j}>{c}</td>)}</tr>)}</tbody>
      </table></div>
    );
  }
  return <div className="vs vs-prose">{vs.content}</div>;
}

function Tags({ items }) {
  const t = items.filter((x) => x && x[1] != null && x[1] !== "" && !(Array.isArray(x[1]) && !x[1].length));
  if (!t.length) return null;
  return <div className="tags">{t.map(([k, v], i) => (
    <span className="tag" key={i}><b>{k}</b> {Array.isArray(v) ? v.join(", ") : String(v)}</span>
  ))}</div>;
}

function PeriodCard({ p }) {
  const m = p.meta || {};
  return (
    <div className="entry">
      <div className="entry-rail">
        <div className="entry-no">{pad(p.number)}</div>
        {m.duration_minutes ? <div className="entry-dur">{m.duration_minutes}′</div> : null}
      </div>
      <div className="entry-body">
        <div className="entry-title">{p.title}</div>
        {p.activities?.length ? <ul className="acts">{p.activities.map((a, i) => <li key={i}>{a}</li>)}</ul> : null}
        {p.learning_outcomes?.length ?
          <div className="field"><span className="field-k">Learning outcome</span>{p.learning_outcomes.join("; ")}</div> : null}
        <Tags items={[["Pedagogy", m.pedagogical_method || m.pedagogical_approach], ["Mode", m.dominant_mode], ["Materials", m.materials]]} />
        {p.teacher_notes?.length ? <div className="tnote">{p.teacher_notes.join(" ")}</div> : null}
        {p.homework ? <div className="field"><span className="field-k">Homework</span>{p.homework}</div> : null}
      </div>
    </div>
  );
}

function Group({ g, nested }) {
  const m = g.meta || {};
  return (
    <section className={`sec ${nested ? "nested" : ""}`}>
      <div className="sec-hd">
        <span className="kicker">{kickerOf(g.type)}</span>
        <span className="sec-label">{g.label}</span>
        {m.weight ? <span className="sec-badge">weight {m.weight}</span> : null}
      </div>
      {m.implied_lo ? <div className="sec-imp">{m.implied_lo}</div> : (m.description ? <div className="sec-imp">{m.description}</div> : null)}
      {g.periods?.map((p, i) => <PeriodCard key={i} p={p} />)}
      {g.children?.map((c, i) => <Group key={i} g={c} nested />)}
    </section>
  );
}

function QItem({ it, n }) {
  const m = it.meta || {};
  const comp = m.competency && m.competency.c_code ? m.competency.c_code : null;
  return (
    <div className="qentry">
      <div className="q-no">Q{n}</div>
      <div className="q-body">
        <div className="q-type">{it.item_type}</div>
        <div className="q-prompt">{it.prompt}</div>
        <Stimulus vs={it.visual_stimulus} />
        {it.options?.length ? <ol className="opts">{it.options.map((o, i) => <li key={i}>{o}</li>)}</ol> : null}
        {it.answer ? <div className="ans">{it.answer}</div> : null}
        {it.implied_lo ? <div className="field"><span className="field-k">Implied LO</span>{it.implied_lo}</div> : null}
        {it.teacher_guide?.length ? <div className="field"><span className="field-k">Teacher guide</span>{it.teacher_guide.join(" · ")}</div> : null}
        <Tags items={[["Cognitive", m.cognitive_demand], ["Competency", comp]]} />
      </div>
    </div>
  );
}

function DocHead({ kicker, title, meta }) {
  return (
    <div className="doc-hd">
      <span className="kicker">{kicker}</span>
      <div className="doc-title">{title}</div>
      {meta ? <div className="doc-meta">{meta}</div> : null}
    </div>
  );
}

function ViewModelView({ view }) {
  const lp = view.lesson_plan, a = view.assessment;
  return (
    <div className="doc">
      <DocHead kicker="Lesson Plan" title={lp.chapter_title}
        meta={<>{pretty(lp.subject)} <span>·</span> Grade {gradeUp(lp.grade)} <span>·</span> {lp.total_periods} periods</>} />
      <div className="rule-hero" />
      {lp.groups.map((g, i) => <Group key={i} g={g} />)}
      <div style={{ marginTop: 50 }} />
      <DocHead kicker="Assessment" title={a.chapter_title} />
      <div className="rule-hero" />
      {a.groups.map((g, i) => (
        <section className="sec" key={i}>
          <div className="sec-hd">
            <span className="kicker">{kickerOf(g.type)}</span>
            <span className="sec-label">{g.label}</span>
          </div>
          {g.meta?.implied_lo ? <div className="sec-imp">{g.meta.implied_lo}</div> : null}
          {g.items.map((it, j) => <QItem key={j} it={it} n={j + 1} />)}
        </section>
      ))}
    </div>
  );
}

/* ───────── tabs ───────── */
function PeriodRows({ rows, setRows }) {
  const upd = (i, k, v) => setRows(rows.map((r, j) => (j === i ? { ...r, [k]: v } : r)));
  return (
    <div className="prows">
      {rows.map((r, i) => (
        <div className="prow" key={i}>
          <input className="pin" type="number" min="0" value={r.count} onChange={(e) => upd(i, "count", e.target.value)} />
          <span className="px">periods ×</span>
          <input className="pin" type="number" min="5" step="5" value={r.minutes} onChange={(e) => upd(i, "minutes", e.target.value)} />
          <span className="px">min</span>
          {rows.length > 1 ? <button className="prm" title="remove" onClick={() => setRows(rows.filter((_, j) => j !== i))}>×</button> : null}
        </div>
      ))}
      <button className="padd" onClick={() => setRows([...rows, { count: 20, minutes: 60 }])}>+ add period type</button>
    </div>
  );
}

const toPeriodRows = (rows) => rows.map((r) => ({ minutes: Number(r.minutes), count: Number(r.count) })).filter((r) => r.count > 0 && r.minutes > 0);

function Allocate({ subject, grade }) {
  const [chapters, setChapters] = useState([]);
  const [basis, setBasis] = useState(null);
  const [rows, setRows] = useState([{ count: 120, minutes: 45 }, { count: 40, minutes: 60 }]);
  const [res, setRes] = useState(null);
  const [busy, setBusy] = useState(false);
  const [showHow, setShowHow] = useState(false);

  useEffect(() => { setRes(null);
    getJSON(`/subjects/${subject}/${grade}/chapters`).then((d) => { setChapters(d.chapters); setBasis(d.allocation_basis); }).catch(() => { setChapters([]); setBasis(null); });
  }, [subject, grade]);

  const run = async () => { setBusy(true);
    try { setRes(await getJSON(`/subjects/${subject}/${grade}/allocate`,
      { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ period_rows: toPeriodRows(rows) }) })); }
    finally { setBusy(false); }
  };

  const dur = res ? res.durations : [];
  const byCh = res ? Object.fromEntries(res.allocations.map((a) => [a.chapter_number, a])) : {};
  const maxW = Math.max(1, ...chapters.map((c) => c.weight || 0));

  return (
    <div>
      <p className="h2">Allocate the year across {chapters.length} chapters.</p>
      <PeriodRows rows={rows} setRows={setRows} />
      <button className="primary" onClick={run} disabled={busy || !chapters.length} style={{ marginBottom: 22 }}>{busy ? "Allocating…" : "Allocate"}</button>

      {basis ? (
        <div className="howbox">
          <button className="howtoggle" onClick={() => setShowHow(!showHow)}>{showHow ? "▾" : "▸"} How are periods allocated?</button>
          {showHow ? (
            <div className="howbody">
              <p>Each chapter receives periods in proportion to its {basis.basis}, which reflects:</p>
              <ul>{basis.factors.map((f, i) => <li key={i}>{f}</li>)}</ul>
              <p className="howmore">Curious why a particular chapter gets more or fewer? Just <b>Ask Aruvi</b>.</p>
            </div>
          ) : null}
        </div>
      ) : null}

      {!chapters.length ? <div className="empty">No chapter mappings for this subject &amp; grade.</div> :
        res ? (
          <table className="atable">
            <thead><tr>
              <th>Chapter</th>
              {dur.map((m) => <th className="num" key={m}>{m}′</th>)}
              <th className="num">Periods</th>
            </tr></thead>
            <tbody>{chapters.map((c) => { const a = byCh[c.chapter_number]; return (
              <tr key={c.chapter_number}>
                <td><span className="chn">CH {pad(c.chapter_number)}</span>{c.chapter_title}</td>
                {dur.map((m) => <td className="num" key={m}>{a ? a.periods_by_duration[m] : ""}</td>)}
                <td className="num total">{a ? a.total_periods : ""}</td>
              </tr>); })}</tbody>
            <tfoot><tr>
              <td className="lbl">Total · {res.totals.minutes.toLocaleString()} min</td>
              {dur.map((m) => <td className="num" key={m}>{res.totals.by_duration[m]}</td>)}
              <td className="num total">{res.totals.periods}</td>
            </tr></tfoot>
          </table>
        ) : (
          <div>{chapters.map((c) => (
            <div className="emph-row" key={c.chapter_number}>
              <div className="emph-name"><span className="chn">CH {pad(c.chapter_number)}</span>{c.chapter_title}</div>
              <div className="emph-track"><div className="emph-fill" style={{ width: `${(c.weight / maxW) * 100}%` }} /></div>
            </div>
          ))}</div>
        )}
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

  if (loading) return <div className="spin">Opening plan…</div>;
  if (view) return (<div><button className="back" onClick={() => setView(null)}>← all plans</button><ViewModelView view={view} /></div>);
  return (
    <div>
      <p className="h2">{plans.length} saved plan{plans.length === 1 ? "" : "s"}.</p>
      {plans.map((p) => (
        <div className="plan-row" key={p.filename} onClick={() => open(p.filename)}>
          <span className="plan-num">CH {pad(p.chapter_number)}</span>
          <span className="plan-title">{p.chapter_title}</span>
          <span className="plan-date">{(p.saved_at || "").slice(0, 10)}</span>
        </div>
      ))}
      {!plans.length && <div className="empty">No saved plans for this subject &amp; grade yet.</div>}
    </div>
  );
}

function Generate({ subject, grade }) {
  const [chapters, setChapters] = useState([]);
  const [plans, setPlans] = useState([]);
  const [chNum, setChNum] = useState("");
  const [rows, setRows] = useState([{ count: 4, minutes: 45 }, { count: 1, minutes: 60 }]);
  const [view, setView] = useState(null);
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => { setView(null); setNote("");
    getJSON(`/subjects/${subject}/${grade}/chapters`).then((d) => { setChapters(d.chapters); setChNum(String(d.chapters[0]?.chapter_number ?? "")); }).catch(() => setChapters([]));
    getJSON(`/plans/${subject}/${grade}`).then((d) => setPlans(d.plans)).catch(() => setPlans([]));
  }, [subject, grade]);

  const run = async () => { setBusy(true); setView(null); setNote("");
    try {
      const sched = toPeriodRows(rows).map((r) => `${r.count}×${r.minutes}′`).join(" + ") || "—";
      const match = plans.find((p) => String(p.chapter_number) === String(chNum));
      if (match) {
        setView((await getJSON(`/plans/${subject}/${grade}/${match.filename}/view`)).view);
        setNote(`Preview — live generation is coming soon. Showing a previously generated plan for this chapter (your schedule: ${sched}).`);
      } else { setNote("Live generation is wired but deferred, and there is no saved example for this chapter yet."); }
    } finally { setBusy(false); }
  };

  return (
    <div>
      <p className="h2">Generate a lesson plan &amp; assessment.</p>
      <label className="fld" style={{ marginBottom: 16, maxWidth: 480 }}><span>Chapter</span>
        <select value={chNum} onChange={(e) => setChNum(e.target.value)}>
          {chapters.map((c) => <option key={c.chapter_number} value={c.chapter_number}>Ch {c.chapter_number} — {c.chapter_title}</option>)}
        </select></label>
      <div className="kicker" style={{ marginBottom: 9 }}>Period schedule</div>
      <PeriodRows rows={rows} setRows={setRows} />
      <button className="primary" onClick={run} disabled={busy || !chapters.length} style={{ marginBottom: 22 }}>{busy ? "Generating…" : "Generate"}</button>
      {note && <div className="note">{note}</div>}
      {view ? <ViewModelView view={view} /> : !note && <div className="empty">Pick a chapter &amp; period schedule, then Generate.</div>}
    </div>
  );
}

/* ───────── app shell ───────── */
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
        <div className="brand">Aruvi<em>.</em><small>lesson studio</small></div>
        <div className="sel">
          <label className="fld"><span>Subject</span>
            <select value={subject} onChange={(e) => setSubject(e.target.value)}>
              {subjects.map((s) => <option key={s} value={s}>{pretty(s)}</option>)}
            </select></label>
          <label className="fld"><span>Grade</span>
            <select value={grade} onChange={(e) => setGrade(e.target.value)}>
              {grades.map((g) => <option key={g} value={g}>{gradeUp(g)}</option>)}
            </select></label>
        </div>
      </header>
      <div className="tabs">
        {["allocate", "generate", "myplans"].map((t) => (
          <button key={t} className={`tab ${tab === t ? "active" : ""}`} onClick={() => setTab(t)}>
            {t === "myplans" ? "My Plans" : t}
          </button>
        ))}
      </div>
      <main>
        {!subject ? <div className="empty">Connecting to the Aruvi engine…</div> :
          tab === "allocate" ? <Allocate subject={subject} grade={grade} /> :
          tab === "generate" ? <Generate subject={subject} grade={grade} /> :
          <MyPlans subject={subject} grade={grade} />}
      </main>
    </>
  );
}
