#!/usr/bin/env python3
"""S5 · the_world_around_us · preparatory — P1: the LP constitution, v1.2 → v1.3.

testing.md §3 P1: Amendment A1 (exactly ONE standard period row) + Amendments A5/A7
(the self-contained register, as ONE block, in the SS·secondary v1.10 three-ban re-cut).

TWAU is NOT S6's two-ban exception. Its units anchor to textbook sections
(`section_ref`), it has a section axis, and its units travel between canonicals under
the variant-canonical serve engine — so ban 2 (forward reference / completion) binds in
full, exactly as it does for every stage except science·middle.

Nothing pedagogical moves. Every edit is an exact-string replacement with a guard, and
the script refuses to write if any anchor is missing or already applied.
"""
from __future__ import annotations

import difflib
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
LP = (ROOT / "data/content/constitutions/lesson_plan/the_world_around_us"
           / "preparatory/lesson_plan_constitution.txt")
OUT = pathlib.Path(__file__).resolve().parent

src = LP.read_text(encoding="utf-8")
before = src

# ─────────────────────────────────────────────────────────────────────────────
# 1 · VERSION
# ─────────────────────────────────────────────────────────────────────────────
edits: list[tuple[str, str, str]] = []

edits.append((
    "VERSION 1.2 → 1.3",
    "ARUVI · LESSON PLAN GENERATION CONSTITUTION · THE WORLD AROUND US · VERSION 1.2",
    "ARUVI · LESSON PLAN GENERATION CONSTITUTION · THE WORLD AROUND US · VERSION 1.3",
))

# ─────────────────────────────────────────────────────────────────────────────
# 2 · VOCABULARY — stop TEACHING the forward reference ban 2 forbids.
#     The old cross-reference examples were literally "the previous unit" / "this
#     unit"; the first is fine, the second is fine, but the pair reads as a licence
#     to cross-reference by POSITION, which is what ban 2 exists to stop. Same edit
#     S7 and S8 made to the maths files. "session" joins the excluded register.
# ─────────────────────────────────────────────────────────────────────────────
edits.append((
    "VOCABULARY — drop the positional cross-reference examples; exclude 'session'",
    'The atomic teaching chunk is called a "unit" in ALL teacher-facing prose — '
    'teacher_facilitation_note, activity titles, homework, and any cross-reference to '
    'another chunk (e.g. "the previous unit", "this unit"). The token "period" is '
    'retained ONLY in (a) schema field names (period_number, period_duration_minutes, '
    'periods[], etc.) and (b) the scheduling/allocation budget (period schedule, period '
    'count, per-period budget). Never write "period" in prose the teacher reads.',

    'The atomic teaching chunk is called a "unit" in ALL teacher-facing prose — '
    'teacher_facilitation_note, activity titles, homework, and any cross-reference to '
    'another chunk. The token "period" is retained ONLY in (a) schema field names '
    '(period_number, period_duration_minutes, periods[], etc.) and (b) the '
    'scheduling/allocation budget (period schedule, period count, per-period budget). '
    'Never write "period" in prose the teacher reads; "session" is outside the register '
    'too. Cross-reference another unit by the CONTENT it built, never by its position '
    '(see THE SELF-CONTAINED REGISTER below).',
))

