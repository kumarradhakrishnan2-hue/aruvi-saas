#!/usr/bin/env python3
"""S11 · ARV-D-138 — close the poem-text conduit. Assessment v1.4 -> v1.5.

WHY. C14 measured the ch 7 library against the extracted NCERT PDF and found it clean:
zero verbatim runs of six words or more in any assessment item, and an EXTRACT_ANALYSIS
stimulus that is verbatim from Aruvi's OWN `prose_summary` (12-word overlap with the
summary, zero 6-word runs shared with the textbook). On a PROSE chapter the conduit is
closed by construction — what reaches the cloud is Aruvi's prose.

On a POEM it is open. Rule 9 permitted the extract block to be copied from `poem_text`,
and `poem_text` is not a paraphrase — it is the poem. Measured on ch 2 'Bharat Our Land':
the summary carries 16 poem lines and 13 of them appear verbatim in the NCERT PDF. So a
poem chapter's item would have placed 3–8 lines of an NCERT-published poem into a
CANONICAL, and canonicals are exactly what the copyright review's v1.1 ruling sends to the
cloud (summaries and PDFs never leave the machine). That is finding F2 of
`docs/NCERT_copyright_review.md`, which C14 exists to police: "the verbatim conduit must
be either closed (substitute a paraphrase + page ref) or licensed before English plans are
served commercially." 8 of english IX's 16 chapters are poems.

THE FIX IS A LOCATOR, NOT A SHORTER QUOTE. The student is holding the textbook; the
stimulus does not have to reproduce the poem to point at it. Five sites, because the
permission was written in five places and three of them are output-facing in ways the
first read missed (Rule 4's type definition carries an "or inline" escape into `item_stem`,
and the schema comment repeats the format list).

WHY THE INCIPIT IS PART OF THE DESIGN, not a hedge (founder, 2026-08-12). NCERT prints NO
line numbers on its poems, and ch 2's stanzas break across a page boundary mid-poem — so
"lines 5–8" alone would have a student counting. A few words of the first line find it at
once. Legally it is the smallest possible quotation: it identifies, it does not
substitute, and it is the convention of every citation index and every exam paper. The
only real risk is drift, so the cap is hard (eight words, one line, no ellipsis, no second
fragment) and stated in the rule rather than left to judgement.

NOT CHANGED: the item type, the item count, the sub-question structure, the cognitive
demand, and the entire prose/drama path. What the generator may READ is also untouched —
INPUTS §2, Rule 2(a) and Rule 6 still name `poem_text` as a content source, because
reading it is what makes a good question possible and the summary never leaves the machine.
Only REPRODUCTION into the artefact is closed.

§9: a constitution change, stage-scoped. It re-authors any poem-chapter library authored
under v1.4 — NONE EXISTS (ch 7 is prose, and it is the only english library on disk), which
is why this is free today and would not be after the first poem chapter is generated.
"""
from __future__ import annotations

import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).resolve().parent
AS = ROOT / "data/content/constitutions/assessment/english/secondary/assessment_constitution.txt"


