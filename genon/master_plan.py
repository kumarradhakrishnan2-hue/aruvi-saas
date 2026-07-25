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
            "floor_periods_at_standard": math.ceil(floor_min / dur),
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
                            f"floor_minutes = {DROP_THRESHOLD} x recommended_periods x standard_duration",
        "skipped": [f"{s} {c}: {why}" for s, c, why in skipped],
    },
    "combos": plan,
}
with open(NORMS / "master_plan.json", "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

# ---- human-readable md ----
L = []
L.append("# GENON MASTER PLAN — step 2 (2026-07-24)")
L.append("")
L.append("Realistic annual budgets (founder's workbook, NOT the NCF norms) spread per chapter")
L.append("by effort weight (largest remainder — the same allocator the app uses). Canonical")
L.append("plans are authored at the class-standard duration: **40 min ≤ VII · 45 min VIII ·")
L.append("50 min IX** (HANDOVER Decision 2). Floor = the point where the three-regime")
L.append(f"compression doctrine starts dropping trailing units (ratio < {DROP_THRESHOLD}):")
L.append(f"floor_minutes = {DROP_THRESHOLD} × periods × duration; 'floor P' below is that floor")
L.append("expressed in standard-duration periods (rounded up).")
L.append("")
L.append("Source: `data/content/allocation_norms/ncf_chapterwise_period_allocation.xlsx`")
L.append("(budget + Chapters sheets, cleaned 2026-07-24). Regenerate with `genon/master_plan.py` (writes here, to allocation_norms).")
L.append("")
if skipped:
    L.append("**Not planned:** " + "; ".join(f"{s} {c} ({why})" for s, c, why in skipped) + ".")
    L.append("")
L.append("## Portfolio summary")
L.append("")
L.append("| Subject | Class | Std dur | Annual periods | Chapters | Canonical hours |")
L.append("|---|---|---|---|---|---|")
for key, p in plan.items():
    hours = sum(r["canonical_minutes"] for r in p["chapters"]) / 60
    L.append(f"| {p['subject']} | {p['class']} | {p['standard_duration_minutes']} | "
             f"{p['annual_budget_periods']} | {p['n_chapters']} | {hours:.0f} |")
L.append("")
for key, p in plan.items():
    L.append(f"## {p['subject']} · {p['class']} — {p['annual_budget_periods']} periods/yr "
             f"× {p['standard_duration_minutes']} min")
    L.append("")
    L.append("| Ch | Title | Wt | Periods | Canon min | Floor min | Floor P |")
    L.append("|---|---|---|---|---|---|---|")
    for r in p["chapters"]:
        t = r["title"] if len(str(r["title"])) <= 48 else str(r["title"])[:45] + "..."
        flag = " ⚠" if r["placeholder"] else ""
        L.append(f"| {r['chapter']} | {t}{flag} | {r['weight']} | {r['recommended_periods']} | "
                 f"{r['canonical_minutes']} | {r['floor_minutes']:.0f} | {r['floor_periods_at_standard']} |")
    L.append("")
    if any(r["placeholder"] for r in p["chapters"]):
        L.append("⚠ placeholder chapters (awaiting NCERT release) hold flat weights — this")
        L.append("combo's numbers will shift when the real chapters land; do not author")
        L.append("canonicals for ⚠ rows.")
        L.append("")
with open(NORMS / "master_plan.md", "w") as f:
    f.write("\n".join(L))

print("combos planned:", len(plan), "| skipped:", len(skipped))
for s, c, why in skipped:
    print("  skipped:", s, c, "-", why)
tot = sum(p["annual_budget_periods"] for p in plan.values())
print("total annual periods across portfolio:", tot)
ss9 = plan["social_sciences|IX"]["chapters"][4]
print("spot check SS IX ch5:", ss9)
