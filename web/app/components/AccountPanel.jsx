"use client";
import { useEffect, useState } from "react";
import { API, withUser, fetchEntitlement, pretty } from "../lib/format";

/* ── Your account — the settings-gear surface (Step 6 slice 2, founder 2026-08-24) ──
 *
 * Rendered below the teaching profile in the gear area. Three blocks:
 *   1. SUBSCRIPTION — plan/status/scope/counter from GET /entitlement, in plain words.
 *      Hidden entirely while the gate is off (dev): a subscription card describing
 *      rules that aren't enforced would be a lie.
 *   2. YOUR DATA — download everything as Word or PDF (the Step-4 export). A plain
 *      <a href> cannot carry the X-Aruvi-User header, so the download is a fetch →
 *      blob → anchor-click; on iPhone Safari this opens the file viewer, which is the
 *      platform's normal save path.
 *   3. DELETE MY ACCOUNT — the Step-4 erase, and Apple 5.1.1(v)'s required in-app
 *      deletion. Typed confirmation ("erase") mirrors the API's own guard — the UI
 *      never makes destruction one tap. On success: show the receipt's essentials,
 *      then sign out (the account is gone; the ID simply starts fresh if reused).
 *
 * Data-rights actions are NEVER gated on subscription state (§2.5) — this panel works
 * identically for trial, active, and lapsed teachers. */

const scopeLabel = (s) =>
  s === "*" ? "All subjects" : pretty(String(s).replace("/", " · "));

export default function AccountPanel({ onSignOut }) {
  const [ent, setEnt] = useState(null);
  const [busy, setBusy] = useState("");        // "docx" | "pdf" | "erase" | ""
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [confirmText, setConfirmText] = useState("");
  const [failMsg, setFailMsg] = useState("");
  const [receipt, setReceipt] = useState(null); // erase result → farewell screen

  useEffect(() => { fetchEntitlement().then(setEnt); }, []);

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

  /* Post-erase farewell: the account no longer exists, so the only exit is sign-out.
   * Shown INSTEAD of the panel — there is no account left to describe. */
  if (receipt) {
    return (
      <div className="acct">
        <div className="kicker kicker-soft">Your account</div>
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

  const onTrial = ent && ent.enforced && ent.status === "trial";
  const active = ent && ent.enforced && (ent.status === "active" || ent.status === "grace");
  const lapsed = ent && ent.enforced && ent.status === "expired";

  return (
    <div className="acct">
      <div className="kicker kicker-soft">Your account</div>

      {/* 1 · Subscription — only when the gate is live (see header note). */}
      {onTrial && (
        <div className="acct-row">
          <span className="acct-k">Plan</span>
          <span className="acct-v">
            Free trial — {ent.trial_chapters_used} of {ent.trial_chapter_cap} chapters used
          </span>
        </div>
      )}
      {active && (
        <>
          <div className="acct-row">
            <span className="acct-k">Plan</span>
            <span className="acct-v">Subscribed · {(ent.scopes || []).map(scopeLabel).join(", ") || "—"}</span>
          </div>
          {ent.valid_until && (
            <div className="acct-row">
              <span className="acct-k">Valid until</span>
              <span className="acct-v">{String(ent.valid_until).slice(0, 10)}</span>
            </div>
          )}
        </>
      )}
      {lapsed && (
        <div className="acct-row">
          <span className="acct-k">Plan</span>
          <span className="acct-v">
            Subscription ended — your plans remain yours to open, export and print
          </span>
        </div>
      )}

      {/* 2 · Your data */}
      <p className="acct-blurb">
        Everything you've created — your profile, notes and teaching progress — in one
        document.
      </p>
      <div className="acct-btns">
        <button className="acct-dl" disabled={!!busy} onClick={() => download("docx")}>
          {busy === "docx" ? "Preparing…" : "Download my data (Word)"}
        </button>
        <button className="acct-dl" disabled={!!busy} onClick={() => download("pdf")}>
          {busy === "pdf" ? "Preparing…" : "Download my data (PDF)"}
        </button>
      </div>

      {/* 3 · Delete account — typed confirmation, mirrors the API's own guard. */}
      {!confirmOpen ? (
        <button className="acct-del-open" onClick={() => setConfirmOpen(true)}>
          Delete my account…
        </button>
      ) : (
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
