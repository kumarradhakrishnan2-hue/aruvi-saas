"use client";
import { useEffect, useRef, useState } from "react";
import { API, getJSON } from "../lib/format";
import SubscribeFlow from "./SubscribeFlow";

/* ───────── The front door — onboarding + sign-in (founder, 2026-08-24/25) ─────────
 *
 * FIRST-TIME device → CHOOSE (benefits + Free-to-try/Subscribe cards, honest bullets)
 * → OTP (mobile IS the identity; four auto-advancing boxes; ★ stub code 0000, labeled)
 * → TRIAL: straight in · SUBSCRIBE: SubscribeFlow (About you → Subjects-cart → Pay
 * stub — ONE implementation shared with the in-app paywall's Subscribe button).
 * OTP verification REGISTERS the number in the tenant database (/onboarding/verified);
 * the SIGN-IN screen (returning device) admits registered identities only
 * (/onboarding/known) and points unknown numbers at Create sign in. Production: the
 * app identifies the number itself + face/biometrics; the contracts stay. */

const Benefits = () => (
  <>
    <h1 className="ob-headline">Plan engaging, NCF-aligned lessons in seconds.</h1>
    <p className="ob-benefits">
      <span className="ob-tick">✓</span> Lesson plan in seconds, not hours&ensp;
      <span className="ob-tick">✓</span> NCF / NCERT aligned&ensp;
      <span className="ob-tick">✓</span> Assessment built in&ensp;
      <span className="ob-tick">✓</span> Every section&rsquo;s status at one glance
    </p>
  </>
);

/* The ONE bar — the same chrome the shell and first run wear, un-fixed for these
 * scrolling screens. */
const Bar = () => (
  <div className="fr-brand ob-bar">
    <header className="hdr">
      <div className="brand">
        <span className="brand-row">Aruvi<em>.</em></span>
        <span className="hdr-brand-tag">lesson studio</span>
      </div>
    </header>
  </div>
);

const SEEN_KEY = "aruvi_device_seen";

