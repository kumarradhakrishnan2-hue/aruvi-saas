"""Reverse deduction of variant spacing — covering condition, mandate, weighting.

Stdlib only; run directly: python3 tests/test_variant_solver.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aruvi_core.genon.variant_solver import (  # noqa: E402
    _even_ranges, outcome_for, solve,
)

# a 12-unit top canonical, one section per unit
TOP = [(i, i) for i in range(12)]

# ── the modelled compact variant is a contiguous partition ───────────────────
r = _even_ranges(12, 7, 4)
assert r[-1] == (8, 11) and r[0][0] == 0
flat = [i for lo, hi in r for i in range(lo, hi + 1)]
assert flat == list(range(12)), "contiguous, complete, in order"

# ── outcomes: exact variant hits and above-top are full ──────────────────────
cr = {12: TOP, 9: _even_ranges(12, 9, 2), 7: _even_ranges(12, 7, 4)}
for x in (7, 9, 12, 14):
    assert outcome_for(x, cr, 12) == "full"
# 11 against 12: missing lo = 10; 9-variant closer starts at 10 -> exact fill
assert outcome_for(11, cr, 12) == "full"
# 10 against 12: missing lo = 9; 7-variant closer starts at 8 -> superset
assert outcome_for(10, cr, 12) == "full"
# 8 against 9 with only a one-section top closer available -> partial at best
cr2 = {12: TOP, 9: _even_ranges(12, 9, 2)}
assert outcome_for(8, cr2, 12) in ("partial", "full")

# ── solve: three variants over floor 7 achieve full coverage on 7..12 ───────
sol = solve(TOP, floor=7, sigma=4)
assert sol["counts"][0] == 12 and sol["counts"][2] == 7, "C sits at the floor"
assert all(v == "full" for v in sol["table"].values()), sol["table"]
assert all(s <= 4 for s in sol["closing_spans"].values()), "mandate respected"

# ── sigma too small: coverage degrades, and the table says so honestly ──────
sol2 = solve(TOP, floor=7, sigma=1)
assert any(v != "full" for v in sol2["table"].values()), \
    "a 1-section closing span cannot cover multi-unit gaps"

# ── demand weighting can move B ──────────────────────────────────────────────
w_hi = {x: (5.0 if x >= 10 else 0.1) for x in range(7, 13)}
sol3 = solve(TOP, floor=7, sigma=2, weights=w_hi)
assert sol3["counts"][1] >= sol2["counts"][1] - 2  # sanity: solver still returns
assert sol3["table"][11] == "full", "the demanded region is served first"

print("test_variant_solver: all assertions passed")
