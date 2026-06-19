"""
Guardrail test: the canonical view model is structure-PRESERVING.

Each of the five organizing structures developed iteratively in the prototype must be
expressible without flattening — and the whole thing must serialize to JSON. This is the
acceptance shape; when real subjects are ported, their prototype outputs become the parity
fixtures checked against this same contract.

Run standalone:  python3 tests/test_view_model.py     (also pytest-compatible)
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aruvi_core.view_model import (  # noqa: E402
    AssessmentGroup, AssessmentItem, AssessmentView, Group, LessonPlanView,
    Period, StimulusType, ViewModel, VisualStimulus,
)


def _english_lesson_plan() -> LessonPlanView:
    # Two nested axes: section -> spine. The distinction must survive as nesting.
    return LessonPlanView(
        subject="english", grade="vii", chapter_number=1,
        chapter_title="Learning Together", total_periods=4,
        groups=[Group(type="section", label="The Kite (prose)", children=[
            Group(type="spine", label="Reading for Comprehension",
                  periods=[Period(number=1, title="Close reading")]),
            Group(type="spine", label="Listening",
                  periods=[Period(number=2, title="Listen and respond")]),
        ])],
    )


def _social_science_lesson_plan() -> LessonPlanView:
    # Competency-based grouping; weight + c_code preserved in meta.
    return LessonPlanView(
        subject="social_sciences", grade="vii", chapter_number=2,
        chapter_title="Understanding the Weather", total_periods=3,
        groups=[Group(type="competency", label="C-2.1 Analyses diversity",
                      meta={"c_code": "C-2.1", "weight": 3},
                      periods=[Period(number=1, title="Mapping climate zones")])],
    )


def _science_lesson_plan() -> LessonPlanView:
    # Progression-stage grouping.
    return LessonPlanView(
        subject="science", grade="vii", chapter_number=2,
        chapter_title="Acids and Bases", total_periods=2,
        groups=[Group(type="progression_stage", label="Stage 1: Observe",
                      meta={"stage_index": 1},
                      periods=[Period(number=1, title="Indicators")])],
    )


def _maths_middle_assessment() -> AssessmentView:
    # A/B/C sections.
    return AssessmentView(
        subject="mathematics", grade="vii", chapter_number=5, chapter_title="Prime Time",
        groups=[
            AssessmentGroup(type="section", label="Section A",
                            items=[AssessmentItem(prompt="2^4 x 5^4 = ?", item_type="MCQ",
                                                  options=["10000", "20"], answer="10000")]),
            AssessmentGroup(type="section", label="Section B",
                            items=[AssessmentItem(prompt="Explain co-primes.", item_type="OPEN_TASK")]),
            AssessmentGroup(type="section", label="Section C",
                            items=[AssessmentItem(prompt="Investigate factor trees.", item_type="OPEN_TASK")]),
        ],
    )


def _maths_secondary_assessment() -> AssessmentView:
    # Section-wise, each carrying its implied LO in meta; an SVG stimulus typed (not raw text).
    return AssessmentView(
        subject="mathematics", grade="ix", chapter_number=1, chapter_title="Coordinates",
        groups=[AssessmentGroup(
            type="section", label="Locating Points",
            meta={"implied_lo": "Locates and plots points on the Cartesian plane"},
            items=[AssessmentItem(
                prompt="Plot (3, -2).", item_type="OPEN_TASK",
                visual_stimulus=VisualStimulus(type=StimulusType.SVG, content="<svg>...</svg>"),
            )],
        )],
    )


def test_structures_are_preserved_and_serializable():
    cases = {
        "english_nested": ViewModel(_english_lesson_plan(),
                                    AssessmentView("english", "vii", 1, "Learning Together")),
        "ss_competency": ViewModel(_social_science_lesson_plan(),
                                   AssessmentView("social_sciences", "vii", 2, "Weather")),
        "science_stage": ViewModel(_science_lesson_plan(),
                                   AssessmentView("science", "vii", 2, "Acids and Bases")),
        "maths_middle_abc": ViewModel(LessonPlanView("mathematics", "vii", 5, "Prime Time"),
                                      _maths_middle_assessment()),
        "maths_secondary_lo": ViewModel(LessonPlanView("mathematics", "ix", 1, "Coordinates"),
                                        _maths_secondary_assessment()),
    }
    for name, vm in cases.items():
        d = vm.to_dict()
        json.dumps(d)  # must be JSON-serializable (str-Enum included)

    # English keeps its two-axis nesting
    eng = cases["english_nested"].to_dict()["lesson_plan"]["groups"][0]
    assert eng["type"] == "section"
    assert eng["children"][0]["type"] == "spine"

    # SS keeps competency weight/c_code
    ss = cases["ss_competency"].to_dict()["lesson_plan"]["groups"][0]
    assert ss["type"] == "competency" and ss["meta"]["weight"] == 3

    # Science keeps progression stage
    assert cases["science_stage"].to_dict()["lesson_plan"]["groups"][0]["type"] == "progression_stage"

    # Maths-middle keeps A/B/C sections distinct
    mm = cases["maths_middle_abc"].to_dict()["assessment"]["groups"]
    assert [g["label"] for g in mm] == ["Section A", "Section B", "Section C"]

    # Maths-secondary keeps per-section implied LO + typed SVG (not raw text dumped as prose)
    ms = cases["maths_secondary_lo"].to_dict()["assessment"]["groups"][0]
    assert ms["meta"]["implied_lo"].startswith("Locates")
    assert ms["items"][0]["visual_stimulus"]["type"] == "svg"


if __name__ == "__main__":
    test_structures_are_preserved_and_serializable()
    print("OK — all 5 subject structures preserved and JSON-serializable.")
