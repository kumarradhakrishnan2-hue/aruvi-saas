#!/usr/bin/env python3
"""S9 · english · preparatory — write C5 into the tracker. No defects raised.

    python3 genon/out/stage_prep_english_preparatory/update_tracker_s9_c5.py

Read: genon/out/stage_prep_english_preparatory/C5_certification_read_english_iii_ch11.md
C-steps live under `combos`, not `stages` (see fix_s9_c_steps_scope.py).
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/preparatory"

C5 = ("pass", "Claude", """CERTIFICATION REPORT READ 2026-08-13 — ALL PASS, QUARANTINE EMPTY. Report: genon/out/library_reports/english_iii_ch11_20260813_124746.md, verdict line 'DETERMINISTIC CHECKS ALL PASS'. Implementation cited by line in genon/build_library.py::certify (:242), not re-specified. Full read: genon/out/stage_prep_english_preparatory/C5_certification_read_english_iii_ch11.md

QUARANTINE: backup/quarantine/english/iii/ does not exist. The only english entries in quarantine are english/ix (S11's ARV-D-136 re-author, 3 files) - a different stage and chapter. Exit met on both halves.

NOTE ON WHICH REPORT: an earlier one exists for the same chapter (..._20260813_123939.md) from the --top-only pass, whose single FAIL 'library complete' was the not-yet-authored compacts. Superseded; the newest is read, as C5 requires.

THE ELEVEN CHECKS.
1 LIBRARY COMPLETE (:264) PASS - three files vs plan [12, 10, 7], in order.
2 EVERY FILE COMPILES (compile_stream v0.5, :236) PASS BY ABSENCE - the check reports only on failure, so a clean report IS the pass. Confirmed independently: all three load through compile_stream in the sweep, which could not run otherwise. Stated explicitly because a compile failure is the error mode that reports itself as 'does not compile' on EVERY file while naming nothing (the P5.5 carrier trap).
3 ANCHORS VERBATIM (:361) PASS x3 - every unit of every file draws its anchor byte-for-byte from the five-cell registry B|reading . B|oracy . B|writing . B|word_work . B|beyond_text. The reserved synthesis token is exempt by design.
4 FIRST-VISIT ORDER (:371) PASS x3 - first visits at units 1, 3, 5, 7, 9 in the top; revisit tails (u10 writing, u11 reading+oracy) legal; synthesis skipped by the walk. THE THREE FILES AGREE, which is the property the Xth-unit choice set depends on - a compact whose first-visit order differed would make a borrowed unit arrive out of sequence.
5 COVERAGE REACHES THE FINAL REGISTRY SECTION (:373) PASS x3 - the standard reaches B|beyond_text at unit 9, well inside the A-1 bound of 11.
6 SYNTHESIS-ANCHOR GATE (:350, :354) PASS x3 - standard closes with it and carries it nowhere else; reserved away from both compacts. ON THIS STAGE THE CARRIER IS THE '\"synthesis\": true' BOOLEAN, not a section_anchor token, because genon_anchor_field_present is False for english - the brief asked for the boolean and the gate reads it. P5.5 part 5, working end to end.
7 SERVE SWEEP PASS - X from floor-2 (5) to top+2 (14), no exception at any X.
8 NO DEFENSIVE TRUNCATION (:727) PASS x10 - choice set non-empty at every X. Case 3 stays structurally impossible.
9 REGISTER CLEAN (register_scan.py, :473) PASS x3, AND THE SCAN IS PROVEN TO HAVE REACHED THE TEXT - 0 ban hits over 49 / 50 / 34 bands plus activity_title, materials, teacher_notes and homework. The band-count line matters more than the zero: a scan that read nothing also reports zero. No advisories.
9a MCQ OPTIONS IN ARRANGEMENT ORDER (:636) PASS x3, and the FIRST-PASS count is the finding: '4 of 6 item(s) re-ordered' - p07 2 of 2, p10 2 of 2, the top 0 of 2 BECAUSE its two were already sorted by the earlier --top-only certify run. Across the library the correct option was authored at position B in FIVE OF FIVE MCQ/TRUE_FALSE items and the sort scattered them to C, D, B, C, B.
10 ITEM COUNTS PER COMPETENCY - ADVISORY, reports '0 items vs 0 expected' on all three, AND THAT IS CORRECT, NOT A MISS. English has no competency axis: LP Rule 7 forbids C-codes anywhere and the item count is structural (2 x section_contributions), so there is no per-competency slate to compare against. It is reporting an empty grouping. The real count check for english lives at C3/C4 item 3, where 5 contributions -> 10 items passed on all three. DO NOT READ A FUTURE '0 vs 0' HERE AS A MISS, at any english stage.
11 REGISTRY <-> CHAPTER SUMMARY (summary_sections.py, :293) PASS, AND IT GATES FOR THIS STAGE - '5 summary section(s) vs 5 registry entr(ies)', every one anchored. English declares its sections in JSON main_sections[] and its registry entries are the SPINE CELLS, so this is a gating subject, not an SS-style advisory. Zero unmatched in either direction. This is the check added the same day that caught three real misses in its first 33-chapter sweep; here it is satisfied outright.

THE SWEEP, RE-DERIVED INDEPENDENTLY THROUGH serve_plan rather than transcribed from the report (floor 7, top 12, 40 min):
  X=5   5u  fill/single      DROPS B|beyond_text   (below floor)
  X=6   6u  fill/single      DROPS B|beyond_text   (below floor)
  X=7   7u  identity         serves p07 whole
  X=8   8u  RESCUE/COMPLETE (from 10)   0 drops
  X=9   9u  fill/single      0 drops
  X=10 10u  identity         serves p10 whole
  X=11 11u  synthesis        p10 complete + the standard's synthesis unit
  X=12 12u  identity         serves the standard whole
  X=13 12u  identity         1 period surrendered
  X=14 12u  identity         2 periods surrendered

EVERYTHING INSIDE THE BAND [7, 12] SERVES COMPLETE - ZERO DROPS AT EVERY ONE OF THE SIX PERIOD COUNTS A TEACHER CAN ACTUALLY LAND ON. That is what FULL SPINE COVERAGE bought: a library whose compacts were subsets of the standard would have dropped somewhere in that range. The two drops are at X=5 and X=6, BOTH BELOW THE FLOOR, which is specified behaviour, and both are filed through the teacher-facing channel rather than swallowed ('Time budget short of the chapter's full span: B|beyond_text could not be scheduled - the material is included for you to share as guided self-study or homework'). Surrender above the top is declared the same way ('1 period(s) (40 minutes) exceed this chapter's fullest plan and return to your budget').

X=8 IS THE ROW WORTH READING TWICE. 'rescue/complete (from 10)' is Case 1b (e15): the ordinary upward serve would have taken the PREFIX of the 10-unit compact plus a borrowed Xth unit, and that path WOULD HAVE DROPPED a section, because a 10-unit plan's first 8 units have not yet reached B|beyond_text. Instead the engine served the 7-UNIT CANONICAL COMPLETE, closed with the standard's synthesis unit, and reached 8 units with NOTHING DROPPED. 'rescued_from: 10' names the count it rescued FROM, so the sweep shows what the trade cost: the teacher gets the floor plan's richness rather than the 10-plan's, in exchange for complete coverage. THAT TRADE IS THE HUMAN GATE'S TO READ, NOT CERTIFICATION'S - the certifier only proves no section was lost. It is also the sharpest available evidence that this library is dense enough: the rescue exists precisely so a gap between authored counts does not cost a section, and it fires once, at the one X that needed it.

NO DEFECT RAISED. Nothing in the report fails and nothing in the sweep needs a repair or a re-author; the drops and surrenders are declared costs of their period counts.

HANDED FORWARD: C8 inherits X=8 (the rescue) and X=11 (the synthesis borrow) as the two transitions worth reading in prose - the only rows where a served plan is not simply one authored file. C6 inherits the band [7, 12] as CLEAN, so any coverage note it sees inside that range at 40 minutes is a regression rather than an expected cost; its mixed-duration requests (kumar3 at 40/50) are the untested axis, this sweep being single-duration by construction.""")


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s9_c5"))
    status, by, comment = C5
    state.setdefault("combos", {}).setdefault(KEY, {})["C5"] = {
        "status": status, "by": by, "at": NOW, "comment": comment}
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"tracker updated · combos[{KEY!r}] · C5 · {NOW} · no defects")


if __name__ == "__main__":
    main()
