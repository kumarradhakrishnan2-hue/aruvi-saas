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

Anything that breaks that shape raises ConsentDocumentError at read time rather than
serving a half-document — a consent screen missing a tick is worse than a 500, because
nobody would notice.
"""
from __future__ import annotations

import os
import re
from typing import Any, Dict, List, Optional

from .config import DATA_DIR

DOCUMENT_ID = "consent_and_disclaimer"
LANGUAGE = "en"          # English governs until certified translations exist (§ front matter)
FINAL_ACK_ID = "final"

_FILE_RE = re.compile(r"^consent_and_disclaimer_v([0-9][0-9.]*)\.md$")
# "### ☐ 1. Aruvi is a teaching aid — …"  (the box may be ☐ or ☑ in a future draft)
_ACK_RE = re.compile(r"^###\s+[☐☑]\s*(\d+)\.\s*(.+?)\s*$")
_FINAL_RE = re.compile(r"^###\s+[☐☑]\s*(.+?)\s*$")
_AGREE_LINE = "**I understand and agree.**"


class ConsentDocumentError(RuntimeError):
    """The document on disk is missing or does not have the expected shape."""


def _legal_dir() -> str:
    return os.path.join(DATA_DIR, "legal")


def _version_key(v: str) -> tuple:
    """"0.10" sorts above "0.9" — compare part by part, not as text."""
    return tuple(int(p) for p in v.split(".") if p.isdigit())


def available_versions() -> List[str]:
    """Every published version on disk, oldest first."""
    try:
        names = os.listdir(_legal_dir())
    except OSError:
        return []
    out = [m.group(1) for m in (_FILE_RE.match(n) for n in names) if m]
    return sorted(out, key=_version_key)


def current_version() -> str:
    """The version a teacher signing today must accept — the highest published."""
    vs = available_versions()
    if not vs:
        raise ConsentDocumentError(
            f"No consent document found in {_legal_dir()} "
            f"(expected consent_and_disclaimer_v{{version}}.md).")
    return vs[-1]


def _read(version: str) -> str:
    path = os.path.join(_legal_dir(), f"consent_and_disclaimer_v{version}.md")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError as exc:
        raise ConsentDocumentError(f"Consent document v{version} is not readable.") from exc


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
            if in_final:
                m = _FINAL_RE.match(s)
                if m and not final_text:
                    final_text = m.group(1)
                continue        # nothing after the final tick but the draft footer
            agreement.append(ln)
            continue

    close_ack()

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
    }
    _cache[version] = doc
    return doc


def acknowledgement_ids(version: Optional[str] = None) -> List[str]:
    """The ids every acceptance must carry — the five, in order. The final tick is
    recorded separately (it accepts the body, not one point)."""
    return [a["id"] for a in load_consent_document(version)["acknowledgements"]]
