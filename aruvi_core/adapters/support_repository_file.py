"""File-based implementation of SupportRepository (2026-08-27).

Layout, under ARUVI_STATE_DIR:

    support/{tenant}/{user}/ARV-S-742.json     the request, as she wrote it
    support/_series/support.json               the reference counter

The two placements are deliberate and opposite:

**The request is HERS.** It is her words, filed under her identity, so the erase
traversal reaches it by folder boundary like every other Bucket-B store, and the data
export renders it. A teacher who asks for everything Aruvi holds about her and is not
shown the messages she sent has not been shown everything.

**The counter is the SELLER'S.** It sits in `support/_series/`, outside any tenant
folder — the invoice-series precedent (`_slug` strips the leading underscore, so no
tenant can ever collide with it). If it lived inside a teacher's folder her erasure
would take it with her and the next teacher would be handed a reference already in use.
The counter holds one integer and nothing about anybody.

References are short on purpose: they are quoted in email subject lines and read aloud.
No financial year, no zero padding — a case belongs to the day it was raised, not to a
book that has to balance, and 742 → 1000 is a counter growing, not a format breaking.
"""
from __future__ import annotations

import json
import os
import tempfile
import threading
from dataclasses import asdict
from pathlib import Path
from typing import List

from aruvi_core.ports import SupportRepository, SupportRequest


def _slug(s: str) -> str:
    """Filesystem-safe slug for a tenant/user id (defends against path traversal)."""
    s = str(s).strip() or "local"
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s).strip("-_") or "local"


def reference_to_file(reference: str) -> str:
    """Guard a hand-passed reference into a filename ("ARV-S-742")."""
    return _slug(str(reference).replace("/", "-"))


class SupportRepositoryFileImpl(SupportRepository):
    """Per-teacher support store plus the shared reference series."""

    def __init__(self, data_dir: str, prefix: str = "MEY-S", start: int = 742):
        """
        Args:
            data_dir: ARUVI_STATE_DIR — the support/ folder lives here.
            prefix:   the reference prefix ("MEY-S-742"; ARV-S until 2026-09-03).
            start:    ★ the FIRST reference ever issued (founder, 2026-08-27). Not 1.
                      A reference number is the one part of an acknowledgement a teacher
                      can read volume from, and "ARV-S-1" tells her she is the first
                      person who ever needed help — which is true, briefly, and does
                      nothing for her confidence that anyone is on the other end. Three
                      digits says nothing either way. An OFFSET, not a fiction: the
                      series is gapless and counts real cases, so it stays auditable;
                      the only thing hidden is where the count began.
        """
        self.base_dir = Path(data_dir) / "support"
        self.series_dir = self.base_dir / "_series"
        self.prefix = (prefix or "MEY-S").strip() or "MEY-S"
        self.start = int(start)
        self._lock = threading.Lock()

    # ── paths ──
    def _dir(self, tenant_id: str, user_id: str) -> Path:
        return self.base_dir / _slug(tenant_id) / _slug(user_id)

    # ── numbering ──
    def next_reference(self) -> str:
        """Next in the gapless series. Process-locked and written whole via a temp file
        + atomic replace — honest for one uvicorn process and NOT enough for two; the
        partner's DB adapter must take this from a sequence or a row lock. A duplicated
        reference is worse here than in most places: two teachers quoting the same
        number in two threads is a support system quietly lying to both of them."""
        path = self.series_dir / "support.json"
        with self._lock:
            n = 0
            if path.exists():
                try:
                    with open(path, "r") as f:
                        n = int((json.load(f) or {}).get("last", 0))
                except (json.JSONDecodeError, IOError, TypeError, ValueError):
                    n = 0
            # `start` is the FLOOR, not just the seed: a corrupt or missing counter can
            # only ever restart the series, never rewind past a reference already given
            # to somebody.
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
        return f"{self.prefix}-{n}"

    # ── read / write ──
    def save(self, request: SupportRequest) -> None:
        d = self._dir(request.tenant_id, request.user_id)
        d.mkdir(parents=True, exist_ok=True)
        with open(d / f"{reference_to_file(request.reference)}.json", "w") as f:
            json.dump(asdict(request), f, indent=2)

    def load_all(self, tenant_id: str, user_id: str) -> List[SupportRequest]:
        """Every request for this teacher, NEWEST FIRST (by creation time, then
        reference — the reference breaks ties within a same-second double send)."""
        d = self._dir(tenant_id, user_id)
        if not d.exists():
            return []
        out: List[SupportRequest] = []
        for path in sorted(d.glob("*.json")):
            try:
                with open(path, "r") as f:
                    raw = json.load(f) or {}
            except (json.JSONDecodeError, IOError):
                continue          # one unreadable request must not hide the others
            fields = {k: v for k, v in raw.items()
                      if k in SupportRequest.__dataclass_fields__}
            fields.setdefault("reference", path.stem)
            fields.setdefault("tenant_id", tenant_id)
            fields.setdefault("user_id", user_id)
            fields.setdefault("category", "")
            fields.setdefault("message", "")
            out.append(SupportRequest(**fields))
        out.sort(key=lambda r: (r.created_at, r.reference), reverse=True)
        return out
