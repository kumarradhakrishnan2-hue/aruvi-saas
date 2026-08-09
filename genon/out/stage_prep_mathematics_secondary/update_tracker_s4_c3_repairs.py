#!/usr/bin/env python3
"""S4 · C3 follow-up — the two leaked-deliberation repairs and the founder ruling on
ARV-D-081 (2026-08-09).

Three register changes, all downstream of the C3 that ran earlier the same day:

  ARV-D-084  CLOSED, genuinely fixed — maths IX ch 4 top item 4's wrong verified answer.
  ARV-D-085  OPENED and CLOSED in the same pass — science IX ch 8 p07 item 4's broken
             student-facing stem, found by the corpus sweep off 084, on a stage already
             green at C3.
  ARV-D-081  ACCEPTED by founder — guides that name options by letter; not remedied.

Also records the C5 tooling gap the sweep exposed and re-states C3 as fail-with-repairs
rather than flipping it green: two defects were repaired, fifteen remain open.

Run from the repo root:
    python3 genon/out/stage_prep_mathematics_secondary/update_tracker_s4_c3_repairs.py
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()

REPAIR_TOOL = "genon/repair_leaked_deliberation.py v1.0"

CLOSE_084 = f"""CLOSED {NOW[:10]} — repaired in place at zero cost by {REPAIR_TOOL}.
expected_answer 8(3m - 2n)^2 -> 8(3m - n)^2, and method_one_line rewritten without the
model's 'wait, verify... Let me re-check' aside. The repaired value is the one the file was
ALREADY carrying in two of its three places (the method line's own conclusion, and the
guide's inclusivity note 'verify by expanding 8(3m-n)^2'), so nothing pedagogical was
invented and the stem, identity and guide are untouched. Every edit is declared field-by-field
in genon_canonical.repairs[]; backup at backup/answer_repair/. Regression test:
genon/out/answer_checks/mathematics_ix_ch04_check.py — 25 determinate checks over 19 items
across all three canonicals, 0 WRONG."""

D085_TITLE = ("science IX ch 8 p07 item 4(b): the model's self-correction shipped inside the "
              "STUDENT-FACING stem, and the key resolved the part to the atom it was given")

D085_EVIDENCE = """FOUND 2026-08-09 by the corpus-wide sweep that followed ARV-D-084: all 16
installed canonical files scanned for self-correction markers in every human-facing text field.
Two hits, both item 4 (coincidence). This is the second.

The stem read: '(b) A second atom has the symbol 27-13-Al. Write the full nuclide notation for
an atom of the same element that has 14 neutrons instead of 14 - wait, this atom has 14
neutrons. Calculate its mass number and write the corrected nuclide notation.'

Two failures, not one. The visible one is the deliberation in text a STUDENT reads. The one
underneath is that the answer key had settled the stumble the wrong way - expected_elements[1]
resolved (b) to 27-13-Al, 'same as the given atom', i.e. the question hands the student its own
answer. The phrase 'the corrected nuclide notation' shows the model was reaching for an
isotope and lost the thread.

WHAT MAKES IT A CAMPAIGN FINDING, not just a defect: science/secondary is green at C3 and at
every one of its 14 C-steps, and its C3 comment says in terms 'ch_08_canonical.json (TOP, 12
units) and ch_08_canonical_p07.json (COMPACT, 7 units) ... Both files in every row.' So this
file WAS read rule-by-rule and the broken stem was not seen - because it is not a rule
violation, it is a wrecked sentence, and a reader checking rules does not see it. A regex over
the text fields catches it in milliseconds at zero cost and nothing runs one (see the C5
tooling note).

CLOSED in the same pass by founder ruling 2026-08-09: option 1 of three - restore the isotope
teaching point rather than paper over the stumble. 15 neutrons, A = Z + n = 13 + 15 = 28,
notation 28-13-Al, keyed as an isotope of the given atom. The LO, section anchor, competency
and parts (a) and (c) are untouched. Repaired by """ + REPAIR_TOOL + """, declared in
genon_canonical.repairs[], backup at backup/answer_repair/."""

D081_ACCEPT = f"""ACCEPTED by founder {NOW[:10]}, not remedied. Guides that refer to an option
by its letter ('confirm option A') in 4 places across the two files; STEP 6's label-reference
guard reads options[] only, not the guide, and caught 1 of 4.

Founder reasoning, recorded because it sets a precedent: the post-hoc re-ordering in STEP 6 is
itself what makes a letter reference fragile, and the answer is not to write yet another
constitutional rule telling the model not to mention options - the rule surface is already the
thing under strain, and naming option positions at all keeps position salient to a model that
should never reason about it (the same argument that struck the arrangement sentence at
assessment v1.7). The occurrence is rare and a teacher reading a guide that says 'option A'
beside an item whose correct answer is marked C will resolve it correctly. Accepted as a known,
bounded cosmetic defect.

