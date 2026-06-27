"use client";
import Allocate from "./Allocate";

/* ───────── Generate tab (Phase 1) ─────────
 * The single Generate tab — Allocate is folded in here (no longer a sibling tab).
 * Readiness gates it: when `ready` is false the tab is visible but inert (the G1
 * locked state), pointing the teacher back to My Plans to finish setup. When ready,
 * it hosts the allocation flow. Phase 3 expands this into the full G2 hub + spokes. */
export default function GenerateTab({ subject, grade, ready, readiness, onNavigate }) {
  if (!ready) {
    return (
      <div className="gate">
        <div className="gate-lock">🔒</div>
        <p className="h2 gate-title">Generate unlocks after setup</p>
        <p className="gate-sub">
          Aruvi needs your weekly grid and annual budget first — that&rsquo;s how the plans it
          makes can fit your real classes and your real year.
        </p>
        <button className="primary" onClick={() => onNavigate && onNavigate("myplans")}>
          Finish setup in My Plans →
        </button>
      </div>
    );
  }
  return <Allocate subject={subject} grade={grade} readiness={readiness} onNavigate={onNavigate} />;
}
