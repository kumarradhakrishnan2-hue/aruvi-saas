#!/usr/bin/env python3
"""
S4 · mathematics · secondary — stage-preparation amendments (docs/testing.md §3, P1–P4).

Carry-forward from the SS·secondary reference pair (LP v1.10 · assessment v1.7).

  LP         v1.0 -> v1.1   A1 (one standard row) + A5/A7 (the self-contained register)
                            + A6's derived-anchor integrity line
  Assessment v1.0 -> v1.1   A6-confirm (derived section_number anchor) + A9 (two lines;
                            the item-18 removal is N/A — this file never carried it)
  P3                        N/A — Group A, time_bands already
  P4                        CHANGELOG.md sidecars, written separately

Every edit asserts EXACTLY ONE occurrence of its anchor before replacing, so a re-run
on an already-amended file fails loudly rather than silently double-applying.

Run from the repo root:  python3 genon/out/stage_prep_mathematics_secondary/apply_s4_amendments.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LP = ROOT / "data/content/constitutions/lesson_plan/mathematics/secondary/lesson_plan_constitution.txt"
AS = ROOT / "data/content/constitutions/assessment/mathematics/secondary/assessment_constitution.txt"

edits = []


def sub(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"ABORT [{label}]: anchor found {n} times, expected exactly 1\n---\n{old[:300]}\n---")
    edits.append(label)
    return text.replace(old, new, 1)


def absent(text, needle, label):
    if needle.lower() in text.lower():
        raise SystemExit(f"ABORT [{label}]: '{needle}' must be absent but is present")


# ===========================================================================
# LESSON PLAN CONSTITUTION  ·  v1.0 -> v1.1
# ===========================================================================
lp = LP.read_text()

lp = sub(
    lp,
    "MATHEMATICS · SECONDARY STAGE · VERSION 1.0",
    "MATHEMATICS · SECONDARY STAGE · VERSION 1.1",
    "LP VERSION line",
)

# --- A5/A7 consequential: VOCABULARY drops its positional cross-reference examples
# (they instruct exactly what the position doctrine now discourages) and gains the
# "session" exclusion, per the v1.10 reference.
lp = sub(
    lp,
    'The atomic teaching chunk is called a "unit" in ALL teacher-facing prose — '
    "teacher_notes, activity titles, homework, and any cross-reference to another chunk "
    '(e.g. "the previous unit", "this unit"). The token "period" is retained ONLY in '
    "(a) schema field names (period_number, period_duration_minutes, periods[], etc.) and "
    "(b) the scheduling/allocation budget (period schedule, period count, per-period budget). "
    'Never write "period" in prose the teacher reads.',
    'The atomic teaching chunk is called a "unit" in ALL teacher-facing prose — '
    'teacher_notes, activity titles, homework. The token "period" is retained ONLY in '
    "(a) schema field names (period_number, period_duration_minutes, periods[], etc.) and "
    "(b) the scheduling/allocation budget (period schedule, period count, per-period budget). "
    'Never write "period" in prose the teacher reads; "session" is outside the register too.',
    "LP VOCABULARY (A5/A7 consequential)",
)

# --- A5 + A7 · THE SELF-CONTAINED REGISTER, as ONE block after VOCABULARY.
REGISTER = """
THE SELF-CONTAINED REGISTER (binds Rules 9 and 10)
Three things no time band or teacher note may do, each because the platform enforces it:
1. NAME A CLOCK QUANTITY — the platform scales every band's minutes in proportion to the sitting that carries it, so a stated number is falsified silently: no "for three minutes", "the remaining time", "half the session". Where a task is genuinely brief or genuinely long, say so in kind — "a quick individual calculation", "an extended derivation" — never in number.
2. POINT FORWARD OR CLAIM COMPLETION — a teacher's plan may end, or hand over to a companion variant's unit, after any unit, so "the next unit", "as we will see", "having covered all three identities" are wrong for someone. Each unit closes on its own ground.
3. NAME CALENDAR TIME — Aruvi keeps no calendar and sittings do not map to days: today, yesterday, this week, next class are unknowable at authoring.
Backward continuity is welcome, and is best carried by naming the content built on ("Having established the expansion of a binomial product, …" — Rule 10's continuity link) rather than a unit's position.
"""

lp = sub(
    lp,
    "\nSubject group : mathematics\nStage         : Secondary Stage\n",
    REGISTER + "\nSubject group : mathematics\nStage         : Secondary Stage\n",
    "LP register block (A5 + A7)",
)

# --- A1 · INPUTS 4 — exactly ONE standard row.
lp = sub(
    lp,
    "4. Period schedule — one or more rows of {duration_minutes, count}.",
    "4. Period schedule — exactly ONE row {duration_minutes, count}: the class-standard\n"
    "   duration (40 min for classes up to VII, 45 for VIII, 50 for IX) × the period\n"
    "   count. Teacher timetable variation never reaches generation; it is handled\n"
    "   downstream at serve time.",
    "LP INPUTS 4 (A1)",
)

# --- Rule 9 · teacher-facing text — bind the register by reference, never restate it.
lp = sub(
    lp,
    "5. Internal item ids (WE-N, E-N) — use book_ref instead.\n",
    "5. Internal item ids (WE-N, E-N) — use book_ref instead.\n"
    "6. Anything barred by THE SELF-CONTAINED REGISTER. Each band speaks in the present\n"
    "   of its own activity; sequence lives in the plan's structure, and unit-to-unit\n"
    "   linking lives only in teacher_notes (Rule 10).\n",
    "LP Rule 9 prohibition 6 (register bind)",
)

# --- Rule 10 · the continuity link becomes position-free (reference wording).
lp = sub(
    lp,
    "- A brief recap of what the previous unit covered and how it connects to this\n"
    "  one (omit for the first unit).\n",
    "- A continuity link to the content already taught — named by that content\n"
    "  itself, never by its position. The first unit instead orients the teacher to\n"
    "  the chapter's entry point.\n",
    "LP Rule 10 continuity link",
)

# --- Rule 10 · prohibition binds the register.
lp = sub(
    lp,
    'teacher_notes MUST NOT begin with the word "Transition" or any section label,\n'
    "MUST NOT contain C-codes, CG codes, internal item ids, or effort-index terms,\n"
    "and MUST NOT exceed three sentences. Refer to any textbook item by book_ref.",
    'teacher_notes MUST NOT begin with the word "Transition" or any section label,\n'
    "MUST NOT contain C-codes, CG codes, internal item ids, or effort-index terms,\n"
    "and MUST NOT exceed three sentences. Refer to any textbook item by book_ref.\n"
    "MUST NOT breach THE SELF-CONTAINED REGISTER.",
    "LP Rule 10 prohibition (register bind)",
)

# --- A1 · INTEGRITY · TIME restated for the single standard row.
lp = sub(
    lp,
    "- TIME: total minutes = sum of (duration × count) per schedule row; total period\n"
    "  count = sum of row counts. Each period has exactly one anchored section's work\n"
    "  calibrated to its duration. The full budget is teaching only — no period is\n"
    "  reserved for assessment, and no assessment task or time estimate is embedded\n"
    "  in the lesson plan.",
    "- TIME: the schedule is a single standard row. Total minutes = duration × count.\n"
    "  Total period count = count. Each period has exactly one anchored section's work\n"
    "  calibrated to the standard duration. The full budget is teaching only — no period\n"
    "  is reserved for assessment, and no assessment task or time estimate is embedded\n"
    "  in the lesson plan.\n"
    "- ITEM ANCHORING IS DERIVED, NOT DECLARED: an assessment item's anchor unit is\n"
    "  resolved by the platform from its section_number through this handoff's\n"
    "  period_numbers. MUST NOT emit period_ref (or any unit number) on an assessment\n"
    "  item — at this stage the unique link is the SECTION, and a section may be taught\n"
    "  across several units (Rule 7).",
    "LP INTEGRITY TIME + derived anchoring (A1, A6)",
)

# --- A1 · A3 schema comment + field constraint.
lp = sub(
    lp,
    '  "period_schedule": [ { "duration_minutes": "integer", "count": "integer" } ],',
    '  "period_schedule": [ { "duration_minutes": "integer — the class-standard duration", "count": "integer" } ],',
    "LP A3 period_schedule comment (A1)",
)

lp = sub(
    lp,
    "Field constraints:\n"
    "- time_bands tile the period exactly from 0 to period_duration_minutes, no gaps\n"
    "  or overlaps; minimum 3 bands per period.\n",
    "Field constraints:\n"
    "- period_schedule: exactly one row — the class-standard duration × count (INPUTS 4).\n"
    "- time_bands tile the period exactly from 0 to period_duration_minutes, no gaps\n"
    "  or overlaps; minimum 3 bands per period.\n",
    "LP A3 field constraint (A1)",
)

# --- A5/A7 consequential: the A3 schema echoed Rule 10's OLD positional framing
# ("recap-and-connect"). Rule 10's bullet is now position-free, so the echo is pointed at
# the rule instead of restating a framing that no longer exists — the shape
# science·secondary's A3 comment already had ("see Rule 10").
lp = sub(
    lp,
    '        "teacher_notes": "string — 2–3 sentences (Rule 10); recap-and-connect, '
    'one likely error from this section, optional self-study book_ref",',
    '        "teacher_notes": "string — 2–3 sentences (Rule 10); continuity by content '
    'not position, one likely error from this section, optional self-study book_ref",',
    "LP A3 teacher_notes comment (A5/A7 consequential)",
)

lp = sub(
    lp,
    "Mathematics Lesson Plan Constitution · Version 1.0 · Secondary Stage · Internal Document",
    "Mathematics Lesson Plan Constitution · Version 1.1 · Secondary Stage · Internal Document",
    "LP footer version",
)

# --- Guards: P3 target shape intact, no cancelled amendment or arrangement rule crept in.
for needle in ("phases[", '"phases"', "band_id", "alphabetically", "never led with",
               "first word at which they differ"):
    absent(lp, needle, "LP guard")
assert lp.count("time_bands") >= 2, "LP: time_bands vanished"
assert lp.count("THE SELF-CONTAINED REGISTER") == 3, (
    f"LP: register referenced {lp.count('THE SELF-CONTAINED REGISTER')} times, expected 3 "
    "(the block heading + Rule 9 + Rule 10)"
)

LP.write_text(lp)

# ===========================================================================
# ASSESSMENT CONSTITUTION  ·  v1.0 -> v1.1
# ===========================================================================
a = AS.read_text()

a = sub(
    a,
    "MATHEMATICS · SECONDARY STAGE · VERSION 1.0",
    "MATHEMATICS · SECONDARY STAGE · VERSION 1.1",
    "AS VERSION line",
)

# --- A9 line 1 · option order carries no meaning (v1.7 wording, Rule 7 MANDATE).
a = sub(
    a,
    "predictable slip (sign error, off-by-one in a pattern's nth term, transposing a\n"
    "and b); or recall of a related-but-wrong definition from the section's slice.\n",
    "predictable slip (sign error, off-by-one in a pattern's nth term, transposing a\n"
    "and b); or recall of a related-but-wrong definition from the section's slice.\n"
    "Option order carries no meaning and is not yours to set: emit the four options in\n"
    "whatever order they were authored, and never let where an option sits influence how\n"
    "it is written. Uneven letters across a chapter are coincidence, not a defect.\n",
    "AS Rule 7 option-order mandate (A9)",
)

# --- A9 line 2 · the by-label option-reference prohibition, with its reason.
#     The pre-existing "none of the above"/"all of the above" ban is absorbed into it —
#     same prohibition, now carrying why a downstream sort cannot reorder it.
a = sub(
    a,
    "PROHIBITION\n"
    "No true/false; no implausible, arbitrary, or out-of-chapter distractors; no\n"
    '"none of the above" / "all of the above".',
    "PROHIBITION\n"
    "1. No true/false; no implausible, arbitrary, or out-of-chapter distractors.\n"
    "2. MUST NOT write an option that refers to another option by its label (\"both A and\n"
    "   B\", \"none of the above\", \"all of the above\") — options are ordered downstream and a\n"
    "   label reference would be falsified.",
    "AS Rule 7 by-label prohibition (A9)",
)

# --- A6-confirm · the anchor is DERIVED from section_number; period_ref forbidden.
a = sub(
    a,
    "· section_number is internal (generation + guide block); never in user-facing output.\n",
    "· section_number is internal (generation + guide block); never in user-facing output.\n"
    "· ANCHORING: section_number IS the item's anchor. The platform resolves it to the\n"
    "  unit(s) that teach the section through the LP's coverage_handoff period_numbers;\n"
    "  MUST NOT emit period_ref or any unit number on an item.\n",
    "AS integrity anchoring line (A6)",
)

a = sub(
    a,
    "Mathematics Assessment Constitution · Version 1.0 · Secondary Stage · Internal Document",
    "Mathematics Assessment Constitution · Version 1.1 · Secondary Stage · Internal Document",
    "AS footer version",
)

for needle in ("alphabetically", "never led with", "first word at which they differ",
               "phase_ref", "is_correct MUST", "consecutive items"):
    absent(a, needle, "AS guard")
assert a.count("period_ref") == 1, "AS: period_ref should appear exactly once — in the ban"

AS.write_text(a)

print(f"OK — {len(edits)} edits applied:")
for e in edits:
    print(f"  · {e}")
print("\nP3: N/A (Group A — time_bands already; no phases[ or band_id in either file)")
print("A9 removal: N/A — this file never carried the item-18 position prohibition")
