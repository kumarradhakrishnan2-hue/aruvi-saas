"use client";
import { useEffect, useMemo, useRef, useState } from "react";
import { API, getJSON, pretty } from "../lib/format";

/* ───────── The front door — onboarding + sign-in (founder, 2026-08-24) ─────────
 *
 * FIRST-TIME visitor (this device has never signed in):
 *   1 · CHOOSE   — benefits + "Choose what works for you": Free to try (highlighted
 *                  by default, no badge) vs Subscribe (honest bullets only — no
 *                  "priority support"/"export & more": trial exports too, and support
 *                  doesn't exist yet). One CTA: "Create sign in".
 *   2 · OTP      — mobile number IS the identity (WhatsApp/UPI-era norm; one field,
 *                  not two). Generate OTP → enter code. ★ STUB: code 0000 verifies —
 *                  this is UI shaped for the real SMS vendor behind the AuthProvider
 *                  seam; a dummy OTP protects nothing and is honestly labeled.
 *   3a · SUBSCRIBE path, with the step rail (Verify → About you → Subjects → Pay):
 *        About you — name/role/state/city/school(optional): what the receipt and
 *        DPDP contact genuinely need, nothing more. Subjects — the picker IS the
 *        cart: tick subject·stage combos, the total updates live (price from the
 *        server). Pay — ★ HONEST STUB: no fake gateway; the preview activates the
 *        subscription server-side (ManualBillingProvider) and says so. On iOS this
 *        whole step swaps to Apple IAP later — it stays its own screen for that.
 *   3b · TRIAL path — straight in: onEnter(mobile), first run takes over.
 *
 * RETURNING visitor (device has signed in before): the SIGN-IN screen — same benefits
 * block, then "Who's planning today?" (no sub-text; founder), a field that accepts a
 * mobile number or a legacy user ID, Enter Aruvi. "New to Aruvi?" links back to 1.
 *
 * onEnter(id) stays the single exit for every path — the shell stores the id and the
 * X-Aruvi-User contract is unchanged (mobile is just the id's new shape). */

