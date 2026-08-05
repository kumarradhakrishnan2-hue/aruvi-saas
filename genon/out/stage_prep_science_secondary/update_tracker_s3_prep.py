#!/usr/bin/env python3
"""Record S3 · science · secondary stage preparation (P1-P4 + P5 + SIGN) into the
campaign tracker state. Idempotent: re-running overwrites the same keys.

Run:  python3 genon/out/stage_prep_science_secondary/update_tracker_s3_prep.py
"""
import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
KEY = "science/secondary"
NOW = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

shutil.copy2(STATE, STATE.with_suffix(".json.bak_s3prep"))
d = json.loads(STATE.read_text(encoding="utf-8"))


def item(status, comment, by="Claude"):
    return {"status": status, "by": by, "at": NOW, "comment": comment}


d.setdefault("stages", {})[KEY] = {
    "P1": item("pass",
        "AMENDED 2026-08-05. LP constitution v1.0 -> v1.1.\n"
        "A1: INPUTS 4 was 'one or more rows of {duration_minutes, count}'; now 'exactly ONE row "
        "{duration_minutes, count}: the class-standard duration (40 min for classes up to VII, 45 "
        "for VIII, 50 for IX) x the period count'. INTEGRITY TIME restated as the single-row form "
        "(total minutes = duration x count; total period count = count), replacing the "
        "sum-over-rows form. A3 preamble gains 'period_schedule: exactly one row - the "
        "class-standard duration x count (INPUTS 4)'; the schema comment reads 'integer - the "
        "class-standard duration'. grep 'one or more rows' = 0.\n"
        "DECLARED DEVIATION: the reference's closing clause says 'handled downstream at PARTITION "
        "time'; the partition engine was retired 2026-07-31, so this file says SERVE time. This is "
        "S2's finding 2, fixed here rather than propagated.\n"
        "A5/A7 REGISTER: present as ONE block after VOCABULARY, titled 'THE SELF-CONTAINED REGISTER "
        "(binds Rules 7 and 10)', carrying exactly the three v1.10 bans with their live mechanisms "
        "and the 'backward continuity is welcome' closing line. Rule 7 references it as prohibition "
        "6 (band text), Rule 10 as prohibition 4 (teacher notes) - referenced, never restated. "
        "VOCABULARY drops its now-contradicted positional examples ('the previous unit', 'this "
        "unit') and adds '\"session\" is outside the register too'. Rule 10's continuity link is "
        "restated position-free: 'Connect this unit to the content already taught - named by that "
        "content itself, never by its position.'\n"
        "DECLARED DEVIATION: the reference's illustrative example is Social Sciences content "
        "('Having traced the Vedic political vocabulary...'). A Vedic example inside a Science "
        "constitution would be a defect in kind, so the EXAMPLE ALONE is substituted with a Science "
        "one. The three bans and the closing rule are verbatim.\n"
        "CANCELLED AMENDMENTS ABSENT: grep -ci for band_id, band_refs, phase_ref, role_handoff, "
        "unit_handoff = 0 on every term. No V-rule anywhere.\n"
        "Artefacts: genon/out/stage_prep_science_secondary/ - lesson_plan_constitution_v1.0_pre.txt, "
        "lp_v1.0_to_v1.1.diff (109 lines), apply_s3_amendments.py (asserts exactly-one occurrence "
        "per edit; re-run reproduces the live file byte-identically - verified by md5)."),

    "P2": item("pass",
        "AMENDED 2026-08-05. Assessment constitution v1.1 -> v1.2.\n"
        "A9 - ONE REMOVAL + TWO LINES, never an arrangement rule. REMOVED the MEMORY-item-18 "
        "position prohibition: 'Answer position carries no signal: is_correct MUST be distributed "
        "across A-D within an assessment and MUST NOT repeat on the same label across consecutive "
        "items or cluster on one letter.' ADDED to Rule 7's mandate, in the v1.7 wording: 'Option "
        "order carries no meaning and is not yours to set: emit the four options in whatever order "
        "they were authored... Uneven letters across a chapter are coincidence, not a defect.' "
        "Prohibitions numbered; new prohibition 2 bans an option referring to another option by its "
        "label ('both A and B', 'none of the above'). VERIFIED NO ARRANGEMENT SENTENCE CAME BACK: "
        "grep -i for alphabetic / never led with / vary in position / consecutive items / distribute "
        "= 0 hits. Ordering is STEP 6 (genon/normalize_options.py), gated at C3 9a.\n"
        "A6 - PRESENT VIA THE SUBJECT'S EQUIVALENT; the reference's period_ref field is NOT ported, "
        "by ruling. Science secondary's unique link is the SECTION, not the unit: LOs are per-section "
        "(LP Rule 6), the handoff is one entry per section, and a section may be taught across "
        "several units (LP Rule 4), so there is no single unit for the model to name. Both "
        "constitutions instead gain ONE integrity line recording that the platform DERIVES the "
        "anchor from section_number through coverage_handoff.period_numbers, and forbidding the "
        "model emitting period_ref or any unit number. FOUNDER RULING 2026-08-05: derive the link, "
        "never demand it - the same doctrine as compile v0.5's derived band ids. grep -c phase_ref "
        "= 0 in both files; the reversed v1.2-era band-level anchoring was never here and was not "
        "introduced.\n"
        "Artefacts: assessment_constitution_v1.1_pre.txt, assess_v1.1_to_v1.2.diff (45 lines), "
        "apply_s3_amendments.py."),

    "P3": item("na",
        "N/A - Group A. This stage already emits time_bands[{minutes, activity}]: "
        "grep -c 'phases\\[' = 0 and grep -c '\"description\"' = 0 in both constitutions. Nothing to "
        "convert; matches the docs/testing.md section 3 stage table, which lists science/secondary "
        "under 'time_bands'."),

    "P4": item("pass",
        "DONE 2026-08-05. CHANGELOG.md created beside each amended constitution "
        "(data/content/constitutions/lesson_plan/science/secondary/ and "
        ".../assessment/science/secondary/). Neither file carried an in-document version-history "
        "block, so nothing was lifted out of the constitutions; both keep their VERSION first line "
        "and their footer version string (both updated to 1.1 / 1.2). Each changelog records the "
        "per-amendment rationale, both declared deviations, and the artefact paths. Pre-v1.1/v1.2 "
        "history is honestly marked as unrecorded (git is the record)."),

    "P5": item("pass",
        "RECORDED 2026-08-05 - provisional, P5.4 OPEN (founder ruling 2026-08-02 permits signing "
        "with only P5.4 outstanding; C6 is the hard stop).\n"
        "P5.1 FLOOR - accepted at the standing ratio, no override. round(0.6 x 12) = 7; the row "
        "carries floor_minutes 360.0, floor_periods_at_standard 7. Equal dispersion over [7,12]: "
        "A-C = 5 >= 4 -> {12, ceil(19/2)=10, 7}; canonical_periods is exactly [12,10,7].\n"
        "P5.2 SECTION REGISTRY - a real cut, RECORDED AS 16 NUMBERED SECTIONS (8.1 / 8.2 / 8.2.1 / "
        "8.2.2 / 8.2.3 / 8.3 / 8.3.1 / 8.4 / 8.5 / 8.6 / 8.7 / 8.7.1 / 8.8 / 8.9 / 8.9.1 / 8.9.2), "
        "with the four lettered sub-blocks (A/B/C under 8.2.2, A under 8.9.1) folded into their "
        "parents. REOPENED SAME SESSION and NOT YET SETTLED: at 16 sections the standard's 11 body "
        "units run 1.45 sections/unit and the floor runs 2.29, i.e. this chapter merges at EVERY "
        "count including the standard - where SS/VIII ch3 ran 0.73 at the standard (15 body units "
        "over 11 sections) and only merged at its floor. The architecture assumes the standard is "
        "the richest treatment and compaction does the merging, so a coarser cut (~12 sections, "
        "keeping 8.2's three numbered children and folding the leaf sub-sections 8.3.1 / 8.7.1) is "
        "on the table. FOUNDER CALL, DUE BEFORE C1.\n"
        "P5.3 PILOT CHAPTER - CONFIRMED. Chapter 8 'Journey Inside the Atom'. "
        "data/content/chapters/science/ix/ has both ch_08_summary.txt and ch_08_mapping.json (all 13 "
        "chapters do). master_plan.json combos['science|IX'] chapter 8: placeholder false, "
        "recommended_periods 12, standard_duration_minutes 50, weight 8. canonical_plan is present "
        "but provisional true / basis 'arithmetic' / registry_sections null / authored [] - the "
        "expected pre-C1 state; it finalizes at C1 once the registry is authored.\n"
        "P5.4 THREE TEST IDENTITIES - OPEN. All three still carry Social Sciences profiles left over "
        "from S1/S2: kumar1 SS VIII-A + IX-A/B, kumar2 SS VIII-B + IX-C/E, kumar3 SS VIII-C + "
        "IX-A/Y. They must be rebuilt for SCIENCE IX through the app's own first-run / profile flow "
        "(the setup doubles as a live check of that flow), with different sections per identity and "
        "one longer duration alongside the 50-min standard so C6's mixed-duration matrix has "
        "something real to draw on."),

    "SIGN": item("blocked",
        "NOT SIGNED - C1 MUST NOT RUN YET. P1-P4 are complete and verified (a verification subagent "
        "re-derived all eight claim families independently; all passed, and it corrected two errors "
        "now fixed in the sign-off). The stage is blocked on ENGINE work, not constitutional work: "
        "the amended constitutions and the pipeline now contradict each other and the pipeline "
        "loses.\n"
        "1. genon/generate_canonical.py::validate requires period_ref on every assessment item "
        "('no resolvable anchor unit (period_ref)'), which the amended assessment constitution now "
        "FORBIDS the model emitting. A science canonical would fail certification by construction. "
        "GATES C1.\n"
        "2. aruvi_core/genon/compile.py::_anchor_items must derive unit_ref from section_number "
        "through the handoff's period_numbers when period_ref is absent - the same join "
        "link_resolver.handoff_period_index already performs for the screen. GATES C1.\n"
        "3. aruvi_core/genon/serve.py's handoff remap does 'for c in handoff.values()' and reads "
        "c['los'] - the SS dict-of-competency shape. Science secondary's coverage_handoff is a JSON "
        "ARRAY of section entries with no 'los' key: an AttributeError on the first science serve, "
        "not a subtle mis-anchoring. Fix belongs in the science normalizer, not a branch in serve. "
        "GATES C6.\n"
        "4. aruvi_core/genon/compile.py's unit projection reads pedagogical_approaches (PLURAL) "
        "while this stage's A3 emits pedagogical_approach (singular), so every served science unit "
        "would carry an empty approaches list and the Overview 'Pedagogy' row would render blank; it "
        "also reads section_context and competency_edges off the period, both of which LP Rule 6 "
        "forbids inside a period object at this stage. Silent, not an error. GATES C12.\n"
        "All four are the same shape - the engine currently knows only the SS carrier family - and "
        "none of them changes a constitution, so none triggers the section 9 cascade.\n"
        "ANCHORING RULING (founder, 2026-08-05): the item's anchor is the LAST unit teaching its "
        "section, NOT the full unit set. Rationale: an item tests the section's whole implied_lo, so "
        "it becomes available only when the section completes - if you did not teach it all, the "
        "class cannot be tasked on any of it. The alternative (full-set membership) would hand a "
        "class a question two thirds of whose material was never taught, which is worse than an "
        "absent question. The engine's own preference sort protects this: a split-section unit has "
        "reach == M, so it lands in the M-alone class and loses to any forward-reaching candidate "
        "before self or pacing is consulted. Consequence to MEASURE at C9: when the winning Xth-unit "
        "candidate IS a split-section unit, its item is deterministically lost (first_dealing_unit "
        "returns the section's FIRST unit, never the one the item is pinned to). Not probabilistic - "
        "count it. Rider still owed: the invariant 'an item appears iff its section completed' is "
        "currently emergent from max() in link_resolver and must be written down, in the architecture "
        "doc and as a line in the assessment constitution. Side effect: with a singleton unit_ref an "
        "item can match the borrow loop or the dropped-unit loop but never both, so the two-loop "
        "duplication risk dissolves and the engine list above stays at four.\n"
        "Also open: P5.2's registry cut (see P5) and P5.4 (the three Science IX profiles).\n"
        "Full record: genon/out/stage_prep_science_secondary/STAGE_SIGNOFF_S3_science_secondary.md"),
}

