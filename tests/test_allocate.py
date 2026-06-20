"""
Allocate test — distribute a period budget across chapters.

- Algorithm: proportional to weight, respects per-chapter minimums, hits the total exactly.
- Per-subject seam: Social Sciences reads `chapter_weight`, the effort-index subjects read
  `effort_index` — verified on REAL mapping JSONs (heavier chapter gets more periods, which
  only holds if the right field is read).

Run standalone:  python3 tests/test_allocate.py
"""
from __future__ import annotations

import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import aruvi_core.subjects.science          # noqa: E402  (register)
import aruvi_core.subjects.social_sciences  # noqa: E402  (register)
from aruvi_core.allocate import allocate_for_subject, allocate_periods  # noqa: E402

FXM = os.path.join(os.path.dirname(__file__), "fixtures", "mappings")


def _mappings(subject):
    return [json.load(open(f)) for f in sorted(glob.glob(os.path.join(FXM, subject, "*.json")))]


def test_algorithm_basic_proportional_and_exact_total():
    items = [{"chapter_number": 1, "weight": 10}, {"chapter_number": 2, "weight": 5},
             {"chapter_number": 3, "weight": 5}]
    alloc = allocate_periods(items, 20)
    assert sum(a.periods for a in alloc) == 20            # exact total
    assert alloc[0].periods == 10 and alloc[1].periods == 5 and alloc[2].periods == 5  # proportional


def test_algorithm_respects_minimums():
    items = [{"chapter_number": 1, "weight": 1, "min_periods": 4},
             {"chapter_number": 2, "weight": 9}]
    alloc = allocate_periods(items, 10)
    assert sum(a.periods for a in alloc) == 10
    assert alloc[0].periods >= 4                          # minimum seated first


def test_ss_reads_chapter_weight_real_data():
    ms = _mappings("social_sciences")
    assert len(ms) == 12
    alloc = allocate_for_subject("social_sciences", ms, 50)
    assert sum(a.periods for a in alloc) == 50
    # the heaviest chapter (weight 9) must get at least as many periods as the lightest (4)
    hi = max(alloc, key=lambda a: a.weight)
    lo = min(alloc, key=lambda a: a.weight)
    assert hi.weight == 9 and lo.weight == 4 and hi.periods >= lo.periods


def test_science_reads_effort_index_real_data():
    ms = _mappings("science")
    alloc = allocate_for_subject("science", ms, 60)
    assert sum(a.periods for a in alloc) == 60
    hi = max(alloc, key=lambda a: a.weight)
    lo = min(alloc, key=lambda a: a.weight)
    # effort_index range 4..11 -> if it wrongly read chapter_weight (absent->0), all equal
    assert hi.weight == 11.0 and lo.weight == 4.0 and hi.periods > lo.periods


if __name__ == "__main__":
    test_algorithm_basic_proportional_and_exact_total()
    test_algorithm_respects_minimums()
    test_ss_reads_chapter_weight_real_data()
    test_science_reads_effort_index_real_data()
    print("OK — Allocate: proportional + minimums + exact total; SS reads chapter_weight and "
          "Science reads effort_index, verified on real 12-chapter mappings.")
