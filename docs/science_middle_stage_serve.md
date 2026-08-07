# Stage-granularity serving — science · middle

**Addendum to `docs/variant_canonical_architecture.md` (read §0 there first).**
Version 1.1 · 2026-08-07 · founder rulings of 2026-08-07. §4 implemented the same day (e17).

This is the campaign's **one structural exception**. Ten of the eleven subject·stages anchor
learning units to textbook SECTIONS; science·middle anchors them to the chapter's COGNITIVE
PROGRESSION ARC. That was a deliberate design decision — teaching and its testing are aligned
to the arc — and it makes the unit-granularity serve engine inapplicable here. This file
records what replaces it and what must change in code before S6's C1.

---

## 1. Why the standard engine cannot serve this stage

The serve engine's atom is the UNIT: it takes a prefix of X−1 units from a canonical and
borrows a unit for slot X, and it reasons about coverage in sections.

Neither half works here.

**There are no sections.** The LP constitution (Rule 1) derives the arc from the chapter
summary at generation time — "the ordered sequence of increasingly demanding cognitive
operations from first encounter with the phenomenon to the highest-order operation the
dissolution test sentence names." Units belong to arc stages, not to sections. Assessment
items link to stages and to nothing else; `coverage_handoff` carries exactly one entry per
stage. There is no `section_anchor` in the schema, and there cannot honestly be one: the arc
rides over the whole summary and is not decomposable into the book's section list.

**A prefix is not a plan.** A stage spans several units (Rule 2), its implied LO is the
outcome of the *complete* stage (Rule 5), and its assessment items test that LO. Truncating
a 15-unit canonical to 13 leaves the last stage 2 units short: the class is tested on an
operation it was taught 60% of. And unlike a dropped section, there is no honest sentence to
declare it with — "you covered part of a cognitive operation" is not actionable. So no
prefix of a canonical is a valid plan, and with truncation dead, borrowing (which exists
only to fill the hole truncation makes) is dead too.

**Arcs are not comparable across canonicals** (founder, 2026-08-07). Stage count, labels and
structure are derived freshly at each generation and may differ between a chapter's own
canonicals. There is therefore no shared registry of any kind for this stage, and **stages
may never be borrowed between canonicals.**

The single fact every canonical of a chapter shares is the arc's TERMINUS: Rule 1 requires
the final stage to correspond to the operation named in the dissolution test sentence. That
one commonality is what licenses the synthesis borrow in §2, and it is the only thing a
borrowed synthesis unit may assume.

---

## 2. The serve law

Given a library `{…, K, …}` of canonical counts and a request for X sittings:

| Case | Rule | Mode |
|---|---|---|
| X = some K | serve that canonical whole | `identity` |
| X = K + 1 | that canonical whole, plus the TOP canonical's synthesis unit as sitting X | `synthesis` |
| X < lowest K | the lowest canonical truncated to X; the remainder carried as `dropped_units` | `truncation` |
| X > top | serve the top; `surrendered_periods` = X − top | `surrender` |

Notes that make this law total:

- **No surrender inside the band.** Guaranteed by the density rule (§3), not by a fallback.
- **The synthesis comes from the TOP, always** — it is the library's only synthesis unit.
- **Duration scaling is unchanged.** Identity fires only at the authored duration; any other
  duration serves the canonical whole with proportional band scaling, exactly as today.
- **Below the floor, partial stages ARE tolerated.** That range is already declared-deficit
  territory, and showing the teacher the units she will not reach is more useful than
  refusing. Drops ride e09's existing channel: `result.dropped_units`, flagged
  `unscheduled`, rendered online via `/view` → `view.dropped_lp`, **omitted from exports**
  (founder, 2026-08-07 — consistent with every other stage; the dropped tail is not
  home-study material to be handed out).
- **The last stage's items ride with the last unit of that stage**, which is the existing
  carrier rule (`aruvi_core/genon/carriers.py`, the 2026-08-05 anchoring ruling: where a
  group maps to several units the item anchors to the LAST). So when a below-floor
  truncation drops that unit, the stage's items travel with it as `unscheduled`. No new
  behaviour is needed.
- **The borrowed synthesis brings NO assessment items, and joins the host's LAST stage**
  (founder, 2026-08-07 — **reverses the earlier ruling on the same day**, ARV-D-067).
  C9.2's "a borrowed unit brings its own items" presupposes UNIT-level anchoring. Here a
  unit has no items of its own: it inherits its whole STAGE's set. So the borrow imported
  the top's entire final-stage assessment into a class that never had that stage's earlier
  units, and the lender's handoff row grew a phantom sixth stage holding one sitting. The
  variant has already met its own per-stage minimums (assessment v1.5), so it needs no more
  items; the top's stage keeps its questions. The unit arrives as the closing sitting of the
  host's final stage, content intact, with nothing anchored to it. The earlier ruling stands
  for the ten section-axis stages, where a borrowed unit really does own its items.

---

## 3. Density: the spacing is forced, not tuned

