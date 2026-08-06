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


def item_container(result: Dict[str, Any]) -> Dict[str, Any] | None:
    """The subject's own WRAPPER around its item list, or None if it stores a bare list.

    The mirror of `raw_item_list` above, and the reason it exists (ARV-D-060,
    2026-08-06): unwrapping was one-way. Science·secondary stores its assessment as
    {grade, subject, stage, chapter_number, chapter_title, chapter_cg,
    reasoning_floor_lift_applied, questions: [...]}, and its port decides the plan is
    secondary by seeing that wrapper. `compile` unwrapped to the bare list serve speaks
    and nothing put the wrapper back, so every SERVED science plan arrived at the screen
    looking like a middle-stage plan — the port then joined on `progression_stage`, which
    secondary items do not carry, matched nothing, and LessonView's "if nothing is
    anchored, show everything" fallback printed EVERY question under EVERY sitting.
    SS and TWAU store a bare list, which is why two certified stages never saw it.

    Same contract as to_engine_handoff/from_engine_handoff, and deliberately the same
    shape of solution: a CONTAINER lookup, shape-based not subject-based. The
    subject-specific part — how an item finds its unit — stays in the plugin.
    """
    raw = result.get("assessment_items")
    if isinstance(raw, dict):
        for k in ("questions", "assessment_items"):
            if isinstance(raw.get(k), list):
                return {"_key": k,
                        "_shell": {kk: vv for kk, vv in raw.items() if kk != k}}
    return None


def from_engine_items(items: List[Dict[str, Any]],
                      container: Dict[str, Any] | None) -> Any:
    """The inverse of `item_container` — put the served list back inside the subject's
    own wrapper. Identity for the bare-list families, so callers need not branch."""
    if not container or not container.get("_key"):
        return items
    out = dict(container.get("_shell") or {})
    out[container["_key"]] = items
    return out


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


def item_anchor_label(item: Dict[str, Any], n: int = 0) -> str:
    """A short human label for an item's anchor, for REPORTS only — never a join.

    `period_ref[0]` reads "U7" for the item-self-sufficient family; the
    handoff-bridged family carries no `period_ref` at all (science secondary's
    constitution forbids it), so it reads "S3" from `section_number` or "PS2" from
    `progression_stage`. Reporting code that assumed `period_ref[0]` crashed STEP 6
    with `'NoneType' object is not subscriptable` on the first science library.
    """
    pr = [u for u in (item.get("period_ref") or []) if u is not None]
    if pr:
        return f"U{pr[0]}"
    for key, prefix in (("section_number", "S"), ("progression_stage", "PS"),
                        ("stage_number", "PS")):
        v = item.get(key)
        if v is not None:
            return f"{prefix}{v}"
    return f"#{n}" if n else "?"


# ── the coverage handoff · round trip ────────────────────────────────────────────
# serve.py remaps the handoff in ONE shape: {key: {..., "los": [{period_number, …}]}}.
# That is Social Sciences' competency-keyed block, and `serve` does `handoff.values()`
# and reads `c["los"]` — an AttributeError the moment it meets science's ARRAY of
# section entries. Rather than teach `serve` two shapes (a subject conditional inside
# the engine, the very thing this module exists to remove), the handoff is normalized
# IN and restored OUT: the engine sees one shape, and a served plan keeps its own
# subject's native shape, so the app's display path is untouched.
#
# The marker travels in the data (`_carrier`), so restoring needs no side-channel.

_SCIENCE_SECTION = "science_section"


