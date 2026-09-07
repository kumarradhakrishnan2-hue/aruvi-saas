"""File-based implementation of SectionHistoryRepository.

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
import json
import os
import tempfile
import threading
from pathlib import Path
from typing import Any, Dict, List

from aruvi_core.ports import SectionHistoryEntry, SectionHistoryRepository


def _slug(s: str) -> str:
    """Filesystem-safe slug for a tenant/user id (defends against path traversal)."""
    s = str(s).strip() or "local"
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s).strip("-") or "local"


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

    def __init__(self, data_dir: str):
        """
        Args:
            data_dir: Base directory where section_history/ lives (e.g. ARUVI_STATE_DIR).
        """
        self.data_dir = Path(data_dir)
        self.base_dir = self.data_dir / "section_history"
        # Serialize the read-modify-write of the shared history.json WITHIN this process,
        # for the reason section_state_repository_file spells out: FastAPI runs handlers on
        # a threadpool, so two near-simultaneous merges would otherwise both read the same
        # snapshot and the second write would lose the first section's row. os.replace keeps
        # a write from tearing the file; this lock keeps writes from losing each other.
        # One module-level repo instance (api/main.py) → the lock is process-wide. A
        # multi-process deployment moves this to the DB row-lock (Supabase, §2.4).
        self._lock = threading.Lock()

    def _path(self, tenant_id: str, user_id: str, year_id: str) -> Path:
        return (self.base_dir / _slug(tenant_id) / _slug(user_id) / _slug(year_id)
                / "history.json")

    def _read(self, tenant_id: str, user_id: str, year_id: str) -> Dict[str, Any]:
        path = self._path(tenant_id, user_id, year_id)
        if not path.exists():
            return {}
        try:
            with open(path, "r") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except IOError:
            return {}
        except json.JSONDecodeError:
            # SELF-HEAL a file torn by a legacy non-atomic write, exactly as the section-state
            # adapter does: raw_decode parses the VALID leading object and ignores trailing
            # garbage, so a damaged file still returns the real ledger instead of {}. Returning
            # {} is what lets a corrupt file look like "she has taught nothing".
            try:
                with open(path, "r") as f:
                    raw = f.read()
                obj, _ = json.JSONDecoder().raw_decode(raw.lstrip())
                return obj if isinstance(obj, dict) else {}
            except Exception:               # noqa: BLE001
                return {}

    def _write(self, tenant_id: str, user_id: str, year_id: str,
               data: Dict[str, Any]) -> None:
        # ATOMIC write: temp file in the same dir, then os.replace over the target, which is
        # atomic on POSIX/Windows — a reader always sees the complete old file or the
        # complete new one, never a half-written one.
        path = self._path(tenant_id, user_id, year_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = None
        try:
            fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".history-", suffix=".tmp")
            with os.fdopen(fd, "w") as f:
                json.dump(data, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, path)
            tmp = None
        except IOError as e:
            raise ValueError(f"Failed to save section history to {path}: {e}")
        finally:
            if tmp is not None and os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except OSError:
                    pass

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
        with self._lock:
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
        with self._lock:
            data = self._read(tenant_id, user_id, year_id)
            if section_key in data:
                data.pop(section_key, None)
                self._write(tenant_id, user_id, year_id, data)

    def clear_all(self, tenant_id: str, user_id: str, year_id: str) -> None:
        """Erase this teacher's whole ledger for the year (profile reset / start fresh)."""
        with self._lock:
            path = self._path(tenant_id, user_id, year_id)
            if not path.exists():
                return
            try:
                path.unlink()
            except OSError:
                # mounts that allow overwrite but not unlink → write an empty map instead
                self._write(tenant_id, user_id, year_id, {})
