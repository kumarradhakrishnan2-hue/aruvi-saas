"""The calibrated standard is what the product defaults to (founder, 2026-07-26).

Two period tables live under data/cloud/content/allocation_norms/ and they disagree:

  ncf_period_norms.json  — the NCF adaptation. Annual totals by subject·STAGE, counted in a
                           flat 40-minute period (its own _meta.unit says so).
  master_plan.json       — OUR calibrated standard. Annual budgets by subject·CLASS from the
                           founder's workbook, spread per chapter by effort weight, at the
                           class-banded standard duration (40 ≤VII / 45 VIII / 50 IX).

First run used to seed a flat 12 periods × 40 min for every chapter of every class, so the
default a teacher saw contradicted the certified canonical she was about to generate — on
Social Sciences IX ch 5 that is 480 minutes against the canonical's 1050 (21×50). These tests
pin the rule that fixed it: master plan first, NCF norms only as fallback.

Stdlib only. Run directly:  python3 tests/test_calibrated_defaults.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import data  # noqa: E402


def eq(got, want, what):
    assert got == want, f"{what}: expected {want!r}, got {got!r}"


# ── 1. Class-banded standard durations, incl. the X extension ──────────────────
# genon/master_plan.py's std_duration bands: ≤VII → 40, VIII → 45, IX → 50. Class X has no
# master-plan row (no chapter weights in the workbook yet) but sits in the same secondary
# band, so the DURATION extends to it; its period counts still fall back to the NCF norms.
for grade, want in [("iii", 40), ("v", 40), ("vii", 40), ("viii", 45), ("ix", 50), ("x", 50)]:
    eq(data.standard_duration_minutes(grade), want, f"standard duration for class {grade.upper()}")

# An unknown grade must not explode — it lands on the flat NCF period.
eq(data.standard_duration_minutes("zz"), data.FALLBACK_STANDARD_DURATION, "unknown grade duration")

# Where the master plan HAS a row, the file itself is authoritative over the band table, so a
# band could be moved in the workbook without touching code.
eq(data.standard_duration_minutes("ix", "social_sciences"), 50, "SS IX duration from combo")
eq(data.standard_duration_minutes("viii", "mathematics"), 45, "Maths VIII duration from combo")

# ── 2. The per-chapter recommendation matches the certified canonical ──────────
# SS IX ch 5 is the first live canonical (21×50 under LP v1.2.1). The default the teacher is
# shown before generating it must be that same 21 periods, at that same 50-minute class.
ss9 = data.master_recommended_periods("social_sciences", "ix")
eq(ss9.get(5), 21, "SS IX ch 5 recommended periods")
eq(ss9.get(5) * data.standard_duration_minutes("ix", "social_sciences"), 1050,
   "SS IX ch 5 recommended minutes vs the canonical's 1050")

# Every chapter of a covered combo carries a positive whole-period figure.
assert ss9 and all(isinstance(p, int) and p > 0 for p in ss9.values()), \
    "every master-plan chapter needs a positive integer recommendation"

# The per-chapter figures sum to exactly the calibrated annual budget (largest remainder —
# no rounding drift), so the year plan's fallback total is the budget, not an approximation.
eq(sum(ss9.values()), data.master_annual_budget("social_sciences", "ix"),
   "SS IX per-chapter recommendations must sum to the annual budget")

# ── 3. Fallback: no master-plan row → empty, and the caller drops to the NCF norms ──
# Science has no preparatory chapters in the workbook (and the NCF table has no figure for
# science·preparatory either), so both tables come back empty and the UI's flat constant wins.
eq(data.master_recommended_periods("science", "v"), {}, "science V has no master-plan row")
eq(data.master_annual_budget("science", "v"), None, "science V has no calibrated budget")
eq(data.ncf_total_periods("science", "preparatory"), None, "science preparatory has no NCF norm")

# Class X: no calibrated row, but the NCF norm covers the secondary stage, so the API's
# fallback path has something real to distribute.
eq(data.master_annual_budget("science", "x"), None, "class X has no calibrated budget yet")
assert data.ncf_total_periods("science", "secondary"), "science secondary NCF norm must exist"

# ── 4. The two tables really do disagree — this is the whole reason for the change ──
# If these ever converge the test is telling you the fix is moot, not that it broke.
assert data.master_annual_budget("social_sciences", "ix") != \
    data.ncf_total_periods("social_sciences", "secondary"), \
    "SS IX: calibrated budget and NCF norm are expected to differ (245 vs 150)"

print("ALL CALIBRATED-DEFAULT TESTS PASSED")
