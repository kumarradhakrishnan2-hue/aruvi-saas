"""
Mathematics subject plugin — the stage-split case.

Stage is derived from grade (never passed in). Middle and secondary genuinely differ:
  MIDDLE    LP walks textbook_segments (5.1, 5.2…) with a per-period section_goal;
            assessment is A/B/C section groups.
  SECONDARY LP groups by section_anchor (2.1–2.6);
            assessment is a dict of questions[], each carrying its section's implied_lo.

Both collapse into the SAME canonical view model (section-type Groups), so the one renderer
handles both — the structural difference lives here, in the translator, not in the renderer.
"""
from __future__ import annotations

from typing import Any, Dict, List, Union

from ..base import Subject  # noqa: F401
from ...grades import stage_for
from ...link_resolver import (
    handoff_period_index, norm_code, period_field_index, stamp,
)
from ...normalize import as_list, band_lines, classify_stimulus, normalize_options, text_lines
from ...ports import Prompt
from ...view_model import (
    AssessmentGroup, AssessmentItem, AssessmentView, Group, LessonPlanView, Period,
)


def _hw(v: Any) -> str:
    if isinstance(v, list):
        return "; ".join(text_lines(v))
    return v or ""


class MathematicsSubject:
    name = "mathematics"

    def __init__(self, *, constitutions: Dict[str, Dict[str, str]] = None, pedagogy: str = "") -> None:
        # constitutions[stage] = {"lp": "...", "assessment": "..."}
        self._const = constitutions or {}
        self._pedagogy = pedagogy

    # ── Prompt assembly (stage-aware) ───────────────────────────────────────────
    def build_lesson_plan_prompt(self, *, grade, chapter, summary, mapping, period_profile) -> Prompt:
        stage = stage_for(grade)
        lp_const = self._const.get(stage, {}).get("lp", "")
        system = ("You are Aruvi's Mathematics lesson plan generator. The constitution below "
                  f"is binding.\n\n=== MATHS LP CONSTITUTION ({stage}) ===\n{lp_const}\n")
        user = (f"=== PEDAGOGY ===\n{self._pedagogy}\n\n=== CHAPTER SUMMARY ===\n{summary}\n\n"
                f"=== MAPPING ===\n{mapping}\n\n=== TEACHER PERIOD SCHEDULE ===\n{period_profile}\n\n"
                "Output a single valid JSON object with lesson_plan.periods[] and coverage_handoff. "
                "Raw JSON only.")
        return Prompt(system=system, messages=[{"role": "user", "content": user}], cache_system=True)

    def build_assessment_prompt(self, *, grade, chapter, summary, mapping, lesson_plan) -> Prompt:
        stage = stage_for(grade)
        a_const = self._const.get(stage, {}).get("assessment", "")
        system = ("You are Aruvi's Mathematics assessment generator. The constitution below is "
                  f"binding.\n\n=== MATHS ASSESSMENT CONSTITUTION ({stage}) ===\n{a_const}\n")
        user = (f"=== CHAPTER SUMMARY ===\n{summary}\n\n=== LESSON PLAN (handoff) ===\n{lesson_plan}\n\n"
                "Raw JSON only.")
        return Prompt(system=system, messages=[{"role": "user", "content": user}], cache_system=True)

    def chapter_weight(self, mapping):
        return float(mapping.get("effort_index") or 0)

    def allocation_basis(self, grade):
        if stage_for(grade) == "secondary":
            factors = ["Conceptual demand", "Reasoning load", "In-class execution load"]
        else:
            factors = ["Conceptual demand",
                       "The core competency and any adjacent ones",
                       "Activities and worked examples",
                       "In-class execution load"]
        return {"basis": "effort index", "factors": factors}

    # ── Validation ──────────────────────────────────────────────────────────────
    def validate(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        lp = raw.get("lesson_plan", raw)
        if isinstance(lp, dict) and "periods" in lp:
            if not lp["periods"]:
                raise ValueError("Maths lesson plan has no periods (possible truncation).")
        elif "questions" in raw:                       # secondary assessment
            if not raw["questions"]:
                raise ValueError("Maths (secondary) assessment has no questions.")
        elif "assessment_items" in raw:                # middle assessment (section groups)
            if not raw["assessment_items"]:
                raise ValueError("Maths (middle) assessment has no items.")
        return raw

    # ── Lesson plan → view (dispatch by stage) ──────────────────────────────────
    def lesson_plan_to_view(self, raw: Dict[str, Any], *, grade, chapter) -> LessonPlanView:
        periods = raw.get("lesson_plan", raw).get("periods", [])
        secondary = stage_for(grade) == "secondary"
        groups: List[Group] = []
        index: Dict[str, Group] = {}
        for p in periods:
            if secondary:
                key = label = str(p.get("section_anchor", ""))
                bands = p.get("time_bands")
                gmeta = {"section_anchor": key}
            else:
                seg = (p.get("textbook_segments") or [{}])[0]
                key = str(seg.get("ref", "")) or "lesson"
                label = " — ".join(x for x in (seg.get("ref"), seg.get("title")) if x) or "Lesson"
                bands = p.get("phases")
                gmeta = {"ref": seg.get("ref", "")}
            if key not in index:
                g = Group(type="section", label=label, meta=gmeta)
                index[key] = g
                groups.append(g)
            index[key].periods.append(Period(
                number=p.get("period_number", 0),
                title=p.get("activity_title", ""),
                activities=text_lines(p.get("textbook_items_in_class")) + band_lines(bands),
                teacher_notes=as_list(p.get("teacher_notes")),
                homework=_hw(p.get("homework")),
                meta={"section_goal": p.get("section_goal", ""),
                      "pedagogical_method": p.get("pedagogical_method", ""),
                      "materials": p.get("materials", ""),
                      "visual_aids": p.get("visual_aids", ""),
                      "duration_minutes": p.get("period_duration_minutes")},
            ))
        return LessonPlanView(
            subject="mathematics", grade=grade,
            chapter_number=chapter.get("chapter_number", 0),
            chapter_title=chapter.get("chapter_title", ""),
            total_periods=len(periods), groups=groups,
        )

    # ── Assessment → view (dispatch by stage) ───────────────────────────────────
    def assessment_to_view(self, raw: Union[Dict[str, Any], list], *, grade, chapter,
                           link_context: Dict[str, Any] = None) -> AssessmentView:
        ctx = link_context or {}
        if stage_for(grade) == "secondary":
            groups = self._secondary_assess(raw, ctx)   # rule 6
        else:
            groups = self._middle_assess(raw, ctx, grade)  # rules 4 (middle) & 5 (prep)
        return AssessmentView(
            subject="mathematics", grade=grade,
            chapter_number=chapter.get("chapter_number", 0),
            chapter_title=chapter.get("chapter_title", ""),
            groups=groups,
        )

    def _middle_assess(self, raw, ctx, grade) -> List[AssessmentGroup]:
        # Rules 4 (middle) & 5 (preparatory) — period-field join, no handoff. Each leaf item
        # carries `section_ref`; match it to the period's own section field:
        #   MIDDLE  → period.textbook_segments[].ref   ("section 2.1")
        #   PREP    → period.section_refs[]             ("S2")
        # Both normalize through norm_code so "section 2.1"/"2.1" and "S2"/"s2" converge.
        periods = ctx.get("periods", []) or []
        prep = stage_for(grade) == "preparatory"
        if prep:
            extract = lambda p: p.get("section_refs", []) or []
        else:
            extract = lambda p: [seg.get("ref", "") for seg in (p.get("textbook_segments") or [])]
        period_index = period_field_index(periods, extract)

        section_groups = raw.get("assessment_items", raw) if isinstance(raw, dict) else raw
        out: List[AssessmentGroup] = []
        for sg in section_groups or []:
            g = AssessmentGroup(
                type="section",
                label=f"Section {sg.get('section_code', '')}: {sg.get('section_title', '')}".strip(": "),
                meta={"section_code": sg.get("section_code", ""), "note": sg.get("note", "")},
            )
            for it in sg.get("items", []):
                options, answer = normalize_options(it.get("options"))
                ref = it.get("section_ref", "")
                meta = {"section_ref": ref, "goal": it.get("goal", ""),
                        "exercise": it.get("exercise", "")}
                stamp(meta, period_index.get(norm_code(ref), []), None)  # rules 4/5: no LO
                g.items.append(AssessmentItem(
                    prompt=it.get("prompt", ""),
                    item_type=it.get("question_type", ""),
                    options=options, answer=answer,
                    teacher_guide=as_list(it.get("teacher_guide")),
                    visual_stimulus=classify_stimulus(it.get("visual_stimulus", "")),
                    meta=meta,
                ))
            out.append(g)
        return out

    def _secondary_assess(self, raw, ctx) -> List[AssessmentGroup]:
        # Rule 6 — handoff-bridged on the INTEGER section_number → period_numbers (NEVER the
        # section_anchor/section_ref text, per the plan's correction). Falls back to the periods'
        # section_anchor only if a handoff is absent — but secondary plans carry handoffs.
        handoff = ctx.get("handoff", []) or []
        period_index = handoff_period_index(handoff, "section_number")
        questions = raw.get("questions", raw) if isinstance(raw, dict) else raw
        out: List[AssessmentGroup] = []
        index: Dict[str, AssessmentGroup] = {}
        for q in questions or []:
            key = str(q.get("section_ref", q.get("section_number", "")))
            if key not in index:
                g = AssessmentGroup(
                    type="section",
                    label=" ".join(x for x in (str(q.get("section_ref", "")), q.get("section_title", "")) if x),
                    meta={"implied_lo": q.get("implied_lo_assessed", ""),
                          "section_number": q.get("section_number", "")},
                )
                index[key] = g
                out.append(g)
            options, answer = normalize_options(q.get("options"))
            guide = (as_list(q.get("look_for")) + as_list(q.get("expected_elements"))
                     + as_list(q.get("scaffold")) + as_list(q.get("guide"))
                     + as_list(q.get("method_one_line")))
            sn = q.get("section_number")
            lo = q.get("implied_lo_assessed", "")
            meta = {"competency": q.get("competency", {}),
                    "cognitive_demand": q.get("cognitive_demand", "")}
            linked = period_index.get(int(sn), []) if sn is not None else []
            stamp(meta, linked, lo)
            index[key].items.append(AssessmentItem(
                prompt=q.get("question_text", ""),
                item_type=q.get("question_type", ""),
                options=options,
                answer=str(q.get("expected_answer") or answer),
                teacher_guide=guide,
                implied_lo=lo,
                visual_stimulus=classify_stimulus(q.get("visual_stimulus", "")),
                meta=meta,
            ))
        return out
