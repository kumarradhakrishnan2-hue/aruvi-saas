# English · Secondary — assessment item density

Analysis note, 2026-08-12. Why English secondary is the lowest item:unit ratio of any
subject·stage group, what the sister constitutions do instead, and three ways to raise it.

---

## 1. The measurement

Realized ratios from `data/content/saved_plans/` (items ÷ units, canonical + variant plans):

| Subject · stage | items / unit | governing rule |
|---|---|---|
| Maths · preparatory | 2.1 – 3.9 | one item per handoff **task** |
| SS · middle / secondary | 1.25 – 2.6 | **exact counts per competency weight** (5 / 3 / 2) |
| Science · middle | 1.5 – 1.75 | **floors per progression stage** (≥3, ≥4 on the final) |
| Science · secondary | 1.0 | ≈ one item per **section**, a second only when rich |
| TWAU · preparatory | 1.0 | exactly one item per **period** (hard cap) |
| Maths · middle / secondary | 0.93 – 1.08 | one item per **goal** / per **implied_lo** |
| **English · secondary** | **0.35 – 0.60** | one item per **(section × spine) cell** |

English IX ch 7 *Vitamin-M*, the certified canonical: **17 units, 6 items.**

## 2. The root cause — a capacity-bounded axis, not a content-bounded one

Every other subject's assessment axis **scales with the chapter's substance**: sections,
competencies, LOs, goals, periods. English's axis is the **spine**, and there are exactly
six of them, fixed by NCF and never re-sequenced (LP Rule 1).

Since the 2026-07-01 chapter split, an English chapter is **one main_section**. So the
(section × spine) grid collapses from 3 × 6 to **1 × 6**, and

    item ceiling = number of spines present ≤ 6

…regardless of whether the chapter is taught in 10 units or 21. Assessment constitution
Rule 2 states this explicitly and treats it as a feature:

> "That count does NOT vary with the number of periods the chapter was taught in… never a
> shorter assessment."

The corollary was never stated: it is also never a **longer** one. English is the only
subject whose item count is flat in plan length.

## 3. The distribution problem is worse than the ratio

Running the real resolver (`aruvi_core/genon/carriers.assessment_items`) over the three
certified ch 7 plans:

| plan | units | items | units carrying an ASSESS tab |
|---|---|---|---|
| `ch_07_canonical` | 17 | 6 | 6 → units 8, 11, 12, 14, 15, 16 |
| `ch_07_canonical_p14` | 14 | 6 | 6 |
| `ch_07_canonical_p10` | 10 | 6 | 5 (two items collide on unit 8) |

**Eleven of seventeen units have no Assess tab at all** — including units 1–7, the entire
reading arc. Reading for Comprehension is taught across 8 units, carries 8 anchored tasks
in the handoff, and yields **one** item, anchored at the close (unit 8; unit 17 is the
synthesis unit and is deliberately excluded from the index).

The substance is demonstrably there. `coverage_handoff.reading_for_comprehension` for
ch 7 lists eight `tasks_anchored` entries — three "Check Your Understanding" sets and
three "Critical Reflection" extracts. The textbook itself pairs a comprehension check
with a critical-reflection extract; the constitution collapses both into one item.

The `implied_lo` is likewise compound:

> "Student analyses character motivation, theme, and authorial purpose using prose as the
> vehicle."

Three separable outcomes, one item.

## 4. What the sister constitutions do that English does not

- **SS (both stages), Rule 4 — weight-driven exact counts.** Competency weight is "the
  sole architectural governor": Central = 5 items with prescribed types, Substantive = 3,
  Present = 2. Density follows *importance*, and type is prescribed by weight, not chosen.
- **Science middle, Rule on stage floors.** Item count is set by stage **position** —
  first ≥2 MCQ, every middle stage ≥2 MCQ + ≥1 SCR, final ≥2 MCQ + 1 ECR + 1 Open Task.
  Uncapped above the floor.
