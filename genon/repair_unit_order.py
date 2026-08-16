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
from typing import Dict

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from purge_derived import purge                                  # noqa: E402

# ── the declared moves, keyed by (subject, grade, chapter) ───────────────────────
# `order` is the NEW sequence written in OLD period numbers. It must be a permutation of
# 1..N — asserted below, so a typo cannot silently drop or duplicate a unit.
MOVES = {
    ("social_sciences", "viii", 15): {
        "file": "data/content/saved_plans/social_sciences/viii/ch_15_canonical_p14.json",
        "order": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 12, 14],
        "family": "competency_los",
        "why": ("S2 batch wave 2, AFTER a re-author. The original p14 first-taught [2] Regional "
                "saints in its CLOSING unit; it was re-bought at Rs 28.17 (2026-08-16) and that "
                "defect is gone — saints now sit third. The re-author drew two milder breaks "
                "instead, which is the lottery working exactly as the doctrine says it does.\n"
                "THIS MOVE FIXES ONE OF THEM: U12 anchors [15] Regional Architectural "
                "Developments and sits BEFORE U13's [13,14] Cultural Exchange — Food/Clothing. "
                "Swapping the two restores registry order for the tail. Founder ruling "
                "2026-08-16: move 15 where it belongs and close the case.\n"
                "SAFE: the two units share no section and neither references the other — U13 "
                "is the food/clothing pair, U12 the architecture close; the compact's final "
                "unit (U14) consolidates all 16 sections either way, so nothing downstream "
                "depends on which of the two it follows.\n"
                "NOT FIXED HERE, and deliberately: U7 anchors [6, 9] jointly (Gardens bundled "
                "with Vocational education), which pulls 9 ahead of 7 and 8. No permutation "
                "can resolve that — moving the unit later just makes 6 late — and 9 is taught "
                "nowhere else in the compact, so the token cannot be dropped either. It is an "
                "authoring choice and it goes to F1 with the viii ch 8 orphans."),
    },
    ("social_sciences", "vii", 8): {
        "file": "data/content/saved_plans/social_sciences/vii/ch_08_canonical_p13.json",
        "order": [1, 2, 3, 4, 5, 6, 8, 7, 10, 9, 11, 12, 13],
        "family": "competency_los",
        "why": ("S2 batch wave 2. Two ADJACENT TRANSPOSITIONS against the top's registry: the "
                "compact teaches [6] Sacred Geography Beyond India before [5] From Pilgrimage "
                "to Trade, and [8] Restoring and Conserving the Sacred before [7] More Sacred "
                "Sites. Founder ruling 2026-08-16, declared a ONE-OFF.\n"
                "CHECKED FIRST, because the two sibling cases this wave LOOKED like order "
                "defects and were not — vi ch 7 and vii ch 3 were both under-labelled anchors, "
                "fixed with one token each and no unit moved. This one is different: each of "
                "the four units genuinely teaches its own registry section (U7 'Sacred Land "
                "Beyond India: Global Patterns' = [6]; U8 'Sacred Routes, Sacred Trade: the "
                "Uttarapatha and Dakṣhinapātha' = [5]), so no anchor edit can reconcile it. "
                "The order is the defect.\n"
                "SAFE: U8's note reads 'Having established the sacred networks and the idea of "
                "pilgrimage as cultural exchange' — that is units 1-6, not U7, so it may "
                "precede U7; U7 'repositions the chapter's Indian examples within a global "
                "frame', which reads no worse after the trade routes. The top's own sequence "
                "is 5 → 6 → 7 → 8, which is what this restores."),
    },
    ("mathematics", "vii", 7): {
        "file": "data/content/saved_plans/mathematics/vii/ch_07_canonical.json",
        "order": [1, 2, 3, 11, 4, 5, 6, 7, 8, 9, 10, 12],
        "family": "goal_cluster",
        "why": ("LP v3.6 Rule 1 (contiguity): unit 11 anchored section 7.2 after the plan had "
                "moved through 7.3, 7.4 and 7.5. Moved to sit beside units 2 and 3, closing "
                "section 7.2's run. Founder ruling 2026-08-10, declared a ONE-OFF: the unit is "
                "self-contained on 7.2 (no later-section content, items and homework all 7.2 "
                "and disjoint from units 2-3), and Rule 5 survives the move."),
    },
    ("the_world_around_us", "v", 5): {
        "file": "data/content/saved_plans/the_world_around_us/v/ch_05_canonical.json",
        "order": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 14, 16],
        "family": "item_self_sufficient",
        "why": ("ARV-D-119, partial: the standard's last two teaching units are a PAIR — U15 "
                "'Cultural Fair — Research and Prepare' MAKES the posters, U16 (the mandated "
                "synthesis) presents them ('materials: Group posters and charts prepared "
                "previously'). The X-1+1 form at X=15 serves U1..U14 + the synthesis and drops "
                "U15, so the closer needs posters no unit in that plan ever made. Swapping U14 "
                "and U15 puts the poster-making inside the X=15 prefix. Founder ruling "
                "2026-08-11, declared a ONE-OFF on the TOP canonical alone.\n"
                "SAFE: the two units are mutually independent and both sit on the same section "
                "('Spirit of Togetherness'), so no anchor, registry, first-visit order or "
                "contiguity fact moves. U14 (Local Contributors) sources elders and community "
                "and names no Cultural Fair content; U15 sources Textbook p. 92 and family "
                "knowledge and names no Local Contributors content; each already closes on its "
                "own ground. Rule 3's cap survives (…O&R · C&E · HI · D&C — no run of two).\n"
                "SCOPE, STATED: this does NOT fix X=14, which serves the prefix of 13 and drops "
                "BOTH units whatever their order. X=14 needs the poster unit at position <=13 "
                "— a three-unit move, not this swap — and stays open on ARV-D-119."),
    },
    ("the_world_around_us", "iv", 8): {
        "file": "data/content/saved_plans/the_world_around_us/iv/ch_08_canonical_p11.json",
        "order": [1, 2, 3, 4, 6, 7, 8, 9, 10, 5, 11],
        "family": "item_self_sufficient",
        "why": ("FIRST-VISIT ORDER, wave 2 of S5's corpus (2026-08-12). p11's U5 'Observe and "
                "Classify Paper Types' is the first visit to 'Different Types of Paper and "
                "their Uses' — the registry's LAST section — arriving before sections 2, 3 and "
                "4 are taught at all. Coverage is tracked as a single frontier, so any "
                "truncated serve of p11 (X=9, X=10) would have taught section 5 while the "
                "frontier claimed the whole registry was covered, under-reporting the drop. "
                "The move puts U5 immediately before U11, its own section's other unit. "
                "Founder ruling 2026-08-12, declared a ONE-OFF on this compact alone.\n"
                "THE TOP IS NOT AT FAULT AND IS NOT TOUCHED: the chapter summary's section "
                "order — taken from the textbook — is exactly the registry order (How Paper "
                "is Made / Making Responsible Choices / Let Us Get Creative / Let us reflect "
                "/ Different Types), so the top is faithful to the source and p11 is the "
                "deviant. p08, the other compact, already keeps the section last and passes.\n"
                "SAFE: the two units are the same section and read as a pair once adjacent — "
                "U5 observes and matches samples to the Textbook p. 123 table, U11 'completes "
                "any remaining portions' of that same table, so U11's existing backward "
                "dependency gets stronger, not weaker. Neither names content from sections 2-4, "
                "and each item follows its own unit through the remap."),
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


def apply_move_item_self_sufficient(doc, order, why, key):
    """The ITEM-SELF-SUFFICIENT family (8-rule rows 3 and 8: social_sciences, TWAU).

    Added 2026-08-11 for TWAU·V ch 5. Everything the goal-cluster path has to RECONSTRUCT is
    stated outright in this family, which is what makes it the simpler and safer of the two:

      * the coverage handoff is a FLAT LIST whose entries carry their own `period_number`
        (TWAU LP Rule 9: "one entry per period"), so period -> entry is read, never inverted
        from an ordering rule;
      * the items are a FLAT LIST carrying their own `period_ref[]` (the family's defining
        property — no handoff bridge, no period-field join), so an item follows its unit by
        renumbering that field and by nothing else.

    So no item is reordered and no list is re-sorted: units and handoff entries move together
    in the declared order, and every `period_ref` is rewritten through the same old->new map.
    Nothing INSIDE a unit or an item is touched.
    """
    r = doc["result"]
    periods = r["lesson_plan"]["periods"]
    n = len(periods)
    if sorted(order) != list(range(1, n + 1)):
        raise SystemExit(f"ABORT: declared order is not a permutation of 1..{n}. Nothing written.")

    handoff = r.get("coverage_handoff")
    if not isinstance(handoff, list):
        raise SystemExit("ABORT: this family expects a FLAT coverage_handoff list. Nothing written.")
    if len(handoff) != n:
        raise SystemExit(f"ABORT: {len(handoff)} handoff entries vs {n} periods — LP Rule 9 "
                         "requires one per period. Nothing written.")
    by_old_p = {p["period_number"]: p for p in periods}
    by_old_h = {h["period_number"]: h for h in handoff}
    if sorted(by_old_p) != list(range(1, n + 1)) or sorted(by_old_h) != list(range(1, n + 1)):
        raise SystemExit("ABORT: period numbers are not exactly 1..N on both sides. Nothing written.")

    old_to_new = {old: new for new, old in enumerate(order, start=1)}

    # ── units and handoff entries, in the declared order, renumbered together ──
    new_periods, new_handoff = [], []
    for new_no, old_no in enumerate(order, start=1):
        p, h = by_old_p[old_no], by_old_h[old_no]
        p["period_number"] = new_no
        h["period_number"] = new_no
        new_periods.append(p)
        new_handoff.append(h)
    r["lesson_plan"]["periods"] = new_periods
    r["coverage_handoff"] = new_handoff

    # ── the items follow their own declared anchor, and only that ─────────────
    items = r.get("assessment_items") or []
    if not isinstance(items, list):
        raise SystemExit("ABORT: this family expects a FLAT assessment_items list. Nothing written.")
    def _refs(it):
        v = it.get("period_ref")
        return v if isinstance(v, list) else ([v] if v is not None else [])

    # how many items each unit carried BEFORE — the invariant the remap must preserve
    before: Dict[int, int] = {}
    for it in items:
        for x in _refs(it):
            try:
                old = int(x)
            except (TypeError, ValueError):
                raise SystemExit(f"ABORT: item carries a non-numeric period_ref {x!r}. "
                                 "Nothing written.")
            if old not in old_to_new:
                raise SystemExit(f"ABORT: item anchors to unit {old}, which is not in 1..{n}. "
                                 "Nothing written.")
            before[old] = before.get(old, 0) + 1

    moved = 0
    for it in items:
        refs = [int(x) for x in _refs(it)]
        remapped = [old_to_new[x] for x in refs]
        if remapped != refs:
            moved += 1
        it["period_ref"] = remapped

    # THE ASSERTION THAT MATTERS: the unit a given item sat on before the move must be the
    # SAME unit, at its new number, after it. Anything else means an item changed hands —
    # which on this family would be a silent content error, since the item's stem was written
    # for that unit's activity.
    after: Dict[int, int] = {}
    for it in items:
        for x in it["period_ref"]:
            after[x] = after.get(x, 0) + 1
    expected = {old_to_new[old]: c for old, c in before.items()}
    if after != expected:
        raise SystemExit(f"ABORT: item/unit accounting changed in the remap "
                         f"(expected {sorted(expected.items())}, got {sorted(after.items())}). "
                         "Nothing written.")

    gc = doc.setdefault("genon_canonical", {})
    gc.setdefault("repairs", []).append({
        "tool": "repair_unit_order.py", "at": datetime.now().isoformat(timespec="seconds"),
        "kind": "unit_order", "family": "item_self_sufficient",
        "key": "|".join(str(x) for x in key),
        "order": order, "items_reanchored": moved, "why": why,
    })
    return doc


def apply_move_competency_los(doc, order, why, key):
    """The COMPETENCY-LOS family (social_sciences · middle and secondary).

    Added 2026-08-16 for SS·VIII ch 15. The goal-cluster path aborts on this subject with
    "period 1 goal '' routes to no cluster", and that abort is CORRECT: SS periods carry no
    `section_goal`, so there is no cluster to route to. Its handoff is not a flat list either,
    so the item-self-sufficient path does not fit. It is a THIRD shape:

        coverage_handoff = {"C-7.1": {..., "los": [{period_number, section_anchor, ...}, ...]}}

    and that shape needs no reconstruction at all — every entry states its own
    `period_number`. So, like the TWAU family, period -> entry is READ, never inverted from an
    ordering rule.

    WHAT MAKES THIS THE SAFEST OF THE THREE, and the reason it is worth having rather than
    re-authoring at ~Rs 28 a roll: each entry ALSO carries `section_anchor`. After the remap we
    can assert that every entry's anchor is still one of the anchors of the unit it now points
    at. The maths path can only check that a reconstructed goal matches; here the artefact
    carries an independent witness, so a wrong remap cannot pass quietly.

    Nothing inside a unit, an entry or an item is touched. Only `period_number` / `period_ref`
    change, and only because a unit's position did.
    """
    r = doc["result"]
    periods = r["lesson_plan"]["periods"]
    n = len(periods)
    if sorted(order) != list(range(1, n + 1)):
        raise SystemExit(f"ABORT: declared order is not a permutation of 1..{n}. Nothing written.")

    handoff = r.get("coverage_handoff")
    if not isinstance(handoff, dict) or not handoff:
        raise SystemExit("ABORT: this family expects a DICT coverage_handoff keyed by "
                         "competency. Nothing written.")
    by_old_p = {p["period_number"]: p for p in periods}
    if sorted(by_old_p) != list(range(1, n + 1)):
        raise SystemExit("ABORT: period numbers are not exactly 1..N. Nothing written.")

    old_to_new = {old: new for new, old in enumerate(order, start=1)}

    def anchors_of(period):
        raw = period.get("section_anchor") or ""
        return [s.strip() for s in raw.split(" / ") if s.strip()]

    # anchors keyed by OLD number, captured before anything is renumbered
    anchors_by_old = {old: anchors_of(p) for old, p in by_old_p.items()}

    # ── units, in the declared order, renumbered ─────────────────────────────
    new_periods = []
    for new_no, old_no in enumerate(order, start=1):
        p = by_old_p[old_no]
        p["period_number"] = new_no
        new_periods.append(p)
    r["lesson_plan"]["periods"] = new_periods

    # ── every LO entry follows its own unit, then is re-sorted into new order ─
    moved = 0
    for code, block in handoff.items():
        los = block.get("los") or []
        for e in los:
            old = e.get("period_number")
            if old not in old_to_new:
                raise SystemExit(f"ABORT: handoff {code} entry points at unit {old!r}, which is "
                                 f"not in 1..{n}. Nothing written.")
            new = old_to_new[old]
            # THE WITNESS: the entry named a section; that section must still be taught by the
            # unit the entry now points at. A wrong remap fails here, not in a teacher's hand.
            # An entry may name ONE section or the unit's whole composite ("A / B"), so the
            # test is subset, not membership — split both sides and require the entry's
            # sections to be among the unit's. (Membership alone aborted SS·VIII ch 15 p14 on
            # a correct artefact: the entry named "Gardens / Vocational education" whole.)
            want = (e.get("section_anchor") or "").strip()
            want_set = {s.strip() for s in want.split(" / ") if s.strip()}
            if want_set and not want_set <= set(anchors_by_old[old]):
                raise SystemExit(f"ABORT: handoff {code} entry claims section(s) {sorted(want_set)} "
                                 f"on unit {old}, whose anchors are {anchors_by_old[old]}. The "
                                 "artefact disagrees with itself — not a remap this tool may make.")
            e["period_number"] = new
            moved += 1
        block["los"] = sorted(los, key=lambda x: x["period_number"])

    # ── items follow their unit by renumbering period_ref, nothing else ──────
    items = r.get("assessment_items")
    if items is not None and not isinstance(items, list):
        raise SystemExit("ABORT: this family expects a FLAT assessment_items list. "
                         "Nothing written.")
    before: Dict[int, int] = {}
    for it in (items or []):
        v = it.get("period_ref")
        for x in ([v] if isinstance(v, int) else list(v or [])):
            if not isinstance(x, int) or x not in old_to_new:
                raise SystemExit(f"ABORT: item carries period_ref {x!r}, not a unit in 1..{n}. "
                                 "Nothing written.")
            before[x] = before.get(x, 0) + 1
    for it in (items or []):
        v = it.get("period_ref")
        if isinstance(v, int):
            it["period_ref"] = old_to_new[v]
        elif v:
            it["period_ref"] = [old_to_new[x] for x in v]
    after: Dict[int, int] = {}
    for it in (items or []):
        v = it.get("period_ref")
        for x in ([v] if isinstance(v, int) else list(v or [])):
            after[x] = after.get(x, 0) + 1
    expected = {old_to_new[old]: c for old, c in before.items()}
    if after != expected:
        raise SystemExit(f"ABORT: item/unit accounting changed in the remap "
                         f"(expected {sorted(expected.items())}, got {sorted(after.items())}). "
                         "Nothing written.")

    gc = doc.setdefault("genon_canonical", {})
    gc.setdefault("repairs", []).append({
        "tool": "repair_unit_order.py", "at": datetime.now().isoformat(timespec="seconds"),
        "kind": "unit_order", "family": "competency_los",
        "key": "|".join(str(x) for x in key),
        "order": order, "handoff_entries_remapped": moved, "why": why,
    })
    return doc


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
        # Dispatch on the 8-rule FAMILY, declared per move — never sniffed. The two paths
        # differ only in how an item finds its unit, which is the one thing the table exists
        # to say, and a wrong guess here silently re-anchors assessment.
        fn = {"item_self_sufficient": apply_move_item_self_sufficient,
              "competency_los": apply_move_competency_los}.get(
                  mv.get("family"), apply_move)
        doc = fn(doc, mv["order"], mv["why"], key)
        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"    APPLIED — backup at {bak.name}")

        # ── INVALIDATE THE DERIVED PLANS (added 2026-08-11, S5) ──────────────────
        # This tool was the ONE repair of seven that did not do this: repair_anchors,
        # repair_c3, repair_chapter_cg, repair_leaked_deliberation, repair_register and
        # normalize_options all purge, and the most structural repair in the set opted out.
        #
        # It matters MORE here than anywhere, not less. `canonical_version` is the
        # generation's `ledger_ts` (api/data.py), which an in-place repair does not change —
        # so a plan served before the move keeps EXACTLY the filename the cache will look for
        # afterwards, and the pre-move bytes are then served forever. That is ARV-D-034
        # verbatim (the pilot served a repaired-away register breach for four hours), and the
        # founder's chosen resolution was explicitly "the invariant lives in the repair
        # tools", not a fingerprint in the key. A unit permutation is the loudest possible
        # version of it: the stale plan is not merely out of date, it is the plan the move
        # was made to stop being served.
        #
        # Found at S5 because TWAU·V ch 5 had three derived plans on disk and two teachers
        # holding them at the moment the move landed. Nothing was lost only because the
        # founder happened to re-serve after restarting the API.
        _subject, _grade, _ch = key
        gone = purge(_subject, _grade, _ch, reason="genon/repair_unit_order.py")
        print(f"    PURGED {len(gone)} derived plan(s) built from the pre-move canonical"
              + (": " + ", ".join(gone) if gone else " (none on disk)"))
        print("    Teachers holding one re-prepare and get the repaired plan (~11 ms).")
    if not listing:
        print("\nNow re-certify (free):  python3 genon/build_library.py <subject> <grade> <ch> --certify-only")
    return 0


if __name__ == "__main__":
    sys.exit(main())
