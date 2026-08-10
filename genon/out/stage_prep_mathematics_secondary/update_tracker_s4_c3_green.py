#!/usr/bin/env python3
"""S4 · C3 closes — ARV-D-078 and ARV-D-079 accepted, cell goes green (2026-08-09, founder).

Same treatment S3 received on 2026-08-06: nothing is re-read and nothing is regenerated; the
founder accepts the two remaining defects rather than remedy them, so the cell is green and the
register carries the reasons. Every other defect on this stage was genuinely repaired.

Run from the repo root:
    python3 genon/out/stage_prep_mathematics_secondary/update_tracker_s4_c3_green.py
"""
import datetime
import json
import pathlib
import shutil
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()

A078 = f"""ACCEPTED by founder {NOW[:10]}, not remedied. std item 1 is anchored to 4.1 but
demands the full algebraic argument, which is 4.3's LO and what item 5 already asks — so the
standard's assessment carries one mis-owned, duplicated question.

Standing consequence, to be read whenever this chapter's assessment is discussed: the STANDARD
canonical (and only the standard) asks the consecutive-square proof twice, at items 1 and 5. A
teacher served at X >= 13 sees both. p12 and p09 do NOT have this — their 4.1 items stay at
conjecture, which is what 4.1's LO asks — so it never reaches a class served below X=13.

Not remedied because the alternatives are worse: a hand-written replacement is a draft on an
uncalibrated model, and a re-author to fix one duplicated question would discard a verified-clean
library for a fresh draw on nine defect classes that recurred in both prior generations. The
correct fix arrives free at the next re-author this chapter has for another reason."""

A079 = f"""ACCEPTED by founder {NOW[:10]}, not remedied. p12 item 9 is tagged Analysis on an
Application LO and carries an off-menu format_type ('Procedure / argument evaluation'), so its
OPEN_TASK is unlicensed by Rule 5. Assessment v1.2's synthesis clause deliberately does not
rescue it — the item anchors 4.6, not the synthesis entry.

Accepted because the cost is bounded and the rule is now correctly stated. Rule 6's reasoning
floor is met on p12 without this item (it carries two ECRs), so nothing about the assessment's
shape depends on the mis-format; what the teacher gets is a sound factorisation task delivered
as an open task rather than as NUM/SCR. Tag and format must move together, so remedying it means
re-authoring the item — the same trade as ARV-D-078 and refused for the same reason.

What S7/S8 inherit is the part that matters: Rule 4's reading guide and Rule 5's mapping were
already right, so this is a generation defect, and the amendment pass deliberately did NOT widen
a rule to make it disappear."""

C3_HEADER = f"""[GREEN BY FOUNDER RULING, {NOW[:10]}. The rule table below is UNCHANGED and still
records every fail as found. Of the seventeen defects it opened: THIRTEEN WERE GENUINELY
REPAIRED at zero cost (both S1s — the wrong verified answer and its leaked deliberation — plus
the register, positional continuity, the method label, 27 internal ids, period_numbers, c_code,
16 descriptions, the Rule 8 clause, 52 empty guide fields, and the over-length labels); THREE
BECAME AMENDMENTS because the evidence pointed at the rule (LP v1.3's method-cap exception and
two widened word-count bands; assessment v1.2's synthesis OPEN_TASK clause, which resolved a
standing contradiction with architecture v2.0 that most of the corpus sits in); and ONE was
accepted earlier (ARV-D-081, option-by-letter guides). The two below are now accepted, so the
cell is green and the register carries the reasons.
  · ARV-D-078 (S2) ACCEPTED — the standard asks the consecutive-square proof twice, at items 1
    and 5. Reaches a class only at X >= 13; p12 and p09 are correct.
  · ARV-D-079 (S3) ACCEPTED — p12 item 9's Analysis tag on an Application LO leaves its
    OPEN_TASK unlicensed. Rule 6's floor is met without it; the rule was already right and was
    deliberately not widened to absorb it.
NO RE-AUTHOR was performed and none is owed: both amendments are relaxation-only and the
installed library was verified compliant with LP v1.3 / assessment v1.2 clause by clause
(testing.md §9's new carve-out, written from this stage). Library state at sign-off:
deterministic certification ALL PASS · 25/25 determinate answers re-derived from their stems ·
0 internal ids · 0 register hits · 0 empty guide fields · 0 non-verbatim descriptions · c_code
identical across all three canonicals · serve sweep unchanged at every X from 6 to 17.]"""

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_c3_green"))
by_id = {d["id"]: d for d in state["defects"]}

for did, note in (("ARV-D-078", A078), ("ARV-D-079", A079)):
    d = by_id[did]
    d["status"] = "accepted"
    d["closed"] = NOW
    d["at"] = NOW
    d["owner"] = "founder"
    d["resolution"] = note

cell = state["combos"]["mathematics/secondary"]["C3"]
cell["status"] = "pass"
cell["at"] = NOW
cell["comment"] = C3_HEADER + "\n\n" + cell["comment"]

state["updated_at"] = NOW
STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")

ds = [d for d in state["defects"] if d.get("combo") == "mathematics/secondary"]
combo = state["combos"]["mathematics/secondary"]
print("C3 = pass (green by founder ruling) · 078 + 079 accepted")
print("S4 defects:", dict(Counter(d["status"] for d in ds)))
print("S4 steps  :", {k: v.get("status") for k, v in combo.items()
                      if isinstance(v, dict) and k.startswith("C")})
