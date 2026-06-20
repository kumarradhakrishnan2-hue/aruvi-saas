"""
Parity test for the Mathematics port — the stage-split subject.

ONE plugin, stage derived from grade, must produce the right structure for BOTH:
- MIDDLE (grade vi): LP grouped by textbook section; assessment in A/B/C section groups.
- SECONDARY (grade ix): LP grouped by section_anchor; assessment grouped by section, each
  carrying its implied LO.
Both render through the one renderer, with no leaked dicts.

Run standalone:  python3 tests/test_maths_port.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import aruvi_core.subjects.mathematics  # noqa: E402  (register)
from aruvi_core import subjects  # noqa: E402
from aruvi_core.grades import stage_for  # noqa: E402
from aruvi_core.render import render_view_fragment  # noqa: E402
from aruvi_core.subjects.mathematics import MathematicsSubject  # noqa: E402
from aruvi_core.view_model import ViewModel  # noqa: E402

FX = os.path.join(os.path.dirname(__file__), "fixtures")


def _vm(fixture):
    saved = json.load(open(os.path.join(FX, fixture)))
    r = saved["result"]
    ch = {"chapter_number": saved["chapter_number"], "chapter_title": saved["chapter_title"]}
    sub = MathematicsSubject()
    lp = sub.lesson_plan_to_view(r["lesson_plan"], grade=saved["grade"], chapter=ch)
    a = sub.assessment_to_view(r["assessment_items"], grade=saved["grade"], chapter=ch)
    return ViewModel(lp, a), r, saved


def test_registered_and_stage_derivation():
    assert "mathematics" in subjects.available()
    assert stage_for("vi") == "middle" and stage_for("ix") == "secondary"


def test_middle_abc_assessment_and_periods():
    vm, r, saved = _vm("maths_vi_ch05_saved.json")
    assert vm.lesson_plan.total_periods == len(r["lesson_plan"]["periods"]) == 10
    # A/B/C sections preserved
    labels = [g.label for g in vm.assessment.groups]
    assert len(labels) == 3 and all(l.startswith("Section ") for l in labels)
    total_items = sum(len(g.items) for g in vm.assessment.groups)
    assert total_items == sum(len(g["items"]) for g in r["assessment_items"])


def test_secondary_section_wise_implied_lo():
    vm, r, saved = _vm("maths_ix_ch02_saved.json")
    assert vm.lesson_plan.total_periods == len(r["lesson_plan"]["periods"]) == 10
    # LP grouped by section_anchor (2.1, 2.2, …)
    assert vm.lesson_plan.groups[0].meta.get("section_anchor")
    # assessment grouped by section, each carrying an implied LO
    qs = r["assessment_items"]["questions"]
    assert sum(len(g.items) for g in vm.assessment.groups) == len(qs)
    assert any(g.meta.get("implied_lo") for g in vm.assessment.groups)
    assert any(it.implied_lo for g in vm.assessment.groups for it in g.items)


def test_both_render_clean():
    for fx in ("maths_vi_ch05_saved.json", "maths_ix_ch02_saved.json"):
        html = render_view_fragment(_vm(fx)[0])
        assert "is_correct" not in html       # options clean
        assert "'minutes'" not in html        # time bands / phases not dumped as dicts
        assert 'grp-type">section' in html


if __name__ == "__main__":
    test_registered_and_stage_derivation()
    test_middle_abc_assessment_and_periods()
    test_secondary_section_wise_implied_lo()
    test_both_render_clean()
    print("OK — Mathematics port: one plugin, stage from grade; middle A/B/C and secondary "
          "section-wise implied-LO both preserved and render clean.")
