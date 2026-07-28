#!/usr/bin/env python3
"""Reproduce the genon constitutional amendments for SS-secondary by surgical string edits.

APPLIED LIVE 2026-07-24: the outputs of this script were written directly onto the
live SaaS constitutions (data/content/constitutions/.../social_sciences/secondary/),
which are now the canonical v1.1 (LP) and v1.2 (assessment) texts. This script is the
reproducible record: it reads the pre-amendment texts from amended/originals/ and
re-derives the amended texts byte-identically. Every edit asserts exactly-one
occurrence; everything else is untouched.

History:
- 2026-07-23 (v1 of this script): drafts made from the PROTOTYPE MIRROR v1.0 texts.
  Superseded — the mirror base lacked the assessment's v1.1 MCQ answer-distribution
  rule, so those drafts would have silently dropped it.
- 2026-07-24 (this version): rebased onto the live SaaS texts (LP v1.0, assessment
  v1.1 incl. the MCQ rule); added the single-standard-row time-input edits
  (HANDOVER Decision 2); assessment version lands at v1.2.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "amended" / "originals"
OUT = HERE / "amended"
OUT.mkdir(parents=True, exist_ok=True)


def edit(text, old, new):
    assert text.count(old) == 1, f"expected exactly 1 occurrence, got {text.count(old)}: {old[:80]!r}"
    return text.replace(old, new)


# ---------------- LP constitution: v1.0 -> v1.1.1 ----------------
# (v1.1.1, 2026-07-25: after the first live 21×50 canonical came out uniformly
#  3-banded hook→dev→consolidation, Rule 14's role clause was made definitional:
#  arc verbs removed, "exactly one of" → best-effort guidance, the
#  exception-catalogue sentence dropped. Founder-approved minimal change.)
lp = (SRC / "lesson_plan_constitution_v1.0.txt").read_text()

lp = edit(
    lp,
    "ARUVI · LESSON PLAN GENERATION CONSTITUTION · SOCIAL SCIENCES · SECONDARY STAGE · VERSION 1.0",
    "ARUVI · LESSON PLAN GENERATION CONSTITUTION · SOCIAL SCIENCES · SECONDARY STAGE · VERSION 1.3\n"
    "(v1.1, 2026-07-24: Rule 14 — band identity, role, and edge band anchoring; time input = single standard row. "
    "Serialization and input-shape only; no pedagogical rule changed.)\n"
    "(v1.1.1, 2026-07-25: Rule 14 role guidance made definitional — arc framing removed, roles judged on a "
    "best-effort basis. Labeling only; band structure and all other rules unchanged.)\n"
    "(v1.1.2, 2026-07-25: temporal self-containment — band text carries no calendar words and no cross-unit "
    "references; teacher notes' previous-unit link is the only cross-unit reference, always backward, never "
    "in calendar time. Register only; no pedagogical rule changed.)\n"
    "(v1.2, 2026-07-25: roles leave the bands — Rule 14 carries identity and anchoring only; a new Rule 15 "
    "classifies every band's role in a single role_handoff emitted after the plan is complete, so authoring "
    "is never shaped by the role taxonomy. Serialization only; no pedagogical rule changed.)\n"
    "(v1.2.1, 2026-07-26: teacher notes become position-free — the continuity link names the content it "
    "builds on, never a unit's position; positional orientation belongs exclusively to the platform, which "
    "alone knows where a timetable places each boundary. Register only; no pedagogical rule changed.)\n"
    "(v1.3, 2026-07-28: a new Rule 16 emits unit_handoff — a title and a teacher note for every adjacent "
    "pair of units, authored after the plan is complete, so the platform can name and annotate a sitting "
    "that spans a unit boundary without an LLM in the request path. Companion output only; no pedagogical "
    "rule changed.)",
)

# --- time input: single standard row (HANDOVER Decision 2) ---
lp = edit(
    lp,
    "4. Period schedule — one or more rows of {duration_minutes, count}",
    "4. Period schedule — exactly ONE row {duration_minutes, count}: the class-standard duration "
    "(40 min for classes up to VII, 45 for VIII, 50 for IX) × the period count. "
    "Teacher timetable variation never reaches generation; it is handled downstream at partition time.",
)

lp = edit(
    lp,
    "- TIME: total minutes = Σ(duration × count); total unit count = Σ(row counts); exactly one activity per unit, calibrated to its duration.",
    "- TIME: the schedule is a single standard row; total minutes = duration × count; total unit count = count; "
    "exactly one activity per unit, calibrated to the standard duration.",
)

# --- v1.1.2: temporal self-containment (2026-07-25) ---
# Found live: the 21x50 canonical carried "today" and "next unit" inside band text
# (P1.1/P4.1/P10.2 temporal; 11 positional) — deixis that re-orients the teacher from
# flow to day and breaks under repartition. Doctrine: content is TIMELESS; navigation
# belongs to container text the engine owns.
lp = edit(
    lp,
    'MUST NOT restate the activity verbatim, cite c-codes or internal IDs, fabricate confusions, or open with "Transition"/a section label.',
    'MUST NOT restate the activity verbatim, cite c-codes or internal IDs, fabricate confusions, or open with "Transition"/a section label.\n'
    "MUST NOT use calendar words (today, yesterday, this week, next class) or forward references "
    "(the next unit, in the next…, we shall see) — the Rule-10 link to the previous unit is the ONLY "
    "cross-unit reference, and it always looks backward.",
)

lp = edit(
    lp,
    "4. MUST NOT invent a parallel activity prompt where the section's own captured apparatus box already supplies one that serves the unit's purpose.",
    "4. MUST NOT invent a parallel activity prompt where the section's own captured apparatus box already supplies one that serves the unit's purpose.\n"
    "5. MUST NOT anchor band text in calendar time or unit position — no calendar words (today, "
    "yesterday, this week, next class) and no cross-unit references (the previous unit, the next unit, "
    "as we saw, in the next…). Each band speaks in the present of its own activity; sequence lives in "
    "the plan's structure, and unit-to-unit linking lives only in teacher_notes (Rule 10).",
)

# --- v1.2.1: position-free teacher notes (2026-07-26) ---
# Founder finding: under partition, stacked notes juggle multiple positional anchors
# ("previous unit… this unit…" × N), and after a seam "the previous unit" can describe
# content taught minutes earlier in the SAME sitting — anachronistic. Continuity is now
# expressed by NAMING the content; position words originate only in the engine's seam
# clause, where the actual partition makes them true.
lp = edit(
    lp,
    'The atomic teaching chunk is a "unit" in ALL teacher-facing prose (teacher_notes, activity titles, homework, cross-references such as "the previous unit").',
    'The atomic teaching chunk is a "unit" in ALL teacher-facing prose (teacher_notes, activity titles, homework).',
)

lp = edit(
    lp,
    "Every unit carries non-blank teacher_notes: 2–3 sentences of flowing prose weaving in a link to the previous unit (the first unit orients to the chapter's start), one common confusion drawn only from the chapter summary, and optionally a facilitation pointer.",
    "Every unit carries non-blank teacher_notes: 2–3 sentences of flowing prose weaving in a continuity link "
    "to the content already taught — named by that content itself, never by its position (the first unit "
    "orients to the chapter's start), one common confusion drawn only from the chapter summary, and "
    "optionally a facilitation pointer.",
)

lp = edit(
    lp,
    "MUST NOT use calendar words (today, yesterday, this week, next class) or forward references "
    "(the next unit, in the next…, we shall see) — the Rule-10 link to the previous unit is the ONLY "
    "cross-unit reference, and it always looks backward.",
    "MUST NOT use calendar words (today, yesterday, this week, next class) or positional references of any "
    "direction — the previous unit, this unit, the next unit, last time, in the next…. Continuity is "
    "expressed by naming the content it builds on (“Having traced the Vedic political vocabulary, …”), "
    "never by pointing at units: only the platform knows where a teacher's timetable places each boundary.",
)

# --- Rule 14 ---
RULE14 = """================================================================================
RULE 14 · BAND IDENTITY AND EDGE BAND ANCHORING — SERIALIZATION ONLY

