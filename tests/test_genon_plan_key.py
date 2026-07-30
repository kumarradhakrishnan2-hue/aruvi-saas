"""Adapted plans are CACHE ENTRIES: the filename must be a pure function of what
determines the bytes (founder decision 2026-07-26).

Guards:
  1. matrix normalisation — 17x50 and 10x50+7x50 and 7x50+10x50 all key the same,
     so a teacher never misses her own entry because of how she typed the rows;
  2. every key component actually changes the key (chapter, matrix, canonical
     version, engine version) — the polished flag was removed with the polish
     path at test-campaign step 0 (docs/testing.md §2, 2026-07-29);
  3. regenerating the canonical yields a NEW key — an existing plan is never
     silently overwritten under a teacher mid-chapter;
  4. save -> load round trip with an explicit filename (the cache fill + hit),
     and that a second save of the same key does not create a second file.

Run:  ARUVI_DATA_DIR=$PWD/data/content python3 tests/test_genon_plan_key.py
(stdlib only, like every other suite)
"""
import copy
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("ARUVI_DATA_DIR", os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "content"))

from api import data  # noqa: E402

FAILURES = []


def check(label, cond, detail=""):
    print(("PASS  " if cond else "FAIL  ") + label + (("  <- " + detail) if not cond and detail else ""))
    if not cond:
        FAILURES.append(label)


CANON = {"genon_canonical": {"ledger_ts": "20260726_112240"},
         "result": {"lesson_plan": {"periods": []}}}
key = lambda ch, m, c=CANON: data.genon_plan_filename(ch, m, c)

# ── 1. matrix normalisation ─────────────────────────────────────────────────
k17 = key(5, [(50, 17)])
check("aggregates split rows of one duration", key(5, [(50, 10), (50, 7)]) == k17)
check("row order does not matter", key(5, [(50, 7), (50, 10)]) == k17)
check("mixed matrix is order-independent",
      key(5, [(40, 10), (30, 4)]) == key(5, [(30, 4), (40, 10)]))
check("longest duration leads the label", "40m10-30m4" in key(5, [(30, 4), (40, 10)]),
      key(5, [(30, 4), (40, 10)]))
check("zero/negative rows are ignored",
      key(5, [(50, 17), (0, 9), (45, 0)]) == k17)
check("readable shape", k17 == "ch_05_50m17_e07_c20260726112240.json", k17)

# ── 2. every component moves the key ───────────────────────────────────────
check("chapter changes the key", key(6, [(50, 17)]) != k17)
check("period count changes the key", key(5, [(50, 16)]) != k17)
check("duration changes the key", key(5, [(45, 17)]) != k17)
check("no _p variant exists any more", not k17.endswith("_p.json"), k17)

# ── 3. canonical identity ──────────────────────────────────────────────────
other = {"genon_canonical": {"ledger_ts": "20260726_183000"}, "result": CANON["result"]}
check("a regenerated canonical yields a new key", key(5, [(50, 17)], other) != k17)
noted = {"result": {"lesson_plan": {"periods": [{"period_number": 1}]}}}
h1 = data.canonical_version(noted)
check("no ledger_ts -> content hash", len(h1) == 12 and h1.isalnum(), h1)
check("content hash is stable", data.canonical_version(copy.deepcopy(noted)) == h1)
noted2 = {"result": {"lesson_plan": {"periods": [{"period_number": 2}]}}}
check("different content -> different hash", data.canonical_version(noted2) != h1)

# ── 4. the real canonical on disk, and the save/load round trip ────────────
live = data.load_genon_canonical("social_sciences", "ix", 5)
if live is None:
    print("SKIP  live-canonical checks (no ch 5 canonical on disk)")
else:
    lk = data.genon_plan_filename(5, [(50, 16)], live)
    check("live canonical keys cleanly", lk.startswith("ch_05_50m16_e07_c") and lk.endswith(".json"), lk)
    check("key is deterministic across calls",
          lk == data.genon_plan_filename(5, [(50, 16)], live))

    with tempfile.TemporaryDirectory() as tmp:
        real = data.DATA_DIR
        try:
            data.DATA_DIR = tmp
            plan = {"chapter_number": 5, "chapter_title": "T", "result": {}, "genon": {"matrix": [{"duration": 50, "count": 16}]}}
            f1 = data.save_generated_plan("social_sciences", "ix", plan, filename=lk)
            check("save honours the given filename", f1 == lk, f1)
            check("cache hit: load returns the entry",
                  (data.load_saved_plan("social_sciences", "ix", lk) or {}).get("filename") == lk)
            data.save_generated_plan("social_sciences", "ix", copy.deepcopy(plan), filename=lk)
            n = len(os.listdir(os.path.join(tmp, "saved_plans", "social_sciences", "ix")))
            check("re-saving the same key does not add a file", n == 1, f"{n} files")
            legacy = data.save_generated_plan("social_sciences", "ix", copy.deepcopy(plan))
            check("legacy timestamp path still works", legacy.startswith("ch_05_2") and legacy != lk, legacy)
        finally:
            data.DATA_DIR = real

print("\n" + ("ALL PASS" if not FAILURES else "FAILURES: " + ", ".join(FAILURES)))
sys.exit(1 if FAILURES else 0)
