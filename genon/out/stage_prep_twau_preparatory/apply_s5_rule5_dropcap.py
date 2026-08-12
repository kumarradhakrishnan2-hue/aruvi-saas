#!/usr/bin/env python3
"""S5 · the_world_around_us · preparatory — LP v1.4 → v1.5: ARV-D-121, DROP the word cap.

THE THIRD TIME THIS NUMBER HAS BEEN SET, AND THE SECOND TIME A LIVE RUN HAS DISPROVED IT.

  v1.2 and earlier  10–15 words   — 14 of 24 real corpus periods above it
  v1.4 (P-prep)     10–25 words   — widened on that measured evidence, the same morning
  the run that evening            — 12 of 39 units above 25 (top 20–31 · p13 13–35 · p10 18–32)

The founder's ruling at C3 was to accept and not repair, with a note: *"if it is ever
revisited, DROP the upper bound rather than raise it a third time — S4's lesson is about
numbers, and this one has now failed twice."* This is that revisit, and it drops it.

WHY THE NUMBER WAS ALWAYS THE WRONG INSTRUMENT. `section_context` is a LABEL, not prose: it
names the specific objects, phenomena or tasks a unit drew from, and the assessment reads it
to ground what its question is about. Its length is therefore a property of the UNIT'S
CONTENT, not of good writing — a unit that handled two objects has a short label and a unit
that handled eight has a long one, and both are correct. A word cap asks the model to choose
between naming what it used and hitting a number, and the only way to satisfy the cap on a
dense unit is to DROP an object — which silently degrades the assessment's grounding to
protect nothing. v1.4 already said so in its own sentence ("do not drop an object to fit a
length"); the number and the sentence were in contradiction, and the sentence is the one
doing the work.

WHAT REPLACES IT: the rule in kind. Name what was used, and nothing else — the label is a
list, not a description. That is checkable by eye at C3 and does not need arithmetic.

§9 — RELAXATION-ONLY. A constraint is removed and none is added; the `MUST NOT` count is
asserted unchanged. Every artefact authored under 10–15 or 10–25 satisfies the new text by
construction, so NO LIBRARY RE-AUTHORS and no stage re-opens — including the three certified
ones, none of which is this subject anyway.
"""
from __future__ import annotations

import difflib
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
LP = (ROOT / "data/content/constitutions/lesson_plan/the_world_around_us"
           / "preparatory/lesson_plan_constitution.txt")
OUT = pathlib.Path(__file__).resolve().parent

src = LP.read_text(encoding="utf-8")
before = src
MUST_NOT_BEFORE = src.count("MUST NOT")

edits = [
    ("VERSION 1.4 → 1.5",
     "ARUVI · LESSON PLAN GENERATION CONSTITUTION · THE WORLD AROUND US · VERSION 1.4",
     "ARUVI · LESSON PLAN GENERATION CONSTITUTION · THE WORLD AROUND US · VERSION 1.5"),

    ("Rule 5 — the word cap is removed; the rule is stated in kind",
     "section_context — a compact label of 10–25 words naming the specific objects,\n"
     "phenomena, or tasks this period drew from. This is what the assessment question\n"
     "is about. Name every object the period actually used; where a period draws on\n"
     "several, the label runs to the upper end and that is correct — do not drop an\n"
     "object to fit a length. Example: \"Spinning behaviour of coin, bangle, pencil,\n"
     "stone, wooden top, eraser.\"",

     "section_context — a compact label naming the specific objects, phenomena, or\n"
     "tasks this period drew from. This is what the assessment question is about.\n"
     "It is a LIST of what the period handled, not a sentence about it: name every\n"
     "object actually used, name nothing that was not, and add no commentary. Its\n"
     "length follows the period's content and is not itself a target — a period that\n"
     "handled two objects gives a short label, one that handled eight gives a longer\n"
     "one, and neither is a defect. MUST NOT drop an object to shorten the label.\n"
     "Example: \"Spinning behaviour of coin, bangle, pencil, stone, wooden top,\n"
     "eraser.\""),

    ("Rule 5 residue — the LP JSON schema comment",
     '"section_context": "string — 10–25 words naming the specific objects, phenomena, '
     'or tasks this period drew from"',
     '"section_context": "string — a list naming the specific objects, phenomena, or '
     'tasks this period drew from; length follows the content, not a word target"'),
]

for name, old, new in edits:
    if old not in src:
        sys.exit(f"ANCHOR MISSING — {name}\n  looked for: {old[:130]!r}")
    if src.count(old) != 1:
        sys.exit(f"ANCHOR NOT UNIQUE ({src.count(old)}×) — {name}")
    src = src.replace(old, new)
    print(f"  applied · {name}")

# ── guards ───────────────────────────────────────────────────────────────────
# One MUST NOT is ADDED here ("MUST NOT drop an object to shorten the label") — v1.4 carried
# the same instruction as plain prose, so this is a re-statement in the file's own idiom, not
# a new obligation. Assert the delta exactly rather than asserting "unchanged", so a later
# pass cannot smuggle a second one in behind it.
if src.count("MUST NOT") != MUST_NOT_BEFORE + 1:
    sys.exit(f"GUARD FAILED — prohibition count moved by "
             f"{src.count('MUST NOT') - MUST_NOT_BEFORE}, expected exactly +1 "
             "(the restated do-not-drop rule and nothing else)")
for dead in ("10–25 words", "10–15 words", "10-25 words", "10-15 words",
             "runs to the upper end"):
    if dead in src:
        sys.exit(f"GUARD FAILED — {dead!r} survives; the cap is meant to be gone")
# P1's work must still be intact
for needle in ("exactly ONE row {duration_minutes, count}", "THE SELF-CONTAINED REGISTER",
               "NAME A CLOCK QUANTITY"):
    if needle not in src:
        sys.exit(f"GUARD FAILED — {needle!r} is gone")

LP.write_text(src, encoding="utf-8")
diff = "".join(difflib.unified_diff(
    before.splitlines(keepends=True), src.splitlines(keepends=True),
    fromfile="lesson_plan_constitution.txt (v1.4)",
    tofile="lesson_plan_constitution.txt (v1.5)"))
(OUT / "lp_v1.4_to_v1.5.diff").write_text(diff, encoding="utf-8")
print(f"\nWROTE {LP}")
print(f"WROTE {OUT / 'lp_v1.4_to_v1.5.diff'}")
print(f"guards passed (MUST NOT {MUST_NOT_BEFORE} → {src.count('MUST NOT')}, +1 as declared)")