MANDATE
This rule changes how the finished plan is REPORTED, never how it is planned. Author every unit exactly as Rules 1–13 direct; then label what was authored:
1. band_id — every time band carries a stable identifier "P<period_number>.<ordinal>" (the first band of unit 7 is "P7.1").
2. band_refs — every competency edge names the band_id(s) OF ITS OWN UNIT whose activity actually executes that competency's cognitive operation, applying Rule 5's genuineness test band by band. At least one band; several when the operation genuinely spans bands.
3. The coverage handoff copies each edge's band_refs verbatim onto its LO row (Amendment A2).

PROHIBITION
1. MUST NOT default band_refs to all bands of the unit — the genuineness test is applied per band.
2. MUST NOT let band_refs reach outside the unit that owns the edge.

================================================================================
RULE 15 · ROLE HANDOFF — REQUIRED COMPANION OUTPUT

MANDATE
After the lesson plan and coverage handoff are fully built, emit role_handoff as a sibling of lesson_plan: a flat classification covering EVERY band_id in the plan, in plan order. Each band is classified by the function its already-written text performs, exactly one of:
   hook — a provocation, recall bridge, or orienting question.
   development — reading, source work, construction, structured discussion that advances content.
   consolidation — synthesis, resolution, wrap-up writing.
Judge each band from its own text alone. This is a reading of the finished plan, never an input to it.

