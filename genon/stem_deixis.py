#!/usr/bin/env python3
"""stem_deixis.py — does an item's STEM point at something the item does not carry?

    python3 genon/stem_deixis.py                        # census the whole corpus
    python3 genon/stem_deixis.py mathematics iii        # one subject·grade
    python3 genon/stem_deixis.py --tiers                # census grouped by remedy tier

WHY THIS EXISTS (2026-08-19, S8 · W1, founder-found by reading a served plan).
mathematics III ch 5's Q-A-1 reads *"On the dot grid below, draw a simple rangoli
design…"* and its `visual_stimulus` is `""`. There is no dot grid. The item certified
ALL PASS, and so did forty others like it across english and mathematics.

Nothing in the pipeline could see it. The DECLARED-TYPE GATE (ARV-D-113) validates the
one thing a model DECLARES — the `number_line:` tag — and `assessment_norm.mistyped_tag`
returns None on any input that is not a string carrying that prefix. So an EMPTY
stimulus is, to every existing check, indistinguishable from an item that never wanted
one. The relationship this module tests — between the stem's language and the stimulus
field beside it — is not tested anywhere else.

It is the same shape as C5 check 11: two fields that certification reads separately and
never compares. Check 11 reconciles the registry against the chapter summary; this
reconciles the stem against its own stimulus.

★ THE TEST HAS THREE CONDITIONS, AND THE THIRD IS THE WHOLE ACCURACY OF IT. A first
draft used two (deixis present · stimulus empty) and reported 406 items, most of which
were correct. Measured against the corpus, the misses were all one kind — the material
IS there, inline in the stem, after the pointer:

    "Sort the letters below into three groups…\n\nLetters: A, B, H, V, C, X"
    "Place the numbers into the four boxes below…\n\n___ ÷ ___ = ___"
    "The addition below has a missing digit.\n  4 ☐ 3 + 2 5 8 ------ 7 0 1"
    "Read the line below from the story: 'Come dear hen, let us go to the village fair.'"

Every one of those is a sound, self-contained item. A pointer followed by its referent
is not a dangling pointer, and a gate that fails those gets switched off in a week
(runbook trap 4). So the third condition asks whether anything FOLLOWS the pointer that
could be what it points at.

TWO KINDS, BECAUSE THE REMEDIES DIFFER COMPLETELY.
  * WORKSPACE — the item asks the CHILD to make marks in the named area ("draw on the
    dot grid below", "write in the box below"). Nothing is missing in the content sense;
    the item wants a drawing AREA, which is layout. In 88% of the measured cases the
    item's own `exercise` block already names the textbook page that HAS the grid, so
    the remedy is usually to repoint rather than to draw anything. ADVISORY.
  * FIGURE — the item asks the child to READ something ("the shape below remains",
    "Below is an L-shaped figure"). That is missing content and no layout fixes it.
    GATES.

`above` IS NOT TREATED AS BARE DEIXIS, deliberately. Across this corpus it is
overwhelmingly spatial CONTENT — "a drone flies directly above a school", "one metre
above the floor", "+210 m (above sea level)" — on stages that teach viewpoint and
elevation. Only the phrasal forms ("shown above", "the figure above") are pointers.
Same reasoning as the `clock`-in-quotes and `last term` rulings: narrow the pattern
rather than strike correct teaching to satisfy it.
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLANS = REPO / "data" / "content" / "saved_plans"

FIGURE, WORKSPACE = "figure", "workspace"

# ── condition 1 · the pointer ────────────────────────────────────────────────────
# Bare `below` is a pointer. Bare `above` is not (see the header); only its phrasal
# forms are. `shown here` / `as shown` are pointers in any position.
_DEIXIS = re.compile(
    r"\bbelow\b"
    r"|\bshown (?:here|above)\b"
    r"|\bas shown\b"
    r"|\bthe (?:figure|picture|diagram|drawing|table|grid|image|shape) above\b",
    re.I)

# `below` relative to the CHILD'S OWN work or to a described position is not a pointer
# at the page: "write one sentence below your drawing", "below each number write E".
_NOT_A_POINTER = re.compile(
    r"\bbelow (?:your|you|me|us|each|every|the line you|it|them|this line)\b"
    r"|\b(?:sea level|the floor|the mark|the surface|the water|zero)\b",
    re.I)

# A GEOMETRY LABEL after the word is a POSITION, not a pointer — "the angle formed below q
# on the left of t". Added 2026-08-19 after the Tier-1 dry run proposed rewriting exactly
# that stem (mathematics vii ch 5) into "the angle formed in section 5.8 q", which is the
# repair-writes-nonsense failure the dry run exists to catch. Labels are matched narrowly:
# a capital or a conventional line letter, never a word, so "the line below is 6 cm long"
# is untouched ("is" is neither).
_GEOMETRY_LABEL = re.compile(
    r"\b(?:above|below)\s+(?:line\s+|point\s+|segment\s+)?"
    r"(?:[A-Z]{1,2}\b|[k-np-tx-z]\b)")

# A MEASURED DISTANCE before the word is a position too, and it is the last maths hit:
# "a hole is punched … 2 cm below the fold line" (vi ch 9). Tested on the text BEFORE the
# match, since the quantity always precedes it.
_MEASURED = re.compile(r"\d+(?:\.\d+)?\s*(?:cm|mm|m|km|inch(?:es)?|ft|units?|squares?|"
                       r"steps?|dots?|rows?|floors?)\s*$", re.I)

# ── condition 2 · a locator makes the reference legitimate ──────────────────────
# "the picture below on p.44" points at the book, which the teacher has.
_PAGEREF = re.compile(r"\b(?:p\.\s*\d|pp\.\s*\d|page\s+\d|textbook|your book|section\s+\d"
                      r"|fig\.\s*\d|figure\s+\d+\.\d)", re.I)

# ── condition 4 · the item's own OPTIONS are a referent ─────────────────────────
# Found by running condition 3 over the corpus (2026-08-19): it reported 71 gating hits
# and english dominated them, all of one shape —
#     "Read the statements below and write True or False next to each one."
#     "Choose the correct shape from the four options below."
# — where the statements ARE `options[]`. A TRUE_FALSE item's four numbered options are
# rendered under the stem, so the pointer lands exactly where it should. These are sound
# items and gating them would have been the "fails good chapters" failure again.
#
# But options cannot satisfy every pointer. "The shape below remains" or "Below is an
# L-shaped figure" names something an option list can never be, even on an MCQ. So the
# exemption is refused when the pointer's own noun is VISUAL — decided by the noun
# immediately before the pointer, not by the item's type.
# `arrangement` was in this list and is now out (2026-08-20, W2). It produced the list's
# one false positive: mathematics iii ch 14 p08 Q-A-2 asks "Which arrangement below is
# symmetrical?" and its four options ARE the arrangements — `G G G O G G G O`, `G G G O O
# G G G`, … — bead sequences written as text. The visual-noun override exists to stop an
# options list satisfying a pointer at a real figure, and an arrangement is only sometimes
# one. Every other member of this list names something that cannot be an option.
_VISUAL_NOUN = re.compile(
    r"\b(?:figure|picture|diagram|drawing|image|shape|line|rectangle|square|triangle|"
    r"circle|net|grid|dot\s+grid|clock\s+face|pattern|design|half-rangoli|"
    r"tiles?|frames?|string|garden|room|graph|map|sketch|object)"
    r"\s+(?:shown\s+|drawn\s+|given\s+)?(?:below|above)\b"
    r"|\b(?:below|above)\s+is\s+(?:a|an|the)\s+[\w-]{0,14}\s?"
    r"(?:figure|picture|diagram|drawing|shape|rectangle|square|triangle|circle|net|"
    r"grid|room|garden|row|pattern)\b",
    re.I)


def _options_satisfy(item: dict, stem: str) -> bool:
    """True when the stem's pointer is answered by the item's own rendered options."""
    opts = item.get("options") or []
    if len(opts) < 2:
        return False
    return not _VISUAL_NOUN.search(stem)

# ── condition 3 · is the referent inline, after the pointer? ────────────────────
# Any of: a blank line then content · a colon then a quoted span or a list · an
# enumeration marker · a run of fill-in placeholders · an arithmetic/ASCII block.
_INLINE = re.compile(
    r"\n\s*\S"                                  # a line break followed by content
    r"|:\s*[\"'‘“]"                   # colon then a quoted span
    r"|:\s*\n?\s*(?:\d+[.)]|\([a-z]\)|[-•])"   # colon then an enumeration
    r"|(?:^|\s)(?:\d+[.)]\s+\S.*){2,}"          # two or more numbered items
    r"|:\s*\S+(?:\s*[/,;]\s*\S+){2,}"          # a labelled inline run: "Words: a / b / c"
    r"|_{3,}|□|☐|❑"              # ___ or ☐ placeholders
    r"|\|",                                     # an inline pipe row
    re.S)

# ── the two kinds ───────────────────────────────────────────────────────────────
# WORKSPACE needs BOTH halves, and they are tested independently because they occur in
# either order. "Draw tally marks in the box below" puts the verb first; "Look at the
# dot grid below. Connect the dots…" puts it in the next sentence, and an ordered
# pattern misses the second — which is exactly the item the founder found.
#   _WS_NOUN  the referent is an AREA to be marked, not an object to be read
#   _WS_VERB  the item asks the child to make marks
# "the shape below remains" has the verb nowhere and the noun is not an area → FIGURE.
_WS_NOUN = re.compile(
    r"\bthe\s+(?:dot\s+grid|grid|graph\s+paper|box(?:es)?|space|blank\s+[\w\s]{0,14}?|"
    r"tens\s+frames?|frames?|table|circle)\s+below\b", re.I)
_WS_VERB = re.compile(
    r"\b(?:draw|write|shade|colour|color|trace|mark|place|connect|join|fill|complete|"
    r"sketch|copy|design|create)\b", re.I)


# ── where it GATES, and where it only reports ───────────────────────────────────
# Same asymmetry, and the same reason, as C5 check 11's social_sciences carve-out.
#
# On MATHEMATICS the test is precise: a stem's `below` is a pointer at a figure or a
# workspace, the referent is a visual object, and the four conditions separate the
# populations cleanly — measured over the corpus, every maths hit is real.
#
# On ENGLISH it is not, and iterating further would not make it so. English stems talk
# ABOUT text that is itself full of the word: "the child imagines people below staring
# up", "looking down while people below stare", "what one thing would you most want to
# see below you". And where the referent IS a real list, it lives in a field that varies
# by spine — `options` on a TRUE_FALSE, inline on a WRITING_TASK, in the teacher's own
# reading on an ORAL_PROMPT. A gate that fails a correct poem item gets switched off in
# a week (runbook trap 4), so english returns an ADVISORY shortlist ruled on at C7.
# science / social_sciences / TWAU produce no hits at all: their stimuli are tables,
# which are populated, so condition 2 never fires.
_GATES = ("mathematics",)


def gates_for(subject: str) -> bool:
    return (subject or "").lower() in _GATES


def stem_of(item: dict) -> str:
    return (item.get("prompt") or item.get("item_stem") or "") if isinstance(item, dict) else ""


def _stimulus_empty(item: dict) -> bool:
    vs = item.get("visual_stimulus")
    if item.get("passage"):
        return False                     # extract items carry their own block
    if vs is None:
        return True
    if isinstance(vs, str):
        return not vs.strip()
    return not vs                        # {} / [] count as empty; a populated dict does not


def classify(item: dict):
    """(kind, phrase) if the stem points at an absent stimulus, else None.

    `kind` is FIGURE (gates) or WORKSPACE (advisory)."""
    if not isinstance(item, dict):
        return None
    stem = stem_of(item)
    if not stem or not _stimulus_empty(item):
        return None
    if _PAGEREF.search(stem):
        return None
    m = _DEIXIS.search(stem)
    if not m:
        return None
    tail = stem[max(0, m.start() - 4):m.end() + 24]
    if (_NOT_A_POINTER.search(tail)
            or _GEOMETRY_LABEL.match(stem[m.start():])
            or _MEASURED.search(stem[max(0, m.start() - 20):m.start()])):
        return None
    if _options_satisfy(item, stem):
        return None
    # CONDITION 3 — anything after the pointer that could BE the referent.
    if _INLINE.search(stem[m.end():]):
        return None
    workspace = bool(_WS_NOUN.search(stem)) and bool(_WS_VERB.search(stem))
    return (WORKSPACE if workspace else FIGURE, m.group(0))


def scan_plan(plan: dict):
    """-> [ {id, kind, phrase, stem, book_ref} ] over every item in a saved plan."""
    out = []
    for it in _items(plan):
        got = classify(it)
        if got:
            ex = it.get("exercise") or {}
            out.append({"id": it.get("id"), "kind": got[0], "phrase": got[1],
                        "stem": stem_of(it), "book_ref": ex.get("book_ref") or ""})
    return out


def _items(o):
    if isinstance(o, dict):
        i = o.get("id")
        if isinstance(i, str) and i.startswith("Q-"):
            yield o
        for v in o.values():
            yield from _items(v)
    elif isinstance(o, list):
        for v in o:
            yield from _items(v)


def report(hits, name=""):
    """Human-readable block; returns (n_gating, n_advisory)."""
    gate = [h for h in hits if h["kind"] == FIGURE]
    adv = [h for h in hits if h["kind"] == WORKSPACE]
    if name and hits:
        print(f"\n--- {name}: {len(gate)} figure, {len(adv)} workspace")
    for h in gate + adv:
        tag = "FIGURE" if h["kind"] == FIGURE else "workspace (advisory)"
        print(f"  {h['id']:<12} [{tag}] {h['phrase']!r} — {h['stem'][:90]}")
    return len(gate), len(adv)


# ── remedy tiers (the one-off corpus repair, 2026-08-19) ────────────────────────
# T1 GENERIC   — the item's own `exercise.book_ref` names a page, so the pointer can be
#                repointed at it with no per-item judgement. Derivable → a generic pass.
# T2 DECLARED  — no usable book_ref, but the stem states everything the referent would
#                have shown (dimensions, counts, colours). Strike the pointer. Needs
#                language per item.
# T3 FIGURE    — neither. The item genuinely needs a rendered figure; free repair cannot
#                reach it. Founder ruling or a diagram primitive.
_PAGE_IN_REF = re.compile(r"\b(?:p\.?\s*\d+|pp\.\s*\d+|page\s+\d+|section\s+\d+\.\d+)", re.I)


def tier(hit) -> str:
    if _PAGE_IN_REF.search(hit.get("book_ref") or ""):
        return "T1"
    return "T2" if hit["kind"] == WORKSPACE else "T3"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("subject", nargs="?")
    ap.add_argument("grade", nargs="?")
    ap.add_argument("--tiers", action="store_true")
    a = ap.parse_args()
    pat = str(PLANS / (a.subject or "*") / (a.grade or "*") / "ch_*_canonical*.json")
    files, rows, total = sorted(glob.glob(pat)), [], 0
    for p in files:
        try:
            d = json.loads(Path(p).read_text(encoding="utf-8"))
        except Exception:                                            # noqa: BLE001
            continue
        total += sum(1 for _ in _items(d))
        for h in scan_plan(d):
            h["file"] = os.path.relpath(p, PLANS)
            rows.append(h)
    print(f"files {len(files)} · items {total} · hits {len(rows)} ({len(rows)/max(total,1):.2%})")
    if a.tiers:
        by = collections.Counter(tier(h) for h in rows)
        print(f"\nT1 generic (repoint at the book page) : {by['T1']}")
        print(f"T2 declared (stem is self-sufficient)  : {by['T2']}")
        print(f"T3 figure   (needs a real diagram)     : {by['T3']}")
        for t in ("T1", "T2", "T3"):
            print(f"\n── {t} ──")
            for h in rows:
                if tier(h) == t:
                    print(f"  {h['file']:<34} {h['id']:<12} {h['kind']:<9} "
                          f"ref={(h['book_ref'] or '—')[:28]:<29} {h['stem'][:70]}")
    else:
        for h in rows:
            print(f"  {h['file']:<34} {h['id']:<12} {h['kind']:<9} {h['stem'][:80]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
