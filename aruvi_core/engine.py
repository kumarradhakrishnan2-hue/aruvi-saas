"""
The engine — a tiny, subject-agnostic orchestrator.

It resolves a subject from the registry and walks the same pipeline for every subject:
    prompt -> LLM -> validate -> normalize to canonical view model.
It never branches on subject and never touches storage, auth, or caching — those are the
service layer's concern (output caching wraps this call; see ports.OutputCache).
"""
from __future__ import annotations

import json
from typing import Any, Dict, Union

from . import subjects
from .ports import LLMClient, AllocationRecord, AllocationRepository, AllocationSummary
from .view_model import AssessmentView, LessonPlanView, ViewModel


class GenerationError(RuntimeError):
    pass


def _parse_json(text: str) -> Dict[str, Any]:
    """Tolerant parse. The prototype learned that truncation yields invalid JSON that
    silently became an empty plan; here we fail loudly instead (the service layer logs
    token usage to distinguish truncation from a real error)."""
    s = text.strip()
    if s.startswith("```"):
        # strip a ```json ... ``` fence if the model wrapped its output
        inner = s.split("```")
        if len(inner) >= 2:
            s = inner[1]
            if s.lstrip().lower().startswith("json"):
                s = s.lstrip()[4:]
            s = s.strip()
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        raise GenerationError(f"Model output was not valid JSON ({e}).") from e


def generate(
    *,
    subject_name: str,
    grade: str,
    chapter: Dict[str, Any],
    summary: Any,
    mapping: Dict[str, Any],
    period_profile: Dict[str, Any],
    llm: LLMClient,
) -> ViewModel:
    """Generate one chapter's lesson plan + assessment as a canonical ViewModel."""
    subject = subjects.get(subject_name)

    lp_prompt = subject.build_lesson_plan_prompt(
        grade=grade, chapter=chapter, summary=summary,
        mapping=mapping, period_profile=period_profile,
    )
    lp_raw = subject.validate(_parse_json(llm.generate(lp_prompt).text))
    lp_view: LessonPlanView = subject.lesson_plan_to_view(lp_raw, grade=grade, chapter=chapter)

    a_prompt = subject.build_assessment_prompt(
        grade=grade, chapter=chapter, summary=summary,
        mapping=mapping, lesson_plan=lp_raw,
    )
    a_raw = subject.validate(_parse_json(llm.generate(a_prompt).text))
    a_view: AssessmentView = subject.assessment_to_view(a_raw, grade=grade, chapter=chapter)

    return ViewModel(lesson_plan=lp_view, assessment=a_view)


def save_allocation(
    *,
    tenant_id: str,
    user_id: str,
    subject_name: str,
    grade: Union[str, int],
    chapters_allocation: Dict[str, AllocationRecord],
    allocation_repo: AllocationRepository,
) -> None:
    """Save allocation data to this teacher's Persistent Annual Allocation Register.

    Merges chapters_allocation into the existing register — new/overwritten chapters
    replace existing ones; untouched chapters persist. Keyed per tenant + user.
    """
    allocation_repo.save_allocation(tenant_id, user_id, subject_name, grade, chapters_allocation)


def get_allocation_summary(
    *,
    tenant_id: str,
    user_id: str,
    subject_name: str,
    grade: Union[str, int],
    allocation_repo: AllocationRepository,
) -> AllocationSummary:
    """Retrieve a summary of this teacher's current allocation register state."""
    return allocation_repo.get_summary(tenant_id, user_id, subject_name, grade)


def get_allocation_register(
    *,
    tenant_id: str,
    user_id: str,
    subject_name: str,
    grade: Union[str, int],
    allocation_repo: AllocationRepository,
) -> Dict[str, AllocationRecord]:
    """Retrieve this teacher's full saved register ({chapter_num: AllocationRecord}) so the
    frontend can rehydrate its final-allocation view without re-deriving it from the
    LRM/mappings."""
    return allocation_repo.load_register(tenant_id, user_id, subject_name, grade)


def clear_allocation_register(
    *,
    tenant_id: str,
    user_id: str,
    subject_name: str,
    grade: Union[str, int],
    allocation_repo: AllocationRepository,
) -> None:
    """Erase this teacher's saved register for a subject·grade (the "Reset allocations"
    action)."""
    allocation_repo.clear_register(tenant_id, user_id, subject_name, grade)
