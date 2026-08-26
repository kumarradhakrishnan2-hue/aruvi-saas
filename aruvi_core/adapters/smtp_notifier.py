"""SMTP implementation of the Notifier port — the real send.

Credentials NEVER live in this file or in the repo. They come from the environment,
which the founder sets himself:

    ARUVI_SMTP_HOST      smtp.gmail.com
    ARUVI_SMTP_PORT      587
    ARUVI_SMTP_USER      kumar.radhakrishnan2@gmail.com
    ARUVI_SMTP_PASSWORD  a Google APP PASSWORD (never the account password)
    ARUVI_MAIL_FROM      kumar.radhakrishnan2@gmail.com   (defaults to SMTP_USER)

Gmail requires an app password with 2-step verification on; the ordinary account
password will be refused. Without ARUVI_SMTP_HOST/USER/PASSWORD set, api/main.py
installs FileNotifier instead and nothing is sent — the preview stays credential-free.

This is a stop-gap sender for the preview and small volumes. A transactional provider
(SES / Postmark / Resend) belongs behind this same Notifier port before real scale:
Gmail enforces daily send limits and personal-account sending hurts deliverability.
"""
from __future__ import annotations

import smtplib
import ssl
from email.message import Message
from email.utils import formatdate, make_msgid
from typing import Any, Dict

from aruvi_core.ports import EmailMessage, Notifier


class SmtpNotifier(Notifier):
    """Sends over SMTP with STARTTLS. Never raises — failures come back as a result."""

    def __init__(self, host: str, port: int, user: str, password: str,
                 from_addr: str = "", timeout: int = 20):
        self.host = host
        self.port = int(port or 587)
        self.user = user
        self.password = password
        self.from_addr = from_addr or user
        self.timeout = timeout

    def send(self, msg: EmailMessage) -> Dict[str, Any]:
        """Deliver one message. Returns a result dict; never raises."""
        if not (msg.to or "").strip():
            return {"status": "skipped", "reason": "no recipient address"}
        if not (self.host and self.user and self.password):
            return {"status": "skipped", "reason": "SMTP not configured"}
        try:
            m = Message()
            m["From"] = self.from_addr
            m["To"] = msg.to
            m["Subject"] = msg.subject
            m["Date"] = formatdate(localtime=True)
            m["Message-ID"] = make_msgid()
            if msg.reply_to:
                m["Reply-To"] = msg.reply_to
            m.set_payload(msg.text, charset="utf-8")

            context = ssl.create_default_context()
            with smtplib.SMTP(self.host, self.port, timeout=self.timeout) as s:
                s.ehlo()
                s.starttls(context=context)
                s.ehlo()
                s.login(self.user, self.password)
                s.send_message(m)
            return {"status": "sent", "to": msg.to}
        except Exception as e:                       # noqa: BLE001 — never break a caller
            return {"status": "error", "detail": f"{type(e).__name__}: {e}"}
