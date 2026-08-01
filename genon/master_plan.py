#!/usr/bin/env python3
"""Genon step-2 master plan: annual budgets -> per-chapter allocation + drop floors.

Source: data/content/allocation_norms/ncf_chapterwise_period_allocation.xlsx
(budget sheet = founder's realistic annual budgets; Chapters sheet = effort weights).
Standard durations (HANDOVER Decision 2): 40 min for classes <= VII, 45 for VIII, 50 for IX.
Floor: unit-dropping begins when teacher_minutes / canonical_minutes < 0.6
(compression doctrine); floor_minutes = 0.6 x canonical_minutes.
"""
import json
import math

import openpyxl

from pathlib import Path
REPO = Path(__file__).resolve().parent.parent          # aruvi-saas/
NORMS = REPO / "data" / "content" / "allocation_norms"
WB = str(NORMS / "ncf_chapterwise_period_allocation.xlsx")
DROP_THRESHOLD = 0.6

# budget-sheet subject label -> repo subject key; Chapters-sheet label -> same key
SUBJECT_KEY = {
    "English": "english",
    "Mathematics": "mathematics",
    "Science": "science",
    "Social Sciences": "social_sciences",
    "TWAU": "the_world_around_us",
    "The World Around Us": "the_world_around_us",
}
ROMAN = {"III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10}


def std_duration(cls_roman):
    n = ROMAN[cls_roman]
    if n <= 7:
        return 40
    if n == 8:
        return 45
    return 50


def largest_remainder(budget, weights):
    total_w = sum(weights)
    exact = [budget * w / total_w for w in weights]
    base = [int(x) for x in exact]
    rem = budget - sum(base)
    order = sorted(range(len(exact)), key=lambda i: exact[i] - base[i], reverse=True)
    for i in order[:rem]:
        base[i] += 1
    assert sum(base) == budget
    return base, exact


wb = openpyxl.load_workbook(WB, data_only=True)

budgets = {}  # (subject_key, class_roman) -> annual periods
for r in wb["budget"].iter_rows(min_row=2, values_only=True):
    if r[0] is None:
        continue
    key = (SUBJECT_KEY[r[0]], r[1])
    assert key not in budgets, f"duplicate budget row {key}"
    budgets[key] = r[2]

chapters = {}  # (subject_key, class_roman) -> [(ch, title, weight)]
for r in wb["Chapters"].iter_rows(min_row=2, values_only=True):
    if r[0] is None:
        continue
    chapters.setdefault((SUBJECT_KEY[r[0]], r[1]), []).append((r[2], r[3], r[4]))

plan = {}
skipped = []
for key in sorted(chapters, key=lambda k: (k[0], ROMAN[k[1]])):
    subject, cls = key
    budget = budgets.get(key)
    if budget is None:
        skipped.append((subject, cls, "no annual budget in budget sheet"))
        continue
    chs = sorted(chapters[key])
    alloc, exact = largest_remainder(budget, [c[2] for c in chs])
    dur = std_duration(cls)
    rows = []
    for (ch, title, w), periods, ex in zip(chs, alloc, exact):
        canonical_min = periods * dur
        floor_min = DROP_THRESHOLD * canonical_min
        rows.append({
            "chapter": ch,
            "title": title,
            "weight": w,
            "exact_share": round(ex, 2),
            "recommended_periods": periods,
            "canonical_minutes": canonical_min,
            "floor_minutes": round(floor_min, 1),
            "floor_periods_at_standard": round(floor_min / dur),  # nearest, not ceil (founder, 2026-07-31)
            "placeholder": "Placeholder" in str(title),
        })
    plan[f"{subject}|{cls}"] = {
        "subject": subject,
        "class": cls,
        "standard_duration_minutes": dur,
        "annual_budget_periods": budget,
        "total_effort_weight": sum(c[2] for c in chs),
        "n_chapters": len(chs),
        "chapters": rows,
    }

# budgets with no chapter data (e.g. class X)
for key, budget in sorted(budgets.items(), key=lambda kv: (kv[0][0], ROMAN[kv[0][1]])):
    if budget is not None and key not in chapters:
        skipped.append((key[0], key[1], f"budget {budget} but no chapters in workbook"))

out = {
    "_meta": {
        "generated": "2026-07-24",
        "source_workbook": "data/content/allocation_norms/ncf_chapterwise_period_allocation.xlsx",
        "standard_durations": {"<=VII": 40, "VIII": 45, "IX": 50},
        "allocation_method": "largest remainder over chapter effort weights (same as Allocate.jsx / api allocator)",
        "floor_definition": f"unit-dropping begins when teacher_minutes/canonical_minutes < {DROP_THRESHOLD}; "
                            f"floor_minutes = {DROP_THRESHOLD} x recommended_periods x standard_duration; "
                            "floor_periods_at_standard rounded to the NEAREST whole period (founder, 2026-07-31)",
        "skipped": [f"{s} {c}: {why}" for s, c, why in skipped],
    },
    "combos": plan,
}
with open(NORMS / "master_plan.json", "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

# ---- no derived md: master_plan.json is the single artifact (2026-07-31) ----
# The human-readable master_plan.md was RETIRED after it served a stale floor
# to the founder (ceil vs round, corrected the same day): a derived view that
# can drift from its source will eventually lie. To eyeball the plan, read the
# JSON fresh (python3 -m json.tool) or GET /subjects/{s}/{g}/chapters, which
# carries recommended_periods, floors, and variant_plan per chapter.

print("combos planned:", len(plan), "| skipped:", len(skipped))
for s, c, why in skipped:
    print("  skipped:", s, c, "-", why)
tot = sum(p["annual_budget_periods"] for p in plan.values())
print("total annual periods across portfolio:", tot)
ss9 = plan["social_sciences|IX"]["chapters"][4]
print("spot check SS IX ch5:", ss9)
