"""The genon carrier seam — every subject's real saved plan, run through compile.

WHY (2026-08-05, S3 · science · secondary stage prep). `compile.py` used to read
`result["assessment_items"]` directly and assume a flat list of item dicts. That holds
for Social Sciences and TWAU and for nothing else: Science secondary wraps its items
under a "questions" key, so iterating the wrapper yielded its KEY NAMES as strings — a
canonical that compiled clean with ZERO questions, and `normalize_options` then dying on
`'str' object has no attribute 'get'`. Genon had only ever run on Social Sciences, so the
assumption was invisible. carriers.py routes genon through the subject plugin, exactly as
the app has always done (CLAUDE.md §3).

This suite is the cheap half of that fix: it runs every subject's parity fixture through
the seam TODAY, so the remaining stages don't each rediscover their own version of the
bug at generation cost. Stdlib only; run directly.
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aruvi_core.genon.carriers import (          # noqa: E402
    CarrierNotImplemented, assessment_items, backfill_unit_context, from_engine_handoff,
    items_by_handoff, subject_key, to_engine_handoff, unit_approaches,
)

FIX = Path(__file__).resolve().parent / "fixtures"


def load(name):
    return json.loads((FIX / name).read_text(encoding="utf-8"))


class TestSubjectKey(unittest.TestCase):
    def test_display_names_map_to_registry_keys(self):
        self.assertEqual(subject_key("Social Science"), "social_sciences")
        self.assertEqual(subject_key("The World Around Us"), "the_world_around_us")
        self.assertEqual(subject_key("Science"), "science")
        self.assertEqual(subject_key("Mathematics"), "mathematics")
        self.assertEqual(subject_key("English"), "english")

    def test_unrecognisable_is_none_not_a_guess(self):
        self.assertIsNone(subject_key(""))
        self.assertIsNone(subject_key(None))
        self.assertIsNone(subject_key("Astrophysics"))


class TestItemSelfSufficientFamily(unittest.TestCase):
    """social_sciences + the_world_around_us: period_ref is an identity."""

    def _check(self, fixture):
        plan = load(fixture)
        result = plan.get("result", plan)
        items = assessment_items(plan, result)
        self.assertTrue(items, f"{fixture}: no items extracted")
        for it in items:
            self.assertIsInstance(it, dict, f"{fixture}: item is not a dict — the wrapper bug")
            self.assertIn("unit_ref", it)
            self.assertIsInstance(it["unit_ref"], list)
            self.assertLessEqual(len(it["unit_ref"]), 1,
                                 "anchoring is a singleton: the section's LAST unit")
        return items

    def test_ss_vi_ch06(self):
        self._check("ss_vi_ch06_saved.json")

    def test_ss_vii_ch04_edge(self):
        self._check("ss_vii_ch04_edge_saved.json")

    def test_twau_iii_ch01(self):
        self._check("twau_iii_ch01_saved.json")


class TestHandoffBridgedFamily(unittest.TestCase):
    """science: the container shape differs by stage, and both bridge on an integer."""

    def test_science_middle_flat_list(self):
        plan = load("science_vii_ch02_saved.json")
        result = plan.get("result", plan)
        items = assessment_items(plan, result)
        self.assertTrue(items)
        for it in items:
            self.assertIsInstance(it, dict)
            self.assertIn("unit_ref", it)

    def test_secondary_wrapper_is_unwrapped_not_iterated(self):
        """The exact bug: a {..., "questions": [...]} container must yield the QUESTIONS,
        never the wrapper's key names."""
        result = {
            "assessment_items": {
                "grade": "Grade IX", "subject": "science", "stage": "secondary",
                "chapter_number": 8, "chapter_title": "Journey Inside the Atom",
                "chapter_cg": "CG-1", "reasoning_floor_lift_applied": False,
                "questions": [
                    {"section_number": 1, "question_type": "MCQ", "question_text": "q1"},
                    {"section_number": 2, "question_type": "SCR", "question_text": "q2"},
                ],
            },
            "coverage_handoff": [
                {"section_number": 1, "period_numbers": [1]},
                {"section_number": 2, "period_numbers": [2, 3, 4]},
            ],
        }
        items = assessment_items({"subject": "Science"}, result)
        self.assertEqual(len(items), 2, "must be 2 questions, not 8 wrapper keys")
        self.assertEqual([it["question_text"] for it in items], ["q1", "q2"])
        for it in items:
            self.assertNotIsInstance(it, str)

    def test_multi_unit_section_anchors_to_its_LAST_unit(self):
        """The 2026-08-05 anchoring ruling: an item tests the whole section, so it
        becomes available only when the section completes."""
        result = {
            "assessment_items": {"questions": [{"section_number": 2}]},
            "coverage_handoff": [{"section_number": 2, "period_numbers": [2, 3, 4]}],
        }
        items = assessment_items({"subject": "Science"}, result)
        self.assertEqual(items[0]["unit_ref"], [4])

    def test_unresolvable_group_leaves_unit_ref_empty_for_compile_to_report(self):
        result = {
            "assessment_items": {"questions": [{"section_number": 9}]},
            "coverage_handoff": [{"section_number": 1, "period_numbers": [1]}],
        }
        items = assessment_items({"subject": "Science"}, result)
        self.assertEqual(items[0]["unit_ref"], [])

    def test_period_ref_is_the_fallback_for_legacy_files(self):
        result = {
            "assessment_items": {"questions": [{"section_number": 9, "period_ref": [5]}]},
            "coverage_handoff": [{"section_number": 1, "period_numbers": [1]}],
        }
        items = assessment_items({"subject": "Science"}, result)
        self.assertEqual(items[0]["unit_ref"], [5])

    def test_never_joins_on_anchor_TEXT(self):
        """link_resolver's hard-won rule: two sections can carry near-identical labels
        (ch 2's 'Organelles of the Cell' and '… (Nucleus sub-section)'), so the integer
        is the only safe join."""
        result = {
            "assessment_items": {"questions": [
                {"section_number": 6, "section_label": "Section 2.3.1 — Organelles of the Cell"},
                {"section_number": 7,
                 "section_label": "Section 2.3.1 — Organelles of the Cell (Nucleus sub-section)"},
            ]},
            "coverage_handoff": [
                {"section_number": 6, "period_numbers": [6, 10],
                 "section_label": "Section 2.3.1 — Organelles of the Cell"},
                {"section_number": 7, "period_numbers": [11],
                 "section_label": "Section 2.3.1 — Organelles of the Cell (Nucleus sub-section)"},
            ],
        }
        items = assessment_items({"subject": "Science"}, result)
        self.assertEqual([it["unit_ref"] for it in items], [[10], [11]])


class TestHandoffRoundTrip(unittest.TestCase):
    """serve remaps in ONE shape; a served plan must leave in the SUBJECT's shape, or
    the app's display path — which iterates science's handoff as a list — links nothing."""

    SCI = {"coverage_handoff": [
        {"section_number": 1, "section_label": "8.1 Roots", "total_sections": 2,
         "period_numbers": [1], "section_context": "ctx one", "c_code": "C-1.1"},
        {"section_number": 2, "section_label": "8.2 Models", "total_sections": 2,
         "period_numbers": [2, 3], "section_context": "ctx two", "c_code": "C-1.1"},
    ]}

    def test_array_becomes_a_dict_serve_can_walk(self):
        eng = to_engine_handoff(self.SCI)
        self.assertIsInstance(eng, dict)
        for blk in eng.values():                      # what serve.py actually does
            self.assertIsInstance(blk.get("los"), list)
            for lo in blk["los"]:
                self.assertIn("period_number", lo)

    def test_round_trip_is_lossless_and_keeps_order(self):
        back = from_engine_handoff(json.loads(json.dumps(to_engine_handoff(self.SCI))))
        self.assertEqual([h["section_label"] for h in back], ["8.1 Roots", "8.2 Models"])
        self.assertEqual([h["period_numbers"] for h in back], [[1], [2, 3]])
        self.assertEqual(set(self.SCI["coverage_handoff"][0]), set(back[0]))

    def test_no_engine_marker_leaks_into_a_served_plan(self):
        back = from_engine_handoff(to_engine_handoff(self.SCI))
        for h in back:
            self.assertNotIn("_carrier", h)
            self.assertNotIn("_entry", h)
            self.assertNotIn("_order", h)

    def test_keyed_on_the_LABEL_not_the_per_plan_section_number(self):
        """Two canonicals that cut differently can number the same section differently;
        the label is the verbatim registry anchor and is stable across them (V2)."""
        self.assertEqual(sorted(to_engine_handoff(self.SCI)), ["8.1 Roots", "8.2 Models"])

    def test_a_section_with_no_surviving_unit_is_dropped(self):
        eng = to_engine_handoff(self.SCI)
        eng["8.2 Models"]["los"] = []                 # serve filtered them all away
        back = from_engine_handoff(eng)
        self.assertEqual([h["section_label"] for h in back], ["8.1 Roots"])
        self.assertEqual(back[0]["total_sections"], 1, "recomputed for THIS plan")

    def test_block_shaped_families_pass_through_untouched(self):
        ss = {"coverage_handoff": {"C-1.1": {"cg": "CG-1", "los": [{"period_number": 2}]}}}
        self.assertEqual(to_engine_handoff(ss), ss["coverage_handoff"])
        self.assertEqual(from_engine_handoff(ss["coverage_handoff"]), ss["coverage_handoff"])


class TestUnitProjection(unittest.TestCase):
    def test_approach_is_read_under_all_three_spellings(self):
        self.assertEqual(unit_approaches({"pedagogical_approaches": ["A", "B"]}), ["A", "B"])
        self.assertEqual(unit_approaches({"pedagogical_approach": "Inquiry"}), ["Inquiry"])
        self.assertEqual(unit_approaches({"dominant_mode": "Hands-on Investigation"}),
                         ["Hands-on Investigation"])
        self.assertEqual(unit_approaches({}), [])

    def test_section_context_backfills_from_the_handoff(self):
        """Science secondary's LP Rule 6 FORBIDS section_context inside a period object,
        so reading it off the period leaves the served Overview blank."""
        units = [{"unit": 1, "section_context": None}, {"unit": 3, "section_context": None},
                 {"unit": 9, "section_context": "already here"}]
        backfill_unit_context(units, TestHandoffRoundTrip.SCI)
        self.assertEqual(units[0]["section_context"], "ctx one")
        self.assertEqual(units[1]["section_context"], "ctx two")
        self.assertEqual(units[2]["section_context"], "already here", "never overwritten")


class TestUnimplementedFamiliesFailLoudly(unittest.TestCase):
    """A subject·stage genon has never run on must REFUSE, not return something plausible.

    Keyed by subject·STAGE since 2026-08-08 (S4). It used to be per subject, which made
    `mathematics` a single entry spanning TWO families — handoff-bridged at secondary
    (row 6), period-field at middle/preparatory (rows 4/5) — so landing secondary would
    have silently declared the other two ready.
    """

    def test_a_middle_file_with_no_goal_on_any_item_refuses_rather_than_guessing(self):
        result = {
            "assessment_items": [{"section_code": "A",
                                  "items": [{"id": "Q1", "section_ref": "section 5.1"}]}],
            "lesson_plan": {"periods": [{"period_number": 1,
                                         "textbook_segments": [{"ref": "section 5.1"}]}]},
        }
        with self.assertRaises(CarrierNotImplemented):
            assessment_items({"subject": "Mathematics", "grade": "Grade VI"}, result)

    def test_an_owed_stage_still_refuses_even_though_the_table_is_now_empty(self):
        """`_NOT_YET` emptied at S9 (2026-08-13) — every campaign stage is carried.

        This test has been MOVED at every english removal rather than deleted: it ran on
        secondary until S11, middle until S10, and preparatory until S9. There is no owed
        stage left to point it at, so it now inserts a synthetic entry and proves the
        REFUSAL MACHINERY still works — which is the property that was ever under test.
        Without it, emptying the table would quietly retire the pre-flight, and the next
        subject·stage brought into genon would find out at certification, after paying.
        """
        import aruvi_core.genon.carriers as C
        self.assertEqual(C._NOT_YET, {}, "the campaign owes no carrier — S9 closed the last")

        plan = load("english_vii_ch01_saved.json")
        plan = dict(plan, grade="Grade III")
        saved = dict(C._NOT_YET)
        C._NOT_YET[("english", "preparatory")] = "synthetic — owed by SX (row 7)"
        try:
            with self.assertRaises(CarrierNotImplemented) as cm:
                assessment_items(plan, plan.get("result", plan))
            self.assertIn("english", str(cm.exception))
            self.assertIn("SX", str(cm.exception), "the gap names the stage that owes it")
        finally:
            C._NOT_YET.clear()
            C._NOT_YET.update(saved)

        # and the real table is genuinely open again afterwards
        self.assertIsNone(C.carrier_gap("english", "iii"))


