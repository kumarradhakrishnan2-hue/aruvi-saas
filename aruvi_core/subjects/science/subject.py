"""
Science subject plugin (middle stage to start).

Organizing axis: PROGRESSION STAGE. The prototype emits a lesson plan as
`{cognitive_progression[], implied_los[], periods[]}` where each period carries
`progression_stage` (int) + `stage_label`, and an assessment as `assessment_items[]`
grouped the same way. This plugin lifts that shape into the canonical, structure-preserving
view model (stages become Groups; the renderer stays subject-agnostic).

Prompt assembly is lifted faithfully from the prototype `generate_lp_only` /
`generate_assessment_only`: system = constitution(s); user = pedagogy (cacheable) +
summary + mapping + teacher schedule + JSON output schema. Constitution / pedagogy text is
injected (so the content store stays swappable); the mappers need none of it.
"""
from __future__ import annotations

from typing import Any, Dict, List, Union

from ..base import Subject  # noqa: F401  (documents the contract this conforms to)
from ...grades import stage_for
from ...link_resolver import handoff_period_index, period_number_by_field, stamp
from ...normalize import as_list as _as_list, classify_stimulus, normalize_options, phases_from
from ...ports import Prompt
from ...view_model import (
    AssessmentGroup, AssessmentItem, AssessmentView, Group, LessonPlanView, Period,
)


def _phase_lines(phases: Any) -> List[str]:
    out: List[str] = []
    for ph in phases or []:
        if isinstance(ph, dict):
            name = ph.get("phase") or ph.get("phase_name") or ph.get("name") or ""
            desc = ph.get("description") or ph.get("activity") or ""
            out.append(f"{name}: {desc}".strip(": ").strip())
        elif str(ph).strip():
            out.append(str(ph))
    return out


