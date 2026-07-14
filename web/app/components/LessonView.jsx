"use client";
import { useEffect, useMemo, useRef, useState } from "react";
import { pushSectionState } from "../lib/sectionState";
import { userKey, boldMarks } from "../lib/format";

/* ───────── Lesson view (Screen 3) + assessment artifact (Screen 3b) ─────────
 * A COMPLETION surface, not a navigation one (2026-06-29 redesign). The plan's periods
 * (lesson_plan.groups[].periods[]) ARE the Learning Units; each period's activities are its
 * phases (no fabricated per-phase minutes — Phase 5 decision).
 *
 * Tracking mode (opened from My Week, has a section): shows ONLY the current unit + a segmented
 * progress bar (same look as Track) + one "Mark unit complete" action. Marking advances the
 * per-section pointer (localStorage) by one and shows a confirmation with the next unit and an
 * Undo that lives only for this visit (cleared on refresh/leave — no persisted trail). There is
 * no per-unit forward/back navigation and no rail; the WHOLE plan is one tap away via "View full
 * lesson plan", which re-renders this view in preview layout.
 *
 * Preview mode (opened from My Lesson Plans, or the in-view "View full lesson plan"): every unit
 * stacked top-to-bottom for reading, no pointer, no completion controls.
 *
 * Assessment "tags along" as the green ASSESS tab of the unit's tab bar (2026-07-10) — present
 * in BOTH the tracking view (scoped to the current unit) and the unit preview (scoped to the
 * previewed unit; §I-ter: preview shows future periods, their assessment comes along for free),
 * and only rendered when the unit actually anchors items. */

// Flatten groups → a single ordered Unit list, carrying the parent group label
// (progression stage / section / spine / competency) as context for each unit.
function flattenUnits(lp) {
  const units = [];
  const walk = (groups, ctx) => {
    (groups || []).forEach((g) => {
      const label = [ctx, g.label].filter(Boolean).join(" · ");
      (g.periods || []).forEach((p) => units.push({ ...p, context: label, groupType: g.type }));
      if (g.children) walk(g.children, label);
    });
  };
  walk(lp.groups, "");
  return units;
}

// Phase duration in minutes (end − start, parsed once by the engine); null when unparsed.
const phaseMin = (ph) =>
  Number.isFinite(ph?.start_min) && Number.isFinite(ph?.end_min) ? ph.end_min - ph.start_min : null;

/* ───────── The TABBED unit anatomy (2026-07-10, founder-directed) ─────────
 * The 2026-07-09 stacked anatomy is re-organized behind four per-unit tabs so nothing
 * reads "jumbled" on a phone: the header keeps ONLY the unit number + title, and the
 * content splits into
 *   OVERVIEW  — spine (group context) · time · pedagogy as ledger rows + teacher notes
 *   MATERIAL  — the pre-class checklist
 *   LESSON    — the timed phase spine (durations in the marginal rail) + homework
 *   ASSESS    — the unit's anchored assessment items, green language — the tab EXISTS
 *               only when the unit actually carries items (§I-ter anchor rule)
 * Overview/Material/Lesson always show (a slot simply says so when empty); LO is still
 * NEVER rendered in the LP (founder rule 2026-07-09) — it lives on the assess cards.
 * Spec mockup: docs/mockups/lesson-unit-tabs.html. */

// Which assessment items belong to THIS unit — same §I-ter anchor logic the old 3b
// sub-view used: an item surfaces once, at its anchor (closing) period; legacy views
// without anchor metadata fall back to all items so we never hide data by mistake.
function unitAssessItems(assessment, u) {
  if (!assessment?.groups?.length) return [];
  const all = assessment.groups.flatMap((g) => g.items || []);
  const anyAnchored = all.some((it) => it.meta?.anchor_period != null);
  return anyAnchored ? all.filter((it) => it.meta?.anchor_period === u.number) : all;
}

// Row label for the unit's group context, spelled from the plugin's group type.
const CTX_LABEL = { spine: "Spine", section: "Section", competency: "Competency", stage: "Stage", progression_stage: "Stage" };

function OverviewPanel({ u, chapterTitle }) {
  const dur = u.meta?.duration_minutes;
  // Axis row value: normally the group label (u.context). But where "section" is only a PROXY
  // for the axis and the grouping collapsed (maths prep → a single "Lesson" group), the plugin
  // hands the period its OWN anchored section in meta.section_label — use it so the row shows the
  // real section, not "Lesson". No-op elsewhere (TWAU's context already IS the section; maths
  // middle/secondary leave section_label empty and fall back to the group label).
  const axisVal = u.meta?.section_label || u.context;
  const rows = [
    ["Chapter", chapterTitle],
    [CTX_LABEL[u.groupType] || "Spine", axisVal],
    ["Time", dur ? `${dur} mins` : null],
    ["Pedagogy", u.approach],
  ].filter(([, v]) => v);
  return (
    <>
      {rows.length ? (
        <div className="uv-ovrows">
          {rows.map(([k, v]) => (
            <div className="uv-ovrow" key={k}>
              <span className="kicker kicker-soft">{k}</span>
              <span className="uv-ovval">{v}</span>
            </div>
          ))}
        </div>
      ) : null}
      {/* Teacher notes moved to the LESSON tab (founder 2026-07-10) — one home only:
          a collapsed clay teaser ribbon at the top of the phase spine. */}
      {!rows.length ? (
        <div className="empty">No overview details recorded for this unit.</div>
      ) : null}
    </>
  );
}

function MaterialPanel({ u }) {
  if (!u.materials?.length) return <div className="empty">Nothing to prepare — this unit needs no materials.</div>;
  return <div className="uv-mat"><ul>{u.materials.map((m, i) => <li key={i}>{m}</li>)}</ul></div>;
}

function LessonPanel({ u }) {
  const phases = (u.phases || []).filter((ph) => ph.text || ph.label);
  const notes = u.teacher_notes?.length ? u.teacher_notes.join(" ") : null;
  return (
    <>
      {/* Teacher notes — a colleague's margin note, living WHERE IT'S READ: the top of
          the lesson spine (its only home — founder 2026-07-10). Collapsed to a one-line
          clay teaser so a verbose note never pushes phase 1 below the fold; one tap
          expands it in place. data-tour="lesson-notes" kept for tour positioning. */}
      {notes ? (
        <details className="uv-tnotes-rib" data-tour="lesson-notes">
          <summary>
            <span className="kicker">Teacher notes</span>
            <span className="uv-tnotes-teaser">{notes}</span>
          </summary>
          <p>{notes}</p>
        </details>
      ) : null}
      {/* Phases — the hero; durations in the marginal rail, one aligned column.
          Legacy fallback: plans normalized before Phase landed render activities lines. */}
      {phases.length ? (
        <div className="uv-phases">
          {phases.map((ph, i) => {
            const mins = phaseMin(ph);
            return (
              <div className="uv-phase" key={i} data-tour={i === 0 ? "lesson-phase-1" : undefined}>
                <div className="uv-ph-time">
                  <span className="uv-ph-n">{mins != null ? mins : (ph.label || "—")}</span>
                  {mins != null ? <span className="uv-ph-u">min</span> : null}
                </div>
                <p className="uv-ph-t">{ph.text}</p>
              </div>
            );
          })}
        </div>
      ) : (u.activities && u.activities.length) ? u.activities.map((act, i) => (
        <div className="phaserow" key={i} data-tour={i === 0 ? "lesson-phase-1" : undefined}><span className="phasetext">{act}</span></div>
      )) : <div className="empty">No phases recorded for this unit.</div>}

      {/* Homework — the single tinted block, full text (no word caps). */}
      {u.homework ? (
        <div className="uv-hw">
          <span className="kicker">Homework</span>
          <p>{boldMarks(u.homework)}</p>
        </div>
      ) : null}
    </>
  );
}

