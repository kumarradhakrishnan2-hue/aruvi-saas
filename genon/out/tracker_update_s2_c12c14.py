#!/usr/bin/env python3
"""One-shot tracker write: S2 (social_sciences · middle) C12 (founder-verified) and C14.

C13 is deliberately NOT written here — it needs four live break requests that only run on
the founder's machine.

    python3 genon/out/tracker_update_s2_c12c14.py
"""
import json
from pathlib import Path

STATE = Path(__file__).resolve().parents[2] / "data" / "testing" / "campaign_state.json"
NOW = "2026-08-04T22:40:00"


def step(status, comment, by="Claude"):
    return {"status": status, "by": by, "at": NOW, "comment": comment}


C12 = """[e14 2026-08-04 - PASS, VISUALLY VERIFIED BY THE FOUNDER] Kumar opened the view and \
all eight files and confirmed they render correctly. Recorded on his verification, not on a \
Cowork read - the Cowork sandbox cannot open a PDF or a DOCX, so this step is his by \
construction.

SUBJECT: ch_03_60m3-45m9_e14_c20260804162039.json - the mixed-duration plan (60x3 + 45x9 = 12 \
sittings), chosen deliberately because it is the ONLY plan class in this band that carries a \
BORROWED sitting, which C12 requires the export to render: sitting 12 is the TOP canonical's \
`synthesis` unit lending into a p13 plan (mode synthesis, borrowed_from 16, self_fill false).

COVERED: GET /api/plans/.../view, then the three plan exports (lesson | assessment | \
integrated) in both format=pdf and format=docx, plus the allocation report \
(POST /api/allocation/export-pdf and export-docx) for social_sciences/viii = 8 files.

WHAT THE SUBJECT PLAN EXERCISES: SS-middle's stage-grouped view-model shape; a borrowed \
closing sitting reading as a whole unit; two duration classes in one plan (45 and 60, scale \
1.0 / 1.333) with exact band tiling on all 12 sittings; answers=1 rendering the answer layer.

DROPPED-UNIT SPLIT (e09/e13): this plan carries NO drops (uncovered_sections empty), so the \
`dropped_lp` half of the check - unreached units present in /view, paged AFTER the served \
units and visibly unscheduled, and ABSENT from every export - is exercised on the below-floor \
plans (45m9, 1 drop; 45m8, 2 drops) rather than on this one. The code path was confirmed at C9 \
check 3(d): api/main.py:1118 filters `unscheduled` items out of the export while /view keeps \
them via dropped_lp.

TABLE RENDERING - this pass is also the first visual confirmation of the ARV-D-051 fix (ragged \
stimulus tables). The founder-reported Maratha-navy MCQ now renders with its title row as a \
CAPTION above a uniform 3-column grid, in the online view and in PDF and Word alike, because \
the fix lives at the single shared split point (normalize.parse_table) that all four renderers \
consume.

EXIT: 8 files open without error; no blank sections, no raw JSON, unit/phase structure visible \
and matching the plan, the borrowed sitting reading as a whole unit, the answer layer present."""


C14 = """[e14 2026-08-04 - PASS] Run as its own check, NOT mirrored from C13. (Founder asked \
whether C13's record could be reused; it cannot - C13 is failure-path error handling and C14 is \
copyright exposure. They share the artefacts, not the subject matter, and a certification \
register that records evidence for the wrong question is worse than an empty row. Running it \
properly cost one pass, so it was run.)

Campaign reference: docs/NCERT_copyright_review.md v1.1. F1 is closed by founder ruling \
(private personal backup; canonicals-only to cloud; PDFs local forever). F2 - English verbatim \
task-text in served plans - is the sole open finding, and is N/A HERE: it is a property of the \
English inline-substitution conduit, and no SS pipeline carries one.

CHECK 1 - NO VERBATIM TEXTBOOK REPRODUCTION BEYOND SHORT QUOTATION. Measured, not \
eyeballed. Source: textbooks/social_sciences/viii/'chapter 03 - The Rise of the Marathas.pdf' \
extracted with pdftotext (5,569 words, 5,533 10-grams). Every teacher-facing surface of all \
three canonicals was word-normalised and matched against it: activity titles, teacher notes, \
time_bands[].activity, homework, assessment stems, tasks, scaffolds, table/source stimuli and \
MCQ option text.

   ch_03_canonical.json      7,402 plan words | longest verbatim run 10 words | ~33 words in \
any 10-gram match = 0.45% of the plan, 0.59% of the chapter
   ch_03_canonical_p13.json  6,778 plan words | longest verbatim run 14 words | ~37 words = \
0.55% of the plan, 0.66% of the chapter
   ch_03_canonical_p10.json  5,935 plan words | longest verbatim run 10 words | ~10 words = \
0.17% of the plan, 0.18% of the chapter

Every matched run is FACTUAL statement whose phrasing is dictated by the facts - proper nouns, \
dates, geography - not protected expression. The longest (14 words, p13 U10) is \
"the history of the Bhonsle family inscribed on the walls of the Brihadishwara temple". The \
others: "Mocha in Yemen, Muscat in Oman and Malacca in Malaysia", "built and restored hundreds \
of temples, ghats, wells and roads ... from Kedarnath to Rameswaram", "in present-day Tamil \
Nadu in the late 17th century". No continuous run reaches 15 words anywhere in the library and \
total overlap stays under 0.7% of the chapter - de minimis by any reading, and squarely inside \
short quotation. Section-registry anchors are exempt by the step's own terms (structural \
references, not reproduced content).

CHECK 2 - NO THIRD-PARTY COPYRIGHTED MATERIAL. Every quoted run of 12+ words in the three \
canonicals was extracted (54 / 55 / 47 per file) and tested against the textbook. All of them \
are ARUVI'S OWN teacher prompts carried in quotation marks by the LP convention - "What \
geographic feature do you notice about the Maratha homeland?", "The bhakti saints wrote in \
Marathi rather than Sanskrit. What does this choice tell you...?" - i.e. original questions, \
not reproduced content. NO poems, song lyrics, story excerpts, brand text or embedded images \
from outside the textbook anywhere in the library. The table stimuli are Aruvi-composed \
summaries of chapter facts, not lifted tables.

EXIT: no reproduction beyond short quotation; no third-party material; F2 N/A for this \
stage."""


def main():
    st = json.loads(STATE.read_text())
    mid = st["combos"]["social_sciences/middle"]
    mid["C12"] = step("pass", C12, by="Kumar + Claude")
    mid["C14"] = step("pass", C14)
    st["updated_at"] = NOW
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=2))
    print("wrote", STATE)
    for k in ("C12", "C14"):
        print("  social_sciences/middle %s -> %s (%d chars)"
              % (k, mid[k]["status"], len(mid[k]["comment"])))
    print("  steps now:", list(mid))
    print("  STILL OPEN for this stage: C13 (needs four live break requests)")


if __name__ == "__main__":
    raise SystemExit(main())
