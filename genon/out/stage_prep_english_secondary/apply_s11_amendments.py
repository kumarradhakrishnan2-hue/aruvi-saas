#!/usr/bin/env python3
"""S11 · english · secondary — the P1/P2/P3 amendment pass (testing.md §3).

Reproducible edit script, in the S3/S4/S6/S7/S8 pattern: every edit asserts EXACTLY ONE
occurrence of its target before replacing, and the run closes on guard assertions for the
strings that must NOT come back (the struck A9 arrangement sentence, the retired `phases`
shape, an invented `section_anchor`, any cancelled amendment or V-rule) and for the strings
that must now be present.

Landed pair:  LP  v1.1 -> v1.2   ·   assessment  v1.3 -> v1.4
Reference:    SS·secondary LP v1.10 · assessment v1.7, read through the mathematics
              middle/preparatory adaptation — english is the THIRD stage-family in the
              period-field carrier family (8-rule row 7), so the anchoring block ports from
              rows 4/5 changing only the join key and the code vocabulary.

WHAT THIS PASS DOES *NOT* DO (founder ruling 2026-08-10, carried from S7 and S8).
No new field is invented to feed the serve engine. `section_anchor` is NOT added to the
period and no `period_number` is added anywhere. English's unit anchor is already in the
authored file under this stage's own names — `section_id` + `spines_taught[]` — and the
plugin mediates the read (`english/subject.py::genon_unit_anchor`). That is P5.5's work,
not P1's.

THE FOUR NON-CARRY-FORWARD EDITS, all founder calls of 2026-08-12 taken at P-prep on
measured evidence, and all free because no library for this stage exists:

  1. FULL SPINE COVERAGE (Rule 2 STEP 3). The rule licensed a short plan to stop and leave
     later spines unanchored. The real corpus does it: `backup/saved_plans/english/ix/
     ch_12_*.json` (4 periods) carries NO beyond_text contribution at all. Under
     architecture v2.0 a chapter's canonicals must share ONE section registry — the compacts
     are the same chapter at fewer periods, not a smaller chapter — so a legal drop at
     authoring time breaks the choice-set arithmetic before serve ever runs. Curation stays
     where Rule 3 already puts it: at the TASK level.
  2. Rule 1's spine cap gains the closing-unit exception. "Exactly one main_section and one
     or two ADJACENT spines" cannot describe a whole-chapter closing unit, which the platform
     brief mandates of the standard canonical. This is the S8 lesson applied without paying
     for it twice ("Rule 1's cap was never a risk, it was a certainty"); the constitution
     still names no V-rule.
  3. `task_brief` ≤ 12 -> ≤ 18 words. Rule 9 mandates the brief carry a locator
     ("<Subheading> (p.NN): <brief>") which eats 3–4 words of the 12. Measured on the real
     IX corpus: 17 of 28 briefs exceed 12 words as authored; 27 of 28 fit 18.
  4. `section_context` 10–15 -> 10–18 words. Measured: 3 of 11 IX contributions run 16, 16
     and 17. The lower bound is kept — the field is useless at two words.

ALSO HERE, and it is the same class of edit S7 and S8 both had to make: the VOCABULARY
paragraph was TEACHING the positional cross-reference that register ban 2 forbids (its
examples were literally "the previous unit", "this unit"), and the `teacher_notes` schema
comment asked for "transition from prior / preview next" — the forward half of which is the
known direct contradiction testing.md P1 names for this constitution family.

P3 is REAL for this stage (Group B): `phases[{minutes, description}]` ->
`time_bands[{minutes, activity}]`, array and key both, with the prose following. No
`band_id` in the target shape.
"""
from __future__ import annotations

import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).resolve().parent
LP = ROOT / "data/content/constitutions/lesson_plan/english/secondary/lesson_plan_constitution.txt"
AS = ROOT / "data/content/constitutions/assessment/english/secondary/assessment_constitution.txt"