class TestMathematicsSecondaryLanded(unittest.TestCase):
    """S4, 2026-08-08 — maths·secondary is 8-rule ROW 6, and it is a DELEGATION.

    The join already existed for the app (`_secondary_assess`); all that was missing was
    genon's door onto it (`genon_assessment`, which returns RAW item dicts rather than the
    display objects `assessment_to_view` builds). These tests pin the row, not the plumbing.
    """

    PLAN = None

    def setUp(self):
        self.plan = load("maths_ix_ch02_saved.json")
        self.result = self.plan.get("result", self.plan)

    def test_it_no_longer_raises(self):
        items = assessment_items(self.plan, self.result)
        self.assertTrue(items, "the fixture has questions; the seam must return them")

    def test_every_item_resolves_through_the_handoff_not_the_label(self):
        index = {int(h["section_number"]): [int(p) for p in h["period_numbers"]]
                 for h in self.result["coverage_handoff"]
                 if h.get("section_number") is not None}
        for it in assessment_items(self.plan, self.result):
            sn = it.get("section_number")
            if not isinstance(sn, int) or sn not in index:
                continue
            self.assertEqual(it["unit_ref"], [max(index[sn])],
                             "row 6 anchors at the section's LAST unit (2026-08-05 ruling)")

    def test_raw_item_fields_survive(self):
        """Genon needs the RAW dicts: served files and exports read these."""
        items = assessment_items(self.plan, self.result)
        self.assertTrue(
            any(("options" in it) or ("expected_answer" in it) or ("guide" in it)
                for it in items),
            "options / expected_answer / guide must not be stripped to display objects")

    def test_the_wrapper_that_caused_all_this_is_handled(self):
        """maths·secondary wraps items under `questions`, exactly like science·secondary —
        the shape whose mishandling created this whole module at S3."""
        self.assertIsInstance(self.result["assessment_items"], dict)
        self.assertIn("questions", self.result["assessment_items"])
        self.assertEqual(len(assessment_items(self.plan, self.result)),
                         len(self.result["assessment_items"]["questions"]))

    def test_the_seam_does_not_need_a_grade(self):
        """`genon_assessment` receives only `result`, and the grade lives on the enclosing
        PLAN — so a `stage_for(grade)` read here is None on the very call the carrier makes.
        The stage is told apart by container shape instead. This test is the regression."""
        self.assertIsNone(self.result.get("grade"), "fixture: grade is on the plan, not here")
        assessment_items(self.plan, self.result)          # must not raise UnknownGradeError


class TestMathematicsMiddleLanded(unittest.TestCase):
    """S7, 2026-08-10 — maths·middle is 8-rule ROW 4, the PERIOD-FIELD family's first stage.

    The item names a section ("section 5.2"), the period names the sections it teaches
    (`textbook_segments[].ref`), and the code itself is the join — no coverage_handoff
    anywhere in the path, no LO. `carriers.items_by_period_field` is that family, built on
    `link_resolver`'s `period_field_index`/`norm_code`, the same parity-tested mechanics the
    display side (`_middle_assess`) has always used.

    Fixture: the real saved plan `maths_vi_ch05_saved.json` — 10 periods over sections
    5.1–5.6, 11 items in three A/B/C groups.
    """

    def setUp(self):
        self.plan = load("maths_vi_ch05_saved.json")
        self.result = self.plan.get("result", self.plan)

    # ── the join itself ───────────────────────────────────────────────────────
    def test_every_item_resolves_to_exactly_one_unit_with_zero_orphans(self):
        items = assessment_items(self.plan, self.result)
        self.assertEqual(len(items), 11)
        for it in items:
            self.assertIsInstance(it, dict, "the group wrapper must be flattened, not iterated")
            self.assertEqual(len(it["unit_ref"]), 1,
                             f"{it.get('id')} did not anchor to exactly one unit")

    def test_an_item_anchors_where_its_HANDOFF_ANCHOR_is_first_worked(self):
        """REPLACES `…anchors_at_its_LAST_unit` (2026-08-19, ARV-D-181).

        The 2026-08-05 ruling — an item tests its section's whole goal, so hold it until
        the section closes — was right for a stage whose sections are topics and wrong for
        this one, where they are banners over a fortnight. It put 553 items on 37% of
        sittings at 2.8 apiece and cost a three-quarter-length serve 43% of its questions.
        The rule now: an item anchors where its handoff anchor is FIRST worked.

        This fixture shows the difference and shows it is an improvement, not a
        relabelling. Section 5.2 is taught at U3 AND U4:
            Q-A-2's anchor is E-17, worked at U3  → U3, not U4
            Q-B-1's anchor is E-19, worked at U4  → U4, unchanged
        Two items on one section, now on the two different sittings that actually work
        their exercises. Same at 5.5: E-43 is worked at U8, so Q-B-3 moves 9 → 8.
        """
        by_id = {it["id"]: it["unit_ref"] for it in assessment_items(self.plan, self.result)}
        self.assertEqual(by_id["Q-A-2"], [3], "E-17 is worked at U3, not at 5.2's close")
        self.assertEqual(by_id["Q-B-1"], [4], "E-19 is worked at U4 — same section, later")
        self.assertEqual(by_id["Q-B-3"], [8], "E-43 is worked at U8, not at 5.5's close")
        self.assertEqual(by_id["Q-C-5"], [10], "5.6 is taught once; both rules agree")

    def test_the_SECTION_rule_still_answers_when_the_anchor_does_not(self):
        """The two declared fallbacks (ARV-D-181's ruling), which is why
        `items_by_period_field` is still the base pass and not dead code.

        (a) an item with no `exercise` companion — 11 in the live corpus, ARV-D-184;
        (b) an item whose companion names no handoff anchor.
        Both must land on the section's last unit, exactly as before.
        """
        from aruvi_core.subjects.mathematics.subject import _anchor_then_section
        result = {"coverage_handoff": {"section_a": {"goals": [
                      {"anchor_id": "E-1", "anchor_book_ref": "Figure it Out Q1, p.1"}]}},
                  "lesson_plan": {"periods": [
                      {"period_number": 1, "textbook_segments": [{"ref": "section 1.1"}],
                       "textbook_items_in_class": [{"id": "E-1"}]},
                      {"period_number": 2, "textbook_segments": [{"ref": "section 1.1"}]}]}}
        ex = lambda p: [s["ref"] for s in (p.get("textbook_segments") or [])]
        got = _anchor_then_section(result, [
            {"id": "ANCHORED", "goal": "recall", "section_ref": "section 1.1",
             "exercise": {"book_ref": "Figure it Out Q1, p.1"}},
            {"id": "BLANK", "goal": "recall", "section_ref": "section 1.1",
             "exercise": {"book_ref": "", "description": ""}},
            {"id": "UNKNOWN", "goal": "recall", "section_ref": "section 1.1",
             "exercise": {"book_ref": "Some Other Exercise, p.9"}},
        ], stage="middle", extract=ex)
        by_id = {it["id"]: it["unit_ref"] for it in got}
        self.assertEqual(by_id["ANCHORED"], [1], "anchor resolves — first working wins")
        self.assertEqual(by_id["BLANK"], [2], "no companion — section's last unit")
        self.assertEqual(by_id["UNKNOWN"], [2], "companion is not an anchor — same")

    def test_an_anchor_worked_ONLY_in_the_synthesis_unit_falls_back(self):
        """The capstones (25 in the live corpus). Their anchor is worked only in the
        closer, which holds no items — so the resolver must decline rather than anchor
        there, and the section rule answers. `first_working` skips the synthesis unit, so
        this is the absence of a special case rather than one."""
        from aruvi_core.subjects.mathematics.subject import _anchor_then_section
        result = {"coverage_handoff": {"section_a": {"goals": [
                      {"anchor_id": "E-9", "anchor_book_ref": "Figure it Out Q9, p.9"}]}},
                  "lesson_plan": {"periods": [
                      {"period_number": 1, "textbook_segments": [{"ref": "section 1.1"}]},
                      {"period_number": 2, "textbook_segments": [{"ref": "section 1.1"}],
                       "synthesis": True,
                       "textbook_items_in_class": [{"id": "E-9"}]}]}}
        got = _anchor_then_section(result, [
            {"id": "CAPSTONE", "goal": "apply", "section_ref": "section 1.1",
             "exercise": {"book_ref": "Figure it Out Q9, p.9"}}],
            stage="middle",
            extract=lambda p: [s["ref"] for s in (p.get("textbook_segments") or [])])
        self.assertEqual(got[0]["unit_ref"], [1],
                         "the synthesis unit is not a candidate; section rule answers")

    def test_a_section_no_period_teaches_resolves_to_EMPTY_not_a_guess(self):
        from aruvi_core.genon.carriers import items_by_period_field
        result = {"lesson_plan": {"periods": [
            {"period_number": 1, "textbook_segments": [{"ref": "section 5.1"}]}]}}
        got = items_by_period_field(
            result, items=[{"id": "Q", "goal": "recall", "section_ref": "section 5.9"}],
            item_key="section_ref",
            extract=lambda p: [s["ref"] for s in p.get("textbook_segments") or []])
        self.assertEqual(got[0]["unit_ref"], [], "compile.py reports the orphan by name")

    def test_the_code_join_is_tolerant_the_way_the_display_side_is(self):
        from aruvi_core.genon.carriers import items_by_period_field
        result = {"lesson_plan": {"periods": [
            {"period_number": 3, "textbook_segments": [{"ref": "Section 5.2"}]}]}}
        got = items_by_period_field(
            result, items=[{"id": "Q", "section_ref": "section 5.2"}],
            item_key="section_ref",
            extract=lambda p: [s["ref"] for s in p.get("textbook_segments") or []])
        self.assertEqual(got[0]["unit_ref"], [3], "norm_code converges the two spellings")

    def test_raw_item_fields_survive_the_seam(self):
        """Genon needs the RAW dicts, not display objects: served files and exports read
        options / is_correct / teacher_guide / visual_stimulus straight off them."""
        it = next(i for i in assessment_items(self.plan, self.result) if i["id"] == "Q-A-1")
        self.assertTrue(it["options"])
        self.assertTrue(any(o.get("is_correct") for o in it["options"]))
        self.assertIn("expected_answer", it["teacher_guide"])
        self.assertIn("visual_stimulus", it)
        self.assertIn("exercise", it)

    def test_the_second_real_chapter_joins_too(self):
        p = (Path(__file__).resolve().parents[1]
             / "backup/saved_plans/mathematics/vii/ch_04_20260523_124721.json")
        if not p.is_file():
            self.skipTest("maths VII prototype plan not on disk")
        plan = json.loads(p.read_text(encoding="utf-8"))
        items = assessment_items(plan, plan["result"])
        self.assertEqual(len(items), 11)
        for it in items:
            self.assertEqual(len(it["unit_ref"]), 1, f"{it.get('id')} unanchored")

    def test_the_seam_does_not_need_a_grade(self):
        """`genon_assessment` receives only `result`; the grade lives on the enclosing PLAN.
        The stage is told apart by CONTAINER SHAPE — the S4 regression, re-pinned for the
        stage that shares its container with preparatory."""
        self.assertIsNone(self.result.get("grade"), "fixture: grade is on the plan, not here")
        assessment_items(self.plan, self.result)

    def test_a_middle_file_is_NOT_diverted_onto_preparatorys_field(self):
        """S8 opened row 5 on the same family helper. The two stages share a container, so
        the discriminator does the whole job: middle items carry `goal`, prep items carry
        `intent`. A middle file whose periods happen to carry no `section_refs` must still
        join on `textbook_segments[].ref` and must not silently orphan."""
        items = assessment_items(self.plan, self.result)
        self.assertTrue(all(it["unit_ref"] for it in items), "middle still joins on its own field")
        for p in self.result["lesson_plan"]["periods"]:
            self.assertNotIn("section_refs", p, "fixture: middle has no prep field to borrow")

    # ── E · the group-nested container ────────────────────────────────────────
    def test_raw_item_list_returns_ITEMS_not_the_A_B_C_GROUPS(self):
        """The live bug this closed: `raw_item_list` returned `raw` whenever it was a list,
        so STEP 6 (normalize_options) and generate_canonical.validate were iterating GROUP
        dicts. Same class as science's `questions` wrapper (ARV-D-060), different subject."""
        from aruvi_core.genon.carriers import raw_item_list
        got = raw_item_list(self.result)
        self.assertEqual(len(got), 11, "3 groups would be the bug")
        for it in got:
            self.assertIn("question_type", it)
            self.assertNotIn("items", it)

    def test_mutating_a_raw_item_reaches_the_saved_structure(self):
        """STEP 6 mutates options in place and writes the file back — the flattened list is
        new, but its ELEMENTS must be the live objects."""
        from aruvi_core.genon.carriers import raw_item_list
        raw_item_list(self.result)[0]["options"] = "TOUCHED"
        self.assertEqual(self.result["assessment_items"][0]["items"][0]["options"],
                         "TOUCHED")

    def test_bare_list_families_are_untouched_by_the_group_detector(self):
        from aruvi_core.genon.carriers import item_container, item_groups, raw_item_list
        for fixture in ("ss_vi_ch06_saved.json", "twau_iii_ch01_saved.json"):
            r = load(fixture).get("result")
            self.assertIsNone(item_groups(r["assessment_items"]), fixture)
            self.assertIsNone(item_container(r), fixture)
            self.assertIs(raw_item_list(r), r["assessment_items"], fixture)

    def test_container_round_trips_the_groups_including_an_empty_one(self):
        from aruvi_core.genon.carriers import from_engine_items, item_container
        container = item_container(self.result)
        items = [it for it in assessment_items(self.plan, self.result)
                 if it["_genon_group"] != "B"]          # serve dropped every B item
        back = from_engine_items(items, container)
        self.assertEqual([g["section_code"] for g in back], ["A", "B", "C"])
        self.assertEqual([len(g["items"]) for g in back], [3, 0, 5],
                         "an emptied group is emitted, never omitted")
        self.assertEqual(back[0]["section_title"], "Recall and Apply")
        self.assertEqual(back[0]["items"][0]["id"], "Q-A-1")

    def test_no_engine_marker_reaches_a_restored_plan(self):
        from aruvi_core.genon.carriers import from_engine_items, item_container
        back = from_engine_items(assessment_items(self.plan, self.result),
                                 item_container(self.result))
        for g in back:
            for it in g["items"]:
                self.assertNotIn("_genon_group", it)

    def test_the_marker_never_pollutes_the_LIVE_raw_items(self):
        assessment_items(self.plan, self.result)
        for g in self.result["assessment_items"]:
            for it in g["items"]:
                self.assertNotIn("_genon_group", it)

    def test_live_raw_items_re_bucket_through_the_item_id_map(self):
        """api/main.py's export filter passes `raw_item_list` output — live items with no
        marker on them — so the container carries an id -> group map as the second route."""
        from aruvi_core.genon.carriers import from_engine_items, item_container, raw_item_list
        container = item_container(self.result)
        back = from_engine_items(list(raw_item_list(self.result)), container)
        self.assertEqual([len(g["items"]) for g in back], [3, 3, 5])
        self.assertEqual([it["id"] for it in back[1]["items"]],
                         ["Q-B-1", "Q-B-2", "Q-B-3"])

    # ── C · the mediated unit anchor ──────────────────────────────────────────
    def test_unit_anchor_is_the_VERBATIM_textbook_segment_ref(self):
        """The founder ruling: no field is invented, the read is mediated. Verbatim matters
        because certification compares this against the registry drawn from the summary's
        own `sections[].ref` — both sides are the string "section 5.1"."""
        from aruvi_core.genon.carriers import unit_anchor
        periods = self.result["lesson_plan"]["periods"]
        got = [unit_anchor(p, subject="Mathematics", grade="Grade VI") for p in periods]
        self.assertEqual(got[0], "section 5.1")
        self.assertEqual(got[9], "section 5.6")

    def test_a_two_segment_period_joins_on_the_V2_ANCHOR_JOINER(self):
        from aruvi_core.genon.carriers import _ANCHOR_JOINER, unit_anchor
        p = self.result["lesson_plan"]["periods"][5]           # period 6: 5.3 and 5.4
        self.assertEqual(unit_anchor(p, subject="Mathematics", grade="Grade VI"),
                         "section 5.3" + _ANCHOR_JOINER + "section 5.4")

    def test_a_declared_section_anchor_still_wins(self):
        from aruvi_core.genon.carriers import unit_anchor
        p = {"period_number": 1, "section_anchor": "2.1",
             "textbook_segments": [{"ref": "section 2.1"}]}
        self.assertEqual(unit_anchor(p, subject="Mathematics", grade="Grade IX"), "2.1")

    def test_a_section_axis_stage_with_nothing_to_read_still_raises(self):
        from aruvi_core.genon.carriers import unit_anchor
        with self.assertRaises(KeyError):
            unit_anchor({"period_number": 4}, subject="Social Science", grade="Grade VII")

    # ── D · the goal-cluster coverage handoff ─────────────────────────────────
    def test_the_goal_cluster_dict_becomes_a_shape_serve_can_walk(self):
        """It used to fall through `to_engine_handoff` unchanged, so serve read `c["los"]`
        as empty, filtered nothing, and a served plan carried handoff rows for units it did
        not contain."""
        eng = to_engine_handoff(self.result)
        self.assertEqual(len(eng), 11, "one block per goal ENTRY, not per cluster")
        for blk in eng.values():                        # what serve.py actually does
            self.assertIsInstance(blk.get("los"), list)
            self.assertTrue(blk["los"], "every entry's section is taught in this plan")
            for lo in blk["los"]:
                self.assertIn("period_number", lo)

    def test_an_entrys_los_are_the_periods_that_teach_its_section(self):
        eng = to_engine_handoff(self.result)
        self.assertEqual([lo["period_number"] for lo in eng["section_a|section 5.2"]["los"]],
                         [3, 4], "section 5.2 is taught at 3 and 4")
        self.assertEqual([lo["period_number"] for lo in eng["section_c|section 5.6"]["los"]],
                         [10])

    def test_round_trip_is_lossless_and_keeps_all_three_clusters(self):
        back = from_engine_handoff(json.loads(json.dumps(to_engine_handoff(self.result))))
        self.assertEqual(list(back), ["section_a", "section_b", "section_c"])
        self.assertEqual(back, self.result["coverage_handoff"],
                         "byte-for-byte the subject's own native shape")

    def test_an_entry_whose_units_are_all_filtered_out_is_dropped(self):
        eng = to_engine_handoff(self.result)
        eng["section_a|section 5.2"]["los"] = []         # serve filtered them all away
        back = from_engine_handoff(eng)
        self.assertEqual([g["section_ref"] for g in back["section_a"]["goals"]],
                         ["section 5.1", "section 5.3"])
        self.assertEqual(back["section_a"]["goal_cluster"], ["recall"])

    def test_a_cluster_that_loses_every_entry_survives_EMPTY_not_absent(self):
        """LP Rule 11 and assessment Rule 1 both require all three clusters to exist."""
        eng = to_engine_handoff(self.result)
        for key in list(eng):
            if key.startswith("section_b|"):
                eng[key]["los"] = []
        back = from_engine_handoff(eng)
        self.assertEqual(list(back), ["section_a", "section_b", "section_c"])
        self.assertEqual(back["section_b"]["goals"], [])
        self.assertEqual(back["section_b"]["goal_cluster"], ["reason"])

    def test_no_engine_marker_leaks_into_a_served_handoff(self):
        back = from_engine_handoff(to_engine_handoff(self.result))
        for cluster in back.values():
            self.assertEqual(set(cluster), {"goal_cluster", "goals"})
            for g in cluster["goals"]:
                for k in ("_carrier", "_entry", "_order", "_cluster", "_cluster_order"):
                    self.assertNotIn(k, g)

    # ── the whole path, compile -> serve -> native shapes back ────────────────
    def test_it_compiles_and_SERVES_keeping_both_of_its_native_shapes(self):
        """The end-to-end proof. The fixture predates S7's P3 schema conversion, so its
        periods still carry `phases[]` where compile v0.5 reads `time_bands[]`; the bands are
        renamed here so the CARRIER work can be exercised on real content. Everything else —
        anchors, items, handoff — is the file as authored.
        """
        from aruvi_core.genon import compile_stream, serve_plan
        plan = json.loads(json.dumps(self.plan))
        for p in plan["result"]["lesson_plan"]["periods"]:
            p["time_bands"] = [{"minutes": ph["minutes"], "activity": ph["description"]}
                               for ph in p.pop("phases")]
        stream = compile_stream(plan)
        self.assertEqual([u["section_anchor"] for u in stream["units"]][:3],
                         ["section 5.1", "section 5.1", "section 5.2"])
        self.assertEqual(len(stream["assessment_items"]), 11)
        for x in (10, 7, 5):
            with self.subTest(x=x):
                served = serve_plan([stream], [(40, x)])["result"]
                self.assertEqual(len(served["lesson_plan"]["periods"]), x)
                ho = served["coverage_handoff"]
                self.assertEqual(list(ho), ["section_a", "section_b", "section_c"],
                                 "must come back as maths·middle's own goal-cluster DICT")
                for cluster in ho.values():
                    self.assertEqual(set(cluster), {"goal_cluster", "goals"})
                items = served["assessment_items"]
                self.assertEqual([g["section_code"] for g in items], ["A", "B", "C"],
                                 "must come back inside its own A/B/C groups")
                for g in items:
                    for it in g["items"]:
                        self.assertNotIn("_genon_group", it)
                        self.assertTrue(it.get("period_ref"))

    def test_the_other_families_handoffs_are_untouched(self):
        """SS/TWAU blocks carry `los` and pass through; science's ARRAY still wraps as the
        science carrier and comes back as a list."""
        ss = {"coverage_handoff": {"C-1.1": {"cg": "CG-1", "los": [{"period_number": 2}]}}}
        self.assertEqual(to_engine_handoff(ss), ss["coverage_handoff"])
        eng = to_engine_handoff(TestHandoffRoundTrip.SCI)
        self.assertTrue(all(b["_carrier"] == "science_section" for b in eng.values()))
        self.assertIsInstance(from_engine_handoff(eng), list)


