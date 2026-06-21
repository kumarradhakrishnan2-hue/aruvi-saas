"use client";
import { pretty, gradeUp, kickerOf } from "../lib/format";

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
        <div className="entry-no">{String(p.number ?? "").padStart(2, "0")}</div>
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

export default function ViewModelView({ view }) {
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