const SEEN_KEY = "aruvi_device_seen";
const STAGE_OF = (g) => {
  const r = (g || "").toLowerCase();
  if (["iii", "iv", "v"].includes(r)) return "preparatory";
  if (["vi", "vii", "viii"].includes(r)) return "middle";
  return "secondary";
};
const ROLES = ["Teacher", "Academic coordinator", "Head of school", "Other"];
const STATES = ["Andhra Pradesh", "Assam", "Bihar", "Chhattisgarh", "Delhi", "Goa",
  "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
  "Madhya Pradesh", "Maharashtra", "Odisha", "Punjab", "Rajasthan", "Tamil Nadu",
  "Telangana", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Other"];

const Benefits = () => (
  <>
    <h1 className="ob-headline">Plan engaging, NCF-aligned lessons in minutes.</h1>
    <ul className="fr-pain-list ob-ticks">
      <li><span className="fr-pain-tick">✓</span><span>Lesson plan in seconds, not hours</span></li>
      <li><span className="fr-pain-tick">✓</span><span>NCF / NCERT aligned</span></li>
      <li><span className="fr-pain-tick">✓</span><span>Assessment built in</span></li>
      <li><span className="fr-pain-tick">✓</span><span>Every section&rsquo;s status at one glance</span></li>
    </ul>
  </>
);

const Bar = () => (
  <div className="ob-bar">
    <span className="brand-row">Aruvi<em>.</em></span>
    <span className="ob-bar-tag">lesson studio · NCF 2023 aligned</span>
  </div>
);

/* The subscribe path's step rail (founder: the subscriber needs to know the stages). */
const Steps = ({ at }) => {
  const names = ["Verify", "About you", "Subjects", "Pay"];
  return (
    <div className="ob-steps">
      {names.map((n, i) => (
        <span key={n} className={`ob-step ${i === at ? "on" : ""} ${i < at ? "done" : ""}`}>
          <span className="ob-step-n">{i + 1}</span>
          <span className="ob-step-l">{n}</span>
        </span>
      ))}
    </div>
  );
};

export default function Login({ onEnter }) {
  const [screen, setScreen] = useState("signin");   // choose | signin | otp | about | cart | pay
  const [mode, setMode] = useState("trial");        // trial | subscribe (the page-1 choice)
  // OTP
  const [mobile, setMobile] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [otp, setOtp] = useState("");
  const [otpErr, setOtpErr] = useState("");
  // About you
  const [name, setName] = useState("");
  const [role, setRole] = useState("");
  const [stateName, setStateName] = useState("");
  const [city, setCity] = useState("");
  const [school, setSchool] = useState("");
  // Cart
  const [combos, setCombos] = useState([]);         // [{id:"subject/stage", label}]
  const [cart, setCart] = useState([]);             // picked combo ids
  const [price, setPrice] = useState(500);          // per subject-stage, from the server
  const [payBusy, setPayBusy] = useState(false);
  const [payErr, setPayErr] = useState("");
  // Legacy sign-in
  const [id, setId] = useState("");
  const inputRef = useRef(null);

  // First-time device → the choose screen; returning → sign-in.
  useEffect(() => {
    try {
      if (!window.localStorage.getItem(SEEN_KEY)) setScreen("choose");
    } catch {}
  }, []);

  // Desktop-only autofocus on the sign-in field (2026-08-08 rule — phones must not
  // raise the keyboard over the brand on load).
  useEffect(() => {
    if (screen !== "signin") return;
    if (typeof window === "undefined" || !window.matchMedia) return;
    if (window.matchMedia("(min-width: 601px)").matches) inputRef.current?.focus();
  }, [screen]);

  // The 11 subject-stage combos, derived (never hardcoded) from what the content
  // actually offers; price rides on /entitlement.
  useEffect(() => {
    if (screen !== "cart" || combos.length) return;
    getJSON("/entitlement").then((d) => {
      if (d && d.price_per_subject_stage) setPrice(d.price_per_subject_stage);
    }).catch(() => {});
    getJSON("/subjects").then(async (d) => {
      const out = [];
      for (const s of d.subjects || []) {
        try {
          const g = await getJSON(`/subjects/${s}/grades`);
          const stages = Array.from(new Set((g.grades || []).map(STAGE_OF)));
          ["preparatory", "middle", "secondary"].forEach((st) => {
            if (stages.includes(st)) out.push({ id: `${s}/${st}`, label: `${pretty(s)} · ${pretty(st)}` });
          });
        } catch {}
      }
      setCombos(out);
    }).catch(() => setCombos([]));
  }, [screen, combos.length]);

  const markSeen = () => { try { window.localStorage.setItem(SEEN_KEY, "1"); } catch {} };
  const enter = (theId) => { markSeen(); onEnter && onEnter(theId); };

  const mobileOk = /^\d{10}$/.test(mobile.trim());
  const verifyOtp = () => {
    if (otp.trim() !== "0000") { setOtpErr("That code didn't match. (Preview build: use 0000.)"); return; }
    setOtpErr("");
    if (mode === "subscribe") setScreen("about");
    else enter(mobile.trim());                       // trial: straight in, first run takes over
  };

  const doCheckout = async () => {
    setPayBusy(true); setPayErr("");
    try {
      const r = await fetch(`${API}/onboarding/checkout`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-Aruvi-User": mobile.trim() },
        body: JSON.stringify({ scopes: cart, name, role, state: stateName, city, school }),
      });
      if (!r.ok) throw new Error(String(r.status));
      enter(mobile.trim());
    } catch {
      setPayErr("Couldn't complete the activation. Try again in a moment.");
      setPayBusy(false);
    }
  };

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
            <span className="ob-plan-points">Unlimited chapters · your full subject &amp; stage, every class in it · everything in Free to try, without the 3-chapter cap</span>
          </button>

          <p className="ob-switchnote">🔒 You can upgrade or switch anytime.</p>
        </div>
        <div className="ob-foot">
          <button className="primary fr-cta" onClick={() => { setScreen("otp"); }}>
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
          {mode === "subscribe" && <Steps at={0} />}
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
              <label className="login-field ob-field">
                <span>Enter the OTP</span>
                <input type="tel" inputMode="numeric" maxLength={4} value={otp}
                  onChange={(e) => setOtp(e.target.value.replace(/\D/g, ""))}
                  placeholder="4-digit code" />
              </label>
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

  /* ── 3a·1 · ABOUT YOU (subscribe) ── */
  if (screen === "about") {
    return (
      <div className="ob-wrap">
        <Bar />
        <div className="ob-body">
          <Steps at={1} />
          <h1 className="ob-title">Tell us a bit about yourself</h1>
          <p className="ob-sub">For your receipt and your account — nothing more.</p>
          <label className="login-field ob-field"><span>Your name</span>
            <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Enter your full name" /></label>
          <label className="login-field ob-field"><span>Role</span>
            <select value={role} onChange={(e) => setRole(e.target.value)}>
              <option value="">Select your role</option>
              {ROLES.map((r) => <option key={r} value={r}>{r}</option>)}
            </select></label>
          <label className="login-field ob-field"><span>State</span>
            <select value={stateName} onChange={(e) => setStateName(e.target.value)}>
              <option value="">Select your state</option>
              {STATES.map((s) => <option key={s} value={s}>{s}</option>)}
            </select></label>
          <label className="login-field ob-field"><span>City</span>
            <input type="text" value={city} onChange={(e) => setCity(e.target.value)} placeholder="Enter your city" /></label>
          <label className="login-field ob-field"><span>School name (optional)</span>
            <input type="text" value={school} onChange={(e) => setSchool(e.target.value)} placeholder="Enter your school name" /></label>
        </div>
        <div className="ob-foot">
          <button className="primary fr-cta" disabled={!name.trim() || !role || !stateName}
            onClick={() => setScreen("cart")}>Save &amp; continue →</button>
          <button className="fr-link" onClick={() => setScreen("otp")}>← Back</button>
        </div>
      </div>
    );
  }

  /* ── 3a·2 · SUBJECTS & STAGES — the picker IS the cart ── */
  if (screen === "cart") {
    const total = cart.length * price;
    const toggle = (cid) => setCart((c) => (c.includes(cid) ? c.filter((x) => x !== cid) : [...c, cid]));
    return (
      <div className="ob-wrap">
        <Bar />
        <div className="ob-body">
          <Steps at={2} />
          <h1 className="ob-title">What do you teach?</h1>
          <p className="ob-sub">Each subject &amp; stage is its own subscription — unlimited lesson
            plans across all its classes. Tick what you teach; the total updates as you go.</p>
          {combos.length === 0 && <div className="fr-loading">Loading subjects…</div>}
          {combos.map((c) => (
            <button type="button" key={c.id} className={`ob-combo ${cart.includes(c.id) ? "on" : ""}`}
              onClick={() => toggle(c.id)}>
              <span className="ob-combo-tick">{cart.includes(c.id) ? "✓" : ""}</span>
              <span className="ob-combo-l">{c.label}</span>
              <span className="ob-combo-p">₹{price}/yr</span>
            </button>
          ))}
          <div className="ob-total"><span>Total</span><b>₹{total} / year</b></div>
        </div>
        <div className="ob-foot">
          <button className="primary fr-cta" disabled={!cart.length}
            onClick={() => setScreen("pay")}>Continue →</button>
          <button className="fr-link" onClick={() => setScreen("about")}>← Back</button>
        </div>
      </div>
    );
  }

  /* ── 3a·3 · PAY (honest stub — activates via the founder-gateway, says so) ── */
  if (screen === "pay") {
    const total = cart.length * price;
    return (
      <div className="ob-wrap">
        <Bar />
        <div className="ob-body">
          <Steps at={3} />
          <h1 className="ob-title">Review &amp; pay</h1>
          {cart.map((cid) => {
            const c = combos.find((x) => x.id === cid);
            return <div className="ob-payrow" key={cid}><span>{c ? c.label : cid}</span><span>₹{price}</span></div>;
          })}
          <div className="ob-total"><span>Total</span><b>₹{total} / year</b></div>
          <p className="ob-quiet">Preview build: online payment opens soon — this activates your
            subscription right away.</p>
          {payErr && <p className="ob-err" role="alert">{payErr}</p>}
        </div>
        <div className="ob-foot">
          <button className="primary fr-cta" disabled={payBusy} onClick={doCheckout}>
            {payBusy ? "Activating…" : `Pay ₹${total} & start →`}
          </button>
          <button className="fr-link" onClick={() => setScreen("cart")}>← Back</button>
        </div>
      </div>
    );
  }

  /* ── SIGN IN (returning) ── */
  const trimmed = id.trim();
  return (
    <div className="ob-wrap">
      <Bar />
      <div className="ob-body">
        <Benefits />
        <div className="ob-rule" />
        <div className="kicker login-kicker">Sign in</div>
        <h1 className="login-q">Who&rsquo;s planning today?</h1>
        <form onSubmit={(e) => { e.preventDefault(); if (trimmed) enter(trimmed); }}>
          <label className="login-field ob-field">
            <span>Mobile number or user ID</span>
            <input ref={inputRef} type="text" value={id} onChange={(e) => setId(e.target.value)}
              placeholder="e.g. 98xxxxxxxx" autoComplete="off" spellCheck={false} />
          </label>
          <button type="submit" className="primary login-btn" disabled={!trimmed}>
            Enter Aruvi →
          </button>
        </form>
        <p className="fr-secure">🛡 Your data is private and secure</p>
      </div>
      <div className="ob-foot">
        <button className="fr-link" onClick={() => setScreen("choose")}>New to Aruvi? Get started →</button>
      </div>
    </div>
  );
}
