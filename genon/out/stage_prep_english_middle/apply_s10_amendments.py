#!/usr/bin/env python3
"""S10 · english · middle — P1 + P3 + the measured edits, applied to the LP constitution.

Reproducible, guarded, and idempotent-by-refusal: every replacement asserts an
EXACT occurrence count against the pre-file before it is made, so a re-run on an
already-amended file fails loudly rather than half-applying.

Pre-file, diff and this script are the P1/P3 artefacts (testing.md §3).

  english/middle lesson_plan_constitution.txt   v1.6 -> v1.7

WHAT LANDS, and under which step:

  P1 · A1     INPUTS 3 becomes exactly ONE row at the class-standard duration
              (40 min <=VII, 45 VIII, 50 IX-X — the master-plan calibration
              bands). Ported from english/secondary v1.2 verbatim in substance.

  P1 · A5/A7  THE SELF-CONTAINED REGISTER, one block after VOCABULARY, in the
              v1.10 three-ban re-cut. VOCABULARY's own positional examples
              ("the previous unit", "this unit") are struck — testing.md P1
              names this file's forward-preview clause as the known direct
              contradiction, and the VOCABULARY line was teaching the very
              cross-reference ban 2 forbids.

  P3          phases[{minutes, description}] -> time_bands[{minutes, activity}],
              array and key, with Rule 5, Rule 9's heading, Rule 2A's "explicit
              timed phase" and every prose reference following. No band_id.

  MEASURED (not carry-forward; taken here because P-prep is where they are free)

  M1  Rule 2 STEP 3 — FULL SPINE COVERAGE replaces the drop licence.
  M2  Rule 1 — the closing-unit exception.
  M3  Rule 10 — the item-count line said ONE item per cell; assessment v3.6
      (2026-08-12) emits TWO. A live contradiction between the pair.
  M4  Rule 10 — `section_context` 10-15 -> 10-18 words.
  M5  Schema — `task_brief` <= 12 -> <= 18 words, and Rule 9 names WHICH
      subheading a merged cell uses.
  M6  Rule 2 STEP 1 — the 45-minute class-standard budget line (VIII).
"""
from __future__ import annotations

import difflib
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
LP = ROOT / "data/content/constitutions/lesson_plan/english/middle/lesson_plan_constitution.txt"
OUT = pathlib.Path(__file__).resolve().parent

original = LP.read_text(encoding="utf-8")
text = original

edits: list[tuple[str, str, str, int]] = []   # label, old, new, expected count


def edit(label: str, old: str, new: str, count: int = 1) -> None:
    edits.append((label, old, new, count))


# ---------------------------------------------------------------- P1 · header
edit(
    "VERSION header 1.6 -> 1.7",
    "ARUVI — ENGLISH LESSON PLAN CONSTITUTION · VERSION 1.6",
    "ARUVI — ENGLISH LESSON PLAN CONSTITUTION · VERSION 1.7",
)
edit(
    "footer 1.6 -> 1.7",
    "English Lesson Plan Constitution · Version 1.6 · Internal Document",
    "English Lesson Plan Constitution · Version 1.7 · Internal Document",
)

# ------------------------------------------------- P1 · A5/A7 · the register
OLD_VOCAB = (
    'The atomic teaching chunk is called a "unit" in ALL teacher-facing prose — '
    "teacher_notes, activity titles, homework, and any cross-reference to another "
    'chunk (e.g. "the previous unit", "this unit"). The token "period" is retained '
    "ONLY in (a) schema field names (period_number, period_duration_minutes, "
    "periods[], etc.) and (b) the scheduling/allocation budget (period schedule, "
    'period count, per-period budget). Never write "period" in prose the teacher '
    "reads.\nStage: Middle (Grades VI–VIII)\n"
)
NEW_VOCAB = (
    'The atomic teaching chunk is called a "unit" in ALL teacher-facing prose — '
    "teacher_notes, activity titles, homework, and any cross-reference to another "
    "chunk. A cross-reference names the CONTENT built on, never a unit's position "
    '— see THE SELF-CONTAINED REGISTER below. The token "period" is retained '
    "ONLY in (a) schema field names (period_number, period_duration_minutes, "
    "periods[], etc.) and (b) the scheduling/allocation budget (period schedule, "
    'period count, per-period budget). Never write "period" in prose the teacher '
    'reads; "session" is outside the register too.\n'
    "\n"
    "THE SELF-CONTAINED REGISTER (binds Rule 9 and teacher_notes)\n"
    "Three things no time band or teacher note may do, each because the platform "
    "enforces it:\n"
    "1. NAME A CLOCK QUANTITY — the platform scales every band's minutes in "
    "proportion to the sitting that carries it, so a stated number is falsified "
    'silently: no "for three minutes", "the remaining time", "half the session". '
    "Where a task is genuinely brief or genuinely long, say so in kind — "
    '"a quick paired exchange", "an unhurried reading aloud" — never in number.\n'
    "2. POINT FORWARD OR CLAIM COMPLETION — a teacher's plan may end, or hand over "
    'to a companion variant\'s unit, after any unit, so "the next unit", "as we '
    'will see", "having now read the whole poem" are wrong for someone. Each unit '
    "closes on its own ground.\n"
    "3. NAME CALENDAR TIME — Aruvi keeps no calendar and sittings do not map to "
    "days: today, yesterday, this week, next class are unknowable at authoring.\n"
    "Backward continuity is welcome, and is best carried by naming the content "
    'built on ("Having read the bird\'s complaint aloud, …") rather than a unit\'s '
    "position.\n"
    "\n"
    "Stage: Middle (Grades VI–VIII)\n"
)
edit("A5/A7 register block + VOCABULARY re-cut", OLD_VOCAB, NEW_VOCAB)

