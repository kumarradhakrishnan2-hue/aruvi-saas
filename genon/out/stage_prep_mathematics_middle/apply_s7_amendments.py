#!/usr/bin/env python3
"""S7 · mathematics · middle — the P1/P2/P3 amendment pass (testing.md §3).

Reproducible edit script, in the S3/S4/S6 pattern: every edit asserts EXACTLY ONE
occurrence of its target before replacing, and the run closes on guard assertions for
the strings that must NOT come back (the struck arrangement sentence, the retired
`phases` shape) and for the strings that must now be present.

Landed pair:  LP  v3.3 -> v3.4   ·   assessment  v3.2 -> v3.3
Reference:    SS·secondary LP v1.10 · assessment v1.7, via the mathematics·secondary
              v1.3 / v1.2 adaptation (same subject vocabulary, one stage up).

WHAT THIS PASS DOES *NOT* DO, and why it matters (founder ruling, 2026-08-10).
No new field is invented to feed the serve engine. `section_anchor` is NOT added to the
period, and no `period_number` is added to the coverage handoff. Both facts are already
in the authored file — the period's `textbook_segments[].ref` and the handoff entry's
`section_ref` — and the prototype resolved exactly this shape variance at the READ
boundary (`app/aruvi_streamlit/lp_pdf_generator.py:2583-2592` prefers textbook_segments
then falls back to section_anchor; `assessment_pdf_generator.py:117-192` re-buckets
middle-maths items by `section_ref` at render time, stating in terms that "the
constitution / generated JSON is NOT changed"). The SaaS keeps that answer but moves it
to the sanctioned seam — `aruvi_core/genon/carriers.py` and the mathematics plugin
(CLAUDE.md §3) — which is P5.5's work, not P1's.

The ONE shape item that could not be absorbed by a tolerant read is P3: `compile.py`
rebuilds the timed spine from `p["time_bands"]` (:124) and asserts an inventory
invariant over `tb["activity"]` (:208-210). Founder called it for the amendment,
following testing.md P3 and S6's 2026-08-07 conversion.
"""
from __future__ import annotations

import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).resolve().parent
LP = ROOT / "data/content/constitutions/lesson_plan/mathematics/middle/lesson_plan_constitution.txt"
AS = ROOT / "data/content/constitutions/assessment/mathematics/middle/assessment_constitution.txt"

EDITS: list[tuple[str, str, str]] = []          # (label, old, new) — filled below