// The unit's assessment tab — flat on the unit's paper (the green box was retired in the
// same-day revision; assessment keeps its own voice via PINE accents). ONE anchored item
// renders bare; more than one introduces the one-at-a-time PINE question pager — pine,
// never clay, so it can't be mistaken for the unit strip. Paging resets the item's tabs
// to Overview.
//
// FROZEN CHROME (founder 2026-07-10): everything down to and including the item tab bar
// stays pinned — the pager + item tabs sit in ONE sticky group that stacks directly
// below whatever is already frozen above (in preview, .lv-stick pins the header + UNIT
// tab bar). The group's `top` is measured at mount (app nav + .lv-stick height when
// present) since those heights vary with title wrapping. Only panel content scrolls.
function AssessPanel({ items, mathsMiddle = false, mathsSecondary = false }) {
  const [at, setAt] = useState(0);
  const [itab, setITab] = useState("ov");
  const grpRef = useRef(null);
  const idx = Math.min(at, items.length - 1);
  const many = items.length > 1;
  const it = items[idx];
  const n = it?.normalized;
  const set = n && n.template ? itemTabSet(n) : null;
  // Guard: if paging lands on an item without the previously-active tab, fall back.
  const tab = set && set.tabs.some(([id]) => id === itab) ? itab : "ov";
  const goto = (i) => { setAt(i); setITab("ov"); };

  useEffect(() => {
    const el = grpRef.current;
    if (!el || typeof window === "undefined") return;
    const place = () => {
      const navH = parseInt(getComputedStyle(document.documentElement).getPropertyValue("--nav-h"), 10) || 118;
      const stick = document.querySelector(".lv-stick");
      el.style.top = `${navH + (stick ? stick.offsetHeight : 0)}px`;
    };
    place();
    window.addEventListener("resize", place);
    return () => window.removeEventListener("resize", place);
  }, []);

  return (
    <>
      <div className="uv-assess-stick" ref={grpRef}>
        {many ? (
          <div className="uv-apager">
            <button className={`uv-apgbtn ${idx <= 0 ? "off" : ""}`} disabled={idx <= 0}
              onClick={() => goto(idx - 1)}>← Previous</button>
            <span className="uv-apgmid">Question {idx + 1} / {items.length}</span>
            <button className={`uv-apgbtn ${idx >= items.length - 1 ? "off" : ""}`} disabled={idx >= items.length - 1}
              onClick={() => goto(idx + 1)}>Next →</button>
          </div>
        ) : null}
        {set ? (
          <div className="assess-mtabs" role="tablist">
            {set.tabs.map(([id, label]) => (
              <button key={id} role="tab" aria-selected={tab === id}
                className={`assess-mt${tab === id ? " on" : ""}`}
                onClick={() => setITab(id)}>{label}</button>
            ))}
          </div>
        ) : null}
      </div>
      <AssessBody it={it} tab={tab} qn={many ? idx + 1 : null} mathsMiddle={mathsMiddle} mathsSecondary={mathsSecondary}
        onNext={many && idx < items.length - 1 ? () => goto(idx + 1) : null} key={idx} />
    </>
  );
}

/* Tab state + rendered parts (bar / panel) for a unit. Split so the preview view can pin the
 * bar inside its frozen header while the panel scrolls beneath. Callers key the consuming
 * component by unit index so paging to another unit resets the active tab to Overview.
 * data-tour="unit-tabs": tour step 8's tooltip hangs below the bar. */
function useUnitTabsParts(u, assessment, chapterTitle) {
  const items = unitAssessItems(assessment, u);
  // Inclusivity keyword-bolding is stage-specific: middle maths writes differentiation as
  // "…struggling student…; challenge: …", so those two words are weighted (see InclusivityText).
  // Secondary maths writes it as "Support: … Challenge: …" — both labels weighted, each on its
  // own row.
  const g = String(assessment?.grade || "").toLowerCase().replace(/grade|class/g, "").trim();
  const mathsMiddle = assessment?.subject === "mathematics" && ["vi", "vii", "viii"].includes(g);
  const mathsSecondary = assessment?.subject === "mathematics" && ["ix", "x"].includes(g);
  const [tab, setTab] = useState("overview");
  const tabs = [
    ["overview", "Overview"],
    ["material", "Material"],
    ["lesson", "Lesson"],
    ...(items.length ? [["assess", "Assess"]] : []),
  ];
  const bar = (
    <div className="uv-tabs" data-tour="unit-tabs" role="tablist">
      {tabs.map(([id, label]) => (
        <button
          key={id} role="tab" aria-selected={tab === id}
          className={`uv-tab${tab === id ? " on" : ""}`}
          onClick={() => setTab(id)}
        >{label}</button>
      ))}
    </div>
  );
  const panel = (
    <>
      {tab === "overview" ? <OverviewPanel u={u} chapterTitle={chapterTitle} /> : null}
      {tab === "material" ? <MaterialPanel u={u} /> : null}
      {tab === "lesson" ? <LessonPanel u={u} /> : null}
      {tab === "assess" ? <AssessPanel items={items} mathsMiddle={mathsMiddle} mathsSecondary={mathsSecondary} /> : null}
    </>
  );
  return { bar, panel };
}

// Tracking view: bar + panel together, in normal flow.
function UnitTabs({ u, assessment, chapterTitle }) {
  const { bar, panel } = useUnitTabsParts(u, assessment, chapterTitle);
  return <>{bar}{panel}</>;
}

// Preview view: the header + tab bar are frozen together (one sticky block); only the panel
// scrolls. `headerContent` is the topbar + name-plate built by the caller.
function PreviewUnit({ headerContent, u, assessment, chapterTitle }) {
  const { bar, panel } = useUnitTabsParts(u, assessment, chapterTitle);
  return (
    <>
      <div className="lv-stick">
        {headerContent}
        {bar}
      </div>
      {panel}
    </>
  );
}

/* The 📝 period-note invoke — a slot reserved by design (v0.2 §Period Notes): pull-based,
 * occupies nothing until used. The feature itself is deferred; the control answers with a
 * gentle placeholder so the affordance is honest, not dead. */
function NoteInvoke() {
  const [msg, setMsg] = useState(false);
  return (
    <div className="uv-note">
      <button onClick={() => setMsg((v) => !v)}>📝&nbsp; Add a note about this class</button>
      {msg ? <span className="uv-notemsg">Notes are on their way — coming in an upcoming update.</span> : null}
    </div>
  );
}

/* ───────── Screen 3b — normalized assessment cards (question-type registry) ─────────
 * SUBJECT-AGNOSTIC by contract: every card reads ONLY item.normalized (the NormalizedItem
 * shape from aruvi_core/view_model.py, spec docs/assessment-question-type-registry.md §2)
 * and switches on n.template — 6 card templates for the 12 registry types. Card order is
 * always LO (absent, not blank, when null — the Maths middle/prep case) → type/meta →
 * stem → stimulus → the template's marking surface → inclusivity. Items normalized before
 * the contract shipped fall back to the legacy card. Tables arrive PRE-SPLIT from the
 * engine (normalize.parse_table) — this renderer never re-splits pipe strings. */

// A maths number line — an ordered tick line (labels + blank ticks) the engine parsed from a
// pipe row, drawn as an axis with ticks, NOT a grid. Blank ticks are the positions a student
// marks; the instruction sits below.
function ANumberLine({ nl }) {
  const ticks = nl?.ticks || [];
  if (!ticks.length) return null;
  const W = 320, padX = 26, y = 26, n = ticks.length;
  const step = n > 1 ? (W - 2 * padX) / (n - 1) : 0;
  const x = (i) => padX + i * step;
  return (
    <div className="assess-vs assess-vs-nl">
      <svg viewBox={`0 0 ${W} 52`} className="assess-nl-svg" role="img" aria-label="Number line">
        <line x1={padX - 12} y1={y} x2={W - padX + 12} y2={y} className="assess-nl-axis" />
        <polygon points={`${padX - 12},${y} ${padX - 4},${y - 4} ${padX - 4},${y + 4}`} className="assess-nl-arrow" />
        <polygon points={`${W - padX + 12},${y} ${W - padX + 4},${y - 4} ${W - padX + 4},${y + 4}`} className="assess-nl-arrow" />
        {ticks.map((t, i) => (
          <g key={i}>
            <line x1={x(i)} y1={y - 6} x2={x(i)} y2={y + 6} className="assess-nl-tick" />
            {t.label ? <text x={x(i)} y={y + 20} className="assess-nl-lab" textAnchor="middle">{t.label}</text> : null}
          </g>
        ))}
      </svg>
      {nl.instruction ? <div className="assess-nl-instr">{nl.instruction}</div> : null}
    </div>
  );
}

// Typed stimulus/passage block — same typing as LP visuals (svg / table / number_line / prose).
function ATyped({ b, passage = false }) {
  if (!b || !b.content) return null;
  if (b.type === "svg") return <div className="assess-vs assess-vs-svg" dangerouslySetInnerHTML={{ __html: b.content }} />;
  if (b.type === "number_line" && b.number_line) return <ANumberLine nl={b.number_line} />;
  if (b.type === "table" && b.table) {
    return (
      <div className="assess-vs">
        <table className="assess-table">
          <thead><tr>{b.table.header.map((c, i) => <th key={i}>{c}</th>)}</tr></thead>
          <tbody>{b.table.rows.map((r, i) => <tr key={i}>{r.map((c, j) => <td key={j}>{c}</td>)}</tr>)}</tbody>
        </table>
      </div>
    );
  }
  return <div className={passage ? "assess-passage" : "assess-vs assess-vs-prose"}>{b.content}</div>;
}

// A labelled prose block (SUGGESTED ANSWER / ANSWER KEY / METHOD / SCAFFOLD / …).
function ABlock({ k, text }) {
  if (!text) return null;
  return (
    <div className="assess-look">
      <span className="assess-look-k">{k}</span>
      <div className="assess-look-t">{text}</div>
    </div>
  );
}

