"use client";
import { useMemo, useRef, useState } from "react";
import { pushSectionState } from "../lib/sectionState";

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
 * Assessment "tags along" as a dedicated green sub-view — reachable from BOTH the tracking
 * view (scoped to the current unit) and the unit preview (scoped to the previewed unit;
 * §I-ter: preview shows future periods, their assessment comes along for free). */

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

/* One unit's teaching content — THE STANDARD ANATOMY (2026-07-09, founder-approved;
 * spec docs/mockups/lesson-period-layout.html): teacher notes (clay margin-note, TOP)
 * → materials (hairline box) → phases (duration in the marginal rail) → homework (the
 * one tinted block, BOTTOM) → 📝 note-invoke (a control, never an empty box).
 * LO is NEVER rendered here — reserved for assessment. Identical for every subject;
 * slots simply stay empty where a subject has no data. */
function UnitBody({ u, assessment, onAssess }) {
  const phases = (u.phases || []).filter((ph) => ph.text || ph.label);
  return (
    <>
      {/* 1 · Teacher notes — prep reading, a colleague's margin note.
          data-tour="lesson-notes": the tour positions its box relative to this block. */}
      {u.teacher_notes?.length ? (
        <div className="uv-tnotes" data-tour="lesson-notes">
          <span className="kicker">Teacher notes</span>
          <p>{u.teacher_notes.join(" ")}</p>
        </div>
      ) : null}

      {/* 2 · Materials — the pre-class checklist. */}
      {u.materials?.length ? (
        <>
          <span className="kicker kicker-soft uv-slotk">Materials</span>
          <div className="uv-mat"><ul>{u.materials.map((m, i) => <li key={i}>{m}</li>)}</ul></div>
        </>
      ) : null}

      {/* 3 · Phases — the hero; durations in the marginal rail, one aligned column.
          First phase carries data-tour="lesson-phase-1" (tour step 8 hangs below it).
          Legacy fallback: plans normalized before Phase landed render activities lines. */}
      <div className="lv-phasehd uv-slotk">
        <span className="kicker">Lesson</span>
        {assessment && onAssess ? <span className="lv-assesslink" onClick={onAssess}>assessment here →</span> : null}
      </div>
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

      {/* 4 · Homework — the single tinted block, full text (no word caps). */}
      {u.homework ? (
        <div className="uv-hw">
          <span className="kicker">Homework</span>
          <p>{u.homework}</p>
        </div>
      ) : null}
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

// Typed stimulus/passage block — same typing as LP visuals (svg / table / prose).
function ATyped({ b, passage = false }) {
  if (!b || !b.content) return null;
  if (b.type === "svg") return <div className="assess-vs assess-vs-svg" dangerouslySetInnerHTML={{ __html: b.content }} />;
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
function AReveals({ reveals }) {
  const entries = Object.entries(reveals || {});
  if (!entries.length) return null;
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
                <span>{txt}</span>
              </div>
            ))}
      </div>
    </div>
  );
}

