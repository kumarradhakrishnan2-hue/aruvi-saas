#!/usr/bin/env python3
"""S6 · science · middle — stage preparation edits (testing.md §3, P1–P3).

Reproducible, idempotent-checked: every edit asserts EXACTLY ONE occurrence of the
string it replaces, so a re-run against an already-amended file fails loudly rather
than corrupting it.

WHAT THIS APPLIES
  P1  A1  — the period schedule is exactly ONE standard row at the class-standard
            duration (40 min VI–VII · 45 VIII). Restated in INPUTS 4, Rule 6's TIME
            statement and Amendment A3's field constraints.
      A5+A7 — THE SELF-CONTAINED REGISTER as ONE block, in a TWO-BAN cut:
            (1) no clock quantity, (2) no calendar time. The reference's third ban
            (forward reference / completion language) is DELIBERATELY NOT PORTED —
            founder ruling 2026-08-07. Science middle is the one stage whose plan is
            a single cognitive arc taught whole or not at all: every unit of a plan
            is served with every other unit of that plan, so forward reference and
            completion claims are TRUE here. Bans 1 and 3 are untouched by that
            reasoning — duration scaling and the Calendar Purge are orthogonal to
            the serve model — and both stand.
  P2  A6  — CONFIRMED, not amended: every item already carries `progression_stage`.
            One integrity block added recording that the anchor is DERIVED (stage →
            coverage_handoff.period_numbers → the LAST of them), and forbidding the
            model emitting period_ref.
      A9  — one removal + two additions, never an arrangement rule.
  P3      — Group B schema conversion: phases[{minutes, description}] ->
            time_bands[{minutes, activity}]. No band_id in the target shape.

Run from the repo root:  python3 genon/out/stage_prep_science_middle/apply_s6_amendments.py
"""
from __future__ import annotations

import difflib
import pathlib
import textwrap

ROOT = pathlib.Path(__file__).resolve().parents[3]
PREP = ROOT / "genon/out/stage_prep_science_middle"
LP = ROOT / "data/content/constitutions/lesson_plan/science/middle/lesson_plan_constitution.txt"
AS = ROOT / "data/content/constitutions/assessment/science/middle/assessment_constitution.txt"


def sub(text: str, old: str, new: str, what: str) -> str:
    n = text.count(old)
    assert n == 1, f"{what}: expected exactly 1 occurrence, found {n}"
    return text.replace(old, new)


# ─────────────────────────────────────────────────────────────────────────────
# P1 + P3 — the lesson plan constitution, v2.1 -> v2.2
# ─────────────────────────────────────────────────────────────────────────────
lp = LP.read_text(encoding="utf-8")

lp = sub(
    lp,
    "ARUVI — LESSON PLAN GENERATION CONSTITUTION · SCIENCE · VERSION 2.1",
    "ARUVI — LESSON PLAN GENERATION CONSTITUTION · SCIENCE · MIDDLE STAGE · VERSION 2.2",
    "header/VERSION",
)

# A1 — INPUTS 4
lp = sub(
    lp,
    "4. Period schedule — one or more rows of {duration in minutes, period count}",
    "4. Period schedule — exactly ONE row {duration_minutes, count}: the class-standard\n"
    "   duration (40 min for classes VI–VII, 45 for VIII) × the period count. Teacher\n"
    "   timetable variation never reaches generation; it is handled downstream at serve\n"
    "   time.",
    "A1/INPUTS 4",
)

# VOCABULARY — the "session" exclusion. The positional cross-reference examples are
# KEPT (deviation from the reference, declared): at this stage they are legal.
lp = sub(
    lp,
    'Never write "period" in prose the teacher reads.',
    'Never write "period" in prose the teacher reads; "session" is outside the register too.',
    "VOCABULARY/session",
)

REGISTER = """
THE SELF-CONTAINED REGISTER (binds Rules 6 and 10)
Two things no time band or teacher note may do, each because the platform enforces it:
1. NAME A CLOCK QUANTITY — the platform scales every band's minutes in proportion to the sitting that carries it, so a stated number is falsified silently: no "for three minutes", "the remaining time", "half the session". Where a task is genuinely brief or genuinely long, say so in kind — "a quick individual observation", "an extended investigation" — never in number.
2. NAME CALENDAR TIME — Aruvi keeps no calendar and sittings do not map to days: today, yesterday, this week, next class are unknowable at authoring.

FORWARD REFERENCE AND COMPLETION LANGUAGE ARE LEGAL AT THIS STAGE — the one place the reference constitution's third ban is deliberately not carried. The cognitive progression binds the chapter into a single arc that is taught whole or not at all, and every unit of a plan is served with every other unit of that plan. So a unit may look ahead, and a closing unit may draw the chapter together and say so, because at this stage both are true. Continuity by position — "the previous unit", "in the next unit" — is welcome, and Rule 10 asks for it.
"""

