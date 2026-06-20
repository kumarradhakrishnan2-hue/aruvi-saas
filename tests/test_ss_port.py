"""
Parity test for the Social Sciences port — the competency-based case.

Loads a real saved SS plan and asserts the LP groups by COMPETENCY (carrying weight) and
the assessment groups by question type, all through the canonical view model + one renderer.

Run standalone:  python3 tests/test_ss_port.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import aruvi_core.subjects.social_sciences  # noqa: E402  (register)
from aruvi_core import subjects  # noqa: E402
from aruvi_core.render import render_view_fragment  # noqa: E402
from aruvi_core.subjects.social_sciences import SocialSciencesSubject  # noqa: E402
from aruvi_core.view_model import ViewModel  # noqa: E402

FX = os.path.join(os.path.dirname(__file__), "fixtures", "ss_vi_ch06_saved.json")


def _vm():
    saved = json.load(open(FX))
    r = saved["result"]
    ch = {"chapter_number": saved["chapter_number"], "chapter_title": saved["chapter_title"]}
    sub = SocialSciencesSubject()
    lp = sub.lesson_plan_to_view(r["lesson_plan"], grade=saved["grade"], chapter=ch)
    a = sub.assessment_to_view(r["assessment_items"], grade=saved["grade"], chapter=ch)
    return ViewModel(lp, a), r


def test_registered():
    assert "social_sciences" in subjects.available()


def test_lp_grouped_by_competency_with_weight():
    vm, r = _vm()
    assert vm.lesson_plan.total_periods == len(r["lesson_plan"]["periods"]) == 7
    assert vm.lesson_plan.groups and all(g.type == "competency" for g in vm.lesson_plan.groups)
    # weight (the allocation driver) is carried, not dropped
    assert any(g.meta.get("weight") for g in vm.lesson_plan.groups)
    assert sum(len(g.periods) for g in vm.lesson_plan.groups) == vm.lesson_plan.total_periods


def test_assessment_grouped_by_type_and_clean_render():
    vm, r = _vm()
    assert sum(len(g.items) for g in vm.assessment.groups) == len(r["assessment_items"]) == 16
    assert all(g.type == "question_type" for g in vm.assessment.groups)
    html = render_view_fragment(vm)
    assert "is_correct" not in html and "'minutes'" not in html
    assert 'grp-type">competency' in html


if __name__ == "__main__":
    test_registered()
    test_lp_grouped_by_competency_with_weight()
    test_assessment_grouped_by_type_and_clean_render()
    print("OK — Social Sciences port: LP by competency (weights preserved), assessment by "
          "question type, renders clean.")
