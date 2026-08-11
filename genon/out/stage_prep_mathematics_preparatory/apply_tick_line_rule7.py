#!/usr/bin/env python3
"""Rule 7's `number_line:` becomes a TICK LINE — labels may be words, not only numbers.

Maths preparatory + middle assessment constitutions, 2026-08-11, founder-directed at S8's C4.

WHY. Rule 7 admitted `number_line:` so a real number line had somewhere legal to go instead of
being faked as a header-less pipe table (MEMORY item 14). Its first live exercise, maths III
ch 5 Q-C-4, used it for an alternating SHAPE pattern — `number_line: line | curve | line |
curve | ... ` — which is genuinely the right picture for "draw the next two repeat units", and
which the rule as written forbade ("each cell a number ... endpoints must be numbers").

The founder's ruling (2026-08-11) is that the tick line IS the better representation here, so
the rule follows the practice rather than the other way round. Without this edit every future
generation doing the wanted thing is technically in breach and C3 re-raises it at every chapter.

WHAT ELSE MOVED, so this text is not the only thing holding it up:
  * `assessment_norm._nl_block` now validates STRUCTURE (single row, >=3 cells, short labels)
    instead of cell TYPE. The numeric test predated the tag, from when typing had to be guessed
    from a bare pipe row; once intent is declared, re-deriving it from the cells is redundant.
  * a tagged stimulus that fails the contract no longer degrades silently into a TABLE with the
    tag visible — the tag is stripped and a single row falls to prose (ARV-D-113: the teacher
    was shown the literal token "number_line: line").
  * `build_library.py` gained a DECLARED-TYPE GATE, so a mis-tagged stimulus stops the run.
    That is the part that makes this a guarantee rather than a convention.

§9: RELAXATION-ONLY. Every edit widens — a form is permitted that was not, nothing is
tightened, no obligation is created (`MUST NOT`/`PROHIBITED` counts asserted unchanged). Output
authored under the old text satisfies the new text by construction: a numeric tick line is
still a tick line. maths·middle's library (ch 7) and maths·preparatory's (ch 5) therefore do
NOT re-author. Neither carries a non-numeric tag today anyway — ch 5's Q-C-4 is the only tagged
stimulus in either, and under the amended engine it now resolves as intended.
"""
from __future__ import annotations

import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).resolve().parent
C = ROOT / "data/content/constitutions/assessment/mathematics"

NEW = """- Tick line (tagged `number_line:`): one line tagged `number_line:` then the
  ticks split by "|". Each cell is either a LABEL — a number, or a short word
  naming what sits at that tick — or "..." (a blank tick the student fills in).
  At least three cells; a label is a label, not a sentence. The ticks are drawn
  as an ordered line, never as a grid.
    numbers:  `number_line: {NUMERIC}`
    words:    `number_line: {WORDY}`
  Keep the task wording in `prompt`. Do not emit a tick line as a pipe-table,
  and do not tag a pipe-table as a tick line: a stimulus that declares this tag
  and does not satisfy it is rejected at certification and renders as plain
  prose, losing the picture it asked for.
"""

JOBS = [
    ("preparatory", "1.3", "1.4",
     "Mathematics Assessment Constitution (Preparatory) · Version {v} · Internal Document",
     "200 | ... | ... | ... | 260", "line | curve | line | curve | ... | ...",
     """- Number line: one line tagged `number_line:` then the ticks split by "|",
  each cell a number (labelled tick) or "..." (blank tick the student marks);
  endpoints must be numbers. E.g. `number_line: 200 | ... | ... | ... | 260`.
  Keep the task wording in `prompt`. Do not emit a number line as a pipe-table.
"""),
    ("middle", "3.4", "3.5",
     "Mathematics Assessment Constitution · Version {v} · Internal Document",
     "-3 | ... | 0 | ... | 3", "shorter | ... | ... | longer",
     """- Number line: one line tagged `number_line:` then the ticks split by "|",
  each cell a number (labelled tick) or "..." (blank tick the student marks);
  endpoints must be numbers. E.g. `number_line: -3 | ... | 0 | ... | 3`.
  Keep the task wording in `prompt`. Do not emit a number line as a pipe-table.
"""),
]


def sub(text, old, new, label):
    n = text.count(old)
    assert n == 1, f"{label}: expected exactly 1 occurrence, found {n}"
    return text.replace(old, new)


def main() -> int:
    for stage, oldv, newv, footer, numeric, wordy, old_block in JOBS:
        p = C / stage / "assessment_constitution.txt"
        t0 = t = p.read_text(encoding="utf-8")
        shutil.copy2(p, OUT / f"assess_{stage}_v{oldv}_pre_tickline.txt")

        assert f"VERSION {oldv}" in t.splitlines()[0], \
            f"{stage}: head is {t.splitlines()[0]!r}, expected VERSION {oldv}"
        t = sub(t, f"VERSION {oldv}", f"VERSION {newv}", f"{stage} version")
        t = sub(t, old_block,
                NEW.replace("{NUMERIC}", numeric).replace("{WORDY}", wordy),
                f"{stage} Rule 7 tick line")
        t = sub(t, footer.format(v=oldv), footer.format(v=newv), f"{stage} footer")

        # ── guards ──────────────────────────────────────────────────────────
        assert "endpoints must be numbers" not in t, f"{stage}: the numeric mandate survived"
        assert "each cell a number (labelled tick)" not in t, f"{stage}: old cell rule survived"
        assert "or a short word" in t, f"{stage}: the widening did not land"
        assert "rejected at certification" in t, f"{stage}: the gate is not referenced"
        for k in ("MUST NOT", "PROHIBITED"):
            assert t.count(k) == t0.count(k), \
                f"{stage}: {k} count moved — this must stay RELAXATION-ONLY (§9)"
        assert "inline SVG" in t or "PROHIBITED" in t, f"{stage}: the SVG prohibition was disturbed"
        p.write_text(t, encoding="utf-8")
        print(f"  mathematics/{stage:<12} assessment v{oldv} -> v{newv}")
    print("\n2 constitutions amended; relaxation-only, no library re-authors.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
