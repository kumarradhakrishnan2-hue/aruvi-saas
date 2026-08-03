"""aruvi_core.genon — the gen-on-gen adaptation engine.

VARIANT-SERVE ARCHITECTURE (v2.0 2026-08-03 — docs/variant_canonical_architecture.md §0).
A chapter is authored as a LIBRARY of canonicals — the same section list planned
FREE at counts spaced by equal dispersion over [floor, standard], each a complete
plan + its own assessment, all at the class-standard duration; the standard alone
closes with the mandated whole-chapter `synthesis` unit. A teacher's duration
matrix is served by deterministic SELECTION:

    canonicals ── compile (STRICT declared-only) ──▶ streams
    streams + duration matrix ── serve (next-highest, X-1+1, the first-exposure
                                        choice set §0.4, proportional scaling)
                                        ──▶ teacher plan

There is NO LLM in the request path, and no algorithmic composition either: every
sitting is one authored unit-arc; slot X borrows the unit that FIRST deals the
next-due section (Case 1: the standard's synthesis; Case 3: honest truncation);
minutes scale in proportion to the sitting's duration and nothing else.

The old partition engine (DP boundary choice, CUT_COST, three-regime compression,
role/unit handoffs, seam text) is RETIRED — moved to _to_delete/ with polish.py,
joined 2026-08-03 by variant_solver.py (the σ/closing-span reverse deduction,
retired with the mandate it existed to place — ARV-D-025). Failure modes are
recorded in the architecture doc; do not reintroduce them.
"""
from .compile import GenonDeclarationError, compile_stream
from .serve import ServeError, order_durations, parse_matrix, serve_plan

__all__ = [
    "GenonDeclarationError", "compile_stream",
    "ServeError", "order_durations", "parse_matrix", "serve_plan",
]
