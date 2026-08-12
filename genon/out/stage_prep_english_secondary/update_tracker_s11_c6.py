#!/usr/bin/env python3
"""S11 · english · secondary — C6 (API serve checks) into the tracker, with two defects.

Run from the repo root:
    python3 genon/out/stage_prep_english_secondary/update_tracker_s11_c6.py

Full table: docs/testing_artefacts/c6_english_ix_ch07.md
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/secondary"

C6 = """RUN 2026-08-12 - PASS on the matrix, TWO S2 FINDINGS on assessment coverage. Ten serves on disk: identities to kumar1 (10/14/17), non-identities to kumar2 (16, 15, 13, 12, 11, 9), the mixed week to kumar3. Library authored at 50 min. Full table: docs/testing_artefacts/c6_english_ix_ch07.md

THE NON-IDENTITY TABLE (cells in LP | cells in assessment | items):
  X=9  fill/single -1s  (var 10, brw 10)  LP 5 [RFC VG LIS SPK WRT] | ASSESS 6 [+BYT] | 6 items | DECLARED (note + dropped_units)
  X=11 rescue/complete  (var 10, brw 17)  LP 6 | ASSESS 6 | 6 items | declared closing sitting
  X=12 fill/single      (var 14, brw 14)  LP 6 | ASSESS 4 [-WRT -BYT] | 4 items | NOTHING DECLARED
  X=13 fill/single      (var 14, brw 14)  LP 6 | ASSESS 5 [-BYT]     | 5 items | NOTHING DECLARED
  X=15 rescue/complete  (var 14, brw 17)  LP 6 | ASSESS 6 | 6 items | declared
  X=15 MIXED 60x2+50x13 (var 14, brw 17)  LP 6 | ASSESS 6 | 6 items | declared
  X=16 fill/single      (var 17, brw 17)  LP 6 | ASSESS 6 | 6 items | none needed
Identities X=10/14/17: 6 | 6 | 6, own filename, no new file written.

FINDING 1 (ARV-D-134, S2) - A SERVED PLAN CAN TEACH A CELL AND LOSE ITS QUESTION, SILENTLY, INSIDE THE BAND. At X=12 the LP covers all six cells and the assessment carries FOUR items; at X=13, five. Mechanism is exact: an item anchors at its cell's LAST unit (founder 2026-08-05), and a prefix serve can include a cell's FIRST unit and stop before its last. In p14 the last unit teaching WRT is 12 and BYT is 14; neither is served at X=12, so both items are filtered out while both cells are taught. genon.assessment_items_unserved says 2 - in the PROVENANCE block, which no teacher sees. section_coverage_note is None, dropped_units is empty, and the six-spine handoff rides in full, so the artefact asserts complete coverage while shipping a paper missing a third of itself. ENGLISH FEELS THIS HARDER THAN ANY STAGE YET because Rule 2 gives it exactly ONE item per cell: two lost items is 33% of the assessment, where SS-secondary would lose 2 of 18. And unlike the below-floor drop it is UNDECLARED and happens INSIDE the band, at counts a teacher routinely asks for.

FINDING 2 (ARV-D-135, S2) - THE INVERSE, BELOW THE FLOOR: A DROPPED CELL KEEPS ITS QUESTION. At X=9 the LP correctly drops BYT and declares it properly (coverage note names A|beyond_text, dropped_units carries the unit flagged unscheduled). But the assessment still carries Q-BT-A-1 with period_ref [10] - sitting 10 of a NINE-sitting plan. genon.assessment_items_unscheduled: 1 records it in provenance; the item is neither dropped nor marked in the artefact. The teacher is handed a question on the one thing the plan told her she would not have time to teach.

THE REST OF THE MATRIX IS AS EXPECTED. Identity fires only at the authored duration and writes no file (three identity requests, zero new files). Complete fills (12, 13, 16) return mode fill / fill_class single with uncovered_sections empty. The prefix-completes-early rows (11, 15) return complete_rescue with borrowed_from 17 - the STANDARD's synthesis unit, from a plan two counts up - and the closing-sitting note. Below-floor (9) returns non-empty uncovered_sections, a note naming exactly what was not scheduled, and dropped_units sourced from the lending plan. MIXED WEEK (kumar3, 60x2 + 50x13 = 15): duration_sequence 50 50 50 50 60 50 50 50 50 50 60 50 50 50 50 - shortest sitting opens the week, both 60s interior and NOT adjacent (positions 5 and 11) - and the scaled bands re-tile with ZERO gaps or overruns on all 15 sittings.

ONE ROW NOT RUN: X = A_top + 1 (18). The certifier's sweep proved the ENGINE path (18 and 19 both surrender), but the API's surrender RESPONSE is untested - coverage_note carrying the surrender sentence, and period_schedule_display printing the SERVED count rather than the ask (e10). One request closes it.

