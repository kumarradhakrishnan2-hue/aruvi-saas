"""Aruvi phase-stream compiler — v0.3, STRICT declared-only.

A pure REWRITER: canonical plan JSON -> phase stream. Writes no content — every
string is copied verbatim; it only re-addresses content (phase IDs, roles,
durations, unit table as the reference partition, assessment phase_refs).
Subject-agnostic: never branches on subject.

v0.3 doctrine (2026-07-25): declarations are REQUIRED. Every time band must
carry band_id + role, every competency edge band_refs, every assessment item
phase_ref — as the v1.1+ LP / v1.2+ assessment constitutions mandate. A plan
missing any declaration raises GenonDeclarationError listing every violation.
The lab compiler's inference path (v0.2) is deliberately NOT ported: no
heuristic code in the product engine, no back-support for pre-v1.1 plans.
"""
from __future__ import annotations

import json

VALID_ROLES = {"hook", "development", "consolidation"}


class GenonDeclarationError(ValueError):
    """The canonical plan lacks v1.1 declarations; it cannot feed the strict compiler."""

    def __init__(self, problems):
        self.problems = list(problems)
        super().__init__(
            "canonical plan is not v1.1-declared (%d problem%s): %s"
            % (len(self.problems), "s" if len(self.problems) != 1 else "",
               "; ".join(self.problems[:8]) + ("; …" if len(self.problems) > 8 else ""))
        )


def _parse_band(s):
    a, b = str(s).replace("–", "-").split("-")
    return int(a), int(b)


def _check_declarations(periods, items):
    problems = []
    for p in periods:
        n = p.get("period_number")
        for i, tb in enumerate(p.get("time_bands") or []):
            if not tb.get("band_id"):
                problems.append(f"P{n} band {i+1}: missing band_id")
            if tb.get("role") not in VALID_ROLES:
                problems.append(f"P{n} band {i+1}: role {tb.get('role')!r}")
        band_ids = {tb.get("band_id") for tb in p.get("time_bands") or []}
        for e in p.get("competency_edges") or []:
            refs = e.get("band_refs")
            if not refs:
                problems.append(f"P{n} edge {e.get('c_code')}: missing band_refs")
            elif not set(refs) <= band_ids:
                problems.append(f"P{n} edge {e.get('c_code')}: band_refs outside unit")
    for it in items:
        if isinstance(it, dict) and not it.get("phase_ref"):
            problems.append(f"assessment item {it.get('id', '?')}: missing phase_ref")
    return problems


def compile_stream(plan: dict) -> dict:
    """Canonical plan JSON -> phase stream (strict). Raises GenonDeclarationError."""
    result = plan.get("result", plan)
    periods = result["lesson_plan"]["periods"]
    items_in = result.get("assessment_items", []) or []

    problems = _check_declarations(periods, items_in)
    if problems:
        raise GenonDeclarationError(problems)

    phases, units = [], []
    seq = 0
    for p in periods:
        unum = p["period_number"]
        unit_phase_ids = []
        for tb in p["time_bands"]:
            a, z = _parse_band(tb["minutes"])
            phases.append({
                "phase_id": tb["band_id"],
                "seq": seq,
                "minutes": z - a,
                "role": tb["role"],
                "activity": tb["activity"],
                "unit": unum,
            })
            unit_phase_ids.append(tb["band_id"])
            seq += 1
        units.append({
            "unit": unum,
            "activity_title": p["activity_title"],
            "section_anchor": p["section_anchor"],
            "section_context": p.get("section_context"),
            "materials": p.get("materials") or [],
            "visual_aids": p.get("visual_aids"),
            "pedagogical_approaches": p.get("pedagogical_approaches") or [],
            "teacher_notes": p.get("teacher_notes", ""),
            "homework": p.get("homework") or [],
            "competency_edges": [dict(e) for e in p.get("competency_edges") or []],
            "phase_ids": unit_phase_ids,
            "authored_duration_minutes": p["period_duration_minutes"],
        })

    items = [json.loads(json.dumps(it)) for it in items_in]

    stream = {
        "stream_format": "aruvi-phase-stream v0.3 (declared-only)",
        "meta": {
            "subject": plan.get("subject"), "grade": plan.get("grade"),
            "chapter_number": plan.get("chapter_number"),
            "chapter_title": plan.get("chapter_title"),
            "source_file": plan.get("filename"),
            "role_provenance": "declared",
            "authored_matrix": plan.get("period_rows_snapshot")
                or plan.get("period_schedule")
                or (result.get("period_schedule") if isinstance(result, dict) else None),
        },
        "phases": phases,
        "units": units,                      # the reference partition
        "coverage_handoff": result.get("coverage_handoff", {}),
        "assessment_items": items,
    }

    # ---- content-inventory audit: the rewriter must add nothing, drop nothing ----
    src_inv = sorted(tb["activity"] for p in periods for tb in p["time_bands"])
    out_inv = sorted(ph["activity"] for ph in phases)
    assert src_inv == out_inv, "INVENTORY VIOLATION: activity text changed in compile"
    src_notes = sorted(p.get("teacher_notes", "") for p in periods)
    out_notes = sorted(u["teacher_notes"] for u in units)
    assert src_notes == out_notes, "INVENTORY VIOLATION: teacher notes changed in compile"
    return stream
