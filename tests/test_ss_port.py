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
FX_EDGE = os.path.join(os.path.dirname(__file__), "fixtures", "ss_vii_ch04_edge_saved.json")


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


def _edge_lp():
    saved = json.load(open(FX_EDGE))
    ch = {"chapter_number": saved["chapter_number"], "chapter_title": saved["chapter_title"]}
    # full result passed (§3e caller rule)
    return SocialSciencesSubject().lesson_plan_to_view(
        saved["result"], grade=saved["grade"], chapter=ch), saved["result"]


def test_edge_model_flat_unit_group_in_teaching_order():
    """Edge-model plans (competency_edges): ONE flat 'unit' group, plan order preserved —
    competency is an overlay, never a spine (rewrite brief §1)."""
    lp, r = _edge_lp()
    periods = r["lesson_plan"]["periods"]
    assert len(lp.groups) == 1 and lp.groups[0].type == "unit"
    assert lp.groups[0].meta.get("edge_model") is True
    assert [p.number for p in lp.groups[0].periods] == [p["period_number"] for p in periods]


def test_edge_model_edges_carried_and_zero_edge_units_allowed():
    lp, r = _edge_lp()
    vps = lp.groups[0].periods
    raw_ps = r["lesson_plan"]["periods"]
    # edges carried verbatim on Period.meta, count-parity with the raw plan
    for vp, rp in zip(vps, raw_ps):
        edges = vp.meta.get("competency_edges")
        assert isinstance(edges, list) and len(edges) == len(rp.get("competency_edges", []))
        for e in edges:
            assert {"c_code", "implied_lo", "cognitive_demand"} <= set(e)
        # LOs gathered per edge (data for the assessment link, never LP display)
        assert vp.learning_outcomes == [e["implied_lo"] for e in edges]
    # a unit that genuinely realises no competency is allowed (brief §2.5)
    assert any(not vp.meta["competency_edges"] for vp in vps)
    # gap note rides the view meta (empty string when the plan records none)
    assert "competency_gap_note" in lp.meta


if __name__ == "__main__":
    test_registered()
    test_lp_grouped_by_competency_with_weight()
    test_assessment_grouped_by_type_and_clean_render()
    test_edge_model_flat_unit_group_in_teaching_order()
    test_edge_model_edges_carried_and_zero_edge_units_allowed()
    print("OK — Social Sciences port: LP by competency (weights preserved) for old plans, "
          "flat unit group + competency_edges overlay for edge-model plans, assessment by "
          "question type, renders clean.")
