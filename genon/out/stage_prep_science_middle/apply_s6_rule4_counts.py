#!/usr/bin/env python3
"""S6 · science · middle — assessment constitution v1.4 -> v1.5 (ARV-D-065, C3 defect).

THE DEFECT. Rule 4's per-stage item minimums sum to 15 (2 first + 3+3+3 middle + 4 final).
The pilot library produced 13, 15, 14, 12 — three of four canonicals short, and the WORST
offender was the 12-unit top, which had the most room. So it is not a room problem: the
mandated minimum sits at the very top of the model's natural range, leaving zero slack, and
compliance became a question of whether a run happened to reach its own ceiling.

WHY THE MODEL IS NOT BOUND. `grep -ci "must.*at least|must.*minimum"` over v1.4 returns 0.
The minimums exist ONLY as a column header ("Minimum") inside a whitespace-aligned sub-table
nested inside a cell of the outer ASCII table. No sentence containing MUST states a count.
The two MUST sentences in Rule 4 govern something else entirely — question FORMAT, and
stage-label leakage. A model emitting two items in a middle stage has broken no mandate; it
has under-filled a table column.

AND ONE SENTENCE WORKS AGAINST IT. The MANDATE, two lines above a table of fixed integers,
reads "Stage position is a relational test — never a fixed integer. Assessment length is
uncapped." In context that is about `stage_position` being relational rather than hardcoded.
Next to that table it reads as licence on counts.

THE THREE EDITS (founder, 2026-08-07):
  1. State the counts as MUST prose in the MANDATE. The table stays as the summary, never
     as the source.
  2. Re-scope "never a fixed integer" so it cannot be read as governing counts, and move
     "uncapped" next to an explicit floor so the two are read together.
  3. Add an under-count PROHIBITION — the gap that let this pass silently.
(The third change, adding science·middle to EXACT_ITEM_COUNTS in genon/build_library.py, is
applied separately in that file so C5's advisory measures against the constitution rather
than the library's own modal count.)

Run from the repo root:
    python3 genon/out/stage_prep_science_middle/apply_s6_rule4_counts.py
"""
from __future__ import annotations

import difflib
import pathlib
import re
import textwrap

ROOT = pathlib.Path(__file__).resolve().parents[3]
PREP = ROOT / "genon/out/stage_prep_science_middle"
AS = ROOT / "data/content/constitutions/assessment/science/middle/assessment_constitution.txt"

pre = AS.read_text(encoding="utf-8")
PREP.joinpath("assessment_constitution_v1.4_pre.txt").write_text(pre, encoding="utf-8")
a = pre


def sub(text, old, new, what):
    n = text.count(old)
    assert n == 1, f"{what}: expected exactly 1 occurrence, found {n}"
    return text.replace(old, new)


a = sub(a, "Version 1.4 · Ten rules", "Version 1.5 · Ten rules", "VERSION")

# ── the Rule 4 table: rebuild the MANDATE and PROHIBITION cells on its own geometry ──
lines = a.split("\n")
sep_i = next(i for i, ln in enumerate(lines)
             if ln.startswith("+---") and "Rule 4" in lines[i + 1])
sep = lines[sep_i]
lc = sep.index("+", 1) - 1
rc = len(sep) - lc - 3


def row(label, text):
    out = "|" + (" " + label).ljust(lc) + "|" + (" " + text).ljust(rc) + "|"
    assert len(out) == len(sep), f"geometry {len(out)} != {len(sep)}"
    return out


def para(text, label=""):
    w = textwrap.wrap(text, rc - 2)
    return [row(label if i == 0 else "", ln) for i, ln in enumerate(w)]


# EDIT 1+2 — replace the MANDATE's opening sentence with count prose.
old_open = ("The system MUST structure the assessment using progression stage position as "
            "the sole architectural governor. Stage position is a relational test — never a "
            "fixed integer. Assessment length is uncapped.")
