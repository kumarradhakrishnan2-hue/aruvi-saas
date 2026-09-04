"""The user agreement, read from disk and cut into the shape the UI ticks (2026-08-27).

ONE SOURCE, TWO SURFACES. `data/cloud/content/legal/consent_and_disclaimer_v{V}.md` is
the founder's document, and it is the only copy: the subscribe wizard's Agreement step
and Settings › Legal both render THIS text, parsed, never a re-typed summary. A legal
document that exists twice is a legal document that will disagree with itself, and the
half a teacher ticked is the half that binds.

It lives under DATA_DIR (Bucket A-serve, CLAUDE.md §7) and not under docs/ or
data/authoring/, for a plain reason: the runtime serves it to every teacher before she
pays, so it must travel inside the migration unit. It is shared, read-only, versioned
content — exactly what Bucket A is.

**The version is the filename.** `..._v0.1.md` → "0.1". That is deliberate: publishing a
new version is dropping a new FILE beside the old one, never editing text a teacher has
already accepted. Her consent record names the version she saw, so the file she saw must
still exist to be shown back to her. `current_version()` picks the highest on disk; older
files stay readable by `load_consent_document("0.1")`.

**What the parser expects** (the document's own shape — see the file):

    > blockquote           founder/legal-review notes — DROPPED, never shown to a teacher
    ## Before you subscribe …
    *intro paragraph*
    ### ☐ 1. Title         one of the five acknowledgements …
    body …
    **I understand and agree.**        … each ending on this line
    ---
    ---
    # Full User Agreement …            the body the final tick accepts
    ## Final acknowledgement
    ### ☐ I have read …                the sixth tick
    ## Optional                        …and, from v0.4, anything below this heading
    ### ☐ Send me occasional emails …  the OPTIONAL tick — never one of the six

Anything that breaks that shape raises ConsentDocumentError at read time rather than
serving a half-document — a consent screen missing a tick is worse than a 500, because
nobody would notice.

★ THE OPTIONAL TICK IS NOT AN ACKNOWLEDGEMENT (founder, 2026-09-04). Marketing consent is
parsed into its own `optional` slot and never into `acknowledgements`, for reasons that
are legal before they are structural: DPDP §6 requires consent to be free, specific and
unconditional, so a marketing choice may not gate the service. Everything in `acks` is
mandatory by construction — Agreement.jsx computes `allTicked` from it and the five-box
tally counts it — so putting marketing there would bundle it into the accept button, which
is the exact thing the law forbids. It is also the reason the five-count guard below stays
at 5 and must not be relaxed to "5 or 6": the guard is what would catch someone quietly
promoting an optional term into a required one.

Its ANSWER is stored on the Account (withdrawable, erased with her), never in the retained
consent ledger — see POST /legal/consent in api/main.py.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

DOCUMENT_ID = "consent_and_disclaimer"
LANGUAGE = "en"          # English governs until certified translations exist (§ front matter)
FINAL_ACK_ID = "final"
# The optional marketing tick (v0.4+). Deliberately not in `acknowledgement_ids()` — an
# acceptance is valid whether or not this was ticked.
OPTIONAL_ID = "marketing_email"

_FILE_RE = re.compile(r"^consent_and_disclaimer_v([0-9][0-9.]*)\.md$")
# "### ☐ 1. Aruvi is a teaching aid — …"  (the box may be ☐ or ☑ in a future draft)
_ACK_RE = re.compile(r"^###\s+[☐☑]\s*(\d+)\.\s*(.+?)\s*$")
_FINAL_RE = re.compile(r"^###\s+[☐☑]\s*(.+?)\s*$")
_AGREE_LINE = "**I understand and agree.**"


class ConsentDocumentError(RuntimeError):
    """The document on disk is missing or does not have the expected shape."""


# ★ Reads go through the Storage port (2026-08-29), like every other Bucket A read.
# The agreement is content the runtime serves to every teacher before she pays, so it
# travels inside the migration unit and belongs behind the same seam as the library —
# it was reading DATA_DIR directly for the same reason api/data.py was: the port had no
# way to list, and listing is how a published version is discovered.
_LEGAL_PREFIX = "legal"


def _version_key(v: str) -> tuple:
    """"0.10" sorts above "0.9" — compare part by part, not as text."""
    return tuple(int(p) for p in v.split(".") if p.isdigit())


def available_versions() -> List[str]:
    """Every published version in the content store, oldest first."""
    from . import data
    names = [k.rsplit("/", 1)[-1]
             for k in data.storage().list_prefix(_LEGAL_PREFIX, ".md")]
    out = [m.group(1) for m in (_FILE_RE.match(n) for n in names) if m]
    return sorted(out, key=_version_key)


def current_version() -> str:
    """The version a teacher signing today must accept — the highest published."""
    vs = available_versions()
    if not vs:
        raise ConsentDocumentError(
            f"No consent document found under {_LEGAL_PREFIX}/ "
            f"(expected consent_and_disclaimer_v{{version}}.md).")
    return vs[-1]


def _read(version: str) -> str:
    from . import data
    text = data.storage().get_text(
        f"{_LEGAL_PREFIX}/consent_and_disclaimer_v{version}.md")
    if text is None:
        raise ConsentDocumentError(f"Consent document v{version} is not readable.")
    return text


def _strip(lines: List[str]) -> str:
    """Join a block back into markdown, trimmed of the blank lines and bare `---` rules
    that separated it from its neighbours in the file. Those rules divide the DOCUMENT;
    the UI draws its own boundaries, so a leading or trailing one is just a stray line."""
    def junk(s: str) -> bool:
        return (not s.strip()) or s.strip() == "---"
    while lines and junk(lines[0]):
        lines.pop(0)
    while lines and junk(lines[-1]):
        lines.pop()
    return "\n".join(lines)


_cache: Dict[str, Dict[str, Any]] = {}


def load_consent_document(version: Optional[str] = None) -> Dict[str, Any]:
    """The parsed document. Cached per version in-process — the file only changes when
    the founder publishes a new one, and a new one is a new filename."""
    version = version or current_version()
    if version in _cache:
        return _cache[version]

    raw = _read(version)
    # The `> …` front matter is a note to the LAWYER (placement, review status, what to
    # record). Showing it to a teacher would be showing her the scaffolding.
    body = [ln for ln in raw.splitlines() if not ln.lstrip().startswith(">")]

    intro: List[str] = []
    acks: List[Dict[str, Any]] = []
    agreement: List[str] = []
    final_text = ""

    section = "head"            # head → intro → acks → agreement
    cur: Optional[Dict[str, Any]] = None
    cur_body: List[str] = []
    in_final = False
    in_optional = False
    optional_text = ""

    def close_ack() -> None:
        nonlocal cur, cur_body
        if cur is not None:
            cur["body"] = _strip(cur_body)
            acks.append(cur)
        cur, cur_body = None, []

    for ln in body:
        s = ln.strip()

        if s.startswith("## Before you subscribe"):
            section = "intro"
            continue
        if s.startswith("# Full User Agreement"):
            close_ack()
            section = "agreement"
            continue
        if s.startswith("## Final acknowledgement"):
            in_final = True
            continue
        # ★ v0.4: everything below "## Optional" is the marketing tick, which is NOT one
        #   of the six. Absent in v0.1–v0.3, so `optional` is simply None there and every
        #   already-signed version keeps parsing exactly as it did.
        if s.startswith("## Optional"):
            in_final = False
            in_optional = True
            continue

        if section == "intro":
            m = _ACK_RE.match(s)
            if m:
                close_ack()
                section = "acks"
                cur = {"id": f"ack{m.group(1)}", "n": int(m.group(1)), "title": m.group(2)}
                continue
            intro.append(ln)
            continue

        if section == "acks":
            m = _ACK_RE.match(s)
            if m:
                close_ack()
                cur = {"id": f"ack{m.group(1)}", "n": int(m.group(1)), "title": m.group(2)}
                continue
            if s == _AGREE_LINE or s == "---":
                continue        # the tick's own label; the UI draws the checkbox
            cur_body.append(ln)
            continue

        if section == "agreement":
            if in_optional:
                m = _FINAL_RE.match(s)
                if m and not optional_text:
                    optional_text = m.group(1)
                continue
            if in_final:
                m = _FINAL_RE.match(s)
                if m and not final_text:
                    final_text = m.group(1)
                continue        # nothing after the final tick but the draft footer
            agreement.append(ln)
            continue

    close_ack()

    # ★ STAYS AT 5 — do not relax this to "5 or 6" when the optional tick is present.
    #   The optional tick is parsed elsewhere precisely so that this guard keeps meaning
    #   what it means: it is what would catch an optional term being quietly promoted
    #   into a required one, which for a marketing consent is a DPDP §6 violation.
    if len(acks) != 5:
        raise ConsentDocumentError(
            f"Consent document v{version} has {len(acks)} acknowledgements; expected 5. "
            "The five ticks are the document's contract with the UI — fix the document "
            "or update api/legal.py deliberately.")
    if not final_text:
        raise ConsentDocumentError(
            f"Consent document v{version} has no final acknowledgement line.")

    doc = {
        "document_id": DOCUMENT_ID,
        "version": version,
        "language": LANGUAGE,
        "title": "User Agreement & Disclaimer",
        "intro": _strip(intro),
        "acknowledgements": acks,
        "agreement": _strip(agreement),
        "final": {"id": FINAL_ACK_ID, "text": final_text},
        # None on v0.1–v0.3 (they have no "## Optional" section). The UI renders the
        # box only when this is present, so an older version shows exactly what it did.
        "optional": ({"id": OPTIONAL_ID, "text": optional_text} if optional_text else None),
    }
    _cache[version] = doc
    return doc


def acknowledgement_ids(version: Optional[str] = None) -> List[str]:
    """The ids every acceptance must carry — the five, in order. The final tick is
    recorded separately (it accepts the body, not one point)."""
    return [a["id"] for a in load_consent_document(version)["acknowledgements"]]
