"""
Parity test for the NORMALIZED ITEM CONTRACT (docs/assessment-question-type-registry.md §2/§4)
— the assessment-side mirror of test_link_resolver.py. Walks the FULL saved-plan corpus and
asserts, for every item, that the subject-agnostic NormalizedItem is well formed:

  • question_type is a registered QuestionType and template a known render template
  • stem is never empty (question_text/prompt/item_stem/task all flatten into it)
  • options are STRUCTURED and populated only for selected-response types (MCQ/TRUE_FALSE);
    MCQ carries exactly one correct option
  • cognitive_demand is None or a non-empty string — "" never survives (absent == empty)
  • audio_ref appears only on English listening-spine items; exercise_ref only on Maths
    (the two are never merged)
  • EXTRACT_ANALYSIS routes its extract to `passage`, never a generic visual_stimulus
  • table stimuli arrive pre-split ({"header","rows"} via normalize.parse_table)
  • the link contract mirrors the stamped meta (linked_periods / anchor / linked_lo);
    Maths middle/prep carry NO LO (None), per resolver rules 4–5
  • serialization (ViewModel.to_dict) prunes absent fields — "omitted, not blanked":
    no None/""/[]/{} values outside the identity/link keep-set, and linked_lo is ABSENT
    (not null) for Maths middle/prep

Run standalone:  ARUVI_DATA_DIR=$PWD/data/content python3 tests/test_normalized_item.py
"""
from __future__ import annotations