PROHIBITION
1. MUST NOT shape, size, order, or count any band in anticipation of this classification — the plan is authored complete under Rules 1–13 before this rule reads it.
2. MUST NOT use values outside {hook, development, consolidation}.
3. MUST NOT omit, invent, or duplicate a band_id — role_handoff covers exactly the bands the plan contains.

"""
lp = edit(
    lp,
    "================================================================================\nINTEGRITY CONSTRAINTS",
    RULE14 + "================================================================================\nINTEGRITY CONSTRAINTS",
)

# --- v1.3: Rule 16 · unit handoff (2026-07-28) ---
# Founder design. The plan is authored at one standard duration; a teacher's timetable
# cuts it somewhere else, and a sitting then routinely holds the tail of one unit and the
# head of the next. Until now the platform either joined the two titles mechanically
# ("A — continued, then B") or paid an LLM at request time to repair the join. Neither is
# right: the join is not a title, and the repair puts a model, a latency and a failure
# path in front of every teacher. A plan of N units has only N-1 adjacent joints, so the
# whole space is enumerable — author it once, here, where both units are fully in view.
RULE16 = """================================================================================
RULE 16 · UNIT HANDOFF — REQUIRED COMPANION OUTPUT

MANDATE
After the lesson plan, the coverage handoff, and the role handoff are complete, emit unit_handoff as a sibling of lesson_plan: one entry for every ADJACENT pair of units, keyed "<earlier>-<later>" in plan order. A plan of N units yields exactly N-1 entries — units 1&2, 2&3, … (N-1)&N.

This plan is authored at one standard duration. A teacher's timetable divides it elsewhere, so a single sitting will often carry the closing stretch of one unit and the opening stretch of the next. Each entry is the container text for one such joint, written once, here, where both units are fully in view — their bands, notes, section anchors, and the chapter summary. The platform selects the entry; it never composes one.

Each entry carries two fields:
- title — what the two units are jointly about: the single object of study that spans them, named as a teacher would name that sitting. Under 70 characters where that costs nothing.
- teacher_notes — one flowing note, at most 90 words, in the register of Rule 10. It opens by naming the content the sitting pivots on (the move from the one body of material to the other), then carries each unit's own named confusion, then at most one facilitation pointer. Everything in it comes from the two units' own text.

