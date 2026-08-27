"""API config — the data layer, laid out along the cloud/local boundary (2026-08-23).

`data/cloud/` is the literal migration unit — everything under it goes to production
(CLOUD_DATA_MODEL.md §0.5). Two seams live under it, kept strictly apart (§0):

  DATA_DIR    — Bucket A-serve: shared, read-only CONTENT the runtime reads (chapter
                mappings, framework glossaries/spine map, allocation norms, saved plans =
                canonical libraries + served-plan cache). Default:
                aruvi-saas/data/cloud/content/. Env override: ARUVI_DATA_DIR.
                The cloud object store replaces this.

  STATE_DIR   — Bucket B: per-user / per-tenant STATE the app writes at runtime
                (accounts, academic years, readiness, allocations, section state,
                prepared plans, plan archive, plan notes). Default:
                aruvi-saas/data/cloud/state/. Env override: ARUVI_STATE_DIR.
                Supabase Postgres replaces this folder.

  TESTING_DIR — the founder's testing-campaign state (api/testing_campaign.py).
                LOCAL-only, never syncs; deliberately outside data/cloud/. Default:
                aruvi-saas/data/testing/. Env override: ARUVI_TESTING_DIR.

Founder-secure authoring content (constitutions, chapter summaries) lives at
data/authoring/ and is read ONLY by the genon pipeline / chapter skill — never from
api/ or aruvi_core/ (§0.5's grep-able invariant). Paths are derived from this file's
location (never hardcoded to a machine); env vars override for other layouts.
"""
import os
from pathlib import Path

# Repo root derived from this file: api/config.py → parent.parent.
_REPO_ROOT = Path(__file__).resolve().parent.parent

# Bucket A-serve — read-only runtime content, at data/cloud/content/.
_DEFAULT_DATA = str(_REPO_ROOT / "data" / "cloud" / "content")
DATA_DIR = os.environ.get("ARUVI_DATA_DIR", _DEFAULT_DATA)

# Bucket B — per-user/tenant state, at data/cloud/state/ (subfolders per state kind).
_DEFAULT_STATE = str(_REPO_ROOT / "data" / "cloud" / "state")
STATE_DIR = os.environ.get("ARUVI_STATE_DIR", _DEFAULT_STATE)

# Testing-campaign state — local-only, outside the migration unit.
_DEFAULT_TESTING = str(_REPO_ROOT / "data" / "testing")
TESTING_DIR = os.environ.get("ARUVI_TESTING_DIR", _DEFAULT_TESTING)

# ── Entitlement (administrative architecture Step 5) ────────────────────────────
# ENTITLEMENT_ENFORCED: the gate in front of generation. Default OFF — the seam is
# fully built and tested, but daily dev is undisturbed until the founder flips it
# (set ARUVI_ENTITLEMENT_ENFORCED=1) for persona testing and at launch.
ENTITLEMENT_ENFORCED = os.environ.get("ARUVI_ENTITLEMENT_ENFORCED", "").strip().lower() in (
    "1", "true", "yes", "on")

# TRIAL_CHAPTER_CAP: the free trial covers ANY N chapters across all subject-stages,
# with unlimited re-serves per chapter (period-fitting takes several attempts — that IS
# the trial; docs/subscription_model_discussion.md §0). Counted in CHAPTERS, never
# serves. Empirical; env-overridable for the field test.
TRIAL_CHAPTER_CAP = int(os.environ.get("ARUVI_TRIAL_CHAPTERS", "3"))

# PRICE_PER_SUBJECT_STAGE (₹/year): the working figure from the subscription-model
# discussion (§0 — ₹500 pending the field test). Config, never code; the onboarding
# cart reads it via GET /entitlement.
PRICE_PER_SUBJECT_STAGE = int(os.environ.get("ARUVI_PRICE_PER_SUBJECT_STAGE", "500"))

# ── Invoicing (2026-08-26) ─────────────────────────────────────────────────────
# Aruvi is NOT GST-registered today (founder's call), so an invoice carries no GSTIN
# and no tax row — it says so in words instead, because a "₹0.00 tax" line reads like a
# rate that happens to be zero rather than a seller who does not charge it. The day
# registration happens: set ARUVI_GSTIN (and ARUVI_TAX_RATE, a percentage) and the
# document grows its tax rows. TAX_INCLUSIVE says whether PRICE_PER_SUBJECT_STAGE
# already contains the tax — the answer changes what she PAYS, so it is stated, never
# assumed.
GSTIN = os.environ.get("ARUVI_GSTIN", "").strip()
TAX_RATE = float(os.environ.get("ARUVI_TAX_RATE", "0") or 0)
TAX_INCLUSIVE = os.environ.get("ARUVI_TAX_INCLUSIVE", "1").strip().lower() in (
    "1", "true", "yes", "on")
