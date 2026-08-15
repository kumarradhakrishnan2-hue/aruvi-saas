#!/usr/bin/env python3
"""F1 dossiers — for every cross-canonical borrowed seam, dump the ASSUMPTION SURFACE.

Built by SERVING the plan, not by guessing which unit was borrowed. `borrowed_seams.py`
identifies the seams; this re-serves each one and reads the result, so the Xth unit is the
one the engine actually chose and the X-1 prefix is the one the class actually met. (The
first cut of this script inferred the borrowed unit from the lender's last period, which is
right only for the synthesis modes and wrong for every `fill/*`.)

The F1 question is not "is this unit good" but "does it assume something the HOST class
never had". So the dossier is deliberately asymmetric:

  * the host prefix is summarised by unit TITLES only — that is what the class met, and it
    is the whole of what the borrowed unit is entitled to assume;
  * the borrowed Xth unit is dumped in FULL on every surface where an assumption can hide —
    teacher notes, MATERIALS, each band's text, homework. ARV-D-119's lesson: the
    dependency arrived through `materials`, not through the prose.

Read each against its SHORTEST prefix (the hardest case), per testing.md C8.

    python3 genon/out/f1_seam_dossiers.py english vi > /tmp/f1_vi.txt
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
SAVED = REPO / "data" / "content" / "saved_plans"

from aruvi_core.genon import compile_stream, serve_plan            # noqa: E402
# NOTE: serve_plan returns the FULL saved-plan envelope — the periods live at
# result.lesson_plan.periods, and below-floor serves carry unreached units in the
# same list flagged `unscheduled` (e09). Both matter here: reading an unscheduled
# unit as the borrowed Xth would invent a seam that no class ever meets.


def note_of(u):
    for f in ("teacher_notes", "teacher_facilitation_note"):
        if f in u:
            return u.get(f) or ""
    return ""


def seam_rows(subject, grade):
    out = subprocess.run([sys.executable, str(REPO / "genon" / "borrowed_seams.py"),
                          subject, grade], capture_output=True, text=True, cwd=REPO).stdout
    rows = []
    for line in out.splitlines():
        if " X=" not in line:
            continue
        p = line.split()
        rows.append((int(p[0].split("/ch")[1]), int(p[1].split("=")[1]), p[2]))
    return rows


def main():
    subject, grade = sys.argv[1], sys.argv[2]
    dur = {"vi": 40, "vii": 40, "viii": 45}[grade]
    for ch, x, mode in seam_rows(subject, grade):
        files = sorted((SAVED / subject / grade).glob(f"ch_{ch:02d}_canonical*.json"))
        streams = [compile_stream(json.loads(f.read_text())) for f in files]
        res = serve_plan(streams, [(dur, x)])
        per = [u for u in res["result"]["lesson_plan"]["periods"]
               if not u.get("unscheduled")]
        g = res.get("genon", {})
        sf = g.get("slot_fill") or {}
        borrowed, prefix = per[-1], per[:-1]
        print("\n" + "=" * 78)
        print(f"SEAM  {grade}/ch{ch:02d}  X={x}  {mode}  · chosen {sf.get('chosen')} "
              f"· borrowed_from {sf.get('borrowed_from')} · self_fill {sf.get('self_fill')}")
        print("-" * 78)
        print(f"HOST PREFIX — the {len(prefix)} sitting(s) this class actually had:")
        for u in prefix:
            print(f"   U{u['period_number']:<2} {u.get('activity_title', '?')}")
        print(f"\nBORROWED Xth UNIT — the class's LAST sitting:")
        print(f"   TITLE      {borrowed.get('activity_title')}")
        print(f"   ANCHOR     {borrowed.get('section_anchor')}")
        print(f"   MATERIALS  {borrowed.get('materials')}")
        print(f"   NOTES      {note_of(borrowed)}")
        for i, b in enumerate(borrowed.get("time_bands") or []):
            print(f"   BAND {i}     {b.get('activity')}")
        print(f"   HOMEWORK   {borrowed.get('homework')}")


if __name__ == "__main__":
    main()
