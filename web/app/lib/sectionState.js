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
      } else if (!serverEmpty) {
        // Server has state for OTHER sections but not this one → a genuine untrack; clear local.
        // (Skipped entirely when serverEmpty — see the guard above.)
        window.localStorage.removeItem(chapterKey(sk));
        window.localStorage.removeItem(pointerKey(sk));
        window.localStorage.removeItem(doneKey(sk));
      }
    } catch {}
  });
}