class TestMathematicsPreparatoryLanded(unittest.TestCase):
    """S8, 2026-08-11 — maths·preparatory is 8-rule ROW 5: the SAME family as middle on a
    DIFFERENT field.

    The item names a section ("S3"), the period names the sections it teaches
    (`section_refs[]`), and the code itself is the join — no coverage_handoff in the path,
    no LO. What separates it from middle is only the field and the item vocabulary
    (`intent`, not `goal`), which is why the two are distinct rows of the 8-rule table and
    why neither may borrow the other's join.

    Fixture: the real prototype-era saved plan `backup/saved_plans/mathematics/iii/
    ch_06_*.json` — 9 periods over sections S1–S11, 26 items in four A/B/C/D INTENT groups
    (the prep container is the intent axis, not a section axis).
    """

    FIXTURE = ("backup/saved_plans/mathematics/iii/ch_06_20260603_180712.json")

    def setUp(self):
        p = Path(__file__).resolve().parents[1] / self.FIXTURE
        if not p.is_file():
            self.skipTest("maths III prototype plan not on disk")
        self.plan = json.loads(p.read_text(encoding="utf-8"))
        self.result = self.plan["result"]

    def test_the_stage_is_no_longer_owed(self):
        from aruvi_core.genon.carriers import carrier_gap
        self.assertIsNone(carrier_gap("mathematics", "iii"))
        self.assertIsNone(carrier_gap("mathematics", "iv"))
        self.assertIsNone(carrier_gap("mathematics", "v"))

    def test_every_item_resolves_to_exactly_one_unit_with_zero_orphans(self):
        items = assessment_items(self.plan, self.result)
        self.assertEqual(len(items), 26, "26 items across four intent groups, flattened")
        for it in items:
            self.assertIsInstance(it, dict, "the group wrapper must be flattened, not iterated")
            self.assertEqual(len(it["unit_ref"]), 1,
                             f"{it.get('id')} did not anchor to exactly one unit")

    def test_every_anchor_is_its_TASKs_first_working_or_the_sections_last_unit(self):
        """REPLACES `…equals_the_LAST_period_teaching_that_section` (2026-08-19,
        ARV-D-181). Preparatory is the same change as middle under other names: the
        handoff clusters by INTENT and carries `tasks[].task_id`, the period lists
        `tasks_in_class[].id`. Measured on iii ch 5 the section rule put every item on one
        sitting of fourteen (7%); the anchor rule spreads them over twelve (86%).

        Computed independently off the periods, both rules, so the test states which one
        answered rather than trusting the helper. S3 spans periods 2-3 and S8 spans 6-7,
        so the two rules genuinely differ here.
        """
        periods = self.result["lesson_plan"]["periods"]
        secs = {p["period_number"]: p["section_refs"] for p in periods}
        self.assertEqual(secs[2], ["S2", "S3"])
        self.assertEqual(secs[3], ["S3", "S4"])          # S3 spans 2-3
        self.assertEqual(secs[6], ["S8"])
        self.assertEqual(secs[7], ["S8", "S9"])          # S8 spans 6-7
        firsts = {}
        for p in periods:
            for key in ("tasks_in_class", "homework"):
                for t in (p.get(key) or []):
                    if isinstance(t, dict) and t.get("id") not in firsts:
                        firsts[t.get("id")] = p["period_number"]
        handoff = self.result.get("coverage_handoff") or {}
        by_ref = {}
        for blk in (handoff.values() if isinstance(handoff, dict) else []):
            for e in (blk.get("tasks") or []):
                if e.get("book_ref") and e.get("task_id"):
                    by_ref.setdefault(" ".join(str(e["book_ref"]).split()).lower(),
                                      e["task_id"])
        anchored = 0
        for it in assessment_items(self.plan, self.result):
            ref = " ".join(str((it.get("exercise") or {}).get("book_ref") or "").split()).lower()
            want = firsts.get(by_ref.get(ref)) if ref else None
            if want is None:
                want = max(n for n, refs in secs.items() if it["section_ref"] in refs)
            else:
                anchored += 1
            self.assertEqual(it["unit_ref"], [want],
                             f"{it['id']} ({it['section_ref']}) anchored wrongly")
        self.assertGreater(anchored, 0, "the anchor path must actually be exercised here")

    def test_it_joins_on_section_refs_NOT_middles_textbook_segments(self):
        """The whole reason row 5 is its own row. A prep period carries `section_refs` and
        no `textbook_segments`; borrowing middle's field would orphan every item."""
        for p in self.result["lesson_plan"]["periods"]:
            self.assertIn("section_refs", p)
            self.assertNotIn("textbook_segments", p)
        self.assertTrue(all(it["unit_ref"] for it in
                            assessment_items(self.plan, self.result)))

    def test_a_section_no_period_teaches_resolves_to_EMPTY_not_a_guess(self):
        from aruvi_core.genon.carriers import items_by_period_field
        result = {"lesson_plan": {"periods": [
            {"period_number": 1, "section_refs": ["S1"]}]}}
        got = items_by_period_field(
            result, items=[{"id": "Q", "intent": "reason", "section_ref": "S9"}],
            item_key="section_ref",
            extract=lambda p: [str(r) for r in (p.get("section_refs") or [])])
        self.assertEqual(got[0]["unit_ref"], [], "compile.py reports the orphan by name")

    def test_the_code_join_is_tolerant_the_way_the_display_side_is(self):
        from aruvi_core.genon.carriers import items_by_period_field
        result = {"lesson_plan": {"periods": [
            {"period_number": 4, "section_refs": ["s3"]}]}}
        got = items_by_period_field(
            result, items=[{"id": "Q", "intent": "solve", "section_ref": "S3"}],
            item_key="section_ref",
            extract=lambda p: [str(r) for r in (p.get("section_refs") or [])])
        self.assertEqual(got[0]["unit_ref"], [4], "norm_code converges the two spellings")

    def test_raw_item_fields_survive_the_seam(self):
        """Genon needs the RAW dicts, not display objects: served files and exports read
        teacher_guide / visual_stimulus / exercise straight off them."""
        it = next(i for i in assessment_items(self.plan, self.result) if i["id"] == "Q-A-1")
        self.assertIn("expected_answer", it["teacher_guide"])
        self.assertIn("visual_stimulus", it)
        self.assertIn("exercise", it)
        self.assertIn("intent", it, "the discriminator itself must survive")

    def test_the_seam_does_not_need_a_grade(self):
        """`genon_assessment` receives only `result`, and prep is told from middle by
        CONTAINER SHAPE — the S4 regression, now load-bearing for two stages of one
        subject that share a container."""
        self.assertIsNone(self.result.get("grade"), "fixture: grade is on the plan, not here")
        assessment_items(self.plan, self.result)

    def test_raw_item_list_returns_ITEMS_not_the_intent_GROUPS(self):
        from aruvi_core.genon.carriers import raw_item_list
        got = raw_item_list(self.result)
        self.assertEqual(len(got), 26, "4 groups would be the bug")
        for it in got:
            self.assertIn("intent", it)

    def test_unit_anchor_is_the_VERBATIM_section_ref(self):
        """`genon_unit_anchor`'s preparatory branch — written unexercised at S7, exercised
        here for the first time. Verbatim, joined with the V2 multi-section joiner."""
        from aruvi_core.genon.carriers import unit_anchor
        periods = self.result["lesson_plan"]["periods"]
        self.assertEqual(unit_anchor(periods[0], subject="mathematics", grade="iii"), "S1")
        self.assertEqual(unit_anchor(periods[1], subject="mathematics", grade="iii"),
                         "S2 / S3")


