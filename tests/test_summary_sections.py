#!/usr/bin/env python3
"""Registry <-> chapter-summary reconciliation (batch-runbook trap 5, 2026-08-13).

The regression these lock is the FIRST DRAFT'S SILENT PASS: it gave "8.5" the parent
"8", `covered("8")` matched by containment against "8.1 Rediscovering…", and every
section in the chapter was therefore "covered by its ancestor". The gate reported ALL
PASS on the one library that had already been proved defective by hand.

Run directly: python3 tests/test_summary_sections.py
"""
import os
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "genon"))

os.environ.setdefault("ARUVI_DATA_DIR", str(REPO / "data" / "content"))

from summary_sections import (  # noqa: E402
    NONE, PROSE, STRUCTURED, closing_anchors, reconcile, summary_sections,
)


def sec(key, label=None, parent=None):
    from aruvi_core.genon.serve import _norm
    return {"key": _norm(key), "label": label or key,
            "parent": _norm(parent) if parent else None}


class TestReconcile(unittest.TestCase):
    def test_a_top_level_ref_has_no_ancestor_to_hide_behind(self):
        """8.5's 'parent' is the CHAPTER, and a chapter is not a section."""
        reg = ["8.1 Roots", "8.2 Models", "8.4 Symbols", "8.6 Mass Number"]
        missing, _, _ = reconcile(reg, [sec("8.5", "8.5 Atomic Number")])
        self.assertEqual(missing, ["8.5 Atomic Number"])

    def test_a_sub_section_is_covered_by_its_parent(self):
        reg = ["8.2 A Short Historical Journey"]
        missing, _, _ = reconcile(reg, [sec("8.2.1", "8.2.1 Thomson's model", parent="8.2")])
        self.assertEqual(missing, [])

    def test_a_sub_section_is_covered_by_a_grandparent(self):
        reg = ["8.2 A Short Historical Journey"]
        missing, _, _ = reconcile(
            reg, [sec("8.2.1.3", "8.2.1.3 A deeper cut", parent="8.2.1")])
        self.assertEqual(missing, [])

    def test_a_ref_is_matched_by_boundary_not_by_containment(self):
        """`8.1` must not be satisfied by a registry that only reaches 8.1.2."""
        missing, _, _ = reconcile(["8.1.2 Building up atoms"], [sec("8.1", "8.1 Roots")])
        self.assertEqual(missing, ["8.1 Roots"])

    def test_a_title_is_matched_by_containment_either_way(self):
        """A prose lead under-grabs at its own colon; the plan anchors the full title."""
        missing, _, _ = reconcile(["Punjab Floods 2025: A Case Study"],
                               [sec("Punjab Floods 2025")])
        self.assertEqual(missing, [])

    def test_the_reverse_direction_is_never_a_failure(self):
        """A registry entry the summary does not name is reported, never gated."""
        missing, _, extra = reconcile(
            ["Introduction to the Atmosphere", "Monsoon"], [sec("Monsoon")])
        self.assertEqual(missing, [])
        self.assertEqual(extra, ["Introduction to the Atmosphere"])

    def test_an_empty_summary_gates_nothing(self):
        self.assertEqual(reconcile(["Monsoon"], []), ([], [], ["Monsoon"]))

    def test_the_closing_synthesis_unit_teaches_but_is_not_in_the_registry(self):
        """It is skipped by `section_registry` so it never enters first-visit
        arithmetic — which is not the same as it teaching nothing."""
        missing, closing, _ = reconcile(
            ["Playing Together"], [sec("Playing Together"), sec("Let us reflect")],
            closing_anchors=["Let us reflect"])
        self.assertEqual(missing, [])
        self.assertEqual(closing, ["Let us reflect"])

    def test_the_reserved_token_teaches_nothing(self):
        """On a token-carrying stage the closing anchor is `synthesis`, which is not a
        section — so it must not launder a genuinely omitted one."""
        missing, closing, _ = reconcile(
            ["8.4 Symbols"], [sec("8.5", "8.5 Atomic Number")],
            closing_anchors=["synthesis"])
        self.assertEqual((missing, closing), (["8.5 Atomic Number"], []))

    def test_a_sub_section_is_covered_by_a_parent_the_closing_unit_teaches(self):
        missing, closing, _ = reconcile(
            [], [sec("8.2.1", "8.2.1 Thomson's model", parent="8.2")],
            closing_anchors=["8.2 Models"])
        self.assertEqual((missing, closing), ([], []))