// A fill-in scaffold template. The SPLIT into rows is done ONCE in the engine
// (assessment_norm.split_scaffold_lines) so a numbered/step template never runs together in
// one paragraph — the renderer just lays out whatever rows it produced (blank string = a
// spacer between blocks, e.g. Part A / Part B). Falls back to plain prose when unsplit.
function AScaffold({ n }) {
  if (!n.scaffold) return null;
  const lines = n.scaffold_lines;
  if (!lines?.length) return <ABlock k="SCAFFOLD" text={n.scaffold} />;
  return (
    <div className="assess-look">
      <span className="assess-look-k">SCAFFOLD</span>
      <div className="assess-scaf">
        {lines.map((ln, i) =>
          ln
            ? <div className="assess-scaf-row" key={i}>{ln}</div>
            : <div className="assess-scaf-gap" key={i} aria-hidden="true" />
        )}
      </div>
    </div>
  );
}

// A numbered/lettered part list — {marker, text} rows, marker in the mono margin. The
// SPLIT is done ONCE in the engine (assessment_norm.split_parts), never here — the
// renderer only renders whatever list the normalizer produced, so any subject/notation
// the normalizer understands lands the same way. Shared by the question stem and the
// answer key.
function APartsList({ lead, parts }) {
  return (
    <>
      {lead ? <p className="assess-parts-lead">{lead}</p> : null}
      <div className="assess-ansrows">
        {parts.map((p, i) => (
          <div className="assess-ansrow" key={i}>
            {p.marker ? <span className="assess-ans-lab">{p.marker}</span> : null}
            <span className="assess-ans-t">{p.text}</span>
          </div>
        ))}
      </div>
    </>
  );
}

// A labelled answer block. Renders the engine-structured multi-part key (n.answer_parts)
// as rows when present; otherwise the plain model_answer prose.
function AAnswerBlock({ k, n }) {
  if (!n || !n.model_answer) return null;
  if (!n.answer_parts?.length) return <ABlock k={k} text={n.model_answer} />;
  return (
    <div className="assess-look">
      <span className="assess-look-k">{k}</span>
      <APartsList lead={n.answer_lead} parts={n.answer_parts} />
    </div>
  );
}

// A labelled tick-list (LOOK FOR / EXPECTED ELEMENTS / SPEAKING RUBRIC / WHAT TO PRODUCE).
function ATicks({ k, items }) {
  if (!items?.length) return null;
  return (
    <div className="assess-look">
      <span className="assess-look-k">{k}</span>
      <ul className="assess-ticks">{items.map((t, i) => <li key={i}>{t}</li>)}</ul>
    </div>
  );
}

// "What each choice reveals" — label → misconception rows. The "note" key is the
// tolerated legacy prose fallback (un-migrated English MCQs, older SS/TWAU annotations)
// and renders as a plain paragraph, not a labelled row.
function AReveals({ reveals, opts = [] }) {
  const entries = Object.entries(reveals || {});
  // Which choice's wording is popped open (label), or null. Lets the teacher relate a
  // "what this reveals" line back to the actual choice text (founder 2026-07-11).
  const [shown, setShown] = useState(null);
  if (!entries.length) return null;
  const optFor = (lab) => opts.find((o) => o.label === lab) || null;
  const popped = shown ? optFor(shown) : null;
  return (
    <div className="assess-look">
      <span className="assess-look-k">WHAT EACH CHOICE REVEALS</span>
      <div className="assess-rev">
        {entries.map(([lab, txt], i) =>
          lab === "note"
            ? <div className="assess-look-t" key={i}>{txt}</div>
            : (
              <div className="assess-revrow" key={i}>
                <span className="assess-rev-lab">{lab}</span>
                <span>
                  {txt}
                  {optFor(lab) ? (
                    <button type="button" className="assess-rev-choice" onClick={() => setShown(lab)}>
                      Choice {lab}
                    </button>
                  ) : null}
                </span>
              </div>
            ))}
      </div>
      {/* Choice-wording popup — Aruvi paper/ink/pine, ✕ pinned top-LEFT. Backdrop click
          or ✕ closes. */}
      {popped ? (
        <div className="assess-choicepop" role="dialog" aria-modal="true" onClick={() => setShown(null)}>
          <div className="assess-choicepop-box" onClick={(e) => e.stopPropagation()}>
            <button className="assess-choicepop-x" aria-label="Close" onClick={() => setShown(null)}>✕</button>
            <span className="assess-choicepop-lab">Choice {shown}</span>
            <p className="assess-choicepop-t">{popped.text}</p>
          </div>
        </div>
      ) : null}
    </div>
  );
}

// The pre-contract card (plans normalized before NormalizedItem shipped).
function ALegacyCard({ it }) {
  return (
    <>
      <div className="assess-qtype">{qtypeName(it.item_type)}</div>
      <div className="assess-prompt">{it.prompt}</div>
      {it.options?.length ? (
        <ol className="assess-opts">{it.options.map((o, k) => <li key={k}>{o}</li>)}</ol>
      ) : null}
      {it.answer ? <div className="assess-ans">Answer: {it.answer}</div> : null}
      {it.teacher_guide?.length ? (
        <div className="assess-look">
          <span className="assess-look-k">LOOK FOR</span>
          <div className="assess-look-t">{it.teacher_guide.join(" · ")}</div>
        </div>
      ) : null}
    </>
  );
}

/* ── The per-item TAB SET (founder spec 2026-07-10): OVERVIEW · QUESTION · ANSWER ·
 * INCLUSIVITY — the unit-tabs interaction grammar. Same-day palette revision: the green
 * artifact box is RETIRED — items sit flat on the unit's paper in the site's pine voice;
 * what stays distinctly "assessment" is the PINE question pager (vs the clay unit strip)
 * and pine accents. Slotting by the audience test:
 *   OVERVIEW    — why it's asked: LO (absent, not blank, when null) · type · cognitive
 *                 demand · competency. The old always-visible LO strip lives here now.
 *   QUESTION    — everything said/shown to the class: extract, stem, listening cue,
 *                 stimulus, PLAIN options (NO correct tick — the phone can face the
 *                 class), what-to-produce, scaffold, the open-task reading guide
 *                 (format / demonstrates / reading-the-scaffold; still collapsed),
 *                 textbook ref.
 *   ANSWER      — everything student work is checked against: correct option(s) ✓,
 *                 model answer / key, what-each-choice-reveals, expected elements,
 *                 look-fors, method line. Tab exists only when any of these is populated.
 *   INCLUSIVITY — its own tab (class diversity is first-class); exists only when populated.
 * strong_vs_weak_markers is DATA-ONLY (carried in NormalizedItem, never rendered —
 * founder 2026-07-10: verbose, and it restates expected elements + look-fors).
 * Pre-contract items keep the flat legacy card, no tabs. */

// Full-word display names for question types — NEVER acronyms on screen (founder
// 2026-07-10). Long forms per the registry §3; unknown types fall back to the raw
// value with underscores spaced.
const QTYPE_NAME = {
  MCQ: "Multiple choice question",
  TRUE_FALSE: "True or false",
  SCR: "Short constructed response",
  ECR: "Extended constructed response",
  OPEN_TASK: "Open task",
  PROJECT: "Project",
  WRITING_TASK: "Writing task",
  FILL_IN: "Fill in the blanks",
  MATCH: "Match the following",
  ORAL_PROMPT: "Oral prompt",
  NUM: "Numerical problem",
  EXTRACT_ANALYSIS: "Extract analysis",
};
const qtypeName = (t) => QTYPE_NAME[t] || String(t || "").replace(/_/g, " ");

function AOverviewPanel({ n, lo }) {
  const comp = n.competency ? [n.competency.code, n.competency.text].filter(Boolean).join(" — ") : null;
  // ONLY the outcome's value is right-aligned (founder 2026-07-10); the short values
  // read left, next to their labels.
  return (
    <div className="assess-ovrows">
      {/* Every field leads with a BOLD single-row heading, its value below as a normal
          paragraph — the same block layout as Learning outcome. Order (founder 2026-07-11):
          Competency → Learning outcome → Question type → Cognitive demand. */}
      {comp ? (
        <div className="assess-ovlo">
          <span className="assess-ovk assess-ovk-b">Competency</span>
          <p className="assess-ovlo-t">{comp}</p>
        </div>
      ) : null}
      {lo ? (
        <div className="assess-ovlo">
          <span className="assess-ovk assess-ovk-b">Learning outcome</span>
          <p className="assess-ovlo-t">{lo}</p>
        </div>
      ) : null}
      <div className="assess-ovlo">
        <span className="assess-ovk assess-ovk-b">Question type</span>
        <p className="assess-ovlo-t">{qtypeName(n.question_type)}</p>
      </div>
      {n.cognitive_demand ? (
        <div className="assess-ovlo">
          <span className="assess-ovk assess-ovk-b">Cognitive demand</span>
          <p className="assess-ovlo-t">{n.cognitive_demand}</p>
        </div>
      ) : null}
    </div>
  );
}

