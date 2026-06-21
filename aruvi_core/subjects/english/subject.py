"""
English subject plugin — the two-axis case (the architecture's hardest stress test).

Organizing structure: OUTER axis = main_sections (a poem/prose/dialogue), INNER axis = the
6-spine cells within each section (Reading, Listening, Speaking, Writing, Vocab/Grammar,
Beyond-the-Text). The prototype emits periods carrying both `section_id`/`section_title` and
`spines_taught[]`, and an assessment ALREADY grouped by spine. NCF compliance is implicit in
the spine structure — there are NO C-codes in the English LP.

This plugin maps that into nested canonical Groups (section -> spine -> periods) so the
shared renderer reproduces the two-axis layout without any English-specific branch.

Prompt assembly strips `tasks_verbatim`/`question_bank` from the summary before sending
(MEMORY #26 / prototype TASK #4): constitution prohibitions alone can't stop the model
copying textbook exercises it can see — so we remove them from context.
"""
from __future__ import annotations

import copy
from typing import Any, Dict, List, Union

from ..base import Subject  # noqa: F401
from ...normalize import as_list, classify_stimulus, normalize_options
from ...ports import Prompt
from ...view_model import (
    AssessmentGroup, AssessmentItem, AssessmentView, Group, LessonPlanView, Period,
)


def _spine_label(codes: List[str]) -> str:
    return " + ".join(c.replace("_", " ").title() for c in codes) or "General"


def _task_lines(tasks: Any) -> List[str]:
    """English tasks_in_class are dicts {spine, task_index, task_brief}; show the brief."""
    out: List[str] = []
    for t in tasks or []:
        if isinstance(t, dict):
            txt = t.get("task_brief") or t.get("task") or t.get("brief") or ""
            if txt:
                out.append(str(txt))
        elif str(t).strip():
            out.append(str(t))
    return out


def _homework_text(hw: Any) -> str:
    """Homework may be a plain string OR a list of task dicts (same shape as tasks_in_class)."""
    if isinstance(hw, list):
        return "; ".join(_task_lines(hw))
    return hw or ""


def _phase_lines(phases: Any) -> List[str]:
    out: List[str] = []
    for ph in phases or []:
        if isinstance(ph, dict):
            name = ph.get("phase") or ph.get("phase_name") or ph.get("name") or ""
            desc = ph.get("description") or ph.get("activity") or ""
            line = f"{name}: {desc}".strip(": ").strip()
            if line:
                out.append(line)
        elif str(ph).strip():
            out.append(str(ph))
    return out


