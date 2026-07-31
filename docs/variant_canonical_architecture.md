# The Variant-Canonical Architecture — serving lesson plans by selection, never composition

VERSION 1.0 · 2026-07-31 · Founder + Claude, settled over one working session.
Supersedes the deterministic partition engine (partition.py v0.5, DP/three-regime) and the
Rule 15/16 handoff machinery outright. Read alongside `docs/testing.md` (whose C-steps this
changes — §9 below) and `docs/partition_constitution_rollout.md` (whose A3/A4 amendments
this cancels for the ten remaining constitutions — §8).

---

## 1. Why the partition engine had to go — the evidence, not the vibe

The promise was right: one paid generation per chapter, unlimited free deterministic
adaptations. The premise smuggled in underneath it was wrong: that a lesson plan is a
divisible stream of minutes — that pedagogical structure survives re-tiling. The first live
partition at a realistic compression (SS·IX ch 3, 12×50 canonical served at 9×50, engine
e06) demonstrated the failure on every axis at once:

- **Every sitting was a joint.** At ratio 0.75 each sitting spans 1.33 units, so all nine
  sittings straddled a unit boundary (`handoff_used` = 9/9, `mid_unit_openings` = 6/9). The
  Rule-16 pair notes — designed for the *occasional* joint — became the plan's entire
  teaching voice. Every teacher note read "the sitting pivots from X to Y"; the authored
  unit notes, the actual pedagogy, appeared zero times.
- **The role-aware DP failed on its own terms.** `CUT_COST` priced a cut after a hook at 6
  and after a consolidation at 0 — yet P1, P4 and P7 all ended with the *next unit's hook*
  in their last 7–8 minutes. Hook fires at minute 43, bell rings, development happens days
  later. Not a bug: the fill-tolerance window is a hard constraint and role cost a soft
  one, so when tiling and pedagogy conflict, tiling wins by construction.
- **Uniform percentage cuts are not judgments.** The role-weighted regime scaled every
  development band by exactly 0.8 and every hook/consolidation by 0.714. Whether a
  20-minute discussion survives at 16 depends on what the discussion is *for* — a fact
  available only at authoring time. A deterministic engine that pretends otherwise is
  presenting sophistication that does not exist.
- **Every phase at any cost.** BAND_MIN scraps, `[Continued]` fragments, sittings shaped
  consolidation → hook → half-a-development: an ending, an opening, then part of a middle.

Root cause in one sentence: **the pedagogy's quantum is the unit-arc; the engine's quantum
was the phase — and everything above is a symptom of cutting below the quantum.**

The constraint set that survives (and always held): no LLM in the request path; a
deterministic engine can SELECT authored material but can never MAKE a pedagogical
judgment; therefore every judgment the serve needs must be pre-made at authoring time and
serialized, or it will be faked by arithmetic. Rule 16 already stated this doctrine for
container text — "selected, never composed." The pivot extends the same doctrine to
structure and time. The founder's framing stands as the design's conscience: acknowledge
the constraints, be honest about what is possible, and take pride in being sincere to the
promise rather than presenting a sophistication that does not exist.

---

## 2. The architecture in one paragraph

A chapter is authored as a small **library of variant canonicals**: the same ordered
section list planned at two or three period counts (e.g. 12 / 9 / 7), each a complete,
coherent plan — its own unit-arcs, its own notes, its own assessment — all at the
class-standard duration. Serving a teacher's request is **selection**: pick the
next-highest variant; serve its first X−1 units verbatim, one whole unit per sitting; fill
slot X from the library's closing units by a fixed ladder; scale minutes inside each unit
in proportion to the sitting that carries it; surrender only above the top variant. Every
sitting a teacher ever sees opens with an authored hook, closes with an authored
consolidation, and carries its unit's own authored title and notes. Nothing is composed at
request time; nothing is cut below the unit.

## 3. The serving rules (settled with the founder, 2026-07-31)

