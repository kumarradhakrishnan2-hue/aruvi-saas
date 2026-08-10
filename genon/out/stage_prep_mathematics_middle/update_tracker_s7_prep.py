#!/usr/bin/env python3
"""Write S7 (mathematics · middle) P1-P5 + SIGN into the campaign tracker state.

Run from the repo root:
    python3 genon/out/stage_prep_mathematics_middle/update_tracker_s7_prep.py
Restart the API afterwards, or just reload docs/testing_tracker.html.
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "mathematics/middle"

ROWS = {
    "P1": ("pass", "Claude", """AMENDED 2026-08-10. LP constitution v3.3 -> v3.4.

A1: INPUTS 4 was 'Period schedule: {duration, count} ROWS; total = B' - which licensed exactly the mixed-duration plan the variant engine cannot use. Now 'exactly ONE row {duration_minutes, count}: the class-standard duration (40 min for classes up to VII, 45 for VIII, 50 for IX-X - the master-plan calibration bands, not NCF's flat 40) x the period count; total = B. Teacher timetable variation never reaches generation; it is handled downstream at serve time.' The schema's period_duration_minutes carries the same constraint where it is actually read. Declared deviation: 'serve time' not the reference's 'partition time' - the partition engine was retired 2026-07-31 (same correction S3, S4 and S6 made).

A5+A7 THE SELF-CONTAINED REGISTER: ONE block after VOCABULARY in the v1.10 THREE-ban re-cut (this stage is NOT S6's two-ban exception - its units anchor to textbook sections and travel between plans, so ban 2 binds in full). Bound at Rule 10 (band narration) and at the teacher_notes schema comment by reference, never as scattered prohibitions. Declared deviation: illustrative strings are middle-maths ones ('a quick mental calculation', 'an extended construction', 'having covered all three angle pairs', 'Having established that vertically opposite angles are equal, ...'). Two consequential edits, both following the reference: VOCABULARY was TEACHING the forward reference ban 2 forbids - its cross-reference examples were literally 'the previous unit', 'this unit' - so the examples are dropped and 'session' joins the excluded register; and the teacher_notes continuity bullet ('briefly recap what the previous unit covered') is now position-free, naming the content built on.

Stale footer corrected: it had been left at 'Version 3.1' through the 3.2 and 3.3 bumps.

NO NEW FIELD (founder ruling 2026-08-10). section_anchor was NOT added to the period object. maths-middle already carries the fact under another name - textbook_segments[].ref - and the prototype resolved exactly this shape variance at the READ boundary (lp_pdf_generator.py:2583-2592: 'Prefer textbook_segments when present, else section_anchor'). The SaaS keeps that answer and moves it to the plugin seam; that is P5.5's work, not P1's. The edit script asserts the absence as a guard.

No pedagogical rule changed: Rules 1-5, 7-9 and 11 byte-identical in force. Artefacts in genon/out/stage_prep_mathematics_middle/ (pre-file, lp_v3.3_to_v3.4.diff, apply_s7_amendments.py - every edit asserts exactly-one occurrence)."""),

    "P2": ("pass", "Claude", """AMENDED 2026-08-10. Assessment constitution v3.2 -> v3.3.

A6-confirm: CONFIRMED, not amended. Items already carry section_ref, copied verbatim from the LP handoff entry. Middle mathematics is the PERIOD-FIELD family (verified 8-rule row 4): the platform resolves section_ref against each period's own textbook_segments[].ref, with NO coverage_handoff in the path - so the reference's period_ref field is not ported, and neither is secondary's section_number. Added an ANCHORING (PLATFORM INTEGRITY) block, which the file had none of, recording four things: section_ref IS the anchor and is pass-through; a section spanning several units anchors at the LAST of them (founder 2026-08-05 - an item tests the section's whole goal, so it becomes available only when the section completes); period_ref / period_number / any unit number MUST NOT be emitted, because declaring the link would freeze an arrangement the platform varies per teacher; and anchor_id is NOT an anchor in this sense (Rule 8) - it seeds the exercise companion only. Same doctrine as science-secondary v1.2 and science-middle v1.4: derive the link, never demand it. grep -c phase_ref = 0.

