#!/usr/bin/env python3
"""f1_transitions.py — the mechanical half of C8, run across a batch (F1).

    python3 genon/f1_transitions.py mathematics iii iv v --sample docs/testing_artefacts/f1_sample_*.txt
    python3 genon/f1_transitions.py mathematics iii 5 --x 12          # one transition

WHAT C8 ASKS. The serve engine fills slot X by BORROWING a unit — from the plan's own
successor, from another canonical, or (Case 1) the standard's closing synthesis. The
defect v2.0 was built to kill (ARV-D-023, ARV-D-025) is a borrowed unit that assumes
lessons the served class never had: the plan is section-complete on paper and jumpy in
the room. "Anchoring is not teaching."

WHAT THIS TOOL DOES AND DOES NOT DO. It does the part a machine can do without judgement:
serve at X, identify the borrowed unit and the units the serve WITHHELD, work out which
sections those withheld units were the FIRST to teach, and report whether the borrowed
unit's own text reaches for them. It does not decide whether a hit is a real breach —
a synthesis unit naming a section it is licensed to synthesise is fine, and a passing
mention of a shape name is not the same as assuming a technique. **The output is a
worklist for a reader, not a verdict**, which is the same contract `register_scan` has.

WHY THE WITHHELD SET IS THE RIGHT TARGET rather than "everything after X". A served plan
is a PREFIX plus a borrowed tail, so the units that exist-but-were-not-served are exactly
the content the class is missing while still meeting a unit written to follow them. That
set is `slot_fill.withheld_units` on a self-fill and the lender's un-served units on a
cross-canonical borrow.
"""
from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from aruvi_core.genon import compile_stream, serve_plan                # noqa: E402

PLANS = REPO / "data" / "content" / "saved_plans"


def library(subject: str, grade: str, ch: int):
    streams = [compile_stream(json.loads(Path(p).read_text(encoding="utf-8")))
               for p in sorted(glob.glob(str(PLANS / subject / grade / f"ch_{ch:02d}_canonical*.json")))]
    return sorted(streams, key=lambda s: -len(s["units"]))


def _units(plan):
    lp = (plan.get("result") or plan).get("lesson_plan") or plan.get("lesson_plan") or {}
    return lp.get("periods", [])


def _sections(unit) -> list:
    """Anchors, with COMPOUND forms split. An authored unit may anchor "S9 / S10"; the
    serve engine splits that into ["S9", "S10"] on the way out, so a naive comparison
    between a served unit and its own lender never matches — which is how the first run
    of this tool located the borrowed unit in only 1 of 4 spot-checks and then reported
    a confident zero over a set it had never looked at."""
    v = unit.get("section_refs") or unit.get("section_anchor") or []
    raw = [v] if isinstance(v, str) else list(v)
    out = []
    for item in raw:
        for part in re.split(r"\s*/\s*", str(item)):
            part = part.strip()
            if part and part not in out:
                out.append(part)
    return out


def _text(unit) -> str:
    """Everything a teacher reads in the unit, as one string."""
    parts = [unit.get("activity_title") or "", unit.get("teacher_notes") or ""]
    for b in unit.get("time_bands", []) or []:
        parts.append(b if isinstance(b, str) else (b.get("activity") or b.get("description") or ""))
    for h in unit.get("homework", []) or []:
        parts.append(h if isinstance(h, str) else (h.get("description") or ""))
    return "\n".join(str(p) for p in parts)


