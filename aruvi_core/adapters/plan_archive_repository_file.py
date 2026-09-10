"""Document-backend implementation (file or Postgres — Track C, 2026-09-09) of PlanArchiveRepository.

Persists which saved plans a teacher has archived as JSON at
ARUVI_STATE_DIR/plan_archive/{tenant_id}/{user_id}/{year_id}/archive.json, shaped as

    { "science/vi/ch_03_....json": "2026-07-04T09:12:00+00:00", ... }

i.e. {plan_key: archived_at_iso}. The plan_key is the frontend's
`${subjectSlug}/${gradeSlug}/${filename}` — the same identity used to LOAD the plan — so the
archive flag binds to the plan without copying any of its content. This is Bucket-B STATE
(the plan asset stays put as shared read-only content; only the flag is per-tenant), so it
lives under STATE_DIR alongside readiness / allocations / section_state.

There is deliberately NO hard delete of plans anywhere: archiving is reversible (restore drops
the key), and the plan's frozen identity means every back-reference (LU pointer, notes, section
attachment) survives untouched. See ports.PlanArchiveRepository for the full rationale.

Every store is keyed by tenant_id + user_id + year_id (administrative_architecture.md
Step 1, 2026-08-22): My Lessons folds each closing year into its own archive folder, so the
flag lives inside the year it was set in. The API layer resolves which year is current;
this adapter just addresses by it. With no auth yet tenant_id == user_id (the X-Aruvi-User
value); the partner's cloud adapter replaces this file (behind the same port) with an
`archived_at` column on the plan row / a small `plan_archive` table.
"""
from datetime import datetime, timezone
from typing import Any, Dict

from aruvi_core.ports import PlanArchiveRepository
from aruvi_core.adapters.document_backend import as_backend, slug as _slug




class PlanArchiveRepositoryFileImpl(PlanArchiveRepository):
    """File-based per-tenant archived-plans store."""

    def __init__(self, data_dir):
        """
        Args:
            data_dir: a DocumentBackend, or a directory (→ FileBackend at that root, e.g.
                      ARUVI_STATE_DIR — every existing call site and test). Read-modify-
                      write is serialised per DOCUMENT through backend.lock(): a thread
                      lock on files (one process, as before) and additionally a
                      transaction-scoped advisory lock on Postgres, so two API instances
                      cannot lose each other's update (the DB row-lock the file version
                      always said was "later").
        """
        self.backend = as_backend(data_dir)

    def _key(self, tenant_id: str, user_id: str, year_id: str) -> str:
        return f"plan_archive/{_slug(tenant_id)}/{_slug(user_id)}/{_slug(year_id)}/archive.json"

    # File-backend diagnostic (tests inspect the raw document on disk).
    def _path(self, tenant_id: str, user_id: str, year_id: str):
        return self.backend._path(self._key(tenant_id, user_id, year_id))

    def _locked(self, tenant_id: str, user_id: str, year_id: str):
        return self.backend.lock(self._key(tenant_id, user_id, year_id))

    def _read(self, tenant_id: str, user_id: str, year_id: str) -> Dict[str, Any]:
        """The whole document, or {} when absent. Corruption is self-healed by the file
        backend (raw_decode keeps the valid leading object — the 2026-07-03 rule)."""
        data = self.backend.get_json(self._key(tenant_id, user_id, year_id))
        return data if isinstance(data, dict) else {}

    def _write(self, tenant_id: str, user_id: str, year_id: str, data: Dict[str, Any]) -> None:
        self.backend.put_json(self._key(tenant_id, user_id, year_id), data)

    def load_all(self, tenant_id: str, user_id: str, year_id: str) -> Dict[str, str]:
        """All archived plan keys for this teacher's year: {plan_key: archived_at_iso}."""
        return self._read(tenant_id, user_id, year_id)

    def archive(self, tenant_id: str, user_id: str, year_id: str, plan_key: str) -> None:
        """Mark one plan archived. Idempotent — keeps the original archived_at if already set."""
        with self._locked(tenant_id, user_id, year_id):
            data = self._read(tenant_id, user_id, year_id)
            if plan_key not in data:
                data[plan_key] = datetime.now(timezone.utc).isoformat()
                self._write(tenant_id, user_id, year_id, data)

    def restore(self, tenant_id: str, user_id: str, year_id: str, plan_key: str) -> None:
        """Un-archive one plan. No-op if absent."""
        with self._locked(tenant_id, user_id, year_id):
            data = self._read(tenant_id, user_id, year_id)
            if plan_key in data:
                data.pop(plan_key, None)
                self._write(tenant_id, user_id, year_id, data)