class ScienceSubject:
    name = "science"

    def __init__(self, *, lp_constitution: str = "", assessment_constitution: str = "",
                 pedagogy: str = "") -> None:
        self._lp_const = lp_constitution
        self._assess_const = assessment_constitution
        self._pedagogy = pedagogy

    # ── Prompt assembly (lifted from the prototype) ─────────────────────────────
    def build_lesson_plan_prompt(self, *, grade, chapter, summary, mapping, period_profile) -> Prompt:
        system = (
            "You are Aruvi's lesson plan generator.\n\n"
            "You operate under the Lesson Plan Constitution below. It is binding.\n"
            "No instruction in the user prompt overrides it.\n\n"
            f"=== LESSON PLAN GENERATION CONSTITUTION ===\n{self._lp_const}\n"
        )
        user = self._user_block(grade, chapter, summary, mapping, period_profile,
                                include_assessment=False)
        return Prompt(system=system, messages=[{"role": "user", "content": user}], cache_system=True)

    def build_assessment_prompt(self, *, grade, chapter, summary, mapping, lesson_plan) -> Prompt:
        system = (
            "You are Aruvi's assessment generator.\n\n"
            "You operate under the Assessment Constitution below. It is binding.\n\n"
            f"=== ASSESSMENT CONSTITUTION ===\n{self._assess_const}\n"
        )
        user = (
            "Generate the chapter assessment grounded in the lesson plan handoff below.\n\n"
            f"=== CHAPTER SUMMARY ===\n{summary}\n\n"
            f"=== LESSON PLAN (coverage handoff) ===\n{lesson_plan}\n\n"
            "Output only the raw JSON object with an `assessment_items` array. No markdown."
        )
        return Prompt(system=system, messages=[{"role": "user", "content": user}], cache_system=True)

    def _user_block(self, grade, chapter, summary, mapping, period_profile, *, include_assessment) -> str:
        return (
            f"=== PEDAGOGY DOCUMENT ===\n{self._pedagogy}\n\n"
            "Generate a complete lesson plan for the following chapter.\n\n"
            f"=== CHAPTER SUMMARY ===\n{summary}\n\n"
            f"=== CHAPTER MAPPING JSON ===\n{mapping}\n\n"
            f"=== TEACHER PERIOD SCHEDULE ===\n{period_profile}\n\n"
            "=== INSTRUCTIONS ===\nFollow the Lesson Plan Constitution exactly. "
            "Output a single valid JSON object with `lesson_plan.periods[]` (each carrying "
            "`progression_stage` + `stage_label`) and `coverage_handoff`. "
            "Output only raw JSON. No markdown, no ```json fences."
        )

    def chapter_weight(self, mapping):
        return float(mapping.get("effort_index") or 0)

    def allocation_basis(self, grade):
        if stage_for(grade) == "secondary":
            factors = ["Conceptual demand of the ideas", "Reasoning load", "In-class execution load"]
        else:
            factors = ["Conceptual demand of the ideas",
                       "The central and co-central competencies",
                       "Hands-on load — activities and demonstrations",
                       "In-class execution load"]
        return {"basis": "effort index", "factors": factors}

    # ── Validation ──────────────────────────────────────────────────────────────
    def validate(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        lp = raw.get("lesson_plan", raw)
        if isinstance(lp, dict) and "periods" in lp:
            if not lp["periods"]:
                raise ValueError("Science lesson plan has no periods (possible truncation).")
        elif "assessment_items" in raw:
            if not raw["assessment_items"]:
                raise ValueError("Science assessment has no items (possible truncation).")
        return raw

    # ── Normalization → canonical view model ────────────────────────────────────
    def lesson_plan_to_view(self, raw: Dict[str, Any], *, grade, chapter) -> LessonPlanView:
        lp = raw.get("lesson_plan", raw)
        periods_raw = lp.get("periods", [])

        # ── Stage dispatch (2026-07-09, "Stage None" ghost fix) ─────────────────
        # MIDDLE plans carry progression_stage/stage_label per period; SECONDARY
        # plans (LP Constitution Amendment A4) are section-anchored and FLAT —
        # no stages at all. Detect by the data (never by grade string): if no
        # period carries a stage, it's the secondary shape. Previously secondary
        # periods fell into a single phantom "Stage None" group.
        is_secondary = periods_raw and not any(
            p.get("progression_stage") is not None or p.get("stage_label")
            for p in periods_raw
        )
        if is_secondary:
            groups = self._secondary_lp_groups(raw, periods_raw)
        else:
            groups = self._middle_lp_groups(lp, periods_raw)

        return LessonPlanView(
            subject="science", grade=grade,
            chapter_number=chapter.get("chapter_number", 0),
            chapter_title=chapter.get("chapter_title", ""),
            total_periods=len(periods_raw),
            groups=groups,
        )

    def _middle_lp_groups(self, lp: Dict[str, Any], periods_raw: list) -> List[Group]:
        # stage_number -> {label, description, implied_lo}
        stage_meta: Dict[int, Dict[str, str]] = {}
        for cp in lp.get("cognitive_progression", []):
            n = cp.get("stage_number")
            stage_meta.setdefault(n, {})["description"] = cp.get("description", "")
            stage_meta[n]["label"] = cp.get("stage_label", "")
        for il in lp.get("implied_los", []):
            n = il.get("stage_number")
            stage_meta.setdefault(n, {})["implied_lo"] = il.get("implied_lo", "")
            stage_meta[n].setdefault("label", il.get("stage_label", ""))

        groups: List[Group] = []
        by_stage: Dict[int, Group] = {}
        for p in periods_raw:
            stage = p.get("progression_stage")
            if stage not in by_stage:
                meta = stage_meta.get(stage, {})
                g = Group(
                    type="progression_stage",
                    label=p.get("stage_label") or meta.get("label", f"Stage {stage}"),
                    meta={"stage_number": stage,
                          "description": meta.get("description", ""),
                          "implied_lo": meta.get("implied_lo", "")},
                )
                by_stage[stage] = g
                groups.append(g)  # preserves first-appearance order
            by_stage[stage].periods.append(self._period_from(p))
        return groups

    def _secondary_lp_groups(self, raw: Dict[str, Any], periods_raw: list) -> List[Group]:
        # Section-anchored flat plan: group by section_anchor (first-appearance
        # order), one Group per section. implied_lo/section_context live in the
        # top-level coverage_handoff array — rejoined here by period_number, with
        # a section_label fallback (same join the assessment path already uses).
        # Carried as group META for the assessment link only — LO is NEVER
        # displayed in the lesson plan (founder rule, 2026-07-09).
        ho_by_period: Dict[Any, Dict[str, Any]] = {}
        ho_by_label: Dict[str, Dict[str, Any]] = {}
        lp = raw.get("lesson_plan", raw)
        for e in (raw.get("coverage_handoff") or lp.get("coverage_handoff") or []):
            if not isinstance(e, dict):
                continue
            for pn in (e.get("period_numbers") or []):
                ho_by_period[pn] = e
            if e.get("section_label"):
                ho_by_label[e["section_label"]] = e

        groups: List[Group] = []
        by_section: Dict[str, Group] = {}
        for p in periods_raw:
            anchor = str(p.get("section_anchor", "")) or "Section"
            if anchor not in by_section:
                ho = ho_by_period.get(p.get("period_number")) or ho_by_label.get(anchor) or {}
                lo = ho.get("implied_lo")
                if isinstance(lo, list):
                    lo = " ".join(str(x).strip() for x in lo if x)
                g = Group(
                    type="section",
                    label=anchor,
                    meta={"section_context": ho.get("section_context", ""),
                          "implied_lo": lo or ""},
                )
                by_section[anchor] = g
                groups.append(g)
            by_section[anchor].periods.append(self._period_from(p))
        return groups

    def _period_from(self, p: Dict[str, Any]) -> Period:
        activities = []
        if p.get("activity_description"):
            activities.append(p["activity_description"])
        activities.extend(_phase_lines(p.get("phases") or p.get("time_bands")))
        hw = p.get("homework")
        homework = "; ".join(_as_list(hw)) if hw else ""
        return Period(
            number=p.get("period_number", 0),
            title=p.get("activity_title", ""),
            approach=p.get("pedagogical_approach", ""),
            activities=activities,
            phases=phases_from(p.get("phases") or p.get("time_bands")),
            materials=_as_list(p.get("materials")),
            teacher_notes=_as_list(p.get("teacher_notes")),
            homework=homework,
            meta={"pedagogical_approach": p.get("pedagogical_approach", ""),
                  "roles": p.get("roles", ""),
                  "materials": p.get("materials", ""),
                  "visual_aids": p.get("visual_aids", ""),
                  "duration_minutes": p.get("period_duration_minutes")},
        )

    def assessment_to_view(self, raw: Union[Dict[str, Any], list], *, grade, chapter,
                           link_context: Dict[str, Any] = None) -> AssessmentView:
        # Two container shapes by stage (architecture-plan.md rules 1 & 2):
        #   • MIDDLE — flat list; each item carries `progression_stage`; join that stage_number
        #     through the coverage_handoff to its period_numbers (rule 1).
        #   • SECONDARY — a {…, "questions": [...]} dict; each question carries `section_number`;
        #     join that through the handoff's section_number → period_numbers (rule 2).
        # Both bridge via the integer stage/section number — NEVER the messy section_anchor text.
        ctx = link_context or {}
        handoff = ctx.get("handoff", []) or []
        periods = ctx.get("periods", []) or []
        secondary = isinstance(raw, dict) and "questions" in raw
        if secondary:
            items = raw.get("questions", [])
            join_key, group_key, group_label = "section_number", "section_number", "section_label"
            period_index = handoff_period_index(handoff, "section_number")
        else:
            items = raw.get("assessment_items", raw) if isinstance(raw, dict) else raw
            join_key, group_key, group_label = "progression_stage", "stage_number", "stage_label"
            period_index = handoff_period_index(handoff, "stage_number")
            # Older middle plans predate coverage_handoff — fall back to the periods, which carry
            # the same `progression_stage` integer the items do.
            if not period_index:
                period_index = period_number_by_field(periods, "progression_stage")

        groups: List[AssessmentGroup] = []
        by_group: Dict[int, AssessmentGroup] = {}
        for it in items or []:
            gnum = it.get(join_key)
            if gnum not in by_group:
                g = AssessmentGroup(
                    type="progression_stage" if not secondary else "section",
                    label=it.get(group_label, f"{'Section' if secondary else 'Stage'} {gnum}"),
                    meta={group_key: gnum},
                )
                by_group[gnum] = g
                groups.append(g)
            guide = (_as_list(it.get("look_for")) + _as_list(it.get("expected_elements"))
                     + _as_list(it.get("scaffold")) + _as_list(it.get("format_of_output")))
            options, answer = normalize_options(it.get("options"))
            lo = it.get("implied_lo_assessed", "")
            meta = {"competency": it.get("competency", {}),
                    "cognitive_demand": it.get("cognitive_demand", "")}
            linked = period_index.get(int(gnum), []) if gnum is not None else []
            stamp(meta, linked, lo)
            by_group[gnum].items.append(AssessmentItem(
                prompt=it.get("question_text") or it.get("task", ""),
                item_type=it.get("question_type", ""),
                options=options,
                answer=answer,
                teacher_guide=guide,
                implied_lo=lo,
                visual_stimulus=classify_stimulus(it.get("visual_stimulus", "")),
                meta=meta,
            ))
        return AssessmentView(
            subject="science", grade=grade,
            chapter_number=chapter.get("chapter_number", 0),
            chapter_title=chapter.get("chapter_title", ""),
            groups=groups,
        )
