#!/usr/bin/env python3
"""Write S11 (english · secondary) P1-P5 + SIGN into the campaign tracker state.

Run from the repo root:
    python3 genon/out/stage_prep_english_secondary/update_tracker_s11_prep.py
Then reload docs/testing_tracker.html.

Full note: genon/out/stage_prep_english_secondary/STAGE_SIGNOFF_S11_english_secondary.md
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/secondary"

ROWS = {
    "P1": ("pass", "Claude", """AMENDED 2026-08-12. LP constitution v1.1 -> v1.2. Reference: SS-secondary v1.10, read through the mathematics middle/preparatory adaptation - english is the THIRD stage-family in the period-field carrier family, so the anchoring work ports from rows 4/5.

A1: INPUTS 3 was '{ period_duration_minutes, period_count }, where period_count = B is supplied at generation time (allocation tab suggests; user may override)' - which licensed exactly the mixed-duration, teacher-chosen plan the variant engine cannot use. Now 'exactly ONE row { period_duration_minutes, period_count }: the class-standard duration (40 min for classes up to VII, 45 for VIII, 50 for IX-X - the master-plan calibration bands, not NCF's flat 40) x the period count ... handled downstream at serve time.' Class IX's standard is 50 min, matching the master_plan row. Declared deviation: 'serve time', not 'partition time' - the same correction S3, S4, S6, S7 and S8 made.

