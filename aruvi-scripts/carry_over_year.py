"""Carry unchanged chapters into the next lesson-plan edition (admin architecture §2.2).

    python3 aruvi-scripts/carry_over_year.py --to 2027-28 --dry-run
    python3 aruvi-scripts/carry_over_year.py --to 2027-28
    python3 aruvi-scripts/carry_over_year.py --to 2027-28 --except social_sciences/ix

★ WHAT "CARRYING OVER" MEANS, AND WHY IT COPIES THE CACHE TOO.

Every year the library is re-versioned whether or not the textbook changed (§2.2). Most
chapters are NOT re-authored — they are the same plan wearing a new edition label. The
founder's rule: a carried chapter is stamped with the NEW year even though nothing in it
changed, so a teacher never holds a plan whose edition she cannot name.

The trap that rule sets: derived (served) plans live in the SAME folder as the canonical
they came from. Copy only the canonical into 2027-28/ and that folder has no derived
plans at all — so every serve of an unchanged chapter regenerates from scratch, and you
re-pay in June, at peak load, for content that did not change. That is precisely the bill
§2.2 exists to prevent ("get this wrong and every June you re-pay…").

So carry-over copies the canonical AND its derived plans, rewriting ONLY `academic_year`
on each and leaving `ledger_ts` and every FILENAME untouched. The filename is unchanged
because the year was never part of the key:

    ch_05_50m16_e19_c20260812165329ssix05p17.json
              ^engine  ^constitution-run          — no year, by design

Year is the LABEL, (engine, constitution-run) is the KEY. That is what makes the copied
cache still hit. Put the year in the key and this script becomes pointless.

★ WHAT IS NOT CARRIED. Chapters you re-authored. Name them with --except (repeatable), or
let the script skip any chapter that ALREADY exists in the target edition — a
re-authoring batch that has already written 2027-28/ch_07_canonical.json will not have it
overwritten by last year's copy. Re-authored chapters get new ledger_ts values, so their
caches correctly start empty and the first serve pays once.

IDEMPOTENT: re-running copies nothing it has already copied. Never deletes; never touches
the source edition.
"""
import argparse
import json
import os
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from api import config  # noqa: E402

_YEAR_RE = re.compile(r"^\d{4}-\d{2}$")
_CH_RE = re.compile(r"^ch_(\d{2})_")


def chapter_of(filename: str):
    m = _CH_RE.match(filename)
    return int(m.group(1)) if m else None


def is_canonical(filename: str) -> bool:
    return "_canonical" in filename


def restamp(src: Path, dst: Path, year: str, dry_run: bool = False) -> bool:
    """Copy one plan, rewriting only its academic_year. False if it could not be read."""
    try:
        doc = json.loads(src.read_text())
    except (OSError, ValueError):
        return False
    if not isinstance(doc, dict):
        return False
    key = "genon_canonical" if isinstance(doc.get("genon_canonical"), dict) else (
        "genon" if isinstance(doc.get("genon"), dict) else "genon_canonical")
    block = dict(doc.get(key) or {})
    block["academic_year"] = year
    # Provenance: an auditor should be able to see that this file's BYTES are last
    # year's even though its label is this year's. Without it, a carried chapter and a
    # re-authored one look identical from the outside.
    block["carried_from"] = block.get("carried_from") or _source_year(src)
    doc[key] = block
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        tmp = dst.with_suffix(dst.suffix + ".tmp")
        tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=2))
        os.replace(tmp, dst)
    return True


def _source_year(src: Path):
    return src.parent.name if _YEAR_RE.match(src.parent.name) else None