function AQuestionPanel({ n, opts }) {
  // TRUE_FALSE: statements are stored twice at source (in the stem AND as options). The
  // engine folds them into `tf_statements`; show that ONCE as the statement list and NEVER
  // the options block (which would repeat every statement). The instruction line is stem_lead.
  const isTF = n.template === "true_false" && n.tf_statements?.length;
  return (
    <>
      {/* T6c (EXTRACT_ANALYSIS): the extract is set off BEFORE the multi-part stem. */}
      {n.template === "passage" ? <ATyped b={n.passage} passage /> : null}
      {isTF ? (
        <div className="assess-prompt assess-prompt-tab">
          {n.stem_lead || n.stem ? <p className="assess-parts-lead">{n.stem_lead || n.stem}</p> : null}
          <div className="assess-ansrows">
            {n.tf_statements.map((s, i) => (
              <div className="assess-ansrow" key={i}>
                {s.marker ? <span className="assess-ans-lab">{s.marker}</span> : null}
                <span className="assess-ans-t">{s.text}</span>
              </div>
            ))}
          </div>
        </div>
      ) : n.stem_parts?.length ? (
        /* When the engine found a numbered/lettered list inside the stem, render the intro
           then the parts as rows; otherwise the plain stem prose. */
        <div className="assess-prompt assess-prompt-tab">
          <APartsList lead={n.stem_lead} parts={n.stem_parts} />
        </div>
      ) : (
        <div className="assess-prompt assess-prompt-tab">{n.stem}</div>
      )}
      {/* Listening input the item can't run without — a cue, never a citation. */}
      {n.audio_ref ? (
        <div className="assess-audio">
          <svg className="assess-audio-ico" width="14" height="14" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M4 10v4" /><path d="M8 7v10" /><path d="M12 4v16" /><path d="M16 8v8" /><path d="M20 11v2" />
          </svg>
          <span className="assess-audio-t"><i>Listening passage</i>
            <span className="assess-audio-ref"> — {n.audio_ref}, read aloud</span></span>
        </div>
      ) : null}
      <ATyped b={n.visual_stimulus} />
      {/* Options are PLAIN here — the tick lives in the ANSWER tab. TRUE_FALSE never shows
          them (the statements above ARE the options; showing both duplicates every line). */}
      {opts.length && !isTF ? (
        <ul className="assess-opts2">
          {opts.map((o, i) => (
            <li key={i}>
              <span className="assess-opt-lab">{o.label}</span>
              <span>{o.text}</span>
            </li>
          ))}
        </ul>
      ) : null}
      <ATicks k="WHAT TO PRODUCE" items={n.format_of_output} />
      <AScaffold n={n} />
      {/* Task-setting part of the open-task guide — belongs to the question process
          (founder 2026-07-10); stays collapsed so the card isn't a wall on a phone. */}
      {n.open_task_guide ? (
        <details className="assess-otg">
          <summary>READING THIS TASK</summary>
          <div className="assess-otg-body">
            <ABlock k="FORMAT" text={[n.open_task_guide.format_type, n.open_task_guide.format_rationale].filter(Boolean).join(" — ")} />
            <ABlock k="WHAT THIS DEMONSTRATES" text={n.open_task_guide.what_this_demonstrates} />
            <ABlock k="READING THE SCAFFOLD" text={n.open_task_guide.reading_the_scaffold} />
          </div>
        </details>
      ) : null}
      {n.exercise_ref || n.exercise_desc ? (
        <div className="assess-look">
          <span className="assess-look-k">TEXTBOOK EXERCISE</span>
          <div className="assess-look-t">
            {/* The book item (book_ref) is bold; the task description follows in normal weight. */}
            {n.exercise_ref ? <strong className="assess-book-item">{n.exercise_ref}</strong> : null}
            {n.exercise_ref && n.exercise_desc ? " — " : null}
            {n.exercise_desc}
          </div>
        </div>
      ) : null}
    </>
  );
}

function AAnswerPanel({ n, correct, opts = [] }) {
  // TRUE_FALSE: one verdict + reason per statement, from the engine's collapsed key. This
  // REPLACES both the "CORRECT ANSWER" tick-list (which showed only the true statements, a
  // misleading half-answer) and the standalone suggested-answer prose (already folded in).
  if (n.template === "true_false" && n.tf_statements?.length) {
    const hasReasons = n.tf_statements.some((s) => s.reason);
    // Fallback shape: the suggested-answer prose could NOT be split into per-statement reasons
    // (grouped like "Statements 2, 3 and 4 are TRUE", or an odd format), so the engine kept the
    // whole prose with the key's reasons empty. That prose already states every verdict — show
    // it ALONE, never beside a bare verdict list (that pairing was the residual duplication).
    if (!hasReasons && n.model_answer) {
      return <ABlock k="SUGGESTED ANSWER" text={n.model_answer} />;
    }
    // Aligned shape: the key carries marker · verdict · reason and IS the whole answer
    // (model_answer was folded away in the engine). Bare-verdict list only if neither survives.
    return (
      <div className="assess-look">
        <span className="assess-look-k">ANSWER KEY</span>
        <div className="assess-ansrows">
          {n.tf_statements.map((s, i) => (
            <div className="assess-tf-row" key={i}>
              {s.marker ? <span className="assess-ans-lab">{s.marker}</span> : null}
              <span className="assess-ans-t">
                <span className={s.verdict ? "assess-tf-t" : "assess-tf-f"}>
                  {s.verdict ? "True" : "False"}
                </span>
                {s.reason ? <> — {s.reason}</> : null}
              </span>
            </div>
          ))}
        </div>
      </div>
    );
  }
  return (
    <>
      {correct.length ? (
        <div className="assess-look">
          <span className="assess-look-k">CORRECT ANSWER</span>
          {correct.map((o, i) => (
            <div className="assess-corr-row" key={i}>
              <span className="assess-opt-lab">{o.label}</span>
              <span>{o.text}<span className="assess-tickmark"> ✓</span></span>
            </div>
          ))}
        </div>
      ) : null}
      {n.template === "selected_response" ? (
        <>
          {/* TRUE_FALSE verdict+justification arrives as model_answer, not reveals. */}
          <AAnswerBlock k="ANSWER" n={n} />
          <AReveals reveals={n.option_reveals} opts={opts} />
        </>
      ) : n.template === "scr" ? (
        <>
          {n.model_answer
            ? <AAnswerBlock k="SUGGESTED ANSWER" n={n} />
            : <ATicks k="LOOK FOR" items={n.expected_elements} />}
          {/* Maths-only "how to solve" — method_one_line is null for other families, so
              ABlock renders nothing (no subject branch needed). */}
          <ABlock k="METHOD" text={n.method_one_line} />
        </>
      ) : n.template === "ecr" ? (
        <>
          <ATicks k="LOOK FOR" items={n.look_fors} />
          <ATicks k="EXPECTED ELEMENTS" items={n.expected_elements} />
          <AAnswerBlock k="SUGGESTED ANSWER" n={n} />
          <ABlock k="METHOD" text={n.method_one_line} />
        </>
      ) : n.template === "open_task" ? (
        <>
          <ATicks k="EXPECTED ELEMENTS" items={n.expected_elements} />
          <ATicks k="LOOK FOR" items={n.look_fors} />
        </>
      ) : n.template === "cloze_match" ? (
        <AAnswerBlock k="ANSWER KEY" n={n} />
      ) : n.template === "match" ? (
        n.match_pairs?.length ? (
          <div className="assess-look">
            <span className="assess-look-k">ANSWER KEY</span>
            <div className="assess-ansrows">
              {n.match_pairs.map((p, i) => (
                <div className="assess-match-row" key={i}>
                  <span className="assess-match-l">{p.left}</span>
                  <span className="assess-match-arw" aria-hidden="true">→</span>
                  <span className="assess-match-r">{p.right}</span>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <AAnswerBlock k="ANSWER KEY" n={n} />
        )
      ) : n.template === "oral" ? (
        <ATicks k="SPEAKING RUBRIC" items={n.expected_elements} />
      ) : n.template === "numeric" ? (
        <>
          <AAnswerBlock k="WORKED ANSWER" n={n} />
          <ABlock k="METHOD" text={n.method_one_line} />
        </>
      ) : n.template === "passage" ? (
        <ATicks k="EXPECTED ELEMENTS" items={n.expected_elements} />
      ) : null}
    </>
  );
}

// Which tabs a normalized item offers (ANSWER / INCLUSIVITY only when populated),
// plus the derived option lists both panels need.
function itemTabSet(n) {
  const opts = (n.options || []).map((o, i) => ({ ...o, label: o.label || String.fromCharCode(65 + i) }));
  const correct = opts.filter((o) => o.is_correct);
  const hasAnswer = !!(correct.length || n.model_answer || n.expected_elements?.length
    || n.look_fors?.length || Object.keys(n.option_reveals || {}).length || n.method_one_line
    || n.tf_statements?.length || n.match_pairs?.length);
  return {
    opts, correct,
    tabs: [
      ["ov", "Overview"],
      ["q", "Question"],
      ...(hasAnswer ? [["an", "Answer"]] : []),
      ...(n.inclusivity ? [["inc", "Inclusivity"]] : []),
    ],
  };
}

/* Inclusivity prose with differentiation cues bolded. Three families:
 *   • Colon-LABELS ("Support: …; stretch: …", maths prep) — only a token followed by ":" is
 *     emphasised (a bare "support" in another subject's note stays plain) and it is normalised
 *     to a capitalised form so the pair reads matched. Middle maths adds "challenge:" here.
 *   • In-prose KEYWORD ("…a struggling student…", middle maths) — bolded WHERE it sits, casing
 *     left untouched (it is an adjective mid-sentence, not a label). Middle-maths only, via
 *     `mathsMiddle`, so no other subject's inclusivity prose is touched.
 *   • Secondary maths ("Support: … Challenge: …", via `mathsSecondary`) — both labels are
 *     colon-labelled/weighted, and the note is broken so each label starts its OWN row rather
 *     than running on continuously. */
function InclusivityText({ text, mathsMiddle = false, mathsSecondary = false }) {
  if (!text) return null;
  const labels = mathsMiddle ? "support|stretch|challenge"
    : mathsSecondary ? "support|challenge"
    : "support|stretch";
  // Bold colon-labels (title-cased) + middle-maths in-prose "struggling" within one chunk.
  const render = (chunk, keyBase) => {
    const parts = [`\\b(?:${labels})\\b(?=\\s*:)`];             // colon-labelled → title-cased
    if (mathsMiddle) parts.push(`\\b(?:struggling)\\b`);        // in-prose keyword → bold in place
    const re = new RegExp(`(${parts.join("|")})`, "gi");
    const out = [];
    let last = 0, m, k = 0;
    while ((m = re.exec(chunk)) !== null) {
      if (m.index > last) out.push(chunk.slice(last, m.index));
      const w = m[0];
      const isLabel = new RegExp(`^(?:${labels})$`, "i").test(w);  // labels capitalise; keywords don't
      const shown = isLabel ? w.charAt(0).toUpperCase() + w.slice(1).toLowerCase() : w;
      out.push(<strong key={`${keyBase}-${k++}`}>{shown}</strong>);
      last = m.index + w.length;
    }
    out.push(chunk.slice(last));
    return out;
  };
  // Secondary maths: split before each "Support:"/"Challenge:" so the two land on separate rows.
  if (mathsSecondary) {
    const rows = text.split(/(?=\b(?:support|challenge)\s*:)/i).map((s) => s.trim()).filter(Boolean);
    if (rows.length > 1) {
      return <>{rows.map((r, i) => <div key={i} className="assess-inc-row">{render(r, i)}</div>)}</>;
    }
  }
  return <>{render(text, 0)}</>;
}

/* The item's ACTIVE PANEL only — no card chrome, no Q-number/type header (the pager
 * carries position; type lives in Overview). The item's tab BAR is rendered by
 * AssessPanel inside the frozen chrome group (see below), so `tab` arrives as a prop.
 * Legacy pre-contract items keep the old flat white card, whatever the tab. */
function AssessBody({ it, tab, qn, onNext, mathsMiddle = false, mathsSecondary = false }) {
  const n = it.normalized;
  const lo = n ? n.linked_lo : (it.meta?.linked_lo || it.implied_lo);
  // A light nudge so a teacher who reaches the bottom of an item doesn't miss that the unit
  // anchors more questions. Placed at the END of the Answer AND Inclusivity panels — the two
  // tabs a teacher tends to finish on (Answer almost always; Inclusivity is often skipped, so
  // the link rides both to catch either exit). Null on the last question / single-item units.
  const nextQ = onNext ? (
    <div className="assess-nextq-wrap">
      <span className="assess-nextq" role="button" tabIndex={0} onClick={onNext}
        onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); onNext(); } }}>
        Next question →
      </span>
    </div>
  ) : null;
  // `qn` (Q1., Q2., …) is set ONLY when the unit anchors more than one item. FLOATED
  // (never a full row) so it shares the line with each panel's opening words —
  // Learning outcome / stem / answer / inclusivity — and the teacher always knows
  // which question the panel belongs to.
  const qmark = qn ? <span className="assess-qmark">Q{qn}.</span> : null;
  if (!n || !n.template) {
    return (
      <div className="assess-card">
        {qmark}
        {lo ? (
          <div className="assess-lo">
            <span className="assess-lo-k">LEARNING OUTCOME</span>
            <div className="assess-lo-t">{lo}</div>
          </div>
        ) : null}
        <ALegacyCard it={it} />
      </div>
    );
  }
  const { opts, correct } = itemTabSet(n);
  return (
    <div className="assess-flat">
      {qmark}
      {tab === "ov" ? <AOverviewPanel n={n} lo={lo} /> : null}
      {tab === "q" ? <AQuestionPanel n={n} opts={opts} /> : null}
      {tab === "an" ? <>{<AAnswerPanel n={n} correct={correct} opts={opts} />}{nextQ}</> : null}
      {tab === "inc" ? <><div className="assess-inc"><InclusivityText text={n.inclusivity} mathsMiddle={mathsMiddle} mathsSecondary={mathsSecondary} /></div>{nextQ}</> : null}
    </div>
  );
}