# ─────────────────────────────────────────────────────────────────────────────
# 3 · THE SELF-CONTAINED REGISTER — one block, three bans, TWAU's own strings.
#     Placed immediately after VOCABULARY, before the SUBJECT line, exactly where
#     the v1.10 reference puts it.
# ─────────────────────────────────────────────────────────────────────────────
REGISTER = '''
THE SELF-CONTAINED REGISTER (binds Rule 5's time_bands and teacher_facilitation_note, and Rule 10's IKS prompt)
Three things no time band or facilitation note may do, each because the platform enforces it:
1. NAME A CLOCK QUANTITY — the platform scales every band's minutes in proportion to the sitting that carries it, so a stated number is falsified silently: no "for three minutes", "the remaining time", "half the session". Where a task is genuinely brief or genuinely long, say so in kind — "a quick look round the classroom", "an unhurried sorting activity" — never in number. The band's own "minutes" field is the schema's, not prose, and is untouched by this ban.
2. POINT FORWARD OR CLAIM COMPLETION — a teacher's plan may end, or hand over to a companion variant's unit, after any unit, so "the next unit", "as we will see", "now that we have named every landform" are wrong for someone. Each unit closes on its own ground.
3. NAME CALENDAR TIME — Aruvi keeps no calendar and sittings do not map to days: today, yesterday, this week, next class are unknowable at authoring.
Backward continuity is welcome, and is best carried by naming the content built on ("The children have already watched water change state, …") rather than a unit's position.
'''

edits.append((
    "insert THE SELF-CONTAINED REGISTER after VOCABULARY",
    "\nSUBJECT: the_world_around_us   STAGE: Preparatory (Grades III, IV, V)",
    REGISTER + "\nSUBJECT: the_world_around_us   STAGE: Preparatory (Grades III, IV, V)",
))

# ─────────────────────────────────────────────────────────────────────────────
# 4 · AMENDMENT A1 (the CAMPAIGN's A1 — not this file's "AMENDMENT A1 — FULL LP
#     JSON SCHEMA", which is a different thing with the same name). INPUTS 4.
#     "serve time", not the reference's "partition time": the partition engine was
#     retired 2026-07-31. Same declared deviation S3, S4, S6, S7 and S8 carry.
# ─────────────────────────────────────────────────────────────────────────────
edits.append((
    "A1 — INPUTS 4 becomes exactly ONE standard row",
    "4.  Period schedule — one or more rows of {duration_minutes, count}.",
    "4.  Period schedule — exactly ONE row {duration_minutes, count}: the\n"
    "    class-standard duration (40 min for the Preparatory stage — the\n"
    "    master-plan calibration band) × the period count; total = that product.\n"
    "    Teacher timetable variation never reaches generation; it is handled\n"
    "    downstream at serve time.",
))

# The INTEGRITY CONSTRAINTS time line still speaks of "rows" in the plural, which
# licenses the shape A1 has just removed. Same fact, stated once.
edits.append((
    "INTEGRITY CONSTRAINTS — TIME line follows A1 to the single row",
    "- TIME: total minutes = sum of (duration × count) per schedule row; total period\n"
    "  count = sum of row counts. The full budget is teaching only.",
    "- TIME: the schedule is ONE row (A1), so total minutes = duration × count and the\n"
    "  total period count IS that count. The full budget is teaching only.",
))

# And the schema's period_schedule array, which is the surface the model copies from
# — S8's transferable lesson: grep the SHAPE, not just the rule.
edits.append((
    "A1 residue — the period_schedule schema comment",
    '  "period_schedule": [\n'
    '    { "duration_minutes": "integer", "count": "integer" }\n'
    '  ],',
    '  "period_schedule": [                      // EXACTLY ONE row (INPUTS 4)\n'
    '    { "duration_minutes": "integer", "count": "integer" }\n'
    '  ],',
))

# ─────────────────────────────────────────────────────────────────────────────
# 5 · Bind the register at the two fields it governs, BY REFERENCE — never as
#     scattered prohibitions (testing.md P1: "as ONE block, never as scattered
#     prohibitions").
# ─────────────────────────────────────────────────────────────────────────────
edits.append((
    "Rule 5 — bind the register at teacher_facilitation_note",
    "teacher_facilitation_note — one brief note: an open question, grouping, or\n"
    "pacing cue.",
    "teacher_facilitation_note — one brief note: an open question, grouping, or\n"
    "pacing cue. A pacing cue is given in KIND, never in number, and the note obeys\n"
    "THE SELF-CONTAINED REGISTER in full.",
))

