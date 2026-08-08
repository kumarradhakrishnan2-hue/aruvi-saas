#!/usr/bin/env python3
"""S4 · P5.5 landed — the mathematics carrier exists. P5 and SIGN both go green.

Rewrites ONLY P5 and SIGN for mathematics/secondary. All P-steps are now closed and the
stage is clear to enter C1.

Run from the repo root:
    python3 genon/out/stage_prep_mathematics_secondary/update_tracker_s4_p5_closed.py
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "mathematics/secondary"

P5 = """CLOSED 2026-08-08 — all five sub-items done.

P5.1 FLOOR: standing ratio, no override. round(0.6 x 14) = 8, matching floor_periods_at_standard. Equal dispersion over [8, 14] gives counts [14, 11, 8] — three canonicals, three authoring runs.

P5.2 REGISTRY: obvious, no definition needed. The summary carries an explicit sections[] spine of {ref, title} and LP A3 specifies section_anchor as the bare ref. Ch 4's registry is the eight refs in summary order (4.1 Introduction ... 4.8 Simplifying Rational Expressions). Consistency across the library is guaranteed by construction: standard_registry() reads it off the AUTHORED standard, briefs_for() prints it verbatim into every compact brief. Nothing about the registry enters a constitution.

  ITS OPEN ITEM IS NOW FIXED — the synthesis unit's handoff row. On a DERIVED-anchor stage an item reaches its unit only through a coverage_handoff row; the synthesis unit is not a section, so it got no row and could hold no question, making C9.2 unsatisfiable on the Case-1 borrow. Measured on the CERTIFIED science ix ch 8 library: the model invented a row unprompted and NO item used it (item section_numbers stopped at 10; stamped unit_refs never reached unit 12). Fixed by one added instruction in variant_plans.top_brief_for, emitted ONLY where carriers.item_anchor_is_derived() is true — verified present for mathematics ix and science ix, absent for social_sciences ix (item-self-sufficient) and for science viii (plan-granularity arc brief). V-series, so no constitution moved and only a --certify-only re-run is implied for existing libraries.

P5.3 PILOT CHAPTER: mathematics / IX / ch 4 'Exploring Algebraic Identities' — founder pick from the eight eligible (9-16 are placeholder). Summary + mapping on disk, placeholder false, canonical_plan present, 8 sections, 18 worked examples, 21 exercises, core_cg CG-3, co_central false, effort_index 11.0.

P5.4 TEST IDENTITY PROFILES for class IX: DONE, set up by Kumar through the app's own first-run flow. Verified on disk: Mathematics IX on all three; sections DISJOINT (kumar1 B+D, kumar2 F, kumar3 H+I); MIXED DURATION on the right identity — kumar3 carries [50, 60] with ppw_by_duration {50: 5, 60: 2}, anchor 50, and section 4 assigns the mixed-duration matrix to kumar3. kumar1/kumar2 are 50-only at 7 ppw. Leftovers from S1-S3/S6 accepted per the 2026-08-07 ruling. grids[] all -1, correct post-Calendar-Purge.

