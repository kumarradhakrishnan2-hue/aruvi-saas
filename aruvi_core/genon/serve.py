"""Aruvi variant-serve engine — v1.0 (2026-07-31). Replaces the partition engine.

Doctrine (docs/variant_canonical_architecture.md): a chapter is authored as a small
LIBRARY of variant canonicals — the same section list planned at two or three period
counts, each a complete, coherent plan whose every sitting is one authored unit-arc.
Serving a teacher's request is SELECTION, never composition:

  * the NEXT-HIGHEST variant is chosen (full richness; surrender only above the top);
  * the first X-1 sittings are that variant's units 1..X-1, verbatim;
  * slot X is SELECTED from the library's closing units by a fixed ladder —
    exact fill > superset (minimal overlap, revision runway) > longest suffix >
    truncation (serve unit X, withhold the tail, hand the material over);
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


def _norm(s):
    return " ".join(str(s or "").split()).casefold()


def _unit_anchors(unit):
    return [a.strip() for a in str(unit.get("section_anchor") or "").split(_ANCHOR_JOINER)
            if a.strip()]


def section_registry(stream):
    """Ordered unique section anchors across a stream's units."""
    out, seen = [], set()
    for u in stream["units"]:
        for a in _unit_anchors(u):
            k = _norm(a)
            if k not in seen:
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