- **Science secondary, per-section count.** "A rich section MAY carry more than one item
  and MAY mix types (MCQ on a fact + SCR on the procedure); a thin section gets one." A
  budget with an explicit anti-inflation guard.
- **Maths secondary, Rule 5.** "A two-LO section yields two items, typically at two
  different cognitive demands." Density rides on LO count, which rides on content.

Common shape: **more than one item per anchor is normal, and the second item is
distinguished by demand rung or question type, never by being "another one of the same".**

## 5. The code is already ready for 2 per cell

`aruvi_core/subjects/english/subject.py :: cell_resolver` — the N-to-N positional pairing
(2026-07-11, MEMORY.md): *"when a cell has N items AND exactly N units (N ≥ 2), they pair
POSITIONALLY."* Shared by the display path and the genon carrier. There is already a
synthetic guard for it:

    tests/test_genon_carriers.py :: test_the_N_to_N_pairing_survives_into_the_carrier
    """…no english chapter in the corpus authors two items for one cell — Rule 10 emits
    one item per cell — but the shape is legal and the resolver supports it."""

Nothing in the genon serve engine constrains item counts: assessments are per-canonical,
a borrowed unit brings its own items, and certification (`build_library.py`) gates the
synthesis anchor, not counts. TWAU/science/SS all vary item counts per canonical already.

---

## 6. Three approaches

### A — Two items per cell, differentiated (smallest change; what was asked for)

Amend assessment constitution Rule 2: **two items per `section_contribution`**, and they
MUST differ on both axes:

- **Demand:** one at the comprehension/application rung, one at analysis/evaluation. The
  secondary delta already mandates a lean to the higher rung — make the pair carry it.
- **Type:** the two items MUST NOT share a `question_type`. For Reading, prescribe the
  pair explicitly, mirroring the textbook's own structure:
  `1 × EXTRACT_ANALYSIS or ECR` + `1 × MCQ / TRUE_FALSE / SCR`.

Per-spine slot table, in the SS Rule 4 style:

| Spine | Item 1 (lower rung) | Item 2 (higher rung) |
|---|---|---|
| Reading for Comprehension | MCQ / TRUE_FALSE / SCR | EXTRACT_ANALYSIS or ECR |
| Listening | MCQ / TRUE_FALSE | SCR or FILL_IN |
| Speaking | ORAL_PROMPT (describe/recount) | ORAL_PROMPT (argue with rationale) |
| Writing | WRITING_TASK (functional form) | WRITING_TASK (discursive/critical form) |
| Vocabulary & Grammar | MATCH or FILL_IN | SCR (transformation / usage in context) |
| Beyond the Text | ECR | PROJECT |

Result on ch 7: **6 → 12 items, 0.35 → 0.71.** Above maths·secondary, still below SS.

**Caveat — spread does not improve on its own.** With 2 items and a 9-unit RFC cell, N-to-N
does not fire (2 ≠ 9), both items take the full span, and both anchor at the close. Units
with an Assess tab stay at 6/17; one of them now carries two items. See A′.

### A′ — A, plus even dispersion in the resolver (fixes spread too)

Extend `cell_resolver`: when a cell has N items and M > N units, deal the items across the
span by **even dispersion** (the same idea `genon/master_plan.py canonical_periods` already
uses) instead of handing every item the union. Ch 7 would go from 6/17 units assessed to
roughly 12/17.

This requires a matching statement in the constitution, because it contradicts Rule 8A's
current promise:

> "an item tests the cell's whole `implied_lo`, so it becomes available only when the cell
> completes."

Rule 8A would need to say that item 1 is scoped to the cell's **first** teaching span and
item 2 to its completion — which is true of the A slot table above (the lower-rung item
genuinely is answerable earlier), but it must be declared, not assumed. Note also the
standing caveat from 2026-07-11: positional pairing assumes items are authored in teaching
order. The A slot table makes that ordering explicit rather than incidental, which
strengthens it.

