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

from . import carriers as _carriers


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
    """True iff the unit is the standard canonical's mandated closer (§0.3).

    Two carriers for one fact (2026-08-07): section-axis stages put the reserved token
    in `section_anchor`; a stage with no section axis (science·middle) has nowhere to
    put it and its brief mandates the explicit `synthesis` boolean, which compile.py
    stamps onto the unit. Read both here so no caller has to know the difference."""
    if unit.get("synthesis") is True:
        return True
    return [_norm(a) for a in _unit_anchors(unit)] == [SYNTH_TOKEN]


def section_registry(stream):
    """Ordered unique section anchors across a stream's units (the reserved
    synthesis token is not a section and never enters the registry).

    THE SYNTHESIS UNIT IS SKIPPED THROUGH `is_synthesis_unit`, not by filtering its
    anchor text (2026-08-10, S7). Filtering the token was enough while the token was
    the only carrier; on a MEDIATED-anchor stage the carrier is the `synthesis` boolean
    and the unit's anchor is whatever its period fields yielded, so a text filter would
    have let a synthesis unit contribute sections to the registry. Behaviour on the ten
    token-carrying stages is unchanged: the mandate gives that unit the token and nothing
    else, so skipping the unit and filtering its one anchor are the same operation."""
    out, seen = [], set()
    for u in stream["units"]:
        if is_synthesis_unit(u):
            continue
        for a in _unit_anchors(u):
            k = _norm(a)
            if k != SYNTH_TOKEN and k not in seen:
                seen.add(k)
                out.append(a)
    return out


def authored_registry(stream):
    """The registry as AUTHORING and CERTIFICATION must see it: `section_registry` plus the
    cells the standard teaches ONLY in its closing synthesis unit (ARV-D-157, 2026-08-14).

    NOT FOR SERVING. `section_registry` above is the serve registry and must keep excluding
    the synthesis unit — `unit_range` returns None for it, and §0.4 Case 1 depends on that
    unit being rangeless. This function exists because two OTHER readers need a different
    answer, and until now they silently got the serve one:

        variant_plans.standard_registry  -> writes the compact's brief
        build_library.certify            -> judges the compact against it

    On a MEDIATED-anchor stage the standard's closing unit may be the only place a real cell
    is taught: a short english chapter folds `writing` and `beyond_text` into its synthesis
    unit, so neither entered the registry. The brief then listed four cells instead of six and
    said "every unit's section reference MUST be drawn verbatim from this list" — so the
    compact was FORBIDDEN to teach writing, complied, and was certified incomplete. The one
    compact that taught the missing cell anyway was quarantined for anchoring outside the
    registry. Brief and judge agreed with each other and disagreed with the chapter.

    The tail is appended in the order the synthesis unit names it, which is also its true
    teaching order — that unit is last. So first-appearance order still reads straight.

    ONE function, both call sites, deliberately: the bug was not that either reader was wrong
    on its own, it was that the brief and the check could drift apart at all.
    """
    reg = section_registry(stream)
    body = {_norm(a) for u in stream["units"] if not is_synthesis_unit(u)
            for a in _unit_anchors(u)}
    seen, tail = set(), []
    for u in stream["units"]:
        if not is_synthesis_unit(u):
            continue
        for a in _unit_anchors(u):
            k = _norm(a)
            if k != SYNTH_TOKEN and k not in body and k not in seen:
                seen.add(k)
                tail.append(a)
    return reg + tail


