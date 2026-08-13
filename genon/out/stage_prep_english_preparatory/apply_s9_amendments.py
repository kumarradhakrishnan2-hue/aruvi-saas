#!/usr/bin/env python3
"""S9 · english · preparatory — P1 + P3 + the measured edits, on the LP constitution.

Reproducible, guarded, idempotent-by-refusal: every replacement asserts an EXACT
occurrence count against the pre-file before it is made, so a re-run on an already
amended file fails loudly rather than half-applying.

Pre-file, diff and this script are the P1/P3 artefacts (testing.md §3).

  english/preparatory lesson_plan_constitution.txt   v1.1 -> v1.2

WHAT LANDS, and under which step:

  P1 · A1     INPUTS 3 becomes exactly ONE row at the class-standard duration.
              THIS STAGE'S A1 IS NOT THE USUAL ONE-ROW EDIT. The file did not
              merely permit several rows — it named the WRONG BAND outright:
              "`period_duration_minutes` is 30 or 35 at prep (35 default)".
              master_plan.json carries english|III, english|IV and english|V at
              standard_duration_minutes = 40. Rule 2 STEP 1's ceiling table was
              stated for 30- and 35-minute periods and named no 40 at all, and
              the schema comment read "// 30 or 35". All three are corrected to
              the single 40-minute preparatory standard. Evidence that this was
              live, not theoretical: of the four saved preparatory plans, three
              carry MIXED durations inside one plan (iii ch 2 = 2x40 + 2x35;
              iv ch 1 = 5x35 + 2x40; v ch 1 = 3x35 + 2x40 + 1x30).

  P1 · A5/A7  THE SELF-CONTAINED REGISTER, one block after VOCABULARY, in the
              v1.10 three-ban re-cut. VOCABULARY's own positional examples
              ("the previous unit", "this unit") are struck with it — the line
              was TEACHING the cross-reference ban 2 forbids — and so is the
              teacher_notes schema comment's "preview into next", which
              testing.md P1 names as the known direct contradiction in the
              english family.

  P3          phases[{minutes, description}] -> time_bands[{minutes, activity}],
              array and key, with Rule 5, Rule 9's heading, Rule 2A's "explicit
              timed phase", Rule 3's narration and listening bands, Rule 8's
              locator mirror, the lint-scope line and the schema all following.
              No band_id. Target: zero occurrences of "phase" in the file, as
              at english/middle and english/secondary.

  MEASURED (not carry-forward; taken here because P-prep is where they are free)

  M1  Rule 2 STEP 3 — FULL SPINE COVERAGE replaces the drop licence. Under
      architecture v2.0 a library shares ONE registry, so a compact that drops
      a spine is a different chapter from its standard. The preparatory corpus
      does it: iii ch 1's handoff carries 3 of its 5 summary cells.

  M2  Rule 1 — the closing-unit exception. v2.0 mandates the standard
      canonical's whole-chapter synthesis unit; Rule 1's "exactly ONE
      main_section and one or two adjacent spines" (with prep's extra
      "secondary spine carries 1 task only") cannot describe it.

  M3  Rule 10 — the item-count line said ONE item per (section x spine) cell;
      this stage's own assessment constitution v1.4 (2026-08-12) emits TWO.
      testing.md's S10 sign-off predicted this line would be here and free.

  M4  Rule 9 — WHICH SUBHEADING a merged cell names. 93 of preparatory's 167
      cells (55%) carry a MERGED `section_name`, the longest 28 words; the
      pilot's writing and word_work cells are both merged. The rule is
      unsatisfiable at any brief cap without this clause.

  M5  Schema — `task_brief` gains the family cap of <= 18 words INCLUDING the
      Rule 9 locator. Preparatory stated NO cap at all, against a Rule 9 that
      mandates the locator: simulating the locator at its true cost (+4 words)
      puts 14 of 29 saved briefs over 12 and 0 over 16.

  M6  `activity_title` <= 10 -> <= 12 words (family alignment; the preparatory
      corpus already sits exactly ON the old cap at 10) and `section_context`
      10-15 -> 10-18 words (family alignment; preparatory's own corpus maxes at
      13 and does not force it — recorded as unforced in the sign-off).

  M7  Footer said "Version 1.0" against a v1.1 header. Stale since the v1.1
      bump; corrected to 1.2 with the family's "· Internal Document" suffix.
"""
from __future__ import annotations

