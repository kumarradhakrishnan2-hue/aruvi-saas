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

A subject·stage that has not yet been brought through this seam raises
`CarrierNotImplemented` rather than returning something plausible and wrong. When a stage
arrives (S7–S11), implement `genon_assessment` on the plugin — DELEGATING to this module's
family helper for that stage's row in the 8-rule table, never writing a fresh join — and
remove the entry from `_NOT_YET`.

**`mathematics` landed 2026-08-08 (S4): secondary only, via row 6.** Middle and preparatory
belong to the period-field family and are still owed, which is why `_NOT_YET` is now keyed by
subject·STAGE rather than by subject — see the table below.

**`mathematics·middle` landed 2026-08-10 (S7): the PERIOD-FIELD family's first stage, row 4.**
It wrote `items_by_period_field` — the third family, named in the list above since 2026-08-05
and never implemented — plus three shape adapters the family drags in with it, none of which
invents a field (founder ruling 2026-08-10: nothing new may be added to a constitution to feed
the serve engine; everything is derived from what the authored file already carries, exactly as
the prototype absorbed the same variance at its read boundary):

  • the unit ANCHOR is mediated through the plugin (`genon_unit_anchor`), because maths·middle
    has a section axis under another field name — `textbook_segments[].ref`, joined verbatim
    with `_ANCHOR_JOINER`, never reformatted, so it matches the registry drawn from the
    summary's `sections[].ref` by construction;
  • the coverage HANDOFF is a dict of three goal clusters, so `to_engine_handoff` grew a
    second carrier marker (`_MATHS_GOAL_CLUSTER`) beside science's — without it the dict fell
    through unchanged, serve read `c["los"]` as empty, filtered nothing, and a served plan
    carried handoff rows for units it did not contain;
  • the item CONTAINER is a list of A/B/C groups, so `raw_item_list` / `item_container` /
    `from_engine_items` learned the group-nested shape. That is the SAME class of bug as
    science's `questions` wrapper (ARV-D-060) and it was live: `raw_item_list` returned `raw`
    whenever it was a list, so STEP 6 and `generate_canonical.validate` were iterating GROUP
    dicts, not items.

