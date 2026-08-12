# C6 — API serve checks · english · IX · ch 7 *Vitamin-M*

**Date:** 2026-08-12 · **Library authored at 50 min** · engine 19 · LP v1.2 / assessment v1.4
· identities served to **kumar1**, non-identities to **kumar2**, the mixed week to **kumar3**

Ten serves on disk. Cell abbreviations: **RFC** reading_for_comprehension · **VG**
vocabulary_grammar · **LIS** listening · **SPK** speaking · **WRT** writing · **BYT** beyond_text.
The chapter's registry is those six, in that on-page order.

---

## The table asked for — every NON-IDENTITY serve

| X | file | mode | variant | borrowed | **cells in LP** | **cells in assessment** | **items** | declared? |
|---|---|---|---|---|---|---|---|---|
| **9** | `…50m9…` | fill/single **−1s** | 10 | 10 | **5** — RFC VG LIS SPK WRT | **6** — RFC LIS SPK WRT VG **BYT** | **6** | ✅ coverage note + `dropped_units` |
| **11** | `…50m11…` | rescue/complete (from 14) | 10 | **17** | 6 — all | 6 — all | 6 | ✅ closing-sitting note |
| **12** | `…50m12…` | fill/single | 14 | 14 | 6 — all | **4** — RFC LIS SPK VG | **4** | ❌ **nothing** |
| **13** | `…50m13…` | fill/single | 14 | 14 | 6 — all | **5** — RFC LIS SPK WRT VG | **5** | ❌ **nothing** |
| **15** | `…50m15…` | rescue/complete (from 17) | 14 | **17** | 6 — all | 6 — all | 6 | ✅ closing-sitting note |
| **15** | `…60m2-50m13…` | rescue/complete (from 17) | 14 | **17** | 6 — all | 6 — all | 6 | ✅ (mixed week) |
| **16** | `…50m16…` | fill/single | 17 | 17 | 6 — all | 6 — all | 6 | — none needed |

*(Identities for reference: X = 10, 14, 17 all serve their own canonical whole — 6 cells in the
LP, 6 in the assessment, 6 items, no new file written.)*

**Read the two columns against each other and the finding is in the middle of the table.** LP
coverage and assessment coverage agree on five of the seven non-identity serves and **disagree in
opposite directions on the other two**.

---

## Finding 1 — a served plan can TEACH a cell and LOSE its question (X = 12, 13) · ARV-D-134 · S2

X = 12 serves p14's prefix plus one borrowed unit. The LP covers **all six cells**. The
assessment carries **four items**. Writing and Beyond-the-Text are taught and unassessed.

The mechanism is the anchoring rule meeting prefix serving, and it is exact:

| cell | last unit teaching it in p14 | served at X=12? | item survives? |
|---|---|---|---|
| RFC | 6 | yes | ✅ |
| VG | 8 | yes | ✅ |
| LIS | 9 | yes | ✅ |
| SPK | 10 | yes | ✅ |
| WRT | **12** | no | ❌ |
| BYT | **14** | no | ❌ |

An item anchors at its cell's **last** unit (founder ruling 2026-08-05 — an item tests the
cell's whole `implied_lo`, so it becomes available only when the cell completes). A prefix serve
can include a cell's *first* unit and stop before its last; the cell is then taught, appears in
the LP and in the handoff, and its item is filtered out. `genon.assessment_items_unserved` says
`2` — **in the provenance block, which no teacher sees**. `section_coverage_note` is `None`,
`dropped_units` is empty, and the six-spine handoff is carried in full, so the served artefact
asserts complete coverage while shipping a paper missing a third of itself.

**English feels this harder than any stage tested so far**, because Rule 2 gives it exactly one
item per cell: two lost items is 33 % of the assessment. On SS·secondary the same mechanism
costs a couple of items out of eighteen.

**Not the same thing as the below-floor drop.** That case is declared (Finding 2); this one is
silent, and it happens **inside the band**, at counts a teacher will routinely ask for.

## Finding 2 — a DROPPED cell keeps its question, anchored to a sitting that does not exist (X = 9) · ARV-D-135 · S2

The inverse. At X = 9 (below the floor of 10) the LP legitimately drops **BYT** — declared
properly: `section_coverage_note` names it (*"Time budget short of the chapter's full span:
A|beyond_text could not be scheduled"*) and `dropped_units` carries the lost unit flagged
`unscheduled`. That half is exactly right.

But the assessment still carries **Q-BT-A-1**, and it carries `period_ref: [10]` — **sitting 10
of a nine-sitting plan**. `genon.assessment_items_unscheduled: 1` records it in provenance; the
item itself is neither dropped nor marked. A teacher printing this paper asks her class a
question on the one thing the plan told her she would not have time to teach.

---

## The rest of C6's matrix — every row as expected

| Row | Identity | Result |
|---|---|---|
| X = each canonical's count (10, 14, 17) | kumar1 | `identity`, the canonical's own filename, **no new file written** — three files on disk, all authored, none served. |
| X between canonicals (complete fill) | kumar2 | X = 12, 13, 16 → `mode: fill`, `fill_class: single`, `uncovered_sections` empty, no note needed. ✅ |
| X where the prefix completes coverage early | kumar2 | X = 11 and 15 → `complete_rescue`, **`borrowed_from: 17`** — the STANDARD's synthesis unit, from a plan two counts up — with the closing-sitting note. ✅ |
| X = floor − 1 | kumar2 | X = 9 → `fill` with `uncovered_sections` non-empty, note naming `A|beyond_text`, `dropped_units` carrying the lost unit verbatim and flagged. ✅ (and see Finding 2) |
| mixed-duration weekly matrix | kumar3 | 60 × 2 + 50 × 13 = 15 sittings. **`duration_sequence` = 50 50 50 50 60 50 50 50 50 50 60 50 50 50 50** — the shortest sitting opens the week, both 60s sit interior and are **not adjacent** (positions 5 and 11). Bands re-tiled to the scaled durations with **zero gaps or overruns** on all 15. ✅ |
| X = A_top + 1 | kumar2 | **NOT RUN** — no 18-period serve on disk. The certifier's sweep exercised X = 18 and 19 and both returned `surrender`, so the engine path is proven; what is untested is the API's surrender *response* — `coverage_note` carrying the surrender sentence, and `period_schedule_display` printing the SERVED count rather than the ask (e10). One request closes it. |

**Identity fires only at the authored duration**, as the template requires: the mixed-duration
15 wrote a file and scaled, where the 50-minute 15 also wrote one — and the three identity counts
at 50 min wrote nothing.

---

## What C7–C9 inherit

- **C9 owns both findings.** They are one seam read from two sides: the item's unit is resolved
  once, at authoring time, against a plan the teacher may only partly receive.
- **C8's joint is unchanged and now has a number**: X = 11 and 15 are the Case-1 borrows, both
  taking unit 17 from the standard — the same unit C3's ARV-D-132 flagged for requiring U15's
  draft article. At X = 11 the host is p10, whose writing unit asks for the whole article in one
  sitting; that is the transition to read.
- **One serve is owed** (X = 18) to close C6's last row.
