"""InvoiceRepository over the document backend (file or Postgres — Track C, 2026-09-09).

Layout (document keys; folders on disk, row keys in Postgres):

    invoices/{tenant}/{user}/MEY-2026-27-0001.json    the record
    invoices/{tenant}/{user}/MEY-2026-27-0001.pdf     the exact bytes she was sent
    invoices/_series/2026-27.json                     the seller's counter

Two deliberate choices:

**The PDF is stored, not re-rendered.** A document she may show an accountant must not
change because a template did. Re-rendering on download would quietly reissue history
every time the house style moves; the bytes on disk are the bytes she was mailed.

**The counter lives OUTSIDE any tenant folder.** The series belongs to the SELLER, not
to a teacher, and it must survive a teacher erasing her account — a right-to-be-forgotten
erase walks `{tenant}` trees, and a counter inside one would take the seller's books with
it. `invoices/_series/` is not a valid tenant slug (`_slug` strips the leading
underscore), so no tenant can ever collide with it.

Numbers are formatted MEY/2026-27/0001 for humans and MEY-2026-27-0001 on disk — the
filesystem has no business holding slashes.
"""
from __future__ import annotations

from dataclasses import asdict
from typing import List, Optional

from aruvi_core.ports import Invoice, InvoiceLine, InvoiceRepository
from aruvi_core.adapters.document_backend import as_backend, slug as _slug


def number_to_file(number: str) -> str:
    """MEY/2026-27/0001 → MEY-2026-27-0001 (also guards a hand-passed number)."""
    return _slug(str(number).replace("/", "-"))


class InvoiceRepositoryFileImpl(InvoiceRepository):
    """Per-teacher invoice store plus the seller's shared number series."""

    def __init__(self, data_dir: str, prefix: str = "MEY", start: int = 7834):
        """
        Args:
            data_dir: ARUVI_STATE_DIR — the invoices/ folder lives here.
            prefix:   the seller's series prefix ("MEY/2026-27/7834").
            start:    ★ the FIRST number of each financial year (founder, 2026-08-26).
                      Not 1. A number is the one part of an invoice a customer can read
                      volume from, and "0001" tells every early teacher she is the first
                      sale Aruvi ever made — which is true, and none of her business.
                      Four digits from 7834 says nothing either way. It is a starting
                      OFFSET, not a fake: the series is still gapless and still counts
                      real invoices, so the books remain auditable — the only thing
                      hidden is where the count began.
        """
        self.backend = as_backend(data_dir)
        self.prefix = (prefix or "MEY").strip() or "MEY"
        self.start = int(start)

    # ── keys ──
    def _prefix(self, tenant_id: str, user_id: str) -> str:
        return f"invoices/{_slug(tenant_id)}/{_slug(user_id)}"

    # ── numbering ──
    def next_number(self, financial_year: str) -> str:
        """Next in the seller's gapless series for that financial year.

        Read-modify-write under the backend's per-document lock: a process lock on
        files (honest for one uvicorn process) and, on Postgres, a transaction-scoped
        advisory lock — the "sequence or row lock" the file version always said the DB
        adapter must bring. Said here because a duplicated invoice number is the kind of
        thing nobody notices until an audit.
        """
        fy = _slug(financial_year or "0000-00")
        key = f"invoices/_series/{fy}.json"
        with self.backend.lock(key):
            raw = self.backend.get_json(key)
            try:
                n = int((raw or {}).get("last", 0)) if isinstance(raw, dict) else 0
            except (TypeError, ValueError):
                n = 0
            # A fresh year opens at `start`; thereafter it is a plain +1. A corrupt or
            # missing counter can only ever RESTART the year, never rewind past a number
            # already issued — which is why `start` is the floor, not just the seed.
            n = max(n + 1, self.start)
            self.backend.put_json(key, {"last": n})
        return f"{self.prefix}/{financial_year}/{n:04d}"

    # ── read / write ──
    def save(self, tenant_id: str, user_id: str, invoice: Invoice,
             pdf: Optional[bytes] = None) -> None:
        stem = number_to_file(invoice.number)
        base = self._prefix(tenant_id, user_id)
        self.backend.put_json(f"{base}/{stem}.json", asdict(invoice))
        if pdf:
            self.backend.put_bytes(f"{base}/{stem}.pdf", pdf)

    def load_all(self, tenant_id: str, user_id: str) -> List[Invoice]:
        """Every invoice for this teacher, NEWEST FIRST (by issue time, then number —
        the number breaks ties within a same-second double purchase)."""
        base = self._prefix(tenant_id, user_id)
        out: List[Invoice] = []
        for key in self.backend.list_keys(base):
            if not key.endswith(".json") or "/" in key[len(base) + 1:]:
                continue
            raw = self.backend.get_json(key)
            if not isinstance(raw, dict):
                continue          # one unreadable invoice must not hide the others
            lines = [InvoiceLine(**{k: v for k, v in (ln or {}).items()
                                    if k in InvoiceLine.__dataclass_fields__})
                     for ln in (raw.get("lines") or [])]
            fields = {k: v for k, v in raw.items()
                      if k in Invoice.__dataclass_fields__ and k != "lines"}
            fields.setdefault("number", "")
            fields.setdefault("issued_at", "")
            fields.setdefault("tenant_id", tenant_id)
            fields.setdefault("user_id", user_id)
            out.append(Invoice(lines=lines, **fields))
        out.sort(key=lambda i: (i.issued_at, i.number), reverse=True)
        return out

    def load_pdf(self, tenant_id: str, user_id: str, number: str) -> Optional[bytes]:
        return self.backend.get_bytes(f"{self._prefix(tenant_id, user_id)}/{number_to_file(number)}.pdf")
