/* ───────── shared formatting helpers ───────── */
export const API = "http://localhost:8000";
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
