"""Phases as the timed spine (layout decision 2026-07-09).

Covers:
  1. parse_minutes_band — en-dash / hyphen / em-dash / spaced / junk forms.
  2. phases_from — {minutes, description|activity} dicts -> typed Phase objects.
  3. phase_tiling_issues — gap / overlap / wrong-end detection.
  4. THE REAL LIBRARY: every saved plan under data/content/saved_plans runs through its
     subject's lesson_plan_to_view; every period must carry parsed phases, and phase
     tiling is REPORTED (not asserted per-period — saved plans are carried as-is; we
     assert only that parsing succeeded and the overwhelming majority tile cleanly).

Run:  ARUVI_DATA_DIR=$PWD/data/content python3 tests/test_phases.py
(stdlib only, like every other suite)
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aruvi_core.normalize import parse_minutes_band, phases_from, phase_tiling_issues
from aruvi_core.view_model import Phase
import aruvi_core.subjects.english      # noqa: F401  (import registers the plugin)
import aruvi_core.subjects.mathematics  # noqa: F401
import aruvi_core.subjects.science      # noqa: F401
import aruvi_core.subjects.social_sciences      # noqa: F401
import aruvi_core.subjects.the_world_around_us  # noqa: F401
from aruvi_core import subjects

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVED = os.path.join(REPO, "data", "content", "saved_plans")

failures = []


def check(name, cond, detail=""):
    if cond:
        print(f"  ok   {name}")
    else:
        failures.append(name)
        print(f"  FAIL {name}  {detail}")


# ── 1. parser forms ────────────────────────────────────────────────────────────
print("parse_minutes_band:")
check("en-dash", parse_minutes_band("0–5") == (0, 5))
check("hyphen", parse_minutes_band("10-30") == (10, 30))
check("em-dash", parse_minutes_band("5—12") == (5, 12))
check("spaced", parse_minutes_band("0 - 10") == (0, 10))
check("'to' form", parse_minutes_band("15 to 25") == (15, 25))
check("suffix junk", parse_minutes_band("30–40 min") == (30, 40))
check("no range -> None", parse_minutes_band("ten minutes") == (None, None))
check("reversed -> None", parse_minutes_band("30–4") == (None, None))
check("empty/None", parse_minutes_band("") == (None, None) and parse_minutes_band(None) == (None, None))

# ── 2. phases_from ─────────────────────────────────────────────────────────────
print("phases_from:")
ph = phases_from([
    {"minutes": "0–5", "description": "hook"},
    {"minutes": "5-40", "activity": "main task"},   # SS/TWAU key
    "bare string line",
])
check("count", len(ph) == 3)
check("typed", all(isinstance(p, Phase) for p in ph))
check("ints parsed", (ph[0].start_min, ph[0].end_min, ph[1].end_min) == (0, 5, 40))
check("text key drift", ph[1].text == "main task")
check("raw label kept", ph[0].label == "0–5")
check("bare string carried", ph[2].text == "bare string line" and ph[2].start_min is None)
check("empty input", phases_from(None) == [] and phases_from([]) == [])

# ── 3. tiling validation ───────────────────────────────────────────────────────
print("phase_tiling_issues:")
clean = phases_from([{"minutes": "0-5", "description": "a"}, {"minutes": "5-40", "description": "b"}])
check("clean tiles", phase_tiling_issues(clean, 40) == [])
gap = phases_from([{"minutes": "0-5", "description": "a"}, {"minutes": "10-40", "description": "b"}])
check("gap flagged", any("gap" in i for i in phase_tiling_issues(gap, 40)))
short = phases_from([{"minutes": "0-30", "description": "a"}])
check("short end flagged", any("ends at 30" in i for i in phase_tiling_issues(short, 40)))
late = phases_from([{"minutes": "5-40", "description": "a"}])
check("late start flagged", any("not 0" in i for i in phase_tiling_issues(late, 40)))
check("no phases flagged", phase_tiling_issues([], 40) == ["no phases"])

# ── 4. the real library ────────────────────────────────────────────────────────
print("saved-plan library:")


def walk_periods(groups):
    for g in groups:
        for p in g.periods:
            yield p
        yield from walk_periods(g.children)


total_plans = total_periods = with_phases = parsed_ok = tiled = 0
untiled_report = []
for f in sorted(glob.glob(os.path.join(SAVED, "*", "*", "*.json"))):
    parts = f.split(os.sep)
    subject_slug, filename = parts[-3], parts[-1]
    saved = json.load(open(f))
    sub = subjects.get(subject_slug)
    lp = sub.lesson_plan_to_view(
        saved.get("result", {}),   # full result — plugins unwrap lesson_plan themselves
        grade=saved.get("grade", ""),
        chapter={"chapter_number": saved.get("chapter_number"),
                 "chapter_title": saved.get("chapter_title")},
    )
    total_plans += 1
    for period in walk_periods(lp.groups):
        total_periods += 1
        if period.phases:
            with_phases += 1
            if all(p.start_min is not None and p.end_min is not None for p in period.phases):
                parsed_ok += 1
            dur = period.meta.get("duration_minutes")
            issues = phase_tiling_issues(period.phases, dur)
            if not issues:
                tiled += 1
            else:
                untiled_report.append(f"{subject_slug}/{filename} P{period.number}: {issues}")
        # materials should be a clean list everywhere
        assert isinstance(period.materials, list), f"{f} P{period.number} materials not a list"

print(f"  {total_plans} plans, {total_periods} periods; "
      f"{with_phases} with phases, {parsed_ok} fully parsed, {tiled} tile cleanly")
for line in untiled_report:
    print(f"    untiled: {line}")

check("every period has phases", with_phases == total_periods,
      f"{total_periods - with_phases} without")
check("every phase band parses to ints", parsed_ok == with_phases,
      f"{with_phases - parsed_ok} periods with unparseable bands")
# Tiling is generator-quality, not a hard contract on legacy plans — require the vast majority.
check("≥90% of periods tile cleanly", with_phases and tiled / with_phases >= 0.9,
      f"only {tiled}/{with_phases}")

print()
if failures:
    print(f"FAILED: {len(failures)} -> {failures}")
    sys.exit(1)
print("ALL PHASE TESTS PASSED")
