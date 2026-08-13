#!/usr/bin/env python3
"""S9 · english · preparatory — C6, the API serve checks, executed against a live API.

    python3 -m uvicorn api.main:app --port 8000        # in another shell
    python3 genon/out/stage_prep_english_preparatory/run_s9_c6.py

Library: english III ch 11, counts [12, 10, 7], floor 7, authored duration 40.
Identity split is testing.md §4's standard: kumar1 the identity requests, kumar2 the
between-variant / below-floor / surrender requests, kumar3 the mixed-duration weekly matrix.

Writes the response bundle to C6_responses_english_iii_ch11.json beside this script.
Exit code 0 iff every assertion holds.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

BASE = "http://localhost:8000"
SUBJ, GRADE, CH = "english", "iii", 11
OUT = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path(__file__).resolve().parents[3]

TOP, MID, LOW = 12, 10, 7
FLOOR, DUR = 7, 40

results: list[dict] = []
fails: list[str] = []


def post(user: str, rows: list[tuple[int, int]]) -> tuple[int, dict]:
    body = json.dumps({"rows": [{"duration": d, "count": c} for d, c in rows]}).encode()
    req = urllib.request.Request(
        f"{BASE}/genon/{SUBJ}/{GRADE}/{CH}/plan", data=body, method="POST",
        headers={"Content-Type": "application/json", "X-Aruvi-User": user})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


def get(user: str, path: str):
    req = urllib.request.Request(f"{BASE}{path}", headers={"X-Aruvi-User": user})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def saved_files() -> set[str]:
    d = ROOT / f"data/content/saved_plans/{SUBJ}/{GRADE}"
    return {p.name for p in d.glob("*.json")}


def check(ok: bool, label: str, detail: str = "") -> None:
    print(("  PASS  " if ok else "  FAIL  ") + label + (f"  — {detail}" if detail else ""))
    if not ok:
        fails.append(label)


def tiling_ok(plan: dict) -> tuple[bool, str]:
    """Every unit's bands tile 0..its own duration exactly."""
    bad = []
    for p in ((plan.get("result") or plan).get("lesson_plan") or {}).get("periods") or []:
        prev, dur = 0, p.get("period_duration_minutes")
        for b in p.get("time_bands") or []:
            try:
                a, e = (int(v) for v in re.split(r"[–\-—]", str(b["minutes"]).strip()))
            except Exception:                                # noqa: BLE001
                bad.append((p["period_number"], "unparseable", b.get("minutes")))
                break
            if a != prev:
                bad.append((p["period_number"], "gap/overlap", b.get("minutes")))
            prev = e
        else:
            if prev != dur:
                bad.append((p["period_number"], "sum", f"{prev} vs {dur}"))
    return (not bad), str(bad[:4])


def plan_of(rec: dict) -> dict | None:
    """Load the plan a row served. Keyed off `response.filename`, NOT `new_files`: a served
    plan is a CACHE ENTRY addressed by (chapter, matrix, variant version, engine), so a
    re-run is a hit that writes nothing and `new_files` is legitimately empty. Keying on the
    write would make every assertion below silently skip on the second run."""
    fn = (rec.get("response") or {}).get("filename")
    if not fn:
        return None
    p = ROOT / f"data/content/saved_plans/{SUBJ}/{GRADE}/{fn}"
    return json.loads(p.read_text()) if p.is_file() else None


