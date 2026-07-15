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
from ...assessment_norm import from_constitution
from ...link_resolver import stamp
from ...normalize import as_list, band_lines, classify_stimulus, normalize_options, phases_from
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

    # ── Lesson plan → view ───────────────────────────────────────────────────────
    # TWO plan generations live in the corpus (constitution rewrite, 2026-07-15 —
    # docs/middle_ss_constitution_rewrite_brief.md):
    #   OLD (pre-v3): each period carries ONE `competency` → grouped by contiguous
    #        competency runs (below, unchanged).
    #   EDGE MODEL (v3+): each period carries `competency_edges[]` — zero, one, or many
    #        (unit × competency) edges, each owning one implied LO + cognitive demand.
    #        Competency is no longer a spine (a 3-edge unit would live in three folders;
    #        a 0-edge unit in none), so the view is ONE flat "unit" group in the plan's
    #        own teaching order, with the edges carried on Period.meta. The renderer
    #        (ChapterOrg's SS flow view) draws the unit↔competency graph from those edges.
    def lesson_plan_to_view(self, raw: Dict[str, Any], *, grade, chapter) -> LessonPlanView:
        inner = raw.get("lesson_plan", raw)
        periods = inner.get("periods", [])
        if any("competency_edges" in p for p in periods):
            return self._edge_model_lp(raw, inner, periods, grade=grade, chapter=chapter)
        # Group by CONTIGUOUS RUNS of the same competency, never a first-appearance merge:
        # SS plans interleave competencies (viii ch_04 raw order 1..11 flattened to
        # 1,3,10,2,5,… under the old dict merge), and the flattened Learning-Unit rail —
        # and the POINTER — must follow the plan's own period_number teaching sequence
        # (founder rule 2026-07-14, set on maths secondary; the order is the contract,
        # enforced corpus-wide by tests/test_unit_order.py). A competency the plan returns
        # to later simply appears again as its own group.
        groups: List[Group] = []
        prev_code: Any = object()  # sentinel ≠ any real c_code
        for p in periods:
            comp = p.get("competency") or {}
            c_code = comp.get("c_code", "") or "general"
            if c_code != prev_code:
                label = comp.get("c_code", "General")
                if comp.get("competency_text"):
                    label = f"{label} — {comp['competency_text']}"
                groups.append(Group(type="competency", label=label,
                                    meta={"c_code": comp.get("c_code", ""), "cg": comp.get("cg", ""),
                                          "weight": comp.get("weight", "")}))
                prev_code = c_code
            appr = p.get("pedagogical_approaches")
            approach = self._join_approaches(appr)
            hw = p.get("homework")
            homework = "; ".join(as_list(hw)) if hw else ""
            groups[-1].periods.append(Period(
                number=p.get("period_number", 0),
                title=p.get("activity_title", ""),
                approach=approach,
                activities=band_lines(p.get("time_bands")),
                phases=phases_from(p.get("time_bands")),
                materials=as_list(p.get("materials")),
                learning_outcomes=as_list(p.get("implied_lo")),
                teacher_notes=as_list(p.get("teacher_notes")),
                homework=homework,
                meta={"section_anchor": p.get("section_anchor", ""),
                      "materials": p.get("materials", ""),
                      "pedagogical_approaches": appr or [],
                      "duration_minutes": p.get("period_duration_minutes")},
            ))
        return LessonPlanView(
            subject="social_sciences", grade=grade,
            chapter_number=chapter.get("chapter_number", 0),
            chapter_title=chapter.get("chapter_title", ""),
            total_periods=len(periods), groups=groups,
        )

    # approach (2026-07-15): SS LP constitution v2.7 emits pedagogical_approaches —
    # a list of one-to-few approaches (verbatim from the Pedagogy doc). Join the
    # unique values in order into the canonical Period.approach line. Older SS plans
    # without the field leave approach empty (unchanged behaviour).
    @staticmethod
    def _join_approaches(appr: Any) -> str:
        if isinstance(appr, list):
            seen: List[str] = []
            for a in appr:
                a = str(a or "").strip()
                if a and a not in seen:
                    seen.append(a)
            return "; ".join(seen)
        return str(appr or "").strip()

    def _edge_model_lp(self, raw: Dict[str, Any], inner: Dict[str, Any],
                       periods: List[Dict[str, Any]], *, grade, chapter) -> LessonPlanView:
        """Edge-model plans (competency_edges per period) → ONE flat 'unit' group.

        Teaching order is the contract (tests/test_unit_order.py); competency is an
        OVERLAY carried per-period as meta["competency_edges"] (verbatim edge dicts:
        c_code / cg / weight / competency_text / implied_lo / cognitive_demand).
        Period.learning_outcomes gathers the edges' LOs — carried for the assessment
        link, never displayed in the LP (founder rule 2026-07-09). A unit with no
        edges is taught but generates no LO — by design, never bucketed as 'General'.
        The chapter-level competency_gap_note (brief §2.5) rides LessonPlanView.meta."""
        group = Group(type="unit", label="Units", meta={"edge_model": True})
        for p in periods:
            raw_edges = p.get("competency_edges") or []
            edges = [e for e in raw_edges if isinstance(e, dict)] if isinstance(raw_edges, list) else []
            appr = p.get("pedagogical_approaches")
            hw = p.get("homework")
            group.periods.append(Period(
                number=p.get("period_number", 0),
                title=p.get("activity_title", ""),
                approach=self._join_approaches(appr),
                activities=band_lines(p.get("time_bands")),
                phases=phases_from(p.get("time_bands")),
                materials=as_list(p.get("materials")),
                learning_outcomes=[str(e.get("implied_lo", "")).strip()
                                   for e in edges if e.get("implied_lo")],
                teacher_notes=as_list(p.get("teacher_notes")),
                homework="; ".join(as_list(hw)) if hw else "",
                meta={"section_anchor": p.get("section_anchor", ""),
                      "section_context": p.get("section_context", ""),
                      "materials": p.get("materials", ""),
                      "pedagogical_approaches": appr or [],
                      "inclusivity": p.get("inclusivity", ""),
                      "competency_edges": edges,
                      "duration_minutes": p.get("period_duration_minutes")},
            ))
        gap = str(inner.get("competency_gap_note")
                  or raw.get("competency_gap_note") or "").strip()
        return LessonPlanView(
            subject="social_sciences", grade=grade,
            chapter_number=chapter.get("chapter_number", 0),
            chapter_title=chapter.get("chapter_title", ""),
            total_periods=len(periods), groups=[group],
            meta={"competency_gap_note": gap, "edge_model": True},
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
                normalized=from_constitution(it, meta),  # the §2 uniform contract (3b reads this)
            ))
        return AssessmentView(
            subject="social_sciences", grade=grade,
            chapter_number=chapter.get("chapter_number", 0),
            chapter_title=chapter.get("chapter_title", ""),
            groups=groups,
        )
