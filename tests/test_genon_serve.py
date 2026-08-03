"""Serve engine v2.0 / e12 — selection, the Xth-unit choice set (§0.4), scaling, edges.

Synthetic canonical library over a 12-section chapter (equal-dispersion counts):
  * A — the STANDARD, 13 units: one section per unit + the mandated closing
        `synthesis` unit (reserved token, §0.3);
  * B — 11 units: coverage completes at U8 (whose unit condenses the last two
        sections); U9–U11 are backward revisit sittings (frontier arithmetic);
  * C — 8 units (the floor): condensed pairs.
Stdlib only; run directly: python3 tests/test_genon_serve.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aruvi_core.genon.serve import (   # noqa: E402
    ServeError, choose_variant, fill_slot, first_dealing_unit, is_synthesis_unit,
    order_durations, section_registry, serve_plan, synthesis_unit_of, _norm,
)

SECTIONS = ["Sec %02d" % i for i in range(1, 13)]


def _mk_stream(ranges, tag):
    """A synthetic compiled stream: `ranges` entries are (lo, hi) section index
    pairs — or the string "synthesis" for the standard's reserved closer."""
    units, phases = [], []
    for n, r in enumerate(ranges, 1):
        anchor = "synthesis" if r == "synthesis" else " / ".join(SECTIONS[r[0]:r[1] + 1])
        pids = ["P%d.%d" % (n, k) for k in (1, 2, 3)]
        for k, pid in enumerate(pids):
            phases.append({"phase_id": pid, "seq": len(phases),
                           "minutes": [10, 25, 15][k], "role": None,
                           "activity": "%s unit %d band %d" % (tag, n, k + 1),
                           "unit": n})
        units.append({
            "unit": n, "activity_title": "%s U%d" % (tag, n),
            "section_anchor": anchor, "section_context": "ctx",
            "materials": [], "visual_aids": None, "pedagogical_approaches": [],
            "teacher_notes": "%s U%d notes" % (tag, n), "homework": [],
            "competency_edges": [{"c_code": "C1", "band_refs": [pids[1]]}],
            "phase_ids": pids, "authored_duration_minutes": 50,
        })
    return {
        "meta": {"subject": "social_sciences", "grade": "ix",
                 "chapter_number": 3, "chapter_title": "T", "source_file": tag},
        "phases": phases, "units": units, "coverage_handoff": {},
        "assessment_items": [
            {"id": "%s-i%d" % (tag, n), "unit_ref": [n], "period_ref": [n]}
            for n, u in enumerate(units, 1)
        ],
    }


A = _mk_stream([(i, i) for i in range(12)] + ["synthesis"], "A")           # 13
B = _mk_stream([(0, 0), (1, 1), (2, 2), (3, 3), (4, 5), (6, 7), (8, 9),
                (10, 11), (3, 3), (0, 0), (5, 5)], "B")                    # 11
C = _mk_stream([(0, 1), (2, 3), (4, 4), (5, 5), (6, 7), (8, 9),
                (10, 10), (11, 11)], "C")                                  # 8
LIB = [A, B, C]
RIDX = {_norm(a): i for i, a in enumerate(SECTIONS)}


def periods(plan):
    return plan["result"]["lesson_plan"]["periods"]


# ── the synthesis token: registry exclusion + detection ──────────────────────
assert section_registry(A) == SECTIONS, "the reserved token never enters the registry"
assert is_synthesis_unit(A["units"][-1]) and not is_synthesis_unit(A["units"][0])
s, u = synthesis_unit_of(LIB)
assert s is A and u["unit"] == 13, "the standard's closer is the library's synthesis"

# ── selection (unchanged): next-highest, full richness ───────────────────────
chosen, surr = choose_variant(LIB, 13)
assert chosen is A and surr == 0
chosen, surr = choose_variant(LIB, 15)
assert chosen is A and surr == 2, "surrender only above the top"
chosen, surr = choose_variant(LIB, 12)
assert chosen is A and surr == 0, "next-highest, full richness"
chosen, surr = choose_variant(LIB, 9)
assert chosen is B, "9 is served by the 11-canonical, never the 8"
chosen, surr = choose_variant(LIB, 5)
assert chosen is C, "below the smallest, the smallest serves"