# ------------------------------------------------------------------- P1 · A1
OLD_INPUTS3 = (
    "3. Period schedule: { period_duration_minutes, period_count } where\n"
    "   period_count = B is supplied at generation time (allocation tab\n"
    "   suggests, user may override).\n"
)
NEW_INPUTS3 = (
    "3. Period schedule — exactly ONE row { period_duration_minutes,\n"
    "   period_count }: the class-standard duration (40 min for classes up to\n"
    "   VII, 45 for VIII, 50 for IX–X — the master-plan calibration bands,\n"
    "   not NCF's flat 40) × the period count, where period_count = B.\n"
    "   Teacher timetable variation never reaches generation; it is handled\n"
    "   downstream at serve time.\n"
)
edit("A1 · INPUTS 3", OLD_INPUTS3, NEW_INPUTS3)

# ------------------------------------------------------- M2 · Rule 1 closing
OLD_R1 = (
    "Each period anchors to:\n"
    "  - exactly ONE main_section, AND\n"
    "  - one or two adjacent spines within that section.\n"
    "\n"
    "A period MUST NOT straddle two main_sections (a period cannot mix\n"
    "the prose section with the poem section).\n"
)
NEW_R1 = (
    "Each period anchors to:\n"
    "  - exactly ONE main_section, AND\n"
    "  - one or two adjacent spines within that section.\n"
    "\n"
    "A period MUST NOT straddle two main_sections (a period cannot mix\n"
    "the prose section with the poem section).\n"
    "\n"
    "The one exception is a CLOSING unit that draws the whole main_section\n"
    "together — revisiting what several spines built rather than teaching a\n"
    "new cell. It may name as many spines as it genuinely revisits, and it\n"
    "teaches no cell of its own. Every OTHER unit stays inside the two-spine\n"
    "bound.\n"
)
edit("M2 · Rule 1 closing-unit exception", OLD_R1, NEW_R1)

# ------------------------------------------------- M6 · Rule 2 STEP 1 budget
OLD_BUDGET = (
    "A 40-minute period holds at most 2–3 tasks across its spine(s).\n"
    "A 60-minute period holds at most 3–5 tasks. Do not exceed these\n"
    "ceilings regardless of how many tasks the summary contains.\n"
)
NEW_BUDGET = (
    "A 40-minute period (the class-standard for VI–VII, INPUTS 3) holds at\n"
    "most 2–3 tasks across its spine(s); a 45-minute period (the VIII\n"
    "class-standard) at most 3; a 60-minute period at most 3–5. Do not\n"
    "exceed these ceilings regardless of how many tasks the summary contains.\n"
)
edit("M6 · Rule 2 STEP 1 · the 45-min class standard", OLD_BUDGET, NEW_BUDGET)