def sub(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    assert n == 1, f"{label}: expected exactly 1 occurrence, found {n}"
    return text.replace(old, new)


def amend(t: str) -> str:
    # ── header + footer ──────────────────────────────────────────────────────
    t = sub(t, "ARUVI — ENGLISH ASSESSMENT CONSTITUTION · VERSION 1.4 (SECONDARY)",
            "ARUVI — ENGLISH ASSESSMENT CONSTITUTION · VERSION 1.5 (SECONDARY)",
            "header")
    t = sub(t, "English Assessment Constitution · Version 1.4 (Secondary) · Internal Document",
            "English Assessment Constitution · Version 1.5 (Secondary) · Internal Document",
            "footer")

    # ── 1 · Rule 4, the type definition (and its "or inline" escape hatch) ───
    t = sub(t,
            "  EXTRACT_ANALYSIS — [SECONDARY DELTA] a short verbatim extract (passage\n"
            "                 or stanza) from the section, placed in `visual_stimulus`\n"
            "                 (preferred) or inline, followed by 1–3 analytical",
            "  EXTRACT_ANALYSIS — [SECONDARY DELTA] a short extract from the section,\n"
            "                 placed in `visual_stimulus` (preferred) or inline,\n"
            "                 followed by 1–3 analytical",
            "rule 4 · type definition")
    t = sub(t,
            "                 device, meaning) as a numbered list in `item_stem`\n"
            "                 (Rule 9). Mirrors \"Critical Reflection\". OPEN (Rule 5);\n"
            "                 carries `expected_elements`, not `options[]`.",
            "                 device, meaning) as a numbered list in `item_stem`\n"
            "                 (Rule 9). Mirrors \"Critical Reflection\". OPEN (Rule 5);\n"
            "                 carries `expected_elements`, not `options[]`.\n"
            "                 FOR A **POEM** SECTION THE EXTRACT IS NEVER REPRODUCED:\n"
            "                 `visual_stimulus` carries a LOCATOR instead (Rule 9), and\n"
            "                 the \"or inline\" alternative does not apply — a poem's\n"
            "                 lines may not appear in `item_stem` either.",
            "rule 4 · poem branch")

    # ── 2 · Rule 3's REQUIRED list ───────────────────────────────────────────
    t = sub(t,
            "  - a specific line, image, or phrase from poem_text;",
            "  - a specific image, phrase or turn in the poem — IDENTIFIED BY ITS\n"
            "    LOCATION, NOT REPRODUCED: a stanza or line reference plus an incipit\n"
            "    of at most eight words (Rule 9);",
            "rule 3 · required list")

    # ── 3 · Rule 9's opening sentence ────────────────────────────────────────
    t = sub(t,
            "`visual_stimulus` is non-empty only for tabular data grounded in the\n"
            "section, OR [SECONDARY DELTA] for an EXTRACT_ANALYSIS verbatim extract.",
            "`visual_stimulus` is non-empty only for tabular data grounded in the\n"
            "section, OR [SECONDARY DELTA] for an EXTRACT_ANALYSIS extract block\n"
            "(prose · drama) or LOCATOR (poem).",
            "rule 9 · opening")

    # ── 4 · Rule 9's permitted-formats bullet, split in two ──────────────────
    t = sub(t,
            "  - Verbatim extract block [SECONDARY DELTA]: a short passage/stanza copied\n"
            "    verbatim from prose_/drama_summary / poem_text, plain lines (no \"|\"),\n"
            "    3–8 lines. Used by EXTRACT_ANALYSIS.",
            "  - Verbatim extract block [SECONDARY DELTA] — PROSE · DRAMA · NARRATIVE ·\n"
            "    INFORMATIONAL ONLY: a short passage copied verbatim from\n"
            "    `prose_summary` / `drama_summary`, plain lines (no \"|\"), 3–8 lines.\n"
            "    Used by EXTRACT_ANALYSIS. (This is the summary's own prose, written for\n"
            "    Aruvi, which is what makes reproducing it safe.)\n"
            "  - Poem locator [SECONDARY DELTA] — the ONLY permitted form for a POEM\n"
            "    section: ONE line, in the shape\n"
            "        Read lines N–M on p.PP, beginning \"<incipit>\".\n"
            "    The incipit is AT MOST EIGHT WORDS, taken from the first line of the\n"
            "    span, in double quotes, with NO ellipsis and NO second fragment. Where\n"
            "    the printed stanzas are a clearer address than a line count, use\n"
            "    \"the second stanza on p.PP\" instead — NCERT prints no line numbers,\n"
            "    and a stanza may break across a page.\n"
            "    THE POEM'S LINES ARE NOT COPIED — not into `visual_stimulus`, not into\n"
            "    `item_stem`, not into `suggested_answer`, not into `expected_elements`.\n"
            "    The student reads them in her own textbook; the incipit is there to\n"
            "    find them, not to replace them.",
            "rule 9 · permitted formats")

    # ── 5 · the schema comment ───────────────────────────────────────────────
    t = sub(t,
            '          "visual_stimulus":      string,   // "" | pipe-table | verbatim\n'
            "                                            // extract block (EXTRACT_ANALYSIS)",
            '          "visual_stimulus":      string,   // "" | pipe-table | extract\n'
            "                                            // block (prose/drama) | poem\n"
            "                                            // LOCATOR (Rule 9)",
            "schema comment")
    return t


def main() -> None:
    pre = AS.read_text(encoding="utf-8")
    shutil.copyfile(AS, OUT / "assessment_constitution_v1.4_pre_poem_locator.txt")
    AS.write_text(amend(pre), encoding="utf-8")
    now = AS.read_text(encoding="utf-8")

    # ── guards · the conduit must be shut, and only where it was open ────────
    assert "copied\n    verbatim from prose_/drama_summary / poem_text" not in now
    assert now.count("poem_text") == 3, (
        "poem_text must survive in exactly the three READ sites (INPUTS §2, Rule 2(a), "
        f"Rule 6) and nowhere else — found {now.count('poem_text')}")
    for read_site in ("`poem_text` +\n   `poem_appreciation_summary` (poem). These are the "
                      "content sources.",
                      "`drama_summary` / `poem_text` + `poem_appreciation_summary`. Exception:",
                      "`drama_summary` (or `poem_text` + `poem_appreciation_summary`)."):
        assert read_site in now, f"a READ site was damaged: {read_site[:50]}"
    assert now.count("Poem locator [SECONDARY DELTA]") == 1
    assert now.count("AT MOST EIGHT WORDS") == 1
    assert now.count("THE POEM'S LINES ARE NOT COPIED") == 1
    assert now.count("VERSION 1.5 (SECONDARY)") == 1
    assert now.count("Version 1.5 (Secondary)") == 1
    # nothing about the prose path moved
    assert "3–8 lines.\n    Used by EXTRACT_ANALYSIS." in now
    print("assessment v1.4 -> v1.5 · the poem conduit is closed; the three read sites stand")


if __name__ == "__main__":
    main()
