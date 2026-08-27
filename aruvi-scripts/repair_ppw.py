"""Re-derive periods-a-week from the calibrated annual budget (2026-08-27).

    python3 aruvi-scripts/repair_ppw.py --dry-run          # report, touch nothing
    python3 aruvi-scripts/repair_ppw.py --user 1000000001  # one teacher
    python3 aruvi-scripts/repair_ppw.py                    # only the untouched flat 6s
    python3 aruvi-scripts/repair_ppw.py --all              # EVERY ppw with a standard behind it

★ WHY. Three places seeded a teaching profile and all three set periods-a-week to a flat 6
while setting the annual budget from the calibrated master plan. The two disagree for 18 of 25
subject·grades, and the profile prints both on one line — social_sciences·ix reads "245 periods
for the year, at 6 a week", which is 41 teaching weeks and not a school year. Reported live on
account 1000000001 after subscribing to SS·secondary.

All three seeding paths are fixed (FirstRun, TeachingProfile.applyManageClasses,
api.main._default_grade_record). This repairs the records already written.

★ WHAT IT WILL AND WILL NOT TOUCH — the whole point of the script.

By DEFAULT it rewrites `periods_per_week` (and the matching single-entry `ppw_by_duration`)
ONLY when:

  1. the stored value is exactly the flat default 6 — anything else is a figure a teacher
     chose, and a repair script must never overwrite an answer; AND
  2. the master plan HAS a calibrated annual for that subject·class — no calibrated figure
     means no derivation, ever (deriving from her stored budget would be circular: with no
     master-plan row that budget is itself ppw × 30); AND
  3. the derived value actually differs from 6.

★ `--all` DROPS RULE 1 and re-derives every ppw that has a standard behind it (founder,
2026-08-27: "amend all the periods per week in existing records — these are test records
only"). Rules 2 and 3 still hold. On a test estate there is no chosen figure to protect, and
leaving half the records on the old flat 6 would make the estate itself inconsistent.
⚠️ Against LIVE teacher data --all overwrites deliberate answers. Say so out loud first.

It NEVER touches the budget. A wrong-looking budget is reported and left alone: the annual
total is the number she is invited to disagree with, and silently rewriting it is the exact
defect (`setMethod` replacing rather than converting) that this day's work removed.

A multi-duration class (she has split her week across period lengths) is reported and skipped —
its `ppw_by_duration` is a distribution the script has no basis to redistribute.
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from api import config, data  # noqa: E402
from api.main import ESTIMATE_WEEKS, ppw_from_annual  # noqa: E402

FLAT_DEFAULT = 6


def subject_slug(name: str) -> str:
    return (name or "").lower().replace(" ", "_")


def repair_profile(doc: dict, every: bool = False) -> tuple:
    """Returns (changes, notes). Mutates `doc` in place for the changes.

    `every` (--all) drops the "only the flat default 6" guard and re-derives EVERY ppw that
    has a calibrated standard behind it. Founder, 2026-08-27: "keep the standards as per the
    numbers already established … based on approx 30 weeks, amend all the periods per week in
    existing records (these are test records only)". The guard exists to protect a figure a
    real teacher chose; on a test estate there is no such figure to protect, and leaving half
    the records on the old flat 6 would make the estate itself inconsistent.
    ⚠️ Do NOT run --all against live teacher data without saying so out loud: it overwrites
    deliberate answers, which is precisely what the default mode refuses to do.
    """
    changes, notes = [], []
    for s in doc.get("subjects") or []:
        slug = subject_slug(s.get("name"))
        for gi, g in enumerate(s.get("grades") or []):
            gslug = (g.get("grade") or "").lower()
            where = f"{s.get('name')} {g.get('grade')}"
            # ALWAYS the calibrated standard — never the stored budget, which is itself
            # ppw × 30 for an unset record and would hand back the value we are replacing.
            annual = data.master_annual_budget(slug, gslug)
            cur = g.get("periods_per_week")
            want = ppw_from_annual(annual)

            b = (s.get("budget") or {}).get(str(gi)) or (s.get("budget") or {}).get(gi)
            if annual and b and b.get("method") == "periods" and b.get("value") != annual:
                notes.append(f"{where}: budget {b.get('value')} differs from the standard "
                             f"{annual} — LEFT ALONE (budgets are hers)")
            elif annual and b and b.get("method") == "auto" and b.get("value"):
                notes.append(f"{where}: budget {b.get('value')} is a legacy auto record "
                             f"(standard is {annual}) — LEFT ALONE")

            if not every and cur != FLAT_DEFAULT:
                if cur is not None and want and cur != want:
                    notes.append(f"{where}: ppw {cur} (not the default) vs implied {want} "
                                 f"— LEFT ALONE (looks chosen)")
                continue
            if not want:
                notes.append(f"{where}: no calibrated standard — ppw left at {cur}")
                continue
            if want == cur:
                continue
            durs = g.get("ppw_by_duration") or {}
            if len(durs) > 1:
                notes.append(f"{where}: ppw split across {len(durs)} durations — SKIPPED")
                continue

            g["periods_per_week"] = want
            if len(durs) == 1:
                g["ppw_by_duration"] = {k: want for k in durs}
            changes.append(f"{where}: ppw {cur} → {want}   (standard {annual} ÷ {ESTIMATE_WEEKS})")
    return changes, notes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--user", help="repair only this user id (default: everyone)")
    ap.add_argument("--all", dest="every", action="store_true",
                    help="re-derive EVERY ppw with a calibrated standard, not only the ones "
                         "still on the flat default 6. Overwrites deliberate answers — "
                         "intended for the test estate.")
    ap.add_argument("--dry-run", action="store_true", help="report only; change nothing")
    args = ap.parse_args()

    root = Path(config.STATE_DIR) / "readiness"
    if not root.is_dir():
        print(f"! no readiness store under {config.STATE_DIR}")
        return 2

    total_changes = total_notes = files = 0
    for prof in sorted(root.glob("*/*/profile.json")):
        uid = prof.parent.name
        if args.user and uid != args.user:
            continue
        try:
            doc = json.loads(prof.read_text())
        except (OSError, ValueError):
            print(f"  ! {uid}: unreadable, skipped")
            continue
        changes, notes = repair_profile(doc, every=args.every)
        if not changes and not notes:
            continue
        files += 1
        print(f"\n{uid}")
        for c in changes:
            print(f"   {'would fix' if args.dry_run else 'FIXED'}  {c}")
        for n in notes:
            print(f"   note      {n}")
        total_changes += len(changes)
        total_notes += len(notes)
        if changes and not args.dry_run:
            blob = json.dumps(doc, ensure_ascii=False, indent=2)
            # Atomic where the filesystem allows it. Some mounts (the Cowork sandbox among
            # them) refuse the .tmp sidecar, and a repair that dies half way through the
            # estate is worse than one that writes in place — so fall back rather than stop.
            try:
                tmp = prof.with_suffix(".tmp")
                tmp.write_text(blob)
                os.replace(tmp, prof)
            except OSError:
                prof.write_text(blob)

    head = "DRY RUN — nothing changed" if args.dry_run else "Repaired"
    print(f"\n{head}: {total_changes} periods-a-week value(s) across {files} profile(s); "
          f"{total_notes} left alone.")
    if args.dry_run:
        print("Re-run without --dry-run to apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
