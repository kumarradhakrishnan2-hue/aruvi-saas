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

LIB = REPO / "data" / "content" / "saved_plans" / "social_sciences" / "ix"
BACKUP = REPO / "backup" / "register_repair"

# ── the declared edits ───────────────────────────────────────────────────────────
# file -> [(unit_number, field_locator, old, new, rule_broken, note)]
# field_locator: "teacher_notes" | "band:<index>" | "homework:<index>"
REPAIRS = {
    "ch_03_canonical.json": [
        (1, "band:3",
         " — framing what is to come.", ".",
         "register/forward",
         "trailing appositive dropped; the band still names all six structural elements"),
        (2, "band:3",
         " — a thread to pick up in the climate-change unit.", ".",
         "register/forward",
         "promise to a unit a compact variant may never serve"),
        (6, "teacher_notes",
         ", which the next unit develops mechanistically.", ".",
         "register/forward",
         "clause dropped; the confusion it introduces stands on its own"),
        (6, "band:3",
         " — a thread that the monsoon unit develops further.", ".",
         "register/forward",
         "trailing appositive dropped"),
        (6, "homework:0",
         ". Bring the log to the next unit and note which IMD season these days belong to.",
         ", and note which IMD season these days belong to.",
         "register/forward",
         "the classifying task is KEPT (it carries the cognitive floor); only the delivery "
         "instruction to a following unit goes. NOTE: the five-day span and U8's dependency on "
         "this homework are NOT repaired here — see ARV-D-012, human gate"),
        (8, "band:3",
         ", a point the climate-change unit will show is now under threat.", ".",
         "register/forward",
         "the synthesis itself is kept; only the forward promise goes"),
        (9, "teacher_notes",
         " The carbon-footprint activity distinguishes this unit from the next, which examines "
         "a specific crisis event rather than general causes and responses.", "",
         "register/forward",
         "whole sentence is about unit ORDER; notes remain 2 sentences (Rule 10 allows 2-3)"),
        (9, "band:3",
         " (C-4.6)", "", "rule10/ids", "competency code out of teacher-facing band text"),
        (9, "band:3",
         " (C-4.5)", "", "rule10/ids", "competency code out of teacher-facing band text"),
        (12, "teacher_notes",
         "Having worked through every section of the chapter, this unit asks",
         "This unit asks",
         "register/completion",
         "U12 is the fill ladder's prime borrow candidate; the completion claim is false the "
         "moment it is served into a shorter plan"),
    ],
    "ch_03_canonical_p09.json": [
        (5, "teacher_notes",
         ", previewing the inter-linkage work of the next unit.", ".",
         "register/forward", "trailing clause dropped"),
        (6, "band:3",
         ", connecting forward to the climate-change and Punjab-floods themes of later units.",
         ".",
         "register/forward", "trailing clause dropped"),
    ],
    "ch_03_canonical_p07.json": [
        (4, "band:2",
         " from the previous unit", "",
         "rule13/positional",
         "ADVISORY, not a ban (v1.10 legalised backward references) — but Rule 13 P3 keeps "
         "unit-to-unit linking in teacher_notes, and the distinction reads fine unqualified"),
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
            "tool": "genon/repair_register.py v1.0",
            "reason": "register backfill (founder ruling 2026-08-02; testing.md C3 / ARV-D-011..013)",
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
    if dry:
        print("dry run — re-run with --apply to write.")
    return 1 if total_after else 0


if __name__ == "__main__":
    sys.exit(main())