### B — Weight the spines (the SS model)

Keep one item per contribution but let **spine weight** set the count: derive Central /
Substantive / Present from the effort-index mapping (or from units-spanned), then
Central = 3 items, Substantive = 2, Present = 1. Ch 7 → RFC 3, V&G 2, Speaking 2,
Listening 1, Writing 1, Beyond 1 = **10 items (0.59)**.

More faithful to chapter shape than a flat 2 — a one-unit Listening cell does not need
two items, and a nine-unit Reading cell arguably needs three. But it is a larger
amendment, needs a weight source the assessment generator is allowed to read, and it
lands *below* option A on the headline ratio.

### C — Raise the number of cells, not items per cell (the structural fix)

The bottleneck is upstream. LP constitution Rule 10 emits **one contribution per
(section × spine)**, so a spine taught over eight units still produces one broad
`implied_lo`. Amend it to emit one contribution per **(section × spine × topic cluster)** —
one per distinct sub-skill the spine actually taught — and the assessment constitution
needs *no* change: "one item per contribution" then yields roughly one item per unit, and
the existing N-to-N pairing distributes them positionally **with zero code change**.

This is what every other subject already does — their handoff unit is content-sized
(LO, goal, competency, task), never capacity-bounded.

Costs: it is an LP constitution amendment (english/secondary v1.2 → v1.3, and middle +
preparatory for consistency), it touches metered STEP 1 generation, and it invalidates the
certified English canonicals — they would need regeneration. It also drops Rule 2's
"count does not vary with period count" promise, though that promise is self-imposed and
no other subject holds it.

---

## 7. Recommendation — ✅ SHIPPED 2026-08-12 (A′, all three stages)

> **Decided and implemented.** Founder chose: relax Rule 8A to two-stage scoping · prescriptive
> SS-style slot table · **all three English stages** (not secondary only). Landed as assessment
> constitution `english/secondary` **v1.5 → v1.6**, `english/middle` **v3.5 → v3.6**,
> `english/preparatory` **v1.3 → v1.4** (Rule 8A is NEW at middle and preparatory), plus
> `_disperse()` in `aruvi_core/subjects/english/subject.py` and three tests in
> `tests/test_genon_carriers.py`. Measured on the three real ch 7 plans: ratio
> 0.35 → **0.71** / 0.43 → **0.86** / 0.60 → **1.20**; assessed units 6 → **9** of 17.
> STATIC + unit-verified only — the certified ch 7 canonicals are pre-amendment 6-item files
> and must be regenerated. Section 6's options are kept below as the reasoning of record;
> **option C remains open** and is the only route to genuine 1:1 coverage.

**Ship A′ now, keep C as the eventual destination.**

A′ delivers exactly the doubling asked for, fixes the distribution defect (which is the
worse of the two problems), reuses a resolver behaviour that already exists and is tested,
and is a single-constitution amendment that leaves the LP and the certified canonicals
untouched. C is architecturally correct but pays a regeneration bill and an LP amendment
for a benefit A′ mostly captures.

Two things to decide before drafting:

1. Whether Rule 8A's "available only when the cell completes" may be relaxed to a
   two-stage scoping (needed for the spread fix; A without it doubles the ratio but not
   the coverage).
2. Whether the per-spine slot table above is prescriptive (SS style — types fixed by slot)
   or advisory (science-secondary style — a budget with an anti-inflation guard). The SS
   style is more deterministic and easier to certify; the science style leaves the
   generator room on thin spines.

## 8. Open observation, not part of this proposal

The chapter's closing **synthesis unit carries no assessment at any subject or stage** —
`carriers.is_synthesis` excludes it from the item index by design (indexing it would make
it the last unit of every cell and collapse the whole chapter onto it). In English IX ch 7
that is unit 17 of 17. Worth a separate decision: the unit where the teacher pulls the
whole chapter together is the one unit with nothing to assess.
