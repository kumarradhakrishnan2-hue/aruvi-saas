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


def briefs_for(subject, klass, chapter):
    """{compact_count: brief_text} for the chapter, filled from the master-plan
    row and the AUTHORED top canonical's registry. Raises SystemExit with a
    plain message when the top canonical is missing or the row is provisional."""
    mp = json.load(open(MP))
    key = f"{subject}|{klass}"
    combo = mp["combos"][key]
    row = next(c for c in combo["chapters"] if c["chapter"] == int(chapter))
    vp = row.get("variant_plan")
    if not vp or vp.get("provisional"):
        raise SystemExit("Row is provisional — author and certify the top canonical, "
                         "run this script's annotate pass, then ask again.")
    p = os.path.join(SAVED, subject, GRADE_KEY.get(klass, klass.lower()),
                     f"ch_{int(chapter):02d}_canonical.json")
    if not os.path.isfile(p):
        raise SystemExit(f"No top canonical on disk ({p}) — author it first; if the "
                         "row says finalized it is stale: re-run the annotate pass.")
    reg = section_registry(compile_stream(json.load(open(p))))
    dur = combo["standard_duration_minutes"]
    out = {}
    for k in vp["counts"][1:]:
        span = vp["closing_spans"][str(k)]
        tail = reg[-span:]
        lines = [
            f"VARIANT BRIEF — {k} periods (platform-computed; binding)",
            "",
            f"- This is a COMPLETE, self-sufficient lesson plan for the whole "
            f"chapter at {k} periods x {dur} minutes (period_schedule: exactly "
            f"one row {{{dur}, {k}}}). It is NOT a compression, summary, or "
            f"edit of any other plan of this chapter — author it from the "
            f"chapter summary as if it were the only plan.",
            "- SECTION REGISTRY (verbatim; the chapter's ordered sections):",
        ]
        lines += [f"    {i}. {a}" for i, a in enumerate(reg, 1)]
        lines += [
            "  Every unit's section_anchor MUST be drawn verbatim from this "
            "list (a multi-section unit joins its sections with \" / \" in "
            "list order). Sections must FIRST APPEAR in registry order; a "
            "later unit may revisit earlier sections for synthesis.",
            f"- COVERAGE IS TOTAL: all {len(reg)} registry sections must appear "
            f"in this plan. With the closing mandate consuming the last "
            f"{span}, the remaining {len(reg) - span} sections must ALL "
            f"first-appear across the earlier units — merge ADJACENT sections "
            f"into shared units wherever the count demands it. NO section may "
            f"be omitted, and section_coverage_note is NOT available to a "
            f"variant: this period count was solver-chosen to fit the chapter, "
            f"so a coverage gap is an authoring failure, never a budget note.",
            f"- CLOSING MANDATE: the final unit is the chapter's closing "
            f"synthesis and its section_anchor lists exactly the last "
            f"{span} registry section(s): " + " / ".join(tail) + ". The "
            "synthesis may draw on the whole chapter; its anchor names exactly "
            "these. If a coherent closing arc cannot be built at this span, "
            "SAY SO at the end of the run instead of complying badly.",
            "- The assessment for this variant is generated from THIS plan's "
            "coverage_handoff in the normal way; it references no other "
            "variant of this chapter.",
            f"- Save as: ch_{int(chapter):02d}_canonical_p{k:02d}.json",
        ]
        out[k] = "\n".join(lines) + "\n"
    return out, vp


def print_briefs(subject, klass, chapter):
    """`python3 genon/variant_plans.py brief <subject> <CLASS> <ch>`."""
    briefs, vp = briefs_for(subject, klass, chapter)
    print(f"# Variant briefs · {subject} {klass} ch {chapter} · "
          f"library {vp['counts']} · sigma {vp['sigma']}\n")
    for k, text in briefs.items():
        print("=" * 72)
        print(text)


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
    if len(sys.argv) > 1 and sys.argv[1] == "brief":
        print_briefs(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        main()
