#!/usr/bin/env python3
"""S4 · mathematics·secondary LP v1.1 -> v1.2 — Rule 12 / A4: period_numbers lists the
units that TEACH the section, not every unit that touches it.

WHY (founder ruling 2026-08-08, from the maths·IX ch 4 pilot).
`coverage_handoff.period_numbers` is the only route an assessment item has to a unit on this
stage, and `carriers.items_by_handoff` anchors the item at the LAST unit in the list — because
"an item tests its section's whole implied_lo, so it becomes available only when the section
COMPLETES: if the class was not taught all of it, it cannot be tasked on any of it" (the
2026-08-05 anchoring ruling).

Rule 12 said "a section spanning several periods is ONE entry whose period_numbers lists them
all". Applied to a REVISIT that changes nothing about when the LO is delivered, that goes
beyond the anchoring rule's own rationale and costs questions. Measured on ch 4:

  * p11, sec#1 (4.1): Introduction taught at U1, "revisited" at U10/U11 — which are actually
    whole-chapter consolidation and deliver nothing of the row's single LO ("verify the
    consecutive-square invariant ... express the general pattern with n-1, n, n+1").
    period_numbers [1, 10, 11] -> the item anchors at U11 and vanishes at X=9 and X=10.
    THIS IS THE CASE THE AMENDMENT IS FOR.
  * the top's sec#1 lists only [1] and its item survives at every X where U1 is served. The
    same model produced both behaviours on one chapter, so this is variance, not policy —
    which is why it needs a rule rather than a repair.

  * NOT AN EXAMPLE OF THIS DEFECT, and corrected here after checking the LOs (an earlier
    draft of this script cited it as one): the top's sec#6 (4.6) = [6, 13]. It carries TWO
    LOs and each unit delivers one — U6 "Splitting the Middle Term" delivers the factorising
    LO, U13 "Proving and Justifying" delivers the proof-construction LO. Both are teaching
    units, so [6, 13] is CORRECT under this amendment and stays. Its 4.6 items still vanish
    at X=12/13, but for a DIFFERENT reason: anchoring is per-SECTION while outcomes are
    per-LO, so LO1's item anchors at U13 too, though U6 taught it. That is a granularity
    mismatch this amendment does not touch and must not be confused with it — it is recorded
    as an open item in the S4 sign-off.

So the field is narrowed to what the anchoring rule actually needs: the units that DELIVER the
implied_lo. A section introduced early and COMPLETED late still lists both — the last of them
is a teaching unit and the item correctly waits for it. Only units that add nothing to the LO
are excluded.

NOT CHANGED, deliberately: the anchoring rule itself (last listed unit), Rule 6's one-or-two
LOs, Rule 1's section anchoring, and the display. The renderer groups by `section_anchor` with
an anchor FALLBACK for the title (subject.py: `ho_by_period.get(pn) or ho_by_ref.get(key)`), so
narrowing period_numbers cannot blank a group label — proven by the top canonical, whose
U10/11/12 are already absent from every period_numbers list and still render.

Run from the repo root:
    python3 genon/out/stage_prep_mathematics_secondary/apply_s4_rule12_teaching_units.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LP = ROOT / "data/content/constitutions/lesson_plan/mathematics/secondary/lesson_plan_constitution.txt"

edits = []


def sub(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"ABORT [{label}]: anchor found {n} times, expected 1\n---\n{old[:300]}")
    edits.append(label)
    return text.replace(old, new, 1)


lp = LP.read_text()

lp = sub(lp,
         "MATHEMATICS · SECONDARY STAGE · VERSION 1.1",
         "MATHEMATICS · SECONDARY STAGE · VERSION 1.2",
         "VERSION line")

# ── Rule 12 · the MANDATE sentence ────────────────────────────────────────────
lp = sub(
    lp,
    "Exactly ONE entry per anchored section, in chapter-summary order. A section\n"
    "spanning several periods is ONE entry whose period_numbers lists them all. An\n"
    "entry carries one or two implied_lo values (Rule 6).",

    "Exactly ONE entry per anchored section, in chapter-summary order. A section\n"
    "taught across several periods is ONE entry, and period_numbers lists the periods\n"
    "that TEACH it — the ones that deliver the implied_lo(s) recorded here. A period\n"
    "that only REVISITS or consolidates a section already taught is NOT listed, even\n"
    "though it anchors to that section: it adds nothing to the outcome, and listing it\n"
    "would postpone the section's assessment item to a period the class may never\n"
    "reach (the item anchors to the LAST period listed). A section introduced early\n"
    "and COMPLETED later lists both — the later period is a teaching period and the\n"
    "item rightly waits for it. An entry carries one or two implied_lo values (Rule 6).",
    "Rule 12 MANDATE — teaching periods only")

# ── Amendment A4 · the schema comment ─────────────────────────────────────────
lp = sub(
    lp,
    '    "period_numbers":          [integer]  — period number(s) assigned to this section',
    '    "period_numbers":          [integer]  — the period(s) that TEACH this section, i.e.\n'
    "                                           deliver the implied_lo(s) below (Rule 12).\n"
    "                                           A period that only revisits or consolidates\n"
    "                                           the section is EXCLUDED, even though it\n"
    "                                           anchors to it. Ascending order.",
    "A4 period_numbers comment")

# ── the integrity constraint that states the anchoring consequence ────────────
lp = sub(
    lp,
    "- ITEM ANCHORING IS DERIVED, NOT DECLARED: an assessment item's anchor unit is\n"
    "  resolved by the platform from its section_number through this handoff's\n"
    "  period_numbers. MUST NOT emit period_ref (or any unit number) on an assessment\n"
    "  item — at this stage the unique link is the SECTION, and a section may be taught\n"
    "  across several units (Rule 7).",

    "- ITEM ANCHORING IS DERIVED, NOT DECLARED: an assessment item's anchor unit is\n"
    "  resolved by the platform from its section_number through this handoff's\n"
    "  period_numbers, and lands on the LAST unit listed there. MUST NOT emit period_ref\n"
    "  (or any unit number) on an assessment item — at this stage the unique link is the\n"
    "  SECTION, and a section may be taught across several units (Rule 7). Because the\n"
    "  anchor is the last listed unit, period_numbers carries only the units that TEACH\n"
    "  the section (Rule 12): a revisit listed here would withhold the item from a class\n"
    "  that had already been taught the whole section.",
    "INTEGRITY — anchoring consequence")

lp = sub(lp,
         "Mathematics Lesson Plan Constitution · Version 1.1 · Secondary Stage · Internal Document",
         "Mathematics Lesson Plan Constitution · Version 1.2 · Secondary Stage · Internal Document",
         "footer version")

# ── guards: nothing else moved ────────────────────────────────────────────────
for needle in ("lists them all", "period number(s) assigned to this section"):
    if needle in lp:
        raise SystemExit(f"ABORT: superseded wording survives — {needle!r}")
for needle in ("phases[", "band_id", "alphabetically"):
    if needle in lp:
        raise SystemExit(f"ABORT: guard tripped — {needle!r}")
assert lp.count("THE SELF-CONTAINED REGISTER") == 3, "register block disturbed"
assert lp.count("time_bands") >= 2, "time_bands disturbed"

LP.write_text(lp)
print(f"OK — {len(edits)} edits applied:")
for e in edits:
    print(f"  · {e}")
