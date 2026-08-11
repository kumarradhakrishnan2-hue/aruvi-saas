#!/usr/bin/env python3
"""recover_from_raw.py — re-parse and install a canonical whose RAW output is on disk.

    python3 genon/recover_from_raw.py genon/out/canonical/mathematics/iii/ch_05_20260811_110409_raw.txt

WHY THIS EXISTS (2026-08-11, S8's C1).
`generate_canonical.py` writes the model's raw output to disk BEFORE parsing it
(`:457-458`). So a run that streams to completion and then fails to parse has already
bought everything it needed — the text is there, whole. Until now there was no way to
use it: the only path back was `--redo`, which pays the full price a second time for
output already in hand. maths III ch 5's 11-period compact died on the 10-repair bound
with ₹40.72 spent and a complete 96 KB file sitting in `genon/out/canonical/`.

This script is the deterministic half of `generate_canonical.py` run on its own: strip
fences → the SAME bounded naked-quote repair → the SAME `validate()` → the SAME
`install_canonical()`. It calls no API and costs nothing. It is not a new code path —
every function it uses is imported from `generate_canonical`, so a fix there fixes this
too, and the two can never drift.

WHAT IT DELIBERATELY DOES NOT DO. It does not re-run the model, does not touch the
ledger's cost columns (the money was already logged by the run that earned it), and does
not skip the validator: findings ride along in `genon_canonical.validation` exactly as
they would have. A recovered file is byte-for-byte what the original run would have
installed had the bound been right.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
# BOTH paths: the repo root for `genon.*`, and genon/ itself because
# generate_canonical imports its siblings as top-level modules (`import prompt_assembly`).
# Running this file as a script gets genon/ for free; being IMPORTED does not.
for _p in (str(HERE.parent), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# THE PARSER IS IMPORTED, NEVER COPIED. The first draft of this file held a hand-copy of
# generate_canonical's repair loop with a comment claiming it was "byte-identical" — which
# is a promise a copy cannot keep. `parse_with_repair` was extracted the same day so that
# the live path and the recovery path are literally the same function: a change to the
# bound, the span, or the repair itself reaches both, or neither.
from genon.generate_canonical import (  # noqa: E402
    install_canonical, parse_with_repair, validate,
)

# Kept as a name so existing callers/tests referring to `repair_parse` keep working.
repair_parse = parse_with_repair


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("raw", type=Path, help="the *_raw.txt written by the failed run")
    ap.add_argument("--dry-run", action="store_true",
                    help="parse and validate, print the verdict, install nothing")
    a = ap.parse_args()

    raw_path = a.raw.resolve()
    if not raw_path.is_file():
        raise SystemExit(f"no such raw file: {raw_path}")

    # subject/grade/ch/ts all come off the path the generator itself chose, so a
    # mistyped argument cannot install a plan into the wrong chapter.
    #   genon/out/canonical/<subject>/<grade>/ch_NN[_tag]_<TS>_raw.txt
    grade_folder = raw_path.parent.name
    subject_folder = raw_path.parent.parent.name
    m = re.match(r"ch_(\d+)(?:_.*?)?_(\d{8}_\d{6})_raw\.txt$", raw_path.name)
    if not m:
        raise SystemExit(f"cannot read chapter/timestamp from {raw_path.name}")
    ch, ts = int(m.group(1)), m.group(2)

    full = raw_path.read_text(encoding="utf-8")
    parsed, problems, repairs = repair_parse(full)
    print(f"raw      : {raw_path.relative_to(HERE.parent)}  ({len(full):,} chars)")
    print(f"chapter  : {subject_folder} · {grade_folder} · ch {ch} · ledger_ts {ts}")
    if repairs:
        print(f"repaired : {len(repairs)} naked inner quote(s) — "
              + "; ".join(repr(r) for r in repairs[:3]) + (" …" if len(repairs) > 3 else ""))
    if parsed is None:
        for p in problems:
            print(f"  ⚠ {p}")
        raise SystemExit("NOT RECOVERABLE — the raw does not parse even after repair.")

    # The period count and duration are properties of the artefact, read from it rather
    # than re-derived, so a recovery cannot silently install against the wrong schedule.
    periods = (parsed.get("lesson_plan") or {}).get("periods") or []
    count = len(periods)
    durations = {p.get("period_duration_minutes") for p in periods}
    if len(durations) != 1:
        raise SystemExit(f"refusing to install: mixed durations {durations} (A1 requires one row)")
    duration = durations.pop()
    variant_arg = None
    top = int(round(count))
    print(f"parsed   : {count} periods × {duration} min")

    problems = validate(parsed, count, False)
    status = "ok" if not problems else "problems"
    print(f"validate : {status}")
    for p in problems:
        print(f"  ⚠ {p}")

    # Is this the standard canonical or a compact? The master plan's counts settle it —
    # the top is the largest, anything below it installs under its own _pNN name.
    mp = json.loads((HERE.parent / "data/content/allocation_norms/master_plan.json")
                    .read_text(encoding="utf-8"))
    klass = {"iii": "III", "iv": "IV", "v": "V", "vi": "VI", "vii": "VII",
             "viii": "VIII", "ix": "IX", "x": "X"}[grade_folder]
    row = next(c for c in mp["combos"][f"{subject_folder}|{klass}"]["chapters"]
               if c["chapter"] == ch)
    counts = (row.get("canonical_plan") or {}).get("counts") or []
    if counts and count != max(counts):
        variant_arg = count
    if counts and count not in counts:
        print(f"  ⚠ {count} is not one of this chapter's canonical counts {counts} — "
              f"installing anyway, but check the brief that produced it")
    print(f"install  : {'compact p%02d' % variant_arg if variant_arg else 'standard canonical'}")

    if a.dry_run:
        print("\n--dry-run: nothing written.")
        return 0

    const_label = f"recovered from raw {raw_path.name}"
    dest = install_canonical(parsed, subject_folder, grade_folder, ch, ts,
                             duration, count, const_label, status, problems,
                             variant=variant_arg)
    print(f"installed: {dest}")
    print("\nThe money for this artefact was logged by the run that earned it; "
          "nothing is added to the cost columns here.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
