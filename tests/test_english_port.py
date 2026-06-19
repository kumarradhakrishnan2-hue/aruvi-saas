"""
Parity test for the English port — the two-axis (section x spine) stress test.

Loads a REAL prototype output (saved English VII Ch 01) and asserts the canonical view
model preserves BOTH axes: outer `section` Groups each containing inner `spine` Groups,
with every period placed and none lost; and the spine-grouped assessment preserved intact.
If the "one renderer, many subjects" thesis were going to break anywhere, it's here.

Run standalone:  python3 tests/test_english_port.py   (also pytest-compatible)
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import aruvi_core.subjects.english  # noqa: E402  (registers the plugin)
from aruvi_core import subjects  # noqa: E402
from aruvi_core.subjects.english import EnglishSubject  # noqa: E402

FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures", "english_vii_ch01_saved.json")


def _load():
    saved = json.load(open(FIXTURE))
    return saved["result"], saved


def test_english_registered():
    assert "english" in subjects.available()


def test_lesson_plan_preserves_two_axes():
    result, saved = _load()
    sub = EnglishSubject()
    chapter = {"chapter_number": saved["chapter_number"], "chapter_title": saved["chapter_title"]}
    lp = sub.lesson_plan_to_view(result["lesson_plan"], grade=saved["grade"], chapter=chapter)

    raw_periods = result["lesson_plan"]["periods"]
    assert lp.total_periods == len(raw_periods) == 11

    # Outer axis = sections; every top-level group is a section
    assert lp.groups and all(g.type == "section" for g in lp.groups)
    assert len(lp.groups) == len({p.get("section_id") for p in raw_periods})  # 3 sections

    # Inner axis = spines; every section has spine children, and no period is lost
    placed = 0
    for sec in lp.groups:
        assert sec.children and all(sp.type == "spine" for sp in sec.children)
        for sp in sec.children:
            placed += len(sp.periods)
    assert placed == lp.total_periods  # 11 periods all placed in a section->spine cell


def test_assessment_grouped_by_spine():
    result, saved = _load()
    sub = EnglishSubject()
    chapter = {"chapter_number": saved["chapter_number"], "chapter_title": saved["chapter_title"]}
    a = sub.assessment_to_view(result, grade=saved["grade"], chapter=chapter)

    raw_groups = result["assessment_items"]
    assert len(a.groups) == len(raw_groups) == 6
    assert all(g.type == "spine" for g in a.groups)
    total = sum(len(g.items) for g in a.groups)
    assert total == sum(len(g["items"]) for g in raw_groups) == 14
    # implied LO (source_lo) carried per item
    assert any(it.implied_lo for g in a.groups for it in g.items)

    json.dumps(a.__dict__, default=lambda o: o.__dict__)


def test_contamination_strip():
    # tasks_verbatim / question_bank must be removed from summary before prompting (MEMORY #26)
    sub = EnglishSubject()
    dirty = {"section": {"question_bank": [1, 2], "tasks_verbatim": ["x"], "prose": "keep me"}}
    clean = sub._strip_contamination(dirty)
    assert "question_bank" not in clean["section"]
    assert "tasks_verbatim" not in clean["section"]
    assert clean["section"]["prose"] == "keep me"
    assert "question_bank" in dirty["section"]  # original untouched (deep-copied)


if __name__ == "__main__":
    test_english_registered()
    test_lesson_plan_preserves_two_axes()
    test_assessment_grouped_by_spine()
    test_contamination_strip()
    print("OK — English port: section->spine nesting, all 11 periods placed, "
          "6 spine assessment groups, contamination strip all preserved.")
