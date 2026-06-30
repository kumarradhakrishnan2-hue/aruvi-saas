"""
The Subject contract — one self-contained plugin per subject.

A subject owns: prompt building, validation, and normalization to the canonical view model.
The engine never branches on subject; it only calls this interface. Adding subject N+1 means
implementing this Protocol and dropping its constitution/data under subjects/{name}/ — with
zero edits to shared code. This is what kills the prototype's "shotgun surgery" debt.
"""
from __future__ import annotations

from typing import Any, Dict, Protocol, runtime_checkable

from ..ports import Prompt
from ..view_model import AssessmentView, LessonPlanView


@runtime_checkable
class Subject(Protocol):
    name: str  # registry key, e.g. "science", "english", "mathematics", "social_sciences"

    def build_lesson_plan_prompt(
        self, *, grade: str, chapter: Dict[str, Any], summary: Any,
        mapping: Dict[str, Any], period_profile: Dict[str, Any],
    ) -> Prompt: ...

    def build_assessment_prompt(
        self, *, grade: str, chapter: Dict[str, Any], summary: Any,
        mapping: Dict[str, Any], lesson_plan: Dict[str, Any],
    ) -> Prompt: ...

    def validate(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Subject-specific structural validation of the model's raw JSON."""
        ...

    def lesson_plan_to_view(
        self, raw: Dict[str, Any], *, grade: str, chapter: Dict[str, Any],
    ) -> LessonPlanView:
        """Normalize this subject's shape into the canonical, structure-preserving view."""
        ...

    def assessment_to_view(
        self, raw: Dict[str, Any], *, grade: str, chapter: Dict[str, Any],
        link_context: Dict[str, Any] | None = None,
    ) -> AssessmentView:
        """Normalize the assessment into the canonical view AND resolve each item's link to
        the lesson plan's periods (architecture-plan.md §Link resolution). `link_context`, when
        provided, carries what handoff-bridged/period-field resolvers need:
            {"periods": [raw period dicts], "handoff": coverage_handoff}
        Every item ends up with item.meta {linked_periods[], anchor_period, linked_lo} via
        aruvi_core.link_resolver.stamp(). link_context=None (older callers/tests) → items still
        normalize, just with empty link metadata."""
        ...

    def chapter_weight(self, mapping: Dict[str, Any]) -> float:
        """The single number that drives Allocate for this chapter — read from the chapter's
        mapping JSON. SS reads `chapter_weight`; the effort-index subjects read `effort_index`."""
        ...

    def allocation_basis(self, grade: str) -> Dict[str, Any]:
        """Static, subject/stage-level explanation of WHAT the allocation weight reflects —
        the factors enumerated, never the numbers/ranges. Powers the teacher-facing
        'How are periods allocated?' note. Shape: {"basis": str, "factors": [str, ...]}."""
        ...
