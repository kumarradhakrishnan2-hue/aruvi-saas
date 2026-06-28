"""API config — the data layer, now fully inside the SaaS repo (everything under data/).

`data/` is the single root for all data that eventually migrates to the cloud/Supabase.
Two seams live under it, kept strictly apart (see CLOUD_DATA_MODEL.md §0):

  DATA_DIR  — Bucket A: shared, read-only CONTENT (chapter summaries/mappings,
              constitutions, framework, sample saved plans). Default:
              aruvi-saas/data/content/ — a self-contained copy lifted from the prototype
              mirror so the SaaS app no longer reads from ../Project Aruvi at runtime.
              Env override: ARUVI_DATA_DIR. The cloud content / vector store replaces this.

  STATE_DIR — Bucket B: per-user / per-tenant STATE the app writes at runtime (readiness
              teaching profiles, allocation registers; saved plans + pointers next).
              Default: aruvi-saas/data/ (subfolders readiness/, allocations/, ...).
              Env override: ARUVI_STATE_DIR. Supabase Postgres replaces this folder.

Both default under data/, so a single folder is the migration unit. Paths are derived from
this file's location (never hardcoded to a machine); env vars override for other layouts.
"""
import os
from pathlib import Path

# Repo root derived from this file: api/config.py → parent.parent.
_REPO_ROOT = Path(__file__).resolve().parent.parent

# Bucket A — read-only content, self-contained inside the SaaS repo at data/content/.
_DEFAULT_DATA = str(_REPO_ROOT / "data" / "content")
DATA_DIR = os.environ.get("ARUVI_DATA_DIR", _DEFAULT_DATA)

# Bucket B — per-user/tenant state, at data/ (subfolders per state kind).
_DEFAULT_STATE = str(_REPO_ROOT / "data")
STATE_DIR = os.environ.get("ARUVI_STATE_DIR", _DEFAULT_STATE)