def sub(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    assert n == 1, f"{label}: expected exactly 1 occurrence, found {n}"
    return text.replace(old, new)


# ══════════════════════════════════════════════════════════════════════════════
# LESSON PLAN  v3.3 -> v3.4
# ══════════════════════════════════════════════════════════════════════════════
REGISTER = """
THE SELF-CONTAINED REGISTER (binds Rule 10 and teacher_notes)
Three things no time band or teacher note may do, each because the platform enforces it:
1. NAME A CLOCK QUANTITY — the platform scales every band's minutes in proportion to the sitting that carries it, so a stated number is falsified silently: no "for three minutes", "the remaining time", "half the session". Where a task is genuinely brief or genuinely long, say so in kind — "a quick mental calculation", "an extended construction" — never in number.
2. POINT FORWARD OR CLAIM COMPLETION — a teacher's plan may end, or hand over to a companion variant's unit, after any unit, so "the next unit", "as we will see", "having covered all three angle pairs" are wrong for someone. Each unit closes on its own ground.
3. NAME CALENDAR TIME — Aruvi keeps no calendar and sittings do not map to days: today, yesterday, this week, next class are unknowable at authoring.
Backward continuity is welcome, and is best carried by naming the content built on ("Having established that vertically opposite angles are equal, …" — Rule 10's continuity link) rather than a unit's position.
"""


def amend_lp(t: str) -> str:
    # ── VERSION ───────────────────────────────────────────────────────────────
    t = sub(t,
            "ARUVI — MATHEMATICS LESSON PLAN CONSTITUTION · VERSION 3.3",
            "ARUVI — MATHEMATICS LESSON PLAN CONSTITUTION · VERSION 3.4",
            "LP version line")
    t = sub(t,
            "Mathematics Lesson Plan Constitution · Version 3.1 · Internal Document",
            "Mathematics Lesson Plan Constitution · Version 3.4 · Internal Document",
            "LP footer version (was stale at 3.1)")

    # ── VOCABULARY · drop the positional examples, add the session exclusion ──
    # Consequential to register ban 2: the vocabulary was *teaching* the forward
    # reference it now forbids ("the previous unit", "this unit" as cross-references).
    # Same edit science·secondary and mathematics·secondary made.
    t = sub(t,
            'homework, and any cross-reference to another chunk (e.g. "the previous unit", '
            '"this unit"). The token "period"',
            'homework, and any cross-reference to another chunk. The token "period"',
            "LP VOCABULARY positional examples")
    t = sub(t,
            'Never write "period" in prose the teacher reads.',
            'Never write "period" in prose the teacher reads; "session" is outside the register too.',
            "LP VOCABULARY session exclusion")

    # ── A5 + A7 · THE SELF-CONTAINED REGISTER, as ONE block after VOCABULARY ──
    t = sub(t,
            "Stages: Foundational, Preparatory, Middle, Secondary\n\n"
            "================================================================================\n"
            "DESIGN PRINCIPLE",
            "Stages: Foundational, Preparatory, Middle, Secondary\n"
            + REGISTER +
            "\n================================================================================\n"
            "DESIGN PRINCIPLE",
            "LP register block")

    # ── A1 · the period schedule is exactly ONE standard row ─────────────────
    t = sub(t,
            "4. Period schedule: {duration, count} rows; total = B.",
            "4. Period schedule — exactly ONE row {duration_minutes, count}: the\n"
            "   class-standard duration (40 min for classes up to VII, 45 for VIII,\n"
            "   50 for IX–X — the master-plan calibration bands, not NCF's flat 40)\n"
            "   × the period count; total = B. Teacher timetable variation never\n"
            "   reaches generation; it is handled downstream at serve time.",
            "LP A1 INPUTS 4")

    # ── P3 · phases[{minutes, description}] -> time_bands[{minutes, activity}] ─
    t = sub(t,
            "Each period's phases sum exactly to `period_duration_minutes`. Minimum\n"
            "3 phases per period.\n\n"
            "`phases[].minutes` is a STRING time-range (e.g., `\"0–10\"`, `\"10–25\"`).\n"
            "Ranges tile the period from `0` to `period_duration_minutes` with no\n"
            "gaps and no overlaps.",
            "Each period's time bands sum exactly to `period_duration_minutes`.\n"
            "Minimum 3 time bands per period.\n\n"
            "`time_bands[].minutes` is a STRING time-range (e.g., `\"0–10\"`,\n"
            "`\"10–25\"`). Ranges tile the period from `0` to\n"
            "`period_duration_minutes` with no gaps and no overlaps.",
            "P3 Rule 6 prose")
    t = sub(t,
            "table and in mapping/audit JSON, never in periods, phases, or\nteacher_notes.",
            "table and in mapping/audit JSON, never in periods, time bands, or\nteacher_notes.",
            "P3 Rule 8 prose")
    t = sub(t,
            "RULE 10 | PHASE NARRATION USES book_ref, NOT INTERNAL ID",
            "RULE 10 | TIME-BAND NARRATION USES book_ref, NOT INTERNAL ID",
            "P3 Rule 10 heading")
    t = sub(t,
            "When a phase invokes a textbook item, the phase's `description` text",
            "When a time band invokes a textbook item, the band's `activity` text",
            "P3 Rule 10 opening")
    t = sub(t,
            "The phase description MUST NOT use the internal `id` (e.g., `A-1`,",
            "The band's `activity` text MUST NOT use the internal `id` (e.g., `A-1`,",
            "P3 Rule 10 prohibition")
    t = sub(t,
            "both empty (a guard case — Rule 6 phases normally require",
            "both empty (a guard case — Rule 6 time bands normally require",
            "P3 Rule 11 guard case")
    t = sub(t,
            "                                                  // used by phases to",
            "                                                  // used by bands to",
            "P3 schema textbook_items description comment")
    t = sub(t,
            '  "phases": [\n'
            "    {\n"
            '      "minutes":     string,                      // time range, e.g.\n'
            '                                                  // "0–10". Tiles\n'
            "                                                  // 0..period_duration\n"
            "                                                  // with no gaps.\n"
            '      "description": string                       // narrative; refers\n'
            "                                                  // to items by\n"
            "                                                  // book_ref only\n"
            "    }\n"
            "  ],",
            '  "time_bands": [\n'
            "    {\n"
            '      "minutes":  string,                         // time range, e.g.\n'
            '                                                  // "0–10". Tiles\n'
            "                                                  // 0..period_duration\n"
            "                                                  // with no gaps.\n"
            '      "activity": string                          // narrative; refers\n'
            "                                                  // to items by\n"
            "                                                  // book_ref only.\n"
            "                                                  // Bound by THE\n"
            "                                                  // SELF-CONTAINED\n"
            "                                                  // REGISTER.\n"
            "    }\n"
            "  ],",
            "P3 schema array")

    # ── A1 where the schema is actually read ─────────────────────────────────
    t = sub(t,
            '  "period_number":           integer,\n'
            '  "period_duration_minutes": integer,',
            '  "period_number":           integer,\n'
            '  "period_duration_minutes": integer,          // the ONE class-standard\n'
            "                                               // duration of INPUTS 4;\n"
            "                                               // identical on every\n"
            "                                               // period of the plan",
            "LP A1 schema field constraint")

    # ── Rule 10 · bind the register ──────────────────────────────────────────
    t = sub(t,
            "Do not use prose to describe the textbook item.",
            "Do not use prose to describe the textbook item.\n\n"
            "Every band is additionally bound by THE SELF-CONTAINED REGISTER: it\n"
            "names no clock quantity, points forward at nothing, claims no\n"
            "completion, and names no calendar time. Each band speaks in the present\n"
            "of its own activity; unit-to-unit linking lives only in teacher_notes.",
            "LP Rule 10 register bind")

    # ── teacher_notes · position-free continuity + register bind ─────────────
    t = sub(t,
            "                                                  //  - Briefly recap what\n"
            "                                                  //    the previous unit\n"
            "                                                  //    covered and connect\n"
            "                                                  //    it to this one.",
            "                                                  //  - Carry continuity by\n"
            "                                                  //    NAMING THE CONTENT\n"
            "                                                  //    built on, never a\n"
            "                                                  //    unit's position\n"
            "                                                  //    (THE SELF-CONTAINED\n"
            "                                                  //    REGISTER, ban 2).",
            "LP teacher_notes continuity bullet")
    return t


# ══════════════════════════════════════════════════════════════════════════════
# ASSESSMENT  v3.2 -> v3.3
# ══════════════════════════════════════════════════════════════════════════════
ANCHORING = """
================================================================================
ANCHORING (PLATFORM INTEGRITY — NOT A GENERATION CHOICE)
================================================================================

· `section_ref` IS the item's anchor. It is copied verbatim from the LP
  handoff entry the item was generated from, in the LP's own vocabulary
  ("section 4.1"), and the platform resolves it to the unit(s) that teach
  that section by matching it against each period's own
  `textbook_segments[].ref`. Nothing about that link is declared by the
  generator; it is derived.

· Where a section is taught across several units, the item anchors at the
  LAST of them. An item tests the section's whole goal, so it becomes
  available only once the section completes: a class that was not taught
  all of it cannot be tasked on any of it.

· MUST NOT emit `period_ref`, `period_number`, or any unit number on an
  item. Declaring the link would freeze an arrangement the platform varies
  per teacher.

· `section_title` is likewise copied verbatim from the handoff entry and
  matches the summary's `sections[i].title`. Both fields are pass-through:
  the generator neither reformats nor abbreviates them.

· `anchor_id` is NOT an anchor in this sense (Rule 8). It seeds the
  exercise companion only, stays internal, and never reaches the platform's
  item-to-unit resolution.

"""


def amend_assess(t: str) -> str:
    t = sub(t,
            "ARUVI — MATHEMATICS ASSESSMENT CONSTITUTION · VERSION 3.2",
            "ARUVI — MATHEMATICS ASSESSMENT CONSTITUTION · VERSION 3.3",
            "assessment version line")
    t = sub(t,
            "Mathematics Assessment Constitution · Version 3.2 · Internal Document",
            "Mathematics Assessment Constitution · Version 3.3 · Internal Document",
            "assessment footer version")

    # ── A9 · option order is not the model's to set ──────────────────────────
    # REMOVAL is N/A for this file: it never carried the MEMORY item-18 position
    # prohibition (asserted in the guards below), so A9 lands as the two lines alone —
    # the same shape it took at S4.
    t = sub(t,
            "  MCQ:\n"
            "    options: [ {label, text, is_correct}, … ]   // exactly 4 options;\n"
            "                                                // exactly one\n"
            "                                                // is_correct: true\n"
            "    teacher_guide.what_each_option_reveals:\n"
            "        {A:..., B:..., C:..., D:...}",
            "  MCQ:\n"
            "    options: [ {label, text, is_correct}, … ]   // exactly 4 options;\n"
            "                                                // exactly one\n"
            "                                                // is_correct: true\n"
            "    teacher_guide.what_each_option_reveals:\n"
            "        {A:..., B:..., C:..., D:...}\n\n"
            "    Option order carries no meaning and is not yours to set: emit the\n"
            "    four options in whatever order they were authored, and never let\n"
            "    where an option sits influence how it is written. Uneven letters\n"
            "    across a chapter are coincidence, not a defect.\n\n"
            "    PROHIBITED: an option that refers to another option by its label\n"
            '    ("both A and B", "none of the above", "all of the above") — options\n'
            "    are ordered downstream and a label reference would be falsified.",
            "A9 option-order lines")

    # ── A6-confirm · the anchoring block ─────────────────────────────────────
    t = sub(t,
            "\n================================================================================\n"
            "ASSESSMENT JSON SCHEMA\n",
            ANCHORING +
            "\n================================================================================\n"
            "ASSESSMENT JSON SCHEMA\n",
            "A6 anchoring block")
    return t


# ══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    lp0 = LP.read_text(encoding="utf-8")
    as0 = AS.read_text(encoding="utf-8")
    shutil.copy2(LP, OUT / "lesson_plan_constitution_v3.3_pre.txt")
    shutil.copy2(AS, OUT / "assessment_constitution_v3.2_pre.txt")

    lp1 = amend_lp(lp0)
    as1 = amend_assess(as0)

    # ── guards · what must NOT be there ──────────────────────────────────────
    # P3: the retired shape, in every form it could survive in.
    assert "phases[" not in lp1, "GUARD: `phases[` survived P3"
    assert '"phases"' not in lp1, 'GUARD: `"phases"` survived P3'
    assert "band_id" not in lp1, "GUARD: band_id must not enter the target shape"
    # A9: the arrangement sentence struck at the reference's v1.7 must never come back.
    for bad in ("alphabetically", "never led with", "first word at which they differ",
                "vary in position", "same label"):
        assert bad not in as1.lower(), f"GUARD: struck A9 arrangement string {bad!r} present"
    # A6: the reversed band-level phase_ref must not be reintroduced.
    assert "phase_ref" not in as1 and "phase_ref" not in lp1, "GUARD: phase_ref reintroduced"
    # The founder ruling of 2026-08-10: no new field invented for the serve engine.
    assert "section_anchor" not in lp1, "GUARD: section_anchor invented in the LP"
    assert lp1.count("period_number") == lp0.count("period_number"), \
        "GUARD: a period_number field was added somewhere"

    # ── guards · what MUST be there ──────────────────────────────────────────
    # The heading + Rule 10's bind read as one phrase; teacher_notes' bind is wrapped
    # across two comment lines by the schema's column width, so it is checked apart.
    assert lp1.count("THE SELF-CONTAINED REGISTER") == 2, \
        "GUARD: register heading + Rule 10 bind expected"
    assert "//    (THE SELF-CONTAINED\n" in lp1 and "//    REGISTER, ban 2)." in lp1, \
        "GUARD: teacher_notes register bind"
    assert lp1.count("time_bands") == 2, "GUARD: time_bands expected in Rule 6 and the schema"
    assert '"activity": string' in lp1, "GUARD: the band's activity key"
    assert "exactly ONE row {duration_minutes, count}" in lp1, "GUARD: A1"
    assert "ANCHORING (PLATFORM INTEGRITY" in as1, "GUARD: A6 block"
    assert "Option order carries no meaning" in as1, "GUARD: A9 mandate line"
    assert "by its label" in as1, "GUARD: A9 by-label prohibition"

    LP.write_text(lp1, encoding="utf-8")
    AS.write_text(as1, encoding="utf-8")
    print("LP  v3.3 -> v3.4  ", LP)
    print("AS  v3.2 -> v3.3  ", AS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
