#!/usr/bin/env python3
"""Write S9 (english · preparatory) P1-P5 + SIGN into the campaign tracker state,
plus the two defect rows this prep raised.

Run from the repo root:
    python3 genon/out/stage_prep_english_preparatory/update_tracker_s9_prep.py
Then reload docs/testing_tracker.html (or GET /api/testing/tracker).

Full note: genon/out/stage_prep_english_preparatory/STAGE_SIGNOFF_S9_english_preparatory.md
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/preparatory"

ROWS = {
    "P1": ("pass", "Claude", """AMENDED 2026-08-13. LP constitution v1.1 -> v1.2. Drawn class III (standard duration 40 min). Reference: SS-secondary v1.10, read through english-secondary v1.2 and english-middle v1.7 - S9 is the THIRD and last stage of the period-field family's english branch, so the carry-forward ports from its two siblings rather than from the reference directly.

A1 IS THE FINDING OF THIS PREP, AND IT IS NOT THE USUAL ONE-ROW EDIT. Every other stage's A1 replaced 'one or more rows' with one row - a SHAPE correction. This file needed that too, but its real defect was the NUMBER. Three sites said 30/35: INPUTS 3 ('period_duration_minutes is 30 or 35 at prep (35 default)'), Rule 2 STEP 1's ceiling table ('A 30-min period holds at most 2-3 tasks; a 35-min period holds 2-4'), and the schema comment ('// 30 or 35'). master_plan.json carries english|III, english|IV AND english|V at standard_duration_minutes = 40 - the calibration band this campaign authors at and the band FirstRun.jsx already shows a teacher. So the constitution named a duration the platform does not use, and a library authored under it would have been at the wrong minute count throughout: 12 x 35 = 420 minutes against the row's canonical_minutes of 480.

IT WAS LIVE, NOT THEORETICAL. Three of the four saved preparatory plans carry MIXED durations inside a single plan - iii ch 2 = 2x40 + 2x35, iv ch 1 = 5x35 + 2x40, v ch 1 = 3x35 + 2x40 + 1x30. That is exactly the shape A1 exists to make impossible, and it is why A1 is doubly load-bearing under the variant engine. INPUTS 3 now reads 'exactly ONE row { period_duration_minutes, period_count }: the class-standard duration (40 min for classes up to VII, 45 for VIII, 50 for IX-X - the master-plan calibration bands, not NCF's flat 40) x the period count ... Preparatory is classes III-V, so every preparatory plan is authored at 40 MINUTES. There is no 30- or 35-minute preparatory period', STEP 1 states the 40-minute ceiling ALONE (2-3 tasks), and the schema follows. NAMING ONLY 40 IS DELIBERATE: preparatory spans one class-standard, unlike middle, so a table of alternatives would invite the author to branch on a number A1 has already fixed. Declared deviation: 'serve time', not the reference's 'partition time' - carried by S3, S4, S6, S7, S8, S11, S10. VERIFIED DOWNSTREAM: the dry pre-flight assembles at 12 x 40 min.

A5 + A7 THE SELF-CONTAINED REGISTER - present, one block after VOCABULARY, in the v1.10 three-ban re-cut (clock quantity . forward reference or completion . calendar time), binding Rule 9 and teacher_notes by reference and never as scattered prohibitions. NOT S6's two-ban exception: preparatory units anchor to cells and travel between plans under the Xth-unit choice set, so ban 2 binds in full. Declared deviation: the illustrative strings are prep-english and pilot-appropriate ('a quick paired chant', 'now that we have recited the whole poem', 'Having chanted the laddoo rhyme together, ...'). THE SAME TWO CONSEQUENTIAL REMOVALS EVERY ENGLISH STAGE HAS HAD TO MAKE: VOCABULARY was TEACHING the positional cross-reference - its worked examples were literally 'the previous unit' and 'this unit', which is a unit's position and precisely what ban 2 strikes - and the teacher_notes schema comment asked for 'transition from prior unit; PREVIEW INTO NEXT', the clause testing.md's P1 names by hand as the english family's known direct contradiction. grep -c 'the previous unit' = 0, grep -c 'preview into next' = 0.

