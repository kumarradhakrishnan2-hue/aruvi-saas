#!/usr/bin/env python3
"""repair_anchors.py — repair V2 section-anchor SERIALIZATION in an authored library (v1.0, 2026-08-03).

WHY THIS EXISTS, AND WHY IT IS NOT repair_register.py. The SS·IX ch 3 library (12/10/7) was
certified against a CORRUPTED registry: all three canonicals wrote the same two-section anchor
joined with a semicolon —

    "Weather and Climate; Elements of Weather and Climate"

— where V2 mandates " / " (serve._ANCHOR_JOINER). A semicolon is not split, so the string
entered section_registry as ONE opaque section. The derived registry still counted 9 entries
(which is why `registry_sections: 9` passed), but it carried a phantom composite at index 3,
had no standalone "Weather and Climate", and displaced "Elements of Weather and Climate" two
slots past its true position. Consequences: p10 was quarantined for a first-visit-order
"skip" that does not exist; X=8 reported a phantom dropped section; X=9 served a redundant
re-teach where the Case 1 synthesis belongs.

repair_register.py's docstring draws the line this script respects: STRUCTURAL and
PEDAGOGICAL defects — including "an anchor that names the wrong section" — are out of scope
there, because repairing them as text hygiene would launder content changes. This is neither.
The anchors name the RIGHT sections in the RIGHT order; only the DELIMITER between them is
wrong. Nothing about what is taught changes. That is a serialization repair, and it gets its
own tool so the two classes of edit never blur.

SAME SAFETY DOCTRINE as repair_register.py:
  * every edit is a STATED (old -> new) pair. No rule-based rewrite, no model authors text.
    A general "replace any separator with ' / '" normalizer is deliberately NOT what this
    does — that is a generated rewrite, and it would silently "fix" anchors nobody read.
  * if `old` is not found verbatim the file is left untouched and the run fails loudly.
  * the artefact records what was done in genon_canonical.repairs[], so corpus statistics can
    still separate generation quality from repair quality.
  * the registry is re-derived and printed after the write, because the whole point of the
    repair is the registry — a repair that leaves it wrong must be visible immediately.

    python3 genon/repair_anchors.py           # dry run: show the declared edits + both registries
    python3 genon/repair_anchors.py --apply   # back up, apply, record, re-derive
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

from purge_derived import purge                                  # noqa: E402

from aruvi_core.genon import compile_stream                        # noqa: E402
from aruvi_core.genon.serve import (                               # noqa: E402
    _norm, is_synthesis_unit, section_registry, unit_range,
)

LIB = REPO / "data" / "content" / "saved_plans" / "social_sciences" / "ix"
BACKUP = REPO / "backup" / "anchor_repair"

# ── the declared edits ───────────────────────────────────────────────────────────
# file -> [(unit_number, old_anchor, new_anchor, rule_broken, note)]
#
# Note p07 U3: the author wrote the semicolon composite AND then appended the standalone
# section — evidence the two sections were understood as two. A naive ";"->" / " swap would
# leave "Elements of Weather and Climate" duplicated in the anchor; the declared repair emits
# the clean two-section form instead. unit_range would have tolerated the duplicate (it takes
# min/max), but a duplicate anchor is not what V2 says and the next reader would trip on it.
REPAIRS = {
    "ch_03_canonical.json": [
        (4,
         "Weather and Climate; Elements of Weather and Climate",
         "Weather and Climate / Elements of Weather and Climate",
         "V2/joiner",
         "two-section unit; ';' is not the mandated joiner, so the registry read it as one "
         "opaque section. Sections named and their order are unchanged."),
    ],
    "ch_03_canonical_p10.json": [
        (4,
         "Weather and Climate; Elements of Weather and Climate",
         "Weather and Climate / Elements of Weather and Climate",
         "V2/joiner",
         "same slip as the standard canonical. THIS is the edit that clears p10's false "
         "first-visit-order failure: its U9 is an ordinary backward revisit of Elements "
         "(legal under the §4 frontier rule), not a skip."),
    ],
    "ch_03_canonical_p07.json": [
        (3,
         "Weather and Climate; Elements of Weather and Climate / Elements of Weather and Climate",
         "Weather and Climate / Elements of Weather and Climate",
         "V2/joiner",
         "semicolon composite plus a redundant repeat of the second section; the clean "
         "two-section form is emitted. Unit coverage is unchanged (sections 3-4)."),
    ],
}


def registry_of_library():
    """Compile the library and derive the registry from the top canonical, exactly as
    build_library.certify does — so what is printed here is what certification will see."""
    paths = [LIB / "ch_03_canonical.json"] + sorted(LIB.glob("ch_03_canonical_p*.json"))
    lib = [(p.name, compile_stream(json.loads(p.read_text(encoding="utf-8"))))
           for p in paths if p.is_file()]
    lib.sort(key=lambda t: -len(t[1]["units"]))
    reg = section_registry(lib[0][1])
    return lib, reg


def first_visit_check(lib, reg):
    ridx = {_norm(a): i for i, a in enumerate(reg)}
    out = []
    for name, s in lib:
        seen, bad = -1, []
        for u in [x for x in s["units"] if not is_synthesis_unit(x)]:
            r = unit_range(u, ridx)
            if r is None:
                bad.append((u["unit"], "anchor not in registry"))
                continue
            if r[1] > seen:
                if r[0] > seen + 1:
                    bad.append((u["unit"], f"skips s{seen + 1}"))
                seen = r[1]
        out.append((name, bad, seen, len(reg) - 1))
    return out


def show_registry(label):
    lib, reg = registry_of_library()
    print(f"\n{label} — registry ({len(reg)} sections):")
    for i, s in enumerate(reg):
        print(f"    {i}  {s}")
    print(f"{label} — first-visit order:")
    for name, bad, seen, last in first_visit_check(lib, reg):
        print(f"    {name:<28} {'OK' if not bad else 'FAIL ' + str(bad):<34} "
              f"frontier {seen}/{last}")
    return reg


def apply_file(fname, edits, dry):
    path = LIB / fname
    if not path.is_file():
        raise SystemExit(f"missing: {path}")
    plan = json.loads(path.read_text(encoding="utf-8"))
    units = {u["period_number"]: u for u in plan["result"]["lesson_plan"]["periods"]}
    done = []
    for unit_no, old, new, rule, note in edits:
        u = units.get(unit_no)
        if u is None:
            raise SystemExit(f"{fname}: no unit {unit_no}")
        cur = u.get("section_anchor") or ""
        if cur != old:
            raise SystemExit(
                f"{fname} U{unit_no} section_anchor: declared text not found — the artefact "
                f"has changed since this repair was written. Re-read it, do not force.\n"
                f"  wanted: {old!r}\n  found : {cur!r}")
        if not dry:
            u["section_anchor"] = new
        done.append({"unit": unit_no, "field": "section_anchor", "rule": rule,
                     "removed": old, "replaced_with": new, "note": note})
    if not dry:
        gc = plan.setdefault("genon_canonical", {})
        gc.setdefault("repairs", []).append({
            "at": datetime.now().isoformat(timespec="seconds"),
            "tool": "genon/repair_anchors.py v1.0",
            "reason": "V2 section-anchor joiner repair (';' read as one opaque registry "
                      "section; corrupted the derived registry, falsely quarantined p10, "
                      "and mis-served X=8/X=9)",
            "edits": done,
        })
        path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    return done


def main():
    dry = "--apply" not in sys.argv
    show_registry("BEFORE")
    if not dry:
        BACKUP.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        for fname in REPAIRS:
            shutil.copy2(LIB / fname, BACKUP / f"{fname[:-5]}_{ts}.json")
        print(f"\nbacked up {len(REPAIRS)} file(s) -> {BACKUP.relative_to(REPO)}/")
    print()
    for fname, edits in REPAIRS.items():
        done = apply_file(fname, edits, dry)
        print(f"=== {fname} — {len(done)} edit(s)"
              f"{' (DRY RUN, nothing written)' if dry else ''}")
        for d in done:
            print(f"  U{d['unit']:<3} section_anchor   [{d['rule']}]")
            print(f"        - {d['removed']}")
            print(f"        + {d['replaced_with']}")
    if dry:
        print("\ndry run — re-run with --apply to write.")
        return 0
    # A repaired canonical invalidates every plan derived from it (ARV-D-034) — the serve
    # cache keys on the canonical's ledger_ts, which a repair does not move.
    purge("social_sciences", "ix", 3, reason="genon/repair_anchors.py")
    reg = show_registry("AFTER")
    bad = [b for _, b, _, _ in first_visit_check(*registry_of_library()) if b]
    print(f"\nregistry is {len(reg)} sections; "
          f"{'ALL plans pass first-visit order.' if not bad else 'FAILURES REMAIN — read above.'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
