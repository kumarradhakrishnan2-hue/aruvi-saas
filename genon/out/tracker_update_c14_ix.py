#!/usr/bin/env python3
"""Fill SS·secondary (class IX ch 3) C14 with the MEASURED copyright evidence — the row was
ticked pass on 2026-08-04 with an EMPTY comment, i.e. a verdict with no evidence behind it.

    python3 genon/out/tracker_update_c14_ix.py
"""
import json
from pathlib import Path

STATE = Path(__file__).resolve().parents[2] / "data" / "testing" / "campaign_state.json"
NOW = "2026-08-04T23:40:00"

C14 = """[e14 2026-08-04 - PASS, MEASURED] Backfilled evidence: this row was ticked pass \
earlier today with an EMPTY comment field. Same method as SS-middle's C14 - the check is \
measured against the actual textbook, not eyeballed - so the two stages are comparable.

Campaign reference: docs/NCERT_copyright_review.md v1.1. F1 closed by founder ruling (private \
personal backup; canonicals-only to cloud; PDFs local forever). F2 - English verbatim task-text \
in served plans - is N/A here: it is a property of the English inline-substitution conduit and \
no SS pipeline carries one.

CHECK 1 - NO VERBATIM TEXTBOOK REPRODUCTION BEYOND SHORT QUOTATION.
Source: textbooks/social_sciences/ix/'chapter 03 - Atmosphere and Climate.pdf' extracted with \
pdftotext (6,037 words, 6,019 10-grams). Every teacher-facing surface of all three canonicals \
word-normalised and matched: activity titles, teacher notes, band text, homework, assessment \
stems, tasks, scaffolds, sub-questions, table/source stimuli and MCQ option text.

   ch_03_canonical.json      5,455 plan words | longest verbatim run 12 words | ~12 words \
matched = 0.22% of the plan, 0.20% of the chapter | 1 distinct run
   ch_03_canonical_p10.json  5,415 plan words | longest verbatim run 12 words | ~34 words \
matched = 0.63% of the plan, 0.56% of the chapter | 2 distinct runs
   ch_03_canonical_p07.json  4,487 plan words | longest verbatim run  0 words | ZERO overlap \
at 10 words or more - not one matching run in the whole file

Both distinct runs are FACTUAL enumeration whose wording is dictated by the facts, not \
protected expression:
   (a) "carbon dioxide, argon, helium, neon, krypton, xenon, ozone and hydrogen in smaller \
quantities, plus water vapour" - a list of gases; there is no other order or phrasing available.
   (b) "reducing carbon footprints, using renewable energy, protecting forests and adopting \
sustainable lifestyles" - the chapter's own four mitigation measures, named.
Nothing reaches 13 continuous words anywhere in the library and total overlap stays at or below \
0.56% of the chapter. De minimis, and squarely inside short quotation. Section-registry anchors \
are exempt by the step's own terms.

Comparative note: SS-IX is CLEANER than SS-VIII on the same measure (longest run 12 vs 14 \
words; the 7-period compact carries literally zero). Both are far inside the line, but the \
figures are now on record so a future stage that drifts is visible against them.

CHECK 2 - NO THIRD-PARTY COPYRIGHTED MATERIAL. Every quoted run of 12+ words was extracted \
(23 / 22 / 41 per file) and tested against the textbook. All are ARUVI'S OWN teacher prompts \
and notes carried in quotation marks by the LP convention - "Why does a small change in water \
vapour matter far more than its percentage suggests?", "Why does the thermosphere heat up even \
though it is very thin?" - original questions, not reproduced content. NO poems, song lyrics, \
story excerpts, brand text or embedded outside images anywhere in the library.

THE STIMULI CHECKED SEPARATELY, because a SOURCE_INTERPRETATION stimulus is the highest-risk \
surface in the whole artefact - it is the one field whose PURPOSE is to put source material in \
front of a student. All five typed table stimuli across the three files score ZERO 8-gram hits \
against the textbook: the atmospheric-composition tables (Q3 in each file), the Punjab-floods \
cause/effect table (top Q11) and the carbon-footprint audit table (p10 Q14) are Aruvi-composed \
arrangements of chapter facts, not lifted tables. The atmospheric figures are re-tabulated from \
Fig. 3.2 with our own column labels; the attribution lines ('- Adapted from Fig. 3.2, Chapter \
3') name the source and are now rendered as a source note beneath the table rather than as a \
broken row (ARV-D-051).

EXIT: no reproduction beyond short quotation; no third-party material; F2 N/A for this stage."""


def main():
    st = json.loads(STATE.read_text())
    sec = st["combos"]["social_sciences/secondary"]
    before = len(sec["C14"].get("comment") or "")
    sec["C14"] = {"status": "pass", "by": "Kumar + Claude", "at": NOW, "comment": C14}
    st["updated_at"] = NOW
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=2))
    print("wrote", STATE)
    print("  social_sciences/secondary C14 -> pass  (comment %d -> %d chars)"
          % (before, len(C14)))
    mid = st["combos"]["social_sciences/middle"]["C14"]
    print("  social_sciences/middle    C14 -> %s (comment %d chars, unchanged)"
          % (mid["status"], len(mid["comment"])))


if __name__ == "__main__":
    raise SystemExit(main())