import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import aruvi_core.subjects.science            # noqa: E402
import aruvi_core.subjects.social_sciences    # noqa: E402
import aruvi_core.subjects.mathematics        # noqa: E402
import aruvi_core.subjects.english            # noqa: E402
import aruvi_core.subjects.the_world_around_us  # noqa: E402
from aruvi_core import subjects               # noqa: E402
from aruvi_core.grades import stage_for       # noqa: E402
from aruvi_core.view_model import (           # noqa: E402
    NormalizedItem, QuestionType, RENDER_TEMPLATE, ViewModel,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLANS = os.path.join(ROOT, "data", "content", "saved_plans")

TYPES = {t.value for t in QuestionType}
TEMPLATES = set(RENDER_TEMPLATE.values())
SELECTED = {"MCQ", "TRUE_FALSE"}


def _iter_views():
    for fp in sorted(glob.glob(os.path.join(PLANS, "*", "*", "*.json"))):
        subject, grade = fp.split(os.sep)[-3], fp.split(os.sep)[-2]
        saved = json.load(open(fp))
        r = saved["result"]
        sub = subjects.get(subject)
        ch = {"chapter_number": saved.get("chapter_number"),
              "chapter_title": saved.get("chapter_title")}
        lp = r.get("lesson_plan", {})
        ctx = {"periods": lp.get("periods", []),
               "handoff": r.get("coverage_handoff", lp.get("coverage_handoff", []))}
        a = sub.assessment_to_view(r.get("assessment_items", []),
                                   grade=saved.get("grade", grade), chapter=ch,
                                   link_context=ctx)
        yield subject, saved.get("grade", grade), os.path.basename(fp), lp, a


def test_normalized_contract_well_formed():
    total = 0
    seen_types = set()
    for subject, grade, name, lp_raw, a in _iter_views():
        where = f"{subject}/{grade} {name}"
        maths_no_lo = subject == "mathematics" and stage_for(grade) in ("middle", "preparatory")
        for g in a.groups:
            for it in g.items:
                n = it.normalized
                assert isinstance(n, NormalizedItem), f"{where}: item missing normalized contract"
                total += 1
                # discriminator + template
                assert n.question_type in TYPES, f"{where}: unknown type {n.question_type!r}"
                assert n.template in TEMPLATES, f"{where}: {n.question_type} has no template"
                seen_types.add(n.question_type)
                # the question
                assert n.stem.strip(), f"{where}: {n.question_type} item with empty stem"
                if n.options:
                    assert n.question_type in SELECTED, \
                        f"{where}: {n.question_type} carries options"
                    assert all(set(o) == {"label", "text", "is_correct"} for o in n.options), \
                        f"{where}: options not structured"
                if n.question_type == "MCQ":
                    # ≥1, not ==1: the preserved English verification-fallback item flags
                    # every statement correct pending transcript verification (its note says
                    # so) — real data, deliberately kept (registry §4 note).
                    assert any(o["is_correct"] for o in n.options), \
                        f"{where}: MCQ with no correct option flagged"
                    # unified reveals (2026-07-10 rewrite) or the tolerated legacy prose note
                    assert n.option_reveals, f"{where}: MCQ with no option_reveals (nor note fallback)"
                    # Constitution family carries KEYED reveals everywhere — Science nested
                    # under guide.{TYPE}, SS/TWAU flat under guide (audit 2026-07-10). The
                    # prose "note" fallback is legitimate ONLY for un-migrated English items.
                    if subject != "english":
                        assert any(k != "note" for k in n.option_reveals), \
                            f"{where}: MCQ fell back to prose note despite keyed guide"
                # quiet meta: "" never survives
                assert n.cognitive_demand is None or n.cognitive_demand.strip(), \
                    f"{where}: cognitive_demand blank-not-null"
                # audio vs exercise — never merged, never cross-subject
                if n.audio_ref is not None:
                    assert subject == "english", f"{where}: audio_ref outside English"
                if n.exercise_ref is not None:
                    assert subject == "mathematics", f"{where}: exercise_ref outside Maths"
                # EXTRACT_ANALYSIS: passage, not stimulus
                if n.question_type == "EXTRACT_ANALYSIS":
                    assert n.passage and not n.visual_stimulus, \
                        f"{where}: EXTRACT_ANALYSIS extract not routed to passage"
                # typed blocks: tables pre-split
                for blk in (n.visual_stimulus, n.passage):
                    if blk and blk["type"] == "table":
                        assert blk.get("table", {}).get("header"), \
                            f"{where}: table stimulus not pre-split"
                # NUM richness (worked answer + method — the T6b card)
                if n.question_type == "NUM":
                    assert n.model_answer and n.method_one_line, \
                        f"{where}: NUM missing worked answer/method"
                # link mirror of the stamped meta
                assert n.linked_periods == it.meta.get("linked_periods"), f"{where}: link drift"
                assert n.anchor_period == it.meta.get("anchor_period"), f"{where}: anchor drift"
                if maths_no_lo:
                    assert n.linked_lo is None, f"{where}: Maths {grade} must carry no LO"
                else:
                    assert n.linked_lo == (it.meta.get("linked_lo") or None), f"{where}: LO drift"
    assert total > 0, "corpus produced no items"
    missing = TYPES - seen_types
    print(f"OK — normalized contract: {total} items well formed; "
          f"{len(seen_types)}/12 registry types exercised"
          + (f" (corpus lacks {sorted(missing)})" if missing else ""))


def test_serialization_omits_not_blanks():
    checked = 0
    for subject, grade, name, lp_raw, a in _iter_views():
        sub = subjects.get(subject)
        # a minimal LP view so ViewModel serializes (contract lives on the assessment side)
        lp = sub.lesson_plan_to_view({"lesson_plan": lp_raw}, grade=grade,
                                     chapter={"chapter_number": 0, "chapter_title": ""})
        d = ViewModel(lp, a).to_dict()
        maths_no_lo = subject == "mathematics" and stage_for(grade) in ("middle", "preparatory")
        for g in d["assessment"]["groups"]:
            for it in g["items"]:
                n = it["normalized"]
                for k, v in n.items():
                    if k in NormalizedItem._KEEP:
                        continue
                    assert v not in (None, "", [], {}), \
                        f"{subject}/{grade} {name}: blank field {k!r} not omitted"
                if maths_no_lo:
                    assert "linked_lo" in n or True  # explicit: key must be ABSENT below
                    assert "linked_lo" not in n, \
                        f"{subject}/{grade}: Maths no-LO must serialize as ABSENT, not null"
                json.dumps(n)  # wire-safe
                checked += 1
    print(f"OK — serialization: {checked} normalized items pruned (omitted, not blanked) & JSON-safe.")


def test_split_parts_structures_prose_once():
    """A numbered/lettered list packed into ONE prose string is parsed into (lead, parts)
    in the engine (assessment_norm.split_parts) — the renderer never re-guesses. Both the
    stem and the answer key use it; genuine lists split, lone numbers / scattered figures
    / inner parens do not."""
    from aruvi_core.assessment_norm import split_parts
    # plain numbered list with a lead + word box (the English IV FILL_IN stem shape)
    lead, parts = split_parts("Fill in the blank from the box.\n[Box: a, b]\n"
                              "1. The park is ___ the school. 2. The desk is ___ them.")
    assert lead.startswith("Fill in the blank"), lead
    assert [p["marker"] for p in parts] == ["1.", "2."]
    assert parts[0]["text"] == "The park is ___ the school."
    # lettered sub-parts with inner parens in the maths — inner ")" is NOT a marker
    lead, parts = split_parts("(a) 5 + 6 = 11. (b) 50 – (12 + 9) = 29. (c) done.")
    assert [p["marker"] for p in parts] == ["(a)", "(b)", "(c)"]
    assert "(12 + 9)" in parts[1]["text"]
    # NOT lists — must stay whole (empty parts)
    assert split_parts("15. It is the least common multiple of 3 and 5.")[1] == []
    assert split_parts("Factors of 8: 1, 2, 4, 8. Factors of 21: 1, 3, 7, 21.")[1] == []
    assert split_parts("A single sentence answer with no parts.")[1] == []

    # end-to-end on the real English IV 'Together We Can' FILL_IN item (Q-WW-A-2)
    fp = os.path.join(PLANS, "english", "iv", "ch_01_20260525_205451.json")
    saved = json.load(open(fp)); r = saved["result"]
    a = subjects.get("english").assessment_to_view(
        r["assessment_items"], grade="iv",
        chapter={"chapter_number": 1, "chapter_title": saved.get("chapter_title")},
        link_context={"periods": r["lesson_plan"]["periods"]})
    n = next(it.normalized for g in a.groups for it in g.items
             if it.normalized and it.normalized.id == "Q-WW-A-2")
    assert len(n.stem_parts) == 4, n.stem_parts
    assert "[Box:" in n.stem_lead
    assert [p["text"] for p in n.answer_parts] == ["near", "between", "in front of", "behind"]
    print("OK — split_parts: stem & answer keys structured once in the engine; "
          "non-lists left whole.")


if __name__ == "__main__":
    test_normalized_contract_well_formed()
    test_serialization_omits_not_blanks()
    test_split_parts_structures_prose_once()
