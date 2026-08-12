"""
The World Around Us (TWAU) subject plugin — preparatory stage only.

Single organizing axis: SECTION (`section_ref`), with a per-period `dominant_mode`
activity-type label (Explore/Discuss/Create etc.). Assessment groups by question type and
supports the performance_task variant. Collapses into the canonical view model like the rest.
"""
from __future__ import annotations

from typing import Any, Dict, List, Union

from ..base import Subject  # noqa: F401
from ...assessment_norm import from_constitution
from ...genon.carriers import is_synthesis as _is_synth   # boolean OR token (S7)
from ...genon.serve import _ANCHOR_JOINER      # " / " — the V2 multi-section join
from ...link_resolver import stamp
from ...normalize import (as_list, band_lines, classify_stimulus, normalize_options,
                          phases_from, SYNTHESIS_DISPLAY)
from ...ports import Prompt
from ...view_model import (
    AssessmentGroup, AssessmentItem, AssessmentView, Group, LessonPlanView, Period,
)

# dominant_mode code → spelled-out approach line (prototype's _modeFull map; the
# canonical Period.approach carries the FULL name, never the acronym).
_MODE_FULL = {
    "O&R": "Observe and Record",
    "HI": "Hands-on Investigation",
    "D&C": "Discussion and Connection",
    "C&E": "Create and Express",
    "R&A": "Reflect and Act",
}


