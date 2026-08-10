#!/usr/bin/env python3
"""S7 · mathematics · middle — LP v3.4 -> v3.5, Rule 5's consecutive-method cap.

Found at C1 on ch 7's top canonical (2026-08-10): units 10, 11 and 12 are all
Problem-solving, a run of three against a cap of two. This is ARV-D-072's twin — the
same defect, at the same place in the chapter, for the same reason S4 measured at its
own C3: the tail genuinely converges on problem work (extended construction practice ->
applying triangle geometry in a real context -> whole-chapter synthesis), and satisfying
the cap there means labelling a unit with a method its content does not support.

Ported verbatim in substance from mathematics·secondary LP v1.3 (2026-08-09).

RELAXATION-ONLY (testing.md §9's carve-out): the edit only WIDENS — an exception is
added, nothing is tightened, no new obligation is created. Output that satisfied v3.4
satisfies v3.5 by construction, and the clause amended is the very one ch 7's top
breached, so the installed canonical becomes compliant rather than breaching. No
re-author is owed. Timed before STEP 4 so the two compacts are authored against the
corrected rule instead of inheriting the breach.
"""
from __future__ import annotations

import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).resolve().parent
LP = ROOT / "data/content/constitutions/lesson_plan/mathematics/middle/lesson_plan_constitution.txt"

OLD = """Diversity: same method MUST NOT appear in more than two consecutive
periods. Each method SHOULD appear at least once per chapter where
content permits."""

NEW = """Diversity: same method SHOULD NOT appear in more than two consecutive
periods. Each method SHOULD appear at least once per chapter where
content permits.

The cap YIELDS where the anchored sections genuinely converge on one
kind of work — most often at a chapter's tail, where extended practice,
contextual application and a closing synthesis are all honestly
problem-solving. Where it yields, the method named is the one the
content supports; a run produced for convenience, or to avoid thinking
about pedagogy, remains forbidden. The default mapping above still
binds, and a chapter whose every period carries one method is a defect,
not an exception."""


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = LP.read_text(encoding="utf-8")
    shutil.copy2(LP, OUT / "lesson_plan_constitution_v3.4_pre.txt")

    assert t0.count("VERSION 3.4") == 1, "expected VERSION 3.4"
    assert t0.count(OLD) == 1, "Rule 5 diversity paragraph: expected exactly 1 occurrence"

    t1 = t0.replace("ARUVI — MATHEMATICS LESSON PLAN CONSTITUTION · VERSION 3.4",
                    "ARUVI — MATHEMATICS LESSON PLAN CONSTITUTION · VERSION 3.5")
    t1 = t1.replace("Mathematics Lesson Plan Constitution · Version 3.4 · Internal Document",
                    "Mathematics Lesson Plan Constitution · Version 3.5 · Internal Document")
    t1 = t1.replace(OLD, NEW)

    # ── guards ───────────────────────────────────────────────────────────────
    # RELAXATION-ONLY: nothing that v3.4 permitted may be forbidden by v3.5. The only
    # MUST NOT removed is the one being relaxed; every other prohibition survives.
    assert t1.count("MUST NOT") == t0.count("MUST NOT") - 1, \
        "GUARD: exactly one MUST NOT should have relaxed to SHOULD NOT"
    assert "a run produced for convenience" in t1, "GUARD: the exception's own limit"
    assert "is a defect,\nnot an exception" in t1, "GUARD: the whole-chapter backstop"
    # Nothing else moved.
    assert t1.count("time_bands") == 2 and "phases[" not in t1, "GUARD: P3 intact"
    assert t1.count("THE SELF-CONTAINED REGISTER") == 2, "GUARD: register intact"
    assert "exactly ONE row {duration_minutes, count}" in t1, "GUARD: A1 intact"
    assert "section_anchor" not in t1, "GUARD: no field invented (founder, 2026-08-10)"

    LP.write_text(t1, encoding="utf-8")
    print("LP  v3.4 -> v3.5  ", LP)
    return 0


if __name__ == "__main__":
    sys.exit(main())
