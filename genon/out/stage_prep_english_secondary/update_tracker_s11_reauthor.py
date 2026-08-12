#!/usr/bin/env python3
"""S11 — the TOP canonical was re-authored to close ARV-D-136 (2026-08-12).

Closes ARV-D-136 and ARV-D-132, records the incidental clean-ups, and appends the
re-verification to the C-steps the change touches (C1, C3, C5, C7, C8).
"""
import datetime, json, pathlib, shutil
ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/secondary"

REAUTH = """

--- TOP CANONICAL RE-AUTHORED 2026-08-12 (ARV-D-136), and re-verified. ---
Only ch_07_canonical.json was regenerated; the two compacts were never touched (build resumability skipped them). Cost Rs 28.74 (in 25,609 / out 15,705), library total now Rs 109.03. Report: genon/out/library_reports/english_ix_ch07_20260812_154726.md - DETERMINISTIC CHECKS ALL PASS, registry unchanged at 6 cells, and BOTH COMPACTS still verbatim against the NEW top (the one way this could have gone wrong).

THE FIX LANDED, and the model picked up the brief's own words. The new U17 is 'Whole-Chapter Synthesis: Memory, Dignity, and Belonging', spines [reading_for_comprehension, beyond_text] - it no longer touches the writing spine at all. Its writing act is a REFLECTIVE PARAGRAPH, and the band says so: 'Students write a reflective paragraph - BEGUN AND COMPLETED IN THIS SITTING'. Materials are 'Notebook or writing paper for reflective paragraph' - a blank, not a produced artefact. The teacher note goes further: 'The reflective paragraph task begins and ends within this sitting; students should not attempt to extend or revise work from other units.' Artefact scan on the new file: 0 hits of ANY family.
And the cause was fixed too, not just the symptom: U15 now drafts the COMPLETE article in its own sitting (model format 0-10, plan 10-20, draft all four paragraphs 20-42, peer read 42-50), which is what both compacts already did.

BOTH FORMERLY-JUMPY TRANSITIONS ARE NOW CLEAN. X=11 (p10 prefix) and X=15 (p14 prefix) both end on the new synthesis: LP cells 6, items 6, unserved 0, unscheduled 0. Nothing in the closer presumes a sitting the host never had.

INCIDENTAL CLEAN-UPS - the re-authored top also cleared three of C3's accepted findings, without being asked to: ARV-D-129 (Rule 4 diversity: 'shared-reading' x3 consecutive - now zero >2 runs), ARV-D-130's top-file half (five MCQ/SCR leaks into teacher-facing prose - now zero; p10's U4 note still carries one), and most of ARV-D-131 (the 20-word task_brief is gone; 20 briefs, all located, none over 18. Rule 11 bullets over 12 words: 5 -> 1). What did NOT clear: one section_context at 19 words (cap 18) and that one bullet - both the same accepted numeric-cap family.

WHAT DID NOT CHANGE, correctly: ARV-D-134 and ARV-D-135 are p14/p10 prefix defects, not the top's, so X=12 still loses 2 items, X=13 loses 1, and X=9 still carries its unscheduled beyond_text item. Re-measured after the re-author to be sure.

ONE THING GOT THINNER: the library now has ZERO options-bearing items (the old top's single TRUE_FALSE came back as a FILL_IN), so 'options arranged: 0 of 0'. C4's item-2 finding stands and is now stronger - the MCQ path, A9's arrangement and the keyed option-reveals are untested at this stage, and their owner is the first MCQ-bearing english chapter."""


def main():
    st = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s11_reauthor"))
    for step in ("C1", "C3", "C5", "C7", "C8"):
        st["combos"][KEY][step]["comment"] += REAUTH
        st["combos"][KEY][step]["at"] = NOW
    st["combos"][KEY]["provenance"]["ledger_ts"] = (
        "top RE-AUTHORED 20260812_154726 (ARV-D-136) · p14 20260812_142352 · "
        "p10 20260812_142824 (cert report 20260812_154726, ALL PASS)")
    st["combos"][KEY]["provenance"]["stages"]["reruns"] = {
        "wall_s": "279.0", "tokens_in": "25609", "tokens_out": "15705", "cost_inr": "28.74"}
    st["combos"][KEY]["provenance"]["total_cost_inr"] = 109.03

    for d in st["defects"]:
        if d.get("id") == "ARV-D-136":
            d["status"] = "closed"; d["closed"] = NOW; d["at"] = NOW
            d["evidence"] += (
                "\n\nCLOSED 2026-08-12 BY RE-AUTHORING THE TOP (Rs 28.74; the compacts were not "
                "touched). The new U17 drops the writing spine entirely, its writing act is a "
                "reflective paragraph 'BEGUN AND COMPLETED IN THIS SITTING', its materials are a "
                "blank notebook, and its teacher note says outright: 'students should not attempt "
                "to extend or revise work from other units.' The model used the brief's own "
                "words. X=11 and X=15 re-inspected: both CLEAN. Artefact scan on the new file: 0 "
                "hits of any family. Registry unchanged, both compacts still certify against the "
                "new top.")
        if d.get("id") == "ARV-D-132":
            d["status"] = "closed"; d["closed"] = NOW; d["at"] = NOW
            d["evidence"] += (
                "\n\nCLOSED 2026-08-12 — superseded by the ARV-D-136 re-author. This row was the "
                "C3 (authoring) reading of the same unit and was ACCEPTED as authored; the "
                "artefact it describes no longer exists on disk. The `materials` line and the "
                "'complete the draft' band are both gone from the re-authored U17.")
        if d.get("id") in ("ARV-D-129", "ARV-D-130", "ARV-D-131"):
            d["evidence"] += (
                "\n\nPARTLY OVERTAKEN 2026-08-12 by the ARV-D-136 re-author of the TOP canonical "
                "(this row stays `accepted`, not closed, because the finding was accepted as a "
                "RATE across the stage). On the new top: Rule 4 has no >2-consecutive method run; "
                "zero internal type codes in teacher-facing prose; 20 briefs, none over 18 words, "
                "all located; expected_elements bullets over 12 words 5 -> 1. What survives on "
                "disk: one section_context at 19 words, one over-long bullet, and p10 U4's "
                "'The MCQ on emotion' note.")
    st["updated_at"] = NOW
    STATE.write_text(json.dumps(st, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"tracker updated · ARV-D-136 + ARV-D-132 closed · C1/C3/C5/C7/C8 re-verified · {NOW}")


if __name__ == "__main__":
    main()
