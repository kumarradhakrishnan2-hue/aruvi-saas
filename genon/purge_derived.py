#!/usr/bin/env python3
"""purge_derived.py — a repaired canonical invalidates the plans derived from it (v1.0, 2026-08-04).

WHY THIS EXISTS. `repair_anchors.py`, `repair_register.py` and `normalize_options.py` all
rewrite a canonical IN PLACE. The served plans already on disk were built from the OLD bytes,
and the serve cache addresses them by (chapter, matrix, engine, canonical ledger_ts) — none of
which changes when a repair lands. So without something to invalidate them, a teacher keeps
being served the pre-repair text. That is not hypothetical: on the SS·IX ch 3 pilot the
8-period plan was served four hours after its canonical was repaired, still carrying the
register breach the repair had removed and five unarranged MCQs, and only a manual delete
dislodged it (ARV-D-034).

TWO WAYS TO FIX IT, and why this is the one we kept:
  * put a repair fingerprint in the cache key — every repair mints a new entry, old files stay
    valid for whoever holds them. Built 2026-08-03, REVERTED 2026-08-04 (founder): it hangs a
    hash tail off every served filename (`…_c20260803143426r4d21e.json`) that no human can read.
  * PURGE the derived plans when the canonical changes — this file. The names stay clean
    (`ch_03_50m6_e13_c20260803143426.json`) and the next request rebuilds from the repaired
    canonical in ~11 ms. That rebuild being free is the whole reason this is affordable.

WHAT IT DELETES, and what it must never touch:
  * deletes: derived/served plans for that chapter — `ch_NN_<matrix>_e<NN>_c<version>.json`.
  * NEVER: `ch_NN_canonical*.json` (the library itself), any other chapter, anything outside
    the subject·grade directory. The regex is anchored and the canonical pattern cannot match it.

THE COST, stated plainly: a teacher holding a purged plan loses that file. Her prepared-plans
register still names it, and `GET /plans/...` simply stops listing it — the listing walks the
directory and marks what is prepared, so a dangling key is skipped, not an error. She re-prepares
and gets the repaired plan. At pilot scale that is the right trade; if it ever stops being, the
fingerprint branch above is the alternative, not a third invention.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO))
from api import config  # noqa: E402

# ★ THIS PATH WAS DEAD (fixed 2026-08-27, with the edition change). It named
# `data/content/saved_plans`, which stopped existing at the 2026-08-23 cloud/local
# restructure — the live tree is `data/cloud/content/`. Every purge since then found no
# directory and returned [] : the invariant this file EXISTS to enforce (ARV-D-034 — a
# repaired canonical must not keep serving from a cache entry cut before the repair)
# has been quietly off. It reads config.DATA_DIR now, so it cannot drift from the
# runtime again.
CONTENT = Path(config.DATA_DIR) / "saved_plans"


def derived_pattern(ch: int) -> re.Pattern:
    """`ch_NN_<matrix>_e<engine>_c<version>.json` — the served plans, and only those."""
    return re.compile(rf"^ch_{int(ch):02d}_(?:\d+m\d+)(?:-\d+m\d+)*_e\d+_c[0-9a-z]+\.json$")


def purge(subject: str, grade: str, ch: int, reason: str = "", apply: bool = True):
    """Remove every plan derived from this chapter's canonicals. Returns the names removed."""
    base = CONTENT / subject / grade
    if not base.is_dir():
        return []
    pat = derived_pattern(ch)
    # EVERY edition, not just the current one (§2.2). A repair to a canonical that was
    # CARRIED forward invalidates the derived plans in both the edition it was authored
    # in and every edition it was carried into — they share a ledger_ts, so they share a
    # cache key, so a stale entry in last year's folder is still reachable by
    # data.load_saved_plan's look-back. Purging only the current edition would leave
    # exactly the stale entry this file exists to destroy.
    dirs = [base] + [d for d in sorted(base.iterdir()) if d.is_dir()]
    doomed = sorted(p for d in dirs for p in d.iterdir()
                    if p.is_file() and pat.match(p.name))
    removed, failed = [], []
    for p in doomed:
        if not apply:
            removed.append(p.name)
            continue
        try:
            p.unlink()
            removed.append(p.name)
        except OSError as e:                       # read-only mount (a Cowork sandbox), etc.
            failed.append((p.name, str(e)))
    if removed or failed:
        print(f"\n== derived plans invalidated by {reason or 'a canonical change'} ==")
        for n in removed:
            print(f"   {'removed' if apply else 'would remove'}  {n}")
        for n, e in failed:
            print(f"   COULD NOT REMOVE  {n} — {e}")
        print("   (the next request for each rebuilds from the repaired canonical, ~11 ms)")
    if failed:
        raise SystemExit(
            "STOP: derived plans could not be deleted, so a stale plan can still be served. "
            "Delete them by hand and re-run, or run this on a machine with write access.")
    return removed


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 3:
        raise SystemExit(__doc__)
    subject, grade, ch = args[0], args[1].lower(), int(args[2])
    out = purge(subject, grade, ch, reason="a manual run",
                apply="--list" not in sys.argv)
    if not out:
        print("nothing to purge — no derived plans on disk for this chapter")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
