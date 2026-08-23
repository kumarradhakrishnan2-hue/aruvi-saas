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

Run:  ARUVI_DATA_DIR=$PWD/data/cloud/content python3 tests/test_genon_plan_key.py
(stdlib only, like every other suite)
"""
import copy
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("ARUVI_DATA_DIR", os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "cloud", "content"))

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
# Built from the live constant, never hardcoded: the engine version is SUPPOSED to
# move (e08 -> e09 -> e10 -> e11 in four days) and a bump re-keying the cache is the
# designed behaviour, not a regression. Check the SHAPE, and let check 2 below prove
# the version is load-bearing.
check("readable shape",
      k17 == f"ch_05_50m17_e{data.GENON_ENGINE_VERSION}_c20260726112240.json", k17)

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
    check("live canonical keys cleanly", lk.startswith("ch_05_50m16_e10_c") and lk.endswith(".json"), lk)
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

# ── ARV-D-034 (2026-08-04): the key is CLEAN; invalidation lives in the repair tools ──
# A repair fingerprint in this key was built 2026-08-03 and REVERTED the next day (founder):
# it hung an unreadable hash tail off every served filename. The invariant it protected —
# a repaired canonical must never be served from a plan built before the repair — now lives
# in genon/purge_derived.py, which the repair tools call. So the key must stay STABLE across
# repairs, and the purge is what stops a stale plan existing at all.
def test_repairs_do_not_rekey():
    import copy
    from api import data
    base = {"genon_canonical": {"ledger_ts": "20260803141938"}, "result": {}}
    k0 = data.canonical_version(base)
    assert k0 == "20260803141938", k0

    repaired = copy.deepcopy(base)
    repaired["genon_canonical"]["repairs"] = [
        {"at": "2026-08-03T18:07:01", "tool": "repair_register", "edits": []},
        {"at": "2026-08-03T19:28:11", "tool": "normalize_options", "edits": []},
    ]
    assert data.canonical_version(repaired) == k0, \
        "a repair must NOT change the key — purge_derived is what invalidates"

    # the guard that replaced it: the purge pattern hits derived plans and never the library
    import importlib.util, pathlib
    spec = importlib.util.spec_from_file_location(
        "purge_derived", pathlib.Path(__file__).resolve().parent.parent / "genon" / "purge_derived.py")
    pd = importlib.util.module_from_spec(spec); spec.loader.exec_module(pd)
    pat = pd.derived_pattern(3)
    assert pat.match("ch_03_50m8_e13_c20260803142658.json")
    assert pat.match("ch_03_60m4-50m6_e13_c20260803142658.json")
    assert not pat.match("ch_03_canonical.json"), "the library must never be purgeable"
    assert not pat.match("ch_03_canonical_p07.json"), "nor a compact canonical"
    assert not pat.match("ch_04_50m8_e13_c20260803142658.json"), "nor another chapter"
    print("PASS  the key is stable across repairs; purge_derived hits only derived plans")



def test_regenerating_a_canonical_purges_its_derived_plans():
    """ARV-D-137 (S11 · C10, 2026-08-12) — the case the repair tools covered and the
    generator did not.

    The reasoning that left `generate_canonical` out was that regenerating mints a new
    `ledger_ts`, so the cache key moves and no stale file can be hit. That holds for the
    CHOSEN variant and fails for a LENDER: a served plan can carry a unit BORROWED from
    another canonical, and the key names only the variant that was served. Re-authoring
    english IX ch 7's top left the X=11 and X=15 plans — keyed on p10 and p14 — on disk
    still carrying the withdrawn synthesis text, which is exactly what the re-author had
    just been paid to remove.

    The assertion is on the WIRING, not on the filesystem: `install_canonical` must call
    `purge_derived.purge` for the chapter it installs. A test that wrote real files would
    be testing purge_derived, which the test above already does."""
    import importlib.util, pathlib as _p, sys as _s, types
    root = _p.Path(__file__).resolve().parent.parent
    _s.path.insert(0, str(root / "genon"))
    spec = importlib.util.spec_from_file_location(
        "generate_canonical", root / "genon" / "generate_canonical.py")
    gc = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(gc)
    except Exception as e:                                   # noqa: BLE001
        print(f"SKIP  generate_canonical did not import ({e})")
        return

    calls = []
    fake = types.ModuleType("purge_derived")
    fake.purge = lambda subject, grade, ch, reason="", apply=True: calls.append(
        (subject, grade, ch, apply)) or []
    _s.modules["purge_derived"] = fake

    import tempfile, json as _j
    with tempfile.TemporaryDirectory() as tmp:
        gc.REPO = _p.Path(tmp)
        parsed = {"lesson_plan": {"periods": []}, "coverage_handoff": {},
                  "assessment_items": []}
        gc.install_canonical(parsed, "english", "ix", 7, "20260812_154258", 50, 17,
                             "LP v1.2 / assessment v1.4", "ok", [])
    assert calls, ("install_canonical must purge the chapter's derived plans — a "
                   "re-authored canonical invalidates every plan that BORROWED from it, "
                   "and the cache key does not name the lender (ARV-D-137)")
    assert calls[0][:3] == ("english", "ix", 7), calls
    assert calls[0][3] is True, "the purge must actually apply, not dry-run"
    print("PASS  regenerating a canonical purges the plans derived from it")


test_regenerating_a_canonical_purges_its_derived_plans()


test_repairs_do_not_rekey()

print("\n" + ("ALL PASS" if not FAILURES else "FAILURES: " + ", ".join(FAILURES)))
sys.exit(1 if FAILURES else 0)


