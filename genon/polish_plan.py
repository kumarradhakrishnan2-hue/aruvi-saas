#!/usr/bin/env python3
"""Run tier-1 seam polish over an already-partitioned saved plan — the inspection lab.

The teacher-facing path is the "Smooth unit transitions with AI" checkbox in Prepare
(api/main.py genon_make_plan -> aruvi_core.genon.polish.run_polish). This CLI runs the
SAME function over a plan already on disk, so a polish pass can be judged without
creating another plan in the teacher's library:

    python3 genon/polish_plan.py data/cloud/content/saved_plans/social_sciences/ix/ch_05_20260726_120401.json --dry
    ANTHROPIC_API_KEY=... python3 genon/polish_plan.py <plan.json>

--dry builds and prints the flagged payload (no API call, no spend). A live run writes
the polished twin to genon/out/polish_tests/, prints a before/after report, and appends
a mode=polish row to genon/ledger.csv so step-8 cost tracking stays in one file.
The plan on disk is NEVER modified.
"""
from __future__ import annotations

import argparse
import copy
import csv
import json
import os
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from aruvi_core.genon import polish as PL   # noqa: E402


def words(s) -> int:
    return len(str(s or "").split())


def matrix_label(plan: dict) -> str:
    m = (plan.get("genon") or {}).get("matrix") or plan.get("period_rows_snapshot") or []
    return " · ".join(f"{r['count']}x{r['duration']}" for r in m) or "?"


def report(before: dict, after: dict, rec: dict) -> None:
    bp = before["result"]["lesson_plan"]["periods"]
    ap = {p["period_number"]: p for p in after["result"]["lesson_plan"]["periods"]}
    changed = set(rec.get("periods_polished") or [])
    kept = set(rec.get("tier0_kept") or [])

    print("\n" + "=" * 78)
    print(f"POLISH REPORT — {before.get('subject')} {before.get('grade')} ch "
          f"{before.get('chapter_number')} — {matrix_label(before)}")
    print("=" * 78)
    print(f"model {rec.get('model')} | flagged {len(rec.get('flagged') or [])} | "
          f"polished {len(changed)} | tier-0 kept {len(kept)} | "
          f"parse failures {rec.get('parse_failures', 0)}")
    print(f"{rec.get('input_tokens')} in / {rec.get('output_tokens')} out | "
          f"Rs. {rec.get('cost_inr')} | {rec.get('wall_seconds')}s")
    if rec.get("tier0_reasons"):
        print("tier-0 kept, with reasons:")
        for n, why in rec["tier0_reasons"].items():
            print(f"   P{n}: {why}")

    print("\n--- TITLES " + "-" * 66)
    for p in bp:
        n = p["period_number"]
        new = ap[n]["activity_title"]
        if new != p["activity_title"]:
            print(f"  P{n:>2} -  {p['activity_title']}")
            print(f"      +  {new}")
        elif n in changed or n in kept:
            print(f"  P{n:>2} =  {p['activity_title']}   [unchanged]")

    print("\n--- TEACHER NOTES " + "-" * 59)
    tot_b = tot_a = 0
    for p in bp:
        n = p["period_number"]
        b, a = p["teacher_notes"], ap[n]["teacher_notes"]
        tot_b += words(b)
        tot_a += words(a)
        if a == b:
            continue
        flag = "" if n not in kept else "  (TIER-0 KEPT)"
        print(f"\n  P{n} — {words(b)}w -> {words(a)}w{flag}")
        print(f"    BEFORE: {b[:200].replace(chr(10), ' | ')}…")
        print(f"    AFTER : {a[:400].replace(chr(10), ' | ')}")
    print(f"\n  note words in total: {tot_b} -> {tot_a}")

    print("\n--- INVARIANTS " + "-" * 62)
    sb = [tb["activity"] for p in bp for tb in p["time_bands"]]
    sa = [tb["activity"] for p in ap.values() for tb in p["time_bands"]]
    print(f"  band (phase) text untouched: {sb == sa}")
    mb = [tb["minutes"] for p in bp for tb in p["time_bands"]]
    ma = [tb["minutes"] for p in ap.values() for tb in p["time_bands"]]
    print(f"  band timings untouched:      {mb == ma}")
    bad = [n for n, p in ap.items()
           if any(w in p["teacher_notes"].lower() for w in ("last time", "next period", "tomorrow", "today's lesson"))]
    print(f"  notes with calendar words:   {bad or 'none'}")
    fwd = [n for n, p in ap.items() if "next unit" in p["teacher_notes"].lower()]
    print(f"  notes with forward refs:     {fwd or 'none'}")


def ledger_row(plan: dict, rec: dict, out_file: str) -> None:
    path = os.path.join(ROOT, "genon", "ledger.csv")
    kept = rec.get("tier0_kept") or []
    row = [datetime.now().strftime("%Y%m%d_%H%M%S"), "polish", matrix_label(plan),
           rec.get("model"), plan.get("subject"), plan.get("grade"),
           plan.get("chapter_number"), matrix_label(plan), "", "polish-tier1",
           rec.get("input_tokens"), rec.get("output_tokens"), rec.get("cost_inr"),
           rec.get("wall_seconds"), "ok" if not kept else "problems",
           ("tier0_kept: " + ",".join(str(k) for k in kept)) if kept else "",
           os.path.basename(out_file)]
    with open(path, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(row)
    print(f"\nledger row appended -> genon/ledger.csv")


def main() -> int:
    ap_ = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap_.add_argument("plan", help="path to a partitioned saved plan (.json)")
    ap_.add_argument("--dry", action="store_true", help="print the flagged payload, call nothing")
    ap_.add_argument("--out", help="where to write the polished twin")
    ap_.add_argument("--no-ledger", action="store_true")
    a = ap_.parse_args()

    plan = json.load(open(a.plan))
    if (plan.get("plan_status") or "") == "canonical":
        print("REFUSING: that is the certified canonical, not an adapted plan.", file=sys.stderr)
        return 2

    flagged = PL.build_polish_request(copy.deepcopy(plan))
    print(f"{os.path.basename(a.plan)} — {matrix_label(plan)} — "
          f"{len(plan['result']['lesson_plan']['periods'])} periods, {len(flagged)} flagged")
    for f in flagged:
        print(f"   P{f['n']:>2}  seam={str(f['needs_seam_note']):<5} units={len(f['source_unit_titles'])} "
              f"budget={f['word_budget']}w  note now {words(f['current_teacher_note'])}w")
    if a.dry:
        print("\n--- payload that would be sent " + "-" * 47)
        print(json.dumps(flagged, ensure_ascii=False, indent=1)[:4000])
        print("\n[--dry] nothing called, nothing spent.")
        return 0

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY is not set — export it first.", file=sys.stderr)
        return 2

    before = copy.deepcopy(plan)
    rec = PL.run_polish(plan)
    out = a.out or os.path.join(ROOT, "genon", "out", "polish_tests",
                               os.path.basename(a.plan).replace(".json", "_polished.json"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    report(before, plan, rec)
    print(f"\npolished twin -> {os.path.relpath(out, ROOT)}")
    print(f"source plan untouched -> {a.plan}")
    if not a.no_ledger:
        ledger_row(plan, rec, out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
