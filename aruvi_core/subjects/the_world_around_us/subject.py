"""
The World Around Us (TWAU) subject plugin — preparatory stage only.

Single organizing axis: SECTION (`section_ref`), with a per-period `dominant_mode`
activity-type label (Explore/Discuss/Create etc.). Assessment groups by question type and
supports the performance_task variant. Collapses into the canonical view model like the rest.
"""
from __future__ import annotations

from typing import Any, Dict, List, Union

from ..base import Subject  # noqa: F401
from ...normalize import as_list, band_lines, classify_stimulus, normalize_options
from ...ports import Prompt
from ...view_model import (
    AssessmentGroup, AssessmentItem, AssessmentView, Group, LessonPlanView, Period,
)


class TheWorldAroundUsSubject:
    name = "the_world_around_us"

    def __init__(self, *, lp_constitution: str = "", assessment_constitution: str = "",
                 pedagogy: str = "") -> None:
        self._lp_const = lp_constitution
        self._assess_const = assessment_constitution
        self._pedagogy = pedagogy

    # ── Prompt assembly ─────────────────────────────────────────────────────────
    def build_lesson_plan_prompt(self, *, grade, chapter, summary, mapping, period_profile) -> Prompt:
        system = ("You are Aruvi's TWAU lesson plan generator. The constitution below is "
                  f"binding.\n\n=== TWAU LP CONSTITUTION ===\n{self._lp_const}\n")
        user = (f"=== PEDAGOGY ===\n{self._pedagogy}\n\n=== CHAPTER SUMMARY ===\n{summary}\n\n"
                f"=== MAPPING ===\n{mapping}\n\n=== TEACHER PERIOD SCHEDULE ===\n{period_profile}\n\n"
                "Walk sections; each period carries section_ref and a dominant_mode. Output a "
                "single valid JSON object with lesson_plan.periods[] and coverage_handoff. Raw JSON only.")
        return Prompt(system=system, messages=[{"role": "user", "content": user}], cache_system=True)

    def build_assessment_prompt(self, *, grade, chapter, summary, mapping, lesson_plan) -> Prompt:
        system = ("You are Aruvi's TWAU assessment generator. The constitution below is binding.\n\n"
                  f"=== TWAU ASSESSMENT CONSTITUTION ===\n{self._assess_const}\n")
        user = (f"=== CHAPTER SUMMARY ===\n{summary}\n\n=== LESSON PLAN (handoff) ===\n{lesson_plan}\n\n"
                "Raw JSON only with an `assessment_items` array.")
        return Prompt(system=system, messages=[{"role": "user", "content": user}], cache_system=True)

    # ── Validation ──────────────────────────────────────────────────────────────
    def validate(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        lp = raw.get("lesson_plan", raw)
        if isinstance(lp, dict) and "periods" in lp:
            if not lp["periods"]:
                raise ValueError("TWAU lesson plan has no periods (possible truncation).")
        elif "assessment_items" in raw:
            if not raw["assessment_items"]:
                raise ValueError("TWAU assessment has no items.")
        return raw

    # ── Lesson plan → view (grouped by section) ─────────────────────────────────
    def lesson_plan_to_view(self, raw: Dict[str, Any], *, grade, chapter) -> LessonPlanView:
        periods = raw.get("lesson_plan", raw).get("periods", [])
        groups: List[Group] = []
        index: Dict[str, Group] = {}
        for p in periods:
            sec = str(p.get("section_ref", "")) or "Section"
            if sec not in index:
                g = Group(type="section", label=sec, meta={"section_ref": sec})
                index[sec] = g
                groups.append(g)
            index[sec].periods.append(Period(
                number=p.get("period_number", 0),
                title=p.get("activity_title", ""),
                activities=band_lines(p.get("time_bands")),
                learning_outcomes=as_list(p.get("implied_lo")),
                teacher_notes=as_list(p.get("teacher_facilitation_note")),
                meta={"dominant_mode": p.get("dominant_mode", ""),
                      "textbook_anchor": p.get("textbook_anchor", ""),
                      "section_context": p.get("section_context", ""),
                      "materials": p.get("materials", ""),
                      "duration_minutes": p.get("period_duration_minutes")},
            ))
        return LessonPlanView(
            subject="the_world_around_us", grade=grade,
            chapter_number=chapter.get("chapter_number", 0),
            chapter_title=chapter.get("chapter_title", ""),
            total_periods=len(periods), groups=groups,
        )

    # ── Assessment → view (grouped by question type) ────────────────────────────
    def assessment_to_view(self, raw: Union[Dict[str, Any], list], *, grade, chapter) -> AssessmentView:
        items = raw.get("assessment_items", raw) if isinstance(raw, dict) else raw
        groups: List[AssessmentGroup] = []
        index: Dict[str, AssessmentGroup] = {}
        for it in items or []:
            qtype = it.get("question_type", "") or "ITEM"
            if qtype not in index:
                g = AssessmentGroup(type="question_type", label=qtype, meta={})
                index[qtype] = g
                groups.append(g)
            options, answer = normalize_options(it.get("options"))
            guide = (as_list(it.get("look_for")) + as_list(it.get("expected_elements"))
                     + as_list(it.get("scaffold")) + as_list(it.get("format_of_output"))
                     + as_list(it.get("guide")))
            index[qtype].items.append(AssessmentItem(
                prompt=it.get("question_text") or it.get("task", ""),
                item_type=qtype,
                options=options, answer=answer,
                teacher_guide=guide,
                implied_lo=it.get("implied_lo", ""),
                visual_stimulus=classify_stimulus(it.get("visual_stimulus", "")),
                meta={"competency": it.get("competency", {}),
                      "cognitive_demand": it.get("cognitive_demand", ""),
                      "performance_task": it.get("performance_task", ""),
                      "period_ref": it.get("period_ref", "")},
            ))
        return AssessmentView(
            subject="the_world_around_us", grade=grade,
            chapter_number=chapter.get("chapter_number", 0),
            chapter_title=chapter.get("chapter_title", ""),
            groups=groups,
        )