A5+A7 THE SELF-CONTAINED REGISTER: ONE block after VOCABULARY, v1.10 THREE-ban re-cut (not S6's two-ban exception - english units travel between plans under the X-1+1 fill, so ban 2 binds in full). Bound to Rule 9 (band narration) and teacher_notes by reference. Illustrative strings are english ones. TWO consequential edits, the same two S7 and S8 made: VOCABULARY was TEACHING the positional cross-reference (its examples were literally 'the previous unit', 'this unit') and now names the CONTENT built on, with 'session' joining the excluded register; and the teacher_notes schema comment asked for 'transition from prior / PREVIEW NEXT' - the forward half being the direct contradiction testing.md P1 names for this constitution family.

FOUR NON-CARRY-FORWARD EDITS, all founder calls taken here because P-prep is where they are free (no library exists):
1. FULL SPINE COVERAGE (Rule 2 STEP 3). The rule licensed a short plan to stop and leave later spines unanchored, and the corpus does it: backup/saved_plans/english/ix/ch_12_*.json (4 periods) carries NO beyond_text contribution at all. Under v2.0 a chapter's canonicals must share ONE registry - a compact is the same chapter in fewer periods, not a smaller chapter - so an authoring-time drop breaks the Xth-unit choice set before serve runs. Coverage is now mandatory at every count; curation stays at TASK level where Rule 3 governs it. Rule 10's 'spine with no anchored tasks' clause rewritten to match: absent-from-summary is a state, dropped-for-time is a defect.
2. Rule 1 gains the closing-unit exception: 'exactly ONE main_section and one or two ADJACENT spines' cannot describe a whole-chapter closer, which the platform brief mandates of the standard. S8's lesson applied without paying for it twice (S7 met it at C3 as ARV-D-094). No V-rule enters the constitution.
3. task_brief 12 -> 18 words, locator counted in. Rule 9 mandates the brief carry '<Subheading> (p.NN): <plain brief>', which eats 3-4 of the 12. Measured: 17 of 28 real IX briefs exceed 12; 27 of 28 fit 18.
4. section_context 10-15 -> 10-18 words. Measured: 3 of 11 IX contributions run 16, 16, 17. Lower bound kept.
Also: Rule 2 STEP 1's task budget named a 40-min and a 60-min period but NOT the 50-min class standard this stage authors at. It now does (<= 3-4 tasks).

NOT DONE, deliberately (founder ruling 2026-08-10): no field invented to feed the serve engine. section_anchor is NOT added to the period; the anchor is mediated from section_id + spines_taught[]. That is P5.5's work. Guards assert the absence.

Artefacts in genon/out/stage_prep_english_secondary/: lesson_plan_constitution_v1.1_pre.txt, lp_v1.1_to_v1.2.diff, apply_s11_amendments.py (every edit asserts exactly-one occurrence; the run closes on guards for the struck A9 strings, the retired phases shape, band_id, phase_ref, section_anchor, the cancelled amendments' vocabulary and the V-rules)."""),

    "P2": ("pass", "Claude", """AMENDED 2026-08-12. Assessment constitution v1.3 -> v1.4. Paired with LP v1.2.

A6: landed as a NEW RULE (8A), because the anchoring facts had no home in this file - Rule 8 (SOURCE TAGGING) is a field inventory, not a rule about linkage. The two fields that carry the anchor (source_section_id + source_spine) were already mandated, but nothing said they WERE the anchor, nothing said what the platform does with them, and nothing forbade a unit number beside them. English is 8-rule ROW 7, the period-field family, and THE ONLY PAIR KEY IN THE TABLE: the platform resolves the (section x spine) CELL against each period's own section_id + spines_taught[] - no coverage_handoff in the path, and the LO rides on the item (source_lo) so it needs no bridge either. Rule 8A records: the cell IS the anchor and there is no third field to emit; a cell taught across several units anchors at the LAST of them (founder 2026-08-05); and period_ref / period_number / unit_ref MUST NOT be emitted, because declaring the link would freeze an arrangement the platform varies per teacher. Same shape as science-secondary v1.2, science-middle v1.4, maths-middle v3.3, maths-prep v1.3: derive the link, never demand it. grep -c phase_ref = 0.

A9 - TWO ADDITIONS, no removal, no arrangement rule. REMOVAL is N/A: this file never carried the MEMORY item-18 position prohibition (testing.md names the four files that do; this is not one). Confirmed by grep: consecutive, same label, vary in position all 0. ADDED in RULE 4, where english states its MCQ semantics (declared deviation from the reference, which puts it in the answer-layer rule; english's Rule 5 is an indented bullet list where a two-paragraph block would read as part of the MATCH bullet): the option-order mandate and the by-label option-reference prohibition ('both A and B', 'none of the above', 'all of the above', 'either B or C'). Purely additive - no prior 'none of the above' ban. NOT re-added and asserted absent: alphabetically, never led with, first word at which they differ.

ALSO: item-count invariance stated at Rule 2, following the LP's new coverage mandate - the count does not vary with the period count, so a shorter plan yields the same cells and the same items, tested on less anchored practice, never a shorter assessment. Stated because Rule 2's count formula is where a reader would otherwise infer the opposite.

Both footers were already correct (the first stage in four where they had not drifted) and now track the new headers.

Artefacts: assessment_constitution_v1.3_pre.txt, assess_v1.3_to_v1.4.diff."""),

    "P3": ("pass", "Claude", """APPLIED 2026-08-12 - english secondary is GROUP B and the conversion was REAL (the fourth such stage, after S6, S7 and S8).

phases[{minutes, description}] -> time_bands[{minutes, activity}]: array and key both renamed, with Rule 5 (the time constraint), Rule 9's heading (PHASE NARRATION -> BAND NARRATION) and prose, Rule 2A's 'explicit timed phase' (the one place the word carried pedagogical weight - it is the rule that makes reading aloud class time), Rule 3, Rule 7, Rule 8 and the schema following. NO band_id in the target shape.

Guards: grep -c 'phases[' = 0, '\"phases\"' = 0, band_id = 0, time_bands = 2, '\"activity\": string' present.

THIS STAGE NEEDED A STEP THE OTHERS DID NOT. The english plugin read p['phases'] only (lesson_plan_to_view, both the typed spine and the activity lines), so a converted constitution would have rendered every EXISTING english plan - the whole corpus, at all three stages - with no timed spine the moment a new one arrived. The both-keys-newest-first read landed with the conversion as english/subject.py::_bands, exactly as mathematics carries it (subject.py:211-219). normalize.phases_from already accepted either text key, so nothing below that line had to change."""),

    "P4": ("pass", "Claude", """DONE 2026-08-12.
- data/content/constitutions/lesson_plan/english/secondary/CHANGELOG.md: existed (created 2026-08-11 by the cross-stage curly-quote pass); gains the v1.2 entry with the carry-forward and the four measured edits, each with its measurement.
- data/content/constitutions/assessment/english/secondary/CHANGELOG.md: created. v1.4 entry, plus back-fills of v1.1 (Rule 4's 'NAME THE REFERENCED WORD', 2026-07-13, MEMORY item 10) and v1.0 (the fork from middle v3.1) from the only surviving record.

RECORDED AS A GAP RATHER THAN GUESSED AT: v1.2 and v1.3 of the assessment constitution are undocumented - no sidecar, no in-document history, MEMORY's constitution inventory stops at v1.1, and data/ is git-ignored. Third stage running where a version moved without a record (S8 found the same on both mathematics-preparatory files). Nothing in the v1.4 pass depends on knowing what they were.

Neither constitution carried an in-document version-history block, so nothing had to be lifted out; the VERSION line stays in the file. Both footers were already correct and now track the new headers."""),

    "P5": ("amber", "Claude", """RECORDED 2026-08-12 - PROVISIONAL, P5.4 OPEN (founder ruling 2026-08-02 permits signing with P5.4 open; C6 is the hard stop). P5.5 IS CLOSED, so C1 is NOT gated.

P5.1 THE FLOOR - accepted at the standing ratio for the pilot: round(0.6 x 17) = 10, matching floor_periods_at_standard. Equal dispersion over [10, 17]: A-C = 7 >= 4, so counts are [17, 14, 10]. ONE OVERRIDE IS OWED ELSEWHERE IN THE CLASS as a consequence of the coverage mandate: a six-spine chapter needs >= 4 periods (VocGram alone per Rule 2 STEP 4, plus five spines at <= 2 adjacent), and ch 12 'A Friend Found in Music' is the only chapter in the class whose floor (3) falls below it. Raise it to 4 - counts become [5, 4] - immediately before ch 12 is authored at pre-warm, NOT now: master_plan.py regeneration wipes these rows (the runbook pair at 0.3), and the pilot is unaffected.

P5.2 THE SECTION REGISTRY - the step this template names english explicitly for, and the definition it asked for. THE REGISTRY MEMBER IS THE (section x spine) CELL. Not the main_section: post-split every english chapter is ONE, so section_id is a constant and looks like no axis at all. Not the spine either: the constitution permits 1-3 main_sections and the middle fixture is a live example - sections A, B and C each teach Reading, and joining on the spine alone collapses three cells into one. The constitution's own DESIGN PRINCIPLE already says this ('period bin-packing is across (section x spine) cells, NOT across spines alone') and Rule 1 makes the order strict, which is V2's first-visit requirement satisfied by the constitution rather than by a new rule. TOKEN: '<section_id>|<spine_key>', e.g. A|reading_for_comprehension, joined 'A|listening / A|speaking' for a two-spine unit. Both halves are authored closed vocabulary, so the registry is stable across a chapter's canonicals BY CONSTRUCTION; the on-page section_name is deliberately not used (ch 7's reading cell is the 9-word merged string 'Reflect and Respond + Reading for Meaning + Check Your Understanding + Critical Reflection'). FIRST-VISIT ORDER is the summary's on-page spine order - for ch 7: Reading, VocGram, Listening, Speaking, Writing, Beyond - and it is NOT the canonical enumeration order the handoff is keyed by. Those two orders are deliberately different (Rule 2 STEP 3 says so) and a C5 check that compares one against the other will fail a good plan. SIX MEMBERS AGAINST SEVENTEEN UNITS is the thinnest ratio in the campaign; C8's borrow will nearly always be the opening unit of a cell.

P5.3 THE PILOT - english|IX ch 7 'Vitamin-M'. Summary and mapping on disk, placeholder false, canonical_plan present, counts [17, 14, 10]. Chosen (founder) over ch 13, ch 11 and ch 3 on band width: 17 -> 10 is the widest in the class, so the compacts have the most condensation room and C8 has the most to look at. THE COST IS NAMED: it is also the largest chapter (three runs at 17/14/10), and it is PROSE, so the drama branch - drama_summary, role-assigned reading, act-splitting, a whole [SECONDARY DELTA] path through Rules 1, 2A, 3 and 4 - is NOT exercised by the pilot. ch 11 is the only drama in class IX; the pre-warm sweep owes it a run.

P5.4 THE THREE PROFILES - OPEN, stage signed provisionally. Class IX, different sections per identity, one duration longer than 50 alongside the standard so C6's mixed-duration matrix has something real. Through the app's own first-run flow, never by hand-editing JSON.

P5.5 THE CARRIER - CLOSED, and it is the one carrier in the campaign where 'delegate to the family helper' was the WRONG answer. Trace: rule 7 . period-field family . item (source_section_id + source_spine) -> period (section_id + spines_taught[]) . container: a list of SPINE groups each carrying items[] . plugin method EnglishSubject.assessment_to_view (shipping for the app since before the campaign) . genon_assessment present as of 2026-08-12 . not in _NOT_YET. See the SIGN row for why the helper was wrong and what landed instead."""),

    "SIGN": ("pass", "Claude", """S11 IS CLEAR TO ENTER C1 (2026-08-12). P1-P5.5 complete; P5.4 amber by design, C6 its hard stop. No gate carried into the C-cycle. Full note: genon/out/stage_prep_english_secondary/STAGE_SIGNOFF_S11_english_secondary.md

THE FINDING THAT WOULD HAVE COST MONEY, and it is about the word 'delegation'. items_by_period_field is the obvious thing to hand english to: it is the period-field family, S7 and S8 both used it. Running it here would have been wrong twice. (1) It joins ONE code against one period field; english's key is a PAIR - and passing source_spine alone is the error that would have LOOKED correct, because every english IX chapter has a single main_section, so it produces right answers across the entire certified class and fails only on the multi-section chapters S9 and S10 are full of. (2) It anchors every item of a group at the group's last unit, which would undo the N-to-N pairing the display path has carried since 2026-07-11 - two items of one cell taught over two units belong one per unit, and anchoring both at the close is exactly the defect that pairing was written to fix, re-created on the served side where a teacher meets it. So the delegation was made LITERAL: the join, the pairing and the section-wide fallback were lifted out of assessment_to_view into english/subject.py::cell_resolver, and BOTH paths now call it - the screen and the served file cannot disagree because there is one resolver. Genon adds only the anchoring RULE, through a new carriers.items_with_units (the third family's second helper): a cell taught across several units anchors at the LAST of them.

THREE PLATFORM ITEMS LANDED WITH IT, none of them stage-specific. (a) carriers.group_key - item_container and _stamp_group_keys keyed groups on section_code and fell back to the LIST INDEX; english keys spine_code, and a positional key is safe only while both sides of a serve are the same list in the same order, which is exactly what stops being true when a unit and its item are BORROWED. (b) _ENGLISH_SPINE_CELL - english's coverage_handoff is a spine-keyed DICT of section_contributions[], a THIRD handoff shape; it fell through to_engine_handoff unchanged, serve read c['los'] as empty and filtered nothing, so a served 8-unit plan would have carried the full six-cell coverage of the 17-unit canonical, claiming spines the class never met. Identical defect to the one _MATHS_GOAL_CLUSTER was written for at S7. One difference recorded in code: a spine left with no surviving cell is DROPPED, where a maths goal cluster is kept empty - assessment Rule 1 omits a spine with zero contributions. (c) English joined the synthesis-reads-as-Synthesis probe, whose docstring had asked for exactly this decision when the carrier landed: it is a section-grouped port, so without the fix a whole-chapter closer would have been filed under whichever spines it revisits ('Listening + Writing') - ARV-D-016's and ARV-D-101's shape on a fourth port.

VERIFIED ON THE REAL SAVED SHAPE, not an invented fixture: backup/saved_plans/english/ix/ch_11_20260608_213837.json - 7 units over one main_section, 6 items in 6 spine groups. All 6 resolve, ZERO orphans, every unit_ref a singleton, and every anchor equal to the independently computed 'last unit teaching this cell' (RFC spans 1-3 -> anchors at 3; VocGram spans 4-5 -> 5; listening and speaking share 6; writing and beyond_text share 7). genon_unit_anchor returns 'A|reading_for_comprehension' and 'A|listening / A|speaking', and equals period_section_codes split on the joiner for every unit - the anchor and the join code are ONE expression, not two agreeing ones. With its bands in the P3 shape the plan compiles: 30 phases, 7 units, 6 items anchored, registry = the six cells in first-visit order. On its authored phases[] shape compile_stream raises KeyError('time_bands'), which is correct - compile v0.5 is declared-only and the corpus predates P3.

tests/test_genon_carriers.py: 97 tests with 8 failures -> 113, GREEN. The eight failures were the 'english is a declared-field stage / english is still owed' assertions, which is precisely what this step invalidates; replaced by TestEnglishSecondaryLanded (thirteen) plus three brief-carrier tests. Full suite otherwise green (test_api fails on a missing fastapi in the sandbox - environmental, pre-existing).

P5.4 remains the only open item and C6 is its hard stop."""),
}


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s11"))
    row = state.setdefault("stages", {}).setdefault(KEY, {})
    for step, (status, by, comment) in ROWS.items():
        row[step] = {"status": status, "by": by, "at": NOW, "comment": comment}
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"tracker updated · {KEY} · {', '.join(ROWS)} · {NOW}")


if __name__ == "__main__":
    main()
