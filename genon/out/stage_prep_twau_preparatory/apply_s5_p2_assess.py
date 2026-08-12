#!/usr/bin/env python3
"""S5 · the_world_around_us · preparatory — P2: the assessment constitution, v1.3 → v1.4.

testing.md §3 P2 is two items:

  A6 — a CONFIRMATION, not an amendment. TWAU is 8-rule ROW 8, the
       ITEM-SELF-SUFFICIENT family: the item carries `period_ref[]` directly and
       carries its own `implied_lo` inline; there is no handoff bridge and no
       period-field join. The field is already in the schema, so nothing is added
       to the item — what lands is an ANCHORING block that writes down what
       `period_ref` IS, so a later pass cannot re-read it as decoration. Same shape
       as science·secondary v1.2, science·middle v1.4, maths·middle v3.3 and
       maths·prep v1.3, on this stage's own row.

  A9 — MCQ option order. The REMOVAL half is **N/A**: testing.md names four files
       that carry the MEMORY-item-18 position prohibition (SS + Science, middle and
       secondary) and this is not one — asserted by guard below. So A9 lands as the
       two v1.7 lines alone, and NO arrangement rule may be added.

Nothing pedagogical moves.
"""
from __future__ import annotations

import difflib
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
AS = (ROOT / "data/content/constitutions/assessment/the_world_around_us"
           / "preparatory/assessment_constitution.txt")
OUT = pathlib.Path(__file__).resolve().parent

src = AS.read_text(encoding="utf-8")
before = src

edits: list[tuple[str, str, str]] = []

# ─────────────────────────────────────────────────────────────────────────────
# 1 · VERSION
# ─────────────────────────────────────────────────────────────────────────────
edits.append((
    "VERSION 1.3 → 1.4",
    "ARUVI · CHAPTER ASSESSMENT CONSTITUTION · THE WORLD AROUND US · VERSION 1.3",
    "ARUVI · CHAPTER ASSESSMENT CONSTITUTION · THE WORLD AROUND US · VERSION 1.4",
))

# ─────────────────────────────────────────────────────────────────────────────
# 2 · A6 — the ANCHORING block, appended to Rule 2 (the rule that already binds an
#     item to its period). Confirmation in substance; the block is the record.
# ─────────────────────────────────────────────────────────────────────────────
ANCHORING = '''
ANCHORING (what period_ref is, and what it is not)
period_ref IS the item's anchor to its unit, and TWAU declares it directly — the item
carries the period number it was built from, and carries implied_lo inline beside it.
There is no mediating row: the Coverage Handoff supplies the material, but the platform
never joins through it to find the unit. Emit the period number of the handoff entry
whose implied_lo this item tests, and nothing else.

Where one item legitimately reaches several units, it anchors at the LAST of them. An
item tests its material's whole implied_lo, so it becomes available only when that
material COMPLETES: a class that was not taught all of it cannot be tasked on any of it.

MUST NOT emit a band-level reference of any kind — anchoring is UNIT-level. The
band/phase-level reference of earlier drafts is reversed and MUST NOT be reintroduced.
'''

edits.append((
    "A6 — the ANCHORING block after Rule 2's prohibitions",
    "3. MUST NOT anchor an item to a c_code not present in the COMPETENCY\n"
    "   DESCRIPTIONS block.\n"
    "4. MUST NOT introduce weight tiers or weight-based minimum counts.\n",

    "3. MUST NOT anchor an item to a c_code not present in the COMPETENCY\n"
    "   DESCRIPTIONS block.\n"
    "4. MUST NOT introduce weight tiers or weight-based minimum counts.\n"
    + ANCHORING,
))

