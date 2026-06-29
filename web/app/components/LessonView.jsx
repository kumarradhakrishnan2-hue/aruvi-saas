"use client";
import { useMemo, useState } from "react";

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
 * Assessment "tags along" as a dedicated green sub-view (tracking mode only). */

// Flatten groups → a single ordered Learning Unit list, carrying the parent group label
// (progression stage / section / spine) as context for each unit.
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

// One unit's teaching content (phases + outcomes + notes + homework). Shared by the
// current-unit tracking view and the preview "full plan" listing.
function UnitBody({ u, totalMin, assessment, onAssess }) {
  return (
    <>
      <div className="lv-phasehd">
        <span className="kicker kicker-soft">PHASES{totalMin ? ` · ${totalMin} MIN TOTAL` : ""}</span>
        {assessment && onAssess ? <span className="lv-assesslink" onClick={onAssess}>assessment here →</span> : null}
      </div>
      {(u.activities && u.activities.length) ? u.activities.map((act, i) => (
        <div className="phaserow" key={i}><span className="phasetext">{act}</span></div>
      )) : <div className="empty">No phases recorded for this unit.</div>}
      {u.learning_outcomes?.length ? (
        <div className="lv-lo"><span className="lv-lo-k">Learning outcome</span> {u.learning_outcomes.join("; ")}</div>
      ) : null}
      {u.teacher_notes?.length ? <div className="lv-tnote">{u.teacher_notes.join(" ")}</div> : null}
      {u.homework ? <div className="lv-lo"><span className="lv-lo-k">Homework</span> {u.homework}</div> : null}
    </>
  );
}

