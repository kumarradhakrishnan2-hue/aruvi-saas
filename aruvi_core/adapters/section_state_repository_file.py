"""Document-backend implementation (file or Postgres — Track C, 2026-09-09) of SectionStateRepository.

Persists per-section teaching execution state as JSON at
ARUVI_DATA_DIR/section_state/{tenant_id}/{user_id}/{year_id}/state.json, shaped as

    { section_key: {chapter, unit_index, done, bookmark_unit, bookmark_phase, updated_at}, ... }

This is the Bucket-B "teaching pointer" (CLOUD_DATA_MODEL.md §2.4) lifted OFF browser
localStorage so a teacher's tracking + progress follow her across devices. localStorage
stays a client-side optimistic cache; this file is authoritative on load/reconcile. A
Supabase adapter (the `lesson_pointer` table extended with `chapter` + `done`) swaps in
later behind the same SectionStateRepository port with no change to the API or the app.

Every store is keyed by tenant_id + user_id + year_id (administrative_architecture.md
Step 1, 2026-08-22): pointers, done flags and bookmarks are the most year-bound state
there is — the teacher-side cutover clears them by opening a new year folder, never by
rewriting rows. The API layer resolves which year is current; this adapter just
addresses by it. With no auth yet tenant_id == user_id (the X-Aruvi-User value).

save_one is a full per-section snapshot upsert (the client always sends the complete
current state for a section), so there is no field-level merge to reason about.
"""
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from aruvi_core.ports import SectionState, SectionStateRepository
from aruvi_core.adapters.document_backend import as_backend, slug as _slug




class SectionStateRepositoryFileImpl(SectionStateRepository):
    """File-based per-section teaching-state store."""

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
        return f"section_state/{_slug(tenant_id)}/{_slug(user_id)}/{_slug(year_id)}/state.json"

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

    def load_all(self, tenant_id: str, user_id: str, year_id: str) -> Dict[str, SectionState]:
        """All tracked sections for this teacher's year. Empty dict if none."""
        return self._read(tenant_id, user_id, year_id)

    def save_one(self, tenant_id: str, user_id: str, year_id: str, section_key: str,
                 chapter: str, unit_index: Optional[int], done: bool,
                 bookmark_unit: Optional[int] = None,
                 bookmark_phase: Optional[int] = None) -> None:
        """Upsert one section's execution state (full snapshot for that section).

        `bookmark_unit`/`bookmark_phase` (0-based, both None when unset) carry the teacher's
        phase place-marker on the same row — default None so existing callers/tests that don't
        pass them store no bookmark, unchanged."""
        with self._locked(tenant_id, user_id, year_id):
            data = self._read(tenant_id, user_id, year_id)
            data[section_key] = {
                "chapter": chapter,
                "unit_index": unit_index,
                "done": bool(done),
                "bookmark_unit": bookmark_unit,
                "bookmark_phase": bookmark_phase,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            self._write(tenant_id, user_id, year_id, data)

    def delete_one(self, tenant_id: str, user_id: str, year_id: str, section_key: str) -> None:
        """Remove one section's state (untrack). No-op if absent."""
        with self._locked(tenant_id, user_id, year_id):
            data = self._read(tenant_id, user_id, year_id)
            if section_key in data:
                data.pop(section_key, None)
                self._write(tenant_id, user_id, year_id, data)

    def clear_all(self, tenant_id: str, user_id: str, year_id: str) -> None:
        """Erase ALL section teaching-state for this teacher's year. Used by the 'start setup
        over' profile reset (DELETE /readiness) so stale bindings can't resurrect into a
        freshly rebuilt profile — otherwise a section key reused by the new profile inherits
        the old chapter + pointer. No-op if nothing is stored."""
        with self._locked(tenant_id, user_id, year_id):
            # (the file backend writes an empty map where unlink is forbidden)
            self.backend.delete(self._key(tenant_id, user_id, year_id))
