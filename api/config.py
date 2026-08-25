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