# ── exact canonical hit: whole plan verbatim, synthesis served as authored ───
p = serve_plan(LIB, [(50, 13)])
assert p["genon"]["variant_used"] == 13 and p["genon"]["slot_fill"] is None
assert periods(p)[-1]["activity_title"] == "A U13"
assert periods(p)[-1]["section_anchor"] == "synthesis"
assert p["result"]["section_coverage_note"] is None

# ── Case 2 / single, self fill — A at 12: M = Sec 12, A's own U12 wins the tie
#    (no re-cross, same reach, densest at equal distance) ─────────────────────
p = serve_plan(LIB, [(50, 12)])
g = p["genon"]["slot_fill"]
assert g["mode"] == "fill" and g["fill_class"] == "single" and g["self_fill"], g
assert g["first_section"] == "Sec 12" and g["uncovered_sections"] == []
assert periods(p)[11]["activity_title"] == "A U12"
assert p["result"]["section_coverage_note"] is None, "complete fill discloses nothing"
assert p["result"]["dropped_units"] is None

# ── Case 1 — B at 10: prefix U1..U9 covers all 12 sections (U9 is a revisit),
#    so slot 10 borrows the STANDARD's synthesis unit ────────────────────────
p = serve_plan(LIB, [(50, 10)])
g = p["genon"]["slot_fill"]
assert g["mode"] == "synthesis" and g["borrowed_from"] == 13, g
assert periods(p)[9]["activity_title"] == "A U13", "the mandated synthesis is the borrow"
assert "draws the chapter together" in p["result"]["section_coverage_note"]
assert p["result"]["dropped_units"] is None, "nothing lost — only revisits withheld"

# ── Case 2 / forward — C at 7: M = Sec 11; B's U8 condenses Sec 11+12 and
#    outreaches every single-section candidate ───────────────────────────────
p = serve_plan(LIB, [(50, 7)])
g = p["genon"]["slot_fill"]
assert g["mode"] == "fill" and g["fill_class"] == "forward", g
assert g["borrowed_from"] == 11 and not g["self_fill"]
assert periods(p)[6]["activity_title"] == "B U8"
assert g["uncovered_sections"] == [], "forward reach completes the chapter"
assert p["result"]["section_coverage_note"] is None

# ── Case 2 with dropped sections — C at 6: M = Sec 09; C's own U6 (Sec 09+10)
#    wins (count closest to X); Sec 11+12 drop, SOURCED FROM THE LENDER (C) ──
p = serve_plan(LIB, [(50, 6)])
g = p["genon"]["slot_fill"]
assert g["mode"] == "fill" and g["fill_class"] == "forward" and g["self_fill"], g
assert g["uncovered_sections"] == ["Sec 11", "Sec 12"]
assert "could not be scheduled" in p["result"]["section_coverage_note"]
du = p["result"]["dropped_units"]
assert du and [q["activity_title"] for q in du] == ["C U7", "C U8"], \
    "drops ride from the lending plan's subsequent units"
assert all(q["unscheduled"] for q in du)

# ── Case 2 / backward — no forward or single candidate exists for M:
#    the L+M unit is borrowed, the re-cross named as runway ──────────────────
REG4 = ["Sec %02d" % i for i in range(1, 5)]
R4 = {_norm(a): i for i, a in enumerate(REG4)}
T1 = _mk_stream([(0, 0), (1, 1), (1, 2), (3, 3)], "T1")
T2 = _mk_stream([(0, 0), (1, 2), (3, 3)], "T2")
f = fill_slot([T1, T2], T1, 3, REG4)
assert f["mode"] == "fill" and f["fill_class"] == "backward", f
assert f["stream"] is T2, "count closest to X breaks the backward tie"
assert f["overlap_sections"] == ["Sec 02"]

