/* ───────── section chapter-history: server-backed, localStorage-cached ─────────
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
 * ★ PERSISTENCE — SERVER-BACKED SINCE 2026-09-07, and the LAST teaching state to become so.
 * It was localStorage-only, and this header used to say the mirror was owed "when Phase 4 lands".
 * The mobile-migration assessment (docs/mobile_migration_assessment.md §4) made the cost concrete:
 * every other piece of teaching state already reconciles from the server, so a teacher on a phone
 * AND a laptop would have agreed about everything except what her classes have actually been
 * taught — the exact two-device disagreement sectionState.js was built to end, surviving in the
 * one store nobody had migrated. So: same shape as sectionState.js — localStorage stays the
 * SYNCHRONOUS optimistic cache (readHistory/hasHistory are called during render and must never
 * become promises), writes push, and a pull reconciles on load.
 *
 * ★ BUT IT MERGES, WHERE sectionState.js SNAPSHOTS — the one deliberate difference, mirrored on
 * the server. Section state is CURRENT state, so the last writer rightly holds the truth. History
 * is CUMULATIVE: a whole-map push from a phone that has never seen the laptop's rows would delete
 * them. Every write sends only the entries it is adding, the server upserts each under its own
 * chapter file with latest-`ts`-wins, and the pull UNIONS rather than replaces. Convergence from
 * any device, in any order, with no loss — and no need for the wholesale-empty guard sectionState
 * carries, because a merge that adopts nothing simply changes nothing.
 *
 * Deliberately NOT cleared by clearBinding — untracking a chapter must not erase the record that
 * it was once taught. (Removing the SECTION itself is a different act, and the server drops the
 * ledger there; see the port's `delete_section`.) */
import { API, withUser, getJSON, getUser } from "./format";

const historyKey = (sk) => `section_history_${sk}`;
/* ★ WHOSE ledger this browser is holding. Load-bearing, not bookkeeping — see claimCache. */
const OWNER_KEY = "section_history_owner";

/* The localStorage cache as its raw {file: entry} MAP (the stored shape). Internal — callers
 * outside this module get the array form from readHistory. */
function readMap(sectionKey) {
  if (typeof window === "undefined" || !sectionKey) return {};
  try {
    const raw = window.localStorage.getItem(historyKey(sectionKey));
    if (!raw) return {};
    const obj = JSON.parse(raw);
    return obj && typeof obj === "object" ? obj : {};
  } catch {
    return {};
  }
}

function writeMap(sectionKey, map) {
  try {
    window.localStorage.setItem(historyKey(sectionKey), JSON.stringify(map));
  } catch { /* private mode / storage full — the server copy is still authoritative */ }
}

/* An entry's ts as a comparable number; 0 when absent or unparseable. Must mirror the
 * adapter's `_ts_of` — a row that loses the comparison here must lose it there too, or the
 * two sides disagree about which write is newer. */
function tsOf(entry) {
  const n = Number((entry && entry.ts) || 0);
  return Number.isFinite(n) ? n : 0;
}

/* All logged entries for a section, as an array (unsorted — caller sorts).
 * SYNCHRONOUS, from the cache: this is called during render (the history popup, and the glyph
 * on every card), so it can never become a promise. */
export function readHistory(sectionKey) {
  return Object.values(readMap(sectionKey));
}

/* Upsert one chapter's history entry (keyed by file → latest action wins). The caller has already
 * applied the qualifying gate; entry needs at least { file, status }. Writes the optimistic cache
 * then pushes the single entry to the server (fire-and-forget: a failed push never blocks the UI,
 * and the next successful one carries the row up, because the push is a MERGE and so replaying it
 * costs nothing). */
export function recordHistory(sectionKey, entry) {
  if (typeof window === "undefined" || !sectionKey || !entry || !entry.file || !entry.status) return;
  const row = {
    file: entry.file,
    chapter_number: entry.chapter_number ?? null,
    chapter_title: entry.chapter_title ?? "",
    status: entry.status,
    units_done: entry.units_done ?? null,
    total_units: entry.total_units ?? null,
    ts: entry.ts || Date.now(),
  };
  const map = readMap(sectionKey);
  map[row.file] = row;
  writeMap(sectionKey, map);
  pushHistory(sectionKey, [row]);
}

/* Does this section have any PAST chapters logged? Drives whether the card shows the history glyph
 * (the current, still-bound chapter is not "history" — only left-the-slot chapters are). */
export function hasHistory(sectionKey) {
  return readHistory(sectionKey).length > 0;
}

/* ── server sync ──────────────────────────────────────────────────────────────────────────── */

/* Push entries for ONE section. Fire-and-forget, and safe to repeat: the server merges by file
 * with latest-ts-wins, so a duplicate push is a no-op rather than a churn. No read-back
 * verification (unlike sectionState's verifiedWrite) because there is nothing here a teacher can
 * be misled about mid-action — the ledger is written as a side effect of an act she has already
 * seen confirmed (the card changing state), and a row that arrives on the next reconcile instead
 * of this one costs her nothing. */
