/* ───────── section teaching-state: server-backed, localStorage-cached ─────────
 * Which chapter each section tracks (`current_chapter_*`), how far along (`lu_pointer_*`),
 * and whether it's done (`lu_done_*`) USED to live only in the browser's localStorage — so
 * two devices (e.g. Chrome desktop vs iPhone Safari) never agreed. These helpers keep the
 * SAME localStorage keys as an OPTIMISTIC CACHE (the UI stays synchronous + instant) while
 * making the server the source of truth for cross-device consistency (CLOUD_DATA_MODEL.md
 * §2.4). Writes push a snapshot; loads reconcile the cache from the server.
 *
 * The three keys per section, so the naming can never drift between reader and writer: */
import { API, withUser, getJSON } from "./format";

const chapterKey = (sk) => `current_chapter_${sk}`;
const pointerKey = (sk) => `lu_pointer_${sk}`;
const doneKey = (sk) => `lu_done_${sk}`;
// The teacher's ONE bookmark on this section's chapter — a place-marker on a phase of the
// in-progress unit (LessonView's PhaseBookmark). Stored as "unit:phase" (both 0-based).
// Rides the SAME per-section row + push/pull path as the pointer, so it migrates to Supabase
// with it at Phase 4 (CLOUD_DATA_MODEL.md §2.4) — no separate plumbing. One bookmark per
// section-chapter (founder decision 2026-07-23).
const bookmarkKey = (sk) => `lu_bookmark_${sk}`;

/* Bind a prepared chapter to a section — the single shared writer for "attach a lesson to a
 * class", used by BOTH My Classes' "+" and the My Lessons preview's "Attach to a class" CTA so
 * the two paths can never drift. Writes the optimistic localStorage cache (fresh pointer, not
 * done) then pushes to the server. Switching to a new chapter resets pointer + done so the new
 * chapter starts at its first learning unit. */
export function bindSectionChapter(sectionKey, filename) {
  if (typeof window === "undefined" || !sectionKey || !filename) return;
  try {
    window.localStorage.setItem(chapterKey(sectionKey), filename);
    window.localStorage.removeItem(pointerKey(sectionKey));
    window.localStorage.removeItem(doneKey(sectionKey));
    window.localStorage.removeItem(bookmarkKey(sectionKey));   // fresh chapter → no bookmark yet
  } catch {}
  pushSectionState(sectionKey);
}

/* Clear a section's binding (pointer + done too). The chapter itself is untouched (still in My
 * Lessons); the card returns to the unstarted "Pick a chapter" state. Shared unbind writer. */
export function unbindSection(sectionKey) {
  if (typeof window === "undefined" || !sectionKey) return;
  try {
    window.localStorage.removeItem(chapterKey(sectionKey));
    window.localStorage.removeItem(pointerKey(sectionKey));
    window.localStorage.removeItem(doneKey(sectionKey));
    window.localStorage.removeItem(bookmarkKey(sectionKey));
  } catch {}
  pushSectionState(sectionKey);   // no chapter now → the server row is deleted (untrack)
}

/* Read this section's bookmark from the localStorage cache → {unit, phase} (both 0-based),
 * or null if none set. */
export function readLocalBookmark(sectionKey) {
  if (typeof window === "undefined" || !sectionKey) return null;
  try {
    const raw = window.localStorage.getItem(bookmarkKey(sectionKey));
    if (!raw) return null;
    const [u, p] = String(raw).split(":");
    const unit = Number(u), phase = Number(p);
    if (!Number.isFinite(unit) || !Number.isFinite(phase)) return null;
    return { unit, phase };
  } catch {
    return null;
  }
}

/* Move (or clear) this section's bookmark. Writes the optimistic localStorage cache then
 * pushes the whole section snapshot to the server (same fire-and-forget path as the pointer).
 * Pass unit=null (or phase=null) to clear it. */
export function writeLocalBookmark(sectionKey, unit, phase) {
  if (typeof window === "undefined" || !sectionKey) return;
  try {
    if (unit == null || phase == null) window.localStorage.removeItem(bookmarkKey(sectionKey));
    else window.localStorage.setItem(bookmarkKey(sectionKey), `${unit}:${phase}`);
  } catch {}
  pushSectionState(sectionKey);
}

/* Read one section's current state straight from the localStorage cache. */
export function readLocalSection(sectionKey) {
  if (typeof window === "undefined") return { chapter: null, unit: null, done: false };
  try {
    return {
      chapter: window.localStorage.getItem(chapterKey(sectionKey)) || null,
      unit: window.localStorage.getItem(pointerKey(sectionKey)),
      done: window.localStorage.getItem(doneKey(sectionKey)) === "1",
    };
  } catch {
    return { chapter: null, unit: null, done: false };
  }
}