class TestEnglishSecondaryLanded(unittest.TestCase):
    """S11, 2026-08-12 — english·secondary is 8-rule ROW 7: the period-field family again,
    and the first row in the table whose join key is a PAIR.

    The item names a CELL (`source_section_id` + `source_spine`), the unit names the cells it
    teaches (`section_id` + `spines_taught[]`), and the pair is the join — no coverage_handoff
    in the path, and the LO rides on the item itself (`source_lo`), so it needs no bridge
    either. What makes it its own row is that neither half identifies a cell alone.

    Fixture: the real saved plan `backup/saved_plans/english/ix/ch_11_*.json` — 7 units over
    one main_section (the post-split shape), 6 items in 6 SPINE groups, two cells genuinely
    spanning several units (RFC over 1-3, VocGram over 4-5).
    """

    FIXTURE = "backup/saved_plans/english/ix/ch_11_20260608_213837.json"

    def setUp(self):
        p = Path(__file__).resolve().parents[1] / self.FIXTURE
        if not p.is_file():
            self.skipTest("english IX saved plan not on disk")
        self.plan = json.loads(p.read_text(encoding="utf-8"))
        self.result = self.plan["result"]

    def test_the_stage_is_no_longer_owed_and_nor_are_its_siblings(self):
        from aruvi_core.genon.carriers import carrier_gap
        self.assertIsNone(carrier_gap("english", "ix"))
        self.assertIsNone(carrier_gap("english", "vii"), "S10 landed middle 2026-08-13")
        self.assertIsNone(carrier_gap("english", "iii"), "S9 landed preparatory 2026-08-13")

    def test_every_item_resolves_to_exactly_one_unit_with_zero_orphans(self):
        items = assessment_items(self.plan, self.result)
        self.assertEqual(len(items), 6, "6 items across 6 spine groups, flattened")
        for it in items:
            self.assertIsInstance(it, dict, "the spine wrapper must be flattened, not iterated")
            self.assertEqual(len(it["unit_ref"]), 1,
                             f"{it.get('id')} did not anchor to exactly one unit")

    def test_every_anchor_equals_the_LAST_unit_teaching_THAT_CELL(self):
        """The 2026-08-05 ruling, computed independently off the units. Both spanning cells
        are real cases here: RFC is taught in units 1-3 and VocGram in 4-5, so an item that
        anchored at the FIRST unit, or at the union, would show a different number."""
        cells = {p["period_number"]: (p["section_id"], p["spines_taught"])
                 for p in self.result["lesson_plan"]["periods"]}
        self.assertEqual([n for n, (s, sp) in cells.items()
                          if "reading_for_comprehension" in sp], [1, 2, 3])
        self.assertEqual([n for n, (s, sp) in cells.items()
                          if "vocabulary_grammar" in sp], [4, 5])
        for it in assessment_items(self.plan, self.result):
            last = max(n for n, (sid, sp) in cells.items()
                       if sid == it["source_section_id"] and it["source_spine"] in sp)
            self.assertEqual(it["unit_ref"], [last],
                             f"{it['id']} anchored off its cell's last unit")

    def test_the_join_is_the_PAIR_not_the_spine_alone(self):
        """The reason row 7 is its own row, shown on the only shape that can prove it: a
        MULTI-section english plan, where three different sections each teach RFC. Joining on
        the spine alone would make every RFC item share one cell and collapse all three onto
        the last section's unit. (The fixture is a middle-stage plan, so it goes through the
        resolver directly — the gated seam would refuse it, which is S10's business.)"""
        from aruvi_core.subjects.english.subject import cell_resolver
        plan = load("english_vii_ch01_saved.json")
        r = plan["result"]
        periods = r["lesson_plan"]["periods"]
        resolve = cell_resolver(periods, r["assessment_items"])
        got = {}
        for sg in r["assessment_items"]:
            for it in sg["items"]:
                if it["source_spine"] == "reading_for_comprehension":
                    got[it["source_section_id"]] = resolve(it)
                else:
                    resolve(it)                      # keep the counters aligned
        self.assertEqual(len(got), 3, "sections A, B and C each carry an RFC item")
        self.assertEqual(len({tuple(v) for v in got.values()}), 3,
                         "three sections, three DIFFERENT unit sets — not one shared cell")

    def test_the_N_to_N_pairing_survives_into_the_carrier(self):
        """Two items sharing a cell taught over exactly two units pair POSITIONALLY, one per
        unit, instead of both anchoring at the close. This is the 2026-07-11 display fix, and
        the carrier delegates to the same resolver so it cannot be lost on the served side.
        The M == N case of the 2026-08-12 even-dispersion generalisation: every block is one
        unit long, so the original behaviour falls out of the same arithmetic."""
        result = {"lesson_plan": {"periods": [
            {"period_number": 4, "section_id": "A", "spines_taught": ["vocabulary_grammar"]},
            {"period_number": 5, "section_id": "A", "spines_taught": ["vocabulary_grammar"]}]},
            "assessment_items": [{"spine_code": "vocabulary_grammar", "items": [
                {"id": "Q1", "source_section_id": "A", "source_spine": "vocabulary_grammar"},
                {"id": "Q2", "source_section_id": "A", "source_spine": "vocabulary_grammar"}]}]}
        got = assessment_items({"subject": "English", "grade": "Grade IX"}, result)
        self.assertEqual([it["unit_ref"] for it in got], [[4], [5]])

    def test_the_PAIR_disperses_across_a_multi_unit_cell(self):
        """M > N: the v1.6/v3.6/v1.4 PAIR over a cell taught in eight units is DEALT as two
        contiguous blocks — slot 1 anchors at the end of the first half, slot 2 at the close —
        instead of both items taking the union and both anchoring at unit 8. This is the
        coverage half of the 2026-08-12 amendment: doubling the items without dispersing them
        doubled the ratio but left the same six units of seventeen carrying an Assess tab."""
        result = {"lesson_plan": {"periods": [
            {"period_number": n, "section_id": "A",
             "spines_taught": ["reading_for_comprehension"]} for n in range(1, 9)]},
            "assessment_items": [{"spine_code": "reading_for_comprehension", "items": [
                {"id": "Q-RFC-A-1", "source_section_id": "A",
                 "source_spine": "reading_for_comprehension"},
                {"id": "Q-RFC-A-2", "source_section_id": "A",
                 "source_spine": "reading_for_comprehension"}]}]}
        got = assessment_items({"subject": "English", "grade": "Grade IX"}, result)
        # unit_ref is POST-stamp — each item anchors at the LAST unit of its own block.
        self.assertEqual([it["unit_ref"] for it in got], [[4], [8]],
                         "slot 1 closes the first block, slot 2 closes the cell")
        # …and the blocks themselves, pre-stamp, are the contiguous halves.
        from aruvi_core.subjects.english.subject import cell_resolver
        resolve = cell_resolver(result["lesson_plan"]["periods"], result["assessment_items"])
        self.assertEqual([resolve(it) for it in result["assessment_items"][0]["items"]],
                         [[1, 2, 3, 4], [5, 6, 7, 8]])

    def test_a_TRUE_SPAN_still_keeps_the_whole_set(self):
        """N == 1 over many units is a genuine span — one item re-tested across the cell — and
        must NOT be dealt. It keeps the UNION (and then anchors at the close), unchanged by the
        dispersion generalisation. Asserted pre-stamp, since stamping a span and stamping a
        block both yield one number and would hide the difference."""
        periods = [{"period_number": n, "section_id": "A", "spines_taught": ["speaking"]}
                   for n in (2, 3, 4)]
        groups = [{"spine_code": "speaking", "items": [
            {"id": "Q1", "source_section_id": "A", "source_spine": "speaking"}]}]
        from aruvi_core.subjects.english.subject import cell_resolver
        resolve = cell_resolver(periods, groups)
        self.assertEqual(resolve(groups[0]["items"][0]), [2, 3, 4], "the whole span, not a block")
        got = assessment_items({"subject": "English", "grade": "Grade IX"},
                               {"lesson_plan": {"periods": periods}, "assessment_items": groups})
        self.assertEqual([it["unit_ref"] for it in got], [[4]], "anchors at the close")

    def test_MORE_items_than_units_BACK_FILLS_when_the_cell_spans_units(self):
        """M < N over MORE THAN ONE unit back-fills to the close (2026-08-15, S11·W1).

        The regression this pins: english·preparatory iii ch 3 (A, oracy) is taught in units
        4, 5 and 6 and carries FOUR items — two authored pairs that share one (section × spine)
        address because the cell key is coarser than `source_lo`. The old guard (`M >= N`)
        failed, the cell fell to the shared-span branch, and all four items anchored on unit 6
        while units 4 and 5 — which teach that very cell — showed no Assess tab at all.

        Back-fill anchors one item per unit BACKWARDS from the close and piles the surplus on
        the first unit, so the last item still lands at the cell's completion (Rule 8A) and the
        earlier sittings stop coming up empty."""
        result = {"lesson_plan": {"periods": [
            {"period_number": n, "section_id": "A", "spines_taught": ["oracy"]}
            for n in (4, 5, 6)]},
            "assessment_items": [{"spine_code": "oracy", "items": [
                {"id": f"Q{i}", "source_section_id": "A", "source_spine": "oracy"}
                for i in range(1, 5)]}]}
        got = assessment_items({"subject": "English", "grade": "Grade III"}, result)
        self.assertEqual([it["unit_ref"] for it in got], [[4], [4], [5], [6]],
                         "surplus on the first unit; the LAST item still closes the cell")
        self.assertEqual(len({tuple(it["unit_ref"]) for it in got}), 3,
                         "all three teaching units carry an item, not just the close")

    def test_MORE_items_than_units_keeps_the_shared_set_in_a_SINGLE_unit_cell(self):
        """M == 1 — a pair whose cell was taught in a single unit — cannot be dealt. Both items
        keep the full set and both anchor there; splitting would invent a unit. This is the one
        shape the 2026-08-15 back-fill deliberately leaves alone."""
        result = {"lesson_plan": {"periods": [
            {"period_number": 12, "section_id": "A", "spines_taught": ["listening"]}]},
            "assessment_items": [{"spine_code": "listening", "items": [
                {"id": "Q1", "source_section_id": "A", "source_spine": "listening"},
                {"id": "Q2", "source_section_id": "A", "source_spine": "listening"}]}]}
        got = assessment_items({"subject": "English", "grade": "Grade IX"}, result)
        self.assertEqual([it["unit_ref"] for it in got], [[12], [12]])

    def test_a_cell_no_unit_teaches_resolves_to_EMPTY_not_a_guess(self):
        result = {"lesson_plan": {"periods": [
            {"period_number": 1, "section_id": "A", "spines_taught": ["listening"]}]},
            "assessment_items": [{"spine_code": "writing", "items": [
                {"id": "Q", "source_section_id": "B", "source_spine": "writing"}]}]}
        got = assessment_items({"subject": "English", "grade": "Grade IX"}, result)
        self.assertEqual(got[0]["unit_ref"], [], "compile.py reports the orphan by name")

    def test_a_synthesis_unit_is_not_indexed(self):
        """A closing unit revisits several cells without teaching one. Indexed, it would be
        the LAST unit of every cell it names and the whole chapter's items would collapse onto
        it — the defect S7 met on maths·middle ch 7, third site, same seam."""
        result = {"lesson_plan": {"periods": [
            {"period_number": 1, "section_id": "A", "spines_taught": ["listening"]},
            {"period_number": 2, "section_id": "A", "spines_taught": ["writing"]},
            {"period_number": 3, "section_id": "A", "synthesis": True,
             "spines_taught": ["listening", "writing"]}]},
            "assessment_items": [{"spine_code": "listening", "items": [
                {"id": "Q", "source_section_id": "A", "source_spine": "listening"}]}]}
        got = assessment_items({"subject": "English", "grade": "Grade IX"}, result)
        self.assertEqual(got[0]["unit_ref"], [1], "unit 3 is a synthesis, not the cell's close")

    def test_unit_anchor_is_the_COMPOSITE_cell_code(self):
        from aruvi_core.genon.carriers import period_section_codes, unit_anchor
        periods = self.result["lesson_plan"]["periods"]
        self.assertEqual(unit_anchor(periods[0], subject="English", grade="Grade IX"),
                         "A|reading_for_comprehension")
        self.assertEqual(unit_anchor(periods[5], subject="English", grade="Grade IX"),
                         "A|listening / A|speaking")
        for p in periods:
            got = unit_anchor(p, subject="English", grade="Grade IX")
            self.assertEqual(got.split(" / "), period_section_codes(p),
                             "the anchor and the join code are one expression, not two")

    def test_the_spine_keyed_handoff_survives_a_ROUND_TRIP_and_filters(self):
        """Without `_ENGLISH_SPINE_CELL` the dict fell through `to_engine_handoff` unchanged,
        serve read `c["los"]` as empty and filtered nothing, so a short serve carried the full
        canonical's coverage — claiming spines the class never met."""
        from aruvi_core.genon.carriers import from_engine_handoff, to_engine_handoff
        eng = to_engine_handoff(self.result)
        self.assertEqual(len(eng), 6, "one engine block per (section × spine) CELL")
        self.assertEqual([lo["period_number"] for lo in eng["vocabulary_grammar|A"]["los"]],
                         [4, 5])
        for blk in eng.values():                       # a serve that keeps units 1-4
            blk["los"] = [lo for lo in blk["los"] if lo["period_number"] <= 4]
        back = from_engine_handoff(eng)
        self.assertEqual(list(back), ["reading_for_comprehension", "vocabulary_grammar"],
                         "spines with no surviving cell are omitted (assessment Rule 1)")
        self.assertEqual(back["reading_for_comprehension"]["section_contributions"][0],
                         self.result["coverage_handoff"]["reading_for_comprehension"]
                         ["section_contributions"][0], "contributions ride back verbatim")

    def test_raw_item_list_returns_ITEMS_not_the_SPINE_groups(self):
        from aruvi_core.genon.carriers import raw_item_list
        got = raw_item_list(self.result)
        self.assertEqual(len(got), 6, "6 spine groups would be the bug")
        for it in got:
            self.assertIn("source_spine", it)

    def test_the_container_is_keyed_on_spine_code_not_on_position(self):
        """Positional keys are safe only while both sides of a serve are the same list in the
        same order — which is exactly what stops being true when a unit, and its item, is
        BORROWED from a companion canonical."""
        from aruvi_core.genon.carriers import from_engine_items, item_container
        cont = item_container(self.result)
        self.assertEqual([g["_gkey"] for g in cont["_groups"]],
                         ["reading_for_comprehension", "listening", "speaking", "writing",
                          "vocabulary_grammar", "beyond_text"])
        out = from_engine_items(assessment_items(self.plan, self.result), cont)
        self.assertEqual([g["spine_code"] for g in out],
                         [g["_gkey"] for g in cont["_groups"]])
        self.assertEqual([len(g["items"]) for g in out], [1] * 6)
        self.assertTrue(all("_genon_group" not in it for g in out for it in g["items"]),
                        "engine residue must never reach a served file")

    def test_raw_item_fields_survive_the_seam(self):
        it = next(i for i in assessment_items(self.plan, self.result)
                  if i["id"] == "Q-RFC-A-1")
        self.assertIn("teacher_guide", it)
        self.assertIn("visual_stimulus", it)
        self.assertIn("source_lo", it, "the LO rides on the item — row 7 needs no bridge")

    def test_the_seam_does_not_need_a_grade(self):
        """`genon_assessment` receives only `result`; the grade lives on the enclosing plan
        (the S4 trap). English needs no stage discriminator at all — all three stages are
        row 7 on the same two fields — but the method must still not reach for one."""
        self.assertIsNone(self.result.get("grade"), "fixture: grade is on the plan, not here")
        assessment_items(self.plan, self.result)