def fill_slot(streams, chosen, requested, registry):
    """The slot-X ladder. Returns a dict describing the fill, or a truncation.

    FRONTIER ARITHMETIC (founder ruling, 2026-07-31): what the prefix has
    covered is measured by its first-visit frontier — the furthest registry
    section any prefix unit reaches. Backward-anchored synthesis sittings (ch 5
    authors three of them) revisit sections without advancing the frontier, so
    the UNCOVERED span is always a registry suffix even when unit anchors are
    not monotonic. When the frontier already stands at the last section, the
    withheld tail is synthesis-only: coverage is complete and slot X borrows a
    companion variant's closing synthesis (nearest in scale), or hands the
    synthesis material over.

    Candidates are the CLOSING units of the other variants only — a fill is a
    designed consolidation from a denser plan, never a skip inside the chosen
    plan (the founder's 11-vs-12 ruling: with no denser closing unit available,
    curtail and hand the material over, don't jump the chapter's own sequence)."""
    ridx = {_norm(a): i for i, a in enumerate(registry)}
    last = len(registry) - 1
    units = chosen["units"]
    ranges = [unit_range(u, ridx) for u in units]
    if any(r is None for r in ranges):
        raise ServeError("SERVE INVALID: chosen variant has units outside its own registry")
    frontier = max((r[1] for r in ranges[:requested - 1]), default=-1)
    lo = frontier + 1

    if lo > last:
        # prefix covers every section — the withheld tail is synthesis-only
        others = [s for s in streams if s is not chosen]
        if others:
            c = min(others, key=lambda s: (abs(len(s["units"]) - requested),
                                           len(s["units"])))
            return {"mode": "synthesis", "stream": c, "unit": c["units"][-1],
                    "borrowed_from": len(c["units"]),
                    "overlap_sections": [], "uncovered_sections": [],
                    "withheld_units": [u["unit"] for u in units[requested - 1:]]}
        return {"mode": "truncation", "stream": chosen, "unit": units[requested - 1],
                "borrowed_from": None, "overlap_sections": [],
                "uncovered_sections": [], "synthesis_only": True,
                "withheld_units": [u["unit"] for u in units[requested:]]}

    exact_or_super, suffixes = [], []
    for s in streams:
        if s is chosen:
            continue
        cu = s["units"][-1]
        r = unit_range(cu, ridx)
        if r is None or r[1] != last:
            continue                      # not closure-bearing in this registry
        clo = r[0]
        cand = {"stream": s, "unit": cu, "variant_count": len(s["units"]), "range": r}
        if clo <= lo:
            cand["overlap"] = registry[clo:lo]
            exact_or_super.append(cand)
        else:
            cand["uncovered"] = registry[lo:clo]
            suffixes.append(cand)

    if exact_or_super:
        exact_or_super.sort(key=lambda c: (len(c["overlap"]), -c["variant_count"]))
        c = exact_or_super[0]
        mode = "exact" if not c["overlap"] else "superset"
        return {"mode": mode, "stream": c["stream"], "unit": c["unit"],
                "borrowed_from": c["variant_count"],
                "overlap_sections": list(c["overlap"]), "uncovered_sections": []}
    if suffixes:
        suffixes.sort(key=lambda c: (len(c["uncovered"]), -c["variant_count"]))
        c = suffixes[0]
        return {"mode": "suffix", "stream": c["stream"], "unit": c["unit"],
                "borrowed_from": c["variant_count"],
                "overlap_sections": [], "uncovered_sections": list(c["uncovered"])}
    # truncation — serve the chosen variant's own unit X, withhold the tail.
    # Uncovered = registry sections beyond the frontier INCLUDING unit X's reach;
    # when that is empty the withheld tail is synthesis-only and says so.
    f2 = max(frontier, ranges[requested - 1][1])
    uncov = list(registry[f2 + 1:])
    return {"mode": "truncation", "stream": chosen, "unit": units[requested - 1],
            "borrowed_from": None, "overlap_sections": [],
            "uncovered_sections": uncov, "synthesis_only": not uncov,
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

    items = []
    for it in chosen["assessment_items"]:
        it2 = json.loads(json.dumps(it))
        anchors = it2.get("unit_ref") or []
        live = [unit_to_sitting[u] for u in anchors if u in unit_to_sitting]
        if anchors and not live:
            it2["period_ref"] = []
            it2["scheduling_note"] = ("anchor unit not scheduled in this plan "
                                      "(time budget)")
        else:
            it2["period_ref"] = [max(live)] if live else it2.get("period_ref")
        items.append(it2)
    if fill and fill.get("borrowed_from"):
        fn = fill["unit"]["unit"]
        fsit = len(served)
        for it in fill["stream"]["assessment_items"]:
            if fn in (it.get("unit_ref") or []):
                it2 = json.loads(json.dumps(it))
                it2["period_ref"] = [fsit]
                items.append(it2)

    # ── coverage handoff: chosen's rows, filtered to served units, remapped ──
    handoff = json.loads(json.dumps(chosen.get("coverage_handoff") or {}))
    for c in handoff.values():
        kept = [lo for lo in c.get("los", [])
                if int(lo.get("period_number", -1)) in served_chosen_units]
        for lo in kept:
            lo["period_number"] = unit_to_sitting[int(lo["period_number"])]
        c["los"] = kept

    # ── the honest notes ─────────────────────────────────────────────────────
    coverage_note = None
    if fill:
        if fill["mode"] == "superset" and fill["overlap_sections"]:
            coverage_note = (
                "The closing sitting briefly re-crosses "
                + "; ".join(fill["overlap_sections"])
                + " as runway before completing the chapter.")
        elif fill["mode"] == "suffix":
            coverage_note = (
                "Time budget short of the chapter's full span: "
                + "; ".join(fill["uncovered_sections"])
                + " could not be scheduled — share this material for guided "
                  "self-study or homework. The closing sitting completes the chapter.")
        elif fill["mode"] == "synthesis":
            coverage_note = (
                "Every section is covered; the time budget trims the chapter's "
                "closing synthesis to one sitting.")
        elif fill["mode"] == "truncation":
            if fill.get("synthesis_only"):
                coverage_note = (
                    "Every section is covered; the chapter's remaining synthesis "
                    "sittings could not be scheduled — their material is included "
                    "for you to draw on.")
            else:
                coverage_note = (
                    "Time budget short of the chapter's full span: "
                    + "; ".join(fill["uncovered_sections"])
                    + " could not be scheduled. The material is included for you to "
                      "share — cover it as homework or found time.")
    surrender_note = None
    if surrendered:
        surrender_note = ("%d period(s) (%d minutes) exceed this chapter's fullest "
                          "plan and return to your budget."
                          % (surrendered, sum(surrendered_durations)))
        # Founder ruling 2026-08-01: surrender surfaces EXACTLY where drops do — the
        # generation-time note channel (section_coverage_note), and nowhere else.
        # Surrender and coverage loss are mutually exclusive, so no collision.
        coverage_note = surrender_note

    # ── Dropped sections (founder, 2026-08-01): below the floor — i.e. whenever the
    # serve leaves sections uncovered — the plan CARRIES the unserved units whose
    # coverage was lost, verbatim as authored, flagged unscheduled. Online-only
    # self-study material ("give her access to it"); exports deliberately omit it.
    dropped_units = []
    if fill and (fill.get("uncovered_sections") or []):
        _ridx = {_norm(a): i for i, a in enumerate(registry)}
        uncov = {_ridx[_norm(a)] for a in fill["uncovered_sections"] if _norm(a) in _ridx}
        base = len(served)
        for u in units:
            if u["unit"] in served_chosen_units:
                continue
            r = unit_range(u, _ridx)
            if r is None:
                continue
            if set(range(r[0], r[1] + 1)) <= uncov:   # its coverage was truly lost
                p = _period_from_unit(chosen, u, base + len(dropped_units) + 1,
                                      u["authored_duration_minutes"])
                p["unscheduled"] = True
                dropped_units.append(p)

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
            "engine": ("serve v1.1 (variant library, next-highest selection, "
                       "X-1+1 slot fill, proportional duration scaling, "
                       "unit-anchored assessment)"),
            "library": sorted((len(s["units"]) for s in streams), reverse=True),
            "variant_used": n_units,
            "requested_periods": requested,
            "sittings": len(served),
            "slot_fill": (None if not fill else {
                "mode": fill["mode"],
                "borrowed_from": fill.get("borrowed_from"),
                "overlap_sections": fill.get("overlap_sections") or [],
                "uncovered_sections": fill.get("uncovered_sections") or [],
                "synthesis_only": bool(fill.get("synthesis_only")),
                "withheld_units": fill.get("withheld_units") or [],
            }),
            "surrendered_periods": surrendered,
            "surrender_note": surrender_note,
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
