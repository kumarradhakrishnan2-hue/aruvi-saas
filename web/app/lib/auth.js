/* ───────── Supabase Auth on the web (Track B, 2026-09-09) ─────────
 *
 * The API accepts two credentials, never both (api/config.AUTH_PROVIDER): the X-Aruvi-User
 * dev header, or a Supabase access token as `Authorization: Bearer`. This module owns the
 * web's side of the second one and is deliberately small:
 *   · `authEnabled()` — true when NEXT_PUBLIC_SUPABASE_URL/ANON_KEY are set. Without them
 *     the front door keeps its honest 0000 stub and withUser() sends the header, so a
 *     local `npm run dev` against a header-mode API is unchanged.
 *   · `sendOtp` / `verifyOtp` — Supabase issues, delivers (via the SMS provider) and
 *     checks the code. The web never sees the code's truth, only the verdict.
 *   · `accessToken()` — SYNCHRONOUS, because withUser() is (every fetch helper builds its
 *     headers inline). supabase-js keeps the session in localStorage and refreshes it in the
 *     background; we mirror the current token into a module variable from
 *     onAuthStateChange, and fall back to reading supabase-js's own storage key so the very
 *     first call after a reload is not empty.
 *   · `signOutAuth()` — ends the Supabase session; page.jsx calls it beside clearUser().
 *
 * The IDENTITY the app runs under is still the 10-digit mobile: the API derives it from the
 * token's verified phone claim and hands it back from /onboarding/verified, and the front
 * door uses THAT (not the number she typed) for setUser — one source, server-side. */
import { createClient } from "@supabase/supabase-js";

const URL = process.env.NEXT_PUBLIC_SUPABASE_URL || "";
const KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "";
export const OTP_LEN = 6;   // Supabase's default code length

let client = null;
let token = "";

function getClient() {
  if (client || !URL || !KEY || typeof window === "undefined") return client;
  client = createClient(URL, KEY, { auth: { persistSession: true, autoRefreshToken: true } });
  client.auth.getSession().then(({ data }) => { token = data?.session?.access_token || ""; }).catch(() => {});
  client.auth.onAuthStateChange((_event, session) => { token = session?.access_token || ""; });
  return client;
}

export const authEnabled = () => !!(URL && KEY);

/* The current access token, or "" — synchronous by contract (see the header). */
export function accessToken() {
  if (!authEnabled()) return "";
  getClient();
  if (token) return token;
  try {
    const k = Object.keys(window.localStorage).find((x) => x.startsWith("sb-") && x.endsWith("-auth-token"));
    if (k) {
      const s = JSON.parse(window.localStorage.getItem(k) || "null");
      token = (s && s.access_token) || "";
    }
  } catch {}
  return token;
}

const e164 = (mobile10) => `+91${String(mobile10 || "").replace(/\D/g, "")}`;

/* Ask Supabase to send the OTP. Resolves to "" on success, or the sentence to show. */
export async function sendOtp(mobile10) {
  const c = getClient();
  if (!c) return "Sign-in service is not configured.";
  const { error } = await c.auth.signInWithOtp({ phone: e164(mobile10) });
  if (!error) return "";
  if (/rate|too many|limit/i.test(error.message)) return "Too many attempts — please wait a minute and try again.";
  return "Couldn't send the OTP right now. Please try again.";
}

/* Check the code. Resolves to "" on success (the session is now live), else the sentence. */
export async function verifyOtp(mobile10, code) {
  const c = getClient();
  if (!c) return "Sign-in service is not configured.";
  const { data, error } = await c.auth.verifyOtp({ phone: e164(mobile10), token: String(code || ""), type: "sms" });
  if (error) {
    if (/expired/i.test(error.message)) return "That code has expired — tap Resend to get a new one.";
    return "That code didn't match. Please check and try again.";
  }
  token = data?.session?.access_token || token;
  return "";
}

export async function signOutAuth() {
  token = "";
  const c = getClient();
  if (!c) return;
  try { await c.auth.signOut(); } catch {}
}

/* Identity headers for the few fetches that run BEFORE setUser (front-door subscribe path:
 * Agreement, SubscribeFlow). Bearer when a Supabase session exists, else the dev header —
 * the same rule withUser() applies for signed-in calls. */
export function authHeaders(userId) {
  const t = accessToken();
  if (t) return { Authorization: `Bearer ${t}` };
  return userId ? { "X-Aruvi-User": userId } : {};
}
