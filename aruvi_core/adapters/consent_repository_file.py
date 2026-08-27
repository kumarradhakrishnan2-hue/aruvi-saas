"""File-based implementation of ConsentRepository (2026-08-27).

Layout, under ARUVI_STATE_DIR:

    consents/_ledger/{tenant}.json      an append-only list of acceptances

**Why `_ledger/` and not `consents/{tenant}/{user}/`.** The erase traversal
(DataRightsServiceFileImpl) removes `{kind}/{tenant}/{user}` folders wholesale, and a
consent record filed that way would go with them. It must not: the record is the proof
that the agreement was accepted, and proof the other party can delete is not proof. So
it sits where the invoice number series sits — outside every tenant-shaped folder the
traversal walks. `_ledger` is not a reachable tenant slug (`_slug` strips the leading
underscore), so no tenant can collide with it, and no tenant walk can reach it.

That is a retention decision, not an accident, so it is said out loud in three places
that must agree: the ConsentRepository port, the erasure receipt's `kept` list, and §G
of the agreement itself. Change one, change all three.

★ BUT SURVIVING IS NOT THE SAME AS STILL BINDING (founder, 2026-08-27). Erase now calls
`supersede()`, which stamps the tenant's rows with the date they stopped applying and
leaves everything else intact. The rows are still evidence; they are no longer a
standing signature, so an id that comes back after erasure is asked to sign again.
Without this, a teacher who erased and returned walked straight past the agreement —
and worse, so would the NEXT holder of a reassigned mobile number.

The file is a plain JSON list, oldest first, written whole (an acceptance is a few
hundred bytes and a teacher accumulates one per document version — this will not grow).
Appends are process-locked and land via a temp file + atomic replace, the same honesty
the invoice counter carries: enough for one uvicorn process, NOT enough for two. The
partner's DB adapter makes this an INSERT.
"""
from __future__ import annotations

import json
import os
import tempfile
import threading
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from aruvi_core.ports import ConsentRecord, ConsentRepository


def _slug(s: str) -> str:
    """Filesystem-safe slug for a tenant id (also defends against path traversal)."""
    s = str(s).strip() or "local"
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s).strip("-_") or "local"


class ConsentRepositoryFileImpl(ConsentRepository):
    """Append-only consent ledger, one file per tenant, outside the erase traversal."""

    def __init__(self, data_dir: str):
        self.base_dir = Path(data_dir) / "consents" / "_ledger"
        self._lock = threading.Lock()

    def _path(self, tenant_id: str) -> Path:
        return self.base_dir / f"{_slug(tenant_id)}.json"

    # ── read ──
    def load_all(self, tenant_id: str) -> List[ConsentRecord]:
        path = self._path(tenant_id)
        if not path.exists():
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = json.load(f) or []
        except (json.JSONDecodeError, IOError):
            return []
        out: List[ConsentRecord] = []
        for row in raw:
            if not isinstance(row, dict):
                continue
            fields = {k: v for k, v in row.items() if k in ConsentRecord.__dataclass_fields__}
            fields.setdefault("tenant_id", tenant_id)
            fields.setdefault("user_id", "")
            fields.setdefault("document_id", "")
            fields.setdefault("document_version", "")
            out.append(ConsentRecord(**fields))
        out.sort(key=lambda r: r.accepted_at)
        return out

    def latest(self, tenant_id: str, document_id: str,
               version: str = "") -> Optional[ConsentRecord]:
        """The most recent acceptance IN FORCE. `superseded_at` rows are skipped here and
        only here: load_all keeps them (the export must show what was kept), the gate
        must not (an erased account's old signature binds nobody)."""
        rows = [r for r in self.load_all(tenant_id)
                if r.document_id == document_id and not r.superseded_at]
        if version:
            rows = [r for r in rows if r.document_version == version]
        return rows[-1] if rows else None

    # ── write ──
    def save(self, record: ConsentRecord) -> None:
        """Append. Read-modify-write under the lock: two ticks in the same second from
        two tabs must both survive, and a lost one is a lost signature."""
        path = self._path(record.tenant_id)
        with self._lock:
            rows = []
            if path.exists():
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        rows = json.load(f) or []
                except (json.JSONDecodeError, IOError):
                    rows = []          # a corrupt file must not swallow this signature
            rows.append(asdict(record))
            self._write(path, rows)

    def supersede(self, tenant_id: str, at: str = "") -> int:
        """★ End every standing signature for this tenant, keeping the rows (2026-08-27).

        Called by the erase traversal. This is the ONE write that touches an existing
        row, and it adds a field rather than changing one: what she accepted, when, and
        which points she ticked are all still there — only the fact that it still binds
        goes away. An already-stamped row keeps its first date, so erasing twice cannot
        rewrite when the agreement actually ended.

        A missing file is not an error. A tenant who never signed has nothing to end,
        and erase must stay idempotent."""
        stamp = at or datetime.now(timezone.utc).isoformat()
        path = self._path(tenant_id)
        with self._lock:
            if not path.exists():
                return 0
            try:
                with open(path, "r", encoding="utf-8") as f:
                    rows = json.load(f) or []
            except (json.JSONDecodeError, IOError):
                return 0
            n = 0
            for row in rows:
                if isinstance(row, dict) and not row.get("superseded_at"):
                    row["superseded_at"] = stamp
                    n += 1
            if n:
                self._write(path, rows)
            return n

    def _write(self, path: Path, rows: list) -> None:
        """Whole-file write via temp + atomic replace — a half-written ledger is a
        half-lost signature. Callers hold the lock."""
        self.base_dir.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=str(self.base_dir), suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(rows, f, indent=2, ensure_ascii=False)
            os.replace(tmp, path)
        except Exception:
            if os.path.exists(tmp):
                os.unlink(tmp)
            raise
