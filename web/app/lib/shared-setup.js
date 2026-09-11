/* ───────── web boot for @aruvi/shared (Track D step 1, 2026-09-11) ─────────
 *
 * The client logic that used to live in this folder now lives in packages/shared and runs
 * on the phone too. It knows nothing about browsers: this module installs the three things
 * the web supplies, and every lib/*.js wrapper imports it FIRST so the install has happened
 * before any shared function runs, whichever wrapper a component imported.
 *   · storage      → window.localStorage (SSR: the in-memory stand-in; nothing renders from
 *                    it there anyway — every cache is read on the client after mount)
 *   · API          → NEXT_PUBLIC_API_URL when set (web/.env.local — e.g. the deployed
 *                    https://meyy-api.onrender.com); otherwise the host the page loaded
 *                    from, so a plain `npm run dev` works on localhost and on the Mac's LAN
 *                    IP (phone testing over WiFi) with no hand-edited IP per session
 *   · accessToken  → the shared auth module's mirror of the supabase-js session, whose
 *                    client is created here when NEXT_PUBLIC_SUPABASE_URL/ANON_KEY are set */
import { createClient } from "@supabase/supabase-js";
import { configure } from "@aruvi/shared/config";
import { setStorage, webStorage } from "@aruvi/shared/storage";
import { configureAuth, accessToken } from "@aruvi/shared/auth";

setStorage(webStorage());

configure({
  apiBase:
    (process.env.NEXT_PUBLIC_API_URL || "").replace(/\/+$/, "") ||
    (typeof window !== "undefined" ? `http://${window.location.hostname}:8000` : "http://localhost:8000"),
  accessToken,
});

const URL = process.env.NEXT_PUBLIC_SUPABASE_URL || "";
const KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "";
if (URL && KEY && typeof window !== "undefined") {
  configureAuth({ client: createClient(URL, KEY, { auth: { persistSession: true, autoRefreshToken: true } }) });
}
