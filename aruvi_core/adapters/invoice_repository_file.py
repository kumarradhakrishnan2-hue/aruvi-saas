"""File-based implementation of InvoiceRepository (2026-08-26).

Layout, under ARUVI_STATE_DIR:

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

import json
import os
import tempfile
import threading
from dataclasses import asdict
from pathlib import Path
from typing import List, Optional

from aruvi_core.ports import Invoice, InvoiceLine, InvoiceRepository


def _slug(s: str) -> str:
    """Filesystem-safe slug for a tenant/user id (defends against path traversal)."""
    s = str(s).strip() or "local"
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s).strip("-_") or "local"


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
        self.base_dir = Path(data_dir) / "invoices"
        self.series_dir = self.base_dir / "_series"
        self.prefix = (prefix or "MEY").strip() or "MEY"
        self.start = int(start)
        self._lock = threading.Lock()

    # ── paths ──
    def _dir(self, tenant_id: str, user_id: str) -> Path:
        return self.base_dir / _slug(tenant_id) / _slug(user_id)

    # ── numbering ──
    def next_number(self, financial_year: str) -> str:
        """Next in the seller's gapless series for that financial year.

        Process-locked and written whole via a temp file + atomic replace. That is
        honest for one uvicorn process and is NOT enough for two: the partner's DB
        adapter must take this from a sequence or a row lock. Said here because a
        duplicated invoice number is the kind of thing nobody notices until an audit.
        """
        fy = _slug(financial_year or "0000-00")
        path = self.series_dir / f"{fy}.json"
        with self._lock:
            n = 0
            if path.exists():
                try:
                    with open(path, "r") as f:
                        n = int((json.load(f) or {}).get("last", 0))
                except (json.JSONDecodeError, IOError, TypeError, ValueError):
                    n = 0
            # A fresh year opens at `start`; thereafter it is a plain +1. A corrupt or
            # missing counter can only ever RESTART the year, never rewind past a number
            # already issued — which is why `start` is the floor, not just the seed.
            n = max(n + 1, self.start)
            self.series_dir.mkdir(parents=True, exist_ok=True)
            fd, tmp = tempfile.mkstemp(dir=str(self.series_dir), suffix=".tmp")
            try:
                with os.fdopen(fd, "w") as f:
                    json.dump({"last": n}, f)
                os.replace(tmp, path)
            except Exception:
                if os.path.exists(tmp):
                    os.unlink(tmp)
                raise
        return f"{self.prefix}/{financial_year}/{n:04d}"

    # ── read / write ──
    def save(self, tenant_id: str, user_id: str, invoice: Invoice,
             pdf: Optional[bytes] = None) -> None:
        d = self._dir(tenant_id, user_id)
        d.mkdir(parents=True, exist_ok=True)
        stem = number_to_file(invoice.number)
        with open(d / f"{stem}.json", "w") as f:
            json.dump(asdict(invoice), f, indent=2)
        if pdf:
            with open(d / f"{stem}.pdf", "wb") as f:
                f.write(pdf)

    def load_all(self, tenant_id: str, user_id: str) -> List[Invoice]:
        """Every invoice for this teacher, NEWEST FIRST (by issue time, then number —
        the number breaks ties within a same-second double purchase)."""
        d = self._dir(tenant_id, user_id)
        if not d.exists():
            return []
        out: List[Invoice] = []
        for path in sorted(d.glob("*.json")):
            try:
                with open(path, "r") as f:
                    raw = json.load(f) or {}
            except (json.JSONDecodeError, IOError):
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
        path = self._dir(tenant_id, user_id) / f"{number_to_file(number)}.pdf"
        if not path.exists():
            return None
        try:
            with open(path, "rb") as f:
                return f.read()
        except IOError:
            return None
