"""aruvi_core.genon — the gen-on-gen adaptation engine (step 6, 2026-07-25).

One certified canonical LP+assessment per chapter (authored at the class-standard
duration), adapted to any teacher duration matrix by deterministic code:

    canonical plan  ── compile (v0.3, STRICT declared-only) ──▶  phase stream
    phase stream + duration matrix ── partition (three-regime) ──▶ teacher plan
    optional seam polish (tier-1 LLM, container text only)

Lifted from the genon/ lab (compile_stream.py v0.2, partition.py v0.3,
polish_seams.py) with one doctrine change: the compiler REFUSES plans without
declared band_id/role/band_refs/phase_ref (no inference in the product engine —
founder decision 2026-07-25, no back-support for pre-v1.1 plans).
"""
from .compile import GenonDeclarationError, compile_stream
from .partition import build_plan, parse_matrix
from .polish import build_polish_request, apply_polish

__all__ = [
    "GenonDeclarationError", "compile_stream",
    "build_plan", "parse_matrix",
    "build_polish_request", "apply_polish",
]
