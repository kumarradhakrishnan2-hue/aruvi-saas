"""
Social Sciences subject plugin — the competency-based case (middle stage only).

Organizing axis: COMPETENCY. Each LP period carries a competency {c_code, cg, weight,
competency_text} — the weights drive the Allocate tab. So the lesson plan groups by
competency; the assessment groups by question type (its natural grouping). Both collapse
into the canonical view model through the one renderer.
"""
from __future__ import annotations

from typing import Any, Dict, List, Union

from ..base import Subject  # noqa: F401
from ...link_resolver import stamp
from ...normalize import as_list, band_lines, classify_stimulus, normalize_options
from ...ports import Prompt
from ...view_model import (
    AssessmentGroup, AssessmentItem, AssessmentView, Group, LessonPlanView, Period,
)


class SocialSciencesSubject:
    name = "social_sciences"

    def __init__(self, *, lp_constitution: str = "", assessment_constitution: str = "",
                 pedagogy: str = "") -> None:
        self._lp_const = lp_constitution
        self._assess_const = assessment_constitution
        self._pedagogy = pedagogy

    # ── Prompt assembly ─────────────────────────────────────────────────────────
    def build_lesson_plan_prompt(self, *, grade, chapter, summary, mapping, period_profile) -> Prompt:
        system = ("You are Aruvi's Social Sciences lesson plan generator. The constitution "
                  f"below is binding.\n\n=== SS LP CONSTITUTION ===\n{self._lp_const}\n")
        user = (f"=== PEDAGOGY ===\n{self._pedagogy}\n\n=== CHAPTER SUMMARY ===\n{summary}\n\n"
                f"=== COMPETENCY MAPPING ===\n{mapping}\n\n"
                f"=== TEACHER PERIOD SCHEDULE ===\n{period_profile}\n\n"
                "Each period carries its competency {c_code, weight}. Output a single valid "
                "JSON object with lesson_plan.periods[] and coverage_handoff. Raw JSON only.")
        return Prompt(system=system, messages=[{"role": "user", "content": user}], cache_system=True)

    def build_assessment_prompt(self, *, grade, chapter, summary, mapping, lesson_plan) -> Prompt:
        system = ("You are Aruvi's Social Sciences assessment generator. The constitution below "
                  f"is binding.\n\n=== SS ASSESSMENT CONSTITUTION ===\n{self._assess_const}\n")
        user = (f"=== CHAPTER SUMMARY ===\n{summary}\n\n=== LESSON PLAN (handoff) ===\n{lesson_plan}\n\n"
                "Permitted question types follow the competency weights. Raw JSON only with an "
                "`assessment_items` array.")
        return Prompt(system=system, messages=[{"role": "user", "content": user}], cache_system=True)

    def chapter_weight(self, mapping):
        return float(mapping.get("chapter_weight") or 0)

    def allocation_basis(self, grade):
        return {"basis": "NCF competency weight", "factors": [
            "The NCF competencies each chapter develops",
            "How central each competency is to the chapter",
            "Whether a competency is engaged structurally or only in passing",
        ]}

    # ── Validation ──────────────────────────────────────────────────────────────
    def validate(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        lp = raw.get("lesson_plan", raw)
        if isinstance(lp, dict) and "periods" in lp:
            if not lp["periods"]:
                raise ValueError("SS lesson plan has no periods (possible truncation).")
        elif "assessment_items" in raw:
            if not raw["assessment_items"]:
                raise ValueError("SS assessment has no items.")
        return raw

    # ── Lesson plan → view (grouped by competency) ──────────────────────────────
    def lesson_plan_to_view(self, raw: Dict[str, Any], *, grade, chapter) -> LessonPlanView:
        periods = raw.get("lesson_plan", raw).get("periods", [])
        groups: List[Group] = []
        index: Dict[str, Group] = {}
        for p in periods:
            comp = p.get("competency") or {}
            c_code = comp.get("c_code", "") or "general"
            if c_code not in index:
                label = comp.get("c_code", "General")
                if comp.get("competency_text"):
                    label = f"{label} — {comp['competency_text']}"
                g = Group(type="competency", label=label,
                          meta={"c_code": comp.get("c_code", ""), "cg": comp.get("cg", ""),
                                "weight": comp.get("weight", "")})
                index[c_code] = g
                groups.append(g)
            index[c_code].periods.append(Period(
                number=p.get("period_number", 0),
                title=p.get("activity_title", ""),
                activities=band_lines(p.get("time_bands")),
                learning_outcomes=as_list(p.get("implied_lo")),
                teacher_notes=as_list(p.get("teacher_notes")),
                meta={"section_anchor": p.get("section_anchor", ""),
                      "materials": p.get("materials", ""),
                      "duration_minutes": p.get("period_duration_minutes")},
            ))
        return LessonPlanView(
            subject="social_sciences", grade=grade,
            chapter_number=chapter.get("chapter_number", 0),
            chapter_title=chapter.get("chapter_title", ""),
            total_periods=len(periods), groups=groups,
        )

    # ── Assessment → view (grouped by question type) ────────────────────────────
    def assessment_to_view(self, raw: Union[Dict[str, Any], list], *, grade, chapter,
                           link_context: Dict[str, Any] = None) -> AssessmentView:
        # Rule 3 (item-self-sufficient): the item carries its own `period_ref[]` and inline
        # `implied_lo` — no handoff needed. Stamp those straight onto the uniform contract.
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
                     + as_list(it.get("scaffold")) + as_list(it.get("format_of_output")))
            lo = it.get("implied_lo", "")
            meta = {"weight_label": it.get("weight_label", ""),
                    "chapter_section": it.get("chapter_section", ""),
                    "period_ref": it.get("period_ref", ""),
                    "cognitive_demand": it.get("cognitive_demand", "")}
            stamp(meta, as_list(it.get("period_ref")), lo)
            index[qtype].items.append(AssessmentItem(
                prompt=it.get("question_text") or it.get("task", ""),
                item_type=qtype,
                options=options, answer=answer,
                teacher_guide=guide,
                implied_lo=lo,
                visual_stimulus=classify_stimulus(it.get("visual_stimulus", "")),
                meta=meta,
            ))
        return AssessmentView(
            subject="social_sciences", grade=grade,
            chapter_number=chapter.get("chapter_number", 0),
            chapter_title=chapter.get("chapter_title", ""),
            groups=groups,
        )
