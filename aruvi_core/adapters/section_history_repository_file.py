"""Document-backend implementation (file or Postgres — Track C, 2026-09-09) of SectionHistoryRepository.

Persists each section's ledger of chapters already taught as JSON at
ARUVI_STATE_DIR/section_history/{tenant_id}/{user_id}/{year_id}/history.json, shaped as

    { section_key: { chapter_file: {file, chapter_number, chapter_title, status,
                                    units_done, total_units, ts}, ... }, ... }

This is the server mirror `web/app/lib/sectionHistory.js` was written owing (its own
header: "localStorage only for now… when Phase 4 lands, this gains a server mirror
exactly like sectionState.js"). Without it a teacher on a phone and a laptop keeps two
disagreeing accounts of what each class has been taught — the exact split-brain
sectionState.js was built to end. localStorage stays a synchronous optimistic cache;
this file is authoritative on load/reconcile.

★ THE ONE DIFFERENCE FROM section_state_repository_file: writes MERGE, they do not
  replace. Section state is CURRENT state, so a per-section snapshot is right — the last
  writer holds the truth. History is CUMULATIVE, so a whole-map write from a device that
  has never seen another device's rows would DELETE them. Every entry is upserted under
  its own chapter file with latest-`ts`-wins, which converges from any device in any
  order. That also makes every write idempotent: replaying a push changes nothing.

Year-scoped like the pointer (administrative_architecture.md Step 1): a new academic year
is a new cohort, and last year's trail belongs to last year. The API layer resolves which
year is current; this adapter just addresses by it. With no auth yet tenant_id == user_id
(the X-Aruvi-User value).
"""
from typing import Any, Dict, List

from aruvi_core.ports import SectionHistoryEntry, SectionHistoryRepository
from aruvi_core.adapters.document_backend import as_backend, slug as _slug




def _ts_of(entry: Dict[str, Any]) -> int:
    """An entry's timestamp as a comparable int; 0 when absent or unparseable.

    Never raises: a malformed `ts` from an old client must lose the comparison, not fail
    the write. Losing means the stored row is kept, which is the safe direction for a
    ledger — a merge may not destroy what it cannot prove is stale."""
    try:
        return int(entry.get("ts") or 0)
    except (TypeError, ValueError):
        return 0


class SectionHistoryRepositoryFileImpl(SectionHistoryRepository):
    """File-based per-section chapter-history store."""

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
        return f"section_history/{_slug(tenant_id)}/{_slug(user_id)}/{_slug(year_id)}/history.json"

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

    def load_all(self, tenant_id: str, user_id: str,
                 year_id: str) -> Dict[str, Dict[str, SectionHistoryEntry]]:
        """The whole ledger for this teacher's year: {section_key: {file: entry}}."""
        return self._read(tenant_id, user_id, year_id)

    def record(self, tenant_id: str, user_id: str, year_id: str, section_key: str,
               entries: List[SectionHistoryEntry]) -> None:
        """Merge entries into one section's ledger, each keyed by its own `file`,
        latest `ts` winning. Entries without a `file` are skipped — a row with no chapter
        identity has nowhere to live and would silently accumulate under an empty key."""
        if not section_key or not entries:
            return
        with self._locked(tenant_id, user_id, year_id):
            data = self._read(tenant_id, user_id, year_id)
            rows = dict(data.get(section_key) or {})
            changed = False
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                fname = str(entry.get("file") or "").strip()
                status = str(entry.get("status") or "").strip()
                if not fname or not status:
                    continue
                incoming = {
                    "file": fname,
                    "chapter_number": entry.get("chapter_number"),
                    "chapter_title": entry.get("chapter_title") or "",
                    "status": status,
                    "units_done": entry.get("units_done"),
                    "total_units": entry.get("total_units"),
                    "ts": _ts_of(entry),
                }
                existing = rows.get(fname)
                # Latest wins; a tie keeps the stored row (a re-push of the same entry is
                # then a true no-op, so an offline device replaying its queue cannot churn
                # the file).
                if existing is not None and _ts_of(existing) >= incoming["ts"]:
                    continue
                rows[fname] = incoming
                changed = True
            if not changed:
                return
            data[section_key] = rows
            self._write(tenant_id, user_id, year_id, data)

    def delete_section(self, tenant_id: str, user_id: str, year_id: str,
                       section_key: str) -> None:
        """Drop one section's whole ledger (the section left the profile). No-op if absent.

        ⚠️ Deliberately NOT reachable from untrack: a chapter set aside keeps its row (see
        sectionHistory.js — "untracking a chapter must not erase the record that it was once
        taught"). This exists only for the two sites that already delete the section's
        POINTER, where the section itself is gone."""
        with self._locked(tenant_id, user_id, year_id):
            data = self._read(tenant_id, user_id, year_id)
            if section_key in data:
                data.pop(section_key, None)
                self._write(tenant_id, user_id, year_id, data)

    def clear_all(self, tenant_id: str, user_id: str, year_id: str) -> None:
        """Erase this teacher's whole ledger for the year (profile reset / start fresh)."""
        with self._locked(tenant_id, user_id, year_id):
            # (the file backend writes an empty map where unlink is forbidden)
            self.backend.delete(self._key(tenant_id, user_id, year_id))
