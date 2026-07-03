"""File-based implementation of SectionStateRepository.

Persists per-section teaching execution state as JSON at
ARUVI_DATA_DIR/section_state/{tenant_id}/{user_id}/state.json, shaped as

    { section_key: {chapter, unit_index, done, updated_at}, ... }

This is the Bucket-B "teaching pointer" (CLOUD_DATA_MODEL.md §2.4) lifted OFF browser
localStorage so a teacher's tracking + progress follow her across devices. localStorage
stays a client-side optimistic cache; this file is authoritative on load/reconcile. A
Supabase adapter (the `lesson_pointer` table extended with `chapter` + `done`) swaps in
later behind the same SectionStateRepository port with no change to the API or the app.

Every store is keyed by tenant_id + user_id. With no auth yet both stub to the same
X-Aruvi-User value; Phase 4 swaps the values from the Supabase auth token, no schema change.

save_one is a full per-section snapshot upsert (the client always sends the complete
current state for a section), so there is no field-level merge to reason about.
"""
import json
import os
import tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from aruvi_core.ports import SectionState, SectionStateRepository


def _slug(s: str) -> str:
    """Filesystem-safe slug for a tenant/user id (defends against path traversal)."""
    s = str(s).strip() or "local"
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s).strip("-") or "local"


class SectionStateRepositoryFileImpl(SectionStateRepository):
    """File-based per-section teaching-state store."""

    def __init__(self, data_dir: str):
        """
        Args:
            data_dir: Base directory where the section_state/ folder lives (e.g. ARUVI_STATE_DIR).
        """
        self.data_dir = Path(data_dir)
        self.base_dir = self.data_dir / "section_state"
        # Serialize the read-modify-write of the shared state.json WITHIN this process. FastAPI
        # runs request handlers on a threadpool, so two near-simultaneous POSTs (the app fires
        # pointer + done back-to-back on mark-complete) would otherwise both read the same
        # snapshot and the second overwrite would LOSE the first section's row. os.replace keeps
        # each write from corrupting the file; this lock keeps concurrent writes from losing each
        # other's updates. One module-level repo instance (api/main.py) → the lock is process-wide.
        # A multi-process/multi-instance deployment moves this to the DB row-lock (Supabase, §2.4).
        self._lock = threading.Lock()

    def _path(self, tenant_id: str, user_id: str) -> Path:
        return self.base_dir / _slug(tenant_id) / _slug(user_id) / "state.json"

    def _read(self, tenant_id: str, user_id: str) -> Dict[str, Any]:
        path = self._path(tenant_id, user_id)
        if not path.exists():
            return {}
        try:
            with open(path, "r") as f:
                return json.load(f) or {}
        except IOError:
            return {}
        except json.JSONDecodeError:
            # SELF-HEAL a file corrupted by the legacy non-atomic write race — the classic symptom
            # is a stray trailing brace ("...}}\n") that makes json.load raise "Extra data".
            # raw_decode parses the VALID leading object and ignores the trailing garbage, so a
            # corrupt file still returns the REAL tracked sections instead of {}. Returning {} here
            # is exactly what let a corrupt file wipe every device's local bindings; salvaging it
            # instead means the corruption can no longer cause data loss even before the atomic-
            # write fix is deployed. The next save_one() rewrites the file cleanly (atomically).
            try:
                with open(path, "r") as f:
                    raw = f.read()
                obj, _ = json.JSONDecoder().raw_decode(raw.lstrip())
                return obj if isinstance(obj, dict) else {}
            except Exception:
                return {}

    def _write(self, tenant_id: str, user_id: str, data: Dict[str, Any]) -> None:
        # ATOMIC write (2026-07-03): write a temp file in the same dir, then os.replace() it
        # over the target. os.replace is atomic on POSIX/Windows, so a reader always sees either
        # the complete old file or the complete new one — never a half-written file. Critically,
        # two concurrent writers (the app fires pointer + done POSTs back-to-back on
        # mark-complete) can no longer INTERLEAVE their writes into corrupt JSON with a stray
        # brace — each writer replaces atomically and the last one wins, both valid. The previous
        # open(path,"w") truncate-then-write could tear under that race, and a corrupt file made
        # _read() fall back to {} → the client reconcile then wiped every local binding.
        path = self._path(tenant_id, user_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = None
        try:
            fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".state-", suffix=".tmp")
            with os.fdopen(fd, "w") as f:
                json.dump(data, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, path)
            tmp = None
        except IOError as e:
            raise ValueError(f"Failed to save section state to {path}: {e}")
        finally:
            if tmp is not None and os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except OSError:
                    pass

    def load_all(self, tenant_id: str, user_id: str) -> Dict[str, SectionState]:
        """All tracked sections for this teacher. Empty dict if none."""
        return self._read(tenant_id, user_id)

    def save_one(self, tenant_id: str, user_id: str, section_key: str,
                 chapter: str, unit_index: Optional[int], done: bool) -> None:
        """Upsert one section's execution state (full snapshot for that section)."""
        with self._lock:
            data = self._read(tenant_id, user_id)
            data[section_key] = {
                "chapter": chapter,
                "unit_index": unit_index,
                "done": bool(done),
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            self._write(tenant_id, user_id, data)

    def delete_one(self, tenant_id: str, user_id: str, section_key: str) -> None:
        """Remove one section's state (untrack). No-op if absent."""
        with self._lock:
            data = self._read(tenant_id, user_id)
            if section_key in data:
                data.pop(section_key, None)
                self._write(tenant_id, user_id, data)
