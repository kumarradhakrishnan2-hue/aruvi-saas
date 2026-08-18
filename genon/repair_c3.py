#!/usr/bin/env python3
"""repair_c3.py v1.0 — 2026-08-09

Repairs the C3 defects that can be repaired without re-authoring, on an installed library.

Two kinds of pass, deliberately kept apart, because they scale differently:

  GENERIC passes derive the correct value from an AUTHORITATIVE SOURCE — the chapter summary,
  the Pedagogy document, the mapping JSON, the schema. They take no per-chapter input and are
  intended to run over the whole corpus at the mass pre-warm, exactly as STEP 6 does for option
  order. Adding a chapter costs nothing.

  DECLARED passes apply a hand-written table of old → new strings for one chapter. They do NOT
  generalise: a register phrasing or a word-count rewrite needs language, per instance. They are
  here so this chapter's repair is reproducible and auditable, and so the shared plumbing
  (backup · refuse-on-drift · declared repairs[] · idempotent) is written once.

Every pass refuses rather than guesses: if the value on disk matches neither the expected old
nor the already-repaired new, the file is left alone and the run reports it.

Run from the repo root:
    python3 genon/repair_c3.py mathematics ix 4 --dry-run
    python3 genon/repair_c3.py mathematics ix 4
"""
from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import re
import shutil
import sys

TOOL = "genon/repair_c3.py v1.0"
ROOT = pathlib.Path(__file__).resolve().parents[1]
PLANS = ROOT / "data/content/saved_plans"
CHAPTERS = ROOT / "data/content/chapters"
BACKUP = ROOT / "backup/c3_repair"

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT))
from purge_derived import purge                                    # noqa: E402
from aruvi_core.genon import carriers as _carriers                 # noqa: E402

# The Pedagogy document's method names, verbatim. Source of truth for ARV-D-071.
PEDAGOGY_METHODS = ["Play-way", "Discovery/Inquiry", "Problem solving", "Inductive", "Deductive"]

# Rule 8's closing requirement, in the constitution's own words.
SUBSTITUTION_CLAUSE = (
    " The teacher may substitute any other format from the Mathematics open-task menu."
)

# Both forms observed in the corpus: a bare parenthetical "(E-3)" and a narrated one
# "(from E-1)". The book_ref always precedes it, so both are pure deletion.
ID_IN_PROSE = re.compile(r"\s*\((?:from\s+)?(?:WE|E)-\d+\)")


# =======================================================================================
# GENERIC PASSES — corpus-safe, source-derived, no per-chapter input
# =======================================================================================

def pass_method_label(result, ctx):
    """ARV-D-071 — pedagogical_method named exactly as the Pedagogy document writes it."""
    edits = []
    lookup = {m.lower(): m for m in PEDAGOGY_METHODS}
    for period in result["lesson_plan"]["periods"]:
        current = period.get("pedagogical_method") or ""
        correct = lookup.get(current.lower())
        if correct and correct != current:
            edits.append({"unit": period["period_number"], "field": "pedagogical_method",
                          "old": current, "new": correct})
            period["pedagogical_method"] = correct
    return edits


def pass_strip_internal_ids(result, ctx):
    """ARV-D-073 — Rule 9 P5: no WE-N / E-N in teacher-facing text; the book_ref is already
    there, so the parenthetical is pure deletion."""
    edits = []
    for period in result["lesson_plan"]["periods"]:
        unit = period["period_number"]

        for idx, band in enumerate(period.get("time_bands", [])):
            cleaned = ID_IN_PROSE.sub("", band["activity"])
            if cleaned != band["activity"]:
                edits.append({"unit": unit, "field": f"time_bands[{idx}].activity",
                              "old": band["activity"], "new": cleaned})
                band["activity"] = cleaned

        for idx, item in enumerate(period.get("homework", [])):
            cleaned = ID_IN_PROSE.sub("", item)
            if cleaned != item:
                edits.append({"unit": unit, "field": f"homework[{idx}]",
                              "old": item, "new": cleaned})
                period["homework"][idx] = cleaned

        for field in ("teacher_notes", "activity_title"):
            cleaned = ID_IN_PROSE.sub("", period.get(field, ""))
            if cleaned != period.get(field, ""):
                edits.append({"unit": unit, "field": field,
                              "old": period[field], "new": cleaned})
                period[field] = cleaned
    return edits


