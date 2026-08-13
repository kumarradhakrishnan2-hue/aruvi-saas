#!/usr/bin/env python3
"""S10 · english · middle — C5 (read the certification report) into the tracker."""
import datetime, json, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/middle"

C5 = """PASS 2026-08-13. Report: genon/out/library_reports/english_vi_ch08_20260813_111056.md (the --certify-only re-run after the retired-handoff strip; the first-pass report is ...103144.md and differs only in STEP 6's arrangement count). DETERMINISTIC CHECKS ALL PASS - 37 PASS lines, zero FAIL. Each of the eleven checks in build_library.py::certify was READ in the report AND independently re-derived off the files, because a report agreeing with itself proves nothing.

1 LIBRARY COMPLETE - PASS. ch_08_canonical.json + _p10 + _p07 against plan [12, 10, 7]; the row reads basis authored_standard, registry 6 sections, authored [12, 10, 7].

2 EVERY FILE COMPILES - PASS, re-derived. compile_stream v0.5 on each: 12 units / 47 phases, 10 / 40, 7 / 25; 12 assessment items and a 6-spine coverage_handoff on all three. Worth noting this is the first english library whose bands were AUTHORED in the time_bands shape - the whole saved corpus predates P3 and raises KeyError('time_bands') here, exactly as S11 recorded.

3 ANCHORS VERBATIM - PASS on all three, re-derived against a registry rebuilt from the top canonical rather than read from the report: B|reading_for_comprehension, B|listening, B|speaking, B|writing, B|vocabulary_grammar, B|beyond_text. Every anchor in every file resolves; the synthesis unit is correctly exempt.

4 FIRST-VISIT ORDER - PASS on all three. New cells appear in registry order in the standard AND in both compacts. NOTE FOR THE RECORD: on THIS chapter the summary's on-page spine order happens to coincide with the canonical enumeration order, so the two orders P5.2 warns are different cannot be told apart here. That is a property of ch 8, not a general fact - english IX ch 7 had them differ. A C5 check on another chapter must still not compare one against the other.

5 COVERAGE REACHES THE FINAL REGISTRY SECTION - PASS. All 6 cells reached in every file, and in the standard before the synthesis unit (by unit 11 of 12). This is FULL SPINE COVERAGE - the P1 amendment - holding at 12, at 10 and at the floor of 7.

6 SYNTHESIS-ANCHOR GATE - PASS. The standard's last unit (12) carries synthesis: true and the token appears nowhere else in it; NEITHER compact uses it. Re-derived: synthesis units [12] / [] / [].

7 SERVE SWEEP - PASS, re-derived ask by ask from floor-2 to top+2, ten asks, zero exceptions:
     X=5  fill/single   5 units  2 DROPS  (lender 7)  note names B|vocabulary_grammar...
     X=6  fill/single   6 units  1 DROP   (lender 7)  note names B|beyond_text...
     X=7  IDENTITY      7 units  0 drops
     X=8  fill/single   8 units  0 drops  (lender 10)
     X=9  fill/single   9 units  0 drops  (lender 10)
     X=10 IDENTITY     10 units  0 drops
     X=11 SYNTHESIS    11 units  0 drops  (borrowed_from 12, self_fill TRUE, withheld [11])
     X=12 IDENTITY     12 units  0 drops
     X=13 surrender    12 served, note "1 period(s) (40 minutes) exceed this chapter's fullest plan"
     X=14 surrender    12 served, note "2 period(s) (80 minutes) exceed..."
   Three identities land exactly on the three authored counts, which is the cheapest possible proof the library is what the plan says. THE X=11 ROW IS THE ONE WORTH READING TWICE: slot_fill.mode "synthesis", borrowed_from 12, SELF_FILL TRUE - the 12-unit canonical lends its own closing synthesis into an 11-unit prefix of ITSELF rather than reaching for a stranger's unit. That is engine e14's "ties resolve SELF FIRST" (architecture v2.1, after the engine was found borrowing a foreign unit while the plan being served had its own candidate), visible in a live serve.

8 NO DEFENSIVE TRUNCATION - PASS. All ten asks report a non-empty choice set. Drops occur ONLY at X=5 and X=6, both BELOW the floor of 7, where truncation with declared drops is legal and the coverage note names the lost cells. Zero truncation inside [7, 12]. Case 3 stayed structurally impossible, as v2.0 §0.4 says it must on a certified library.

9 REGISTER CLEAN - PASS, 0 ban hits on all three, and the scan is CONFIRMED TO HAVE REACHED THE TEXT (47 / 40 / 25 bands read, plus activity_title, teacher_notes, materials and homework) - the S6 failure mode where a clean result meant the scanner never read anything. Bans 1 (clock quantity) and 2 (forward reference / completion claim) are clean across all 112 bands, which is the harder half and includes the closing synthesis unit where a completion claim would have been the natural thing to write. The one advisory-grade calendar word is ARV-D-140, already filed and dismissed by the founder.

9a MCQ OPTIONS IN ARRANGEMENT ORDER - PASS on all three. Read on the FIRST pass as the template instructs: report ...103144 recorded "4 of 4 item(s) re-ordered", i.e. STEP 6 moved every options-bearing item in the library. The re-run's "0 of 4" means only that nothing was left to move. C4 read the consequence from the other side: the p07 MCQ's correct answer sits at B where the standard's sits at C, and the reveals keys track the new labels - the arrangement stage visibly working end to end.

10 ITEM COUNTS PER COMPETENCY - ADVISORY, and STRUCTURALLY VACUOUS AT THIS STAGE. The block reports "expected {(from handoff): 0}" and 0 items vs 0 expected on all three files. That is not a miss: english has NO competency axis at all - LP Rule 7 forbids C-codes anywhere in the JSON and the assessment indexes on the (section x spine) CELL - so there is nothing for a per-competency census to count. The equivalent english check is item count = 2 x contributions, which C4 ran (12 = 6 x 2 on all three). Recorded so a later reader does not mistake the zeros for a failure; the same will hold at S9.

11 REGISTRY <-> CHAPTER SUMMARY - PASS, and this library is the first english one ever to face this check: it was added TODAY (2026-08-13, genon/summary_sections.py) and its first sweep covered 33 chapters, none of them english·middle. "6 summary section(s) vs 6 registry entr(ies)", every section the summary carries anchored by some unit of the standard. This is the one check that looks OUTSIDE the library - checks 3-5 are all built from the top canonical's own registry and are blind to a section the top never named. For english the summary's declared sections ARE the spine cells (a post-split chapter is one main_section), so the gate is live here rather than advisory as it is for social_sciences.

QUARANTINE - EMPTY FOR THIS CHAPTER. backup/quarantine/english/ contains only ix/ (S11's three files); there is no english/vi directory at all, so nothing from this build was quarantined and no file failed structurally. CARRIED AS A CAMPAIGN NOTE, NOT A C5 FAIL: the quarantine is not empty overall - 13 files across english/ix 3, TWAU iv 3, TWAU v 3, social_sciences/ix 2, science/ix 1, TWAU iii 1. Step 0.8 requires an EMPTY quarantine at campaign start and calls a non-empty one "an open fix worklist"; that worklist is now 13 long and belongs to the stages that own those files.

ADVISORY CARRIED FROM THE REPORT: TRUE_FALSE is used by exactly one item in the whole library. Read against the constitution's type table it is correct - assessment Rule 2's slot table permits MCQ or TRUE_FALSE at Listening slot 1, and the standard chose TRUE_FALSE there while p07 chose FILL_IN for the same slot (which C3 recorded as a slot-table miss, dismissed by the founder). One use is thin, not wrong.

EXIT MET: report says ALL PASS; quarantine empty for this chapter."""


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s10_c5"))
    state["combos"][KEY]["C5"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C5}
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"tracker updated · {KEY} · C5 pass · {NOW}")


if __name__ == "__main__":
    main()
