/* ───────── runtime configuration (Track D step 1, 2026-09-11) ─────────
 *
 * The web derived the API host from `window.location` and read the Supabase token through
 * a module-level import of lib/auth.js. Neither works on a phone, and neither belongs in
 * shared code — so both are INJECTED once at boot:
 *
 *   configure({ apiBase, accessToken })
 *     apiBase      "https://meyy-api.onrender.com" (no trailing slash; one is stripped)
 *     accessToken  () => string — SYNCHRONOUS, "" when signed out. withUser() calls it on
 *                  every fetch; the web passes lib/auth.js's accessToken, the phone passes
 *                  its own mirror of the supabase-js session.
 *
 * `API` is a live ESM binding: importers that read `API + path` see the configured value
 * even if they imported before configure() ran — as long as they read it at call time, which
 * every helper here does. Reading it at module top level would freeze the default. */

export let API = "http://localhost:8000";
let tokenProvider = () => "";

export function configure({ apiBase, accessToken } = {}) {
  if (apiBase != null) API = String(apiBase).replace(/\/+$/, "") || API;
  if (typeof accessToken === "function") tokenProvider = accessToken;
}

/* The current bearer token or "" — whatever the app installed. Never throws. */
export function getAccessToken() {
  try { return tokenProvider() || ""; } catch { return ""; }
}
