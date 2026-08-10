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
from ...genon.carriers import is_synthesis as _is_synth   # the token OR the boolean (S7)
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
                # The composite test comes FIRST and does not depend on `title` being empty.
                # A multi-section unit is often routed by the handoff under ONE of its
                # sections, which supplies that section's title — p09 U1 anchors "4.1 / 4.2"
                # and was labelled "Visualising Identities", silently hiding that Introduction
                # is taught in the same sitting. A single section's name is the wrong name for
                # a unit teaching several.
                if _is_synth(p):
                    # CAPITALISED FOR DISPLAY (2026-08-10, S7). The founder ruling above
                    # stands untouched — the closing unit keeps the NAME "synthesis" rather
                    # than a title-derived label — but `section_anchor` carries the reserved
                    # TOKEN, and printing a token verbatim put a lowercase heading among
                    # capitalised ones on the teacher's screen. Only the presentation
                    # changes: same word, same unit, same data, and the token is untouched
                    # everywhere it is actually read (serve, the registry, certification).
                    # Now agrees with the mediated-anchor stages, which reached "Synthesis"
                    # from the boolean in the branch below.
                    label = "Synthesis"
                elif _ANCHOR_JOINER in key:
                    label = group_label_from_unit(p.get("activity_title")) or key
                else:
                    label = title or key
                bands = p.get("time_bands")
                gmeta = {"section_anchor": key, "section_title": title}
            else:
                seg = (p.get("textbook_segments") or [{}])[0]
                # THE SYNTHESIS UNIT IS ITS OWN GROUP (2026-08-10, S7). On a token stage the
                # anchor IS the word, so maths·IX files its closer under "synthesis" without
                # anyone doing anything. A mediated-anchor stage has no token, and this branch
                # read `textbook_segments[0]` — so ch 7's whole-chapter synthesis, which
                # correctly lists all five sections it draws together, was filed under
                # "Equilateral Triangles (Revisit)": the first section it names, marked as a
                # repeat. The unit was right and the brief was obeyed; only the grouping was
                # wrong. Read the fact through the seam, as every other synthesis-aware site
                # now does.
                if _is_synth(p):
                    key, seg = "synthesis", {}
                else:
                    key = str(seg.get("ref", "")) or "lesson"
                # Same founder rule for MIDDLE: title alone ("Simple Expressions", not
                # "section 2.1 — Simple Expressions"); the ref stays in meta + key, and is
                # the label only when the segment has no title.
                label = ("Synthesis" if key == "synthesis" else
                         str(seg.get("title") or "").strip()
                         or str(seg.get("ref") or "") or "Lesson")
                # BOTH KEYS, newest first (2026-08-10, S7's P3). The middle constitution
                # emitted `phases[{minutes, description}]` until LP v3.4 renamed it to
                # `time_bands[{minutes, activity}]` — the rename `compile.py` requires, since
                # it rebuilds the timed spine from `time_bands` and asserts an inventory
                # invariant over `activity`. Reading only `phases` left every unit of a
                # v3.4-authored canonical with an EMPTY timed spine: no band text, no minutes
                # in the marginal rail, only the bare textbook-item lines. The whole existing
                # middle/preparatory corpus is still `phases`, so both must be read — the same
                # tolerance the secondary branch above and the prototype's renderer already
                # have (`lp_pdf_generator.py:2594-2609`: "Accept whichever is present").
                # `phases_from` and `band_lines` already read either text key.
                bands = p.get("time_bands") or p.get("phases")
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
        # The synthesis unit is excluded from the join, for the reason
        # `genon/carriers.py::items_by_period_field` records at length (2026-08-10, S7): it
        # teaches no section, and on this stage it declares the sections it REVISITS, so
        # indexing it makes the closing unit the last unit of every section and every item
        # anchors there. The display side must agree with the platform stamp, or a canonical
        # read straight from disk would anchor differently from the same plan served.

        periods = [p for p in periods if not _is_synth(p)]
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
        default (True) and changes no behaviour.

        SECONDARY puts the anchor in `section_anchor` (LP A3), which is the field
        `carriers.unit_anchor` and the whole serve arithmetic read — so genon works on it
        as-is.

        MIDDLE and PREPARATORY have a section axis but DO NOT USE THAT FIELD NAME:
        `grep -c section_anchor` is 0 in both constitutions. Middle carries
        `textbook_segments[].ref`, preparatory carries `section_refs[]` (which is also why
        their assessment join is the period-field family, rows 4 and 5).

        THE CHOICE THAT SENTENCE USED TO PUT TO S7/S8 IS MADE (founder ruling, 2026-08-10):
        **mediate the read; do not rename the field.** No new field may be invented to feed
        the serve engine — everything is derived from what the authored file already carries,
        which is what the prototype did at its own read boundary. `genon_unit_anchor` below
        is that mediation, and `carriers.unit_anchor` asks it before it decides an anchor is
        missing. Flipping this to False remains forbidden for the reason it always was: it
        would tell the engine these chapters have no sections, which is untrue, and would
        silently disable the section arithmetic their serve depends on."""
        return True

    def genon_unit_anchor(self, period, grade=None):
        """This period's section anchor, in the field THIS stage's constitution uses.

        Read VERBATIM and joined with `carriers._ANCHOR_JOINER`, in authored order, deduped.
        Verbatim is the whole point: certification compares the anchor against the registry
        drawn from the chapter summary's own `sections[].ref`, and both sides are the string
        "section 7.1" — so they match by construction, and any reformatting here (dropping
        the word "section", padding, re-casing) would manufacture a mismatch that then needs
        a second normalizer to undo. A unit teaching two sections reads
        "section 5.3 / section 5.4", the same multi-section join secondary's own anchors use.

          MIDDLE       `textbook_segments[].ref`
          PREPARATORY  `section_refs[]`

        Branching is on the PERIOD's shape, not on `stage_for(grade)` — `grade` is passed
        for symmetry with the other genon hooks and is deliberately not required, because
        this is called from `compile.py` where the grade comes off the enclosing plan and
        can be absent (the same trap `genon_assessment` documents below).

        SECONDARY never reaches here: `carriers.unit_anchor` returns `section_anchor`
        directly when the period has one.

        PREPARATORY's branch is written because the field is known and the code is the same
        three lines — but preparatory is STILL in `carriers._NOT_YET` (its assessment family,
        row 5, is owed by S8), so no preparatory plan can reach compile in the first place.
        Treat this branch as unexercised until S8 certifies it.
        """
        refs = [str(s.get("ref") or "").strip()
                for s in (period.get("textbook_segments") or []) if isinstance(s, dict)]
        if not any(refs):
            refs = [str(x or "").strip() for x in (period.get("section_refs") or [])]
        seen = []
        for r in refs:
            if r and r not in seen:
                seen.append(r)
        return _ANCHOR_JOINER.join(seen) or None

    def genon_anchor_field_present(self, grade) -> bool:
        """Does THIS stage's constitution define a `section_anchor` field on the period?

        SECONDARY yes (LP A3). MIDDLE and PREPARATORY no — `grep -c section_anchor` is 0
        in both, which is precisely why `genon_unit_anchor` above exists. Same fact, other
        side: that method says WHERE the anchor is when the field is absent, this one says
        that it is absent at all, and a caller that needs to WORD something cannot read it
        off the other (a mediated anchor and a declared one are indistinguishable once
        `unit_anchor` has returned a string).

        WHAT IT CHANGES (2026-08-10, S7). `variant_plans.top_brief_for` asks it before it
        writes the standard canonical's synthesis mandate. Where the field exists the
        mandate is the reserved token `synthesis` in it; here there is no field to put a
        token in, so the mandate is the explicit `"synthesis": true` boolean instead — the
        same carrier science·middle already uses, and the one `carriers.is_synthesis` has
        read all along. Without this the brief would have asked a maths·middle generation,
        at metered STEP 1, for a field its constitution never defines, and the certifier's
        synthesis gate would then have found no synthesis unit in the library it paid for.

        NOT a licence to emit `section_anchor` here: the founder ruling of 2026-08-10
        stands (nothing new may be added to a constitution to feed the serve engine). This
        method reports the constitution as it is; it never asks it to change.
        """
        return stage_for(grade) == "secondary"

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

          • MIDDLE — 8-rule ROW 4, the PERIOD-FIELD family, landed 2026-08-10 (S7): items
            are nested inside A/B/C section GROUPS (`[{section_code, section_title, note,
            items:[…]}, …]`), each leaf carrying a `section_ref` ("section 5.2"), and the
            join is that code against the PERIOD's own `textbook_segments[].ref`. No
            `coverage_handoff` is in the path and there is no LO. It delegates to
            `carriers.items_by_period_field`, which runs `link_resolver`'s
            `period_field_index` / `norm_code` — the identical mechanics `_middle_assess`
            above uses for the display side, so the two can never drift. Anchoring is the
            same 2026-08-05 ruling: the section's LAST unit.

          • PREPARATORY (row 5) — the same family on a different field
            (`section_refs[]`) and a different item vocabulary (`intent`, not `goal`). Owed
            by S8, so it still RAISES rather than borrowing middle's field or secondary's
            join, either of which would anchor every item through a rule that is not theirs.

        The stage is told apart by CONTAINER SHAPE, not by `stage_for(grade)` — this method
        receives only `result`, and the grade lives on the enclosing saved PLAN, so a grade
        read here is `None` on the very call the carrier makes (found by
        `tests/test_genon_carriers.py` the moment this landed). Science's `genon_assessment`
        branches on shape for the same reason. The shapes are unambiguous: secondary wraps
        its questions in a dict (A1); middle and preparatory both emit section groups
        carrying `items[]`, and are then separated the way the prototype's
        `_regroup_middle_maths_by_section` separates them — MIDDLE items carry `goal` and no
        `intent`, PREPARATORY items carry `intent`.
        """
        from ...genon.carriers import (CarrierNotImplemented, item_groups,
                                       items_by_handoff, items_by_period_field)

        raw = result.get("assessment_items")
        if isinstance(raw, dict) and "questions" in raw:            # SECONDARY — row 6
            return items_by_handoff(result, items=raw.get("questions") or [],
                                    join_key="section_number",
                                    handoff_key="section_number")

        groups = item_groups(raw)
        if groups is not None:
            flat = [it for g in groups for it in g["items"] if isinstance(it, dict)]
            if any("intent" in it for it in flat) or not any("goal" in it for it in flat):
                raise CarrierNotImplemented(
                    "mathematics preparatory is 8-rule ROW 5 — the period-field family on "
                    "`section_refs[]`, with `intent`-carrying items. Owed by S8. It must "
                    "not borrow middle's row 4 (a different period field) or secondary's "
                    "row 6 (a different family entirely). This branch also catches a "
                    "MIDDLE file whose items carry no `goal`, which is a defect worth "
                    "failing on rather than guessing past."
                )
            return items_by_period_field(                            # MIDDLE — row 4
                result, items=flat, item_key="section_ref",
                extract=lambda p: [s.get("ref", "")
                                   for s in (p.get("textbook_segments") or [])
                                   if isinstance(s, dict)])

        raise CarrierNotImplemented(
            "mathematics: `assessment_items` is neither the secondary `{…, questions: []}` "
            "wrapper (row 6) nor the middle/preparatory list of section groups carrying "
            "`items[]` (rows 4 and 5). A SECONDARY plan lands here if its items are not "
            "under the wrapper A1 mandates — which is itself a defect worth failing on."
        )
