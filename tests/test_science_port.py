"""
Parity test for the Science port.

Loads a REAL prototype output (saved Science VII Ch 02 plan) and runs it through
ScienceSubject's normalizers, asserting the canonical view model preserves the
progression-stage structure, the periods, the assessment grouping, and — crucially —
types the visual stimulus (the litmus pipe-table) as TABLE rather than dumping it as prose.

Run standalone:  python3 tests/test_science_port.py   (also pytest-compatible)
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import aruvi_core.subjects.science  # noqa: E402  (import registers the plugin)
from aruvi_core import subjects  # noqa: E402
from aruvi_core.subjects.science import ScienceSubject  # noqa: E402
from aruvi_core.view_model import StimulusType  # noqa: E402

FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures", "science_vii_ch02_saved.json")


def _load():
    saved = json.load(open(FIXTURE))
    return saved["result"], saved


def test_science_registered():
    assert "science" in subjects.available()
    assert subjects.get("science").name == "science"


def test_lesson_plan_preserves_progression_stages():
    result, saved = _load()
    sub = ScienceSubject()
    chapter = {"chapter_number": saved["chapter_number"], "chapter_title": saved["chapter_title"]}
    lp = sub.lesson_plan_to_view(result["lesson_plan"], grade=saved["grade"], chapter=chapter)

    # All periods preserved
    assert lp.total_periods == len(result["lesson_plan"]["periods"]) == 7
    # Grouped by progression stage, order preserved, no period lost
    assert [g.type for g in lp.groups] == ["progression_stage"] * len(lp.groups)
    assert sum(len(g.periods) for g in lp.groups) == lp.total_periods
    # Stage metadata carried (label + implied LO), not flattened
    assert all(g.label for g in lp.groups)
    assert any(g.meta.get("implied_lo") for g in lp.groups)
    # Stage count matches the cognitive_progression the prototype emitted
    assert len(lp.groups) == len(result["lesson_plan"]["cognitive_progression"])


def test_assessment_groups_and_typed_stimulus():
    result, saved = _load()
    sub = ScienceSubject()
    chapter = {"chapter_number": saved["chapter_number"], "chapter_title": saved["chapter_title"]}
    a = sub.assessment_to_view(result, grade=saved["grade"], chapter=chapter)

    total_items = sum(len(g.items) for g in a.groups)
    assert total_items == len(result["assessment_items"]) == 9
    assert all(g.type == "progression_stage" for g in a.groups)

    # The first item's litmus table must be typed TABLE (not dumped as prose)
    first = a.groups[0].items[0]
    assert first.visual_stimulus.type == StimulusType.TABLE
    assert "|" in first.visual_stimulus.content
    # Per-item implied LO + question type preserved
    assert first.item_type  # e.g. MCQ
    assert first.implied_lo

    # Whole thing serializes to JSON
    json.dumps(a.__dict__, default=lambda o: o.__dict__)


if __name__ == "__main__":
    test_science_registered()
    test_lesson_plan_preserves_progression_stages()
    test_assessment_groups_and_typed_stimulus()
    print("OK — Science port: stages, periods, assessment grouping, and typed stimulus all preserved.")