# ------------------------------------------- M1 · Rule 2 STEP 3 full coverage
OLD_STEP3 = (
    "STEP 3 — Within each section, cover spines in textbook order,\n"
    "stopping when the section's periods are full.\n"
    "Work through the section's spines in textbook order\n"
    "(RFC → Listening → Speaking → Writing → VocGram → Beyond-text).\n"
    "Pack tasks into periods using the budget from Step 1. When the\n"
    "section's allocated periods are exhausted, stop — remaining spines\n"
    "and tasks in that section are not anchored. Do not force a spine\n"
    "into a period simply because it exists in the summary. A spine or\n"
    "task that does not fit is noted in `teacher_notes` of the last period\n"
    "of that section as a self-study pointer for the teacher. This is not\n"
    "a defect — it is an honest reflection of available time.\n"
)
NEW_STEP3 = (
    "STEP 3 — Within each section, cover spines in textbook order.\n"
    "Work through the section's spines in textbook order\n"
    "(RFC → Listening → Speaking → Writing → VocGram → Beyond-text).\n"
    "Pack tasks into periods using the budget from Step 1.\n"
    "\n"
    "FULL SPINE COVERAGE: every spine the summary records for a section MUST\n"
    "be taught in at least one of that section's periods. Dropping a spine is\n"
    "FORBIDDEN, at every period count — a shorter plan is the same chapter\n"
    "taught in fewer periods, not a smaller chapter. A class given six periods\n"
    "instead of twelve should still listen, speak and write; it should do less\n"
    "of each. A spine the summary does not carry for that section is simply\n"
    "absent and is not a drop.\n"
    "\n"
    "Curation happens at TASK level, where Rule 3 governs it: a spine under\n"
    "pressure is taught with fewer of its tasks anchored, never skipped.\n"
    "Unfitted TASKS go to homework (Rule 8) or are left unanchored and flagged\n"
    "in the period's `teacher_notes` as a self-study pointer; that is an honest\n"
    "reflection of available time, not a defect. An unfitted SPINE is a defect.\n"
)
edit("M1 · Rule 2 STEP 3 · FULL SPINE COVERAGE", OLD_STEP3, NEW_STEP3)

# ------------------------------------------------------------ P3 · Rule 2A
edit(
    "P3 · Rule 2A · timed phase -> timed band",
    "is a core classroom act, not a pre-class assumption. It must appear as\n"
    "an explicit timed phase somewhere within the periods allocated to that\n"
    "section.",
    "is a core classroom act, not a pre-class assumption. It must appear as\n"
    "an explicit timed band somewhere within the periods allocated to that\n"
    "section.",
)

# ------------------------------------------------------------- P3 · Rule 3
edit(
    "P3 · Rule 3 · phase descriptions -> band activities (task reference)",
    "Task references in `tasks_in_class[]` use the summary's enumeration\n"
    "key (spine + zero-based task_index). Phase descriptions reference\n"
    "tasks by spine_section_name and a brief — they do not restate the\n"
    "full `task_text` or enumerate sub-items verbatim.",
    "Task references in `tasks_in_class[]` use the summary's enumeration\n"
    "key (spine + zero-based task_index). Band activities reference\n"
    "tasks by spine_section_name and a brief — they do not restate the\n"
    "full `task_text` or enumerate sub-items verbatim.",
)
edit(
    "P3 · Rule 3 · phase descriptions -> band activities (split task)",
    "in period N+1), each period lists the same key; phase descriptions\n"
    "distinguish what happens in each period.",
    "in period N+1), each period lists the same key; band activities\n"
    "distinguish what happens in each period.",
)

# ------------------------------------------------------------- P3 · Rule 5
edit(
    "P3 · Rule 5 · time constraint",
    "Each period's phases sum exactly to `period_duration_minutes`. Minimum\n"
    "3 phases per period.\n"
    "\n"
    '`phases[].minutes` is a STRING time-range (e.g., "0–10", "10–25").\n'
    "Ranges tile the period from 0 to `period_duration_minutes` with no\n"
    "gaps and no overlaps. Overrun is not permitted.",
    "Each period's time bands sum exactly to `period_duration_minutes`.\n"
    "Minimum 3 bands per period.\n"
    "\n"
    '`time_bands[].minutes` is a STRING time-range (e.g., "0–10", "10–25").\n'
    "Ranges tile the period from 0 to `period_duration_minutes` with no\n"
    "gaps and no overlaps. Overrun is not permitted.",
)

# ------------------------------------------------------------- P3 · Rule 7
edit(
    "P3 · Rule 7 · C-code prohibition surface list",
    "periods, phases, teacher_notes, or coverage_handoff.",
    "periods, time bands, teacher_notes, or coverage_handoff.",
)

# ------------------------------------------------------------- P3 · Rule 8
edit(
    "P3 · Rule 8 · locator mirror",
    'range when the task has none). This mirrors the "(page NN)" locator a phase\n'
    "gives an in-class task",
    'range when the task has none). This mirrors the "(page NN)" locator a band\n'
    "gives an in-class task",
)

