"use client";
import { useEffect, useState } from "react";
import { API, withUser, fetchEntitlement, pretty } from "../lib/format";
import ThemeToggle from "./ThemeToggle";
import { ROLES, STATES } from "./SubscribeFlow";

const EMAIL_OK = (e) => /^\S+@\S+\.\S+$/.test((e || "").trim());
const maskEmail = (e) => {
  const [u, d] = String(e).split("@");
  if (!d) return "•••";
  return `${u.slice(0, 1)}•••@${d}`;
};

/* ── Settings — the gear's own screen (founder, 2026-08-24 second pass) ──
 *
 * CARD list in the founder's order, each a plain-fill card (--card-bg, distinct from
 * the paper background) with icon · title · small text · chevron:
 *
 *   Subscription & billing · "Plan, billing & usage"      → subview (plan state now;
 *                             billing/invoices arrive with online payments)
 *   Your data & export     · "Download your Aruvi data"   → subview (Word / PDF)
 *   Help                   · "Ask Aruvi guide"            → opens Ask Aruvi
 *   Support                · "Email & feedback"           → subview (placeholder —
 *                             UI link now, content when support channels exist)
 *   About Aruvi            · "Version info / legal"       → subview (placeholder)
 *
 * Below the cards, two quiet rows: Appearance (the ThemeToggle, moved off the top
 * bar) and Account (Log out · Delete my account — Apple 5.1.1(v), typed-"erase"
 * confirmation mirroring the API guard). NO Profile card — the person icon beside
 * the gear is the profile's dedicated door (founder point 3).
 *
 * Some cards are deliberately UI-first: the founder's direction is to shape the
 * surface now and fill content as features land (payments → billing; support
 * channels → Support; legal texts → About). Placeholders say so honestly.
 * Data-rights actions are never gated on subscription state (§2.5). */

const scopeLabel = (s) =>
  s === "*" ? "All subjects" : pretty(String(s).replace("/", " · "));

/* Settings › Personal profile — view + edit of the account record. Self-contained:
 * fetches GET /account on mount, saves via POST /account (partial). */
