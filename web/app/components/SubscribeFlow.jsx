"use client";
import { useEffect, useMemo, useState } from "react";
import { API, getJSON, pretty } from "../lib/format";

/* ── The subscribe wizard: About you → Subjects & stages (dropdown-row cart) → Pay ──
 *
 * ONE implementation, two doors (founder, 2026-08-25):
 *   · the FRONT DOOR — Login's subscribe path, entered after OTP verification;
 *   · IN-APP — the trial-exhausted paywall's Subscribe button, for a teacher who is
 *     already signed in (her mobile already verified), landing at About you with the
 *     rail showing Verify done.
 *
 * Props: userId (the mobile/id the checkout runs as — the X-Aruvi-User header),
 * chrome (optional bar element rendered on top; Login passes its Bar, the in-app
 * overlay passes none), onDone(userId) after activation, onCancel for backing out of
 * the first step. Pay is the HONEST STUB (no fake gateway; activates instantly via
 * the server's dev checkout and says so). */

const ROLES = ["Teacher", "Academic coordinator", "Head of school", "Other"];
const STATES = ["Andhra Pradesh", "Assam", "Bihar", "Chhattisgarh", "Delhi", "Goa",
  "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
  "Madhya Pradesh", "Maharashtra", "Odisha", "Punjab", "Rajasthan", "Tamil Nadu",
  "Telangana", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Other"];
const STAGE_OF = (g) => {
  const r = (g || "").toLowerCase();
  if (["iii", "iv", "v"].includes(r)) return "preparatory";
  if (["vi", "vii", "viii"].includes(r)) return "middle";
  return "secondary";
};
/* Secondary says Class 9 only for now — the Class 10 books are not out yet
 * (founder, 2026-08-25). */
const STAGE_CLASSES = { preparatory: "Class 3, 4 & 5", middle: "Class 6, 7 & 8",
                        secondary: "Class 9 (Class 10 coming soon)" };
const scopeLabel = (scope) => {
  const [s, st] = String(scope).split("/");
  return `${pretty(s)} · ${pretty(st)}`;
};

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

/* The ONE bar (same chrome the shell/first-run/front-door wear) — the wizard's default
 * when the caller passes none, so the in-app paywall path is never bare-headed
 * (founder, 2026-08-25). */
const DefaultBar = () => (
  <div className="fr-brand ob-bar">
    <header className="hdr">
      <div className="brand">
        <span className="brand-row">Aruvi<em>.</em></span>
        <span className="hdr-brand-tag">lesson studio</span>
      </div>
    </header>
  </div>
);

export default function SubscribeFlow({ userId, chrome = <DefaultBar />, onDone, onCancel }) {
  const [screen, setScreen] = useState("about");    // about | cart | pay
  const [name, setName] = useState("");
  const [role, setRole] = useState("");
  const [stateName, setStateName] = useState("");
  const [city, setCity] = useState("");
  const [school, setSchool] = useState("");
  const [stageMap, setStageMap] = useState(null);
  const [rows, setRows] = useState([{ subject: "", stage: "" }]);
  const [price, setPrice] = useState(500);
  const [payBusy, setPayBusy] = useState(false);
  const [payErr, setPayErr] = useState("");

  useEffect(() => {
    if (screen !== "cart" || stageMap) return;
    getJSON("/entitlement").then((d) => {
      if (d && d.price_per_subject_stage) setPrice(d.price_per_subject_stage);
    }).catch(() => {});
    getJSON("/subjects").then(async (d) => {
      const map = {};
      for (const s of d.subjects || []) {
        try {
          const g = await getJSON(`/subjects/${s}/grades`);
          const stages = Array.from(new Set((g.grades || []).map(STAGE_OF)));
          map[s] = ["preparatory", "middle", "secondary"].filter((st) => stages.includes(st));
        } catch {}
      }
      setStageMap(map);
    }).catch(() => setStageMap({}));
  }, [screen, stageMap]);

  const cartScopes = useMemo(() => Array.from(new Set(
    rows.filter((r) => r.subject && r.stage).map((r) => `${r.subject}/${r.stage}`))),
    [rows]);

  const doCheckout = async () => {
    setPayBusy(true); setPayErr("");
    try {
      const r = await fetch(`${API}/onboarding/checkout`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-Aruvi-User": userId },
        body: JSON.stringify({ scopes: cartScopes, name, role, state: stateName, city, school }),
      });
      if (!r.ok) throw new Error(String(r.status));
      onDone && onDone(userId);
    } catch {
      setPayErr("Couldn't complete the activation. Try again in a moment.");
      setPayBusy(false);
    }
  };

  if (screen === "about") {
    return (
      <div className="ob-wrap">
        {chrome}
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
          <button className="fr-link" onClick={() => onCancel && onCancel()}>← Back</button>
        </div>
      </div>
    );
  }

  if (screen === "cart") {
    const total = cartScopes.length * price;
    const subjectsAvail = stageMap ? Object.keys(stageMap) : [];
    const setRow = (i, patch) => setRows((rs) =>
      rs.map((r, j) => (j === i ? { ...r, ...patch } : r)));
    const dropRow = (i) => setRows((rs) =>
      rs.length > 1 ? rs.filter((_, j) => j !== i) : [{ subject: "", stage: "" }]);
    return (
      <div className="ob-wrap">
        {chrome}
        <div className="ob-body">
          <Steps at={2} />
          <h1 className="ob-title">What do you teach?</h1>
          <p className="ob-sub">Each subject &amp; stage is its own subscription — unlimited
            lesson plans across all its classes. The total updates as you add.</p>
          {!stageMap && <div className="fr-loading">Loading subjects…</div>}
          {stageMap && rows.map((r, i) => (
            <div className="ob-row" key={i}>
              {/* No per-row price (founder, 2026-08-25) — the total below carries the
                  money; the row is all Subject + Stage. Placeholder words bold. */}
              <div className="ob-row-selects">
                <select value={r.subject} className={r.subject ? "" : "ob-ph"}
                  onChange={(e) => setRow(i, { subject: e.target.value, stage: "" })}>
                  <option value="">Subject</option>
                  {subjectsAvail.map((s) => <option key={s} value={s}>{pretty(s)}</option>)}
                </select>
                <select value={r.stage} disabled={!r.subject} className={r.stage ? "" : "ob-ph"}
                  onChange={(e) => setRow(i, { stage: e.target.value })}>
                  <option value="">Stage</option>
                  {(stageMap[r.subject] || []).map((st) =>
                    <option key={st} value={st}>{pretty(st)}</option>)}
                </select>
                <button type="button" className="ob-row-x" aria-label="Remove this row"
                  onClick={() => dropRow(i)}>✕</button>
              </div>
              {r.stage && <p className="ob-row-classes">{STAGE_CLASSES[r.stage]}</p>}
            </div>
          ))}
          {stageMap && (
            <button type="button" className="ob-addrow"
              onClick={() => setRows((rs) => [...rs, { subject: "", stage: "" }])}>
              + Add another subject &amp; stage
            </button>
          )}
          <div className="ob-total"><span>Total</span><b>₹{total} / year</b></div>
        </div>
        <div className="ob-foot">
          <button className="primary fr-cta" disabled={!cartScopes.length}
            onClick={() => setScreen("pay")}>Continue →</button>
          <button className="fr-link" onClick={() => setScreen("about")}>← Back</button>
        </div>
      </div>
    );
  }

  /* pay */
  const total = cartScopes.length * price;
  return (
    <div className="ob-wrap">
      {chrome}
      <div className="ob-body">
        <Steps at={3} />
        <h1 className="ob-title">Review &amp; pay</h1>
        {cartScopes.map((cid) => (
          <div className="ob-payrow" key={cid}><span>{scopeLabel(cid)}</span><span>₹{price}</span></div>
        ))}
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
