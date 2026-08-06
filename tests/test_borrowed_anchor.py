"""ARV-D-064 — a BORROWED unit's questions must stay attached to the borrowed unit.

The live science·ix ch 8 library cannot exercise this: its only cross-plan borrow is
the e15 rescue of the TOP's `synthesis` unit, and that unit carries no question, so no
item ever crosses plans. This file supplies the case the corpus withholds — a
science·secondary-shaped library in which the borrowed unit DOES carry questions, and
in which the lender's `section_number` deliberately COLLIDES with a different section
of the host plan, on a sitting the host actually serves. That collision is the point:
it is what a render-time join cannot survive.

THE LIBRARY (one chapter, nine registry sections):
  HOST   ·  9 units, 9 handoff rows — one section per unit. Its section 6 is
            "8.6 Mass Number".
  LENDER · 12 units, 7 handoff rows — the same chapter cut COARSER, so its numbering
            drifts: its section 6 is "8.8 Valency / 8.9 Isotopes", and the unit that
            deals it (U11) carries two questions numbered 6.

SERVING X = 8 chooses the HOST (smallest count ≥ 8) and fills the eighth slot from the
lender's U11, which first-deals the next-due section AND reaches forward — so it beats
the host's own M-alone candidate (§0.4). The two borrowed questions arrive carrying
"section 6". The host's section 6 is a different section, and its sitting 6 IS served.

  Before the fix: the port re-derived the anchor from that number through the HOST's
  index and filed both questions on sitting 6, under a heading reading "8.6 Mass
  Number" — a question about valency printed inside the lesson on mass number.
  After it: they read the stamp the engine already wrote and stay on sitting 8, under
  their own heading, with their LO carried into the plan's coverage (e16).

Stdlib only; run directly:  python3 tests/test_borrowed_anchor.py
"""
import copy
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aruvi_core.genon.compile import compile_stream          # noqa: E402
from aruvi_core.genon.serve import serve_plan                # noqa: E402
from aruvi_core.link_resolver import platform_anchor         # noqa: E402
from aruvi_core.subjects import get as get_subject           # noqa: E402
import aruvi_core.subjects.science                           # noqa: E402,F401  (registers)


SEC = ["8.1 Laws of Chemical Combination", "8.2 Dalton's Atomic Theory",
       "8.3 Atoms and Their Symbols", "8.4 Atomic Mass",
       "8.5 Molecules and Ions", "8.6 Mass Number",
       "8.7 Electronic Configuration", "8.8 Valency", "8.9 Isotopes"]

# HOST — one section per unit, so its section_number k IS its sitting k.
HOST_UNITS = [[s] for s in SEC]                                   # 9 units
HOST_ROWS = [([s], [i]) for i, s in enumerate(SEC, 1)]            # 9 handoff rows

# LENDER — same chapter, twelve units, but only SEVEN handoff rows: it groups its
# sections coarsely, which is what makes its numbering drift from the host's. U11
# first-deals 8.8 AND reaches forward into 8.9 — the §0.4 preference that lets a
# foreign candidate beat the host's own.
LENDER_UNITS = [[SEC[0]], [SEC[1]], [SEC[2]], [SEC[3]], [SEC[4]], [SEC[4]],
                [SEC[5]], [SEC[5]], [SEC[6]], [SEC[6]], [SEC[7], SEC[8]],
                ["synthesis"]]                                    # 12 units
LENDER_ROWS = [([SEC[0], SEC[1]], [1, 2]), ([SEC[2], SEC[3]], [3, 4]),
               ([SEC[4]], [5, 6]), ([SEC[5]], [7, 8]), ([SEC[6]], [9, 10]),
               ([SEC[7], SEC[8]], [11]), (["synthesis"], [12])]   # 7 handoff rows

BORROWED_LABEL = " / ".join([SEC[7], SEC[8]])      # the lender's section 6
COLLIDES_WITH = SEC[5]                             # the host's section 6


def _period(n, anchors, minutes=50):
    anchor = " / ".join(anchors)
    return {
        "period_number": n, "period_duration_minutes": minutes,
        "activity_title": f"{anchor} — sitting {n}", "section_anchor": anchor,
        "materials": ["chalk"], "visual_aids": None,
        "pedagogical_approaches": ["Inquiry"], "teacher_notes": f"notes · {anchor}",
        "homework": [], "competency_edges": [],
        "time_bands": [{"minutes": "0-10", "activity": f"open {anchor}"},
                       {"minutes": "10-40", "activity": f"work {anchor}"},
                       {"minutes": f"40-{minutes}", "activity": f"close {anchor}"}],
    }


