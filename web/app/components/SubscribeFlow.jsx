"use client";
import { useEffect, useMemo, useState } from "react";
import { API, getJSON, pretty, idInUse, errDetail } from "../lib/format";

/* The "already in use" sentence, said the same way wherever a credential clashes
 * (founder, 2026-08-26). Deliberately the SAME words the server's 409 carries — this
 * client-side copy exists only because the early check (/onboarding/known) has no
 * sentence of its own to return; the server's text stays the authority on the Pay path.
 * If one is reworded, reword both: api/main.py `_guard_email_not_taken`. */
export const EMAIL_TAKEN =
  "This email is already in use by another Aruvi account. Use a different address, "
  + "or sign in with that account's mobile number.";
/* Founder, 2026-08-26: this screen CREATES a sign-in, so its refusal stays inside that
 * job — "use a different number". The first cut sent her to the sign-in door with a
 * link; she is standing at the create door, and the instruction there is to create. */
export const MOBILE_TAKEN =
  "This mobile number is already in use. Create using a different number.";

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

export const ROLES = ["Teacher", "Academic coordinator", "Head of school", "Other"];
export const STATES = ["Andhra Pradesh", "Assam", "Bihar", "Chhattisgarh", "Delhi", "Goa",
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
const EMAIL_OK = (e) => /^\S+@\S+\.\S+$/.test((e || "").trim());
const maskEmail = (e) => {
  const [u, d] = String(e).split("@");
  if (!d) return "•••";
  return `${u.slice(0, 1)}•••@${d}`;
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
  /* Email — DOUBLE-BLIND confirmation (founder, 2026-08-25): she types it once; it is
     then HIDDEN (masked) and she types it again fresh. Only a match confirms — a typo
     can't be rubber-stamped by reading the first entry back. Stages:
     enter → confirm → ok. "Change" restarts. */
  const [email, setEmail] = useState("");
  const [email2, setEmail2] = useState("");
  const [emailStage, setEmailStage] = useState("enter");   // enter | confirm | ok
  const [emailErr, setEmailErr] = useState("");
  const [emailBusy, setEmailBusy] = useState(false);   // the "already in use" round-trip
  const [role, setRole] = useState("");
  const [stateName, setStateName] = useState("");
  const [city, setCity] = useState("");
  const [school, setSchool] = useState("");
  const [stageMap, setStageMap] = useState(null);
  const [owned, setOwned] = useState([]);            // live scopes — not for sale again
  const [trialChapters, setTrialChapters] = useState([]);   // for the purge notice on Pay
  const [rows, setRows] = useState([{ subject: "", stage: "" }]);
  const [price, setPrice] = useState(500);
  const [payBusy, setPayBusy] = useState(false);
  const [payErr, setPayErr] = useState("");

  /* A KNOWN personal profile skips About-you (founder, 2026-08-26): a lapsed teacher
     re-subscribing already gave her name/email/role/state at first checkout — asking
     again is friction with no purpose. Prefill ALWAYS (checkout overwrites account
     fields, so resending her existing values is what preserves them); jump straight to
     the SUBJECTS step when the essentials are complete. A fresh post-OTP account has
     empty fields → About-you shows as normal. */
  useEffect(() => {
    let live = true;
    fetch(`${API}/account`, { headers: { "X-Aruvi-User": userId } })
      .then((r) => (r.ok ? r.json() : null))
      .then((a) => {
        if (!live || !a) return;
        const nm = (a.display_name || "").trim();
        const looksReal = nm && !/^\d+$/.test(nm);           // a number is not a name
        if (looksReal) setName(nm);
        if (a.email) { setEmail(a.email); setEmailStage("ok"); }
        if (a.role) setRole(a.role);
        if (a.state) setStateName(a.state);
        if (a.city) setCity(a.city);
        if (a.school_name) setSchool(a.school_name);
        if (looksReal && a.email && a.role && a.state) setScreen("cart");
      })
      .catch(() => {});
    return () => { live = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userId]);

  useEffect(() => {
    if (screen !== "cart" || stageMap) return;
    getJSON("/entitlement").then((d) => {
      if (d && d.price_per_subject_stage) setPrice(d.price_per_subject_stage);
      /* ★ What she ALREADY holds, live, is not for sale again (founder, 2026-08-26).
         `live_scopes` is the server's own answer — the client never compares dates. A
         trial's "*" is not a holding: it would swallow the entire catalogue. */
      const live = (d && Array.isArray(d.live_scopes)) ? d.live_scopes : [];
      setOwned(d && d.status === "trial" ? [] : live.filter((s) => s !== "*"));
      // Only a teacher still ON the trial has trial artifacts left to lose.
      setTrialChapters(d && d.status === "trial" ? (d.trial_chapters || []) : []);
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
        body: JSON.stringify({ scopes: cartScopes, name, email: email.trim(),
                               role, state: stateName, city, school }),
      });
      /* ★ THE SERVER'S OWN SENTENCE (2026-08-26). This used to throw the status code
         away and print "Try again in a moment" — advice that can never work for a
         deterministic 409 (a taken email), and which hid a CORRECT refusal well enough
         to read as a broken product. Same lesson as ARV-D-088, same rule: 4xx strings
         are written for her, 5xx are engine talk and keep the generic line. The
         Verify-step check above should have caught the clash already; this is the net
         for the address taken in between, or reached by a path that skipped it. */
      if (!r.ok) {
        setPayErr(await errDetail(r, "Couldn't complete the activation. Try again in a moment."));
        setPayBusy(false);
        return;
      }
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

          {/* Email — double-blind confirm (see the state note above). */}
          {emailStage === "enter" && (
            <>
              <label className="login-field ob-field"><span>Email</span>
                <input type="email" inputMode="email" autoComplete="off" value={email}
                  onChange={(e) => { setEmail(e.target.value); setEmailErr(""); }}
                  placeholder="Enter your email" /></label>
              {/* The taken-address message lands HERE — the stage the fix belongs to. */}
              {emailErr && <p className="ob-err" role="alert">{emailErr}</p>}
              {EMAIL_OK(email) && (
                <button type="button" className="fr-link ob-email-next"
                  onClick={() => { setEmail2(""); setEmailStage("confirm"); }}>
                  Confirm this email →
                </button>
              )}
            </>
          )}
          {emailStage === "confirm" && (
            <>
              <label className="login-field ob-field"><span>Re-enter your email</span>
                <input type="email" inputMode="email" autoComplete="off" autoFocus value={email2}
                  onChange={(e) => { setEmail2(e.target.value); setEmailErr(""); }}
                  placeholder="Type it again to confirm" /></label>
              {emailErr && <p className="ob-err" role="alert">{emailErr}</p>}
              {/* ★ The "already in use" check happens HERE, not at Pay (2026-08-26).
                  The server's 409 was always right; arriving at the END of a checkout is
                  what made it useless — she had chosen subjects and pressed Pay before
                  anything told her, and the only advice on screen was "try again", which
                  for a deterministic clash can never work. One tap from the field she
                  would have to change anyway. */}
              <button type="button" className="fr-link ob-email-next"
                disabled={!EMAIL_OK(email2) || emailBusy}
                onClick={async () => {
                  if (email2.trim().toLowerCase() !== email.trim().toLowerCase()) {
                    setEmailErr("The two entries don't match — try again."); setEmail2("");
                    return;
                  }
                  setEmailBusy(true);
                  const taken = await idInUse(email, userId);
                  setEmailBusy(false);
                  if (taken) {
                    // Back to ENTER with her text intact: the fix is to edit this field.
                    setEmailErr(EMAIL_TAKEN); setEmail2(""); setEmailStage("enter");
                    return;
                  }
                  setEmailStage("ok"); setEmailErr("");
                }}>
                {emailBusy ? "Checking…" : "Verify →"}
              </button>
            </>
          )}
          {emailStage === "ok" && (
            <label className="login-field ob-field"><span>Email</span>
              <div className="ob-email-view">
                <span><span className="ob-tick">✓</span> {maskEmail(email)}</span>
                <button type="button" className="fr-link"
                  onClick={() => { setEmail(""); setEmail2(""); setEmailStage("enter"); }}>
                  change
                </button>
              </div>
            </label>
          )}

          <label className="login-field ob-field"><span>Role</span>
            <select value={role} className={role ? "" : "ob-unset"}
              onChange={(e) => setRole(e.target.value)}>
              <option value="">Select your role</option>
              {ROLES.map((r) => <option key={r} value={r}>{r}</option>)}
            </select></label>
          <label className="login-field ob-field"><span>State</span>
            <select value={stateName} className={stateName ? "" : "ob-unset"}
              onChange={(e) => setStateName(e.target.value)}>
              <option value="">Select your state</option>
              {STATES.map((s) => <option key={s} value={s}>{s}</option>)}
            </select></label>
          <label className="login-field ob-field"><span>City</span>
            <input type="text" value={city} onChange={(e) => setCity(e.target.value)} placeholder="Enter your city" /></label>
          <label className="login-field ob-field"><span>School name (optional)</span>
            <input type="text" value={school} onChange={(e) => setSchool(e.target.value)} placeholder="Enter your school name" /></label>
        </div>
        <div className="ob-foot">
          <button className="primary fr-cta"
            disabled={!name.trim() || emailStage !== "ok" || !role || !stateName}
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
    /* ★ A PAIR MAY BE BOUGHT ONCE (founder, 2026-08-26). The billing unit is
       subject × stage, so a second row of the same pair is meaningless in both
       directions: `cartScopes` de-dupes, so she would see two rows and be charged for
       one — a discrepancy that reads as a bug whichever way she notices it. Rather than
       validate after the fact, the choice is simply not offered: a pair taken by ANOTHER
       row is disabled and says why, and a subject whose every stage is spoken for is
       disabled whole. Never disable this row's OWN value (hence `j !== self`), or
       changing your mind would strand the select on a dead option. */
    /* Taken = in another row of THIS cart, or already held and still running. The two
       are one question to her ("can I pick this?") and so they are one predicate; only
       the wording differs, because "already added" and "you have this" are different
       facts and telling her the wrong one would be worse than saying nothing. */
    const takenElsewhere = (subject, stage, self) => rows.some(
      (r, j) => j !== self && r.subject === subject && r.stage === stage)
      || owned.includes(`${subject}/${stage}`);
    const alreadyOwned = (subject, stage) => owned.includes(`${subject}/${stage}`);
    const subjectFull = (subject, self) => {
      const stages = stageMap[subject] || [];
      return stages.length > 0 && stages.every((st) => takenElsewhere(subject, st, self));
    };
    const nothingLeft = subjectsAvail.length > 0
      && subjectsAvail.every((s) => subjectFull(s, -1));
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
                  {subjectsAvail.map((s) => {
                    const full = subjectFull(s, i);
                    return (
                      <option key={s} value={s} disabled={full}>
                        {pretty(s)}{full ? " — all stages added" : ""}
                      </option>
                    );
                  })}
                </select>
                <select value={r.stage} disabled={!r.subject} className={r.stage ? "" : "ob-ph"}
                  onChange={(e) => setRow(i, { stage: e.target.value })}>
                  <option value="">Stage</option>
                  {(stageMap[r.subject] || []).map((st) => {
                    const dup = takenElsewhere(r.subject, st, i);
                    const mine = alreadyOwned(r.subject, st);
                    return (
                      <option key={st} value={st} disabled={dup}>
                        {pretty(st)}
                        {mine ? " · you have this" : dup ? " · already added" : ""}
                      </option>
                    );
                  })}
                </select>
                <button type="button" className="ob-row-x" aria-label="Remove this row"
                  onClick={() => dropRow(i)}>✕</button>
              </div>
              {r.stage && <p className="ob-row-classes">{STAGE_CLASSES[r.stage]}</p>}
            </div>
          ))}
          {stageMap && (
            // Nothing left to add = no empty row to add it in.
            <button type="button" className="ob-addrow" disabled={nothingLeft}
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
  /* Subjects she TRIALLED but is not buying — their lessons go when this activates.
     Derived from the trial chapter keys ("{subject}/{grade}/{chapter}"), which
     GET /entitlement already returns; nothing new is fetched to ask this. */
  const buying = new Set(cartScopes.map((s) => s.split("/")[0]));
  const droppedTrial = Array.from(new Set(
    (trialChapters || []).map((k) => String(k).split("/")[0]).filter((s) => s && !buying.has(s))));
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
        {/* ★ SAID BEFORE SHE PAYS (founder, 2026-08-26 evening). Subscribing clears
            what the trial left in subjects she is NOT buying. That is her work
            disappearing, so it is stated on the screen with the money on it — the one
            place she can still change the cart — and not discovered afterwards in an
            emptier My Lessons. Named, because "some trial lessons" would send her
            hunting for which. */}
        {droppedTrial.length > 0 && (
          <p className="ob-quiet ob-purge-note">
            Your trial lessons in {droppedTrial.map(pretty).join(" and ")} will be cleared
            when this activates — {droppedTrial.length > 1 ? "those subjects are" : "that subject is"} not
            in your subscription. Everything in what you are subscribing to stays.
          </p>
        )}
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
