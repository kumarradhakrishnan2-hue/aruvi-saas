#!/usr/bin/env python3
"""repair_unit_order.py — a DECLARED unit permutation on an authored canonical (v1.0, 2026-08-10).

WHY THIS EXISTS, AND THE LINE IT SITS ON.
`repair_register.py` puts structural and pedagogical defects explicitly OUT of scope —
"repairing those here would launder content changes as text hygiene" — and at S4 the founder
declined a far smaller structural repair (a unit wearing the wrong section label) on exactly
that ground. Moving a unit is the most structural edit there is. So this tool is NOT a
general-purpose reorderer and must not become one: it exists for a case the founder has
inspected and declared a ONE-OFF, and every run is recorded in the artefact so corpus
statistics can still tell generation quality from repair quality.

THE CASE IT WAS BUILT FOR (mathematics · VII · ch 7, founder ruling 2026-08-10).
The top canonical placed a third section-7.2 unit at position 11 — after the plan had moved
through 7.3, 7.4 and 7.5 — which LP v3.6 Rule 1 forbids ("a section's periods are
CONTIGUOUS"). Because an item anchors at its section's LAST unit, all three of 7.2's
assessment items landed on that stranded revisit rather than inside the run that taught the
section: the sitting a teacher is most likely to skip was carrying a quarter of the chapter's
assessment. Regeneration is a lottery (founder, 2026-08-02) and this chapter had already drawn
the same defect twice, so the unit is moved instead.

WHAT MAKES IT SAFE HERE — checked before the tool was written, not assumed:
  * unit 11 references NO content from 7.3/7.4/7.5 (no altitudes, SAS/ASA, classification);
  * its in-class items (E-9, E-11) and homework (E-7) are all section 7.2, and disjoint from
    units 2 and 3 (E-4/E-5/E-6 and E-8/E-12/E-10) — the three units partition 7.2's exercises;
  * its teacher note already reads as unit 3's successor;
  * the moved method sequence contains no run of three (Rule 5).

WHAT MAKES IT SAFE IN GENERAL:
  * the permutation is a STATED list, not a computed reordering. Nothing is inferred about
    what "should" come next.
  * the coverage handoff is remapped by a DERIVED-then-ASSERTED mapping, never by trust:
    Rule 11 fixes one entry per period, in period order within each goal cluster, so walking
    the OLD period order and taking the next entry from each period's own cluster reconstructs
    period→entry exactly. The reconstruction is checked (12 periods ↔ 12 entries, and every
    entry's `goal` must equal its period's `section_goal`) and the run aborts if it does not
    hold. Assessment items follow the handoff (assessment Rule 1: items appear in handoff
    order), remapped by the same permutation.
  * nothing inside a unit is touched — not a band, not a note, not an item. Only
    `period_number` changes, and only because the unit's position did.
  * the move is recorded in `genon_canonical.repairs[]`, and the file is backed up first.

    python3 genon/repair_unit_order.py --list
    python3 genon/repair_unit_order.py --apply
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# ── the declared moves, keyed by (subject, grade, chapter) ───────────────────────
# `order` is the NEW sequence written in OLD period numbers. It must be a permutation of
# 1..N — asserted below, so a typo cannot silently drop or duplicate a unit.
MOVES = {
    ("mathematics", "vii", 7): {
        "file": "data/content/saved_plans/mathematics/vii/ch_07_canonical.json",
        "order": [1, 2, 3, 11, 4, 5, 6, 7, 8, 9, 10, 12],
        "why": ("LP v3.6 Rule 1 (contiguity): unit 11 anchored section 7.2 after the plan had "
                "moved through 7.3, 7.4 and 7.5. Moved to sit beside units 2 and 3, closing "
                "section 7.2's run. Founder ruling 2026-08-10, declared a ONE-OFF: the unit is "
                "self-contained on 7.2 (no later-section content, items and homework all 7.2 "
                "and disjoint from units 2-3), and Rule 5 survives the move."),
    },
}


def _clusters(handoff):
    return [k for k in ("section_a", "section_b", "section_c") if k in handoff]


def period_to_entry(periods, handoff):
    """Reconstruct which handoff entry belongs to which period.

    LP Rule 11: ONE entry per period, routed to the cluster matching the period's
    `section_goal`, and within a cluster the entries appear in period order. So walking the
    periods in order and taking the next unused entry from that period's own cluster is not a
    guess — it inverts the rule exactly. Returns {period_number: (cluster, index)}."""
    cursor = {c: 0 for c in _clusters(handoff)}
    out = {}
    for p in periods:
        goal = str(p.get("section_goal") or "")
        cluster = next((c for c in _clusters(handoff)
                        if goal in (handoff[c].get("goal_cluster") or [])), None)
        if cluster is None:
            raise SystemExit(f"ABORT: period {p['period_number']} goal {goal!r} routes to no cluster")
        i = cursor[cluster]
        goals = handoff[cluster].get("goals") or []
        if i >= len(goals):
            raise SystemExit(f"ABORT: cluster {cluster} has fewer entries than periods routed to it")
        entry = goals[i]
        if str(entry.get("goal") or "") != goal:
            raise SystemExit(f"ABORT: period {p['period_number']} goal {goal!r} != entry goal "
                             f"{entry.get('goal')!r} — Rule 11's ordering does not hold, "
                             "so the mapping cannot be reconstructed. Nothing written.")
        out[p["period_number"]] = (cluster, i)
        cursor[cluster] = i + 1
    total = sum(len(handoff[c].get("goals") or []) for c in _clusters(handoff))
    if total != len(periods):
        raise SystemExit(f"ABORT: {total} handoff entries vs {len(periods)} periods "
                         "(Rule 11 requires one per period). Nothing written.")
    return out


def apply_move(doc, order, why, key):
    r = doc["result"]
    periods = r["lesson_plan"]["periods"]
    n = len(periods)
    if sorted(order) != list(range(1, n + 1)):
        raise SystemExit(f"ABORT: declared order is not a permutation of 1..{n}. Nothing written.")

    by_old = {p["period_number"]: p for p in periods}
    handoff = r.get("coverage_handoff") or {}
    p2e = period_to_entry(periods, handoff)

    # ── the units, in the declared order, renumbered ─────────────────────────
    new_periods = []
    for new_no, old_no in enumerate(order, start=1):
        p = by_old[old_no]
        p["period_number"] = new_no
        new_periods.append(p)
    r["lesson_plan"]["periods"] = new_periods

    # ── the handoff, re-sorted so each cluster is in the NEW period order ────
    entries = {c: list(handoff[c].get("goals") or []) for c in _clusters(handoff)}
    rebuilt = {c: [] for c in _clusters(handoff)}
    for old_no in order:
        cluster, i = p2e[old_no]
        rebuilt[cluster].append(entries[cluster][i])
    for c in _clusters(handoff):
        if len(rebuilt[c]) != len(entries[c]):
            raise SystemExit(f"ABORT: cluster {c} lost an entry in the remap. Nothing written.")
        handoff[c]["goals"] = rebuilt[c]

    # ── the items follow the handoff (assessment Rule 1) ─────────────────────
    CODE = {"section_a": "A", "section_b": "B", "section_c": "C"}
    order_pos = {old_no: i for i, old_no in enumerate(order)}
    for grp in r.get("assessment_items") or []:
        cluster = next((c for c, code in CODE.items() if code == grp.get("section_code")), None)
        if cluster is None or cluster not in entries:
            continue
        items = grp.get("items") or []
        if len(items) != len(entries[cluster]):
            raise SystemExit(f"ABORT: section {grp.get('section_code')} has {len(items)} items "
                             f"vs {len(entries[cluster])} handoff entries. Nothing written.")
        # item i belonged to the i-th entry of this cluster, which belonged to a period;
        # re-sort by that period's NEW position.
        owner = {}
        for old_no, (c, i) in p2e.items():
            if c == cluster:
                owner[i] = old_no
        grp["items"] = [it for _, it in sorted(zip(range(len(items)), items),
                                               key=lambda t: order_pos[owner[t[0]]])]

    gc = doc.setdefault("genon_canonical", {})
    gc.setdefault("repairs", []).append({
        "tool": "repair_unit_order.py", "at": datetime.now().isoformat(timespec="seconds"),
        "kind": "unit_order", "key": "|".join(str(x) for x in key),
        "order": order, "why": why,
    })
    return doc


def main() -> int:
    listing = "--list" in sys.argv
    if not listing and "--apply" not in sys.argv:
        print(__doc__.strip().splitlines()[0])
        print("\nusage: repair_unit_order.py --list | --apply")
        return 2
    for key, mv in MOVES.items():
        path = REPO / mv["file"]
        print(f"\n=== {'|'.join(str(x) for x in key)} → {mv['file']}")
        print(f"    order: {mv['order']}")
        print(f"    why:   {mv['why']}")
        if listing:
            continue
        if not path.is_file():
            print("    SKIPPED — file not on disk")
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        if any(rp.get("kind") == "unit_order"
               for rp in (doc.get("genon_canonical") or {}).get("repairs", [])):
            print("    SKIPPED — a unit_order repair is already recorded on this file "
                  "(the declaration is stale by design once applied)")
            continue
        bak = path.with_suffix(".json.bak_pre_unit_order")
        shutil.copy2(path, bak)
        doc = apply_move(doc, mv["order"], mv["why"], key)
        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"    APPLIED — backup at {bak.name}")
    if not listing:
        print("\nNow re-certify (free):  python3 genon/build_library.py <subject> <grade> <ch> --certify-only")
    return 0


if __name__ == "__main__":
    sys.exit(main())