TAX_LABEL = os.environ.get("ARUVI_TAX_LABEL", "GST").strip() or "GST"
# What the seller's books call this financial year's series. Indian FY runs April→March,
# which is also the academic-year anchor already in the code.
INVOICE_PREFIX = os.environ.get("ARUVI_INVOICE_PREFIX", "ARV").strip() or "ARV"
# ★ Each financial year's series OPENS here, not at 1 (founder, 2026-08-26). The number
# is the one part of an invoice a customer can read volume from, and "0001" tells an
# early teacher she is the first sale Aruvi ever made. An offset, not a fiction: the
# series is still gapless and still counts real invoices.
INVOICE_START = int(os.environ.get("ARUVI_INVOICE_START", "7834"))

# ── Outbound mail (administrative architecture Step 6 — the Notifier port) ──────
# Credentials NEVER live in the repo. With SMTP_HOST/USER/PASSWORD all set, main.py
# installs SmtpNotifier and confirmations really send; otherwise FileNotifier writes
# them to STATE_DIR/outbox/ and nothing leaves the machine. For Gmail, PASSWORD must
# be an APP PASSWORD (2-step verification on) — the account password is refused.
SMTP_HOST = os.environ.get("ARUVI_SMTP_HOST", "").strip()
SMTP_PORT = int(os.environ.get("ARUVI_SMTP_PORT", "587"))
SMTP_USER = os.environ.get("ARUVI_SMTP_USER", "").strip()
SMTP_PASSWORD = os.environ.get("ARUVI_SMTP_PASSWORD", "")
# The address teachers see as sender / reply-to. The founder's own mail id for now
# (founder, 2026-08-26); a support@ address replaces it without touching code.
MAIL_FROM = os.environ.get("ARUVI_MAIL_FROM", "").strip() or SMTP_USER or "kumar.radhakrishnan2@gmail.com"
MAIL_REPLY_TO = os.environ.get("ARUVI_MAIL_REPLY_TO", "").strip() or MAIL_FROM
# Send the founder a copy of every subscription confirmation (his own sales log).
MAIL_BCC_FOUNDER = os.environ.get("ARUVI_MAIL_BCC_FOUNDER", "1").strip().lower() in (
    "1", "true", "yes", "on")

# ── Support (2026-08-27) ───────────────────────────────────────────────────────
# Email is the only channel, so the acknowledgement carries the whole weight of "your
# message arrived and it is somebody's job now". The reference is the handle both sides
# use afterwards; SUPPORT_START is where the series opens (see support_repository_file
# for why it is not 1). SUPPORT_REPLY_DAYS is the promise the screen and the mail BOTH
# make — one value, so they cannot drift apart and leave the teacher with two answers.
SUPPORT_PREFIX = os.environ.get("ARUVI_SUPPORT_PREFIX", "ARV-S").strip() or "ARV-S"
SUPPORT_START = int(os.environ.get("ARUVI_SUPPORT_START", "742"))
SUPPORT_REPLY_DAYS = int(os.environ.get("ARUVI_SUPPORT_REPLY_DAYS", "2"))
# Billing questions get the firmer promise: money carries a different anxiety, and a
# teacher who thinks she has paid twice should not wait as long as one with a layout
# question.
SUPPORT_BILLING_REPLY_DAYS = int(os.environ.get("ARUVI_SUPPORT_BILLING_REPLY_DAYS", "1"))

# ── Academic-year cutover (administrative architecture Step 2) ──────────────────
# CUTOVER_MONTH_DAY: the date each year on which Aruvi starts OFFERING the new academic
# year. June 1 by default — Indian schools reopen late May/early June, and a teacher
# still finishing a chapter in April must not be cut over out from under her. Config,
# never code: boards differ and the founder will move this after the first June.
CUTOVER_MONTH_DAY = os.environ.get("ARUVI_CUTOVER_MONTH_DAY", "06-01").strip()

# SIMULATED_TODAY: pretend it is this date (ISO, e.g. "2027-06-01"). ★ TESTING ONLY —
# cutover's whole behaviour hangs on the calendar, and waiting until June to find out it
# is wrong is not a test strategy. Every date decision in api/main.py goes through
# _today(), so setting this makes the WHOLE system agree about what day it is
# (entitlement expiry included) rather than only the piece under test. Unset in
# production; the server logs a warning when it is set.
SIMULATED_TODAY = os.environ.get("ARUVI_TODAY", "").strip()