def unit_sections(unit, registry_index):
    """The registry indices a unit ACTUALLY anchors — a SET, not a span.

    `unit_range` collapses a unit to (min, max), which is right for ordering and wrong
    for coverage: a unit anchored [12, 15] reports (12, 15) and the caller concludes it
    taught 13 and 14. It did not. Coverage must be counted section by section
    (ARV-D-168, 2026-08-16 · found at F1 on SS·VIII ch 15 X=11, where the served plan
    silently omitted Cultural Exchange — Food and Clothing with uncovered_sections: []).
    Contiguity was ASSUMED here — this function's docstring said "Contiguity (V2) makes
    every co-dealt section adjacent to M" — and 43 of 1,519 units in SS·middle alone
    break it. A synthesis unit is rangeless and therefore sectionless, same as above."""
    if is_synthesis_unit(unit):
        return set()
    out = set()
    for a in _unit_anchors(unit):
        i = registry_index.get(_norm(a))
        if i is not None:
            out.add(i)
    return out


def unit_range(unit, registry_index):
    """Unit -> (lo, hi) inclusive indices into the registry. None if any anchor
    is unknown to the registry (the candidate then simply doesn't qualify).

    A SYNTHESIS UNIT IS RANGELESS BY THE SEAM (2026-08-10, S7), for the same reason
    `section_registry` skips it there. On a token-carrying stage it was rangeless
    incidentally — "synthesis" is not a registry key — but on a mediated-anchor stage its
    anchor may well be a real section string, and a synthesis unit that reports a range
    can be picked by `first_dealing_unit` as somebody's Xth unit. It is the one unit whose
    only prior is FULL coverage (§0.4 Case 1), so it must never enter first-visit
    arithmetic. No change on the ten token stages."""
    if is_synthesis_unit(unit):
        return None
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


def exact_fit_rescue(streams, chosen, requested):
    """Case 1b (§0.4, v2.2 / e15) — the EXACT-FIT COMPLETE RESCUE.

    Called only when Case 2's fill has left registry sections uncovered. Returns
    the canonical whose FULL unit count is exactly `requested - 1`, if the library
    has one and it is not already the chosen plan; else None. The caller serves it
    complete and gives slot X to the standard's `synthesis` unit, so the teacher
    receives the whole chapter, closed, in exactly the periods she asked for.

    This is Case 1 with a wider set of bases, not a new mechanism: Case 1's warrant
    is that the synthesis unit's only prior is FULL COVERAGE, and a complete
    canonical satisfies that more strongly than a prefix does. It does not reopen
    ARV-D-025 — that was a synthesis MANDATED onto a compact at authoring time
    regardless of what preceded it; nothing is mandated here and the base is
    complete by construction (certify check 5 guarantees every canonical reaches
    the final registry section, so this rung can never itself drop).

    EXACT FIT ONLY (founder, 2026-08-06). Where count(D) + 1 < X the rescue would
    have to surrender the residual — serving is selection, so padding is not
    available — and the teacher would meet two visible compromises, a coarser plan
    AND periods handed back, to buy one gain. A returned period reads as the app
    failing to use her time. At exact fit there is no time cost at all: the only
    difference is front-section granularity, which she cannot perceive. The
    restriction loses nothing structural, because the inversion being fixed is a
    one-above-a-canonical event (X = C is identity and complete; X = C+1 moves onto
    the next canonical's pacing with only C units of prefix) — exactly the X at
    which a canonical of count X - 1 exists.
    """
    for s in streams:
        if s is not chosen and len(s["units"]) == requested - 1:
            return s
    return None