class TheWorldAroundUsSubject:
    name = "the_world_around_us"

    def __init__(self, *, lp_constitution: str = "", assessment_constitution: str = "",
                 pedagogy: str = "") -> None:
        self._lp_const = lp_constitution
        self._assess_const = assessment_constitution
        self._pedagogy = pedagogy

    # ── Prompt assembly ─────────────────────────────────────────────────────────
    def build_lesson_plan_prompt(self, *, grade, chapter, summary, mapping, period_profile) -> Prompt:
        system = ("You are Aruvi's TWAU lesson plan generator. The constitution below is "
                  f"binding.\n\n=== TWAU LP CONSTITUTION ===\n{self._lp_const}\n")
        user = (f"=== PEDAGOGY ===\n{self._pedagogy}\n\n=== CHAPTER SUMMARY ===\n{summary}\n\n"
                f"=== MAPPING ===\n{mapping}\n\n=== TEACHER PERIOD SCHEDULE ===\n{period_profile}\n\n"
                "Walk sections; each period carries section_ref and a dominant_mode. Output a "
                "single valid JSON object with lesson_plan.periods[] and coverage_handoff. Raw JSON only.")
        return Prompt(system=system, messages=[{"role": "user", "content": user}], cache_system=True)

    def build_assessment_prompt(self, *, grade, chapter, summary, mapping, lesson_plan) -> Prompt:
        system = ("You are Aruvi's TWAU assessment generator. The constitution below is binding.\n\n"
                  f"=== TWAU ASSESSMENT CONSTITUTION ===\n{self._assess_const}\n")
        user = (f"=== CHAPTER SUMMARY ===\n{summary}\n\n=== LESSON PLAN (handoff) ===\n{lesson_plan}\n\n"
                "Raw JSON only with an `assessment_items` array.")
        return Prompt(system=system, messages=[{"role": "user", "content": user}], cache_system=True)

    def chapter_weight(self, mapping):
        return float(mapping.get("effort_index") or 0)

    def allocation_basis(self, grade):
        return {"basis": "effort index", "factors": [
            "The curricular goals the chapter develops",
            "The breadth of explore, discuss and create activities",
        ]}

    # ── Validation ──────────────────────────────────────────────────────────────
    def validate(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        lp = raw.get("lesson_plan", raw)
        if isinstance(lp, dict) and "periods" in lp:
            if not lp["periods"]:
                raise ValueError("TWAU lesson plan has no periods (possible truncation).")
        elif "assessment_items" in raw:
            if not raw["assessment_items"]:
                raise ValueError("TWAU assessment has no items.")
        return raw

    # ── Lesson plan → view (grouped by section) ─────────────────────────────────
    def lesson_plan_to_view(self, raw: Dict[str, Any], *, grade, chapter) -> LessonPlanView:
        periods = raw.get("lesson_plan", raw).get("periods", [])
        groups: List[Group] = []
        index: Dict[str, Group] = {}
        for p in periods:
            # THE SYNTHESIS UNIT IS ITS OWN GROUP, LABELLED "Synthesis" (2026-08-11, S5).
            # ARV-D-101's shape on a third stage. This port grouped purely on
            # `section_ref`, and TWAU's synthesis closer wears a REAL section title (its
            # anchor is mediated, so there is no reserved token to file it under) — so the
            # standard canonical's whole-chapter closer was merged into whichever section
            # it happened to name, and a teacher served X=15 read a three-unit "Spirit of
            # Togetherness" group whose last sitting is the chapter synthesis. The unit was
            # right; only the grouping was wrong, which is exactly what ARV-D-101 said of
            # maths·middle and ARV-D-016 of SS·secondary.
            #
            # Read the fact through the SEAM (`carriers.is_synthesis`), never off the title
            # or the anchor: on this stage the boolean is the only carrier, because
            # `genon_anchor_field_present` is False. The word itself is
            # `normalize.SYNTHESIS_DISPLAY`, so all three synthesis-aware ports say the
            # same thing in the same case.
            if _is_synth(p):
                sec, label = "\x00synthesis", SYNTHESIS_DISPLAY
            else:
                sec = str(p.get("section_ref", "")) or "Section"
                label = sec
            if sec not in index:
                g = Group(type="section", label=label,
                          meta={"section_ref": "" if label == SYNTHESIS_DISPLAY else sec,
                                **({"synthesis": True} if label == SYNTHESIS_DISPLAY else {})})
                index[sec] = g
                groups.append(g)
            index[sec].periods.append(Period(
                number=p.get("period_number", 0),
                title=p.get("activity_title", ""),
                approach=_MODE_FULL.get(p.get("dominant_mode", ""), p.get("dominant_mode", "")),
                activities=band_lines(p.get("time_bands")),
                phases=phases_from(p.get("time_bands")),
                materials=as_list(p.get("materials")),
                learning_outcomes=as_list(p.get("implied_lo")),
                teacher_notes=as_list(p.get("teacher_facilitation_note")),
                meta={"dominant_mode": p.get("dominant_mode", ""),
                      "textbook_anchor": p.get("textbook_anchor", ""),
                      "section_context": p.get("section_context", ""),
                      "materials": p.get("materials", ""),
                      "duration_minutes": p.get("period_duration_minutes")},
            ))
        return LessonPlanView(
            subject="the_world_around_us", grade=grade,
            chapter_number=chapter.get("chapter_number", 0),
            chapter_title=chapter.get("chapter_title", ""),
            total_periods=len(periods), groups=groups,
        )

    # ── Assessment → view (grouped by question type) ────────────────────────────
    def assessment_to_view(self, raw: Union[Dict[str, Any], list], *, grade, chapter,
                           link_context: Dict[str, Any] = None) -> AssessmentView:
        # Rule 8 (item-self-sufficient, 1:1): the item carries its own `period_ref[]` + inline
        # `implied_lo` — same family as SS, stamped directly.
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
                     + as_list(it.get("scaffold")) + as_list(it.get("format_of_output"))
                     + as_list(it.get("guide")))
            lo = it.get("implied_lo", "")
            meta = {"competency": it.get("competency", {}),
                    "cognitive_demand": it.get("cognitive_demand", ""),
                    "performance_task": it.get("performance_task", ""),
                    "period_ref": it.get("period_ref", "")}
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
            subject="the_world_around_us", grade=grade,
            chapter_number=chapter.get("chapter_number", 0),
            chapter_title=chapter.get("chapter_title", ""),
            groups=groups,
        )

    # ── genon: the carrier seam (aruvi_core/genon/carriers.py) ───────────────────
    # Landed 2026-08-11 at S5's P5.5. TWAU's ASSESSMENT half never needed a door: it is
    # 8-rule ROW 8, the item-self-sufficient family, so `carriers.assessment_items`
    # falls through to `items_by_period_ref` and has always been right — which is why
    # the subject was never in `_NOT_YET`. What WAS missing is the other half of the
    # seam, the LESSON PLAN's section anchor, and nothing had noticed because no TWAU
    # chapter had ever reached compile. `tests/test_genon_carriers.py` had it recorded
    # as an open gap ("TWAU's registry join has no owner yet; S5 owes it").

    def genon_has_section_axis(self, grade) -> bool:
        """TWAU anchors every unit to one named textbook section, so this is the platform
        default (True) and changes no behaviour. LP Rule 1 is titled SINGLE-AXIS SECTION
        ANCHORING and mandates walking `sections[]` in reading order; the serve engine's
        section arithmetic is therefore live for this stage and flipping this to False
        would silently disable it."""
        return True

    def genon_unit_anchor(self, period, grade=None):
        """This period's section anchor, in the field THIS constitution uses: `section_ref`.

        `carriers.unit_anchor` reads `period["section_anchor"]` first, and TWAU has no such
        field — `grep -c section_anchor` is 0 in its LP constitution, and the real saved
        plans carry `section_ref` (a full section TITLE, e.g. "A Special Day in School").
        Without this mediation compile raises KeyError on the very first period.

        FOUNDER RULING 2026-08-10 applies unchanged: no new field may be invented to feed
        the serve engine, so the constitution is NOT amended to add `section_anchor` — the
        READ is mediated here, where a subject's own field names belong. Same shape as
        mathematics' `textbook_segments[].ref` / `section_refs[]` mediation, on a third
        field name.

        Returned VERBATIM. Certification compares the anchor against a registry drawn from
        the chapter summary's own `sections[].title`, and both sides are the same authored
        string, so they match by construction; any reformatting here (trimming a subtitle,
        re-casing, collapsing an em dash) would manufacture a mismatch that then needs a
        second normalizer to undo.

        TWAU's `section_ref` is a scalar string, not a list — one unit anchors to exactly
        one section (LP Rule 1: a long section may span several units, never the reverse).
        A list is still accepted and joined with `carriers._ANCHOR_JOINER`, so a future
        multi-section unit needs no code change and cannot arrive as a stringified list.

        Branching is on the PERIOD's shape, never on `stage_for(grade)` — `grade` is passed
        for symmetry with the other genon hooks and is deliberately not required, because
        compile.py reads the grade off the enclosing plan, where it can be absent.
        """
        raw = period.get("section_ref")
        refs = raw if isinstance(raw, list) else [raw]
        seen: List[str] = []
        for r in refs:
            t = str(r or "").strip()
            if t and t not in seen:
                seen.append(t)
        return _ANCHOR_JOINER.join(seen) or None

    def genon_anchor_field_present(self, grade) -> bool:
        """Does this constitution define a `section_anchor` field on the period? NO.

        The other side of `genon_unit_anchor` above: that method says WHERE the anchor is,
        this one says the declared field is absent at all — a caller that needs to WORD
        something cannot read it off the other, because a mediated anchor and a declared
        one are indistinguishable once `unit_anchor` has returned a string.

        WHAT IT CHANGES. `variant_plans.top_brief_for` asks it before writing the standard
        canonical's synthesis mandate. Where the field exists the mandate is the reserved
        token `synthesis` in it; here there is no field to put a token in, so the mandate is
        the explicit `"synthesis": true` boolean instead — the carrier `carriers.is_synthesis`
        has read all along. Without this the brief would ask a TWAU generation, at metered
        STEP 1, for a field its constitution never defines, and the certifier's synthesis
        gate would then find no synthesis unit in the library it had already paid for.

        NOT a licence to emit `section_anchor` here."""
        return False

    def genon_item_anchor_family(self, grade) -> str:
        """The 8-rule table's family column (base.py). TWAU preparatory is **row 8**,
        item-self-sufficient: the item carries `period_ref[]` directly and its own inline
        `implied_lo`. Declared rather than inferred, so `item_anchor_is_derived` answers
        False and `top_brief_for` does not ask for a synthesis handoff row this stage has
        no use for."""
        return "item"
