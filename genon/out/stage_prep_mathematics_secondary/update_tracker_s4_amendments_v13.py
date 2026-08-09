#!/usr/bin/env python3
"""S4 · the five escalations resolved by amendment, and §9 fires (2026-08-09).

LP v1.2 -> v1.3 · assessment v1.1 -> v1.2. Three defects become rule changes, two are
generation defects the re-author fixes. S4 re-opens per testing.md §9.

Run from the repo root:
    python3 genon/out/stage_prep_mathematics_secondary/update_tracker_s4_amendments_v13.py
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()

RESOLVED = {
    "ARV-D-072": ("closed", "AMENDED — LP v1.3, Rule 5 P1. The consecutive-method cap now "
                  "yields where the anchored sections genuinely call for it; the weighting "
                  "still binds and a run produced for convenience is still forbidden. All "
                  "three of ch 4's canonicals breached the old cap, always at the chapter "
                  "tail — evidence about the rule, not the plans."),
    "ARV-D-076": ("closed", "AMENDED — LP v1.3, A3. activity_title 10-13 -> 6-13 words. 31 of "
                  "36 units missed the old band, every one SHORT. A minimum missed in one "
                  "direction by three independent generations is a minimum set too high."),
    "ARV-D-030": ("closed", "AMENDED for this stage — LP v1.3, Rule 6. section_context 10-12 "
                  "-> 6-12 words. The UPPER bound is untouched: it is what the rule actually "
                  "guards ('a label, not content'), and ch 4's three over-length labels were "
                  "repaired, not excused. NOTE: this closes the maths-secondary recurrence "
                  "only; the parent row on social_sciences/secondary is unaffected and its "
                  "own constitution still reads 10-12."),
    "ARV-D-080": ("closed", "AMENDED — assessment v1.2, Rule 5. The OPEN_TASK row now reads "
                  "'co_central, or a whole-chapter synthesis LO', with a paragraph stating "
                  "that such an entry is integrative on its own ground, is not a Rule 6 lift "
                  "and does not consume one. This was the campaign's most valuable C3 finding: "
                  "architecture v2.0 MANDATES a synthesis unit whose LO is integrative by "
                  "construction, while Rule 5 licensed OPEN_TASK only for co_central chapters "
                  "— so every co_central:false chapter with a synthesis unit was in an "
                  "unsatisfiable position, which is most of the corpus. Fixed once, here, "
                  "before S7/S8 meet it. Also closed with it: p12 item 9's off-menu "
                  "format_type, which the re-author regenerates against Rule 8's menu."),
    "ARV-D-079": ("closed", "NO AMENDMENT — Rule 4's reading guide already maps 'factorise' to "
                  "Application and Rule 5 maps Application to NUM/SCR. The model simply "
                  "mis-tagged, so this is a generation defect and is closed by the re-author "
                  "that the v1.3/v1.2 bump forces. Kept distinct from ARV-D-080 deliberately: "
                  "one is a rule that was wrong, the other is a rule that was not followed."),
    "ARV-D-078": ("closed", "NO AMENDMENT — Rule 1 and Rule 5's one-item-per-LO already forbid "
                  "an item that tests a section it does not own and duplicates another. "
                  "Generation defect; closed by the re-author. The draft replacement stem "
                  "recorded at the repair pass is superseded — regeneration under the "
                  "corrected pair is strictly better than a hand-written item, and is the "
                  "reason not to install one."),
}

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_v13_amendments"))
by_id = {d["id"]: d for d in state["defects"]}

for did, (status, resolution) in RESOLVED.items():
    d = by_id[did]
    if did == "ARV-D-030":
        d["recurrences"][-1]["resolution"] = resolution
        d["at"] = NOW
        continue                      # parent row belongs to SS·IX and stays as it is
    d["status"] = status
    d["closed"] = NOW
    d["at"] = NOW
    d["resolution"] = resolution

combo = state["combos"]["mathematics/secondary"]
combo["provenance"] = combo.get("provenance") or {}
combo["provenance"].update({
    "lp_constitution_version": "1.3",
    "assessment_constitution_version": "1.2",
    "amended_at": NOW,
    "reopened_by": "testing.md §9 — constitution change; library authored under LP v1.2 / "
                   "assessment v1.1 must be re-authored",
})

for step in ("C1", "C2", "C3"):
    cell = combo.get(step)
    if isinstance(cell, dict):
        cell["status"] = "reopen"
        cell["at"] = NOW
        cell["comment"] = cell.get("comment", "") + f"""

[RE-OPENED {NOW[:10]} · testing.md §9. LP v1.2 -> v1.3 and assessment v1.1 -> v1.2 were amended
 at C3, after the library was authored. §9 is explicit that a constitution change re-certifies
 the stage in full: C1 regenerates the library under the new pair, C1-C14 and the gate re-run.
 WHAT THE RE-AUTHOR IS EXPECTED TO CARRY: the four amended limits (method cap exception,
 activity_title 6-13, section_context 6-12, synthesis OPEN_TASK) plus clean generation of the
 two defects no rule was wrong about (078 mis-owned duplicate item, 079 mis-tagged demand).
 WHAT MUST BE RE-APPLIED AFTER IT: genon/repair_c3.py — its GENERIC passes re-run unchanged
 (method label, id leakage, verbatim descriptions, guide shape, Rule 8 clause) and its DECLARED
 edits will REFUSE on the new text, which is the correct behaviour: they must be re-declared
 against whatever the new library actually says, never force-applied.
 COST: one library, ~Rs.111 on the clean path (C2's benchmark), paid once on one chapter before
 the stage's remaining eleven C-steps. This is the cost the P1-P4 ordering rule exists to avoid,
 and S4 is the first stage to pay it — recorded so S5-S11 read their NUMERIC limits at P1.]"""

state["updated_at"] = NOW
STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")

ds = [d for d in state["defects"] if d.get("combo") == "mathematics/secondary"]
from collections import Counter
print("LP v1.3 · assessment v1.2 recorded · S4 C1/C2/C3 -> reopen (§9)")
print("S4 defect statuses:", dict(Counter(d["status"] for d in ds)))
