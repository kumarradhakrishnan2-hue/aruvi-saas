"""Aruvi variant-serve engine — v2.0 / engine e12 (2026-08-03). Replaces the partition engine.

Doctrine (docs/variant_canonical_architecture.md §0): a chapter is authored as a small
LIBRARY of canonicals — the same section list planned FREE at counts spaced by equal
dispersion over [floor, standard]; the standard alone closes with a mandated
whole-chapter synthesis unit anchored to the reserved token `synthesis`. Serving a
teacher's request is SELECTION, never composition:

  * the NEXT-HIGHEST canonical is chosen (full richness; surrender only above the top);
  * the first X-1 sittings are that canonical's units 1..X-1, verbatim;
  * slot X is SELECTED by the Xth-unit CHOICE SET (§0.4, replaces the v1 fill ladder):
      Case 1 — prefix covers every section: borrow the standard's `synthesis` unit
        (full coverage is the only prior a whole-chapter synthesis needs);
      Case 2 — sections remain (M = first uncovered): borrow, from ANY canonical, the
        unit that FIRST deals M in its own plan — a first-exposure unit's only backward
        dependency is "the sections before mine were taught", which the prefix
        guarantees (ARV-D-025: mandated closing syntheses imported foreign priors and
        produced the jumpy Xth unit; first-exposure selection is the structural fix).
        Preference: forward reach without re-cross (M+N…, furthest first) > M alone >
        backward combinations (L+M…, redundancy is not jumpiness). Sections still
        uncovered after the fill ride as dropped units SOURCED FROM THE LENDER's
        subsequent units;
      Case 3 — empty choice set (defensive; structurally impossible on a well-formed
        library): truncate, no dropped sections, message asking for the reference
        canonical's count;
  * within a unit, time expands/contracts in proportion to the sitting's duration
    (the only arithmetic left — bounded, per-unit, against an authored arc).

There is NO DP, no cut cost, no compression regime, no role weighting, no seam or
handoff text: a sitting's title and notes are its unit's own authored title and notes.
The old engine's failure modes (pivot-notes as the plan's entire voice, hooks stranded
at sitting ends, uniform percentage cuts with no pedagogical basis) are structurally
impossible here, not merely discouraged.

Kept from partition v0.5: order_durations (the weekly dispersion of a mixed matrix —
still the least-wrong sequence under ignorance of her timetable), integerise, BAND_MIN.
Everything a teacher sees was authored by the generation pass; every number is either
an authored number or a declared proportional scaling of one.
"""
from __future__ import annotations

import json


class ServeError(RuntimeError):
    """The serve failed validation — never serve an invalid plan."""


BAND_MIN = 3


def parse_matrix(spec):
    rows = []
    for part in spec.split("+"):
        c, d = part.lower().split("x")
        rows.append((int(d), int(c)))
    return rows


# ── duration ordering: the week, not the row (kept verbatim from partition v0.4) ──
#
# A duration matrix is a BAG, not a sequence. The teacher's timetable is a weekly
# pattern that repeats; within a week the longer durations are placed at maximum
# dispersion — shortest opens the week, longer durations interior, never adjacent,
# short runs between them as equal as the arithmetic allows.


