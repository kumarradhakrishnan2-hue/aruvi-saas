"""Aruvi phase-stream compiler — v0.5, STRICT declared-only.

A pure REWRITER: canonical plan JSON -> phase stream. Writes no content — every
string is copied verbatim; it only re-addresses content (band minutes, the unit
table as the served atoms, assessment anchor units).
Subject-agnostic: never branches on subject.

v0.5 doctrine (2026-07-31, second pass of the variant-serve pivot): THE BAND
LAYER IS NO LONGER A DECLARATION. band_id, band_refs and phase_ref existed so a
unit SPLIT across sittings could be re-addressed band by band; whole-unit
serving makes the unit the anchor, and the unit's period_number is already on
every assessment item (period_ref — "linkage is an identity"). So: band ids are
DERIVED positionally here ("P<unit>.<ordinal>"; a declared band_id is accepted
and used, never required); roles are optional passthrough; band_refs and
phase_ref are passthrough. The ONE remaining item requirement: every assessment
item must resolve to a known unit (period_ref, else legacy phase_ref via the
declared band ids) — normalized onto the item as unit_ref, which is what the
serve engine consumes. A plan whose items cannot be anchored raises
GenonDeclarationError listing every violation.
The lab compiler's inference path (v0.2) is deliberately NOT ported: no
heuristic code in the product engine.
"""
from __future__ import annotations

import json


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


def _anchor_items(items, band_unit, unit_numbers):
    """Normalize each item's anchor to unit_ref (a list of unit numbers).
    Source of truth: period_ref (the identity); legacy fallback: phase_ref
    mapped through the declared band ids. Returns the problem list."""
    problems = []
    for it in items:
        if not isinstance(it, dict):
            continue
        units = [u for u in (it.get("period_ref") or [])
                 if isinstance(u, int) and u in unit_numbers]
        if not units:
            units = sorted({band_unit[r] for r in (it.get("phase_ref") or [])
                            if r in band_unit})
        if not units:
            problems.append(f"assessment item {it.get('id', '?')}: "
                            "no resolvable anchor unit (period_ref/phase_ref)")
        it["unit_ref"] = units
    return problems


def compile_stream(plan: dict) -> dict:
    """Canonical plan JSON -> phase stream (strict). Raises GenonDeclarationError."""
    result = plan.get("result", plan)
    periods = result["lesson_plan"]["periods"]
    items_in = result.get("assessment_items", []) or []
    role_handoff = result.get("role_handoff") or plan.get("role_handoff") or {}

    phases, units = [], []
    seq = 0
    for p in periods:
        unum = p["period_number"]
        unit_phase_ids = []
        for i, tb in enumerate(p["time_bands"]):
            a, z = _parse_band(tb["minutes"])
            bid = tb.get("band_id") or f"P{unum}.{i + 1}"   # derived, never demanded
            phases.append({
                "phase_id": bid,
                "seq": seq,
                "minutes": z - a,
                "role": role_handoff.get(bid) or tb.get("role"),
                "activity": tb["activity"],
                "unit": unum,
            })
            unit_phase_ids.append(bid)
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
    band_unit = {ph["phase_id"]: ph["unit"] for ph in phases}
    problems = _anchor_items(items, band_unit, {u["unit"] for u in units})
    if problems:
        raise GenonDeclarationError(problems)

    stream = {
        "stream_format": "aruvi-phase-stream v0.5 (unit-anchored)",
        "meta": {
            "subject": plan.get("subject"), "grade": plan.get("grade"),
            "chapter_number": plan.get("chapter_number"),
            "chapter_title": plan.get("chapter_title"),
            "source_file": plan.get("filename"),
            "role_provenance": ("declared (role_handoff)" if role_handoff
                                else "inline-or-absent (optional since serve v1.0)"),
            "authored_matrix": plan.get("period_rows_snapshot")
                or plan.get("period_schedule")
                or (result.get("period_schedule") if isinstance(result, dict) else None),
        },
        "phases": phases,
        "units": units,                      # the served atoms: one sitting = one unit
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
