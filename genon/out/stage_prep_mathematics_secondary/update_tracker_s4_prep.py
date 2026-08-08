#!/usr/bin/env python3
"""Write S4 (mathematics · secondary) P1-P5 + SIGN into the campaign tracker state.

Run from the repo root:
    python3 genon/out/stage_prep_mathematics_secondary/update_tracker_s4_prep.py
Restart the API afterwards, or just reload docs/testing_tracker.html.
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "mathematics/secondary"

ROWS = {
    "P1": ("pass", "Claude", """AMENDED 2026-08-08. LP constitution v1.0 -> v1.1.

A1: INPUTS 4 was 'one or more rows of {duration_minutes, count}'; now 'exactly ONE row {duration_minutes, count}: the class-standard duration (40 min for classes up to VII, 45 for VIII, 50 for IX) x the period count ... handled downstream at serve time'. The TIME integrity constraint is restated as duration x count (was 'sum of (duration x count) per schedule row; total period count = sum of row counts'); the A3 schema comment names the standard duration and a NEW field constraint states the one-row rule where the schema is actually read. Bands are the master-plan calibration, not NCF's flat 40. Declared deviation from the verbatim port: the reference says 'partition time', this file says SERVE time (the partition engine was retired 2026-07-31) - the same correction S3 made.

A5+A7 THE SELF-CONTAINED REGISTER: PRESENT as ONE block after VOCABULARY in the v1.10 three-ban re-cut (clock quantity / forward reference or completion / calendar time, plus the closing backward-continuity line). Bound at Rule 9 (prohibition 6 - teacher-facing text and band activity) and Rule 10 (teacher notes) BY REFERENCE, never as scattered bans; the edit script asserts the phrase appears exactly 3 times (heading + two binds). Declared deviation: the reference's illustrative strings are Social Sciences content, substituted with mathematics ones ('a quick individual calculation', 'an extended derivation', 'having covered all three identities', 'Having established the expansion of a binomial product, ...'). The three bans and the closing rule are verbatim in substance.

Consequential edits, both following the reference: VOCABULARY dropped its positional cross-reference examples ('the previous unit', 'this unit') and gained the 'session' exclusion; Rule 10's continuity bullet ('a brief recap of what the previous unit covered and how it connects to this one') is now position-free, naming the content built on.

Also added here, as A6's LP-side half: an ITEM ANCHORING IS DERIVED, NOT DECLARED integrity line - the platform resolves an item's anchor unit from section_number through the handoff's period_numbers; MUST NOT emit period_ref or any unit number.

One more consequential edit, added 2026-08-08 after verification: A3's teacher_notes schema comment read 'recap-and-connect', the exact positional framing Rule 10's bullet was rewritten away from. Now 'continuity by content not position' - matching science secondary's practice of pointing at the rule rather than restating it.

TWO RESIDUES DISCLOSED, deliberately NOT fixed (science secondary v1.1 and science middle v2.2 carry the same ones; patching maths alone would put four signed stages out of step for no gain): (a) A4's period_duration_minutes comment still says 'if mixed across this section's periods, the most common' - inert under one standard row; (b) INPUTS 4 names the bands '40 <=VII, 45 VIII, 50 IX' verbatim from the reference in a constitution whose grades are ix and x, where testing.md P1 writes '50 IX-X'. Inert (step 0.6: class X has no content anywhere); align in the REFERENCE and port if the founder wants it changed.

No pedagogical rule changed: Rules 1-8, 11, 12, Amendment A4 and every period field byte-identical. Artefacts in genon/out/stage_prep_mathematics_secondary/ (lesson_plan_constitution_v1.0_pre.txt, lp_v1.0_to_v1.1.diff, apply_s4_amendments.py - every edit asserts exactly-one occurrence; re-running the script from the PRE files reproduces both live constitutions byte-for-byte, and re-running it against the amended files aborts loudly)."""),

    "P2": ("pass", "Claude", """AMENDED 2026-08-08. Assessment constitution v1.0 -> v1.1.

