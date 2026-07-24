#!/usr/bin/env python3
"""Produce v1.1 amended SS-secondary constitutions by surgical string edits.
Every edit asserts exactly-one occurrence; the rest of the text is byte-identical."""
from pathlib import Path

SRC = Path("/mnt/user-data/uploads/Project Aruvi/app/mirror/constitutions")
OUT = Path("/home/claude/genon/amended")
OUT.mkdir(parents=True, exist_ok=True)


def edit(text, old, new):
    assert text.count(old) == 1, f"expected exactly 1 occurrence, got {text.count(old)}: {old[:80]!r}"
    return text.replace(old, new)


# ---------------- LP constitution ----------------
lp = (SRC / "lesson_plan/social_sciences/secondary/lesson_plan_constitution.txt").read_text()

lp = edit(
    lp,
    "ARUVI · LESSON PLAN GENERATION CONSTITUTION · SOCIAL SCIENCES · SECONDARY STAGE · VERSION 1.0",
    "ARUVI · LESSON PLAN GENERATION CONSTITUTION · SOCIAL SCIENCES · SECONDARY STAGE · VERSION 1.1\n"
    "(v1.1, 2026-07-23: Rule 14 — band identity, role, and edge band anchoring. Serialization only; no pedagogical rule changed.)",
)

RULE14 = """================================================================================
RULE 14 · BAND IDENTITY, ROLE, AND EDGE BAND ANCHORING — SERIALIZATION ONLY

MANDATE
This rule changes how the finished plan is REPORTED, never how it is planned. Author every unit exactly as Rules 1–13 direct; then label what was authored:
1. band_id — every time band carries a stable identifier "P<period_number>.<ordinal>" (the first band of unit 7 is "P7.1").
2. role — every time band declares the function its text already performs, exactly one of:
   hook — opens the unit's arc: provocation, recall bridge, orienting question.
   development — carries teaching forward: reading, source work, construction, structured discussion that advances content.
   consolidation — gathers, closes, or fixes what the unit built: synthesis, resolution, wrap-up writing.
   Judge role from the band's own text, not its position. A unit may legitimately open without a hook or carry two consolidations — report what is there.
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

(OUT / "lesson_plan_constitution_v1.1.txt").write_text(lp)

# ---------------- Assessment constitution ----------------
ac = (SRC / "assessment/social_sciences/secondary/assessment_constitution.txt").read_text()

ac = edit(
    ac,
    "ARUVI · CHAPTER ASSESSMENT CONSTITUTION · SOCIAL SCIENCES · SECONDARY STAGE · VERSION 1.0",
    "ARUVI · CHAPTER ASSESSMENT CONSTITUTION · SOCIAL SCIENCES · SECONDARY STAGE · VERSION 1.1\n"
    "(v1.1, 2026-07-23: phase_ref — band-level anchoring copied from the LO's band_refs. Serialization only; no selection or design rule changed.)",
)

ac = edit(
    ac,
    "   { period_number, section_anchor, section_context, implied_lo, cognitive_demand }",
    "   { period_number, band_refs, section_anchor, section_context, implied_lo, cognitive_demand }",
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

(OUT / "assessment_constitution_v1.1.txt").write_text(ac)
print("LP v1.1  :", len(lp), "chars (orig 16758-ish)")
print("ASSESS v1.1:", len(ac), "chars (orig 18380-ish)")
print("written to", OUT)
