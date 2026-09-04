#!/usr/bin/env python3
"""Say OUT LOUD why an Aruvi mail did not send.

SmtpNotifier.send() never raises — by design, so a failed acknowledgement can never
lose a teacher's words. The cost is that the reason is swallowed: the route reads only
`status`, and a real SMTP failure reaches the screen as `emailed: False`, which the
support screen then reports as "there is no email address on your account". This script
is the missing half — it runs the SAME adapter with the SAME environment and PRINTS the
detail the route throws away.

Run it exactly as you run the API, with the same env vars:

    ARUVI_SMTP_HOST=smtp.gmail.com \
    ARUVI_SMTP_USER=support@meyy.in \
    ARUVI_SMTP_PASSWORD='xxxx xxxx xxxx xxxx' \
    ARUVI_MAIL_FROM=support@meyy.in \
    python3 aruvi-scripts/smtp_check.py you@example.com

With no recipient it stops after login, so you can test credentials without sending.
"""
from __future__ import annotations

import os
import smtplib
import ssl
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import config  # noqa: E402


def mask(secret: str) -> str:
    s = (secret or "").replace(" ", "")
    return f"{len(s)} chars, ends …{s[-4:]}" if len(s) >= 4 else "(empty)"


def main() -> int:
    to = sys.argv[1].strip() if len(sys.argv) > 1 else ""

    print("── what the API would use ──────────────────────────────")
    print(f"  SMTP_HOST       {config.SMTP_HOST or '(unset)'}")
    print(f"  SMTP_PORT       {config.SMTP_PORT}")
    print(f"  SMTP_USER       {config.SMTP_USER or '(unset)'}")
    print(f"  SMTP_PASSWORD   {mask(config.SMTP_PASSWORD)}")
    print(f"  MAIL_FROM       {config.MAIL_FROM}")
    print(f"  SUPPORT_ADDRESS {config.SUPPORT_ADDRESS}")
    print(f"  MAIL_REPLY_TO   {config.MAIL_REPLY_TO}")

    if not (config.SMTP_HOST and config.SMTP_USER and config.SMTP_PASSWORD):
        print("\n✗ One of HOST/USER/PASSWORD is unset — the API installs FileNotifier "
              "and NOTHING sends. Mail lands in "
              f"{config.STATE_DIR}/outbox/ instead.")
        return 1

    if config.MAIL_FROM.strip().lower() != config.SMTP_USER.strip().lower():
        print("\n⚠ MAIL_FROM differs from SMTP_USER. Gmail rewrites a From address the "
              "authenticated account does not own, so the teacher may see a different "
              "sender than you intend (and SPF alignment can suffer).")

    print("\n── connecting ──────────────────────────────────────────")
    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=20) as s:
            s.set_debuglevel(0)
            code, banner = s.ehlo()
            print(f"  EHLO      {code} {banner.decode(errors='replace').splitlines()[0]}")
            s.starttls(context=ctx)
            s.ehlo()
            print("  STARTTLS  ok")
            s.login(config.SMTP_USER, config.SMTP_PASSWORD)
            print(f"  LOGIN     ok as {config.SMTP_USER}")

            if not to:
                print("\n✓ Credentials work. Pass a recipient to send a real test:\n"
                      "    python3 aruvi-scripts/smtp_check.py you@example.com")
                return 0

            from email.message import EmailMessage
            m = EmailMessage()
            m["From"] = config.MAIL_FROM
            m["To"] = to
            m["Subject"] = "Meyy SMTP check"
            m["Reply-To"] = config.MAIL_REPLY_TO
            m.set_content("If you are reading this, Meyy can send mail.\n")
            s.send_message(m)
            print(f"  SEND      ok → {to}")

        print("\n✓ Sent. Check the RECIPIENT's inbox (and spam).")
        print("  Note: mail submitted over SMTP is NOT copied to Gmail's Sent folder — "
              "that only happens for mail composed in Gmail itself. An empty Sent box "
              "is expected and proves nothing.")
        return 0

    except smtplib.SMTPAuthenticationError as e:
        print(f"\n✗ AUTH REFUSED — {e.smtp_code} {e.smtp_error!r}")
        print("  Usual causes, in order:")
        print("   1. The app password belongs to a DIFFERENT account than SMTP_USER.")
        print("   2. SMTP_USER is an ALIAS (e.g. support@ pointing at your own mailbox)."
              " Aliases cannot hold app passwords — authenticate as the real user and "
              "set ARUVI_MAIL_FROM to the alias instead.")
        print("   3. 2-Step Verification is off for that user, so the app password is "
              "not valid.")
        print("   4. Workspace admin has SMTP/less-secure access restricted for the OU.")
        return 1
    except Exception as e:  # noqa: BLE001
        print(f"\n✗ {type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