hits = [i for i, ln in enumerate(lines) if old_open in re.sub(r"\s+", " ", ln)]
assert len(hits) == 1, f"MANDATE opening: found {len(hits)}"
i = hits[0]
new_cells = (
    para("The system MUST structure the assessment using progression stage position as the "
         "sole architectural governor. Stage position is a RELATIONAL test — it is computed "
         "against total_stages and is never hardcoded to a particular stage number. That "
         "relational rule governs POSITION only; the item counts below are fixed minimums "
         "and are not subject to it.", "MANDATE")
    + [row("", "")]
    + para("PER-STAGE MINIMUMS — these are floors, and every one of them MUST be met in "
           "every stage of every assessment:")
    + [row("", "")]
    + para("· The FIRST stage MUST carry at least 2 MCQs.")
    + para("· EVERY MIDDLE stage MUST carry at least 2 MCQs AND at least 1 SCR. A middle "
           "stage with fewer than 3 items is non-compliant, however few periods it spans — "
           "item count is set by stage POSITION, never by how many periods the stage was "
           "given in the lesson plan.")
    + para("· The FINAL stage MUST carry at least 2 MCQs AND at least 1 ECR AND exactly 1 "
           "Open Task.")
    + [row("", "")]
    + para("So an assessment over N stages carries at least 2 + 3(N-2) + 4 items. Assessment "
           "length is uncapped ABOVE these floors: more than the minimum is always "
           "acceptable, fewer never is. Count the items per stage before emitting, and if a "
           "stage is short, add items rather than redistributing them.")
    + [row("", "")]
)
lines[i:i + 1] = new_cells

# EDIT 3 — the missing under-count prohibition, added to Rule 4's PROHIBITION cell.
anchor = "The system MUST NOT derive question format from the implied LO type."
hits = [i for i, ln in enumerate(lines) if anchor in re.sub(r"\s+", " ", ln)]
assert len(hits) == 1, f"PROHIBITION anchor: found {len(hits)}"
i = hits[0]
lines[i + 1:i + 1] = ([row("", "")] + para(
    "The system MUST NOT emit fewer items than the per-stage minimums above, and MUST NOT "
    "trade a shortfall in one stage against a surplus in another — the minimums are per "
    "stage, not per assessment. The system MUST NOT use a question type outside the set its "
    "stage position allows (no ECR or Open Task in a middle stage)."))
a = "\n".join(lines)

# ── assertions: the defect's own signature must now be absent ────────────────────
flat = re.sub(r"\s+", " ", a)
assert "never a fixed integer" not in flat, "the licence phrasing survived"
assert flat.count("MUST carry at least 2 MCQs AND at least 1 SCR") == 1
assert "MUST NOT emit fewer items than the per-stage minimums" in flat
assert "2 + 3(N-2) + 4" in flat
for old in ("MUST NOT place the correct answer", "alphabetically", "never led with"):
    assert old not in a, f"an earlier amendment regressed: {old}"
assert "Option order carries no meaning" in flat and "by its label" in flat, "A9 lost"
assert "ANCHORING IS DERIVED" in a, "A6 integrity block lost"
# Rule 4's OWN table only: from its opening separator to the closing one. (An earlier
# version of this assertion used a fixed +40 window, which after the insertions ran past
# the end of Rule 4 and into Rule 5's table — a different width, and a false alarm.)
_ls = a.split("\n")
_end = sep_i + 1
_seps = 0
while _end < len(_ls) and _seps < 3:
    _end += 1
    if _ls[_end].startswith("+---"):
        _seps += 1
w = {len(ln) for ln in _ls[sep_i:_end + 1] if ln.startswith(("|", "+"))}
assert w == {len(sep)}, f"Rule 4 table geometry broke: widths {w} vs sep {len(sep)}"

AS.write_text(a, encoding="utf-8")
d = difflib.unified_diff(pre.split("\n"), a.split("\n"),
                         fromfile="assessment_constitution.txt (v1.4)",
                         tofile="assessment_constitution.txt (v1.5)", lineterm="")
PREP.joinpath("assess_v1.4_to_v1.5.diff").write_text("\n".join(d) + "\n", encoding="utf-8")
print("assessment constitution -> v1.5; diff at assess_v1.4_to_v1.5.diff")
