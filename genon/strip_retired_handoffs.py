#!/usr/bin/env python3
"""strip_retired_handoffs.py — remove `role_handoff` / `unit_handoff` from installed canonicals.

    python3 genon/strip_retired_handoffs.py            # report only
    python3 genon/strip_retired_handoffs.py --write    # strip them

FOUNDER RULING 2026-08-13, at S10's C3: both keys are RETIRED and are to be removed
everywhere they are found.

WHAT THEY WERE. `role_handoff` (LP Rule 15) classified every band as hook / development /
consolidation; `unit_handoff` (Rule 16) gave a title and a note for each adjacent pair of
units. Both fed the DETERMINISTIC PARTITION ENGINE — the thing that cut plans below the unit
and had to stitch the seams. That engine was retired on 2026-07-31 and the variant-canonical
serve engine replaced it (`docs/variant_canonical_architecture.md` §1 records why); Amendments
A2/A3/A4 were cancelled with it, and `docs/testing.md` §1 lists `role_handoff` and
`unit_handoff` among the things "never tested again; never reintroduced".

SO WHY WERE THEY STILL IN THE FILES. Two lines in `generate_canonical.py` wrote
`parsed.get("role_handoff", {})` into every saved canonical, and the output sketch in
`prompt_assembly.py` still asked the model for `"role_handoff": <per LP Constitution>`.
No live constitution has defined either since the cancellation, so the model had nothing to
emit and the `{}` default won every time. The result: a retired declaration, present and
empty, in the one artefact class that reaches the cloud. Both sources were closed on
2026-08-13; this pass cleans what they already wrote.

WHY THIS IS SAFE, and why it does NOT purge derived plans (the usual repair-tool duty):

  * NOTHING IS LOST. Measured before writing: of 280 installed canonicals carrying either
    key, ZERO are populated. Every one is `{}`. The script refuses to strip a populated key
    anyway, so a prototype-era plan that really does carry role data cannot be damaged.
  * THE SERVED BYTES ARE IDENTICAL. `compile.py` reads
    `result.get("role_handoff") or plan.get("role_handoff") or {}` — absent and `{}` give the
    same `{}` — and `role_provenance` branches on truthiness, where `{}` is already falsy.
  * THE PLAN KEY DOES NOT MOVE. `api/data.canonical_version` keys off `genon_canonical.
    ledger_ts`, not a content hash, so a cached serve still resolves to the same filename.

That combination is why `purge_derived` is deliberately NOT called here. The standing rule
(ARV-D-034) is that a repair changing what a serve produces must delete the chapter's derived
plans; this one provably changes nothing a serve produces, and purging would throw away real
teachers' plans to no end. If you extend this script to touch anything a serve READS, wire
purge_derived in first.

READERS ARE LEFT ALONE ON PURPOSE. `aruvi_core/genon/compile.py` and `api/data.py` still read
both keys where they are POPULATED — prototype-era saved plans and the v1.3 Rule-16 back-fill
corpus. Those files are outside `data/content/saved_plans/*/*/ch_*canonical*.json` and are not
touched here; deleting the readers would break them.
"""
from __future__ import annotations

import glob
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
KEYS = ("role_handoff", "unit_handoff")
WRITE = "--write" in sys.argv


def main() -> int:
    files = sorted(glob.glob(str(ROOT / "data/content/saved_plans/*/*/ch_*canonical*.json")))
    empty = populated = touched = 0
    refused: list[str] = []

    for p in files:
        doc = json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
        res = doc.get("result")
        if not isinstance(res, dict):
            continue
        present = [k for k in KEYS if k in res]
        if not present:
            continue
        live = [k for k in present if res[k]]
        if live:
            populated += len(live)
            refused.append(f"{pathlib.Path(p).relative_to(ROOT)}: {live} POPULATED — left alone")
            present = [k for k in present if not res[k]]
        if not present:
            continue
        empty += len(present)
        if WRITE:
            for k in present:
                res.pop(k, None)
            pathlib.Path(p).write_text(
                json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
            touched += 1

    print(f"canonicals scanned          : {len(files)}")
    print(f"empty retired keys found    : {empty}")
    print(f"POPULATED keys (never touched): {populated}")
    for r in refused[:20]:
        print("   " + r)
    if WRITE:
        print(f"files rewritten             : {touched}")
        print("derived plans NOT purged — the served bytes are unchanged (see the docstring).")
    else:
        print("\nreport only — pass --write to strip them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