def sub(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    assert n == 1, f"{label}: expected exactly 1 occurrence, found {n}"
    return text.replace(old, new)


# ══════════════════════════════════════════════════════════════════════════════
# LESSON PLAN  v1.1 -> v1.2
# ══════════════════════════════════════════════════════════════════════════════

REGISTER = """

THE SELF-CONTAINED REGISTER (binds Rule 9 and teacher_notes)
Three things no time band or teacher note may do, each because the platform enforces it:
1. NAME A CLOCK QUANTITY — the platform scales every band's minutes in proportion to the sitting that carries it, so a stated number is falsified silently: no "for three minutes", "the remaining time", "half the session". Where a task is genuinely brief or genuinely long, say so in kind — "a quick paired exchange", "an unhurried reading aloud" — never in number.
2. POINT FORWARD OR CLAIM COMPLETION — a teacher's plan may end, or hand over to a companion variant's unit, after any unit, so "the next unit", "as we will see", "having now heard the whole play" are wrong for someone. Each unit closes on its own ground.
3. NAME CALENDAR TIME — Aruvi keeps no calendar and sittings do not map to days: today, yesterday, this week, next class are unknowable at authoring.
Backward continuity is welcome, and is best carried by naming the content built on ("Having read the terrace scene aloud, …") rather than a unit's position.
"""

A1 = """3. Period schedule — exactly ONE row { period_duration_minutes,
   period_count }: the class-standard duration (40 min for classes up to
   VII, 45 for VIII, 50 for IX–X — the master-plan calibration bands,
   not NCF's flat 40) × the period count, where period_count = B.
   Teacher timetable variation never reaches generation; it is handled
   downstream at serve time."""


def amend_lp(t: str) -> str:
    # ── header + footer ──────────────────────────────────────────────────────
    t = sub(t, "ARUVI — ENGLISH LESSON PLAN CONSTITUTION · VERSION 1.1 (SECONDARY)",
            "ARUVI — ENGLISH LESSON PLAN CONSTITUTION · VERSION 1.2 (SECONDARY)",
            "LP header")
    t = sub(t, "English Lesson Plan Constitution · Version 1.1 (Secondary) · Internal Document",
            "English Lesson Plan Constitution · Version 1.2 (Secondary) · Internal Document",
            "LP footer")

    # ── VOCABULARY: stop teaching the positional cross-reference ─────────────
    t = sub(t,
            'homework, and any cross-reference to another chunk (e.g. "the previous unit", '
            '"this unit").',
            "homework, and any cross-reference to another chunk. A cross-reference names the "
            "CONTENT built on, never a unit's position — see THE SELF-CONTAINED REGISTER below.",
            "LP vocabulary cross-reference examples")
    t = sub(t,
            'Never write "period" in prose the teacher reads.',
            'Never write "period" in prose the teacher reads; "session" is outside the '
            "register too.",
            "LP vocabulary session")

    # ── A5 + A7: the register, ONE block, immediately after VOCABULARY ───────
    t = sub(t, "\nStage: Secondary (Grade IX; extensible to X)",
            REGISTER + "\nStage: Secondary (Grade IX; extensible to X)",
            "LP register insertion")

    # ── A1: exactly one standard row ─────────────────────────────────────────
    t = sub(t,
            "3. Period schedule: { period_duration_minutes, period_count }, where\n"
            "   period_count = B is supplied at generation time (allocation tab\n"
            "   suggests; user may override).",
            A1, "LP A1 period schedule")

    # ── Rule 1: the closing-unit exception to the two-spine cap ──────────────
    t = sub(t,
            "Each period anchors to exactly ONE main_section and one or two spines\n"
            "ADJACENT in that on-page sequence. A period MUST NOT straddle two\n"
            "main_sections.",
            "Each period anchors to exactly ONE main_section and, ordinarily, one or\n"
            "two spines ADJACENT in that on-page sequence. A period MUST NOT straddle\n"
            "two main_sections.\n"
            "\n"
            "The one exception is a CLOSING unit that draws the whole main_section\n"
            "together — revisiting what several spines built rather than teaching a new\n"
            "cell. It may name as many spines as it genuinely revisits, and it teaches\n"
            "no cell of its own. Every OTHER unit stays inside the two-spine bound.",
            "LP rule 1 closing-unit exception")

    # ── Rule 2 STEP 1: the class-standard duration is 50 at this stage ───────
    t = sub(t,
            "A 40-min period holds ≤ 2–3 tasks; a 60-min period ≤ 3–5. Never exceed\n"
            "these regardless of how many tasks the summary contains.",
            "A 40-min period holds ≤ 2–3 tasks; a 50-min period (the secondary\n"
            "class-standard, INPUTS 3) ≤ 3–4; a 60-min period ≤ 3–5. Never exceed\n"
            "these regardless of how many tasks the summary contains.",
            "LP rule 2 step 1 fifty-minute budget")

    # ── Rule 2 STEP 3: FULL SPINE COVERAGE ───────────────────────────────────
    t = sub(t,
            "Pack tasks per Step 1's budget. When the section's periods are exhausted,\n"
            "stop — remaining spines/tasks are unanchored. Do not force a spine into\n"
            "a period merely because it exists. Note an unfitted spine/task in the\n"
            "last period's `teacher_notes` as a self-study pointer; this is honest\n"
            "reflection of available time, not a defect.",
            "Pack tasks per Step 1's budget.\n"
            "\n"
            "FULL SPINE COVERAGE: every spine the summary records for a section MUST be\n"
            "taught in at least one of that section's periods. Dropping a spine is\n"
            "FORBIDDEN, at every period count — a shorter plan is the same chapter taught\n"
            "in fewer periods, not a smaller chapter. A spine the summary does not carry\n"
            "for that section is simply absent and is not a drop.\n"
            "\n"
            "Curation happens at TASK level, where Rule 3 governs it: a spine under\n"
            "pressure is taught with fewer of its tasks anchored, never skipped. Unfitted\n"
            "TASKS go to homework (Rule 8) or are left unanchored and flagged in the\n"
            "period's `teacher_notes` as a self-study pointer; that is honest reflection\n"
            "of available time, not a defect. An unfitted SPINE is a defect.",
            "LP rule 2 step 3 full spine coverage")

    # ── P3 · phases -> time_bands, array + key, with the prose following ─────
    t = sub(t, "ACROSS acts (Act I → II → III) and the read-aloud phase (Rule 2A) is",
            "ACROSS acts (Act I → II → III) and the read-aloud band (Rule 2A) is",
            "P3 drama read-aloud phase")
    t = sub(t, "   teacher_notes and phase descriptions.",
            "   teacher_notes and time-band activity text.",
            "P3 inputs prose")
    t = sub(t,
            "explicit timed phase within that section's periods — never collapsed",
            "explicit timed band within that section's periods — never collapsed",
            "P3 rule 2A timed phase")
    t = sub(t, "stage directions and asides. The phase description must say so (e.g.",
            "stage directions and asides. The band's `activity` must say so (e.g.",
            "P3 rule 2A drama phase description")
    t = sub(t, "Still a timed reading phase, not a task slot.",
            "Still a timed reading band, not a task slot.",
            "P3 rule 2A timed reading phase")
    t = sub(t, "task_index). Phase descriptions reference tasks by spine_section_name +",
            "task_index). Time-band activity text references tasks by spine_section_name +",
            "P3 rule 3 phase descriptions")
    t = sub(t, "across two) lists the same key in each period; phase descriptions",
            "across two) lists the same key in each period; the bands' activity text",
            "P3 rule 3 long-task phase descriptions")
    t = sub(t,
            "Each period's phases sum EXACTLY to `period_duration_minutes`; minimum\n"
            "3 phases. `phases[].minutes` is a STRING range (e.g. \"0–10\", \"10–25\")",
            "Each period's time bands sum EXACTLY to `period_duration_minutes`; minimum\n"
            "3 bands. `time_bands[].minutes` is a STRING range (e.g. \"0–10\", \"10–25\")",
            "P3 rule 5 time constraint")
    t = sub(t, "anywhere in the LP JSON — header, periods, phases, teacher_notes, or",
            "anywhere in the LP JSON — header, periods, time bands, teacher_notes, or",
            "P3 rule 7 c-codes")
    t = sub(t, 'range when the task has none). This mirrors the "(page NN)" locator a phase',
            'range when the task has none). This mirrors the "(page NN)" locator a band',
            "P3 rule 8 homework locator")
    t = sub(t, "RULE 9 | PHASE NARRATION", "RULE 9 | BAND NARRATION", "P3 rule 9 heading")
    t = sub(t, "A phase invoking a task names it by anchor location + a ≤10-word brief.",
            "A time band invoking a task names it by anchor location + a ≤10-word brief.",
            "P3 rule 9 opening")
    t = sub(t, "  - phase `description`", "  - a time band's `activity`",
            "P3 rule 9 teacher-facing list")
    t = sub(t, "scans every `teacher_notes`, phase `description`, and `task_brief` for all the",
            "scans every `teacher_notes`, time band `activity`, and `task_brief` for all the",
            "P3 rule 9 lint prose")
    t = sub(t,
            '  "phases": [\n'
            '    { "minutes":     string,          // "0–10" — tiles 0..duration\n'
            '      "description": string }         // refers to tasks by\n'
            "                                      // spine_section_name + brief\n"
            "  ],",
            '  "time_bands": [\n'
            '    { "minutes":  string,             // "0–10" — tiles 0..duration\n'
            '      "activity": string }            // refers to tasks by\n'
            "                                      // spine_section_name + brief\n"
            "  ],",
            "P3 schema block")

    # ── the numeric limits, measured against the real IX corpus ──────────────
    t = sub(t, '      "task_brief": string }          // ≤ 12 words, teacher-facing',
            '      "task_brief": string }          // ≤ 18 words INCLUDING the Rule 9\n'
            "                                      // locator; teacher-facing",
            "task_brief cap · period schema")
    t = sub(t, '      "task_brief": string }  // ≤ 12 words, copied from tasks_in_class;',
            '      "task_brief": string }  // ≤ 18 words, copied from tasks_in_class;',
            "task_brief cap · contribution schema")
    t = sub(t,
            '    Format: "<Subheading> (p.NN): <plain brief>".',
            '    Format: "<Subheading> (p.NN): <plain brief>", ≤ 18 words in all — the\n'
            "    locator is part of the brief and part of the count.",
            "task_brief cap · rule 9 format")
    t = sub(t, "  - `section_context` — 10–15 words naming the specific content/text/topic",
            "  - `section_context` — 10–18 words naming the specific content/text/topic",
            "section_context range · rule 10")
    t = sub(t, "                        be an INVENTED 10–15 word context that reflects",
            "                        be an INVENTED 10–18 word context that reflects",
            "section_context range · rule 10 writing spine")
    t = sub(t, '  "section_context": string,  // 10–15 words: the specific content/text/topic',
            '  "section_context": string,  // 10–18 words: the specific content/text/topic',
            "section_context range · contribution schema")

    # ── teacher_notes: the forward half of "transition / preview" is ban 2 ───
    t = sub(t,
            '  "teacher_notes": string,            // 2–3 sentences max, in priority order:\n'
            "                                      // 1. transition from prior / preview next;",
            '  "teacher_notes": string,            // 2–3 sentences max, in priority order:\n'
            "                                      // 1. backward continuity, naming the\n"
            "                                      //    CONTENT built on — never a unit's\n"
            "                                      //    position, and never a preview of\n"
            "                                      //    what comes next (register ban 2);",
            "LP teacher_notes forward reference")

    # ── Rule 10: a spine with no anchored tasks is now a defect, not a state ─
    t = sub(t,
            "A spine with no anchored tasks across any section is emitted with empty\n"
            "`section_contributions: []`; assessment omits that spine entirely.",
            "A spine the summary does not carry for any section is emitted with empty\n"
            "`section_contributions: []`, and assessment omits it entirely. A spine the\n"
            "summary DOES carry may not arrive here empty — that is a breach of Rule 2's\n"
            "FULL SPINE COVERAGE, not a permitted state.",
            "LP rule 10 empty spine")
    return t


# ══════════════════════════════════════════════════════════════════════════════
# ASSESSMENT  v1.3 -> v1.4
# ══════════════════════════════════════════════════════════════════════════════

ANCHORING = """
================================================================================
RULE 8A | ITEM ANCHORING — THE CELL IS THE ANCHOR, AND IT IS NOT YOURS TO NUMBER
================================================================================

An item's anchor is the (section × spine) CELL it was generated from, carried
by the two Rule 8 fields it already has: `source_section_id` and
`source_spine`, both copied verbatim from the handoff contribution consumed.
Together they ARE the anchor — there is no third field to emit.

The platform resolves that cell to the unit(s) that taught it by matching the
pair against each period's own `section_id` + `spines_taught[]`. Where a cell
is taught across several units, the item anchors at the LAST of them: an item
tests the cell's whole `implied_lo`, so it becomes available only when the
cell completes.

MUST NOT emit `period_ref`, `period_number`, `unit_ref`, or any other unit
number or position. The number of units a chapter is taught in varies per
teacher and is decided long after this file is written; declaring the link
would freeze an arrangement the platform varies, and the platform would then
have to choose between your number and the truth.
"""

A9 = """
MCQ OPTION ORDER IS NOT YOURS TO SET. Emit the four options in whatever order
they were authored; order carries no meaning. Uneven letters across a chapter
are coincidence, not a defect, and correcting them is not your job — the
platform arranges options deterministically after generation.

An option MUST NOT refer to another option by its label: no "both A and B",
"none of the above", "all of the above", "either B or C". Those are the one
construction a downstream arrangement cannot reorder without rewriting the
item.
"""


def amend_assessment(t: str) -> str:
    t = sub(t, "ARUVI — ENGLISH ASSESSMENT CONSTITUTION · VERSION 1.3 (SECONDARY)",
            "ARUVI — ENGLISH ASSESSMENT CONSTITUTION · VERSION 1.4 (SECONDARY)",
            "assessment header")
    t = sub(t, "English Assessment Constitution · Version 1.3 (Secondary) · Internal Document",
            "English Assessment Constitution · Version 1.4 (Secondary) · Internal Document",
            "assessment footer")

    # ── A6: the anchoring block, after Rule 8 (SOURCE TAGGING) ──────────────
    t = sub(t,
            "\n================================================================================\n"
            "RULE 9 | VISUAL STIMULUS AND STRUCTURAL FIDELITY",
            ANCHORING +
            "\n================================================================================\n"
            "RULE 9 | VISUAL STIMULUS AND STRUCTURAL FIDELITY",
            "assessment A6 anchoring block")

    # ── A9: the two lines, in Rule 4 where MCQ semantics live ───────────────
    t = sub(t,
            "     Carries `options[]`; `suggested_answer` is OMITTED (correct option\n"
            "     already flagged via `is_correct`).",
            "     Carries `options[]`; `suggested_answer` is OMITTED (correct option\n"
            "     already flagged via `is_correct`).\n" + A9.rstrip("\n"),
            "assessment A9 lines")

    # ── the item count follows the LP's coverage mandate ────────────────────
    t = sub(t,
            "No fallback path: a cell with no section_contribution produces no item.\n"
            "Item count per chapter = total section_contributions across all spines.",
            "No fallback path: a cell with no section_contribution produces no item.\n"
            "Item count per chapter = total section_contributions across all spines.\n"
            "That count does NOT vary with the number of periods the chapter was taught\n"
            "in: the LP covers every spine the summary carries at every period count, so\n"
            "a shorter plan yields the same cells and the same items, tested on less\n"
            "anchored practice — never a shorter assessment.",
            "assessment item count invariance")
    return t


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for path, name, fn in ((LP, "lesson_plan_constitution_v1.1_pre.txt", amend_lp),
                           (AS, "assessment_constitution_v1.3_pre.txt", amend_assessment)):
        pre = path.read_text(encoding="utf-8")
        shutil.copyfile(path, OUT / name)
        path.write_text(fn(pre), encoding="utf-8")

    lp = LP.read_text(encoding="utf-8")
    ass = AS.read_text(encoding="utf-8")

    # ── guards · what must NOT be there ─────────────────────────────────────
    for bad in ("phases[", '"phases"', "band_id", "section_anchor", "role_handoff",
                "unit_handoff", "band_ref", "role weighting", "section registry",
                "synthesis unit", "reserved token"):
        assert lp.count(bad) == 0, f"LP guard failed: {bad!r} present"
    for bad in ("alphabetically", "never led with", "first word at which they differ",
                "vary in position", "same label", "phase_ref", "role_handoff",
                "unit_handoff", "band_ref", "section registry", "synthesis unit",
                "reserved token"):
        assert ass.count(bad) == 0, f"assessment guard failed: {bad!r} present"

    # ── guards · what MUST be there ─────────────────────────────────────────
    # twice by design: the block itself, and VOCABULARY's pointer at it
    assert lp.count("THE SELF-CONTAINED REGISTER") == 2
    assert lp.count("THE SELF-CONTAINED REGISTER (binds Rule 9 and teacher_notes)") == 1
    assert lp.count("NAME A CLOCK QUANTITY") == 1
    assert lp.count("POINT FORWARD OR CLAIM COMPLETION") == 1
    assert lp.count("NAME CALENDAR TIME") == 1
    assert lp.count("exactly ONE row") == 1
    assert lp.count("time_bands") == 2, lp.count("time_bands")
    assert lp.count('"activity": string') == 1
    assert lp.count("FULL SPINE COVERAGE") == 2
    assert lp.count("VERSION 1.2 (SECONDARY)") == 1
    assert ass.count("RULE 8A | ITEM ANCHORING") == 1
    assert ass.count("MCQ OPTION ORDER IS NOT YOURS TO SET") == 1
    assert ass.count("both A and B") == 1
    assert ass.count("VERSION 1.4 (SECONDARY)") == 1
    print("S11 amendments applied · LP v1.1 -> v1.2 · assessment v1.3 -> v1.4")


if __name__ == "__main__":
    main()
