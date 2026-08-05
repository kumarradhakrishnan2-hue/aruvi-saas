"""The genon carrier seam — the plugin layer genon was missing.

WHY THIS EXISTS (2026-08-05, found at S3 · science · secondary stage prep).
`compile.py` read a saved plan's `result["assessment_items"]` directly and assumed
it was a flat list of item dicts, each carrying `period_ref`. That is true of Social
Sciences and TWAU and of nothing else. Science secondary wraps its items in an object
(`{grade, subject, …, "questions": [...]}`), so iterating it yielded the wrapper's KEY
NAMES as bare strings: the canonical compiled clean with zero questions, and
`normalize_options` then died on `'str' object has no attribute 'get'`. Every chapter
genon had ever processed was Social Sciences, so the assumption was invisible.

The app never had this bug, because the app goes through the subject plugin
(`aruvi_core/subjects/*/subject.py`), which knows each subject's shape. Genon skipped
that layer — in direct breach of CLAUDE.md §3 ("subjects are plugins, not conditionals;
the engine never branches on subject"). This module is that layer for genon.

THE THREE CARRIER FAMILIES are not new: they are `link_resolver`'s verified 8-rule
table, which the display side has used all along.

  • item-self-sufficient  — social_sciences, the_world_around_us: `period_ref[]` is
                            read straight off the item.
  • handoff-bridged       — science (both stages), mathematics secondary: the item
                            carries an integer section/stage number; join it through
                            `coverage_handoff` to that group's `period_numbers`.
  • period-field join     — mathematics middle/preparatory, english: match the item's
                            section/spine code against the period's own field.

ANCHORING RULE (founder, 2026-08-05). Where a group maps to SEVERAL units, the item
anchors to the LAST of them. An item tests its section's whole `implied_lo`, so it
becomes available only when the section COMPLETES: if the class was not taught all of
it, it cannot be tasked on any of it. The alternative — full-set membership — would
hand a class a question most of whose material it never saw, which is worse than an
absent question. `unit_ref` is therefore a singleton, matching `link_resolver`'s
`anchor_period`.

A subject that has not yet been brought through this seam raises
`CarrierNotImplemented` rather than returning something plausible and wrong. Genon has
never run on mathematics or english; when their stages arrive (S4, S7–S11), implement
`genon_assessment` on the plugin and delete the entry from `_NOT_YET`.
"""
from __future__ import annotations

import json
from typing import Any, Dict, List

from .. import subjects as _subjects


def _ensure_registered() -> None:
    """Importing a subject package registers its plugin. The API does this at startup;
    genon runs standalone from Terminal, so do it here too (idempotent)."""
    if _subjects.available():
        return
    for mod in ("science", "social_sciences", "mathematics", "english",
                "the_world_around_us"):
        try:
            __import__(f"aruvi_core.subjects.{mod}")
        except Exception:                                   # noqa: BLE001
            pass


class CarrierNotImplemented(NotImplementedError):
    """This subject has not been brought through the genon carrier seam yet."""


# Saved plans carry DISPLAY names ("Social Science", "The World Around Us"); the
# registry is keyed by slug. One place, so nobody re-derives it.
_DISPLAY_TO_KEY = {
    "science": "science",
    "social science": "social_sciences",
    "social sciences": "social_sciences",
    "mathematics": "mathematics",
    "maths": "mathematics",
    "english": "english",
    "the world around us": "the_world_around_us",
}

# Families still to be implemented, with the stage that owes each one.
_NOT_YET = {
    "mathematics": "period-field join (middle/prep) + handoff-bridged (secondary) — owed by S4/S7/S8",
    "english": "period-field join on spines/section_refs — owed by S9/S10/S11",
}


def subject_key(name: Any) -> str | None:
    """Registry key for a saved plan's `subject` string, or None if unrecognisable."""
    t = " ".join(str(name or "").split()).lower()
    if not t:
        return None
    if t in _DISPLAY_TO_KEY:
        return _DISPLAY_TO_KEY[t]
    _ensure_registered()
    slug = t.replace(" ", "_")
    return slug if slug in _subjects.available() else None