# ─────────────────────────────────────────────────────────────────────────────
# 3 · A9 — the two v1.7 lines, in Rule 6 (MCQ DISTRACTOR DESIGN). The removal half
#     is N/A for this file. NO arrangement sentence: naming arrangement at all keeps
#     position salient to a model that should never reason about it (founder, v1.6
#     and v1.7 both).
# ─────────────────────────────────────────────────────────────────────────────
edits.append((
    "A9 — 'order carries no meaning' mandate line",
    "related but incorrect detail from the same chapter section. The guide names what\n"
    "each distractor indicates.\n",
    "related but incorrect detail from the same chapter section. The guide names what\n"
    "each distractor indicates.\n"
    "Option order carries no meaning and is not yours to set: emit the four options in\n"
    "whatever order they were authored, and never let where an option sits influence how\n"
    "it is written. Uneven letters across a chapter are coincidence, not a defect.\n",
))

edits.append((
    "A9 — the by-label option-reference prohibition",
    "PROHIBITION\n"
    "1. MUST NOT use true/false format.\n"
    "2. MUST NOT use distractors that are implausible, arbitrary, or sourced from\n"
    "   outside the chapter.\n",

    "PROHIBITION\n"
    "1. MUST NOT use true/false format.\n"
    "2. MUST NOT use distractors that are implausible, arbitrary, or sourced from\n"
    "   outside the chapter.\n"
    "3. MUST NOT write an option that refers to another option by its label (\"both A\n"
    "   and B\", \"none of the above\", \"all of the above\") — options are ordered\n"
    "   downstream and a label reference would be falsified.\n",
))

# ─────────────────────────────────────────────────────────────────────────────
for name, old, new in edits:
    if old not in src:
        sys.exit(f"ANCHOR MISSING — {name}\n  looked for: {old[:120]!r}")
    if src.count(old) != 1:
        sys.exit(f"ANCHOR NOT UNIQUE ({src.count(old)}×) — {name}")
    src = src.replace(old, new)
    print(f"  applied · {name}")

# ─────────────────────────────────────────────────────────────────────────────
# guards
# ─────────────────────────────────────────────────────────────────────────────
def assert_absent(needle: str, why: str) -> None:
    if needle.lower() in src.lower():
        sys.exit(f"GUARD FAILED — {needle!r} present: {why}")

# A9's REMOVAL is N/A — prove the item-18 prohibition was never here, so "N/A" is a
# measurement and not an assumption.
for bad in ("consecutive", "same label", "vary in position"):
    assert_absent(bad, "MEMORY item 18 — this file never carried it; N/A must stay N/A")

# A9 MUST NOT re-add an arrangement rule.
for bad in ("alphabetic", "never led with", "first word at which they differ",
            "in ascending order", "sort the options"):
    assert_absent(bad, "A9 forbids naming arrangement at all")

# cancelled amendments + V-rules
for bad, why in (("phase_ref", "band-level anchoring is reversed"),
                 ("band_ref", "retired declaration"),
                 ("band_id", "derived positionally by compile v0.5"),
                 ("role_handoff", "A2/A3/A4 cancelled"),
                 ("unit_handoff", "A2/A3/A4 cancelled"),
                 ("section registry", "V2 is brief-carried"),
                 ("synthesis unit", "V3 is brief-carried"),
                 ("reserved token", "V-series, never constitutional")):
    assert_absent(bad, why)

# the two A9 lines landed exactly once each
for needle in ("Option order carries no meaning and is not yours to set",
               "refers to another option by its label"):
    if src.count(needle) != 1:
        sys.exit(f"GUARD FAILED — {needle!r} appears {src.count(needle)}×, expected 1")

# A6 landed and period_ref survived
if src.count("ANCHORING (what period_ref is, and what it is not)") != 1:
    sys.exit("GUARD FAILED — the ANCHORING block did not land exactly once")
if '"period_ref":        array' not in src:
    sys.exit("GUARD FAILED — the period_ref schema line moved or vanished")

AS.write_text(src, encoding="utf-8")

diff = "".join(difflib.unified_diff(
    before.splitlines(keepends=True), src.splitlines(keepends=True),
    fromfile="assessment_constitution.txt (v1.3)",
    tofile="assessment_constitution.txt (v1.4)"))
(OUT / "assess_v1.3_to_v1.4.diff").write_text(diff, encoding="utf-8")

print(f"\nWROTE {AS}")
print(f"WROTE {OUT / 'assess_v1.3_to_v1.4.diff'}")
print("all guards passed")
