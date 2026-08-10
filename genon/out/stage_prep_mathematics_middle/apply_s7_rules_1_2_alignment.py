#!/usr/bin/env python3
"""S7 · mathematics · middle — LP v3.5 -> v3.6: Rules 1 and 2 aligned with SECONDARY.

WHY (founder, 2026-08-10, on ch 7's top canonical). The top revisited sections 7.2, 7.3
and 7.5 after moving past them, so three of its twelve units taught nothing new and the
assessment items — which anchor at a section's LAST unit — landed on those revisits instead
of on the sittings that actually taught the section. A teacher skips a revisit; she then
misses the assessment too.

THE CAUSE IS ARITHMETIC, AND IT IS RULE 2'S OWN CAP. Rule 2 allowed a heavy section to
split across "two adjacent periods". Five sections x 2 = 10 body units; ch 7's top needs 11.
The model could not place its eleventh unit without breaking something, so it broke both
rules available to it: one run of three on 7.3 (Rule 2) and three returns (Rule 1). The
constraint binds exactly when body_units > 2 x sections — measured across the corpus:

    maths VII ch 7 top   11 body / 5 sections   11 > 10  BINDS    3 sections revisited
    maths VII ch 7 p10   10 body / 5 sections   10 = 10  MARGINAL 1 revisited
    maths VII ch 7 p07    7 body / 5 sections    7 < 10  SLACK    0
    maths IX  ch 4 top   14 body / 8 sections   14 < 16  SLACK    0
    science IX ch 8      11 body / 10 sections           SLACK    0

MATHS SECONDARY HAS NO SUCH CAP, which is why maths IX never revisits: its Rule 7
("FULL-SECTION COVERAGE") says a section "may span more than one period where its content
warrants it; emphasis follows the substance of the section", and forbids any numerical
allocation formula across sections. Its Rule 2 is not a packing rule at all. Middle's
"PERIOD BIN-PACKING" is the outlier in the maths family and the only one of the three that
names a number — which is the standing lesson of this campaign (testing.md v2.9: a limit
stated as a number is what live generation most often disproves).

So this is a PORT, not an invention: secondary's Rule 7 discipline moved down one stage,
where it has already been exercised at S4 and produces exactly the wanted behaviour.

§9: this is a CONSTITUTION CHANGE IN THE FULL SENSE, not the relaxation-only carve-out.
Removing the cap and generalising the two-goal wording are relaxations, but Rule 1's
contiguity sentence and Rule 2's two ported prohibitions are TIGHTENINGS, and one tightening
anywhere forfeits the carve-out. S7 re-opens: ch 7's three canonicals re-author under
LP v3.6 (~Rs 106) and C1-C3 re-run.
"""
from __future__ import annotations

import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).resolve().parent
LP = ROOT / "data/content/constitutions/lesson_plan/mathematics/middle/lesson_plan_constitution.txt"

OLD_R1 = """LP walks textbook section order. Do NOT reorder, interleave, or
re-sequence. Each period anchors to one or at most two adjacent sections.
"""

NEW_R1 = """LP walks textbook section order. Do NOT reorder, interleave, or
re-sequence. Each period anchors to one or at most two adjacent sections.

A section's periods are CONTIGUOUS. Once the plan has moved past a
section it does not return: a later period MUST NOT re-anchor a section
an earlier run already completed. Consolidation and extended practice
belong INSIDE that section's own run, where the class is still working
on it — never as a revisit after other sections have been taught.
"""

OLD_R2 = """RULE 2 | PERIOD BIN-PACKING
================================================================================

Allocate exactly B periods across sections.

- Heavy sections (many enumerated items, or two-goal declaration in
  the summary) MAY split across two adjacent periods.
- Light sections MAY merge with an adjacent section.
- Every section listed in the summary MUST appear in at least one
  period's `textbook_segments`. Dropping a section is FORBIDDEN —
  including consolidation-only sections (e.g., "Parallel Illusions"
  closing §s).

When a section's summary `section_goal` is a two-element array, the
LP MAY split it across two adjacent periods — period N gets the
first-listed goal, period N+1 gets the second-listed goal, in
textbook order.

The LP MUST NOT split a single-goal section across two different
goals. If a heavy single-goal section is split for time-budget
reasons, both periods carry the same `section_goal`.
"""