/* ── Chapter Notes — the notebook popup (arch-plan §I-bis). The teacher's ONE writable
 * surface on an otherwise read-only plan: a school-ruled notebook keyed to the PLAN ASSET
 * (subject·grade·chapter, section-independent) so the SAME note surfaces in preview (My
 * Lessons) and in tracking — one record at two altitudes, nothing to sync. Grey guidance
 * rides the ruled lines as the field's placeholder → vanishes on the first keystroke. Soft
 * 400-word cap (the counter turns clay past it, never blocks). localStorage today; migrates
 * to the per-tenant overlay (CLOUD_DATA_MODEL §2.3) at Phase 4, alongside the pointer. */
const CN_CAP = 400;
const cnWordCount = (s) => { const t = (s || "").trim(); return t ? t.split(/\s+/).length : 0; };
const CN_GUIDE =
  "For next year, jot what you'll want to remember:\n" +
  "  · where the class generally struggled\n" +
  "  · materials you brought in beyond the book\n" +
  "  · what to do differently next time";
// "Subject · Grade" for the modal header — subject title-cased, grade in Roman numerals.
const CN_ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"];
function cnSubjectGrade(lp) {
  const subj = String(lp.subject || "").replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()).trim();
  const gm = String(lp.grade || "").match(/\d+/);
  const grade = gm
    ? (CN_ROMAN[parseInt(gm[0], 10)] || gm[0])
    : String(lp.grade || "").replace(/grade|class/gi, "").trim().toUpperCase();
  return [subj, grade].filter(Boolean).join(" · ");
}

function ChapterNotesModal({ chapterTitle, subjectGrade, initial, onSave, onClose }) {
  const [text, setText] = useState(initial || "");
  const taRef = useRef(null);
  useEffect(() => { taRef.current?.focus(); }, []);
  const wc = cnWordCount(text);
  // Hard cap: block input that would push past 400 words; deletions/edits still allowed
  // (only reject when the new value grows the count beyond the cap).
  const changeText = (e) => {
    const v = e.target.value;
    if (cnWordCount(v) > CN_CAP && cnWordCount(v) > wc) return;
    setText(v);
  };
  return (
    <div className="cn-modal-bg" onClick={onClose}>
      <div className="cn-modal" onClick={(e) => e.stopPropagation()}>
        <div className="cn-head">
          <div className="cn-head-t">
            <div className="kicker kicker-soft">Chapter notes</div>
            <div className="cn-title">{chapterTitle}</div>
            {subjectGrade ? <div className="cn-sg">{subjectGrade}</div> : null}
            <div className="cn-scope">Shared across every section on this plan</div>
          </div>
          <button className="cn-x" aria-label="Close" onClick={onClose}>✕</button>
        </div>
        <textarea
          ref={taRef}
          className="cn-paper"
          spellCheck={false}
          value={text}
          onChange={changeText}
          placeholder={CN_GUIDE}
        />
        <div className="cn-foot">
          <div className="cn-foot-l">
            <button className="cn-speak" onClick={() => taRef.current?.focus()}>
              <svg className="cn-speak-mic" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <rect x="9" y="2" width="6" height="12" rx="3" />
                <path d="M5 11a7 7 0 0 0 14 0" />
                <line x1="12" y1="18" x2="12" y2="22" />
                <line x1="8" y1="22" x2="16" y2="22" />
              </svg>
              Speak
            </button>
            <span className={`cn-count${wc >= CN_CAP ? " over" : ""}`}>{wc} / {CN_CAP} words</span>
          </div>
          <button className="cn-save" onClick={() => onSave(text)}>Save</button>
        </div>
      </div>
    </div>
  );
}

/* Science SECONDARY section anchors carry a leading NCF section number, in either notation:
 * a bare number ("8.1 Rediscovering the Roots of Atomic Theory", "8.2 … / 8.2.1 …") or a
 * "Section N.N — Title" label ("Section 2.1 — The Challenge of Studying Cells"). On the
 * Chapter Organization page the title alone is enough — strip the number (and any leading
 * "Section" word / dash separator) from each " / "-joined segment. A pure-number anchor with
 * no title (e.g. "2.1") keeps its number; a trailing " (Revisit)" is preserved
 * (founder 2026-07-14). */
