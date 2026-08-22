"""File-based implementation of PlanNoteRepository.

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
read-modify-write (FastAPI threadpool), and writes are atomic (temp file + os.replace)
so a reader never sees a half-written file. A multi-instance deployment moves this to
the partner DB's row lock.
"""
import json
import os
import tempfile
import threading
from pathlib import Path
from typing import Any, Dict, Optional

from aruvi_core.ports import PlanNote, PlanNoteRepository, StaleNoteWrite


def _slug(s: str) -> str:
    """Filesystem-safe slug for a tenant/user/year id (defends against path traversal)."""
    s = str(s).strip() or "local"
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s).strip("-") or "local"


class PlanNoteRepositoryFileImpl(PlanNoteRepository):
    """File-based per-tenant chapter-notes store."""

    def __init__(self, data_dir: str):
        """
        Args:
            data_dir: Base directory where the plan_notes/ folder lives (e.g. ARUVI_STATE_DIR).
        """
        self.data_dir = Path(data_dir)
        self.base_dir = self.data_dir / "plan_notes"
        self._lock = threading.Lock()

    def _path(self, tenant_id: str, user_id: str, year_id: str) -> Path:
        return self.base_dir / _slug(tenant_id) / _slug(user_id) / _slug(year_id) / "notes.json"

    def _read(self, tenant_id: str, user_id: str, year_id: str) -> Dict[str, Any]:
        path = self._path(tenant_id, user_id, year_id)
        if not path.exists():
            return {}
        try:
            with open(path, "r") as f:
                return json.load(f) or {}
        except (IOError, json.JSONDecodeError):
            return {}

    def _write(self, tenant_id: str, user_id: str, year_id: str, data: Dict[str, Any]) -> None:
        # ATOMIC write: temp file in the same dir, then os.replace() over the target, so a
        # reader always sees the complete old or complete new file — never a torn one.
        path = self._path(tenant_id, user_id, year_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = None
        try:
            fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".notes-", suffix=".tmp")
            with os.fdopen(fd, "w") as f:
                json.dump(data, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, path)
            tmp = None
        except IOError as e:
            raise ValueError(f"Failed to save plan notes to {path}: {e}")
        finally:
            if tmp is not None and os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except OSError:
                    pass

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
        with self._lock:
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
        with self._lock:
            data = self._read(tenant_id, user_id, year_id)
            if note_key in data:
                data.pop(note_key, None)
                self._write(tenant_id, user_id, year_id, data)