WHAT C7-C9 INHERIT: C9 owns both findings - they are one seam read from two sides, the item's unit resolved once at authoring time against a plan the teacher may only partly receive. C8's joint now has a number: X=11 and X=15 are the Case-1 borrows, both taking unit 17 from the standard, which is the same unit C3's ARV-D-132 flagged for requiring U15's draft article; at X=11 the host is p10, whose writing unit asks for the whole article in one sitting."""

DEFECTS = [
    {
        "id": "ARV-D-134", "combo": KEY, "step": "C6", "severity": "S2",
        "owner": "founder", "status": "open",
        "title": ("a served plan TEACHES a cell and LOSES its question — silently, inside the "
                  "band, because the item anchors at the cell's LAST unit and a prefix serve "
                  "stops before it"),
        "evidence": (
            "X=12 (english IX ch 7, variant p14): LP covers all six cells, assessment carries "
            "FOUR items. X=13: five. Neither serve declares anything — `section_coverage_note` "
            "is None, `dropped_units` is empty, and the six-spine `coverage_handoff` rides in "
            "full, so the artefact asserts complete coverage.\n\n"
            "MECHANISM, exact. An item anchors at its cell's LAST unit (founder ruling "
            "2026-08-05: an item tests the cell's whole `implied_lo`, so it becomes available "
            "only when the cell completes). p14's last-unit map is RFC 6 · VG 8 · LIS 9 · "
            "SPK 10 · WRT 12 · BYT 14. At X=12 the serve is p14's first 11 units plus one "
            "borrowed unit, so units 12 and 14 are not served — WRT's and BYT's items are "
            "filtered out while both cells ARE taught (the prefix contains their first units, "
            "and the borrowed unit first-deals BYT).\n\n"
            "`genon.assessment_items_unserved: 2` is the engine's own record of it, and it "
            "lives in the PROVENANCE block that no teacher and no export reads.\n\n"
            "WHY ENGLISH IS THE STAGE THAT SURFACES IT: assessment Rule 2 gives english exactly "
            "ONE item per (section × spine) cell — six per chapter — so two lost items is 33% "
            "of the paper. SS·secondary, with 18 items over 9 sections, loses the same way and "
            "it reads as a couple of missing questions. The mechanism is subject-agnostic; only "
            "the visibility is english's.\n\n"
            "NOT the below-floor drop (ARV-D-135 is that, and it is declared). This is INSIDE "
            "the band, at counts a teacher routinely asks for, with nothing said.\n\n"
            "The shape of a fix is a founder call and there are at least three: anchor the item "
            "at the cell's FIRST served unit when its last is not served; or keep the anchoring "
            "rule and DECLARE the loss in `section_coverage_note` the way a dropped section is "
            "declared; or refuse a fill whose prefix truncates a cell mid-run. The first changes "
            "what an item means, the second changes only what the teacher is told."),
    },
    {
        "id": "ARV-D-135", "combo": KEY, "step": "C6", "severity": "S2",
        "owner": "founder", "status": "open",
        "title": ("below the floor a DROPPED cell keeps its question — the item survives, "
                  "anchored to a sitting that does not exist in the served plan"),
        "evidence": (
            "X=9 (below the floor of 10). The LP half is exactly right: BYT is dropped, "
            "`section_coverage_note` names it (\"Time budget short of the chapter's full span: "
            "A|beyond_text could not be scheduled\"), and `result.dropped_units` carries the "
            "lost unit verbatim, flagged `unscheduled: true`.\n\n"
            "The assessment half is not. `Q-BT-A-1` is still in the paper, carrying "
            "`period_ref: [10]` — sitting 10 of a NINE-sitting plan. "
            "`genon.assessment_items_unscheduled: 1` records it in provenance; the item itself "
            "is neither removed nor marked, so a teacher who prints this assessment asks her "
            "class a question on the one thing the plan has just told her she has no time to "
            "teach.\n\n"
            "The inverse of ARV-D-134 and the same seam: the item's unit is resolved once, at "
            "authoring time, against a plan the teacher may only partly receive. Here the "
            "platform already KNOWS (it dropped the unit and said so), which is what makes this "
            "the cheaper half to fix: whatever channel declares a dropped section can drop or "
            "flag the item that tests it."),
    },
]


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s11_c6"))
    state["combos"][KEY]["C6"] = {"status": "pass", "by": "Kumar", "at": NOW, "comment": C6}
    have = {d.get("id") for d in state["defects"] if isinstance(d, dict)}
    for d in DEFECTS:
        assert d["id"] not in have, f"{d['id']} already filed"
        d.update({"opened": NOW, "closed": None, "at": NOW})
        state["defects"].append(d)
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"tracker updated · {KEY} · C6 pass · defects ARV-D-134, ARV-D-135 · {NOW}")


if __name__ == "__main__":
    main()