def row(label: str, user: str, rows, expect: dict) -> dict:
    before = saved_files()
    status, r = post(user, rows)
    after = saved_files()
    new = sorted(after - before)
    rec = {"label": label, "identity": user, "rows": rows, "status": status,
           "response": r, "new_files": new}
    results.append(rec)
    print(f"\n{label}  [{user}]  rows={rows}")
    check(status == 200, f"{label}: 200", f"got {status} {r.get('detail','')}")
    if status != 200:
        return rec

    serve = r.get("serve") or {}
    fill = serve.get("slot_fill") or {}

    if expect.get("identity"):
        check(r.get("identity") is True, f"{label}: identity: true")
        check(r.get("filename") == expect["filename"],
              f"{label}: serves its own file", f"{r.get('filename')}")
        check(not new, f"{label}: NO new file saved", f"new={new}")
        check(r["filename"].startswith("ch_11_canonical"),
              f"{label}: registers the CANONICAL itself, not a served copy", r["filename"])
    else:
        check(not r.get("identity"), f"{label}: not an identity serve")
        if expect.get("mode"):
            got = fill.get("mode")
            check(got == expect["mode"], f"{label}: mode == {expect['mode']}", f"got {got}")
        if expect.get("fill_class"):
            check(fill.get("fill_class") == expect["fill_class"],
                  f"{label}: fill_class == {expect['fill_class']}",
                  f"got {fill.get('fill_class')}")
        if "drops" in expect:
            unc = fill.get("uncovered_sections") or []
            check(len(unc) == expect["drops"],
                  f"{label}: uncovered_sections == {expect['drops']}", f"got {unc}")
            if expect["drops"]:
                note = (r.get("coverage_note") or "")
                check(all(u in note for u in unc),
                      f"{label}: coverage_note NAMES every dropped section", note[:110])
        if expect.get("surrender"):
            sp = serve.get("surrendered_periods")
            n = sp if isinstance(sp, int) else len(sp or [])
            check(n >= 1, f"{label}: surrendered_periods >= 1", f"got {n}")
            check("return to your budget" in (r.get("coverage_note") or ""),
                  f"{label}: surrender sentence is in coverage_note (e09)",
                  (r.get("coverage_note") or "")[:110])
        if expect.get("borrowed_from"):
            check(fill.get("borrowed_from") == expect["borrowed_from"],
                  f"{label}: borrowed_from == {expect['borrowed_from']}",
                  f"got {fill.get('borrowed_from')}")
        if new:
            print(f"        saved: {new[0]}")
    return rec


print("=" * 78)
print("C6 · english III ch 11 · library [12, 10, 7] · floor 7 · authored 40 min")
print("=" * 78)

# ── kumar1 · identity, at the authored duration ────────────────────────────────
print("\n### kumar1 — identity requests (authored duration)")
row("identity X=12 (top)", "kumar1", [(DUR, TOP)],
    {"identity": True, "filename": "ch_11_canonical.json"})
row("identity X=10 (p10)", "kumar1", [(DUR, MID)],
    {"identity": True, "filename": "ch_11_canonical_p10.json"})
row("identity X=7 (p07)", "kumar1", [(DUR, LOW)],
    {"identity": True, "filename": "ch_11_canonical_p07.json"})

# ── kumar2 · the adaptation rows ───────────────────────────────────────────────
print("\n### kumar2 — between-variant, synthesis, surrender, below-floor")
row("complete fill X=9", "kumar2", [(DUR, 9)],
    {"mode": "fill", "fill_class": "single", "drops": 0})
row("rescue/complete X=8", "kumar2", [(DUR, 8)], {"mode": "complete_rescue", "drops": 0})
row("synthesis X=11", "kumar2", [(DUR, 11)], {"mode": "synthesis", "drops": 0,
                                              "borrowed_from": TOP})
row("surrender X=13 (top+1)", "kumar2", [(DUR, TOP + 1)], {"surrender": True})
row("below floor X=6", "kumar2", [(DUR, FLOOR - 1)],
    {"mode": "fill", "drops": 1})

# ── kumar3 · the mixed-duration weekly matrix ──────────────────────────────────
print("\n### kumar3 — mixed-duration weekly matrix (her profile is [40, 50], ppw 3:2)")
mixed = row("mixed 7x40 + 5x50", "kumar3", [(40, 7), (50, 5)], {})

# ── the deliberate nuance: identity fires ONLY at the authored duration ────────
print("\n### the nuance — identity only fires at the AUTHORED duration")
nud = row("X=12 at 50 min (not 40)", "kumar1", [(50, TOP)], {})

print("\n" + "=" * 78)
print("STRUCTURAL ASSERTIONS ON THE SERVED PLANS")
print("=" * 78)

# scaling + tiling on the non-authored duration
if nud["status"] == 200:
    plan = plan_of(nud)
    if plan:
        ok, det = tiling_ok(plan)
        check(ok, "X=12@50: every unit tiles 0..duration exactly", det)
        durs = sorted({p["period_duration_minutes"]
                       for p in plan["result"]["lesson_plan"]["periods"]})
        check(durs == [50], "X=12@50: every unit scaled to 50 min", str(durs))
        check(len(plan["result"]["lesson_plan"]["periods"]) == TOP,
              "X=12@50: all 12 units served (whole variant, scaled)")

