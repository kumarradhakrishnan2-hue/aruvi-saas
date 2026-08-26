"""File-based implementation of the Notifier port — the dev/preview transport.

Writes each outbound message to ARUVI_STATE_DIR/outbox/{timestamp}-{slug}.txt instead
of sending it. This is the notification twin of ManualBillingProvider: the whole flow
runs end to end with NO vendor and no credentials, and the founder can read exactly
what a teacher would have received.

Nothing above the port knows which notifier is installed — swap in SmtpNotifier (real
send) or the partner's transactional-email adapter later with no caller change.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from aruvi_core.ports import EmailMessage, Notifier


def _slug(s: str) -> str:
    """Filesystem-safe fragment of an address, for a readable filename."""
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", str(s or "unknown")).strip("-")
    return (s or "unknown")[:60]


class FileNotifier(Notifier):
    """Writes messages to an outbox folder; never sends, never raises."""

    def __init__(self, data_dir: str, from_addr: str = ""):
        """
        Args:
            data_dir: Base directory (ARUVI_STATE_DIR) — the outbox/ folder lives here.
            from_addr: The address the real transport would send AS; recorded in the
                file so the preview shows the same header the live mail will carry.
        """
        self.outbox_dir = Path(data_dir) / "outbox"
        self.from_addr = from_addr

    def send(self, msg: EmailMessage) -> Dict[str, Any]:
        """Write the message to the outbox. Returns a result dict; never raises."""
        if not (msg.to or "").strip():
            return {"status": "skipped", "reason": "no recipient address"}
        try:
            self.outbox_dir.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
            path = self.outbox_dir / f"{stamp}-{_slug(msg.to)}.txt"
            header = [
                f"From: {self.from_addr}" if self.from_addr else "From: (unset)",
                f"To: {msg.to}",
                f"Reply-To: {msg.reply_to}" if msg.reply_to else "",
                f"Subject: {msg.subject}",
                f"Date: {datetime.now(timezone.utc).isoformat()}",
                "",
            ]
            # Attachments are written BESIDE the message, not described in it
            # (2026-08-26): the point of the outbox is that the founder can open
            # exactly what a teacher would have received, and an invoice he cannot
            # open is not that.
            written = []
            # The HTML part is written as its own .html so the founder can OPEN it in a
            # browser and see what a teacher will see. An outbox that only ever shows
            # the plain-text half cannot preview the mail that actually goes out.
            if (msg.html or "").strip():
                try:
                    with open(self.outbox_dir / f"{stamp}-{_slug(msg.to)}.html", "w") as hf:
                        hf.write(msg.html)
                    written.append(f"{stamp}-{_slug(msg.to)}.html")
                except Exception:                    # noqa: BLE001
                    pass
            for att in (msg.attachments or []):
                name = f"{stamp}-{_slug(att.filename or 'attachment')}"
                try:
                    with open(self.outbox_dir / name, "wb") as af:
                        af.write(att.content or b"")
                    written.append(name)
                except Exception:                    # noqa: BLE001
                    pass
            with open(path, "w") as f:
                f.write("\n".join(h for h in header if h != "") + "\n")
                f.write(msg.text.rstrip() + "\n")
                if written:
                    f.write("\n--\nWritten beside this message:\n")
                    for name in written:
                        f.write(f"  {name}\n")
            return {"status": "written", "path": str(path), "attachments": written}
        except Exception as e:                       # noqa: BLE001 — never break a caller
            return {"status": "error", "detail": str(e)}
