"""Serve engine (variant library) — selection, fill ladder, scaling, edges.

Synthetic three-variant library over a 12-section chapter:
  * top variant  A=12 — one section per unit;
  * mid variant  B=9  — closing unit spans the last 2 sections;
  * dense variant C=7 — closing unit spans the last 4 sections.
Stdlib only; run directly: python3 tests/test_genon_serve.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aruvi_core.genon.serve import (   # noqa: E402
    ServeError, choose_variant, fill_slot, order_durations, section_registry,
    serve_plan,
)

SECTIONS = ["Sec %02d" % i for i in range(1, 13)]


def _mk_stream(count, ranges, tag):
    """A synthetic compiled stream: `ranges` is a list of (lo, hi) section index
    pairs, one per unit, covering 0..11 contiguously."""
    units, phases = [], []
    for n, (lo, hi) in enumerate(ranges, 1):
        anchor = " / ".join(SECTIONS[lo:hi + 1])
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
        # unit_ref is what compile v0.5 normalizes onto every item
        "assessment_items": [
            {"id": "%s-i%d" % (tag, n), "unit_ref": [n], "period_ref": [n]}
            for n, u in enumerate(units, 1)
        ],
    }


def _ranges_even(count, closing):
    body = 12 - closing
    base, rem = divmod(body, count - 1)
    out, lo = [], 0
    for i in range(count - 1):
        w = base + (1 if i < rem else 0)
        out.append((lo, lo + w - 1))
        lo += w
    out.append((lo, 11))
    return out


A = _mk_stream(12, [(i, i) for i in range(12)], "A")
B = _mk_stream(9, _ranges_even(9, 2), "B")
C = _mk_stream(7, _ranges_even(7, 4), "C")
LIB = [A, B, C]


def periods(plan):
    return plan["result"]["lesson_plan"]["periods"]


# ── registry + selection ─────────────────────────────────────────────────────
assert section_registry(A) == SECTIONS
chosen, surr = choose_variant(LIB, 12)
assert chosen is A and surr == 0
chosen, surr = choose_variant(LIB, 15)
assert chosen is A and surr == 3, "surrender only above the top variant"
chosen, surr = choose_variant(LIB, 11)
assert chosen is A and surr == 0, "next-highest, full richness"
chosen, surr = choose_variant(LIB, 8)
assert chosen is B, "8 is served by the 9-variant, never the 7"
chosen, surr = choose_variant(LIB, 5)
assert chosen is C, "below the smallest, the smallest serves"

# ── exact variant hit: whole plan verbatim, no fill, no notes ────────────────
p = serve_plan(LIB, [(50, 9)])
assert p["genon"]["variant_used"] == 9 and p["genon"]["slot_fill"] is None
assert [q["activity_title"] for q in periods(p)] == ["B U%d" % i for i in range(1, 10)]
assert p["result"]["section_coverage_note"] is None

# ── X-1+1: exact fill — A at 11: prefix A1..A10 + B's closing unit (last 2) ──
p = serve_plan(LIB, [(50, 11)])
g = p["genon"]
assert g["variant_used"] == 12 and g["slot_fill"]["mode"] == "exact"
assert g["slot_fill"]["borrowed_from"] == 9
ps = periods(p)
assert [q["activity_title"] for q in ps[:10]] == ["A U%d" % i for i in range(1, 11)]
assert ps[10]["activity_title"] == "B U9", "slot 11 is B's closing unit"
assert p["result"]["section_coverage_note"] is None, "exact fill discloses nothing"

# ── superset fill — A at 10: missing 3, B's closer spans 2 (suffix), C's 4 ──
p = serve_plan(LIB, [(50, 10)])
g = p["genon"]["slot_fill"]
assert g["mode"] == "superset" and g["borrowed_from"] == 7
assert g["overlap_sections"] == ["Sec 09"], g
assert "re-crosses" in p["result"]["section_coverage_note"]

# ── suffix fill — B at 6: missing B-units 6..9, no closer reaches back ──────
p = serve_plan([A, B], [(50, 8)])
g = p["genon"]["slot_fill"]
assert g["mode"] in ("suffix",), g
assert g["borrowed_from"] == 12, "A's one-section closer is the only candidate"
assert g["uncovered_sections"], "the gap is named"
assert "could not be scheduled" in p["result"]["section_coverage_note"]

# ── truncation — single-variant library, the founder's 11-vs-12 ruling ──────
p = serve_plan([A], [(50, 11)])
g = p["genon"]["slot_fill"]
assert g["mode"] == "truncation" and g["withheld_units"] == [12]
ps = periods(p)
assert ps[10]["activity_title"] == "A U11", "no skip inside the chosen plan"
assert "could not be scheduled" in p["result"]["section_coverage_note"]

# ── surrender above the top ──────────────────────────────────────────────────
p = serve_plan(LIB, [(50, 14)])
assert p["genon"]["sittings"] == 12 and p["genon"]["surrendered_periods"] == 2
assert "return to your budget" in p["genon"]["surrender_note"]

# ── proportional scaling: tiling exact at 40 and 60, bands keep proportion ──
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

# ── assessment remap: unit-anchored — prefix items live, withheld items noted,
#    the borrowed fill unit brings its own items from its home variant ─────────
p = serve_plan(LIB, [(50, 11)])
items = p["result"]["assessment_items"]
by_id = {i["id"]: i for i in items}
assert by_id["A-i10"]["period_ref"] == [10]
assert by_id["A-i11"]["scheduling_note"], "unserved A-unit item carries the note"
assert by_id["B-i9"]["period_ref"] == [11], "borrowed unit brings its own items"
assert "B-i8" not in by_id, "only the borrowed unit's items travel"

# ── edges pass through verbatim (band layer is internal since compile v0.5) ──
ps = periods(p)
for e in ps[10]["competency_edges"]:
    assert e["band_refs"], "edges are untouched passthrough"

# ── weekly dispersion retained ───────────────────────────────────────────────
assert order_durations([(50, 14), (60, 4)])[:9] == [50, 50, 60, 50, 50, 50, 60, 50, 50]

# ── guards ───────────────────────────────────────────────────────────────────
try:
    serve_plan([], [(50, 5)])
    raise AssertionError("empty library must raise")
except ServeError:
    pass

print("test_genon_serve: all assertions passed")

# ── frontier arithmetic: synthesis tails (founder ruling, 2026-07-31) ────────
# a 12-unit top over 9 sections whose last three units are backward-anchored
# synthesis sittings, plus a 7-unit companion over the SAME registry
SYN = _mk_stream(12, [(i, i) for i in range(9)] + [(5, 5), (3, 3), (0, 0)], "S")
D = _mk_stream(7, [(0, 0), (1, 1), (2, 2), (3, 4), (5, 6), (7, 7), (8, 8)], "D")

p = serve_plan([SYN], [(50, 11)])
g = p["genon"]["slot_fill"]
assert g["mode"] == "truncation" and g["uncovered_sections"] == [], g
assert "synthesis" in p["result"]["section_coverage_note"], "coverage complete, synthesis named"

p = serve_plan([SYN, D], [(50, 11)])
g = p["genon"]["slot_fill"]
assert g["mode"] == "synthesis" and g["borrowed_from"] == 7, g
assert periods(p)[10]["activity_title"] == "D U7", "borrowed closing synthesis in slot 11"
assert "closing synthesis" in p["result"]["section_coverage_note"]

# X=9 against SYN alone: unit 9 completes coverage, withheld 10-12 are synthesis
p = serve_plan([SYN], [(50, 9)])
g = p["genon"]["slot_fill"]
assert g["mode"] == "truncation" and g["synthesis_only"] and g["uncovered_sections"] == [], g
assert "synthesis" in p["result"]["section_coverage_note"]

# X=8 against SYN alone: real coverage gap — Sec 09 unreached, named
p = serve_plan([SYN], [(50, 8)])
g = p["genon"]["slot_fill"]
assert g["mode"] == "truncation" and g["uncovered_sections"] == ["Sec 09"], g

print("frontier/synthesis assertions passed")

# ── dropped units (founder, 2026-08-01): below-floor plans carry unreached units ──
p = serve_plan(LIB, [(50, 5)])            # below floor: suffix fill, sections lost
du = p["result"]["dropped_units"]
assert du and all(q["unscheduled"] for q in du), "lost coverage rides as unscheduled units"
uncv = set(p["genon"]["slot_fill"]["uncovered_sections"])
for q in du:
    assert set(q["section_anchor"].split(" / ")) <= uncv, "dropped units cover only lost sections"
p = serve_plan(LIB, [(50, 11)])           # exact fill, nothing lost
assert p["result"]["dropped_units"] is None
p = serve_plan([SYN], [(50, 9)])          # synthesis-only truncation: coverage complete
assert p["result"]["dropped_units"] is None
p = serve_plan([A], [(50, 10)])           # truncation with real loss
du = p["result"]["dropped_units"]
assert du and len(du) == len(p["genon"]["slot_fill"]["withheld_units"])
print("dropped-units assertions passed")

# ── surrender files in the drop channel (founder ruling, 2026-08-01) ─────────
p = serve_plan(LIB, [(50, 14)])
assert "return to your budget" in p["result"]["section_coverage_note"]
assert p["result"]["dropped_units"] is None, "surrender loses nothing"
print("surrender-note assertion passed")

# ── LENDABLE UNIT (engine e11, 2026-08-02; ARV-D-023) ───────────────────────────
# A variant that spends slack on a trailing SYNTHESIS unit — one whose anchored
# sections an earlier unit of the SAME plan already taught — must not lend that unit
# to another plan's slot X. It is authored to be met at the end of its own arc
# ("having traced the full arc…"), so in a foreign prefix it assumes lessons the
# class never had. The ladder walks back to the unit that TAUGHT those sections.
from aruvi_core.genon.serve import lendable_unit, _norm   # noqa: E402

RIDX = {_norm(a): i for i, a in enumerate(SECTIONS)}

# D = 9 units: U1..U8 teach all 12 sections, U9 re-anchors the last one (synthesis).
D = _mk_stream(9, _ranges_even(8, 2) + [(11, 11)], "D")
assert len(D["units"]) == 9
assert lendable_unit(D, RIDX)["unit"] == 8, "trailing synthesis is walked past"
assert lendable_unit(B, RIDX)["unit"] == len(B["units"]), \
    "a closing unit that introduces its sections stays lendable"

# more than one step: E ends with TWO trailing revisit units
E = _mk_stream(10, _ranges_even(8, 2) + [(11, 11), (11, 11)], "E")
assert lendable_unit(E, RIDX)["unit"] == 8, "walk-back takes as many steps as needed"

# "all", not "any": a unit anchoring one repeat PLUS new sections still teaches.
# This is the real p07 U7 shape — Climate Change (taught at U6) + Punjab Floods (new).
F = _mk_stream(9, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 9)]
               + [(9, 11)], "F")
assert lendable_unit(F, RIDX)["unit"] == 9, "a partial repeat still introduces"

# the ladder borrows the TAUGHT unit, never the synthesis — whatever rung it lands on
p = serve_plan([A, D], [(50, 10)])
fill = p["genon"]["slot_fill"]
assert fill and fill["borrowed_from"] == 9, fill          # borrowed from D
closing = p["result"]["lesson_plan"]["periods"][-1]["activity_title"]
assert closing == "D U8", "slot X must be D's taught closing unit, not its synthesis"

# EXCEPT in synthesis mode — prefix already covers every section, so the trailing
# synthesis assumes nothing false and is the right borrow.
p = serve_plan([A, D], [(50, 12)])         # A serves 11 units = all 12 sections
if (p["genon"]["slot_fill"] or {}).get("mode") == "synthesis":
    assert p["result"]["lesson_plan"]["periods"][-1]["activity_title"] == "D U9", \
        "synthesis mode borrows the closing synthesis as authored"

print("lendable-unit assertions passed")