function sectionTitleOnly(label) {
  if (!label) return label;
  const cleaned = label.split(" / ").map((seg) => {
    const s = seg.trim();
    const stripped = s.replace(/^(?:Section\s+)?\d+(?:\.\d+)*\s*[—–:.)-]?\s*/i, "").trim();
    return stripped || s;   // number-only segment → keep as-is
  }).join(" / ");
  return cleaned || label;
}

/* ── Chapter Organization — the chapter's front door (chapter altitude, arch-plan §E).
 * The My Classes section card, opened up: the same tick rail expands into one card per
 * unit (pine = taught · ochre = now · hairline = ahead), grouped under quiet mono
 * dividers from the plugin's Group tree. Tapping a card is NAVIGATION, never pointer
 * movement. `pointer` is the live unit index, or null (preview — no place-marker). */
function ChapterOrg({ lp, units, pointer, doneAll, onOpenUnit, onBack, backTour }) {
  // Chapter Notes state — asset-keyed (NOT the per-section pointer key), so preview and
  // tracking, and every section, read/write ONE shared note (arch-plan §I-bis).
  // Per-user scope (userKey appends _{user}) so chapter notes never bleed across teachers on
  // a shared browser — the asset key alone (subject·grade·chapter) is identical across users.
  const notesKey = userKey(`chapter_notes_${lp.subject}_${lp.grade}_${lp.chapter_title || ""}`);
  const [noteText, setNoteText] = useState("");
  const [notesOpen, setNotesOpen] = useState(false);
  useEffect(() => {
    if (typeof window === "undefined") return;
    setNoteText(window.localStorage.getItem(notesKey) || "");
  }, [notesKey]);
  const saveNote = (t) => {
    setNoteText(t);
    if (typeof window !== "undefined") {
      if (t.trim()) window.localStorage.setItem(notesKey, t);
      else window.localStorage.removeItem(notesKey);
    }
    setNotesOpen(false);
  };
  const hasNote = !!noteText.trim();
  // Each top-level group is a collapsible drop-down; only ONE is open at a time (accordion).
  // The first group opens by default; opening another closes the rest (re-tapping the open
  // one collapses it). -1 = all closed.
  const [openIdx, setOpenIdx] = useState(0);
  // Maths PREPARATORY is the one subject·stage with no real section axis: its periods carry
  // many-to-many markers (S2+S3, S3+S4…) that can't cleanly nest, so the normalizer collapses
  // every period into a single fallback group labelled "Lesson" (see mathematics/subject.py).
  // For that one case we DON'T show the pointless one-item accordion — we render the units flat
  // under the chapter header inside a fixed-height "wheel" window (~4 units); units beyond the
  // fold are reached by scrolling INSIDE that region (founder 2026-07-13, replacing the earlier
  // click-to-reveal link). "Lesson" (the exact fallback string) is unique to the maths middle/
  // prep branch and only actually fires for prep, so it's a safe, precise signature.
  const mathsFlat = lp.subject === "mathematics" && (lp.groups || []).length === 1
    && lp.groups[0]?.label === "Lesson";
  const FLAT_SHOWN = 4;   // units shown before the window starts scrolling
  // Total units under a group (its own periods + all descendants) — shown on the group header.
  const countUnits = (g) => (g.periods?.length || 0) + (g.children || []).reduce((s, c) => s + countUnits(c), 0);
  // Rebuild the group walk so cards sit under their group bars (flat index kept in sync
  // with flattenUnits — same traversal order). `visible` gates rendering but NOT the flat
  // index: idx advances across every period of every group (open or collapsed) so a unit's
  // number matches the pointer regardless of which drop-down is expanded.
  let idx = -1;
  const renderGroup = (g, depth, keyPrefix, visible) => {
    const bars = [];
    if (visible && g.label) {
      bars.push(
        <div className="co-groupbar" key={`${keyPrefix}-bar`}>
          <span className="co-subname">{lp.subject === "science" && g.type === "section" ? sectionTitleOnly(g.label) : g.label}</span>
        </div>
      );
    }
    if (g.periods?.length) {
      const cards = g.periods.map((p, i) => {
        idx += 1;
        const n = idx;
        if (!visible) return null;
        const status = pointer == null ? "" : (doneAll || n < pointer) ? "done" : n === pointer ? "cur" : "up";
        const dur = p.meta?.duration_minutes;
        return (
          <div className={`co-card ${status}`} key={i} onClick={() => onOpenUnit(n)}>
            <span className="co-num">{n + 1}.</span>
            <div className="co-body"><div className="co-utitle">{p.title || `Unit ${n + 1}`}</div></div>
            <div className="co-side">
              {status === "cur" ? <span className="co-now">now</span> : null}
              {dur ? <span className="co-dur"><span className="co-dur-n">{dur}</span><span className="co-dur-u">min</span></span> : null}
              {status === "done" ? <span className="co-mark">✓ taught</span> : null}
            </div>
          </div>
        );
      });
      if (visible) bars.push(<div className="co-list" key={`${keyPrefix}-list`}>{cards}</div>);
    }
    (g.children || []).forEach((c, i) => bars.push(...renderGroup(c, depth + 1, `${keyPrefix}-${i}`, visible)));
    return bars;
  };

  const total = units.length;
  const taught = pointer == null ? 0 : doneAll ? total : pointer;
  // Duration breakdown for the meta line, e.g. "2 units × 35 min · 1 unit × 45 min"
  // (grouped by each unit's period duration, shortest first).
  const durCounts = {};
  units.forEach((u) => { const d = u.meta?.duration_minutes; if (d) durCounts[d] = (durCounts[d] || 0) + 1; });
  // Period combination, stacked one per line, e.g. "3 × 40 min" / "4 × 50 min"
  // (grouped by duration, shortest first).
  const durParts = Object.entries(durCounts)
    .sort((a, b) => Number(a[0]) - Number(b[0]))
    .map(([d, c]) => `${c} × ${d} min`);
  // The organizing axis (or axes) of this chapter — the type of the top-level groups, plus any
  // nested grouping type. Named + explained below the header rule so the teacher knows what the
  // drop-downs represent. Each blurb carries a DEFINITE BUT MILD nod to the NCF (founder
  // 2026-07-13): the reference is made only where the axis genuinely reflects NCF pedagogy —
  // Science's staged inquiry (§4.6.1), the NCF's competency-based design (Social Sciences), and
  // the integrated language-skills the NCF asks of languages (English spine). Section is the
  // most structural axis, so its nod is the lightest (graded, build-from-the-familiar sequencing).
  const AXIS_INFO = {
    stage: ["Stages", "the learning progression each group moves through, from first contact to confident practice — the staged, inquiry-led sequence the NCF asks of Science."],
    progression_stage: ["Stages", "the learning progression each group moves through, from first contact to confident practice — the staged, inquiry-led sequence the NCF asks of Science."],
    section: ["Sections", "the parts of the chapter, taught in the graded, build-from-the-familiar sequence the NCF encourages."],
    competency: ["Competencies", "the skill each group of units builds — the competency-based design at the heart of the NCF."],
    spine: ["Spines", "the language skills the units develop together, in the integrated way the NCF asks languages to be taught."],
  };
  const axisTypes = [];
  const collectAxis = (groups) => (groups || []).forEach((g) => {
    if (g.type && AXIS_INFO[g.type] && !axisTypes.includes(g.type)) axisTypes.push(g.type);
    collectAxis(g.children);
  });
  collectAxis(lp.groups);
  return (
    <div className="lessonview co-view" data-subject={lp.subject || ""}>
      {/* Frozen header — stays pinned down through the meta row; the unit list scrolls under it.
          data-tour="preview-back" (preview only): the guided tour's step-4 hand sits on the exit. */}
      <div className="co-stick">
        <div className="co-topbar">
          {/* {subject} · {class as Roman} · Ch. NN (founder 2026-07-10). */}
          <span className="kicker kicker-soft co-topkick">
            {String(lp.subject || "").replace(/_/g, " ")}
            {lp.grade ? ` · ${String(lp.grade).replace(/grade|class/gi, "").trim().toUpperCase()}` : ""}
            {lp.chapter_number ? ` · Ch. ${String(lp.chapter_number).padStart(2, "0")}` : ""}
          </span>
          <button className="back back-tr" data-tour={backTour} onClick={onBack}>← back</button>
        </div>
        <div className="co-head">
          <div className="co-title">{lp.chapter_title}</div>
          <div className="co-meta">
            {total} Learning Unit{total !== 1 ? "s" : ""}{durParts.length ? ` ${durParts.join(". ")}` : ""}
          </div>
          {pointer != null ? (
            <div className="co-rail" aria-label={`${taught} of ${total} units taught`}>
              {units.map((_, i) => (
                <span key={i} className={`co-tick ${doneAll || i < pointer ? "done" : i === pointer ? "cur" : ""}`} />
              ))}
            </div>
          ) : null}
        </div>
        {/* Hairline divider under the meta — frozen with the header. */}
        <div className="co-headrule" aria-hidden="true"></div>
        {/* Axis legend — names the organizing axis of the drop-downs + a small explanation.
            Frozen WITH the header (founder 2026-07-11): the note on the axis stays pinned
            as the unit list scrolls beneath it. Maths PREP (the flat case) has no group
            axis, but the legend must not simply vanish (founder 2026-07-14) — it gets its
            own row describing the flat organization, with a tap hint that matches flat
            cards (each card IS a unit; there is nothing "underneath"). */}
        {mathsFlat ? (
          <div className="co-axis">
            <div className="co-axis-row">
              <span className="co-axis-name">Units</span>
              <span className="co-axis-blurb">one continuous run of learning units in the textbook&apos;s own teaching order — the activity-led, play-way flow the NCF asks of the preparatory stage. Tap a unit to open it.</span>
            </div>
          </div>
        ) : axisTypes.length ? (
          <div className="co-axis">
            {axisTypes.map((t) => (
              <div className="co-axis-row" key={t}>
                <span className="co-axis-name">{AXIS_INFO[t][0]}</span>
                <span className="co-axis-blurb">{AXIS_INFO[t][1]} Click each card to access units underneath.</span>
              </div>
            ))}
          </div>
        ) : null}
      </div>
      {mathsFlat ? (
        /* Maths prep — no axis: units flat under the header (no "Lesson" bucket header —
           founder 2026-07-13: remove the word). Beyond 4 units the list lives in a capped
           "wheel" window that scrolls internally; a soft bottom fade hints "more below".
           Flat idx = card order, so pointer status maps 1:1 to the unit. */
        (() => {
          const periods = lp.groups[0].periods || [];
          const list = (
            <div className="co-list">
              {periods.map((p, i) => {
                const n = i;
                const status = pointer == null ? "" : (doneAll || n < pointer) ? "done" : n === pointer ? "cur" : "up";
                const dur = p.meta?.duration_minutes;
                return (
                  <div className={`co-card ${status}`} key={i} onClick={() => onOpenUnit(n)}>
                    <span className="co-num">{n + 1}.</span>
                    <div className="co-body"><div className="co-utitle">{p.title || `Unit ${n + 1}`}</div></div>
                    <div className="co-side">
                      {status === "cur" ? <span className="co-now">now</span> : null}
                      {dur ? <span className="co-dur"><span className="co-dur-n">{dur}</span><span className="co-dur-u">min</span></span> : null}
                      {status === "done" ? <span className="co-mark">✓ taught</span> : null}
                    </div>
                  </div>
                );
              })}
            </div>
          );
          return periods.length > FLAT_SHOWN ? (
            <div className="co-flatwrap">
              <div className="co-flatscroll">{list}</div>
              <div className="co-flatfade" aria-hidden="true" />
            </div>
          ) : list;
        })()
      ) : lp.groups.map((g, gi) => {
        const open = openIdx === gi;
        // Render the body (periods + children) for EVERY group so idx advances in order;
        // the group's own label becomes the clickable header, so skip it in the body walk.
        const body = renderGroup({ periods: g.periods, children: g.children, type: g.type }, 0, `g${gi}`, open);
        const cnt = countUnits(g);
        return (
          // The OPEN axis is the filled one; closed axes render unfilled/white so the
          // options read as options (founder 2026-07-10).
          <div className={`co-acc${open ? " open" : ""}`} key={gi}>
            <button
              className={`co-acchead${open ? " open" : ""}`}
              onClick={() => setOpenIdx(open ? -1 : gi)}
              aria-expanded={open}
            >
              <span className="co-acc-name">{(lp.subject === "science" && g.type === "section" ? sectionTitleOnly(g.label) : g.label) || `Section ${gi + 1}`}</span>
              <span className="co-count">{cnt}</span>
              <span className="co-chev" aria-hidden="true">
                <svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M2.5 4.5L6 8l3.5-3.5" />
                </svg>
              </span>
            </button>
            {open ? <div className="co-accbody">{body}</div> : null}
          </div>
        );
      })}
      {/* Chapter Notes — ONE collapsed, pull-based control opening the notebook popup
          (arch-plan §I-bis). Mark + teaser when a note exists; quiet "＋" when empty. */}
      <div className={`co-notes${hasNote ? " has" : ""}`}>
        <button onClick={() => setNotesOpen(true)}>
          <span className="kicker kicker-soft">Chapter notes</span>
          {hasNote ? (
            <span className="co-note-teaser">{noteText.trim()}</span>
          ) : (
            <span className="co-hint">none yet · ＋</span>
          )}
        </button>
      </div>
      {notesOpen ? (
        <ChapterNotesModal
          chapterTitle={lp.chapter_title}
          subjectGrade={cnSubjectGrade(lp)}
          initial={noteText}
          onSave={saveNote}
          onClose={() => setNotesOpen(false)}
        />
      ) : null}
    </div>
  );
}

