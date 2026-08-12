#!/usr/bin/env python3
"""repair_item_type.py — declared correction of a mislabelled assessment `question_type` (v1.0, 2026-08-12).

    python3 genon/repair_item_type.py --list     # show the declared repairs, change nothing
    python3 genon/repair_item_type.py            # apply them

WHY THIS EXISTS. ARV-D-120: the assessment constitutions select a question type from a TABLE
whose left column is a different enumeration (TWAU's `dominant_mode`, science's mode, SS's
weight tier). A model that copies the left column emits a value that looks like data because
it IS data — from the wrong column. The item is otherwise a perfectly good item: only the
label is wrong. Regenerating a whole canonical to fix one string is not worth the money, and
hand-editing the artefact is what every other repair tool in this folder exists to avoid.

WHAT IT WILL NOT DO, and this is the point of a DECLARED repair:
  * it never guesses the correct type. Every repair is written out below by a human with its
    evidence, and the script refuses unless what is on disk matches the declared `frm`;
  * it CROSS-CHECKS the target against the item's own `guide` block. A TWAU item's guide is
    keyed by its own question_type (assessment constitution Rule 9), so a mislabelled item
    carries the right answer in the key: `guide.SCR` on an item claiming `HI` says SCR. If
    the guide key and the declared target disagree, the repair is refused;
  * it touches ONE field. No text, no options, no reordering.

QUARANTINE. `build_library.py` moves a failed canonical to `backup/quarantine/` — so the file
this repairs is usually NOT in the library. When the library copy is missing, the newest
quarantined copy for that chapter is repaired and INSTALLED back under its proper name.

AND IT PURGES (ARV-D-034, and the 2026-08-11 lesson that `repair_unit_order.py` was the one
repair tool that forgot): an in-place repair does not change `canonical_version`, so any plan
already served from the old bytes keeps the cache key it was built with. Derived plans for
this chapter are removed; the next request rebuilds in milliseconds.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

from aruvi_core.genon.carriers import raw_item_list                # noqa: E402
from purge_derived import purge                                    # noqa: E402

LIB = REPO / "data" / "content" / "saved_plans"
QUAR = REPO / "backup" / "quarantine"

# ── THE DECLARED REPAIRS ────────────────────────────────────────────────────────
# subject, grade, chapter, unit_ref, frm, to, evidence (why `to` is the right answer).
DECLARED = [
    dict(subject="the_world_around_us", grade="iv", chapter=6, unit=13,
         frm="HI", to="SCR",
         evidence="ARV-D-120 recurrence, wave 1 of S5's corpus (2026-08-12). 'HI' is the "
                  "period's dominant_mode (Hands-on Investigation), copied from the LEFT "
                  "column of assessment v1.5 Rule 3's table; the row reads "
                  "'HI / CG-6 inquiry steps ... | SCR'. The item is an SCR in every other "
                  "respect: guide key SCR with two expected_elements, options [], look_for "
                  "[], task/scaffold '', performance_task false, and a populated stem "
                  "(Nila's three nights of sleep data). Founder authorised the back-fill "
                  "rather than a regeneration."),
]


def newest_quarantined(subject: str, grade: str, ch: int) -> Path | None:
    d = QUAR / subject / grade
    if not d.is_dir():
        return None
    hits = sorted(d.glob(f"ch_{ch:02d}_canonical_*.json"))
    return hits[-1] if hits else None


def guide_key(item: dict) -> str | None:
    g = item.get("guide")
    if isinstance(g, dict) and len(g) == 1:
        return next(iter(g))
    return None


def apply_one(rep: dict, dry: bool) -> bool:
    subject, grade, ch = rep["subject"], rep["grade"], rep["chapter"]
    target = LIB / subject / grade / f"ch_{ch:02d}_canonical.json"
    source, from_quarantine = target, False
    if not target.is_file():
        q = newest_quarantined(subject, grade, ch)
        if q is None:
            print(f"  REFUSED {subject}/{grade} ch {ch}: no library copy and none quarantined")
            return False
        source, from_quarantine = q, True
        print(f"  (library copy absent — repairing the quarantined file {q.name})")

    doc = json.loads(source.read_text(encoding="utf-8"))
    res = doc.get("result", doc)
    hits = [it for it in raw_item_list(res)
            if rep["unit"] in [int(x) for x in (it.get("period_ref") or [])
                               if str(x).isdigit()]
            or str(it.get("period_ref")) == str(rep["unit"])]
    hits = [it for it in hits if str(it.get("question_type")) == rep["frm"]]
    if len(hits) != 1:
        print(f"  REFUSED {subject}/{grade} ch {ch} unit {rep['unit']}: expected exactly one "
              f"item carrying question_type {rep['frm']!r}, found {len(hits)}")
        return False
    item = hits[0]
    gk = guide_key(item)
    if gk != rep["to"]:
        print(f"  REFUSED {subject}/{grade} ch {ch} unit {rep['unit']}: guide key {gk!r} does "
              f"not agree with the declared target {rep['to']!r}")
        return False

    print(f"  {subject}/{grade} ch {ch} unit {rep['unit']}: question_type "
          f"{rep['frm']!r} -> {rep['to']!r}  (guide key {gk!r} agrees)")
    if dry:
        return True

    item["question_type"] = rep["to"]
    doc.setdefault("genon_canonical", {}).setdefault("repairs", []).append({
        "tool": "repair_item_type.py", "at": datetime.now().isoformat(timespec="seconds"),
        "unit": rep["unit"], "field": "question_type",
        "from": rep["frm"], "to": rep["to"], "evidence": rep["evidence"],
    })
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  written: {target.relative_to(REPO)}"
          + ("  (restored from quarantine)" if from_quarantine else ""))
    gone = purge(subject, grade, ch, reason="repair_item_type")
    print(f"  derived plans purged: {len(gone)}" + (f" — {gone}" if gone else ""))
    return True


def main() -> int:
    dry = "--list" in sys.argv
    print(f"repair_item_type.py — {len(DECLARED)} declared repair(s)"
          + ("  [--list: nothing will be written]" if dry else ""))
    ok = all(apply_one(r, dry) for r in DECLARED)
    if not dry and ok:
        print("\nNext: re-certify the chapter(s), e.g.\n"
              "  python3 genon/build_library.py the_world_around_us iv 6 --certify-only")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