def _copy(it: Dict[str, Any]) -> Dict[str, Any]:
    return json.loads(json.dumps(it))


def _last(units) -> List[int]:
    """The anchoring rule: a group's LAST unit, as a length-one list. Empty when the
    group reaches no unit — the caller reports that as an unanchored item."""
    live = sorted({int(u) for u in (units or []) if u is not None})
    return [live[-1]] if live else []


def raw_item_list(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """The LIVE list object holding this chapter's items — NOT copies.

    For tools that mutate items in place and write the file back
    (`normalize_options` STEP 6, the repair scripts) and for anything that only
    needs to COUNT or scan them (`build_library`'s competency inventory,
    `generate_canonical.validate`). Those callers must not use
    `assessment_items()` above, whose copies would discard their edits.

    This is a CONTAINER lookup and is deliberately shape-based, not subject-based:
    the only variation is whether the subject wrapped its list under a key. The
    subject-specific part — how an item finds its unit — stays in the plugin.
    """
    raw = result.get("assessment_items")
    if isinstance(raw, dict):
        for k in ("questions", "assessment_items"):
            if isinstance(raw.get(k), list):
                return raw[k]
        return []
    return raw if isinstance(raw, list) else []


# ── family 1 · item-self-sufficient (social_sciences, the_world_around_us) ────────
def items_by_period_ref(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """`period_ref` is an identity: the item names its own unit. Tolerates a dict
    container for older files that wrapped the list under its own key."""
    raw = result.get("assessment_items") or []
    if isinstance(raw, dict):
        raw = raw.get("assessment_items") or raw.get("questions") or []
    out = []
    for it in raw:
        if not isinstance(it, dict):
            continue
        it2 = _copy(it)
        it2["unit_ref"] = _last(u for u in (it2.get("period_ref") or [])
                                if isinstance(u, int))
        out.append(it2)
    return out


# ── family 2 · handoff-bridged (science both stages, mathematics secondary) ───────
def items_by_handoff(result: Dict[str, Any], *, items, join_key: str,
                     handoff_key: str) -> List[Dict[str, Any]]:
    """Join the item's integer group number through `coverage_handoff` to that
    group's `period_numbers`, then anchor at the last of them.

    NEVER matches `section_anchor` text — `link_resolver` records why (labels are
    merged strings that differ between canonicals, and two sections can share one).
    Falls back to `period_ref` only for legacy files that happen to carry it.
    """
    index: Dict[int, List[int]] = {}
    for h in (result.get("coverage_handoff") or []):
        if not isinstance(h, dict) or h.get(handoff_key) is None:
            continue
        index[int(h[handoff_key])] = [int(p) for p in (h.get("period_numbers") or [])
                                      if p is not None]
    out = []
    for it in items or []:
        if not isinstance(it, dict):
            continue
        it2 = _copy(it)
        gnum = it2.get(join_key)
        units = index.get(int(gnum)) if isinstance(gnum, int) else None
        if not units:
            units = [u for u in (it2.get("period_ref") or []) if isinstance(u, int)]
        it2["unit_ref"] = _last(units)
        out.append(it2)
    return out


# ── the seam itself ──────────────────────────────────────────────────────────────
def assessment_items(plan: Dict[str, Any], result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """The chapter's assessment as a FLAT list of item dicts, each stamped `unit_ref`.

    Resolution order: the subject plugin's own `genon_assessment` if it has one;
    otherwise the family default. An unrecognised subject falls back to
    `items_by_period_ref` so nothing that worked before regresses.
    """
    key = subject_key(plan.get("subject") or result.get("subject"))
    if key in _NOT_YET:
        raise CarrierNotImplemented(
            f"genon has no carrier for subject {key!r}: {_NOT_YET[key]}. "
            "Implement genon_assessment on the plugin before running genon on it."
        )
    if key:
        _ensure_registered()
        try:
            plugin = _subjects.get(key)
        except Exception:                                   # noqa: BLE001
            plugin = None
        fn = getattr(plugin, "genon_assessment", None) if plugin else None
        if callable(fn):
            return fn(result)
    return items_by_period_ref(result)
