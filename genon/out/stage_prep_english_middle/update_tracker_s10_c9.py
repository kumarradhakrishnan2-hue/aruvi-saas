#!/usr/bin/env python3
"""S10 · english · middle — C9 (assessment anchoring across the serve) into the tracker."""
import datetime, json, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/middle"

C9 = """PASS 2026-08-13 - zero mis-anchored items across six serves (X=5, 6, 8, 9, 11, 13), re-served from the REPAIRED canonicals. One sub-clause of check 3c is NOT met and it is a PLATFORM gap, not this stage's - recorded below, no defect raised against S10.

CHECK 1 - PREFIX REMAP. PASS on all six. Every served item's `period_ref` falls inside 1..N for that plan's own N; zero outside. Anchor spread, sitting -> item count:
    X=5   {2:1, 3:3, 4:2, 5:2}  + 6:2, 7:2 on the DROPPED units
    X=6   {2:1, 3:3, 4:2, 5:2, 6:2} + 7:2 dropped
    X=8   {2:1, 4:2, 5:2, 6:2, 7:2, 8:1}
    X=9   {2:1, 4:2, 5:2, 6:2, 7:2, 8:1, 9:1}
    X=11  {3:1, 5:1, 6:2, 7:2, 8:2, 9:2, 10:1}
    X=13  {3:1, 5:1, 6:2, 7:2, 8:2, 9:2, 10:1, 11:1}  (surrender: the full 12 served)

CHECK 2 - THE BORROWED UNIT BRINGS ITS OWN ITEMS. PASS, and the interesting row is the one that brings NONE.
    X=5  fill sitting 5 carries Q-W-B-1, Q-W-B-2 - the WRITING pair, and the fill unit is p07 U5 "Imagining Other Worlds: Writing from a Baby's and a Fish's..." (writing spine). Match.
    X=6  fill sitting 6 carries Q-VG-B-1, Q-VG-B-2 - the VocGram pair against p07 U6 "Rhyming Words and Describing Words". Match.
    X=8  fill sitting 8 carries Q-BT-B-1 against p10 U9 "Homes and Materials" (beyond_text). Match.
    X=9  fill sitting 9 carries Q-BT-B-1, same unit. Match.
    X=11 fill sitting 11 carries NOTHING - and that is CORRECT, not a miss. The borrowed unit is the mandated SYNTHESIS unit, which teaches no cell of the registry, so no item can anchor to it. S11's sign-off predicted exactly this ("C9.2's 'a borrowed unit brings its own items' is vacuous for the closing unit at this stage; maths middle and maths prep are in the same position"), and this is its live confirmation on a fourth stage. What C9 must check in its place is that the standard's twelve items and a compact's twelve are the SAME SIX CELLS - which C4 did (6 contributions x 2 = 12 on all three files).

CHECK 3a - NO EMPTY period_ref ANYWHERE. PASS, all six serves, including the unscheduled items (which carry a real ref, to their dropped sitting).

CHECK 3b - UNSERVED-ANCHOR ITEMS ARE ABSENT AND COUNTED. PASS, and the counts are coherent unit by unit rather than merely non-zero:
    X=8  10 items served, `assessment_items_unserved` = 2 - the prefix is p10 units 1-7 plus U9, so items anchored at p10 U8 and U10 are absent. Two units withheld, two items gone.
    X=9  11 items, unserved = 1 - prefix is units 1-8 plus U9, so only p10 U10's item is absent.
    X=11 11 items, unserved = 1 - the withheld unit is the top's U11, and the top's beyond_text PAIR splits across U10 and U11, so exactly the U11 item goes with it.
  That last row is e13 working in the open: "an item whose unit is not in the plan is not in the plan". The withheld unit's question leaves with the unit rather than being re-anchored somewhere plausible.

CHECK 3c - BELOW-FLOOR: DROPPED UNITS' ITEMS PRESENT, NUMBERED IN THIS PLAN, FLAGGED. PASS on the items; the HANDOFF half is not met (below).
    X=5  served 5; `result.dropped_units` carries units numbered 6 and 7 with `unscheduled: true`; their four items (Q-VG-B-1/2, Q-BT-B-1/2) are PRESENT, anchored [6] and [7], each flagged `unscheduled: true`.
    X=6  served 6; drops unit 7; its two beyond_text items present, anchored [7], flagged.
  ONE HONEST LIMIT ON THIS EVIDENCE: the rule says the dropped unit's sitting number must be THIS plan's, "never the lender's own numbering". On this library the two are IDENTICAL - the prefix is a true prefix of the 7-canonical, so its units 6 and 7 are also sittings 6 and 7 - and the check therefore cannot distinguish a correct implementation from the defect it was written against. It passes, but it does not PROVE. A stage whose below-floor lender is not a prefix of the served plan is what would test it.

CHECK 3d - EXPORTS OMIT EXACTLY THE UNSCHEDULED ITEMS. PASS, verified through the API's own code path (api/main.py:1179) rather than by calling the port directly:
    X=5  12 items -> export renders 8, the four unscheduled omitted, zero leaked.
    X=6  12 items -> export renders 10, the two unscheduled omitted, zero leaked.
  Worth recording HOW that is achieved, because it is not the port's doing: the filter lives once in api/main.py and runs THROUGH THE CARRIER SEAM (`raw_item_list` -> filter -> `from_engine_items` -> `item_container`), which is the shape ARV-D-063 built after the same line, written as a bare list walk, made every science·IX export 500. No subject plugin knows the word `unscheduled` - grep is 0 across all five - and that is the right place for it.

CHECK 4 - NO CROSS-VARIANT REFERENCES. PASS, and VACUOUSLY so on this library, which is worth saying plainly rather than banking: every fill in the sweep reports `self_fill: true`, so no serve mixes two variants at all. The check cannot fail here because the condition it guards against never arises. That is engine e14's self-preference again (see C8), and it means cross-variant item provenance is UNTESTED at this stage rather than proven.

── THE ONE THING NOT MET, and it belongs to the platform ──────────────────────
3c says the dropped units' handoff rows must be "restored and flagged". On a below-floor english serve they are RESTORED - all six spine cells present with their contributions - but NOT FLAGGED: a contribution carries only {implied_lo, section_context, section_id, section_title, section_type, tasks_anchored}, and no `unscheduled` key appears on the two cells whose units were dropped. So anything reading the handoff to learn what the class was actually taught over-reports coverage on a below-floor plan.
THIS IS NOT AN ENGLISH DEFECT. `carriers.py` sets that flag in exactly ONE place (line 875, `entry["unscheduled"] = True` when all of a row's LOs are unscheduled) and that place is the SCIENCE-SECTION handoff shape. Neither of the other two shapes sets it: `_goal_clusters_from_engine` (mathematics, since S7) and `_spine_cells_from_engine` (english, since S11) both carry zero occurrences. So the flag is implemented on one handoff shape of three, and maths·middle passed its own C9 with the same gap open. Recorded here as a cross-stage observation for the founder rather than raised against S10, since the practical bite today is small: nothing in the request path reads the flag, the ITEMS are correctly flagged, and the export filter keys off the items rather than the handoff.

── AN ASYMMETRY WORTH THE HUMAN GATE'S ATTENTION (not a C9 check) ─────────────
On the SCREEN, a below-floor plan renders all twelve questions, the four belonging to dropped units among them, with nothing marking which. The dropped LESSON units are cleanly separated - /view puts them in `vm["dropped_lp"]` with `dropped_sections` beside them - but their QUESTIONS sit in the ordinary assessment list, and the `unscheduled` flag does not survive into the view's item meta. That is arguably correct by e09's design ("dropped units ride into the VIEW only... online is an option, not an imposition"), and the export is what the founder ruled must stay clean. But the lesson and its questions are presented to opposite standards, and a teacher on a 5-period plan sees four questions for two sittings she was told she is not getting.

EXIT MET: zero mis-anchored items; no item carries an empty ref; every unserved-anchor item is absent and counted."""


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s10_c9"))
    state["combos"][KEY]["C9"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C9}
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"tracker updated · {KEY} · C9 pass · {NOW}")


if __name__ == "__main__":
    main()