/* Sync one section to the server AFTER the caller has already written localStorage
 * (optimistic). Fire-and-forget — a failed sync never blocks or breaks the UI; the local
 * cache still reflects the teacher's action, and the next successful push reconciles.
 * No chapter bound → the section is untracked → DELETE the row. */
export function pushSectionState(sectionKey) {
  if (typeof window === "undefined" || !sectionKey) return;
  const { chapter, unit, done } = readLocalSection(sectionKey);
  const bm = readLocalBookmark(sectionKey);
  try {
    if (!chapter) {
      fetch(`${API}/section-state/${encodeURIComponent(sectionKey)}`,
        withUser({ method: "DELETE" })).catch(() => {});
      return;
    }
    fetch(`${API}/section-state`, withUser({
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        section_key: sectionKey,
        chapter,
        unit_index: unit === null || unit === "" ? null : Number(unit),
        done: !!done,
        // The bookmark rides the same snapshot (null when unset). An older API that doesn't
        // know these fields simply ignores them (Pydantic drops extras) — the cache still holds
        // the bookmark; cross-device sync of it lights up once the field lands server-side.
        bookmark_unit: bm ? bm.unit : null,
        bookmark_phase: bm ? bm.phase : null,
      }),
    })).catch(() => {});
  } catch {}
}

/* Authoritative reconcile on load: pull every tracked section from the server and rewrite
 * the localStorage cache to match. For each KNOWN section key (from the readiness profile),
 * apply the server row, or clear the local cache if the server has none — so a device that
 * missed a track (or an untrack) done elsewhere converges to server truth. Returns a promise;
 * callers bump a render tick once it resolves so the cards re-read the refreshed cache. */
export async function pullSectionState(sectionKeys) {
  if (typeof window === "undefined") return;
  let states = {};
  try {
    states = (await getJSON("/section-state")).states || {};
  } catch {
    return; // offline / server down → keep the existing local cache untouched
  }
  // SAFETY GUARD (2026-07-03): a WHOLESALE-empty server response ({} for every section) is far
  // more likely a transient/corrupt-empty read than the teacher having genuinely untracked every
  // single class — and the old code responded by DELETING every local binding, which is exactly
  // how a corrupted state.json flashed all the cards back to "pick a chapter". So when the server
  // returns nothing at all, we ADOPT nothing and DELETE nothing: local optimistic state is kept
  // intact. Per-section untrack from another device still propagates, because that case returns a
  // NON-empty payload (the other tracked sections are present) and the absent key is cleared below.
  const serverEmpty = Object.keys(states).length === 0;
  (sectionKeys || []).forEach((sk) => {
    const st = states[sk];
    try {
      if (st && st.chapter) {
        window.localStorage.setItem(chapterKey(sk), st.chapter);
        if (st.unit_index === null || st.unit_index === undefined) {
          window.localStorage.removeItem(pointerKey(sk));
        } else {
          window.localStorage.setItem(pointerKey(sk), String(st.unit_index));
        }
        if (st.done) window.localStorage.setItem(doneKey(sk), "1");
        else window.localStorage.removeItem(doneKey(sk));
        // Bookmark rides the same row — but ADOPT it only when the server actually carries one.
        // When the server row has NO bookmark (an API that doesn't persist the fields yet, or a
        // row written before this feature), we must NOT wipe the local optimistic value: doing
        // so erased the teacher's saved phase on every sign-in, so it snapped back to the top of
        // the unit. Same spirit as the serverEmpty guard above — keep local truth until the
        // server has something real to override it with. A bound chapter always carries a
        // bookmark locally; the only legitimate clear is unbind/bind, which deletes the whole
        // row (the untrack branch below).
        if (st.bookmark_unit != null && st.bookmark_phase != null) {
          window.localStorage.setItem(bookmarkKey(sk), `${st.bookmark_unit}:${st.bookmark_phase}`);
        }
      } else if (!serverEmpty) {
        // Server has state for OTHER sections but not this one → a genuine untrack; clear local.
        // (Skipped entirely when serverEmpty — see the guard above.)
        window.localStorage.removeItem(chapterKey(sk));
        window.localStorage.removeItem(pointerKey(sk));
        window.localStorage.removeItem(doneKey(sk));
        window.localStorage.removeItem(bookmarkKey(sk));
      }
    } catch {}
  });
}
