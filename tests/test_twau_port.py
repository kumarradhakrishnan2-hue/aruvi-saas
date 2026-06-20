"""
Parity test for The World Around Us (TWAU) port — single-axis section grouping.

Run standalone:  python3 tests/test_twau_port.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import aruvi_core.subjects.the_world_around_us  # noqa: E402  (register)
from aruvi_core import subjects  # noqa: E402
from aruvi_core.render import render_view_fragment  # noqa: E402
from aruvi_core.subjects.the_world_around_us import TheWorldAroundUsSubject  # noqa: E402
from aruvi_core.view_model import ViewModel  # noqa: E402

FX = os.path.join(os.path.dirname(__file__), "fixtures", "twau_iii_ch01_saved.json")


def _vm():
    saved = json.load(open(FX))
    r = saved["result"]
    ch = {"chapter_number": saved["chapter_number"], "chapter_title": saved["chapter_title"]}
    sub = TheWorldAroundUsSubject()
    lp = sub.lesson_plan_to_view(r["lesson_plan"], grade=saved["grade"], chapter=ch)
    a = sub.assessment_to_view(r["assessment_items"], grade=saved["grade"], chapter=ch)
    return ViewModel(lp, a), r


def test_registered_and_section_grouping():
    vm, r = _vm()
    assert "the_world_around_us" in subjects.available()
    assert vm.lesson_plan.total_periods == len(r["lesson_plan"]["periods"]) == 7
    assert vm.lesson_plan.groups and all(g.type == "section" for g in vm.lesson_plan.groups)
    assert sum(len(g.periods) for g in vm.lesson_plan.groups) == vm.lesson_plan.total_periods
    # dominant_mode (activity-type label) carried per period
    assert any(p.meta.get("dominant_mode") for g in vm.lesson_plan.groups for p in g.periods)


def test_assessment_and_clean_render():
    vm, r = _vm()
    assert sum(len(g.items) for g in vm.assessment.groups) == len(r["assessment_items"]) == 7
    html = render_view_fragment(vm)
    assert "is_correct" not in html and "'minutes'" not in html


if __name__ == "__main__":
    test_registered_and_section_grouping()
    test_assessment_and_clean_render()
    print("OK — TWAU port: section-grouped LP (dominant_mode preserved), assessment by type, "
          "renders clean.")
