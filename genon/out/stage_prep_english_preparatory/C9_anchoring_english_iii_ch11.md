# C9 · Assessment anchoring across the serve — english · III · ch 11

Read on all **seven C6 served plans**, 70 items in total. Library [12, 10, 7] · floor 7.

**Verdict: checks 1, 2, 3(a), 3(b), 3(d) and 4 PASS. Check 3(c) passes on the ITEMS and fails
on the HANDOFF ROWS — one defect, with a mechanical cause now named.**

---

## The anchor table

| plan | sittings | dropped | items | unscheduled | `unserved` | anchors in range | empty `period_ref` | items on the synthesis sitting | cross-variant refs |
|---|---|---|---|---|---|---|---|---|---|
| X=6 below floor | 1–6 | **7** | 10 | **2** | 0 | ✓ | 0 | — | 0 |
| X=8 rescue | 1–8 | — | 10 | 0 | 0 | ✓ | 0 | **none** (sitting 8) | 0 |
| X=9 fill/single | 1–9 | — | **8** | 0 | **2** | ✓ | 0 | — | 0 |
| X=11 synthesis | 1–11 | — | **8** | 0 | **2** | ✓ | 0 | **none** (sitting 11) | 0 |
| X=13 surrender | 1–12 | — | 10 | 0 | 0 | ✓ | 0 | **none** (sitting 12) | 0 |
| mixed 40/50 | 1–12 | — | 10 | 0 | 0 | ✓ | 0 | **none** (sitting 12) | 0 |
| X=12 @ 50 min | 1–12 | — | 10 | 0 | 0 | ✓ | 0 | **none** (sitting 12) | 0 |

---

## 1 · Prefix remap — **PASS**, and it confirms Rule 8A end to end

Every item's `period_ref` equals its `unit_ref` and points at a **served sitting** (or, for the
two `unscheduled` items, at the dropped unit's sitting). Zero out-of-range anchors across 70
items.

**Worth stating because it is this stage's whole anchoring story:** the *authored* files carry
**no `period_ref` at all** — Rule 8A prohibits emitting `period_ref` / `period_number` /
`unit_ref`, and the model obeyed it in all three canonicals. The anchor is therefore stamped
entirely by the carrier (`cell_resolver` → `items_with_units`) at compile time from the
(section × spine) CELL, and remapped unit → sitting at serve time. A6's confirmation at P2, the
carrier's delegation at P5.5 and this remap are one chain, and it holds live.

## 2 · Borrowed unit brings its own items — **VACUOUS, as predicted**

The only borrowed unit anywhere in the serve set is the standard's **synthesis** (X=8 and
X=11 — C8 established there is no other foreign borrow). A synthesis unit teaches no cell, so
no item anchors to it: **zero items on the synthesis sitting in every plan that carries one.**