**Check it BEFORE you spend.** `carrier_gap()` / `require_carrier()` are the free pre-flight
(testing.md P5.5). The build's own failure lands at certification, which runs after the metered
steps, so relying on it costs a whole library and misreports itself as "does not compile" on
every file.
"""
from __future__ import annotations

import json
from typing import Any, Dict, List

from .. import subjects as _subjects
from ..link_resolver import norm_code, period_field_index
from ..normalize import group_label_from_unit
from .serve import _ANCHOR_JOINER          # " / " — the V2 multi-section join


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

# Families still to be implemented, keyed by (subject, STAGE) with the campaign stage that
# owes each one and its row in the verified 8-rule table (docs/architecture-plan.md
# §"Link resolution").
#
# KEYED BY SUBJECT·STAGE SINCE 2026-08-08 (S4). It used to be keyed by subject alone, which
# made it a trap: mathematics spans TWO carrier families — handoff-bridged at secondary
# (row 6) and period-field at middle/preparatory (rows 4 and 5) — so opening secondary by
# deleting one entry would silently have declared middle and preparatory ready too, and the
# next stage's items would have joined through a rule that is not theirs. A stage-granular
# table cannot do that, and it stays an honest inventory of what is still owed.
#
# `("mathematics", "middle")` was REMOVED 2026-08-10 (S7) — row 4 is implemented
# (`items_by_period_field` + the plugin's middle branch). Preparatory stays: it is row 5, a
# different period field (`section_refs[]`) on a different item vocabulary (`intent`, not
# `goal`), and it is owed by S8. Its unit ANCHOR is already mediated, which is deliberate and
# not the same thing as its carrier being ready.
_NOT_YET = {
    ("mathematics", "preparatory"): (
        "period-field join, item section_ref → period section_refs[] "
        "(8-rule row 5) — owed by S8"),
    ("english", "preparatory"): (
        "period-field join on (source_section_id + source_spine) → (section_id + "
        "spines_taught[]) (8-rule row 7) — owed by S9"),
    ("english", "middle"): (
        "period-field join on (source_section_id + source_spine) (8-rule row 7) "
        "— owed by S10"),
    ("english", "secondary"): (
        "period-field join on (source_section_id + source_spine) (8-rule row 7) "
        "— owed by S11"),
}


def carrier_gap(subject: Any, grade: Any) -> str | None:
    """The reason this subject·stage has no genon carrier yet, or None if it has one.

    THE pre-flight check behind testing.md's P5.5. Read it BEFORE spending money: the
    build's own failure arrives at certification, which is after the metered steps, so
    a missing carrier otherwise costs a full library (₹110–150) and reports itself as
    "does not compile" on every file rather than naming the subject.

    With an unknown or absent grade the answer is conservative — if ANY stage of the
    subject is still owed, treat it as owed. Guessing "ready" is the expensive mistake.
    """
    key = subject_key(subject)
    if not key:
        return None
    try:
        from ..grades import stage_for
        stage = stage_for(grade) if grade else None
    except Exception:                                       # noqa: BLE001
        stage = None
    if stage:
        return _NOT_YET.get((key, stage))
    owed = [v for (s, _st), v in _NOT_YET.items() if s == key]
    if owed:
        return (f"grade not given, and {key} still owes at least one stage: "
                + " · ".join(owed))
    return None


def require_carrier(subject: Any, grade: Any) -> None:
    """Raise `CarrierNotImplemented` unless this subject·stage has a genon carrier.

    Call it at the TOP of any metered pipeline (see `genon/build_library.py`), so the
    gate is free instead of paid."""
    gap = carrier_gap(subject, grade)
    if gap:
        raise CarrierNotImplemented(
            f"genon has no carrier for {subject_key(subject)!r}·{grade}: {gap}. "
            "Implement genon_assessment on the plugin (delegating to this module's "
            "family helper for that subject·stage's row in the 8-rule table) and remove "
            "the entry from _NOT_YET before running genon on it."
        )


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


# The group key travels on the COPIES `assessment_items()` makes, never on the live raw
# items, and `from_engine_items` strips it. Underscore-prefixed so a served file that somehow
# kept one is obviously engine residue rather than authored content.
_GROUP_KEY = "_genon_group"


def item_groups(raw: Any) -> List[Dict[str, Any]] | None:
    """The A/B/C section GROUPS a subject nests its items inside, or None.

    Shape-based, never subject-based — the same contract as `raw_item_list` below: a LIST
    whose EVERY element is a dict carrying its own `items` list is a group container, not a
    list of items. mathematics·middle is the case that made this necessary (2026-08-10, S7):
    its `assessment_items` is `[{section_code, section_title, note, items:[…]}, …]`, so every
    reader that assumed "a list is a list of items" was iterating GROUP dicts — the same class
    of bug as science's `questions` wrapper (ARV-D-060), on a different subject.

    Requiring EVERY element to qualify is what keeps it safe for the bare-list families: one
    Social Sciences item that happened to carry an `items` key could not turn its whole list
    into a group container.
    """
    if not isinstance(raw, list) or not raw:
        return None
    for g in raw:
        if not isinstance(g, dict) or not isinstance(g.get("items"), list):
            return None
    return raw


def raw_item_list(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """The LIVE item objects holding this chapter's assessment — NOT copies.

    For tools that mutate items in place and write the file back
    (`normalize_options` STEP 6, the repair scripts) and for anything that only
    needs to COUNT or scan them (`build_library`'s competency inventory,
    `generate_canonical.validate`). Those callers must not use
    `assessment_items()` above, whose copies would discard their edits.

    This is a CONTAINER lookup and is deliberately shape-based, not subject-based:
    the only variation is whether the subject wrapped its list under a key, or nested it
    inside GROUPS. The subject-specific part — how an item finds its unit — stays in the
    plugin.

    MUTATION CONTRACT (matters for the group-nested shape, 2026-08-10). The returned LIST is
    new — a flattening of the groups' own `items[]` — but its ELEMENTS are the live item
    dicts. So mutating a FIELD on an item (which is all STEP 6 does: it reorders `options`
    and re-flags `is_correct`) reaches the saved structure and is written back. APPENDING to
    or REMOVING from the returned list does NOT propagate, because no group owns it; a caller
    that needs to add or drop items must go through `item_container` / `from_engine_items`.
    The bare-list families return their own live list and have always had both.
    """
    raw = result.get("assessment_items")
    if isinstance(raw, dict):
        for k in ("questions", "assessment_items"):
            if isinstance(raw.get(k), list):
                return raw[k]
        return []
    groups = item_groups(raw)
    if groups is not None:
        return [it for g in groups for it in g["items"] if isinstance(it, dict)]
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

    THE GROUP-NESTED SHAPE (2026-08-10, S7 · mathematics·middle) is the second thing this
    has to put back. Its items live inside A/B/C section groups whose `section_code`,
    `section_title` and `note` are teacher-facing and are the assessment's own headings, so a
    served plan that came back as one flat list would lose the artefact's structure. The
    shells are captured here; `from_engine_items` re-buckets. Two routes back, in order:
    the `_GROUP_KEY` marker carried on the copies `assessment_items()` made, and — for callers
    that pass the LIVE raw items instead (api/main.py's export filter) — an item-id → group
    map built here, which is why it is stored rather than derived.
    """
    raw = result.get("assessment_items")
    if isinstance(raw, dict):
        for k in ("questions", "assessment_items"):
            if isinstance(raw.get(k), list):
                return {"_key": k,
                        "_shell": {kk: vv for kk, vv in raw.items() if kk != k}}
        return None
    groups = item_groups(raw)
    if groups is None:
        return None
    shells: List[Dict[str, Any]] = []
    by_item_id: Dict[str, str] = {}
    seen: set = set()
    for i, g in enumerate(groups):
        key = str(g.get("section_code") or "").strip() or str(i)
        if key in seen:                       # duplicated codes must not merge two groups
            key = f"{key}#{i}"
        seen.add(key)
        shells.append({"_gkey": key,
                       "_shell": {kk: vv for kk, vv in g.items() if kk != "items"}})
        for it in g["items"]:
            if isinstance(it, dict) and it.get("id") is not None:
                by_item_id.setdefault(str(it["id"]), key)
    return {"_groups": shells, "_by_item_id": by_item_id}


