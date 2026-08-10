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

    # ── genon: WHERE this stage keeps its unit's section anchor (default: None) ──────
    # Added 2026-08-10 at S7. `carriers.unit_anchor` reads `period["section_anchor"]`, which
    # is what most section-axis constitutions emit. mathematics·middle has a section axis but
    # spells it `textbook_segments[].ref`, and preparatory spells it `section_refs[]`.
    #
    # FOUNDER RULING 2026-08-10: no new field may be invented to feed the serve engine — the
    # constitutions are NOT amended to add `section_anchor`, the READ is mediated instead.
    # This is that mediation, and it belongs on the plugin because a field name is a fact
    # about a subject's constitution, never about the engine (CLAUDE.md §3). The prototype
    # absorbed exactly this variance at its own read boundary
    # (`lp_pdf_generator.py`'s textbook_segments-else-section_anchor branch).
    #
    # Return the anchor VERBATIM — the certifier compares it against a registry drawn from
    # the chapter summary's own `sections[].ref`, so any reformatting manufactures a mismatch.
    # Several sections in one unit join with `carriers._ANCHOR_JOINER` (" / "). Return None
    # (or do not implement the method) when the stage has nothing to say; `unit_anchor` then
    # behaves exactly as it did before — raising on a section-axis stage, None otherwise.
    #
    # `period` is the raw period dict; `grade` is passed for symmetry and may be None, since
    # compile.py reads the grade off the enclosing saved plan.
    def genon_unit_anchor(self, period: Dict[str, Any], grade: str | None) -> Any: ...

    # ── genon: is the anchor a FIELD, or is it mediated? (default: True) ─────────────
    # Added 2026-08-10 at S7, alongside `genon_unit_anchor`. It answers one question and
    # only one: DOES THIS SUBJECT·STAGE'S CONSTITUTION DEFINE A `section_anchor` FIELD ON
    # THE PERIOD OBJECT, or is the anchor mediated out of another field by
    # `genon_unit_anchor`? True for ten of the eleven stages; False for
    # mathematics·middle (`textbook_segments[].ref`) and mathematics·preparatory
    # (`section_refs[]`).
    #
    # WHY IT IS DECLARED RATHER THAN INFERRED. It could be guessed — "does this plugin
    # override `genon_unit_anchor`?" — and that guess would be wrong the first time a
    # subject mediates one stage and not another, which mathematics ALREADY does
    # (secondary keeps the field; middle and preparatory do not, and all three share one
    # plugin object). Sniffing for a method override cannot see a per-stage fact, and a
    # per-stage fact is what this is.
    #
    # WHAT READS IT (2026-08-10). `genon/variant_plans.py::top_brief_for`. The standard
    # canonical's synthesis mandate has two carriers for one fact (architecture §0.3, and
    # `carriers.is_synthesis`): a stage WITH the field puts the reserved token `synthesis`
    # in it; a stage WITHOUT the field carries `"synthesis": true` on the period object
    # instead. Asking a mediated stage for `section_anchor` would demand a field its
    # constitution never defines, at metered STEP 1, and the certifier's synthesis gate
    # would then find no synthesis unit at all. It is a BRIEF matter, never a constitution
    # amendment (founder ruling 2026-08-10: nothing new may be added to a constitution to
    # feed the serve engine).
    #
    # It is NOT the same question as `genon_has_section_axis`. A stage can have a section
    # axis and no `section_anchor` field (mathematics·middle: True/False), or no axis at
    # all (science·middle: False/…). Nor is it the same as serve granularity.
    def genon_anchor_field_present(self, grade: str) -> bool: ...

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
