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
from ...assessment_norm import from_constitution
from ...grades import stage_for
from ...link_resolver import (handoff_period_index, period_number_by_field,
                              platform_anchor, stamp)
from ...normalize import (as_list as _as_list, classify_stimulus, normalize_options,
                          parse_table, phases_from, SYNTHESIS_DISPLAY)
from ...genon.carriers import is_synthesis as _is_synth   # token OR boolean (S7)
from ...ports import Prompt
from ...view_model import (
    AssessmentGroup, AssessmentItem, AssessmentView, Group, LessonPlanView, Period,
)


def _typed_visual_aids(raw: Any):
    """Normalize `visual_aids` to what the renderer consumes (polish pass, 2026-08-18).

    Legacy shape is a plain STRING (a textbook-figure reference) — passed through
    unchanged. The polished synthesis units carry a LIST of typed entries
    ({type: table|prose, title, table|text}); table payloads are split HERE through
    normalize.parse_table — the single splitter every renderer shares — so no consumer
    ever re-splits the raw pipe string (the recurring drift-bug class its docstring
    records)."""
    if not isinstance(raw, list):
        return raw or ""
    out = []
    for va in raw:
        if not isinstance(va, dict):
            continue
        if va.get("type") == "table" and va.get("table"):
            out.append({"type": "table", "title": va.get("title", ""),
                        "table": parse_table(va["table"])})
        elif va.get("type") == "prose" and va.get("text"):
            out.append({"type": "prose", "title": va.get("title", ""),
                        "text": va["text"]})
    return out


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

    # ── genon: how each stage is served (base.py; docs/science_middle_stage_serve.md) ──
    def genon_serve_granularity(self, grade) -> str:
        """SECONDARY serves at UNIT granularity like every other stage — its LP Rule 1
        anchors each activity to a named chapter section, so the standard X-1+1 fill and
        its section arithmetic apply unchanged.

        MIDDLE serves at PLAN granularity, and is the only stage in the corpus that does.
        Its LP is organised by the chapter's COGNITIVE PROGRESSION ARC (LP Rule 1): units
        belong to arc stages, a stage's implied LO is the outcome of the COMPLETE stage
        (Rule 5) and its assessment items test that LO. So a prefix of a canonical is not
        a plan — truncating mid-stage would test a class on an operation it was taught
        part of, with no honest way to declare what is missing. Truncation dies, and
        borrowing with it. Serving is whole-canonical selection; the only bridge between
        two counts is the top canonical's single synthesis unit (founder, 2026-08-07)."""
        return "plan" if stage_for(grade) == "middle" else "unit"

    def genon_group_fields(self, grade) -> tuple:
        """MIDDLE groups its periods by progression stage, so those two fields say which
        group a unit belongs to. A unit borrowed into a foreign plan must ADOPT its host's
        values for them (ARV-D-067): the top's synthesis unit carries `progression_stage: 6`
        from a six-stage arc, and served into an 8-unit variant with five stages it invented
        a sixth. SECONDARY groups by section_anchor, which the serve engine already handles
        and which never travels this path."""
        return ("progression_stage", "stage_label") if stage_for(grade) == "middle" else ()

    def genon_has_section_axis(self, grade) -> bool:
        """Middle has none: the arc rides over the whole chapter summary and is derived
        fresh at generation time, so its units carry no `section_anchor` — by design, not
        by omission. Secondary anchors every activity to a section (LP Rule 1)."""
        return stage_for(grade) != "middle"

    def genon_item_anchor_family(self, grade) -> str:
        """The 8-rule table's family column (base.py). Science is handoff-bridged at BOTH
        stages — secondary joins `section_number` (row 2), middle joins `progression_stage`
        (row 1) — which `genon_assessment` below already encodes. Declared separately
        because the family has a consequence the join does not: a derived anchor means the
        standard's closing synthesis unit needs its own handoff row or nothing can be
        anchored to it (see `carriers.item_anchor_is_derived`)."""
        return "handoff"

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

        # Group by CONTIGUOUS RUNS of the same anchor, never a first-appearance merge:
        # secondary plans deliberately RETURN to a section later (science ix ch_02 revisits
        # §2.3.1 at period 10, after 2.4/2.5). A dict-merge pulled the revisit up next to the
        # first visit, reordering the flattened Learning-Unit rail (and the pointer) away from
        # the plan's own period_number teaching sequence — that sequence is the contract
        # (founder 2026-07-14; found on maths secondary, same fix in mathematics/subject.py).
        groups: List[Group] = []
        prev_anchor: Any = object()  # sentinel ≠ any real anchor
        seen_anchors: set = set()    # anchors already opened once — a re-opening is a REVISIT
        for p in periods_raw:
            anchor = str(p.get("section_anchor", "")) or "Section"
            if anchor != prev_anchor:
                ho = ho_by_period.get(p.get("period_number")) or ho_by_label.get(anchor) or {}
                lo = ho.get("implied_lo")
                if isinstance(lo, list):
                    lo = " ".join(str(x).strip() for x in lo if x)
                # A section re-opened later in the plan is intentional (consolidation /
                # deferred depth). Say so on the label, so the teacher reads the repeat
                # as deliberate, not a mistake (founder 2026-07-14; same in mathematics).
                revisit = anchor in seen_anchors
                groups.append(Group(
                    type="section",
                    # The closing synthesis reads as a proper heading, never as the
                    # reserved token verbatim (2026-08-10, S7 — see normalize.
                    # SYNTHESIS_DISPLAY). It can never be a "(Revisit)" either: it is
                    # the one unit of the plan that anchors no section.
                    label=(SYNTHESIS_DISPLAY if _is_synth(p)
                           else f"{anchor} (Revisit)" if revisit else anchor),
                    meta={"section_context": ho.get("section_context", ""),
                          "implied_lo": lo or "",
                          **({"revisit": True} if revisit else {})},
                ))
                prev_anchor = anchor
                seen_anchors.add(anchor)
            groups[-1].periods.append(self._period_from(p))
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
                  "visual_aids": _typed_visual_aids(p.get("visual_aids")),
                  "duration_minutes": p.get("period_duration_minutes")},
        )

    def genon_assessment(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """The genon carrier seam (aruvi_core/genon/carriers.py) — Science is
        HANDOFF-BRIDGED at both stages, and the container shape differs by stage:

          • SECONDARY — items live under `assessment_items["questions"]`, each carrying
            `section_number`; bridge it through coverage_handoff's `section_number`.
          • MIDDLE    — items are a flat list, each carrying `progression_stage`;
            bridge it through coverage_handoff's `stage_number`.

        Same two facts `assessment_to_view` above already encodes — stated once more here
        because genon needs the RAW item dicts (options, is_correct, guide, visual_stimulus
        intact, for served files and exports), where the view model returns display objects.
        Anchoring is the section's LAST unit, per the 2026-08-05 ruling.
        """
        from ...genon.carriers import items_by_handoff

        raw = result.get("assessment_items")
        if isinstance(raw, dict) and "questions" in raw:          # secondary
            return items_by_handoff(result, items=raw.get("questions") or [],
                                    join_key="section_number",
                                    handoff_key="section_number")
        items = raw if isinstance(raw, list) else (                # middle
            (raw or {}).get("assessment_items") or [])
        return items_by_handoff(result, items=items,
                                join_key="progression_stage",
                                handoff_key="stage_number")

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
        by_group: Dict[Any, AssessmentGroup] = {}
        for it in items or []:
            gnum = it.get(join_key)
            # GROUP ON THE ITEM'S OWN LABEL, not on the mediating number (ARV-D-064).
            # This used to key on `gnum` and take the heading from the FIRST item to
            # claim that number. A borrowed unit's question carries the lender's
            # numbering, so it was filed under whatever the host plan calls that number
            # — a question about 8.2.2 sitting under a heading reading "8.2.3 Bohr's
            # model". The item carries its own true `section_label`; use it. For plans
            # that never borrow this is identical grouping (one label per number), and
            # the number is still reported in the group's meta.
            glabel = it.get(group_label) or f"{'Section' if secondary else 'Stage'} {gnum}"
            gkey = glabel
            if gkey not in by_group:
                g = AssessmentGroup(
                    type="progression_stage" if not secondary else "section",
                    label=glabel,
                    meta={group_key: gnum},
                )
                by_group[gkey] = g
                groups.append(g)
            guide = (_as_list(it.get("look_for")) + _as_list(it.get("expected_elements"))
                     + _as_list(it.get("scaffold")) + _as_list(it.get("format_of_output")))
            options, answer = normalize_options(it.get("options"))
            lo = it.get("implied_lo_assessed", "")
            meta = {"competency": it.get("competency", {}),
                    "cognitive_demand": it.get("cognitive_demand", "")}
            # The platform's stamp wins; the handoff join is the fallback for an
            # un-served library file (link_resolver.platform_anchor — ARV-D-064).
            linked = platform_anchor(it) or (
                period_index.get(int(gnum), []) if gnum is not None else [])
            stamp(meta, linked, lo)
            by_group[gkey].items.append(AssessmentItem(
                prompt=it.get("question_text") or it.get("task", ""),
                item_type=it.get("question_type", ""),
                options=options,
                answer=answer,
                teacher_guide=guide,
                implied_lo=lo,
                visual_stimulus=classify_stimulus(it.get("visual_stimulus", "")),
                meta=meta,
                normalized=from_constitution(it, meta),  # the §2 uniform contract (3b reads this)
            ))
        return AssessmentView(
            subject="science", grade=grade,
            chapter_number=chapter.get("chapter_number", 0),
            chapter_title=chapter.get("chapter_title", ""),
            groups=groups,
        )
