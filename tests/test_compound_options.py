"""Compound items: options split back under their sub-question (2026-08-14).

The rule under test is a DISPLAY rule over the corpus's grouped storage label (1A…2D),
not a schema — see aruvi_core/compound_options.py for why. So the two things that matter
are (a) a compound item groups correctly and shows A–D, and (b) NOTHING ELSE CHANGES:
every ordinary flat item must come back None and keep its existing render path.

Run: python3 tests/test_compound_options.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from aruvi_core.compound_options import (          # noqa: E402
    display_label, group_of, grouped_option_sets,
)
from aruvi_core.normalize import normalize_options  # noqa: E402

SAVED = REPO / "data" / "content" / "saved_plans" / "english" / "ix"


def opt(label, text, correct=False):
    return {"label": label, "text": text, "is_correct": correct}


def test_flat_items_are_untouched():
    """The regression that matters most: an ordinary MCQ must not enter the new branch."""
    flat = [opt("A", "one"), opt("B", "two", True), opt("C", "three"), opt("D", "four")]
    assert grouped_option_sets(flat) is None, "a flat A–D MCQ must not group"
    assert grouped_option_sets([]) is None
    assert grouped_option_sets(None) is None
    assert grouped_option_sets([opt("A", "only")]) is None, "one option cannot be compound"
    # TRUE_FALSE statement lists use digit labels
    assert grouped_option_sets([opt("1", "s1", True), opt("2", "s2")]) is None
    # a single group is not compound — there is nothing to separate it from
    assert grouped_option_sets([opt("1A", "a"), opt("1B", "b")]) is None
    # mixed labels never group (half-migrated data must fall back, not half-render)
    assert grouped_option_sets([opt("1A", "a"), opt("B", "b")]) is None
    # labels are unchanged for flat items
    assert display_label(flat, "B") == "B"
    assert group_of(flat, "B") is None
    print("  ok  flat items untouched")


def test_compound_groups_and_letters():
    opts = [opt("1A", "q1 a"), opt("1B", "q1 b", True), opt("1C", "q1 c"), opt("1D", "q1 d"),
            opt("2A", "q2 a"), opt("2B", "q2 b"), opt("2C", "q2 c", True), opt("2D", "q2 d")]
    sets = grouped_option_sets(opts)
    assert sets is not None and len(sets) == 2, sets
    assert [s["group"] for s in sets] == ["1", "2"]
    for s in sets:
        assert [o["display"] for o in s["options"]] == ["A", "B", "C", "D"], s
        assert len(s["options"]) == 4
    # the storage label survives — every downstream join still works
    assert [o["label"] for o in sets[0]["options"]] == ["1A", "1B", "1C", "1D"]
    assert display_label(opts, "2C") == "C"
    assert group_of(opts, "2C") == "2"
    assert display_label(opts, "1B") == "B" and group_of(opts, "1B") == "1"
    # one correct answer per sub-question, and each is attributable
    correct = [o["label"] for o in opts if o["is_correct"]]
    assert {group_of(opts, c) for c in correct} == {"1", "2"}, "one answer per sub-question"
    print("  ok  compound groups, letters A–D, labels preserved")


def test_normalize_options_keeps_every_correct_answer():
    """The scalar-`answer` bug: two correct options used to report only the last."""
    opts = [opt("1A", "x"), opt("1B", "y", True), opt("2A", "z"), opt("2B", "w", True)]
    _, answer = normalize_options(opts)
    assert answer == "1B, 2B", answer
    # single-correct is byte-identical to the old behaviour
    _, answer = normalize_options([opt("A", "x"), opt("B", "y", True)])
    assert answer == "B", answer
    # plain-string options still carry no answer
    assert normalize_options(["one", "two"]) == (["one", "two"], "")
    print("  ok  normalize_options reports every correct option")


def test_the_two_real_items():
    """The corpus itself — english·ix ch 5 and ch 9, the only compound MCQs there are."""
    if not SAVED.is_dir():
        print("  SKIP the corpus check — saved_plans not present")
        return
    sys.path.insert(0, str(REPO))
    from aruvi_core.genon.carriers import raw_item_list

    seen = 0
    for path in sorted(SAVED.glob("ch_*_canonical.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        for it in raw_item_list(doc.get("result", doc)):
            if not isinstance(it, dict):
                continue
            sets = grouped_option_sets(it.get("options"))
            if sets is None:
                continue
            seen += 1
            assert it["question_type"] == "MCQ", it["id"]
            assert len(sets) == 2, (path.name, it["id"])
            for s in sets:
                assert [o["display"] for o in s["options"]] == ["A", "B", "C", "D"]
                n_correct = sum(1 for o in s["options"] if o.get("is_correct"))
                assert n_correct == 1, (path.name, it["id"], s["group"], n_correct)
            # every diagnostic keys a real option, and none keys a correct one
            rev = (it.get("teacher_guide") or {}).get("what_each_option_reveals") or {}
            labels = {o["label"] for o in it["options"]}
            correct = {o["label"] for o in it["options"] if o.get("is_correct")}
            assert set(rev) == labels - correct, (path.name, it["id"], sorted(rev))
            print(f"  ok  {path.name} {it['id']} — 2 sub-questions, A–D each, "
                  f"answers {sorted(group_of(it['options'], c) + '·' + display_label(it['options'], c) for c in correct)}")
    assert seen == 2, f"expected exactly 2 compound items in english·ix, found {seen}"


if __name__ == "__main__":
    os.environ.setdefault("ARUVI_DATA_DIR", str(REPO / "data" / "content"))
    test_flat_items_are_untouched()
    test_compound_groups_and_letters()
    test_normalize_options_keeps_every_correct_answer()
    test_the_two_real_items()
    print("test_compound_options: PASS")
