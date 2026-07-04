"""File-based implementation of PlanArchiveRepository.

Persists which saved plans a teacher has archived as JSON at
ARUVI_STATE_DIR/plan_archive/{tenant_id}/{user_id}/archive.json, shaped as

    { "science/vi/ch_03_....json": "2026-07-04T09:12:00+00:00", ... }

i.e. {plan_key: archived_at_iso}. The plan_key is the frontend's
`${subjectSlug}/${gradeSlug}/${filename}` — the same identity used to LOAD the plan — so the
archive flag binds to the plan without copying any of its content. This is Bucket-B STATE
(the plan asset stays put as shared read-only content; only the flag is per-tenant), so it
lives under STATE_DIR alongside readiness / allocations / section_state.

There is deliberately NO hard delete of plans anywhere: archiving is reversible (restore drops
the key), and the plan's frozen identity means every back-reference (LU pointer, notes, section
attachment) survives untouched. See ports.PlanArchiveRepository for the full rationale.

Every store is keyed by tenant_id + user_id. With no auth yet both stub to the same
X-Aruvi-User value; Phase 4 swaps the values from the Supabase auth token, no schema change,
and this file adapter is replaced (behind the same port) by an `archived_at` column on the
plan row / a small `plan_archive` table.
"""
import json
import os
import tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from aruvi_core.ports import PlanArchiveRepository


def _slug(s: str) -> str:
    """Filesystem-safe slug for a tenant/user id (defends against path traversal)."""
    s = str(s).strip() or "local"
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s).strip("-") or "local"


class PlanArchiveRepositoryFileImpl(PlanArchiveRepository):
    """File-based per-tenant archived-plans store."""

    def __init__(self, data_dir: str):
        """
        Args:
            data_dir: Base directory where the plan_archive/ folder lives (e.g. ARUVI_STATE_DIR).
        """
        self.data_dir = Path(data_dir)
        self.base_dir = self.data_dir / "plan_archive"
        # Serialize read-modify-write of the shared archive.json within this process (FastAPI
        # runs handlers on a threadpool). One module-level repo instance → process-wide lock; a
        # multi-instance deployment moves this to the DB row-lock at Phase 4.
        self._lock = threading.Lock()

    def _path(self, tenant_id: str, user_id: str) -> Path:
        return self.base_dir / _slug(tenant_id) / _slug(user_id) / "archive.json"

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
            fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".archive-", suffix=".tmp")
            with os.fdopen(fd, "w") as f:
                json.dump(data, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, path)
            tmp = None
        except IOError as e:
            raise ValueError(f"Failed to save plan archive to {path}: {e}")
        finally:
            if tmp is not None and os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except OSError:
                    pass

    def load_all(self, tenant_id: str, user_id: str) -> Dict[str, str]:
        """All archived plan keys for this teacher: {plan_key: archived_at_iso}."""
        return self._read(tenant_id, user_id)

    def archive(self, tenant_id: str, user_id: str, plan_key: str) -> None:
        """Mark one plan archived. Idempotent — keeps the original archived_at if already set."""
        with self._lock:
            data = self._read(tenant_id, user_id)
            if plan_key not in data:
                data[plan_key] = datetime.now(timezone.utc).isoformat()
                self._write(tenant_id, user_id, data)

    def restore(self, tenant_id: str, user_id: str, plan_key: str) -> None:
        """Un-archive one plan. No-op if absent."""
        with self._lock:
            data = self._read(tenant_id, user_id)
            if plan_key in data:
                data.pop(plan_key, None)
                self._write(tenant_id, user_id, data)