d.setdefault("combos", {})[KEY] = {
    "provenance": {
        "klass": "ix",
        "draw": "seed 'science|secondary|2026-08-02' over ['ix'] -> ix (sole eligible class)",
        "by": "Claude",
        "at": NOW,
        "chapter": "8 - Journey Inside the Atom",
        "duration": "50",
        "model": "claude-sonnet-4-6 (pinned; not yet run)",
        "date": "2026-08-05 (stage prep; C1 not run)",
        "lp_ver": "1.1 (amended from 1.0 at P1, 2026-08-05)",
        "as_ver": "1.2 (amended from 1.1 at P2, 2026-08-05)",
        "engine": "14 live; UNCHANGED FOR THIS STAGE YET - four engine gaps recorded at SIGN must "
                  "land before C1/C6/C12",
        "variant_plan": "canonical_plan: counts [12, 10, 7] - provisional TRUE - basis 'arithmetic' "
                        "- registry_sections null - authored [] (pre-C1 state; finalizes when the "
                        "registry is authored). Equal dispersion over [7,12], A-C = 5 >= 4.",
        "ledger_ts": "none - C1 not run",
        "report": "none - C1 not run",
        "files": "none - C1 not run",
        "durations_run": "none - C6 not run",
    }
}

d["updated_at"] = NOW
STATE.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"wrote {STATE}")
print("  stages['science/secondary'] :", {k: v["status"] for k, v in d["stages"][KEY].items()})
