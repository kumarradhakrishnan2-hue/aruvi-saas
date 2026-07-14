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
// Teacher-facing label: teachers say "Class 7", not "Grade VII". Roman grade slug → Arabic class
// number (ROMAN[0] "iii" → 3). Falls back to the upper-cased input for anything unrecognised.
export const classNum = (g) => {
  const idx = ROMAN.indexOf((g || "").toLowerCase());
  return idx >= 0 ? idx + 3 : (g || "").toUpperCase();
};
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

/* Build a per-user localStorage key so one teacher's client state never bleeds into another's
 * on a shared browser (A3, 2026-07-06). Mirrors the plus_portal_{user}/expand_*_{user} scheme
 * already used in MyPlans. Pre-login (no user yet) it falls back to a bare "_" suffix, so the
 * key is still stable and non-leaking. Use for any per-user client cache/preference key. */
export function userKey(base) {
  return `${base}_${getUser() || ""}`;
}

/* Render a string with `**…**` markdown-bold spans as React nodes. Used for homework lines,
 * where the maths normalizer wraps the textbook locator (e.g. "Figure it Out Q11, section 5.2
 * p.115") in `**…**` so the reference alone reads bold. Plain strings (no markers) return as-is.
 * Returns an array of strings / <strong> elements suitable for direct use as React children. */
export function boldMarks(text) {
  const s = String(text ?? "");
  if (!s.includes("**")) return s;
  const out = [];
  const re = /\*\*([^*]+)\*\*/g;
  let last = 0, m, i = 0;
  while ((m = re.exec(s)) !== null) {
    if (m.index > last) out.push(s.slice(last, m.index));
    out.push(<strong key={i++}>{m[1]}</strong>);
    last = re.lastIndex;
  }
  if (last < s.length) out.push(s.slice(last));
  return out;
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

/* Record a saved plan as PREPARED by this teacher (POST /plans-prepared). Called when she
 * actually generates/attaches a lesson — first-run activation and the everyday PrepareLesson
 * flow — so My Lessons lists only her own work, not the whole shared sample library. Fire-and-
 * forget: the UI never blocks on it, and the flag simply stays false if the write is lost.
 * subject/grade are SLUGS; filename is the saved-plan file. */
export function markPrepared(subject, grade, filename, periods) {
  if (!subject || !grade || !filename) return Promise.resolve();
  // `periods` (optional) is the teacher's chosen period count for this chapter — stored server-
  // side so budget tracking reflects what she allocated, not the served plan's authored length.
  // Returns the (error-swallowed) promise so callers that need the write to land before they
  // refetch /plans — e.g. PrepareLesson's auto-attach return — can await it. Fire-and-forget
  // callers can still ignore the return value.
  const body = { subject, grade, filename };
  if (periods != null) body.periods = periods;
  return fetch(`${API}/plans-prepared`, withUser({
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })).catch(() => {});
}

/* Annual budget in PERIODS for a subject·grade, read from the CANONICAL readiness.subjects[]
 * (not the active-subject projection). Mirrors Readiness.computeBudget / Allocate's copy so the
 * Prepare screen's budget meter and Allocate agree. budget is { gradeIdx: {method, value} }:
 *   periods → value directly; weeks → weeklyPeriods×value; days → weeklyPeriods×(days/6);
 *   estimate/auto/none → weeklyPeriods×30. weeklyPeriods = grid cells for that grade ÷ #sections,
 *   falling back to the grade's periods_per_week (post calendar-purge profiles). null when the
 *   subject·grade isn't in the profile or no basis can be derived. */
export function annualBudgetPeriods(readiness, subjectSlugArg, gradeSlugArg) {
  const subs = (readiness && readiness.subjects) || [];
  const slugify = (n) => (n || "").toLowerCase().replace(/ /g, "_");
  const sub = subs.find((s) => slugify(s.name) === subjectSlugArg);
  if (!sub) return null;
  const gi = (sub.grades || []).findIndex((g) => (g.grade || "").toLowerCase() === gradeSlugArg);
  if (gi < 0) return null;
  const b = (sub.budget || {})[String(gi)];
  // weekly periods for this grade: marked grid cells ÷ section count, else periods_per_week.
  const gridG = (sub.grids || [])[gi] || [];
  const secCount = gridG.length || 1;
  let cells = 0;
  gridG.forEach((row) => (row || []).forEach((v) => { if (v != null && v >= 0) cells++; }));
  let weeklyPeriods = Math.round(cells / secCount);
  if (!weeklyPeriods) weeklyPeriods = Number((sub.grades[gi] || {}).periods_per_week) || 0;
  if (!b) return weeklyPeriods ? weeklyPeriods * 30 : null;      // no budget set → estimate
  if (b.method === "periods") return b.value;
  if (b.method === "weeks") return weeklyPeriods * b.value;
  if (b.method === "days") return Math.round(weeklyPeriods * (b.value / 6));
  return weeklyPeriods ? weeklyPeriods * 30 : null;             // estimate / auto / unknown
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
