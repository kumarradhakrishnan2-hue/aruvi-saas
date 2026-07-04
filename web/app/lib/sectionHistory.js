/* ───────── section chapter-history: per-section teaching ledger (localStorage) ─────────
 * My Classes' section-state (sectionState.js) only ever holds the CURRENT chapter binding +
 * pointer + done flag; the moment a chapter leaves the current slot (untrack, or move-on from a
 * completed chapter) that record is deleted. So the trail of what a section has actually taught
 * lived nowhere. This log is that trail — the natural completion of the "where did I stop?"
 * model (MEMORY.md 2026-07-04).
 *
 * SHAPE — a per-section MAP keyed by chapter FILE, so there is exactly ONE row per chapter and the
 * latest action wins automatically (a new event for a chapter overwrites the old one). Each value:
 *   { file, chapter_number, chapter_title, status, units_done, total_units, ts }
 * status ∈ { "completed" | "untracked" }.  ("ongoing" is never STORED — it's live state the popup
 * overlays from the current binding; only chapters that have LEFT the current slot are logged.)
 * units_done / total_units stamp the progress reached, so the row can say "LU 2 of 10 completed".
 *
 * WHAT QUALIFIES (the anti-noise gate, teacher's rule 2026-07-04): a chapter enters history only
 * when it earned its place — at least one learning unit was marked complete before it left.
 * Completed chapters always qualify (all units done); a set-aside chapter qualifies only if the
 * pointer had advanced ≥1. Casual attach→untrack with no progress logs NOTHING. The gate lives in
 * the CALLER (MyPlans) where the pointer is known; this module just stores what it's handed.
 *
 * PERSISTENCE — localStorage only for now, matching the lesson pointer's current status
 * (CLAUDE.md §9: pointer + ready flag are the remaining localStorage-only state to migrate). When
 * Phase 4 lands, this gains a server mirror exactly like sectionState.js (push snapshot / pull
 * reconcile) so history follows the teacher across devices. Deliberately NOT cleared by
 * clearBinding — untracking a chapter must not erase the record that it was once taught. */

const historyKey = (sk) => `section_history_${sk}`;

/* All logged entries for a section, as an array (unsorted — caller sorts). */
export function readHistory(sectionKey) {
  if (typeof window === "undefined" || !sectionKey) return [];
  try {
    const raw = window.localStorage.getItem(historyKey(sectionKey));
    if (!raw) return [];
    const obj = JSON.parse(raw);
    return obj && typeof obj === "object" ? Object.values(obj) : [];
  } catch {
    return [];
  }
}

/* Upsert one chapter's history entry (keyed by file → latest action wins). The caller has already
 * applied the qualifying gate; entry needs at least { file, status }. */
export function recordHistory(sectionKey, entry) {
  if (typeof window === "undefined" || !sectionKey || !entry || !entry.file || !entry.status) return;
  try {
    const raw = window.localStorage.getItem(historyKey(sectionKey));
    const obj = raw ? (JSON.parse(raw) || {}) : {};
    obj[entry.file] = {
      file: entry.file,
      chapter_number: entry.chapter_number ?? null,
      chapter_title: entry.chapter_title ?? "",
      status: entry.status,
      units_done: entry.units_done ?? null,
      total_units: entry.total_units ?? null,
      ts: entry.ts || Date.now(),
    };
    window.localStorage.setItem(historyKey(sectionKey), JSON.stringify(obj));
  } catch {}
}

/* Does this section have any PAST chapters logged? Drives whether the card shows the history glyph
 * (the current, still-bound chapter is not "history" — only left-the-slot chapters are). */
export function hasHistory(sectionKey) {
  return readHistory(sectionKey).length > 0;
}