def _plan(tag, unit_anchors, rows, extra_questions=()):
    """A science·secondary-shaped saved plan: coverage_handoff is a LIST keyed by
    section_number, items live under an {..., "questions": [...]} wrapper."""
    periods = [_period(i, a) for i, a in enumerate(unit_anchors, 1)]
    handoff, questions = [], []
    for i, (labels, pns) in enumerate(rows, 1):
        label = " / ".join(labels)
        handoff.append({"section_number": i, "section_label": label,
                        "total_sections": len(rows), "period_duration_minutes": 50,
                        "activity_summary": f"summary · {label}",
                        "implied_lo": f"LO · {label}", "section_context": f"ctx · {label}",
                        "c_code": "C-1.1", "period_numbers": list(pns)})
        if label == "synthesis":
            continue
        questions.append({
            "section_number": i, "section_label": label, "total_sections": len(rows),
            "implied_lo_assessed": f"LO · {label}", "section_context": f"ctx · {label}",
            "question_type": "MCQ", "competency": {"c_code": "C-1.1"},
            "cognitive_demand": "Understanding",
            "question_text": f"[{tag}] question on {label}",
            "options": [{"label": "A", "text": "a", "is_correct": True},
                        {"label": "B", "text": "b", "is_correct": False}]})
    for snum, label, text in extra_questions:
        questions.append({
            "section_number": snum, "section_label": label, "total_sections": len(rows),
            "implied_lo_assessed": f"LO · {label}", "section_context": f"ctx · {label}",
            "question_type": "ECR", "competency": {"c_code": "C-1.1"},
            "cognitive_demand": "Analysis",
            "question_text": f"[{tag}] {text}", "options": []})
    return {
        "filename": f"ch_08_{tag}.json", "subject": "science", "grade": "ix",
        "chapter_number": 8, "chapter_title": "Atoms and Molecules",
        "period_rows_snapshot": [{"duration": 50, "count": len(periods)}],
        "result": {"lesson_plan": {"periods": periods},
                   "coverage_handoff": handoff,
                   "assessment_items": {"grade": "Grade IX", "subject": "science",
                                        "stage": "secondary", "chapter_number": 8,
                                        "chapter_title": "Atoms and Molecules",
                                        "questions": questions}},
    }


HOST = _plan("host", HOST_UNITS, HOST_ROWS)
LENDER = _plan("lender", LENDER_UNITS, LENDER_ROWS,
               extra_questions=[(6, BORROWED_LABEL, "SECOND question on valency and isotopes")])

STREAMS = [compile_stream(copy.deepcopy(LENDER)), compile_stream(copy.deepcopy(HOST))]

# ── the fixture must itself be right, or everything below passes for a wrong reason ──
_borrowable = [i for i in STREAMS[0]["assessment_items"] if i["unit_ref"] == [11]]
assert len(_borrowable) == 2, \
    f"fixture: the lender's U11 must carry two questions, got {len(_borrowable)}"
_host_row6 = [h for h in HOST["result"]["coverage_handoff"] if h["section_number"] == 6]
assert _host_row6[0]["section_label"] == COLLIDES_WITH, "fixture: the collision target"
assert all(i["section_number"] == 6 for i in _borrowable), \
    "fixture: the borrowed questions must carry the COLLIDING number"
assert BORROWED_LABEL != COLLIDES_WITH


# ── serve X = 8 ──────────────────────────────────────────────────────────────────
plan = serve_plan(STREAMS, [(50, 8)])
g, sf = plan["genon"], (plan["genon"]["slot_fill"] or {})
assert g["variant_used"] == 9, g["variant_used"]           # the host was chosen
assert g["sittings"] == 8
assert sf.get("self_fill") is False, f"expected a CROSS-PLAN borrow, got {sf}"
assert sf.get("borrowed_from") == 12, sf

r = plan["result"]
periods = r["lesson_plan"]["periods"]
assert [p["section_anchor"] for p in periods] == SEC[:7] + [BORROWED_LABEL], \
    [p["section_anchor"] for p in periods]

