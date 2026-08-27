"""The lesson-plan EDITION stamp — administrative architecture §2.2 (2026-08-27).

The one thing these tests exist to protect: **the year is a LABEL, and the cache key is
(engine, constitution-run).** Everything else here is a consequence of that.

If someone ever puts the year into `genon_plan_filename`, `test_carried_chapter_still_hits_its_cache`
fails — and that failure is the difference between carrying a library forward for free
and re-buying it every June at peak load (§2.2: "get this wrong and every June you
re-pay to regenerate content that did not change").

Run: python3 tests/test_lp_year.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "tests"))

from api import config, data          # noqa: E402
from corpus import plan_paths          # noqa: E402

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"{'PASS' if cond else 'FAIL'}  {name}" + (f"  <- {detail}" if not cond and detail else ""))


# ── 1. the stamp exists on the real library ────────────────────────────────────
def test_every_live_plan_carries_an_edition():
    paths = plan_paths()
    check("the corpus is non-empty (a vacuous pass proves nothing)", bool(paths),
          f"{len(paths)} plans")
    if not paths:
        return
    missing = []
    for fp in paths:
        try:
            d = json.load(open(fp))
        except Exception:
            continue
        if not data.plan_lp_year(d):
            missing.append(os.path.basename(fp))
    check("every plan in the library carries an academic_year", not missing,
          f"{len(missing)} without one, e.g. {missing[:3]}")


def test_the_stamp_is_not_in_any_filename():
    """The invariant, stated as a test. A year in the filename IS a year in the cache key."""
    named = [os.path.basename(p) for p in plan_paths()
             if config.LP_YEAR in os.path.basename(p)]
    check("no plan FILENAME contains the year (year is a label, not a key)", not named,
          f"e.g. {named[:2]}")


# ── 2. path resolution ─────────────────────────────────────────────────────────
def test_library_dir_prefers_the_edition_and_falls_back_flat():
    with tempfile.TemporaryDirectory() as tmp:
        real = data.DATA_DIR
        try:
            data.DATA_DIR = tmp
            flat = Path(tmp) / "saved_plans" / "science" / "vi"
            flat.mkdir(parents=True)
            (flat / "ch_01_canonical.json").write_text("{}")
            check("a flat legacy tree still resolves",
                  data.lp_library_dir("science", "vi") == str(flat))
            dated = flat / config.LP_YEAR
            dated.mkdir()
            check("an editioned tree wins once it exists",
                  data.lp_library_dir("science", "vi") == str(dated))
            check("editions are listed newest first",
                  data.lp_library_years("science", "vi") == [config.LP_YEAR])
            # A subject·grade with NO folder at all must still WRITE into the edition,
            # not recreate the flat layout underneath a migrated tree.
            check("an unseen subject·grade still writes into the edition",
                  data.lp_library_dir("science", "ix").endswith(config.LP_YEAR))
        finally:
            data.DATA_DIR = real


def test_a_plan_from_an_older_edition_is_still_openable():
    """§2.3 — a plan attached to a section is immutable for the life of that attachment,
    so opening it must not depend on it being the CURRENT edition."""
    with tempfile.TemporaryDirectory() as tmp:
        real = data.DATA_DIR
        try:
            data.DATA_DIR = tmp
            old = Path(tmp) / "saved_plans" / "science" / "vi" / "2025-26"
            old.mkdir(parents=True)
            (old / "ch_09_canonical.json").write_text(json.dumps({"filename": "x"}))
            (Path(tmp) / "saved_plans" / "science" / "vi" / config.LP_YEAR).mkdir()
            got = data.load_saved_plan("science", "vi", "ch_09_canonical.json")
            check("a prior edition's plan is found by look-back", got is not None)
        finally:
            data.DATA_DIR = real


# ── 3. THE ONE THAT MATTERS — carry-over keeps the cache ───────────────────────
def test_carried_chapter_still_hits_its_cache():
    """Carry an unchanged chapter into a new edition and serve it again. The key must be
    IDENTICAL and the entry must hit — otherwise carrying a library forward costs a full
    regeneration of every variant, in June, at peak (§2.2)."""
    src = None
    for p in plan_paths("social_sciences", "ix", "ch_05_canonical*.json"):
        src = Path(p).parent
        break
    if src is None:
        print("SKIP  carry-over cache test — social_sciences/ix ch 5 not in the corpus")
        return

    with tempfile.TemporaryDirectory() as tmp:
        real = data.DATA_DIR
        try:
            dst = Path(tmp) / "saved_plans" / "social_sciences" / "ix" / config.LP_YEAR
            dst.mkdir(parents=True)
            for f in src.glob("ch_05_canonical*.json"):
                shutil.copy(f, dst / f.name)
            data.DATA_DIR = tmp

            # serve once in the CURRENT edition and cache the result
            from aruvi_core.genon.serve import serve_plan
            streams = data.load_genon_streams("social_sciences", "ix", 5)
            lib = data.load_genon_library("social_sciences", "ix", 5)
            matrix = [(50, 16)]
            plan = serve_plan(streams, matrix)

            def cnt(c):
                return int((c.get("period_rows_snapshot") or [{}])[0].get("count") or 0)

            chosen = next(c for c in lib if cnt(c) == plan["genon"]["variant_used"])
            key_before = data.genon_plan_filename(5, matrix, chosen)
            data.save_generated_plan("social_sciences", "ix", plan, filename=key_before)

            # carry the chapter into the NEXT edition
            nxt = "2027-28"
            r = subprocess.run(
                [sys.executable, str(REPO / "aruvi-scripts" / "carry_over_year.py"),
                 "--to", nxt, "--from", config.LP_YEAR],
                cwd=str(REPO), capture_output=True, text=True,
                env={**os.environ, "ARUVI_DATA_DIR": tmp})
            check("carry_over_year.py runs clean", r.returncode == 0, r.stderr[-200:])

            # …and serve the same request against the new edition
            os.environ["ARUVI_LP_YEAR"] = nxt
            import importlib
            importlib.reload(config)
            importlib.reload(data)
            data.DATA_DIR = tmp

            streams2 = data.load_genon_streams("social_sciences", "ix", 5)
            lib2 = data.load_genon_library("social_sciences", "ix", 5)
            plan2 = serve_plan(streams2, matrix)
            chosen2 = next(c for c in lib2 if cnt(c) == plan2["genon"]["variant_used"])
            key_after = data.genon_plan_filename(5, matrix, chosen2)

            check("★ the cache key is IDENTICAL across the edition bump",
                  key_after == key_before, f"{key_before} != {key_after}")
            hit = data.load_saved_plan("social_sciences", "ix", key_after)
            check("★ the carried derived plan HITS — no regeneration is paid for",
                  hit is not None)
            check("the carried plan wears the NEW edition label",
                  data.plan_lp_year(hit) == nxt, str(data.plan_lp_year(hit)))
            check("…and records the edition its bytes actually came from",
                  (hit.get("genon") or {}).get("carried_from") == "2026-27",
                  str((hit.get("genon") or {}).get("carried_from")))
        finally:
            os.environ.pop("ARUVI_LP_YEAR", None)
            import importlib
            importlib.reload(config)
            importlib.reload(data)
            data.DATA_DIR = real


# ── 4. the display rule ────────────────────────────────────────────────────────
def test_the_year_shows_only_for_a_prior_edition():
    """Founder's rule: every canonical carries the stamp, but a teacher only SEES it when
    the plan is from an older edition than the one being served."""
    def display(lp_year, current):
        return lp_year if lp_year and lp_year < current else None

    check("the current edition shows nothing", display("2026-27", "2026-27") is None)
    check("a prior edition shows its year", display("2026-27", "2027-28") == "2026-27")
    check("an unstamped legacy plan shows nothing", display(None, "2026-27") is None)
    check("a FUTURE stamp shows nothing (never guess about her record)",
          display("2028-29", "2027-28") is None)


if __name__ == "__main__":
    for fn in [v for k, v in sorted(globals().items())
               if k.startswith("test_") and callable(v)]:
        fn()
    print(f"\n{len(PASS)} passed, {len(FAIL)} failed")
    if FAIL:
        print("FAILURES: " + ", ".join(FAIL))
        raise SystemExit(1)
    print("ALL PASS")
