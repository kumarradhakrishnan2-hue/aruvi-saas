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
    "ARUVI · LESSON PLAN GENERATION CONSTITUTION · SOCIAL SCIENCES · SECONDARY STAGE · VERSION 1.1.1\n"
    "(v1.1, 2026-07-24: Rule 14 — band identity, role, and edge band anchoring; time input = single standard row. "
    "Serialization and input-shape only; no pedagogical rule changed.)\n"
    "(v1.1.1, 2026-07-25: Rule 14 role guidance made definitional — arc framing removed, roles judged on a "
    "best-effort basis. Labeling only; band structure and all other rules unchanged.)",
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

# --- Rule 14 ---
RULE14 = """================================================================================
RULE 14 · BAND IDENTITY, ROLE, AND EDGE BAND ANCHORING — SERIALIZATION ONLY

MANDATE
This rule changes how the finished plan is REPORTED, never how it is planned. Author every unit exactly as Rules 1–13 direct; then label what was authored:
1. band_id — every time band carries a stable identifier "P<period_number>.<ordinal>" (the first band of unit 7 is "P7.1").
2. role — every time band declares the function its text already performs, based on the following guidance, applied on a best-effort basis:
   hook — a provocation, recall bridge, or orienting question.
   development — reading, source work, construction, structured discussion that advances content.
   consolidation — synthesis, resolution, wrap-up writing.
   Judge role from the band's own text, not its position.
3. band_refs — every competency edge names the band_id(s) OF ITS OWN UNIT whose activity actually executes that competency's cognitive operation, applying Rule 5's genuineness test band by band. At least one band; several when the operation genuinely spans bands.
4. The coverage handoff copies each edge's band_refs verbatim onto its LO row (Amendment A2).

PROHIBITION
1. MUST NOT alter, add, reorder, or retime any band to fit a role pattern — roles label the authored plan; they are never a template for it.
2. MUST NOT default band_refs to all bands of the unit — the genuineness test is applied per band.
3. MUST NOT let band_refs reach outside the unit that owns the edge.
4. MUST NOT use role values outside {hook, development, consolidation}.

"""
lp = edit(
    lp,
    "================================================================================\nINTEGRITY CONSTRAINTS",
    RULE14 + "================================================================================\nINTEGRITY CONSTRAINTS",
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
    '"minutes": "string e.g. 0-8", "activity": "string", '
    '"role": "hook | development | consolidation (Rule 14)" } ],',
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

(OUT / "lesson_plan_constitution_v1.1.1.txt").write_text(lp)

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
print("LP  v1.1.1:", len(lp), "chars")
print("AC  v1.2:", len(ac), "chars")
print("written to", OUT)