function pushHistory(sectionKey, entries) {
  if (typeof window === "undefined" || !sectionKey || !entries || !entries.length) return Promise.resolve();
  try {
    return fetch(`${API}/section-history`, withUser({
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ section_key: sectionKey, entries }),
    })).then(() => {}).catch(() => {});
  } catch {
    return Promise.resolve();
  }
}

/* ★ THE GUARD THE PUSH-BACK MADE NECESSARY — claim this browser's cache for the signed-in
 * teacher, wiping it first if it belongs to someone else. Returns nothing; call before merging.
 *
 * Why it exists: sign-out does not clear the section caches today (the privacy notice's own
 * "sign-out residue" FIX item), so a shared staff-room browser can hold teacher A's rows when
 * teacher B signs in. For sectionState that is merely stale — its pull OVERWRITES local from the
 * server and only pushes on an explicit act of hers. This module's pull PUSHES OWED ROWS UP, so
 * without this guard A's leftover rows for any section key B also teaches would be merged into
 * B's server ledger: not a stale read but a cross-account WRITE, and a DPDP one at that.
 *
 * An ABSENT stamp is treated as the current teacher's, deliberately: that is the pre-migration
 * browser, whose accumulated ledger is exactly what the push-back exists to carry up, and before
 * this feature a cache could only ever have come from the one teacher using that browser. Every
 * cache written from here on carries a stamp, so the unstamped case expires by itself. */
function claimCache(userId) {
  if (typeof window === "undefined") return;
  try {
    const owner = window.localStorage.getItem(OWNER_KEY);
    if (owner && userId && owner !== userId) clearLocalHistoryCache();
    if (userId) window.localStorage.setItem(OWNER_KEY, userId);
  } catch { /* private mode — nothing cached, nothing to mis-attribute */ }
}

/* Authoritative reconcile on load: pull the whole ledger and UNION it into the localStorage
 * cache, then push up anything this device holds that the server does not.
 *
 * ★ UNION, NOT REPLACE — and that is what makes the wholesale-empty guard sectionState needs
 * unnecessary here. There, a transient empty read once wiped every local binding, so an empty
 * payload has to be distrusted. Here an empty payload adopts nothing and deletes nothing by
 * construction: the only way a row leaves this cache is the section leaving the profile.
 *
 * The push-back half is what carries an EXISTING teacher across: her ledger has been accumulating
 * in one browser since 2026-07-04 and the server has never seen a row of it. Without it, the day
 * this ships her trail would look empty on her second device and she would conclude the feature
 * lost it. It runs once per section per load and is a merge, so it is idempotent.
 *
 * Resolves TRUE when the server answered, FALSE when it could not (offline / server down — the
 * cache is untouched and is NOT trustworthy as "she has taught nothing"), matching
 * pullSectionState's contract so callers can treat the two the same way. */
export async function pullSectionHistory(sectionKeys) {
  if (typeof window === "undefined") return false;
  // Claim the cache BEFORE the fetch resolves — a cache belonging to another teacher must not
  // survive to be merged, and must certainly not be pushed up under this account.
  claimCache(getUser());
  let history = {};
  try {
    history = (await getJSON("/section-history")).history || {};
  } catch {
    return false; // offline / server down → keep the existing local cache untouched
  }
  (sectionKeys || []).forEach((sk) => {
    try {
      const local = readMap(sk);
      const remote = history[sk] || {};
      const merged = { ...local };
      let localChanged = false;
      Object.keys(remote).forEach((f) => {
        const r = remote[f];
        if (!r || !r.file) return;
        // Latest wins, both directions — a tie keeps the local row, so a reconcile that
        // learns nothing new also writes nothing.
        if (!merged[f] || tsOf(r) > tsOf(merged[f])) { merged[f] = r; localChanged = true; }
      });
      if (localChanged) writeMap(sk, merged);
      // Anything the server is missing or holds an older copy of goes back up, in ONE request
      // per section. Includes this device's pre-migration rows.
      const owed = Object.keys(merged)
        .filter((f) => !remote[f] || tsOf(merged[f]) > tsOf(remote[f]))
        .map((f) => merged[f]);
      if (owed.length) pushHistory(sk, owed);
    } catch { /* one bad section must not cost the reconcile of the others */ }
  });
  return true;
}

/* Drop this device's cached ledger. The cutover twin of clearLocalSectionCache: the server has
 * already cleared the year's ledger, and without this the browser would keep showing last
 * cohort's trail until something happened to overwrite it. Nothing on the server is touched. */
export function clearLocalHistoryCache() {
  if (typeof window === "undefined") return 0;
  let removed = 0;
  try {
    const doomed = [];
    for (let i = 0; i < window.localStorage.length; i += 1) {
      const k = window.localStorage.key(i);
      if (k && k.startsWith("section_history_")) doomed.push(k);
    }
    doomed.forEach((k) => { window.localStorage.removeItem(k); removed += 1; });
    // The owner stamp shares the prefix and goes with them, so the next claim starts clean
    // rather than reading a stamp with no rows behind it.
    window.localStorage.removeItem(OWNER_KEY);
  } catch { /* private mode / storage disabled — the server is the authority regardless */ }
  return removed;
}
