"""The erasure consent log — the ONE record that deliberately outlives an erasure.

Everything else about a teacher is destroyed by DataRightsService.erase(). That is the
point of erasure, and it is why, until now, an erased account left **no evidence that
she had ever confirmed it** — an obvious gap the moment anyone disputes a deletion, and
one a data-protection regime expects to be closed.

So this log lives OUTSIDE the erase walk (`STATE_DIR/erasure_log/`, never traversed by
data_rights_service_file) and holds the minimum that makes the record meaningful:

    tenant_id · user_id · confirmed_downloaded · confirmed_at · erased_at · counts

**It carries the identifier and nothing else** — no name, no email, no school, no
content. ★ The identifier IS personal data: `user_id` is her sign-in MOBILE NUMBER
(account_id == mobile, Login.jsx), and calling it "no personal data" was wrong
(privacy_policy_considerations.md §3.5). The founder's decision (2026-09-04) was to KEEP
the number rather than hash it, and to SAY so: the Privacy Notice §7 and the erasure
receipt's `_KEPT` both name this record, plainly, as one of the things that survive.
Writing more here would quietly reintroduce the very data the teacher asked to have
destroyed.

Append-only, one file per tenant so a school's deletions sit together (founder,
2026-08-26: "digital confirmation to be captured tenant/user wise").
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


def _slug(s: str) -> str:
    """Filesystem-safe slug for a tenant/user id (defends against path traversal)."""
    s = str(s).strip() or "local"
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s).strip("-") or "local"


class ErasureLogFileImpl:
    """Append-only consent + receipt log for account deletions."""

    def __init__(self, data_dir: str):
        """
        Args:
            data_dir: Base directory (ARUVI_STATE_DIR). The erasure_log/ folder lives
                here but is NOT part of the erase traversal — that is the whole point.
        """
        self.log_dir = Path(data_dir) / "erasure_log"

    def _path(self, tenant_id: str) -> Path:
        return self.log_dir / f"{_slug(tenant_id)}.json"

    # NOTE: Optional[...], never `X | None` — the founder's Mac runs Python 3.9, where
    # PEP 604 unions are a TypeError at import. Keep every annotation 3.9-safe.
    def record(self, tenant_id: str, user_id: str, confirmed_downloaded: bool,
               erased: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
        """Append one deletion record and return it. Never raises: a logging failure
        must not block a teacher's right to be forgotten — the erasure is the promise,
        the log is the evidence, and the promise wins if they ever conflict."""
        entry = {
            "tenant_id": _slug(tenant_id),
            "user_id": _slug(user_id),
            "confirmed_downloaded": bool(confirmed_downloaded),
            "confirmed_at": datetime.now(timezone.utc).isoformat(),
            "erased_counts": dict(erased or {}),
        }
        try:
            self.log_dir.mkdir(parents=True, exist_ok=True)
            path = self._path(tenant_id)
            existing: List[Dict[str, Any]] = []
            if path.exists():
                try:
                    with open(path, "r") as f:
                        existing = json.load(f) or []
                except (json.JSONDecodeError, IOError):
                    existing = []          # a corrupt log must not block a deletion
            existing.append(entry)
            with open(path, "w") as f:
                json.dump(existing, f, indent=2)
            entry["logged"] = True
        except Exception:                  # noqa: BLE001 — see the docstring
            entry["logged"] = False
        return entry

    def for_tenant(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Every deletion recorded under this tenant, oldest first. Empty when none."""
        path = self._path(tenant_id)
        if not path.exists():
            return []
        try:
            with open(path, "r") as f:
                return json.load(f) or []
        except (json.JSONDecodeError, IOError):
            return []
