#!/usr/bin/env python3
"""S9 — MOVE C1/C2/C3 from the `stages` scope to `combos`, where the tracker reads them.

    python3 genon/out/stage_prep_english_preparatory/fix_s9_c_steps_scope.py

WHY. `docs/testing_tracker.html` renders two different matrices from two different scopes:

    stages table   ->  cellHtml("stages", st.key, P-step)     P1 P2 P3 P4 P5 SIGN
    C-cycle table  ->  cellHtml("combos", comboKey(c), C-step)  C1 ... C14

`comboKey(c)` is `c[0]+"/"+c[1]`, which is the SAME string as the stage key
("english/preparatory") — so writing a C-step under `stages` produces a state file that looks
correct in every way except that nothing renders it. english/middle is the shape to copy:
its C1–C14 sit under `combos`, its P1–SIGN under `stages`.

This moves the three entries, verbatim, and leaves the P-steps and the provenance alone.
Idempotent: re-running after the move is a no-op.
"""
import datetime
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/preparatory"
CSTEPS = ("C1", "C2", "C3")

state = json.loads(STATE.read_text(encoding="utf-8"))
stage_row = state.setdefault("stages", {}).setdefault(KEY, {})
combo_row = state.setdefault("combos", {}).setdefault(KEY, {})

moved, already = [], []
for c in CSTEPS:
    if c in stage_row:
        combo_row[c] = stage_row.pop(c)
        moved.append(c)
    elif c in combo_row:
        already.append(c)

if not moved and already:
    print(f"no-op — {', '.join(already)} already under combos[{KEY!r}]")
    sys.exit(0)
if not moved:
    print(f"NOTHING TO MOVE and nothing present: {KEY} has no {CSTEPS} in either scope",
          file=sys.stderr)
    sys.exit(1)

shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s9_scopefix"))
state["updated_at"] = NOW
STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")

print(f"moved {', '.join(moved)} : stages[{KEY!r}] -> combos[{KEY!r}]")
print(f"  stages[{KEY!r}] now: {sorted(stage_row)}")
print(f"  combos[{KEY!r}] now: {sorted(combo_row)}")
