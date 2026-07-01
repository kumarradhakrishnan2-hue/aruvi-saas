"""
Parity test for the assessment → period LINK RESOLVER (architecture-plan.md §"Link resolution
— verified 8-rule table"). The guardrail the plan demands: for every subject·grade, EVERY
assessment item resolves to >= 1 period with ZERO orphans, and the uniform contract is well
formed (anchor_period == max(linked_periods)).

Unlike the per-subject port tests (one fixture each), this walks the FULL real saved-plan
corpus under data/content/saved_plans/ so all 8 rules are exercised on real data, exactly as
the plan requires ("derived from saved-file inspection, never constitution prose").

Run standalone:  ARUVI_DATA_DIR=$PWD/data/content python3 tests/test_link_resolver.py
"""
from __future__ import annotations

import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# register every subject
import aruvi_core.subjects.science            # noqa: E402
import aruvi_core.subjects.social_sciences    # noqa: E402
import aruvi_core.subjects.mathematics        # noqa: E402
import aruvi_core.subjects.english            # noqa: E402
import aruvi_core.subjects.the_world_around_us  # noqa: E402
from aruvi_core import subjects               # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLANS = os.path.join(ROOT, "data", "content", "saved_plans")


def _link_context(r):
    lp = r.get("lesson_plan", {})
    return {"periods": lp.get("periods", []),
            "handoff": r.get("coverage_handoff", lp.get("coverage_handoff", []))}


def _iter_saved():
    for fp in sorted(glob.glob(os.path.join(PLANS, "*", "*", "*.json"))):
        parts = fp.split(os.sep)
        subject, grade = parts[-3], parts[-2]
        yield subject, grade, fp


def _items(view):
    return [it for g in view.groups for it in g.items]


def test_every_item_resolves_zero_orphans():
    seen_subjects = set()
    total_items = 0
    for subject, grade, fp in _iter_saved():
        saved = json.load(open(fp))
        r = saved["result"]
        sub = subjects.get(subject)
        ch = {"chapter_number": saved.get("chapter_number"),
              "chapter_title": saved.get("chapter_title")}
        a = sub.assessment_to_view(r.get("assessment_items", []), grade=saved.get("grade", grade),
                                   chapter=ch, link_context=_link_context(r))
        items = _items(a)
        assert items, f"{subject}/{grade} {os.path.basename(fp)}: produced no items"
        for it in items:
            lp_set = it.meta.get("linked_periods")
            anchor = it.meta.get("anchor_period")
            assert lp_set, (f"ORPHAN — {subject}/{grade} {os.path.basename(fp)}: "
                            f"item resolved to no period. meta={it.meta}")
            assert anchor == max(lp_set), (f"{subject}/{grade}: anchor {anchor} != "
                                           f"max(linked) {max(lp_set)}")
            assert "linked_lo" in it.meta, "uniform contract missing linked_lo"
            total_items += 1
        seen_subjects.add(subject)
    # corpus actually covered all 5 subject plugins
    assert seen_subjects == {"science", "social_sciences", "mathematics", "english",
                             "the_world_around_us"}, f"corpus missed subjects: {seen_subjects}"
    print(f"OK — link resolver: {total_items} items across {len(list(_iter_saved()))} saved "
          f"plans, 0 orphans, anchors consistent, all 5 subjects covered.")


def test_backward_compat_no_context():
    # Older callers (and existing port tests) pass no link_context — items must still normalize,
    # just with empty link metadata (no crash).
    subject, grade, fp = next(_iter_saved())
    saved = json.load(open(fp)); r = saved["result"]
    sub = subjects.get(subject)
    ch = {"chapter_number": saved.get("chapter_number"), "chapter_title": saved.get("chapter_title")}
    a = sub.assessment_to_view(r.get("assessment_items", []), grade=saved.get("grade", grade), chapter=ch)
    assert _items(a), "normalization must still work without link_context"
    print("OK — backward compatible: assessment_to_view works with no link_context.")


if __name__ == "__main__":
    test_every_item_resolves_zero_orphans()
    test_backward_compat_no_context()
