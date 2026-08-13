#!/usr/bin/env python3
"""S9 · english · preparatory — write C6 into the tracker. No defects raised.

    python3 genon/out/stage_prep_english_preparatory/update_tracker_s9_c6.py

Runner:    genon/out/stage_prep_english_preparatory/run_s9_c6.py   (re-runnable)
Responses: genon/out/stage_prep_english_preparatory/C6_responses_english_iii_ch11.json
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

C6 = ("pass", "Claude", """API SERVE CHECKS RUN 2026-08-13 AGAINST A LIVE API — ALL ROWS RETURN AS EXPECTED, every assertion passes. Runner: genon/out/stage_prep_english_preparatory/run_s9_c6.py (re-runnable, exit 0 iff clean). Responses + files: C6_responses_english_iii_ch11.json.

WHERE IT WAS RUN, and why that is legitimate. C6 is a [Kumar] step in the template because the C-cycle's metered half must run on the founder's machine (0.1). THIS STEP IS NOT METERED - serving is selection, costs milliseconds, and touches no credentialed API - so it was executed in the Cowork sandbox against 'python3 -m uvicorn api.main:app --port 8000' on the same file-backed data, with fastapi installed locally. Nothing about the result is machine-dependent; re-run it on your machine if you want founder-machine provenance.

LIBRARY: english III ch 11, counts [12, 10, 7], floor 7, AUTHORED DURATION 40 min (recorded as C6 requires). Identity split is the template's standard - kumar1 the identity requests, kumar2 the between-variant / below-floor / surrender requests, kumar3 the mixed-duration weekly matrix.

ROW 1 - IDENTITY, at the authored duration (kumar1). X=12, X=10 and X=7 all return identity:true, each naming ITS OWN canonical (ch_11_canonical.json / _p10 / _p07), and NO NEW FILE IS SAVED in any of the three. Asserted additionally that the filename registered is the CANONICAL itself rather than a served copy - the identity rule is a REGISTRATION, not a serve.

ROW 2 - COMPLETE FILL between canonicals (kumar2). X=9: mode 'fill', fill_class 'single', uncovered_sections EMPTY, no coverage note needed. Also ran X=8 deliberately, which is not a plain fill: mode 'complete_rescue' (Case 1b / e15), uncovered_sections EMPTY. The ordinary upward serve at X=8 would have taken the 10-unit compact's first 8 units and DROPPED a section; the engine instead served the 7-unit canonical COMPLETE and closed with the standard's synthesis. C5 called this the row to read twice and the API confirms it end to end.

ROW 3 - SYNTHESIS (kumar2). X=11: mode 'synthesis', uncovered_sections empty, and slot_fill.borrowed_from == 12 - THE BORROWED UNIT IS THE STANDARD'S SYNTHESIS UNIT, exactly as the template requires.

ROW 4 - SURRENDER, X = A_top + 1 = 13 (kumar2). surrendered_periods = 1; the surrender sentence appears in COVERAGE_NOTE, the same channel as drops (e09): '1 period(s) (40 minutes) exceed this chapter's fullest plan and return to your budget.' And e10 holds: the served schedule prints the SERVED count, not the ask - period_schedule_display reads 'Row 1: 40 minutes x 12 periods = 480 minutes / Total: 12 periods . 8h 00min' with no 13 anywhere - while THE REQUEST SURVIVES in period_rows_snapshot as [{'id': 0, 'duration': 40, 'count': 13}].

ROW 5 - BELOW FLOOR, X = floor - 1 = 6 (kumar2). mode 'fill' with uncovered_sections ['B|beyond_text']; coverage_note NAMES it ('Time budget short of the chapter's full span: B|beyond_text could not be scheduled - the material is included for you to share as guided self-study or homework'); result.dropped_units carries the lost unit VERBATIM, flagged unscheduled: true.

ROW 6 - MIXED-DURATION WEEKLY MATRIX (kumar3), rows [(40, 7), (50, 5)] - her real profile ratio (ppw {40:3, 50:2}) scaled across the chapter's 12 periods. 200, served whole. WEEKLY DISPERSION HOLDS, asserted from genon.duration_sequence = [40, 50, 40, 50, 40, 40, 50, 40, 50, 40, 50, 40]: the SHORTEST sitting opens the week; the five long sittings sit at indices 1, 3, 6, 8, 10 - ALL INTERIOR AND NEVER ADJACENT. Every unit tiles 0..its own duration exactly across two different durations in one plan.

THE NUANCE ASSERTED DELIBERATELY - IDENTITY FIRES ONLY AT THE AUTHORED DURATION. X=12 at 50 minutes (kumar1) is NOT an identity serve: the variant is served whole with proportional scaling and a file is written. All 12 units present, every unit at 50 min, every unit tiling 0..50 exactly. This is the ORDINARY teacher case, not an edge - her periods rarely match the authored standard.

TENANCY (X1 evidence). kumar1's ch-11 register holds the three CANONICALS (identity registers the file and saves no copy) plus its own 50m12 serve; kumar2 holds five served files; kumar3 holds two. THE TWO SERVED SETS ARE DISJOINT - zero shared filenames - which is what makes 'which tenant does this plan belong to' answerable. Sections are disjoint too (3C / 3B / 3E) per P5.4.

ONE METHOD NOTE WORTH CARRYING TO EVERY FUTURE C6, learned the hard way here: A SERVED PLAN IS A CACHE ENTRY, addressed by (chapter, normalised matrix, chosen variant's version, engine version). A re-run of the same request is a HIT that writes nothing, so an assertion keyed on 'a new file appeared' SILENTLY SKIPS on the second run and reports a pass it never made. The runner now keys its structural assertions off response.filename instead, which is stable across hits and misses alike. The first pass of this runner reported an empty STRUCTURAL section for exactly that reason and looked clean.

NO DEFECT RAISED. Every row in the template's table returned as specified, and the two structural invariants the template singles out (weekly dispersion; served-count printing) both hold.

HANDED FORWARD: C7/C8/C9/C12 inspect kumar3's mixed plan (ch_11_50m5-40m7_e19_c20260813123304.json), per the template. C8's two transitions are X=8 (the rescue) and X=11 (the synthesis borrow), now confirmed live rather than only in the certification sweep.""")


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s9_c6"))
    status, by, comment = C6
    state.setdefault("combos", {}).setdefault(KEY, {})["C6"] = {
        "status": status, "by": by, "at": NOW, "comment": comment}
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"tracker updated · combos[{KEY!r}] · C6 · {NOW} · no defects")


if __name__ == "__main__":
    main()