def transition(subject: str, grade: str, ch: int, x: int, duration: int = 40) -> dict:
    lib = library(subject, grade, ch)
    if not lib:
        return {"error": "no library"}
    served = serve_plan(lib, [(duration, x)])
    g = served.get("genon", {})
    sf = g.get("slot_fill") or {}
    units = _units(served)
    if not units:
        return {"error": "no units served"}
    borrowed = units[-1]

    # The lender: whichever canonical this serve drew its tail from.
    lender_n = sf.get("borrowed_from") or sf.get("rescued_from") or g.get("variant_used")
    lender = next((s for s in lib if len(s["units"]) == lender_n), None)

    # ── WHAT THE CLASS NEVER HAD ────────────────────────────────────────────────
    # `slot_fill.withheld_units` is populated ONLY on a synthesis borrow; on `fill` and
    # `complete_rescue` it is empty, so a first version of this tool compared against
    # nothing for 33 of 55 sampled transitions and reported a confident zero. The
    # general target is the same in every mode: the lender's units that come BEFORE the
    # borrowed one. Those are what the borrowed unit was written to follow, and the
    # served class met them only if its own prefix happened to teach the same sections.
    #
    # The borrowed unit is located in the lender by identity (title + anchors) rather
    # than by index, because the served plan renumbers its periods from 1.
    # TITLE ONLY. Anchors cannot be part of the key for the reason `_sections` records.
    def _key(u):
        return (u.get("activity_title") or "").strip()

    lender_units = lender["units"] if lender else []
    idx = next((i for i, u in enumerate(lender_units) if _key(u) == _key(borrowed)), None)
    predecessors = lender_units[:idx] if idx is not None else []

    withheld_idx = sf.get("withheld_units") or []
    if withheld_idx and lender:
        predecessors += [lender_units[i - 1] for i in withheld_idx
                         if 1 <= i <= len(lender_units)]

    # Sections the SERVED prefix taught, vs sections only the lender's predecessors teach.
    taught = {s for u in units[:-1] for s in _sections(u)}
    withheld_only = []
    for u in predecessors:
        for s in _sections(u):
            if s not in taught and s not in withheld_only:
                withheld_only.append(s)

    # Does the borrowed unit reach for any of them by name?
    body = _text(borrowed)
    reaches = [s for s in withheld_only if re.search(rf"\b{re.escape(str(s))}\b", body)]

    return {
        "chapter": f"{grade} ch{ch}", "X": x,
        "mode": sf.get("mode"), "self_fill": sf.get("self_fill"),
        "lender": lender_n, "stream": g.get("stream_source"),
        "withheld": withheld_idx,
        "served_sections": sorted(taught),
        "withheld_only_sections": withheld_only,
        "borrowed_unit": borrowed.get("activity_title"),
        "borrowed_sections": _sections(borrowed),
        "reaches_untaught": reaches,
        "dropped": sf.get("dropped_unit_count") or 0,
        "coverage_note": (served.get("result") or served).get("section_coverage_note"),
        "text": body,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("subject")
    ap.add_argument("rest", nargs="*")
    ap.add_argument("--sample")
    ap.add_argument("--x", type=int)
    ap.add_argument("--full", action="store_true", help="print the borrowed unit's text")
    a = ap.parse_args()

    jobs = []
    if a.sample:
        pat = re.compile(r"^\s*(M?)\s*(\w+)\s+ch(\d+)\s+X=(\d+)\s+(\S+)")
        for line in Path(sorted(glob.glob(a.sample))[-1]).read_text().splitlines():
            m = pat.match(line)
            if m:
                jobs.append((m.group(2), int(m.group(3)), int(m.group(4)), m.group(1) == "M"))
    else:
        jobs = [(a.rest[0], int(a.rest[1]), a.x, True)]

    flagged = 0
    print(f"{'ch':10} {'X':>3}  {'mode':16} {'lender':>6}  {'withheld':16} reaches-untaught")
    for grade, ch, x, mand in jobs:
        r = transition(a.subject, grade, ch, x)
        if "error" in r:
            print(f"  {grade} ch{ch} X={x}: {r['error']}")
            continue
        hit = r["reaches_untaught"]
        flagged += bool(hit)
        mark = "!!" if hit else ("M " if mand else "  ")
        print(f"{mark}{r['chapter']:9}{x:>3}  {str(r['mode']):16} {str(r['lender']):>6}  "
              f"{str(r['withheld'])[:15]:16} {hit if hit else '—'}")
        if a.full and hit:
            print("   borrowed:", r["borrowed_unit"])
            print("   " + r["text"][:700].replace("\n", "\n   "))
    print(f"\n{len(jobs)} transition(s) · {flagged} reach a section only the withheld units teach")
    print("A hit is a WORKLIST ENTRY, not a verdict — a synthesis unit is licensed to name "
          "what it synthesises. Read each one.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