def pass_verbatim_descriptions(result, ctx):
    """ARV-D-077 — A3: textbook item description is verbatim from the summary. The summary IS
    the authority, so this is a copy, not a judgement."""
    edits = []
    canon = ctx["summary_items"]
    for period in result["lesson_plan"]["periods"]:
        for idx, item in enumerate(period.get("textbook_items_in_class", [])):
            source = canon.get(item.get("id"))
            if not source:
                continue
            want = source.get("description")
            if want and item.get("description") != want:
                edits.append({"unit": period["period_number"],
                              "field": f"textbook_items_in_class[{idx}].description",
                              "old": item.get("description"), "new": want})
                item["description"] = want
    return edits


def pass_guide_shape(result, ctx):
    """ARV-D-083 — A1: 'Populate every field; empty strings and empty arrays are not permitted
    for required fields.' Rule 9 defines ONE guide sub-block per question type. Sub-blocks for
    other types are set to null, which is the shape the other two canonicals already use."""
    edits = []
    for pos, item in enumerate(iter_items(result), 1):
        guide = item.get("guide")
        if not isinstance(guide, dict):
            continue
        keep = item.get("question_type")
        for key, block in list(guide.items()):
            if key == keep or block is None:
                continue
            if isinstance(block, dict):
                empties = sum(1 for v in block.values() if v in ("", [], {}))
                # learning_outcome is a duplicate of the kept block's own; everything else in a
                # foreign block must be empty for it to be safely prunable. A foreign block
                # carrying real content is a different defect and is not ours to delete.
                substantive = {k: v for k, v in block.items() if k != "learning_outcome"}
                if any(v not in ("", [], {}, None) for v in substantive.values()):
                    continue
                edits.append({"item": pos, "field": f"guide.{key}",
                              "old": f"<{len(block)} keys, {empties} empty>", "new": None})
                guide[key] = None
    return edits


def pass_open_task_substitution(result, ctx):
    """ARV-D-082 — Rule 8 requires the guide to state that the teacher may substitute any other
    menu format. Fixed sentence, so it is computable.

    SUBJECT-GATED SINCE 2026-08-12 (S5), AND THE GATE IS THE POINT. This pass sits in the
    GENERIC list, whose contract is "derive the correct value from an AUTHORITATIVE SOURCE …
    intended to run over the whole corpus at the mass pre-warm". It is not generic. Its
    authority is MATHEMATICS' Rule 8 open-task menu, and `SUBSTITUTION_CLAUSE` says so in
    words — "any other format from the **Mathematics** open-task menu".

    Run on TWAU it proposed **nine edits across the library** (4 + 3 + 2), appending that
    sentence to OPEN_TASK guides on a stage whose Rule 8 is EXECUTABILITY BOUNDARY and which
    has no open-task menu to substitute from. That is not a no-op that happens to be
    harmless — it writes a false statement about a rule that does not exist, in another
    subject's vocabulary, into a certified artefact. Found only because S5 ran this tool for
    an unrelated declared repair; at the mass pre-warm it would have reached every non-maths
    OPEN_TASK guide in the corpus.

    The other four passes are safe on TWAU by accident rather than by design, and it is worth
    recording which is which: `pass_method_label` keys on `pedagogical_method`, a field TWAU's
    schema does not have (its equivalent is the closed five-value `dominant_mode`);
    `pass_strip_internal_ids` matches `WE-N`/`E-N`, which TWAU never emits (its internal ids
    are `T-N`, and the LP already forbids them); `pass_verbatim_descriptions` reads
    `enumerated_worked_examples`/`enumerated_exercises` off the summary, which TWAU summaries
    do not carry. Only `pass_guide_shape` is genuinely subject-agnostic. **When a fifth stage
    arrives, check each pass's AUTHORITY, not its behaviour on one file.**"""
    if ctx.get("subject") != "mathematics":
        return []
    edits = []
    for pos, item in enumerate(iter_items(result), 1):
        if item.get("question_type") != "OPEN_TASK":
            continue
        block = (item.get("guide") or {}).get("OPEN_TASK")
        if not isinstance(block, dict):
            continue
        rationale = block.get("format_rationale") or ""
        if "substitute" in rationale.lower():
            continue
        new = rationale.rstrip() + SUBSTITUTION_CLAUSE
        edits.append({"item": pos, "field": "guide.OPEN_TASK.format_rationale",
                      "old": rationale, "new": new})
        block["format_rationale"] = new
    return edits


