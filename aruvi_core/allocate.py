"""
Allocate — distribute a teacher's period budget across a subject's chapters.

Subject-agnostic. Each chapter contributes a single allocation *weight* (Social Sciences uses
its competency-sum `chapter_weight`; the effort-index subjects use `effort_index`) — which
number to read is the subject's call (Subject.chapter_weight), so there is no `if subject`
here. This module just does the proportional maths, respecting any per-chapter minimum
(e.g. Science's `min_viable_periods`) and hitting the requested total exactly.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from . import subjects


@dataclass
class ChapterAllocation:
    chapter_number: Any
    chapter_title: str
    weight: float
    min_periods: int
    periods: int


def allocate_periods(items: List[Dict[str, Any]], total_periods: int) -> List[ChapterAllocation]:
    """items: dicts with chapter_number, chapter_title, weight, optional min_periods.

    Strategy: seat each chapter's minimum first, then distribute the remaining periods in
    proportion to weight using largest-remainder rounding so the totals add up exactly.
    """
    n = len(items)
    if n == 0:
        return []
    mins = [int(it.get("min_periods") or 0) for it in items]
    weights = [max(0.0, float(it.get("weight") or 0)) for it in items]
    base = sum(mins)
    extra = max(0, total_periods - base)

    tw = sum(weights)
    if tw <= 0:                                   # no weights -> even split of the extra
        shares = [extra // n] * n
        for i in range(extra % n):
            shares[i] += 1
    else:
        raw = [extra * w / tw for w in weights]
        floors = [int(math.floor(r)) for r in raw]
        remainder = extra - sum(floors)
        order = sorted(range(n), key=lambda i: raw[i] - floors[i], reverse=True)
        for i in order[:remainder]:
            floors[i] += 1
        shares = floors

    out: List[ChapterAllocation] = []
    for i, it in enumerate(items):
        out.append(ChapterAllocation(
            chapter_number=it.get("chapter_number"),
            chapter_title=it.get("chapter_title", ""),
            weight=weights[i],
            min_periods=mins[i],
            periods=mins[i] + shares[i],
        ))
    return out


def allocate_for_subject(subject_name: str, mappings: List[Dict[str, Any]],
                         total_periods: int) -> List[ChapterAllocation]:
    """Read each chapter's allocation weight via the subject plugin, then allocate."""
    return allocate_periods(_subject_items(subject_name, mappings), total_periods)


def _subject_items(subject_name: str, mappings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    sub = subjects.get(subject_name)
    return [{
        "chapter_number": m.get("chapter_number"),
        "chapter_title": m.get("chapter_title", ""),
        "weight": sub.chapter_weight(m),
        "min_periods": _min_periods(m),
    } for m in mappings]


def allocate_schedule(items: List[Dict[str, Any]],
                      period_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Allocate a multi-row period schedule across chapters.

    period_rows: [{minutes, count}], e.g. [{minutes:45, count:150}, {minutes:60, count:50}].
    Each duration pool is allocated independently across chapters by weight (largest-
    remainder, so each column sums exactly). Per-chapter totals are the row sums. The
    largest pool carries any per-chapter minimum (e.g. Science min_viable_periods).
    """
    pool: Dict[int, int] = {}
    order: List[int] = []
    for r in period_rows or []:
        m, c = int(r.get("minutes") or 0), int(r.get("count") or 0)
        if m <= 0 or c <= 0:
            continue
        if m not in pool:
            order.append(m)
        pool[m] = pool.get(m, 0) + c

    largest_m = max(pool, key=lambda m: pool[m]) if pool else None
    by_m: Dict[int, Dict[Any, int]] = {}
    for m in order:
        items_m = [{**it, "min_periods": (it.get("min_periods") if m == largest_m else None)} for it in items]
        by_m[m] = {a.chapter_number: a.periods for a in allocate_periods(items_m, pool[m])}

    allocations = []
    for it in items:
        cn = it.get("chapter_number")
        per = {m: by_m[m].get(cn, 0) for m in order}
        allocations.append({
            "chapter_number": cn,
            "chapter_title": it.get("chapter_title", ""),
            "weight": max(0.0, float(it.get("weight") or 0)),
            "periods_by_duration": {str(m): per[m] for m in order},
            "total_periods": sum(per.values()),
            "total_minutes": sum(m * per[m] for m in order),
        })
    return {
        "durations": order,
        "allocations": allocations,
        "totals": {
            "periods": sum(pool.values()),
            "minutes": sum(m * c for m, c in pool.items()),
            "by_duration": {str(m): pool[m] for m in order},
        },
    }


def allocate_schedule_for_subject(subject_name: str, mappings: List[Dict[str, Any]],
                                  period_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    return allocate_schedule(_subject_items(subject_name, mappings), period_rows)


def _min_periods(mapping: Dict[str, Any]) -> Optional[int]:
    v = mapping.get("min_viable_periods")
    return int(v) if v else None
