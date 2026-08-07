#!/usr/bin/env python3
"""Write S6 (science · middle) P1-P5 into the campaign tracker state.

Run from the repo root:
    python3 genon/out/stage_prep_science_middle/update_tracker_s6_prep.py
Restart the API afterwards, or just reload docs/testing_tracker.html.
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "science/middle"

ROWS = {
    "P1": ("pass", "Claude", """AMENDED 2026-08-07. LP constitution v2.1 -> v2.2.

A1: INPUTS 4 was 'one or more rows of {duration in minutes, period count}'; now 'exactly ONE row {duration_minutes, count}: the class-standard duration (40 min for classes VI-VII, 45 for VIII) x the period count ... handled downstream at serve time'. Rule 6's TIME statement restated as duration x count (was a sum over rows); A3 gains 'period_schedule: exactly one row - the class-standard duration x count (INPUTS 4)'. Bands are the master-plan calibration, not NCF's flat 40.

A5+A7 THE SELF-CONTAINED REGISTER: present as ONE block after VOCABULARY, bound at Rule 6 (band text) and Rule 10 (teacher notes) by reference. TWO-BAN CUT, founder ruling 2026-08-07 - ban 1 (clock quantity) and ban 3 (calendar time) port in substance; ban 2 (forward reference / completion language) is DELIBERATELY NOT PORTED. Reason, stated in the file itself rather than left silent: science middle is the one stage organised by the cognitive progression arc, an arc is taught whole or not at all, so every unit of a canonical is served with every other unit of that canonical - 'in the next unit' is never wrong for anyone and a closing completion claim is simply true. Bans 1 and 3 are untouched by that argument (duration scaling and Calendar Purge are orthogonal to the serve model) and stand in full. Consequently VOCABULARY KEEPS its positional cross-reference examples and Rule 10 keeps position-linked continuity - both of which the other stages had to strike. The one residue of ban 2 (the closing synthesis unit travels into companion plans, so it alone must be self-contained) is left to the platform brief; per testing.md section 3 the V-series is not constitutional.

Header also gained its missing stage marker: '. SCIENCE . MIDDLE STAGE . VERSION 2.2'.

No pedagogical rule changed: Rules 1-5, 7-9, Amendment A4 and every other period field byte-identical. Artefacts in genon/out/stage_prep_science_middle/ (pre-file, lp_v2.1_to_v2.2.diff, apply_s6_amendments.py - every edit asserts exactly-one occurrence)."""),

    "P2": ("pass", "Claude", """AMENDED 2026-08-07. Assessment constitution v1.3 -> v1.4.

A6-confirm: PRESENT via the subject's equivalent, not amended. Every item already carries progression_stage and coverage_handoff maps each stage to period_numbers. Added an INTEGRITY CONSTRAINTS block (the file had none) recording that ANCHORING IS DERIVED, NOT DECLARED - the platform resolves progression_stage to the units teaching that stage and anchors to the LAST of them, since an item tests the stage's whole implied LO and becomes available only when the stage completes (the 2026-08-05 anchoring ruling) - and forbidding the model emitting period_ref, phase_ref or any unit number. Same doctrine as science secondary's section_number line at v1.2. The carrier already implements it (aruvi_core/genon/carriers.py, handoff-bridged family, join_key progression_stage -> handoff_key stage_number). phase_ref appears exactly once in the file, inside the new prohibition.

A9 - ONE REMOVAL + TWO ADDITIONS, no arrangement rule. REMOVED Rule 7's item-18 prohibition ('The system MUST NOT place the correct answer at the same label across consecutive items; is_correct MUST be distributed across A-D so no single letter dominates a chapter'). ADDED, in the v1.7 wording: the option-order mandate (order carries no meaning, not yours to set, emit as authored, uneven letters are coincidence not a defect) and the by-label option-reference prohibition ('both A and B', 'none of the above'). NOT re-added and asserted absent by the edit script: 'alphabetically', 'never led with', 'first word at which they differ'.

NOT CHANGED, deliberately - the synthesis unit carries its own assessment items and brings them along on a borrow. Founder ruling 2026-08-07, taken after an audit found the installed libraries already behave this way (SS VIII ch 3 anchors items to synthesis unit 12; SS IX ch 3 to unit 16) and that C9.2 mandates it. Science middle is aligned with the platform here, not excepted, so no rule was written.

No pedagogical rule changed: Rules 1-6 and 8-10, the stage-position architecture, the guide layer and the whole A1 schema including VS-1..VS-4 are byte-identical. Artefacts: assessment_constitution_v1.3_pre.txt, assess_v1.3_to_v1.4.diff."""),

    "P3": ("pass", "Claude", """APPLIED 2026-08-07 - science middle is GROUP B, the conversion was real (unlike S1/S2/S3, which were all Group A / N-A).

