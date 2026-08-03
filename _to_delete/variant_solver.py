"""Reverse deduction of variant spacing — v1.0 (2026-07-31).

Given the TOP canonical (authored first, fixing the chapter's section list), solve
for the compact variants' period counts and their MANDATED CLOSING SPANS before
those variants are authored — so the fill ladder's candidates exist by construction,
not by luck (docs/variant_canonical_architecture.md §5).

Model. Sections m come from the top canonical's registry. A compact variant with
count B partitions the same m sections into B contiguous units; its closing unit is
mandated to span s_B sections (s_B <= sigma, the largest closing consolidation the
founder will defend pedagogically). For a teacher request X served by variant Y, the
missing span is the sections of Y's units X..Y; the request gets FULL coverage iff
X hits a variant exactly, or some OTHER variant's closing span covers that missing
span (exact or superset). Outcomes are scored over the demand range [floor, top],
optionally weighted (e.g. by distance from master_plan's recommended_periods).

Approximations, stated: unauthored variants are modelled as even partitions of m
with the mandated closing span; the top variant uses its REAL unit ranges. The
adaptation table this emits is a projection — certification re-derives it from the
authored variants and diffs the two.
"""
from __future__ import annotations


def _even_ranges(m, count, closing_span):
    """Model a compact variant: contiguous, non-decreasing unit ranges over m
    sections, closing unit spanning closing_span, the body as even as the
    arithmetic allows. When the body has more units than sections (the top
    canonical itself does this — 12 units over 9 sections), sections are SHARED:
    several consecutive units sit on one section, exactly as Rule 4 permits."""
    closing_span = max(1, min(closing_span, m))
    n = count - 1
    if n <= 0:
        return [(0, m - 1)]
    body = m - closing_span
    ranges = []
    if body <= 0:
        ranges = [(0, 0)] * n                    # degenerate: floor below sense
    elif n >= body:
        base, rem = divmod(n, body)              # units share sections
        for si in range(body):
            k = base + (1 if si < rem else 0)
            ranges.extend([(si, si)] * k)
    else:
        base, rem = divmod(body, n)              # units span section runs
        lo = 0
        for i in range(n):
            w = base + (1 if i < rem else 0)
            ranges.append((lo, lo + w - 1))
            lo += w
    ranges.append((m - closing_span, m - 1))
    return ranges


def demand_weights(recommended, floor, top, spread=2.0):
    """Gaussian demand profile over [floor, top], centred on the master-plan
    recommendation — where teacher requests will cluster."""
    import math
    return {x: math.exp(-((x - recommended) ** 2) / (2 * spread ** 2))
            for x in range(floor, top + 1)}


def outcome_for(x, counts_ranges, m):
    """Serve outcome for a request of x sittings against modelled variants.

    counts_ranges: dict count -> list of (lo, hi) unit ranges (top's are real).
    FRONTIER arithmetic (2026-07-31): the prefix's coverage is its first-visit
    frontier, so backward-anchored synthesis tails don't distort the missing
    span. Returns 'full' | 'partial' | 'truncation'."""
    counts = sorted(counts_ranges, reverse=True)
    top = counts[0]
    if x >= top or x in counts_ranges:
        return "full"                      # exact variant hit (or surrender above top)
    y = min(c for c in counts if c >= x)
    ry = counts_ranges[y]
    frontier = max((r[1] for r in ry[:x - 1]), default=-1)
    lo_missing = frontier + 1
    if lo_missing > m - 1:
        # synthesis-only tail: a companion variant's closing synthesis serves
        return "full" if len(counts) > 1 else "partial"
    closers = [counts_ranges[c][-1] for c in counts if c != y]
    closers = [r[0] for r in closers if r[1] == m - 1]   # must close the chapter
    if any(clo <= lo_missing for clo in closers):
        return "full"                      # exact or superset fill
    if closers:
        return "partial"                   # suffix fill: closure kept, gap named
    return "truncation"


def solve(top_ranges, floor, sigma, n_variants=3, weights=None):
    """Solve for the compact counts + mandated closing spans.

    top_ranges: the top canonical's real unit ranges (from serve.section arithmetic);
    floor: the smallest period count the chapter should serve coherently (lower band);
    sigma: max closing span (sections) a single consolidation sitting may be asked
    to carry; weights: optional {x: weight} over the demand range.

    Returns {counts, closing_spans, score, table} — table maps each x in
    [floor, top] to its projected outcome."""
    m = top_ranges[-1][1] + 1
    top = len(top_ranges)
    if floor >= top:
        raise ValueError("floor must be below the top count")
    w = weights or {}

    def score_set(counts, spans):
        cr = {top: top_ranges}
        for c, s in zip(counts, spans):
            cr[c] = _even_ranges(m, c, s)
        total = 0.0
        table = {}
        for x in range(floor, top + 1):
            o = outcome_for(x, cr, m)
            table[x] = o
            total += w.get(x, 1.0) * {"full": 1.0, "partial": 0.4, "truncation": 0.0}[o]
        return total, table

    best = None
    if n_variants <= 1:
        s, t = score_set([], [])
        return {"counts": [top], "closing_spans": {}, "score": round(s, 3), "table": t}
    # C is the floor (the reason the densest variant exists); search B between.
    c = floor
    for b in range(c + 1, top):
        for s_b in range(1, sigma + 1):
            for s_c in range(1, sigma + 1):
                sc, table = score_set([b, c], [s_b, s_c])
                key = (sc, -abs((top - b) - (b - c)))   # tie: even spacing
                if best is None or key > best[0]:
                    best = (key, b, s_b, s_c, sc, table)
    _, b, s_b, s_c, sc, table = best
    return {
        "counts": [top, b, c],
        "closing_spans": {b: s_b, c: s_c},
        "score": round(sc, 3),
        "table": table,
    }
