#!/usr/bin/env python3
"""PLAN-granularity serving — science · middle (engine e17, 2026-08-07).

Spec: docs/science_middle_stage_serve.md. The stage under test is the corpus's one
structural exception: its units belong to a cognitive progression arc, a stage is taught
whole or not at all, so no prefix of a canonical is a valid plan. Serving is
whole-canonical selection.

THE FOUR LAWS (spec §2), each asserted below:
  X = K            -> identity, that canonical whole
  X = K + 1        -> that canonical whole + the TOP's synthesis unit as sitting X
  X < lowest K     -> the lowest canonical truncated, remainder as dropped_units
  X > top          -> the top, surrendering the excess

Plus the property the density rule exists to guarantee: NO SURRENDER INSIDE THE BAND.

Fixtures are synthetic — science middle has no authored library yet (that is C1, and it
is metered). They are built to the stage's real shape: progression_stage per period, NO
section_anchor anywhere, a coverage_handoff of one entry per stage, and a flat item list
joined to the handoff by progression_stage.

Run: python3 tests/test_genon_plan_granularity.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aruvi_core.genon.compile import compile_stream                      # noqa: E402
from aruvi_core.genon.serve import serve_plan, select_whole_plan         # noqa: E402
from aruvi_core.genon import carriers as C                               # noqa: E402

DUR = 45                     # class VIII standard


def canonical(count, *, synthesis=False, stages=3, chapter=6):
    """A science·middle canonical of `count` units spread over `stages` arc stages.

    Deliberately shaped like the constitution's output and NOT like any other stage:
    no `section_anchor` on any period; the closing unit of a standard canonical carries
    the explicit `synthesis: true` boolean, which is the carrier this stage uses because
    it has no anchor field to hold the reserved token."""
    arc = count - (1 if synthesis else 0)
    periods, handoff, items = [], [], []
    per = max(1, arc // stages)
    stage_units = {}
    for i in range(1, arc + 1):
        st = min(stages, (i - 1) // per + 1)
        stage_units.setdefault(st, []).append(i)
        periods.append({
            "period_number": i,
            "period_duration_minutes": DUR,
            "progression_stage": st,
            "stage_label": "Stage %d" % st,
            "activity_title": "c%d unit %d" % (count, i),
            "pedagogical_approach": "Guided Inquiry",
            "materials": ["board"],
            "time_bands": [{"minutes": "0-15", "activity": "c%d u%d open" % (count, i)},
                           {"minutes": "15-45", "activity": "c%d u%d main" % (count, i)}],
            "teacher_notes": "notes c%d u%d" % (count, i),
            "homework": [],
        })
    if synthesis:
        periods.append({
            "period_number": count,
            "period_duration_minutes": DUR,
            "progression_stage": stages,
            "stage_label": "Stage %d" % stages,
            "activity_title": "c%d whole-chapter synthesis" % count,
            "pedagogical_approach": "Discussion",
            "materials": [],
            "synthesis": True,                       # ← the carrier for this stage
            "time_bands": [{"minutes": "0-45", "activity": "c%d synthesis" % count}],
            "teacher_notes": "draw the chapter together",
            "homework": [],
        })
        stage_units[stages].append(count)
    for st in sorted(stage_units):
        handoff.append({"stage_number": st, "stage_label": "Stage %d" % st,
                        "total_stages": stages, "period_numbers": stage_units[st],
                        "implied_lo": "LO for stage %d" % st, "c_code": "C%d" % st})
        for q in range(2):
            items.append({"progression_stage": st, "question_type": "MCQ",
                          "question_text": "c%d s%d q%d" % (count, st, q),
                          "options": [], "competency": {"c_code": "C%d" % st}})
    return {"subject": "Science", "grade": "viii", "chapter_number": chapter,
            "chapter_title": "Pressure, Winds, Storms, and Cyclones",
            "filename": "ch_%02d_canonical%s.json" % (chapter, "" if synthesis
                                                      else "_p%02d" % count),
            "result": {"lesson_plan": {"periods": periods},
                       "coverage_handoff": handoff, "assessment_items": items}}


def library(counts):
    """counts[0] is the standard (it alone carries the synthesis)."""
    return [compile_stream(canonical(c, synthesis=(i == 0)))
            for i, c in enumerate(counts)]


def modes(streams, lo, hi):
    out = {}
    for X in range(lo, hi + 1):
        p = serve_plan(streams, [(DUR, X)])
        g, sf = p["genon"], (p["genon"]["slot_fill"] or {})
        out[X] = {"mode": sf.get("mode") or "identity", "sittings": g["sittings"],
                  "surrendered": g["surrendered_periods"], "used": g["variant_used"],
                  "drops": len(p["result"].get("dropped_units") or []), "plan": p}
    return out


# ── the four laws ────────────────────────────────────────────────────────────────

def test_plugin_declares_plan_granularity():
    assert C.serve_granularity("Science", "viii") == "plan"
    assert C.has_section_axis("Science", "viii") is False
    # and the sibling stage must NOT have moved
    assert C.serve_granularity("Science", "ix") == "unit"
    assert C.has_section_axis("Science", "ix") is True
    print("ok   plugin declares plan granularity for middle, unit for secondary")


def test_compiles_without_section_anchor():
    s = library([12])[0]
    assert all(u["section_anchor"] is None for u in s["units"]), \
        "a stage with no section axis must compile with null anchors"
    assert s["units"][-1]["synthesis"] is True, "synthesis boolean must reach the unit"
    assert not any(u["synthesis"] for u in s["units"][:-1])
    print("ok   compiles with no section_anchor; synthesis carried by the boolean")


def test_identity_at_every_canonical_count():
    counts = [12, 10, 8, 7]
    m = modes(library(counts), 7, 12)
    for k in counts:
        assert m[k]["mode"] == "identity", (k, m[k]["mode"])
        assert m[k]["used"] == k and m[k]["sittings"] == k and m[k]["surrendered"] == 0
        assert m[k]["drops"] == 0
    print("ok   X = K -> identity, whole canonical, at every count", counts)


def test_synthesis_borrow_at_k_plus_one():
    counts = [12, 10, 8, 7]
    m = modes(library(counts), 7, 12)
    # k = 7 is excluded on purpose: 7+1 = 8 is ITSELF a canonical, and identity must win
    # that tie — a plan authored for 8 sittings beats a 7-arc with a closer bolted on.
    assert m[8]["mode"] == "identity" and m[8]["used"] == 8
    for k in (8, 10):                          # 12 is the top; 12+1 is surrender
        X = k + 1
        r = m[X]
        assert r["mode"] == "synthesis", (X, r["mode"])
        assert r["used"] == k, "the K canonical must be served WHOLE, not truncated"
        assert r["sittings"] == X and r["surrendered"] == 0
        ps = r["plan"]["result"]["lesson_plan"]["periods"]
        assert len(ps) == X
        assert "synthesis" in ps[-1]["activity_title"], ps[-1]["activity_title"]
        assert ps[-1]["activity_title"].startswith("c12"), \
            "the synthesis must come from the TOP canonical"
        # every one of K's own units is present, in order, before it
        assert [p["activity_title"] for p in ps[:-1]] == \
               ["c%d unit %d" % (k, i) for i in range(1, k + 1)]
    print("ok   X = K+1 -> K complete + the TOP's synthesis as sitting X")


def test_no_surrender_and_no_holes_inside_the_band():
    """The property the step-2 density rule exists to guarantee (spec §3)."""
    for counts in ([12, 10, 8, 7], [18, 16, 14, 12, 11], [6, 4], [9, 7, 5]):
        top, floor = counts[0], counts[-1]
        m = modes(library(counts), floor, top)
        for X in range(floor, top + 1):
            assert m[X]["surrendered"] == 0, (counts, X, "surrender inside the band")
            assert m[X]["sittings"] == X, (counts, X, "did not use every period")
            assert m[X]["drops"] == 0, (counts, X, "dropped a unit inside the band")
            assert m[X]["mode"] in ("identity", "synthesis"), (counts, X, m[X]["mode"])
    print("ok   no surrender, no drops, no unused periods anywhere inside [floor, top]")


def test_below_floor_truncates_with_declared_drops():
    counts = [12, 10, 8, 7]
    for X in (6, 5):
        p = serve_plan(library(counts), [(DUR, X)])
        g, sf = p["genon"], p["genon"]["slot_fill"]
        assert sf["mode"] == "truncation" and g["surrendered_periods"] == 0
        assert g["used" if False else "variant_used"] == 7, "must truncate the LOWEST"
        assert g["sittings"] == X
        dropped = p["result"]["dropped_units"]
        assert len(dropped) == 7 - X, (X, len(dropped))
        assert all(d["unscheduled"] is True for d in dropped)
        # renumbered into THIS plan's sequence, continuing after the served sittings
        assert [d["period_number"] for d in dropped] == list(range(X + 1, 8))
        note = p["result"]["section_coverage_note"]
        assert "could not be scheduled" in note and str(7 - X) in note, note
        # the dropped units' questions ride with them, and are NOT counted as unserved
        rode = [i for i in _flat(p) if i.get("unscheduled")]
        assert rode, "a dropped unit's questions must travel with it"
        assert g["assessment_items_unserved"] == 0, g["assessment_items_unserved"]
    print("ok   X < floor -> lowest canonical truncated, drops declared + carried")


def test_surrender_only_above_the_top():
    counts = [12, 10, 8, 7]
    for X, expect in ((13, 1), (15, 3)):
        p = serve_plan(library(counts), [(DUR, X)])
        g = p["genon"]
        assert g["surrendered_periods"] == expect and g["variant_used"] == 12
        assert g["sittings"] == 12 and (p["result"].get("dropped_units") or []) == []
        assert "return to your budget" in p["result"]["section_coverage_note"]
        # e10 still holds: the print reflects what was SERVED, not the ask
        assert "Total: 12 periods" in p["period_schedule_display"]
        assert g["matrix"][0]["count"] == X, "the request survives as provenance"
    print("ok   X > top -> top served, excess surrendered, served schedule printed")


# ── assessment, the reason the stage is an exception at all ──────────────────────

def _flat(plan):
    it = plan["result"]["assessment_items"]
    return it if isinstance(it, list) else (it or {}).get("questions") or []


def test_assessment_matches_the_arc_actually_taught():
    counts = [12, 10, 8, 7]
    lib = library(counts)
    # identity: the canonical's own assessment, entire, nothing unserved
    p = serve_plan(lib, [(DUR, 10)])
    assert len(_flat(p)) == 6 and p["genon"]["assessment_items_unserved"] == 0
    # K+1: STILL exactly the base plan's items. REVERSED at ARV-D-067 (2026-08-07) — this
    # test previously asserted the opposite ("the borrowed synthesis brings its own items"),
    # which was C9.2's rule read across from the section-axis stages. It does not survive
    # stage-level anchoring: a unit there has no items of its own, it inherits its whole
    # STAGE's set, so the borrow imported the lender's entire final-stage assessment into a
    # class that never had that stage's earlier units.
    q = serve_plan(lib, [(DUR, 11)])
    assert len(_flat(q)) == len(_flat(p)), \
        "the borrowed synthesis must bring NO items (ARV-D-067)"
    assert q["genon"]["assessment_items_unserved"] == 0
    for i in _flat(q):
        assert i.get("period_ref"), "every served item must carry a sitting anchor"
        assert max(i["period_ref"]) <= 11
    print("ok   assessment follows the arc served; the borrowed synthesis brings NO items")


def test_stages_are_never_split():
    """The whole reason for plan granularity: no served plan may contain part of a
    progression stage. Every stage present must be present in full."""
    counts = [12, 10, 8, 7]
    lib = library(counts)
    for X in range(7, 13):
        p = serve_plan(lib, [(DUR, X)])
        titles = [pp["activity_title"] for pp in p["result"]["lesson_plan"]["periods"]]
        base = [t for t in titles if "synthesis" not in t]
        k = p["genon"]["variant_used"]
        assert base == ["c%d unit %d" % (k, i) for i in range(1, len(base) + 1)], \
            (X, "served a PREFIX of a canonical rather than the whole plan")
    print("ok   no served plan is a partial canonical -> no stage is ever split")


def test_selection_is_pure_and_deterministic():
    lib = library([12, 10, 8, 7])
    for X in range(5, 15):
        a = select_whole_plan(lib, X)
        b = select_whole_plan(lib, X)
        assert (len(a[0]["units"]), a[1], (a[2] or {}).get("mode")) == \
               (len(b[0]["units"]), b[1], (b[2] or {}).get("mode"))
    print("ok   selection is deterministic")


def test_served_plan_still_renders_through_the_subject_port():
    """A served plan must carry whatever its subject's PORT groups on.

    The engine's unit projection models the fields SERVING reasons about, which is not
    the set DISPLAY needs. science·middle groups on `progression_stage`/`stage_label`,
    and when those were dropped every served plan collapsed into a single "Stage None"
    group — the phantom CLAUDE.md §3 records for science secondary, reappearing on the
    serve side. compile.py carries the unmodelled fields in `unit["extra"]`; this is the
    regression guard."""
    import aruvi_core.subjects.science                                   # noqa: F401
    from aruvi_core import subjects
    port = subjects.get("science")
    lib = library([12, 10, 8, 7])
    for X, expect_mode in ((10, "identity"), (11, "synthesis"), (6, "truncation")):
        p = serve_plan(lib, [(DUR, X)])
        assert ((p["genon"]["slot_fill"] or {}).get("mode") or "identity") == expect_mode
        for per in p["result"]["lesson_plan"]["periods"]:
            assert per["progression_stage"] is not None, (X, "stage lost in the serve")
            assert per["stage_label"], (X, "stage label lost in the serve")
            assert per["period_number"] <= X, "extra must not overwrite the sitting number"
        v = port.lesson_plan_to_view(p["result"], grade="viii",
                                     chapter={"chapter_number": 6, "chapter_title": "x"})
        assert v.groups and all(g.type == "progression_stage" for g in v.groups), \
            (X, [(g.type, g.label) for g in v.groups])
        assert all(g.label and g.label != "None" for g in v.groups), \
            (X, "the Stage-None phantom is back")
        assert sum(len(g.periods) for g in v.groups) == X
    print("ok   served plans still group by progression stage in the subject port")


def test_borrowed_synthesis_brings_nothing_but_itself():
    """ARV-D-067. C9.2's "a borrowed unit brings its own items" presupposes UNIT-level
    anchoring. Under STAGE-level anchoring a unit has no items of its own — it inherits its
    whole stage's set — so the borrow dragged the lender's entire final-stage assessment
    into a plan whose class never had that stage's earlier units, and the lender's handoff
    row grew a phantom extra stage holding one sitting."""
    counts = [12, 10, 8, 7]
    lib = library(counts)
    own = {len(s["units"]): len(s["assessment_items"]) for s in lib}
    for X, base in ((9, 8), (11, 10)):
        p = serve_plan(lib, [(DUR, X)])
        r, g = p["result"], p["genon"]
        assert (g["slot_fill"] or {}).get("mode") == "synthesis"
        assert g["variant_used"] == base
        items = _flat(p)
        # 1 · the item set is EXACTLY the base canonical's — nothing imported
        assert len(items) == own[base], (X, len(items), own[base])
        # 2 · no phantom group: the served plan carries no stage the base plan lacked
        base_stages = {h["stage_number"] for s in lib if len(s["units"]) == base
                       for h in _handoff(s)}
        assert {h["stage_number"] for h in r["coverage_handoff"]} == base_stages, X
        # 3 · the synthesis sitting joined the host's LAST group, not one of its own
        ps = r["lesson_plan"]["periods"]
        assert ps[-1]["progression_stage"] == ps[-2]["progression_stage"], X
        assert ps[-1]["stage_label"] == ps[-2]["stage_label"], X
        # …while keeping its own content
        assert "synthesis" in ps[-1]["activity_title"]
        assert ps[-1]["activity_title"] != ps[-2]["activity_title"]
        # 4 · NO item anchors to the synthesis sitting
        assert X not in {a for i in items for a in (i.get("period_ref") or [])}, X
        assert g["assessment_items_unserved"] == 0
    print("ok   borrowed synthesis: no items, no phantom stage, adopts the host's last stage")


def _handoff(stream):
    ho = stream.get("coverage_handoff") or {}
    return [dict(v.get("_entry") or {}, stage_number=(v.get("_entry") or {}).get("stage_number"))
            for v in ho.values()] if isinstance(ho, dict) else ho


def test_unit_granularity_stages_are_untouched():
    """The guard that matters most: ten stages must not have moved."""
    import glob
    import json
    seen = 0
    for sub, gr, ch in (("social_sciences", "ix", "ch_03"),
                        ("social_sciences", "viii", "ch_03"),
                        ("science", "ix", "ch_08")):
        fs = sorted(glob.glob("data/cloud/content/saved_plans/%s/%s/%s_canonical*.json"
                              % (sub, gr, ch)))
        if not fs:
            continue
        streams = [compile_stream(json.load(open(f))) for f in fs]
        counts = sorted((len(s["units"]) for s in streams), reverse=True)
        p = serve_plan(streams, [(50, counts[0])])
        assert p["genon"]["serve_granularity"] == "unit", (sub, gr)
        assert p["genon"]["slot_fill"] is None and p["genon"]["variant_used"] == counts[0]
        seen += 1
    assert seen, "no real libraries found — this guard proved nothing"
    print("ok   the %d authored unit-granularity libraries still serve as before" % seen)


if __name__ == "__main__":
    for fn in (test_plugin_declares_plan_granularity,
               test_compiles_without_section_anchor,
               test_identity_at_every_canonical_count,
               test_synthesis_borrow_at_k_plus_one,
               test_no_surrender_and_no_holes_inside_the_band,
               test_below_floor_truncates_with_declared_drops,
               test_surrender_only_above_the_top,
               test_assessment_matches_the_arc_actually_taught,
               test_stages_are_never_split,
               test_selection_is_pure_and_deterministic,
               test_served_plan_still_renders_through_the_subject_port,
               test_borrowed_synthesis_brings_nothing_but_itself,
               test_unit_granularity_stages_are_untouched):
        fn()
    print("\nALL PLAN-GRANULARITY TESTS PASS")
