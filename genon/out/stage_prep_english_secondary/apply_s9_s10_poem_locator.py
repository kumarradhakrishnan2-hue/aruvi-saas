#!/usr/bin/env python3
"""S9 + S10 — carry the poem locator into english preparatory and middle (ARV-D-138).

Assessment  preparatory  v1.2 -> v1.3   ·   middle  v3.4 -> v3.5

WHY, in one line: `poem_text` is the NCERT poem, and an item that reproduces it puts
published verse into a canonical — the one artefact class that goes to the cloud. Measured
at S11's C14 on english IX ch 2: 13 of the summary's 16 poem lines appear verbatim in the
textbook PDF. Finding F2 of `docs/NCERT_copyright_review.md`.

**THE EDIT IS SMALLER HERE THAN AT SECONDARY, AND THE READING IS WHY.** Secondary's Rule 9
carries an EXTRACT_ANALYSIS "verbatim extract block, 3–8 lines", which was the sharp end of
the conduit and needed five edit sites to close. NEITHER of these two stages has that block:
preparatory's `visual_stimulus` is `"" | pipe-table` and does not carry EXTRACT_ANALYSIS at
all; middle's is `"" | pipe-table` likewise. So the only open door is Rule 3's REQUIRED
line — "a specific line, image, or phrase from `poem_text`" — which invites an item to
quote the poem into `item_stem`, where nothing caps it.

Two edits per file, therefore, not five:
  1. Rule 3 REQUIRED  — the poem is addressed by LOCATION, not reproduced.
  2. Rule 3 PROHIBITED — a positive ban on reproducing the lines, with the incipit cap,
     because a REQUIRED clause tells a model what it may do and a PROHIBITED clause is what
     it checks itself against.

**PREPARATORY ALREADY HAS THE DOCTRINE, WRITTEN FOR PICTURES**, and the poem clause is
deliberately phrased to echo it rather than to import secondary's wording: "do NOT introduce
a separate visual format. Instead, reference the textbook page in `item_stem` itself — 'Look
at the picture on Textbook page 6…'. The teacher has the book; the image lives there." The
same sentence, applied to verse, is the whole amendment.

READING IS UNTOUCHED at both stages. INPUTS, the grounding rule and the verification rule
still name `poem_text` as a content source — reading the poem is what makes a good question
possible, and the summary never leaves the machine. Only reproduction into the artefact is
closed.

§9: a constitution change at two stages, and it re-authors NOTHING — neither stage has a
library, or a canonical, or a certified chapter. Both are pre-C1. This is exactly the window
S11's C14 named: free before the first poem chapter is authored, ~₹80 a library afterwards.
"""
from __future__ import annotations

import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).resolve().parent
PREP = ROOT / "data/content/constitutions/assessment/english/preparatory/assessment_constitution.txt"
MID = ROOT / "data/content/constitutions/assessment/english/middle/assessment_constitution.txt"


def sub(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    assert n == 1, f"{label}: expected exactly 1 occurrence, found {n}"
    return text.replace(old, new)


# The locator, worded once and shared — the cap is the load-bearing part.
_LOCATOR = ('a stanza or line reference plus\n'
            '    an incipit of AT MOST EIGHT WORDS in double quotes — e.g.\n'
            '    Read the lines on page 42 beginning "The mighty mountains stand".')


def amend_prep(t: str) -> str:
    t = sub(t, "ARUVI — ENGLISH ASSESSMENT CONSTITUTION · PREPARATORY · VERSION 1.2",
            "ARUVI — ENGLISH ASSESSMENT CONSTITUTION · PREPARATORY · VERSION 1.3",
            "prep header")
    t = sub(t, "English Assessment Constitution · Preparatory · Version 1.2",
            "English Assessment Constitution · Preparatory · Version 1.3",
            "prep footer")
    t = sub(t,
            "  - A specific line, image, or phrase from `poem_text`.",
            "  - A specific image, sound-pattern or phrase in the poem — ADDRESSED\n"
            "    BY ITS PLACE, NOT COPIED OUT: " + _LOCATOR,
            "prep · rule 3 required")
    t = sub(t,
            "Prohibited:\n"
            "  - Stems answerable without reading the section.\n"
            "  - Stems recycled from textbook exercise wording.",
            "Prohibited:\n"
            "  - Stems answerable without reading the section.\n"
            "  - Stems recycled from textbook exercise wording.\n"
            "  - REPRODUCING THE POEM. A poem's lines are not copied into\n"
            "    `item_stem`, `visual_stimulus`, `suggested_answer` or any rubric\n"
            "    field — beyond the eight-word incipit that locates them, and never\n"
            "    with an ellipsis continuing the quotation. The child is holding the\n"
            "    book; the poem lives there, exactly as a textbook picture does\n"
            "    (Rule 9).",
            "prep · rule 3 prohibited")
    return t


def amend_mid(t: str) -> str:
    t = sub(t, "ARUVI — ENGLISH ASSESSMENT CONSTITUTION · VERSION 3.4",
            "ARUVI — ENGLISH ASSESSMENT CONSTITUTION · VERSION 3.5",
            "middle header")
    t = sub(t, "English Assessment Constitution · Version 3.4 · Internal Document",
            "English Assessment Constitution · Version 3.5 · Internal Document",
            "middle footer")
    t = sub(t,
            "  - A specific line, image, or phrase from poem_text.",
            "  - A specific image, phrase or turn in the poem — ADDRESSED BY ITS\n"
            "    PLACE, NOT COPIED OUT: " + _LOCATOR,
            "middle · rule 3 required")
    t = sub(t,
            "PROHIBITED:\n"
            "  - Stems that could be answered without reading the section\n"
            "    (e.g., \"What is the main idea?\" with no section-specific anchor).\n"
            "  - Stems recycled from textbook exercise wording or question_bank entries.",
            "PROHIBITED:\n"
            "  - Stems that could be answered without reading the section\n"
            "    (e.g., \"What is the main idea?\" with no section-specific anchor).\n"
            "  - Stems recycled from textbook exercise wording or question_bank entries.\n"
            "  - REPRODUCING THE POEM. A poem's lines are not copied into `item_stem`,\n"
            "    `visual_stimulus`, `suggested_answer` or any rubric field — beyond the\n"
            "    eight-word incipit that locates them, and never with an ellipsis\n"
            "    continuing the quotation. The student is holding the book; the poem\n"
            "    lives there, and the item's work is the analysis, not the transcription.",
            "middle · rule 3 prohibited")
    return t


def main() -> None:
    for path, pre_name, fn, stage in (
            (PREP, "assess_english_preparatory_v1.2_pre.txt", amend_prep, "preparatory"),
            (MID, "assess_english_middle_v3.4_pre.txt", amend_mid, "middle")):
        pre = path.read_text(encoding="utf-8")
        shutil.copyfile(path, OUT / pre_name)
        path.write_text(fn(pre), encoding="utf-8")
        now = path.read_text(encoding="utf-8")
        # guards · the door is shut, the reading is not
        assert "specific line, image, or phrase from" not in now, \
            f"{stage}: the REQUIRED line still invites a quotation"
        assert now.count("REPRODUCING THE POEM") == 1, stage
        assert now.count("AT MOST EIGHT WORDS") == 1, stage
        # the READ sites must survive untouched
        assert now.count("poem_appreciation_summary") >= 2, \
            f"{stage}: a read site was damaged"
        assert "poem_text" in now, f"{stage}: reading poem_text must stay legal"
        print(f"{stage}: poem conduit closed · read sites intact "
              f"({now.count('poem_text')} poem_text mentions remain)")


if __name__ == "__main__":
    main()