class TestEnglishMiddleLanded(unittest.TestCase):
    """S10, 2026-08-13 — english·middle is row 7 too, and the deletion WAS the whole job.

    No new code landed with this stage: `cell_resolver`, `genon_assessment`,
    `genon_unit_anchor` and `_ENGLISH_SPINE_CELL` are all stage-agnostic and all arrived at
    S11. The `_NOT_YET` note asked a successor to CONFIRM three things rather than re-derive
    them — spine set, container shape, spine-keyed handoff — and all three held across VI,
    VII and VIII (46 chapters, 272 taught cells, 12 saved plans, 53 items, zero orphans;
    `genon/out/stage_prep_english_middle/verify_s10_carrier.py`).

    WHY THIS CLASS EXISTS ANYWAY, ALONGSIDE THE SECONDARY ONE. Middle is the stage where the
    PAIR key is load-bearing. Every english IX chapter is one `main_section`, so joining on
    `source_spine` alone produces correct anchors across the whole certified secondary class —
    S11 recorded that as the error that "would have looked correct". Middle's corpus is
    genuinely multi-section: this fixture teaches Reading in sections A, B and C, so a
    spine-only join collapses three cells onto one and the wrong answer finally shows.

    The fixture predates assessment v3.6's PAIR (one item per cell, not two), which is what
    makes it a clean test of the JOIN in isolation.
    """

    FIXTURE = "english_vii_ch01_saved.json"

    def setUp(self):
        self.plan = load(self.FIXTURE)
        self.result = self.plan.get("result", self.plan)
        self.periods = (self.result.get("lesson_plan") or {}).get("periods") or []

    def test_the_stage_is_no_longer_owed_and_nor_is_preparatory(self):
        from aruvi_core.genon.carriers import carrier_gap
        for g in ("vi", "vii", "viii"):
            self.assertIsNone(carrier_gap("english", g), f"S10 landed {g}")
        self.assertIsNone(carrier_gap("english", "iii"), "S9 landed preparatory 2026-08-13")

    def test_the_multi_section_join_does_not_collapse_onto_the_spine(self):
        """THE test this stage adds. Reading is taught in A (units 1-2), B (6-7) and C (10).
        A spine-only join anchors all three RFC items at unit 10; the pair key does not."""
        anchors = {it["id"]: it["unit_ref"]
                   for it in assessment_items(self.plan, self.result)}
        self.assertEqual(anchors["Q-RFC-A-1"], [2])
        self.assertEqual(anchors["Q-RFC-B-1"], [7])
        self.assertEqual(anchors["Q-RFC-C-1"], [10])
        self.assertEqual(len({tuple(anchors[k]) for k in
                              ("Q-RFC-A-1", "Q-RFC-B-1", "Q-RFC-C-1")}), 3,
                         "three Reading cells must reach three different units")

    def test_every_anchor_equals_the_LAST_unit_teaching_THAT_CELL(self):
        """The 2026-08-05 ruling, computed independently off the units rather than asserted
        as a literal, so the test cannot drift into agreeing with the code by construction."""
        last: dict = {}
        for i, p in enumerate(self.periods, start=1):
            for sp in p.get("spines_taught") or []:
                last[(str(p.get("section_id")).strip(), str(sp).strip())] = i
        items = assessment_items(self.plan, self.result)
        self.assertEqual(len(items), 14, "14 cells taught, one item each pre-v3.6")
        for it in items:
            cell = (str(it["source_section_id"]).strip(), str(it["source_spine"]).strip())
            self.assertEqual(it["unit_ref"], [last[cell]],
                             f"{it['id']} ({cell}) did not anchor at its cell's close")

    def test_zero_orphans(self):
        for it in assessment_items(self.plan, self.result):
            self.assertTrue(it.get("unit_ref"), f"{it.get('id')} orphaned")

    def test_unit_anchor_is_the_COMPOSITE_cell_code_at_this_stage_too(self):
        """`section_anchor` is 0 in all three english LP constitutions, so the read is
        mediated. A unit teaching two spines joins them with the V2 joiner."""
        from aruvi_core.genon.carriers import unit_anchor
        self.assertEqual(unit_anchor(self.periods[0], subject="English", grade="Grade VII"),
                         "A|reading_for_comprehension")
        self.assertEqual(unit_anchor(self.periods[2], subject="English", grade="Grade VII"),
                         "A|listening / A|speaking")

    def test_the_anchor_field_is_declared_ABSENT_for_middle(self):
        """The expensive half: without this, `top_brief_for` demands the reserved token in a
        field the constitution never defines — at metered STEP 1 — and the certifier then
        finds no closing unit in a library already paid for."""
        from aruvi_core.genon.carriers import anchor_field_present
        self.assertFalse(anchor_field_present("english", "vii"))


class TestEnglishPreparatoryLanded(unittest.TestCase):
    """S9, 2026-08-13 — row 7's third and last stage, and the entry that emptied `_NOT_YET`.

    No new code landed with this stage either. The `_NOT_YET` note named ONE difference for a
    successor to check, and it was real: **preparatory's spine set is FIVE, not six** —
    `reading` (not `reading_for_comprehension`), `oracy` (listening and speaking MERGED, with
    listening riding as per-task `transcript_ref`/`transcript_text` inside it), `writing`,
    `word_work` (not `vocabulary_grammar`) and `beyond_text`.

    WHY A DIFFERENT SPINE SET COSTS NOTHING, and why that is worth a test rather than a
    comment: no part of the carrier reads a spine NAME. `cell_resolver` joins whatever
    `spines_taught[]` holds against whatever `source_spine` holds, and `genon_unit_anchor`
    composes the cell token from both halves without a vocabulary. A carrier that had hard-coded
    the six middle keys — the obvious shortcut when secondary was the only stage — would pass
    S11 and S10 and fail every chapter of this one.

    WHAT THIS FIXTURE ADDS that neither sibling has. IV ch 1 teaches `word_work` across units
    4 AND 5 and carries TWO items for it, so the N-to-N pairing is exercised on prep's own
    shape; `oracy` is taught across units 2-3 with ONE item, so the last-unit rule is exercised
    beside it, in the same plan. The fixture predates assessment v1.4's PAIR, which is what
    makes the two branches distinguishable at all.
    """

    FIXTURE = "english_iv_ch01_saved.json"

    def setUp(self):
        self.plan = load(self.FIXTURE)
        self.result = self.plan.get("result", self.plan)
        self.periods = (self.result.get("lesson_plan") or {}).get("periods") or []

    def test_the_stage_is_no_longer_owed_and_the_table_is_empty(self):
        import aruvi_core.genon.carriers as C
        for g in ("iii", "iv", "v"):
            self.assertIsNone(C.carrier_gap("english", g), f"S9 landed {g}")
        self.assertEqual(C._NOT_YET, {}, "the last entry in the campaign")

    def test_the_five_prep_spines_resolve_and_none_of_the_six_middle_keys_appear(self):
        """The one difference `_NOT_YET` asked this stage to check."""
        MIDDLE_ONLY = {"reading_for_comprehension", "listening",
                       "speaking", "vocabulary_grammar"}
        seen = {str(it["source_spine"]).strip()
                for it in assessment_items(self.plan, self.result)}
        self.assertEqual(seen, {"reading", "oracy", "writing", "word_work", "beyond_text"})
        self.assertFalse(seen & MIDDLE_ONLY, "a middle spine key must never resolve here")

    def test_a_cell_taught_over_two_units_with_two_items_pairs_N_to_N(self):
        """`word_work` is taught in units 4 and 5 and carries two items — one per unit, in
        order. Anchoring both at the close is the defect the pairing was written to fix."""
        anchors = {it["id"]: it["unit_ref"]
                   for it in assessment_items(self.plan, self.result)}
        self.assertEqual(anchors["Q-WW-A-1"], [4])
        self.assertEqual(anchors["Q-WW-A-2"], [5])

    def test_a_cell_taught_over_two_units_with_ONE_item_anchors_at_the_close(self):
        """`oracy` spans units 2-3 with a single item — the 2026-08-05 anchoring ruling, in
        the same plan as the pairing above, which is what keeps the two branches honest."""
        anchors = {it["id"]: it["unit_ref"]
                   for it in assessment_items(self.plan, self.result)}
        self.assertEqual(anchors["Q-ORACY-A-1"], [3])

    def test_every_anchor_equals_the_LAST_unit_teaching_THAT_CELL(self):
        """Computed independently off the units, so the test cannot drift into agreeing with
        the code. Cells with an N-to-N pairing are excluded — they are the case above."""
        units: dict = {}
        for i, p in enumerate(self.periods, start=1):
            for sp in p.get("spines_taught") or []:
                units.setdefault((str(p.get("section_id")).strip(), str(sp).strip()), []).append(i)
        items = assessment_items(self.plan, self.result)
        self.assertEqual(len(items), 6, "5 cells taught, word_work carrying two items")
        by_cell: dict = {}
        for it in items:
            cell = (str(it["source_section_id"]).strip(), str(it["source_spine"]).strip())
            by_cell.setdefault(cell, []).append(it)
        for cell, got in by_cell.items():
            if len(got) == 1:
                self.assertEqual(got[0]["unit_ref"], [units[cell][-1]],
                                 f"{got[0]['id']} ({cell}) did not anchor at its cell's close")

    def test_zero_orphans(self):
        for it in assessment_items(self.plan, self.result):
            self.assertTrue(it.get("unit_ref"), f"{it.get('id')} orphaned")

    def test_unit_anchor_is_the_COMPOSITE_cell_code_at_this_stage_too(self):
        from aruvi_core.genon.carriers import unit_anchor
        self.assertEqual(unit_anchor(self.periods[0], subject="English", grade="Grade IV"),
                         "A|reading")

    def test_the_anchor_field_is_declared_ABSENT_for_preparatory(self):
        """`section_anchor` is 0 in all three english LP constitutions. Without this,
        `top_brief_for` demands the reserved token in a field the constitution never defines,
        at metered STEP 1."""
        from aruvi_core.genon.carriers import anchor_field_present
        self.assertFalse(anchor_field_present("english", "iv"))


