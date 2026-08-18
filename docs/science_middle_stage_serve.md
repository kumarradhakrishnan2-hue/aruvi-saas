# Stage-granularity serving — science · middle

**Addendum to `docs/variant_canonical_architecture.md` (read §0 there first).**
Version 1.3 · 2026-08-17 · §6 added from the F1 full-enumeration findings, then CORRECTED
the same day (v1.2's separate CODA asset → v1.3's in-place synthesis re-author; §6.2 records
why). §§1–5 are v1.1 (2026-08-07, implemented e17) and stand unchanged — including the serve
law, which v1.3 deliberately does not touch.

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

> ★ **The law is unchanged by §6 (v1.3, 2026-08-17) — what changed is what the borrowed
> unit IS AUTHORED AGAINST:** after wave 2, the top's synthesis unit is re-authored reading
> across the chapter's compacts (§6), so the unit this row borrows sits properly on every
> compact it can land after. Same four rows, same selection, nothing stage-specific added.

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

> **Answered 2026-08-17, by the batch F1 rather than the pilot — and the answer motivates §6.**
> The arcs DO reach the shared terminus (zero seams failed on arc grounds). What §5 did not
> ask is what the borrowed synthesis *adds* to a plan that is already whole — and that is
> where the design leaked.

---

## 6. Re-authoring the top's synthesis against the whole library (v1.3, 2026-08-17)

### 6.1 The finding that forces this

S6's batch F1 read **every K+1 serve in the corpus — 114 of 114** (37 chapters, each compact
ending against the appended top synthesis). Verdict: **10 CLEAN · 57 SERVICEABLE-MATERIAL ·
44 SERVICEABLE-MILD · 3 JUMPY.** Roughly 100 of 114 serves carry an issue, and the issues are
two families with one root:

- **Double capstone (the 101 serviceables).** Every compact is a complete plan, so its final
  unit closes its own arc — correctly, identity serves need it. The appended synthesis then
  closes the chapter AGAIN. MATERIAL (50% of all serves) is when the two closings share a
  *specific* device: the Gandhian quote read aloud on consecutive days (vi ch 11, all three
  serves), the shell question "answered definitively" twice (vi ch 10), the bukhari stove
  re-posed (vii ch 7), "Happy investigating!" twice (viii ch 1). The collision is structural:
  the top's synthesis and every compact's closer were authored by the same unconstrained
  brief against the same chapter, so they independently reach for the chapter's signature
  device.
- **The intersection violation (the 3 JUMPY).** vii ch 8 at X=9 AND X=11: neither p08 nor p10
  ever teaches distance-time graphs, and the synthesis demands "complete the graph by
  plotting the missing points". viii ch 13 at X=7: p06 omits the Section 13.6 response
  framework the synthesis asks students to map. A compact may freely drop a strand; the top's
  synthesis was authored assuming the top's arc taught it. **Certification is structurally
  blind to this family** — no section registry exists here, and the synthesis-anchor gate
  checks a token, not conceptual coverage.

Both families are one design error, named by the founder: *the K+1 serve invokes a fully
formed plan, so nothing more was pedagogically needed; if a unit is appended for completion
alone, it must be designed to sit lightly on a plan that has already closed — and the top's
synthesis was never designed for that.* The 2026-08-07 reasoning ("the terminus is the one
shared fact, so the top's synthesis is the one safe borrow") answered the JUMPY risk it could
see and missed the redundancy risk, because in every OTHER stage the synthesis is only ever
served when X−1 sittings have covered all sections and no closing unit exists yet. Here it
lands on top of one.

### 6.2 The ruling — and the same-day correction

v1.2's first answer was a separate per-chapter **CODA asset** with its own serve mode,
storage convention, fallback and staleness gate. **The founder struck it within the hour,
for a structural reason worth keeping:** it would have given one stage of eleven its own
serve algorithm and a second authored artefact to maintain forever — breaking the
one-flow-across-eleven property that the whole carrier design exists to protect, to fix
what is ultimately one unit's authoring problem.

**v1.3: the top's synthesis unit itself is RE-AUTHORED, in place, after wave 2 — reading
across the chapter's compacts.** The serve law (§2) stays byte-identical; no new asset, no
new mode, no fallback, no staleness machinery. The trade accepted with eyes open: the
re-authored unit is also the top's own finale, so any residual lightness it has in that
seat is confined to ONE serve — the top's identity — instead of the 114 K+1 serves
carrying today's defects. The unit closes the chapter *through a fresh application* (the
pattern every CLEAN seam in §6.1 shared) rather than through a ceremonial recap, which is
arguably a better closer for the top's own class too.

