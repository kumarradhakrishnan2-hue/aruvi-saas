#!/usr/bin/env python3
"""S8 · mathematics · preparatory — Rules 1 and 2 aligned with SECONDARY and MIDDLE.

LP v1.2 -> v1.3, at P-prep, BEFORE any canonical for this stage is authored.

WHY, AND WHY IT DID NOT WAIT FOR C1 (founder ruling, 2026-08-11).
The first sign-off recommended leaving both numeric caps alone on the grounds that the pilot
chapter dodges the binding case and that prep sections are "small and task-dense" in a way
middle's are not. The founder challenged it and the data does not support the recommendation:

1. THE COPRUS ALREADY BREAKS THE CAP, WITH SLACK IN HAND. `backup/saved_plans/mathematics/iv/
   ch_08_*.json` runs section S5 across periods 6, 7 AND 8 — three periods against a cap of
   two — on a plan of 9 body units against a cap of 12. Arithmetic did not force it; the
   content did. So the cap does not only break when body units > 2 x sections (4 of class
   III's 14 chapters); it breaks whenever a heavy section warrants a third period, which is
   a property of the section, not of the budget. The pilot dodging the arithmetic case buys
   nothing.
2. "SMALL AND TASK-DENSE" IS HALF-WRONG. Across class III's 98 sections the median is 3 tasks
   and the mean 4.2 — but the max is 13, and NINE sections carry more than 8. Those are
   exactly the sections a two-period cap mis-sizes.
3. PREPARATORY IS NOW THE SOLE OUTLIER IN THE MATHS FAMILY. Secondary never had the cap;
   middle's went at v3.6. S7's own changelog named the tell — "the only one of the three that
   named a number" — and that tell now points here.

And Rule 1's other cap is not a risk at all but a CERTAINTY: the platform brief mandates a
closing whole-chapter synthesis unit, and "one — or at most two adjacent — sections" cannot
describe it. S7 met exactly this at C3 (ARV-D-094) and amended mid-cycle. Doing it now costs
nothing; §3's ordering rule exists for precisely this.

WHAT IS PORTED: middle's END STATE (v3.8), not the v3.6 text.
This matters. v3.6 introduced a SURPLUS bullet ("where the period budget exceeds what the
sections need one-for-one, the surplus is spent by DEEPENING sections inside their own
runs...") and v3.8 DELETED it two days later as the cause of the hoarding it was meant to
cure — it framed placement as spending spare units, and a unit conceived as an add-on has no
run to belong to. Porting v3.6 verbatim would import a clause its own stage has already
retired. `grep -cio "surplus|deepen|more time|extra time"` was 0 in this file and the guards
below keep it 0.

ALSO NOT PORTED: middle's two `section_goal` split paragraphs. Preparatory has NO per-period
goal — its cognitive axis is the per-TASK `intent` (Rule 4), and the handoff clusters on
intent (Rule 8). Porting them would invent a field this stage does not have, which is the one
thing the founder ruling of 2026-08-10 forbids.

STRUCTURAL: the coverage mandate MOVES from Rule 1 to Rule 2, where middle keeps it, so the
two stages now read the same rule in the same place. Nothing is lost — the sentence is
reproduced verbatim in substance, against `section_refs` rather than `textbook_segments`.

§9: a constitution change in the FULL sense — the caps coming out are relaxations, but the
contiguity sentence and the two prohibitions are tightenings, and one tightening anywhere
forfeits the relaxation-only carve-out. It costs nothing today because no library for this
stage exists. That is exactly what the §3 ordering rule buys, and it is the difference
between this and S7, which paid ~Rs 106 to learn the same thing.
"""
from __future__ import annotations

import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).resolve().parent
LP = ROOT / "data/content/constitutions/lesson_plan/mathematics/preparatory/lesson_plan_constitution.txt"


