#!/usr/bin/env python3
"""summary_sections.py — the chapter summary's own section list, reconciled against a
top canonical's derived registry. Closes batch-runbook trap 5 (2026-08-13).

WHY IT EXISTS. Certification derives the section registry FROM the top canonical, so it
cannot see what the top canonical left out: a section the chapter has and the standard
plan never names is invisible to checks 3, 4 and 5, which all measure the compacts
against that same derived registry. The runbook's standing instruction was "compare the
registry against the chapter summary's section list by eye until that check exists".

It is not hypothetical. The first sweep, before this file gated anything, found
**science·ix ch 8 — the S3 pilot, certified ALL PASS — omitting 8.5 Atomic Number**,
a top-level section its summary carries and no unit of any canonical in the library
anchors. Two TWAU chapters (iii ch 1, iii ch 9) omit their closing `Let us reflect`
section the same way.

THE TWO DIRECTIONS ARE NOT SYMMETRIC — the same design as the handoff/anchor check
(`build_library.py`, 2026-08-08), and for the same kind of reason:

  a summary section NO canonical anchors     ->  GATE. The chapter is not taught. No
      teacher gets that content at any period count, and serving cannot recover it
      because it was never authored. Unlike a register breach it is not repairable in
      place, so the honest verdict is that the chapter is not releasable.

  a registry entry the summary never names   ->  ADVISORY, never a gate. Legitimate on
      real files: SS opens with an unlabelled introduction the plan quite properly names
      ("Introduction to the Atmosphere"), and a plan may reasonably merge or rename.

SUB-SECTIONS ARE COVERED BY THEIR PARENT. A science summary carries 8.2.1 under 8.2; a
plan that anchors 8.2 has taught it. A numbered section is covered if its own ref or any
ANCESTOR ref is in the registry — which is what leaves 8.5 as the only real miss on ch 8
out of the six numbered entries the registry does not name. A top-level ref has NO
parent: "8.5".rsplit(".") is the CHAPTER number, and treating it as an ancestor made the
first draft of this file pass ch 8 — every section is "covered" by chapter 8.

WHERE IT GATES, AND WHERE IT ONLY ADVISES. Measured over the whole installed corpus
before it was wired in:

    structured, and therefore GATED
      mathematics · english · the_world_around_us   .json  sections[] / main_sections[]
      science                                       .txt   numbered headings (8.1, 8.2.1)

    prose, and therefore ADVISORY
      social_sciences (both stages)                 .txt   no structural section marker

Social science summaries declare their sections differently in every chapter — "Title:
This section explains…" in IX ch 3, "Plate Tectonics presents…" in IX ch 2, a bare
heading paragraph in VIII ch 3 — because each is an independent generation. Every
extractor tried on them recovered the real sections AND sub-topics ("Waterfall",
"Deltas", "GLOFs" under Running Water), so a gate would have failed good chapters on its
first run and been switched off within a week (runbook trap 4: a false positive is fixed
at the scanner, not in the text). What it does instead is reduce "compare by eye" from a
whole summary to a shortlist of one to ten leads. The real fix is upstream — a section
list in the SS chapter-summary prompt's output — and until then this is what is honest.

Usage:
    python3 genon/summary_sections.py                    # sweep every installed library
    python3 genon/summary_sections.py science ix 8       # one chapter
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

from aruvi_core.genon.serve import _norm                                # noqa: E402

# "8.2.1 Thomson's model of an atom" on its own line.
_NUMBERED = re.compile(r"^\s*(\d+(?:\.\d+)+)[.)]?\s+(\S.*?)\s*$")

# A ref token rather than a title: "4.1", "8.2.1", "S1". Matched by boundary, not by
# containment — "8.1" must not be satisfied by a registry entry reading "8.1.2".
_REF = re.compile(r"^[a-z]?\d+(\.\d+)*$")

# The prose lead forms social_sciences summaries actually use, in the order they are
# tried. Advisory only — see the module docstring.
_VERB = (r"(?:presents|introduces|explains|describes|defines|details|examines|traces|"
         r"discusses|covers|frames|illustrates|consolidates|distinguishes|names|notes|"
         r"argues|opens|closes|outlines|explores|establishes|focuses|considers|"
         r"highlights|shows|lists|compares)")
_LEADS = (
    re.compile(r"^(?P<t>[A-Z][^:\n]{2,88}):\s+(?=[A-Z(\"'])"),          # Title: body
    re.compile(r"^(?P<t>[A-Z][^\n]{2,88})\n(?=\S)"),                    # Title \n body
    re.compile(r"^(?P<t>[A-Z][A-Za-z0-9'’\-,&()\. ]{2,70}?)\s+" + _VERB + r"\b"),
)
# Leads that are the document talking about itself, not naming a section.
_NOT_A_SECTION = re.compile(r"^(?:chapter\s|the chapter\b|this chapter\b|it \b)", re.I)

STRUCTURED, PROSE, NONE = "structured", "prose", "none"


def _entry(key, label, parent=None):
    return {"key": _norm(key), "label": str(label), "parent": _norm(parent) if parent else None}


def _parent_ref(ref):
    """The parent SECTION of a ref, or None. `8.2.1` -> `8.2`; `8.5` -> None (its
    "parent" is the chapter, and a chapter is not a section anything can anchor)."""
    ref = str(ref)
    return ref.rsplit(".", 1)[0] if ref.count(".") >= 2 else None


# ── extraction ────────────────────────────────────────────────────────────────

def _from_json(doc):
    out = []
    # english: the axis a plan anchors is the SPINE CELL, not the section. A post-split
    # chapter is ONE main_section, so a section-level list would carry one entry and
    # reconcile against six registry cells — vacuous exactly where the item-density
    # analysis says english is thinnest.
    for ms in doc.get("main_sections") or []:
        sid = ms.get("section_id") or ms.get("title") or "?"
        spines = ms.get("spines")
        if isinstance(spines, dict) and spines:
            out += [_entry(f"{sid}|{sp}", f"{sid}|{sp}") for sp in spines]
        else:
            out.append(_entry(ms.get("title") or sid, ms.get("title") or sid))
    if out:
        return out

    for s in doc.get("sections") or []:
        if not isinstance(s, dict):
            continue
        ref, title = s.get("ref"), s.get("title")
        key = ref or title                    # maths anchors the ref; TWAU the title
        if not key:
            continue
        out.append(_entry(key, f"{ref} {title}".strip() if ref else title,
                          _parent_ref(ref) if ref else None))
    return out


def _from_prose(text):
    """(entries, kind). Numbered headings are structural; leads are advisory."""
    numbered = []
    for ln in text.splitlines():
        m = _NUMBERED.match(ln)
        # A heading is a SHORT line of its own; a paragraph opening "8.1 of the
        # syllabus covers…" is not one. Every real heading measured is under 90 chars.
        if m and len(ln.strip()) <= 90:
            numbered.append(_entry(m.group(1), f"{m.group(1)} {m.group(2)}",
                                   _parent_ref(m.group(1))))
    if len(numbered) >= 2:
        return numbered, STRUCTURED

    out, seen = [], set()
    for para in re.split(r"\n\s*\n", text):
        para = para.strip()
        for pat in _LEADS:
            m = pat.match(para)
            if not m:
                continue
            lead = m.group("t").strip()
            if _NOT_A_SECTION.match(lead) or _norm(lead) in seen:
                break
            seen.add(_norm(lead))
            out.append(_entry(lead, lead))
            break
    return out, (PROSE if out else NONE)


def summary_sections(subject, grade, chapter):
    """(entries, kind) — the summary's section list and how confidently it was read.

    A missing or unreadable summary returns ([], NONE) rather than raising: it must not
    fail a chapter for a reason that is not about the chapter. The reconciler reports it."""
    from prompt_assembly import resolve_paths                            # noqa: PLC0415

    try:
        p = Path(resolve_paths(str(grade), str(subject), int(chapter))["chapter_summary"])
    except Exception:                                                    # noqa: BLE001
        return [], NONE
    if not p.exists():
        return [], NONE
    if p.suffix == ".json":
        try:
            got = _from_json(json.loads(p.read_text(encoding="utf-8")))
        except Exception:                                                # noqa: BLE001
            return [], NONE
        return got, (STRUCTURED if got else NONE)
    try:
        return _from_prose(p.read_text(encoding="utf-8"))
    except Exception:                                                    # noqa: BLE001
        return [], NONE


# ── reconciliation ────────────────────────────────────────────────────────────

def _match(key, reg):
    """Is `key` named by any registry entry? Refs by boundary, titles by containment."""
    if _REF.match(key or ""):
        return any(a == key or (a.startswith(key) and not a[len(key):len(key) + 1].isdigit()
                                and a[len(key):len(key) + 1] != ".")
                   for a in reg)
    return any(key and (key in a or a in key) for a in reg)


def reconcile(registry, sections):
    """(missing, extra). `missing` gates where the read is STRUCTURED; `extra` never does."""
    reg = [_norm(a) for a in registry]
    named = {a for s in sections for a in reg if _match(s["key"], [a])}
    direct = {s["key"] for s in sections if _match(s["key"], reg)}

    missing = []
    for s in sections:
        if s["key"] in direct:
            continue
        anc, hit = s["parent"], False
        while anc and not hit:
            hit = anc in direct or _match(anc, reg)
            anc = _parent_ref(anc)
        if not hit:
            missing.append(s["label"])
    return missing, [a for a, n in zip(registry, reg) if n not in named]


# ── sweep (development instrument; certification calls the two functions above) ─

def _sweep(argv):
    from aruvi_core.genon import compile_stream                          # noqa: PLC0415
    from aruvi_core.genon.carriers import has_section_axis               # noqa: PLC0415
    from aruvi_core.genon.serve import section_registry                  # noqa: PLC0415

    root = REPO / "data" / "content" / "saved_plans"
    tops = ([root / argv[0] / argv[1] / f"ch_{int(argv[2]):02d}_canonical.json"]
            if len(argv) == 3 else sorted(root.glob("*/*/ch_*_canonical.json")))
    gated = advisory = 0
    for p in tops:
        subj, gr = p.parts[-3], p.parts[-2]
        ch = int(re.search(r"ch_(\d+)", p.name).group(1))
        tag = f"{subj}/{gr}/ch{ch:02d}"
        try:
            reg = section_registry(compile_stream(json.loads(p.read_text())))
        except Exception as e:                                           # noqa: BLE001
            print(f"  ERR  {tag}: {e}")
            continue
        if not has_section_axis(subj, gr):
            print(f"  n/a  {tag}: no section axis")
            continue
        secs, kind = summary_sections(subj, gr, ch)
        if kind == NONE:
            print(f"  ??   {tag}: no section list readable from the summary")
            continue
        missing, extra = reconcile(reg, secs)
        gated += bool(missing and kind == STRUCTURED)
        advisory += bool(missing and kind == PROSE)
        flag = ("FAIL" if kind == STRUCTURED else "ADVS") if missing else "ok  "
        print(f"  {flag} {tag} [{kind}]: {len(secs)} summary / {len(reg)} registry"
              + (f"  UNNAMED: {missing}" if missing else "")
              + (f"  (+{len(extra)} registry-only)" if extra else ""))
    print(f"\ngating failures: {gated}   ·   advisory hits: {advisory}   of {len(tops)}")


if __name__ == "__main__":
    _sweep(sys.argv[1:])
