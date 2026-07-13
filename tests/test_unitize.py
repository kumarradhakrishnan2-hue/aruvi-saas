"""Tests for the Lever B display-time 'period' -> 'unit' cleaner (aruvi_core/unitize.py).

Stdlib only; run directly:  python3 tests/test_unitize.py
(No ARUVI_DATA_DIR needed for the unit cases; the corpus scan runs only if saved plans
are reachable under ./data/content/saved_plans.)
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aruvi_core.unitize import unitize, unitize_lesson_plan_dict  # noqa: E402

# ── 1. word-level behaviour ────────────────────────────────────────────────────────
CONVERT = [
    ("In the previous period, we tested the samples.",
     "In the previous unit, we tested the samples."),
    ("This period reuses Period 1's eleven samples.",
     "This unit reuses Unit 1's eleven samples."),
    ("This closing period asks students to classify.",
     "This closing unit asks students to classify."),
    ("Compare with the litmus table from Period 1.",
     "Compare with the litmus table from Unit 1."),
    ("Master observation table from Periods 1 and 2",
     "Master observation table from Units 1 and 2"),
    ("This is a 40-minute period; the extra five minutes help.",
     "This is a 40-minute unit; the extra five minutes help."),
    ("The 30-minute period is tight.", "The 30-minute unit is tight."),
    ("reference in subsequent periods", "reference in subsequent units"),
    ("Grounded in this period's activity.", "Grounded in this unit's activity."),
    ("Teacher previews the next period: 'we will learn...'",
     "Teacher previews the next unit: 'we will learn...'"),
]

# Must be left EXACTLY as-is (domain / punctuation / scheduling / ambiguous senses).
KEEP = [
    "Introduce the periodic table of elements.",
    "Measure the period of a pendulum.",
    "confused the period of the system",
    "as the period of rigidification",
    "organisation as a period of major change",
    "End the sentence with a period.",
    "a period of time",
    "students revise periodically at home",
    "this is the first period of the chapter",          # conservative miss (period of X)
    "35 minutes × 3 periods = 105 minutes",             # scheduling budget line
    "Total: 3 periods · 1h 45min",
]


def test_word_level():
    for src, exp in CONVERT:
        got = unitize(src)
        assert got == exp, f"CONVERT failed:\n  in : {src!r}\n  got: {got!r}\n  exp: {exp!r}"
    for src in KEEP:
        got = unitize(src)
        assert got == src, f"KEEP failed (should be unchanged):\n  in : {src!r}\n  got: {got!r}"


def test_idempotent():
    for src, _ in CONVERT:
        once = unitize(src)
        assert unitize(once) == once, f"not idempotent: {src!r}"


# ── 2. walker only touches narrative fields, never keys / meta / scheduling ─────────
def test_walker_scope():
    lp = {
        "groups": [{
            "type": "progression_stage", "label": "Stage 1: Period patterns",  # label NOT cleaned
            "periods": [{
                "number": 2,
                "title": "Revisiting Period 1",
                "teacher_notes": ["This period builds on the previous period."],
                "materials": ["Samples from Period 1"],
                "activities": ["Compare with Period 1 results"],
                "homework": "Redo the task from Period 1.",
                "phases": [{"text": "Recap the previous period.", "start_min": 0, "end_min": 5}],
                "meta": {"period_schedule_display": "3 periods total",
                         "duration_minutes": 40},
            }],
            "children": [],
        }],
    }
    unitize_lesson_plan_dict(lp)
    p = lp["groups"][0]["periods"][0]
    assert p["title"] == "Revisiting Unit 1"
    assert p["teacher_notes"] == ["This unit builds on the previous unit."]
    assert p["materials"] == ["Samples from Unit 1"]
    assert p["activities"] == ["Compare with Unit 1 results"]
    assert p["homework"] == "Redo the task from Unit 1."
    assert p["phases"][0]["text"] == "Recap the previous unit."
    # untouched: group label, meta (scheduling), and structural keys
    assert lp["groups"][0]["label"] == "Stage 1: Period patterns"
    assert p["meta"]["period_schedule_display"] == "3 periods total"
    assert "number" in p and p["number"] == 2


# ── 3. no corruption anywhere in the historic corpus (best-effort; skipped if absent) ─
def test_corpus_no_corruption():
    root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "content", "saved_plans")
    files = glob.glob(os.path.join(root, "**", "*.json"), recursive=True)
    if not files:
        print("  (corpus scan skipped — no saved plans found)")
        return
    bad = re.compile(r"\bunit(s|'s)?\s+of\b|\bunitic\b|\btime unit\b", re.I)
    corrupt = []

    def walk(o):
        if isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str):
            out = unitize(o)
            if out != o and bad.search(out):
                corrupt.append((o, out))

    for f in files:
        walk(json.load(open(f)))
    assert not corrupt, f"corruption produced on {len(corrupt)} strings, e.g. {corrupt[:3]}"
    print(f"  corpus scan: {len(files)} plans, 0 corruption")


if __name__ == "__main__":
    test_word_level()
    test_idempotent()
    test_walker_scope()
    test_corpus_no_corruption()
    print("OK — unitize: word-level convert/keep, idempotent, walker scope, corpus corruption-free.")