export default function LessonView({ view, sectionKey = "", onExit, preview = false }) {
  const lp = view.lesson_plan;
  const units = useMemo(() => flattenUnits(lp), [lp]);
  const storageKey = `lu_pointer_${sectionKey || lp.subject + "_" + lp.grade + "_" + (lp.chapter_title || "")}`;

  // current pointer (which LU the teacher is on) — restore from localStorage
  const [cur, setCur] = useState(() => {
    if (typeof window === "undefined") return 0;
    const saved = Number(window.localStorage.getItem(storageKey));
    return Number.isFinite(saved) && saved >= 0 && saved < units.length ? saved : 0;
  });
  const [showAssess, setShowAssess] = useState(false);
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

  const writePointer = (i) => {
    const clamped = Math.max(0, Math.min(units.length - 1, i));
    setCur(clamped);
    try { window.localStorage.setItem(storageKey, String(clamped)); } catch {}
    return clamped;
  };

  const markComplete = () => {
    if (cur >= units.length - 1) { writePointer(units.length - 1); setUndoTo(null); return; }
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
    return (<div><button className="back" onClick={onExit}>← back</button><div className="empty">This plan has no learning units.</div></div>);
  }

  // ── Assessment artifact (3b) ──
  if (showAssess) {
    const a = view.assessment;
    return (
      <div className="assess">
        <div className="assess-hd">
          <div className="assess-hd-row">
            <span className="assess-back" onClick={() => setShowAssess(false)}>← Back to lesson</span>
            <span className="assess-tag">ASSESSMENT · TAGS ALONG</span>
          </div>
          <div className="assess-title">{a.chapter_title || lp.chapter_title}</div>
          <div className="assess-sub">Checks whether the class can transfer what this unit built. Each item names the outcome it tests. No marks, no scoring — a teaching aid.</div>
        </div>
        <div className="assess-body">
          {a.groups.map((g, gi) => g.items.map((it, ii) => (
            <div className="assess-card" key={`${gi}-${ii}`}>
              {it.implied_lo ? (
                <div className="assess-lo">
                  <span className="assess-lo-k">LEARNING OUTCOME</span>
                  <div className="assess-lo-t">{it.implied_lo}</div>
                </div>
              ) : null}
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
            </div>
          )))}
          <button className="assess-backbtn" onClick={() => setShowAssess(false)}>← Back to lesson</button>
        </div>
      </div>
    );
  }

  // ── Preview / "View full lesson plan" — ONE unit at a time, back/forward navigation ──
  // Opened from My Lesson Plans (preview prop) or the in-view "View full lesson plan" button
  // (showFullPlan). Defaults to the current pointer — i.e. the next LU after the one just marked
  // complete — so the teacher lands where she's teaching, then can page through the whole plan.
  if (preview || showFullPlan) {
    const pu = units[previewAt] || units[0];
    return (
      <div className="lessonview">
        <button className="back" onClick={showFullPlan ? () => setShowFullPlan(false) : onExit}>
          ← back{showFullPlan ? " to teaching" : " to lesson plans"}
        </button>
        <div className="lv-hd">
          <div className="lv-hd-row">
            <div>
              <div className="kicker kicker-ochre">{lp.chapter_title}</div>
              <div className="lv-title">{pu.title}</div>
            </div>
            <div className="lv-count">Learning Unit {previewAt + 1} of {units.length}</div>
          </div>
          {pu.context ? <div className="kicker lv-stage">{pu.context.toUpperCase()}</div> : null}
        </div>

        <div className="lv-pvnav">
          <button className={`lv-pvbtn ${previewAt <= 0 ? "off" : ""}`}
            onClick={() => previewAt > 0 && setPreviewAt(previewAt - 1)} disabled={previewAt <= 0}>← Previous unit</button>
          <span className="lv-pvmid">LU {previewAt + 1} / {units.length}</span>
          <button className={`lv-pvbtn ${previewAt >= units.length - 1 ? "off" : ""}`}
            onClick={() => previewAt < units.length - 1 && setPreviewAt(previewAt + 1)} disabled={previewAt >= units.length - 1}>Next unit →</button>
        </div>

        <UnitBody u={pu} totalMin={pu.meta?.duration_minutes} assessment={null} onAssess={null} />
      </div>
    );
  }

  // ── Tracking view (Screen 3) — current unit only + completion model ──
  const u = units[cur];
  const stageKicker = (u.context || "").toUpperCase();
  const total = units.length;
  const done = cur;                          // units completed before the current one

  return (
    <div className="lessonview">
      <button className="back" onClick={onExit}>← back to my plans</button>
      <div className="lv-hd">
        <div className="lv-hd-row">
          <div>
            <div className="kicker kicker-ochre">{lp.chapter_title}</div>
            <div className="lv-title">{u.title}</div>
          </div>
          <div className="lv-count">Learning Unit {cur + 1} of {total}</div>
        </div>
        {stageKicker ? <div className="kicker lv-stage">{stageKicker}</div> : null}
      </div>

      {/* Progress bar — same segmented look as the section bars in My Lesson Plans / Track. */}
      <div className="lv-progress" aria-label={`${done} of ${total} learning units complete`}>
        {Array.from({ length: total }, (_, i) => (
          <span key={i} className={`lv-seg ${i < cur ? "fill" : i === cur ? "now" : ""}`} />
        ))}
      </div>

      <UnitBody u={u} totalMin={u.meta?.duration_minutes} assessment={view.assessment} onAssess={() => setShowAssess(true)} />

      {/* Completion action (or the post-complete confirmation + Undo). */}
      {undoTo != null ? (
        <div className="lv-donecard">
          <div className="lv-donerow">
            <div className="lv-doneleft">
              <div className="lv-donemark">✓</div>
              <div>
                <div className="lv-donetitle">Unit marked complete</div>
                <div className="lv-donesub">Section is now ready for the next learning unit.</div>
              </div>
            </div>
            <button className="lv-undo" onClick={undoComplete}>↺ Undo</button>
          </div>
          {/* After marking complete, the pointer has ALREADY advanced — so units[cur] IS the next
              unit. "Open next unit" just dismisses this confirmation to reveal its teaching view. */}
          <div className="lv-nextup">
            <span className="lv-nextup-k">Next up</span>
            <div className="lv-nextup-t">{u.title}</div>
            {u.learning_outcomes?.length ? <div className="lv-nextup-d">{u.learning_outcomes.join("; ")}</div> : null}
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
        <div className="lv-lastcard">This is the final learning unit of the chapter.</div>
      ) : (
        <div className="lv-markcard">
          <div className="lv-markinfo">
            <span className="lv-markicon" aria-hidden="true">ⓘ</span>
            <span>Marking this unit complete moves the teaching position to the next learning unit for this section.</span>
          </div>
          <button className="primary lv-markbtn" onClick={markComplete}>Mark this unit complete</button>
        </div>
      )}
    </div>
  );
}
