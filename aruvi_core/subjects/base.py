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

    # ── genon: how this subject·stage is SERVED (optional; default "unit") ───────────
    # Added 2026-08-07 at S6. The serve engine must not branch on subject (§3), so the
    # subject declares its own granularity and serve.py reads the declaration.
    #
    #   "unit" — units are the atoms: a plan is a prefix of a canonical plus one borrowed
    #            unit, and coverage is measured in SECTIONS. Ten of the eleven stages.
    #   "plan" — canonicals are the atoms. science·middle alone: its units belong to a
    #            cognitive progression arc, a stage is taught whole or not at all, so no
    #            prefix of a canonical is a valid plan. Serving is whole-canonical
    #            selection; the only bridge between two counts is the top's single
    #            synthesis unit. Spec: docs/science_middle_stage_serve.md.
    #
    # A "plan"-granularity stage also has NO SECTION AXIS: `section_anchor` is absent by
    # design, and `genon_has_section_axis` tells compile.py that its absence is expected
    # rather than a malformed plan.
    def genon_serve_granularity(self, grade: str) -> str: ...

    def genon_has_section_axis(self, grade: str) -> bool: ...

    # ── genon: which family LINKS an assessment item to its unit (default "item") ────
    # Added 2026-08-08 at S4. This is the verified 8-rule table's family column
    # (docs/architecture-plan.md §"Link resolution"), declared instead of inferred, so
    # nothing downstream has to guess — and so a subject cannot invent a fourth way.
    #
    #   "item"         — item-self-sufficient: `period_ref[]` is read straight off the
    #                    item. social_sciences, the_world_around_us (rows 3, 8).
    #   "handoff"      — handoff-bridged: the item carries an integer group number
    #                    (section/stage) and the platform joins it through
    #                    `coverage_handoff` → `period_numbers`. science both stages,
    #                    mathematics·secondary (rows 1, 2, 6).
    #   "period_field" — the item's section/spine code matches the PERIOD's own field.
    #                    mathematics middle/preparatory, english (rows 4, 5, 7).
    #
    # It has one consequence beyond the join, which is why it is declared at all: on a
    # "handoff" stage an item's anchor is DERIVED, so a unit with no handoff row can carry
    # no items — and the standard canonical's mandated closing SYNTHESIS unit is exactly
    # such a unit unless the brief asks for a row for it. `variant_plans.top_brief_for`
    # reads this to decide whether to ask. See docs/testing.md §3 P5.5.
    def genon_item_anchor_family(self, grade: str) -> str: ...
