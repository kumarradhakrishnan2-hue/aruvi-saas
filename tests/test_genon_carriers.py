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
    CarrierNotImplemented, assessment_items, items_by_handoff, subject_key,
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


class TestUnimplementedFamiliesFailLoudly(unittest.TestCase):
    """A subject genon has never run on must REFUSE, not return something plausible."""

    def test_mathematics_raises_with_the_owing_stage_named(self):
        plan = load("maths_ix_ch02_saved.json")
        with self.assertRaises(CarrierNotImplemented) as cm:
            assessment_items(plan, plan.get("result", plan))
        self.assertIn("mathematics", str(cm.exception))

    def test_english_raises_with_the_owing_stage_named(self):
        plan = load("english_vii_ch01_saved.json")
        with self.assertRaises(CarrierNotImplemented) as cm:
            assessment_items(plan, plan.get("result", plan))
        self.assertIn("english", str(cm.exception))


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

          • science·middle  — periods carry `phases[]`, not `time_bands[]`. This is
            exactly the Group B conversion testing.md §3 P3 owes stage S6.
          • TWAU            — periods carry `textbook_anchor` / `section_ref`, no
            `section_anchor`. TWAU's registry join has no owner yet; S5 owes it.
        """
        from aruvi_core.genon import compile_stream
        for fixture, missing in (("science_vii_ch02_saved.json", "time_bands"),
                                 ("twau_iii_ch01_saved.json", "section_anchor")):
            with self.subTest(fixture=fixture):
                with self.assertRaises(KeyError) as cm:
                    compile_stream(load(fixture))
                self.assertEqual(cm.exception.args[0], missing)
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


if __name__ == "__main__":
    os.environ.setdefault("ARUVI_DATA_DIR", str(Path(__file__).resolve().parents[1]
                                                / "data" / "content"))
    unittest.main(verbosity=2)
