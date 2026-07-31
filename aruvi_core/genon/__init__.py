"""aruvi_core.genon — the gen-on-gen adaptation engine.

VARIANT-SERVE ARCHITECTURE (2026-07-31 — docs/variant_canonical_architecture.md).
A chapter is authored as a LIBRARY of variant canonicals (the same section list
planned at two or three period counts, each a complete plan + its own assessment,
all at the class-standard duration). A teacher's duration matrix is served by
deterministic SELECTION:

    canonical variants ── compile (v0.4, STRICT declared-only) ──▶ streams
    streams + duration matrix ── serve (next-highest, X-1+1 fill ladder,
                                        proportional scaling) ──▶ teacher plan

There is NO LLM in the request path, and no algorithmic composition either: every
sitting is one authored unit-arc; slot X is selected from the library's closing
units (exact > superset > suffix > truncation); minutes scale in proportion to
the sitting's duration and nothing else.

The old partition engine (DP boundary choice, CUT_COST, three-regime compression,
role/unit handoffs, seam text) is RETIRED — moved to _to_delete/ with polish.py.
Its failure modes are recorded in the brief; do not reintroduce them.
"""
from .compile import GenonDeclarationError, compile_stream
from .serve import ServeError, order_durations, parse_matrix, serve_plan

__all__ = [
    "GenonDeclarationError", "compile_stream",
    "ServeError", "order_durations", "parse_matrix", "serve_plan",
]