def from_engine_items(items: List[Dict[str, Any]],
                      container: Dict[str, Any] | None) -> Any:
    """The inverse of `item_container` — put the served list back inside the subject's
    own wrapper. Identity for the bare-list families, so callers need not branch."""
    if not container:
        return items
    if container.get("_key"):
        out = dict(container.get("_shell") or {})
        out[container["_key"]] = items
        return out
    groups = container.get("_groups")
    if not groups:
        return items
    order = [g["_gkey"] for g in groups]
    buckets: Dict[str, List[Dict[str, Any]]] = {k: [] for k in order}
    by_item_id = container.get("_by_item_id") or {}
    for it in items:
        if not isinstance(it, dict):
            continue
        key = it.pop(_GROUP_KEY, None)        # stripped: never ship engine residue
        if key not in buckets:
            key = by_item_id.get(str(it.get("id")))
        if key not in buckets:
            # A borrowed item from a lender whose groups are coded differently, or an item
            # with neither marker nor id. It belongs in the artefact rather than nowhere, so
            # it rides in the first group — visible and countable, which a silent drop is not.
            key = order[0]
        buckets[key].append(it)
    # An EMPTY group is emitted, not omitted: the group codes are the assessment's own
    # A/B/C headings and a missing one reads as a defect in the plan rather than as a
    # section this shorter serve does not reach.
    return [dict(g["_shell"], items=buckets[g["_gkey"]]) for g in groups]


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


