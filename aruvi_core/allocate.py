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
    sub = subjects.get(subject_name)
    items: List[Dict[str, Any]] = []
    for m in mappings:
        items.append({
            "chapter_number": m.get("chapter_number"),
            "chapter_title": m.get("chapter_title", ""),
            "weight": sub.chapter_weight(m),
            "min_periods": _min_periods(m),
        })
    return allocate_periods(items, total_periods)


def _min_periods(mapping: Dict[str, Any]) -> Optional[int]:
    v = mapping.get("min_viable_periods")
    return int(v) if v else None