GENERIC_PASSES = [
    ("ARV-D-071", "method label verbatim from the Pedagogy document", pass_method_label),
    ("ARV-D-073", "internal WE-N / E-N ids out of teacher-facing text", pass_strip_internal_ids),
    ("ARV-D-077", "textbook descriptions verbatim from the summary", pass_verbatim_descriptions),
    ("ARV-D-083", "one guide sub-block per question type; no empty required fields",
     pass_guide_shape),
    ("ARV-D-082", "Rule 8 substitution statement present in OPEN_TASK guides",
     pass_open_task_substitution),
]


# =======================================================================================
# DECLARED EDITS — this chapter only; each one needed language or a judgement
# =======================================================================================

# ARV-D-069 · the register's three bans. Forward reference and completion language rewritten to
#   stand on their own ground; the calendar word removed.
# ARV-D-070 · Rule 10 continuity by CONTENT, never by position. In every case the content is
#   already named, so the repair is deletion of the positional clause.
# KEYED BY (subject, grade) SINCE 2026-08-17 — the filename key was a live trap twice
# over: (a) running `repair_c3.py science vii 4` walked ch_04_canonical*.json and applied
# MATHEMATICS·IX's declarations to the science files (crashing on a handoff shape the
# maths rows assume), and (b) adding science·vii's own "ch_04_canonical_p09.json" entry
# silently SHADOWED the maths key — the duplicate-dict-key failure repair_meta_leak's
# wave-2 header documents. Same cure as repair_register v1.3: scope the set to the
# subject·grade the run names, and a foreign filename can never be reached.
DECLARED = {
  ("science", "ix"): {
    # ── S3 · science · IX · ch 7 p18 (2026-08-17, batch wave 2) ──────────────────────
    # ARV-D-172 · `question_text: null` on the file's single OPEN_TASK (7.6.3 Lever,
    # the beam-balance table task). Unlike ARV-D-120b nothing is authored here: on an
    # OPEN_TASK the stem MUST be empty ("" — the prompt lives in `task`, where this
    # item's already is, in full). null -> "" is the whole repair; the certifier's
    # str(None) rendering ('None') is what tripped the gate.
    "ch_07_canonical_p18.json": {
        "ARV-D-172": [
            {"item_where": {"question_type": "OPEN_TASK", "section_label": "7.6.3 Lever"},
             "field": "question_text",
             "old": None, "new": ""},
        ],
    },
  },
  ("science", "vi"): {
    # ── S6 · science · middle · VI ch 12 third-pass resynth unit (2026-08-18) ─────────
    # ARV-D-176 · the F1-resynth read's ruling on "Postcards from the Dark Sky Camp":
    # identification layer fully within every compact, but two teacher-notes MANDATES
    # grade mechanisms p08 never taught (Venus orbit-position; comet evaporation/tail
    # direction — and the Milky-Way disc geometry no plan teaches). Founder-approved
    # rewording to supply-if-unmet: a teacher closing a synthesis legitimately adds a
    # fact at the margin; she must not be told to withhold credit for it. Third edit
    # deletes the early-finisher extension that duplicates Postcard 2 (already the
    # Milky Way faint band) — pure deletion, no replacement authored.
    "ch_12_canonical.json": {
        "ARV-D-176": [
            {"unit": 14, "field": "teacher_notes",
             "old": "check that replies include both the orbit-position reasoning and "
                    "the atmosphere explanation for its brightness; neither alone is "
                    "sufficient.",
             "new": "check that replies explain its brightness; if the orbit-position "
                    "reasoning surfaces in no group, supply it as the chapter's fact "
                    "and ask groups to fold it into their reply."},
            {"unit": 14, "field": "teacher_notes",
             "old": "the tail points away from the Sun); prompt those groups to add "
                    "the 'why it looks that way' sentence.",
             "new": "the tail points away from the Sun); if no group produces the "
                    "mechanism, supply it and ask them to add the 'why it looks that "
                    "way' sentence."},
            {"unit": 14, "field": "teacher_notes",
             "old": "If a group finishes early, ask them to add a fifth 'reply' for a "
                    "hypothetical postcard describing the Milky Way as a faint band — "
                    "this extends to Section 12.4 without being required of all "
                    "groups. ",
             "new": ""},
        ],
    },
    # ── S6 · science · middle · VI ch 2 resynth unit (2026-08-18, F1-resynth read) ────
    # ARV-D-175 · factual slip in the re-authored synthesis's model answer: the money
    # plant's card evidence ("soft green stem needing support") is the chapter's own
    # diagnostic for a CLIMBER (takes support; a creeper crawls on the ground), yet the
    # band labels it "creeper". One word; the card evidence, venation, root and habitat
    # readings all stay. Run: repair_c3.py science vi 2 --declared-only
    "ch_02_canonical.json": {
        "ARV-D-175": [
            {"unit": 21, "field": "time_bands[2].activity",
             "old": "soft green stem needing support — creeper",
             "new": "soft green stem needing support — climber"},
        ],
    },
    # ── S6 · science · middle · VI ch 8 (2026-08-17, batch wave 1) ───────────────────
    # ARV-D-173 · same defect as ARV-D-172, next stage over: `question_text: null` on the
    # file's single OPEN_TASK (the water-cycle classification table, stage 5). The item is
    # complete — task, scaffold, format_of_output, full guide — so null -> "" is again the
    # whole repair. Science·middle items carry no section_label (stage-anchored), so the
    # selector is question_type alone, which the certify report confirms is unique in this
    # library. Run as: python3 genon/repair_c3.py science vi 8 --declared-only
    "ch_08_canonical.json": {
        "ARV-D-173": [
            {"item_where": {"question_type": "OPEN_TASK"},
             "field": "question_text",
             "old": None, "new": ""},
        ],
    },
  },
  ("science", "vii"): {
    # ── S6 · science · middle · VII ch 4 p09 (2026-08-17, batch wave 2) ──────────────
    # ARV-D-174 · third instance of the ARV-D-172 family (172 science·ix ch 7 p18,
    # 173 science·vi ch 8): `question_text: null` on the compact's single OPEN_TASK,
    # item otherwise complete. null -> "" again. The rate — 3 in ~190 authored files
    # across two stages — says the schema's `// "" for OPEN_TASK` comment reads as
    # optional to the model roughly 1.5% of the time; a constitution-side fix is only
    # worth it if the rate holds at S7+. Run: repair_c3.py science vii 4 --declared-only
    "ch_04_canonical_p09.json": {
        "ARV-D-174": [
            {"item_where": {"question_type": "OPEN_TASK"},
             "field": "question_text",
             "old": None, "new": ""},
        ],
    },
    # ── ARV-D-177 · polish-fidelity read findings (2026-08-18, founder-licensed). The
    # gap-fill inventions were ACCEPTED as authored content; these five edits are the
    # read's specific corrections. All on the FINAL (synthesis) unit's visual_aids;
    # units are the top's last period per chapter.
    "ch_02_canonical.json": {
        "ARV-D-177": [
            # the response-sheet aid dropped the old materials' neutralisation-equation
            # box; restored as a footer row so the printed sheet has somewhere to write.
            {"unit": 15, "field": "visual_aids[1].table",
             "old": "4 — Stream water (downstream) | Red rose extract turns red to "
                    "green | | |",
             "new": "4 — Stream water (downstream) | Red rose extract turns red to "
                    "green | | |\nWrite the neutralisation reaction for one "
                    "correction: | | | |"},
        ],
    },
    "ch_03_canonical.json": {
        "ARV-D-177": [
            # "Semiconductor" is above the chapter's register (the chapter treats the
            # LED only through polarity / long-wire-positive); "Resistive" likewise.
            {"unit": 18, "field": "visual_aids[1].table",
             "old": "Semiconductor component; polarity must be respected",
             "new": "Polarity-sensitive component; long wire connects to positive"},
            {"unit": 18, "field": "visual_aids[1].table",
             "old": "Resistive component; no polarity requirement",
             "new": "Glows whichever way current flows; no polarity requirement"},
        ],
    },
    "ch_05_canonical.json": {
        "ARV-D-177": [
            # "particulate reasoning" is not a strand this chapter's plans teach —
            # unsourced concept claim in two aids.
            {"unit": 15, "field": "visual_aids[2].text",
             "old": "reversibility with particulate reasoning",
             "new": "reversibility"},
            {"unit": 15, "field": "visual_aids[3].text",
             "old": "desirability, particulate reasoning, slow natural change",
             "new": "desirability, slow natural change"},
        ],
    },
    "ch_11_canonical.json": {
        "ARV-D-177": [
            # the scene-card aid claims luminous vs non-luminous is covered but its
            # mapping table assigns it to no scene — the claim goes, the scenes stand.
            {"unit": 18, "field": "visual_aids[0].text",
             "old": "Principles covered across the five scenes: luminous vs. "
                    "non-luminous sources; rectilinear propagation",
             "new": "Principles covered across the five scenes: rectilinear "
                    "propagation"},
        ],
    },
  },
  ("mathematics", "ix"): {
    "ch_04_canonical.json": {
        "ARV-D-069": [
            {"unit": 3, "field": "time_bands[2].activity",
             "old": "— that is the focal error today.",
             "new": "— that is the focal error to watch for."},
        ],
        "ARV-D-070": [
            {"unit": 12, "field": "time_bands[0].activity",
             "old": "Students who judged the derivations in the previous unit share their "
                    "verdicts",
             "new": "Students who judged these two derivations share their verdicts"},
            {"unit": 12, "field": "time_bands[2].activity",
             "old": "not finished in the previous unit,",
             "new": "not yet finished,"},
        ],
        "ARV-D-030": [
            {"row": 7, "field": "section_context",
             "old": "binomial cube identities, sum and difference of cubes, three-variable cube "
                    "identity, factorisation and numerical application",
             "new": "binomial cube identities, sum and difference of cubes, three-variable cube "
                    "identity"},
            {"row": 9, "field": "section_context",
             "old": "integrative identity selection, expansion, factorisation, rational "
                    "simplification, geometric and numerical application across the chapter",
             "new": "integrative identity selection, expansion, factorisation, and rational "
                    "simplification across the chapter"},
        ],
        "ARV-D-074": [
            {"row": 6, "field": "period_numbers", "old": [8, 9], "new": [8]},
            {"row": 7, "field": "period_numbers", "old": [10, 11, 12], "new": [10, 11]},
        ],
        "ARV-D-075": [
            {"row": 5, "field": "c_code", "old": "C-9.3", "new": "C-3.1"},
        ],
    },
    "ch_04_canonical_p12.json": {
        "ARV-D-069": [
            {"unit": 7, "field": "teacher_notes",
             "old": "two skills that will recur when simplifying rational expressions",
             "new": "two skills that also underpin the simplification of rational expressions"},
            {"unit": 7, "field": "teacher_notes",
             "old": "may be set for later self-study once section 4.7 has been taught.",
             "new": "may be set for self-study by students who have already met the cube "
                    "identities."},
            {"unit": 7, "field": "homework[0]",
             "old": "End of Chapter Q1, p.88 — complete any remaining parts (vii)–(ix) after "
                    "section 4.7 is covered.",
             "new": "End of Chapter Q1, p.88 — complete any remaining parts (vii)–(ix), which "
                    "draw on the cube identities."},
            {"unit": 12, "field": "teacher_notes",
             "old": "a natural place for a final unit that advances coverage",
             "new": "a natural place for a unit that advances coverage"},
        ],
        "ARV-D-070": [
            {"unit": 3, "field": "teacher_notes",
             "old": "Having derived (a+b)² in the previous unit, this unit runs",
             "new": "Having derived (a+b)², this unit runs"},
            {"unit": 6, "field": "teacher_notes",
             "old": "Having seen middle-term splitting via the tile model in the previous unit, "
                    "students now",
             "new": "Having seen middle-term splitting via the tile model, students now"},
            {"unit": 9, "field": "teacher_notes",
             "old": "Having derived the binomial-cube identities in the previous unit, this unit",
             "new": "Having derived the binomial-cube identities, this unit"},
            {"unit": 11, "field": "teacher_notes",
             "old": "a higher demand than the rational-expression simplification of the previous "
                    "unit.",
             "new": "a higher demand than rational-expression simplification."},
        ],
    },
    "ch_04_canonical_p09.json": {
        "ARV-D-070": [
            {"unit": 2, "field": "time_bands[0].activity",
             "old": "Revisit the identity (a+b)^2 = a^2+2ab+b^2 from the previous unit's work and "
                    "pose",
             "new": "Revisit the identity (a+b)^2 = a^2+2ab+b^2 and pose"},
            {"unit": 9, "field": "time_bands[2].activity",
             "old": "for any items not completed in the previous unit.",
             "new": "for any items not yet completed."},
        ],
        "ARV-D-030": [
            {"row": 5, "field": "section_context",
             "old": "x^2, x, and unit tiles; rectangle model for (x+3)(x+4) and (2x+3)(3x+1); "
                    "middle-term split validated spatially",
             "new": "x^2, x, and unit tiles; rectangle model validating the middle-term split "
                    "spatially"},
        ],
        "ARV-D-075": [
            {"row": 5, "field": "c_code", "old": "C-9.3", "new": "C-3.1"},
            {"row": 6, "field": "c_code", "old": "C-3.1", "new": "C-9.3"},
        ],
    },
  },
  ("science", "viii"): {
    # ── ARV-D-177 (continued) · the mangrove data table's salinity row is the one
    # gap-fill whose DIRECTION has no source anywhere (DO and silt directions come from
    # band 4; salinity is wholly new). Student-facing data the task computes on — the
    # row goes rather than stands unsourced.
    "ch_12_canonical.json": {
        "ARV-D-177": [
            {"unit": 12, "field": "visual_aids[1].table",
             "old": "\nSalinity | 18 ppt | 22 ppt",
             "new": ""},
        ],
    },
  },
  ("the_world_around_us", "v"): {
    # ── S5 · the_world_around_us · V · ch 5 (2026-08-12) ─────────────────────────────
    # ARV-D-120 · the U11 item, two breaches on one item, and only ONE of them is mechanical.
    #
    # (a) `question_type: "HI"` — a `dominant_mode` code, outside the closed taxonomy
    #     {MCQ, SCR, ECR, OPEN_TASK}. The correct value is not guessed: the item's OWN
    #     `guide` is keyed `SCR`, it carries three `expected_elements` and an empty
    #     `options` — the SCR shape in every particular — so the file already declares what
    #     it is, and this pass makes the label agree with it. The cause is visible in
    #     assessment Rule 3, whose guidance table puts `dominant_mode` in the LEFT column and
    #     the type in the right ("HI / CG-6 inquiry steps … | SCR"); the model emitted the left.
    #
    # (b) `question_text: null` — A1 permits "" or [], never null, and for an SCR the stem IS
    #     the question, so as authored there was nothing to ask. THIS HALF IS AUTHORED, NOT
    #     DERIVED, and is therefore a DECLARED repair in the strictest sense: the stem below is
    #     written to the item's own three `expected_elements`, one clause each —
    #       1 "names one type of traditional headgear from the section"      -> "Name one …"
    #       2 "identifies at least one reason … climate, cultural occasion,
    #          or material available locally"                               -> "why … suits the
    #                                                                          region it comes from"
    #       3 "connects … to the broader idea that clothing reflects where
    #          people live and who they are"                                -> "what it tells us
    #                                                                          about the people who wear it"
    #     — and grounded in the section the item is anchored to (Diversity Everywhere: saafa/pagri
    #     from Rajasthan, topi from Himachal Pradesh, Textbook p. 87) and in its unit's activity
    #     (U11 "Headgear from Every Region"). No element is added that the guide does not already
    #     expect, and none is left unasked. The item's Rule 7 regional-variation annotation
    #     already covers the answer's regional spread and is untouched.
    "ch_05_canonical.json": {
        "ARV-D-120a": [
            {"item_where": {"period_ref": [11]}, "field": "question_type",
             "old": "HI", "new": "SCR"},
        ],
        "ARV-D-120b": [
            {"item_where": {"period_ref": [11]}, "field": "question_text",
             "old": None,
             "new": ("Name one traditional headgear worn in a particular region of India. "
                     "In two or three sentences, explain why that headgear suits the region "
                     "it comes from, and what it tells us about the people who wear it.")},
        ],
    },
  },
}


