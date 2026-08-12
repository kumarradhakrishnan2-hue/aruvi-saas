#!/usr/bin/env python3
"""S11 · english · secondary — C5 (read the certification report) into the tracker.

Run from the repo root:
    python3 genon/out/stage_prep_english_secondary/update_tracker_s11_c5.py

Full check table + re-derived sweep: docs/testing_artefacts/c5_english_ix_ch07.md
No new defects. One housekeeping action owed on the founder's machine (see the comment).
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/secondary"

C5 = """READ 2026-08-12 - ALL PASS. Report: genon/out/library_reports/english_ix_ch07_20260812_143511.md. Full table + the sweep re-derived independently: docs/testing_artefacts/c5_english_ix_ch07.md. Every check was corroborated rather than quoted back - compile, registry, first-visit, synthesis gate, register scan and the whole serve sweep were re-run outside the certifier and agree with it exactly.

1 LIBRARY COMPLETE - [17, 14, 10] on disk = canonical_plan.counts, basis authored_standard, registry 6 sections.
2 COMPILES - all three under compile_stream v0.5: 17 units/54 phases, 14/57, 10/26, 6 items each.
3 ANCHORS VERBATIM - every anchor on all 41 units resolves in the top registry, zero outside. This stage's token is the COMPOSITE cell the platform builds from section_id + spines_taught[], so the check is really asking whether those two fields came out clean on 41 units; they did.
4 FIRST-VISIT ORDER - all three files reproduce the registry IN FULL AND IN ORDER, identical across standard and compacts, which is the property the Xth-unit choice set runs on.
5 COVERAGE REACHES THE FINAL SECTION - in every file, and on the standard before the synthesis unit. This is S11's coverage amendment holding at every count including the floor.
6 SYNTHESIS GATE - standard closes on U17 and carries the marker nowhere else; NEITHER compact carries it. The fact travels as the "synthesis": true BOOLEAN here, not the reserved token (genon_anchor_field_present is False for english).
7 SERVE SWEEP X=8..19, no exception. Re-derived: 8 fill/forward -2s | 9 fill/single -1s | 10 IDENTITY | 11 rescue/complete (from 14, borrowing the standard's synthesis) | 12,13 fill/single | 14 IDENTITY | 15 rescue/complete (from 17) | 16 fill/single | 17 IDENTITY | 18,19 surrender. Three identities at the three authored counts; NO drops anywhere inside [10,17]; drops only below the floor with a coverage note attached; surrender declared in minutes above the top.
8 NO DEFENSIVE TRUNCATION - the truncation mode appears nowhere in the sweep. The only drop-bearing rows (X=8, X=9) are BELOW the floor of 10, where a drop is the declared cost, not a failure.
9 REGISTER CLEAN - re-ran register_scan myself: 0 BAN hits across all three files over activity_title, materials, teacher_notes, time_bands[].activity and homework[] (54/57/26 bands read). TWO ADVISORIES, both correctly non-gating: p14 U9 'today's podcast on meditation' (calendar family - the template's own 'Will it rain today?' case), and p10 U10 'does not require any classroom artefact from an earlier unit' (positional family). THE SECOND IS WORTH KEEPING: the scanner flagged the phrase, but what the sentence does is DECLARE ARTEFACT INDEPENDENCE OUT LOUD - and the standard canonical failed at exactly that (ARV-D-132, U17 listing U15's draft article in materials). The compact states the rule the standard broke, same chapter, same run, same constitution: generation variance, not a comprehension gap.
9a MCQ ARRANGEMENT - PASS on all three. Read on the FIRST pass as the template requires: 'options arranged: 1 of 1 item(s) re-ordered'. The library has exactly one options-bearing item (the TRUE_FALSE) and STEP 6 moved it; the re-certify run's '0 of 1' means only that nothing was left to move.
10 ITEM COUNTS PER COMPETENCY - advisory, reports 0 vs 0 on all three, and that is the honest reading: english performs no per-chapter competency mapping and C-codes are forbidden in its LP and assessment (LP Rule 7), so there are no competencies to group by. Carried into the C4 record.

ONE EXIT CONDITION IS SATISFIED IN SUBSTANCE BUT NOT IN FACT. backup/quarantine/english/ix/ still holds three files - stale copies from the FALSE-FAIL certification run (ARV-D-127, closed: the item-shape gate read question_text where english's constitution names the field item_stem). The gate is fixed, the files were restored, the library re-certified ALL PASS, so there is no fix worklist behind them and nothing in them is servable. The Cowork sandbox cannot unlink them (PermissionError on both rm and os.remove), so ONE COMMAND IS OWED ON THE FOUNDER'S MACHINE:
    rm backup/quarantine/english/ix/ch_07_canonical*_20260812_143130.json
Recorded rather than waived: step 0.8's doctrine is that a non-empty quarantine reads as an open worklist, and the point of that rule is that nobody should have to ask whether an entry is stale.

WHAT C6 INHERITS: the three identity counts are 10, 14 and 17 (kumar1's identity requests); X=11 and X=15 are the borrow rows and X=8/X=9 the below-floor rows with declared drops of 2 and 1 (kumar2); kumar3's mixed-duration week is real - the profile carries [50, 60] with ppw_by_duration {50: 5, 60: 1}, so the mixed matrix draws on something rather than a synthetic row."""


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s11_c5"))
    state["combos"][KEY]["C5"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C5}
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"tracker updated · {KEY} · C5 pass · {NOW}")


if __name__ == "__main__":
    main()