Predicted at C3 ("C9.2's 'a borrowed unit brings its own items' is vacuous for the closing
unit") and inherited from S11 and S10 rather than discovered here. The check is unsatisfiable at
english by construction, not unmet. What C9 must check instead — that the standard's ten items
and a compact's ten are the SAME five cells — holds in all three canonicals.

## 3(a) · No empty `period_ref` — **PASS**

Zero, across all 70 items on all seven plans.

## 3(b) · Unserved-anchor items ABSENT and counted — **PASS, and the pattern is systematic**

X=9 and X=11 each serve **8 of 10** items, with `genon.assessment_items_unserved: 2`. The two
absent items are e13's rule working: *an item whose unit is not in the plan is not in the plan.*

**Which two is not random.** In both plans it is **`Q-READ-B-2` and `Q-ORAL-B-2`** — the
**slot-2 (production)** items of the two cells whose completing unit was not served (p10's u10
at X=9; the standard's u11, skipped, at X=11). Slot 1 survives in both cases.

That is **Rule 8A's two-stage scoping behaving exactly as designed**: slot 1 is scoped to the
cell's *early* teaching and remains answerable; slot 2 presumes the *whole* cell and correctly
falls away with it. The dispersion the PAIR amendment licensed is what makes the loss precise
rather than arbitrary.

> **And the PAIR cut this problem's blast radius by a third.** S11's C9 recorded the same shape
> (ARV-D-134, downgraded to S3 and accepted) at **2 of 6 items = 33% of the paper**, and framed
> it explicitly as *"an argument about the Rule 2 item-count formula, not about the serve"*.
> Under the PAIR it is **2 of 10 = 20%**. The density amendment was made for coverage, not for
> this — an unlooked-for benefit worth carrying to S10's and S11's re-reads.

## 3(c) · Below-floor dropped units — **items PASS, handoff rows FAIL**

**The items are right.** X=6 carries all 10, with `Q-BEXT-B-1` and `Q-BEXT-B-2` flagged
`unscheduled: true` and anchored to **sitting 7**, the dropped unit's sitting in this plan.
`genon.assessment_items_unscheduled: 2`.

> **An honest limitation of this row.** p07's u7 is *also* numbered 7, so the anchors coincide
> and **this case cannot prove the "never the lender's own numbering" clause**. It needs a serve
> where the dropped unit's sitting number differs from its number in the lender — which this
> library's shape does not produce. Recorded rather than claimed.

**The handoff rows are not flagged.** The clause requires the dropped units' items to be present
*"with their handoff rows restored and flagged"*. X=6's `coverage_handoff` carries the
`beyond_text` contribution with keys `implied_lo · section_context · section_id · section_title ·
section_type · tasks_anchored` — **no `unscheduled`, no flag of any kind.**

**The cause is mechanical, and it is not that english was skipped deliberately.**
`serve.py:803–822` restores and flags dropped rows by iterating `blk["los"]` and reading each
row's `period_number`:

```python
for lo in blk.get("los", []):
    sit = dropped_lender_unit_to_sitting.get(int(lo.get("period_number", -1)))
    ...
    lo2["unscheduled"] = True
```

English's handoff is `_ENGLISH_SPINE_CELL` — a spine-keyed dict of `section_contributions[]`
with **no `los` array and no per-row unit number**. The loop finds nothing, so both the filter
and the flag are **no-ops on the entire english family**. It is the same shape-blindness
`to_engine_handoff` was taught to fix for coverage filtering at S11, on the other half of the
same code path.

**Consequence: the served plan states two different things.** `coverage_handoff` says all five
cells were taught; the plan teaches four and declares the fifth dropped in three other places —
`section_coverage_note`, `result.dropped_units`, and the two `unscheduled` items. **Filed as a
defect** (§7): this is ARV-D-134's class with a second instance and, newly, a named cause.

> **One thing that did NOT fire, stated because it easily could have.** X=9's served handoff is
> byte-identical to p10's and happens to be **accurate**: p10's unserved u10 anchored only
> `(reading, 0)` and `(oracy, 0)`, tasks already anchored in earlier units, so no
> `tasks_anchored` entry advertises work the class never did. That is a property of this
> chapter, not of the engine — the same no-op filter would pass an inaccurate handoff through
> unchanged.

## 3(d) · Exports omit exactly the unscheduled items — **PASS, verified live**

Run through `/api/plans/english/iii/{file}/export/assessment` against the live API:

| export | bytes | the dropped cell's content (float / sink) |
|---|---|---|
| **X=6 below floor** | 89,687 | **absent** |
| top canonical (control) | 90,030 | **present** |

So the export ships 8 items where the screen shows 10, which is ARV-D-037's rule holding: the
dropped units' questions travel with them **on screen** (`view.dropped_lp` is present in the
`/view` payload, and all ten Q-ids appear there) and **not** into the printed artefact.

## 4 · No cross-variant references — **PASS**

Zero references to another variant, by filename, count or any other form, in any of the 70 items.

---

## What is filed

**One defect** — the unflagged handoff rows (3(c)). **No mis-anchored item anywhere**, and every
unserved-anchor item is accounted for by count. Exit is otherwise met.
