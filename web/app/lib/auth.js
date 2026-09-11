/* ───────── Supabase Auth on the web ─────────
 * The logic moved to packages/shared/src/auth.js (Track D step 1, 2026-09-11); the supabase-js
 * client itself is created in shared-setup.js from NEXT_PUBLIC_SUPABASE_URL/ANON_KEY. */
import "./shared-setup";
export * from "@aruvi/shared/auth";