import difflib
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
LP = ROOT / "data/content/constitutions/lesson_plan/english/preparatory/lesson_plan_constitution.txt"
OUT = pathlib.Path(__file__).resolve().parent

original = LP.read_text(encoding="utf-8")
text = original

edits: list[tuple[str, str, str, int]] = []   # label, old, new, expected count


def edit(label: str, old: str, new: str, count: int = 1) -> None:
    edits.append((label, old, new, count))


# ---------------------------------------------------------------- P1 · header
edit(
    "VERSION header 1.1 -> 1.2",
    "ARUVI — ENGLISH LESSON PLAN CONSTITUTION · PREPARATORY · VERSION 1.1",
    "ARUVI — ENGLISH LESSON PLAN CONSTITUTION · PREPARATORY · VERSION 1.2",
)
edit(
    "M7 · footer 1.0 (stale) -> 1.2",
    "English Lesson Plan Constitution · Preparatory · Version 1.0",
    "English Lesson Plan Constitution · Preparatory · Version 1.2 · Internal Document",
)

# ------------------------------------------------- P1 · A5/A7 · the register
OLD_VOCAB = (
    'The atomic teaching chunk is called a "unit" in ALL teacher-facing prose — '
    "teacher_notes, activity titles, homework, and any cross-reference to another "
    'chunk (e.g. "the previous unit", "this unit"). The token "period" is retained '
    "ONLY in (a) schema field names (period_number, period_duration_minutes, "
    "periods[], etc.) and (b) the scheduling/allocation budget (period schedule, "
    'period count, per-period budget). Never write "period" in prose the teacher '
    "reads.\nStage: Preparatory (Grades III–V)\n"
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
    '"a quick paired chant", "an unhurried reading aloud" — never in number.\n'
    "2. POINT FORWARD OR CLAIM COMPLETION — a teacher's plan may end, or hand over "
    'to a companion variant\'s unit, after any unit, so "the next unit", "as we '
    'will see", "now that we have recited the whole poem" are wrong for someone. '
    "Each unit closes on its own ground.\n"
    "3. NAME CALENDAR TIME — Aruvi keeps no calendar and sittings do not map to "
    "days: today, yesterday, this week, next class are unknowable at authoring.\n"
    "Backward continuity is welcome, and is best carried by naming the content "
    'built on ("Having chanted the laddoo rhyme together, …") rather than a '
    "unit's position.\n"
    "\n"
    "Stage: Preparatory (Grades III–V)\n"
)
edit("A5/A7 register block + VOCABULARY re-cut", OLD_VOCAB, NEW_VOCAB)

# ------------------------------------------------------------------- P1 · A1
OLD_INPUTS3 = (
    "3. Period schedule: `{ period_duration_minutes, period_count }`.\n"
    "   `period_count = B` from the Allocate tab.\n"
    "   `period_duration_minutes` is 30 or 35 at prep (35 default).\n"
)
NEW_INPUTS3 = (
    "3. Period schedule — exactly ONE row `{ period_duration_minutes,\n"
    "   period_count }`: the class-standard duration (40 min for classes up to\n"
    "   VII, 45 for VIII, 50 for IX–X — the master-plan calibration bands, not\n"
    "   NCF's flat 40) × the period count, where `period_count = B` from the\n"
    "   Allocate tab. Preparatory is classes III–V, so every preparatory plan is\n"
    "   authored at 40 MINUTES. There is no 30- or 35-minute preparatory period:\n"
    "   teacher timetable variation never reaches generation, it is handled\n"
    "   downstream at serve time.\n"
)
edit("A1 · INPUTS 3 — one row at the 40-min preparatory standard", OLD_INPUTS3, NEW_INPUTS3)