The bridge between canonicals is exactly ONE synthesis unit, so a gap of 2 is the largest
the law in §2 can cross. Canonical counts must therefore step down by **exactly 2** from the
standard, with the floor included:

```
counts = [A, A-2, A-4, …] down to the floor C = round(0.6 × A), C always included
```

Worked, on real science·VIII rows:

| Chapter | Standard | Floor | Today (equal dispersion) | Under this rule |
|---|---|---|---|---|
| 6 · Pressure, Winds, Storms | 12 | 7 | 12, 10, 7 | **12, 10, 8, 7** |
| 5 · Exploring Forces | 18 | 11 | 18, 15, 11 | **18, 16, 14, 12, 11** |
| 1 | 6 | 4 | 6, 4 | **6, 4** (unchanged) |

**Cost, measured (2026-08-07, after the rule landed in `genon/master_plan.py`)** — no longer an
extrapolation. Across science·middle's 37 chapters: **107 → 154 authoring runs, +47 ≈ ₹1,739**
at ₹37/run (VI 50 · VII 51 · VIII 53). Confined to one stage of eleven, and it buys the
elimination of surrender inside the band. Verified exhaustively: for every (top, floor) pair
from 3 to 25, the generated set is strictly descending, duplicate-free, includes both endpoints,
and leaves **no X in [floor, top] unservable** by identity or a K+1 synthesis borrow.

---

## 4. Work required before S6 · C1 — **COMPLETE, 2026-08-07 (engine e17)**

All nine items landed and are regression-checked. The gate on S6's C-cycle is lifted.

1. **The subject plugin declares serve granularity.** `Subject.genon_serve_granularity` and
   `genon_has_section_axis` on the interface (`aruvi_core/subjects/base.py`), implemented on
   the science plugin: middle → `plan` / no section axis, secondary → `unit` / section axis.
   `serve.py` asks `carriers.serve_granularity()` and never learns a subject's name.
2. **`compile.py`'s `section_anchor` read is carrier-mediated.** `carriers.unit_anchor` still
   raises on a section-axis stage (a malformed SS plan fails exactly as loudly as before) and
   returns `None` where the axis does not exist.
3. **`serve.py`'s plan-granularity path** — `select_whole_plan()`, implementing §2 as one rule:
   serve the largest sitting count ≤ X that is either a canonical's own K or K+1. Identity,
   the synthesis borrow, surrender and below-floor truncation all fall out of that line.
   At equal length identity beats the borrow (a plan authored for those periods beats a
   shorter arc with a closer bolted on), so the result cannot depend on glob order.
4. **A synthesis carrier that is not `section_anchor`** — an explicit `"synthesis": true` on
   the period, read by `carriers.is_synthesis`; `is_synthesis_unit` accepts either carrier.
5. **The §3 density rule** in `genon/master_plan.py` (done earlier the same day).
6. **Briefs** — `variant_plans._arc_brief` for both the standard and the compacts: no registry
   is supplied because none exists, the arc is the author's at each count, the plan must be
   whole because it will never be cut, and the travelling synthesis may assume only the
   chapter's content and the dissolution-test terminus.
7. **Certification** — checks 3/4/5 report N/A on a stage with no section axis; check 6 works
   through the boolean carrier; **check 8 redefined**: truncation is a FAILURE inside the band
   and legal below the floor, with a second gate failing any surrender inside the band. Both
   catch an under-dense library — verified by certifying the old `[12, 10, 7]` counts, which
   now fail at X=9 exactly as they should.
8. **`tests/test_genon_plan_granularity.py`** — twelve tests over synthetic fixtures built to
   the stage's real shape.
9. **`docs/testing.md` → v2.7**, recording the S6 exception across C5–C9.

**One defect found and fixed on the way, worth keeping in view.** The engine's unit projection
models the fields SERVING reasons about, which is not the set DISPLAY needs: `progression_stage`
and `stage_label` were dropped, so every served science·middle plan collapsed into a single
"Stage None" group — the phantom CLAUDE.md §3 records for science secondary, reappearing on the
serve side. Fixed generically (`compile._MODELLED` → `unit["extra"]`, spliced back first in
`_period_from_unit`, engine keys winning), which also pre-pays the same debt for mathematics and
english. No test written against the four serve laws would have caught it; only rendering a
served plan through the subject port did.

**Regression evidence.** The three authored libraries (SS·IX ch 3, SS·VIII ch 3, science·IX ch 8)
serve every X in `[floor−1, top+1]` with identical modes, filenames and granularity `unit`.
Full suite 20 passed / 5 failed, the five being the pre-existing environment and fixture gaps
(`fastapi` absent; missing english and science-middle saved-plan fixtures) which fail identically
against the pre-session tree.

## 5. Open, to be answered by the pilot

Do arcs authored at 12 units and at 7 units of the same chapter reach a recognisably similar
terminal operation? §1 leans on the dissolution test sentence as the one shared fact; if
generation does not honour it consistently, the synthesis borrow needs a stronger guarantee
than the brief currently gives it. This is C8's inspection for this stage — and with only one
joint to look at (arc-complete into borrowed synthesis), it is a sharp, cheap test.
