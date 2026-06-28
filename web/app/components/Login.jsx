"use client";
import { useState } from "react";

/* ───────── User-ID portal (pre-auth tenanting) ─────────
 * The primary entry point to Aruvi. No password stage yet: a teacher types a user ID and
 * enters. That ID becomes the tenant key for everything they do — every API call carries it
 * as the X-Aruvi-User header, and the server treats each ID as its own individual-teacher
 * tenant (tenant_id == user_id). This is what makes the persistence testable across multiple
 * "teachers" today, and it is the exact seam Phase 4 replaces with Supabase Auth: swap this
 * screen for a real sign-in, keep the header/tenant contract.
 *
 * onEnter(userId) hands the trimmed ID up to the shell, which stores it (localStorage) and
 * loads that user's saved readiness profile. Warm-paper design system — Fraunces title,
 * Newsreader prose, mono kicker — consistent with §4. */
export default function Login({ onEnter }) {
  const [id, setId] = useState("");
  const trimmed = id.trim();

  const submit = (e) => {
    e.preventDefault();
    if (!trimmed) return;
    onEnter && onEnter(trimmed);
  };

  return (
    <div className="login-wrap">
      <form className="login-card" onSubmit={submit}>
        <div className="login-brand">
          <span className="brand-row">Aruvi<em>.</em></span>
          <span className="login-tag">lesson studio · NCF 2023 aligned</span>
        </div>

        <div className="kicker login-kicker">Sign in</div>
        <h1 className="login-q">Who’s planning today?</h1>
        <p className="login-ask">
          Enter your user ID to open your planner. Everything you set up — your subjects,
          grades, sections and class times — is saved to this ID and waiting when you return.
        </p>

        <label className="login-field">
          <span>User ID</span>
          <input
            type="text"
            value={id}
            onChange={(e) => setId(e.target.value)}
            placeholder="e.g. Kumar1"
            autoFocus
            autoComplete="off"
            spellCheck={false}
          />
        </label>

        <button type="submit" className="primary login-btn" disabled={!trimmed}>
          Enter Aruvi →
        </button>

        <p className="login-note">No password needed yet — this is an early preview.</p>
      </form>
    </div>
  );
}