NOT accepted, and to be kept separate: std item 7's guide names the WRONG option as correct on
the merits ('confirm option A' where C is correct on re-derivation). That is a content error
wearing a letter reference, not an instance of this defect. It rides with the item-level
content debt and is unaffected by this ruling."""

C5_TOOLING = f"""C5 TOOLING GAP, added {NOW[:10]} off ARV-D-084/085: certification has no check
for MODEL SELF-CORRECTION surviving into a shipped field. Two of 16 installed canonicals carry
one - maths IX ch4 top item 4 (method_one_line, teacher-facing) and science IX ch8 p07 item 4
(question_text, student-facing) - and a human rule-by-rule C3 caught the first and missed the
second, because it is not a rule violation. Markers observed: 'wait', 'let me re-check',
'let me verify', 'actually,', 'correction:'. A regex over question_text, expected_answer,
method_one_line, task, scaffold, expected_elements, look_for and the guide blocks costs
nothing and runs at --certify-only. Recommended to land beside register_scan."""

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_c3_repairs"))

by_id = {d["id"]: d for d in state["defects"]}

# --- ARV-D-084: closed, genuinely fixed -------------------------------------------------
d = by_id["ARV-D-084"]
d["status"] = "closed"
d["closed"] = NOW
d["at"] = NOW
d["resolution"] = CLOSE_084

# --- ARV-D-081: accepted by founder -----------------------------------------------------
d = by_id["ARV-D-081"]
d["status"] = "accepted"
d["closed"] = NOW
d["at"] = NOW
d["resolution"] = D081_ACCEPT

# --- ARV-D-085: opened and closed in the same pass ---------------------------------------
if "ARV-D-085" not in by_id:
    state["defects"].append({
        "id": "ARV-D-085",
        "combo": "science/secondary",
        "step": "C3",
        "severity": "S1",
        "owner": "founder",
        "status": "closed",
        "opened": NOW,
        "closed": NOW,
        "at": NOW,
        "title": D085_TITLE,
        "evidence": D085_EVIDENCE,
        "resolution": f"Repaired in place by {REPAIR_TOOL} under founder ruling 2026-08-09; "
                      f"declared in genon_canonical.repairs[].",
    })

# --- the C3 cell: still fail, now annotated with the repairs ------------------------------
c3 = state["combos"]["mathematics/secondary"]["C3"]
c3["comment"] = c3["comment"] + f"""

[FOLLOW-UP {NOW[:10]}, same day. TWO DEFECTS REPAIRED IN PLACE, THE CELL STAYS RED.
 · ARV-D-084 CLOSED, genuinely fixed - the wrong verified answer and the deliberation beside
   it, by {REPAIR_TOOL}. The value adopted is the one the file already carried in its own
   method line and guide, so nothing was invented and no rupee was spent. Regression test:
   genon/out/answer_checks/mathematics_ix_ch04_check.py, 25 checks, 0 WRONG.
 · ARV-D-081 ACCEPTED by founder, not remedied - option-by-letter references in guides. The
   post-hoc re-order is what makes them fragile; a further constitutional rule about options
   would cost more than the defect. Std item 7's guide naming the wrong option on the MERITS
   is explicitly excluded from the acceptance and stays open with the item-content debt.
 · Fifteen defects remain open. C3 = fail stands.
 · The sweep this C3 triggered found ARV-D-085 on a DIFFERENT and already-green stage
   (science/secondary), which is the more important finding: a human rule-by-rule read does
   not catch a wrecked sentence, because it is not a rule violation.
 · TEMPLATE CHANGE: testing.md -> v2.9. C3 gains a maths-only sub-check requiring every
   determinate answer to be re-derived FROM THE STEM (genon/extract_determinate.py writes the
   worksheet). Scoped to S4/S7/S8 - the sweep confirmed science and social_sciences ship zero
   items with an expected_answer, so the other eight stages record it N/A.]"""
c3["at"] = NOW
c3["artefacts"] = [
    "docs/testing_artefacts/c3_mathematics_ix_ch04.md",
    "genon/out/answer_checks/mathematics_ix_ch04_check.py",
]

# --- the C5 tooling note ------------------------------------------------------------------
notes = state.setdefault("tooling_notes", [])
notes.append({"at": NOW, "step": "C5", "note": C5_TOOLING})

state["updated_at"] = NOW
STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")

opened = sum(1 for d in state["defects"] if d.get("status") == "open")
print(f"ARV-D-084 closed (fixed) · ARV-D-085 opened+closed (science/secondary) · "
      f"ARV-D-081 accepted · C3 annotated, still fail · C5 tooling note recorded")
print(f"{opened} defects open campaign-wide · "
      f"backup {STATE.with_suffix('.json.bak_pre_c3_repairs').name}")