**R1 · Next-highest selection (full richness).** The serving variant is the smallest
variant whose period count ≥ the teacher's X. Aruvi's standing approach is full richness:
a teacher between variants is served from above, never rounded down. Surrender exists only
above the top variant: at X > A_top, the top plan is served whole and the balance of her
periods returns to her budget, declared ("2 periods (100 minutes) exceed this chapter's
fullest plan and return to your budget").

**R2 · The X−1+1 form.** Every served plan, without exception, is: the chosen variant's
units 1..X−1 verbatim, plus ONE adaptive slot at position X. Even truncation fits the form
(the slot degenerates to the chosen variant's own unit X with the tail withheld). The
entire adaptation question is therefore a single selector: *what fills slot X, in what
order of preference?*

**R3 · The fill ladder.** Candidates are the CLOSING units of the *other* variants — a
library of V variants has exactly V closure-bearing units, and a fill is a designed
consolidation from a denser plan, never a skip inside the chosen plan. In order:

1. **Exact fill** — a closing unit covering precisely the missing sections. Complete
   coverage, closure intact, nothing to disclose.
2. **Superset fill (minimal overlap)** — a closing unit covering the missing sections plus
   one or two already-taught ones. Complete coverage, closure intact; the note names the
   brief re-crossing as runway. Ranked above any partial option: a brisk revision beats a
   section never taught.
3. **Longest-suffix fill** — no complete candidate; take the closing unit covering the
   longest suffix of the missing span. Closure preserved; the unreached sections are named
   in the coverage note with the material handed over for self-study/homework.
4. **Truncation** — no closure-bearing candidate at all (in practice: a one-variant
   library). Serve unit X, withhold the tail, name it, hand the material over. This is the
   founder's 11-vs-12 ruling: with no denser closing unit available, curtail honestly —
   never jump the chapter's own sequence.

Every rung is deterministic, and every rung below 1 carries its own honest note. The
ladder never manufactures anything: it selects an authored unit or it says what didn't fit.

**R4 · Proportional time inside a unit.** A unit authored at the standard duration D and
served into a sitting of duration d has every band scaled by d/D (BAND_MIN 3, integerised
to exact tiling). This is the only arithmetic left, and it is now defensible: chapter-level
compression is authored (the variant), so proportionality absorbs only *duration*
variation — the same stretch a teacher makes naturally when her period runs 40 instead
of 50, applied to an intact authored arc. The A7 register work (no clock quantities in
band text) is exactly what makes this safe. Mixed matrices keep the weekly-dispersion
ordering (partition v0.4's one keeper): shortest opens the week, long sittings interior,
never adjacent.

**R5 · Per-variant assessments, unit-anchored.** Each variant generates its own
assessment, natively anchored to its own units (the founder's ruling: there is no
cross-variant anchoring problem, because there is no cross-variant anchoring — and no
band-level anchoring problem either, because there are no band-level anchors, §6a).
An item's anchor is its source LO's unit — `period_ref`, already an identity in the
assessment constitutions ("ONE ITEM ← ONE LO → ONE UNIT"). Composition then works for
free: a mixed plan pulls each unit's items from the variant that unit came from — the
prefix's items from the chosen variant, a borrowed closing unit's items from its home
variant, re-anchored to the fill sitting. Items whose anchor unit went unserved carry
the scheduling note, exactly as before.

## 4. Section arithmetic — the join key

The chapter's ordered section list is the library's shared registry (the chapter summary
is its registry of record). Every variant's units are contiguous, section-aligned
partitions of that SAME list, with `section_anchor` strings drawn verbatim from it.
Cross-variant matching is then index arithmetic: a candidate closing unit is exact /
superset / suffix purely by where its range starts relative to the missing span. This is
the one new serialization mandate the whole scheme rests on (V2 in §7); without verbatim
anchors the ladder fails on spelling drift, and with them it is trivial and certifiable.

## 5. Reverse deduction — solving for the variant set

The variant counts are not guessed; they are solved. Since only closing units can fill
slot X, each variant V fully serves a band of requests beneath it, reaching down as far as
the *denser variants' closing spans* allow. Full coverage across the demand range
[floor, A_top] holds iff every gap between consecutive variants is within σ — the largest
closing span the founder will defend pedagogically (a closing sitting that "consolidates
the last five sections" is a summary lecture wearing a unit's clothes; σ is where that
line is drawn).

So the pipeline order inverts the guesswork: author the top canonical (fixing the section
list) → run `aruvi_core/genon/variant_solver.py` (pure arithmetic: enumerate spacings,
simulate the serve table over a demand-weighted range — weights centered on
`master_plan.json`'s `recommended_periods`, where teacher requests will cluster — argmax
full-coverage hits) → emit each compact variant's brief with its period count AND its
**mandated closing span** → author the variants. The fills the ladder depends on then
exist *by construction, not by luck*. The solver also emits the chapter's projected
**adaptation table** (each X → full / partial / truncation), which certification re-derives
from the authored variants and diffs — and which the product can eventually show the
teacher at budget-choosing time: "at 8 periods this chapter closes fully; at 6, one
section moves to homework." The honesty ladder becomes something she shops with.

Large chapters (ch 5 is a 21-unit top canonical) may need a fourth variant rather than a
stretched σ — variant count scales with (A_top − floor) at linear cost (~₹25/chapter each).
That threshold is a founder call, made per subject·stage when the floor is set.

## 6. What the engine now is — and is not

`aruvi_core/genon/serve.py` (v1.1, ~350 lines with its documentation): variant selection,
the X−1+1 fill ladder, section-range arithmetic, proportional scaling, weekly dispersion,
the honest notes, tiling validation. `variant_solver.py` (~120 lines): the reverse
deduction. `compile.py` v0.5: still the strict gate, but the gate is now exactly one
declaration — every assessment item must resolve to a known unit (normalized to
`unit_ref` from `period_ref`, else legacy `phase_ref`).

### 6a · The band layer is internal — nothing declares it (second pass, same day)

Rule 14 fell to the same question that felled Rules 15 and 16: *what still consumes
this?* `band_id` / `band_refs` / `phase_ref` existed so a unit SPLIT across sittings
could be re-addressed band by band — an item had to know which band, hence which
sitting, its anchor content landed in. Whole-unit serving makes the unit indivisible,
so anchoring resolves at unit granularity, and the unit number was already on every
item as `period_ref`. The engine still needs per-band labels internally for scaling
bookkeeping — and derives them positionally in `compile.py` ("P<unit>.<ordinal>"; a
declared band_id is accepted, never demanded), because asking the model to emit labels
code can derive is the failure family the MCQ probe documented (rollout brief A9: the
fix is an affirmative mechanism or no ask at all, never a serialization chore).
Consequences: SS·secondary LP → v1.9 (Rule 14 removed; schema loses band_id/band_refs),
assessment → v1.5 (phase_ref removed, reversing v1.2); **A2 joins A3/A4 as cancelled**
for the ten un-amended constitutions; the rollout brief's X3 item (generalising
`_check_declarations` beyond competency_edges) is void — the check it would have
generalised no longer exists; legacy canonicals (ch 3, ch 5) still compile and serve
through the fallback.

Gone, and recorded here so nobody reinvents them: the DP boundary search, CUT_COST,
SPLIT_COST, fill tolerance, `split_fallback`, the three compression regimes,
DEV_PACE_FLOOR / DEMOTE_BELOW / COVERAGE_FLOOR, role-weighted scaling, seam text,
`unit_handoff` selection with its joiner/vocabulary gates, wide-span reporting,
`mid_unit_openings`. Each was competent engineering aimed at making cutting-below-the-
quantum tolerable; the pivot removes the need rather than improving the tolerance.

What the engine deliberately does NOT do: compose text, reorder units, mix forms inside a
unit, skip interior units of the chosen variant, or serve below the floor without saying
exactly what is missing. When the honest answer is "this chapter cannot be taught
coherently in fewer than K periods," the coverage note says so and the material is handed
over — refusal-with-access is a feature, not a failure.

## 7. The V-series — constitution amendments for the authoring pass

The demolition is done (§8). The authoring side is the next pass, per stage, in the P1–P4
workflow testing.md already defines. Ready-to-port requirement blocks:

- **V1 · The variant brief as input.** INPUTS gains: "Variant brief — this plan's period
  count and, for compact variants, the mandated closing span: the final unit consolidates
  the last k sections." Each variant is authored as a COMPLETE plan under all existing
  rules — never as a compression of the top variant's text.
- **V2 · The shared section registry.** All variants of a chapter draw `section_anchor`
  verbatim from the chapter summary's section list; every unit's coverage is a contiguous
  range of it; multi-section units join anchors with " / " in list order. (Rule 3/4 already
  imply most of this; V2 makes the verbatim-string and contiguity requirements explicit,
  because the fill ladder is string arithmetic on them.)
- **V3 · The closing mandate.** The final unit of a compact variant covers exactly its
  mandated span and closes the chapter — synthesis, resolution — as a real unit-arc, not a
  summary lecture. If the mandated span cannot be closed coherently, the author must say so
  in generation output rather than comply badly (that verdict feeds σ back to the solver).
- **V4 · Per-variant assessment.** Each variant's assessment run consumes ITS OWN coverage
  handoff; item counts scale with the variant's unit count per the existing assessment
  constitution rules. No cross-variant references of any kind.
- **A2, A3 and A4 are ALL CANCELLED** for the ten un-amended constitutions (§6a: roles,
  unit_handoff and the whole band declaration layer are no longer read by anything —
  and X3, the gate generalisation, is void with them). A1 (single standard row) and
  A5/A7 (the register — port the v1.10 re-cut: clock quantity, forward reference /
  completion language, calendar time; backward references freed, content-named
  continuity as best practice) stand. **A6 reduces
  to a confirmation**, not an amendment: each subject's items must carry their anchor
  unit (`period_ref` or that subject's equivalent) — verify per stage during P-prep,
  amend only where absent. Group B's P3 schema conversion (phases[] → time_bands)
  stands unchanged.

## 8. What changed on disk today (2026-07-31)

- `aruvi_core/genon/serve.py`, `variant_solver.py` — NEW (engine + solver).
- `aruvi_core/genon/partition.py`, `polish.py` — RETIRED to `_to_delete/` (the genon/ lab
  at repo root keeps its own historical copy untouched).
- `compile.py` → v0.5 (roles optional passthrough; unit_handoff no longer read; band ids
  derived positionally, never demanded; items normalized to `unit_ref`);
  `__init__.py` re-exports `serve_plan`/`ServeError`.
- `api/data.py` — `GENON_ENGINE_VERSION` "08" (every e07 entry stale by construction);
  `load_genon_library` / `load_genon_streams` (variant files:
  `ch_NN_canonical_pKK.json` beside `ch_NN_canonical.json`).
- `api/main.py` — the genon route serves the library: identity generalised to any
  variant's standard row; cache keyed by the CHOSEN variant's version; response carries a
  `serve` block (variant_used, slot_fill, surrender) while keeping `compression`/
  `seam_periods` keys shaped for the current frontend (seams are now always []).
- SS·secondary LP constitution → **v1.8** (Rules 15/16 removed, register rebound to Rules
  10 and 13 with the whole-unit rationale) → **v1.9** (Rule 14 removed, §6a).
  Assessment constitution → **v1.5** (phase_ref removed, reversing v1.2). Both
  CHANGELOGs carry the dated rows.
- Tests: `test_genon_serve.py`, `test_variant_solver.py` NEW (synthetic three-variant
  library: selection, all four ladder rungs, surrender, scaling/tiling, assessment remap +
  namespacing, dispersion; solver covering condition, σ degradation, demand weighting);
  `test_genon_unit_handoff.py` retired; `test_genon_duration_order.py` repointed to
  serve; `test_genon_plan_key.py` asserts e08. Genon suite green. (Pre-existing failures
  in test_api/test_link_resolver/test_lp_standard/test_normalized_item/test_stimulus/
  test_calibrated_defaults trace to sample english/science saved plans and master-plan
  data absent from `data/content` — present on the founder's machine before this session
  and unrelated to the pivot; verify against the standing 11/11 note in CLAUDE.md §8.)

## 9. Impact on the test campaign (docs/testing.md)

The 25-combo template survives; its middle changes. Per-stage prep loses A3/A4 (P1
shrinks) and gains V1–V4; C1 becomes "generate the chain per variant" (the solver runs
between the top canonical and the compact briefs); C5's five-regime matrix becomes a
serve-table sweep (identity per variant · one exact-fill X · one superset X · one suffix X
· one above-top surrender · the mixed-duration C6 mix); C7's six checks reduce to four
(tiling; unit order + whole-unit integrity; register scan; note correctness per ladder
rung — seam and wide-span checks are void); C9 gains the borrowed-unit item case; C10's
filenames assert `e08` and the chosen-variant version key. C2 now prices the whole
library per chapter — the number that decides the corpus pre-warm, estimated at
₹20,000–35,000 for 330 chapters × 3 variants at batch pricing from the July token log
(₹60/canonical live mean, ~2.3× effective multiplier for smaller compact variants, SS·IX
sample being the heaviest corner), assessments extra but a fraction of LP size. The
pilot (SS·IX ch 5) should author its variants through the solver and read a few borrowed
seams aloud before the template is declared portable.

## 10. Open items

1. **Floor (lower band) per subject·stage** — the smallest period count a chapter serves
   coherently; C = floor is the solver's anchor. Founder sets it (master-plan calibration
   is the natural source).
2. **σ per subject·stage** — the largest defensible closing span. Founder sets it; V3
   feeds violations back.
3. **Variant-count threshold for large chapters** (§5) — when (A_top − floor) exceeds what
   three variants cover at σ, add a fourth vs accept declared partial bands.
4. **The adaptation table as a product surface** — show the teacher what each period count
   buys at budget-choosing time (First-Run chapter step / Year Plan). Deferred UI; the
   solver already emits the data.
5. **Frontend serve-block adoption** — the response's `serve` object (variant_used,
   slot_fill, surrender_note) deserves UI; `compression`/`seam_periods` are kept only for
   compatibility and can retire with the next web pass.
6. **testing.md revision** — apply §9 to the template file itself (its §9 regression rule
   makes that a dated template change).