FOUR MEASURED EDITS, taken here because P-prep is where they are free.
(1) FULL SPINE COVERAGE replaces Rule 2 STEP 3's drop licence. STEP 3 said 'when the section's allocated periods are exhausted, stop ... this is an honest reflection of available time, not a defect'. Under architecture v2.0 that licenses a chapter's compacts to be a DIFFERENT CHAPTER from its standard: a library shares ONE registry, briefs_for() prints the standard's registry verbatim into every compact's brief, and the Xth-unit choice set borrows the unit that FIRST deals the next-due cell - which a compact whose registry is a subset does not have. THE PREPARATORY CORPUS DOES IT: backup/saved_plans/english/iii/ch_01_*.json is a 3-unit plan whose handoff carries 3 of its summary's 5 cells - writing and beyond_text never arrive. Curation moves to TASK level, where Rule 3 already governs it; unfitted TASKS still go to homework or ride as flagged self-study pointers. Rule 10 gained the corollary: ABSENT FROM THE SUMMARY IS A STATE, DROPPED FOR TIME IS A DEFECT.
(2) Rule 1 gains the CLOSING-UNIT EXCEPTION. v2.0 mandates the standard canonical's whole-chapter synthesis unit; Rule 1's 'exactly ONE main_section and one or two adjacent spines' - with preparatory's EXTRA clause (d), 'the secondary spine carries 1 task only', tighter than any sibling - cannot describe it. S7 met it live at C3 (ARV-D-094) and amended mid-cycle; S8, S11 and S10 applied it free. Applied free here. Still no V-rule in the constitution: the exception describes a closing unit's SHAPE and never mandates one.
(3) RULE 10'S ITEM-COUNT LINE - THE THIRD DISCOVERY OF THE SAME STALE SENTENCE. It said 'one item per (section x spine) cell'; this stage's own assessment v1.4 (2026-08-12) emits TWO. S10 struck it at middle, filed secondary's as a defect against a certified stage, and wrote that 'preparatory carries the same line free and should strike it at S9's P1 rather than let it be found a third time'. Struck, with the corollary the assessment file already carries: the item count does not vary with the period count.
(4) RULE 9 NAMES WHICH SUBHEADING a merged cell uses - and AT PREPARATORY THIS IS THE MAJORITY CASE. S10 found it at middle, where 16 of 96 cells carry a MERGED section_name (17%). At preparatory it is 93 of 167 (55%), and the longest runs to 28 WORDS: 'Let us Read + Let us Think A + Let us Think B + Let us Think C + Let us Think D + Let us Think E' - longer by itself than any brief cap, before the brief begins. The pilot's own writing and word_work cells are both merged. Left unsaid, Rule 9 is unsatisfiable on the richest cells in the stage.