A9 - the REMOVAL is N/A, so it landed as TWO LINES ALONE (the S4 shape). This file never carried the MEMORY item-18 position prohibition; testing.md P2 names four files that do (SS + Science, middle and secondary) and this is not one. Confirmed by grep: 'consecutive', 'same label', 'vary in position' all 0. Nothing was struck. ADDED in Rule 10's MCQ block, v1.7 wording: the option-order mandate (order carries no meaning, not yours to set, emit as authored, uneven letters are coincidence not a defect) and the by-label option-reference prohibition ('both A and B', 'none of the above', 'all of the above'). This file carried no prior none/all-of-the-above ban, so the addition is purely additive. NOT re-added and asserted absent by the edit script: 'alphabetically', 'never led with', 'first word at which they differ'.

No pedagogical rule changed: Rules 1-9 and the whole JSON schema byte-identical apart from the two additions. Artefacts: assessment_constitution_v3.2_pre.txt, assess_v3.2_to_v3.3.diff.

Standing renderer debt flagged for the C-cycle rather than the constitution: Rule 7 permits a 'number_line:' stimulus at this stage and prohibits SVG (unlike secondary). Confirm at C13 that both renderers still carry a number_line branch - a permitted format with no detection branch is a known failure mode."""),

    "P3": ("pass", "Claude", """APPLIED 2026-08-10 - mathematics middle is GROUP B, and this is the second stage where the conversion was real (after S6; S1/S2/S3/S4 were all Group A / N-A).

