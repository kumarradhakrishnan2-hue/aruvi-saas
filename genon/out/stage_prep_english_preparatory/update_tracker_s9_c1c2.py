#!/usr/bin/env python3
"""S9 · english · preparatory — write C1 and C2 into the campaign tracker state.

Run from the repo root:
    python3 genon/out/stage_prep_english_preparatory/update_tracker_s9_c1c2.py

Cost table artefact: genon/out/stage_prep_english_preparatory/C2_cost_english_iii_ch11.md
Certification report: genon/out/library_reports/english_iii_ch11_20260813_124746.md
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/preparatory"

ROWS = {
    "C1": ("pass", "Kumar", """LIBRARY BUILT AND CERTIFIED 2026-08-13. english III ch 11 'The Big Laddoo' - counts [12, 10, 7], three canonicals, run as 'python3 genon/build_library.py english iii 11 --top-only' then resumed without the flag. Report: genon/out/library_reports/english_iii_ch11_20260813_124746.md - DETERMINISTIC CHECKS ALL PASS, zero failures, zero quarantines.

BOTH EXIT CRITERIA MET.
(1) The library on disk matches canonical_plan.counts: ch_11_canonical.json (12) + ch_11_canonical_p10.json (10) + ch_11_canonical_p07.json (7), and the row finalized to provisional false / basis authored_standard / registry_sections 5 / authored [12].
(2) GET /genon/english/iii/chapters returns chapters [11], canonical_minutes {11: 480}, canonical_periods {11: 12} - and 480 = 40 x 12, the standard duration from standard_duration_minutes('iii','english') times the top period count. Verified through api.data's own genon_chapters / load_genon_canonical (fastapi is not installed in the Cowork sandbox, so the route body was executed directly rather than over HTTP; identical code path).

WHAT THE CERTIFIER PASSED, and it includes every gate this stage's P-prep was built to test.
- CHECK 11 (the summary reconciliation, new at template v2.10, and GATING for english because its summaries declare sections in JSON main_sections[]): 5 summary sections vs 5 registry entries, every one anchored.
- THE SYNTHESIS GATE: the standard closes with the mandated synthesis unit and carries the token nowhere else; both compacts have it reserved away from them. Coverage reaches the final registry section BEFORE the synthesis unit (first visits land at units 1, 3, 5, 7, 9 - all well inside 1..11).
- REGISTRY DISCIPLINE ACROSS THE LIBRARY: every anchor verbatim in the top registry in all three files, and first-visit order follows the registry in all three - reading > oracy > writing > word_work > beyond_text, IDENTICAL in the 12, the 10 and the 7. That is the property the Xth-unit choice set depends on.
- THE REGISTER: 0 ban hits in all three files, with the scan confirmed to have REACHED the text (49 / 50 / 34 bands read, plus activity_title, materials, teacher_notes and homework). An independent scan of the same surfaces agreed: 0 hits on clock quantity, 0 on forward reference or completion, 0 on calendar time.
- THE SERVE SWEEP, X=5 to 14: choice set non-empty at every X, NO DEFENSIVE TRUNCATION anywhere. Modes: 5 'fill/single -1s' . 6 'fill/single -1s' . 7 IDENTITY . 8 'rescue/complete (from 10)' . 9 'fill/single' . 10 IDENTITY . 11 'synthesis' . 12 IDENTITY . 13-14 surrender. Only the two below-floor asks (X=5, 6) drop a section, which is specified behaviour below the lowest canonical.