P5.5 THE CARRIER: DONE — and it was a DELEGATION of the verified 8-rule table, exactly as the doctrine requires, not a new join. Mathematics secondary is ROW 6: item section_number -> handoff section_number -> period_numbers, never section_anchor text, items under the {..., questions: []} wrapper, anchoring at the section's LAST unit. _secondary_assess already ran that rule for the app; genon needed the same rule on the RAW item dicts. What landed:
  1. genon_assessment on the mathematics plugin — secondary delegates to carriers.items_by_handoff with row 6's two keys; middle/preparatory RAISE naming their own family (period-field, rows 4/5), so they cannot silently borrow row 6. Stage told apart by CONTAINER SHAPE, not stage_for(grade): the method receives only `result` and the grade lives on the enclosing plan, so a grade read there is None on the very call the carrier makes. test_genon_carriers caught that immediately and now pins it.
  2. _NOT_YET re-keyed by subject·STAGE. It was per subject, so 'mathematics' was one entry spanning two families and deleting it would have declared middle+prep ready too. Now secondary is absent while ('mathematics','middle') and ('mathematics','preparatory') remain, each naming its 8-rule row and owing stage (S7/S8).
  3. carrier_gap() / require_carrier() + a STEP 0 pre-flight in build_library.py. P5.5 asked for a read; this makes it a GATE, because a gate cannot be forgotten. An owed stage now stops with 'STOP before spending — ...' before any metered step. Verified: mathematics vii and english ix both stop cleanly; mathematics ix proceeds.
  4. generate_canonical.validate no longer swallows CarrierNotImplemented — it sat in a bare except Exception whose fallback read a key the wrapper subjects lack, so the item-anchor check silently saw zero items and passed. That is what made a missing carrier a PAID failure.
  5. genon_item_anchor_family declared on base/science/mathematics — the 8-rule family column as a first-class fact rather than an inference; it is what the synthesis-row brief line reads.

TESTS: test_genon_carriers 25 -> 36, all green (row-6 join at LAST unit, synthesis row reachable, unserved anchor -> [] not a guess, raw fields survive, the no-grade regression, the pre-flight gate, all eight family rows). Full suite 20 passed / 5 failed, and all five failures were confirmed PRE-EXISTING by re-running them on a tree with these changes reverted (test_api needs fastapi; test_link_resolver and test_normalized_item want a missing English saved plan; test_lp_standard a missing TWAU view; test_stimulus a fixture count)."""

SIGN = """CLEAR TO ENTER C1 — 2026-08-08. Status to be set by Kumar.

CONSTITUTIONAL GATE: clear. A1 lands, the register is ONE block in the full v1.10 three-ban form, A6 anchors present as the derived section_number form on both sides, A9 landed as the v1.7 two lines with the removal recorded N/A (this stage never carried item-18) and no arrangement sentence anywhere, P3 N/A with grep evidence (Group A), no cancelled amendment (A2/A3/A4) and no V-rule in a constitution, no pedagogical rule changed. The edit script reproduces both live constitutions byte-for-byte from the PRE files and aborts loudly on re-run.

BOTH BLOCKERS FIXED, not merely declared (see P5):
  - The carrier — landed as a delegation of 8-rule row 6, plus the stage-aware _NOT_YET, the free STEP 0 pre-flight, and the validate swallow fix that had made a missing carrier a PAID failure rather than a refusal.
  - The synthesis handoff row — one brief line in top_brief_for, emitted only on derived-anchor stages. Note this was a live defect against the CERTIFIED S3 library too (science ix ch 8's invented synthesis row has zero items anchored to it), so S3 may want a --certify-only re-run and a section 7 defect row; it is not an S4 matter.

ONE FOUNDER EYE WORTH SPENDING BEFORE STEP 4: the synthesis-row brief line is new, so ch 4's top canonical is the first artefact generated against it. Read that single handoff row in STEP 1's output before letting STEP 4 buy the two compacts — STEP 1 is resumable, so the check costs nothing and it is the cheapest place to catch a wording problem.

C1 COMMAND: python3 genon/build_library.py mathematics ix 4
It will no longer stop at the carrier. It WILL still stop at STEP 2 with 'Row is provisional' until the standard canonical exists — the normal path for a fresh chapter, not a fault.

Nothing re-opens: no stage carries a signed human GATE, so testing.md section 9 costs nothing. Template is at v2.8, which added P5.5."""

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_s4_closed"))

row = state["stages"][KEY]
row["P5"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": P5}
row["SIGN"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": SIGN}
state["updated_at"] = NOW

STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{KEY}: P5 and SIGN both -> pass")
for step in ("P1", "P2", "P3", "P4", "P5", "SIGN"):
    print(f"  {step:5} {row[step]['status']}")
