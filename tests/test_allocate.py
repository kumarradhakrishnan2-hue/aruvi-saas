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
from aruvi_core.allocate import (  # noqa: E402
    allocate_for_subject, allocate_periods, allocate_schedule_for_subject,
)

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


def test_multi_row_schedule_real_data():
    # Science: 150 periods of 45 min + 50 of 60 min, allocated across 12 chapters.
    res = allocate_schedule_for_subject("science", _mappings("science"),
                                        [{"minutes": 45, "count": 150}, {"minutes": 60, "count": 50}])
    assert res["durations"] == [45, 60]
    a = res["allocations"]
    # each duration column sums EXACTLY to its pool (remainder method)
    assert sum(x["periods_by_duration"]["45"] for x in a) == 150
    assert sum(x["periods_by_duration"]["60"] for x in a) == 50
    # per-chapter total is the row sum; grand total is 200
    assert all(x["total_periods"] == x["periods_by_duration"]["45"] + x["periods_by_duration"]["60"] for x in a)
    assert res["totals"]["periods"] == 200 and res["totals"]["minutes"] == 150 * 45 + 50 * 60
    # heavier chapter gets more total periods
    hi = max(a, key=lambda x: x["weight"]); lo = min(a, key=lambda x: x["weight"])
    assert hi["total_periods"] > lo["total_periods"]


if __name__ == "__main__":
    test_algorithm_basic_proportional_and_exact_total()
    test_algorithm_respects_minimums()
    test_ss_reads_chapter_weight_real_data()
    test_science_reads_effort_index_real_data()
    test_multi_row_schedule_real_data()
    print("OK — Allocate: proportional + minimums + exact total; per-subject weight field; "
          "and multi-row schedule (per-duration columns sum exactly, totals correct).")