# ------------------------------------------------- M2 · Rule 1 closing unit
OLD_R1 = (
    "ONE spine per period is preferred at prep. Two spines are permitted\n"
    "only when (a) both spines exist in the same section, (b) both fit the\n"
    "task budget (Rule 2 Step 1), (c) they are adjacent in the spine walk,\n"
    "and (d) the secondary spine carries 1 task only.\n"
)
NEW_R1 = (
    "ONE spine per period is preferred at prep. Two spines are permitted\n"
    "only when (a) both spines exist in the same section, (b) both fit the\n"
    "task budget (Rule 2 Step 1), (c) they are adjacent in the spine walk,\n"
    "and (d) the secondary spine carries 1 task only.\n"
    "\n"
    "The one exception is a CLOSING unit that draws the whole main_section\n"
    "together — revisiting what several spines built rather than teaching a\n"
    "new cell. It may name as many spines as it genuinely revisits, it is not\n"
    "bound by clause (d), and it teaches no cell of its own. Every OTHER unit\n"
    "stays inside the one-or-two spine bound above.\n"
)
edit("M2 · Rule 1 — closing-unit exception", OLD_R1, NEW_R1)

# ------------------------------- A1 (cont.) · Rule 2 STEP 1 duration ceiling
OLD_STEP1 = (
    "A 30-min period holds at most 2–3 tasks; a 35-min period holds 2–4.\n"
    "Do not exceed these ceilings regardless of summary task count.\n"
)
NEW_STEP1 = (
    "A 40-minute period — the preparatory class-standard and the ONLY duration\n"
    "a plan is authored at (INPUTS 3) — holds at most 2–3 tasks across its\n"
    "spine(s). Do not exceed this ceiling regardless of summary task count.\n"
    "Sittings shorter or longer than 40 minutes are handled downstream at serve\n"
    "time and are never authored for.\n"
)
edit("A1 · Rule 2 STEP 1 — the 40-minute ceiling", OLD_STEP1, NEW_STEP1)

# --------------------------------------- M1 · Rule 2 STEP 3 full coverage
OLD_STEP3 = (
    "STEP 3 — Within each section, cover spines in textbook order, packing\n"
    "tasks per Step 1 budget. When the section's allocated periods are\n"
    "exhausted, stop. Remaining spines/tasks are NOT forced into a period\n"
    "— flag them in `teacher_notes` of the section's last period as a\n"
    "self-study pointer. This is an honest reflection of available time,\n"
    "not a defect.\n"
)
NEW_STEP3 = (
    "STEP 3 — Within each section, cover spines in textbook order, packing\n"
    "tasks per Step 1 budget.\n"
    "\n"
    "FULL SPINE COVERAGE: every spine the summary records for a section MUST\n"
    "be taught in at least one of that section's periods. Dropping a spine is\n"
    "FORBIDDEN, at every period count — a shorter plan is the same chapter\n"
    "taught in fewer periods, not a smaller chapter. A class given seven\n"
    "periods instead of twelve should still read, talk, write and play with\n"
    "words; it should do less of each. A spine the summary does not carry for\n"
    "that section is simply absent and is not a drop.\n"
    "\n"
    "Curation happens at TASK level, where Rule 3 governs it: a spine under\n"
    "pressure is taught with fewer of its tasks anchored, never skipped.\n"
    "Unfitted TASKS go to homework (Rule 8) or are left unanchored and flagged\n"
    "in `teacher_notes` of the section's last period as a self-study pointer;\n"
    "that is an honest reflection of available time, not a defect. An unfitted\n"
    "SPINE is a defect.\n"
)
edit("M1 · Rule 2 STEP 3 — FULL SPINE COVERAGE", OLD_STEP3, NEW_STEP3)

