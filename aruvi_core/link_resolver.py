"""
Assessment → period link resolution (the architecture-plan.md §"Link resolution — verified
8-rule table"). Each subject normalizer runs its rule ONCE at normalize-time and stamps a
UNIFORM contract onto every assessment item so the renderer/engine stay subject-agnostic:

    item.meta["linked_periods"] : sorted list[int]   # the period set the item belongs to
    item.meta["anchor_period"]  : int | None          # closing period of that set (display anchor)
    item.meta["linked_lo"]      : str | None          # the LO the item tests, where one exists

These are the ONLY fields the UI (LessonView Screen 3b) reads to scope an item to the learning
unit (period) the teacher is on. The per-subject *how* lives in each plugin's normalizer; this
module only holds the small shared mechanics they call, so the join logic isn't duplicated.

Three carrier families (the only real variation), per the plan:
  • item-self-sufficient  — SS, TWAU: period_ref[] + implied_lo read straight off the item.
  • handoff-bridged       — Science (both), Maths-secondary: join the integer stage/section
                            number through coverage_handoff → period_numbers. NEVER match
                            section_anchor text (messy/granular; orphans items).
  • period-field join     — Maths middle/prep, English: match the item's section/spine code to
                            the period's own field (textbook_segments / section_refs / spines).

Resolvers must accept many-items→one-group and one-group→many-periods (A/B/C and intent tiers
re-test a section), so the stored value is always the FULL period set with the closing period
flagged as anchor — never "latest only" (lossy).
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional


# ── the uniform stamp every resolver writes ─────────────────────────────────────
def stamp(meta: Dict[str, Any], periods: Iterable[int], lo: Optional[str] = None) -> Dict[str, Any]:
    """Write the uniform link contract into an item's meta dict and return it.

    `periods` is the resolved period set (any iterable of ints, deduped+sorted here).
    `anchor_period` is the closing (max) period of the set — the display anchor. Empty set →
    linked_periods=[] and anchor_period=None (an orphan; parity tests assert this never happens
    on real data, but the UI degrades gracefully if it ever does)."""
    ps = sorted({int(p) for p in periods if p is not None})
    meta["linked_periods"] = ps
    meta["anchor_period"] = ps[-1] if ps else None
    meta["linked_lo"] = (lo or None)
    return meta


# ── handoff-bridged family: stage/section number → period_numbers ───────────────
def handoff_period_index(handoff: Any, key: str) -> Dict[int, List[int]]:
    """Build {stage_or_section_number: [period_numbers]} from a coverage_handoff list.

    `key` is the handoff's join field — "stage_number" (Science middle) or "section_number"
    (Science secondary, Maths secondary). We deliberately read `period_numbers` and NEVER
    `section_anchor` (per the plan's hard-won correction — anchor text orphans items)."""
    index: Dict[int, List[int]] = {}
    for h in (handoff or []):
        if not isinstance(h, dict):
            continue
        n = h.get(key)
        if n is None:
            continue
        pns = h.get("period_numbers") or []
        index[int(n)] = [int(p) for p in pns if p is not None]
    return index


# ── period-field join family: build a code → [period_numbers] index ─────────────
def period_field_index(periods: Iterable[Dict[str, Any]], extract) -> Dict[str, List[int]]:
    """Index periods by a normalized code the item also carries. `extract(period)` returns an
    iterable of codes that period covers (e.g. its textbook_segments refs, section_refs, or
    (section_id, spine) pairs flattened to strings). Returns {code: [period_numbers]}."""
    index: Dict[str, List[int]] = {}
    for p in periods or []:
        pn = p.get("period_number")
        if pn is None:
            continue
        for code in extract(p) or []:
            index.setdefault(_norm(code), []).append(int(pn))
    return index


def period_number_by_field(periods: Iterable[Dict[str, Any]], field: str) -> Dict[int, List[int]]:
    """Fallback for handoff-bridged subjects when coverage_handoff is absent (older saved plans):
    build {field_value: [period_numbers]} straight from the lesson-plan periods, where each
    period carries the same integer join field the item does (e.g. periods also carry
    `progression_stage`). Same join semantics as the handoff — just sourced from the periods."""
    index: Dict[int, List[int]] = {}
    for p in periods or []:
        v = p.get(field)
        pn = p.get("period_number")
        if v is None or pn is None:
            continue
        index.setdefault(int(v), []).append(int(pn))
    return index


def _norm(s: Any) -> str:
    """Normalize a section/segment code for tolerant matching: lowercase, collapse the word
    'section', strip spaces/punctuation. So "section 2.1", "Section 2.1", "2.1", "S2.1" all
    converge as far as the data allows."""
    t = str(s or "").strip().lower()
    t = t.replace("section", " ").replace("sec.", " ").strip()
    t = t.replace(" ", "")
    return t


def norm_code(s: Any) -> str:
    """Public alias of the normalizer for resolvers that build the item-side key."""
    return _norm(s)
