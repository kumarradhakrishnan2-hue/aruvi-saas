"""Genon: annotate master_plan.json with a per-chapter VARIANT PLAN — v1.0 (2026-07-31).

Industrial-scale reverse deduction (docs/variant_canonical_architecture.md §5): for every
chapter row (which already carries standard_duration, recommended_periods, and
floor_periods_at_standard), compute the variant set to author — counts + mandated closing
spans — and write it back into the SAME file, so the authoring pipeline and the API read
one registry of record.

Two-pass honesty:
  * provisional=True  — no top canonical exists yet; the top is MODELED as one section
    per unit. Counts are dependable (they come from recommended/floor); the closing spans
    and coverage projection may shift when the real registry lands.
  * provisional=False — the chapter's ch_NN_canonical.json exists; the solve runs on its
    REAL unit ranges (frontier arithmetic) and the row records the registry size.

Re-run after any canonical is authored/regenerated, floor policy change, or sigma change:
    python3 genon/variant_plans.py
Writes data/content/allocation_norms/master_plan.json in place (idempotent).
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from aruvi_core.genon import compile_stream                      # noqa: E402
from aruvi_core.genon.serve import (                             # noqa: E402
    _norm, section_registry, unit_range,
)
from aruvi_core.genon.variant_solver import (                    # noqa: E402
    _even_ranges, demand_weights, outcome_for, solve,
)

MP = os.path.join(ROOT, "data/content/allocation_norms/master_plan.json")
SAVED = os.path.join(ROOT, "data/content/saved_plans")

# sigma per subject·stage: the widest closing synthesis a compact variant may be
# mandated to anchor. Evidence so far: SS·secondary solves fully at 2 (ch 3 + ch 5,
# 2026-07-31). Others default to 2 until their stages are calibrated — edit here.
SIGMA_DEFAULT = 2
SIGMA = {
    # ("social_sciences", "secondary"): 2,
}

GRADE_KEY = {"III": "iii", "IV": "iv", "V": "v", "VI": "vi", "VII": "vii",
             "VIII": "viii", "IX": "ix", "X": "x"}
STAGE = {"III": "preparatory", "IV": "preparatory", "V": "preparatory",
         "VI": "middle", "VII": "middle", "VIII": "middle",
         "IX": "secondary", "X": "secondary"}


def real_top_ranges(subject, klass, chapter):
    p = os.path.join(SAVED, subject, GRADE_KEY.get(klass, klass.lower()),
                     f"ch_{int(chapter):02d}_canonical.json")
    if not os.path.isfile(p):
        return None, None
    s = compile_stream(json.load(open(p)))
    reg = section_registry(s)
    ridx = {_norm(a): i for i, a in enumerate(reg)}
    ranges = [unit_range(u, ridx) for u in s["units"]]
    if any(r is None for r in ranges):
        return None, None
    return ranges, len(reg)


def plan_chapter(top_ranges, m, A, C, sigma):
    """-> (counts, spans, table). Handles the small-chapter degeneracies."""
    w = demand_weights(A, max(C, 1), A)
    if C >= A or A <= 2:
        cr = {A: top_ranges}
        table = {x: outcome_for(x, cr, m) for x in range(max(C, 1), A + 1)}
        return [A], {}, table
    if A - C < 3:                       # room for the floor variant only
        best = None
        for s_c in range(1, sigma + 1):
            cr = {A: top_ranges, C: _even_ranges(m, C, s_c)}
            table = {x: outcome_for(x, cr, m) for x in range(C, A + 1)}
            score = sum(w.get(x, 1.0) * {"full": 1.0, "partial": 0.4,
                                         "truncation": 0.0}[v]
                        for x, v in table.items())
            if best is None or score > best[0]:
                best = (score, s_c, table)
        _, s_c, table = best
        return [A, C], {C: s_c}, table
    sol = solve(top_ranges, floor=C, sigma=sigma, weights=w)
    return sol["counts"], sol["closing_spans"], sol["table"]


def main():
    mp = json.load(open(MP))
    n_real = n_prov = 0
    for key, combo in mp["combos"].items():
        subject, klass = key.split("|")
        sigma = SIGMA.get((subject, STAGE.get(klass, "")), SIGMA_DEFAULT)
        for ch in combo["chapters"]:
            A = int(ch["recommended_periods"])
            C = int(ch["floor_periods_at_standard"])
            ranges, m = real_top_ranges(subject, klass, ch["chapter"])
            if ranges is None:
                ranges = [(i, i) for i in range(A)]     # modeled: 1 section/unit
                m = A
                provisional = True
                n_prov += 1
            else:
                provisional = False
                n_real += 1
            counts, spans, table = plan_chapter(ranges, m, A, C, sigma)
            full = [x for x, v in table.items() if v == "full"]
            ch["variant_plan"] = {
                "sigma": sigma,
                "counts": counts,                         # variant 1, 2, 3 …
                "closing_spans": {str(k): v for k, v in spans.items()},
                "provisional": provisional,
                "basis": "modeled" if provisional else "authored_canonical",
                "registry_sections": m,
                "full_coverage": ([min(full), max(full)] if full else None),
                "partials_at": sorted(x for x, v in table.items() if v != "full"),
            }
    mp["_meta"]["variant_plans"] = (
        "each chapter carries variant_plan (2026-07-31, genon/variant_plans.py): the "
        "variant counts + mandated closing-synthesis spans to author, solved from "
        "recommended/floor at the stage's sigma. provisional=true rows used a modeled "
        "top (one section per unit) — re-run this script after each top canonical "
        "certifies to finalize its row on real unit ranges.")
    json.dump(mp, open(MP, "w"), ensure_ascii=False, indent=2)
    print(f"variant plans written: {n_real} on authored canonicals, {n_prov} provisional")


if __name__ == "__main__":
    main()
