# C9 — assessment anchoring across the serve · english · IX · ch 7 *Vitamin-M*

**Date:** 2026-08-12 · seven serves re-derived against the **re-authored** library (X = 8, 9, 11,
12, 13, 15, 16) · engine 19 · LP v1.2 / assessment v1.4

**Verdict: all four checks PASS — and C9 corrects one of my own C6 findings and downgrades the
other.** The two defects I raised at C6 turn out to be the engine doing exactly what this step
specifies. That is worth more than a pass: C6 read the outputs without reading the contract they
were written against.

---

## The anchor table — every item, every serve

`period_ref` is the SITTING number in the served plan. "last sitting" is computed independently
from the served units, not read from the file.

| X | item → sitting | last sitting teaching that cell | match |
|---|---|---|---|
| **16** (var 17) | RFC 8 · LIS 12 · SPK 14 · WRT 15 · VG 11 · BYT 16 | 8 · 12 · 14 · 15 · 11 · 16 | ✅ 6/6 |
| **15** (var 14 ← 17) | RFC 6 · LIS 9 · SPK 10 · WRT 12 · VG 8 · BYT 14 | 6 · 9 · 10 · 12 · 8 · 14 | ✅ 6/6 |
| **13** (var 14) | RFC 6 · LIS 9 · SPK 10 · WRT 12 · VG 8 | 6 · 9 · 10 · 12 · 8 | ✅ 5/5 |
| **12** (var 14) | RFC 6 · LIS 9 · SPK 10 · VG 8 | 6 · 9 · 10 · 8 | ✅ 4/4 |
| **11** (var 10 ← 17) | RFC 5 · LIS 8 · SPK 8 · WRT 9 · VG 7 · BYT 10 | 5 · 8 · 8 · 9 · 7 · 10 | ✅ 6/6 |
| **9** (var 10, below floor) | RFC 5 · LIS 8 · SPK 8 · WRT 9 · VG 7 · **BYT 10 `unscheduled`** | 5 · 8 · 8 · 9 · 7 · *(dropped)* | ✅ 6/6 |
| **8** (var 10, below floor) | RFC 5 · LIS 8 · SPK 8 · VG 7 · **WRT 9 + BYT 10 `unscheduled`** | 5 · 8 · 8 · 7 · *(both dropped)* | ✅ 6/6 |

Note the synthesis unit never appears as an anchor: it teaches no cell, so `is_synthesis` keeps
it out of the index. At X=11 the RFC item anchors at sitting 5, not at the borrowed closer that
revisits RFC — which is the correct reading of "the last sitting that TEACHES this cell".

---

## The four checks

**1 · Prefix remap — PASS.** Every item of the chosen variant whose anchor unit is served
carries a `period_ref` pointing at that unit's **sitting** number, and every one of them equals
the independently computed last-teaching sitting. 37 items across seven serves, zero mismatches.

**2 · Borrowed unit brings its own items — PASS, vacuously, and the reason is structural.**
The only borrowed units in this library's sweep are (a) the standard's **synthesis** at X = 11
and 15 and (b) self-fills, where lender and host are the same file. A synthesis unit anchors no
item at this stage — it teaches no (section × spine) cell, by the constitution's own count rule —
so there are no items for it to bring. This is the same outcome testing.md already records for
the derived-anchor stages (C9.2 "unsatisfiable on precisely the Case-1 borrow"), reached here by
a different route: not a missing handoff row, but a unit that legitimately anchors nothing.
**Nothing is owed** — no item is lost, because none existed to lose.

**3 · Unserved anchors — PASS on all four sub-checks.**

- **(a) no empty `period_ref` anywhere** — 37 of 37 items carry a ref. ✅
- **(b) items whose anchor unit was not served are ABSENT, and counted** — X = 12 ships 4 items
  with `assessment_items_unserved: 2`; X = 13 ships 5 with `1`. ✅
- **(c) below-floor: the dropped units' items ARE present, anchored to the dropped unit's sitting
  number IN THIS PLAN, flagged `unscheduled: true`** — X = 9: `Q-BT-A-1`, `period_ref: [10]`,
  **`unscheduled: true`**, and sitting 10 is precisely where `dropped_units` puts the dropped
  Beyond-the-Text unit. X = 8: `Q-WRT-A-1` **[9]** and `Q-BT-A-1` **[10]**, both flagged,
  matching two dropped units. Never the lender's numbering. ✅
- **(d) exports omit exactly the `unscheduled` items** — the export filter is C12's surface;
  carried forward there rather than asserted here.

**4 · No cross-variant references — PASS.** Each serve's items come from its chosen variant
alone, and the item ids make it legible: X = 11 carries p10's `Q-VG-A-1` / `Q-BT-A-1`, X = 15
carries p14's `Q-VGR-A-1` / `Q-BXT-A-1`, X = 16 carries the re-authored top's `Q-LST-A-1`. No
mixing, in either direction.

---

## Two corrections to my own C6 findings

### ARV-D-135 — WITHDRAWN. I misread the artefact.

At C6 I reported that the below-floor serve "keeps a question for a cell it dropped, anchored to
a sitting that does not exist". Two of the three parts of that sentence are wrong.

The item **is flagged `unscheduled: true`**, and sitting 10 **does** exist in this plan's own
numbering — it is the dropped unit's sitting, which `result.dropped_units` carries verbatim.
That is not a defect; **it is check 3(c), verbatim**, and it is deliberate: e13 (ARV-D-037, S1)
established exactly this shape after the opposite behaviour printed 7 of 20 questions about units
a class never had. The material rides along, flagged, so a teacher can set it as the self-study
the coverage note offers — and exports drop it.

I printed `period_ref` and did not print the `unscheduled` key beside it. The lesson is small and
sharp: **when the engine has a documented state for a case, read the state before rating the
output.** Defect withdrawn, status `closed` with this note.

### ARV-D-134 — DOWNGRADED S2 → S3, and re-titled.

The absence of the two items at X = 12 is **specified behaviour** (check 3b), not a loss, and
pedagogically it is the right call: Writing's cell is taught across p14's U11 *and* U12, the
serve stops before U12, so the class drafted the article but never did the revision sitting. An
item tests the cell's **whole** `implied_lo` and becomes available only when the cell completes
(founder, 2026-08-05). Withholding it is the anchoring doctrine working, not failing.

What survives, and it is real but smaller than I claimed: **the served plan says two different
things.** `coverage_handoff` still carries all six cells — the artefact asserts complete
coverage — while the paper ships four items, and the only record of the difference is
`genon.assessment_items_unserved`, which is provenance no teacher reads. There is no
`section_coverage_note`, because nothing was *dropped* in the LP sense.

So the defect is a **declaration gap, not a mis-anchoring**: S3, contract drift a teacher would
notice only by counting. The fix, if you want one, is one sentence in the same channel the
below-floor case already uses — *"two questions are held back: the Writing and Beyond-the-Text
work is not complete at this length"* — rather than any change to anchoring.

**And english is where it shows.** With one item per cell, holding two back is a third of the
paper; on SS·secondary the same rule holds back 2 of 18. The mechanism is subject-agnostic; the
visibility is english's, and that is an argument about the item-count formula (Rule 2), not about
the serve.

---

## Exit

**Zero mis-anchored items across seven serves; every unserved anchor accounted for.** C9's exit
condition is met. One item owed to C12: that exports omit exactly the `unscheduled` items.