def _spread(n, k):
    """Split n items into k+1 gaps as evenly as possible, remainder to the middle."""
    gaps = [n // (k + 1)] * (k + 1)
    rem = n - sum(gaps)
    middle_out = sorted(range(k + 1), key=lambda i: (abs(i - k / 2.0), i))
    for i in middle_out[:rem]:
        gaps[i] += 1
    return gaps


def _disperse(base, extra):
    if not extra:
        return list(base)
    if not base:
        return list(extra)
    if len(base) < len(extra):
        base, extra = extra, base
    gaps = _spread(len(base), len(extra))
    out, idx = [], 0
    for i, g in enumerate(gaps[:-1]):
        out.extend(base[idx:idx + g])
        idx += g
        out.append(extra[i])
    out.extend(base[idx:])
    return out


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def order_durations(matrix):
    """Duration matrix -> the ordered sitting sequence (weekly cycle, dispersed)."""
    agg = {}
    for d, c in matrix:
        d, c = int(d), int(c)
        if d > 0 and c > 0:
            agg[d] = agg.get(d, 0) + c
    if not agg:
        return []
    durs = sorted(agg)
    if len(durs) == 1:
        return [durs[0]] * agg[durs[0]]
    weeks = 0
    for d in durs:
        weeks = _gcd(weeks, agg[d])
    cycle = []
    for d in durs:
        cycle = _disperse(cycle, [d] * (agg[d] // weeks))
    return cycle * weeks


def integerise(mins_float, dur):
    """Round band minutes to integers summing exactly to the sitting duration."""
    mins = [max(BAND_MIN, round(m)) for m in mins_float]
    diff = sum(mins) - dur
    order = sorted(range(len(mins)), key=lambda k: -mins[k])
    k = 0
    while diff != 0:
        j = order[k % len(mins)]
        if diff > 0 and mins[j] > BAND_MIN:
            mins[j] -= 1; diff -= 1
        elif diff < 0:
            mins[j] += 1; diff += 1
        k += 1
    return mins


# ── section arithmetic: the registry and unit ranges ─────────────────────────
#
# The chapter's ordered section list is the join key of the whole library
# (V2 in the brief): every variant's units are contiguous, section-aligned
# partitions of the SAME list, and section_anchor strings are drawn verbatim
# from it. Cross-variant matching is index arithmetic on that shared registry.

_ANCHOR_JOINER = " / "

# The reserved anchor of the standard canonical's mandated closing synthesis
# (§0.3). It is NOT a registry section: section_registry skips it, unit_range
# reports the unit as rangeless, and only Case 1 ever borrows such a unit.
SYNTH_TOKEN = "synthesis"


def _norm(s):
    return " ".join(str(s or "").split()).casefold()


def _unit_anchors(unit):
    return [a.strip() for a in str(unit.get("section_anchor") or "").split(_ANCHOR_JOINER)
            if a.strip()]


def is_synthesis_unit(unit):
    """True iff the unit carries the reserved `synthesis` anchor (standard
    canonical's mandated closer — §0.3; the token is exact and alone)."""
    return [_norm(a) for a in _unit_anchors(unit)] == [SYNTH_TOKEN]


def section_registry(stream):
    """Ordered unique section anchors across a stream's units (the reserved
    synthesis token is not a section and never enters the registry)."""
    out, seen = [], set()
    for u in stream["units"]:
        for a in _unit_anchors(u):
            k = _norm(a)
            if k != SYNTH_TOKEN and k not in seen:
                seen.add(k)
                out.append(a)
    return out


def unit_range(unit, registry_index):
    """Unit -> (lo, hi) inclusive indices into the registry. None if any anchor
    is unknown to the registry (the candidate then simply doesn't qualify)."""
    idxs = []
    for a in _unit_anchors(unit):
        k = _norm(a)
        if k not in registry_index:
            return None
        idxs.append(registry_index[k])
    if not idxs:
        return None
    return (min(idxs), max(idxs))


# ── variant selection + the slot-X fill ladder ───────────────────────────────


def choose_variant(streams, requested):
    """Streams (any order) + requested sitting count -> (chosen, surrendered).

    Full-richness rule: the NEXT-HIGHEST variant serves the request; surrender
    happens only above the top variant. Returns the chosen stream and how many
    requested sittings exceed it (0 unless requested > top count)."""
    ranked = sorted(streams, key=lambda s: -len(s["units"]))
    top = ranked[0]
    if requested >= len(top["units"]):
        return top, requested - len(top["units"])
    eligible = [s for s in ranked if len(s["units"]) >= requested]
    return eligible[-1], 0        # smallest count >= requested


def first_dealing_unit(stream, ridx, m):
    """The unit of `stream` that deals registry section m FOR THE FIRST TIME in
    its own plan (first-visit walk), with its index and range. A first-exposure
    unit's only backward dependency is "the sections before mine were taught" —
    the property the whole choice set rests on (§0.4). None when the stream
    never first-visits m (malformed coverage), or first-visits it in a unit with
    anchors outside the registry."""
    prev = -1
    for i, u in enumerate(stream["units"]):
        r = unit_range(u, ridx)
        if r is None:
            continue                      # synthesis token / foreign anchors
        if r[1] > prev:                   # this unit advances the frontier
            if prev < m <= r[1]:
                if r[0] <= m:
                    return i, u, r
                return None               # the stream SKIPS m — no first exposure
            prev = r[1]
    return None


def synthesis_unit_of(streams):
    """The library's mandated whole-chapter synthesis — the standard canonical's
    closing unit anchored to the reserved token (§0.3). Largest count first, so
    a well-formed library yields the standard's. None on legacy libraries."""
    for s in sorted(streams, key=lambda s: -len(s["units"])):
        if is_synthesis_unit(s["units"][-1]):
            return s, s["units"][-1]
    return None


def fill_slot(streams, chosen, requested, registry):
    """The Xth-unit choice set (§0.4, engine e12 — replaces the v1 fill ladder).

    FRONTIER ARITHMETIC (founder ruling, 2026-07-31): what the prefix has
    covered is measured by its first-visit frontier — the furthest registry
    section any prefix unit reaches — so backward-anchored revisit sittings
    never distort the missing span, which is always a registry suffix.

    Case 1 (frontier at the last section): borrow the standard's `synthesis`
    unit — full coverage is the only prior it needs, and the prefix guarantees
    it. Legacy libraries without the token fall back to the nearest-in-scale
    companion's closing unit (the v1 synthesis mode), else a synthesis-only
    truncation.

    Case 2 (M = first uncovered section): candidates are, per canonical in the
    library (the chosen plan included — its own unit X is the identity
    candidate), the unit that FIRST deals M in its own plan. Contiguity (V2)
    makes every co-dealt section adjacent to M. Preference (founder,
    2026-08-03): forward reach without re-cross (M+N…, furthest first) > M
    alone > backward combinations (least re-cross, then furthest reach) — a
    brisk re-cross is redundancy, and redundancy is not jumpiness. Ties: the
    lender whose count is closest to X (pacing context), then the denser plan.
    Sections beyond the fill's reach are reported; serve_plan carries them as
    dropped units SOURCED FROM THE LENDER's subsequent units.

    Case 3 (empty choice set — defensive, structurally impossible on a
    well-formed library): serve the chosen plan's own unit X, show NO dropped
    sections, and ask for the reference canonical's count (the next higher
    canonical — the depth this teacher's request implies)."""
    ridx = {_norm(a): i for i, a in enumerate(registry)}
    last = len(registry) - 1
    units = chosen["units"]
    ranges = []
    for u in units:
        r = unit_range(u, ridx)
        if r is None and not is_synthesis_unit(u):
            raise ServeError("SERVE INVALID: chosen variant has units outside "
                             "its own registry")
        ranges.append(r)
    frontier = max((r[1] for r in ranges[:requested - 1] if r), default=-1)
    m = frontier + 1

    if m > last:
        # ── Case 1: every section covered — the whole-chapter synthesis is the
        # one borrow that assumes nothing false, wherever the prefix came from.
        syn = synthesis_unit_of(streams)
        if syn:
            s, u = syn
            return {"mode": "synthesis", "stream": s, "unit": u,
                    "borrowed_from": len(s["units"]), "self_fill": s is chosen,
                    "overlap_sections": [], "uncovered_sections": [],
                    "withheld_units": [w["unit"] for w in units[requested - 1:]
                                       if w is not u]}
        others = [s for s in streams if s is not chosen]      # legacy fallback
        if others:
            c = min(others, key=lambda s: (abs(len(s["units"]) - requested),
                                           len(s["units"])))
            return {"mode": "synthesis", "stream": c, "unit": c["units"][-1],
                    "borrowed_from": len(c["units"]), "self_fill": False,
                    "overlap_sections": [], "uncovered_sections": [],
                    "withheld_units": [u["unit"] for u in units[requested - 1:]]}
        return {"mode": "truncation", "stream": chosen, "unit": units[requested - 1],
                "borrowed_from": None, "overlap_sections": [],
                "uncovered_sections": [], "synthesis_only": True,
                "withheld_units": [u["unit"] for u in units[requested:]]}

    # ── Case 2: the choice set — first-exposure units for M across the library.
    cands = []
    for s in streams:
        hit = first_dealing_unit(s, ridx, m)
        if hit is None:
            continue
        i, u, r = hit
        a, b = r
        o = m - a                          # already-taught sections re-crossed
        cands.append({"stream": s, "unit": u, "unit_index": i, "range": r,
                      "overlap": o, "reach": b,
                      "count": len(s["units"])})
    if cands:
        cands.sort(key=lambda c: (0 if c["overlap"] == 0 else 1,   # no re-cross first
                                  c["overlap"],                    # then least re-cross
                                  -c["reach"],                     # furthest reach
                                  abs(c["count"] - requested),     # pacing context
                                  -c["count"]))                    # then denser
        c = cands[0]
        a, b = c["range"]
        fill_class = ("forward" if c["overlap"] == 0 and b > m
                      else "single" if c["overlap"] == 0
                      else "backward")
        uncovered = list(registry[b + 1:])
        s = c["stream"]
        drop_units = []
        if uncovered:
            uncov_idx = set(range(b + 1, last + 1))
            for w in s["units"][c["unit_index"] + 1:]:
                r = unit_range(w, ridx)
                if r and set(range(r[0], r[1] + 1)) <= uncov_idx:
                    drop_units.append(w)
        return {"mode": "fill", "fill_class": fill_class,
                "first_section": registry[m],
                "stream": s, "unit": c["unit"],
                "borrowed_from": c["count"], "self_fill": s is chosen,
                "overlap_sections": list(registry[a:m]),
                "uncovered_sections": uncovered,
                "drop_units": drop_units}

    # ── Case 3: defensive truncation — no dropped sections, ask for the
    # reference canonical's count instead.
    return {"mode": "truncation", "stream": chosen, "unit": units[requested - 1],
            "borrowed_from": None, "overlap_sections": [],
            "uncovered_sections": [], "synthesis_only": False,
            "reference_count": len(units),
            "withheld_units": [u["unit"] for u in units[requested:]]}


# ── the serve itself ─────────────────────────────────────────────────────────


def _unit_phases(stream, unit):
    by_id = {p["phase_id"]: p for p in stream["phases"]}
    return [by_id[pid] for pid in unit["phase_ids"]]


def _scaled_bands(stream, unit, duration):
    phases = _unit_phases(stream, unit)
    src = sum(p["minutes"] for p in phases)
    if src <= 0:
        raise ServeError("SERVE INVALID: unit %s has no authored minutes" % unit["unit"])
    mins = integerise([p["minutes"] * duration / src for p in phases], duration)
    bands, cur = [], 0
    for p, m in zip(phases, mins):
        band = {"band_id": p["phase_id"], "minutes": "%d-%d" % (cur, cur + m),
                "activity": p["activity"]}
        if p.get("role"):
            band["role"] = p["role"]
        bands.append(band)
        cur += m
    return bands


def _period_from_unit(stream, unit, sitting, duration):
    return {
        "period_number": sitting,
        "period_duration_minutes": duration,
        "activity_title": unit["activity_title"],
        "section_anchor": unit["section_anchor"],
        "materials": list(unit.get("materials") or []),
        "visual_aids": unit.get("visual_aids"),
        "time_bands": _scaled_bands(stream, unit, duration),
        "section_context": unit.get("section_context"),
        "pedagogical_approaches": list(unit.get("pedagogical_approaches") or []),
        "teacher_notes": unit.get("teacher_notes", ""),
        "homework": list(unit.get("homework") or []),
        # band ids are internal labels since compile v0.5; edges pass through verbatim
        "competency_edges": [dict(e) for e in (unit.get("competency_edges") or [])],
    }


def serve_plan(streams, matrix):
    """Variant library (compiled streams) + duration matrix -> saved plan dict.

    The plan's shape is renderer-compatible with the old engine's output; the
    genon block reports the serve decisions instead of compression regimes."""
    if not streams:
        raise ServeError("SERVE INVALID: empty variant library")
    durations = order_durations(matrix)
    requested = len(durations)
    if requested < 1:
        raise ServeError("SERVE INVALID: empty duration matrix")

    registry_top = section_registry(max(streams, key=lambda s: len(s["units"])))
    chosen, surrendered = choose_variant(streams, requested)
    registry = section_registry(chosen)
    units = chosen["units"]
    n_units = len(units)

    fill = None
    if surrendered or requested == n_units:
        served = [(chosen, u) for u in units]        # whole variant, verbatim
    else:
        fill = fill_slot(streams, chosen, requested, registry)
        prefix = [(chosen, u) for u in units[:requested - 1]]
        served = prefix + [(fill["stream"], fill["unit"])]

    sit_durations = durations[:len(served)]
    surrendered_durations = durations[len(served):]

    new_periods = [_period_from_unit(stream, unit, i, dur)
                   for i, ((stream, unit), dur) in enumerate(zip(served, sit_durations), 1)]

    # ── assessment: anchoring is unit-level (compile v0.5 normalizes unit_ref) —
    # the chosen variant's items remap unit -> sitting; a borrowed fill unit
    # brings its own items from its home variant, anchored to the fill sitting ──
    served_chosen_units = {u["unit"] for s, u in served if s is chosen}
    unit_to_sitting = {}
    for i, (s, u) in enumerate(served, 1):
        if s is chosen:
            unit_to_sitting[u["unit"]] = i

    # Dropped units are built HERE (they used to be built after the notes) because the
    # assessment needs their sitting numbers: a dropped unit is shown to the teacher as
    # self-study, so its questions must travel with it. They come FROM THE LENDING PLAN's
    # units after the serving unit, and are renumbered N+1, N+2… in this plan's own
    # sequence — never the lender's original numbers, which could collide with a served
    # sitting and hang the questions on the wrong unit.
    dropped_units = []
    dropped_lender_unit_to_sitting = {}
    if fill and fill.get("drop_units"):
        base = len(served)
        for u in fill["drop_units"]:
            p = _period_from_unit(fill["stream"], u, base + len(dropped_units) + 1,
                                  u["authored_duration_minutes"])
            p["unscheduled"] = True
            dropped_lender_unit_to_sitting[u["unit"]] = p["period_number"]
            dropped_units.append(p)

    # ── assessment: anchoring is unit-level (compile v0.5 normalizes unit_ref) —
    # the chosen variant's items remap unit -> sitting; a borrowed fill unit
    # brings its own items from its home variant, anchored to the fill sitting ──
    #
    # AN ITEM WHOSE UNIT IS NOT IN THIS PLAN IS NOT IN THIS PLAN (ARV-D-037, 2026-08-03).
    # It used to be kept with `period_ref: []` and a scheduling note. That state was
    # neither in nor out: the screen anchors items to units, so it rendered nowhere, while
    # the EXPORT walks assessment_items flat and printed it — on the 8-period serve, 7 of
    # 20 questions were invisible on screen and present on paper, about units the class
    # never had. Nor could they be re-anchored to whatever else teaches their section: the
    # item's implied_lo is not in this plan's coverage_handoff (measured: 7 of 7 absent),
    # its demand was set by a sitting that did not happen, and section labels are merged
    # strings that differ between canonicals. So the item is DROPPED, and the count is
    # reported in provenance rather than left to be inferred from a silence.
    items = []
    unserved_items = 0
    for it in chosen["assessment_items"]:
        it2 = json.loads(json.dumps(it))
        anchors = it2.get("unit_ref") or []
        live = [unit_to_sitting[u] for u in anchors if u in unit_to_sitting]
        if live or not anchors:
            it2["period_ref"] = [max(live)] if live else it2.get("period_ref")
            items.append(it2)
            continue
        # not served — but if its unit is one the teacher still SEES (a dropped unit from
        # this same plan), the question rides with that unit instead of being lost.
        drops = [dropped_lender_unit_to_sitting[u] for u in anchors
                 if fill and fill["stream"] is chosen
                 and u in dropped_lender_unit_to_sitting]
        if drops:
            it2["period_ref"] = [max(drops)]
            it2["unscheduled"] = True          # screen: yes (with its unit) · export: no
            items.append(it2)
        else:
            unserved_items += 1
    if fill and fill["stream"] is not chosen and fill.get("borrowed_from"):
        fn = fill["unit"]["unit"]
        fsit = len(served)
        for it in fill["stream"]["assessment_items"]:
            if fn in (it.get("unit_ref") or []):
                it2 = json.loads(json.dumps(it))
                it2["period_ref"] = [fsit]
                items.append(it2)
    # dropped units lent by a DIFFERENT plan bring their questions with them too
    if fill and fill["stream"] is not chosen and dropped_lender_unit_to_sitting:
        for it in fill["stream"]["assessment_items"]:
            hit = [dropped_lender_unit_to_sitting[u] for u in (it.get("unit_ref") or [])
                   if u in dropped_lender_unit_to_sitting]
            if hit:
                it2 = json.loads(json.dumps(it))
                it2["period_ref"] = [max(hit)]
                it2["unscheduled"] = True
                items.append(it2)

    # ── coverage handoff: chosen's rows, filtered to served units, remapped ──
    # Dropped units' rows are RESTORED, flagged: their questions are in the plan, so their
    # LOs must be too — an item whose LO the plan does not contain breaks the identity the
    # whole assessment rests on (one item <- one LO -> one unit).
    handoff = json.loads(json.dumps(chosen.get("coverage_handoff") or {}))
    for c in handoff.values():
        kept = [lo for lo in c.get("los", [])
                if int(lo.get("period_number", -1)) in served_chosen_units]
        for lo in kept:
            lo["period_number"] = unit_to_sitting[int(lo["period_number"])]
        c["los"] = kept
    if dropped_lender_unit_to_sitting:
        lender_ho = (fill["stream"].get("coverage_handoff") or {}) if fill else {}
        for code, blk in lender_ho.items():
            rows = []
            for lo in blk.get("los", []):
                sit = dropped_lender_unit_to_sitting.get(int(lo.get("period_number", -1)))
                if sit is None:
                    continue
                lo2 = json.loads(json.dumps(lo))
                lo2["period_number"] = sit
                lo2["unscheduled"] = True
                rows.append(lo2)
            if not rows:
                continue
            if code in handoff:
                handoff[code]["los"] = (handoff[code].get("los") or []) + rows
            else:
                blk2 = json.loads(json.dumps(blk))
                blk2["los"] = rows
                handoff[code] = blk2

    # ── the honest notes ─────────────────────────────────────────────────────
    coverage_note = None
    if fill:
        if fill["mode"] == "fill":
            parts = []
            if fill["overlap_sections"]:
                parts.append(
                    "The closing sitting briefly re-crosses "
                    + "; ".join(fill["overlap_sections"])
                    + " as runway before introducing "
                    + fill["first_section"] + ".")
            if fill["uncovered_sections"]:
                parts.append(
                    "Time budget short of the chapter's full span: "
                    + "; ".join(fill["uncovered_sections"])
                    + " could not be scheduled — the material is included for "
                      "you to share as guided self-study or homework.")
            coverage_note = " ".join(parts) or None
        elif fill["mode"] == "synthesis":
            coverage_note = (
                "Every section is covered; the closing sitting draws the "
                "chapter together in one synthesis.")
        elif fill["mode"] == "truncation":
            if fill.get("synthesis_only"):
                coverage_note = (
                    "Every section is covered; the chapter's remaining synthesis "
                    "sittings could not be scheduled — their material is included "
                    "for you to draw on.")
            else:
                # Case 3 (§0.4): the request sits too far from its reference
                # canonical to close coherently. No dropped sections are shown —
                # the honest ask is the reference plan's depth.
                coverage_note = (
                    "This chapter cannot be adapted coherently at %d period(s). "
                    "Plan at least %d periods — this chapter's reference plan at "
                    "your budget — to teach it as designed."
                    % (requested, fill.get("reference_count", n_units)))
    surrender_note = None
    if surrendered:
        surrender_note = ("%d period(s) (%d minutes) exceed this chapter's fullest "
                          "plan and return to your budget."
                          % (surrendered, sum(surrendered_durations)))
        # Founder ruling 2026-08-01: surrender surfaces EXACTLY where drops do — the
        # generation-time note channel (section_coverage_note), and nowhere else.
        # Surrender and coverage loss are mutually exclusive, so no collision.
        coverage_note = surrender_note

    # ── Dropped sections (founder, 2026-08-01; re-sourced 2026-08-03 §0.4):
    # whenever the serve leaves sections uncovered, the plan CARRIES the units
    # whose coverage was lost, verbatim as authored, flagged unscheduled — and
    # they come FROM THE LENDING PLAN's units after the serving unit, so the
    # tail continues the plan the closing sitting came from. Online-only
    # self-study material ("give her access to it"); exports deliberately omit
    # it. Case-3 truncation deliberately shows none (the ask is the reference
    # plan's depth, not a salvage).
    # (dropped_units are built above, with the assessment — their questions ride with them)

    # ── the SERVED schedule (founder, 2026-08-01): every teacher-facing time print
    # reflects the periods actually used, never the request. A surrendered request
    # (13 asked, 12 served) prints 12; the request survives in genon.matrix /
    # period_rows_snapshot as provenance.
    served_agg = {}
    for d in sit_durations:
        served_agg[d] = served_agg.get(d, 0) + 1
    served_matrix = [(d, served_agg[d]) for d in sorted(served_agg, reverse=True)]
    total = sum(sit_durations)
    nper = len(served)
    rows = "\n".join("  Row %d: %d minutes × %d periods = %d minutes"
                     % (i + 1, d, c, d * c) for i, (d, c) in enumerate(served_matrix))
    meta = chosen["meta"]
    plan = {
        "filename": None,
        "saved_at": None,
        "grade": meta["grade"],
        "subject": meta["subject"],
        "chapter_number": meta["chapter_number"],
        "chapter_title": meta["chapter_title"],
        "period_schedule_display": ("Period schedule:\n%s\nTotal: %d periods · %dh %02dmin"
                                    % (rows, nper, total // 60, total % 60)),
        "period_rows_snapshot": [{"id": i, "duration": d, "count": c}
                                 for i, (d, c) in enumerate(matrix)],
        "plan_status": "adapted",
        "result": {
            "lesson_plan": {"periods": new_periods},
            "coverage_handoff": handoff,
            "assessment_items": items,
            "section_coverage_note": coverage_note,
            "dropped_units": dropped_units or None,
        },
        "genon": {
            "engine": ("serve v2.1 / e13 (canonical library, next-highest selection, "
                       "X-1+1 slot fill by the first-exposure choice set §0.4, "
                       "proportional duration scaling, unit-anchored assessment; "
                       "e13: an item whose unit is not in the plan is not in the plan, "
                       "and a dropped unit's questions ride with it)"),
            "library": sorted((len(s["units"]) for s in streams), reverse=True),
            "variant_used": n_units,
            "requested_periods": requested,
            "sittings": len(served),
            "slot_fill": (None if not fill else {
                "mode": fill["mode"],
                "fill_class": fill.get("fill_class"),
                "first_section": fill.get("first_section"),
                "borrowed_from": fill.get("borrowed_from"),
                "self_fill": bool(fill.get("self_fill")),
                "overlap_sections": fill.get("overlap_sections") or [],
                "uncovered_sections": fill.get("uncovered_sections") or [],
                "synthesis_only": bool(fill.get("synthesis_only")),
                "reference_count": fill.get("reference_count"),
                "withheld_units": fill.get("withheld_units") or [],
            }),
            "surrendered_periods": surrendered,
            "surrender_note": surrender_note,
            # How much of the canonical's assessment did not come with this serve. Reported
            # so the loss is a number someone can look at, not a silence (ARV-D-037).
            "assessment_items_unserved": unserved_items,
            "assessment_items_unscheduled": sum(1 for i in items if i.get("unscheduled")),
            "stream_source": meta.get("source_file"),
            "matrix": [{"duration": d, "count": c} for d, c in matrix],
            "served_matrix": [{"duration": d, "count": c} for d, c in served_matrix],
            "duration_sequence": durations,
            "scale": [round(d / u["authored_duration_minutes"], 3)
                      for (s, u), d in zip(served, sit_durations)],
            "registry": registry_top,
        },
    }

    # ── validation: tiling + served order — never serve an invalid plan ──────
    probs = []
    for p in plan["result"]["lesson_plan"]["periods"]:
        cur = 0
        for b in p["time_bands"]:
            a, z = (int(x) for x in b["minutes"].split("-"))
            if a != cur:
                probs.append("P%d gap at %s" % (p["period_number"], b["minutes"]))
            cur = z
        if cur != p["period_duration_minutes"]:
            probs.append("P%d sums %d != %d"
                         % (p["period_number"], cur, p["period_duration_minutes"]))
    chosen_served = [u["unit"] for s, u in served if s is chosen]
    if chosen_served != sorted(chosen_served):
        probs.append("served unit order violated")
    if probs:
        raise ServeError("SERVE INVALID:\n  " + "\n  ".join(probs))
    return plan
