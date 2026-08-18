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


# ── declared waivers (2026-08-17, S3 human gate) ─────────────────────────────
# Check 11's FAIL is repairable only by a re-author or a HUMAN RULING — and until this
# table existed the ruling had nowhere to live that certification could read, so every
# future run re-raised a decided question as a fresh FAIL (and a genuinely NEW omission
# would have had to be spotted among familiar ones). Same doctrine as every repair tool:
# declared in code with its evidence, keyed exactly, never computed. A waived section
# reports as a WAIVED line, not a FAIL, and does not gate; anything not in this table
# fails exactly as before.
#
# THE S3 PATTERN, for the record (all seven rulings, founder, 2026-08-17): not one was a
# teaching gap. science·secondary's authoring style anchors at the SUBSECTION level and
# merges small sections into dense units, so a parent heading ("5.3 Methods of
# Separation") or a merged section's label ("13.3.2 Carbon cycle", taught inside the
# water+carbon unit) goes unnamed while its content is verifiably present. The one real
# loss in the whole wave: ch 4's two-sentence oscillatory-motion mention.
#
# keyed (subject, grade, chapter) -> {summary section LABEL (verbatim): ruling}
SECTION_WAIVERS = {
    ("science", "ix", 4): {
        "4.1 Motion in a Straight Line":
            "parent heading; children 4.1.1-4.1.4 anchored U1-U4; only the intro's "
            "oscillatory-motion mention is absent (the wave's one real loss)",
        "4.2 Graphical Representation of Motion":
            "parent heading; children 4.2.1-4.2.3 anchored U5-U7 + revisits U17-U18",
    },
    ("science", "ix", 5): {
        "5.3 Methods of Separation of Homogeneous Mixtures":
            "bare parent heading, no body text; children anchored U6-U9, U15",
        "5.4 How Can We Separate the Components of Heterogeneous Mixtures?":
            "bare parent heading, no body text; children anchored U10-U13",
    },
    ("science", "ix", 7): {
        "7.4 Mechanical Energy":
            "parent heading (one definitional paragraph); children taught across 8 "
            "units, 'mechanical energy' 36x in the plan",
    },
    ("science", "ix", 8): {
        "8.5 Atomic Number":
            "content distributed: Z defined and used in U7 (Symbols, 4x), U8 (Mass "
            "Number, 3x), U9, U11; only the label is unanchored (ruled 2026-08-17, "
            "closing the 2026-08-13 pilot finding)",
    },
    ("science", "ix", 10): {
        "10.6 Characteristics of a Sound Wave":
            "bare parent heading; children anchored U8-U11 + revisit U17",
    },
    ("science", "ix", 11): {
        "11.5 Reproduction in Human Beings":
            "block compressed into U12-U14; model documented the merge in its own "
            "teacher notes",
        "11.5.1 Reproductive maturity":
            "overview paragraph; gametogenesis U12, 'from puberty' U13, maturity U14",
        "11.5.3 What are the parts of the female reproductive system?":
            "taught U12 band 2 (ovaries, oviducts, uterus, cervix, vagina, labelled)",
        "11.5.4 How are reproductive cells made?":
            "taught U12 band 3 (meiosis in testes/ovaries, sperm-egg comparison)",
        "11.5.6 What happens when an egg is not fertilised?":
            "taught U13 bands 2+4 (full menstrual-cycle diagram, causal sequence)",
        "11.5.8 Mother's health during pregnancy":
            "taught U14 band 2 (diet, check-ups, rest, avoidance list)",
        "11.5.9 What does it mean to be sexually mature?":
            "taught U14 band 3 (biological vs emotional maturity)",
        "11.5.10 How can unwanted pregnancies and infections be prevented?":
            "taught U14 band 4 (barrier/hormonal/IUD/surgical, STI prevention)",
    },
    ("science", "ix", 13): {
        "13.3 Biogeochemical Cycles":
            "opening paragraph read aloud in U6 band 1; four cycles taught U6-U7",
        "13.3.2 Carbon cycle":
            "taught U6 bands 3-5 (fast/slow cycle, ocean CO2 reasoning)",
        "13.3.4 Oxygen cycle":
            "taught U7 bands 4-5 (respiration/combustion/photosynthesis balance table)",
    },
}


def section_waivers(subject, grade, chapter):
    """The declared accepted-omission rulings for one chapter ({} when none)."""
    return SECTION_WAIVERS.get((str(subject), str(grade), int(chapter)), {})


# ── reconciliation ────────────────────────────────────────────────────────────

def _match(key, reg):
    """Is `key` named by any registry entry? Refs by boundary, titles by containment."""
    if _REF.match(key or ""):
        return any(a == key or (a.startswith(key) and not a[len(key):len(key) + 1].isdigit()
                                and a[len(key):len(key) + 1] != ".")
                   for a in reg)
    return any(key and (key in a or a in key) for a in reg)


