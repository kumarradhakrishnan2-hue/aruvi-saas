/* ───────── shared formatting helpers ───────── */
/* Derive the API host from whatever host the browser loaded the page from, so this works
 * unmodified on localhost, on the Mac's LAN IP (mobile testing over WiFi), and later on a
 * real domain — no hand-editing an IP address per session. */
export const API =
  typeof window !== "undefined"
    ? `http://${window.location.hostname}:8000`
    : "http://localhost:8000";
export const ROMAN = ["iii", "iv", "v", "vi", "vii", "viii", "ix", "x"];

export const pretty = (s) => (s || "").split("_").map((w) => w.charAt(0).toUpperCase() + w.slice(1)).join(" ");
export const gradeUp = (g) => (g || "").replace(/grade/i, "").trim().toUpperCase();
export const kickerOf = (t) => (t || "").replace(/_/g, " ").toUpperCase();
export const pad = (n) => String(n ?? "").padStart(2, "0");

/* ───────── current user (pre-auth tenanting) ─────────
 * No password stage yet: the login portal stores the entered user ID here, and every API
 * call carries it as the X-Aruvi-User header. The API treats each user ID as its own
 * tenant (tenant_id == user_id). Phase 4 swaps this for a real auth token; the header seam
 * and the per-call injection below stay the same. localStorage so the login survives a
 * refresh — re-entering the ID each session would defeat the persistence we just added. */
const USER_KEY = "aruvi_user";
export function getUser() {
  if (typeof window === "undefined") return "";
  try { return window.localStorage.getItem(USER_KEY) || ""; } catch { return ""; }
}
export function setUser(id) {
  if (typeof window === "undefined") return;
  try { window.localStorage.setItem(USER_KEY, (id || "").trim()); } catch {}
}
export function clearUser() {
  if (typeof window === "undefined") return;
  try { window.localStorage.removeItem(USER_KEY); } catch {}
}

/* Merge the X-Aruvi-User header into any fetch options, preserving caller-set headers. */
export function withUser(opts = {}) {
  const user = getUser();
  const headers = { ...(opts.headers || {}) };
  if (user) headers["X-Aruvi-User"] = user;
  return { ...opts, headers };
}

export async function getJSON(path, opts) {
  const r = await fetch(API + path, withUser(opts));
  if (!r.ok) throw new Error(`${r.status}`);
  return r.json();
}

/* ───────── subject·grade coverage (single source of truth) ─────────
 * Which grades Aruvi actually has chapter content for, per subject (Science → VI–IX, TWAU →
 * III–V, …). The authority is the backend (GET /subjects/{slug}/grades, derived from the chapter
 * dirs). BOTH the setup flow (Readiness) and the editor (MyClasses) must restrict grade choices
 * to this — defined ONCE here so the rule can't drift between the two screens. */
export const ALL_GRADES = ["III", "IV", "V", "VI", "VII", "VIII", "IX", "X"];
export const subjectSlug = (name) => (name || "").toLowerCase().replace(/ /g, "_");

// Module-level cache so we fetch each subject's supported grades at most once per session.
const _supportedGradesCache = {};   // { slug: ["VI","VII",…] (uppercase Roman) }
export async function fetchSupportedGrades(subjectName) {
  const slug = subjectSlug(subjectName);
  if (!slug) return [];
  if (_supportedGradesCache[slug]) return _supportedGradesCache[slug];
  try {
    const d = await getJSON(`/subjects/${slug}/grades`);
    const ups = (d.grades || []).map((g) => String(g).toUpperCase());
    _supportedGradesCache[slug] = ups;
    return ups;
  } catch {
    return [];
  }
}

/* Regenerate the denormalized "active subject" projection from a persisted readiness
 * profile. The API stores ONLY the canonical subjects[] (CLOUD_DATA_MODEL.md §2.1); the
 * current consumers (MyPlans.classesFromReadiness, Allocate.weeklyRatioFromReadiness)
 * still read the projection keys (grades/durations/grids/budget). This mirrors the tail
 * of Readiness.jsx buildPayload() so a rehydrated profile is byte-for-byte what those
 * consumers expect — keeping the projection derived-on-read, never persisted.
 * `profile` is {subjects:[...]}; `activeIdx` selects which subject to project (default 0). */
export function projectReadiness(profile, activeIdx = 0) {
  const subjects = (profile && profile.subjects) || [];
  if (!subjects.length) return null;
  const i = Math.min(Math.max(activeIdx, 0), subjects.length - 1);
  const active = subjects[i];
  return {
    subjects,
    activeSubjectIndex: i,
    // derived active-subject projection (NOT source of truth):
    subject: active.name,
    grades: active.grades,
    durations: active.grades.map((gr) => gr.durations), // per-grade durations
    grids: active.grids,
    budget: active.budget,
  };
}