edits.append((
    "Rule 5 — bind the register at time_bands",
    'style), with the page matching this period\'s textbook_anchor. Bands that are\n'
    'pure setup, oral discussion, board work, or notebook-only reflection need no\n'
    'citation. Example: "Students open Textbook p. 105 and collect the listed\n'
    'objects in the table…". Never surface T-IDs.',

    'style), with the page matching this period\'s textbook_anchor. Bands that are\n'
    'pure setup, oral discussion, board work, or notebook-only reflection need no\n'
    'citation. Example: "Students open Textbook p. 105 and collect the listed\n'
    'objects in the table…". Never surface T-IDs. Every band\'s prose obeys THE\n'
    'SELF-CONTAINED REGISTER in full.',
))

# ─────────────────────────────────────────────────────────────────────────────
# apply
# ─────────────────────────────────────────────────────────────────────────────
for name, old, new in edits:
    if old not in src:
        sys.exit(f"ANCHOR MISSING — {name}\n  looked for: {old[:110]!r}")
    if src.count(old) != 1:
        sys.exit(f"ANCHOR NOT UNIQUE ({src.count(old)}×) — {name}")
    src = src.replace(old, new)
    print(f"  applied · {name}")

# ─────────────────────────────────────────────────────────────────────────────
# guards — the things that must NOT be here afterwards
# ─────────────────────────────────────────────────────────────────────────────
def assert_absent(needle: str, why: str) -> None:
    if needle.lower() in src.lower():
        sys.exit(f"GUARD FAILED — {needle!r} present: {why}")

def assert_count(needle: str, n: int) -> None:
    got = src.count(needle)
    if got != n:
        sys.exit(f"GUARD FAILED — {needle!r} appears {got}×, expected {n}")

# cancelled amendments (testing.md §3: A2/A3/A4 cancelled, X3 void) and V-rules
for bad, why in (
    ("role_handoff",   "A2/A3/A4 are cancelled"),
    ("unit_handoff",   "A2/A3/A4 are cancelled"),
    ("band_id",        "band ids are derived positionally by compile v0.5, never declared"),
    ("band_ref",       "band refs are a retired declaration"),
    ("phase_ref",      "the v1.2-era band-level phase_ref is reversed"),
    ("role weighting", "retired with the partition engine"),
    ("section registry", "V2 is brief-carried, never constitutional"),
    ("reserved token", "the synthesis mandate is V-series, never constitutional"),
    ("section_anchor", "founder ruling 2026-08-10: no new field to feed the serve engine"),
):
    assert_absent(bad, why)

# the band shape is already time_bands (P3 is N/A for this stage) — assert it stayed
assert_count("phases[", 0)
assert_count('"phases"', 0)
if "time_bands" not in src:
    sys.exit("GUARD FAILED — time_bands vanished")

# A1 landed exactly once, and the plural row shape is gone
assert_count("exactly ONE row {duration_minutes, count}", 1)
assert_absent("one or more rows of {duration_minutes, count}", "A1 replaced it")

# the register landed exactly once, with all three bans
assert_count("THE SELF-CONTAINED REGISTER", 3)   # the block heading + 2 bindings
for ban in ("NAME A CLOCK QUANTITY", "POINT FORWARD OR CLAIM COMPLETION",
            "NAME CALENDAR TIME"):
    assert_count(ban, 1)

LP.write_text(src, encoding="utf-8")

diff = "".join(difflib.unified_diff(
    before.splitlines(keepends=True), src.splitlines(keepends=True),
    fromfile="lesson_plan_constitution.txt (v1.2)",
    tofile="lesson_plan_constitution.txt (v1.3)"))
(OUT / "lp_v1.2_to_v1.3.diff").write_text(diff, encoding="utf-8")

print(f"\nWROTE {LP}")
print(f"WROTE {OUT / 'lp_v1.2_to_v1.3.diff'}")
print("all guards passed")
