"""Document-backend implementation (file or Postgres — Track C, 2026-09-09) of PlanNoteRepository.

Persists a teacher's chapter notes as JSON at
ARUVI_STATE_DIR/plan_notes/{tenant_id}/{user_id}/{year_id}/notes.json, shaped as

    { "science/vii/3": {"text": "…", "updated_at": "2026-08-22T09:12:00+00:00"}, ... }

i.e. {note_key: {text, updated_at}} with note_key = "{subject}/{grade}/{chapter_number}"
— the CHAPTER's identity, never a plan filename (one note per chapter per year; founder,
2026-08-22). Year-scoping is what keeps a note with its year's plans at cutover (§2.4):
the new year simply reads an empty folder.

The two §2.4 rules, enforced here:
  * NO VERSION HISTORY. The file holds exactly one text per key; saving overwrites it,
    and saving empty text removes the key. Nothing is ever kept back.
  * ANTI-CLOBBER, not history: save() raises StaleNoteWrite when the incoming
    updated_at is older than the stored one, so a stale phone cannot silently overwrite
    a fresher laptop edit. Equal timestamps are accepted (idempotent re-save).

Same concurrency posture as the section-state adapter: a process-wide lock serializes
read-modify-write (FastAPI threadpool), and writes are atomic (the backend's contract)
so a reader never sees a half-written file. A multi-instance deployment moves this to
the partner DB's row lock.
"""
from typing import Any, Dict, Optional

from aruvi_core.ports import PlanNote, PlanNoteRepository, StaleNoteWrite
from aruvi_core.adapters.document_backend import as_backend, slug as _slug




class PlanNoteRepositoryFileImpl(PlanNoteRepository):
    """File-based per-tenant chapter-notes store."""

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
        return f"plan_notes/{_slug(tenant_id)}/{_slug(user_id)}/{_slug(year_id)}/notes.json"

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

    def load(self, tenant_id: str, user_id: str, year_id: str,
             note_key: str) -> Optional[PlanNote]:
        """One chapter's note, or None."""
        raw = self._read(tenant_id, user_id, year_id).get(note_key)
        if raw is None:
            return None
        return PlanNote(note_key=note_key, text=str(raw.get("text", "")),
                        updated_at=str(raw.get("updated_at", "")))

    def save(self, tenant_id: str, user_id: str, year_id: str, note: PlanNote) -> None:
        """Upsert one note; empty text deletes; older-than-stored raises StaleNoteWrite.

        The timestamp comparison is a plain string compare — valid because both sides
        are ISO-8601 UTC strings, which order lexicographically. A stored record with a
        missing/blank updated_at never blocks a write.
        """
        with self._locked(tenant_id, user_id, year_id):
            data = self._read(tenant_id, user_id, year_id)
            existing = data.get(note.note_key)
            stored_at = str(existing.get("updated_at", "")) if existing else ""
            if stored_at and note.updated_at and note.updated_at < stored_at:
                raise StaleNoteWrite(
                    f"Note {note.note_key!r} has a newer copy on the server "
                    f"({stored_at} > {note.updated_at}); re-read before writing.")
            if note.text.strip():
                data[note.note_key] = {"text": note.text, "updated_at": note.updated_at}
            else:
                if note.note_key not in data:
                    return  # deleting nothing — no write, no error
                data.pop(note.note_key, None)
            self._write(tenant_id, user_id, year_id, data)

    def load_all(self, tenant_id: str, user_id: str, year_id: str) -> Dict[str, PlanNote]:
        """Every note this teacher wrote this year."""
        return {k: PlanNote(note_key=k, text=str(v.get("text", "")),
                            updated_at=str(v.get("updated_at", "")))
                for k, v in self._read(tenant_id, user_id, year_id).items()}

    def delete(self, tenant_id: str, user_id: str, year_id: str, note_key: str) -> None:
        """Remove one note outright. No-op if absent."""
        with self._locked(tenant_id, user_id, year_id):
            data = self._read(tenant_id, user_id, year_id)
            if note_key in data:
                data.pop(note_key, None)
                self._write(tenant_id, user_id, year_id, data)
