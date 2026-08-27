"""One-shot migration for the lesson-plan EDITION stamp (admin architecture §2.2, 2026-08-27).

Gives every plan in the library the one fact it has never carried — which authored
edition it came from — and files the library by that edition:

  BEFORE   saved_plans/{subject}/{grade}/ch_NN_*.json
  AFTER    saved_plans/{subject}/{grade}/2026-27/ch_NN_*.json
           …each file's genon_canonical (or genon) block gaining academic_year.

★ WHY THIS EXISTS AT ALL. Two different years live in this system:

    the TEACHER's academic year — Bucket B, per teacher, the year she is TEACHING in
    the LIBRARY's edition year  — Bucket A, shared, which authored edition a plan IS

They are independent. She can teach one 2026-27 plan for several years running, and My
Lessons already shows a year — HERS. Once a second edition exists, showing her year while
she assumes the plan's is precisely the confusion §2.2 wrote the stamp to prevent. Today
there is exactly one edition, so nothing can be confused yet: this migration is cheap
insurance bought before the price goes up, and the price is the backfill, which only grows.

★ WHAT THIS DELIBERATELY DOES NOT DO. It does not touch any FILENAME. Derived plans stay
keyed by (engine, constitution-run) — data.genon_plan_filename — because the year is a
LABEL and never a cache key (§2.2). Put the year in the key and every edition bump
re-buys the whole variant library at the June peak, which is the exact bill §2.2 exists
to avoid. carry_over_year.py depends on this: it copies an unchanged chapter forward
under its ORIGINAL filename so the cache still hits.

IDEMPOTENT by construction — safe to re-run:
  * a {subject}/{grade} whose plan files already live under year-shaped dirs is skipped;
  * a file that already carries academic_year keeps the value it has (a hand-corrected
    stamp is never overwritten by the default);
  * files are MOVED within one filesystem (os.replace), never copied-then-deleted, so an
    interrupted run leaves every file readable at one path or the other — never neither;
  * junk (.DS_Store and friends) is left exactly where it lies.

Run from the repo root:
    python3 aruvi-scripts/migrate_lp_year.py --dry-run     # report, touch nothing
    python3 aruvi-scripts/migrate_lp_year.py               # do it
    python3 aruvi-scripts/migrate_lp_year.py --year 2026-27

Honours ARUVI_DATA_DIR and ARUVI_LP_YEAR like the app itself (api/config.py).
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from api import config  # noqa: E402

_YEAR_RE = re.compile(r"^\d{4}-\d{2}$")


def _is_year_dir(name: str) -> bool:
    return bool(_YEAR_RE.match(str(name)))


def stamp_block(doc: dict) -> str:
    """Which block carries the edition stamp for this file.

    A canonical is AUTHORED and carries genon_canonical; a served plan is DERIVED and
    carries genon. A file with neither is a legacy hand-saved plan — it gets
    genon_canonical, because that is where data.plan_lp_year looks first.
    """
    if isinstance(doc.get("genon_canonical"), dict):
        return "genon_canonical"
    if isinstance(doc.get("genon"), dict):
        return "genon"
    return "genon_canonical"


def stamp_file(path: Path, year: str, dry_run: bool = False) -> str:
    """Add academic_year to one plan file. Returns 'stamped' | 'kept' | 'unreadable'.

    'kept' means the file already had a stamp — including a DIFFERENT one. Overwriting
    that would silently relabel a plan whose edition somebody has already established,
    which is the one thing a backfill must never do.
    """
    try:
        doc = json.loads(path.read_text())
    except (OSError, ValueError):
        return "unreadable"
    if not isinstance(doc, dict):
        return "unreadable"

    key = stamp_block(doc)
    block = doc.get(key)
    if not isinstance(block, dict):
        block = {}
    if block.get("academic_year"):
        return "kept"

    block["academic_year"] = year
    doc[key] = block
    if not dry_run:
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=2))
        os.replace(tmp, path)          # atomic — a crash leaves the original intact
    return "stamped"


def migrate_grade(gdir: Path, year: str, dry_run: bool = False) -> dict:
    """Stamp and re-file one subject·grade. Returns a counts dict."""
    out = {"stamped": 0, "kept": 0, "moved": 0, "unreadable": 0, "already": 0}

    loose = sorted(p for p in gdir.glob("*.json") if p.is_file())
    dated = [d for d in gdir.iterdir() if d.is_dir() and _is_year_dir(d.name)]

    if not loose and dated:
        # Already migrated. Still walk the year folders, because a re-run after a
        # PARTIAL stamp pass must be able to finish the job.
        for d in dated:
            for p in sorted(d.glob("*.json")):
                out[stamp_file(p, d.name, dry_run)] += 1
        out["already"] = 1
        return out

    if not loose:
        return out

    target = gdir / year
    if not dry_run:
        target.mkdir(parents=True, exist_ok=True)

    for p in loose:
        out[stamp_file(p, year, dry_run)] += 1
        dest = target / p.name
        if dest.exists():
            # Same filename in both layouts: the year folder's copy wins (it is the
            # migrated one). Leave the loose file alone rather than clobbering either —
            # a human should look at why there are two.
            continue
        if not dry_run:
            os.replace(p, dest)
        out["moved"] += 1

    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", default=config.LP_YEAR,
                    help=f"edition to stamp and file under (default {config.LP_YEAR})")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would happen; change nothing")
    args = ap.parse_args()

    if not _is_year_dir(args.year):
        print(f"! --year must look like 2026-27, got {args.year!r}")
        return 2

    root = Path(config.DATA_DIR) / "saved_plans"
    if not root.is_dir():
        print(f"! no saved_plans under {config.DATA_DIR}")
        return 2

    total = {"stamped": 0, "kept": 0, "moved": 0, "unreadable": 0, "already": 0}
    rows = []
    for subject in sorted(p for p in root.iterdir() if p.is_dir()):
        for gdir in sorted(p for p in subject.iterdir() if p.is_dir()):
            if _is_year_dir(gdir.name):
                continue                      # subject/{year} — not the grade level
            r = migrate_grade(gdir, args.year, args.dry_run)
            if any(r.values()):
                rows.append((f"{subject.name}/{gdir.name}", r))
            for k in total:
                total[k] += r[k]

    head = "DRY RUN — nothing changed" if args.dry_run else f"Migrated to {args.year}"
    print(f"\n{head}\n{'-' * 58}")
    for name, r in rows:
        note = " (already foldered)" if r["already"] else ""
        print(f"  {name:<28} stamped {r['stamped']:>4}  moved {r['moved']:>4}"
              f"  kept {r['kept']:>4}{note}")
    print(f"{'-' * 58}")
    print(f"  {'TOTAL':<28} stamped {total['stamped']:>4}  moved {total['moved']:>4}"
          f"  kept {total['kept']:>4}")
    if total["unreadable"]:
        print(f"\n  ! {total['unreadable']} file(s) could not be parsed and were left alone.")
    if args.dry_run:
        print("\n  Re-run without --dry-run to apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
