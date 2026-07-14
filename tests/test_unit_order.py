"""
Unit-order invariant — TEACHING ORDER IS THE CONTRACT (founder rule, 2026-07-14).

The flattened Learning-Unit rail (LessonView walks groups depth-first, exactly like
flattenUnits in web/app/components/LessonView.jsx) drives the LU pointer — the thing that
tells a teacher "teach this next". So for EVERY subject and stage, flattening a plan's
view-model groups must reproduce the saved plan's own periods[] array order, period for
period. Grouping axes (section / stage / spine / competency) may only partition CONTIGUOUS
RUNS of that order — never merge a later revisit up into an earlier group.

History: first-appearance dict merges reordered maths secondary (ix ch_02: revisit period 9
pulled up to position 4; ch_07: consolidation period 11 shown as unit 8), science secondary
(ix ch_02 revisits §2.3.1), and social sciences (interleaved competencies — viii ch_04 read
1,3,10,2,5,…). All three translators now group by contiguous runs; this test sweeps the
WHOLE saved-plan corpus so no translator can regress (and any NEW subject/stage is covered
the day its first plan is saved).

Run: ARUVI_DATA_DIR=$PWD/data/content python3 tests/test_unit_order.py
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aruvi_core.subjects.english.subject import EnglishSubject
from aruvi_core.subjects.mathematics.subject import MathematicsSubject
from aruvi_core.subjects.science.subject import ScienceSubject
from aruvi_core.subjects.social_sciences.subject import SocialSciencesSubject
from aruvi_core.subjects.the_world_around_us.subject import TheWorldAroundUsSubject

PLUGINS = {
    "mathematics": MathematicsSubject(),
    "science": ScienceSubject(),
    "english": EnglishSubject(),
    "social_sciences": SocialSciencesSubject(),
    "the_world_around_us": TheWorldAroundUsSubject(),
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.environ.get("ARUVI_DATA_DIR", os.path.join(ROOT, "data", "content"))


def flatten(groups):
    """Depth-first walk, same order as LessonView.flattenUnits."""
    out = []
    for g in groups:
        out.extend(p.number for p in g.periods)
        out.extend(flatten(g.children or []))
    return out


def main():
    plans = sorted(glob.glob(os.path.join(DATA, "saved_plans", "*", "*", "*.json")))
    assert plans, f"no saved plans found under {DATA} — set ARUVI_DATA_DIR"
    checked, failures = 0, []
    for path in plans:
        parts = path.replace("\\", "/").split("/")
        subject, grade = parts[-3], parts[-2]
        plugin = PLUGINS.get(subject)
        if plugin is None:
            failures.append(f"{subject}/{grade}/{parts[-1]}: no plugin registered")
            continue
        with open(path) as fh:
            doc = json.load(fh)
        raw = doc.get("result", doc)
        lp = raw.get("lesson_plan", raw)
        raw_order = [p.get("period_number") for p in lp.get("periods", [])]
        view = plugin.lesson_plan_to_view(
            raw, grade=grade, chapter={"chapter_number": 0, "chapter_title": ""})
        flat = flatten(view.groups)
        if flat != raw_order:
            failures.append(
                f"{subject}/{grade}/{parts[-1]}: raw {raw_order} → flattened {flat}")
        checked += 1
    if failures:
        print(f"{len(failures)} of {checked} plans REORDERED:")
        for f in failures:
            print("  ", f)
        raise SystemExit(1)
    print(f"OK — unit order preserved across all {checked} saved plans "
          "(flattened view == periods[] teaching order, every subject & stage).")


if __name__ == "__main__":
    main()