def select_whole_plan(streams, requested):
    """PLAN-GRANULARITY selection (science·middle; docs/science_middle_stage_serve.md).

    Where units are not separable — a cognitive-progression stage is taught whole or not
    at all — no prefix of a canonical is a valid plan, so there is nothing to fill and
    nothing to borrow except the chapter's one closing synthesis. Returns
    (chosen, surrendered, fill) for serve_plan, where `fill` is None (serve the canonical
    whole), a `synthesis` borrow (serve it whole, then the top's synthesis as sitting X),
    or a below-floor `truncation` carrying its dropped tail.

    ONE RULE, four consequences: serve the LARGEST number of sittings that is ≤ X and is
    either a canonical's own count K or K+1 (K complete, closed by the borrowed
    synthesis). That single line yields identity at X = K, the synthesis borrow at
    X = K+1, surrender above the top, and — because the density rule spaces canonicals
    exactly 2 apart (genon/master_plan.py) — never surrenders inside the band. Below the
    lowest canonical there is no such number, and only there do we truncate.

    The +1 extension is not offered on the canonical that OWNS the synthesis: it already
    ends with that unit, and lending a plan its own closer would serve it twice."""
    ranked = sorted(streams, key=lambda s: -len(s["units"]))
    top = ranked[0]
    syn = synthesis_unit_of(streams)

    if requested >= len(top["units"]):
        return top, requested - len(top["units"]), None      # identity / surrender

    # Maximise sittings served; at equal length prefer IDENTITY over the borrow. Both
    # forms can reach the same X (X = 8 is the 8-canonical whole, and also the
    # 7-canonical plus a synthesis), and the purpose-authored plan at that exact length
    # is the better teaching object — its arc was written for those periods, where the
    # other is a shorter arc with a closer bolted on. Without this the winner would
    # depend on the order the library happened to glob off disk.
    best = None                                              # (served, prefers, s, syn?)
    for s in streams:
        k = len(s["units"])
        if k <= requested:
            cand = (k, 1, s, False)                          # 1 = identity, wins ties
            if best is None or cand[:2] > best[:2]:
                best = cand
        if syn and s is not syn[0] and k + 1 <= requested:
            cand = (k + 1, 0, s, True)
            if best is None or cand[:2] > best[:2]:
                best = cand

    if best is None:
        # ── Below the lowest canonical. Partial stages ARE tolerated here and only
        # here: the request is already in declared-deficit territory, and showing the
        # teacher the sittings she will not reach beats refusing her a plan. The tail
        # rides e09's channel — dropped_units, online only, omitted from exports — and
        # its questions travel with it through the existing chosen-plan drop path.
        low = ranked[-1]
        return low, 0, {
            "mode": "truncation", "below_floor": True, "fill_class": None,
            "first_section": None, "stream": low, "unit": low["units"][requested - 1],
            "borrowed_from": None, "self_fill": True, "overlap_sections": [],
            "uncovered_sections": [], "synthesis_only": False, "reference_count": None,
            "withheld_units": [], "drop_units": list(low["units"][requested:]),
        }

    served_count, _prefers, s, use_syn = best
    if not use_syn:
        return s, requested - served_count, None
    s_syn, u_syn = syn
    return s, requested - served_count, {
        "mode": "synthesis", "below_floor": False, "fill_class": None,
        "first_section": None, "stream": s_syn, "unit": u_syn,
        "borrowed_from": len(s_syn["units"]), "self_fill": False,
        "overlap_sections": [], "uncovered_sections": [], "synthesis_only": False,
        "reference_count": None, "withheld_units": [], "drop_units": [],
        # ── THE BORROWED SYNTHESIS BRINGS NOTHING BUT ITSELF (ARV-D-067, 2026-08-07) ──
        # C9.2's standing rule — "a borrowed unit brings its own items" — presupposes
        # UNIT-level anchoring. Under stage-level anchoring a unit has no items of its
        # own: it inherits its whole STAGE's set. So carrying the lender's items dragged
        # the top's entire final-stage assessment into a variant whose class was never
        # taught that stage's earlier units, and carrying the lender's handoff row grew a
        # phantom extra stage holding one sitting. Both wrong, and the 2026-08-07 ruling
        # that "the synthesis carries items and travels with them" was made before this
        # distinction was visible — it holds for the section-axis stages and not here.
        #   `silent` suppresses both imports; `adopt_group` makes the unit join the host's
        # LAST group, which is where it belongs: a closing sitting of the final stage, not
        # a stage of its own. Its stage keeps exactly the items the variant authored, and
        # none of them anchor to the synthesis sitting.
        "silent": True,
        "adopt_group": True,
    }


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
    brisk re-cross is redundancy, and redundancy is not jumpiness. Ties (SELF
    FIRST, added 2026-08-04, architecture v2.1): the chosen plan's OWN
    candidate wins every tie it enters, then the lender whose count is closest
    to X (pacing context), then the denser plan.
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
                      "overlap": o, "reach": b, "self": s is chosen,
                      "count": len(s["units"])})
    if cands:
        # SELF-PREFERENCE (2026-08-04, architecture v2.1): the chosen plan's own
        # candidate wins every tie it enters. Until today the sort fell straight
        # from reach to pacing distance, so the identity candidate carried no
        # privilege and the engine handed the teacher a stranger's closing unit
        # while the plan she was being served had its own — SS·IX X=8 (p10 U8 lost
        # to p07 U7 on |7−8| < |10−8|), SS·VIII X=11 and X=14. Every candidate is
        # first-exposure and therefore SAFE, so this is continuity, not correctness:
        # the home unit names the content the class just had, in the voice its own
        # prefix established. It stays a TIE-BREAK — placed below reach, it never
        # lifts a home unit above a better preference class.
        cands.sort(key=lambda c: (0 if c["overlap"] == 0 else 1,   # no re-cross first
                                  c["overlap"],                    # then least re-cross
                                  -c["reach"],                     # furthest reach
                                  0 if c["self"] else 1,           # SELF FIRST
                                  abs(c["count"] - requested),     # pacing context
                                  -c["count"]))                    # then denser
        c = cands[0]
        a, b = c["range"]
        fill_class = ("forward" if c["overlap"] == 0 and b > m
                      else "single" if c["overlap"] == 0
                      else "backward")
        # COVERAGE IS A SET, NOT A FRONTIER (ARV-D-168, 2026-08-16). This was
        # `list(registry[b + 1:])` — everything past the borrowed unit's highest
        # anchor — which silently swallowed any section sitting INSIDE a
        # non-contiguous unit's span. Preference and selection are deliberately
        # untouched: the engine still prefers the furthest-reaching candidate and
        # still borrows the same unit. Only the accounting changes, so a gap is
        # now DECLARED and its sections ride from the lender exactly as §0.4 says.
        taught = set()
        for pu in units[:requested - 1]:
            taught |= unit_sections(pu, ridx)
        taught |= unit_sections(c["unit"], ridx)
        uncov_idx = {i for i in range(last + 1) if i not in taught}
        uncovered = [registry[i] for i in sorted(uncov_idx)]
        s = c["stream"]
        drop_units = []
        if uncovered:
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
    # The authored fields the engine does not model are spliced back FIRST, so the
    # engine's own keys always win (`period_number` in particular must be the SITTING,
    # never the authored unit number). Without this a served plan is missing whatever
    # its subject's port groups on — science·middle's `progression_stage` / `stage_label`,
    # whose absence collapsed a served plan into one "Stage None" group. compile.py's
    # `_MODELLED` decides what lands here; neither end knows a subject's name.
    return {
        **(unit.get("extra") or {}),
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
        # THE SYNTHESIS FLAG MUST SURVIVE THE SERVE (2026-08-10, S7 · C6).
        # `synthesis` is a MODELLED key, so compile strips it from `extra` — and nothing put
        # it back, so every served synthesis unit arrived flagless. On a stage whose anchor is
        # MEDIATED that is not cosmetic: with no flag, `carriers.is_synthesis` is False, the
        # port falls through to `textbook_segments[0]`, and the closing whole-chapter unit was
        # labelled "Equilateral Triangles (Revisit)" — the first section it names, marked as a
        # repeat. The canonical on disk read "Synthesis" and the SERVED plan did not, which is
        # the worse half: the served plan is what a teacher actually opens.
        #
        # Recorded honestly: this residue was DISCLOSED earlier the same day as harmless
        # ("nothing downstream reads it"). That was wrong within hours — `is_synthesis` had
        # just become what the group label reads. A carried-not-emitted field is only harmless
        # until something starts reading it.
        **({"synthesis": True} if unit.get("synthesis") else {}),
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

    # WHICH ENGINE SERVES THIS STAGE — asked of the subject plugin, never inferred from
    # the subject's name (CLAUDE.md §3). "unit" for ten stages; "plan" for science·middle,
    # whose units belong to a cognitive arc and cannot be cut (spec §1).
    _meta0 = max(streams, key=lambda s: len(s["units"]))["meta"]
    meta0_subject, meta0_grade = _meta0.get("subject"), _meta0.get("grade")
    granularity = _carriers.serve_granularity(meta0_subject, meta0_grade)

    rescued_from = None
    if granularity == "plan":
        # ── PLAN GRANULARITY: selection only. No prefix, no choice set, no fill class.
        chosen, surrendered, fill = select_whole_plan(streams, requested)
        units, n_units = chosen["units"], len(chosen["units"])
        registry = section_registry(chosen)          # empty on a stage with no sections
        if fill is None:
            served = [(chosen, u) for u in units]                     # identity/surrender
        elif fill["mode"] == "synthesis":
            served = [(chosen, u) for u in units] + [(fill["stream"], fill["unit"])]
        else:                                                         # below-floor
            served = [(chosen, u) for u in units[:requested]]
    else:
        # ── UNIT GRANULARITY: the standard engine, unchanged (§0.4).
        chosen, surrendered = choose_variant(streams, requested)
        # THE REGISTRY IS THE TOP'S, ESTABLISHED ONCE (ARV-D-169, 2026-08-16).
        # This re-derived it from `chosen`, so coverage was judged against the SERVED
        # variant's own section list — and a compact can never appear to drop what was
        # never on its list. SS·VIII ch 8 X=7 picks the 8-period compact, whose registry
        # omits "Ocean currents" and "Ocean trenches"; it reported full coverage of a
        # chapter it teaches 13 of 15 sections of. Measured before changing: on 1,398 of
        # 1,400 serves the two registries are IDENTICAL, so this corrects a real hole
        # without moving the common case. Same failure shape as C5 check 11 and as the
        # frontier bug (ARV-D-168) — the thing being measured was derived from the thing
        # being judged.
        registry = registry_top
        units = chosen["units"]
        n_units = len(units)
        fill = None
        if surrendered or requested == n_units:
            served = [(chosen, u) for u in units]    # whole variant, verbatim
        else:
            fill = fill_slot(streams, chosen, requested, registry)
            # ── Case 1b (§0.4, v2.2 / e15): the upward serve would DROP. If a canonical's
            # full count is exactly X-1, serve it complete and close with the standard's
            # synthesis instead — the whole chapter, properly ended, in the periods she
            # asked for. Tried LAST, so richness is only ever traded for completeness and
            # never for its own sake. Rebinding `chosen` is required, not optional: the
            # assessment remap below walks `chosen["assessment_items"]` and matches
            # `s is chosen`, so a base swap that left `chosen` behind would strand every
            # item as unserved.
            if fill.get("uncovered_sections"):
                d = exact_fit_rescue(streams, chosen, requested)
                syn = synthesis_unit_of(streams) if d is not None else None
                if d is not None and syn is not None:
                    rescued_from = n_units           # the richer plan we declined
                    s_syn, u_syn = syn
                    chosen, units, n_units = d, d["units"], len(d["units"])
                    registry = registry_top          # unchanged by a base swap
                    fill = {"mode": "complete_rescue", "fill_class": None,
                            "first_section": None, "stream": s_syn, "unit": u_syn,
                            "borrowed_from": len(s_syn["units"]),
                            "self_fill": s_syn is chosen, "overlap_sections": [],
                            "uncovered_sections": [], "synthesis_only": False,
                            "reference_count": None, "withheld_units": [],
                            "drop_units": []}
            prefix = [(chosen, u) for u in units[:requested - 1]]
            served = prefix + [(fill["stream"], fill["unit"])]

    sit_durations = durations[:len(served)]
    surrendered_durations = durations[len(served):]

    new_periods = [_period_from_unit(stream, unit, i, dur)
                   for i, ((stream, unit), dur) in enumerate(zip(served, sit_durations), 1)]

    # ── the borrowed unit joins the HOST's last group (ARV-D-067, 2026-08-07) ──────────
    # Only at plan granularity, and only for the fields the SUBJECT declares as its
    # grouping keys — everything else on the borrowed unit (its title, bands, notes,
    # materials) is its own and must survive verbatim. Without this the top's synthesis
    # arrived still wearing its home arc's stage number and the served plan grew a stage
    # that existed nowhere in what the class was taught.
    if fill and fill.get("adopt_group") and len(new_periods) > 1:
        gf = _carriers.group_fields(meta0_subject, meta0_grade)
        if gf:
            host = new_periods[-2]
            for k in gf:
                if k in host:
                    new_periods[-1][k] = host[k]

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
    if (fill and fill["stream"] is not chosen and fill.get("borrowed_from")
            and not fill.get("silent")):          # `silent` -> ARV-D-067, see select_whole_plan
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
    # A BORROWED SERVED UNIT'S ROW TRAVELS TOO (ARV-D-064, 2026-08-06). The dropped-unit
    # path below has always done this; the borrowed-unit path did not, and the reason it
    # must is the same one stated above — the borrowed unit's questions are in this plan
    # (they are appended a few lines up), so the LO they test has to be in it as well, or
    # the plan asks something its own coverage never claims to teach. This is NOT how the
    # item finds its sitting: that is the platform stamp (`period_ref`), read by
    # link_resolver.platform_anchor. The row is carried for the LO, the label and the
    # coverage ledger. Safe to carry verbatim because the engine handoff is keyed on the
    # section LABEL, not on `section_number` — carriers.to_engine_handoff chose that key
    # for exactly this reason, so a lender's row cannot land on a host section that
    # happens to share its number, and a genuinely shared section merges as it should.
    if (fill and fill["stream"] is not chosen and fill.get("borrowed_from")
            and not fill.get("silent")):          # `silent` -> ARV-D-067, see select_whole_plan
        fn = fill["unit"]["unit"]
        fsit = len(served)
        for code, blk in (fill["stream"].get("coverage_handoff") or {}).items():
            rows = []
            for lo in blk.get("los", []):
                if int(lo.get("period_number", -1)) != fn:
                    continue
                lo2 = json.loads(json.dumps(lo))
                lo2["period_number"] = fsit
                rows.append(lo2)
            if not rows:
                continue
            if code in handoff:
                handoff[code]["los"] = (handoff[code].get("los") or []) + rows
            else:
                blk2 = json.loads(json.dumps(blk))
                blk2["los"] = rows
                # The borrowed unit is the LAST sitting, so its row reads last. The
                # lender's own `_order` is its position in the LENDER's handoff and
                # would otherwise interleave it into the middle of the host's rows.
                blk2["_order"] = 1 + max(
                    [int(b.get("_order", 0)) for b in handoff.values()
                     if isinstance(b, dict) and b.get("_order") is not None] or [0])
                handoff[code] = blk2
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
        elif fill["mode"] in ("synthesis", "complete_rescue"):
            # Case 1b reads to the teacher EXACTLY as Case 1 does, and that is
            # deliberate: from where she sits the two are the same event — every
            # section covered, the chapter drawn together at the end, in the periods
            # she asked for. The base swap is provenance (genon.slot_fill.mode and
            # rescued_from carry it), not news. Saying anything else here would
            # advertise a plan she did not get.
            coverage_note = (
                "Every section is covered; the closing sitting draws the "
                "chapter together in one synthesis.")
        elif fill["mode"] == "truncation":
            if fill.get("below_floor"):
                # PLAN granularity, below the lowest canonical (spec §2). There are no
                # sections to name, so name the sittings — the arc's own closing units,
                # which is what she is actually missing and what the dropped_units panel
                # is about to show her.
                lost = [u["activity_title"] for u in (fill.get("drop_units") or [])]
                coverage_note = (
                    "Time budget short of this chapter's shortest complete plan: "
                    "%d sitting(s) could not be scheduled%s — the material is included "
                    "for you to share as guided self-study or homework."
                    % (len(lost), (" (" + "; ".join(lost) + ")") if lost else ""))
            elif fill.get("synthesis_only"):
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
            # Restored to the SUBJECT's own shape (carriers.from_engine_handoff). The
            # remap above works in the one engine shape; a served plan must leave here
            # looking like the plans the app already reads, or the display path — which
            # iterates science's handoff as a list — silently links no items.
            "coverage_handoff": _carriers.from_engine_handoff(handoff),
            # Restored to the SUBJECT's own container too (ARV-D-060, 2026-08-06) —
            # the handoff line above did this from the start and the items did not,
            # so a served science plan lost the {…, questions: [...]} wrapper its own
            # port uses to recognise the stage. Symmetrical fix, same carrier seam.
            "assessment_items": _carriers.from_engine_items(
                items, chosen.get("assessment_container")),
            "section_coverage_note": coverage_note,
            "dropped_units": dropped_units or None,
        },
        "genon": {
            # PROVENANCE — keep the eNN here in step with api.data.GENON_ENGINE_VERSION.
            # These are two different strings for the same fact: this one is stamped INTO
            # every served plan, that one keys the FILENAME. They drifted at e14 (the
            # filename said e14 while the plan inside still claimed e13), which is
            # invisible until someone diffs an e13 file against its e14 twin — the
            # tracker's amber rule reads provenance, so a stale string here reads as
            # "no engine change" on a plan that is one.
            "engine": ("serve v2.2 / e15 (canonical library, next-highest selection, "
                       "X-1+1 slot fill by the first-exposure choice set §0.4, "
                       "proportional duration scaling, unit-anchored assessment; "
                       "e13: an item whose unit is not in the plan is not in the plan, "
                       "and a dropped unit's questions ride with it; "
                       "e14: SELF-PREFERENCE — the chosen plan's own candidate wins "
                       "every tie in the Xth-unit choice set; "
                       "e15: Case 1b EXACT-FIT COMPLETE RESCUE — rather than drop, "
                       "serve the canonical whose full count is X-1 complete plus the "
                       "standard's synthesis, when one exists; "
                       "e16: a borrowed unit's COVERAGE ROW travels with it, so the LO "
                       "its questions test is in the plan that asks them — and the "
                       "display reads the platform's anchor stamp instead of "
                       "re-deriving it through a plan-local key; "
                       "e17: PLAN GRANULARITY — a stage whose plugin declares it "
                       "(science·middle, whose units belong to an uncuttable cognitive "
                       "arc) is served by whole-canonical selection: identity at X=K, "
                       "K complete + the top's synthesis at X=K+1, truncation with "
                       "declared drops only below the lowest canonical, surrender only "
                       "above the top)"),
            "serve_granularity": granularity,
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
                # PLAN granularity (e17): distinguishes the legal below-floor truncation
                # from the unit engine's defensive Case-3 one, and carries how many
                # sittings it cost — certify's sweep and the human gate both read it.
                "below_floor": bool(fill.get("below_floor")),
                "dropped_unit_count": len(fill.get("drop_units") or []),
                "reference_count": fill.get("reference_count"),
                "withheld_units": fill.get("withheld_units") or [],
                # e15 provenance: the richer canonical the upward rule had selected
                # before Case 1b took a complete base instead. None on every other
                # path, so its presence IS the record that the rescue fired.
                "rescued_from": rescued_from,
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
