#!/usr/bin/env python3
"""Aruvi phase-stream compiler.

A pure REWRITER: saved plan JSON -> canonical phase stream. Writes no content —
every string is copied verbatim; it only re-addresses content (phase IDs, roles,
durations, unit table as the reference partition, assessment phase_refs).
Subject-agnostic: never branches on subject.

Post-v1.1 plans carry declared band_id/role/band_refs — copied through
(provenance "declared"). Pre-v1.1 plans get deterministic inference
(provenance "inferred").

Usage: python3 compile_stream.py <saved_plan.json> <out_stream.json>
"""
import json
import re
import sys


def parse_band(s):
    a, b = str(s).replace("–", "-").split("-")
    return int(a), int(b)


HOOK_PAT = re.compile(r"^(open|begin|start|ask students|recall|pose)", re.I)
CONS_PAT = re.compile(r"(consolidat|conclude|wrap|synthes|summar|close by|exit slip|"
                      r"students write .{0,40}(note|paragraph|sentence)s?\b)", re.I)


def infer_role(idx, n_bands, activity):
    if idx == 0:
        return "hook"
    if idx == n_bands - 1:
        return "consolidation" if not HOOK_PAT.match(activity) else "development"
    return "consolidation" if CONS_PAT.search(activity) and idx == n_bands - 2 else "development"


def compile_stream(plan):
    result = plan.get("result", plan)
    periods = result["lesson_plan"]["periods"]

    phases, units = [], []
    seq = 0
    declared = all("role" in tb and "band_id" in tb
                   for p in periods for tb in p["time_bands"])
    for p in periods:
        unum = p["period_number"]
        n = len(p["time_bands"])
        unit_phase_ids = []
        for i, tb in enumerate(p["time_bands"]):
            a, z = parse_band(tb["minutes"])
            pid = tb.get("band_id") or f"P{unum}.{i+1}"
            role = tb.get("role") or infer_role(i, n, tb["activity"])
            phases.append({
                "phase_id": pid,
                "seq": seq,
                "minutes": z - a,
                "role": role,
                "activity": tb["activity"],
                "unit": unum,
            })
            unit_phase_ids.append(pid)
            seq += 1
        edges = []
        for e in p.get("competency_edges") or []:
            e2 = dict(e)
            if not e2.get("band_refs"):
                e2["band_refs"] = list(unit_phase_ids)   # coarse pre-v1.1 inference
                e2["band_refs_provenance"] = "inferred"
            edges.append(e2)
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
            "competency_edges": edges,
            "phase_ids": unit_phase_ids,
            "authored_duration_minutes": p["period_duration_minutes"],
        })

    # assessment: attach phase_refs (declared passthrough, else inferred via edge match)
    edge_by_lo = {}
    for u in units:
        for e in u["competency_edges"]:
            edge_by_lo[(e.get("c_code"), e.get("implied_lo"))] = (u["unit"], e["band_refs"])
    items = []
    inferred_items = 0
    for it in result.get("assessment_items", []):
        it2 = json.loads(json.dumps(it))
        if not it2.get("phase_ref"):
            key = ((it2.get("competency") or {}).get("c_code"), it2.get("implied_lo"))
            hit = edge_by_lo.get(key)
            if hit is None:  # fall back to the anchor unit's phases
                refs = it2.get("period_ref") or []
                u = int(refs[0]) if refs else units[0]["unit"]
                hit = (u, next(x["phase_ids"] for x in units if x["unit"] == u))
            it2["phase_ref"] = list(hit[1])
            it2["phase_ref_provenance"] = "inferred"
            inferred_items += 1
        items.append(it2)

    stream = {
        "stream_format": "aruvi-phase-stream v0.2",
        "meta": {
            "subject": plan.get("subject"), "grade": plan.get("grade"),
            "chapter_number": plan.get("chapter_number"),
            "chapter_title": plan.get("chapter_title"),
            "source_file": plan.get("filename"),
            "role_provenance": "declared" if declared else "inferred",
            "authored_matrix": plan.get("period_rows_snapshot"),
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


if __name__ == "__main__":
    plan = json.load(open(sys.argv[1]))
    stream = compile_stream(plan)
    json.dump(stream, open(sys.argv[2], "w"), ensure_ascii=False, indent=2)
    ph = stream["phases"]
    from collections import Counter
    print(f"OK  {len(ph)} phases across {len(stream['units'])} units "
          f"({sum(p['minutes'] for p in ph)} min total)")
    print("    roles:", dict(Counter(p["role"] for p in ph)),
          "| provenance:", stream["meta"]["role_provenance"])
    inf = sum(1 for it in stream["assessment_items"] if it.get("phase_ref_provenance"))
    print(f"    assessment items: {len(stream['assessment_items'])} "
          f"({inf} phase_refs inferred)")
    print("    inventory audit: PASSED (verbatim content)")