class EnglishSubject:
    name = "english"

    def __init__(self, *, lp_constitution: str = "", assessment_constitution: str = "",
                 pedagogy: str = "") -> None:
        self._lp_const = lp_constitution
        self._assess_const = assessment_constitution
        self._pedagogy = pedagogy

    # ── Prompt assembly ─────────────────────────────────────────────────────────
    def build_lesson_plan_prompt(self, *, grade, chapter, summary, mapping, period_profile) -> Prompt:
        summary = self._strip_contamination(summary)
        system = (
            "You are Aruvi's English lesson plan generator. The Lesson Plan Constitution "
            "below is binding.\n\n"
            f"=== ENGLISH LESSON PLAN CONSTITUTION ===\n{self._lp_const}\n"
        )
        user = (
            f"=== PEDAGOGY ===\n{self._pedagogy}\n\n"
            f"=== CHAPTER SUMMARY ===\n{summary}\n\n"
            f"=== MAPPING (effort index) ===\n{mapping}\n\n"
            f"=== TEACHER PERIOD SCHEDULE ===\n{period_profile}\n\n"
            "=== INSTRUCTIONS ===\nWalk main_sections in textbook order, then spines within "
            "each section. Periods carry `section_id`, `section_title`, and `spines_taught[]`. "
            "Do NOT emit C-codes. Output a single valid JSON object with `lesson_plan.periods[]` "
            "and `coverage_handoff`. Raw JSON only — no markdown."
        )
        return Prompt(system=system, messages=[{"role": "user", "content": user}], cache_system=True)

    def build_assessment_prompt(self, *, grade, chapter, summary, mapping, lesson_plan) -> Prompt:
        summary = self._strip_contamination(summary)
        system = (
            "You are Aruvi's English assessment generator. The Assessment Constitution below "
            "is binding.\n\n"
            f"=== ENGLISH ASSESSMENT CONSTITUTION ===\n{self._assess_const}\n"
        )
        user = (
            f"=== CHAPTER SUMMARY ===\n{summary}\n\n"
            f"=== LESSON PLAN (section x spine handoff) ===\n{lesson_plan}\n\n"
            "Generate one original item per (section x spine) implied_lo, grounded in section "
            "text. Group items by spine. Raw JSON only with an `assessment_items` array of "
            "spine groups."
        )
        return Prompt(system=system, messages=[{"role": "user", "content": user}], cache_system=True)

    @staticmethod
    def _strip_contamination(summary: Any) -> Any:
        """Remove tasks_verbatim / question_bank everywhere in the summary (MEMORY #26)."""
        if not isinstance(summary, (dict, list)):
            return summary
        s = copy.deepcopy(summary)

        def strip(o: Any) -> None:
            if isinstance(o, dict):
                o.pop("tasks_verbatim", None)
                o.pop("question_bank", None)
                for v in o.values():
                    strip(v)
            elif isinstance(o, list):
                for v in o:
                    strip(v)

        strip(s)
        return s

    def chapter_weight(self, mapping):
        return float(mapping.get("effort_index") or 0)

    def allocation_basis(self, grade):
        return {"basis": "effort index", "factors": [
            "The language spines a chapter exercises — reading, listening, speaking, "
            "writing, vocabulary & grammar, and beyond-the-text",
            "How densely tasks are packed",
            "The writing demand",
            "Any project work",
        ]}

    # ── Validation ──────────────────────────────────────────────────────────────
    def validate(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        lp = raw.get("lesson_plan", raw)
        if isinstance(lp, dict) and "periods" in lp:
            if not lp["periods"]:
                raise ValueError("English lesson plan has no periods (possible truncation).")
        elif "assessment_items" in raw:
            if not raw["assessment_items"]:
                raise ValueError("English assessment has no items (possible truncation).")
        return raw

    # ── Normalization → canonical view model (nested section -> spine) ──────────
    def lesson_plan_to_view(self, raw: Dict[str, Any], *, grade, chapter) -> LessonPlanView:
        lp = raw.get("lesson_plan", raw)
        periods = lp.get("periods", [])
        sections: List[Group] = []
        sec_index: Dict[str, Group] = {}
        spine_index: Dict[tuple, Group] = {}

        for p in periods:
            sid = p.get("section_id", "")
            if sid not in sec_index:
                g = Group(type="section", label=p.get("section_title", ""), meta={"section_id": sid})
                sec_index[sid] = g
                sections.append(g)
            spines = p.get("spines_taught") or []
            sig = "+".join(spines) if spines else "general"
            key = (sid, sig)
            if key not in spine_index:
                sg = Group(type="spine", label=_spine_label(spines), meta={"spine_codes": spines})
                spine_index[key] = sg
                sec_index[sid].children.append(sg)
            spine_index[key].periods.append(Period(
                number=p.get("period_number", 0),
                title=p.get("activity_title", ""),
                activities=_task_lines(p.get("tasks_in_class")) + _phase_lines(p.get("phases")),
                teacher_notes=as_list(p.get("teacher_notes")),
                homework=_homework_text(p.get("homework")),
                meta={"pedagogical_methods": p.get("pedagogical_methods", {}),
                      "materials": p.get("materials", ""),
                      "spines_taught": spines,
                      "duration_minutes": p.get("period_duration_minutes")},
            ))

        return LessonPlanView(
            subject="english", grade=grade,
            chapter_number=chapter.get("chapter_number", 0),
            chapter_title=chapter.get("chapter_title", ""),
            total_periods=len(periods), groups=sections,
        )

    def assessment_to_view(self, raw: Union[Dict[str, Any], list], *, grade, chapter) -> AssessmentView:
        spine_groups = raw.get("assessment_items", raw) if isinstance(raw, dict) else raw
        groups: List[AssessmentGroup] = []
        for sg in spine_groups or []:
            g = AssessmentGroup(
                type="spine",
                label=sg.get("spine_title") or sg.get("spine_code", ""),
                meta={"spine_code": sg.get("spine_code", "")},
            )
            for it in sg.get("items", []):
                options, answer = normalize_options(it.get("options"))
                g.items.append(AssessmentItem(
                    prompt=it.get("item_stem", ""),
                    item_type=it.get("question_type", ""),
                    options=options,
                    answer=answer,
                    teacher_guide=as_list(it.get("teacher_guide")),
                    implied_lo=it.get("source_lo", ""),
                    visual_stimulus=classify_stimulus(it.get("visual_stimulus", "")),
                    meta={"source_section_id": it.get("source_section_id", ""),
                          "source_section_title": it.get("source_section_title", ""),
                          "source_spine": it.get("source_spine", ""),
                          "transcript_ref": it.get("transcript_ref", ""),
                          "id": it.get("id", "")},
                ))
            groups.append(g)
        return AssessmentView(
            subject="english", grade=grade,
            chapter_number=chapter.get("chapter_number", 0),
            chapter_title=chapter.get("chapter_title", ""),
            groups=groups,
        )
