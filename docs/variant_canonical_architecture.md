# The Variant-Canonical Architecture — serving lesson plans by selection, never composition

VERSION 2.0 · 2026-08-03 (v1.0 · 2026-07-31) · Founder + Claude.
Supersedes the deterministic partition engine (partition.py v0.5, DP/three-regime) and the
Rule 15/16 handoff machinery outright. Read alongside `docs/testing.md` (whose C-steps this
changes — §9 below) and `docs/partition_constitution_rollout.md` (whose A3/A4 amendments
this cancels for the ten remaining constitutions — §8).

> ★★ **READ §0 FIRST (v2.0, 2026-08-03).** The solver-mandated closing spans and σ are
> RETIRED. §0 supersedes §3-R3 (the fill ladder), §5 (reverse deduction), §7-V3 (the closing
> mandate) and every reference to `closing_spans`/`sigma`. §§1–2, R1, R2, R4, R5, §4
> (section arithmetic incl. frontier), §6a and V2/V4 stand unchanged and are read through §0.

---

## 0 · VERSION 2.0 — free canonicals, the synthesis anchor, and the Xth-unit choice set

### 0.1 The defect that forced it (ARV-D-025, the "jumpy Xth unit")

v1.0 mandated each compact variant to close with a synthesizing unit spanning its
solver-assigned last-k sections, so the fill ladder's candidates would exist by
construction. The mandate smuggled in a false premise: **by writing the compact's closing
unit to consolidate, we imported the assumption that the BORROWING plan's class has the
same prior exposure to those sections that the LENDING plan built in its own units 1..X−1.**
It does not — the borrowing class reached slot X through a different prefix. The served
plans' X−1→X profile read exactly that way: a closing sitting pitched as consolidation of
lessons the class never had in that shape. Mandated synthesis is jumpiness by construction.

The structural fix inverts the requirement. A borrowed unit is safe in a foreign prefix
exactly when it is a **FIRST-EXPOSURE unit for the sections it advances**: such a unit's
only backward dependency is "the sections before mine have been taught" — which the
deterministic prefix guarantees, because sections are sequential and the frontier stands at
M−1 when slot X opens on section M. (This is e11's "anchoring is not teaching" insight
promoted from a repair to the selection principle itself.) Nothing about the fix needs a
mandate on the lender — it needs the RIGHT PICK from freely authored plans. So the mandates
go, except one (§0.3).

Localization stands deliberately: only slot X is adaptive. Reaching further back would
multiply the contextualization burden (unit X must now cohere with more foreign units)
faster than it adds value; the multiple-canonical library is precisely what makes the
single-slot deliberation sufficient.

### 0.2 The canonical set — equal dispersion, no solver

Per chapter, with A = `recommended_periods` (the standard) and C =
`floor_periods_at_standard` (0.6 × A, rounded — unchanged):

- **A − C ≥ 4:** three canonicals at **{A, mid, C}**, mid = ⌈(A+C)/2⌉ — equal (or
  near-equal) dispersion across the band, endpoints included. The floor canonical anchors
  the bottom of the serve band.
- **1 < A − C < 4:** two canonicals, **{A, C}** (the midpoint would sit adjacent to an
  endpoint and buy nothing).
- **A − C ≤ 1:** the standard alone, **{A}**.

Counts are pure arithmetic in `genon/master_plan.py` (`canonical_periods` on every chapter
row). `variant_solver.py` is RETIRED; `sigma` and `closing_spans` no longer exist anywhere.
Demand weighting is unnecessary: the spacing rule is uniform because the choice set (§0.4)
no longer depends on where requests cluster.

### 0.3 The one surviving mandate — the synthesis anchor (standard canonical only)

Compact canonicals are authored **FREE**: complete plans under all existing rules (V2
registry discipline, total coverage, first-visit order, self-containment) with NO closing
mandate — the author shapes the ending as the count demands, which near the floor will
naturally condense adjacent sections (the same pressure the solver used to formalize).

The STANDARD canonical alone carries one mandate: **its final unit is a whole-chapter
synthesis whose `section_anchor` is exactly the reserved token `synthesis`** — not a
registry section. Rules of the token: it may appear only in the standard canonical, only on
its last unit; all registry sections must first-appear across units 1..A−1; the synthesis
unit may assume every SECTION's content has been taught but never that any particular
activity, reading or homework happened (it is lent into plans whose classes covered the
same sections through different units). The registry is computed ignoring the token;
first-visit and coverage checks skip the synthesis unit.