THREE CAPS, AND ONLY ONE WAS FORCED (recorded separately because S4's lesson is that a limit stated as a number is what live generation most often disproves).
- task_brief: NO CAP -> <= 18 words INCLUDING the Rule 9 locator. FORCED, and it was a HOLE rather than a relaxation: preparatory stated no task_brief cap anywhere against a Rule 9 that MANDATES the '<Subheading> (pp.NN-MM): <plain brief>' locator. Only 2 of 29 saved briefs carry a locator at all - the mandate postdates the corpus - so the raw distribution understates the length. Simulating the locator at its true cost (+4 words) gives max 16, 14 of 29 over 12, 0 over 16. Middle's OLD cap of 12 would have been unreachable; 18 is the number secondary and middle both settled on independently, so the family now carries one number.
- activity_title <= 10 -> <= 12. Family alignment on a SATURATED cap: the preparatory corpus maxes at exactly 10 of a 10-word cap, where middle and secondary allow 12 against a corpus max of 11. A cap the corpus already sits on is one live generation from a defect report.
- section_context 10-15 -> 10-18. Family alignment, and UNFORCED: preparatory's own corpus maxes at 13 of 15. Recorded as unforced so C3 does not read it as evidence-backed. Lower bound kept.

ONE HOUSEKEEPING CORRECTION: the footer read 'Version 1.0' against a v1.1 header - stale since the 2026-08-11 bump. Now tracks, with the family's '. Internal Document' suffix.

CANCELLED AMENDMENTS AND V-RULES: none introduced. Guards assert role_handoff, unit_handoff, band_ref, 'role weighting', phase_ref, band_id, 'section registry', 'reserved token', 'synthesis unit', 'closing synthesis' all 0.

SECTION 9 COSTS NOTHING: no english-preparatory library exists, so nothing re-opens. S7 paid ~Rs.106 and a C1-C3 re-run for the same class of finding.

Artefacts: genon/out/stage_prep_english_preparatory/apply_s9_amendments.py (27 guarded replacements, 22 absence guards, 16 presence guards) . lp_english_preparatory_v1.1_pre.txt . lp_english_preparatory_v1.1_to_v1.2.diff."""),

    "P2": ("pass", "Claude", """AMENDED 2026-08-13. Assessment constitution v1.4 -> v1.5.

A6 IS A GENUINE CONFIRMATION - THE SECOND IN THE CAMPAIGN, after S10's, and for the same reason. P2 asks for a confirmation and an amendment only where absent. RULE 8A ALREADY CARRIES IT IN FULL, having landed a day early with the cross-stage PAIR pass (v1.4, 2026-08-12): the anchor is the (section x spine) CELL, borne by the item's own source_section_id + source_spine - 8-rule ROW 7, the table's ONLY PAIR KEY - resolved by the platform against each period's section_id + spines_taught[], with TWO-STAGE SCOPING declared by SLOT and period_ref / period_number / unit_ref prohibited outright. The v1.2-era band-level phase_ref is absent and was not reintroduced (grep -c phase_ref = 0 in both files). NOTHING WAS AMENDED FOR A6. Asserted by guard, not by eye.

A9 - THE REMOVAL IS N/A; THE TWO LINES ARE PURELY ADDITIVE. This file never carried the MEMORY item-18 position prohibition; testing.md P2 names the four files that do (SS + Science, middle and secondary) and this is not one. Confirmed by grep: 'consecutive items', 'same label', 'vary in position' all 0. The FIFTH stage running where the removal is N/A (after S4, S7, S8, S5, S11, S10). ADDED in the v1.7 wording, in RULE 4 where english states its MCQ semantics - the site secondary chose at v1.4 and middle at v3.7, for the same reason (Rule 5 is an indented bullet list a two-paragraph block reads oddly inside): the 'MCQ OPTION ORDER IS NOT YOURS TO SET' mandate (order carries no meaning; uneven letters are coincidence; the platform arranges deterministically after generation) and the by-label option-reference prohibition ('both A and B', 'none of the above', 'all of the above', 'either B or C'). Purely additive - no prior 'none of the above' ban existed here to absorb. NOT RE-ADDED: 'alphabetic', 'never led with', 'first word at which they differ' all assert 0.

CONFIRMED PRESENT AND UNTOUCHED: the poem locator (Rule 3, ARV-D-138, carried 2026-08-12 - REPRODUCING THE POEM and the eight-word incipit cap), Rule 2's slot table and the PAIR. The pilot chosen for this stage is a POEM, so preparatory's half of the copyright fix is proved by live generation at C3 rather than inherited untested.

Artefacts: genon/out/stage_prep_english_preparatory/apply_s9_assessment.py . assess_english_preparatory_v1.4_pre.txt . assess_english_preparatory_v1.4_to_v1.5.diff."""),

    "P3": ("pass", "Claude", """APPLIED 2026-08-13 - real, not N/A. The SIXTH stage where this was not N/A (after S6, S7, S8, S11, S10).

phases[{minutes, description}] -> time_bands[{minutes, activity}], array and key, with Rule 5, Rule 2A's 'explicit timed phase' and its re-recite band, Rule 3's narration sentence AND ITS TWO LISTENING BANDS - the prep-specific site no sibling has, because listening is not a spine at prep: it rides INSIDE oracy as per-task transcript_ref + transcript_text and Rule 3 gives it its own timed bands - Rule 8's locator mirror, Rule 9's heading (PHASE NARRATION -> BAND NARRATION), the lint-scope line and the schema all following. NO band_id.

Guards: grep -c 'phases[' = 0, '\"phases\"' = 0, band_id = 0, time_bands = 2, '\"activity\": string' present, AND THE WORD 'phase' REACHES ZERO OCCURRENCES in the file, matching english-middle and english-secondary.

THIS STAGE OWED NO PLUGIN WORK - english/subject.py::_bands has read both keys, newest first, since S11 landed it on 2026-08-12, which is what keeps the four saved preparatory plans rendering with a timed spine after the rename. Third time a display debt one stage paid has made a successor's P3 free (maths-prep inherited maths-middle's the same way, and S10 inherited S11's)."""),

    "P4": ("pass", "Claude", """DONE 2026-08-13, AND IT INCLUDED A REMOVAL. Both constitutions already had a CHANGELOG.md sidecar (created 2026-08-11 and 2026-08-12 by the cross-stage passes) and each gains its entry.

THE ASSESSMENT CONSTITUTION CARRIED AN IN-DOCUMENT HISTORY BLOCK - v1.4 wrote its own seven-line changelog above DESIGN PRINCIPLE, which is exactly what P4 forbids. Lifted out and back-filled as the v1.4 sidecar entry, verbatim, with a note saying where it came from; the VERSION line stays in the file. Guard asserts 'v1.4 (2026-08-12)' = 0 in the constitution. The same removal S10 had to make on its own file the same week.

ONE EXTRA CORRECTION on the LP side: the footer read 'Version 1.0' against a v1.1 header - stale since the 2026-08-11 bump. Both footers now track their headers."""),

    "P5": ("pass", "Claude", """ALL FIVE CLOSED 2026-08-13 - P5.4 INCLUDED, so this stage carries NO AMBER. The first stage in the campaign to enter its C-cycle with nothing open at all.

P5.1 THE FLOOR - accepted at the standing ratio, and NO OVERRIDE IS OWED ANYWHERE IN THE STAGE. For the pilot: round(0.6 x 12) = 7, matching floor_periods_at_standard. Equal dispersion over [7, 12]: A-C = 5 >= 4, so counts are [12, 10, 7] - three canonicals, three authoring runs. The full-coverage arithmetic was swept before the rule was accepted (the S8 rule): a prep chapter with N cells needs 1 + ceil((N-1)/2) periods - word_work occupies a period alone per Rule 2 STEP 4, the rest pack at <= 2 adjacent - so a full 5-cell chapter needs 3. Swept across ALL 39 PREPARATORY CHAPTERS, III, IV and V, not only the drawn class: NOTHING BINDS ANYWHERE. The lowest counts in the stage are the 2-period picture-reading chapters (III ch 5, 10, 14) and they carry 1-2 cells against a need of 1-2. The second stage running (after S10) where the sweep found nothing to raise, and the FIRST where the whole three-class stage is clear. Caveat recorded under DEFECTS: the sweep covered 37 of 39 - two class-V summaries are unparseable JSON.

P5.2 THE SECTION REGISTRY - S11's definition INHERITED UNCHANGED, evidenced by S10, and what preparatory changes is the VOCABULARY, not the definition. Member: the (section x spine) CELL; token '<section_id>|<spine_key>'; joined 'B|writing / B|word_work' for a two-spine unit; first-visit order is the summary's on-page spine order, which is NOT the canonical enumeration order the handoff is keyed by (a C5 check comparing one against the other will fail a good plan). THE SPINE SET IS FIVE, AND THREE OF THE FIVE KEYS DIFFER FROM MIDDLE'S: reading (not reading_for_comprehension) . oracy (listening AND speaking MERGED) . writing . word_work (not vocabulary_grammar) . beyond_text. Listening is not a spine here: it rides inside oracy as per-task transcript_ref + transcript_text. A C5 or C9 check written against middle's six keys is WRONG FOR EVERY CHAPTER of this stage.
THE PILOT REGISTRY, in first-visit order: B|reading (Let us recite, 1 task) . B|oracy (Let us think + Let us speak, 2) . B|writing (Let us think + Let us write, 4) . B|word_work (Let us learn + Let us write, 3) . B|beyond_text (Let us explore, 1). TWO TRAPS FOR C5: (a) the section id is B, NOT A - english III is fully split, 17 chapters with one main_section each, and the split KEPT each section's position in its original textbook unit, so ids run A, B across a unit's chapters; five of the seventeen are B and the pilot is one. (b) THREE of the pilot's five cells carry a MERGED section_name, which is what Rule 9's new WHICH SUBHEADING clause is for. FIVE MEMBERS AGAINST TWELVE UNITS is the DENSEST cell-to-unit ratio in the english family (secondary's pilot was six against seventeen), so the Xth-unit borrow at C8 is more often a cell's CLOSING unit than its opening one - named here so C8 reads it as expected rather than as a finding.

P5.3 THE PILOT - english|III ch 11 'The Big Laddoo' (section B, POEM, pp. 70-77). Summary and mapping on disk, placeholder false, canonical_plan present, counts [12, 10, 7], provisional/arithmetic as expected pre-C1. CHOSEN FOR THE POEM (founder, this session) over ch 3 'Badal and Moti' (prose, section A, identical band [12, 10, 7]): ch 11's summary carries poem_text in full, 13 verbatim lines, so it is the chapter that actually exercises the poem-locator rule carried at v1.3 - the campaign's sole open copyright finding (F2), closed on paper on 2026-08-12 and, at THIS stage, never proved by live generation. THE COST IS NAMED: ch 11 is tied for the largest chapter in the class, so three runs at 12/10/7 are among the stage's most expensive; and PICTURE_NARRATIVE - preparatory's OWN section type, four of III's seventeen chapters and exercised nowhere else in the campaign - is NOT the pilot, and is left to the pre-warm sweep the way S11 left drama and S10 left prose. The band is the joint-widest, so C8 loses nothing.

P5.4 THE THREE PROFILES - CLOSED (founder, this session), through the app's own first-run flow, never by hand-editing JSON. Verified on disk: kumar1 = section 3C, durations [40], ppw {40:5}; kumar2 = 3B, [40], {40:5}; kumar3 = 3E, [40, 50], ppw {40:3, 50:2}, anchor 40. SECTIONS ARE DISJOINT, which is the whole of X1's evidence. The mixed duration on kumar3 is a 1.25x stretch (40 -> 50) - a canonical authored at 40 min served into a 50-minute sitting, the ordinary Indian-timetable case, so C6 gets a realistic scaling test rather than an exotic one; the same stretch S10 drew, where S11's was 1.2x. The 'nothing left over from an earlier stage' clause stays waived per the founder ruling of 2026-08-07 (S6): the residue touches no english-III key.

P5.5 THE CARRIER - CLOSED, AND IT WAS THE LAST ENTRY IN _NOT_YET. Trace: rule 7 . period-field family . item (source_section_id + source_spine) -> period (section_id + spines_taught[]) . container: a list of SPINE groups each carrying items[] . plugin method EnglishSubject.assessment_to_view, whose join, N-to-N pairing and section-wide fallback live in english/subject.py::cell_resolver . genon_assessment present, stage-agnostic, landed at S11 . not in _NOT_YET as of 2026-08-13, AND _NOT_YET IS NOW EMPTY. Part 5 (where the PERIOD keeps its section anchor): grep -c section_anchor = 0 in this LP constitution, so the read is mediated - genon_unit_anchor builds the composite cell token (verified returning 'A|reading' on a real saved period) and genon_anchor_field_present returns False, the expensive half. THE EXPENSIVE HALF IS VISIBLE IN THE GENERATED BRIEF: genon/out/briefs/ch_11_top.txt asks for the '\"synthesis\": true' BOOLEAN and says in terms 'this stage's periods have no field to hold a reserved token, so do not invent one' - the metered-STEP-1 failure the S5 note exists to prevent, visibly not happening. See the SIGN row for the confirmation in full."""),

    "SIGN": ("pass", "Claude", """S9 IS CLEAR TO ENTER C1 (2026-08-13), WITH NO GATE AND NO AMBER - the first stage in the campaign to sign with every P-step closed, P5.4 included. Full note: genon/out/stage_prep_english_preparatory/STAGE_SIGNOFF_S9_english_preparatory.md

THE CARRIER WAS THE LAST ENTRY IN _NOT_YET, AND DELETING IT EMPTIED THE TABLE. Every subject-stage in the 11-stage matrix is now carried. The note S11 wrote and S10 confirmed named three things to CONFIRM, not re-derive, plus ONE DIFFERENCE specific to this stage - and the difference was real: PREPARATORY'S SPINE SET IS FIVE, NOT SIX (reading, not reading_for_comprehension; oracy, with listening AND speaking merged; writing; word_work, not vocabulary_grammar; beyond_text). WHY THAT COSTS NOTHING, AND WHY IT IS NOW A TEST RATHER THAN A COMMENT: no part of the carrier reads a spine NAME - cell_resolver joins whatever spines_taught[] holds against whatever source_spine holds, and genon_unit_anchor composes the cell token from both halves without a vocabulary. A carrier that had hard-coded the six middle keys (the obvious shortcut when secondary was the only stage) would have passed S11 and S10 and failed EVERY CHAPTER of this one. So the deletion was again the whole job: NO NEW CODE LANDED.

CONFIRMED AGAINST THE REAL SAVED CORPUS BEFORE THE LINE CAME OUT (genon/out/stage_prep_english_preparatory/verify_s9_carrier.py, re-runnable, and re-run after): 37 readable chapters and 167 taught cells across III/IV/V use the five prep keys AND NOTHING ELSE, all five exercised, and no middle-only key appears in the constitution as a KEY; all 4 saved preparatory plans group items by spine_code; every coverage_handoff is the spine-keyed dict _ENGLISH_SPINE_CELL round-trips. END TO END: 18 items, ZERO ORPHANS, every anchor equal to the INDEPENDENTLY COMPUTED 'last unit teaching that cell', with the N-to-N pairing intact.

_NOT_YET IS KEPT THOUGH EMPTY, and the comment above it says why: an empty table is not a dead switch but the pre-flight that makes carrier_gap() free, and the next subject-stage brought into genon belongs in it BEFORE it is authored, not after it is paid for.

tests/test_genon_carriers.py: 122 tests with 6 failures -> 131, GREEN. The six were exactly the 'preparatory is still owed' assertions this step invalidates, spread across four classes. Rather than delete the properties they protected, THREE WERE KEPT ALIVE AGAINST AN EMPTY TABLE BY A SYNTHETIC ENTRY - the refusal machinery, the stage/row reporting contract, and the conservative gradeless read - because emptying the table would otherwise retire the pre-flight silently and the next subject would find out at certification, after paying. A new TestEnglishPreparatoryLanded class of eight replaces them, on a NEW FIXTURE (tests/fixtures/english_iv_ch01_saved.json, a real saved IV plan) whose centrepiece is what neither sibling fixture has: ONE PLAN EXERCISING BOTH ANCHORING BRANCHES - word_work taught across units 4 AND 5 with TWO items (N-to-N: 4 and 5, not 5 and 5) beside oracy taught across units 2-3 with ONE item (the last-unit rule: 3) - plus the explicit assertion that no middle spine key ever resolves here.

THE DRY PRE-FLIGHT CAUGHT A DEFECT NO CONSTITUTION READ WOULD HAVE FOUND: THE PROMPT BUILDER WAS STILL SAYING 'ONE ITEM PER CELL'. genon/prompt_assembly.py - the english LP+A builder S11 lifted from the prototype - contradicted assessment Rule 2's PAIR in two places, both CITING Rule 2 while contradicting it: the output sketch's assessment_items block ('<one item per section_contribution ... (Assessment Constitution Rule 2)>') and CRITICAL CONSTRAINTS ('Total assessment item count = number of section_contributions ... one item per spine-cell implied_lo ... Generate one original item per cell'). The 2026-08-12 PAIR amendment moved three assessment constitutions; S10 and S9 moved two of the three LPs beside them; NOBODY MOVED THE BUILDER, which sits between both and the model and is the text closest to the output schema. It is stage-agnostic, so it said this to english-secondary and english-middle too. IT DID NOT BITE AT S10 - its library came in at 12 items across 6 cells in all three canonicals, the model following the constitution over the builder - and that is the argument for fixing it, not against: a coin-flip resolved favourably once, on one chapter, by a model that keeps a habit for a whole run or drops it for a whole run. FIXED HERE, FREE, BEFORE C1, and worded so it cannot go stale again: the builder now defers to Rule 2 and its slot table as the sole authority on count and slot order and says 'do not assume one'. V-SERIES / PIPELINE, NOT CONSTITUTIONAL, so section 9 does not fire and no authored library re-opens - the fix makes the builder AGREE with the constitutions S10 and S11 were authored under. Re-verified in a second dry run. Filed as a defect row so S10 and S11 can read it against their own item counts.

DRY PRE-FLIGHT, FREE, RUN BEFORE SIGNING: 'generate_canonical.py one english iii 11 --dry' assembles English . Grade III . ch 11 - 12 x 40 MIN, system 53,588 chars / user 23,383. THE '12 x 40 min' LINE IS ITSELF AN A1 ASSERTION - under v1.1 the same command would have assembled at a duration the master plan does not carry. PRESENT, asserted rather than eyeballed: LP v1.2, assessment v1.5, THE SELF-CONTAINED REGISTER, A1's 'exactly ONE row' + the master-plan bands + 'authored at 40 MINUTES', FULL SPINE COVERAGE, Rule 1's CLOSING unit exception, Rule 9's WHICH SUBHEADING and BAND NARRATION, A9's option-order mandate, RULE 8A, the PAIR + its SLOT TABLE, 'TWO per section_contributions', the poem locator (AT MOST EIGHT WORDS) and REPRODUCING THE POEM, time_bands / '\"activity\": string' in the output sketch, '<= 18 words', the builder's new 'ASSESSMENT RULE 2 ... do not assume one', and the pilot's poem_text (correctly - reading is legal, reproducing is not). ABSENT: '30 or 35', PHASE NARRATION, any surviving phases key, section_anchor, phase_ref, role_handoff, band_id, 'preview into next', 'the previous unit', 'one item per', 'alphabetic', 'never led with', the middle-only spine keys, any stale VERSION 1.1 / 1.4 string. The word 'phase' survives ONCE in the whole prompt, in the assessment constitution's DESIGN PRINCIPLE ('the arc has two phases'), where it is the ordinary word for a stage of a process and names no schema field - left deliberately. build_library.py's STEP 0 pre-flight passes and --certify-only runs to 'Row is provisional', the expected pre-C1 state. The english prompt builder needed no lift: it dispatches on subject, not stage.

TEST SUITES: test_genon_carriers 131 green, test_genon_serve (all e14 assertions), test_genon_duration_order, test_lp_standard, test_calibrated_defaults all pass. test_genon_plan_key fails - CONFIRMED PRE-EXISTING by re-running it against the stashed, unmodified tree.

TWO DEFECTS RAISED, both recorded below: two english-V chapter summaries are UNPARSEABLE JSON (unescaped straight quotes in a value - the same hazard the curly-quote amendment closed on the OUTPUT side, showing up on the INPUT side where no constitution reaches it), and the prompt-builder PAIR contradiction above.

C3 INHERITS A NAMED AGENDA beyond the rule table: the poem locator under the PAIR (two items per cell means two chances to drift, and READ 'LET US RECITE' FIRST - preparatory's reading cell for a poem is a single recitation task, the likeliest place for a stem to reproduce the verse 'so the child can say it back' and the one cell where a locator feels least natural to write; NCERT prints no line numbers on its poems, so a bare 'lines 5-8' with no page is a defect, not a style note); the three caps this pass moved or added - task_brief <= 18 (NEW), activity_title <= 12 (was saturated at 10), section_context 10-18 (UNFORCED, so treat a breach as evidence about the number, not about the plan); and WHETHER THE BUILDER FIX ACTUALLY PRODUCED 10 ITEMS FOR 5 CELLS rather than 5, this being the first library authored under the corrected text.

C5 NOTE: check 11 (the summary reconciliation, new at template v2.10) GATES for this stage - english summaries declare their sections in JSON main_sections[], so it is one of the gating subjects, not an advisory one. The pilot declares exactly one, B."""),
}