# ── first_dealing_unit: a stream that SKIPS m yields no candidate ────────────
GAP = _mk_stream([(0, 0), (2, 2)], "G")
assert first_dealing_unit(GAP, R4, 1) is None, "skipping is not first exposure"

# ── Case 3 — defensive truncation: empty choice set, no drops, the message
#    asks for the reference canonical's count ────────────────────────────────
f = fill_slot([GAP], GAP, 2, REG4[:3])
assert f["mode"] == "truncation" and f["reference_count"] == 2, f
assert f["uncovered_sections"] == [], "Case 3 shows no dropped sections"

# ── surrender above the top ──────────────────────────────────────────────────
p = serve_plan(LIB, [(50, 15)])
assert p["genon"]["sittings"] == 13 and p["genon"]["surrendered_periods"] == 2
assert "return to your budget" in p["genon"]["surrender_note"]
assert "return to your budget" in p["result"]["section_coverage_note"]
assert p["result"]["dropped_units"] is None, "surrender loses nothing"

# ── proportional scaling: tiling exact at 40 and 60, dispersion kept ─────────
p = serve_plan(LIB, [(40, 6), (60, 3)])
for q in periods(p):
    lo = 0
    for b in q["time_bands"]:
        a, z = (int(x) for x in b["minutes"].split("-"))
        assert a == lo
        lo = z
    assert lo == q["period_duration_minutes"]
seq = p["genon"]["duration_sequence"]
assert seq[0] == 40 and 60 not in (seq[0], seq[-1]), "long sittings interior"
assert order_durations([(50, 14), (60, 4)])[:9] == [50, 50, 60, 50, 50, 50, 60, 50, 50]

# ── assessment remap: prefix items live, withheld items noted, the borrowed
#    synthesis brings ITS OWN item from the standard ─────────────────────────
p = serve_plan(LIB, [(50, 10)])          # B prefix + A's synthesis
items = p["result"]["assessment_items"]
by_id = {i["id"]: i for i in items}
assert by_id["B-i9"]["period_ref"] == [9]
assert by_id["B-i10"]["scheduling_note"], "unserved B-unit item carries the note"
assert by_id["A-i13"]["period_ref"] == [10], "the synthesis brings its own item"
assert "A-i12" not in by_id, "only the borrowed unit's items travel"

# a SELF fill adds no foreign items and keeps its own anchored normally
p = serve_plan(LIB, [(50, 6)])
by_id = {i["id"]: i for i in p["result"]["assessment_items"]}
assert by_id["C-i6"]["period_ref"] == [6]
assert all(not k.startswith(("A-", "B-")) for k in by_id), "no foreign items on self fill"

# ── edges pass through verbatim ──────────────────────────────────────────────
p = serve_plan(LIB, [(50, 10)])
for e in periods(p)[9]["competency_edges"]:
    assert e["band_refs"], "edges are untouched passthrough"

# ── legacy library (no synthesis token): Case 1 falls back to the nearest
#    companion's closing unit; single library truncates synthesis-only ───────
L1 = _mk_stream([(i, i) for i in range(9)] + [(5, 5), (3, 3), (0, 0)], "S")   # 12u/9s
L2 = _mk_stream([(0, 0), (1, 1), (2, 2), (3, 4), (5, 6), (7, 7), (8, 8)], "D")
p = serve_plan([L1, L2], [(50, 11)])
g = p["genon"]["slot_fill"]
assert g["mode"] == "synthesis" and g["borrowed_from"] == 7, g
p = serve_plan([L1], [(50, 11)])
g = p["genon"]["slot_fill"]
assert g["mode"] == "truncation" and g["synthesis_only"], g
assert "synthesis" in p["result"]["section_coverage_note"]

# ── guards ───────────────────────────────────────────────────────────────────
try:
    serve_plan([], [(50, 5)])
    raise AssertionError("empty library must raise")
except ServeError:
    pass

print("test_genon_serve: all e12 assertions passed")
