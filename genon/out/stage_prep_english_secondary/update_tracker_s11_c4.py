#!/usr/bin/env python3
"""S11 · english · secondary — C4 (MEMORY amendment items, live) into the tracker.

Run from the repo root:
    python3 genon/out/stage_prep_english_secondary/update_tracker_s11_c4.py

Full item table: docs/testing_artefacts/c4_english_ix_ch07.md
No new defects: every applicable item passed or is N/A with a recorded reason.
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/secondary"

C4 = """CHECKED 2026-08-12 - PASS, no new defects. All THREE canonicals read (17/14/10 - C4 reads the whole library, not C3's pair, because each compact authors its own assessment). Full item table: docs/testing_artefacts/c4_english_ix_ch07.md. Eleven of the twenty-one checklist items touch this stage.

PASSED: item 3 (exact item counts - 6 contributions -> 6 items in all three; english's count rule is structural, one item per (section x spine) cell, so there is no slot-type question of the kind S1 found at ARV-D-028, and the v1.4 invariance line held live: the 10-period canonical produced the same six cells as the 17) | item 4 (SPLIT-CHAPTER REGENERATION, and this is the first time a split chapter has ever been regenerated from scratch - title 'Vitamin-M (Vitamin-M)' in the <section> (<unit>) form, inventory a single {A, Vitamin-M, prose}, section_id A on all 41 units, spines at the top level after the port's singleton collapse) | item 7 (Period.approach - 41 of 41 units non-empty; see below, the item CLOSES) | item 9 (the Jul 12-13 wave's two english-secondary entries: every method drawn from its spine's permitted list, the secondary additions present - grammar-in-writing on reported speech, domain-vocabulary, critical-reading, literary-analysis; EXTRACT_ANALYSIS fired with a verbatim 4-line extract and the listening item verified against the summary's baked-in transcript_text without opening the appendix) | item 10 (referenced word NAMED - zero items say underlined/circled/highlighted/bold anywhere; the grammar items quote their sentences in full) | item 11 (homework locator - 6 of 6 homework briefs located, including one using the section-range FALLBACK the rule specifies, p.97-98, where the task carries no page_ref) | item 12 (FILL_IN anti-duplication - satisfied, vacuously: no FILL_IN carries a visual at all) | item 13 (the NARROWED A/B ban, and this is its vindication: p14's Q-VGR-A-1 emits Part A reported speech + Part B prepositions, both prose, visual_stimulus empty - exactly the case the narrowing permits and an item the old blanket ban would have failed) | item 19 (curly-quote narration - three generations, status ok on all three, ZERO auto-repairs in the ledger) | item 21 (this stage's own P-prep amendments - answered by C1 and C3).

N/A WITH A REASON, not skipped: item 1 (SS/TWAU guide shape) | item 5 (task_density is english MIDDLE's) | item 8 (prep's FILL_IN/MATCH shapes) | items 14-17 (maths/SS) | item 20 (TWAU's type census; english's equivalent passed at C1's item-shape gate).

TWO ITEMS CHANGE STATE BEYOND THIS STAGE.
- ITEM 7 CLOSES ENTIRELY. Its own text named english (S9-S11) as the last stage-family unchecked. English is now measured - unit_approaches and the port's Period.approach are non-empty for 41 of 41 units, reading pedagogical_methods, a {spine: method} DICT joined in first-seen order, which is the one shape ARV-D-086 had returned [] for. Every value is drawn from its spine's permitted list, so ARV-D-043's populated-but-invalid caveat cannot arise (english's methods are a closed per-spine enumeration inside the constitution, not a prose document to quote). The field is identical at all three english stages, so S9/S10 inherit the answer and owe nothing. What survives is the standing fact: MATHEMATICS-PREPARATORY IS THE ONLY LEGITIMATE EMPTY IN THE PORTFOLIO.
- ITEM 4 goes from wholly owed to one-third discharged: IX passes, VI/VII/VIII and III remain with S10 and S9.

ITEM 2 IS NOT TESTABLE HERE, AND THE REASON IS STRUCTURAL RATHER THAN AN OVERSIGHT: the library contains ZERO MCQ items - 18 items across three canonicals, all EXTRACT_ANALYSIS/TRUE_FALSE/FILL_IN/SCR/ORAL_PROMPT/WRITING_TASK/ECR. At secondary Rule 4 prefers EXTRACT_ANALYSIS/ECR for analytical Reading LOs and the other five spines default to non-MCQ types, so a six-cell english chapter can legitimately produce none. The item stays OWED and its owner is now 'the first MCQ-bearing english chapter' rather than a stage; S9 (preparatory, MCQ-heavier type set) is the likeliest place it fires. A9's arrangement half sits in the same position (C3 recorded it): one options-bearing item in the whole library, a TRUE_FALSE, which STEP 6 re-ordered on the first pass.

TWO CLOSURES RECORDED, as testing.md asks the first time they come up: item 6 (time as a duration vector) is CLOSED BY DESIGN - A1 fixes one standard row and the serve engine owns every timetable variation; confirmed live, one row and a single 50-minute duration on every unit of all three files. Item 18 (MCQ position spread) is CLOSED BY THE PIPELINE - the prohibition was struck at P2 and ordering is deterministic in normalize_options.py (STEP 6); the replacement signal is STEP 6's own 'options arranged: 1 of 1 item re-ordered' on the first pass.

ONE RECOVERY C4 MADE THAT P4 COULD NOT: the assessment CHANGELOG recorded v1.2 and v1.3 as undocumented (no sidecar, no in-document history, MEMORY's inventory stopping at v1.1). Checklist items 12 and 13 name BOTH bumps - v1.1->v1.2 is the FILL_IN table anti-duplication clause and v1.2->v1.3 the narrowed A/B ban, both 2026-07-13. The sidecar is now back-filled from the checklist rather than guessed at, and both were tested live above.

STILL UNTESTED AFTER C4, all three recorded rather than glossed: the MCQ path (item 2), the DRAMA branch (item 9 - ch 7 is prose; ch 11 Twin Melodies is class IX's only drama), and the table-bearing FILL_IN (item 12, satisfied by absence)."""


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s11_c4"))
    state["combos"][KEY]["C4"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C4}
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"tracker updated · {KEY} · C4 pass (no new defects) · {NOW}")


if __name__ == "__main__":
    main()