### 6.3 The re-authored unit's contract

Still the top's genuine closing synthesis — it keeps `synthesis: true`, its period number,
its stage — authored to be excellent in BOTH its seats (the top's finale; the K+1 extra
period after any compact):

1. **It closes through one fresh, concrete application** — a scenario, artefact, dataset or
   design problem the chapter itself never uses. What the task shows IS the synthesis.
2. **Its demands are bounded by the INTERSECTION of the compacts' coverage** — it may
   require only what EVERY compact teaches. Kills the JUMPY family by construction: vii
   ch 8's unit cannot demand graphs while p08 and p10 lack them. (The top teaches a
   superset of any honest intersection, so the bound costs its own finale nothing real.)
3. **Its vehicle differs from every compact's final unit**, and it uses none of the
   specific stories, quotes, objects, questions or catchphrases those endings use — the
   endings are supplied in the brief so this is checkable, not aspirational.
4. **Earned closure, not ceremony**: its last band consolidates what the task itself
   showed, naming the chapter's central ideas as the reason the task worked. No re-read
   quote, no re-answered bookend, no second finale rhetoric.
5. **Items and register unchanged**: stage-anchored items stay where they are (the borrow
   still carries none — ARV-D-067 stands verbatim); two-ban register as ever.

### 6.4 Brief construction (`genon/resynth.py`)

Per chapter the brief supplies: the chapter summary; the TOP's unit-title map minus its
final unit (the arc the new unit must close); every compact's unit-title map (the
intersection bound's evidence); and every compact's **final unit in full** (the spent
devices). Constraints are stated as properties of the output, never as prohibitions to
acknowledge — the meta-leak lesson (`repair_meta_leak.py`, 2026-08-13).

The model authors CONTENT fields only (title, description, approach, notes, materials,
bands, homework); install preserves the unit's IDENTITY fields from the old unit
(period_number, duration, progression_stage, stage_label, synthesis, roles), archives the
old unit whole under `genon_canonical.synthesis_reauthor.replaced` with the compact
fingerprints read, and purges derived plans (ARV-D-034). Provenance only — **no staleness
gate**; that was v1.2 machinery and the founder's correction removes the maintenance
surface deliberately.

### 6.5 Wave, cost, certification, reading gate

- **Wave 3, `batch_api.py --wave resynth`** — one request per chapter after the library is
  complete, ~37 runs, small outputs: estimated **₹100–200 for the stage**.
- **Certification is UNCHANGED** — the synthesis-anchor gate, register scan and serve
  sweep all apply to the replaced unit exactly as to its predecessor. The intersection and
  vehicle-novelty bounds remain READING gates: the F1-resynth read — each new synthesis
  against every compact ending of its chapter, CLEAN / SERVICEABLE / JUMPY, enumerated —
  is the human gate on the wave, plus a read of the unit as the TOP's own closer.
- The 154 canonicals otherwise stand; the 3 JUMPY serves and 57 MATERIAL collisions die
  with the replacement.

### 6.6 Standing question for the other ten stages

None of this transfers automatically: elsewhere the synthesis serves only when no closing
unit exists yet (all sections covered by X−1, the slot empty), so the double capstone cannot
arise there — F1 on four prior stages confirms it has not. But the *lesson* transfers: any
serve mode that APPENDS authored content to an already-complete plan must ask what the
appended unit adds, and "it was safe to borrow" is not the same answer as "it belongs".