export default function LessonView({ view, sectionKey = "", onExit, preview = false }) {
  const lp = view.lesson_plan;
  const units = useMemo(() => flattenUnits(lp), [lp]);
  // Preview root — used to reset scroll to the top of the unit when paging (see pvGoto).
  const pvRef = useRef(null);
  const storageKey = `lu_pointer_${sectionKey || lp.subject + "_" + lp.grade + "_" + (lp.chapter_title || "")}`;

  // current pointer (which LU the teacher is on) — restore from localStorage
  const [cur, setCur] = useState(() => {
    if (typeof window === "undefined") return 0;
    const saved = Number(window.localStorage.getItem(storageKey));
    return Number.isFinite(saved) && saved >= 0 && saved < units.length ? saved : 0;
  });
  // Chapter Organization altitude (the chapter's front door). Preview OPENS here — reading a
  // plan starts at chapter altitude (arch-plan §E); once a pointer is live (tracking), the unit
  // view is the default and the org page is one tap away ("chapter organization →").
  const [showOrg, setShowOrg] = useState(preview);
  // After "Mark complete" we show a confirmation + an Undo that reverts to this index. The undo
  // target is INTENTIONALLY in-session only (not persisted): the pointer itself is the source of
  // truth and already saved, so undo is just a convenience for the immediate "oops, wrong button"
  // moment. It's harmless either way — a teacher can always step back by marking again from the
  // full plan — so we don't carry it across refreshes/visits, which would otherwise keep the
  // confirmation card up indefinitely and hide the plain mark-complete action for the new unit.
  const [undoTo, setUndoTo] = useState(null);    // index to revert to, or null = nothing to undo
  // "View full lesson plan" re-renders THIS view in preview layout; previewAt = which unit shows.
  const [showFullPlan, setShowFullPlan] = useState(false);
  // index of the unit shown in full-plan preview — defaults to the current pointer so the teacher
  // lands on the unit she's teaching (the next LU after the last one marked complete).
  const [previewAt, setPreviewAt] = useState(() => {
    if (typeof window === "undefined") return 0;
    const saved = Number(window.localStorage.getItem(storageKey));
    return Number.isFinite(saved) && saved >= 0 && saved < units.length ? saved : 0;
  });

  // Completion flag (per section) — the ONLY signal that a chapter is fully taught, since the
  // pointer clamps at the last unit and can't otherwise distinguish "on the last LU" from "done".
  // My Classes reads `lu_done_${sectionKey}` to shade the card as completed. Mirrored in React
  // state so marking the chapter complete re-renders the view (confirmation card) immediately.
  const doneKey = `lu_done_${sectionKey || lp.subject + "_" + lp.grade + "_" + (lp.chapter_title || "")}`;
  const [doneFlag, setDoneFlag] = useState(() => {
    if (typeof window === "undefined") return false;
    try { return window.localStorage.getItem(doneKey) === "1"; } catch { return false; }
  });
  const setDone = (v) => {
    setDoneFlag(v);
    try {
      if (v) window.localStorage.setItem(doneKey, "1");
      else window.localStorage.removeItem(doneKey);
    } catch {}
    pushSectionState(sectionKey);   // sync completion to the server (cross-device)
  };

  const writePointer = (i) => {
    const clamped = Math.max(0, Math.min(units.length - 1, i));
    setCur(clamped);
    try { window.localStorage.setItem(storageKey, String(clamped)); } catch {}
    if (clamped < units.length - 1) setDone(false);   // moved back off the last unit → not done
    pushSectionState(sectionKey);   // sync the advanced pointer to the server (cross-device)
    return clamped;
  };

  const markComplete = () => {
    if (cur >= units.length - 1) { writePointer(units.length - 1); setDone(true); setUndoTo(null); return; }
    const from = cur;
    writePointer(cur + 1);
    setUndoTo(from);
  };
  const undoComplete = () => {
    if (undoTo == null) return;
    writePointer(undoTo);
    setUndoTo(null);
  };

  if (!units.length) {
    return (<div><button className="back" onClick={onExit}>← back</button><div className="empty">This plan has no units.</div></div>);
  }

  // The unit the teacher is currently on (also the assessment scope — see below).
  const curUnit = units[cur] || units[0];

  // ── Chapter Organization altitude — preview's landing page; one tap away in tracking ──
  if (showOrg) {
    return (
      <div data-tour={preview ? "preview-root" : undefined}>
        <ChapterOrg
          lp={lp} units={units}
          pointer={preview ? null : cur} doneAll={doneFlag}
          onOpenUnit={(n) => {
            // Navigation, never pointer movement: open the tapped unit read-only.
            setPreviewAt(n); setShowOrg(false);
            if (!preview) setShowFullPlan(true);
          }}
          onBack={preview ? onExit : () => setShowOrg(false)}
          backTour={preview ? "preview-back" : undefined}
        />
      </div>
    );
  }

  // ── Preview / "View full lesson plan" — ONE unit at a time, back/forward navigation ──
  // Opened from the Chapter Organization page (card tap) or the in-view "View full lesson
  // plan" button (showFullPlan). Defaults to the current pointer so the teacher lands where
  // she's teaching, then can page through the whole plan. Read-only: no pointer controls.
  if (preview || showFullPlan) {
    const pu = units[previewAt] || units[0];
    // Change the shown unit AND reset scroll to the top of the unit view. Without this, paging
    // from the bottom nav strip leaves the window scrolled down at the frozen header, so the new
    // unit opens mid-way; we land the teacher at the unit's start, just under the pinned header.
    const pvGoto = (n) => {
      setPreviewAt(n);
      if (typeof window === "undefined") return;
      requestAnimationFrame(() => {
        const el = pvRef.current;
        if (!el) { window.scrollTo({ top: 0 }); return; }
        const navH = parseInt(getComputedStyle(document.documentElement).getPropertyValue("--nav-h"), 10) || 118;
        const y = el.getBoundingClientRect().top + window.scrollY - navH;
        window.scrollTo({ top: Math.max(0, y) });
      });
    };
    // The orange-line prev/next strip — rendered pinned in the header AND again at the end of
    // the lesson body (same row, so the teacher can page on from the bottom).
    const pvNav = (endClass = "") => (
      <div className={`lv-pvnav lv-pvnav-thin ${endClass}`}>
        <button className={`lv-pvbtn ${previewAt <= 0 ? "off" : ""}`}
          onClick={() => previewAt > 0 && pvGoto(previewAt - 1)} disabled={previewAt <= 0}>← Previous unit</button>
        <span className="lv-pvmid">Unit {previewAt + 1} / {units.length}</span>
        <button className={`lv-pvbtn ${previewAt >= units.length - 1 ? "off" : ""}`}
          onClick={() => previewAt < units.length - 1 && pvGoto(previewAt + 1)} disabled={previewAt >= units.length - 1}>Next unit →</button>
      </div>
    );
    // Header name-plate for the frozen block (the top orange prev/next strip is retired here —
    // paging now lives only in the bottom strip). data-tour="preview-back": tour step 4's hand.
    // ONE top row (founder 2026-07-10): the unit name-plate sits UP in the first row,
    // wrapping as needed, with the back button beside it top-right — no row spent on
    // the back button alone.
    const headerContent = (
      <div className="lv-hd lv-hd-merge">
        <div className="lv-title lv-title-full"><span className="lv-unum">{previewAt + 1}.</span>{pu.title}</div>
        <button className="back back-tr" data-tour="preview-back"
          onClick={showFullPlan ? () => setShowFullPlan(false) : () => setShowOrg(true)}>
          ← back
        </button>
      </div>
    );
    return (
      // data-tour="preview-root": the guided tour's step-4 spotlight wraps the open preview.
      <div className="lessonview lv-pvview" data-tour="preview-root" ref={pvRef}>
        {/* Frozen block — header AND the Overview/Material/Lesson/Assess tab bar stay pinned;
            only the active panel scrolls beneath. Keyed by unit so paging resets to Overview. */}
        <PreviewUnit key={previewAt} headerContent={headerContent} u={pu} assessment={view.assessment} chapterTitle={lp.chapter_title} />
        {/* Prev/next paging strip at the end of the lesson body. */}
        {pvNav("lv-pvnav-end")}
        {/* The preview is READ-ONLY: the old "Attach to a class" CTA is retired (2026-07-06) —
            attaching happens only via the "+" on a My Classes section card. */}
      </div>
    );
  }

  // ── Tracking view (Screen 3) — current unit only + completion model ──
  const u = curUnit;
  const total = units.length;
  const done = cur;                          // units completed before the current one

  return (
    // data-tour="lesson-root": the guided tour's step-7 spotlight wraps the tracking view.
    <div className="lessonview" data-tour="lesson-root">
      <button className="back" onClick={onExit}>← back to my plans</button>
      <div className="lv-hd">
        <div className="lv-hd-row">
          <div>
            <div className="kicker kicker-ochre">{lp.chapter_title}</div>
            <div className="lv-title"><span className="lv-unum">{cur + 1}.</span>{u.title}</div>
          </div>
          <div className="lv-count">Unit {cur + 1} of {total}</div>
        </div>
        {/* Spine / time / pedagogy moved into the OVERVIEW tab (2026-07-10) — the header
            keeps only the name-plate + the chapter-altitude link. */}
        <div className="lv-hd-row">
          <span />
          {/* Chapter altitude, one tap away — navigation, never pointer movement. */}
          <span className="uv-orglink" onClick={() => setShowOrg(true)}>chapter organization →</span>
        </div>
      </div>

      {/* Progress bar — same segmented look as the section bars in My Lesson Plans / Track. */}
      <div className="lv-progress" aria-label={doneFlag ? `all ${total} units complete` : `${done} of ${total} units complete`}>
        {Array.from({ length: total }, (_, i) => (
          <span key={i} className={`lv-seg ${doneFlag || i < cur ? "fill" : i === cur ? "now" : ""}`} />
        ))}
      </div>

      <UnitTabs key={cur} u={u} assessment={view.assessment} chapterTitle={lp.chapter_title} />
      {/* 📝 Period note — an invoked control (tracking only: notes belong to the section's
          plan instance, not the shared asset). */}
      <NoteInvoke />

      {/* Completion action (or the post-complete confirmation + Undo). */}
      {undoTo != null ? (
        <div className="lv-donecard">
          <div className="lv-donerow">
            <div className="lv-doneleft">
              <div className="lv-donemark">✓</div>
              <div>
                <div className="lv-donetitle">Unit marked complete</div>
                <div className="lv-donesub">Section is now ready for the next unit.</div>
              </div>
            </div>
            <button className="lv-undo" onClick={undoComplete}>↺ Undo</button>
          </div>
          {/* After marking complete, the pointer has ALREADY advanced — so units[cur] IS the next
              unit. "Open next unit" just dismisses this confirmation to reveal its teaching view. */}
          <div className="lv-nextup">
            <span className="lv-nextup-k">Next up</span>
            <div className="lv-nextup-t">{u.title}</div>
            {/* LO is never shown in the LP (founder rule 2026-07-09) — the next-up card names
                the unit only; outcomes surface in the assessment artifact. */}
            {/* Before starting the next unit, a teacher often wants to glance at how the rest of
                the chapter pans out — so the preview lives HERE, paired with Open next unit, not
                as a standalone utility. It opens at the next (now-current) unit. */}
            <div className="lv-nextbtns">
              <button className="primary lv-nextbtn" onClick={() => setUndoTo(null)}>Open next unit →</button>
              <span className="lv-previewlink" onClick={() => { setPreviewAt(cur); setShowFullPlan(true); }}>Preview full chapter →</span>
            </div>
          </div>
        </div>
      ) : cur >= total - 1 ? (
        doneFlag ? (
          // Chapter fully taught — the confirmation the section card reads as "completed" (gold).
          <div className="lv-donecard lv-chapterdone">
            <div className="lv-donerow">
              <div className="lv-doneleft">
                <div className="lv-donemark">✓</div>
                <div>
                  <div className="lv-donetitle">Chapter complete</div>
                  <div className="lv-donesub">Every unit is taught. This class now shows as completed on your home screen.</div>
                </div>
              </div>
              <button className="lv-undo" onClick={() => setDone(false)}>↺ Reopen</button>
            </div>
          </div>
        ) : (
          <div className="lv-markcard">
            <div className="lv-markinfo">
              <span className="lv-markicon" aria-hidden="true">ⓘ</span>
              <span>This is the final unit. Marking it complete finishes the chapter for this section.</span>
            </div>
            <button className="primary lv-markbtn" data-tour="mark-complete" onClick={markComplete}>Mark chapter complete</button>
          </div>
        )
      ) : (
        <div className="lv-markcard">
          <div className="lv-markinfo">
            <span className="lv-markicon" aria-hidden="true">ⓘ</span>
            <span>Marking this unit complete moves the teaching position to the next unit for this section.</span>
          </div>
          {/* data-tour="mark-complete": the guided tour's step-8 spotlight + hand sit here. */}
          <button className="primary lv-markbtn" data-tour="mark-complete" onClick={markComplete}>Mark this unit complete</button>
        </div>
      )}
    </div>
  );
}