Amendment A3's period schema: phases[{minutes, description}] -> time_bands[{minutes, activity}], both the array name and the description key renamed; the trailing constraint sentence follows ('bands must cover the full period from 0 to period_duration_minutes with no gaps'). Rule 6's prose follows too ('The time_bands array is the mechanism for this'). NO band_id in the target shape - the band layer left the declaration surface at compile v0.5 and ids are derived internally.

The edit script asserts no 'phases[' and no '\"phases\"' survives anywhere in the file, and that time_bands is present. roles[] is untouched (carried, ignored downstream for now per CLAUDE.md section 3)."""),

    "P4": ("pass", "Claude", """DONE 2026-08-07. CHANGELOG.md created beside BOTH amended constitutions:
- data/content/constitutions/lesson_plan/science/middle/CHANGELOG.md (v2.2 entry + a v2.1 'pre' stub)
- data/content/constitutions/assessment/science/middle/CHANGELOG.md (v1.4 entry + a v1.3 'pre' stub)

Each lists the bump with date and per-amendment rationale, including the declared deviations (the two-ban register and why ban 2 was dropped; the derived anchor in place of the reference's period_ref field; the synthesis-items ruling). Neither constitution carried an in-document version-history block, so nothing had to be lifted out; the VERSION line stays in the file and nothing in the sidecars is read at generation time."""),

    "P5": ("amber", "Claude", """RECORDED 2026-08-07 - PROVISIONAL, P5.4 OPEN (founder ruling 2026-08-02 permits signing with P5.4 open; C6 is the hard stop).

P5.1 FLOOR: accepted at the standing ratio round(0.6 x recommended_periods), no override. For the pilot chapter round(0.6 x 12) = 7, matching floor_periods_at_standard on the row.

P5.2 REGISTRY - this is the stage P5.2 was written for, and the answer is negative. Science middle has NO section registry and no cross-canonical registry of any kind. Stage count, labels and structure are derived freshly per generation and may legitimately differ between a chapter's own canonicals (founder 2026-08-07), so stages may NEVER be borrowed between canonicals. The one shared fact is the arc's terminus - Rule 1 binds every arc to the operation named in the dissolution test sentence - and that is the only thing a borrowed synthesis unit may assume. Full reasoning in docs/science_middle_stage_serve.md section 1.

P5.3 PILOT CHAPTER: science / VIII / ch 6 'Pressure, Winds, Storms, and Cyclones'. Mid-book, five clean numbered sections (6.1-6.5), summary + mapping both on disk, placeholder false, canonical_plan present, recommended_periods 12, floor 7, counts [12, 10, 7]. Counts WILL be re-derived to [12, 10, 8, 7] when the density rule lands (spec section 3), so the row is valid today but provisional against that change. Chosen over ch 5 (18 periods, 8 sections) on cost - closest shape to the certified SS IX ch 3 pilot at roughly Rs 110-145 for the library.

P5.4 TEST IDENTITY PROFILES for class VIII: OPEN. Row stays amber until they exist."""),

    "SIGN": ("blocked", "Claude", """CONSTITUTIONAL GATE CLEAR - but the C-cycle is BLOCKED on engine work, which is new for this stage and has no precedent in S1-S3. Status to be set by Kumar.

The constitutional side is done and verified: A1 lands, the register is ONE block in a declared two-ban cut, A6 anchors are present as the derived form, A9 landed as the v1.7 removal-plus-two-lines with no arrangement sentence, P3 converted (this stage really is Group B), and no cancelled amendment (A2/A3/A4) or V-rule has crept into a constitution. Full per-item note: genon/out/stage_prep_science_middle/STAGE_SIGNOFF_S6_science_middle.md.

WHY BLOCKED. S6 is the campaign's one structural exception. Science middle anchors learning units to the COGNITIVE PROGRESSION ARC, not to textbook sections, so (a) there is no section_anchor for the serve engine's arithmetic - compile.py's hard read of p['section_anchor'] would kill the first build before any certification check ran - and (b) no prefix of a canonical is a valid plan, because a stage is taught whole or not at all, which kills truncation and with it borrowing. The replacement serve law (identity / K+1 synthesis borrow / below-floor truncation with drops / above-top surrender), the forced step-2 canonical density that removes surrender inside the band, and the nine code items required before C1 are specified in docs/science_middle_stage_serve.md (new, v1.0, 2026-08-07).

Nothing re-opens: no stage carries a signed human GATE, so testing.md section 9 costs nothing here. testing.md itself needs a v2.7 note recording the S6 exception in C5-C9 before the C-cycle opens."""),
}

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_s6"))

row = state.setdefault("stages", {}).setdefault(KEY, {})
for step, (status, by, comment) in ROWS.items():
    row[step] = {"status": status, "by": by, "at": NOW, "comment": comment}
state["updated_at"] = NOW

STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{KEY}: wrote {', '.join(ROWS)}  (backup: {STATE.name}.bak_pre_s6)")
for step in ROWS:
    print(f"  {step:5} {state['stages'][KEY][step]['status']}")