class TestCarrierPreFlight(unittest.TestCase):
    """The gate must be FREE. Before 2026-08-08 the answer arrived at certification, which
    runs after the metered steps, so a missing carrier cost a whole library (₹110-150) and
    reported itself as "does not compile" on every file. testing.md P5.5."""

    def test_ready_stages_report_no_gap(self):
        from aruvi_core.genon.carriers import carrier_gap
        for subject, grade in (("mathematics", "ix"), ("mathematics", "vii"),
                               ("science", "ix"), ("science", "viii"),
                               ("social_sciences", "ix"), ("the_world_around_us", "v"),
                               ("english", "ix")):          # row 7, landed 2026-08-12 (S11)
            self.assertIsNone(carrier_gap(subject, grade), f"{subject}·{grade}")

    def test_no_stage_is_owed_and_the_table_says_so_by_being_empty(self):
        """S9 removed the last entry (english·preparatory, 2026-08-13). Every subject·stage
        in the 11-stage matrix is carried, so the honest inventory is the empty dict."""
        import aruvi_core.genon.carriers as C
        self.assertEqual(C._NOT_YET, {})
        for subject, grade in (("english", "iii"), ("english", "vi"), ("english", "ix")):
            self.assertIsNone(C.carrier_gap(subject, grade), f"{subject}·{grade}")

    def test_an_owed_stage_would_still_report_its_stage_and_row(self):
        """The reporting contract, kept alive against an empty table by a synthetic entry.
        The message must name the stage that owes it — that is what turns a paid, silent
        "does not compile" into a free STOP at STEP 0."""
        import aruvi_core.genon.carriers as C
        saved = dict(C._NOT_YET)
        C._NOT_YET[("english", "preparatory")] = "row 7 · period-field — owed by SX"
        try:
            gap = C.carrier_gap("english", "iii")
            self.assertIsNotNone(gap)
            self.assertIn("SX", gap, "the gap must name the stage that owes it")
            self.assertIn("row 7", gap, "and its row in the 8-rule table")
        finally:
            C._NOT_YET.clear()
            C._NOT_YET.update(saved)

    def test_a_missing_grade_is_conservative_not_optimistic(self):
        """Guessing "ready" is the expensive mistake, so an unknown grade on a subject that
        still owes ANY stage must read as owed. With `_NOT_YET` empty every gradeless call
        is legitimately None, so the conservative branch is exercised against a synthetic
        entry — otherwise emptying the table would delete the rule along with its last
        instance, and the next subject brought into genon would inherit an optimistic read."""
        import aruvi_core.genon.carriers as C
        self.assertIsNone(C.carrier_gap("english", None), "no english stage is owed")
        self.assertIsNone(C.carrier_gap("social_sciences", None), "owes nothing at any stage")
        self.assertIsNone(C.carrier_gap("mathematics", None),
                          "all three maths stages landed — secondary S4, middle S7, "
                          "preparatory S8")
        saved = dict(C._NOT_YET)
        C._NOT_YET[("english", "preparatory")] = "row 7 · period-field — owed by SX"
        try:
            gap = C.carrier_gap("english", None)
            self.assertIsNotNone(gap, "one owed stage makes the whole subject owed "
                                      "when the grade is unknown")
            self.assertIn("grade not given", gap)
            self.assertIsNone(C.carrier_gap("english", "ix"),
                              "and a KNOWN grade still resolves stage-granularly")
        finally:
            C._NOT_YET.clear()
            C._NOT_YET.update(saved)

    def test_require_carrier_raises_only_for_owed(self):
        from aruvi_core.genon.carriers import require_carrier
        import aruvi_core.genon.carriers as C
        require_carrier("mathematics", "ix")                       # must not raise
        require_carrier("mathematics", "vii")                      # landed 2026-08-10 (S7)
        require_carrier("mathematics", "iii")                      # landed 2026-08-11 (S8)
        require_carrier("english", "iii")                          # landed 2026-08-13 (S9)
        saved = dict(C._NOT_YET)
        C._NOT_YET[("english", "preparatory")] = "row 7 · period-field — owed by SX"
        try:
            with self.assertRaises(CarrierNotImplemented):
                require_carrier("english", "iii")
        finally:
            C._NOT_YET.clear()
            C._NOT_YET.update(saved)


class TestItemAnchorFamilyIsDeclared(unittest.TestCase):
    """The 8-rule table's family column, declared on the plugin rather than inferred —
    because it has a consequence beyond the join: on a DERIVED anchor a unit with no
    handoff row can hold no item, which is why the standard's synthesis unit needs one."""

    def test_families_match_the_8_rule_table(self):
        from aruvi_core.genon.carriers import item_anchor_family
        for subject, grade, family in (
                ("science", "viii", "handoff"),          # row 1
                ("science", "ix", "handoff"),            # row 2
                ("social_sciences", "vii", "item"),      # row 3
                ("mathematics", "vii", "period_field"),  # row 4
                ("mathematics", "iii", "period_field"),  # row 5
                ("mathematics", "ix", "handoff"),        # row 6
                ("the_world_around_us", "iii", "item")): # row 8
            self.assertEqual(item_anchor_family(subject, grade), family,
                             f"{subject}·{grade}")

    def test_derived_anchor_stages_are_exactly_the_handoff_family(self):
        from aruvi_core.genon.carriers import item_anchor_is_derived
        self.assertTrue(item_anchor_is_derived("mathematics", "ix"))
        self.assertTrue(item_anchor_is_derived("science", "ix"))
        self.assertFalse(item_anchor_is_derived("social_sciences", "ix"))
        self.assertFalse(item_anchor_is_derived("mathematics", "vii"))


class TestCompileEndToEnd(unittest.TestCase):
    """The regression that started this: compile must never emit a string item."""

    def test_every_genon_ready_subject_compiles_with_dict_items(self):
        from aruvi_core.genon import compile_stream
        for fixture in ("ss_vi_ch06_saved.json", "ss_vii_ch04_edge_saved.json"):
            with self.subTest(fixture=fixture):
                stream = compile_stream(load(fixture))
                items = stream["assessment_items"]
                self.assertTrue(items, f"{fixture}: compiled to zero items")
                for it in items:
                    self.assertIsInstance(
                        it, dict,
                        f"{fixture}: compiled a {type(it).__name__} — the wrapper bug is back")
                    self.assertTrue(it.get("unit_ref"), f"{fixture}: item left unanchored")

    def test_known_LP_SHAPE_gaps_are_recorded_not_hidden(self):
        """ONE fixture does NOT compile, and the reason is the LESSON PLAN shape, not the
        carrier seam — its items extract fine (see the family tests above). Recorded
        here so the gap is registered rather than skipped into silence. When it is
        closed this test FAILS, which is the signal to update it.

          • science·middle  — periods carry `phases[]`, not `time_bands[]`. The Group B
            conversion landed in the CONSTITUTION at S6's P3 (2026-08-07, LP v2.2), so
            plans generated from here on emit `time_bands`; this fixture predates it and
            will not compile until the chapter is regenerated at C1. NOTE: the fixture's
            missing `section_anchor` is NOT a gap for this stage — science·middle has no
            section axis by design (carriers.has_section_axis), so `time_bands` is the
            only thing standing between it and compiling.

        **TWAU LEFT THIS LIST on 2026-08-11 (S5's P5.5).** It used to sit here as
        "periods carry `textbook_anchor` / `section_ref`, no `section_anchor`; TWAU's
        registry join has no owner yet; S5 owes it." It is owed no longer — the join is
        mediated on the plugin (`genon_unit_anchor`) and the positive proof is
        `test_twau_preparatory_compiles_through_the_mediated_anchor` below. This is the
        signal working exactly as the docstring promised.

        Assertion note (2026-08-07): the `section_anchor` read is now mediated by
        carriers.unit_anchor, which still raises KeyError on a section-axis stage but
        names the period and the stage in the message. The failure MODE is what this
        test guards, so it matches on the substring rather than the bare key.
        """
        from aruvi_core.genon import compile_stream
        for fixture, missing in (("science_vii_ch02_saved.json", "time_bands"),):
            with self.subTest(fixture=fixture):
                with self.assertRaises(KeyError) as cm:
                    compile_stream(load(fixture))
                self.assertIn(missing, str(cm.exception.args[0]))
                # the seam itself is fine — items extract as dicts
                plan = load(fixture)
                items = assessment_items(plan, plan.get("result", plan))
                self.assertTrue(all(isinstance(i, dict) for i in items))

    def test_twau_preparatory_compiles_through_the_mediated_anchor(self):
        """S5's P5.5, on the REAL saved shape rather than a fixture invented for it.

        `backup/saved_plans/the_world_around_us/v/ch_05_*` — 9 units over 6 sections, 9
        items (Rule 2's 1:1). Three properties, and the third is the one that earns the
        word "verbatim": every unit gets an anchor; every item resolves with zero orphans;
        and every anchor is a member of the registry drawn from the chapter summary's own
        `sections[].title`, byte for byte. The certifier's registry arithmetic is string
        comparison, so any reformatting in `genon_unit_anchor` would manufacture a mismatch
        that then needs a second normalizer to undo."""
        p = (Path(__file__).resolve().parents[1]
             / "backup/saved_plans/the_world_around_us/v/ch_05_20260531_122055.json")
        if not p.is_file():
            self.skipTest("TWAU V prototype plan not on disk")
        summ = (Path(__file__).resolve().parents[1]
                / "data/authoring/chapters/the_world_around_us/v/summaries/ch_05_summary.json")
        if not summ.is_file():
            self.skipTest("TWAU V ch 5 summary not on disk")

        from aruvi_core.genon import compile_stream
        stream = compile_stream(json.loads(p.read_text(encoding="utf-8")))

        anchors = [u.get("section_anchor") for u in stream["units"]]
        self.assertEqual(len(anchors), 9)
        self.assertTrue(all(a for a in anchors), "a unit compiled with no anchor")

        items = stream["assessment_items"]
        self.assertEqual(len(items), 9, "Rule 2 is 1:1 — one item per unit")
        self.assertFalse([i for i in items if not i.get("unit_ref")],
                         "row 8 is item-self-sufficient; nothing should orphan")

        registry = [s["title"] for s in
                    json.loads(summ.read_text(encoding="utf-8"))["sections"]]
        self.assertEqual([a for a in anchors if a not in registry], [],
                         "anchors must be VERBATIM members of the summary's registry")
        # first-visit order, which is what the choice set does string arithmetic on
        first_seen = list(dict.fromkeys(anchors))
        self.assertEqual(first_seen, registry[:len(first_seen)],
                         "sections must first-appear in registry order")

    def test_science_secondary_shape_compiles_with_its_questions_intact(self):
        """The live proof, on a real Grade IX file: 11 questions, not 8 wrapper keys."""
        p = (Path(__file__).resolve().parents[1]
             / "backup/saved_plans/science/ix/ch_08_20260612_151832.json")
        if not p.is_file():
            self.skipTest("science IX prototype plan not on disk")
        from aruvi_core.genon import compile_stream
        stream = compile_stream(json.loads(p.read_text(encoding="utf-8")))
        items = stream["assessment_items"]
        self.assertEqual(len(items), 11)
        for it in items:
            self.assertIsInstance(it, dict)
            self.assertTrue(it.get("unit_ref"))

    def test_science_secondary_SERVES_and_the_plan_keeps_its_native_handoff(self):
        """End to end: the shape that used to AttributeError inside serve's remap."""
        p = (Path(__file__).resolve().parents[1]
             / "backup/saved_plans/science/ix/ch_08_20260612_151832.json")
        if not p.is_file():
            self.skipTest("science IX prototype plan not on disk")
        from aruvi_core.genon import compile_stream, serve_plan
        stream = compile_stream(json.loads(p.read_text(encoding="utf-8")))
        for x in (11, 9, 6):
            with self.subTest(x=x):
                served = serve_plan([stream], [(50, x)])["result"]
                ho = served["coverage_handoff"]
                self.assertIsInstance(ho, list, "must come back as science's ARRAY")
                self.assertEqual(len(served["lesson_plan"]["periods"]), x)
                for h in ho:
                    self.assertIn("period_numbers", h)
                    self.assertNotIn("_carrier", h, "engine marker leaked into a served plan")


# ── S7 · the MEDIATED-ANCHOR SYNTHESIS MANDATE (2026-08-10) ──────────────────────
#
# THE DEFECT. `variant_plans.top_brief_for` mandated, for every section-axis stage, that
# the standard canonical's final unit put the reserved token `synthesis` in its
# `section_anchor`. mathematics·middle has NO `section_anchor` field in its constitution —
# its anchor is mediated from `textbook_segments[].ref` — so that brief would have asked a
# metered STEP 1 generation for a field the constitution never defines, and the certifier's
# synthesis gate would then have found no synthesis unit in the library it had paid for.
# The S7 analogue of S4's synthesis-handoff defect, and like it a BRIEF matter: no
# constitution is amended (founder ruling 2026-08-10).
#
# THE ANSWER ALREADY EXISTED. `carriers.is_synthesis` has read two carriers for one fact
# since S6 — the reserved token, OR `period["synthesis"] is True` — and `_arc_brief` already
# asks for the boolean at plan granularity. What was wrong was the TEST for which to ask:
# "has no section axis" instead of "has no field to put a token in".
#
# THESE TESTS PIN BOTH SIDES: the mediated stage gets the boolean, and the ten stages that
# have the field get wording byte-identical to what their certified libraries were authored
# against. The exact pre-change lines are literals below; that is the proof.

_TOKEN_MANDATE = (
    "- THE SYNTHESIS MANDATE (this plan alone carries it): unit {n}, the final unit, is "
    "a WHOLE-CHAPTER SYNTHESIS and its section_anchor is exactly the single word: "
    "synthesis (the reserved token — NOT a section name, no joining). It draws the entire "
    "chapter together as a real unit-arc. It may assume every SECTION'S CONTENT has been "
    "taught, and may connect back to concepts BY NAME — but it must NOT assume any "
    "particular earlier activity, reading, discussion, homework or material actually "
    "happened: it will be served to classes that covered the same sections through "
    "DIFFERENT units.")
_TOKEN_COVERAGE = (
    "- COVERAGE COMPLETES BEFORE THE SYNTHESIS: all registry sections first-appear across "
    "units 1..{m}. No other unit may use the synthesis token.")
