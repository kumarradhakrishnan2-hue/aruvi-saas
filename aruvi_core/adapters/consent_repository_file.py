"""ConsentRepository over the document backend (file or Postgres — Track C, 2026-09-09).

Layout (the document KEY; a folder on disk, a row key in Postgres):

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

The document is a plain JSON list, oldest first, written whole (an acceptance is a few
hundred bytes and a teacher accumulates one per document version — this will not grow).
Appends run under the backend's per-document lock — a process lock on files, and a
transaction-scoped advisory lock on Postgres, which is what makes two API instances safe.
"""
from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from typing import List, Optional

from aruvi_core.ports import ConsentRecord, ConsentRepository
from aruvi_core.adapters.document_backend import as_backend, slug as _slug


class ConsentRepositoryFileImpl(ConsentRepository):
    """Append-only consent ledger, one document per tenant, outside the erase traversal."""

    def __init__(self, data_dir):
        self.backend = as_backend(data_dir)

    def _key(self, tenant_id: str) -> str:
        return f"consents/_ledger/{_slug(tenant_id)}.json"

    def _rows(self, tenant_id: str) -> list:
        raw = self.backend.get_json(self._key(tenant_id))
        return raw if isinstance(raw, list) else []

    # ── read ──
    def load_all(self, tenant_id: str) -> List[ConsentRecord]:
        raw = self._rows(tenant_id)
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
        key = self._key(record.tenant_id)
        with self.backend.lock(key):
            rows = self._rows(record.tenant_id)   # a corrupt document must not swallow this signature
            rows.append(asdict(record))
            self.backend.put_json(key, rows)

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
        key = self._key(tenant_id)
        with self.backend.lock(key):
            if not self.backend.exists(key):
                return 0
            rows = self._rows(tenant_id)
            n = 0
            for row in rows:
                if isinstance(row, dict) and not row.get("superseded_at"):
                    row["superseded_at"] = stamp
                    n += 1
            if n:
                self.backend.put_json(key, rows)
            return n
