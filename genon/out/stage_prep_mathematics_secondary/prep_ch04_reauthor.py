#!/usr/bin/env python3
"""Prepare mathematics IX ch 4 for re-authoring at 15 periods.

WHY RE-AUTHOR. The 2026-08-08 library is sound but was authored against three things that
have since changed, and none of them can be repaired into the files on disk:
  1. THE SUMMARY. Its nine end-of-chapter items were all attributed to 4.1, so units 10-12
     wear the "Introduction" label and render to the teacher as "Introduction (Revisit)".
     The summary is corrected; a plan already authored from the old one cannot inherit that.
  2. LP v1.2's Rule 12. p11's sec#1 lists [1, 10, 11] against an LO those units do not
     deliver, which drops the Introduction item at X=9 and X=10. Editing a handoff row is
     assessment anchoring, out of scope for both repair tools by their own doctrine.
  3. THE PERIOD COUNT. ch 3's re-weighting moved ch 4 from 14 to 15 recommended periods.

WHAT THIS SCRIPT DOES (all free):
  * LIFTS the pin on mathematics|IX|4. The pin exists to stop the counts rule moving an
    AUTHORED library; deliberately re-authoring is precisely when it must go, and the pin's
    own text says so ("Lift this pin if ch 4 is ever re-authored"). Without lifting it the
    brief asks for 15 units while canonical_plan.counts still reads [14, 11, 8], and
    certification's library-complete check fails a good run.
  * ARCHIVES the existing three-file library. It must move, not stay: the new counts are
    [15, 12, 9], so the old ch_04_canonical_p11.json / _p08.json would linger beside the
    new p12/p09 and break library-complete. Archived rather than deleted — it is the C2
    cost record and the C10.3 no-overwrite evidence.
  * RE-RUNS master_plan.py + variant_plans.py (the runbook pair) so the row lands at
    [15, 12, 9], provisional again until the new standard is authored.

COST NOTE FOR C2. The Rs 106.52 already spent becomes SUPERSEDED spend, not clean-path.
Per the founder's 2026-08-07 two-figure rule, ch 4's clean-path cost becomes whatever the
new library costs (~Rs 115 at 15/12/9, output scaling with period count); the Rs 106.52 sits
in the all-in figure and must be kept OUT of any 330-chapter extrapolation.

    python3 genon/out/stage_prep_mathematics_secondary/prep_ch04_reauthor.py            # dry run
    python3 genon/out/stage_prep_mathematics_secondary/prep_ch04_reauthor.py --apply
"""
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PINS = ROOT / "data/content/allocation_norms/canonical_period_pins.json"
LIB = ROOT / "data/content/saved_plans/mathematics/ix"
ARCHIVE = ROOT / "backup/superseded_libraries"
KEY = "mathematics|IX|4"

dry = "--apply" not in sys.argv
ts = datetime.now().strftime("%Y%m%d_%H%M%S")

pins = json.loads(PINS.read_text(encoding="utf-8"))
has_pin = KEY in pins.get("pins", {})
files = sorted(LIB.glob("ch_04_canonical*.json"))

print(f"pin {KEY}: {'PRESENT — will be lifted' if has_pin else 'absent (already lifted)'}")
print(f"library files to archive ({len(files)}):")
for f in files:
    print(f"   {f.name}")
print(f"archive dest: backup/superseded_libraries/mathematics_ix_ch04_{ts}/")

if dry:
    print("\ndry run — nothing changed. Re-run with --apply.")
    raise SystemExit(0)

if has_pin:
    lifted = pins["pins"].pop(KEY)
    pins.setdefault("_lifted", {})[f"{KEY}@{ts}"] = {
        **lifted,
        "lifted_on": "2026-08-09",
        "lifted_because": ("ch 4 is being re-authored at 15 periods against the corrected "
                           "summary and LP v1.2, so the counts SHOULD move to [15,12,9]. The "
                           "pin existed only to protect the superseded library."),
    }
    PINS.write_text(json.dumps(pins, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nlifted the pin (kept under _lifted for the record)")

if files:
    dest = ARCHIVE / f"mathematics_ix_ch04_{ts}"
    dest.mkdir(parents=True, exist_ok=True)
    for f in files:
        shutil.move(str(f), dest / f.name)
    (dest / "README.txt").write_text(
        "Superseded mathematics IX ch 4 library, authored 2026-08-08 at [14, 11, 8] for\n"
        "Rs 106.52 and certified ALL PASS (report 20260809_094402).\n\n"
        "Moved aside 2026-08-09 for a re-author at [15, 12, 9]. Reasons: the chapter summary's\n"
        "end-of-chapter attributions were corrected (units 10-12 wore the '4.1' label and\n"
        "rendered as 'Introduction (Revisit)'); LP v1.2 narrowed Rule 12 and p11's\n"
        "sec#1 = [1,10,11] no longer complies; and ch 3's re-weighting moved this chapter\n"
        "from 14 to 15 recommended periods.\n\n"
        "KEEP. This is the C2 cost record for the Rs 106.52 (now SUPERSEDED spend, excluded\n"
        "from the clean-path figure and from any corpus extrapolation) and the C10.3\n"
        "no-overwrite evidence.\n", encoding="utf-8")
    print(f"archived {len(files)} file(s) -> {dest.relative_to(ROOT)}/")

for script in ("genon/master_plan.py", "genon/variant_plans.py"):
    print(f"\n== {script} ==")
    r = subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT,
                       capture_output=True, text=True)
    print("\n".join(r.stdout.strip().splitlines()[-4:]))
    if r.returncode:
        raise SystemExit(f"{script} failed:\n{r.stderr[-1200:]}")

row = [c for c in json.loads((ROOT / "data/content/allocation_norms/master_plan.json")
                             .read_text())["combos"]["mathematics|IX"]["chapters"]
       if c["chapter"] == 4][0]
print(f"\nch 4 row now: recommended_periods {row['recommended_periods']}  "
      f"canonical_periods {row['canonical_periods']}  "
      f"plan.counts {row['canonical_plan']['counts']}  "
      f"provisional {row['canonical_plan']['provisional']}")
print("\nREADY. Run in Terminal (metered):")
print("  python3 genon/build_library.py mathematics ix 4 --top-only")