PROHIBITION
1. MUST NOT form the title by joining the two unit titles. Conjunctions and joiners are banned outright — "and", "&", "with", ", then", "into", "plus", a slash, or a dash used to splice two labels. A title that can be reconstructed by concatenating the two source titles has failed this rule; name the shared object instead.
2. MUST NOT assume either unit runs to completion in the sitting — the platform may place only part of one, or of both. No completion language ("having finished", "by the end of", "once all four are covered"), no counts of what was got through.
3. MUST NOT use calendar words or positional references — Rule 10's prohibition applies here unchanged, and "period", "session", "last time", "the previous unit" are all outside the register.
4. MUST NOT author new content: every fact, confusion, source, and task named must already appear in the two units' bands, notes, or the chapter summary.
5. MUST NOT shape, size, order, or count any unit in anticipation of this rule — the plan is authored complete under Rules 1–13, and read by Rules 15 and 16 afterwards.
6. MUST NOT omit an adjacent pair, emit a non-adjacent pair, or emit the entries out of plan order.

"""
lp = edit(
    lp,
    "================================================================================\nINTEGRITY CONSTRAINTS",
    RULE16 + "================================================================================\nINTEGRITY CONSTRAINTS",
)

# --- A1 schema edits ---
lp = edit(
    lp,
    "Edges carry no period_number: an edge's unit is the period that contains it — nesting is the linkage the assessment inherits.",
    "Edges carry no period_number: an edge's unit is the period that contains it — nesting is the linkage the assessment inherits.\n"
    "period_schedule: exactly one row — the class-standard duration × count (INPUTS 4).",
)

lp = edit(
    lp,
    '  "period_schedule": [ { "duration_minutes": "integer", "count": "integer" } ],',
    '  "period_schedule": [ { "duration_minutes": "integer — the class-standard duration", "count": "integer" } ],',
)

lp = edit(
    lp,
    '"time_bands": [ { "minutes": "string e.g. 0-8", "activity": "string" } ],',
    '"time_bands": [ { "band_id": "string — \\"P<period_number>.<ordinal>\\", e.g. \\"P7.2\\" (Rule 14)", '
    '"minutes": "string e.g. 0-8", "activity": "string" } ],',
)

lp = edit(
    lp,
    '            "cognitive_demand": "Recall | Understanding | Application | Analysis | Evaluation"\n'
    "          }\n"
    "        ]\n"
    "      }\n"
    "    ]\n"
    "  }\n"
    "}",
    '            "cognitive_demand": "Recall | Understanding | Application | Analysis | Evaluation",\n'
    '            "band_refs": ["string — band_id(s) of this unit whose activity executes this competency (Rule 14)"]\n'
    "          }\n"
    "        ]\n"
    "      }\n"
    "    ]\n"
    "  }\n"
    "}",
)

lp = edit(
    lp,
    '''  "coverage_handoff": { "...": "per Amendment A2 — required sibling of lesson_plan" },''',
    '''  "coverage_handoff": { "...": "per Amendment A2 — required sibling of lesson_plan" },
  "role_handoff": { "P<unit>.<n>": "hook | development | consolidation — one entry per band, in plan order (Rule 15)" },''',
)

# --- v1.3: A1 gains the unit_handoff sibling ---
lp = edit(
    lp,
    '''  "role_handoff": { "P<unit>.<n>": "hook | development | consolidation — one entry per band, in plan order (Rule 15)" },''',
    '''  "role_handoff": { "P<unit>.<n>": "hook | development | consolidation — one entry per band, in plan order (Rule 15)" },
  "unit_handoff": { "<n>-<n+1>": { "title": "string — the two units' shared object of study, never a join of their titles", "teacher_notes": "string — one note, ≤90 words, Rule 10 register" } },''',
)

# --- A2 schema edit ---
lp = edit(
    lp,
    '        "cognitive_demand": "Recall | Understanding | Application | Analysis | Evaluation — copied from the edge"\n'
    "      }\n"
    "    ]\n"
    "  }\n"
    "}",
    '        "cognitive_demand": "Recall | Understanding | Application | Analysis | Evaluation — copied from the edge",\n'
    '        "band_refs": ["string — copied verbatim from the edge (Rule 14)"]\n'
    "      }\n"
    "    ]\n"
    "  }\n"
    "}",
)

(OUT / "lesson_plan_constitution_v1.3.txt").write_text(lp)

# ---------------- Assessment constitution: v1.1 -> v1.2 ----------------
ac = (SRC / "assessment_constitution_v1.1_pre_phase_ref.txt").read_text()

ac = edit(
    ac,
    "ARUVI · CHAPTER ASSESSMENT CONSTITUTION · SOCIAL SCIENCES · SECONDARY STAGE · VERSION 1.1",
    "ARUVI · CHAPTER ASSESSMENT CONSTITUTION · SOCIAL SCIENCES · SECONDARY STAGE · VERSION 1.2\n"
    "(v1.2, 2026-07-24: phase_ref — band-level anchoring copied from the LO's band_refs. "
    "Serialization only; no selection or design rule changed.)",
)

ac = edit(
    ac,
    "   { period_number, section_anchor, section_context, implied_lo, cognitive_demand }",
    "   { period_number, band_refs, section_anchor, section_context, implied_lo, cognitive_demand }",
)

ac = edit(
    ac,
    "implied_lo and cognitive_demand were copied verbatim from the edge; the other three from the period that contained it.",
    "implied_lo, cognitive_demand, and band_refs were copied verbatim from the edge; the other three from the period that contained it.",
)

ac = edit(
    ac,
    "period_number is the LO's unit and display anchor;",
    "period_number is the LO's unit and display anchor; band_refs names the band(s) within that unit that execute the LO's competency operation (LP Constitution, Rule 14) and is copied verbatim onto each item as phase_ref;",
)

ac = edit(
    ac,
    "Linkage is an identity: each item's period_ref is the single unit of its source LO, and that unit is its display anchor.",
    "Linkage is an identity: each item's period_ref is the single unit of its source LO, and that unit is its display anchor. "
    "Likewise phase_ref: the source LO's band_refs copied verbatim — the band-level address of the same identity.",
)

ac = edit(
    ac,
    "3. MUST NOT re-adjudicate the inherited demand position on the Recall–Understanding–Application–Analysis–Evaluation spectrum.",
    "3. MUST NOT re-adjudicate the inherited demand position on the Recall–Understanding–Application–Analysis–Evaluation spectrum.\n"
    "4. MUST NOT alter, extend, re-derive, or leave empty phase_ref — it is a verbatim copy of the source LO's band_refs, nothing else.",
)

ac = edit(
    ac,
    '  "period_ref":        array   — exactly one element: the source LO\'s unit number.\n'
    "                                 Length-one array for schema stability.",
    '  "period_ref":        array   — exactly one element: the source LO\'s unit number.\n'
    "                                 Length-one array for schema stability.\n"
    '  "phase_ref":         array   — the source LO\'s band_refs copied VERBATIM (band_ids within\n'
    '                                 the anchor unit, e.g. ["P7.2", "P7.3"]). Never re-derived,\n'
    "                                 never empty (Rule 6).",
)

ac = edit(
    ac,
    "- period_ref is the source LO's single unit — linkage needs no tie-break because it is an identity.",
    "- period_ref is the source LO's single unit — linkage needs no tie-break because it is an identity.\n"
    "- phase_ref is the source LO's band_refs copied verbatim — the same identity at band level; no re-derivation.",
)

(OUT / "assessment_constitution_v1.2.txt").write_text(ac)
print("LP  v1.3:", len(lp), "chars")
print("AC  v1.2:", len(ac), "chars")
print("written to", OUT)
