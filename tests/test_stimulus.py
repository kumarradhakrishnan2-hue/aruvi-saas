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
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "cloud", "content"))


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


def test_structured_dict_stimulus():
    """SS secondary (v2.7+) emits a {type, payload} stimulus. classify_stimulus must route
    by declared type and preserve the payload — never crash on a dict (the old bug)."""
    src = {"type": "source_text",
           "payload": "The Uttaramerur inscription lays down conditions for the assembly."}
    vs = classify_stimulus(src)
    assert vs.type == StimulusType.PROSE
    assert vs.content == src["payload"]
    # declared svg / table win by type; empty payload → NONE; unknown type falls back to heuristics
    assert classify_stimulus({"type": "svg", "payload": "<svg></svg>"}).type == StimulusType.SVG
    assert classify_stimulus({"type": "table", "payload": "A | B\n1 | 2"}).type == StimulusType.TABLE
    assert classify_stimulus({"type": "source_text", "payload": ""}).type == StimulusType.NONE
    assert classify_stimulus({"type": "", "payload": "X | Y\n1 | 2"}).type == StimulusType.TABLE
    # non-string/non-dict is treated as empty, not a crash
    assert classify_stimulus(123).type == StimulusType.NONE


def test_parse_table_structure():
    t = parse_table("Planet | Weight (N)\nEarth | 10\nMoon | 1.6")
    assert t["header"] == ["Planet", "Weight (N)"]
    assert t["rows"] == [["Earth", "10"], ["Moon", "1.6"]]
    assert t["caption"] == "" and t["source_note"] == "", "an ordinary table has neither"
    assert parse_table("") == {"header": [], "rows": [], "caption": "", "source_note": ""}


def test_leading_title_row_becomes_a_caption():
    """SS·VIII ch 3's Maratha-navy MCQ (founder-reported 2026-08-04): the generator put a
    2-cell TITLE line above 3-column data, and every renderer took it as the header — a
    2-column head over a 3-column body, on screen AND in PDF/Word."""
    t = parse_table(
        "Maratha Naval Institution: Two Functions | Evidence from the Chapter\n"
        "Function | Description | Key Evidence\n"
        "Military defence | Protected the west coast | Navy founded 1657\n"
        "Economic sovereignty | Challenged European control | Angre reversed the cartaz")
    assert t["caption"] == ("Maratha Naval Institution: Two Functions · "
                           "Evidence from the Chapter")
    assert t["header"] == ["Function", "Description", "Key Evidence"]
    assert len(t["rows"]) == 2
    assert {len(r) for r in t["rows"]} == {len(t["header"])} == {3}, "grid is uniform"


def test_trailing_attribution_becomes_a_source_note():
    """SS·IX carries four of these — a one-cell '— Adapted from …' line inside the payload."""
    t = parse_table("Gas | Proportion\nNitrogen | ~78%\nOxygen | ~21%\n"
                    "— Adapted from Fig. 3.2, Chapter 3")
    assert t["source_note"] == "— Adapted from Fig. 3.2, Chapter 3"
    assert t["header"] == ["Gas", "Proportion"]
    assert t["rows"] == [["Nitrogen", "~78%"], ["Oxygen", "~21%"]]


def test_short_rows_are_padded_never_truncated():
    t = parse_table("A | B | C\nlong one | 2\nthree | four | five")
    assert {len(r) for r in t["rows"]} == {3}
    assert t["rows"][0] == ["long one", "2", ""], "padded, and no cell dropped"


def test_two_column_table_keeps_its_first_row_as_header():
    """Guard against over-eager caption detection: a genuine 2-column table's first row is
    the header, not a title, because it is not NARROWER than the body."""
    t = parse_table("Word | Meaning\nswarajya | self-rule\ncartaz | trade pass")
    assert t["caption"] == ""
    assert t["header"] == ["Word", "Meaning"]


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
