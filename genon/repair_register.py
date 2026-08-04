#!/usr/bin/env python3
"""repair_register.py — backfill register breaches in an authored library (v1.0, 2026-08-02).

FOUNDER RULING, 2026-08-02: regenerating is a lottery. The SS·IX ch 3 top canonical breached
THE SELF-CONTAINED REGISTER nine times while authored under v1.10, which bans it in terms;
another run samples the same distribution at Rs 39 with no guarantee. So breaches are repaired
in place — and the doctrine that "fixes happen upstream, never by hand-editing artifacts" is
honoured by making the repair a PIPELINE STAGE rather than a text editor session: the edits are
declared here in code, applied by assertion, recorded in the artefact, and re-scanned.

WHAT MAKES THIS SAFE, and the line it must not cross:
  * every edit is a STATED (old -> new) pair, not a generated rewrite. No model authors text
    here. If `old` is not found verbatim the file is left untouched and the run fails loudly —
    so a repair can never silently drift against a regenerated artefact.
  * almost every edit is a DELETION of a trailing clause (the breaches are appositives:
    "— a thread to pick up in the climate-change unit"). Nothing is invented.
  * the artefact records what was done, in genon_canonical.repairs[], so corpus statistics can
    still tell generation quality from repair quality. Without that record we would lose the
    evidence that says whether to change the MECHANISM instead of repairing forever.
  * STRUCTURAL and PEDAGOGICAL defects are OUT OF SCOPE and must stay out: a cross-unit
    materials dependency, approach-diversity repeats, an anchor that names the wrong section.
    Repairing those here would launder content changes as text hygiene. They go to the human
    gate or a regeneration decision.

    python3 genon/repair_register.py --list          # show the declared edits
    python3 genon/repair_register.py --apply         # back up, apply, record, re-scan
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))

from register_scan import scan_plan, report                      # noqa: E402
from purge_derived import purge                                  # noqa: E402

LIB = REPO / "data" / "content" / "saved_plans" / "social_sciences" / "ix"
BACKUP = REPO / "backup" / "register_repair"

# ── the declared edits ───────────────────────────────────────────────────────────
# file -> [(unit_number, field_locator, old, new, rule_broken, note)]
# field_locator: "teacher_notes" | "band:<index>" | "homework:<index>"
#
# DECLARATIONS REWRITTEN 2026-08-03 (v1.1). The previous set was written against the
# 2026-08-01 library (12/9/7) and went stale the moment that library was regenerated under
# LP v1.10 / assessment v1.6 on 2026-08-03 (12/10/7) — `--list` failed its own assertion on
# the very first edit, which is the guard working exactly as designed. The p09 variant no
# longer exists; p07 now scans clean. What follows is declared against the CURRENT artefacts
# (ch_03_canonical.json 14:19, ch_03_canonical_p10.json 14:34, ch_03_canonical_p07.json 14:34)
# and covers the four surviving breaches in the 2026-08-03 certification report.
#
# Three of the four are the SAME family: a clock quantity written into band prose when the
# band already carries its own `minutes`. Those are pure deletions of the quantity — the
# activity, the grouping and the output all stand. The fourth is a forward reference.
# ── v1.2 ADDITIONS, 2026-08-03 (ARV-D-026) ──────────────────────────────────────
# Four breaches found at C3 that the 18:07 pass never saw, because register_scan had no
# pattern for their phrasing: a RANGED clock quantity ("for two to three minutes" — the
# scanner matches "for two minutes") and three forward references in prose the pattern list
# did not cover. The patterns are added to register_scan.py in the same change, so the next
# library is gated on them rather than found by hand. The p10 U1 "the three functions the
# whole chapter unpacks" borderline is deliberately NOT repaired (founder ruling, same day):
# read as orienting prose about the chapter as an object, not a pointer to a later unit.
REPAIRS = {
    "ch_03_canonical_p07.json": [
        (5, "band:3",
         " This bridges toward the climate change and Punjab floods sections that follow.", "",
         "register/forward",
         "found at C8 by reading the LAST sitting of the 5-period serve, where this unit lands "
         "last and the sentence is simply false; at 6 it is half false (the floods section is "
         "dropped). The discussion it closes — monsoon variability as both sustenance and risk — "
         "is complete without it, so the trailing sentence goes whole"),
    ],
}


def _get_set(unit, locator, new=None):
    """Read (new=None) or write the located string on a unit."""
    if locator == "teacher_notes":
        if new is None:
            return unit.get("teacher_notes", "")
        unit["teacher_notes"] = new
    elif locator.startswith("band:"):
        b = unit["time_bands"][int(locator.split(":")[1])]
        if new is None:
            return b.get("activity", "")
        b["activity"] = new
    elif locator.startswith("homework:"):
        i = int(locator.split(":")[1])
        if new is None:
            return unit["homework"][i]
        unit["homework"][i] = new
    else:
        raise SystemExit(f"unknown locator {locator}")
    return None


def apply_file(fname, edits, dry):
    path = LIB / fname
    if not path.is_file():
        raise SystemExit(f"missing: {path}")
    plan = json.loads(path.read_text(encoding="utf-8"))
    units = {u["period_number"]: u for u in plan["result"]["lesson_plan"]["periods"]}
    before = len([h for h in scan_plan(plan) if h["ban"]])
    done = []
    for unit_no, loc, old, new, rule, note in edits:
        u = units.get(unit_no)
        if u is None:
            raise SystemExit(f"{fname}: no unit {unit_no}")
        cur = _get_set(u, loc)
        if old not in cur:
            raise SystemExit(
                f"{fname} U{unit_no} {loc}: declared text not found — the artefact has changed "
                f"since this repair was written. Re-read it, do not force.\n  wanted: {old!r}")
        if not dry:
            _get_set(u, loc, cur.replace(old, new, 1))
        done.append({"unit": unit_no, "field": loc, "rule": rule,
                     "removed": old.strip(), "replaced_with": new.strip(), "note": note})
    after_hits = [h for h in scan_plan(plan) if h["ban"]]
    if not dry:
        gc = plan.setdefault("genon_canonical", {})
        gc.setdefault("repairs", []).append({
            "at": datetime.now().isoformat(timespec="seconds"),
            "tool": "genon/repair_register.py v1.2",
            "reason": "register backfill (founder ruling 2026-08-02; testing.md C3 / ARV-D-011..013, ARV-D-026)",
            "edits": done,
            "ban_hits_before": before, "ban_hits_after": len(after_hits),
        })
        path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    return before, len(after_hits), done, plan


def main():
    dry = "--apply" not in sys.argv
    if not dry:
        BACKUP.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        for fname in REPAIRS:
            shutil.copy2(LIB / fname, BACKUP / f"{fname[:-5]}_{ts}.json")
        print(f"backed up {len(REPAIRS)} file(s) -> {BACKUP.relative_to(REPO)}/")
    total_after = 0
    for fname, edits in REPAIRS.items():
        before, after, done, plan = apply_file(fname, edits, dry)
        total_after += after
        print(f"\n=== {fname} — {len(done)} edit(s); ban hits {before} -> {after}"
              f"{' (DRY RUN, nothing written)' if dry else ''}")
        for d in done:
            print(f"  U{d['unit']:<3} {d['field']:<16} [{d['rule']}]")
            print(f"        - {d['removed']}")
            if d['replaced_with']:
                print(f"        + {d['replaced_with']}")
        if after:
            report([h for h in scan_plan(plan) if h["ban"]], f"{fname} SURVIVING")
    print(f"\nTOTAL surviving ban hits across the library: {total_after}")
    # A repaired canonical invalidates every plan derived from it (ARV-D-034): the serve cache
    # keys on the canonical's ledger_ts, which a repair does not change, so a stale plan would
    # otherwise keep being served. Rebuilding one costs ~11 ms.
    if not dry:
        purge("social_sciences", "ix", 3, reason="genon/repair_register.py")
    if dry:
        print("dry run — re-run with --apply to write.")
    return 1 if total_after else 0


if __name__ == "__main__":
    sys.exit(main())
