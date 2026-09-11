/* ───────── sign-out: clear EVERY per-teacher cache on this device (2026-09-11) ─────────
 *
 * The live product check on the production stack (MEMORY.md 2026-09-11) found the web's
 * sign-out leaving `current_chapter_*`, `lu_*` and `chapter_notes_*` behind — each store had
 * its own clear function and page.jsx called some of them. A phone is more often shared than
 * a laptop (a staffroom device, a family phone), and the identity is the mobile number, so a
 * leftover cache is another teacher's record on the next sign-in. One function, called by
 * both apps' sign-out, that names every prefix this package (and the screens) write:
 *
 *   aruvi_user               the signed-in id (format.js)
 *   current_chapter_ lu_*    section state incl. bookmarks (sectionState.js)
 *   section_history_ + owner section chapter ledger (sectionHistory.js)
 *   chapter_notes_           the notes editor's optimistic cache (LessonView / web page.jsx)
 *   aruvi_ask_bank(_etag)    the Ask Meyy bank (ask-aruvi/bank.js)
 *   sb-…-auth-token          supabase-js's own session, when the app gave it the same storage
 *
 * `extraPrefixes` lets an app add keys only it writes (the web's per-user `userKey()` caches
 * such as the profile-portal queue). Returns the number of keys removed. Never throws. */
import { removeByPrefix, storage } from "./storage.js";
import { clearLocalSectionCache } from "./sectionState.js";
import { clearLocalHistoryCache } from "./sectionHistory.js";
import { clearBank } from "./ask-aruvi/bank.js";
import { clearUser } from "./format.js";

export const TEACHER_CACHE_PREFIXES = [
  "current_chapter_", "lu_pointer_", "lu_done_", "lu_bookmark_",
  "section_history_",            // includes the owner stamp, section_history_owner
  "chapter_notes_",
  "aruvi_ask_bank",
];

export function clearTeacherCaches(extraPrefixes = []) {
  let n = 0;
  n += clearLocalSectionCache();
  n += clearLocalHistoryCache();
  clearBank();
  clearUser();
  // belt and braces: anything the named clears missed, plus the app's own per-user keys
  n += removeByPrefix([...TEACHER_CACHE_PREFIXES, ...extraPrefixes]);
  try { storage.removeItem("aruvi_user"); } catch {}
  return n;
}