# Updated 2026-08-10 (founder ruling, S7 · C9). The compact brief lost two things it was
# never authorised to say: "a later unit may revisit earlier sections" — which flatly
# contradicted LP Rule 1's contiguity sentence in the SAME request — and a COVERAGE bullet
# that mandated a MECHANISM ("ADJACENT sections share a unit") as well as the outcome. The
# second is where p10's composite closing unit came from. These literals now pin the NEW
# text, so an unintended drift is caught; the two absences are asserted separately below,
# because those are the regressions that would actually hurt.
_TOKEN_REGISTRY_RULE = (
    "  Every unit's section_anchor MUST be drawn verbatim from this list (a multi-section "
    "unit joins its sections with \" / \" in list order). Sections must FIRST APPEAR in "
    "registry order. The token `synthesis` is RESERVED to the chapter's standard canonical "
    "— never use it here.")
_COVERAGE_LINE = ("- A canonical covers the whole chapter: section_coverage_note is not "
                  "available here.")

# The eleven certified subject·stages, one representative class each.
_STAGES = [("science", "VII"), ("science", "IX"),
           ("social_sciences", "VII"), ("social_sciences", "IX"),
           ("mathematics", "IV"), ("mathematics", "VII"), ("mathematics", "IX"),
           ("english", "IV"), ("english", "VII"), ("english", "IX"),
           ("the_world_around_us", "IV")]


def _vp():
    """`genon/variant_plans.py` is a script, not a package module — it lives outside
    aruvi_core and imports its siblings by bare name, so its own directory has to be on
    the path before it will load."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "genon"))
    import variant_plans
    return variant_plans


def _count(vp, subject, klass, chapter):
    """The standard canonical's unit count, read the way the brief reads it."""
    combo = json.loads(Path(vp.MP).read_text())["combos"][f"{subject}|{klass}"]
    row = next(c for c in combo["chapters"] if c["chapter"] == int(chapter))
    return int(row["recommended_periods"])


class TestAnchorFieldPresent(unittest.TestCase):
    """The declaration itself — asked of the plugin, never sniffed from an override."""

    # THE MEDIATED STAGES, as of 2026-08-12 (S11): mathematics middle + preparatory,
    # the_world_around_us preparatory, and now ENGLISH at all three stages. Four field
    # shapes, one seam — and english's is the only COMPOSITE one (`section_id` +
    # `spines_taught[]`, joined into "A|listening").
    _MEDIATED = {("mathematics", "IV"), ("mathematics", "VII"),
                 ("the_world_around_us", "IV"),
                 ("english", "IV"), ("english", "VII"), ("english", "IX")}

    def test_the_field_stages_declare_the_field_present(self):
        from aruvi_core.genon.carriers import anchor_field_present
        for subject, klass in _STAGES:
            if (subject, klass) in self._MEDIATED:
                continue
            with self.subTest(stage=f"{subject}·{klass}"):
                self.assertTrue(anchor_field_present(subject, klass))

    def test_mathematics_middle_and_preparatory_declare_it_absent(self):
        from aruvi_core.genon.carriers import anchor_field_present
        for klass in ("III", "IV", "V", "VI", "VII", "VIII"):
            with self.subTest(klass=klass):
                self.assertFalse(anchor_field_present("mathematics", klass),
                                 "grep -c section_anchor is 0 in both constitutions")
        self.assertTrue(anchor_field_present("mathematics", "IX"),
                        "secondary keeps the field (LP A3) — one plugin, three answers")

    def test_twau_preparatory_declares_it_absent(self):
        """Landed 2026-08-11 at S5's P5.5. TWAU has a section axis (LP Rule 1 is titled
        SINGLE-AXIS SECTION ANCHORING) and spells the anchor `section_ref` — a THIRD field
        name, after maths·middle's `textbook_segments[].ref` and maths·prep's
        `section_refs[]`. `grep -c section_anchor` is 0 in its LP constitution, and the
        founder ruling of 2026-08-10 forbids adding one, so the read is mediated."""
        from aruvi_core.genon.carriers import anchor_field_present, has_section_axis
        for klass in ("III", "IV", "V"):
            with self.subTest(klass=klass):
                self.assertFalse(anchor_field_present("the_world_around_us", klass))
                self.assertTrue(has_section_axis("the_world_around_us", klass),
                                "the axis is real — only the field name differs")

    def test_english_declares_it_absent_at_every_stage(self):
        """Landed 2026-08-12 at S11's P5.5. `grep -c section_anchor` is 0 in ALL THREE
        english LP constitutions — one grep, three stages, which is why this is asserted for
        the family rather than for the certified stage alone. The axis is real and is the
        (section × spine) CELL the constitution's own DESIGN PRINCIPLE names; only the field
        is missing, and the anchor is built from the two fields that are there."""
        from aruvi_core.genon.carriers import anchor_field_present, has_section_axis
        for klass in ("III", "IV", "V", "VI", "VII", "VIII", "IX"):
            with self.subTest(klass=klass):
                self.assertFalse(anchor_field_present("english", klass))
                self.assertTrue(has_section_axis("english", klass),
                                "the axis is the cell — only the field name is absent")

    def test_it_is_not_the_same_question_as_the_section_axis(self):
        """maths·middle HAS a section axis and has no field; science·middle has neither.
        A caller that read one for the other gets maths·middle wrong."""
        from aruvi_core.genon.carriers import anchor_field_present, has_section_axis
        self.assertTrue(has_section_axis("mathematics", "VII"))
        self.assertFalse(anchor_field_present("mathematics", "VII"))
        self.assertFalse(has_section_axis("science", "VII"))

    def test_an_unknown_subject_gets_the_platform_default(self):
        from aruvi_core.genon.carriers import anchor_field_present
        self.assertTrue(anchor_field_present("Astrophysics", "VII"))


class TestStandardBriefSynthesisCarrier(unittest.TestCase):
    """`variant_plans.top_brief_for` — which carrier the mandate asks for."""

    def test_mathematics_middle_is_asked_for_the_BOOLEAN(self):
        vp = _vp()
        text = vp.top_brief_for("mathematics", "VII", 1)
        n = _count(vp, "mathematics", "VII", 1)
        self.assertIn('`"synthesis": true` on its period object', text)
        self.assertIn(f"unit {n}, the final unit, is a WHOLE-CHAPTER SYNTHESIS", text)

    def test_mathematics_middle_is_never_asked_for_section_anchor(self):
        """The whole defect in one assertion: a field its constitution does not define,
        demanded at metered STEP 1."""
        vp = _vp()
        for klass in ("VI", "VII", "VIII", "IV"):
            with self.subTest(klass=klass):
                text = vp.top_brief_for("mathematics", klass, 1)
                self.assertNotIn("section_anchor", text)
                self.assertNotIn("the single word: synthesis", text)

    def test_the_no_other_unit_line_forbids_the_BOOLEAN_on_a_mediated_stage(self):
        vp = _vp()
        text = vp.top_brief_for("mathematics", "VII", 1)
        n = _count(vp, "mathematics", "VII", 1)
        self.assertIn(f"first-appear across units 1..{n - 1}. "
                      'No other unit may carry `"synthesis": true`.', text)

    def test_twau_preparatory_is_asked_for_the_BOOLEAN(self):
        """Added 2026-08-11 at S5's P5.5, and it is the same defect as maths·middle's on a
        third field name: without `genon_anchor_field_present` the brief would have asked a
        TWAU generation, at metered STEP 1, to put the reserved token in a `section_anchor`
        its constitution does not define — and the certifier's synthesis gate would then
        have found no synthesis unit in the library it had already paid for."""
        vp = _vp()
        for klass in ("III", "IV", "V"):
            with self.subTest(klass=klass):
                text = vp.top_brief_for("the_world_around_us", klass, 1)
                n = _count(vp, "the_world_around_us", klass, 1)
                self.assertIn('`"synthesis": true` on its period object', text)
                self.assertIn(f"unit {n}, the final unit, is a WHOLE-CHAPTER SYNTHESIS",
                              text)
                self.assertNotIn("section_anchor", text)
                self.assertNotIn("the single word: synthesis", text)

    def test_english_is_asked_for_the_BOOLEAN(self):
        """Added 2026-08-12 at S11's P5.5 — the fourth stage-family to need it, and the one
        where the token would have been hardest to spot as wrong: english's period carries
        `section_id`, so a brief demanding `section_anchor` would have looked almost right
        and produced a field the constitution never defines, at metered STEP 1."""
        vp = _vp()
        for klass in ("IV", "VII", "IX"):
            with self.subTest(klass=klass):
                text = vp.top_brief_for("english", klass, 1)
                n = _count(vp, "english", klass, 1)
                self.assertIn('`"synthesis": true` on its period object', text)
                self.assertIn(f"unit {n}, the final unit, is a WHOLE-CHAPTER SYNTHESIS",
                              text)
                self.assertNotIn("section_anchor", text)
                self.assertNotIn("the single word: synthesis", text)

    def test_the_field_stages_keep_BYTE_IDENTICAL_wording(self):
        """The two lines this change touches, verbatim as they read before it. The
        declared-field stages must not be re-briefed by a fix made for a mediated one.

        `the_world_around_us·III` LEFT this list on 2026-08-11 (S5) and ENGLISH left it on
        2026-08-12 (S11): both are mediated stages now, and are covered by
        `test_twau_preparatory_is_asked_for_the_BOOLEAN` and
        `test_english_is_asked_for_the_BOOLEAN` respectively."""
        vp = _vp()
        for subject, klass in (("mathematics", "IX"), ("social_sciences", "IX"),
                               ("social_sciences", "VII"), ("science", "IX")):
            with self.subTest(stage=f"{subject}·{klass}"):
                text = vp.top_brief_for(subject, klass, 1)
                n = _count(vp, subject, klass, 1)
                self.assertIn(_TOKEN_MANDATE.format(n=n), text)
                self.assertIn(_TOKEN_COVERAGE.format(m=n - 1), text)
                self.assertNotIn('"synthesis": true', text)

    def test_the_plan_granularity_stage_is_untouched(self):
        """science·middle already had the boolean, by the older (narrower) test."""
        vp = _vp()
        text = vp.top_brief_for("science", "VII", 1)
        self.assertIn('`"synthesis": true`', text)
        self.assertIn("THE ARC IS YOURS AT THIS COUNT", text)


class TestSynthesisReadsAsSynthesisOnScreen(unittest.TestCase):
    """The closing unit must reach the teacher as "Synthesis" — the DISPLAY half of §0.3.

    This is the third time the same defect has been found by eye rather than by a test, on
    a third stage, which is why it is now a test:

      • ARV-D-016 (S1, SS·secondary)  — U12 filed under "Climate Change", the section it
        happened to name, though it is a chapter-wide synthesis.
      • ARV-D-101 (S7, maths·middle)  — every SERVED closer read "Equilateral Triangles
        (Revisit)". The canonical on disk said "Synthesis" and the served plan did not,
        which is the worse half: the served plan is what a teacher opens.
      • S5, TWAU·preparatory (2026-08-11) — this port grouped purely on `section_ref`, and
        TWAU's closer wears a REAL section title (its anchor is mediated, so there is no
        reserved token to file it under), so the synthesis merged into a three-unit
        "Spirit of Togetherness" group.

    The guard is one property, asked of every SECTION-GROUPED port: given a unit the seam
    calls a synthesis, the last group's label is `normalize.SYNTHESIS_DISPLAY` — not the
    reserved token verbatim (lowercase among capitalised headings), not a section name, and
    never "(Revisit)". Reading the fact off the title or the anchor instead of through
    `carriers.is_synthesis` is what failed twice, so the probe deliberately gives each port
    the carrier ITS stage uses and nothing else to go on.

    `social_sciences` and `english` are NOT probed, and the reason is recorded rather than
    skipped into silence: SS·secondary renders as a single flat "Units" group with no
    per-section headings at all, so its synthesis is identified by its own `activity_title`
    ("Atmosphere to Action: A Whole-Chapter Synthesis") and there is no group label to get
    wrong. ENGLISH JOINED THE PROBE at S11 (2026-08-12): it groups on the (section, spine
    signature) pair, which is a section-grouped port by this test's definition, and its
    closer would otherwise read as whichever spines it revisits.
    """

    def test_every_section_grouped_port_labels_the_closer(self):
        from aruvi_core import subjects as SUB
        from aruvi_core.normalize import SYNTHESIS_DISPLAY
        for m in ("science", "mathematics", "the_world_around_us", "english"):
            __import__(f"aruvi_core.subjects.{m}")

        # Each stage's OWN synthesis carrier, and its own anchor field — a port that reads
        # the right thing needs no more than this.
        cases = {
            "science":             {"section_anchor": "synthesis",     # token stage
                                    "progression_stage": 9, "stage_label": "Synthesis"},
            "mathematics":         {"section_anchor": "synthesis"},    # token stage (IX)
            "the_world_around_us": {"section_ref": "Spirit of Togetherness"},  # mediated
            # english is mediated too, and on a COMPOSITE anchor: the closer names the
            # spines it revisits, so a port grouping on the spine signature would file it
            # under "Listening + Writing" (S11, 2026-08-12).
            "english":             {"section_id": "A", "section_title": "T",
                                    "spines_taught": ["listening", "writing"]},
        }
        for key, extra in cases.items():
            with self.subTest(subject=key):
                period = {"period_number": 1, "period_duration_minutes": 40,
                          "activity_title": "Whole-Chapter Synthesis: Drawing It Together",
                          "time_bands": [{"minutes": "0-40", "activity": "a"}],
                          "synthesis": True, "materials": [], "implied_lo": "",
                          "teacher_notes": "", **extra}
                raw = {"lesson_plan": {"periods": [period]}, "coverage_handoff": [],
                       "subject": key, "grade": "ix"}
                view = SUB.get(key).lesson_plan_to_view(
                    raw, grade="ix", chapter={"chapter_number": 1, "chapter_title": "t"})
                self.assertTrue(view.groups, f"{key}: produced no groups at all")
                self.assertEqual(
                    view.groups[-1].label, SYNTHESIS_DISPLAY,
                    f"{key}: the closer reads {view.groups[-1].label!r} — ARV-D-101's shape")

    def test_twau_keeps_the_synthesis_out_of_its_section_group(self):
        """The specific regression: TWAU's closer names a real registry section, so a port
        that groups on `section_ref` alone MERGES it with that section's teaching units.
        Two units, same `section_ref`, one of them the synthesis -> two groups, not one."""
        from aruvi_core import subjects as SUB
        from aruvi_core.normalize import SYNTHESIS_DISPLAY
        import aruvi_core.subjects.the_world_around_us          # noqa: F401

        def unit(n, synth=False):
            p = {"period_number": n, "period_duration_minutes": 40,
                 "activity_title": f"Unit {n}", "section_ref": "Spirit of Togetherness",
                 "dominant_mode": "D&C", "materials": [], "implied_lo": "",
                 "time_bands": [{"minutes": "0-40", "activity": "a"}]}
            if synth:
                p["synthesis"] = True
            return p

        raw = {"lesson_plan": {"periods": [unit(1), unit(2), unit(3, synth=True)]}}
        view = SUB.get("the_world_around_us").lesson_plan_to_view(
            raw, grade="v", chapter={"chapter_number": 5, "chapter_title": "t"})
        self.assertEqual([g.label for g in view.groups],
                         ["Spirit of Togetherness", SYNTHESIS_DISPLAY])
        self.assertEqual([p.number for p in view.groups[0].periods], [1, 2])
        self.assertEqual([p.number for p in view.groups[1].periods], [3])
        # and the synthesis group must not claim the section as its own
        self.assertFalse(view.groups[1].meta.get("section_ref"))