// The pre-contract card (plans normalized before NormalizedItem shipped).
function ALegacyCard({ it }) {
  return (
    <>
      <div className="assess-qtype">{it.item_type}</div>
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

function AssessCard({ it }) {
  const n = it.normalized;
  const lo = n ? n.linked_lo : (it.meta?.linked_lo || it.implied_lo);
  return (
    <div className="assess-card">
      {/* LEARNING OUTCOME — per item, above the stem; ABSENT (no label) when null. */}
      {lo ? (
        <div className="assess-lo">
          <span className="assess-lo-k">LEARNING OUTCOME</span>
          <div className="assess-lo-t">{lo}</div>
        </div>
      ) : null}
      {!n || !n.template ? <ALegacyCard it={it} /> : (
        <>
          <div className="assess-metarow">
            <span className="assess-qtype">{n.question_type.replace(/_/g, " ")}</span>
            {n.cognitive_demand ? <span className="assess-cog">{n.cognitive_demand}</span> : null}
          </div>
          {/* T6c (EXTRACT_ANALYSIS): the extract is set off BEFORE the multi-part stem. */}
          {n.template === "passage" ? <ATyped b={n.passage} passage /> : null}
          <div className="assess-prompt">{n.stem}</div>
          {/* Listening input the item can't run without — a cue, never a citation. */}
          {n.audio_ref ? <span className="assess-audio">🔊 Listening passage · {n.audio_ref} (read aloud)</span> : null}
          <ATyped b={n.visual_stimulus} />

          {/* ── the marking surface, per template ── */}
          {n.template === "selected_response" ? (
            <>
              <ul className="assess-opts2">
                {(n.options || []).map((o, i) => (
                  <li key={i} className={o.is_correct ? "correct" : ""}>
                    <span className="assess-opt-lab">{o.label || String.fromCharCode(65 + i)}</span>
                    <span>{o.text}{o.is_correct ? <span className="assess-tickmark"> ✓</span> : null}</span>
                  </li>
                ))}
              </ul>
              {/* TRUE_FALSE verdict+justification arrives as model_answer, not reveals. */}
              <ABlock k="ANSWER" text={n.model_answer} />
              <AReveals reveals={n.option_reveals} />
            </>
          ) : n.template === "scr" ? (
            n.model_answer
              ? <ABlock k="SUGGESTED ANSWER" text={n.model_answer} />
              : <ATicks k="LOOK FOR" items={n.expected_elements} />
          ) : n.template === "ecr" ? (
            <>
              <ATicks k="LOOK FOR" items={n.look_fors} />
              <ATicks k="EXPECTED ELEMENTS" items={n.expected_elements} />
              <ABlock k="SUGGESTED ANSWER" text={n.model_answer} />
              <ABlock k="SCAFFOLD" text={n.scaffold} />
            </>
          ) : n.template === "open_task" ? (
            <>
              <ATicks k="WHAT TO PRODUCE" items={n.format_of_output} />
              <ATicks k="EXPECTED ELEMENTS" items={n.expected_elements} />
              <ATicks k="LOOK FOR" items={n.look_fors} />
              <ABlock k="SCAFFOLD" text={n.scaffold} />
              {n.open_task_guide ? (
                /* the rich OPEN_TASK guide stays collapsed so the card isn't a wall on a phone */
                <details className="assess-otg">
                  <summary>TEACHER GUIDE — READING THIS TASK</summary>
                  <div className="assess-otg-body">
                    <ABlock k="FORMAT" text={[n.open_task_guide.format_type, n.open_task_guide.format_rationale].filter(Boolean).join(" — ")} />
                    <ABlock k="WHAT THIS DEMONSTRATES" text={n.open_task_guide.what_this_demonstrates} />
                    <ABlock k="READING THE SCAFFOLD" text={n.open_task_guide.reading_the_scaffold} />
                    <ABlock k="STRONG VS WEAK MARKERS" text={n.open_task_guide.strong_vs_weak_markers} />
                  </div>
                </details>
              ) : null}
            </>
          ) : n.template === "cloze_match" ? (
            <ABlock k="ANSWER KEY" text={n.model_answer} />
          ) : n.template === "oral" ? (
            <ATicks k="SPEAKING RUBRIC" items={n.expected_elements} />
          ) : n.template === "numeric" ? (
            <>
              <ABlock k="WORKED ANSWER" text={n.model_answer} />
              <ABlock k="METHOD" text={n.method_one_line} />
              <ABlock k="TEXTBOOK" text={n.exercise_ref} />
            </>
          ) : n.template === "passage" ? (
            <ATicks k="EXPECTED ELEMENTS" items={n.expected_elements} />
          ) : null}

          <ABlock k="INCLUSIVITY" text={n.inclusivity} />
        </>
      )}
    </div>
  );
}

/* ── Chapter Organization — the chapter's front door (chapter altitude, arch-plan §E).
 * The My Classes section card, opened up: the same tick rail expands into one card per
 * unit (pine = taught · ochre = now · hairline = ahead), grouped under quiet mono
 * dividers from the plugin's Group tree. Tapping a card is NAVIGATION, never pointer
 * movement. `pointer` is the live unit index, or null (preview — no place-marker). */
function ChapterOrg({ lp, units, pointer, doneAll, onOpenUnit, onBack, backTour }) {
  const [noteMsg, setNoteMsg] = useState(false);
  // Each top-level group is a collapsible drop-down; only ONE is open at a time (accordion).
  // The first group opens by default; opening another closes the rest (re-tapping the open
  // one collapses it). -1 = all closed.
  const [openIdx, setOpenIdx] = useState(0);
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
          <span className={`kicker ${depth > 0 ? "" : "kicker-soft"}`}>{g.label}</span>
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
  const durBreakdown = Object.entries(durCounts)
    .sort((a, b) => Number(a[0]) - Number(b[0]))
    .map(([d, c]) => `${c} unit${c !== 1 ? "s" : ""} × ${d} min`)
    .join(" · ");
  return (
    <div className="lessonview co-view">
      {/* Frozen header — stays pinned down through the meta row; the unit list scrolls under it.
          data-tour="preview-back" (preview only): the guided tour's step-4 hand sits on the exit. */}
      <div className="co-stick">
        <div className="co-topbar">
          <span className="kicker kicker-soft co-topkick">{String(lp.subject || "").replace(/_/g, " ")} · {lp.chapter_title ? `Chapter ${lp.chapter_number || ""}`.trim() : ""}</span>
          <button className="back back-tr" data-tour={backTour} onClick={onBack}>← back</button>
        </div>
        <div className="co-head">
          <div className="co-title">{lp.chapter_title}</div>
          <div className="co-meta">
            <span className="co-lu">{total} Learning Unit{total !== 1 ? "s" : ""}</span>
            {durBreakdown ? <span className="co-break">{durBreakdown}</span> : null}
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
      </div>
      {lp.groups.map((g, gi) => {
        const open = openIdx === gi;
        // Render the body (periods + children) for EVERY group so idx advances in order;
        // the group's own label becomes the clickable header, so skip it in the body walk.
        const body = renderGroup({ periods: g.periods, children: g.children, type: g.type }, 0, `g${gi}`, open);
        const cnt = countUnits(g);
        return (
          <div className="co-acc" key={gi}>
            <button
              className={`co-acchead${open ? " open" : ""}`}
              onClick={() => setOpenIdx(open ? -1 : gi)}
              aria-expanded={open}
            >
              <span className="kicker kicker-soft">{g.label || `Section ${gi + 1}`}</span>
              <span className="co-count">{cnt} unit{cnt !== 1 ? "s" : ""}</span>
              <span className="co-chev" aria-hidden="true">{open ? "–" : "+"}</span>
            </button>
            {open ? <div className="co-accbody">{body}</div> : null}
          </div>
        );
      })}
      {/* Chapter Notes — ONE collapsed, pull-based control (v0.2 §Chapter Notes; deferred). */}
      <div className="co-notes">
        <button onClick={() => setNoteMsg((v) => !v)}>
          <span className="kicker kicker-soft">Chapter notes</span>
          <span className="co-hint">{noteMsg ? "coming in an upcoming update" : "none yet · ＋"}</span>
        </button>
      </div>
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
  // 3b assessment view: null = closed, otherwise the INDEX of the unit it is scoped to.
  // Opened from the tracking view (scoped to the current unit) AND from preview (scoped to
  // the previewed unit — §I-ter: preview shows future periods, so future assessment comes
  // along for free).
  const [showAssess, setShowAssess] = useState(null);
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

  // ── Assessment artifact (3b) — SCOPED to the current learning unit ──
  // The link resolver (aruvi_core, architecture-plan.md §Link resolution) stamps every item
  // with meta.linked_periods[] — the period set it belongs to. Each LU here IS one period
  // (its `number`), so we show ONLY the items whose linked_periods include this unit's period.
  // This is the fix for "the assessment showed every item": it now tags along with the unit.
  if (showAssess != null) {
    const a = view.assessment;
    const aUnit = units[showAssess] || units[0];
    const pnum = aUnit.number;
    const allItems = a.groups.flatMap((g) => g.items);
    // Items linked to THIS unit's period; fall back to all items only if nothing carries link
    // metadata (e.g. an older view served before the resolver shipped) so we never show nothing
    // by mistake on legacy data.
    const anyLinked = allItems.some((it) => Array.isArray(it.meta?.linked_periods) && it.meta.linked_periods.length);
    const items = anyLinked
      ? allItems.filter((it) => (it.meta?.linked_periods || []).includes(pnum))
      : allItems;
    return (
      <div className="lessonview">
        {/* Back sits ABOVE the green box in a sticky top bar — same vertical level as the
            lesson-plan back button (shared .lv-stick/.lv-topbar), which also restores the
            gap under the tabs on mobile. */}
        <div className="lv-stick">
          <div className="lv-topbar">
            <span />
            <button className="back back-tr" onClick={() => setShowAssess(null)}>← back</button>
          </div>
        </div>
        <div className="assess assess-standalone">
          <div className="assess-hd">
            <div className="assess-hd-row">
              <span className="assess-tag">ASSESSMENT</span>
            </div>
            <div className="assess-title">{a.chapter_title || lp.chapter_title}</div>
          </div>
          <div className="assess-body">
            {items.length === 0 ? (
              <div className="assess-empty">No assessment item tags along with this unit. Move through the unit — items appear at the units that build the outcome they test.</div>
            ) : items.map((it, ii) => <AssessCard it={it} key={ii} />)}
            <button className="assess-backbtn" onClick={() => setShowAssess(null)}>← back</button>
          </div>
        </div>
      </div>
    );
  }

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
    const dur = pu.meta?.duration_minutes;
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
    return (
      // data-tour="preview-root": the guided tour's step-4 spotlight wraps the open preview.
      <div className="lessonview lv-pvview" data-tour="preview-root" ref={pvRef}>
        {/* Frozen header — back + title + spine + time/pedagogy + nav all stay pinned; the
            unit body scrolls under them. data-tour="preview-back": tour step 4's hand sits here. */}
        <div className="lv-stick">
          <div className="lv-topbar">
            {pu.context ? <span className="kicker lv-stage lv-topspine">Spine: {pu.context}</span> : <span />}
            <button className="back back-tr" data-tour="preview-back"
              onClick={showFullPlan ? () => setShowFullPlan(false) : () => setShowOrg(true)}>
              ← back
            </button>
          </div>
          <div className="lv-hd">
            <div className="lv-title lv-title-full"><span className="lv-unum">{previewAt + 1}.</span>{pu.title}</div>
            {dur || pu.approach ? (
              <div className="uv-durline lv-tpline">
                {dur ? <span><strong>Time</strong>: {dur} mins</span> : null}
                {pu.approach ? <span><strong>Pedagogy</strong>: {pu.approach}</span> : null}
              </div>
            ) : null}
          </div>

          {pvNav()}
        </div>

        {/* Assessment is part of the period view in preview too (§I-ter: future periods'
            assessment comes along for free) — scoped to the unit being previewed. */}
        <UnitBody u={pu} assessment={view.assessment} onAssess={() => setShowAssess(previewAt)} />
        {/* Same nav strip at the end of the lesson body — page prev/next from the bottom too. */}
        {pvNav("lv-pvnav-end")}
        {/* The preview is READ-ONLY: the old "Attach to a class" CTA is retired (2026-07-06) —
            attaching happens only via the "+" on a My Classes section card. */}
      </div>
    );
  }

  // ── Tracking view (Screen 3) — current unit only + completion model ──
  const u = curUnit;
  const stageKicker = (u.context || "").toUpperCase();
  const uDur = u.meta?.duration_minutes;
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
        {stageKicker ? <div className="kicker lv-stage">{stageKicker}</div> : null}
        <div className="lv-hd-row">
          {uDur || u.approach ? (
            <div className="uv-durline">{uDur ? <b>{uDur} min</b> : null}{uDur && u.approach ? " · " : ""}{u.approach || ""}</div>
          ) : <span />}
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

      <UnitBody u={u} assessment={view.assessment} onAssess={() => setShowAssess(cur)} />
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
