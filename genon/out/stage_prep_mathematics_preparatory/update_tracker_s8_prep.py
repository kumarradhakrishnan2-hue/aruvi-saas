#!/usr/bin/env python3
"""Write S8 (mathematics · preparatory) P1-P5 + SIGN into the campaign tracker state.

Run from the repo root:
    python3 genon/out/stage_prep_mathematics_preparatory/update_tracker_s8_prep.py
Then reload docs/testing_tracker.html.
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "mathematics/preparatory"

ROWS = {
    "P1": ("pass", "Claude", """AMENDED 2026-08-11. LP constitution v1.1 -> v1.2. Ported from the SS-secondary v1.10 reference via the mathematics-middle v3.4 adaptation - same subject vocabulary, one stage up, and the same 8-rule family (period-field), so the port is close to mechanical.

A1: INPUTS 4 was 'Period schedule: {duration, count} rows; total = B.' - one line, licensing exactly the mixed-duration plan the variant engine cannot use. Now 'exactly ONE row {duration_minutes, count}: the class-standard duration (40 min for classes up to VII, 45 for VIII, 50 for IX-X - the master-plan calibration bands, not NCF's flat 40) x the period count; total = B. Teacher timetable variation never reaches generation; it is handled downstream at serve time.' Class III's standard is 40 min, matching the master_plan row. Declared deviation: 'serve time', not the reference's 'partition time' (the partition engine was retired 2026-07-31) - the same correction S3, S4, S6 and S7 made.