def reconcile(registry, sections, closing_anchors=()):
    """(missing, closing, extra).

    `missing` gates where the read is STRUCTURED. `closing` and `extra` never gate.

    THE SYNTHESIS UNIT IS NOT IN THE REGISTRY, AND ON HALF THE STAGES IT TEACHES A REAL
    SECTION (2026-08-13, the first sweep's two TWAU hits). `section_registry` skips that
    unit deliberately — it is the one unit whose only prior is full coverage, so it must
    never enter first-visit arithmetic. But skipping it is not the same as it teaching
    nothing: on a MEDIATED-anchor stage its `section_anchor` is whatever its period fields
    yielded, and measured over the corpus that is a real section on **every** TWAU,
    mathematics and english canonical ("Let us reflect", "S1 / S2 / … / S8",
    "A|reading_for_comprehension / A|beyond_text"), and the reserved token only on the
    token-carrying stages. So TWAU iii ch 1 and ch 9 were reported as omitting "Let us
    reflect" when their closing unit anchors exactly that and teaches its tasks —
    the word-search, the weekly health table, the day circle, all present in the unit.

    A section reached ONLY through the closing unit is therefore taught, and is reported
    in `closing` rather than passed silently: it is the difference between "the chapter
    covers this" and "a unit of the body covers this", and the human gate reads the
    standard's synthesis unit in full anyway. `science·ix ch 8` is unaffected — its
    synthesis unit carries the reserved token, so `8.5 Atomic Number` stays a failure."""
    reg = [_norm(a) for a in registry]
    clo = [_norm(a) for a in closing_anchors if _norm(a) != "synthesis"]
    named = {a for s in sections for a in reg if _match(s["key"], [a])}
    direct = {s["key"] for s in sections if _match(s["key"], reg)}
    by_closing = {s["key"] for s in sections
                  if s["key"] not in direct and _match(s["key"], clo)}

    missing, closing = [], []
    for s in sections:
        if s["key"] in direct:
            continue
        if s["key"] in by_closing:
            closing.append(s["label"])
            continue
        anc, hit = s["parent"], False
        while anc and not hit:
            hit = (anc in direct or anc in by_closing
                   or _match(anc, reg) or _match(anc, clo))
            anc = _parent_ref(anc)
        # A PARENT IS TAUGHT THROUGH ITS CHILDREN (2026-08-18, maths·IX W1). The walk above
        # runs one way only — a child is covered when its parent is anchored — and the
        # reverse case was simply never met until maths ix ch 7, whose "7.3 Elements of
        # Probability: Sample Spaces and Events" is a CONTAINER: its whole content is
        # 7.3.1 Sample Space and 7.3.2 Events, anchored at U7 and U8. Teaching a container
        # as its constituents is correct pedagogy, and demanding a separate unit for the
        # heading would be the gate dictating structure. Required: EVERY child the summary
        # lists is covered — one anchored child of three does not carry the parent.
        #
        # KNOWN COST, recorded rather than hidden (verification pass, 2026-08-18): a
        # children-only test cannot see a parent's OWN body text. science·ix ch 4 carries a
        # declared SECTION_WAIVER saying exactly that — "only the intro's oscillatory-motion
        # mention is absent (the wave's one real loss)" — and this rule now subsumes that
        # waiver, so six of the seven declared waivers stop surfacing in the sweep. A future
        # chapter with the same shape and a genuinely untaught parent paragraph will read ok.
        # The waiver table is the remaining record; the human gate is the remaining reader.
        if not hit:
            kids = [t["key"] for t in sections if t["parent"] == s["key"]]
            hit = bool(kids) and all(k in direct or k in by_closing for k in kids)
        if not hit:
            missing.append(s["label"])
    return missing, closing, [a for a, n in zip(registry, reg) if n not in named]


# ── sweep (development instrument; certification calls the two functions above) ─

def closing_anchors(stream, raw=None):
    """The STANDARD's synthesis unit's own anchors — taught, but not in the registry.

    v1.1, 2026-08-18 (maths·IX W1): on a TOKEN-CARRYING stage the synthesis unit's anchor
    is the reserved word `synthesis` and nothing else, so this returned nothing and a
    wrap-up section taught there read as omitted (maths ix ch 3 "3.7 Conclusion", whose
    teaching is U17's closing band: "Section 3.7 open question: the teacher poses √(-1)").
    On those stages the `coverage_handoff` is the ONLY place the synthesis unit can declare
    what it teaches, so a row that routes a section to it is read as an anchor here.

    THIS DOES NOT WEAKEN THE CHECK, and that was tested before it was written: science·ix
    ch 8 — the chapter this check was built for, which omitted `8.5 Atomic Number` from an
    already-certified library — has exactly one handoff row touching its synthesis unit and
    that row's `section_ref` is the literal string "synthesis". No row claims 8.5. It stays
    a failure. Only a section the handoff NAMES as taught in the closing unit is recognised.
    """
    from aruvi_core.genon.serve import _unit_anchors, is_synthesis_unit  # noqa: PLC0415

    out = [a for u in stream["units"] if is_synthesis_unit(u) for a in _unit_anchors(u)]
    if raw is None:
        return out
    synth = {u["unit"] for u in stream["units"] if is_synthesis_unit(u)}
    for e in ((raw.get("result") or {}).get("coverage_handoff") or []):
        if not isinstance(e, dict):
            continue
        ref = e.get("section_ref") or e.get("section_label") or e.get("section_title") or ""
        pns = {int(p) for p in (e.get("period_numbers") or []) if p is not None}
        if ref and _norm(ref) != "synthesis" and pns and pns <= synth:
            out.append(ref)
    return out


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
            raw = json.loads(p.read_text())
            top = compile_stream(raw)
            reg, clo = section_registry(top), closing_anchors(top, raw)
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
        missing, closing, extra = reconcile(reg, secs, clo)
        gated += bool(missing and kind == STRUCTURED)
        advisory += bool(missing and kind == PROSE)
        flag = ("FAIL" if kind == STRUCTURED else "ADVS") if missing else "ok  "
        print(f"  {flag} {tag} [{kind}]: {len(secs)} summary / {len(reg)} registry"
              + (f"  UNNAMED: {missing}" if missing else "")
              + (f"  [closing unit teaches: {closing}]" if closing else "")
              + (f"  (+{len(extra)} registry-only)" if extra else ""))
    print(f"\ngating failures: {gated}   ·   advisory hits: {advisory}   of {len(tops)}")


if __name__ == "__main__":
    _sweep(sys.argv[1:])