def carry_grade(gdir: Path, from_year: str, to_year: str, skip: set,
                dry_run: bool = False) -> dict:
    """Carry one subject·grade forward. Returns counts + the chapters it touched."""
    out = {"canonicals": 0, "derived": 0, "skipped_present": 0,
           "skipped_excluded": 0, "unreadable": 0, "chapters": set()}
    src_dir, dst_dir = gdir / from_year, gdir / to_year
    if not src_dir.is_dir():
        return out

    for src in sorted(src_dir.glob("*.json")):
        ch = chapter_of(src.name)
        if ch is not None and ch in skip:
            out["skipped_excluded"] += 1
            continue
        dst = dst_dir / src.name
        if dst.exists():
            # Already carried, or freshly RE-AUTHORED. Either way the target edition's
            # copy is the authority — never overwrite it with last year's.
            out["skipped_present"] += 1
            continue
        if not restamp(src, dst, to_year, dry_run):
            out["unreadable"] += 1
            continue
        out["derived" if not is_canonical(src.name) else "canonicals"] += 1
        if ch is not None:
            out["chapters"].add(ch)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--to", required=True, help="target edition, e.g. 2027-28")
    ap.add_argument("--from", dest="from_year", default=config.LP_YEAR,
                    help=f"source edition (default {config.LP_YEAR})")
    ap.add_argument("--except", dest="excluded", action="append", default=[],
                    metavar="SUBJECT/GRADE[:CH,CH]",
                    help="do not carry these (repeatable). 'science/ix' excludes the "
                         "whole grade; 'science/ix:3,7' excludes chapters 3 and 7.")
    ap.add_argument("--dry-run", action="store_true", help="report only; change nothing")
    args = ap.parse_args()

    for y in (args.to, args.from_year):
        if not _YEAR_RE.match(y):
            print(f"! years must look like 2027-28, got {y!r}")
            return 2
    if args.to == args.from_year:
        print("! --to and --from are the same edition")
        return 2

    # subject/grade -> set of chapters to skip; empty set means SKIP THE WHOLE GRADE
    excl = {}
    for spec in args.excluded:
        key, _, chs = spec.partition(":")
        key = key.strip("/ ")
        if chs.strip():
            excl.setdefault(key, set()).update(
                int(c) for c in chs.replace(" ", "").split(",") if c.isdigit())
        else:
            excl[key] = "ALL"

    root = Path(config.DATA_DIR) / "saved_plans"
    if not root.is_dir():
        print(f"! no saved_plans under {config.DATA_DIR}")
        return 2

    total = defaultdict(int)
    rows, whole_skips = [], []
    for subject in sorted(p for p in root.iterdir() if p.is_dir()):
        for gdir in sorted(p for p in subject.iterdir() if p.is_dir()):
            if _YEAR_RE.match(gdir.name):
                continue
            key = f"{subject.name}/{gdir.name}"
            rule = excl.get(key)
            if rule == "ALL":
                whole_skips.append(key)
                continue
            r = carry_grade(gdir, args.from_year, args.to, rule or set(), args.dry_run)
            if r["canonicals"] or r["derived"] or r["skipped_present"] or r["skipped_excluded"]:
                rows.append((key, r))
            for k, v in r.items():
                if k != "chapters":
                    total[k] += v

    head = ("DRY RUN — nothing changed" if args.dry_run
            else f"Carried {args.from_year} → {args.to}")
    print(f"\n{head}\n{'-' * 70}")
    for key, r in rows:
        print(f"  {key:<26} canonicals {r['canonicals']:>4}  derived {r['derived']:>3}"
              f"  present {r['skipped_present']:>4}  excluded {r['skipped_excluded']:>3}")
    print(f"{'-' * 70}")
    print(f"  {'TOTAL':<26} canonicals {total['canonicals']:>4}"
          f"  derived {total['derived']:>3}  present {total['skipped_present']:>4}"
          f"  excluded {total['skipped_excluded']:>3}")
    if whole_skips:
        print(f"\n  Not carried (re-authored): {', '.join(whole_skips)}")
    if total["derived"]:
        print(f"\n  ✓ {total['derived']} derived plan(s) carried with their canonicals — "
              f"those serves stay free.\n    Filenames and ledger_ts unchanged, so the "
              f"cache still hits (§2.2: year is the label, not the key).")
    if total["unreadable"]:
        print(f"\n  ! {total['unreadable']} file(s) could not be parsed and were skipped.")
    if args.dry_run:
        print("\n  Re-run without --dry-run to apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
