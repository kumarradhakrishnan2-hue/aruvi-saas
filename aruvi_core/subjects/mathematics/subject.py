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
from ...assessment_norm import from_maths
from ...grades import stage_for
from ...link_resolver import (
    handoff_period_index, norm_code, period_field_index, platform_anchor, stamp,
)
from ...genon.serve import _ANCHOR_JOINER          # " / " — the V2 multi-section join
from ...normalize import (
    as_list, band_lines, classify_stimulus, normalize_options, phases_from, text_lines, group_label_from_unit,
)
from ...ports import Prompt
from ...view_model import (
    AssessmentGroup, AssessmentItem, AssessmentView, Group, LessonPlanView, Period,
)


def _hw_line(it: Any) -> str:
    """One homework display line. Middle/prep homework items are dicts carrying a
    `book_ref` (which itself holds the section + page, e.g. "Figure it Out Q8,
    section 5.1 p.111") alongside the `description` — keep BOTH so the teacher can
    locate the task, appending the locator when it is not already inside the text.
    Secondary homework items are plain strings with the page baked in — passed through
    untouched. (Fixes the dropped page/section locator; see MEMORY 'amendments to be tested'.)
    The locator is wrapped in `**…**` (markdown bold) so the renderers can weight the reference
    on its own — the teacher's eye lands on "where in the book" without re-reading the task."""
    if isinstance(it, dict):
        desc = str(it.get("description") or it.get("text") or "").strip()
        ref = str(it.get("book_ref") or "").strip()
        if ref and desc:
            return desc if ref in desc else f"{desc} (**{ref}**)"
        return f"**{ref}**" if ref and not desc else desc
    return str(it).strip()


