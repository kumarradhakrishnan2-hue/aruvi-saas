"""Visual-stimulus typing + shared table parsing (normalize.classify_stimulus / parse_table).

Guards the 2-column-table regression: assessment stimuli like "Region | Density" (one pipe
per line) must type as TABLE, not PROSE — otherwise the renderer dumps raw pipes. Also locks
that verse/prose (EXTRACT_ANALYSIS extracts) stays PROSE and that parse_table is the single
splitter. Stdlib only; run directly: python3 tests/test_stimulus.py
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aruvi_core.normalize import classify_stimulus, parse_table  # noqa: E402
from aruvi_core.view_model import StimulusType  # noqa: E402

DATA = os.environ.get("ARUVI_DATA_DIR", os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "content"))


def test_two_column_table_is_table():
    two = "Region of bar magnet | Density of iron filings\nCentre | Sparse\nEnds | Dense"
    assert classify_stimulus(two).type == StimulusType.TABLE, "2-column table mis-typed"


def test_three_plus_column_still_table():
    three = "Trial | Poles | Needle\n1 | N-N | Away\n2 | S-N | Toward"
    assert classify_stimulus(three).type == StimulusType.TABLE


def test_verse_stays_prose():
    verse = ("Music is the ocean\nThat pulls me to the shore.\n"
             "Music is the rhythm\nThat moves me to the core.")
    assert classify_stimulus(verse).type == StimulusType.PROSE


def test_single_incidental_pipe_is_prose():
    # one line, one pipe — a prose aside, not a table
    assert classify_stimulus("Consider the ratio a|b in lowest terms.").type == StimulusType.PROSE


def test_svg_and_empty():
    assert classify_stimulus("<svg viewBox='0 0 1 1'></svg>").type == StimulusType.SVG
    assert classify_stimulus("").type == StimulusType.NONE
    assert classify_stimulus(None).type == StimulusType.NONE


def test_parse_table_structure():
    t = parse_table("Planet | Weight (N)\nEarth | 10\nMoon | 1.6")
    assert t["header"] == ["Planet", "Weight (N)"]
    assert t["rows"] == [["Earth", "10"], ["Moon", "1.6"]]
    assert parse_table("") == {"header": [], "rows": []}


def test_all_pipe_bearing_assessment_stimuli_type_as_table():
    """Every pipe-bearing assessment stimulus in saved plans must classify as TABLE."""
    checked = 0
    offenders = []
    for f in glob.glob(os.path.join(DATA, "saved_plans", "*", "*", "*.json")):
        d = json.load(open(f))

        def walk(o):
            nonlocal checked
            if isinstance(o, dict):
                if o.get("question_type"):
                    v = o.get("visual_stimulus")
                    if isinstance(v, str) and "|" in v and v.strip():
                        checked += 1
                        if classify_stimulus(v).type != StimulusType.TABLE:
                            offenders.append((o.get("question_type"), v[:60]))
                for x in o.values():
                    walk(x)
            elif isinstance(o, list):
                for x in o:
                    walk(x)
        walk(d.get("result", {}))
    assert not offenders, f"pipe stimuli not typed as table: {offenders[:5]}"
    assert checked >= 20, f"expected to check real fixtures, only saw {checked}"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")