A5+A7 THE SELF-CONTAINED REGISTER: present as ONE block after VOCABULARY, in the v1.10 THREE-ban re-cut (this stage is NOT S6's two-ban exception - its units anchor to textbook sections and travel between plans, so ban 2 binds in full). Bound at Rule 6 (band narration) and at the teacher_notes schema comment by reference, never as scattered prohibitions. Declared deviation: illustrative strings are prep-maths ones ('a quick count round the class', 'an unhurried making activity', 'now that we have weighed everything', 'The children have grouped in tens to count large collections'). TWO consequential edits, both the same two S7 made: VOCABULARY was TEACHING the forward reference ban 2 forbids (its cross-reference examples were literally 'the previous unit', 'this unit') so the examples are dropped and 'session' joins the excluded register; and the teacher_notes schema comment asked for positional continuity ('Recap prior unit') and now asks for content-named continuity, citing ban 2.

Footer version corrected (it read 1.1 and now tracks the header). No pedagogical rule changed: Rules 1-4 and 7-9 are untouched in force.

NOT DONE, deliberately (founder ruling 2026-08-10, carried from S7): no field invented to feed the serve engine. section_anchor is NOT added to the period; the unit anchor is already in the authored file as section_refs[] and the plugin mediates the read. That is P5.5's work. Guards assert the absence.

Artefacts in genon/out/stage_prep_mathematics_preparatory/: lesson_plan_constitution_v1.1_pre.txt, lp_v1.1_to_v1.2.diff, apply_s8_amendments.py (every edit asserts exactly-one occurrence; the run closes on guards for the struck A9 strings, the retired phases shape, band_id, phase_ref, section_anchor, period_ref, the cancelled amendments' vocabulary and the V-rules)."""),

    "P2": ("pass", "Claude", """AMENDED 2026-08-11. Assessment constitution v1.2 -> v1.3. Paired with LP v1.2.

A6-confirm: PRESENT via the subject's equivalent, not amended. Items already carry section_ref, copied verbatim from the LP handoff entry (LP Rule 8 emits it, assessment Rule 2 consumes it). Added an ANCHORING (PLATFORM INTEGRITY) block - the file had none - recording that preparatory mathematics is 8-rule ROW 5, the PERIOD-FIELD family: the platform resolves section_ref ('S3') against each period's own section_refs[], NOT middle's textbook_segments[].ref (row 4) and NOT secondary's handoff (row 6), with no coverage_handoff in the path and no LO. The block states four things: section_ref IS the anchor and is pass-through; a section spanning several units anchors at the LAST of them (founder 2026-08-05); period_ref / period_number / any unit number MUST NOT be emitted, because declaring the link would freeze an arrangement the platform varies per teacher; and task_id is not an anchor in this sense (Rule 8) - it seeds the exercise companion only. Same shape as science-secondary v1.2, science-middle v1.4 and maths-middle v3.3: derive the link, never demand it. grep -c phase_ref = 0.

A9 - TWO ADDITIONS, no removal, no arrangement rule. The REMOVAL half is N/A: this file never carried the MEMORY item-18 position prohibition (testing.md P2 names four files that do - SS + Science, middle and secondary - and this is not one). Confirmed by grep: consecutive, same label, vary in position all 0; nothing was struck. ADDED in Rule 9's MCQ block, v1.7 wording: the option-order mandate (order carries no meaning and is not yours to set, emit as authored, uneven letters are coincidence not a defect) and the by-label option-reference prohibition ('both A and B', 'none of the above', 'all of the above'). This file carried no prior 'none of the above' ban, so the addition is purely additive. NOT re-added and asserted absent: alphabetically, never led with, first word at which they differ.

ONE REPAIR rode along, recorded as a repair rather than an amendment: the schema's what_each_option_reveals example read { 'A', 'C', 'C', 'D' } - four keys, 'C' twice, 'B' missing - and contradicted its own prose. S7's apply_s7_distractors_only.py (2026-08-10) rewrote the FIRST line of the two-line example in this file and left the second; prep was collateral to a middle amendment and nobody read the result. It now shows three keys and says why.

Footer was TWO bumps stale ('Version 1.1' after the v1.2 distractors pass) and is corrected to 1.3. No pedagogical rule changed: Rules 1-9 keep their force.

Artefacts: assessment_constitution_v1.2_pre.txt, assess_v1.2_to_v1.3.diff."""),

    "P3": ("pass", "Claude", """APPLIED 2026-08-11 - mathematics preparatory is GROUP B and the conversion was REAL (the third such stage, after S6 and S7).

phases[{minutes, description}] -> time_bands[{minutes, activity}]: both the array name and the description key renamed, with Rule 5 (the time constraint), Rule 6's heading (PHASE NARRATION -> BAND NARRATION) and prose, Rule 7 and the schema following. NO band_id in the target shape - the band layer left the declaration surface at compile v0.5.

Why it could not be absorbed by a tolerant read the way the anchor was: compile.py rebuilds the timed spine from p['time_bands'] (:124) and asserts an inventory invariant over tb['activity'] (:208-210).

Guards: grep -c 'phases[' = 0, '\"phases\"' = 0, band_id = 0, time_bands = 2, '\"activity\": string' present.

Note this leaves the existing preparatory saved-plan corpus on the old phases shape; the plugin's tolerant read still covers display (subject.py:211-219 reads BOTH keys, newest first, and says why)."""),

    "P4": ("pass", "Claude", """DONE 2026-08-11. CHANGELOG.md created beside BOTH constitutions (neither had one):
- data/content/constitutions/lesson_plan/mathematics/preparatory/CHANGELOG.md (v1.2 entry + a v1.1 'pre' stub)
- data/content/constitutions/assessment/mathematics/preparatory/CHANGELOG.md (v1.3 entry, a back-filled v1.2 entry for the S7 collateral distractors bump which had no record anywhere, + a v1.1 'pre' stub)

Each lists the bump with date and per-amendment rationale, including the declared deviations and the standing number_line renderer debt. Neither constitution carried an in-document version-history block, so nothing had to be lifted out; the VERSION line stays in the file. BOTH footers were stale and are corrected - the assessment one by two bumps."""),

    "P5": ("amber", "Claude", """RECORDED 2026-08-11 - PROVISIONAL, P5.4 OPEN (founder ruling 2026-08-02 permits signing with P5.4 open; C6 is the hard stop). P5.5 IS CLOSED, so C1 is NOT gated.

P5.1 FLOOR: accepted at the standing ratio round(0.6 x recommended_periods), no override. For ch 5, round(0.6 x 14) = round(8.4) = 8, matching floor_periods_at_standard. Equal dispersion over [8, 14]: A-C = 6 >= 4, so counts = {A, ceil((A+C)/2), C} = [14, 11, 8] - three canonicals, three authoring runs.

P5.2 REGISTRY: the section model is OBVIOUS and needs no definition. The summary carries an explicit sections[] spine of {ref, title, prose_summary, tasks[]} and the period's section_refs[] reproduces the ref verbatim (LP Rule 1: 'copied from summary sections[].ref'). Ch 5's registry is the eight refs in summary order: S1 Shapes in rangoli / S2 Shapes from boxes - cuboid faces / S3 Rectangles - properties and drawing / S4 Same to Same - squares vs rectangles / S5 Square corners - right angles / S6 Triangles - three sides, three corners / S7 Circus with circles - circle and centre / S8 Comparing and composing shapes. THE TOKEN IS THE BARE CODE 'S1', not 'section 5.1' - the one place preparatory differs from middle in kind rather than degree (middle's codes are chapter-prefixed). link_resolver.norm_code strips the word 'section' and collapses spacing, so 'S1' -> 's1' on both sides and there is no collision. Consistency across the library is by construction: standard_registry() reads the registry off the AUTHORED standard canonical and briefs_for() prints it verbatim into each compact's brief.

P5.3 PILOT CHAPTER: mathematics / III / ch 5 'Fun with Shapes'. Mid-book, 8 sections, summary + mapping both on disk, placeholder false, canonical_plan present. Row: {chapter 5, weight 13, exact_share 14.15, recommended_periods 14, canonical_minutes 560, floor_minutes 336.0, floor_periods_at_standard 8, canonical_periods [14,11,8], placeholder false, canonical_plan {counts [14,11,8], provisional true, basis 'arithmetic', registry_sections null, authored []}}. provisional/arithmetic is the expected pre-C1 state; it finalizes to authored_standard when variant_plans.py annotate runs inside C1. Chosen over ch 9 and ch 7 on section-to-period ratio: 8 sections against 14 periods gives the compacts real condensation room, where ch 7's 13 against 14 leaves almost none.

P5.4 TEST IDENTITY PROFILES for class III: OPEN. Row stays amber until they exist. Three identities, DIFFERENT sections, one duration longer than 40 alongside the class standard so C6's mixed-duration matrix has something real to draw on. Through the app's own first-run flow, never by hand-editing JSON.

P5.5 THE CARRIER - CLOSED 2026-08-11, and it is a DELEGATION. Trace: rule 5 . period-field family . item section_ref ('S3') -> period section_refs[] . container: a list of A/B/C/D INTENT groups each carrying items[] . plugin method MathematicsSubject._middle_assess (its prep branch, shipping for the app since before the campaign) . genon_assessment present as of 2026-08-11 . not in _NOT_YET. S7 had already written both halves of the seam this stage needed - items_by_period_field (the family helper) and genon_unit_anchor's preparatory branch - and left them deliberately unexercised with a note saying so, so the work was three lines of delegation plus a deletion. MATHEMATICS IS NOW CARRIED AT ALL THREE STAGES; the four remaining _NOT_YET entries are english's three stages (row 7, owed by S9-S11). The stage discriminator is the load-bearing part and now carries weight in both directions: genon_assessment receives only result and cannot read the grade (the S4 trap), middle and preparatory share a container, and they are separated the way the prototype separates them - middle items carry 'goal', preparatory items carry 'intent'. The no-goal-and-no-intent case still refuses rather than guessing, with a message naming both fields and both rows. VERIFIED ON THE REAL SAVED SHAPE, not an invented fixture: backup/saved_plans/mathematics/iii/ch_06_20260603_180712.json - 9 periods over S1-S11, 26 items in four intent groups; all 26 resolve, ZERO orphans, every unit_ref a singleton, and every anchor equal to the independently computed 'last period that lists this section' (S3 spans 2-3 -> anchors at 3; S8 spans 6-7 -> anchors at 7). Raw fields survive the seam. genon_unit_anchor's preparatory branch is exercised for the first time and returns 'S1' and 'S2 / S3' verbatim. tests/test_genon_carriers.py: 82 tests with 4 failures -> 92 tests, GREEN (the four failures were the S7-era assertions that preparatory is still owed, which is exactly what this step invalidates)."""),

    "SIGN": ("pass", "Claude", """P1-P5.5 COMPLETE - S8 IS CLEAR TO ENTER C1, with no gate carried into the C-cycle. Status to be set by Kumar. Full per-item note: genon/out/stage_prep_mathematics_preparatory/STAGE_SIGNOFF_S8_mathematics_preparatory.md.

Verified against the SS-secondary v1.10 / v1.7 reference and the rollout brief: A1 lands; the register is ONE block in the v1.10 THREE-ban form (not S6's two-ban exception); A6 anchors are present as the derived period-field form on section_refs[]; A9 landed as the two v1.7 lines with the removal N/A and NO arrangement sentence; P3 converted (Group B, real); P4 sidecars created for both files and both stale footers corrected; no cancelled amendment (A2/A3/A4) and no V-rule has crept into a constitution - all asserted by guard. P5.4 is the only open item and it is amber by design.

THE CHEAPEST STAGE PREP OF THE CAMPAIGN, and both reasons were paid for at S7: preparatory is mathematics' third stage and the second in the period-field family, so P1/P2 ported almost mechanically; and S7 wrote the two halves of the carrier seam this stage needed and left them unexercised with a note. The S7 note turned out to be exactly right about where the work would land.

THE ONE OPEN QUESTION IS FOR THE FOUNDER AND IS NOT AN AMENDMENT - Rule 2's two-adjacent-periods cap, measured before it is paid for. This is the same numeric limit that cost S7 a re-author at LP v3.6, and prep carries two of them (Rule 1's 'one or at most two adjacent sections' and Rule 2's 'a heavy section MAY split across two adjacent periods'). The cap binds when body units > 2 x sections. Measured across all 14 chapters of class III at the top canonical, it is UNSATISFIABLE ON 4 OF 14: ch 3 Double Century (13 body vs cap 10), ch 8 Fair Share (9 vs 8), ch 10 Fun at Class Party! (13 vs 12), ch 13 Time Goes On (13 vs 12). THE PILOT DODGES IT - ch 5 is 13 body against a cap of 16 - which is why nothing is forced today and why the stage signs clear. Claude's read, offered as a read and not a decision: the arithmetic is the same as middle's and the failure mode is documented (the model returns to a section the plan has left, producing a unit that teaches nothing new and dragging the assessment onto the revisit), but the pilot does not exercise it and prep's sections are structurally unlike middle's - small and task-dense - so amending now would be porting a rule change across a pedagogical boundary on arithmetic alone. RECOMMEND LEAVING IT, with the four binding chapters recorded so that the day one of them is authored, that table is read first. Section 4 of the sign-off carries the full table and both options.

Inherited by the C-cycle: (a) C1 unblocked - build_library.py's STEP 0 pre-flight passes; (b) P5.4 amber, C6 is the hard stop; (c) the number_line renderer debt is now owed TWICE (prep and middle both permit it, prep prohibits SVG) - confirm at C13 that both renderers still carry a number_line: detection branch; (d) the saved-plan corpus for this stage is still on the old phases shape - display is covered by the plugin's both-keys read, anything new must emit time_bands."""),
}

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_s8"))

row = state.setdefault("stages", {}).setdefault(KEY, {})
for step, (status, by, comment) in ROWS.items():
    row[step] = {"status": status, "by": by, "at": NOW, "comment": comment}

# The provenance panel lives on the COMBO row (scope "combos", step "provenance"), not on
# the stage row. Pre-fill only what the P-steps actually establish; C1/C2 fill the rest.
prov = (state.setdefault("combos", {}).setdefault(KEY, {})
             .setdefault("provenance", {}))
prov.update({
    "klass": "iii",
    "draw": "seed 'mathematics|preparatory|2026-08-02' over ['iii','iv','v'] -> iii",
    "chapter": "5 — Fun with Shapes",
    "duration": "40",
    "lp_ver": "1.2",
    "as_ver": "1.3",
    "canonical_plan": "counts [14, 11, 8] · provisional true · basis arithmetic · "
                      "registry_sections null · authored []  (finalizes at C1's annotate)",
})
state["updated_at"] = NOW

STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{KEY}: wrote {', '.join(ROWS)} + provenance  (backup: {STATE.name}.bak_pre_s8)")
