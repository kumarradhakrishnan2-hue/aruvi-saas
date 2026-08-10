#!/usr/bin/env python3
"""S7 · mathematics · middle — record C1's TOP-ONLY run + the v3.5 amendment.

Run from the repo root:
    python3 genon/out/stage_prep_mathematics_middle/update_tracker_s7_c1_top.py
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "mathematics/middle"

C1 = """PARTIAL 2026-08-10 - the STANDARD canonical is authored and installed; the two compacts are NOT yet bought (--top-only, deliberate pause for inspection).

RUN: python3 genon/build_library.py mathematics vii 7 --top-only
  ch 7 top, 12 units x 40 min. 18,181 in / 22,362 out - Rs 35.88 - 335.8s.
  saved:     genon/out/canonical/mathematics/vii/ch_07_20260810_161523_canonical.json
  installed: data/content/saved_plans/mathematics/vii/ch_07_canonical.json
  Rs 35.88 against the S4 benchmark of Rs 110-150 for a full three-canonical library - on budget.

THE RUN EXITED 1, AND THE PLAN WAS NEVER THE PROBLEM. generate_canonical.validate reported 'P1..P12: missing section_anchor (the registry join key)' - all twelve units - and stopped the build before STEP 2. It was a FOURTH READ SITE the P5.5 mediation missed: validate read p['section_anchor'] off the period directly instead of through carriers.unit_anchor. Same shape of failure S6 fixed in this very function on 2026-08-07 (it taught validate to ask the seam whether a stage HAS a section axis, but left the anchor read itself hardcoded), one line along. Fixed 2026-08-10: the anchor is read through carriers.unit_anchor, with the synthesis unit exempted (on a mediated stage it anchors to no section and unit_anchor returns None by design; on a token stage it carries the reserved token and would pass anyway). Verified free: validate(result, 12, False) on the installed file now returns NONE. The canonical had already installed ('validator findings recorded, not blocking'), so no rupee was lost and STEP 1 is skipped on resume by skip_if_present.

INSPECTION OF THE TOP - the first artefact ever generated under LP v3.4 / assessment v3.3:
  REGISTER: CLEAN. Zero clock quantities, zero forward references, zero calendar time across all 48 time bands, 12 teacher notes and the homework. Notable - this is the clause set S4's stage breached nine times under a constitution that banned it in terms.
  INTERNAL IDS: zero leaks in teacher-facing prose. No fabricated WE-n despite the chapter having NO worked examples, so P5.3's watch item did not fire - the model simply omitted the optional self-study pointer rather than inventing one.
  RULE 11 ARITHMETIC: exact. 12 handoff entries against 12 periods (1 recall / 3 reason / 8 apply); 12 assessment items against 12 goals.
  SYNTHESIS CARRIER WORKS: unit 12 carries '\"synthesis\": true'. It also lists all five sections in textbook_segments, which is harmless - unit_anchor short-circuits on a synthesis unit.
  ANCHORS: verbatim 'section 7.1'-'section 7.5', first-visit in registry order (7.1@U1, 7.2@U2, 7.3@U4, 7.4@U7, 7.5@U8), so certification check 4 will pass.
  P3: time_bands present, 4 per unit, tiling clean (validate's band checks pass).
  NUMERIC LIMITS ALL HELD: activity_title <= 12 words everywhere, teacher_notes <= 3 sentences everywhere. The opposite of S4, where 31 of 36 titles fell outside the band.
  A9: no by-label options. Only 2 MCQs in 12 items (correct at A and D), consistent with a single recall goal.

TWO FINDINGS:
  1. RULE 5 BREACH -> AMENDED (see the P1 row): units 10, 11, 12 all Problem-solving, a run of three against a cap of two. ARV-D-072's twin.
  2. CONSOLIDATION UNITS, as predicted at P5.3: units 9, 10 and 11 return to sections 7.2, 7.3 and 7.5 after 7.5 first appeared at unit 8. First-visit order is monotone so certification passes, but LP Rule 1's 'do not reorder, interleave, or re-sequence' reads against it on its face. This is the C5 ADVISORY candidate and the S4 ARV-D-088 condition (12 units over 5 sections leaves ~7 units with no new section to name). DO NOT repair it by extending period_numbers - S4 section 3.3 measured that fix and it costs a question and buys nothing.

NOT A DEFECT, recorded so it is not re-raised: the goal split is 1 recall / 3 reason / 8 apply, so section A of the assessment carries a single item. That comes from the summary's own section_goal arrays - a constructions chapter is inherently apply-heavy.

RESUME (buys the two compacts at [10, 7]): python3 genon/build_library.py mathematics vii 7"""

P1_APPEND = """

AMENDED AGAIN 2026-08-10, at C1 - LP v3.4 -> v3.5, Rule 5's consecutive-method cap.

Ch 7's top canonical put units 10, 11 and 12 all on Problem-solving, a run of three against a cap of two - ARV-D-072's twin, at the same place in the chapter and for the same reason S4 measured at its own C3. The tail genuinely converges on problem work (extended construction practice -> applying triangle geometry in a real context -> the whole-chapter synthesis), and satisfying the cap there means labelling a unit with a method its content does not support. Evidence points at the RULE, not the plan.

MUST NOT relaxes to SHOULD NOT, and the exception carries its own limits so it cannot be read as a licence: the cap yields only where the anchored sections genuinely converge, a run produced for convenience remains forbidden, the default goal->method mapping still binds, and a chapter whose every period carries one method is a defect rather than an exception. Ported in substance from mathematics-secondary LP v1.3.

Section 9: RELAXATION-ONLY, so it costs nothing - every edit only widens, nothing is tightened, no new obligation is created. Output authored under v3.4 satisfies v3.5 by construction, and the clause amended is the one ch 7 breached, so the installed top becomes compliant rather than breaching. NO RE-AUTHOR. TIMED DELIBERATELY BEFORE STEP 4 buys the compacts, so they are authored against the corrected rule instead of inheriting the breach and needing the same finding raised twice.

Artefacts: lesson_plan_constitution_v3.4_pre.txt, lp_v3.4_to_v3.5.diff, apply_s7_rule5_exception.py (guards assert exactly one MUST NOT relaxed and that A1, the register and the P3 shape are untouched).

The standing lesson, now twice-confirmed: a limit stated as a number is what live generation most often disproves - but only this one broke. S4's other numeric findings (activity_title, section_context) did NOT recur; ch 7 held every other bound this constitution states."""

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_s7_c1"))

row = state.setdefault("stages", {}).setdefault(KEY, {})
row["C1"] = {"status": "amber", "by": "Claude", "at": NOW, "comment": C1}
if "P1" in row:
    row["P1"]["comment"] = row["P1"].get("comment", "") + P1_APPEND
    row["P1"]["at"] = NOW
state["updated_at"] = NOW

STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{KEY}: C1 = amber (top authored, compacts pending); P1 appended with the v3.5 amendment")
