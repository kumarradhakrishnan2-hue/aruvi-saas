"""File-based implementation of PreparedPlansRepository.

Persists which saved plans a teacher has actually PREPARED as JSON at
ARUVI_STATE_DIR/prepared_plans/{tenant_id}/{user_id}/prepared.json, shaped as

    { "english/vi/ch_04_....json": "2026-07-05T09:12:00+00:00", ... }

i.e. {plan_key: prepared_at_iso}. The plan_key is the frontend's
`${subjectSlug}/${gradeSlug}/${filename}` — the same identity used to LOAD the plan and to key
the archive — so the prepared flag binds to the plan without copying any of its content.

Why this exists: live generation is deferred, so the saved-plan library is shared read-only
CONTENT (Bucket A) and looks identical for every teacher. Listing it directly makes My Lessons
show every sample plan to everyone, which breaks the "assets you've gathered over time"
premise. This register is the per-tenant STATE (Bucket B) that records the teacher's OWN
preparations, so /plans can flag (and the client can filter to) only her work. First-run marks
its chapter on activation; the everyday PrepareLesson flow appends on each generate.

Every store is keyed by tenant_id + user_id. With no auth yet both stub to the same
X-Aruvi-User value; Phase 4 swaps the values from the Supabase auth token, no schema change,
and this file adapter is replaced (behind the same port) by a `prepared_at` column on the
saved-plan row — or, once live generation lands, by the mere existence of the teacher's own
generated plan row.
"""
import json
import os
import tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from aruvi_core.ports import PreparedPlansRepository


def _slug(s: str) -> str:
    """Filesystem-safe slug for a tenant/user id (defends against path traversal)."""
    s = str(s).strip() or "local"
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s).strip("-") or "local"


class PreparedPlansRepositoryFileImpl(PreparedPlansRepository):
    """File-based per-tenant prepared-plans store."""

    def __init__(self, data_dir: str):
        """
        Args:
            data_dir: Base directory where the prepared_plans/ folder lives (e.g. ARUVI_STATE_DIR).
        """
        self.data_dir = Path(data_dir)
        self.base_dir = self.data_dir / "prepared_plans"
        # Serialize read-modify-write of the shared prepared.json within this process (FastAPI
        # runs handlers on a threadpool). One module-level repo instance → process-wide lock; a
        # multi-instance deployment moves this to the DB row-lock at Phase 4.
        self._lock = threading.Lock()

    def _path(self, tenant_id: str, user_id: str) -> Path:
        return self.base_dir / _slug(tenant_id) / _slug(user_id) / "prepared.json"

    def _read(self, tenant_id: str, user_id: str) -> Dict[str, Any]:
        path = self._path(tenant_id, user_id)
        if not path.exists():
            return {}
        try:
            with open(path, "r") as f:
                return json.load(f) or {}
        except (IOError, json.JSONDecodeError):
            return {}

    def _write(self, tenant_id: str, user_id: str, data: Dict[str, Any]) -> None:
        # ATOMIC write: temp file in the same dir, then os.replace() over the target (atomic on
        # POSIX/Windows), so a reader always sees the complete old or complete new file — never a
        # half-written one — and concurrent writers can't interleave into corrupt JSON.
        path = self._path(tenant_id, user_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = None
        try:
            fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".prepared-", suffix=".tmp")
            with os.fdopen(fd, "w") as f:
                json.dump(data, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, path)
            tmp = None
        except IOError as e:
            raise ValueError(f"Failed to save prepared-plans register to {path}: {e}")
        finally:
            if tmp is not None and os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except OSError:
                    pass

    def load_all(self, tenant_id: str, user_id: str) -> Dict[str, str]:
        """All prepared plan keys for this teacher: {plan_key: prepared_at_iso}."""
        return self._read(tenant_id, user_id)

    def mark(self, tenant_id: str, user_id: str, plan_key: str) -> None:
        """Record one plan as prepared. Idempotent — keeps the original prepared_at if set."""
        with self._lock:
            data = self._read(tenant_id, user_id)
            if plan_key not in data:
                data[plan_key] = datetime.now(timezone.utc).isoformat()
                self._write(tenant_id, user_id, data)