def _hw(v: Any) -> str:
    if isinstance(v, list):
        return "; ".join(line for line in (_hw_line(it) for it in v) if line)
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
        lp = raw.get("lesson_plan", raw)
        periods = lp.get("periods", [])
        secondary = stage_for(grade) == "secondary"
        # SECONDARY section titles live in the result-level coverage_handoff (one entry per
        # section: section_ref + section_title + period_numbers), NOT on the period — the
        # period carries only the bare anchor ("2.1"). Rejoin here so the group label reads
        # "2.1 — Introduction" instead of a naked number: period_number-primary with an
        # anchor fallback, the same join the prototype's app.py maths-secondary branch and
        # this repo's science._secondary_lp_groups already use. (Callers pass the FULL saved
        # result, per the §3e LP-standard rule, so the handoff is present here.)
        ho_by_period: Dict[Any, Dict[str, Any]] = {}
        ho_by_ref: Dict[str, Dict[str, Any]] = {}
        if secondary:
            for e in (raw.get("coverage_handoff") or lp.get("coverage_handoff") or []):
                if not isinstance(e, dict):
                    continue
                for pn in (e.get("period_numbers") or []):
                    ho_by_period[pn] = e
                ref = str(e.get("section_ref") or e.get("section_label") or "")
                if ref:
                    ho_by_ref[ref] = e
        # Group by CONTIGUOUS RUNS of the same section, never a first-appearance merge:
        # secondary plans deliberately RETURN to a section later (ix ch_02: 2.3 at periods
        # 3 and 9, 2.6 at 6–8 and 10 — teach, then revisit/consolidate). A dict-merge pulled
        # the revisit up next to the first visit, so the flattened Learning-Unit rail (and
        # the pointer!) read 1,2,3,9,4,… — the prototype renders periods[] flat in
        # period_number order, and that teaching order is the contract (founder 2026-07-14).
        # A revisited section simply appears as its own group again.
        groups: List[Group] = []
        prev_key: Any = object()  # sentinel ≠ any real key
        seen_keys: set = set()    # anchors already opened once — a re-opening is a REVISIT
        for p in periods:
            if secondary:
                key = str(p.get("section_anchor", ""))
                ho = ho_by_period.get(p.get("period_number")) or ho_by_ref.get(key) or {}
                title = str(ho.get("section_title") or "").strip()
                # Founder rule 2026-07-14: the section NUMBER is noise in the label — show the
                # name alone ("Introduction", not "2.1 — Introduction"); the anchor is kept in
                # meta (and remains the grouping key) and shows only when no title exists.
                #
                # A unit spanning several sections anchors on a JOIN ("4.6 / 4.7 / 4.8"),
                # which no handoff row is keyed by — so the title lookup missed and the bare
                # refs reached the screen, the exact thing the rule above forbids. The model
                # has already written a teacher-facing name for that unit, so use it,
                # shortened, rather than inventing vocabulary (founder 2026-08-09).
                #
                # SYNTHESIS IS DELIBERATELY EXCLUDED (founder, same day): the closing unit
                # keeps the name "synthesis". It is the one reserved word teachers should
                # meet as itself, and it is stable across every chapter, where a title-derived
                # label would differ each time.
                if not title and _ANCHOR_JOINER in key:
                    label = group_label_from_unit(p.get("activity_title")) or key
                else:
                    label = title or key
                bands = p.get("time_bands")
                gmeta = {"section_anchor": key, "section_title": title}
            else:
                seg = (p.get("textbook_segments") or [{}])[0]
                key = str(seg.get("ref", "")) or "lesson"
                # Same founder rule for MIDDLE: title alone ("Simple Expressions", not
                # "section 2.1 — Simple Expressions"); the ref stays in meta + key, and is
                # the label only when the segment has no title.
                label = str(seg.get("title") or "").strip() or str(seg.get("ref") or "") or "Lesson"
                bands = p.get("phases")
                gmeta = {"ref": seg.get("ref", "")}
            if key != prev_key:
                # A section re-opened later in the plan is intentional (consolidation /
                # deferred depth — see MEMORY 2026-07-14). Say so on the label, so the
                # teacher reads the repeat as deliberate, not a mistake (founder 2026-07-14).
                if key in seen_keys:
                    label = f"{label} (Revisit)"
                    gmeta["revisit"] = True
                groups.append(Group(type="section", label=label, meta=gmeta))
                prev_key = key
                seen_keys.add(key)
            groups[-1].periods.append(Period(
                number=p.get("period_number", 0),
                title=p.get("activity_title", ""),
                approach=p.get("pedagogical_method", ""),   # absent in preparatory saves
                activities=text_lines(p.get("textbook_items_in_class")) + band_lines(bands),
                phases=phases_from(bands),
                materials=as_list(p.get("materials")),
                teacher_notes=as_list(p.get("teacher_notes")),
                homework=_hw(p.get("homework")),
                meta={"section_goal": p.get("section_goal", ""),
                      "pedagogical_method": p.get("pedagogical_method", ""),
                      "materials": p.get("materials", ""),
                      "visual_aids": p.get("visual_aids", ""),
                      # Prep has NO section axis (all periods collapse to a single "Lesson"
                      # group), so the renderer's Overview "Section" row would otherwise read
                      # "Lesson" for every unit. Carry the period's OWN anchored section — the
                      # proxy for the axis — so the Overview shows the real section it covers
                      # (titles preferred, S-codes as fallback). Empty for middle/secondary,
                      # where the group label already IS the section and the renderer falls
                      # back to it.
                      "section_label": " · ".join(p.get("section_titles") or [])
                                       or " · ".join(p.get("section_refs") or []),
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
                # Platform stamp first, section-code join as fallback (ARV-D-064).
                stamp(meta, platform_anchor(it) or period_index.get(norm_code(ref), []),
                      None)  # rules 4/5: no LO
                g.items.append(AssessmentItem(
                    prompt=it.get("prompt", ""),
                    item_type=it.get("question_type", ""),
                    options=options, answer=answer,
                    teacher_guide=as_list(it.get("teacher_guide")),
                    visual_stimulus=classify_stimulus(it.get("visual_stimulus", "")),
                    meta=meta,
                    normalized=from_maths(it, meta),  # the §2 uniform contract (3b reads this)
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
            # Platform stamp first, section-number join as fallback (ARV-D-064).
            linked = platform_anchor(q) or (
                period_index.get(int(sn), []) if sn is not None else [])
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
                normalized=from_maths(q, meta),  # the §2 uniform contract (3b reads this)
            ))
        return out

    # ── genon: the carrier seam (aruvi_core/genon/carriers.py) ───────────────────
    def genon_has_section_axis(self, grade) -> bool:
        """All three stages anchor units to textbook sections, so this returns the platform
        default (True) and changes no behaviour. It exists to carry a warning to S7/S8.

        SECONDARY puts the anchor in `section_anchor` (LP A3), which is the field
        `carriers.unit_anchor` and the whole serve arithmetic read — so genon works on it
        as-is.

        MIDDLE and PREPARATORY have a section axis but DO NOT USE THAT FIELD NAME:
        `grep -c section_anchor` is 0 in both constitutions. Middle carries
        `textbook_segments[].ref`, preparatory carries `section_refs[]` (which is also why
        their assessment join is the period-field family, rows 4 and 5). So returning True
        here is honest about the axis but leaves `unit_anchor` raising KeyError on their
        periods — the same wall science·middle hit at S6, for a different reason: science
        middle has no axis, maths middle has one under another name.

        S7/S8 must therefore pick deliberately, and it is a founder call, not a default:
        rename the field in those constitutions (the P3-style answer — amend the
        constitution, do not teach the compiler an adapter), or mediate the read the way
        `unit_anchor` already mediates its absence. Do NOT resolve it by flipping this to
        False; that would tell the engine these chapters have no sections, which is untrue
        and would silently disable the section arithmetic their serve depends on."""
        return True

    def genon_item_anchor_family(self, grade) -> str:
        """The 8-rule table's family column (base.py). SECONDARY is row 6, handoff-bridged.
        MIDDLE (row 4) and PREPARATORY (row 5) are the period-field family — declared here
        even though genon cannot reach them yet, so the fact lives in one place."""
        return "handoff" if stage_for(grade) == "secondary" else "period_field"

    def genon_assessment(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """The genon door onto this subject's rows of the verified 8-rule table.

        Nothing is decided here. `_secondary_assess` above already runs the stage's rule
        for the app; genon needs the SAME rule applied to the RAW item dicts (options,
        `is_correct`, guide, `visual_stimulus` intact — served files and exports read
        them), where `assessment_to_view` returns display objects. So this method restates
        the row's two keys and delegates.

          • SECONDARY — 8-rule ROW 6, handoff-bridged: items live under
            `assessment_items["questions"]`, each carrying an integer `section_number`;
            bridge it through `coverage_handoff`'s `section_number` to `period_numbers`.
            NEVER match `section_anchor`/`section_ref` TEXT — labels are merged strings
            that differ between a chapter's canonicals, and two sections can share one
            (link_resolver.py records why). Anchoring is the section's LAST unit, per the
            2026-08-05 ruling, and `items_by_handoff` applies it — an item tests the
            section's whole `implied_lo`, so it becomes available only when the section
            completes. Identical in every argument to science·secondary's row 2, which is
            why this is a delegation and not a join.

          • MIDDLE (row 4) and PREPARATORY (row 5) — the PERIOD-FIELD family: the item's
            `section_ref` matches the period's own field (`textbook_segments[].ref` at
            middle, `section_refs[]` at preparatory), with no handoff in the path at all.
            A different family, owed by S7/S8, so it RAISES rather than silently borrowing
            secondary's join — which would anchor every item through a rule that is not
            theirs. `_middle_assess` has the display-side logic to delegate to when those
            stages arrive; it needs `ctx["periods"]`, which this seam does not yet pass.

        The stage is told apart by CONTAINER SHAPE, not by `stage_for(grade)` — this method
        receives only `result`, and the grade lives on the enclosing saved PLAN, so a grade
        read here is `None` on the very call the carrier makes (found by
        `tests/test_genon_carriers.py` the moment this landed). Science's `genon_assessment`
        branches on shape for the same reason. The shapes are unambiguous: secondary wraps
        its questions in a dict (A1), middle and preparatory emit section groups carrying
        `items[]`.
        """
        from ...genon.carriers import CarrierNotImplemented, items_by_handoff

        raw = result.get("assessment_items")
        if isinstance(raw, dict) and "questions" in raw:            # SECONDARY — row 6
            return items_by_handoff(result, items=raw.get("questions") or [],
                                    join_key="section_number",
                                    handoff_key="section_number")

        raise CarrierNotImplemented(
            "mathematics middle/preparatory is the PERIOD-FIELD family (8-rule rows 4 and "
            "5): the item's section_ref matches the period's OWN field "
            "(textbook_segments[].ref at middle, section_refs[] at preparatory), with no "
            "coverage_handoff in the path. Owed by S7/S8 — implement it by delegating to "
            "the display-side join in _middle_assess, never by reusing row 6, which would "
            "anchor every item through a rule that is not theirs. (This branch is also "
            "where a SECONDARY plan lands if its items are not under the `questions` "
            "wrapper A1 mandates — which is itself a defect worth failing on.)"
        )
