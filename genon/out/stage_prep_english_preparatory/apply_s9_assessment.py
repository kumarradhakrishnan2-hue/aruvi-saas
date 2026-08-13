#!/usr/bin/env python3
"""S9 · english · preparatory — P2 (A6-confirm + A9) and P4's in-file half.

  english/preparatory assessment_constitution.txt   v1.4 -> v1.5

WHAT LANDS:

  P2 · A6   CONFIRMED, NOT AMENDED — the second such confirmation in the
            campaign, after S10's, and for the same reason: Rule 8A landed a
            day early with the cross-stage PAIR pass (v1.4, 2026-08-12) and
            already carries the whole anchoring fact. The anchor is the
            (section x spine) CELL, borne by the item's own `source_section_id`
            + `source_spine` (8-rule row 7, the table's only PAIR key); the
            platform resolves it against each period's `section_id` +
            `spines_taught[]`; `period_ref` / `period_number` / `unit_ref` MUST
            NOT be emitted. The v1.2-era band-level `phase_ref` is absent and is
            not reintroduced. Nothing to amend — asserted by guard, not by eye.

  P2 · A9   The REMOVAL is N/A: this file never carried the MEMORY item-18
            position prohibition (testing.md P2 names the four files that do —
            SS and Science, middle and secondary — and this is not one).
            The two ADDED lines land in Rule 4, beside english's MCQ semantics,
            which is the site english/secondary chose at v1.4 and middle at
            v3.7. Purely additive: preparatory carried no prior "none of the
            above" ban to absorb. No arrangement sentence, at any point.

  P4        The in-document v1.4 history block above DESIGN PRINCIPLE is lifted
            out — P4 forbids version history inside the constitution; the
            `VERSION` line stays. It is back-filled as the sidecar's v1.4 entry
            (see CHANGELOG.md). Same removal S10 had to make on its own file.

  Poem locator: already present (Rule 3, carried 2026-08-12 with ARV-D-138) and
  asserted present here rather than re-landed.
"""
from __future__ import annotations

import difflib
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
AS = ROOT / "data/content/constitutions/assessment/english/preparatory/assessment_constitution.txt"
OUT = pathlib.Path(__file__).resolve().parent

original = AS.read_text(encoding="utf-8")
text = original

edits: list[tuple[str, str, str, int]] = []


def edit(label: str, old: str, new: str, count: int = 1) -> None:
    edits.append((label, old, new, count))


# ------------------------------------------------------------------ header
edit(
    "VERSION header 1.4 -> 1.5",
    "ARUVI — ENGLISH ASSESSMENT CONSTITUTION · PREPARATORY · VERSION 1.4",
    "ARUVI — ENGLISH ASSESSMENT CONSTITUTION · PREPARATORY · VERSION 1.5",
)
edit(
    "footer 1.4 -> 1.5",
    "English Assessment Constitution · Preparatory · Version 1.4",
    "English Assessment Constitution · Preparatory · Version 1.5",
)

# ------------------------------- P4 · the in-document history block, removed
edit(
    "P4 · lift the in-file v1.4 history block to the sidecar",
    "Stage: Preparatory (Grades III–V)\n"
    "\n"
    "v1.4 (2026-08-12) — THE PAIR. Rule 2 now emits TWO items per spine-cell, not\n"
    "one, on a prescriptive per-spine slot table; a new Rule 8A scopes them in two\n"
    "stages across the cell's teaching span. Amended in step with english/middle\n"
    "v3.6 and english/secondary v1.6. At THIS stage the pair is deliberately light —\n"
    "slot 1 is recognition, slot 2 is a single short production — never two long\n"
    "tasks. Reasoning: docs/english_secondary_item_density.md.\n"
    "\n",
    "Stage: Preparatory (Grades III–V)\n"
    "\n",
)

# ------------------------------------------------------------- P2 · A9
edit(
    "A9 · two lines in Rule 4, beside the MCQ semantics",
    'Do NOT classify "select the true statements" tasks as MCQ.\n',
    'Do NOT classify "select the true statements" tasks as MCQ.\n'
    "\n"
    "MCQ OPTION ORDER IS NOT YOURS TO SET. Emit the four options in whatever\n"
    "order they were authored; order carries no meaning. Uneven letters across a\n"
    "chapter are coincidence, not a defect, and correcting them is not your job —\n"
    "the platform arranges options deterministically after generation.\n"
    "\n"
    "An option MUST NOT refer to another option by its label: no \"both A and B\",\n"
    '"none of the above", "all of the above", "either B or C". Those are the one\n'
    "construction a downstream arrangement cannot reorder without rewriting the\n"
    "item.\n",
)

# ------------------------------------------------------------------ apply
failures: list[str] = []
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

# ------------------------------------------------------------------ guards
GUARDS_ZERO = [
    # A9 — no arrangement rule, ever
    "alphabetic",
    "never led with",
    "first word at which they differ",
    # the MEMORY item-18 prohibition (N/A here, and must not arrive)
    "consecutive items",
    "same label",
    "vary in position",
    # A6 — the reversed band-level anchor, and the numbering Rule 8A forbids
    "phase_ref",
    "band_id",
    "band_ref",
    # cancelled amendments
    "role_handoff",
    "unit_handoff",
    "role weighting",
    # V-rules never enter a constitution
    "section registry",
    "reserved token",
    "closing synthesis",
    # P4 — no version history in the file
    "v1.4 (2026-08-12)",
]
GUARDS_PRESENT = {
    # A9's two lines
    "MCQ OPTION ORDER IS NOT YOURS TO SET": 1,
    "MUST NOT refer to another option by its label": 1,
    # A6 — Rule 8A, confirmed present and untouched
    "RULE 8A": 1,
    "source_section_id": 3,
    "source_spine": 3,
    # the poem locator (ARV-D-138), confirmed present and untouched
    "incipit": 2,
    "REPRODUCING THE POEM": 1,
    # the PAIR
    "TWO ITEMS PER SPINE-CELL": 1,
    "VERSION 1.5": 1,
    "Version 1.5": 1,
}
bad = []
for g in GUARDS_ZERO:
    n = text.count(g)
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

# ------------------------------------------------------------------- write
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "assess_english_preparatory_v1.4_pre.txt").write_text(original, encoding="utf-8")
diff = "".join(
    difflib.unified_diff(
        original.splitlines(keepends=True),
        text.splitlines(keepends=True),
        fromfile="assessment_constitution.txt (v1.4)",
        tofile="assessment_constitution.txt (v1.5)",
        n=3,
    )
)
(OUT / "assess_english_preparatory_v1.4_to_v1.5.diff").write_text(diff, encoding="utf-8")
AS.write_text(text, encoding="utf-8")

print(f"OK — {len(edits)} edits applied, {len(GUARDS_ZERO)} absence guards and "
      f"{len(GUARDS_PRESENT)} presence guards passed.")
print(f"     pre-file : {(OUT / 'assess_english_preparatory_v1.4_pre.txt').relative_to(ROOT)}")
print(f"     diff     : {(OUT / 'assess_english_preparatory_v1.4_to_v1.5.diff').relative_to(ROOT)}")
print(f"     amended  : {AS.relative_to(ROOT)}")