LP schema: phases[{minutes, description}] -> time_bands[{minutes, activity}], both the array name and the description key renamed. Rule 6's prose follows ('Each period's time bands sum exactly to period_duration_minutes. Minimum 3 time bands per period'), as do Rule 8, Rule 10's heading (PHASE NARRATION -> TIME-BAND NARRATION) and its two prose references, Rule 11's guard case, and the schema's textbook_items description comment. NO band_id in the target shape - the band layer left the declaration surface at compile v0.5 and ids are derived internally. The edit script asserts no 'phases[', no '\"phases\"' and no band_id survive, and that time_bands is present twice (Rule 6 + schema).

WHY THIS ONE WAS AMENDED WHEN THE ANCHOR AND THE HANDOFF WERE NOT (founder call, 2026-08-10). compile.py does not merely READ the bands - it rebuilds the timed spine from p['time_bands'] (:124) and asserts an inventory invariant over tb['activity'] (:208-210). A tolerant read at the seam could not carry that, so testing.md P3 stands and S6's 2026-08-07 conversion is followed.

Corpus consequence, expected and not a defect: the existing maths middle/prep saved plans stay on the old shape. The prototype's tolerant read still covers display, and the new tests rename the bands in a deep copy of the maths_vi_ch05_saved fixture for exactly this reason."""),

    "P4": ("pass", "Claude", """DONE 2026-08-10. CHANGELOG.md created beside BOTH amended constitutions:
- data/content/constitutions/lesson_plan/mathematics/middle/CHANGELOG.md (v3.4)
- data/content/constitutions/assessment/mathematics/middle/CHANGELOG.md (v3.3)

Each lists the bump with date and per-amendment rationale, including the declared deviations (serve time vs partition time; the middle-maths illustrative strings; the derived period-field anchor in place of the reference's period_ref; A9's N-A removal half) and the founder ruling of 2026-08-10 with the prototype citations behind it. Neither constitution carried an in-document version-history block, so nothing had to be lifted out; the VERSION line stays in the file and nothing in the sidecars is read at generation time.

The LP sidecar also records the §9 reading: this IS a constitution change in the full sense (bounds tightened, new obligations created), so the relaxation-only carve-out does not apply - it costs nothing only because no library for this stage has been authored yet, which is exactly what the §3 ordering rule buys."""),

    "P5": ("amber", "Claude", """RECORDED 2026-08-10 - PROVISIONAL, P5.4 OPEN (founder ruling 2026-08-02 permits signing with P5.4 open; C6 is the hard stop). P5.5 is CLOSED, so C1 is NOT gated.

P5.1 FLOOR: accepted at the standing ratio round(0.6 x recommended_periods), no override. For ch 7 round(0.6 x 12) = 7, matching floor_periods_at_standard on the row. Equal dispersion over [7, 12]: A-C = 5 >= 4, so counts are [12, 10, 7] - three canonicals, three authoring runs.

P5.2 REGISTRY: obvious, needs no definition. The summary carries an explicit sections[] spine of {ref, title, section_goal} and the period's textbook_segments[].ref reproduces the ref verbatim. Ch 7's registry is the five refs in summary order: section 7.1 Equilateral Triangles / 7.2 Constructing a Triangle When its Sides are Given / 7.3 Construction of Triangles When Some Sides and Angles are Given / 7.4 Constructions Related to Altitudes of Triangles / 7.5 Types of Triangles. THE TOKEN CARRIES THE WORD - 'section 7.1', not '7.1' - and the mediated anchor returns it VERBATIM rather than normalising, so anchor and registry are the same string by construction. (The LP schema's illustrative '§5.3' examples are a cosmetic residue; the model copies from the summary, not the example, and norm_code collapses all three forms.)

P5.3 PILOT CHAPTER: mathematics / VII / ch 7 'A Tale of Three Intersecting Lines'. All 15 chapters of the class are eligible (summary + mapping on disk, none placeholder), so this was a shape choice. Mid-book, five clean numbered sections, recommended_periods 12, floor 7, counts [12, 10, 7], core_cg CG-3, effort_index 8.0, canonical_plan present with basis 'arithmetic' and provisional true (expected until the standard is authored). Chosen over ch 5 (9 sections, 15 periods - richer but the priciest in the class) and ch 12 (4 sections). TWO SHAPE NOTES for the C-cycle: (a) 12 units over 5 sections is the S4 consolidation condition - there is no legal anchor token for a unit that consolidates rather than teaches, so expect the certifier's advisory and do NOT repair it by extending period_numbers (S4 §3.3 measured that fix: costs a question, buys nothing); (b) the chapter has ZERO worked examples (1 activity, 30 exercises), so Rule 11's anchor pool is comfortable but Rule 10's optional self-study pointer - 'book_ref of a worked example NOT walked through in class' - is unsatisfiable here. It is optional; a fabricated WE-n would be an internal-ID leak. C3 watch item.

P5.4 TEST IDENTITY PROFILES for class VII: OPEN. Row stays amber until they exist. When set up: through the app's own first-run / profile flow (the setup doubles as the live check of that flow), disjoint sections across the three identities, and the longer duration on kumar3 - the identity §4 assigns the mixed-duration matrix to - alongside the 40-minute class standard.

P5.5 CARRIER - CLOSED 2026-08-10, delegated and never re-invented. Trace: rule 4 · period-field family · item section_ref ('section 7.1') -> period textbook_segments[].ref · NO handoff in the path · NO LO (structural link only; linked_lo is null at this stage and the 3b renderer omits the line by design) · container a LIST of {section_code, section_title, note, items[]} groups · app-side method _middle_assess (subjects/mathematics/subject.py:242, parity-tested, already serving the app) · genon_assessment ABSENT at start · was in _NOT_YET.

What landed: carriers.items_by_period_field (family 3, the one carriers.py's docstring named in 2026-08-05 and never wrote) delegating to link_resolver's parity-tested period_field_index + norm_code; the mathematics plugin's genon_assessment middle branch, told apart by CONTAINER SHAPE not stage_for(grade) and separated from preparatory the prototype's way (middle items carry 'goal' and no 'intent'); the period anchor MEDIATED through a declared genon_unit_anchor plugin hook returning the ' / '-joined textbook_segments[].ref verbatim; the goal-cluster coverage_handoff round trip as a second carrier marker beside science's; and ('mathematics','middle') removed from _NOT_YET (preparatory stays, owed by S8). tests/test_genon_carriers.py 36 -> 80, all green. carrier_gap('mathematics','vii') is now None."""),

    "SIGN": ("pass", "Claude", """SIGNED PROVISIONALLY 2026-08-10 - constitutional gate CLEAR, C1 NOT gated, P5.4 the only amber. Status to be confirmed by Kumar.

Unlike S4 (carrier) and S6 (engine), S7 carries NO gate into its C-cycle: the carrier is landed and tested, and the four items found at P-prep are all fixed. Per-item note: genon/out/stage_prep_mathematics_middle/STAGE_SIGNOFF_S7_mathematics_middle.md.

Verified: A1 lands; the register is ONE block in the v1.10 THREE-ban form (this stage is not S6's exception); A6 anchors are present as the derived period-field form; A9 landed as the two lines alone (removal N-A) with no arrangement sentence; P3 converted (Group B, real); no cancelled amendment (A2/A3/A4) or V-rule has crept into a constitution.

THE STAGE'S ONE IDEA, worth carrying to S8-S11: it looked like it needed three new fields and needed none. Founder ruling 2026-08-10 - maths middle already carries every fact the serve engine wants, under other names (period textbook_segments[].ref = the anchor; handoff entry section_ref = the item's route), and the PROTOTYPE resolved exactly this shape variance at the READ boundary rather than by amendment (lp_pdf_generator.py:2583-2592 for the anchor and the bands; assessment_pdf_generator.py:117-192 for the item regroup, stating in terms that 'the constitution / generated JSON is NOT changed - this runs at render time'). The SaaS keeps that answer and moves it to the sanctioned seam (carriers.py + the plugin, CLAUDE.md §3) instead of scattering it across renderers. So the anchor and the handoff were P5.5 work, not P1 work. The ONE exception was P3, because compile.py rebuilds the spine from time_bands and asserts an inventory invariant over activity - a tolerant read could not carry that. English (S9-S11) is the same period-field family and should be read this way first.

FOUR THINGS FOUND AT P-PREP, all fixed, none constitutional:
1. raw_item_list returned the GROUPS, not the items, for the group-nested container - the ARV-D-060 class, third recurrence, third container shape. STEP 6 and generate_canonical.validate would both have silently no-opped on a paid canonical. Fixed shape-based; item_container / from_engine_items now round-trip the A/B/C groups, emitting an empty group rather than dropping it.
2. The goal-cluster handoff fell through to_engine_handoff unfiltered, so a served plan would have carried handoff rows for units it does not contain. Fixed with a second carrier marker; NO field added - each entry's period set is derived from its own section_ref, and it survives iff a period teaching its section is served (science's semantics).
3. The synthesis mandate named section_anchor, a field this stage does not have - S7's analogue of S4's synthesis-handoff defect, and it would have been PAID (metered STEP 1). Fixed in the BRIEF, never a constitution: the boolean form ('synthesis': true) that _arc_brief already asks science-middle for is now used by any stage whose anchor is MEDIATED, declared as genon_anchor_field_present rather than sniffed. Chasing it turned up TWO LIVE ENGINE BUGS the token had been hiding - serve.section_registry filtered the synthesis unit by anchor TEXT and serve.unit_range was rangeless only incidentally, so a boolean-carried synthesis could have entered the registry and been picked as somebody's Xth unit; both now short-circuit on is_synthesis_unit. Plus carriers.unit_anchor raised KeyError on a mediated synthesis unit and now returns None (not the token - manufacturing an anchor string would write into a field this constitution does not define). The ten token stages are unchanged BY PROOF: 50 standard briefs and 5 compact brief sets snapshotted before the edit, only the six mediated mathematics combos differ.
4. build_library.py mathematics vii 7 --certify-only does not reach the certify branch - STEP 2's annotate runs even under --certify-only and exits 'Row is provisional'. Correct downstream gate, same place S4 stopped, but the free smoke test is unavailable on an un-annotated row. Knowing it stops this reading as a failure.

TEST STATE: test_genon_carriers 36 -> 80 green. test_maths_port, test_genon_serve, test_genon_plan_key, test_genon_duration_order, test_genon_plan_granularity, test_borrowed_anchor, test_genon_approach_survives_serve, test_unit_order, test_unitize all green. Five suites fail pre-existing and unrelated - the same five the S4 sign-off recorded (test_api needs fastapi; test_link_resolver + test_normalized_item want a missing English saved plan; test_lp_standard a missing TWAU view; test_stimulus a fixture count 16 < 20).

TWO HOUSEKEEPING ITEMS FOR KUMAR, both outside the sandbox's reach:
(a) rm .git/index.lock - a stale zero-byte lock from a subagent's attempted git stash; no stash was created and nothing was lost (git stash list is empty), but any git add/commit from the Mac side needs it removed first.
(b) EIGHT S4 SERVED-PLAN FILES were deleted mid-session by a subagent's purge_derived cleanup and have been RESTORED from HEAD (data/content/saved_plans/mathematics/ix/ch_04_*_e17_*.json, *_e18_*.json, ch_99_canonical.json). These are C10.3 no-overwrite evidence for a stage in mid-cycle, so the loss would have been real. git status now shows zero deletions; verify before committing.

§9: nothing re-opens. No stage carries a signed human GATE, and the engine changes (serve.section_registry, serve.unit_range, carriers.unit_anchor, the brief carrier) are the cheap corpus-wide kind - re-run --certify-only across every certified chapter and diff the reports before S7's C1."""),
}

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_s7"))

row = state.setdefault("stages", {}).setdefault(KEY, {})
for step, (status, by, comment) in ROWS.items():
    row[step] = {"status": status, "by": by, "at": NOW, "comment": comment}
state["updated_at"] = NOW

STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{KEY}: wrote {', '.join(ROWS)}  (backup: {STATE.name}.bak_pre_s7)")
for step in ROWS:
    print(f"  {step:5} {state['stages'][KEY][step]['status']}")