# ------------------------------------------------------ P3 · phase -> band
edit(
    "P3 · Rule 2A — explicit timed band",
    "as an explicit timed phase within the periods allocated to that",
    "as an explicit timed band within the periods allocated to that",
)
edit(
    "P3 · Rule 2A — re-recite band",
    "FIRST period; later periods may include a 2–3 min re-recite phase but",
    "FIRST period; later periods may include a 2–3 min re-recite band but",
)
edit(
    "P3 · Rule 3 — band activities reference tasks",
    "(0-based index into the section's `tasks_verbatim[]`). Phase\n"
    "descriptions reference tasks by `spine_section_name` + brief; they do\n"
    "not restate `task_text` or enumerate sub-items verbatim.\n",
    "(0-based index into the section's `tasks_verbatim[]`). Band\n"
    "activities reference tasks by `spine_section_name` + brief; they do\n"
    "not restate `task_text` or enumerate sub-items verbatim.\n",
)
edit(
    "P3 · Rule 3 — listening bands",
    "`transcript_ref` + `transcript_text`, the period MUST include a 3–5\n"
    "min listening phase (teacher reads the transcript aloud, 3–4\n"
    "repetitions per NCF prep guidance) and a 2–3 min student response\n"
    "phase. These phases sit inside the parent oracy task's period and do\n"
    "NOT consume additional task slots.\n",
    "`transcript_ref` + `transcript_text`, the period MUST include a 3–5\n"
    "min listening band (teacher reads the transcript aloud, 3–4\n"
    "repetitions per NCF prep guidance) and a 2–3 min student response\n"
    "band. These bands sit inside the parent oracy task's period and do\n"
    "NOT consume additional task slots.\n",
)
edit(
    "P3 · Rule 3 — split task, band activities",
    "periods; phase descriptions distinguish the two halves.",
    "periods; band activities distinguish the two halves.",
)
edit(
    "P3 · Rule 5 — time_bands",
    "Each period's phases sum exactly to `period_duration_minutes`.\n"
    "Minimum 3 phases; prep periods typically have 4–6.\n"
    "\n"
    '`phases[].minutes` is a STRING time-range (e.g. "0–8", "8–20").\n',
    "Each period's time bands sum exactly to `period_duration_minutes`.\n"
    "Minimum 3 bands; prep periods typically have 4–6.\n"
    "\n"
    '`time_bands[].minutes` is a STRING time-range (e.g. "0–8", "8–20").\n',
)
edit(
    "P3 · Rule 8 — locator mirror",
    'page range when the task has none). This mirrors the "(page NN)" locator\n'
    "a phase gives an in-class task — a homework item a teacher cannot locate\n",
    'page range when the task has none). This mirrors the "(page NN)" locator\n'
    "a band gives an in-class task — a homework item a teacher cannot locate\n",
)

# ---------------------------------- P3 + M4 · Rule 9 heading and narration
OLD_R9_HEAD = (
    "RULE 9 | PHASE NARRATION\n"
    "================================================================================\n"
    "\n"
    "When a phase invokes a textbook task, the description names the task\n"
    "by anchor location + brief (≤ 10 words).\n"
    "\n"
    "Format: `<spine_section_name> (“brief ≤ 10 words”)`\n"
    "Example: `Let us Learn — A. (“consonant-cluster blend-and-say drill”)`\n"
)
NEW_R9_HEAD = (
    "RULE 9 | BAND NARRATION\n"
    "================================================================================\n"
    "\n"
    "When a time band invokes a textbook task, the band's `activity` names the\n"
    "task by anchor location + brief (≤ 10 words).\n"
    "\n"
    "Format: `<spine_section_name> (“brief ≤ 10 words”)`\n"
    "Example: `Let us Learn — A. (“consonant-cluster blend-and-say drill”)`\n"
    "\n"
    "WHICH SUBHEADING. Where the summary's `section_name` for a cell is a\n"
    "MERGED string of several textbook subheadings (e.g. “Let us think + Let\n"
    "us write”), name the single subheading the task actually sits under, not\n"
    "the merged string. The merged form is the cell's identity, not a location\n"
    "a teacher can turn to. At preparatory this is the ordinary case, not the\n"
    "exception: more than half of the stage's cells carry a merged name, and\n"
    "the longest runs to 28 words — longer by itself than the whole brief.\n"
)
edit("P3 + M4 · Rule 9 — BAND NARRATION and WHICH SUBHEADING", OLD_R9_HEAD, NEW_R9_HEAD)

