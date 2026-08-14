"""compound_options.py — a compound item's options, split back under their sub-question.

THE PROBLEM, in one line: some listening items ask TWO questions and the schema gives them
ONE `options[]` array. english·secondary's assessment constitution declares
`"label": "A"–"D" (MCQ)` and `what_each_option_reveals` as a flat `{label: sentence}` map,
so two sets cannot both use A–D — a second "A" would collide in that map. The corpus
resolves it with a GROUPED label: "1A".."1D" for sub-question 1, "2A".."2D" for
sub-question 2.

That label is a STORAGE KEY. It is what the reveals map, the correct-answer list and the
choice popup all join on, and it must never reach a teacher — she reads "A", under the
question it belongs to, exactly as on a simple MCQ (founder, 2026-08-14).

WHY THIS IS A DISPLAY RULE AND NOT A SCHEMA. Nesting the options under a typed
`sub_questions[]` field was the alternative. It touches the engine, the view model, three
renderers, the arrangement pass, the three english constitutions and five test files — and
two of its failure modes are silent: an empty top-level `options` makes `LessonView`'s
Answer tab disappear (`itemTabSet`'s hasAnswer), and makes STEP 6 skip the item while
`unarranged()` still reports clean. The grouped label already encodes the grouping
losslessly, so the split can be derived. Deriving it costs one function, expressed twice
(here and as `groupedOptionSets` in LessonView.jsx), and leaves every other item's path
untouched. `assessment_norm.from_constitution` reached the same conclusion for SS
secondary's `sub_questions[]` — fold, don't fork.

THE CONTRACT: returns None for anything that is not compound — a flat A–D list, a
TRUE_FALSE statement list, fewer than two options, or a single group. Callers keep their
existing flat path on None, so this can only change the two items in the corpus that need
it.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

GROUPED_LABEL = re.compile(r"^(\d+)([A-Z])$")


def grouped_option_sets(options: Any) -> Optional[List[Dict[str, Any]]]:
    """[{group, options:[{**opt, display}]}] for a compound item, else None.

    `display` is the letter the teacher reads; the option's own `label` is left alone so
    every label join (reveals, correct answers, popups) still works.
    """
    opts = list(options or [])
    if len(opts) < 2:
        return None
    marks = [GROUPED_LABEL.match(str(o.get("label") or "")) for o in opts]
    if not all(marks):
        return None
    order: List[str] = []
    by: Dict[str, List[Dict[str, Any]]] = {}
    for opt, m in zip(opts, marks):
        group, letter = m.group(1), m.group(2)
        if group not in by:
            by[group] = []
            order.append(group)
        by[group].append({**opt, "display": letter})
    if len(order) < 2:
        return None
    return [{"group": g, "options": by[g]} for g in order]


def display_label(options: Any, label: Any) -> str:
    """The letter to PRINT for a storage label — "C" for "2C" on a compound item, and the
    label unchanged everywhere else."""
    sets = grouped_option_sets(options)
    if not sets:
        return str(label)
    for s in sets:
        for o in s["options"]:
            if str(o.get("label")) == str(label):
                return str(o["display"])
    return str(label)


def group_of(options: Any, label: Any) -> Optional[str]:
    """The sub-question number a storage label belongs to, or None when not compound."""
    sets = grouped_option_sets(options)
    if not sets:
        return None
    for s in sets:
        if any(str(o.get("label")) == str(label) for o in s["options"]):
            return s["group"]
    return None