# ------------------------------------------------- P3 + M5 · Rule 9 narration
edit(
    "P3 · Rule 9 · heading",
    "RULE 9 | PHASE NARRATION",
    "RULE 9 | BAND NARRATION",
)
edit(
    "P3 + M5 · Rule 9 · the narration sentence",
    "When a phase invokes a textbook task, the phase's `description` text\n"
    'names the task by its anchor location and a 10-word brief, e.g.\n'
    '"Reading for Meaning passage on pankhas (read-aloud + paired\n'
    'discussion)".\n'
    "\n"
    "Format: <spine_section_name> (“brief description up to 10 words....”)\n",
    "When a time band invokes a textbook task, the band's `activity` text\n"
    'names the task by its anchor location and a 10-word brief, e.g.\n'
    '"Let us read passage on pankhas (read-aloud + paired discussion)".\n'
    "\n"
    "Format: <spine_section_name> (“brief description up to 10 words....”)\n"
    "\n"
    "WHICH SUBHEADING. Where the summary's `section_name` for a cell is a\n"
    "MERGED string of several textbook subheadings (e.g. \"Let us read + Let\n"
    "us discuss + Let us think and reflect\"), name the single subheading the\n"
    "task actually sits under, not the merged string. The merged form is the\n"
    "cell's identity, not a location a teacher can turn to.\n",
)
edit(
    "P3 · Rule 9 · THREE FIELDS list",
    "  - phase `description`\n",
    "  - time band `activity`\n",
)
edit(
    "P3 · Rule 9 · lint scope",
    "It scans every `teacher_notes`, phase `description`, and `task_brief` for",
    "It scans every `teacher_notes`, time band `activity`, and `task_brief` for",
)

# ---------------------------------------------------------- P3 · INPUTS 1
edit(
    "P3 · INPUTS 1 · source-of-truth sentence",
    "   The text-summary fields are the source of truth the LP reads when\n"
    "   composing teacher_notes and phase descriptions.",
    "   The text-summary fields are the source of truth the LP reads when\n"
    "   composing teacher_notes and time band activities.",
)

# --------------------------------------------------- M4 + M3 · Rule 10 edits
edit(
    "M4 · Rule 10 · section_context 10-15 -> 10-18",
    "  - `section_context`    — 10–15 words naming the specific content,",
    "  - `section_context`    — 10–18 words naming the specific content,",
)
edit(
    "M1 · Rule 10 · empty-spine state vs breach",
    "If a spine has no anchored tasks across any section, emit the spine\n"
    "key with an empty `section_contributions: []` array. The assessment\n"
    "generator omits that spine from the assessment entirely.\n"
    "\n"
    "Total assessment item count equals the total number of\n"
    "`section_contributions` entries across all spines in the handoff —\n"
    "one item per (section × spine) cell, driven by the cell-level\n"
    "`implied_lo`.\n",
    "A spine the summary does not carry for ANY section is emitted with an\n"
    "empty `section_contributions: []` array, and the assessment generator\n"
    "omits that spine entirely. A spine the summary DOES carry may not arrive\n"
    "here empty — that is a breach of Rule 2's FULL SPINE COVERAGE, not a\n"
    "permitted state. Absent from the summary is a state; dropped for time is\n"
    "a defect.\n"
    "\n"
    "Total assessment item count is TWO per `section_contributions` entry\n"
    "across all spines in the handoff — a PAIR per (section × spine) cell,\n"
    "both items driven by the cell-level `implied_lo` and sampling it at two\n"
    "rungs (assessment constitution Rule 2). The item count does not vary\n"
    "with the period count: a shorter plan yields the same items, tested on\n"
    "less anchored practice.\n",
)