edit(
    "P3 · Rule 9 — three teacher-facing fields",
    "THREE FIELDS ARE TEACHER-FACING and bound by this rule:\n"
    "  - phase `description`\n",
    "THREE FIELDS ARE TEACHER-FACING and bound by this rule:\n"
    "  - time band `activity`\n",
)
edit(
    "P3 · Rule 9 — lint scope",
    "It scans every `teacher_notes`, phase `description`, and `task_brief` for",
    "It scans every `teacher_notes`, time band `activity`, and `task_brief` for",
)

# ------------------------------------------- M6 + M3 · Rule 10 handoff
edit(
    "M6 · Rule 10 — section_context 10–15 -> 10–18",
    "  - `section_context`  10–15 words naming the specific content the\n",
    "  - `section_context`  10–18 words naming the specific content the\n",
)
OLD_R10_TAIL = (
    "The assessment generator reads `implied_lo` (drives question type and\n"
    "cognitive demand) and `section_context` (drives what the question is\n"
    "about). A spine with no anchored tasks emits its key with\n"
    "`section_contributions: []`; the assessment generator omits it\n"
    "entirely. Total assessment items = total `section_contributions`\n"
    "across all spines (one item per (section × spine) cell).\n"
)
NEW_R10_TAIL = (
    "The assessment generator reads `implied_lo` (drives question type and\n"
    "cognitive demand) and `section_context` (drives what the question is\n"
    "about).\n"
    "\n"
    "A spine the summary does not carry for ANY section is emitted with an\n"
    "empty `section_contributions: []` array, and the assessment generator\n"
    "omits that spine entirely. A spine the summary DOES carry may not arrive\n"
    "here empty — that is a breach of Rule 2 STEP 3's FULL SPINE COVERAGE, not\n"
    "a permitted state. Absent from the summary is a state; dropped for time is\n"
    "a defect.\n"
    "\n"
    "Total assessment item count is TWO per `section_contributions` entry\n"
    "across all spines in the handoff — a PAIR per (section × spine) cell,\n"
    "both items driven by the cell-level `implied_lo` and sampling it at two\n"
    "rungs, recognition then short production (assessment constitution Rule 2).\n"
    "The item count does not vary with the period count: a shorter plan yields\n"
    "the same items, tested on less anchored practice.\n"
)
edit("M3 · Rule 10 — THE PAIR replaces one-item-per-cell", OLD_R10_TAIL, NEW_R10_TAIL)

# ------------------------------------------------------------- the schema
edit(
    "A1 · schema — period_duration_minutes comment",
    '  "period_duration_minutes": integer,         // 30 or 35\n',
    '  "period_duration_minutes": integer,         // 40 — the preparatory\n'
    "                                              // class-standard; the only\n"
    "                                              // duration authored (INPUTS 3)\n",
)
edit(
    "M6 · schema — activity_title ≤ 10 -> ≤ 12",
    '  "activity_title": string,                   // ≤ 10 words\n',
    '  "activity_title": string,                   // ≤ 12 words\n',
)
edit(
    "M5 · schema — task_brief cap (tasks_in_class)",
    '  "tasks_in_class": [\n'
    '    { "spine": string, "task_index": integer, "task_brief": string }\n'
    "  ],\n",
    '  "tasks_in_class": [\n'
    '    { "spine": string, "task_index": integer, "task_brief": string }\n'
    "    // task_brief ≤ 18 words INCLUDING the Rule 9 locator; plain English,\n"
    "    // teacher-facing\n"
    "  ],\n",
)
edit(
    "P3 · schema — time_bands",
    '  "phases": [\n'
    '    { "minutes": string, "description": string }\n'
    "    // minutes tiles 0..duration; description per Rule 9\n"
    "  ],\n",
    '  "time_bands": [\n'
    '    { "minutes": string, "activity": string }\n'
    "    // minutes tiles 0..duration; activity per Rule 9\n"
    "  ],\n",
)
edit(
    "P1 · schema — teacher_notes register scope",
    "  \"teacher_notes\": string,                    // 2–3 sentences max. Scope\n"
    "                                              // (priority order):\n"
    "                                              //  1. transition from prior unit;\n"
    "                                              //     preview into next\n",
    "  \"teacher_notes\": string,                    // 2–3 sentences max. Scope\n"
    "                                              // (priority order):\n"
    "                                              //  1. backward continuity, naming\n"
    "                                              //     the CONTENT built on — never\n"
    "                                              //     a unit's position, and never\n"
    "                                              //     a preview of what comes next\n"
    "                                              //     (register ban 2)\n",
)
edit(
    "P3 · schema — materials comment",
    '                                              // any period with a Rule 2A phase\n',
    '                                              // any period with a Rule 2A band\n',
)
edit(
    "M6 · schema — contribution section_context 10–15 -> 10–18",
    '  "section_context": string,                  // 10–15 words\n',
    '  "section_context": string,                  // 10–18 words\n',
)
edit(
    "M5 · schema — contribution task_brief cap",
    '  "tasks_anchored": [\n'
    '    { "spine": string, "task_index": integer, "task_brief": string }\n'
    "  ]\n"
    "}\n",
    '  "tasks_anchored": [\n'
    '    { "spine": string, "task_index": integer, "task_brief": string }\n'
    "    // task_brief ≤ 18 words, copied from tasks_in_class;\n"
    "    // LP audit record only — not read by assessment\n"
    "  ]\n"
    "}\n",
)

