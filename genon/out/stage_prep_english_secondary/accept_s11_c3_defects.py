#!/usr/bin/env python3
"""S11 · C3 — founder ruling 2026-08-12: all eight findings ACCEPTED as authored.

Run from the repo root:
    python3 genon/out/stage_prep_english_secondary/accept_s11_c3_defects.py

C3 was already `pass` (the findings never gated it — none is structural, and the library
certified deterministically ALL PASS at C1). This records the ruling on the six defect rows
that carry the eight findings, using the register's existing `accepted` status — the same
disposition ARV-D-003, ARV-D-007, ARV-D-019 and ARV-D-112 carry. Nothing is deleted: an
accepted defect stays readable, which is what makes a rate visible later.
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()

RULING = ("\n\nACCEPTED AS AUTHORED — founder ruling 2026-08-12, at C3. No repair, no "
          "re-author, no constitution change. The finding stays on the register so the RATE "
          "stays visible across the remaining stages; it does not gate C3 and does not "
          "re-open anything.")

IDS = ["ARV-D-128", "ARV-D-129", "ARV-D-130", "ARV-D-131", "ARV-D-132", "ARV-D-133"]

NOTE = """

FOUNDER RULING 2026-08-12: ALL EIGHT FINDINGS ACCEPTED AS AUTHORED. C3 stands green on the library as it is - no repair pass, no re-author, no constitution amendment. The six defect rows (ARV-D-128 to ARV-D-133) are marked `accepted` rather than deleted, so the rate remains readable when S9 and S10 meet the same caps.

ONE THING TRAVELS FORWARD RATHER THAN CLOSING HERE: ARV-D-132 (the synthesis unit listing U15's draft in `materials`) is accepted as an authoring defect, but C8 inspects exactly that transition - p10's ten units into the borrowed U17 - so it will be read again there on its merits as a SERVE question rather than an authoring one. Acceptance here is not a finding at C8."""


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s11_accept"))

    seen = set()
    for d in state["defects"]:
        if d.get("id") in IDS:
            assert d["status"] == "open", f"{d['id']} is {d['status']}, expected open"
            d["status"] = "accepted"
            d["closed"] = NOW
            d["at"] = NOW
            d["evidence"] = d["evidence"] + RULING
            seen.add(d["id"])
    missing = set(IDS) - seen
    assert not missing, f"not found on the register: {missing}"

    c3 = state["combos"]["english/secondary"]["C3"]
    assert c3["status"] == "pass"
    c3["comment"] = c3["comment"] + NOTE
    c3["at"] = NOW
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"C3 pass (unchanged) · {len(seen)} defects -> accepted · {NOW}")


if __name__ == "__main__":
    main()