NEW_R2 = """RULE 2 | FULL-SECTION COVERAGE
================================================================================

Allocate exactly B periods across sections, in section order.

- Every section listed in the summary MUST appear in at least one
  period's `textbook_segments`. Dropping a section is FORBIDDEN —
  including consolidation-only sections (e.g., "Parallel Illusions"
  closing §s).
- A section MAY span as many ADJACENT periods as its content warrants.
  Emphasis follows the SUBSTANCE of the section — the number of
  enumerated items, the demand of the implied task — never the
  effort_index, which governs only how the chapter as a whole is
  allotted time in the Allocate step, never how periods are
  distributed within it.
- Light sections MAY merge with an adjacent section.
- Where the period budget exceeds what the sections need one-for-one,
  the surplus is spent by DEEPENING sections inside their own runs —
  more practice, a harder case, a second representation, a contextual
  application — never by adding a unit that returns to a section the
  plan has already left (Rule 1).

PROHIBITION
1. MUST NOT apply any numerical allocation formula across sections
   within the chapter.
2. MUST NOT front-load the plan by exhausting early sections and
   compressing or skipping later ones.

When a section's summary `section_goal` is a two-element array, the
LP MAY split that section's run so the EARLIER periods of the run
carry the first-listed goal and the LATER periods the second, in
textbook order.

The LP MUST NOT split a single-goal section across two different
goals. If a heavy single-goal section spans several periods, every
period of that run carries the same `section_goal`.
"""


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = LP.read_text(encoding="utf-8")
    shutil.copy2(LP, OUT / "lesson_plan_constitution_v3.5_pre.txt")

    assert t0.count("VERSION 3.5") == 1, "expected VERSION 3.5"
    assert t0.count(OLD_R1) == 1, "Rule 1 body: expected exactly 1 occurrence"
    assert t0.count(OLD_R2) == 1, "Rule 2 block: expected exactly 1 occurrence"

    t1 = t0.replace("ARUVI — MATHEMATICS LESSON PLAN CONSTITUTION · VERSION 3.5",
                    "ARUVI — MATHEMATICS LESSON PLAN CONSTITUTION · VERSION 3.6")
    t1 = t1.replace("Mathematics Lesson Plan Constitution · Version 3.5 · Internal Document",
                    "Mathematics Lesson Plan Constitution · Version 3.6 · Internal Document")
    t1 = t1.replace(OLD_R1, NEW_R1).replace(OLD_R2, NEW_R2)

    # ── guards · the cap is gone, in every form it could survive in ──────────
    assert "two adjacent periods" not in t1, "GUARD: the 2-period cap survived"
    assert "period N+1 gets the second-listed goal" not in t1, "GUARD: the N/N+1 split survived"
    assert "BIN-PACKING" not in t1, "GUARD: the old rule title survived"
    # ── guards · what the port must have brought ─────────────────────────────
    assert "as many ADJACENT periods as its content warrants" in t1, "GUARD: uncapped span"
    assert "A section's periods are CONTIGUOUS" in t1, "GUARD: Rule 1 contiguity"
    assert "MUST NOT re-anchor a section" in t1, "GUARD: the no-return prohibition"
    assert "MUST NOT apply any numerical allocation formula" in t1, "GUARD: ported prohibition 1"
    assert "MUST NOT front-load the plan" in t1, "GUARD: ported prohibition 2"
    # ── guards · nothing else moved ──────────────────────────────────────────
    assert t1.count("time_bands") == 2 and "phases[" not in t1, "GUARD: P3 intact"
    assert t1.count("THE SELF-CONTAINED REGISTER") == 2, "GUARD: register intact"
    assert "exactly ONE row {duration_minutes, count}" in t1, "GUARD: A1 intact"
    assert "The cap YIELDS where the anchored sections" in t1, "GUARD: v3.5 Rule 5 exception intact"
    assert "section_anchor" not in t1, "GUARD: no field invented (founder, 2026-08-10)"
    # Dropping a section stays forbidden — the relaxation must not have loosened THAT.
    assert "Dropping a section is FORBIDDEN" in t1, "GUARD: full coverage intact"

    LP.write_text(t1, encoding="utf-8")
    print("LP  v3.5 -> v3.6  ", LP)
    return 0


if __name__ == "__main__":
    sys.exit(main())
