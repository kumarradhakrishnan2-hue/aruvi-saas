"""Document-backend implementation (file or Postgres — Track C, 2026-09-09) of PreparedPlansRepository.

Persists which saved plans a teacher has actually PREPARED as JSON at
ARUVI_STATE_DIR/prepared_plans/{tenant_id}/{user_id}/{year_id}/prepared.json, shaped as

    { "english/vi/ch_04_....json": {"at": "2026-07-05T09:12:00+00:00", "periods": 22}, ... }

i.e. {plan_key: {at: prepared_at_iso, periods: chosen_periods|null}}. Older registers stored a
bare ISO string per key ({plan_key: prepared_at_iso}); both shapes are read, and a legacy string
is upgraded to the record form the next time that plan is marked. The plan_key is the frontend's
`${subjectSlug}/${gradeSlug}/${filename}` — the same identity used to LOAD the plan and to key
the archive — so the prepared flag binds to the plan without copying any of its content.

Why this exists: live generation is deferred, so the saved-plan library is shared read-only
CONTENT (Bucket A) and looks identical for every teacher. Listing it directly makes My Lessons
show every sample plan to everyone, which breaks the "assets you've gathered over time"
premise. This register is the per-tenant STATE (Bucket B) that records the teacher's OWN
preparations, so /plans can flag (and the client can filter to) only her work. First-run marks
its chapter on activation; the everyday PrepareLesson flow appends on each generate.

Every store is keyed by tenant_id + user_id + year_id (administrative_architecture.md
Step 1, 2026-08-22): what she prepared belongs to the year she prepared it in — the new
year's My Lessons starts fresh, the old year's stays openable from its folder. The API
layer resolves which year is current; this adapter just addresses by it. With no auth yet
tenant_id == user_id (the X-Aruvi-User value); the partner's cloud adapter replaces this
file (behind the same port) with a `prepared_at` column on the saved-plan row — or, once
live generation lands, the mere existence of the teacher's own generated plan row.
"""
from datetime import datetime, timezone
from typing import Any, Dict

from aruvi_core.ports import PreparedPlansRepository
from aruvi_core.adapters.document_backend import as_backend, slug as _slug




class PreparedPlansRepositoryFileImpl(PreparedPlansRepository):
    """File-based per-tenant prepared-plans store."""

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
        return f"prepared_plans/{_slug(tenant_id)}/{_slug(user_id)}/{_slug(year_id)}/prepared.json"

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

    def load_all(self, tenant_id: str, user_id: str, year_id: str) -> Dict[str, Any]:
        """All prepared plan keys for this teacher's year. Value is either a legacy prepared_at
        ISO string, or a record {"at": iso, "periods": int|None} — callers must handle both."""
        return self._read(tenant_id, user_id, year_id)

    def mark(self, tenant_id: str, user_id: str, year_id: str, plan_key: str, periods=None,
             source_year=None) -> None:
        """Record one plan as prepared. prepared_at is set once (idempotent); `periods` (the
        teacher's chosen period count) is stored as a record and UPDATED on every call so a
        re-prepare tracks the latest generation. Legacy string values are upgraded in place.

        `source_year` (2026-08-26) records that this plan came FROM an earlier academic year —
        she brought last June's chapter forward rather than generating it fresh. It is
        provenance, not a copy: the plan asset is the same either way, but a teacher looking
        at a section card deserves to know she is teaching last year's version. Sticky once
        set: re-preparing does not silently erase where a plan came from, and only a genuinely
        NEW generation (which passes no source_year for a plan that never had one) leaves it
        absent."""
        with self._locked(tenant_id, user_id, year_id):
            data = self._read(tenant_id, user_id, year_id)
            existing = data.get(plan_key)
            # Preserve the original prepared_at across shapes (str = legacy, dict = new record).
            cur_source = None
            if isinstance(existing, dict):
                at = existing.get("at") or datetime.now(timezone.utc).isoformat()
                cur_periods = existing.get("periods")
                cur_source = existing.get("source_year")
            elif isinstance(existing, str):
                at = existing
                cur_periods = None
            else:
                at = datetime.now(timezone.utc).isoformat()
                cur_periods = None
            new_periods = periods if periods is not None else cur_periods
            record = {"at": at, "periods": new_periods}
            new_source = source_year if source_year is not None else cur_source
            if new_source:
                record["source_year"] = new_source
            # Only write when something actually changed (keeps the register churn-free / idempotent).
            if existing != record:
                data[plan_key] = record
                self._write(tenant_id, user_id, year_id, data)

    def unmark(self, tenant_id: str, user_id: str, year_id: str, plan_key: str) -> None:
        """Forget that this plan was prepared (2026-08-26, the trial purge). No-op when
        absent. Removes the RECORD only — the saved plan is shared library content, not
        hers to delete, and another teacher may be served the same file tomorrow."""
        with self._locked(tenant_id, user_id, year_id):
            data = self._read(tenant_id, user_id, year_id)
            if plan_key in data:
                del data[plan_key]
                self._write(tenant_id, user_id, year_id, data)