Why it is safe where the old mandate was not: the synthesis unit is only ever borrowed in
**Case 1** (§0.4), where the borrowing prefix has covered the ENTIRE registry — full
coverage is the only prior a full-chapter synthesis needs, and Case 1 guarantees it.

### 0.4 The Xth-unit choice set (replaces the v1.0 fill ladder)

The X−1+1 form (R2) stands. With the chosen (next-highest) canonical's units 1..X−1 served
verbatim and the frontier at M−1 (M = first uncovered registry section):

**Case 1 — frontier at the last section (all sections covered by X−1).** Slot X borrows
the standard canonical's `synthesis` unit. One choice, no deliberation.

**Case 2 — sections remain.** For every canonical in the library (the chosen one
included — its own unit X is the identity candidate), find the unit that deals section M
**for the first time in its own plan** (first-visit). Contiguity (V2) makes every co-dealt
section adjacent to M, so every such unit qualifies. Preference order, per the founder's
rule (2026-08-03):

1. **Forward, no re-cross** — first-deals M with further reach (M+N, M+N+O …): among
   these, the furthest forward reach wins (fewest dropped sections; condensation matters
   most toward the floor, and the floor-side canonicals are where these units live).
2. **M alone** — first-deals exactly M.
3. **Backward combinations** — first-deals M jointly with already-taught sections (L+M,
   K+L+M …): mild redundancy on the re-crossed sections, which is contextually safe
   (redundancy is not jumpiness); least backward overlap first, then furthest reach.

Ties inside a class: the lender whose period count is closest to X (pacing context), then
the denser plan. Every candidate is first-exposure for M by construction, so the borrowed
unit's priors are satisfied whatever prefix precedes it — the v1.0 exact/superset/suffix
distinction and its closure requirement (r[1] == last) are gone.

