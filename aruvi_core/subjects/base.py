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
    ) -> AssessmentView: ...
