# C2 · Library cost — english · III · ch 11 *The Big Laddoo*

Source: `runtime_data/token_log.csv`, every row whose `(subject, grade, chapter_number)` is
`(english, iii, 11)`. Model `claude-sonnet-4-6`. No cache tokens on any run.

| timestamp | call_type | units | input | output | total | ₹ |
|---|---|---|---|---|---|---|
| 2026-08-13T12:36:10 | `canonical_generation` | 12 (top) | 19,734 | 11,739 | 31,473 | **21.6464** |
| 2026-08-13T12:45:08 | `variant_generation` | 10 (p10) | 19,659 | 12,615 | 32,274 | **22.8346** |
| 2026-08-13T12:47:45 | `variant_generation` | 7 (p07) | 19,659 | 10,113 | 29,772 | **19.3818** |
| | **LIBRARY TOTAL** | | 59,052 | 34,467 | 93,519 | **63.8628** |

**Clean path = all-in = ₹63.86.** No reruns, no superseded generations, nothing missing:
3 log rows · 3 ledger files in `genon/out/canonical/english/iii/` · 3 installed canonicals.
The two `promptdump.json` files (12:19:51, 12:21:27) are the P-prep dry runs and cost ₹0.
Mean **₹21.29 per authoring run** — the cheapest library of the campaign so far, against the
SS·IX ch 3 benchmark of ₹110.99 clean / ₹145.70 all-in.

---

## The cost SHAPE does not match the benchmark, and the reason is structural

The C2 benchmark (SS·IX ch 3, 2026-08-01) records: *"input is flat across runs … while output
falls with period count … so a compact variant costs only ~11% less than the top."*

**Half of that holds here. The other half inverts.**

| | top · 12u | p10 · 10u | p07 · 7u |
|---|---|---|---|
| input | 19,734 | 19,659 | 19,659 |
| output | 11,739 | **12,615** | 10,113 |
| ₹ | 21.65 | **22.83** | 19.38 |

**Input is flat** — 19,734 / 19,659 / 19,659, the 75-token delta being the top brief against
the compact brief. That half ports.

**Output does NOT fall with period count: the 10-unit compact wrote MORE than the 12-unit
standard, and cost 5% MORE (₹22.83 vs ₹21.65).** Two structural reasons, both specific to this
stage and both visible on disk:

1. **The assessment is COUNT-INVARIANT at english.** Rule 2's PAIR is two items per
   (section × spine) cell, and the cell count is a property of the chapter, not of the plan —
   so all three canonicals carry **10 items**, at 12, 10 and 7 units alike. A compact pays for
   the full assessment. (This is assessment v1.4's invariance line, proved live: *"the item
   count does not vary with the period count."*)
2. **Bands do not scale down with units.** The top carries **49 bands over 12 units** (4.08
   per unit) because its closing synthesis is lean; p10 carries **50 bands over 10 units**
   (5.00 per unit). The compact wrote more lesson-plan prose in fewer units than the standard
   did in more.

**Budgeting consequence.** "Count runs, not chapters" still holds and is if anything stronger
here. But **"a compact costs ~11% less than the top" must not be generalised** — at an english
stage a compact costs roughly the same as the standard, and can cost more. Price a library as
`N runs × the flat rate`, with no compact discount.

---

## Corpus extrapolation · english preparatory

**39 non-placeholder chapters → 109 authoring runs** (from `canonical_plan.counts` across III,
IV and V, on the real distribution rather than a flat ×3).

| rate | synchronous | +15% defect allowance |
|---|---|---|
| **₹21.29/run** (this pilot) | **₹2,320** | **₹2,668** |
| ₹37.00/run (campaign budgeting figure) | ₹4,033 | ₹4,638 |

The pilot rate is roughly **57%** of the campaign's ₹37/run budgeting figure, which was set on
SS·secondary — the heaviest corner. Preparatory is the lightest: shorter constitutions, smaller
chapters, fewer cells. Treat ₹21/run as a preparatory-stage figure and ₹37 as the upper-middle
bound the corpus projection should keep using until more stages are measured.

**Caveat on the pilot as a rate source.** Ch 11 is tied for the largest chapter in class III at
12 recommended periods, so it is the *expensive* end of its own stage — the ₹21.29 is not
flattered by a small pilot. What it does not sample is `picture_narrative`, whose chapters run
2–6 periods and will pull the stage mean down further.