THE PAIR HELD AT EVERY PERIOD COUNT - 10 ITEMS IN ALL THREE FILES, 5 cells x 2. This is the first english library authored under the corrected prompt builder (the ARV-D-144 fix landed at this stage's P-prep, hours earlier: the builder had said 'one item per cell' while citing Rule 2), and it settles the question the fix opened - the model produced the PAIR at 12, at 10 and at 7. It also proves assessment v1.4's invariance line LIVE: 'the item count does not vary with the period count'. Every pair differs on type, and the slot table is respected throughout - slot 1 recognition (MCQ / TRUE_FALSE / FILL_IN / MATCH), slot 2 short production (SCR / ORAL_PROMPT / WRITING_TASK).

FULL SPINE COVERAGE HELD AT THE FLOOR. All 5 summary cells are carried in all three canonicals, INCLUDING the 7-period compact - zero drops. That is the rule that replaced Rule 2 STEP 3's drop licence at P1, tested where it binds hardest: the preparatory corpus's own saved plan (iii ch 1) carries 3 of 5 cells under the OLD rule, and the new one is what stops a compact being a different chapter from its standard.

A1 HELD: period_rows_snapshot is a single {40, 12} row, every unit of every file is at 40 minutes, and time_bands tile 0..40 EXACTLY in all 29 units across the three files - no gaps, no overlaps, no overrun. The 'phases' key appears nowhere (P3's conversion, proved by generation rather than by grep).

A9 GOT ITS LIVE EVIDENCE, AND IT IS EMPHATIC. STEP 6 re-ordered 4 of 6 items on the first pass (the top's 2 were sorted on the earlier --top-only certify run). Across the whole library the correct option was authored at position B in FIVE OF FIVE MCQ/TRUE_FALSE items - top #1, p07 #1, p07 #3, p10 #1, p10 #3 - and the sort scattered them to C, D, B, C, B. This is exactly what A9 predicts and why the MEMORY item-18 position prohibition was removed rather than ported: the model cannot produce the randomness that rule asked for, and the deterministic sort is the only thing that does. Guide keys (what_each_option_reveals) remapped correctly to the three non-correct labels in every case.

Ledger: 3 generations, 3 ledger files, 3 installed canonicals, no reruns, no quarantines. See C2 for the cost."""),

    "C2": ("pass", "Claude", """LIBRARY COST Rs 63.86 - CLEAN PATH = ALL-IN, no reruns. Full table: genon/out/stage_prep_english_preparatory/C2_cost_english_iii_ch11.md

Every runtime_data/token_log.csv row for (english, iii, 11) is attributed; no cell is missing.
  12:36:10  canonical_generation  top 12u   in 19,734  out 11,739  total 31,473  Rs 21.6464
  12:45:08  variant_generation    p10 10u   in 19,659  out 12,615  total 32,274  Rs 22.8346
  12:47:45  variant_generation    p07  7u   in 19,659  out 10,113  total 29,772  Rs 19.3818
  LIBRARY TOTAL                             in 59,052  out 34,467  total 93,519  Rs 63.8628

BOTH FIGURES ARE THE SAME because nothing was rerun or superseded: 3 log rows, 3 ledger files in genon/out/canonical/english/iii/, 3 installed canonicals. The two promptdump.json files are the P-prep dry runs and cost Rs 0. Mean Rs 21.29 per authoring run - THE CHEAPEST LIBRARY OF THE CAMPAIGN, against the SS-IX ch 3 benchmark of Rs 110.99 clean / Rs 145.70 all-in.

THE COST SHAPE DOES NOT MATCH THE BENCHMARK, AND THE INVERSION IS STRUCTURAL. The C2 benchmark records 'input is flat across runs while output falls with period count, so a compact variant costs only ~11% less than the top'. HALF OF THAT HOLDS. Input is flat - 19,734 / 19,659 / 19,659, the 75-token delta being the top brief against the compact brief. But OUTPUT DOES NOT FALL WITH PERIOD COUNT: the 10-unit compact wrote MORE than the 12-unit standard (12,615 vs 11,739 output tokens) and COST 5% MORE (Rs 22.83 vs Rs 21.65). Two reasons, both specific to english and both on disk:
  (a) THE ASSESSMENT IS COUNT-INVARIANT. Rule 2's PAIR is two items per (section x spine) cell, and the cell count is a property of the CHAPTER, not of the plan - so all three files carry 10 items. A compact pays for the full assessment.
  (b) BANDS DO NOT SCALE DOWN WITH UNITS. The top carries 49 bands over 12 units (4.08/unit) because its closing synthesis is lean; p10 carries 50 bands over 10 units (5.00/unit). The compact wrote MORE lesson-plan prose in FEWER units than the standard did in more.
BUDGETING CONSEQUENCE: 'count runs, not chapters' holds and is stronger here, but 'a compact costs ~11% less than the top' MUST NOT BE GENERALISED - at an english stage a compact costs about the same as the standard and can cost more. Price a library as N runs x the flat rate, with NO compact discount.

CORPUS EXTRAPOLATION, english preparatory: 39 non-placeholder chapters -> 109 AUTHORING RUNS on the real canonical_plan.counts distribution (not a flat x3). At this pilot's Rs 21.29/run that is Rs 2,320 synchronous, Rs 2,668 with a 15% defect allowance; at the campaign's Rs 37/run budgeting figure, Rs 4,033 / Rs 4,638. The pilot rate is ~57% of the campaign figure, which was set on SS-secondary, the heaviest corner; preparatory is the lightest (shorter constitutions, smaller chapters, five cells rather than six or more). Treat Rs 21/run as a preparatory-stage figure and keep Rs 37 as the corpus upper-middle bound until more stages are measured.

THE PILOT IS NOT A FLATTERING RATE SOURCE: ch 11 is tied for the LARGEST chapter in class III at 12 recommended periods, so it sits at the expensive end of its own stage. What it does not sample is picture_narrative, whose chapters run 2-6 periods and will pull the stage mean down further."""),
}


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s9_c1c2"))
    # C-STEPS LIVE UNDER `combos`, NOT `stages` — the tracker renders the C-cycle
    # matrix from cellHtml("combos", comboKey(c), ...) while the P-steps come from
    # cellHtml("stages", ...). The two keys are the same string, so writing a C-step
    # to `stages` yields a state file that looks right and renders nothing.
    row = state.setdefault("combos", {}).setdefault(KEY, {})
    for step, (status, by, comment) in ROWS.items():
        row[step] = {"status": status, "by": by, "at": NOW, "comment": comment}
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"tracker updated · {KEY} · {', '.join(ROWS)} · {NOW}")


if __name__ == "__main__":
    main()
