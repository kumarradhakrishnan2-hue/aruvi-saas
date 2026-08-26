"""The words Aruvi sends. Kept OUT of api/main.py so copy can be edited without
touching routing, and out of the adapters so the transport never owns the message.

House voice (CLAUDE.md §4): plain, warm, specific. No exclamation marks, no marketing
padding, no "certified" — Aruvi is NCF *aligned*. Amounts in ₹, dates as dd-Mmm-yyyy,
and scopes spelled the way the teacher bought them ("Social Sciences · Middle").
"""
from __future__ import annotations

from datetime import date
from typing import Dict, List, Tuple

# Classes a stage covers, for the line that tells her what her subscription reaches.
_STAGE_CLASSES = {
    "preparatory": "Classes 3, 4 and 5",
    "middle": "Classes 6, 7 and 8",
    "secondary": "Class 9 (Class 10 coming soon)",
}


def _pretty_subject(slug: str) -> str:
    """social_sciences → Social Sciences; the_world_around_us → The World Around Us."""
    words = str(slug or "").replace("-", " ").replace("_", " ").split()
    small = {"the", "of", "and", "around", "us"}
    out = []
    for i, w in enumerate(words):
        out.append(w.capitalize() if (i == 0 or w.lower() not in small) else w.lower())
    return " ".join(out) or slug


def _fmt_date(iso: str) -> str:
    """2027-08-26 → 26-Aug-2027. Falls back to the raw string if it isn't a date."""
    try:
        return date.fromisoformat(str(iso)).strftime("%d-%b-%Y")
    except Exception:                                # noqa: BLE001
        return str(iso or "")


def scope_lines(scopes: List[str]) -> List[Tuple[str, str]]:
    """[(label, classes)] for each purchased "subject/stage" scope. "*" = everything."""
    rows = []
    for s in scopes or []:
        if s == "*":
            rows.append(("All subjects · All stages", "Classes 3 to 10"))
            continue
        subject, _, stage = str(s).partition("/")
        rows.append((f"{_pretty_subject(subject)} · {stage.capitalize()}",
                     _STAGE_CLASSES.get(stage.lower(), "")))
    return rows


def subscription_confirmation(name: str, scopes: List[str], amount_inr: int,
                              valid_until: str, mobile: str) -> Dict[str, str]:
    """The message a teacher gets the moment her subscription activates.

    Deliberately does three jobs and stops: confirms WHAT she bought, tells her WHEN it
    runs to, and shows the mobile her account is keyed to (that number is her sign-in,
    so it belongs in writing somewhere she can find it). No upsell, no feature tour —
    the app itself does that better."""
    first = (name or "").strip().split(" ")[0]
    hello = f"Hello {first[:1].upper() + first[1:]}," if first else "Hello,"
    rows = scope_lines(scopes)
    what = "\n".join(f"  • {label}" + (f" — {classes}" if classes else "")
                     for label, classes in rows)
    plural = "subscriptions" if len(rows) > 1 else "subscription"

    text = f"""{hello}

Your Aruvi {plural} {'are' if len(rows) > 1 else 'is'} active. Here is what you have:

{what}

  Amount    ₹{amount_inr:,} for the year
  Valid to  {_fmt_date(valid_until)}
  Sign in   {mobile}

Within that scope you can prepare as many lesson plans as you like, for every class
and section you teach, for the whole year. Everything you prepare stays yours.

Aruvi's plans follow the National Curriculum Framework and the NCERT textbooks. If a
chapter does not look right for your class, prepare it again with different periods —
it costs nothing.

Online payments and invoices are not open yet, so this activation was recorded by
hand. Reply to this mail if anything looks wrong and it will be put right.

— Aruvi
"""
    subject = ("Your Aruvi subscription is active"
               if len(rows) == 1 else "Your Aruvi subscriptions are active")
    return {"subject": subject, "text": text}
