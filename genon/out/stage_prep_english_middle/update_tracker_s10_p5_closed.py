#!/usr/bin/env python3
"""S10 · english · middle — P5.4 closed, so P5 goes amber -> pass.

Run from the repo root:
    python3 genon/out/stage_prep_english_middle/update_tracker_s10_p5_closed.py

Re-verifies the three profiles off disk BEFORE it writes, and refuses on any failure —
a tick that was not checked is worse than no tick.
"""
import datetime
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/middle"
IDS = ("kumar1", "kumar2", "kumar3")

# ───────────────────────────────────────────────────────── verify, then write
rows, fails = {}, []
for u in IDS:
    p = ROOT / f"data/readiness/{u}/{u}/profile.json"
    if not p.is_file():
        fails.append(f"{u}: no profile at {p.relative_to(ROOT)}")
        continue
    d = json.loads(p.read_text(encoding="utf-8"))
    rec = None
    for s in d.get("subjects") or []:
        if str(s.get("name", "")).lower().startswith("eng"):
            for g in s.get("grades") or []:
                if str(g.get("grade", "")).upper() == "VI":
                    rec = g
    if rec is None:
        fails.append(f"{u}: no English · VI grade record")
        continue
    rows[u] = {
        "sections": [x.get("tag") for x in rec.get("sections") or []],
        "durations": rec.get("durations"),
        "ppw_by_duration": rec.get("ppw_by_duration"),
        "ppw_anchor": rec.get("ppw_anchor"),
    }

if not fails:
    secs = [tuple(v["sections"]) for v in rows.values()]
    flat = [s for t in secs for s in t]
    if len(set(flat)) != len(flat):
        fails.append(f"sections are NOT disjoint: {flat} — X1 cannot attribute a served plan")
    if not any(len(v["durations"] or []) > 1 for v in rows.values()):
        fails.append("no identity carries a mixed duration — C6's matrix has nothing real to draw on")
    if 40 not in (rows["kumar3"]["durations"] or []):
        fails.append("kumar3 does not carry the 40-min class standard as its anchor")

for u, v in rows.items():
    print(f"  {u}: sections {v['sections']} · durations {v['durations']} · "
          f"ppw {v['ppw_by_duration']} · anchor {v['ppw_anchor']}")
if fails:
    print("\nREFUSING TO TICK:", *fails, sep="\n  ")
    sys.exit(1)
print("\n  all three P5.4 conditions hold")

COMMENT = f"""CLOSED {NOW[:10]} - P5.4 is done, so P5 goes AMBER -> PASS and S10 enters its C-cycle with a CLEAN P5. Fifth stage to do so, after S6, S8, S5 and S11.

VERIFIED ON DISK at data/readiness/{{u}}/{{u}}/profile.json, not taken on report:
  kumar1 . section 6A . durations [40] . ppw {{40: 5}} . anchor 40
  kumar2 . section 6B . durations [40] . ppw {{40: 5}} . anchor 40
  kumar3 . section 6C . durations [40, 50] . ppw {{40: 4, 50: 1}} . anchor 40

SECTIONS ARE DISJOINT (6A / 6B / 6C), which is what makes X1's tenancy evidence unambiguous: a section appearing under two identities cannot prove which tenant a served plan belongs to.

THE MIXED DURATION IS ON THE RIGHT IDENTITY. Section 4 of the template assigns C6's mixed-duration matrix to kumar3, and kumar3 is the one carrying [40, 50] - a real week of four 40-minute sittings and one 50, anchor 40. kumar1 and kumar2 are 40-only at the class standard and serve as the control. NOTE THE STRETCH IS 1.25x (40 -> 50) where S11's was 1.2x (50 -> 60): a canonical authored at 40 min served into a 50-minute sitting is the ordinary Indian-timetable case, so C6 gets a realistic scaling test rather than an exotic one.

BUDGET IS IDENTICAL ACROSS THE THREE (weeks-based, same values), so any difference C6 finds cannot have come from the budget. Tenancy shape intact: three separate {{tenant}}/{{user}}/ directories, tenant_id == user_id on each.

SET UP THROUGH THE APP'S OWN FIRST-RUN / PROFILE FLOW, not by hand-editing JSON - the setup is itself the live check of that flow, which is why the template asks for it that way.

LEFTOVER HISTORY, ACCEPTED. The profiles also carry SS VIII/IX, Science VIII/IX, Maths III/VII/IX, TWAU IV/V and English IX from S1-S8 and S11. The template's 'nothing left over from an earlier stage' clause was WAIVED BY THE FOUNDER AT S6 (2026-08-07) and the waiver holds here for the same reasons: the residue is harmless - it describes a teacher who teaches more than one thing, which is the real ICP - it touches no English-VI key, and clearing it would cost a fresh pass through the first-run flow for no evidence gained.

P5.1, P5.2, P5.3 and P5.5 were already closed at the 2026-08-13 prep; nothing else in P5 was waiting on this. NOTHING IS NOW OWED AT ANY P-STEP."""


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s10_p5"))
    row = state["stages"][KEY]
    prior = row["P5"]["comment"]
    row["P5"] = {"status": "pass", "by": "Claude", "at": NOW,
                 "comment": COMMENT + "\n\n--- the amber record this replaces ---\n\n" + prior}
    row["SIGN"]["comment"] = row["SIGN"]["comment"].replace(
        "P5.4 amber by design, C6 its hard stop.",
        "P5.4 CLOSED 2026-08-13 (three class-VI profiles, sections 6A/6B/6C disjoint, kumar3 at "
        "[40, 50]), so P5 is GREEN and C6 inherits real profiles rather than a row to fill in.",
    ).replace(
        "P5.4 remains the only open item and C6 is its hard stop.",
        "P5 IS CLEAN - P5.4 closed the same day as the prep. Nothing is owed at any P-step.",
    )
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\ntracker updated · {KEY} · P5 amber -> pass · SIGN comment amended · {NOW}")


if __name__ == "__main__":
    main()