class TestCompactBriefSynthesisCarrier(unittest.TestCase):
    """`variant_plans.briefs_for` — a compact carrying a synthesis unit is exactly the
    ARV-D-025 failure v2.0 exists to prevent, so the prohibition has to be stated in the
    carrier that stage actually uses. Forbidding a token it was never going to emit
    forbids nothing.

    The real master plan has no finalized mathematics row, so the row is staged in a temp
    copy and the registry is stubbed — `briefs_for`'s wording is what is under test, not
    its disk lookups."""

    REG = ["section 5.1", "section 5.2", "section 5.3"]

    def _briefs(self, subject, klass, chapter=1):
        vp = _vp()
        mp = json.loads(Path(vp.MP).read_text())
        row = next(c for c in mp["combos"][f"{subject}|{klass}"]["chapters"]
                   if c["chapter"] == chapter)
        row["canonical_plan"] = {"counts": [int(row["recommended_periods"]), 8],
                                 "provisional": False, "basis": "authored_standard",
                                 "registry_sections": len(self.REG), "authored": []}
        tmp = Path(tempfile.mkdtemp()) / "master_plan.json"
        tmp.write_text(json.dumps(mp, ensure_ascii=False))
        old_mp, old_reg = vp.MP, vp.standard_registry
        vp.MP = str(tmp)
        vp.standard_registry = lambda *a, **k: list(self.REG)
        try:
            return vp.briefs_for(subject, klass, chapter)[0]
        finally:
            vp.MP, vp.standard_registry = old_mp, old_reg

    def test_a_mathematics_middle_compact_declares_the_BOOLEAN_FALSE(self):
        """A POSITIVE declaration replaced the prohibition (founder, 2026-08-10). A ban can
        only be obeyed by absence, and absence is indistinguishable from never having
        considered it; `false` on every unit is auditable."""
        for text in self._briefs("mathematics", "VII").values():
            self.assertIn('Emit `"synthesis": false` on every unit', text)
            self.assertNotIn('"synthesis": true', text)
            self.assertNotIn("section_anchor", text)
            self.assertNotIn("The token `synthesis`", text)

    def test_no_compact_brief_may_invite_a_revisit_or_a_merge(self):
        """The two deletions, asserted for EVERY stage — this is the regression that matters.
        Four LP amendments (v3.5-v3.8) failed to stop the composite closing unit because the
        brief in the same request kept granting what they forbade."""
        for subject, klass in (("mathematics", "VII"), ("mathematics", "IX"),
                               ("social_sciences", "IX"), ("english", "VII")):
            for text in self._briefs(subject, klass).values():
                with self.subTest(stage=f"{subject}·{klass}"):
                    self.assertNotIn("may revisit earlier sections", text)
                    self.assertNotIn("CLOSING SHAPE", text)
                    self.assertNotIn("ADJACENT sections share a unit", text)
                    self.assertNotIn("judgment is yours", text)
                    self.assertIn(_COVERAGE_LINE, text)

    def test_a_field_stage_compact_is_BYTE_IDENTICAL(self):
        """english·VII LEFT this list on 2026-08-12 (S11) — it is a mediated stage now, so
        its compacts get the field-neutral registry rule, asserted below."""
        for subject, klass in (("mathematics", "IX"), ("social_sciences", "IX")):
            with self.subTest(stage=f"{subject}·{klass}"):
                for text in self._briefs(subject, klass).values():
                    self.assertIn(_TOKEN_REGISTRY_RULE, text)
                    self.assertNotIn('"synthesis": true', text)

    def test_an_english_compact_gets_the_MEDIATED_registry_rule(self):
        """Added 2026-08-12 (S11). A compact of a mediated stage must not be told to put its
        anchor in `section_anchor`, and must still be told the closing synthesis belongs to
        the standard alone — the pair maths·middle already gets, on a fourth field shape."""
        for klass in ("IV", "VII", "IX"):
            with self.subTest(klass=klass):
                for text in self._briefs("english", klass).values():
                    self.assertIn("in the field your own constitution already defines for "
                                  "it", text)
                    self.assertIn('Emit `"synthesis": false` on every unit', text)
                    self.assertNotIn("section_anchor", text)
                    self.assertNotIn('"synthesis": true', text)


class TestCertifierHoldsOnAMediatedAnchorStage(unittest.TestCase):
    """The four reads the synthesis gate depends on, exercised with the BOOLEAN carrier on
    a stage whose anchor is mediated (maths·middle). Two of them read the anchor STRING
    directly and were fixed to go through the seam — `serve.section_registry` and
    `serve.unit_range`; `is_synthesis_unit` and the certifier's own `body`/advisory filters
    already used it. `carriers.unit_anchor` gained the third fix: a synthesis unit has no
    textbook segment to mediate FROM, and the section-axis raise fired on it."""

    def _stream(self, synthesis_segments=None):
        from aruvi_core.genon import compile_stream
        plan = load("maths_vi_ch05_saved.json")
        for p in plan["result"]["lesson_plan"]["periods"]:
            # the fixture is prototype-era (`phases[]`); compile reads `time_bands[]`
            p["time_bands"] = [{"minutes": ph["minutes"], "activity": ph["description"]}
                               for ph in p.pop("phases")]
        periods = plan["result"]["lesson_plan"]["periods"]
        closer = json.loads(json.dumps(periods[-1]))
        closer["period_number"] = len(periods) + 1
        closer["activity_title"] = "Whole-chapter synthesis"
        closer["synthesis"] = True
        closer.pop("textbook_segments", None)
        if synthesis_segments:
            closer["textbook_segments"] = [{"ref": r} for r in synthesis_segments]
        periods.append(closer)
        return compile_stream(plan)

    def test_a_the_standards_synthesis_unit_is_recognised(self):
        from aruvi_core.genon.serve import is_synthesis_unit
        units = self._stream()["units"]
        self.assertEqual([u["unit"] for u in units if is_synthesis_unit(u)], [11])
        self.assertIsNone(units[-1]["section_anchor"],
                          "nothing to mediate from — and no token is invented for it")

    def test_a_the_mediated_synthesis_unit_no_longer_kills_compile(self):
        """Before the fix `carriers.unit_anchor` raised KeyError on it, because the stage
        has a section axis and the closer teaches no segment — the loudest possible
        version of 'the certifier finds no synthesis unit'."""
        from aruvi_core.genon.carriers import unit_anchor
        self.assertIsNone(unit_anchor({"period_number": 11, "synthesis": True},
                                      subject="Mathematics", grade="Grade VI"))
        with self.assertRaises(KeyError):        # a non-synthesis unit still raises
            unit_anchor({"period_number": 4}, subject="Mathematics", grade="Grade VI")

    def test_b_it_is_excluded_from_the_registry_and_from_first_visit_arithmetic(self):
        from aruvi_core.genon.serve import (_norm, first_dealing_unit, is_synthesis_unit,
                                            section_registry, unit_range)
        for segs in (None, ["section 5.1", "section 5.6"]):
            with self.subTest(synthesis_segments=segs):
                s = self._stream(synthesis_segments=segs)
                reg = section_registry(s)
                self.assertEqual(reg, [f"section 5.{i}" for i in range(1, 7)])
                ridx = {_norm(a): i for i, a in enumerate(reg)}
                self.assertIsNone(unit_range(s["units"][-1], ridx),
                                  "a synthesis unit must never be a first-dealing candidate")
                for m in range(len(reg)):
                    hit = first_dealing_unit(s, ridx, m)
                    self.assertIsNotNone(hit)
                    self.assertFalse(is_synthesis_unit(hit[1]))
                # certify checks 3-5, run exactly as build_library runs them
                body = [u for u in s["units"] if not is_synthesis_unit(u)]
                seen, order_ok = -1, True
                for u in body:
                    r = unit_range(u, ridx)
                    self.assertIsNotNone(r, "every body anchor verbatim in the registry")
                    if r[1] > seen:
                        order_ok = order_ok and r[0] <= seen + 1
                        seen = r[1]
                self.assertTrue(order_ok)
                self.assertEqual(seen, len(reg) - 1, "coverage reaches the final section")

    def test_c_a_compact_carrying_the_boolean_still_FAILS_the_gate(self):
        """The gate is `not syn_units` on a file the certifier has already decided is a
        compact, so what has to hold is that the BOOLEAN form is found at all — the token
        stages get this free because the reserved word is in `section_anchor`.

        The flagged unit is APPENDED rather than converted from a teaching unit. Converting
        one produced a plan the brief forbids in terms ("COVERAGE COMPLETES BEFORE THE
        SYNTHESIS"): the fixture's last unit is the only one teaching section 5.6, so
        flagging it left that section taught by nothing, and its item `Q-C-5` orphaned at
        compile. That is the index working as designed — a synthesis unit teaches no
        section, so it is not in the item index — and it is exactly the case the next test
        pins deliberately."""
        from aruvi_core.genon.serve import is_synthesis_unit
        s = self._stream()
        syn = [u["unit"] for u in s["units"] if is_synthesis_unit(u)]
        self.assertTrue(syn, "the gate's `not syn_units` must be False here")

    def test_c_a_section_taught_ONLY_by_the_synthesis_unit_orphans_its_item(self):
        """The deliberate edge of excluding the synthesis unit from the item index, pinned
        so nobody 'fixes' it back (2026-08-10, S7).

        The exclusion exists because ch 7's synthesis unit lists all five sections it draws
        together: indexed, it became the LAST unit of every section, and since an item
        anchors at its section's last unit, all twelve items collapsed onto it and units
        1-11 showed no assessment at all. The cost of excluding it is this: a section no
        BODY unit teaches has no anchor, and its item orphans loudly at compile rather than
        landing on a sitting that never taught it. The brief prevents the situation
        ("COVERAGE COMPLETES BEFORE THE SYNTHESIS"), and a loud orphan is the right failure
        if it ever does not."""
        from aruvi_core.genon import GenonDeclarationError, compile_stream
        plan = load("maths_vi_ch05_saved.json")
        for p in plan["result"]["lesson_plan"]["periods"]:
            p["time_bands"] = [{"minutes": ph["minutes"], "activity": ph["description"]}
                               for ph in p.pop("phases")]
        periods = plan["result"]["lesson_plan"]["periods"]
        periods[-1]["synthesis"] = True           # section 5.6's only teaching unit
        with self.assertRaises(GenonDeclarationError) as cm:
            compile_stream(plan)
        self.assertIn("Q-C-5", str(cm.exception))
        self.assertIn("no resolvable anchor unit", str(cm.exception))

    def test_d_the_unit_routed_by_nothing_advisory_does_not_fire_on_it(self):
        """Two independent reasons, both checked: this stage's `coverage_handoff` is a
        goal-cluster DICT and the advisory block only walks a LIST handoff; and the block's
        own filter goes through `is_synthesis_unit`, so the boolean form is excluded even
        where a list handoff exists."""
        from aruvi_core.genon.serve import is_synthesis_unit
        plan = load("maths_vi_ch05_saved.json")
        self.assertIsInstance(plan["result"]["coverage_handoff"], dict)
        s = self._stream()
        routed = set()                            # nothing routes, as the dict is skipped
        unrouted = [u["unit"] for u in s["units"]
                    if u["unit"] not in routed and not is_synthesis_unit(u)]
        self.assertNotIn(11, unrouted)

    def test_the_served_plan_still_ends_on_the_synthesis_at_full_count(self):
        from aruvi_core.genon import serve_plan
        s = self._stream()
        for x, n in ((11, 11), (10, 10), (6, 6)):
            with self.subTest(x=x):
                served = serve_plan([s], [(40, x)])["result"]
                self.assertEqual(len(served["lesson_plan"]["periods"]), n)
        top = serve_plan([s], [(40, 11)])["result"]["lesson_plan"]["periods"]
        self.assertEqual(top[-1]["activity_title"], "Whole-chapter synthesis")


if __name__ == "__main__":
    os.environ.setdefault("ARUVI_DATA_DIR", str(Path(__file__).resolve().parents[1]
                                                / "data" / "cloud" / "content"))
    unittest.main(verbosity=2)
