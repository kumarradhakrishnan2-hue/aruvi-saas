#!/usr/bin/env python3
"""S11 · english · secondary — P5.4 closed, so P5 goes amber -> pass (2026-08-12).

Run from the repo root:
    python3 genon/out/stage_prep_english_secondary/update_tracker_s11_p5_closed.py
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/secondary"

CLOSE = """

--- P5.4 CLOSED 2026-08-12, and P5 therefore goes GREEN. ---

The three test identities hold ENGLISH IX teaching profiles, set up by Kumar through the app's own first-run / profile flow rather than by hand-editing JSON (the setup is itself the live check of that flow). Verified on disk at data/readiness/{u}/{u}/profile.json:

SECTIONS ARE DISJOINT - kumar1 9A, kumar2 9D, kumar3 9F. That is what makes X1's tenancy evidence unambiguous: a section that appears under two identities cannot prove which tenant a served plan belongs to.

THE MIXED DURATION IS ON THE RIGHT IDENTITY - kumar3 carries durations [50, 60] with ppw_by_duration {50: 5, 60: 1}, anchor 50, periods_per_week 6. Section 4 assigns C6's mixed-duration matrix to kumar3, so the matrix now has something real to draw on rather than a synthetic row: a week of five 50-minute sittings and one 60. kumar1 and kumar2 are 50-only at ppw 6, which is the class standard and the control.

BUDGET is 'weeks' x 27 on all three, consistent across the identities so a difference at C6 cannot come from the budget.

TENANCY SHAPE INTACT - three separate {tenant}/{user}/ directories, tenant_id == user_id on each, no cross-writes.

LEFTOVER HISTORY, ACCEPTED - the profiles also still carry Social Sciences VIII/IX, Science VIII/IX, Mathematics III/VII/IX and TWAU V from S1-S8. The template's 'nothing left over from an earlier stage' was WAIVED by the founder at S6 (2026-08-07) and the waiver holds here for the same reasons: the residue is harmless (it describes a teacher who teaches more than one thing, which is the real ICP anyway), it touches no english-IX key, and clearing it would cost a fresh pass through the first-run flow for no evidence gained.

S11 NOW ENTERS ITS C-CYCLE WITH A CLEAN P5 - the fourth stage to do so, after S6, S8 and S5. Nothing is owed and no gate is carried."""


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s11_p5"))
    row = state["stages"][KEY]["P5"]
    assert row["status"] == "amber", f"expected amber, found {row['status']}"
    row["status"] = "pass"
    row["at"] = NOW
    row["comment"] = row["comment"] + CLOSE
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"tracker updated · {KEY} · P5 amber -> pass · {NOW}")


if __name__ == "__main__":
    main()
