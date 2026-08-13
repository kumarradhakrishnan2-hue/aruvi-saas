#!/usr/bin/env python3
"""borrowed_seams.py — enumerate the X−1 → X joins that F1 actually has to read.

FOUNDER, 2026-08-13, and it is the whole point of this file: **only a GENUINELY BORROWED
Xth unit is at risk.** When the Xth slot is filled from the plan being served — a
self-fill, which the e14 tie-break makes the COMMON case, since a plan's own candidate
wins every tie it enters — the borrowed unit's priors are that plan's own earlier units.
There is no foreign prior, so there is no seam to inspect, and reading it is work that
cannot find anything. `serve.py` already carries the distinction as `slot_fill.self_fill`;
nothing was reading it.

WHAT THIS CHANGES ABOUT F1. It was written as "sample the batch, record the rate". Once
the population is only the cross-canonical borrows, it is small enough to enumerate and
read in FULL, so there is no sample and no rate to defend — which is strictly better than
a defensible sample. What stays with the founder is the ruling on what is found and the
fix; what moves is the reading.

    python3 genon/borrowed_seams.py the_world_around_us iii iv v      # enumerate
    python3 genon/borrowed_seams.py the_world_around_us iii --dump 9  # read one seam in full

Per chapter it sweeps X across [floor − 2 … top + 2] at the class-standard duration, and
keeps a row only where `slot_fill.borrowed_from` names a canonical OTHER than the one
serving. Identity, truncation, surrender and self-fill produce nothing.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

from aruvi_core.genon import compile_stream, serve_plan                 # noqa: E402
from api.data import standard_duration_minutes                          # noqa: E402

SAVED = REPO / "data" / "content" / "saved_plans"


def library(subject, grade, ch):
    """Every canonical of a chapter, compiled, top first."""
    d = SAVED / subject / grade
    files = sorted(d.glob(f"ch_{ch:02d}_canonical*.json"))
    out = []
    for p in files:
        try:
            out.append((p.name, compile_stream(json.loads(p.read_text()))))
        except Exception as e:                                          # noqa: BLE001
            print(f"  ERR {p.name}: {e}", file=sys.stderr)
    out.sort(key=lambda t: -len(t[1]["units"]))
    return out


def seams(subject, grade, ch, duration):
    """Rows for every X whose Xth unit is borrowed from ANOTHER canonical."""
    lib = library(subject, grade, ch)
    if not lib:
        return []
    streams = [s for _, s in lib]
    counts = sorted((len(s["units"]) for s in streams), reverse=True)
    rows = []
    for x in range(max(1, counts[-1] - 2), counts[0] + 3):
        try:
            res = serve_plan(streams, [(duration, x)])
        except Exception as e:                                          # noqa: BLE001
            rows.append({"x": x, "error": str(e)})
            continue
        g = res["genon"]
        f = g.get("slot_fill") or {}
        if not f.get("borrowed_from") or f.get("self_fill"):
            continue                       # identity / truncation / surrender / self-fill
        periods = res["result"]["lesson_plan"]["periods"]
        served = [p for p in periods if not p.get("unscheduled")]
        if len(served) < 2:
            continue
        rows.append({
            "x": x, "mode": f.get("mode"), "fill_class": f.get("fill_class"),
            "chosen": g.get("variant_used"), "lender": f.get("borrowed_from"),
            "library": counts, "sittings": len(served),
            "prev": served[-2], "last": served[-1],
            "overlap": f.get("overlap_sections") or [],
            "uncovered": f.get("uncovered_sections") or [],
        })
    return rows


def _line(subject, grade, ch, r):
    if "error" in r:
        return f"  ix ch{ch:02d} X={r['x']:<3} ERROR {r['error']}"
    return (f"  {grade}/ch{ch:02d} X={r['x']:<3} {r['mode']}"
            f"/{r['fill_class'] or '-':<8} chosen {r['chosen']:<3} <- lender {r['lender']:<3} "
            f"lib {r['library']}   U{r['prev'].get('period_number')}→U{r['last'].get('period_number')}"
            f"  «{(r['last'].get('activity_title') or '')[:52]}»")


def dump(r):
    """Sitting X−1 and sitting X in full, consecutively, as the teacher meets them."""
    for tag, p in (("X−1 (the class's own last lesson)", r["prev"]),
                   ("X   (the BORROWED lesson)", r["last"])):
        print("\n" + "─" * 78)
        print(f"{tag}  ·  sitting {p.get('period_number')}  ·  {p.get('activity_title')}")
        print(f"anchor: {p.get('section_anchor')!r}   synthesis: {p.get('synthesis')}")
        note = p.get("teacher_notes") or p.get("teacher_facilitation_note") or ""
        if note:
            print(f"\nTEACHER NOTE\n  {note}")
        if p.get("materials"):
            print(f"\nMATERIALS\n  {p['materials']}")
        for i, b in enumerate(p.get("time_bands") or p.get("phases") or []):
            print(f"\nBAND[{i}] {b.get('minutes') or b.get('time')}\n  "
                  f"{b.get('activity') or b.get('description')}")
        if p.get("homework"):
            print(f"\nHOMEWORK\n  {p['homework']}")


def main(argv):
    subject, grades = argv[0], [g for g in argv[1:] if not g.startswith("--")]
    want = None
    if "--dump" in argv:
        want = int(argv[argv.index("--dump") + 1])
    total = borrowed = 0
    for grade in grades:
        d = SAVED / subject / grade
        chs = sorted({int(re.search(r"ch_(\d+)", p.name).group(1))
                      for p in d.glob("ch_*_canonical*.json")})
        dur = standard_duration_minutes(grade, subject)
        for ch in chs:
            total += 1
            rows = seams(subject, grade, ch, dur)
            borrowed += len(rows)
            if rows:
                print(f"\n{subject} {grade} ch {ch:02d}  ({dur} min)")
                for r in rows:
                    print(_line(subject, grade, ch, r))
                    if want is not None and ch == want:
                        dump(r)
    print(f"\n{'='*78}\nchapters swept {total} · cross-canonical borrowed seams {borrowed}")


if __name__ == "__main__":
    main(sys.argv[1:])
