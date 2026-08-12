#!/usr/bin/env python3
"""S11 — C9 (assessment anchoring across the serve) + the two C6 corrections."""
import datetime, json, pathlib, shutil
ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/secondary"

C9 = """CHECKED 2026-08-12 - ALL FOUR CHECKS PASS, on seven serves re-derived against the RE-AUTHORED library (X = 8, 9, 11, 12, 13, 15, 16). Full anchor table: docs/testing_artefacts/c9_english_ix_ch07.md. AND C9 CORRECTS ONE OF MY OWN C6 FINDINGS AND DOWNGRADES THE OTHER - both turned out to be the engine doing exactly what this step specifies. C6 read the outputs without reading the contract they were written against.

1 PREFIX REMAP - PASS. Every item of the chosen variant whose anchor unit is served carries a period_ref pointing at that unit's SITTING number, and every one equals the independently computed last-teaching sitting. 37 items across seven serves, ZERO mismatches. (The synthesis unit never appears as an anchor: it teaches no cell, so is_synthesis keeps it out of the index - at X=11 the RFC item anchors at sitting 5, not at the borrowed closer that revisits RFC, which is the correct reading of 'the last sitting that TEACHES this cell'.)

2 BORROWED UNIT BRINGS ITS OWN ITEMS - PASS, vacuously, and the reason is structural. The only borrowed units in this sweep are the standard's SYNTHESIS (X=11, X=15) and self-fills where lender and host are the same file. A synthesis anchors no item at this stage - it teaches no (section x spine) cell, by the constitution's own count rule - so there are no items for it to bring. Same outcome testing.md records for the derived-anchor stages ('C9.2 unsatisfiable on precisely the Case-1 borrow'), reached by a different route: not a missing handoff row but a unit that legitimately anchors nothing. NOTHING IS OWED - no item is lost because none existed to lose.

3 UNSERVED ANCHORS - PASS on all four sub-checks. (a) No empty period_ref anywhere: 37 of 37 carry a ref. (b) Items whose anchor unit was not served are ABSENT and counted: X=12 ships 4 with assessment_items_unserved 2; X=13 ships 5 with 1. (c) BELOW-FLOOR: the dropped units' items ARE present, anchored to the dropped unit's sitting number IN THIS PLAN, flagged unscheduled: true - X=9 Q-BT-A-1 period_ref [10] unscheduled TRUE, and sitting 10 is exactly where dropped_units puts the dropped Beyond-the-Text unit; X=8 Q-WRT-A-1 [9] and Q-BT-A-1 [10] both flagged, matching two dropped units. Never the lender's numbering. (d) Exports omit exactly the unscheduled items - that is C12's surface, carried forward.

4 NO CROSS-VARIANT REFERENCES - PASS. Each serve's items come from its chosen variant alone and the ids make it legible: X=11 carries p10's Q-VG-A-1/Q-BT-A-1, X=15 carries p14's Q-VGR-A-1/Q-BXT-A-1, X=16 carries the re-authored top's Q-LST-A-1. No mixing in either direction.

ARV-D-135 WITHDRAWN - I MISREAD THE ARTEFACT. At C6 I reported that the below-floor serve 'keeps a question for a cell it dropped, anchored to a sitting that does not exist'. The item IS flagged unscheduled: true, and sitting 10 DOES exist in this plan's own numbering - it is the dropped unit's sitting, carried verbatim in result.dropped_units. That is check 3(c) verbatim, and it is deliberate: e13 (ARV-D-037, S1) established this shape after the opposite behaviour printed 7 of 20 questions about units a class never had. I printed period_ref and not the unscheduled key beside it. The lesson: WHEN THE ENGINE HAS A DOCUMENTED STATE FOR A CASE, READ THE STATE BEFORE RATING THE OUTPUT.

ARV-D-134 DOWNGRADED S2 -> S3 and re-titled. The absence of two items at X=12 is SPECIFIED behaviour (check 3b), not a loss, and pedagogically right: Writing's cell is taught across p14's U11 AND U12, the serve stops before U12, so the class drafted the article but never did the revision sitting - and an item tests the cell's WHOLE implied_lo, becoming available only when the cell completes (founder 2026-08-05). What survives is real but smaller: the served plan says two different things - coverage_handoff carries all six cells while the paper ships four, and the only record is genon.assessment_items_unserved, which no teacher reads. A DECLARATION GAP, NOT A MIS-ANCHORING. The fix, if wanted, is one sentence in the channel the below-floor case already uses, not a change to anchoring. English is where it shows: one item per cell means holding two back is a third of the paper, where SS-secondary would hold back 2 of 18 - an argument about the Rule 2 item-count formula, not about the serve."""


def main():
    st = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s11_c9"))
    st["combos"][KEY]["C9"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C9}
    for d in st["defects"]:
        if d.get("id") == "ARV-D-135":
            d["status"] = "closed"; d["closed"] = NOW; d["at"] = NOW
            d["severity"] = "S4"
            d["title"] = ("WITHDRAWN at C9 — the below-floor item IS flagged `unscheduled` and "
                          "its sitting number is the dropped unit's own; this is check 3(c), "
                          "not a defect")
            d["evidence"] += (
                "\n\nWITHDRAWN 2026-08-12 AT C9. The item carries `unscheduled: true` and "
                "`period_ref: [10]`, where sitting 10 is the dropped unit's number in THIS "
                "plan — `result.dropped_units` carries it verbatim. C9 check 3(c) requires "
                "exactly that shape, and e13 (ARV-D-037, S1) established it after the opposite "
                "behaviour printed 7 of 20 questions about units a class never had. My C6 read "
                "printed `period_ref` without printing the `unscheduled` key beside it. Recorded "
                "rather than deleted: the misreading is the useful part — when the engine has a "
                "documented state for a case, read the state before rating the output.")
        if d.get("id") == "ARV-D-134":
            d["severity"] = "S3"
            d["at"] = NOW
            d["title"] = ("a fill serve withholds items correctly but declares nothing — the "
                          "handoff still asserts all six cells while the paper ships four")
            d["evidence"] += (
                "\n\nDOWNGRADED S2 -> S3 AT C9 (2026-08-12), and re-diagnosed. The ABSENCE is "
                "specified behaviour — C9 check 3(b): 'an item whose unit is not in the plan is "
                "not in the plan', with the count reported in `assessment_items_unserved`, which "
                "it is. It is also pedagogically right: p14 teaches Writing across U11 AND U12, "
                "X=12 stops before U12, so the class drafted the article but never did the "
                "revision sitting — and an item tests the cell's WHOLE implied_lo (founder, "
                "2026-08-05). Withholding is the anchoring doctrine working.\n\n"
                "WHAT SURVIVES: the served plan says two different things. `coverage_handoff` "
                "carries all six cells — asserting complete coverage — while the paper ships "
                "four, and the only record of the difference is a provenance field. There is no "
                "`section_coverage_note`, because nothing was dropped in the LP sense. That is a "
                "DECLARATION gap, not a mis-anchoring: contract drift a teacher notices only by "
                "counting. Remedy is one sentence in the channel the below-floor case already "
                "uses, not a change to anchoring.")
    st["updated_at"] = NOW
    STATE.write_text(json.dumps(st, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"C9 pass · ARV-D-135 withdrawn · ARV-D-134 S2->S3 · {NOW}")


if __name__ == "__main__":
    main()