class TestExtraction(unittest.TestCase):
    """Against the real corpus — the shapes are the specification."""

    def test_science_prose_yields_numbered_headings_and_is_structured(self):
        secs, kind = summary_sections("science", "ix", 8)
        self.assertEqual(kind, STRUCTURED)
        self.assertIn("8.5", [s["key"] for s in secs])
        self.assertEqual(next(s for s in secs if s["key"] == "8.2.1")["parent"], "8.2")
        self.assertIsNone(next(s for s in secs if s["key"] == "8.5")["parent"])

    def test_twau_json_yields_titles_and_is_structured(self):
        secs, kind = summary_sections("the_world_around_us", "iii", 1)
        self.assertEqual(kind, STRUCTURED)
        self.assertIn("let us reflect", [s["key"] for s in secs])

    def test_english_yields_spine_cells_not_the_lone_main_section(self):
        """Post-split a chapter is ONE main_section; a section-level list would
        reconcile one entry against six registry cells and prove nothing."""
        secs, kind = summary_sections("english", "ix", 7)
        self.assertEqual(kind, STRUCTURED)
        self.assertEqual(len(secs), 6)
        self.assertTrue(all("|" in s["key"] for s in secs))

    def test_maths_yields_refs(self):
        secs, kind = summary_sections("mathematics", "ix", 4)
        self.assertEqual(kind, STRUCTURED)
        self.assertEqual([s["key"] for s in secs][:3], ["4.1", "4.2", "4.3"])

    def test_social_science_is_prose_and_therefore_advisory(self):
        """The whole reason the SS gate is an advisory: the read is inferred."""
        _, kind = summary_sections("social_sciences", "ix", 3)
        self.assertEqual(kind, PROSE)

    def test_the_document_talking_about_itself_is_not_a_section(self):
        secs, _ = summary_sections("social_sciences", "ix", 3)
        leads = [s["key"] for s in secs]
        self.assertNotIn("chapter 03", leads)
        self.assertFalse([k for k in leads if k.startswith("the chapter")])

    def test_a_missing_summary_reports_rather_than_raises(self):
        self.assertEqual(summary_sections("science", "ix", 99), ([], NONE))


class TestAgainstTheInstalledCorpus(unittest.TestCase):
    def _top(self, subject, grade, ch):
        import json
        from aruvi_core.genon import compile_stream
        from aruvi_core.genon.serve import section_registry
        p = (REPO / "data" / "content" / "saved_plans" / subject / grade
             / f"ch_{ch:02d}_canonical.json")
        top = compile_stream(json.loads(p.read_text()))
        return section_registry(top), closing_anchors(top)

    def test_the_defect_that_motivated_the_check_is_caught(self):
        """science·ix ch 8 — the S3 pilot, certified ALL PASS, omits 8.5 Atomic Number.

        Its synthesis unit carries the reserved token, so the closing-unit allowance
        cannot rescue it — which is the point of keeping the token out of `closing`."""
        reg, clo = self._top("science", "ix", 8)
        secs, kind = summary_sections("science", "ix", 8)
        missing, closing, _ = reconcile(reg, secs, clo)
        self.assertEqual(kind, STRUCTURED)
        self.assertEqual(missing, ["8.5 Atomic Number"])
        self.assertEqual(closing, [])

    def test_a_clean_chapter_stays_clean(self):
        reg, clo = self._top("the_world_around_us", "v", 5)
        secs, _ = summary_sections("the_world_around_us", "v", 5)
        missing, _, extra = reconcile(reg, secs, clo)
        self.assertEqual((missing, extra), ([], []))

    def test_twau_iii_ch1_is_taught_by_its_closing_unit_and_does_not_fail(self):
        """The first sweep's two false positives. `Let us reflect` is anchored by the
        synthesis unit — which teaches its word-search, drawing and writing tasks —
        and `section_registry` skips that unit by design."""
        for ch in (1, 9):
            with self.subTest(chapter=ch):
                reg, clo = self._top("the_world_around_us", "iii", ch)
                secs, _ = summary_sections("the_world_around_us", "iii", ch)
                missing, closing, _ = reconcile(reg, secs, clo)
                self.assertNotIn("Let us reflect", reg)
                self.assertEqual(missing, [])
                self.assertEqual(closing, ["Let us reflect"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
