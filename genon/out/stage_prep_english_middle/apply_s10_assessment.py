#!/usr/bin/env python3
"""S10 · english · middle — P2 (+ the P4 half that lives inside the file).

  english/middle assessment_constitution.txt   v3.6 -> v3.7

P2 · A6 — CONFIRMATION, NOT AMENDMENT. Rule 8A already carries the anchoring
   facts: the (section × spine) CELL is the anchor, carried by the item's own
   `source_section_id` + `source_spine`; the platform resolves it against each
   period's `section_id` + `spines_taught[]`; and `period_ref` / `period_number`
   / `unit_ref` MUST NOT be emitted. It landed on 2026-08-12 with the PAIR
   amendment (v3.6), ahead of this P-prep. Nothing to amend; verified by guard.

P2 · A9 — the REMOVAL is N/A (this file never carried the MEMORY-item-18
   position prohibition: `consecutive`, `same label`, `vary in position` are all
   0), so A9 lands as the two v1.7 lines ALONE, in Rule 4 where english states
   its MCQ semantics — the same site english/secondary v1.4 chose, for the same
   reason (Rule 5 is an indented bullet list a two-paragraph block reads oddly
   inside). Purely additive: there was no prior "none of the above" ban to
   absorb. No arrangement sentence is added, and the guards below assert none
   came back.

P4 · the in-document history block. v3.6 wrote its own changelog into the top
   of the constitution. P4 says the history lives in the sidecar and the VERSION
   line lives in the file, so the block is lifted out here and lands in
   CHANGELOG.md (written by apply_s10_changelogs.py) instead.
"""
from __future__ import annotations

import difflib
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
AS = ROOT / "data/content/constitutions/assessment/english/middle/assessment_constitution.txt"
OUT = pathlib.Path(__file__).resolve().parent

original = AS.read_text(encoding="utf-8")
text = original

edits: list[tuple[str, str, str, int]] = []


def edit(label: str, old: str, new: str, count: int = 1) -> None:
    edits.append((label, old, new, count))


# ------------------------------------------------------------------ version
edit(
    "VERSION header 3.6 -> 3.7",
    "ARUVI — ENGLISH ASSESSMENT CONSTITUTION · VERSION 3.6",
    "ARUVI — ENGLISH ASSESSMENT CONSTITUTION · VERSION 3.7",
)
edit(
    "footer 3.6 -> 3.7",
    "English Assessment Constitution · Version 3.6 · Internal Document",
    "English Assessment Constitution · Version 3.7 · Internal Document",
)

# -------------------------------------------- P4 · history out of the file
edit(
    "P4 · lift the in-document v3.6 history block to the sidecar",
    "Stage: Middle (Grades VI–VIII)\n"
    "\n"
    "v3.6 (2026-08-12) — THE PAIR. Rule 2 now emits TWO items per spine-cell, not\n"
    "one, on a prescriptive per-spine slot table; a new Rule 8A scopes them in two\n"
    "stages across the cell's teaching span. Amended in step with english/secondary\n"
    "v1.6 and english/preparatory v1.4. Reasoning:\n"
    "docs/english_secondary_item_density.md.\n"
    "\n",
    "Stage: Middle (Grades VI–VIII)\n"
    "\n",
)

# ------------------------------------------------------------------ A9
edit(
    "A9 · the two lines, in Rule 4",
    "  Do NOT classify \"select the true statements\" tasks as MCQ.\n"
    "\n"
    "ECR — NAME THE REFERENCED WORD:",
    "  Do NOT classify \"select the true statements\" tasks as MCQ.\n"
    "\n"
    "MCQ OPTION ORDER IS NOT YOURS TO SET. Emit the four options in whatever\n"
    "order they were authored; order carries no meaning. Uneven letters across a\n"
    "chapter are coincidence, not a defect, and correcting them is not your job —\n"
    "the platform arranges options deterministically after generation.\n"
    "\n"
    "An option MUST NOT refer to another option by its label: no \"both A and B\",\n"
    "\"none of the above\", \"all of the above\", \"either B or C\". Those are the one\n"
    "construction a downstream arrangement cannot reorder without rewriting the\n"
    "item.\n"
    "\n"
    "ECR — NAME THE REFERENCED WORD:",
)

# --------------------------------------------------------------------- apply
failures = []
for label, old, new, count in edits:
    got = text.count(old)
    if got != count:
        failures.append(f"  {label}: expected {count} occurrence(s), found {got}")
        continue
    text = text.replace(old, new, count)

if failures:
    print("REFUSING TO WRITE — anchor mismatch:", file=sys.stderr)
    print("\n".join(failures), file=sys.stderr)
    sys.exit(1)

# ------------------------------------------------------------------- guards
GUARDS_ZERO = [
    # A9: the arrangement sentence must never come back, in any of its forms
    "alphabetic",
    "never led with",
    "first word at which they differ",
    # the item-18 position prohibition, which this file never carried
    "vary in position",
    "same label across",
    # cancelled amendments / retired declarations
    "phase_ref",
    "role_handoff",
    "band_ref",
    "band_id",
    # V-rules never enter a constitution
    "section registry",
    "reserved token",
    "closing synthesis",
    # P4: no version history inside the file
    "v3.6 (2026-08-12)",
]
GUARDS_PRESENT = {
    # A6, confirmed rather than amended
    "RULE 8A | ITEM ANCHORING": 1,
    "source_section_id": 3,
    "spines_taught": 1,
    "MUST NOT emit `period_ref`": 1,
    # A9, the two lines
    "MCQ OPTION ORDER IS NOT YOURS TO SET": 1,
    "order carries no meaning": 1,
    "refer to another option by its label": 1,
    "none of the above": 1,
    # the poem locator carried on 2026-08-12 (C14 / ARV-D-138) — still standing
    "AT MOST EIGHT WORDS": 1,
    "REPRODUCING THE POEM": 1,
    # the PAIR
    "TWO ITEMS PER SPINE-CELL": 1,
    "VERSION 3.7": 1,
    "Version 3.7": 1,
}
bad = []
for g in GUARDS_ZERO:
    n = text.lower().count(g.lower())
    if n:
        bad.append(f"  MUST BE ABSENT but found {n}×: {g!r}")
for g, want in GUARDS_PRESENT.items():
    n = text.count(g)
    if n != want:
        bad.append(f"  expected {want}× but found {n}×: {g!r}")
if bad:
    print("REFUSING TO WRITE — guard failure:", file=sys.stderr)
    print("\n".join(bad), file=sys.stderr)
    sys.exit(1)

# -------------------------------------------------------------------- write
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "assess_english_middle_v3.6_pre.txt").write_text(original, encoding="utf-8")
diff = "".join(
    difflib.unified_diff(
        original.splitlines(keepends=True),
        text.splitlines(keepends=True),
        fromfile="assessment_constitution.txt (v3.6)",
        tofile="assessment_constitution.txt (v3.7)",
        n=3,
    )
)
(OUT / "assess_english_middle_v3.6_to_v3.7.diff").write_text(diff, encoding="utf-8")
AS.write_text(text, encoding="utf-8")

print(f"OK — {len(edits)} edits applied, {len(GUARDS_ZERO)} absence guards and "
      f"{len(GUARDS_PRESENT)} presence guards passed.")
print(f"     pre-file : {(OUT / 'assess_english_middle_v3.6_pre.txt').relative_to(ROOT)}")
print(f"     diff     : {(OUT / 'assess_english_middle_v3.6_to_v3.7.diff').relative_to(ROOT)}")
print(f"     amended  : {AS.relative_to(ROOT)}")
