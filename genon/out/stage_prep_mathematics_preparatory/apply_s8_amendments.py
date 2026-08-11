#!/usr/bin/env python3
"""S8 · mathematics · preparatory — the P1/P2/P3 amendment pass (testing.md §3).

Reproducible edit script, in the S3/S4/S6/S7 pattern: every edit asserts EXACTLY ONE
occurrence of its target before replacing, and the run closes on guard assertions for
the strings that must NOT come back (the struck A9 arrangement sentence, the retired
`phases` shape, an invented `section_anchor`) and for the strings that must now be
present.

Landed pair:  LP  v1.1 -> v1.2   ·   assessment  v1.2 -> v1.3
Reference:    SS·secondary LP v1.10 · assessment v1.7, via the mathematics·middle
              v3.4 / v3.3 adaptation (same subject vocabulary, one stage up, and the
              same 8-rule FAMILY — period-field — so the anchoring block ports almost
              verbatim, changing only the field name and the code vocabulary).

WHAT THIS PASS DOES *NOT* DO (founder ruling 2026-08-10, carried from S7).
No new field is invented to feed the serve engine. `section_anchor` is NOT added to the
period, and no `period_number` is added anywhere. The unit anchor is already in the
authored file under this stage's own name — `section_refs[]` — and the plugin mediates
the read (`mathematics/subject.py::genon_unit_anchor`). That is P5.5's work, not P1's.

The ONE shape item a tolerant read cannot absorb is P3: `compile.py` rebuilds the timed
spine from `p["time_bands"]` (:124) and asserts an inventory invariant over
`tb["activity"]` (:208-210). Preparatory is Group B and the conversion is real, exactly
as it was for science·middle (S6) and mathematics·middle (S7).

ALSO REPAIRED HERE (a defect, not an amendment): the assessment schema's
`what_each_option_reveals` example read `{ "A", "C", "C", "D" }` — four keys, "C"
twice, "B" missing. S7's distractors-only pass (2026-08-10) rewrote the FIRST line of
the two-line example and left the second, and this file was collateral. The example now
shows the three NON-CORRECT labels the prose has mandated since v1.2.
"""
from __future__ import annotations

import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).resolve().parent
LP = ROOT / "data/content/constitutions/lesson_plan/mathematics/preparatory/lesson_plan_constitution.txt"
AS = ROOT / "data/content/constitutions/assessment/mathematics/preparatory/assessment_constitution.txt"


