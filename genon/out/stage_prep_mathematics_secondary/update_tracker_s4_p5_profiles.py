#!/usr/bin/env python3
"""S4 · P5.4 landed — the three test identities' Mathematics IX profiles exist.

Rewrites ONLY the P5 cell for mathematics/secondary, preserving every other step.
P5 stays "blocked" because P5.5 (the carrier) is still open — the reason has changed,
not the status.

Run from the repo root:
    python3 genon/out/stage_prep_mathematics_secondary/update_tracker_s4_p5_profiles.py
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "mathematics/secondary"

COMMENT = """RECORDED 2026-08-08; P5.4 CLOSED, P5.5 STILL OPEN — so P5 remains blocked, for a different reason than before.

P5.1 FLOOR: accepted at the standing ratio round(0.6 x recommended_periods), no override. For ch 4, round(0.6 x 14) = round(8.4) = 8, matching floor_periods_at_standard on the row. Equal dispersion over [8, 14]: A-C = 6 >= 4, so counts are {A, ceil((A+C)/2), C} = [14, 11, 8] - three canonicals, three authoring runs.

P5.2 REGISTRY: mathematics secondary's section model is OBVIOUS and needs no definition. The summary carries an explicit sections[] spine of {ref, title} and LP A3 already specifies section_anchor as the bare ref ('e.g. 2.5'). For ch 4 the registry is the eight refs in summary order: 4.1 Introduction, 4.2 Visualising Identities, 4.3 Factorisation of Algebraic Expressions Using Identities, 4.4 More Identities, 4.5 Factorisation Using Algebra Tiles, 4.6 Factorisation Without Using Algebra Tiles, 4.7 Finding New Identities, 4.8 Simplifying Rational Expressions. Library-wide consistency is guaranteed by construction: standard_registry() reads the registry off the AUTHORED standard and briefs_for() prints it verbatim into every compact's brief. Nothing about the registry enters a constitution.

ONE OPEN ITEM RIDES ON P5.2 - the synthesis unit has no home in a DERIVED-anchor handoff. v2.0 mandates the standard's closing synthesis unit with section_anchor = the reserved token, excluded from the registry. Where items anchor by period_ref that is harmless; where the anchor is derived (science secondary, science middle via progression_stage, now mathematics secondary) the item's only route to a unit is its group number -> coverage_handoff -> period_numbers, so a synthesis unit with no handoff entry can carry NO items, and C9.2 ('a borrowed unit brings its own items') becomes unsatisfiable on exactly the Case-1 synthesis borrow that C8 exists to inspect. VERIFIED on the installed science IX ch 8 library: the model invented an 11th entry (section_label 'synthesis', period_numbers [12], total_sections 11) and NO ITEM USES IT - item section_numbers run 1-10, stamped unit_refs are 1,2,4,5,6,7,8,9,10,11, never 12. So C9.2 is ALREADY unsatisfiable on a CERTIFIED library - a defect against S3 (section 7), not only an S4 risk. Maths A4 is stricter still (section_ref/section_title copied VERBATIM from the summary; no summary section to copy), so the model will either omit the entry or contradict A4. One line in top_brief_for closes it for every derived-anchor stage; V-series, never a constitution. SETTLE BEFORE C1 SPENDS.

P5.3 PILOT CHAPTER: mathematics / IX / ch 4 'Exploring Algebraic Identities' - founder pick 2026-08-08 from the eight eligible chapters (9-16 are placeholder: true, awaiting NCERT release). Summary + mapping both on disk, placeholder false, canonical_plan present (counts [14, 11, 8], basis arithmetic, provisional true until the standard is authored). Eight clean numbered sections, mid-book of the covered half, 18 worked examples and 21 exercises for Rule 9's book_ref discipline. core_cg CG-3, co_central FALSE (so Rule 5's OPEN_TASK arrives via Rule 6's lift, not the co-central path), effort_index 11.0. Shape close to the certified SS IX ch 3 pilot, so the roughly Rs 110-150 library benchmark should hold; 3 runs at about Rs 37 is the budget line, and C2 records clean-path and all-in separately.

P5.4 TEST IDENTITY PROFILES for class IX: **DONE 2026-08-08**, set up by Kumar through the app's own first-run / profile flow (which doubles as the live check of that flow). Verified on disk in data/readiness/{u}/{u}/profile.json - every requirement of P5.4 is met:
  - Mathematics IX present on all three identities.
  - Sections DISJOINT, so X1's tenancy evidence is unambiguous: kumar1 = B, D (tags 9B, 9D) - kumar2 = F (9F) - kumar3 = H, I (9H, 9I). No section appears twice.
  - MIXED DURATION present, and on the RIGHT identity: kumar3 carries durations [50, 60] with ppw_by_duration {50: 5, 60: 2}, ppw_anchor 50, periods_per_week 7. Section 4 of the template assigns the mixed-duration weekly matrix to kumar3, so C6's matrix now has real material against the 50-min class standard. kumar1 and kumar2 are 50-only at 7 periods/week - the clean identity/serve rows.
  - Leftovers from S1-S3/S6 remain (Social Sciences VIII+IX, Science VIII+IX) - accepted by founder ruling 2026-08-07: they touch no mathematics-IX key.
  - grids[] are all -1 (no weekly grid), which is correct post-Calendar-Purge, not an omission.
Note this was verified by READING the store, not by calling GET /readiness (the Cowork sandbox cannot reach the local API); the profiles were created through the app, so the API read is implied.

P5.5 THE CARRIER TRACE - the P-step this stage caused to exist (testing.md v2.8 section 3). Genon does not invent linkage; the verified 8-rule table (docs/architecture-plan.md 'Link resolution', restated in link_resolver.py) does, and carriers.py is that table exposed to genon. Mathematics secondary's row: RULE 6, handoff-bridged, item section_number -> handoff section_number -> period_numbers (NEVER section_anchor text), LO from handoff implied_lo (item: implied_lo_assessed), container {..., questions: []} dict, app-side method _secondary_assess (subjects/mathematics/subject.py:263, parity-tested, already serving the app), genon_assessment ABSENT, still in _NOT_YET. The rule is settled and implemented for the app; only genon's door is unopened, and the fix is a ~6-line delegation to items_by_handoff with rule 6's two keys. **OPEN - and this is now the ONLY thing between S4 and C1.** S4's row is identical to S3's rule 2 in everything but the subject name."""

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_s4_p5"))

row = state["stages"][KEY]
row["P5"] = {"status": "blocked", "by": "Claude", "at": NOW, "comment": COMMENT}
state["updated_at"] = NOW

STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{KEY}: P5 rewritten — P5.4 closed, P5.5 open, status still 'blocked'")
for step in ("P1", "P2", "P3", "P4", "P5", "SIGN"):
    print(f"  {step:5} {row[step]['status']}")
