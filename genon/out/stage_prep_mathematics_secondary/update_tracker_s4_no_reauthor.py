#!/usr/bin/env python3
"""S4 · §9 relaxation ruling — the re-author is CANCELLED (2026-08-09, founder).

Corrects the previous script, which re-opened C1/C2/C3 and closed ARV-D-078/079 on the
assumption of a regeneration that is not happening. Both were wrong and are reversed here.

The ruling: LP v1.2 -> v1.3 and assessment v1.1 -> v1.2 are RELAXATION-ONLY. Every edit widens
or permits; nothing tightens. Output authored under the stricter pair satisfies the looser pair
by construction, and the amended clauses are the very ones ch 4 breached — so the installed
library became MORE compliant, not less. testing.md §9 gains this as a standing carve-out.

Run from the repo root:
    python3 genon/out/stage_prep_mathematics_secondary/update_tracker_s4_no_reauthor.py
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()

RULING = f"""[§9 RELAXATION RULING {NOW[:10]} — THE RE-AUTHOR IS CANCELLED. This supersedes the
 re-open note above, which was wrong.
 WHY: both amendments are relaxation-only (method-cap exception · activity_title 10-13 -> 6-13 ·
 section_context 10-12 -> 6-12, upper bound untouched · OPEN_TASK extended to a synthesis LO).
 Nothing tightened, no new obligation. A relaxation cannot invalidate output authored under the
 stricter text — and here the amended clauses are precisely the ones ch 4 breached, so the
 installed library became MORE compliant the moment the versions were bumped.
 AND THE LIBRARY WAS ALREADY REPAIRED: the 31 internal ids, the S1 wrong answer, the register,
 the descriptions, the guide shape, period_numbers and c_code are all fixed and verified on
 disk, and the counts were restored to 15/12/9 with the end-of-chapter section_anchor fix. A
 re-author would have discarded verified-clean output for a fresh draw. The two prior
 generations of this chapter show what that draw looks like: EVERY defect class recurred, and
 internal-id leakage alone went 0 -> 31 between them. Regeneration is a lottery; the constitutional
 fixes are S4-type and will show up in FUTURE authoring, which is where they were always aimed.
 CLAUSE-BY-CLAUSE COMPLIANCE CHECK of the installed library against LP v1.3 / assessment v1.2,
 which is what §9's carve-out requires in place of a re-author:
   activity_title 6-13 words ....... 0 of 36 outside — PASS
   section_context 6-12 words ...... 0 of 25 outside — PASS
   Rule 5 P1 method runs ........... 4 runs of 3-4, each on sections that genuinely converge
                                     (std's run of four covers 4.7 -> 4.8 -> 4.8 -> synthesis) — PASS
   Rule 5 OPEN_TASK licensing ...... std item 14 (section_ref 'synthesis') LICENSED by the new
                                     clause — the very item that provoked it. p12 item 9 NOT
                                     licensed — ordinary defect, stays open (ARV-D-079).
 COST AVOIDED: ~Rs.111 plus a full re-declaration of every repair.
 C1/C2/C3 return to their prior verdicts; C3 stays FAIL on the two open items below.]"""

D078 = f"""RE-OPENED {NOW[:10]}. The previous entry closed this 'by the re-author' — there is no
re-author (see the §9 relaxation ruling), so the defect stands exactly as C3 found it: std item 1
is owned by 4.1, whose LO is 'verify and conjecture the invariant', but the item demands the full
algebraic argument, which is 4.3's LO and what item 5 already asks. No rule was wrong; the model
did not follow one. THREE WAYS OUT, founder's call: (a) accept — the item is a good ECR, it is
merely mis-owned and duplicated, and the cost is one redundant question; (b) install the drafted
replacement stem, which stops at conjecture and restores 4.1's own LO ('Test the pattern on two
further triples ... you are not asked to prove it') — a hand-written item on an uncalibrated
model, so it needs explicit founder sign-off; (c) carry it to the next natural re-author of this
chapter, whenever one is triggered for another reason. Recommend (a) for now and revisit at the
human gate: it is one duplicated question and nothing downstream depends on it."""

D079 = f"""RE-OPENED {NOW[:10]}, and it is the one residue of the amendment pass. p12 item 9 is
tagged Analysis on an Application LO ('factorise a quadratic by finding two integers whose sum is
p and product is q'), and carries an off-menu format_type 'Procedure / argument evaluation'.
Rule 4's reading guide maps 'factorise' to Application and Rule 5 maps Application to NUM or SCR,
so the OPEN_TASK is unlicensed — and assessment v1.2's new synthesis clause does NOT rescue it,
because this item anchors 4.6, not the synthesis entry. The compliance check confirms it: std's
item 14 is licensed, this one is not. Tag and format must move together, so a correct fix is a
re-authored item, not a field edit. Options: accept for this pilot (p12 already carries two ECRs,
so Rule 6's reasoning floor is met without it), or re-author the single item under founder
sign-off. Recommend accept-and-record: it is one compact's one item, and the rule it breaches is
now correctly stated, which is what S7/S8 inherit."""

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_no_reauthor"))
by_id = {d["id"]: d for d in state["defects"]}

for did, note in (("ARV-D-078", D078), ("ARV-D-079", D079)):
    d = by_id[did]
    d["status"] = "open"
    d["closed"] = None
    d["at"] = NOW
    d["owner"] = "founder"
    d["resolution"] = note

combo = state["combos"]["mathematics/secondary"]
combo["provenance"]["reopened_by"] = (
    "CANCELLED — testing.md §9 relaxation carve-out (2026-08-09): both amendments are "
    "relaxation-only, the installed library was verified compliant clause by clause, and no "
    "re-author is required. Provenance versions below are the ones the library is certified "
    "against."
)
combo["provenance"]["reauthor_required"] = False
combo["provenance"]["compliance_checked_at"] = NOW

for step, verdict in (("C1", "pass"), ("C2", "pass"), ("C3", "fail")):
    cell = combo.get(step)
    if isinstance(cell, dict):
        cell["status"] = verdict
        cell["at"] = NOW
        cell["comment"] = cell.get("comment", "") + "\n\n" + RULING

state["updated_at"] = NOW
STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")

from collections import Counter
ds = [d for d in state["defects"] if d.get("combo") == "mathematics/secondary"]
print("re-author CANCELLED · C1 pass · C2 pass · C3 fail (2 open items)")
print("S4 defect statuses:", dict(Counter(d["status"] for d in ds)))
print("open:", [d["id"] for d in ds if d["status"] == "open"])