def sub(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    assert n == 1, f"{label}: expected exactly 1 occurrence, found {n}"
    return text.replace(old, new)


RULE_1_OLD = """The LP walks `sections` in textbook order. Do NOT reorder, interleave, or
re-sequence. Each period anchors to one — or at most two adjacent —
sections. Every section in the summary MUST appear in at least one
period's `section_refs`. Dropping a section is FORBIDDEN."""

RULE_1_NEW = """The LP walks `sections` in textbook order. Do NOT reorder, interleave, or
re-sequence. A period anchors to as many ADJACENT sections as its
content warrants.

A section's periods are CONTIGUOUS. Once the plan has moved past a
section it does not return: a later period MUST NOT re-anchor a section
an earlier run already completed. Consolidation and extended practice
belong INSIDE that section's own run, where the class is still working
on it — never as a revisit after other sections have been taught."""

RULE_2_OLD = """RULE 2 | PERIOD BIN-PACKING
================================================================================

Allocate exactly B periods across sections.

- A heavy section (many tasks) MAY split across two adjacent periods.
- Light sections MAY merge with an adjacent section.
- A section split across periods keeps its tasks in textbook order; no
  task is assigned to two periods."""

RULE_2_NEW = """RULE 2 | FULL-SECTION COVERAGE
================================================================================

Allocate exactly B periods across sections, in section order.

- Every section in the summary MUST appear in at least one period's
  `section_refs`. Dropping a section is FORBIDDEN.
- A section MAY span as many ADJACENT periods as its content warrants.
  Emphasis follows the SUBSTANCE of the section — the number of
  enumerated tasks, the demand of the concept being built — never the
  effort_index, which governs only how the chapter as a whole is
  allotted time in the Allocate step, never how periods are
  distributed within it.
- Light sections MAY merge with an adjacent section.
- A section spanning several periods keeps its tasks in textbook order;
  no task is assigned to two periods.

PROHIBITION
1. MUST NOT apply any numerical allocation formula across sections
   within the chapter.
2. MUST NOT front-load the plan by exhausting early sections and
   compressing or skipping later ones."""


def amend(t: str) -> str:
    t = sub(t,
            "ARUVI — MATHEMATICS LESSON PLAN CONSTITUTION (PREPARATORY) · VERSION 1.2",
            "ARUVI — MATHEMATICS LESSON PLAN CONSTITUTION (PREPARATORY) · VERSION 1.3",
            "version line")
    t = sub(t, RULE_1_OLD, RULE_1_NEW, "Rule 1 — cap out, contiguity in, coverage moved out")
    t = sub(t, RULE_2_OLD, RULE_2_NEW, "Rule 2 — FULL-SECTION COVERAGE")

    # ── THE THREE RESIDUES · a cap removed from one rule and left standing in ─
    # three other places is not removed at all. Found by grep AFTER the two rule
    # edits landed, which is the lesson: S7's v3.7 hit the identical thing (middle's
    # schema comment still read `// 1–2 entries` after Rule 1 was widened). Grep the
    # NUMBER, not the rule.
    t = sub(t,
            "walks the chapter's `sections` (S1, S2, …) in order; each period anchors\n"
            "to one or two adjacent sections.",
            "walks the chapter's `sections` (S1, S2, …) in order; each period anchors\n"
            "to as many adjacent sections as its content warrants.",
            "residue 1 — DESIGN PRINCIPLE restated the cap")
    t = sub(t,
            "Before bin-packing, apply a non-duplicating pass within each section: where",
            "Before allocating periods, apply a non-duplicating pass within each section: where",
            "residue 2 — Rule 2A named the retired rule")
    t = sub(t,
            '  "section_refs":            [ string ],        // 1–2, e.g. ["S3"] — copied\n'
            "                                                //   from summary sections[].ref",
            '  "section_refs":            [ string ],        // e.g. ["S3"] — copied verbatim\n'
            "                                                //   from summary sections[].ref;\n"
            "                                                //   as many ADJACENT sections as\n"
            "                                                //   the unit's content warrants\n"
            "                                                //   (Rule 1), no fixed count",
            "residue 3 — the schema comment carried the cap as a number")
    t = sub(t,
            "Mathematics Lesson Plan Constitution (Preparatory) · Version 1.2 · Internal Document",
            "Mathematics Lesson Plan Constitution (Preparatory) · Version 1.3 · Internal Document",
            "footer")
    return t


def main() -> int:
    t0 = LP.read_text(encoding="utf-8")
    shutil.copy2(LP, OUT / "lesson_plan_constitution_v1.2_pre.txt")
    t1 = amend(t0)

    # ── guards · the caps are gone in EVERY form they could survive in ───────
    for cap in ("at most two adjacent", "two adjacent periods", "split across two",
                "one — or at most two", "PERIOD BIN-PACKING", "one or two adjacent",
                "bin-packing", "bin-pack"):
        assert cap not in t1, f"GUARD: the cap survived as {cap!r}"
    # The number itself, wherever it could hide. Rule 4's "two adjacent reason tasks"
    # (methods) and Rule 9's "1–2 items" (homework) are different subjects and stay; the
    # section-span cap must not appear anywhere, in prose OR in a schema comment.
    assert '// 1–2, e.g. ["S3"]' not in t1, "GUARD: the schema comment still caps the span"
    assert "as many ADJACENT sections" in t1 and "as many adjacent sections" in t1, \
        "GUARD: the widened span must be stated in BOTH Rule 1 and the DESIGN PRINCIPLE"

    # ── guards · the port arrived intact ────────────────────────────────────
    assert "as many ADJACENT sections as its" in t1, "GUARD: Rule 1's widened section span"
    assert "as many ADJACENT periods as its content warrants" in t1, "GUARD: Rule 2's span"
    assert "A section's periods are CONTIGUOUS" in t1, "GUARD: the contiguity sentence"
    assert "MUST NOT apply any numerical allocation formula" in t1, "GUARD: prohibition 1"
    assert "MUST NOT front-load the plan" in t1, "GUARD: prohibition 2"
    assert "FULL-SECTION COVERAGE" in t1, "GUARD: Rule 2's new title"
    # The coverage mandate MOVED; it must exist exactly once, and in Rule 2.
    assert t1.count("Dropping a section is FORBIDDEN") == 1, "GUARD: coverage mandate count"
    assert t1.index("FULL-SECTION COVERAGE") < t1.index("Dropping a section is FORBIDDEN"), \
        "GUARD: the coverage mandate must now sit inside Rule 2"

    # ── guards · v3.8's deleted SURPLUS bullet must NEVER arrive here ────────
    for harmful in ("surplus", "Surplus", "DEEPENING", "deepen",
                    "budget exceeds", "more time available"):
        assert harmful not in t1, f"GUARD: v3.8's retired surplus framing arrived as {harmful!r}"

    # ── guards · no field invented for a stage that does not have one ───────
    assert "section_goal" not in t1, \
        "GUARD: preparatory has no per-period goal — its axis is the per-task `intent`"
    assert "section_anchor" not in t1, "GUARD: section_anchor invented"
    assert "textbook_segments" not in t1, "GUARD: middle's field name leaked in"

    # ── guards · everything the v1.2 pass landed is UNTOUCHED ───────────────
    assert "exactly ONE row {duration_minutes, count}" in t1, "GUARD: A1 disturbed"
    assert t1.count("THE SELF-CONTAINED REGISTER") == 2, "GUARD: the register disturbed"
    assert t1.count("time_bands") == 2 and "phases[" not in t1, "GUARD: the P3 shape disturbed"
    # THREE obligations are created, not two — the guard caught the miscount on the first
    # run and it is left exact rather than loosened. Rule 1's contiguity sentence carries one
    # ("a later period MUST NOT re-anchor a section an earlier run already completed") and
    # Rule 2's PROHIBITION block carries two. This count is what makes the §9 reading in the
    # changelog checkable: three tightenings is why the relaxation-only carve-out does not
    # apply, even though both caps came out.
    assert t1.count("MUST NOT") == t0.count("MUST NOT") + 3, \
        f"GUARD: expected exactly 3 new obligations, got {t1.count('MUST NOT') - t0.count('MUST NOT')}"

    LP.write_text(t1, encoding="utf-8")
    print("LP  v1.2 -> v1.3  ", LP)
    return 0


if __name__ == "__main__":
    sys.exit(main())