# =======================================================================================
# plumbing
# =======================================================================================

def iter_items(obj):
    if isinstance(obj, dict):
        if isinstance(obj.get("questions"), list):
            yield from obj["questions"]
        if isinstance(obj.get("assessment_items"), list):
            yield from obj["assessment_items"]
        for value in obj.values():
            yield from iter_items(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from iter_items(value)


def unit_of(result, number):
    for period in result["lesson_plan"]["periods"]:
        if period["period_number"] == number:
            return period
    raise KeyError(f"no unit {number}")


def get_nested(container, field):
    match = re.fullmatch(r"(\w+)\[(\d+)\](?:\.(\w+))?", field)
    if not match:
        # An ABSENT top-level field reads as None rather than raising (2026-08-17,
        # ARV-D-172): science·ix ch 7 p18's OPEN_TASK omitted `question_text` entirely,
        # and the certifier's str(item.get(...)) renders absent and null identically —
        # a declared edit with old=None must be able to reach both states. The
        # refuse-on-drift guard is unchanged: any OTHER current value still mismatches
        # the declared old and refuses.
        return container.get(field) if isinstance(container, dict) else container[field]
    name, idx, leaf = match.group(1), int(match.group(2)), match.group(3)
    target = container[name][idx]
    return target[leaf] if leaf else target


def set_nested(container, field, value):
    match = re.fullmatch(r"(\w+)\[(\d+)\](?:\.(\w+))?", field)
    if not match:
        container[field] = value
        return
    name, idx, leaf = match.group(1), int(match.group(2)), match.group(3)
    if leaf:
        container[name][idx][leaf] = value
    else:
        container[name][idx] = value


def apply_declared(result, table, filename):
    """Substring replacement inside a named field, or whole-value replacement for non-strings."""
    edits, refusals = [], []
    for defect, entries in table.items():
        for entry in entries:
            if "item_where" in entry:
                # THE ITEM SELECTOR (added 2026-08-12, S5 · ARV-D-120). The declared table
                # could reach a period or a handoff row, but not an assessment item — so a
                # defect in an item's own field had nowhere to be repaired.
                #
                # Selection is by EXACT MATCH on the item's own declared fields, never by a
                # computed join. That is deliberate: how an item finds its unit is the verified
                # 8-rule table's business and varies by subject·stage, so a selector that
                # re-derived it here would be genon inventing linkage — exactly what P5.5's
                # doctrine forbids. Matching literal field values invents nothing and reads the
                # same on every stage. `raw_item_list` returns the LIVE items (it is
                # container-shape aware), so the edit reaches the file.
                where = entry["item_where"]
                cands = [it for it in _carriers.raw_item_list(result)
                         if all(it.get(k) == v for k, v in where.items())]
                if len(cands) != 1:
                    refusals.append(f"{filename}: item_where {where!r} matched "
                                    f"{len(cands)} items, expected exactly 1")
                    continue
                container, label = cands[0], f"item{where}"
            elif "row" in entry:
                # .get, not [] (2026-08-17): a stage without section-numbered handoff
                # rows (science·middle) must REFUSE a foreign declaration, not crash.
                rows = [r for r in result["coverage_handoff"]
                        if r.get("section_number") == entry["row"]]
                if not rows:
                    refusals.append(f"{filename}: no handoff row {entry['row']}")
                    continue
                container, label = rows[0], f"sec#{entry['row']}"
            else:
                container, label = unit_of(result, entry["unit"]), f"U{entry['unit']}"

            current = get_nested(container, entry["field"])

            if isinstance(entry["old"], str):
                # Order matters: `new` is often a PREFIX of `old` (a shortened label), so the
                # already-repaired test must run only after the old text is ruled out.
                if entry["old"] in (current or ""):
                    updated = current.replace(entry["old"], entry["new"])
                elif entry["new"] in (current or ""):
                    continue                              # already repaired
                else:
                    refusals.append(
                        f"{filename} {label}.{entry['field']}: expected text absent — "
                        f"{entry['old'][:60]!r}")
                    continue
            else:
                if current == entry["new"]:
                    continue
                if current != entry["old"]:
                    refusals.append(
                        f"{filename} {label}.{entry['field']}: expected {entry['old']!r}, "
                        f"found {current!r}")
                    continue
                updated = entry["new"]

            set_nested(container, entry["field"], updated)
            edits.append({"defect": defect, "where": label, "field": entry["field"],
                          "old": entry["old"], "new": entry["new"]})
    return edits, refusals


def load_summary_items(subject, grade, chapter):
    path = CHAPTERS / subject / grade / "summaries" / f"ch_{chapter:02d}_summary.json"
    if not path.exists():
        return {}
    summary = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for key in ("enumerated_worked_examples", "enumerated_exercises"):
        for item in summary.get(key, []):
            out[item["id"]] = item
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("subject")
    parser.add_argument("grade")
    parser.add_argument("chapter", type=int)
    parser.add_argument("--dry-run", action="store_true")
    # --declared-only (2026-08-17, founder ruling at S3 wave 2): touch certified artefacts
    # only where a gate flagged them. The generic passes stay available for the corpus
    # pre-warm, but a declared repair must be appliable without dragging them along.
    parser.add_argument("--declared-only", action="store_true")
    args = parser.parse_args()

    folder = PLANS / args.subject / args.grade
    files = sorted(folder.glob(f"ch_{args.chapter:02d}_canonical*.json"))
    if not files:
        print(f"no library at {folder}")
        return 1

    # `subject` rides in ctx so a pass whose AUTHORITY is one subject's constitution can gate
    # itself (see pass_open_task_substitution, 2026-08-12). A pass that needs this is, by that
    # fact, not generic — the gate is a declaration, not a convenience.
    ctx = {"summary_items": load_summary_items(args.subject, args.grade, args.chapter),
           "subject": args.subject, "grade": args.grade, "chapter": args.chapter}
    repaired_any = False
    now = datetime.datetime.now().replace(microsecond=0).isoformat()
    stamp = now.replace("-", "").replace(":", "").replace("T", "_")
    refused_any = False

    for path in files:
        doc = json.loads(path.read_text(encoding="utf-8"))
        result = doc["result"]
        by_defect = {}

        for defect, label, fn in ([] if args.declared_only else GENERIC_PASSES):
            edits = fn(result, ctx)
            if edits:
                by_defect.setdefault(defect, {"label": label, "edits": []})["edits"].extend(edits)

        declared, refusals = apply_declared(
            result,
            DECLARED.get((args.subject, args.grade), {}).get(path.name, {}),
            path.name)
        for edit in declared:
            by_defect.setdefault(edit["defect"], {"label": "declared edit", "edits": []})
            by_defect[edit["defect"]]["edits"].append(
                {k: v for k, v in edit.items() if k != "defect"})
        for line in refusals:
            refused_any = True
            print(f"  REFUSED {line}")

        if not by_defect:
            print(f"OK    {path.name} — nothing to repair")
            continue

        summary = ", ".join(f"{d} ×{len(v['edits'])}" for d, v in sorted(by_defect.items()))
        if args.dry_run:
            print(f"WOULD REPAIR {path.name} — {summary}")
            continue

        backup_dir = BACKUP / stamp
        backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(path, backup_dir / path.name)

        doc.setdefault("genon_canonical", {}).setdefault("repairs", []).append({
            "tool": TOOL,
            "at": now,
            "reason": "C3 defect repair (testing.md C3 · S4 mathematics·secondary). Generic "
                      "passes derive their value from the summary, the Pedagogy document or the "
                      "schema; declared edits are hand-written per instance and listed with "
                      "their defect id. No pedagogical content was regenerated: register and "
                      "continuity edits delete or rephrase a clause whose content is already "
                      "named, and word-count edits shorten a label without adding a fact.",
            "defects": {d: {"note": v["label"], "edits": v["edits"]}
                        for d, v in sorted(by_defect.items())},
        })

        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"REPAIRED {path.name} — {summary}")
        repaired_any = True

    if not args.dry_run:
        print(f"\nbackups: backup/c3_repair/{stamp}/")
        # PURGE THE DERIVED PLANS (testing.md C10.2b, ARV-D-034). An in-place repair does not
        # move the cache key, so any served plan built before this run would keep serving
        # pre-repair bytes until something dislodged it — the pilot did exactly that for four
        # hours. Every other repair tool calls this; omitting it here was found at S4's C10.
        if repaired_any:
            purge(args.subject, args.grade, args.chapter,
                  reason=f"{TOOL} — C3 defect repair")
    return 1 if refused_any else 0


if __name__ == "__main__":
    sys.exit(main())