lp = sub(
    lp,
    '"session" is outside the register too.\n',
    '"session" is outside the register too.\n' + REGISTER,
    "register block insert",
)

# A1 — Rule 6's TIME statement; P3 — the mechanism is time_bands
lp = sub(
    lp,
    "The period schedule is a hard constraint. Total available minutes = sum of all "
    "(duration × count) products across all period rows. The full budget is for teaching. "
    "There is no assessment time inside this budget.\n"
    "\n"
    "Every activity MUST be designed to fit within its period's duration. The phases array "
    "is the mechanism for this: phases must account for the full period and their durations "
    "must sum exactly to period_duration_minutes.",
    "The period schedule is a hard constraint. It is a single standard row: total available "
    "minutes = duration × count, and the total period count = count. The full budget is for "
    "teaching. There is no assessment time inside this budget.\n"
    "\n"
    "Every activity MUST be designed to fit within its period's duration. The time_bands "
    "array is the mechanism for this: bands must account for the full period and their "
    "durations must sum exactly to period_duration_minutes.",
    "Rule 6/TIME + time_bands",
)

lp = sub(
    lp,
    "If a planned activity cannot be completed within the period, it must be scoped down — "
    "not left to overrun.",
    "If a planned activity cannot be completed within the period, it must be scoped down — "
    "not left to overrun.\n"
    "\n"
    "Band text is bound by THE SELF-CONTAINED REGISTER: a band names no clock quantity and "
    "no calendar time.",
    "Rule 6/register binding",
)

# Rule 10 — bind the register in the constraints list
lp = sub(
    lp,
    "- MUST NOT restate the activity_description verbatim — teacher_notes is\n"
    "  guidance on running the activity, not a second description of it.",
    "- MUST NOT restate the activity_description verbatim — teacher_notes is\n"
    "  guidance on running the activity, not a second description of it.\n"
    "- MUST NOT breach THE SELF-CONTAINED REGISTER — no clock quantity, no\n"
    "  calendar time. Links to other units, forward or backward, are welcome:\n"
    "  see the register.",
    "Rule 10/register binding",
)

# A1 — A3 field constraint
lp = sub(
    lp,
    "The system MUST populate every field. Empty strings and empty arrays are not permitted "
    "for required fields.\n"
    "\n"
    "Each period in lesson_plan.periods[] MUST conform to this object schema:",
    "The system MUST populate every field. Empty strings and empty arrays are not permitted "
    "for required fields. Field constraint (do not violate):\n"
    "- period_schedule: exactly one row — the class-standard duration × count (INPUTS 4).\n"
    "\n"
    "Each period in lesson_plan.periods[] MUST conform to this object schema:",
    "A3/period_schedule constraint",
)

# P3 — the schema conversion itself
lp = sub(
    lp,
    '  "phases":                  [\n'
    "                               {\n"
    '                                 "minutes":     string — time range e.g. "0–10",\n'
    '                                 "description": string — one sentence on what happens in this phase; no role embedding\n'
    "                               }\n"
    "                             ]\n"
    "                             — phases must cover the full period from 0 to "
    "period_duration_minutes with no gaps; durations must sum exactly to period_duration_minutes,",
    '  "time_bands":              [\n'
    "                               {\n"
    '                                 "minutes":  string — time range e.g. "0-10",\n'
    '                                 "activity": string — one sentence on what happens in this band; no role embedding\n'
    "                               }\n"
    "                             ]\n"
    "                             — bands must cover the full period from 0 to "
    "period_duration_minutes with no gaps; durations must sum exactly to period_duration_minutes,",
    "P3/phases -> time_bands",
)

assert "phases[" not in lp and '"phases"' not in lp, "P3: a phases declaration survived"
assert "time_bands" in lp, "P3: time_bands absent"

# ─────────────────────────────────────────────────────────────────────────────
# P2 — the assessment constitution, v1.3 -> v1.4
# ─────────────────────────────────────────────────────────────────────────────
a = AS.read_text(encoding="utf-8")