DEFECTS = [
    {
        "combo": "english/preparatory",
        "step": "P5",
        "severity": "S2",
        "owner": "founder",
        "status": "open",
        "title": "Two english·V chapter summaries are NOT PARSEABLE JSON — unescaped straight "
                 "quotes inside a value, on the INPUT side where no constitution reaches it",
        "evidence": (
            "FOUND AT S9's P5.1 floor sweep, which could only cover 37 of the stage's 39 chapters.\n\n"
            "data/content/chapters/english/v/summaries/ch_08_summary.json (The Decision of the "
            "Panchayat) fails at line 50 col 393 and ch_09_summary.json (Vocation) at line 14 "
            "col 139. Both carry UNESCAPED STRAIGHT DOUBLE QUOTES inside a JSON string value — "
            "dialogue in the first ('Who said to whom: a. \"I sold only the well, not the "
            "water.\"'), a poem's own quoted speech in the second ('the hawker crying, "
            "\"Bangles, crystal bangles!\"'). json.load() fails on both, so NEITHER CHAPTER CAN "
            "BE READ AT ALL — not by the pipeline, not by the app, not by any check in this "
            "campaign.\n\n"
            "IT IS THE 2026-08-11 CURLY-QUOTE HAZARD ON THE OTHER SIDE OF THE PIPE. That "
            "cross-stage amendment closed the hazard where the MODEL emits JSON (the Rule 9 "
            "narration format). This is the same failure in AUTHORED CONTENT, which no "
            "constitution governs, so the fix there cannot reach it.\n\n"
            "DOES NOT BLOCK S9 — the drawn class is III and both files are class V — but it "
            "blocks those two chapters at pre-warm, and it means S9's floor sweep is 37 of 39, "
            "not 39 of 39. The repair is mechanical (escape or curl the inner quotes) and is a "
            "CONTENT fix, not a constitutional one; §9 does not fire.\n\n"
            "WORTH A CORPUS-WIDE SWEEP: nothing has ever asserted that every chapter summary "
            "parses. A one-line json.load() over all 330 would say whether these two are the "
            "only ones, and belongs in the certifier's free checks rather than in a stage."
        ),
    },
    {
        "combo": "campaign",
        "step": "C1",
        "severity": "S3",
        "owner": "founder",
        "status": "closed",
        "title": "The english prompt BUILDER still said 'one item per cell' — contradicting "
                 "assessment Rule 2's PAIR at all three english stages, while citing it",
        "evidence": (
            "FOUND AT S9's DRY PRE-FLIGHT, by sweeping the assembled prompt for stale strings "
            "rather than by reading a constitution — which is why it survived two stages of "
            "P-prep.\n\n"
            "genon/prompt_assembly.py (the english LP+A builder S11 lifted from the prototype) "
            "said 'one item per cell' in two places, BOTH CITING RULE 2 WHILE CONTRADICTING "
            "IT: the output sketch's assessment_items block ('<one item per section_contribution "
            "in coverage_handoff for this spine (Assessment Constitution Rule 2)>') and CRITICAL "
            "CONSTRAINTS ('Total assessment item count = number of section_contributions ... "
            "(one item per spine-cell implied_lo, per Assessment Rule 2) ... Generate one "
            "original item per cell').\n\n"
            "THE 2026-08-12 PAIR AMENDMENT MOVED THREE ASSESSMENT CONSTITUTIONS. S10 and S9 "
            "moved two of the three LPs beside them (secondary's is a separate open defect). "
            "NOBODY MOVED THE BUILDER — which sits between both and the model, and is the text "
            "closest to the output schema. It is stage-agnostic (dispatching on "
            "subject_to_folder), so it said this to english·secondary and english·middle too.\n\n"
            "IT DID NOT BITE AT S10, AND THAT IS THE ARGUMENT FOR FIXING IT. S10's authored "
            "library came in at 12 items across 6 cells in all three canonicals — the model "
            "followed the constitution over the builder. A coin-flip resolved favourably once, "
            "on one chapter, by a model that (curly quotes, ARV-D-1xx) keeps a habit for a whole "
            "run or drops it for a whole run.\n\n"
            "FIXED AT S9's P-prep, free, before C1, and worded so it cannot go stale again: the "
            "builder now defers to ASSESSMENT RULE 2 and its slot table as the sole authority "
            "on the count and the slot order, and says in terms 'do not assume one'. Re-verified "
            "in a second dry run — 'one item per' and 'Generate one original item per cell' both "
            "reach 0.\n\n"
            "V-SERIES / PIPELINE, NOT CONSTITUTIONAL: §9 does not fire and no authored library "
            "re-opens — the fix makes the builder AGREE with the constitutions S10 and S11 were "
            "authored under. FOLLOW-UP FOR S11: its library was authored under the stale text "
            "and should be read at its own item count before this is treated as historical."
        ),
    },
]


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s9"))

    row = state.setdefault("stages", {}).setdefault(KEY, {})
    for step, (status, by, comment) in ROWS.items():
        row[step] = {"status": status, "by": by, "at": NOW, "comment": comment}

    defects = state.setdefault("defects", [])
    nums = [int(d["id"].rsplit("-", 1)[1]) for d in defects
            if isinstance(d.get("id"), str) and d["id"].startswith("ARV-D-")
            and d["id"].rsplit("-", 1)[1].isdigit()]
    nxt = (max(nums) if nums else 0) + 1
    added = []
    for d in DEFECTS:
        d = dict(d, id=f"ARV-D-{nxt:03d}", raised_at=NOW)
        defects.append(d)
        added.append(d["id"])
        nxt += 1

    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"tracker updated · {KEY} · {', '.join(ROWS)} · {NOW}")
    print(f"defects added   · {', '.join(added)}")


if __name__ == "__main__":
    main()
