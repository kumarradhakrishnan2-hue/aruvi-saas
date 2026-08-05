#!/usr/bin/env python3
"""S3 · science · secondary — P1/P2 constitutional amendments, applied by surgical
string edits (the reproducible record; the outputs are written LIVE onto
data/content/constitutions/.../science/secondary/).

Carry-forward applied, and nothing more (testing.md v2.6 §3):
  A1        — period schedule is exactly ONE standard row (50 min for IX)
  A5 + A7   — THE SELF-CONTAINED REGISTER, as ONE block, in the v1.10 three-ban re-cut
  A6        — CONFIRMED present via the subject's equivalent (section_number ->
              coverage_handoff.period_numbers); ONE clarifying integrity line added so
              the model never invents a period_ref the platform derives itself
  A9        — the MEMORY-item-18 position prohibition REMOVED; the v1.7 two lines ADDED
  P3        — N/A (Group A: already time_bands[{minutes, activity}])

Every edit asserts exactly-one occurrence. Nothing else is touched.
Run:  python3 genon/out/stage_prep_science_secondary/apply_s3_amendments.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LP_LIVE = ROOT / "data/content/constitutions/lesson_plan/science/secondary/lesson_plan_constitution.txt"
AS_LIVE = ROOT / "data/content/constitutions/assessment/science/secondary/assessment_constitution.txt"


def edit(text, old, new):
    assert text.count(old) == 1, f"expected exactly 1 occurrence, got {text.count(old)}: {old[:90]!r}"
    return text.replace(old, new)


# ══════════════════════════════════════════════════════════════════════════════
# LESSON PLAN CONSTITUTION · v1.0 -> v1.1
# ══════════════════════════════════════════════════════════════════════════════
lp = (HERE / "lesson_plan_constitution_v1.0_pre.txt").read_text(encoding="utf-8")

# ── VERSION line ─────────────────────────────────────────────────────────────
lp = edit(
    lp,
    "ARUVI · LESSON PLAN GENERATION CONSTITUTION · SCIENCE · SECONDARY STAGE · VERSION 1.0",
    "ARUVI · LESSON PLAN GENERATION CONSTITUTION · SCIENCE · SECONDARY STAGE · VERSION 1.1",
)

# ── A5 + A7: the register, as ONE block after VOCABULARY ─────────────────────
# The vocabulary line's positional cross-reference examples go: backward continuity is
# legal again, but it is carried by NAMING THE CONTENT, never a unit's position.
lp = edit(
    lp,
    'The atomic teaching chunk is called a "unit" in ALL teacher-facing prose — '
    'teacher_notes, activity titles, homework, and any cross-reference to another chunk '
    '(e.g. "the previous unit", "this unit"). The token "period" is retained ONLY in '
    "(a) schema field names (period_number, period_duration_minutes, periods[], etc.) and "
    "(b) the scheduling/allocation budget (period schedule, period count, per-period "
    'budget). Never write "period" in prose the teacher reads.',
    'The atomic teaching chunk is called a "unit" in ALL teacher-facing prose — '
    'teacher_notes, activity titles, homework. The token "period" is retained ONLY in '
    "(a) schema field names (period_number, period_duration_minutes, periods[], etc.) and "
    "(b) the scheduling/allocation budget (period schedule, period count, per-period "
    'budget). Never write "period" in prose the teacher reads; "session" is outside the '
    "register too.\n"
    "\n"
    "THE SELF-CONTAINED REGISTER (binds Rules 7 and 10)\n"
    "Three things no time band or teacher note may do, each because the platform enforces it:\n"
    "1. NAME A CLOCK QUANTITY — the platform scales every band's minutes in proportion to the "
    'sitting that carries it, so a stated number is falsified silently: no "for three minutes", '
    '"the remaining time", "half the session". Where a task is genuinely brief or genuinely '
    'long, say so in kind — "a quick individual calculation", "an extended investigation" — '
    "never in number.\n"
    "2. POINT FORWARD OR CLAIM COMPLETION — a teacher's plan may end, or hand over to a "
    'companion variant\'s unit, after any unit, so "the next unit", "as we will see", "having '
    'covered all three models" are wrong for someone. Each unit closes on its own ground.\n'
    "3. NAME CALENDAR TIME — Aruvi keeps no calendar and sittings do not map to days: today, "
    "yesterday, this week, next class are unknowable at authoring.\n"
    "Backward continuity is welcome, and is best carried by naming the content built on "
    '("Having established that mass and charge are carried by different particles, …" — Rule '
    "10's continuity link) rather than a unit's position.",
)

# ── A1: the period schedule is a single standard row ─────────────────────────
lp = edit(
    lp,
    "4. Period schedule — one or more rows of {duration_minutes, count}",
    "4. Period schedule — exactly ONE row {duration_minutes, count}: the class-standard\n"
    "   duration (40 min for classes up to VII, 45 for VIII, 50 for IX) × the period\n"
    "   count. Teacher timetable variation never reaches generation; it is handled\n"
    "   downstream at serve time.",
)

lp = edit(
    lp,
    "- TIME: Total minutes = sum of (duration × count) per row. Total period count =\n"
    "  sum of row counts. Each period has exactly one activity calibrated to its\n"
    "  duration. MUST NOT exceed total period count.",
    "- TIME: the schedule is a single standard row. Total minutes = duration × count.\n"
    "  Total period count = count. Each period has exactly one activity calibrated to\n"
    "  the standard duration. MUST NOT exceed total period count.",
)

# ── A6: the anchor is the subject's own equivalent, and it is DERIVED ────────
lp = edit(
    lp,
    "- Section anchoring (Rule 1) is absolute — no exceptions for introductory,\n"
    "  transition, or review activities.",
    "- Section anchoring (Rule 1) is absolute — no exceptions for introductory,\n"
    "  transition, or review activities.\n"
    "- ITEM ANCHORING IS DERIVED, NOT DECLARED: an assessment item's anchor unit is\n"
    "  resolved by the platform from its section_number through this handoff's\n"
    "  period_numbers. MUST NOT emit period_ref (or any unit number) on an assessment\n"
    "  item — at this stage the unique link is the SECTION, and a section may be taught\n"
    "  across several units (Rule 4).",
)

# ── the register, bound where band text and notes are written ────────────────
lp = edit(
    lp,
    "The competency fields in the Coverage Handoff (Amendment A4) are structured\n"
    "metadata, not teacher-facing text, and are exempt — but their contents MUST NOT\n"
    "leak into any of the teacher-facing fields named above.",
    "6. Anything barred by THE SELF-CONTAINED REGISTER. Each band speaks in the present\n"
    "   of its own activity; sequence lives in the plan's structure, and unit-to-unit\n"
    "   linking lives only in teacher_notes (Rule 10).\n"
    "\n"
    "The competency fields in the Coverage Handoff (Amendment A4) are structured\n"
    "metadata, not teacher-facing text, and are exempt — but their contents MUST NOT\n"
    "leak into any of the teacher-facing fields named above.",
)

# Rule 10's continuity link becomes position-free (v1.10 / v1.2.1 doctrine).
lp = edit(
    lp,
    "- Connect this unit to the one before it — what was covered, how this builds\n"
    "  on it. The first unit instead orients the teacher to the chapter's entry\n"
    "  point.",
    "- Connect this unit to the content already taught — named by that content\n"
    "  itself, never by its position. The first unit instead orients the teacher to\n"
    "  the chapter's entry point.",
)

lp = edit(
    lp,
    "3. MUST NOT restate the unit's activity text verbatim — teacher_notes guides\n"
    "   how to run the activity, it does not re-describe it.",
    "3. MUST NOT restate the unit's activity text verbatim — teacher_notes guides\n"
    "   how to run the activity, it does not re-describe it.\n"
    "4. MUST NOT breach THE SELF-CONTAINED REGISTER.",
)

# ── A1 schema: the single standard row, made explicit at the schema ─────────
lp = edit(
    lp,
    "- section_coverage_note: present only under Rule 4's budget shortfall; else null.",
    "- section_coverage_note: present only under Rule 4's budget shortfall; else null.\n"
    "- period_schedule: exactly one row — the class-standard duration × count (INPUTS 4).",
)

lp = edit(
    lp,
    '  "period_schedule": [\n    { "duration_minutes": "integer", "count": "integer" }\n  ],',
    '  "period_schedule": [\n'
    '    { "duration_minutes": "integer — the class-standard duration", "count": "integer" }\n'
    "  ],",
)

lp = edit(
    lp,
    "Science Lesson Plan Constitution · Version 1.0 · Secondary Stage · Internal Document",
    "Science Lesson Plan Constitution · Version 1.1 · Secondary Stage · Internal Document",
)

LP_LIVE.write_text(lp, encoding="utf-8")
print(f"LP   v1.0 -> v1.1  written: {LP_LIVE}")


# ══════════════════════════════════════════════════════════════════════════════
# ASSESSMENT CONSTITUTION · v1.1 -> v1.2   (A9 only; A6 confirmed, not amended)
# ══════════════════════════════════════════════════════════════════════════════
ac = (HERE / "assessment_constitution_v1.1_pre.txt").read_text(encoding="utf-8")

ac = edit(
    ac,
    "ARUVI · CHAPTER ASSESSMENT GENERATION CONSTITUTION · SCIENCE · SECONDARY STAGE · VERSION 1.1",
    "ARUVI · CHAPTER ASSESSMENT GENERATION CONSTITUTION · SCIENCE · SECONDARY STAGE · VERSION 1.2",
)

# A9 — one REMOVAL (the item-18 position prohibition) and two ADDITIONS.
# Never an arrangement rule: ordering is a pipeline stage (genon/normalize_options.py,
# STEP 6 of build_library.py), and naming arrangement at all keeps position salient to a
# model that should never reason about it.
ac = edit(
    ac,
    "MANDATE\n"
    "Every MCQ has exactly three diagnostic distractors (four options). Each is one\n"
    "nameable engagement failure: a misconception about the section; a confusion\n"
    "between two chapter concepts (same or adjacent section per Rule 3); or recall of a\n"
    "related-but-wrong detail from the section's slice.\n"
    "\n"
    "PROHIBITION\n"
    "No true/false; no implausible, arbitrary, or out-of-chapter distractors.\n"
    "Answer position carries no signal: is_correct MUST be distributed across A–D\n"
    "within an assessment and MUST NOT repeat on the same label across consecutive\n"
    "items or cluster on one letter.",
    "MANDATE\n"
    "Every MCQ has exactly three diagnostic distractors (four options). Each is one\n"
    "nameable engagement failure: a misconception about the section; a confusion\n"
    "between two chapter concepts (same or adjacent section per Rule 3); or recall of a\n"
    "related-but-wrong detail from the section's slice.\n"
    "Option order carries no meaning and is not yours to set: emit the four options in\n"
    "whatever order they were authored, and never let where an option sits influence how\n"
    "it is written. Uneven letters across a chapter are coincidence, not a defect.\n"
    "\n"
    "PROHIBITION\n"
    "1. No true/false; no implausible, arbitrary, or out-of-chapter distractors.\n"
    "2. MUST NOT write an option that refers to another option by its label (\"both A and\n"
    "   B\", \"none of the above\") — options are ordered downstream and a label reference\n"
    "   would be falsified.",
)

# A6 — the anchor is section_number, already carried on every item; the platform derives
# the unit. Stated once at integrity level so no run invents a period_ref.
ac = edit(
    ac,
    "· section_number is internal (generation + guide block); never in user-facing output.",
    "· section_number is internal (generation + guide block); never in user-facing output.\n"
    "· ANCHORING: section_number IS the item's anchor. The platform resolves it to the\n"
    "  unit(s) that teach the section through the LP's coverage_handoff period_numbers;\n"
    "  MUST NOT emit period_ref or any unit number on an item.",
)

ac = edit(
    ac,
    "Science Assessment Constitution · Version 1.1 · Secondary Stage · Internal Document",
    "Science Assessment Constitution · Version 1.2 · Secondary Stage · Internal Document",
)

AS_LIVE.write_text(ac, encoding="utf-8")
print(f"ASSESS v1.1 -> v1.2  written: {AS_LIVE}")