A6-confirm: PRESENT via the subject's equivalent, not amended. Every item already carries section_number matching the handoff, and the LP's coverage_handoff (A4) maps it to period_numbers. Mathematics secondary's unique link is the SECTION, not the unit - LP Rule 7 lets a section span several periods - so the reference's period_ref FIELD is not ported. Added an integrity line recording that ANCHORING is derived (section_number IS the anchor; the platform resolves it through period_numbers) and forbidding period_ref or any unit number on an item. Identical shape to science secondary v1.2 (founder ruling 2026-08-05: derive the link, never demand it). grep -c phase_ref = 0; period_ref appears exactly once, inside the new ban. The carrier family is already NAMED for this join (carriers.py docstring, handoff-bridged) but is NOT YET IMPLEMENTED - see SIGN.

A9 - TWO ADDITIONS; THE REMOVAL IS N/A. This file never carried the MEMORY-item-18 position prohibition: testing.md P2 names four files that carry it (SS + Science, middle and secondary) and mathematics secondary is not one. Confirmed by grep - 'is_correct MUST', 'consecutive items', 'same label' all 0. Nothing was struck.

ADDED, in the v1.7 wording: the Rule 7 mandate line (option order carries no meaning and is not yours to set, emit as authored, uneven letters across a chapter are coincidence not a defect) and the by-label option-reference prohibition. The pre-existing 'none of the above' / 'all of the above' ban is ABSORBED INTO that prohibition rather than duplicated - same ban, now carrying the reason a downstream sort cannot reorder it - and Rule 7's PROHIBITION is renumbered 1/2 to hold both. No scope lost.

NOT re-added and asserted absent by the edit script: 'alphabetically', 'never led with', 'first word at which they differ'. Note that Rule 1's prohibition 3, Rule 4's and Rule 5's 'never position' clauses and the 'Position carries no signal' integrity line all concern a SECTION's position in the chapter - a different subject entirely - and were left untouched.

No pedagogical rule changed: Rules 1-6, 8-12, the guide layer and the whole A1 schema (including VS-1..VS-6 and graph_paper) are byte-identical. Artefacts: assessment_constitution_v1.0_pre.txt, assess_v1.0_to_v1.1.diff."""),

    "P3": ("na", "Claude", """N/A 2026-08-08 - mathematics secondary is GROUP A, matching the testing.md section 3 stage table's 'time_bands' entry for S4.