# ------------------------------------------------------- P3 + M5 · the schema
edit(
    "M5 · schema · tasks_in_class task_brief <= 12 -> <= 18",
    '      "task_brief":    string         // ≤ 12 words, plain English,\n'
    "                                      // teacher-facing\n",
    '      "task_brief":    string         // ≤ 18 words INCLUDING the Rule 9\n'
    "                                      // locator; plain English,\n"
    "                                      // teacher-facing\n",
)
edit(
    "P3 · schema · phases -> time_bands",
    '  "phases": [\n'
    '    { "minutes":     string,          // "0–10" — tiles 0..duration\n'
    '      "description": string }         // narrative; refers to tasks\n'
    "                                      // by spine_section_name + brief\n"
    "  ],\n",
    '  "time_bands": [\n'
    '    { "minutes":  string,             // "0–10" — tiles 0..duration\n'
    '      "activity": string }            // narrative; refers to tasks\n'
    "                                      // by spine_section_name + brief\n"
    "  ],\n",
)
edit(
    "P1 · schema · teacher_notes loses the forward preview",
    '  "teacher_notes": string,            // 2–3 sentences max. Scope (in\n'
    "                                      // priority order):\n"
    "                                      //  1. Transition from prior\n"
    "                                      //     unit; preview into next.\n"
    "                                      //  2. Common pitfall in this\n"
    "                                      //     spine, drawn from the\n"
    "                                      //     anchored section's\n"
    "                                      //     `prose_summary` /\n"
    "                                      //     `poem_appreciation_summary`\n"
    "                                      //     only (no fabrication).\n"
    "                                      //  3. Self-study pointer: a\n"
    "                                      //     task NOT covered in class.\n"
    "                                      // No C-code refs.\n",
    '  "teacher_notes": string,            // 2–3 sentences max, in priority\n'
    "                                      // order:\n"
    "                                      //  1. backward continuity, naming\n"
    "                                      //     the CONTENT built on — never\n"
    "                                      //     a unit's position, and never\n"
    "                                      //     a preview of what comes next\n"
    "                                      //     (register ban 2);\n"
    "                                      //  2. Common pitfall in this\n"
    "                                      //     spine, drawn from the\n"
    "                                      //     anchored section's\n"
    "                                      //     `prose_summary` /\n"
    "                                      //     `poem_appreciation_summary`\n"
    "                                      //     only (no fabrication).\n"
    "                                      //  3. Self-study pointer: a\n"
    "                                      //     task NOT covered in class.\n"
    "                                      // No C-code refs.\n",
)
edit(
    "M5 · schema · contribution task_brief <= 12 -> <= 18",
    '      "task_brief":  string    // ≤ 12 words, copied from tasks_in_class;\n',
    '      "task_brief":  string    // ≤ 18 words, copied from tasks_in_class;\n',
)
edit(
    "M4 · schema · contribution section_context 10-15 -> 10-18",
    '  "section_context":  string,  // 10–15 words: the specific content, text, or\n',
    '  "section_context":  string,  // 10–18 words: the specific content, text, or\n',
)

# --------------------------------------------------------------------- apply
failures = []
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

# ------------------------------------------------------------------- guards
GUARDS_ZERO = [
    "phases[",            # P3: the array is gone
    '"phases"',           # P3: the key is gone
    "band_id",            # the band layer left the declaration surface
    "phase_ref",          # cancelled
    "role_handoff",       # A2/A3/A4 cancelled
    "unit_handoff",
    "band_ref",
    "role weighting",
    "section registry",   # V-rules never enter a constitution
    "reserved token",
    "synthesis unit",
    "alphabetic",         # A9 arrangement sentence must never appear
    "never led with",
    "first word at which they differ",
    "the previous unit",  # register ban 2 / VOCABULARY re-cut
    "preview into next",
]
GUARDS_PRESENT = {
    # once as the VOCABULARY cross-reference, once as the block heading
    "THE SELF-CONTAINED REGISTER": 2,
    "NAME A CLOCK QUANTITY": 1,
    "POINT FORWARD OR CLAIM COMPLETION": 1,
    "NAME CALENDAR TIME": 1,
    "exactly ONE row": 1,
    "master-plan calibration bands": 1,
    "FULL SPINE COVERAGE": 2,
    "time_bands": 2,
    '"activity": string': 1,
    "BAND NARRATION": 1,
    "VERSION 1.7": 1,
    "Version 1.7": 1,
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

# -------------------------------------------------------------------- write
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "lp_english_middle_v1.6_pre.txt").write_text(original, encoding="utf-8")
diff = "".join(
    difflib.unified_diff(
        original.splitlines(keepends=True),
        text.splitlines(keepends=True),
        fromfile="lesson_plan_constitution.txt (v1.6)",
        tofile="lesson_plan_constitution.txt (v1.7)",
        n=3,
    )
)
(OUT / "lp_english_middle_v1.6_to_v1.7.diff").write_text(diff, encoding="utf-8")
LP.write_text(text, encoding="utf-8")

print(f"OK — {len(edits)} edits applied, {len(GUARDS_ZERO)} absence guards and "
      f"{len(GUARDS_PRESENT)} presence guards passed.")
print(f"     pre-file : {(OUT / 'lp_english_middle_v1.6_pre.txt').relative_to(ROOT)}")
print(f"     diff     : {(OUT / 'lp_english_middle_v1.6_to_v1.7.diff').relative_to(ROOT)}")
print(f"     amended  : {LP.relative_to(ROOT)}")
