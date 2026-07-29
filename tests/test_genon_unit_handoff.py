#!/usr/bin/env python3
"""Rule 16 (LP v1.3) — container text is SELECTED from the canonical, never composed.

Covers the selector's three cases (single unit / adjacent pair / 3+ units taking the
pair that carries the most MINUTES of the sitting), the degraded fallback for a canonical
predating Rule 16, and the certification validator that keeps a spliced title out of a
certified canonical.

The 3+ case was decided as "last pair" in v1.3 and re-decided by measurement on 2026-07-28
(partition v0.5): at 12 x 50 the SS-IX ch 5 plan cut P3 as units 4-5-6 with minutes
14 / 32 / 4, where the last pair names a four-minute scrap. The cases below are that plan's
real shapes.

Stdlib only, no network, no spend:  python3 tests/test_genon_unit_handoff.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aruvi_core.genon.partition import (                              # noqa: E402
    handoff_vocab, heaviest_pair, select_container_text, validate_unit_handoff)

FAILED = []


def check(label, cond, got=None):
    print(("PASS  " if cond else "FAIL  ") + label + ("" if cond else f"   got: {got!r}"))
    if not cond:
        FAILED.append(label)


UNITS = {n: {"activity_title": f"Title {n}", "teacher_notes": f"Notes {n}"} for n in range(1, 6)}
HANDOFF = {f"{n}-{n+1}": {"title": f"Joint {n}{n+1}", "teacher_notes": f"Pair note {n}{n+1}"}
           for n in range(1, 5)}

# ── the three span cases ──────────────────────────────────────────────────────
t, notes, key, hit = select_container_text(HANDOFF, UNITS, [3])
check("single unit keeps its authored title", t == "Title 3", t)
check("single unit keeps its authored notes", notes == "Notes 3", notes)
check("single unit consults no handoff", key is None and hit, (key, hit))

t, notes, key, hit = select_container_text(HANDOFF, UNITS, [2, 3])
check("adjacent pair takes its own entry", (t, notes) == ("Joint 23", "Pair note 23"), (t, notes))
check("pair reports the key it used", key == "2-3" and hit, (key, hit))

# 3+ units: the pair carrying the most minutes of the sitting (partition v0.5).
# P3 of the 12 x 50 plan — the opening tail outweighs the closing scrap.
t, notes, key, hit = select_container_text(HANDOFF, UNITS, [2, 3, 4], {2: 14, 3: 32, 4: 4})
check("three units take the HEAVIEST adjacent pair", key == "2-3", key)
check("three units get that pair's text", (t, notes) == ("Joint 23", "Pair note 23"), (t, notes))

# P2 of the same plan — here the heaviest pair IS the last one; the old rule was right.
t, notes, key, hit = select_container_text(HANDOFF, UNITS, [2, 3, 4], {2: 9, 3: 26, 4: 15})
check("heaviest pair agrees with the last pair when it should", key == "3-4", key)

t, notes, key, hit = select_container_text(HANDOFF, UNITS, [1, 2, 3, 4], {1: 4, 2: 6, 3: 20, 4: 20})
check("four units weigh every adjacent pair", key == "3-4" and t == "Joint 34", (key, t))

check("a tie goes to the later pair", heaviest_pair([1, 2, 3], {1: 10, 2: 10, 3: 10}) == (2, 3),
      heaviest_pair([1, 2, 3], {1: 10, 2: 10, 3: 10}))
check("the heaviest pair is always adjacent and in order",
      heaviest_pair([5, 6, 7, 8], {5: 30, 6: 2, 7: 2, 8: 25}) == (5, 6),
      heaviest_pair([5, 6, 7, 8], {5: 30, 6: 2, 7: 2, 8: 25}))
check("no minutes supplied -> the old last-pair behaviour",
      select_container_text(HANDOFF, UNITS, [2, 3, 4])[2] == "3-4")
check("a two-unit sitting is unaffected by minutes",
      select_container_text(HANDOFF, UNITS, [2, 3], {2: 1, 3: 49})[2] == "2-3")

# ── degraded path: a canonical with no Rule-16 table still yields a plan ───────
t, notes, key, hit = select_container_text({}, UNITS, [2, 3])
check("missing table falls back, does not raise", t and notes, (t, notes))
check("missing table is reported as a miss", hit is False and key == "2-3", (hit, key))
check("fallback title carries both units", t == "Title 2 / Title 3", t)
check("fallback notes carry both units", notes == "Notes 2\n\nNotes 3", notes)
check("a half-filled entry still counts as a miss",
      select_container_text({"2-3": {"title": "Joint 23"}}, UNITS, [2, 3])[3] is False)

# ── the certification gate ────────────────────────────────────────────────────
check("complete table passes", validate_unit_handoff(HANDOFF, 5) == [],
      validate_unit_handoff(HANDOFF, 5))
check("absent table is a problem", validate_unit_handoff(None, 5) == ["unit_handoff missing (Rule 16)"])
check("a missing pair is named",
      any("missing 1 pair" in p for p in validate_unit_handoff(
          {k: v for k, v in HANDOFF.items() if k != "3-4"}, 5)))
check("a non-adjacent pair is rejected",
      any("non-adjacent" in p for p in validate_unit_handoff(dict(HANDOFF, **{"1-3": HANDOFF["1-2"]}), 5)))

spliced = dict(HANDOFF)
spliced["2-3"] = {"title": "Title 2 and Title 3", "teacher_notes": "n"}
check("a conjunction-joined title is rejected (Rule 16 prohibition 1)",
      any("banned joiner" in p for p in validate_unit_handoff(spliced, 5)))
for joiner in (", then ", " into ", " & ", " with ", " / ", " — "):
    bad = dict(HANDOFF)
    bad["2-3"] = {"title": f"Title 2{joiner}Title 3", "teacher_notes": "n"}
    check(f"joiner {joiner!r} rejected",
          any("banned joiner" in p for p in validate_unit_handoff(bad, 5)))

# ── the concreteness gate (Rule 16 prohibition 1) ─────────────────────────────
PERIODS = [
    {"period_number": 1, "activity_title": "Society vs State", "section_anchor": "Understanding Early Indian Society",
     "section_context": "society versus state, custom and law"},
    {"period_number": 2, "activity_title": "The Vedas as Evidence", "section_anchor": "The Beginnings",
     "section_context": "Vedic corpus, oral transmission, Sapta-Sindhu"},
]
VOCAB = handoff_vocab(PERIODS)
PAIR = {"1-2": {"title": "", "teacher_notes": "n"}}


def concreteness(title):
    PAIR["1-2"]["title"] = title
    return [p for p in validate_unit_handoff(PAIR, 2, VOCAB) if "names no content" in p]


check("a title citing a unit's own term passes", not concreteness("Reading the Vedic Corpus as Evidence"))
check("stems match across inflections (Vedas/Vedic)", not concreteness("What the Vedas Can Show"))
check("a purely abstract title is rejected", concreteness("Who Could Take Part"))
check("'Early Indian' alone does not rescue it", concreteness("How Early Indian Life Began"))
check("no vocab supplied -> gate is skipped", not [p for p in validate_unit_handoff(
      {"1-2": {"title": "Who Could Take Part", "teacher_notes": "n"}}, 2) if "names no content" in p])

over = dict(HANDOFF)
over["2-3"] = {"title": "Fine Title", "teacher_notes": "word " * 120}
check("an over-budget note is rejected",
      any("> 90" in p for p in validate_unit_handoff(over, 5)))

print("\n" + ("ALL PASS" if not FAILED else f"{len(FAILED)} FAILED: {FAILED}"))
sys.exit(1 if FAILED else 0)