# mixed matrix — weekly dispersion
if mixed["status"] == 200:
    plan = plan_of(mixed)
    if plan:
        g = plan.get("genon") or plan.get("result", {}).get("genon") or {}
        seq = g.get("duration_sequence") or [p["period_duration_minutes"]
                                             for p in plan["result"]["lesson_plan"]["periods"]]
        print(f"\n  duration_sequence: {seq}")
        check(bool(seq), "mixed: duration_sequence present")
        if seq:
            check(seq[0] == min(seq), "mixed: the SHORTEST sitting opens the week",
                  f"opens with {seq[0]}, min is {min(seq)}")
            longs = [i for i, d in enumerate(seq) if d == max(seq)]
            adjacent = [i for i, j in zip(longs, longs[1:]) if j == i + 1]
            check(not adjacent, "mixed: long sittings never adjacent", f"adjacent at {adjacent}")
            interior = all(0 < i < len(seq) - 1 for i in longs) if len(seq) > 2 else True
            check(interior, "mixed: long sittings sit interior", f"long at {longs} of {len(seq)}")
        ok, det = tiling_ok(plan)
        check(ok, "mixed: every unit tiles 0..its own duration exactly", det)

# below-floor: dropped_units carried verbatim, sourced from the LENDING plan
bf = next((r for r in results if r["label"] == "below floor X=6"), None)
if bf and bf["status"] == 200 and plan_of(bf):
    plan = plan_of(bf)
    du = (plan.get("result") or {}).get("dropped_units") or []
    check(bool(du), "X=6: result.dropped_units carries the lost units", f"{len(du)} unit(s)")
    check(all(u.get("unscheduled") is True for u in du),
          "X=6: every dropped unit is flagged unscheduled: true")

# served schedule prints the SERVED count, not the ask (e10)
sur = next((r for r in results if r["label"] == "surrender X=13 (top+1)"), None)
if sur and sur["status"] == 200 and plan_of(sur):
    plan = plan_of(sur)
    disp = plan.get("period_schedule_display") or ""
    print(f"\n  X=13 period_schedule_display: {disp!r}")
    check("12 period" in disp and "13" not in disp,
          "X=13: served schedule prints the SERVED count (12), not the ask (13)", disp[:80])
    snap = plan.get("period_rows_snapshot")
    check(any(int(r.get("count", 0)) == 13 for r in (snap or [])),
          "X=13: the REQUEST survives in period_rows_snapshot", str(snap))

# tenancy — each identity sees only its own prepared plans
print("\n" + "=" * 78)
print("TENANCY (X1 evidence)")
print("=" * 78)
prep = {}
for u in ("kumar1", "kumar2", "kumar3"):
    try:
        # /plans-prepared returns {"prepared": {plan_key: {at, periods}}} — a DICT keyed
        # by plan key, not a list. Reading it as a list silently yields nothing.
        p = get(u, "/plans-prepared")
        prepared = p.get("prepared") if isinstance(p, dict) else p
        keys = set(prepared) if isinstance(prepared, dict) else {str(x) for x in (prepared or [])}
    except Exception as e:                                   # noqa: BLE001
        keys = {f"ERROR {e}"}
    prep[u] = keys
    print(f"  {u}: {len(keys)} prepared")
ch11 = {u: {k for k in v if "ch_11" in str(k)} for u, v in prep.items()}
for u, v in ch11.items():
    print(f"    {u} ch11: {sorted(v)}")
check(all(ch11.values()), "every identity has ch 11 plans of its own")
# The registers are per-tenant on disk; kumar1's identity rows register the CANONICAL
# filenames (no copy saved), while kumar2/kumar3 register their own served files. So the
# expected picture is: kumar1 holds the three canonicals and nothing else, and the two
# served-file sets are disjoint from each other.
check(ch11["kumar1"] == {f"english/iii/ch_11_canonical{s}.json" for s in ("", "_p10", "_p07")}
      | {k for k in ch11["kumar1"] if "_e19_" in k},
      "kumar1 holds the three canonicals (identity registers the file, saves no copy)",
      str(sorted(ch11["kumar1"])))
served2 = {k for k in ch11["kumar2"] if "_e19_" in k}
served3 = {k for k in ch11["kumar3"] if "_e19_" in k}
check(bool(served2) and bool(served3) and not (served2 & served3),
      "kumar2 and kumar3 hold DISJOINT served files — per-tenant registers",
      f"k2={len(served2)} k3={len(served3)} shared={sorted(served2 & served3)}")

(OUT / "C6_responses_english_iii_ch11.json").write_text(
    json.dumps({"library": {"counts": [TOP, MID, LOW], "floor": FLOOR, "authored_duration": DUR},
                "rows": results, "prepared": {k: sorted(v) for k, v in prep.items()}},
               indent=1, ensure_ascii=False), encoding="utf-8")

print("\n" + ("ALL C6 ASSERTIONS PASS" if not fails else f"{len(fails)} FAILURE(S): {fails}"))
print(f"responses -> {(OUT / 'C6_responses_english_iii_ch11.json').relative_to(ROOT)}")
sys.exit(1 if fails else 0)