function PersonalProfile({ onSaved }) {
  const [acct, setAcct] = useState(null);
  const [name, setName] = useState("");
  const [role, setRole] = useState("");
  const [stateName, setStateName] = useState("");
  const [city, setCity] = useState("");
  const [school, setSchool] = useState("");
  const [email, setEmail] = useState("");            // confirmed value (unchanged = keep)
  const [emailStage, setEmailStage] = useState("ok"); // ok | enter | confirm
  const [emailNew, setEmailNew] = useState("");
  const [email2, setEmail2] = useState("");
  const [emailErr, setEmailErr] = useState("");
  const [busy, setBusy] = useState(false);
  const [note, setNote] = useState("");

  useEffect(() => {
    fetch(`${API}/account`, withUser()).then((r) => (r.ok ? r.json() : null)).then((a) => {
      if (!a) return;
      setAcct(a);
      setName(a.display_name || ""); setRole(a.role || ""); setStateName(a.state || "");
      setCity(a.city || ""); setSchool(a.school_name || ""); setEmail(a.email || "");
      setEmailStage(a.email ? "ok" : "enter");
    }).catch(() => {});
  }, []);

  const save = async () => {
    setBusy(true); setNote("");
    try {
      const r = await fetch(`${API}/account`, withUser({
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, role, state: stateName, city, school }),
      }));
      if (!r.ok) throw new Error(String(r.status));
      onSaved && onSaved();          // back to the Settings cards (founder, 2026-08-26)
      return;
    } catch {
      setNote("Couldn't save right now — try again.");
    } finally {
      setBusy(false);
    }
  };

  if (!acct) return <div className="setwrap"><div className="fr-loading">Loading…</div></div>;
  return (
    <div className="setwrap setwrap-tight">
      <h1 className="set-title">Personal profile</h1>
      {/* Labels ABOVE the boxes (founder, 2026-08-26 — placeholder-only left fields
          ambiguous once filled; reverted same day). */}
      <label className="login-field ob-field"><span>Your name</span>
        <input type="text" value={name} placeholder="Enter your full name"
          onChange={(e) => setName(e.target.value)} /></label>
      <div className="acct-row"><span className="acct-k">Mobile</span>
        <span className="acct-v">{acct.phone || "—"}</span></div>

      {emailStage === "ok" && (
        /* Field-styled, like every other row (founder, 2026-08-26 — the confirmed
           email read too small as a bare line). */
        <label className="login-field ob-field"><span>Email</span>
          <div className="ob-email-view">
            <span>{email ? maskEmail(email) : "—"}</span>
            <button type="button" className="fr-link"
              onClick={() => { setEmailNew(""); setEmail2(""); setEmailStage("enter"); }}>
              change
            </button>
          </div>
        </label>
      )}
      {emailStage === "enter" && (
        <>
          <label className="login-field ob-field"><span>New email</span>
            <input type="email" autoComplete="off" value={emailNew}
              onChange={(e) => { setEmailNew(e.target.value); setEmailErr(""); }}
              placeholder="Enter your email" /></label>
          {EMAIL_OK(emailNew) && (
            <button type="button" className="fr-link"
              onClick={() => { setEmail2(""); setEmailStage("confirm"); }}>
              Confirm this email →
            </button>
          )}
        </>
      )}
      {emailStage === "confirm" && (
        <>
          <label className="login-field ob-field"><span>Re-enter your email</span>
            <input type="email" autoComplete="off" autoFocus value={email2}
              onChange={(e) => { setEmail2(e.target.value); setEmailErr(""); }}
              placeholder="Type it again to confirm" /></label>
          {emailErr && <p className="ob-err" role="alert">{emailErr}</p>}
          <button type="button" className="fr-link" disabled={!EMAIL_OK(email2)}
            onClick={() => {
              if (email2.trim().toLowerCase() === emailNew.trim().toLowerCase()) {
                setEmail(emailNew.trim()); setEmailStage("ok"); setEmailErr("");
              } else {
                setEmailErr("The two entries don't match — try again."); setEmail2("");
              }
            }}>
            Verify →
          </button>
        </>
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
        <input type="text" value={city} placeholder="Enter your city"
          onChange={(e) => setCity(e.target.value)} /></label>
      <label className="login-field ob-field"><span>School name (optional)</span>
        <input type="text" value={school} placeholder="Enter your school name"
          onChange={(e) => setSchool(e.target.value)} /></label>

      {/* Save never waits on the email step (founder, 2026-08-26): other fields save
          freely; a half-done email change is simply not saved until Verify completes —
          the previously confirmed email (or none) stays. */}
      <button className="primary fr-cta ob-cta" disabled={busy}
        onClick={save}>{busy ? "Saving…" : "Save"}</button>
      {emailStage !== "ok" && (
        <p className="ob-quiet">Email isn't saved until you confirm it — everything else
          saves now.</p>
      )}
      {note && <p className="ob-quiet">{note}</p>}
    </div>
  );
}

/* Subscribed details as ledger rows (founder, 2026-08-24): Subject · Stage · Class ·
 * Validity, one row each. Classes derive from the stage (the billing unit is
 * subject-STAGE, so the class list is a fact of the stage, not a choice). */
const STAGE_CLASSES = { preparatory: "3, 4 & 5", middle: "6, 7 & 8",
                        secondary: "9 (10 coming soon)" };
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const fmtValidity = (iso) => {
  const s = String(iso || "").slice(0, 10);
  const [y, m, d] = s.split("-").map(Number);
  if (!y || !m || !d) return s;
  return `${String(d).padStart(2, "0")}-${MONTHS[m - 1]}-${String(y).slice(-2)}`;
};
const scopeRows = (scope) => {
  if (scope === "*") return { subject: "All subjects", stage: "All stages", classes: "3 to 10" };
  const [subj, stage] = String(scope).split("/");
  return { subject: pretty(subj), stage: pretty(stage), classes: STAGE_CLASSES[stage] || "—" };
};

/* `view` is LIFTED to page.jsx (founder 2026-08-24: the frozen Settings bar's back
 * button is hierarchical — subview → home → origin — so the shell must know which
 * level is showing). Values: home | subscription | data | support | about. */
export default function Settings({ view, setView, onOpenProfile, onAsk, onSignOut,
                                   onSubscribe, syncTick = 0 }) {
  const [ent, setEnt] = useState(null);
  const [busy, setBusy] = useState("");        // "docx" | "pdf" | "erase" | ""
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [confirmText, setConfirmText] = useState("");
  const [failMsg, setFailMsg] = useState("");
  const [receipt, setReceipt] = useState(null);

  // Re-fetch when the shell signals a subscription change (in-app subscribe done).
  useEffect(() => { fetchEntitlement().then(setEnt); }, [syncTick]);

  const download = async (fmt) => {
    setBusy(fmt); setFailMsg("");
    try {
      const r = await fetch(`${API}/data-rights/export?format=${fmt}`, withUser());
      if (!r.ok) throw new Error(String(r.status));
      const blob = await r.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `aruvi-your-data.${fmt}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 30000);
    } catch {
      setFailMsg("Couldn't prepare your download right now. Try again in a moment.");
    } finally {
      setBusy("");
    }
  };

  const erase = async () => {
    if (confirmText.trim().toLowerCase() !== "erase") return;
    setBusy("erase"); setFailMsg("");
    try {
      const r = await fetch(`${API}/data-rights/erase`, withUser({
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ confirm: "erase" }),
      }));
      if (!r.ok) throw new Error(String(r.status));
      setReceipt(await r.json());
    } catch {
      setFailMsg("Couldn't delete the account right now. Nothing was removed — try again.");
    } finally {
      setBusy("");
    }
  };

  if (receipt) {
    return (
      <div className="setwrap">
        <p className="acct-farewell">
          Your account and all your data have been deleted.
          {Array.isArray(receipt.kept) && receipt.kept.length > 0 &&
            " Backup copies are purged within 30 days."}
        </p>
        <button className="primary acct-bye" onClick={() => onSignOut && onSignOut()}>
          Done
        </button>
      </div>
    );
  }

  // No in-content back links: the frozen Settings bar above carries the one back
  // button (hierarchical — page.jsx settingsBack).
  const back = null;

  /* ── PERSONAL PROFILE subview (founder, 2026-08-25): her account details, editable.
     Email edits use the same double-blind confirmation as acquisition. The mobile
     (her sign-in) is shown, never editable here. */
  if (view === "personal") {
    return <PersonalProfile onSaved={() => setView("home")} />;
  }

  /* ── subviews ── */
  if (view === "subscription") {
    const onTrial = ent && ent.enforced && ent.status === "trial";
    const active = ent && ent.enforced && (ent.status === "active" || ent.status === "grace");
    const lapsed = ent && ent.enforced && ent.status === "expired";
    return (
      <div className="setwrap">
        {back}
        <h1 className="set-title">Subscription &amp; billing</h1>
        <div className="set-card set-card-pad">
          {onTrial && (
            <div className="set-plan"><span className="set-pill">Free trial</span>
              <span className="set-plan-txt">{ent.trial_chapters_used} of {ent.trial_chapter_cap} chapters used</span></div>
          )}
          {active && (
            <div className="set-sub-detail">
              <div className="set-plan"><span className="set-pill set-pill-on">Subscribed</span></div>
              {(ent.scopes || []).map((scope) => {
                const r = scopeRows(scope);
                return (
                  <div key={scope} className="set-scope-block">
                    <div className="acct-row"><span className="acct-k">Subject</span><span className="acct-v">{r.subject}</span></div>
                    <div className="acct-row"><span className="acct-k">Stage</span><span className="acct-v">{r.stage}</span></div>
                    <div className="acct-row"><span className="acct-k">Class</span><span className="acct-v">{r.classes}</span></div>
                  </div>
                );
              })}
              {ent.valid_until && (
                <div className="acct-row"><span className="acct-k">Validity</span>
                  <span className="acct-v">until {fmtValidity(ent.valid_until)}</span></div>
              )}
            </div>
          )}
          {lapsed && (
            <div className="set-plan"><span className="set-pill set-pill-off">Ended</span>
              <span className="set-plan-txt">Your plans remain yours to open, export and print</span></div>
          )}
          {!(onTrial || active || lapsed) && (
            <div className="set-plan"><span className="set-plan-txt">Your plan details will appear here.</span></div>
          )}
        </div>
        {/* Subscribe from here too (founder, 2026-08-25): on trial or ended, the same
            wizard the paywall and the front door open. */}
        {(onTrial || lapsed) && onSubscribe && (
          <button className="paywall-subscribe set-subscribe" onClick={onSubscribe}>
            Subscribe
          </button>
        )}
        <p className="set-hint">Billing, payments and invoices will appear here once online
          payments open.</p>
      </div>
    );
  }

  if (view === "data") {
    return (
      <div className="setwrap">
        {back}
        <h1 className="set-title">Your data &amp; export</h1>
        <p className="set-hint">Everything you've created — your profile, notes and teaching
          progress — in one document.</p>
        <div className="set-card">
          <button className="set-row" disabled={!!busy} onClick={() => download("docx")}>
            <span className="set-lab">{busy === "docx" ? "Preparing…" : "Download as Word"}</span>
            <span className="set-chev">›</span>
          </button>
          <button className="set-row" disabled={!!busy} onClick={() => download("pdf")}>
            <span className="set-lab">{busy === "pdf" ? "Preparing…" : "Download as PDF"}</span>
            <span className="set-chev">›</span>
          </button>
        </div>
        {failMsg && <p className="acct-fail" role="alert">{failMsg}</p>}
      </div>
    );
  }

  if (view === "support") {
    return (
      <div className="setwrap">
        {back}
        <h1 className="set-title">Support</h1>
        <p className="set-hint">Email support and in-app feedback are on their way. Until
          then, Ask Aruvi (Settings › Help) answers most questions about how Aruvi works.</p>
      </div>
    );
  }

  if (view === "about") {
    return (
      <div className="setwrap">
        {back}
        <h1 className="set-title">About Aruvi</h1>
        <div className="set-card set-card-pad">
          <p className="set-plan-txt">Aruvi · Lesson Studio — preview build.<br />
            NCF 2023 aligned.</p>
        </div>
        <p className="set-hint">Version details, terms and the privacy policy will live here.</p>
      </div>
    );
  }

  /* ── home: the five cards, then the quiet rows ── */
  return (
    <div className="setwrap">
      {/* No heading here — the frozen bar above IS the one "Settings" title
          (founder: two different-size "Settings" texts were showing). */}
      {/* Two profiles, clearly told apart (founder, 2026-08-25): PERSONAL (who she is —
          account details, editable here) on top, TEACHING (what she teaches) below. */}
      <button className="set-bigcard" onClick={() => setView("personal")}>
        <span className="set-bigtext"><span className="set-biglab">Personal profile</span>
          <span className="set-bigsub">Your name, email, role and school details</span></span>
        <span className="set-chev">›</span>
      </button>
      <button className="set-bigcard" onClick={() => onOpenProfile && onOpenProfile()}>
        <span className="set-bigtext"><span className="set-biglab">Teaching profile</span>
          <span className="set-bigsub">Subjects, classes, sections and periods you teach</span></span>
        <span className="set-chev">›</span>
      </button>
      <button className="set-bigcard" onClick={() => setView("subscription")}>
        <span className="set-bigtext"><span className="set-biglab">Subscription &amp; billing</span>
          <span className="set-bigsub">Plan, billing &amp; usage</span></span>
        <span className="set-chev">›</span>
      </button>
      <button className="set-bigcard" onClick={() => setView("data")}>
        <span className="set-bigtext"><span className="set-biglab">Your data &amp; export</span>
          <span className="set-bigsub">Download your Aruvi data</span></span>
        <span className="set-chev">›</span>
      </button>
      <button className="set-bigcard" onClick={() => onAsk && onAsk()}>
        <span className="set-bigtext"><span className="set-biglab">Help</span>
          <span className="set-bigsub">Ask Aruvi guide</span></span>
        <span className="set-chev">›</span>
      </button>
      <button className="set-bigcard" onClick={() => setView("support")}>
        <span className="set-bigtext"><span className="set-biglab">Support</span>
          <span className="set-bigsub">Email &amp; feedback</span></span>
        <span className="set-chev">›</span>
      </button>
      <button className="set-bigcard" onClick={() => setView("about")}>
        <span className="set-bigtext"><span className="set-biglab">About Aruvi</span>
          <span className="set-bigsub">Version info / legal</span></span>
        <span className="set-chev">›</span>
      </button>

      <div className="set-group set-group-tail">
        <div className="set-cap">App</div>
        <div className="set-card">
          <div className="set-row set-row-static">
            <span className="set-lab">Appearance</span>
            <ThemeToggle />
          </div>
        </div>
      </div>

      <div className="set-group">
        <div className="set-cap">Account</div>
        <div className="set-card">
          <button className="set-row" onClick={() => onSignOut && onSignOut()}>
            <span className="set-lab">Log out</span>
          </button>
          <button className="set-row set-row-danger" onClick={() => setConfirmOpen(true)}>
            <span className="set-lab">Delete my account…</span>
            <span className="set-chev">›</span>
          </button>
        </div>
      </div>

      {confirmOpen && (
        <div className="acct-del">
          <p className="acct-del-warn">
            This permanently deletes your account and all your data. We suggest
            downloading your data first — it cannot be recovered afterwards. Type
            <b> erase</b> to confirm.
          </p>
          <div className="acct-del-row">
            <input className="acct-del-input" value={confirmText} autoFocus
              onChange={(e) => setConfirmText(e.target.value)}
              placeholder='Type "erase"' />
            <button className="acct-del-go"
              disabled={busy === "erase" || confirmText.trim().toLowerCase() !== "erase"}
              onClick={erase}>
              {busy === "erase" ? "Deleting…" : "Delete forever"}
            </button>
            <button className="acct-del-cancel"
              onClick={() => { setConfirmOpen(false); setConfirmText(""); }}>
              Cancel
            </button>
          </div>
        </div>
      )}

      {failMsg && <p className="acct-fail" role="alert">{failMsg}</p>}
    </div>
  );
}
