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

    def test_mathematics_MIDDLE_still_raises_with_the_owing_stage_named(self):
        plan = load("maths_vi_ch05_saved.json")
        with self.assertRaises(CarrierNotImplemented) as cm:
            assessment_items(plan, plan.get("result", plan))
        msg = str(cm.exception)
        self.assertIn("mathematics", msg)
        self.assertIn("period-field", msg, "must name the family it actually belongs to")

    def test_english_raises_with_the_owing_stage_named(self):
        plan = load("english_vii_ch01_saved.json")
        with self.assertRaises(CarrierNotImplemented) as cm:
            assessment_items(plan, plan.get("result", plan))
        self.assertIn("english", str(cm.exception))


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


class TestCarrierPreFlight(unittest.TestCase):
    """The gate must be FREE. Before 2026-08-08 the answer arrived at certification, which
    runs after the metered steps, so a missing carrier cost a whole library (₹110-150) and
    reported itself as "does not compile" on every file. testing.md P5.5."""

    def test_ready_stages_report_no_gap(self):
        from aruvi_core.genon.carriers import carrier_gap
        for subject, grade in (("mathematics", "ix"), ("science", "ix"), ("science", "viii"),
                               ("social_sciences", "ix"), ("the_world_around_us", "v")):
            self.assertIsNone(carrier_gap(subject, grade), f"{subject}·{grade}")

    def test_owed_stages_report_their_stage_and_row(self):
        from aruvi_core.genon.carriers import carrier_gap
        for subject, grade, owes in (("mathematics", "vii", "S7"),
                                     ("mathematics", "iii", "S8"),
                                     ("english", "iii", "S9"),
                                     ("english", "vi", "S10"),
                                     ("english", "ix", "S11")):
            gap = carrier_gap(subject, grade)
            self.assertIsNotNone(gap, f"{subject}·{grade} is not implemented")
            self.assertIn(owes, gap, "the gap must name the stage that owes it")

    def test_a_missing_grade_is_conservative_not_optimistic(self):
        """Guessing "ready" is the expensive mistake, so an unknown grade on a subject that
        still owes any stage reads as owed."""
        from aruvi_core.genon.carriers import carrier_gap
        self.assertIsNotNone(carrier_gap("mathematics", None))
        self.assertIsNone(carrier_gap("social_sciences", None), "owes nothing at any stage")

    def test_require_carrier_raises_only_for_owed(self):
        from aruvi_core.genon.carriers import require_carrier
        require_carrier("mathematics", "ix")                       # must not raise
        with self.assertRaises(CarrierNotImplemented):
            require_carrier("mathematics", "vii")


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
        """Two fixtures do NOT compile, and the reason is the LESSON PLAN shape, not the
        carrier seam — their items extract fine (see the family tests above). Recorded
        here so the gap is registered rather than skipped into silence. When either is
        closed this test FAILS, which is the signal to update it.

          • science·middle  — periods carry `phases[]`, not `time_bands[]`. The Group B
            conversion landed in the CONSTITUTION at S6's P3 (2026-08-07, LP v2.2), so
            plans generated from here on emit `time_bands`; this fixture predates it and
            will not compile until the chapter is regenerated at C1. NOTE: the fixture's
            missing `section_anchor` is NOT a gap for this stage — science·middle has no
            section axis by design (carriers.has_section_axis), so `time_bands` is the
            only thing standing between it and compiling.
          • TWAU            — periods carry `textbook_anchor` / `section_ref`, no
            `section_anchor`. TWAU's registry join has no owner yet; S5 owes it.

        Assertion note (2026-08-07): the `section_anchor` read is now mediated by
        carriers.unit_anchor, which still raises KeyError on a section-axis stage but
        names the period and the stage in the message. The failure MODE is what this
        test guards, so it matches on the substring rather than the bare key.
        """
        from aruvi_core.genon import compile_stream
        for fixture, missing in (("science_vii_ch02_saved.json", "time_bands"),
                                 ("twau_iii_ch01_saved.json", "section_anchor")):
            with self.subTest(fixture=fixture):
                with self.assertRaises(KeyError) as cm:
                    compile_stream(load(fixture))
                self.assertIn(missing, str(cm.exception.args[0]))
                # the seam itself is fine for both — items extract as dicts
                plan = load(fixture)
                items = assessment_items(plan, plan.get("result", plan))
                self.assertTrue(all(isinstance(i, dict) for i in items))

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


if __name__ == "__main__":
    os.environ.setdefault("ARUVI_DATA_DIR", str(Path(__file__).resolve().parents[1]
                                                / "data" / "content"))
    unittest.main(verbosity=2)