a = sub(
    a,
    "Chapter Assessment Constitution — Science\n",
    "Chapter Assessment Constitution — Science · Middle Stage\n",
    "assessment/title",
)
a = sub(
    a,
    "Version 1.3 · Ten rules governing AI assessment generation for Science",
    "Version 1.4 · Ten rules governing AI assessment generation for Science",
    "assessment/VERSION",
)

# --- Rule 7's ASCII table: derive the column geometry, never hardcode it ---------
lines = a.split("\n")
sep_i = next(i for i, ln in enumerate(lines)
             if ln.startswith("+---") and "Rule 7" in lines[i + 1])
sep = lines[sep_i]
lc = sep.index("+", 1) - 1                     # left column inner width
rc = len(sep) - lc - 3                         # right column inner width


def row(label: str, text: str) -> str:
    out = "|" + (" " + label).ljust(lc) + "|" + (" " + text).ljust(rc) + "|"
    assert len(out) == len(sep), f"geometry mismatch: {len(out)} vs {len(sep)}"
    return out


def para(text: str) -> list[str]:
    return [row("", ln) for ln in textwrap.wrap(text, rc - 2)]


# A9 addition 1 — the option-order mandate, in the v1.7 wording.
anchor = "· recall of a related but incorrect detail from the same chapter section"
hits = [i for i, ln in enumerate(lines) if anchor in ln]
assert len(hits) == 1, f"A9/mandate anchor: found {len(hits)}"
i = hits[0]
lines[i + 1:i + 1] = [row("", "")] + para(
    "Option order carries no meaning and is not yours to set: emit the four options "
    "in whatever order they were authored, and never let where an option sits "
    "influence how it is written. Uneven letters across a chapter are coincidence, "
    "not a defect."
)

# A9 removal — the MEMORY item-18 position prohibition (2 wrapped lines) — and
# addition 2, the by-label option-reference ban, in its place.
old_a = "The system MUST NOT place the correct answer at the same label across consecutive"
hits = [i for i, ln in enumerate(lines) if old_a in ln]
assert len(hits) == 1, f"A9/item-18 line 1: found {len(hits)}"
i = hits[0]
assert lines[i + 1].split("|")[2].strip() == "chapter.", \
    f"A9/item-18 line 2: unexpected continuation {lines[i + 1]!r}"
lines[i:i + 2] = para(
    'The system MUST NOT write an option that refers to another option by its label '
    '("both A and B", "none of the above") — options are ordered downstream and a '
    "label reference would be falsified."
)
a = "\n".join(lines)

assert "MUST NOT place the correct answer" not in a, "A9: item-18 survived"
for banned in ("alphabetically", "never led with", "first word at which they differ"):
    assert banned not in a.lower(), f"A9: an arrangement rule crept in ({banned})"

# A6 — the derived-anchor integrity block. Science middle's unique link is the STAGE.
INTEGRITY = """INTEGRITY CONSTRAINTS (system level — override any other instruction)

· coverage_handoff is committed — no reopening competencies, no re-deriving its fields.
· ANCHORING IS DERIVED, NOT DECLARED: progression_stage IS the item's anchor. The
  platform resolves it to the units that teach that stage through the LP's
  coverage_handoff period_numbers, and anchors the item to the LAST of them — an item
  tests the stage's whole implied LO, so it becomes available only when the stage
  completes. MUST NOT emit period_ref, phase_ref, or any unit number on an item.
· Progression-stage numbers and labels are internal to generation and the guide block;
  they never appear in user-facing output (Rule 4).

"""

a = sub(
    a,
    "Amendment A1 — Full Assessment JSON Schema",
    INTEGRITY + "Amendment A1 — Full Assessment JSON Schema",
    "A6/integrity block",
)
assert "phase_ref" in a and a.count("phase_ref") == 1, "A6: phase_ref should appear only in the ban"

# ─────────────────────────────────────────────────────────────────────────────
# write + diff
# ─────────────────────────────────────────────────────────────────────────────
for path, new, pre, out in (
    (LP, lp, PREP / "lesson_plan_constitution_v2.1_pre.txt", PREP / "lp_v2.1_to_v2.2.diff"),
    (AS, a, PREP / "assessment_constitution_v1.3_pre.txt", PREP / "assess_v1.3_to_v1.4.diff"),
):
    path.write_text(new, encoding="utf-8")
    d = difflib.unified_diff(
        pre.read_text(encoding="utf-8").split("\n"), new.split("\n"),
        fromfile=f"{path.name} (pre)", tofile=f"{path.name} (post)", lineterm="",
    )
    out.write_text("\n".join(d) + "\n", encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}  ->  {out.name}")

print("S6 P1/P2/P3 amendments applied.")