**Dropped sections.** If the fill still leaves registry sections uncovered, the plan
carries them as dropped units **sourced from the LENDING plan** — its units after the
serving unit (their coverage lies wholly beyond the fill's reach, by contiguity), verbatim,
flagged unscheduled. Provenance is consistent: the tail continues the plan the closing
unit came from. (v1.0 sourced drops from the chosen plan; that changes.)

**Case 3 — empty choice set.** With total-coverage canonicals and the generalized adjacency
rule this should be structurally impossible (the chosen plan's own unit X always
qualifies); the rung is kept as a defensive guard. On truncation: serve the chosen plan's
own unit X, show NO dropped sections, and put up the message asking for **at least the
reference canonical's count** — the next higher canonical, not the floor. The gap being
diagnosed is between the request and its reference canonical (the teacher seems to want
that plan's depth); when X < C the reference IS the floor canonical, so the old message
survives as the special case.

### 0.5 What this retires / changes on disk (2026-08-03)

- `aruvi_core/genon/variant_solver.py` → RETIRED to `_to_delete/` (with
  `tests/test_variant_solver.py`). No projected adaptation table; certification's serve
  sweep is the table of record.
- `master_plan.json`: chapter rows carry `canonical_periods` (from `master_plan.py`) and
  `canonical_plan` {counts, provisional, basis, registry_sections, authored} (from
  `variant_plans.py`); `variant_plan`/`closing_spans`/`sigma` are gone.
- `variant_plans.py`: briefs recomposed — the standard brief gains the synthesis-anchor
  mandate; compact briefs lose the closing mandate (free authoring, coverage total).
- `serve.py` → engine **e12**: `fill_slot` implements §0.4; `section_registry`/validation
  learn the `synthesis` token; drops re-sourced to the lender.
- `build_library.py`: closing-span check → synthesis-anchor gate (top only, last unit
  only, token forbidden elsewhere); projected-vs-actual diff dropped.
- V3 is struck from §7's V-series; V1's brief content changes as above; V2/V4 stand.

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

**R3 · The fill ladder.** Candidates are the LENDABLE units of the *other* variants — a
library of V variants offers at most V closure-bearing units, and a fill is a designed
consolidation from a denser plan, never a skip inside the chosen plan.

> **The lendable unit (engine e11, 2026-08-02 — amends "the closing unit").** A variant's
> lendable unit is its last one UNLESS that unit anchors only sections an earlier unit of the
> SAME plan already taught. Such a trailing SYNTHESIS is written to be met at the end of its own
> arc — "having traced the full arc…", "rank the factors from the case study" — so lending it
> into a foreign prefix hands the teacher a sitting that assumes lessons her class never had.
> The ladder walks back to the unit that first introduced those sections ("all", not "any": a
> unit anchoring one repeat plus one new section still teaches, and the walk may take more than
> one step). **Anchoring is not teaching** — the section checks pass on a label while the prose
> treats the section as revision, which is why nothing caught this until a human read the plans
> (ARV-D-023, SS·IX ch 3 C7). Two consequences: the TOP canonical becomes lendable for the first
> time (its own last unit is a synthesis that never reached the final section), and the closing
> mandate — in the brief and in certification check 6 — attaches to the lendable unit, with a
> trailing synthesis forbidden in newly-authored variants. The **exception is synthesis mode**,
> where the prefix already covers the whole registry: there the trailing synthesis assumes
> nothing false and is exactly the right borrow.

In order:

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
is its registry of record). Every variant's units are section-aligned against that SAME
list, with `section_anchor` strings drawn verbatim from it. Cross-variant matching is
then index arithmetic: a candidate closing unit is exact / superset / suffix purely by
where its range starts relative to the missing span. This is the one new serialization
mandate the whole scheme rests on (V2 in §7); without verbatim anchors the ladder fails
on spelling drift, and with them it is trivial and certifiable.

**Frontier arithmetic (founder ruling, 2026-07-31).** Coverage is measured by the
prefix's FIRST-VISIT FRONTIER — the furthest registry section any served unit reaches —
not by per-unit anchor order. The ch 5 canonical's tail proved why: its last three units
are backward-anchored synthesis sittings ("Early Indian Economy: Synthesis", "Unity in
Diversity", "Chapter Synthesis" anchored to the opening section) — legitimate authoring
that revisits sections without advancing the frontier. Under frontier arithmetic the
uncovered span is always a registry suffix even with such tails; when the frontier
already stands at the final section, the withheld tail is synthesis-only — coverage is
complete, and slot X borrows a companion variant's closing synthesis (nearest in scale)
or, in a one-variant library, hands the synthesis material over with a note that says
exactly that. So V2 mandates first-visit ORDER (new sections appear in registry order),
not per-unit monotonicity — synthesis tails remain legal and welcome.

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

## 7. The V-series — carried by the VARIANT BRIEF, never by constitutions

**Founder ruling (2026-08-01): the V-series is NOT constitutional.** The brief is
post-constitution — composed by the platform (`genon/variant_plans.py briefs_for`),
prepended to the generation prompt, invisible to the constitution — and the
deterministic certifier (`genon/build_library.py`) enforces every V-requirement
regardless of wording. Constitutions receive nothing for it: no V-rules, no INPUTS
acknowledgment, no precedence line. Two reasons, both proven in the ch 3 pilot:
the brief's content is per-chapter and parameterized (a constitution cannot carry a
registry), and brief wording must iterate at the speed generation failures teach —
the coverage clause was hardened the same day a variant leaked, at one ₹35 rerun,
where a constitutional amendment would have reopened every certified combo under
testing.md §9. The constitutional carry-forward for the rollout is exactly the list
in partition_constitution_rollout.md §3 (A1 · A5/A7 v1.10 register · A6-confirm ·
A9 · P3 · P4) and nothing more.

The V-requirements themselves, as the brief and certifier carry them:

- **V1 · The variant brief.** The brief carries this plan's period count and, for
  compact variants, the mandated closing span (the final unit consolidates the last k
  sections). Each variant is authored as a COMPLETE plan under all existing rules —
  never as a compression of the top variant's text.
- **V2 · The shared section registry.** All variants of a chapter draw `section_anchor`
  verbatim from the chapter summary's section list; every unit's coverage is a contiguous
  range of it; multi-section units join anchors with " / " in list order. (Rule 3/4 already
  imply most of this; V2 makes the verbatim-string and contiguity requirements explicit,
  because the fill ladder is string arithmetic on them.)
- **V3 · The closing mandate.** The final unit of a compact variant is a CLOSING
  SYNTHESIS anchored to exactly its mandated span — the last k registry sections — and
  closes the chapter as a real unit-arc, not a summary lecture. (The anchor must list
  those k sections so the fill ladder can see it; the synthesis may of course draw on
  the whole chapter, as ch 5's authored closers do.) If the mandated span cannot be
  closed coherently, the author must say so in generation output rather than comply
  badly (that verdict feeds σ back to the solver).
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
