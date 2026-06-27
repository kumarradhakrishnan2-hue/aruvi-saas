"use client";
import { useMemo, useState } from "react";

/* ───────── Lesson view (Screen 3) + assessment artifact (Screen 3b) ─────────
 * Renders a saved plan as Learning Units on a continuous rail. The plan's periods
 * (lesson_plan.groups[].periods[]) ARE the Learning Units; each period's activities are
 * its phases (no fabricated per-phase minutes — Phase 5 decision). The "pointer" (which LU
 * the teacher is on) lives in state and persists per section in localStorage; the pointer
 * moves only when she taps Move. Assessment "tags along" as a dedicated green sub-view. */

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

export default function LessonView({ view, sectionKey = "", onExit }) {
  const lp = view.lesson_plan;
  const units = useMemo(() => flattenUnits(lp), [lp]);
  const storageKey = `lu_pointer_${sectionKey || lp.subject + "_" + lp.grade + "_" + (lp.chapter_title || "")}`;

  // current pointer (which LU the teacher is on) — restore from localStorage
  const [cur, setCur] = useState(() => {
    if (typeof window === "undefined") return 0;
    const saved = Number(window.localStorage.getItem(storageKey));
    return Number.isFinite(saved) && saved >= 0 && saved < units.length ? saved : 0;
  });
  const [peek, setPeek] = useState(cur);      // previewed LU (doesn't move the pointer)
  const [showAssess, setShowAssess] = useState(false);

  const moveTo = (i) => {
    const clamped = Math.max(0, Math.min(units.length - 1, i));
    setCur(clamped); setPeek(clamped);
    try { window.localStorage.setItem(storageKey, String(clamped)); } catch {}
  };

  if (!units.length) {
    return (<div><button className="back" onClick={onExit}>← back</button><div className="empty">This plan has no learning units.</div></div>);
  }

  const u = units[peek];
  const stageKicker = (u.context || "").toUpperCase();

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

  // ── Lesson view (3) ──
  const railNodes = [peek - 1, peek, peek + 1].filter((i) => i >= 0 && i < units.length);
  const totalMin = u.meta?.duration_minutes;
  return (
    <div className="lessonview">
      <button className="back" onClick={onExit}>← back to my plans</button>
      <div className="lv-hd">
        <div className="lv-hd-row">
          <div>
            <div className="kicker kicker-ochre">{lp.chapter_title}</div>
            <div className="lv-title">{u.title}</div>
          </div>
          <div className="lv-count">Learning Unit {peek + 1} of {units.length}</div>
        </div>
        {stageKicker ? <div className="kicker lv-stage">{stageKicker}</div> : null}
      </div>

      <div className="peek">
        <span className={`peeknav ${peek <= 0 ? "off" : ""}`} onClick={() => peek > 0 && setPeek(peek - 1)}>← LU {peek}</span>
        <span className="peekmid">Preview · doesn&rsquo;t move your place</span>
        <span className={`peeknav ${peek >= units.length - 1 ? "off" : ""}`} onClick={() => peek < units.length - 1 && setPeek(peek + 1)}>LU {peek + 2} →</span>
      </div>

      <div className="lurail">
        {railNodes.map((i) => {
          const state = i < cur ? "done" : i === cur ? "now" : "future";
          return (
            <div className={`lunode ${state === "future" ? "future" : ""}`} key={i}>
              <span className="dot">{i + 1}</span>
              <span className="lulabel">Learning Unit {i + 1} · {state}</span>
              <div className="lutitle" style={i === peek ? { fontWeight: 600 } : undefined}>{units[i].title}</div>
            </div>
          );
        })}
      </div>

      <div className="lv-phasehd">
        <span className="kicker kicker-soft">PHASES{totalMin ? ` · ${totalMin} MIN TOTAL` : ""}</span>
        {view.assessment ? <span className="lv-assesslink" onClick={() => setShowAssess(true)}>assessment here →</span> : null}
      </div>

      {(u.activities && u.activities.length) ? u.activities.map((act, i) => (
        <div className="phaserow" key={i}><span className="phasetext">{act}</span></div>
      )) : <div className="empty">No phases recorded for this unit.</div>}

      {u.learning_outcomes?.length ? (
        <div className="lv-lo"><span className="lv-lo-k">Learning outcome</span> {u.learning_outcomes.join("; ")}</div>
      ) : null}
      {u.teacher_notes?.length ? <div className="lv-tnote">{u.teacher_notes.join(" ")}</div> : null}
      {u.homework ? <div className="lv-lo"><span className="lv-lo-k">Homework</span> {u.homework}</div> : null}

      <div className="lv-controls">
        <button className="primary" disabled={cur >= units.length - 1} onClick={() => moveTo(cur + 1)}>
          {cur >= units.length - 1 ? "Last learning unit" : `Move to Learning Unit ${cur + 2} →`}
        </button>
        <button className="ghost" onClick={() => setPeek(cur)}>Stay on Learning Unit {cur + 1}</button>
      </div>

      <div className="lv-stop">
        <button className="clear-btn lv-stopbtn" onClick={onExit}>Stop tracking this chapter</button>
        <div className="lv-stop-note">Removes it from your schedule. The plan stays safe — same as finishing, no trail kept.</div>
      </div>
    </div>
  );
}