export default function Login({ onEnter }) {
  const [screen, setScreen] = useState("signin");   // choose | signin | otp | subscribe
  const [mode, setMode] = useState("trial");        // trial | subscribe (the page-1 choice)
  // OTP — four boxes, auto-advance (founder, 2026-08-25). `otp` is the joined string.
  const [mobile, setMobile] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [otp, setOtp] = useState("");
  const [otpErr, setOtpErr] = useState("");
  const otpRefs = [useRef(null), useRef(null), useRef(null), useRef(null)];
  // Sign-in
  const [id, setId] = useState("");
  const [signinErr, setSigninErr] = useState("");
  const inputRef = useRef(null);

  // First-time device → the choose screen; returning → sign-in.
  useEffect(() => {
    try {
      if (!window.localStorage.getItem(SEEN_KEY)) setScreen("choose");
    } catch {}
  }, []);

  // Desktop-only autofocus on the sign-in field (2026-08-08 rule).
  useEffect(() => {
    if (screen !== "signin") return;
    if (typeof window === "undefined" || !window.matchMedia) return;
    if (window.matchMedia("(min-width: 601px)").matches) inputRef.current?.focus();
  }, [screen]);

  const markSeen = () => { try { window.localStorage.setItem(SEEN_KEY, "1"); } catch {} };
  const enter = (theId) => { markSeen(); onEnter && onEnter(theId); };

  const mobileOk = /^\d{10}$/.test(mobile.trim());

  /* One OTP box changed: keep digits only, write it into position i, advance. */
  const setOtpDigit = (i, v) => {
    const d = v.replace(/\D/g, "").slice(-1);
    setOtp((cur) => {
      const arr = [cur[0] || "", cur[1] || "", cur[2] || "", cur[3] || ""];
      arr[i] = d;
      return arr.join("");
    });
    if (d && i < 3) otpRefs[i + 1].current?.focus();
  };
  const otpKeyDown = (i, e) => {
    if (e.key === "Backspace" && !(otp[i] || "") && i > 0) otpRefs[i - 1].current?.focus();
  };

  /* OTP verified → the number JOINS THE TENANT DATABASE; then route by mode. */
  const verifyOtp = () => {
    if (otp !== "0000") { setOtpErr("That code didn't match. (Preview build: use 0000.)"); return; }
    setOtpErr("");
    const num = mobile.trim();
    fetch(`${API}/onboarding/verified`, {
      method: "POST", headers: { "X-Aruvi-User": num },
    }).catch(() => {});
    if (mode === "subscribe") setScreen("subscribe");
    else enter(num);
  };

  /* ── SUBSCRIBE — the shared wizard (also reachable in-app from the paywall) ── */
  if (screen === "subscribe") {
    return <SubscribeFlow userId={mobile.trim()} chrome={<Bar />}
      onDone={(uid) => enter(uid)} onCancel={() => setScreen("otp")} />;
  }

  /* ── 1 · CHOOSE ── */
  if (screen === "choose") {
    return (
      <div className="ob-wrap">
        <Bar />
        <div className="ob-body">
          <Benefits />
          <h2 className="ob-h2">Choose what works for you</h2>

          <button type="button" className={`ob-plan ${mode === "trial" ? "on" : ""}`}
            onClick={() => setMode("trial")}>
            <span className="ob-plan-hd"><b>Free to try</b></span>
            <span className="ob-plan-sub">Try Aruvi with no cost. Perfect to explore and get started.</span>
            <span className="ob-plan-points">Any 3 chapters · unlimited lesson plans per chapter · all core features to plan &amp; assess</span>
          </button>

          <button type="button" className={`ob-plan ob-plan-sub2 ${mode === "subscribe" ? "on" : ""}`}
            onClick={() => setMode("subscribe")}>
            <span className="ob-plan-hd"><b>Subscribe</b></span>
            <span className="ob-plan-sub">Unlimited access to plan across your entire syllabus.</span>
            <span className="ob-plan-points">Unlimited chapters · your full subject &amp; stage, every class in it</span>
          </button>
        </div>
        <div className="ob-foot">
          <button className="primary fr-cta" onClick={() => setScreen("otp")}>
            Create sign in →
          </button>
          <button className="fr-link" onClick={() => setScreen("signin")}>Already have an ID? Sign in</button>
        </div>
      </div>
    );
  }

  /* ── 2 · OTP (both paths) ── */
  if (screen === "otp") {
    return (
      <div className="ob-wrap">
        <Bar />
        <div className="ob-body">
          <h1 className="ob-title">Let&rsquo;s verify your mobile</h1>
          <p className="ob-sub">We&rsquo;ll send you a one-time password (OTP) to sign in securely.</p>
          <label className="login-field ob-field">
            <span>Enter your mobile number</span>
            <div className="ob-mobile-row">
              <span className="ob-cc">+91</span>
              <input type="tel" inputMode="numeric" maxLength={10} value={mobile}
                onChange={(e) => setMobile(e.target.value.replace(/\D/g, ""))}
                placeholder="Enter mobile number" />
            </div>
          </label>
          <p className="ob-quiet">We&rsquo;ll never share your number.</p>

          {!otpSent ? (
            <button className="primary fr-cta ob-cta" disabled={!mobileOk}
              onClick={() => setOtpSent(true)}>Generate OTP →</button>
          ) : (
            <>
              {/* Four boxes, auto-advance; backspace steps back (founder, 2026-08-25). */}
              <div className="ob-field">
                <span className="ob-otp-label">Enter the OTP</span>
                <div className="ob-otp-row">
                  {[0, 1, 2, 3].map((i) => (
                    <input key={i} ref={otpRefs[i]} className="ob-otp-box" type="tel"
                      inputMode="numeric" maxLength={1} value={otp[i] || ""}
                      onChange={(e) => setOtpDigit(i, e.target.value)}
                      onKeyDown={(e) => otpKeyDown(i, e)}
                      aria-label={`OTP digit ${i + 1}`} />
                  ))}
                </div>
              </div>
              {/* Honest stub — no SMS goes out in the preview. */}
              <p className="ob-quiet">Preview build: enter <b>0000</b>.</p>
              {otpErr && <p className="ob-err" role="alert">{otpErr}</p>}
              <button className="primary fr-cta ob-cta" disabled={otp.length !== 4}
                onClick={verifyOtp}>Verify &amp; continue →</button>
            </>
          )}
        </div>
        <div className="ob-foot">
          <button className="fr-link" onClick={() => setScreen("choose")}>← Back</button>
        </div>
      </div>
    );
  }

  /* ── SIGN IN (returning) — registered identities only, MOBILE or EMAIL only
   * (founder, 2026-08-26: no free-form user IDs at the front door; an email resolves
   * server-side to its account's mobile, which is what the session runs under). ── */
  const trimmed = id.trim();
  const signinOk = /^\d{10}$/.test(trimmed) || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmed);
  const submitSignin = async (e) => {
    e.preventDefault();
    if (!signinOk) return;
    setSigninErr("");
    try {
      const d = await getJSON(`/onboarding/known?id=${encodeURIComponent(trimmed)}`);
      if (d && d.known) { enter(d.id || trimmed); return; }
      if (d && d.reason === "ambiguous_email") {
        // More than one account carries this address — only the mobile identifies her.
        setSigninErr("More than one Aruvi account uses this email. Please sign in with your mobile number.");
        return;
      }
      setSigninErr("We don't recognise this mobile or email yet — tap “New to Aruvi? Get started” below to create your sign in.");
    } catch {
      setSigninErr("Couldn't reach Aruvi right now. Try again in a moment.");
    }
  };
  return (
    <div className="ob-wrap">
      <Bar />
      <div className="ob-body">
        <Benefits />
        <div className="ob-rule" />
        <div className="kicker login-kicker">Sign in</div>
        <h1 className="login-q">Who&rsquo;s planning today?</h1>
        <form onSubmit={submitSignin}>
          <label className="login-field ob-field">
            <span>Mobile number or email</span>
            <input ref={inputRef} type="text" value={id} onChange={(e) => setId(e.target.value)}
              placeholder="98xxxxxxxx or you@example.com" autoComplete="off" spellCheck={false} />
          </label>
          <button type="submit" className="primary login-btn" disabled={!signinOk}>
            Enter Aruvi →
          </button>
        </form>
        {signinErr && <p className="ob-err" role="alert">{signinErr}</p>}
        <p className="fr-secure">🛡 Your data is private and secure</p>
      </div>
      <div className="ob-foot">
        <button className="fr-link" onClick={() => setScreen("choose")}>New to Aruvi? Get started →</button>
      </div>
    </div>
  );
}