def to_engine_handoff(result: Dict[str, Any]) -> Any:
    """Native handoff -> the one shape serve speaks. Identity for the block-shaped
    families (SS, TWAU); a lossless wrapping for the section-array families."""
    ho = result.get("coverage_handoff")
    if not isinstance(ho, list):
        return ho if ho is not None else {}
    out: Dict[str, Any] = {}
    for n, h in enumerate(ho):
        if not isinstance(h, dict):
            continue
        entry = {k: v for k, v in h.items() if k != "period_numbers"}
        # Key on the section LABEL — the verbatim registry anchor, which V2 makes stable
        # ACROSS canonicals of a chapter. `section_number` is per-plan and two canonicals
        # that cut differently can number the same section differently, so keying on it
        # would merge a lender's rows onto the wrong section.
        key = str(h.get("section_label") or h.get("stage_label")
                  or h.get("section_number") or h.get("stage_number") or f"_{n}")
        out[key] = {
            "_carrier": _SCIENCE_SECTION,
            "_entry": entry,
            "_order": n,
            "los": [{"period_number": int(p)} for p in (h.get("period_numbers") or [])
                    if p is not None],
        }
    return out


def from_engine_handoff(handoff: Any) -> Any:
    """The inverse — engine shape -> the subject's native shape, after serve has
    filtered and renumbered the rows. Entries whose units are all gone are DROPPED:
    science's contract is one entry per section THIS plan anchors, so a section the
    plan does not teach has no entry (unlike SS, which keeps the block with empty
    `los`). `total_sections` is recomputed to what this plan actually carries; the
    stale authored count would misdescribe a served plan."""
    if not isinstance(handoff, dict) or not any(
            isinstance(v, dict) and v.get("_carrier") == _SCIENCE_SECTION
            for v in handoff.values()):
        return handoff
    rows = []
    for blk in handoff.values():
        if not isinstance(blk, dict) or blk.get("_carrier") != _SCIENCE_SECTION:
            continue
        los = blk.get("los") or []
        if not los:
            continue
        entry = dict(blk.get("_entry") or {})
        entry["period_numbers"] = sorted({int(lo["period_number"]) for lo in los
                                          if lo.get("period_number") is not None})
        if los and all(lo.get("unscheduled") for lo in los):
            entry["unscheduled"] = True
        rows.append((blk.get("_order", 0), entry))
    rows.sort(key=lambda t: t[0])
    out = [e for _, e in rows]
    for e in out:
        e["total_sections"] = len(out)
    return out


# ── unit projection · the fields whose spelling differs by constitution ───────────
def unit_approaches(period: Dict[str, Any]) -> List[str]:
    """`pedagogical_approaches` (SS, English) vs `pedagogical_approach` (Science,
    Maths) vs `dominant_mode` (TWAU) — the same field under three names, exactly the
    diversity CLAUDE.md §3 already refuses to flatten upstream ("the source keys are
    too diverse … Period.approach is the single normalization point"). This is that
    point for genon. Reading alternative KEY NAMES is serialization tolerance, not a
    branch on subject."""
    v = period.get("pedagogical_approaches")
    if isinstance(v, list) and v:
        return [str(x) for x in v if str(x).strip()]
    for k in ("pedagogical_approach", "dominant_mode"):
        s = str(period.get(k) or "").strip()
        if s:
            return [s]
    return []


def backfill_unit_context(units: List[Dict[str, Any]], result: Dict[str, Any]) -> None:
    """Fill a unit's `section_context` from the handoff when the period does not carry
    it. Science secondary's LP Rule 6 prohibition 2 FORBIDS section_context inside a
    period object — it lives only in the handoff — so reading it off the period leaves
    the served Overview blank. Shape-based and subject-agnostic: any handoff entry that
    names its `period_numbers` and a `section_context` is used. Mutates in place."""
    ho = result.get("coverage_handoff")
    if not isinstance(ho, list):
        return
    by_unit: Dict[int, str] = {}
    for h in ho:
        if not isinstance(h, dict):
            continue
        ctx = str(h.get("section_context") or "").strip()
        if not ctx:
            continue
        for p in (h.get("period_numbers") or []):
            if p is not None:
                by_unit.setdefault(int(p), ctx)
    for u in units:
        if not str(u.get("section_context") or "").strip():
            u["section_context"] = by_unit.get(u.get("unit"))


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
