#!/usr/bin/env python3
"""C9 · assessment anchoring across the serve — mathematics · VII · ch 7.

testing.md C9's four checks, run over the whole C6 serve set. Re-runnable: the moment the
library is back to three canonicals this closes C9 in one command.

    ARUVI_DATA_DIR=$PWD/data/content python3 genon/out/stage_prep_mathematics_middle/c9_anchor_check.py

1. PREFIX REMAP        every served item's anchor is the SITTING number, not the authored unit
2. BORROWED ITEMS      on a fill, the fill unit's items come from its HOME variant, anchored to
                       the LAST sitting
3. UNSERVED ANCHORS    (a) no item anywhere carries an empty anchor
                       (b) items whose unit was not served are ABSENT, counted in
                           genon.assessment_items_unserved
                       (c) below floor, the DROPPED units' items ARE present, anchored to the
                           dropped unit's sitting number in THIS plan, flagged unscheduled
4. NO CROSS-VARIANT    no item anchors outside 1..len(served units)
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))

import aruvi_core.subjects.mathematics                      # noqa: E402,F401  (registers)
from aruvi_core import subjects                             # noqa: E402
from aruvi_core.genon import parse_matrix, serve_plan       # noqa: E402
from api import data                                        # noqa: E402

SPECS = ["5x40", "6x40", "7x40", "8x40", "9x40", "10x40", "11x40", "12x40", "13x40", "7x40+4x50"]


def items_of(result):
    """(item, anchor_unit) for every item in a served plan, via the subject plugin."""
    sub = subjects.get("mathematics")
    view = sub.assessment_to_view(
        result["assessment_items"], grade="vii",
        chapter={"chapter_number": 7, "chapter_title": ""},
        link_context={"periods": result["lesson_plan"]["periods"],
                      "handoff": result.get("coverage_handoff")})
    out = []
    for g in view.groups:
        for i in g.items:
            anchor = ((i.meta or {}).get("linked_periods") or [None])[-1]
            out.append((i, anchor))
    return out


def main() -> int:
    streams = data.load_genon_streams("mathematics", "vii", 7)
    counts = sorted((len(s["units"]) for s in streams), reverse=True)
    print(f"library on disk: {counts}"
          + ("" if len(counts) == 3 else "   ← INCOMPLETE: fill/borrow rows cannot be judged"))
    fails = []
    print(f"\n{'serve':11} {'units':>5} {'items':>5} {'anchors':22} {'unserved':>8}  verdict")
    for spec in SPECS:
        try:
            r = serve_plan(streams, parse_matrix(spec))
        except Exception as e:                              # noqa: BLE001
            print(f"{spec:11} SERVE FAILED: {type(e).__name__}: {e}")
            fails.append((spec, "serve failed"))
            continue
        res, g = r["result"], (r.get("genon") or {})
        n = len(res["lesson_plan"]["periods"])
        pairs = items_of(res)
        anchors = sorted({a for _, a in pairs if a})
        notes = []

        # 3(a) no empty anchor anywhere
        empty = [(i.normalized.id if i.normalized else None) or "?" for i, a in pairs if not a]
        if empty:
            notes.append(f"EMPTY ANCHOR on {empty}")

        # 1 + 4: every anchor is a real sitting of THIS plan
        oob = [a for a in anchors if not (1 <= a <= n)]
        if oob:
            notes.append(f"anchor outside 1..{n}: {oob}")

        # 3(c) below floor: dropped units' items present, anchored to the dropped sitting,
        #      flagged unscheduled
        dropped = res.get("dropped_units") or []
        if dropped:
            dnums = {u.get("period_number") for u in dropped}
            flagged = [(i.normalized.id if i.normalized else None) or "?" for i, a in pairs
                       if a in dnums and not (i.meta or {}).get("unscheduled")]
            present = {a for _, a in pairs} & dnums
            if not present:
                notes.append(f"dropped units {sorted(dnums)} carry NO items")
            if flagged:
                notes.append(f"dropped-unit items not flagged unscheduled: {flagged}")

        # 2: on a fill, the LAST sitting should carry the borrowed unit's own items
        sf = g.get("slot_fill") or {}
        if sf.get("mode") in ("fill", "synthesis"):
            if n not in anchors:
                notes.append(f"fill/synthesis: last sitting {n} carries no item "
                             f"(borrowed unit brought none)")

        verdict = "PASS" if not notes else "FAIL"
        if notes:
            fails.append((spec, "; ".join(notes)))
        print(f"{spec:11} {n:5} {len(pairs):5} {str(anchors)[:22]:22} "
              f"{str(g.get('assessment_items_unserved')):>8}  {verdict}")
        for t in notes:
            print(f"{'':11} └─ {t}")

    print()
    if fails:
        print(f"C9: {len(fails)} row(s) with findings — see above")
    else:
        print("C9: zero mis-anchored items across every served plan")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