def sub(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    assert n == 1, f"{label}: expected exactly 1 occurrence, found {n}"
    return text.replace(old, new)


# ══════════════════════════════════════════════════════════════════════════════
# LESSON PLAN  v1.1 -> v1.2
# ══════════════════════════════════════════════════════════════════════════════
REGISTER = """
THE SELF-CONTAINED REGISTER (binds Rule 6 and teacher_notes)
Three things no time band or teacher note may do, each because the platform enforces it:
1. NAME A CLOCK QUANTITY — the platform scales every band's minutes in proportion to the sitting that carries it, so a stated number is falsified silently: no "for three minutes", "the remaining time", "half the session". Where a task is genuinely brief or genuinely long, say so in kind — "a quick count round the class", "an unhurried making activity" — never in number.
2. POINT FORWARD OR CLAIM COMPLETION — a teacher's plan may end, or hand over to a companion variant's unit, after any unit, so "the next unit", "as we will see", "now that we have weighed everything" are wrong for someone. Each unit closes on its own ground.
3. NAME CALENDAR TIME — Aruvi keeps no calendar and sittings do not map to days: today, yesterday, this week, next class are unknowable at authoring.
Backward continuity is welcome, and is best carried by naming the content built on ("The children have grouped in tens to count large collections, …") rather than a unit's position.
"""

A1 = """4. Period schedule — exactly ONE row {duration_minutes, count}: the
   class-standard duration (40 min for classes up to VII, 45 for VIII,
   50 for IX–X — the master-plan calibration bands, not NCF's flat 40)
   × the period count; total = B. Teacher timetable variation never
   reaches generation; it is handled downstream at serve time."""


def amend_lp(t: str) -> str:
    # ── VERSION ──────────────────────────────────────────────────────────────
    t = sub(t,
            "ARUVI — MATHEMATICS LESSON PLAN CONSTITUTION (PREPARATORY) · VERSION 1.1",
            "ARUVI — MATHEMATICS LESSON PLAN CONSTITUTION (PREPARATORY) · VERSION 1.2",
            "LP version line")

    # ── A5+A7 · VOCABULARY was TEACHING the forward reference ban 2 forbids ──
    # Its cross-reference examples were literally "the previous unit" / "this unit".
    # Same correction S7 made to middle; "session" joins the excluded register.
    t = sub(t,
            'and any cross-reference to another chunk (e.g. "the previous unit", '
            '"this unit"). The token "period"',
            'and any cross-reference to another chunk. The token "period"',
            "VOCABULARY positional examples")
    t = sub(t,
            'Never write "period" in prose the teacher reads.\n',
            'Never write "period" in prose the teacher reads; "session" is outside '
            'the register too.\n',
            "VOCABULARY session exclusion")

    # ── A5+A7 · the register as ONE block, immediately after VOCABULARY ──────
    t = sub(t,
            "Stage: Preparatory (Grades III–V) · Maths Mela\n\n"
            "================================================================================\n"
            "DESIGN PRINCIPLE\n",
            "Stage: Preparatory (Grades III–V) · Maths Mela\n" + REGISTER +
            "\n================================================================================\n"
            "DESIGN PRINCIPLE\n",
            "register block")

    # ── A1 · exactly ONE standard period row ────────────────────────────────
    t = sub(t, "4. Period schedule: {duration, count} rows; total = B.", A1, "A1")

    # ── P3 · phases[{minutes, description}] -> time_bands[{minutes, activity}] ─
    t = sub(t,
            "Each period's phases sum exactly to `period_duration_minutes`. Minimum 3\n"
            "phases per period. `phases[].minutes` is a STRING time-range (e.g.\n"
            '"0–10", "10–25") tiling 0..period_duration with no gaps or overlaps.\n'
            "Overrun is not permitted.",
            "Each period's time bands sum exactly to `period_duration_minutes`.\n"
            "Minimum 3 bands per period. `time_bands[].minutes` is a STRING\n"
            'time-range (e.g. "0–10", "10–25") tiling 0..period_duration with no\n'
            "gaps or overlaps. Overrun is not permitted.",
            "P3 Rule 5")
    t = sub(t,
            "RULE 6 | PHASE NARRATION USES book_ref, NOT INTERNAL ID",
            "RULE 6 | BAND NARRATION USES book_ref, NOT INTERNAL ID",
            "P3 Rule 6 heading")
    t = sub(t,
            "When a phase invokes a task, the phase `description` names it by",
            "When a time band invokes a task, the band's `activity` names it by",
            "P3 Rule 6 narration")
    t = sub(t,
            "The phase description MUST NOT use the internal `id`. Internal ids live\n"
            "only in the structured `tasks_in_class[]` array as join keys.",
            "Every band is additionally bound by THE SELF-CONTAINED REGISTER: it\n"
            "names no clock quantity, points forward at nothing, claims no\n"
            "completion, and names no calendar time. Each band speaks in the present\n"
            "of its own activity; unit-to-unit linking lives only in teacher_notes.\n"
            "\n"
            "The band's `activity` MUST NOT use the internal `id`. Internal ids live\n"
            "only in the structured `tasks_in_class[]` array as join keys.",
            "P3 Rule 6 id ban + register bind")
    t = sub(t,
            "appear in any prose the teacher reads — phases or teacher_notes. When",
            "appear in any prose the teacher reads — time bands or teacher_notes. When",
            "P3 Rule 6 S-code prose")
    t = sub(t,
            "in the mapping JSON, never in periods, phases, or teacher_notes.",
            "in the mapping JSON, never in periods, time bands, or teacher_notes.",
            "P3 Rule 7")
    t = sub(t,
            '  "phases": [\n'
            '    { "minutes": string, "description": string }  // narration via book_ref (Rule 6)\n'
            '  ],',
            '  "time_bands": [\n'
            '    { "minutes": string, "activity": string }     // narration via book_ref (Rule 6)\n'
            '  ],',
            "P3 schema")

    # ── A5+A7 · teacher_notes was asking for POSITIONAL continuity ──────────
    t = sub(t,
            '  "teacher_notes":           string,            // 2–3 sentences, flowing prose.\n'
            '                                                //   Recap prior unit; flag one\n',
            '  "teacher_notes":           string,            // 2–3 sentences, flowing prose.\n'
            '                                                //   Carry continuity by NAMING\n'
            '                                                //   the content built on, never\n'
            '                                                //   a unit\'s position (THE\n'
            '                                                //   SELF-CONTAINED REGISTER,\n'
            '                                                //   ban 2); flag one\n',
            "teacher_notes continuity")

    # ── footer ──────────────────────────────────────────────────────────────
    t = sub(t,
            "Mathematics Lesson Plan Constitution (Preparatory) · Version 1.1 · Internal Document",
            "Mathematics Lesson Plan Constitution (Preparatory) · Version 1.2 · Internal Document",
            "LP footer")
    return t


# ══════════════════════════════════════════════════════════════════════════════
# ASSESSMENT  v1.2 -> v1.3
# ══════════════════════════════════════════════════════════════════════════════
A9 = """
Option order carries no meaning and is not yours to set: emit the four
options in whatever order they were authored, and never let where an
option sits influence how it is written. Uneven letters across a chapter
are coincidence, not a defect.

PROHIBITED: an option that refers to another option by its label ("both A
and B", "none of the above", "all of the above") — options are ordered
downstream and a label reference would be falsified.
"""

ANCHORING = """================================================================================
ANCHORING (PLATFORM INTEGRITY — NOT A GENERATION CHOICE)
================================================================================

· `section_ref` IS the item's anchor. It is copied verbatim from the LP
  handoff entry the item was generated from, in the LP's own vocabulary
  ("S3"), and the platform resolves it to the unit(s) that teach that
  section by matching it against each period's own `section_refs[]`.
  Nothing about that link is declared by the generator; it is derived.

· Where a section is taught across several units, the item anchors at the
  LAST of them. An item tests what its section teaches, so it becomes
  available only once the section completes: a class that was not taught
  all of it cannot be tasked on any of it.

· MUST NOT emit `period_ref`, `period_number`, or any unit number on an
  item. Declaring the link would freeze an arrangement the platform varies
  per teacher.

· `section_title` is likewise copied verbatim from the handoff entry and
  matches the summary's `sections[i].title`. Both fields are pass-through:
  the generator neither reformats nor abbreviates them.

· `task_id` is NOT an anchor in this sense (Rule 8). It seeds the exercise
  companion only, stays internal, and never reaches the platform's link
  resolution.

"""


def amend_assess(t: str) -> str:
    t = sub(t,
            "ARUVI — MATHEMATICS ASSESSMENT CONSTITUTION (PREPARATORY) · VERSION 1.2",
            "ARUVI — MATHEMATICS ASSESSMENT CONSTITUTION (PREPARATORY) · VERSION 1.3",
            "AS version line")

    # ── A9 · two lines in Rule 9's MCQ block; no arrangement rule, ever ─────
    t = sub(t,
            "MCQ requires exactly 4 options, exactly one `is_correct: true`, and a\n"
            "populated `what_each_option_reveals`. SCR/NUM need no options; the teacher\n"
            "reads the answer from `teacher_guide`.\n",
            "MCQ requires exactly 4 options, exactly one `is_correct: true`, and a\n"
            "populated `what_each_option_reveals`. SCR/NUM need no options; the teacher\n"
            "reads the answer from `teacher_guide`.\n" + A9,
            "A9")

    # ── DEFECT REPAIR · the reveals example lost "B" and gained a second "C" ─
    t = sub(t,
            '            "what_each_option_reveals": { "A": string, "C": string,\n'
            '                                          "C": string, "D": string } | {},\n',
            '            "what_each_option_reveals": { "A": string, "C": string,\n'
            '                                          "D": string } | {},\n'
            '                                        // the three NON-CORRECT labels\n'
            '                                        // only; the correct option is\n'
            '                                        // omitted (Rule 6)\n',
            "reveals example repair")

    # ── A6 · the anchoring block, before the schema ─────────────────────────
    t = sub(t,
            "================================================================================\n"
            "ASSESSMENT JSON SCHEMA\n",
            ANCHORING +
            "================================================================================\n"
            "ASSESSMENT JSON SCHEMA\n",
            "A6 anchoring block")

    t = sub(t,
            "Mathematics Assessment Constitution (Preparatory) · Version 1.1 · Internal Document",
            "Mathematics Assessment Constitution (Preparatory) · Version 1.3 · Internal Document",
            "AS footer (was two bumps stale)")
    return t


# ══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    lp0 = LP.read_text(encoding="utf-8")
    as0 = AS.read_text(encoding="utf-8")
    shutil.copy2(LP, OUT / "lesson_plan_constitution_v1.1_pre.txt")
    shutil.copy2(AS, OUT / "assessment_constitution_v1.2_pre.txt")

    lp1 = amend_lp(lp0)
    as1 = amend_assess(as0)

    # ── guards · what must NOT be there ─────────────────────────────────────
    assert "phases[" not in lp1, "GUARD: `phases[` survived P3"
    assert '"phases"' not in lp1, 'GUARD: `"phases"` survived P3'
    assert "band_id" not in lp1, "GUARD: band_id must not enter the target shape"
    for bad in ("alphabetically", "never led with", "first word at which they differ",
                "vary in position", "same label"):
        assert bad not in as1.lower(), f"GUARD: struck A9 arrangement string {bad!r} present"
    assert "phase_ref" not in as1 and "phase_ref" not in lp1, "GUARD: phase_ref reintroduced"
    assert "section_anchor" not in lp1, "GUARD: section_anchor invented in the LP"
    assert "period_ref" not in lp1, "GUARD: period_ref invented in the LP"
    assert lp1.count("period_number") == lp0.count("period_number"), \
        "GUARD: a period_number field was added somewhere"
    # A2/A3/A4 are cancelled; X3 is void. None of their vocabulary may appear.
    for cancelled in ("role_handoff", "unit_handoff", "band_ref", "role weighting"):
        assert cancelled not in lp1 and cancelled not in as1, \
            f"GUARD: cancelled amendment vocabulary {cancelled!r} present"
    # V-rules live in the platform-composed brief, never in a constitution.
    for vrule in ("section registry", "synthesis unit", "reserved token"):
        assert vrule not in lp1.lower() and vrule not in as1.lower(), \
            f"GUARD: V-rule {vrule!r} crept into a constitution"

    # ── guards · what MUST be there ────────────────────────────────────────
    assert lp1.count("THE SELF-CONTAINED REGISTER") == 2, \
        "GUARD: register heading + Rule 6 bind expected"
    assert "//   SELF-CONTAINED REGISTER,\n" in lp1, "GUARD: teacher_notes register bind"
    assert lp1.count("time_bands") == 2, "GUARD: time_bands expected in Rule 5 and the schema"
    assert '"activity": string' in lp1, "GUARD: the band's activity key"
    assert "exactly ONE row {duration_minutes, count}" in lp1, "GUARD: A1"
    assert "ANCHORING (PLATFORM INTEGRITY" in as1, "GUARD: A6 block"
    assert "Option order carries no meaning" in as1, "GUARD: A9 mandate line"
    assert "by its label" in as1, "GUARD: A9 by-label prohibition"
    assert as1.count('"C": string') == 1, "GUARD: the duplicated reveals key survived"

    LP.write_text(lp1, encoding="utf-8")
    AS.write_text(as1, encoding="utf-8")
    print("LP  v1.1 -> v1.2  ", LP)
    print("AS  v1.2 -> v1.3  ", AS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