# ── family 3 · period-field join (mathematics middle/prep, english) ──────────────
def _periods_of(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """The raw period dicts of a saved plan's `result`, wherever the caller nested them."""
    lp = result.get("lesson_plan")
    if isinstance(lp, dict) and isinstance(lp.get("periods"), list):
        return lp["periods"]
    return result.get("periods") if isinstance(result.get("periods"), list) else []


def period_section_codes(period: Dict[str, Any]) -> List[str]:
    """The section codes a PERIOD covers, under whichever name its constitution uses.

    Serialization tolerance in the spirit of `unit_approaches`, not a branch on subject:

        textbook_segments[].ref   mathematics·middle      ("section 5.2")
        section_refs[]            mathematics·preparatory ("S2")
        section_anchor            the declared-anchor stages (split on the V2 join)

    Read VERBATIM. The registry these codes are certified against is drawn from the chapter
    summary's own `sections[].ref`, and both sides are the same authored string — normalising
    here would only create a difference to reconcile later.
    """
    segs = period.get("textbook_segments")
    if isinstance(segs, list) and segs:
        return [str(s.get("ref") or "") for s in segs if isinstance(s, dict)]
    refs = period.get("section_refs")
    if isinstance(refs, list) and refs:
        return [str(x or "") for x in refs]
    anchor = str(period.get("section_anchor") or "").strip()
    return [a.strip() for a in anchor.split(_ANCHOR_JOINER) if a.strip()] if anchor else []


def items_by_period_field(result: Dict[str, Any], *, items, item_key: str,
                          extract) -> List[Dict[str, Any]]:
    """Join the item's own section/spine CODE against the PERIOD's own field.

    The third family, named in this module's docstring since 2026-08-05 and written at S7
    (2026-08-10) for the 8-rule table's row 4. Rows 4, 5 and 7 all live here: there is NO
    `coverage_handoff` anywhere in the path and NO learning outcome — the item names a
    section, the period names the sections it teaches, and the code itself is the join.

    `extract(period)` returns the codes that period covers; `item_key` is the field the item
    carries its code under ("section_ref"). Both sides pass through `link_resolver`'s
    `period_field_index` / `norm_code` — the SAME parity-tested mechanics the display side
    uses in `subjects/mathematics/subject.py::_middle_assess` — so "section 5.2", "Section
    5.2" and "5.2" converge. That is why this is a delegation and not a fresh join.

    Anchoring is the 2026-08-05 rule, identical to the other two families: a section taught
    across several periods anchors its items at the LAST of them, because an item tests the
    section's whole goal and becomes available only when the section completes. A section no
    period teaches yields `[]` — an orphan `compile.py` reports by name, never a guess.
    `period_ref` is honoured as a fallback for legacy files that carry one.
    """
    # THE SYNTHESIS UNIT IS NOT IN THE INDEX (2026-08-10, S7 · found on ch 7's served plan).
    # It teaches no section — it draws the whole chapter together — and on a MEDIATED-anchor
    # stage it says so by listing every section it revisits: ch 7's unit 12 carries all five
    # of `section 7.1`..`section 7.5` in `textbook_segments`. Indexed, that makes 12 the LAST
    # unit of every section, and since an item anchors at its section's last unit, all twelve
    # items collapsed onto the synthesis unit and units 1-11 showed no assessment at all.
    #
    # The token stages never saw this because their synthesis unit's `section_anchor` is the
    # literal reserved word, which matches no section and so never enters the index. Same
    # omission, same reason, as `serve.section_registry` and `serve.unit_range` — this is the
    # third site, and `is_synthesis` is the seam all three now go through.
    index = period_field_index(
        [p for p in _periods_of(result) if not is_synthesis(p)], extract)
    out = []
    for it in items or []:
        if not isinstance(it, dict):
            continue
        it2 = _copy(it)
        units = index.get(norm_code(it2.get(item_key)))
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
_MATHS_GOAL_CLUSTER = "maths_goal_cluster"


def _goal_clusters(ho: Any):
    """The GOAL-CLUSTER handoff — a dict of clusters each carrying `goals[]` — or None.

    mathematics·middle's native shape (2026-08-10, S7):

        {"section_a": {"goal_cluster": ["recall"],
                       "goals": [{section_ref, section_title, goal, anchor_id,
                                  anchor_book_ref, anchor_description}, …]},
         "section_b": …, "section_c": …}

    Shape-based: SS/TWAU blocks carry `los`, never `goals`, so they cannot be mistaken for
    one, and EVERY value must qualify before this claims the shape.
    """
    if not isinstance(ho, dict) or not ho:
        return None
    for v in ho.values():
        if not (isinstance(v, dict) and isinstance(v.get("goals"), list)):
            return None
    return list(ho.items())


def _goal_clusters_to_engine(result: Dict[str, Any], clusters) -> Dict[str, Any]:
    """One engine block per goal ENTRY — not per cluster — with its own `los`.

    WHY PER ENTRY. serve filters `los` and keeps the block; the surviving unit of filtering
    therefore has to be the thing that can independently survive or not, and that is a single
    goal row (one section × one goal cluster), not the whole cluster. Emitting one block per
    CLUSTER would make all three clusters all-or-nothing, so a served plan covering two of six
    sections would still carry every authored goal row.

    THE `los` SEMANTICS, stated once because they are the same ones science's section rows
    already have: an entry's period set is THE PERIODS THAT TEACH ITS SECTION, read off the
    period-field index — the identical index the items join through, so a row and the items
    testing it can never disagree about which sittings they belong to. The entry survives
    filtering iff AT LEAST ONE of those periods is served. It is not an anchor: nothing joins
    on it, it is what tells serve whether this row is still true of the plan it is building.

    Keyed on `cluster|section_ref` — the cluster names are fixed by the constitution and the
    section ref is the verbatim registry anchor, so the key is stable ACROSS a chapter's
    canonicals, which is the property serve's borrowed-row merge depends on (the same reason
    the science branch keys on the section LABEL and not on `section_number`).

    A cluster authored with an EMPTY `goals[]` gets a placeholder block carrying no entry, so
    the cluster's existence survives the round trip even when it contributes no row — LP Rule
    11 and assessment Rule 1 both require all three clusters to be present.
    """
    index = period_field_index(_periods_of(result), period_section_codes)
    out: Dict[str, Any] = {}
    for ci, (ckey, cluster) in enumerate(clusters):
        goals = [g for g in (cluster.get("goals") or []) if isinstance(g, dict)]
        common = {"_carrier": _MATHS_GOAL_CLUSTER, "_cluster": ckey,
                  "_cluster_order": ci, "_goal_cluster": cluster.get("goal_cluster")}
        if not goals:
            out[f"{ckey}|"] = dict(common, _entry=None, _order=0, los=[])
            continue
        for n, g in enumerate(goals):
            ref = str(g.get("section_ref") or "")
            key = f"{ckey}|{ref}" if ref else f"{ckey}|#{n}"
            if key in out:
                key = f"{key}#{n}"
            out[key] = dict(
                common, _entry=_copy(g), _order=n,
                los=[{"period_number": int(p)} for p in index.get(norm_code(ref), [])],
            )
    return out


def _goal_clusters_from_engine(handoff: Dict[str, Any]) -> Dict[str, Any]:
    """The inverse — engine blocks -> the three native clusters, after serve filtered.

    Clusters come back in their AUTHORED order (`_cluster_order`, which is `section_a` /
    `section_b` / `section_c` on a well-formed file) and each cluster's entries in their
    authored `_order`. An entry whose units are all gone is DROPPED — this plan does not
    teach its section, so claiming to cover it would be false. The CLUSTER is kept regardless,
    with an empty `goals[]`: the three clusters are structural (LP Rule 11 / assessment Rule
    1), the rows inside them are not.
    """
    clusters: Dict[str, Dict[str, Any]] = {}
    for blk in handoff.values():
        if not isinstance(blk, dict) or blk.get("_carrier") != _MATHS_GOAL_CLUSTER:
            continue
        ckey = str(blk.get("_cluster") or "")
        c = clusters.setdefault(ckey, {"order": blk.get("_cluster_order", 0),
                                       "goal_cluster": None, "rows": []})
        if c["goal_cluster"] is None and blk.get("_goal_cluster") is not None:
            c["goal_cluster"] = blk.get("_goal_cluster")
        entry = blk.get("_entry")
        if not isinstance(entry, dict) or not (blk.get("los") or []):
            continue
        c["rows"].append((blk.get("_order", 0), entry))
    out: Dict[str, Any] = {}
    for ckey in sorted(clusters, key=lambda k: (clusters[k]["order"], k)):
        c = clusters[ckey]
        c["rows"].sort(key=lambda t: t[0])
        blk: Dict[str, Any] = {}
        if c["goal_cluster"] is not None:
            blk["goal_cluster"] = c["goal_cluster"]
        blk["goals"] = [dict(e) for _, e in c["rows"]]
        out[ckey] = blk
    return out


def to_engine_handoff(result: Dict[str, Any]) -> Any:
    """Native handoff -> the one shape serve speaks. Identity for the block-shaped
    families (SS, TWAU); a lossless wrapping for the section-array families (science,
    maths·secondary) and for the goal-cluster family (maths·middle)."""
    ho = result.get("coverage_handoff")
    clusters = _goal_clusters(ho)
    if clusters is not None:
        return _goal_clusters_to_engine(result, clusters)
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
    if isinstance(handoff, dict) and any(
            isinstance(v, dict) and v.get("_carrier") == _MATHS_GOAL_CLUSTER
            for v in handoff.values()):
        return _goal_clusters_from_engine(handoff)
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
    """The same field under FIVE names, one per subject — exactly the diversity
    CLAUDE.md §3 refuses to flatten upstream ("the source keys are too diverse …
    Period.approach is the single normalization point"). This is that point for genon.
    Reading alternative KEY NAMES is serialization tolerance, not a branch on subject.

        pedagogical_approaches   list  social_sciences
        pedagogical_methods      dict  english   ({spine: method}; unique, first-seen)
        pedagogical_approach     str   science
        pedagogical_method       str   mathematics
        dominant_mode            str   the_world_around_us

    Corrected 2026-08-09 (ARV-D-086, S4·C6): the previous list read three names and its
    docstring claimed `pedagogical_approach` covered "Science, Maths". It does not —
    maths emits `pedagogical_method` and english `pedagogical_methods`, so this returned
    [] for maths, english and TWAU alike. Nothing downstream depended on the value, which
    is why it stayed invisible until a served plan was read at C6."""
    v = period.get("pedagogical_approaches")
    if isinstance(v, list) and v:
        return [str(x) for x in v if str(x).strip()]
    methods = period.get("pedagogical_methods")
    if isinstance(methods, dict) and methods:          # english: {spine: method}
        seen: List[str] = []
        for m in methods.values():
            m = str(m or "").strip()
            if m and m not in seen:
                seen.append(m)
        return seen
    if isinstance(methods, list) and methods:
        return [str(x) for x in methods if str(x).strip()]
    for k in ("pedagogical_approach", "pedagogical_method", "dominant_mode"):
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
    # A COMPOSITE unit is routed by nothing, so the by_unit map above cannot reach it
    # (2026-08-09, maths·IX ch 4). Its anchor joins several sections — "4.6 / 4.7 / 4.8" —
    # and no handoff row is keyed by that string, so its Overview row rendered blank on
    # exactly the units a teacher most needs orienting on.
    #
    # It is filled from the UNIT'S OWN TITLE, shortened — the same substitution the group
    # label makes (founder 2026-08-09: a composite anchor is never shown to a teacher; the
    # truncated unit title stands in for it everywhere).
    #
    # Two alternatives were measured and rejected. Joining the constituent sections'
    # CONTEXTS runs 302 characters for three sections and 390 for four, where
    # `section_context` is specified as a 10-12 word LABEL. Joining their TITLES is shorter
    # but still ~100-140 characters and introduces a second vocabulary for the same unit.
    # The unit's own title is already teacher-facing, already length-capped by the
    # constitution, and is what the teacher reads at the head of the group — so the row
    # agrees with its heading instead of competing with it. On an unrouted unit the field
    # has no assessment job left either (no item anchors there), so orienting is all it does.
    for u in units:
        if str(u.get("section_context") or "").strip():
            continue
        got = by_unit.get(u.get("unit"))
        if not got and _ANCHOR_JOINER in str(u.get("section_anchor") or ""):
            got = group_label_from_unit(u.get("activity_title")) or None
        u["section_context"] = got


def _plugin_for(subject: Any):
    """The registered plugin for a saved plan's `subject` string, or None."""
    key = subject_key(subject)
    if not key:
        return None
    _ensure_registered()
    try:
        return _subjects.get(key)
    except Exception:                                       # noqa: BLE001
        return None


def _ask(subject: Any, grade: Any, method: str, default):
    """Ask the plugin a genon question; fall back to the platform default.

    The default is what ten of the eleven stages want, so a plugin only implements
    these where it differs — and the engine never learns a subject's name."""
    fn = getattr(_plugin_for(subject), method, None)
    if not callable(fn):
        return default
    try:
        return fn(grade)
    except Exception:                                       # noqa: BLE001
        return default


def _ask_period(subject: Any, grade: Any, method: str, period: Dict[str, Any], default):
    """`_ask` for the questions that are about ONE PERIOD rather than the stage as a whole.

    Same contract and same reason: the plugin answers from its own constitution's field
    names, the engine never learns a subject's name, and a plugin that has nothing to say
    simply does not implement the method."""
    fn = getattr(_plugin_for(subject), method, None)
    if not callable(fn):
        return default
    try:
        return fn(period, grade)
    except Exception:                                       # noqa: BLE001
        return default


def serve_granularity(subject: Any, grade: Any) -> str:
    """"unit" (the atoms are units) | "plan" (the atoms are whole canonicals).

    See aruvi_core/subjects/base.py and docs/science_middle_stage_serve.md."""
    g = _ask(subject, grade, "genon_serve_granularity", "unit")
    return g if g in ("unit", "plan") else "unit"


def has_section_axis(subject: Any, grade: Any) -> bool:
    """Does this subject·stage anchor its units to textbook SECTIONS?

    True for ten stages. False for science·middle, whose units belong to a cognitive
    progression arc — there, a missing `section_anchor` is the design, not a defect,
    and compile.py must not treat its absence as a malformed plan."""
    return bool(_ask(subject, grade, "genon_has_section_axis",
                     serve_granularity(subject, grade) == "unit"))


def anchor_field_present(subject: Any, grade: Any) -> bool:
    """Does this subject·stage's constitution DEFINE a `section_anchor` field on the
    period object, or is the anchor mediated out of another field by `genon_unit_anchor`?

    True for ten stages (the platform default). False for mathematics·middle
    (`textbook_segments[].ref`) and mathematics·preparatory (`section_refs[]`).

    Declared by the plugin, never sniffed. "Does this plugin override
    `genon_unit_anchor`?" is the obvious inference and it is already wrong: mathematics
    mediates two of its three stages and keeps the field on the third, out of ONE plugin
    object, so a method-override check cannot tell them apart.

    The one caller that needs it is `variant_plans.top_brief_for`, which must decide WHICH
    of `is_synthesis`'s two carriers to ask a generation for. A brief that named
    `section_anchor` to a mediated stage would demand a field its constitution never
    defines, at metered STEP 1, and the certifier's synthesis gate would then find no
    synthesis unit. Distinct from `has_section_axis`: mathematics·middle HAS the axis and
    does not have the field."""
    return bool(_ask(subject, grade, "genon_anchor_field_present", True))


def forward_reference_legal(subject: Any, grade: Any) -> bool:
    """May a unit point at what comes next, or claim the chapter complete?

    False for ten stages: any unit of a canonical may be somebody's LAST sitting (the
    X-1+1 fill borrows single units across plans), so a forward reference is wrong for
    someone. That is ban 2 of THE SELF-CONTAINED REGISTER.

    True for a PLAN-granularity stage, and derived rather than declared so the two can
    never drift apart: the reason ban 2 exists is that units travel alone, and the reason
    plan granularity exists is that they cannot. Every unit of a science·middle canonical
    is served with every other unit of that canonical, so "in the next unit" is never
    wrong for anyone and a closing completion claim is simply true. Hence its constitution
    carries a TWO-ban register (LP v2.2, founder 2026-08-07) — and `genon/register_scan.py`
    must agree with the constitution it is enforcing, or it fails good plans.

    Bans 1 (clock quantity) and 3 (calendar time) are untouched by this and always apply:
    duration scaling and the Calendar Purge are orthogonal to the serve model."""
    return serve_granularity(subject, grade) == "plan"


def item_anchor_family(subject: Any, grade: Any) -> str:
    """"item" | "handoff" | "period_field" — the 8-rule table's family column, declared.

    See `aruvi_core/subjects/base.py`. Default "item" (item-self-sufficient), which is what
    social_sciences and the_world_around_us want and what nothing else relies on."""
    f = _ask(subject, grade, "genon_item_anchor_family", "item")
    return f if f in ("item", "handoff", "period_field") else "item"


def item_anchor_is_derived(subject: Any, grade: Any) -> bool:
    """Does an item reach its unit through a MEDIATING row rather than off the item itself?

    True for the handoff-bridged family. The consequence that matters at authoring time: a
    unit with no `coverage_handoff` row can carry no assessment item at all, so the standard
    canonical's mandated closing SYNTHESIS unit needs a row of its own or C9.2 ("a borrowed
    unit brings its own items") is unsatisfiable on precisely the Case-1 synthesis borrow.
    Measured on the installed science·ix ch 8 library (2026-08-08): the model invented a
    synthesis row unprompted and NO item used it — item `section_number`s stopped at 10 and
    no stamped `unit_ref` ever reached unit 12. `variant_plans.top_brief_for` asks for the
    row explicitly rather than hoping."""
    return item_anchor_family(subject, grade) == "handoff"


def group_fields(subject: Any, grade: Any) -> tuple:
    """The period fields that say WHICH GROUP a unit belongs to, for this subject·stage.

    Needed only when a unit is borrowed into a foreign plan at PLAN granularity. The
    borrowed unit's own grouping metadata describes a plan the teacher never sees, so
    carrying it verbatim invents a group: the top canonical's synthesis unit arrived in an
    8-unit variant still labelled `progression_stage: 6`, and the served plan grew a sixth
    stage that existed nowhere in the arc the class was taught (ARV-D-067).

    Declared by the plugin so the engine never learns a subject's name. Empty tuple by
    default — a subject that does not group by a period field needs no adoption, and
    section-axis stages never take this path anyway."""
    v = _ask(subject, grade, "genon_group_fields", ())
    return tuple(v or ())


def unit_anchor(period: Dict[str, Any], *, subject: Any, grade: Any) -> Any:
    """A period's `section_anchor`, mediated (2026-08-07, S6; the plugin hook 2026-08-10, S7).

    `compile.py` used to read `p["section_anchor"]` directly — a hard KeyError on any
    stage that does not have one, which would have killed science·middle's first build
    before a single certification check ran. On a section-axis stage a missing anchor is
    still an error (it means a malformed plan, and the serve engine's whole arithmetic
    runs on it); on a stage without the axis it is simply None.

    BETWEEN THOSE TWO SITS A THIRD CASE, and mathematics·middle is it: a stage that HAS a
    section axis but does not spell it `section_anchor` (its periods carry
    `textbook_segments[].ref`). Founder ruling 2026-08-10: no new field may be invented to
    feed the serve engine, so the constitution is NOT amended to add one — the read is
    mediated instead, through `genon_unit_anchor` on the plugin, which is where a subject's
    own field names belong. The precedent is the prototype, which absorbed exactly this
    variance at its read boundary (`lp_pdf_generator.py`'s textbook_segments-else-
    section_anchor branch). The plugin returns the anchor VERBATIM; the certifier compares it
    against a registry drawn from the chapter summary's own `sections[].ref`, and the two are
    the same authored string, so they match by construction.
    """
    if "section_anchor" in period:
        return period["section_anchor"]
    mediated = _ask_period(subject, grade, "genon_unit_anchor", period, None)
    if mediated:
        return mediated
    if is_synthesis(period):
        # THE MEDIATED SYNTHESIS UNIT (2026-08-10, S7). A whole-chapter synthesis is not a
        # textbook section, so on a mediated-anchor stage it has nothing to mediate FROM —
        # maths·middle's closer carries no `textbook_segments[]`, because it teaches no
        # segment. Without this branch the raise below fired on it and the standard
        # canonical did not compile at all, which is the loudest possible version of "the
        # certifier finds no synthesis unit".
        #
        # None, not the reserved token: the boolean already carries the fact (that is what
        # `is_synthesis` just read), and manufacturing an anchor string would write a value
        # into a field this stage's constitution does not define — the same invention the
        # founder ruling of 2026-08-10 forbids, arriving through the back door. Downstream
        # the two are equivalent by construction: `section_registry` and `unit_range` skip
        # a synthesis unit through this same seam, so an empty anchor and the token behave
        # identically in the section arithmetic.
        return None
    if has_section_axis(subject, grade):
        raise KeyError(
            "period %s has no section_anchor, and %s·%s anchors units to sections"
            % (period.get("period_number"), subject, grade))
    return None


def is_synthesis(period: Dict[str, Any]) -> bool:
    """Does this period carry the chapter's closing whole-chapter synthesis?

    Two carriers for one fact. Section-axis stages put the reserved token in
    `section_anchor` (architecture §0.3). A stage with no section axis has nowhere to
    put it, so its brief mandates an explicit boolean instead. Read here so neither
    compile.py nor serve.py has to know which kind of stage it is looking at."""
    if period.get("synthesis") is True:
        return True
    a = " ".join(str(period.get("section_anchor") or "").split()).casefold()
    return a == "synthesis"


# ── the seam itself ──────────────────────────────────────────────────────────────
def assessment_items(plan: Dict[str, Any], result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """The chapter's assessment as a FLAT list of item dicts, each stamped `unit_ref`.

    Resolution order: the subject plugin's own `genon_assessment` if it has one;
    otherwise the family default. An unrecognised subject falls back to
    `items_by_period_ref` so nothing that worked before regresses.
    """
    key = subject_key(plan.get("subject") or result.get("subject"))
    require_carrier(plan.get("subject") or result.get("subject"),
                    plan.get("grade") or result.get("grade"))
    if key:
        _ensure_registered()
        try:
            plugin = _subjects.get(key)
        except Exception:                                   # noqa: BLE001
            plugin = None
        fn = getattr(plugin, "genon_assessment", None) if plugin else None
        if callable(fn):
            return _stamp_group_keys(result, fn(result))
    return _stamp_group_keys(result, items_by_period_ref(result))


def _stamp_group_keys(result: Dict[str, Any],
                      items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remember which A/B/C group each COPY came out of, for `from_engine_items`.

    Shape-based and subject-agnostic, so it sits here beside `item_container` rather than in
    any plugin: a group-nested container is flattened on the way in, and without a mark the
    only way back would be to re-derive the grouping — which is the guessing this module
    exists to remove. The mark rides on the copies alone (the live raw items are never
    touched) and `from_engine_items` pops it, so it can never reach a served file.

    Alignment is positional against `raw_item_list`, which flattens the same groups in the
    same order. If the plugin returned a different number of items the stamp is SKIPPED
    rather than applied to the wrong item — `from_engine_items` still has the item-id map.
    """
    groups = item_groups(result.get("assessment_items"))
    if not groups or not isinstance(items, list):
        return items
    keys, seen = [], set()
    for i, g in enumerate(groups):
        key = str(g.get("section_code") or "").strip() or str(i)
        if key in seen:
            key = f"{key}#{i}"
        seen.add(key)
        keys.extend(key for it in g["items"] if isinstance(it, dict))
    if len(keys) != len(items):
        return items
    for it, key in zip(items, keys):
        if isinstance(it, dict):
            it[_GROUP_KEY] = key
    return items