# ------------------------------------------------------------------ apply
failures: list[str] = []
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
    '"phases"',
    "phase",              # and the word with it, as at middle and secondary
    "Phase",
    "band_id",            # never in the target shape
    "section_anchor",     # english's anchor is mediated (P5.5 part 5)
    "phase_ref",          # the v1.2-era band-level anchor, reversed
    "role_handoff",       # cancelled A2/A3/A4
    "unit_handoff",
    "band_ref",
    "role weighting",
    "section registry",   # V-rules never enter a constitution
    "reserved token",
    "synthesis unit",
    "closing synthesis",
    "alphabetic",         # A9's arrangement sentence must never appear
    "never led with",
    "first word at which they differ",
    "the previous unit",  # register ban 2 / VOCABULARY re-cut
    "preview into next",
    "30 or 35",           # A1: the wrong duration band
    "one item per",       # M3: the stale item-count line
]
GUARDS_PRESENT = {
    # once as the VOCABULARY cross-reference, once as the block heading
    "THE SELF-CONTAINED REGISTER": 2,
    "NAME A CLOCK QUANTITY": 1,
    "POINT FORWARD OR CLAIM COMPLETION": 1,
    "NAME CALENDAR TIME": 1,
    "exactly ONE row": 1,
    "master-plan calibration bands": 1,
    "authored at 40 MINUTES": 1,
    "FULL SPINE COVERAGE": 2,
    "WHICH SUBHEADING": 1,
    "time_bands": 2,
    '"activity": string': 1,
    "BAND NARRATION": 1,
    "TWO per `section_contributions`": 1,
    "≤ 18 words": 2,
    "VERSION 1.2": 1,
    "Version 1.2": 1,
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
(OUT / "lp_english_preparatory_v1.1_pre.txt").write_text(original, encoding="utf-8")
diff = "".join(
    difflib.unified_diff(
        original.splitlines(keepends=True),
        text.splitlines(keepends=True),
        fromfile="lesson_plan_constitution.txt (v1.1)",
        tofile="lesson_plan_constitution.txt (v1.2)",
        n=3,
    )
)
(OUT / "lp_english_preparatory_v1.1_to_v1.2.diff").write_text(diff, encoding="utf-8")
LP.write_text(text, encoding="utf-8")

print(f"OK — {len(edits)} edits applied, {len(GUARDS_ZERO)} absence guards and "
      f"{len(GUARDS_PRESENT)} presence guards passed.")
print(f"     pre-file : {(OUT / 'lp_english_preparatory_v1.1_pre.txt').relative_to(ROOT)}")
print(f"     diff     : {(OUT / 'lp_english_preparatory_v1.1_to_v1.2.diff').relative_to(ROOT)}")
print(f"     amended  : {LP.relative_to(ROOT)}")