Amendment A3's period schema already emits time_bands[{minutes, activity}] with the tiling constraint ('tile the period exactly from 0 to period_duration_minutes, no gaps or overlaps; minimum 3 bands per period'). Verified by grep on both constitutions: 'phases[' = 0, '\"phases\"' = 0, band_id = 0, time_bands present. The edit script re-asserts all four as closing guards, so a future edit cannot silently reintroduce the retired shape.

Nothing to convert; no band_id to remove (the band layer left the declaration surface at compile v0.5 and ids are derived internally)."""),

    "P4": ("pass", "Claude", """DONE 2026-08-08. CHANGELOG.md created beside BOTH amended constitutions:
- data/content/constitutions/lesson_plan/mathematics/secondary/CHANGELOG.md (v1.1 entry + a v1.0 'pre' stub)
- data/content/constitutions/assessment/mathematics/secondary/CHANGELOG.md (v1.1 entry + a v1.0 'pre' stub)

Each lists the bump with date and per-amendment rationale, including the declared deviations (serve time for partition time; mathematics illustrative strings in the register block; the derived section_number anchor in place of the reference's period_ref field; A9's removal recorded as N/A with the grep evidence; the absorbed none/all-of-the-above ban). Neither constitution carried an in-document version-history block, so nothing had to be lifted out; the VERSION line stays in the file and nothing in the sidecars is read at generation time.

The assessment sidecar also carries forward the file's standing RENDERER WIRING debt (VS-2 figure SVG and VS-6 green graph paper are permitted by this stage but honoured by neither renderer) as a note - flagged for the C-cycle as a defect if a pilot item needs a grid, explicitly NOT as a constitutional item."""),

    # NOTE the status is "blocked", not "amber". testing.md section 3 uses the WORD amber for a
    # provisional P5, but the tracker's STATUSES are ["pass","fail","na","blocked","pending"]
    # (docs/testing_tracker.html:256) and there is no .s-amber CSS rule - an "amber" cell renders
    # unstyled with no button selected. "blocked" is the precedent: social_sciences/secondary's
    # P5 is stored blocked for exactly this reason. Read "blocked" as "provisional, P5.4 open".
    "P5": ("blocked", "Claude", """RECORDED 2026-08-08 - PROVISIONAL / AMBER in testing.md's sense (stored as 'blocked' because the tracker has no amber status). P5.4 OPEN; founder ruling 2026-08-02 permits signing with P5.4 open; C6 is the hard stop.

P5.1 FLOOR: accepted at the standing ratio round(0.6 x recommended_periods), no override. For ch 4, round(0.6 x 14) = round(8.4) = 8, matching floor_periods_at_standard on the row. Equal dispersion over [8, 14]: A-C = 6 >= 4, so counts are {A, ceil((A+C)/2), C} = [14, 11, 8] - three canonicals, three authoring runs.

P5.2 REGISTRY: mathematics secondary's section model is OBVIOUS and needs no definition. The summary carries an explicit sections[] spine of {ref, title} and LP A3 already specifies section_anchor as the bare ref ('e.g. 2.5'). For ch 4 the registry is the eight refs in summary order: 4.1 Introduction, 4.2 Visualising Identities, 4.3 Factorisation of Algebraic Expressions Using Identities, 4.4 More Identities, 4.5 Factorisation Using Algebra Tiles, 4.6 Factorisation Without Using Algebra Tiles, 4.7 Finding New Identities, 4.8 Simplifying Rational Expressions. Library-wide consistency is guaranteed by construction, not by hope: standard_registry() reads the registry off the AUTHORED standard and briefs_for() prints it verbatim into every compact's brief. Nothing about the registry enters a constitution.

ONE OPEN ITEM RIDES ON P5.2 - the synthesis unit has no home in a DERIVED-anchor handoff. v2.0 mandates the standard's closing synthesis unit with section_anchor = the reserved token, excluded from the registry. Where items anchor by period_ref that is harmless; where the anchor is derived (science secondary, science middle via progression_stage, now mathematics secondary) the item's only route to a unit is its group number -> coverage_handoff -> period_numbers, so a synthesis unit with no handoff entry can carry NO items, and C9.2 ('a borrowed unit brings its own items') becomes unsatisfiable on exactly the Case-1 synthesis borrow that C8 exists to inspect.

The installed science IX ch 8 library shows the model inventing an 11th entry with section_label 'synthesis', period_numbers [12] and total_sections 11. Nothing asked for it - and VERIFIED 2026-08-08, it does not rescue anything either: NO ITEM USES IT. Ch 8's item section_numbers run 1-10 and assessment_items() stamps unit_ref 1,2,4,5,6,7,8,9,10,11, never 12. So C9.2 is ALREADY UNSATISFIABLE ON THE CERTIFIED REFERENCE LIBRARY, not merely at risk on mathematics - worth raising as a defect (section 7) against S3, not only as an S4 pre-C1 item. The compacts p07/p10 correctly carry no synthesis unit and no such entry.

Maths A4 is stricter still: section_ref and section_title are specified as copied VERBATIM from the summary, and there is no summary section to copy, so the model will either omit the entry or contradict A4. top_brief_for mandates the unit and says nothing about its handoff row. One brief line closes it for every derived-anchor stage. This is a V-series / BRIEF matter and MUST NOT go into a constitution (a brief change triggers only a --certify-only re-run, never the section 9 cascade). Founder call on the values; settle it before ch 4 is authored against a guess.

P5.3 PILOT CHAPTER: mathematics / IX / ch 4 'Exploring Algebraic Identities' - founder pick 2026-08-08 from the eight eligible chapters (9-16 are placeholder: true, awaiting NCERT release). Summary + mapping both on disk, placeholder false, canonical_plan present (counts [14, 11, 8], basis arithmetic, provisional true until the standard is authored - expected at this point in the cycle). Eight clean numbered sections, mid-book of the covered half, 18 worked examples and 21 exercises for Rule 9's book_ref discipline to bite on. core_cg CG-3, co_central FALSE (so Rule 5's OPEN_TASK arrives via Rule 6's lift, not the co-central path), effort_index 11.0. Shape is close to the certified SS IX ch 3 pilot, so the roughly Rs 110-150 library benchmark should hold; 3 runs at about Rs 37 is the budget line, and C2 records clean-path and all-in separately.

P5.5 THE CARRIER TRACE - the P-step this stage caused to exist (testing.md v2.8 section 3). Genon does not invent linkage; the verified 8-rule table (docs/architecture-plan.md, restated in link_resolver.py) does, and carriers.py is that table exposed to genon. Mathematics secondary's row: RULE 6, handoff-bridged, item section_number -> handoff section_number -> period_numbers (NEVER section_anchor text), LO from handoff implied_lo (item: implied_lo_assessed), container {..., questions: []} dict, app-side method _secondary_assess (subjects/mathematics/subject.py:263, parity-tested, already serving the app), genon_assessment ABSENT, still in _NOT_YET. The rule is settled and implemented; only genon's door is unopened. OPEN, and it is the stage's C1 gate (see SIGN). S4's row is identical to S3's rule 2 in everything but the subject name, which is why the fix is a copy rather than a design.

P5.4 TEST IDENTITY PROFILES for class IX: OPEN. Needs the app's own first-run / profile flow, which the Cowork sandbox cannot run. When set up: disjoint sections across kumar1/kumar2/kumar3 so X1's tenancy evidence is unambiguous, and one identity at a duration LONGER than the 50-min class standard (60 works) so C6's mixed-duration matrix - kumar3's row - has real material. Leftovers from S1-S3 and S6 are accepted (founder ruling 2026-08-07): they touch no mathematics-IX key. Row stays amber until the three profiles exist."""),

    "SIGN": ("blocked", "Claude", """CONSTITUTIONAL GATE CLEAR - but the C-cycle is BLOCKED on the mathematics genon CARRIER. Status to be set by Kumar.

The constitutional side is done and verified: A1 lands, the register is ONE block in the full v1.10 three-ban form, A6 anchors are present as the derived section_number form on both sides, A9 landed as the v1.7 two lines with the removal recorded N/A and no arrangement sentence anywhere, P3 is N/A with grep evidence (Group A), and no cancelled amendment (A2/A3/A4) or V-rule has crept into a constitution. No pedagogical rule changed in either file. Full per-item note: genon/out/stage_prep_mathematics_secondary/STAGE_SIGNOFF_S4_mathematics_secondary.md.

WHY BLOCKED. aruvi_core/genon/carriers.py carries an explicit _NOT_YET entry for mathematics ('period-field join (middle/prep) + handoff-bridged (secondary) - owed by S4/S7/S8') and assessment_items() RAISES CarrierNotImplemented on it (carriers.py:469 the test, :470 the raise). Only science implements genon_assessment; social_sciences and TWAU ride the item-self-sufficient default. The S4 analogue of S6's engine gate.

SCOPE, corrected 2026-08-08 after founder challenge - this is NOT 'Aruvi cannot resolve maths assessment links'. It can, and always has: the APP renders maths secondary LPs and assessments correctly through subjects/mathematics/subject.py::_secondary_assess (line 263), which already runs the handoff-bridged join (handoff_period_index(handoff,'section_number') -> period_numbers, platform stamp first) and is parity-tested; link_resolver.py's docstring names Maths-secondary in that family. The gap is ONE METHOD ON ONE ENTRY POINT: the app reaches the plugin via assessment_to_view, which returns DISPLAY objects, while genon needs the RAW item dicts (options, is_correct, guide, visual_stimulus intact, for served files and exports) and so asks for genon_assessment instead - which only science has written. carriers.py's own docstring records it: 'The app never had this bug, because the app goes through the subject plugin ... Genon skipped that layer.' Sizing: the secondary half is about 6 lines of delegation, because items_by_handoff exists and maths secondary needs the IDENTICAL arguments science secondary passes (both wrap items under 'questions', both join section_number -> section_number, and items_by_handoff already anchors at the group's LAST unit per the 2026-08-05 ruling). What makes this serious is not its size - it is that the failure is PAID FOR and MISREPORTED.

AND THE GATE IS POST-PAYMENT, NOT PRE-FLIGHT (corrected 2026-08-08 after verification; an earlier draft of this note said the run 'dies at compile before it spends a rupee', which is false and was the reason the gate looked cheap). certify() is called at build_library.py:514, AFTER metered STEP 1 (:482-484) and metered STEP 4 (:497-501) - the full ~Rs 110-150 is spent first. Worse, STEP 1 does not even fail: generate_canonical.py:154-159 calls the carrier inside a bare 'except Exception' and falls back to parsed.get('assessment_items'), a key maths secondary does not have (its items sit under a 'questions' wrapper, per A1), so the isinstance filter yields [] and the item-anchor validator becomes a SILENT NO-OP. A paid canonical installs looking clean with every item anchored to nothing. The raise finally surfaces at build_library.py:196-199 inside load_library's except, which files it as 'FAIL <file>: does not compile' for EVERY library file; lib is then empty and certify exits at :218-219 with 'STOP: no library on disk to certify' - so quarantine never runs and the message names neither the carrier nor mathematics. Do NOT rely on the build to stop this run.

WHAT S4 NEEDS BEFORE C1 (three items, none constitutional):
1. genon_assessment on the mathematics plugin - for SECONDARY a ~6-line DELEGATION, not new logic: items_by_handoff(result, items=raw['questions'], join_key='section_number', handoff_key='section_number'), which is byte-for-byte the call science secondary makes. The anchoring rule (group's LAST unit) is inherited from items_by_handoff, not re-implemented. The one care point: the middle/preparatory branch must NOT fall through to this join - it is a different family (period-field), owed by S7/S8, and should raise rather than guess.
2. STOP generate_canonical.validate SWALLOWING CarrierNotImplemented INTO A PASS. A subject with no carrier must refuse to generate, not generate unvalidated. This is the same failure mode S3's questions-wrapper bug created the carrier seam to prevent, recurring one layer up - and it is what turns a missing carrier from a free abort into a paid one.
3. Deleting _NOT_YET['mathematics'] OPENS MIDDLE AND PREPARATORY TOO, and those are a different family (period-field join, owed by S7/S8). Founder's call: implement both halves now branching on stage_for(grade), or make _NOT_YET stage-aware so S4 opens without silently unlocking S7/S8. Recommend the latter - smaller change, keeps the campaign's stage-at-a-time discipline.

NOT a gating item (downgraded 2026-08-08): declaring genon_serve_granularity / genon_has_section_axis on the mathematics plugin is cosmetic. Checked live - serve_granularity('mathematics','ix') returns 'unit' and has_section_axis(...) returns True, via carriers._ask's DOCUMENTED DEFAULT, not a swallowed exception. An earlier draft called that 'luck, not design'; it was wrong. Worth declaring for legibility, does not gate C1.

Settle P5.2's synthesis-handoff brief item in the same pass (see P5), before C1 spends anything - and note it is a live defect against the CERTIFIED science secondary library, not only an S4 risk: ch 8's invented synthesis handoff entry has ZERO items anchoring to it (item section_numbers run 1-10; stamped unit_refs never reach 12), so C9.2 is already unsatisfiable there.

Nothing re-opens: no stage carries a signed human GATE, so testing.md section 9 costs nothing here. The template DID need a version note after all - bumped 2.7 -> 2.8 at this P-prep, promoting the carrier precondition and the synthesis-handoff item into section 3. S4 itself is an ordinary section-axis stage and every C-step reads as written."""),
}

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_s4"))

row = state.setdefault("stages", {}).setdefault(KEY, {})
for step, (status, by, comment) in ROWS.items():
    row[step] = {"status": status, "by": by, "at": NOW, "comment": comment}
state["updated_at"] = NOW

STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{KEY}: wrote {', '.join(ROWS)}  (backup: {STATE.name}.bak_pre_s4)")
for step in ROWS:
    print(f"  {step:5} {state['stages'][KEY][step]['status']}")