items = r["assessment_items"]["questions"]
borrowed = [i for i in items if "[lender]" in i["question_text"]]
own = [i for i in items if "[host]" in i["question_text"]]

# 1 · THE QUESTIONS RIDE WITH THE UNIT, AND THE STAMP SAYS WHERE THEY SIT.
assert len(borrowed) == 2, f"the borrowed unit's questions must ride with it, got {len(borrowed)}"
for it in borrowed:
    assert it["period_ref"] == [8], it["period_ref"]
    assert platform_anchor(it) == [8], platform_anchor(it)
# the host's own served questions are untouched; its unserved ones are gone (e13)
assert [i["period_ref"] for i in own] == [[n] for n in range(1, 8)], \
    [i["period_ref"] for i in own]
assert g["assessment_items_unserved"] == 2, g["assessment_items_unserved"]

# 2 · THE LO TRAVELS TOO (e16): the plan asks it, so the plan must claim to teach it.
ho = r["coverage_handoff"]
row = [h for h in ho if h.get("section_label") == BORROWED_LABEL]
assert len(row) == 1, f"the borrowed unit's coverage row must travel — rows: {[h['section_label'] for h in ho]}"
assert row[0]["period_numbers"] == [8], row[0]
assert row[0]["implied_lo"] == f"LO · {BORROWED_LABEL}", row[0]
assert not row[0].get("unscheduled"), "a borrowed SERVED unit is not unscheduled"
assert [h["section_label"] for h in ho] == SEC[:7] + [BORROWED_LABEL], \
    [h["section_label"] for h in ho]

# 3 · THE SCREEN — where the defect actually bit.
sub = get_subject("science")
chapter = {"chapter_number": 8, "chapter_title": "Atoms and Molecules"}
view = sub.assessment_to_view(r["assessment_items"], grade="Grade IX", chapter=chapter,
                              link_context={"periods": periods, "handoff": ho})
flat = [(grp.label, it) for grp in view.groups for it in grp.items]
seen_b = [(lab, it.meta["anchor_period"]) for lab, it in flat if "[lender]" in it.prompt]
seen_o = [(lab, it.meta["anchor_period"]) for lab, it in flat if "[host]" in it.prompt]

# The HOST's own questions first — a number-keyed join clobbers in BOTH directions.
# (Measured on pre-fix code with the e16 row carried: handoff_period_index is a dict,
# so the lender's row 6 overwrote the host's row 6 and the host's own mass-number
# question moved to sitting 8 as well.)
assert [a for _, a in seen_o] == list(range(1, 8)), seen_o
assert [l for l, _ in seen_o] == SEC[:7], seen_o

assert len(seen_b) == 2, seen_b
for label, anchor in seen_b:
    assert anchor == 8, f"borrowed question anchored to sitting {anchor}, expected 8"
    assert anchor != 6, "landed on the host's section 6 — the ARV-D-064 anchor failure"
    # 4 · THE HEADING: its own label, not the host's name for that number.
    assert label == BORROWED_LABEL, f"borrowed question filed under {label!r}"
    assert label != COLLIDES_WITH, "filed under the host's section 6 — the grouping failure"

anchors = sorted(it.meta["anchor_period"] for _, it in flat)
assert anchors == [1, 2, 3, 4, 5, 6, 7, 8, 8], anchors   # 7 host + both borrowed on 8
assert set(anchors) == set(range(1, 9)), "every sitting assessed"
assert all(a is not None for a in anchors), "no orphans"


# ── the fallback still stands: an UN-SERVED library file carries no stamp ────────
raw = copy.deepcopy(HOST["result"])
for q in raw["assessment_items"]["questions"]:
    q.pop("period_ref", None)
    q.pop("unit_ref", None)
lib = sub.assessment_to_view(raw["assessment_items"], grade="Grade IX", chapter=chapter,
                             link_context={"periods": raw["lesson_plan"]["periods"],
                                           "handoff": raw["coverage_handoff"]})
assert sorted(it.meta["anchor_period"] for grp in lib.groups for it in grp.items) == \
    list(range(1, 10)), "an un-stamped library file must still resolve through the handoff"

print("test_borrowed_anchor: OK — the borrowed unit's questions keep their sitting, "
      "their heading and their LO; the un-stamped library file still joins as before")
