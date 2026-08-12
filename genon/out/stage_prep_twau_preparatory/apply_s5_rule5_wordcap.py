#!/usr/bin/env python3
"""S5 · the_world_around_us · preparatory — LP v1.3 → v1.4: Rule 5's section_context cap.

Not part of the constitutional carry-forward set (A1 · A5/A7 · A6 · A9 · P3 · P4). It is
raised here because S8's standing rule for the remaining stages says to:

    "at P-prep, take every number a constitution states and check it against the whole
     class's `sections × canonical_plan.counts` AND against any real saved plan for that
     stage. The corpus check is the one that mattered."

MEASURED, on all three real TWAU saved plans (24 periods):

    ch_01 · III   7 periods   section_context 15–26 words   6 above 15
    ch_07 · IV    8 periods   section_context 10–28 words   2 above 15
    ch_05 · V     9 periods   section_context 15–20 words   6 above 15
                                                           ── 14 of 24 above the cap

The LOWER bound is never breached (min 10, exactly on the boundary once). So this is the
MIRROR of S4's finding rather than a repeat of it: S4 found maths·secondary's lower bounds
too HIGH (live output ran short, 10–13 → 6–13 and 10–12 → 6–12 at LP v1.3); TWAU's evidence
says the UPPER bound is too LOW. Widening the top alone is what the data supports, and
adding lower-end headroom this stage has never needed would be inventing a fix.

WHY THE FIELD TOLERATES IT. `section_context` is a descriptive LABEL — "the specific
objects, phenomena, or tasks this period drew from" — read by the assessment constitution
to ground what the question is about (its INPUTS 1 and TWO-FIELD READING RULE). It is not a
pedagogical constraint, and TWAU periods routinely name several objects at once, which is
exactly why the real output sits at 15–28. A cap that truncates it degrades the assessment's
grounding to protect nothing.

§9 — RELAXATION-ONLY. The edit widens: a length is permitted that was not, nothing is
tightened, and no obligation is created (`MUST NOT` count asserted unchanged below). Output
authored under the old text satisfies the new by construction. No library re-authors — and
none exists for this stage anyway, which is the whole point of catching it at P-prep.
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

edits: list[tuple[str, str, str]] = [
    ("VERSION 1.3 → 1.4",
     "ARUVI · LESSON PLAN GENERATION CONSTITUTION · THE WORLD AROUND US · VERSION 1.3",
     "ARUVI · LESSON PLAN GENERATION CONSTITUTION · THE WORLD AROUND US · VERSION 1.4"),

    ("Rule 5 — section_context 10–15 → 10–25 words",
     "section_context — a compact label of 10–15 words naming the specific objects,\n"
     "phenomena, or tasks this period drew from. This is what the assessment question\n"
     "is about. Example: \"Spinning behaviour of coin, bangle, pencil, stone, wooden\n"
     "top, eraser.\"",

     "section_context — a compact label of 10–25 words naming the specific objects,\n"
     "phenomena, or tasks this period drew from. This is what the assessment question\n"
     "is about. Name every object the period actually used; where a period draws on\n"
     "several, the label runs to the upper end and that is correct — do not drop an\n"
     "object to fit a length. Example: \"Spinning behaviour of coin, bangle, pencil,\n"
     "stone, wooden top, eraser.\""),

    # The schema comment is the surface the model copies from — the residue S7 (v3.7),
    # S8 (v1.3) and this stage's own A1 pass have each had to chase separately.
    ("Rule 5 residue — the LP JSON schema comment",
     '"section_context": "string — 10–15 words naming the specific objects, phenomena, '
     'or tasks this period drew from"',
     '"section_context": "string — 10–25 words naming the specific objects, phenomena, '
     'or tasks this period drew from"'),
]

for name, old, new in edits:
    if old not in src:
        sys.exit(f"ANCHOR MISSING — {name}\n  looked for: {old[:130]!r}")
    if src.count(old) != 1:
        sys.exit(f"ANCHOR NOT UNIQUE ({src.count(old)}×) — {name}")
    src = src.replace(old, new)
    print(f"  applied · {name}")

# ── guards ───────────────────────────────────────────────────────────────────
if src.count("MUST NOT") != MUST_NOT_BEFORE:
    sys.exit(f"GUARD FAILED — prohibition count moved "
             f"({MUST_NOT_BEFORE} → {src.count('MUST NOT')}); this edit is relaxation-only")
if "10–15 words" in src:
    sys.exit("GUARD FAILED — a 10–15 residue survives somewhere")
if src.count("10–25 words") != 2:
    sys.exit(f"GUARD FAILED — expected the new bound in BOTH the rule and the schema, "
             f"found {src.count('10–25 words')}")
# the A1/register work from apply_s5_p1_lp.py must still be intact
for needle in ("exactly ONE row {duration_minutes, count}", "THE SELF-CONTAINED REGISTER"):
    if needle not in src:
        sys.exit(f"GUARD FAILED — P1's {needle!r} is gone; run apply_s5_p1_lp.py first")

LP.write_text(src, encoding="utf-8")

diff = "".join(difflib.unified_diff(
    before.splitlines(keepends=True), src.splitlines(keepends=True),
    fromfile="lesson_plan_constitution.txt (v1.3)",
    tofile="lesson_plan_constitution.txt (v1.4)"))
(OUT / "lp_v1.3_to_v1.4.diff").write_text(diff, encoding="utf-8")

print(f"\nWROTE {LP}")
print(f"WROTE {OUT / 'lp_v1.3_to_v1.4.diff'}")
print(f"all guards passed (MUST NOT count unchanged at {MUST_NOT_BEFORE})")
