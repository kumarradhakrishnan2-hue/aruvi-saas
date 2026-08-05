# S3 · science · secondary — stage preparation sign-off

**Date** 2026-08-05 · **Class IX** (the recorded draw, seed `science|secondary|2026-08-02`;
IX is the only eligible class) · **Pilot chapter 8, *Journey Inside the Atom*** — 12 units ×
50 min, canonicals `[12, 10, 7]`.

**Scope** P1–P4 complete and applied live · P5 recorded below (**P5.4 open**, amber) ·
the [Claude] stage sign-off below · the **C1-gating engine work landed 2026-08-05** (the
carrier seam — see "The blocker"). **C1 has still NOT been run.** The stage is **not signed**.

**Reference pair read live, this session:** SS·secondary LP **v1.10** · assessment **v1.7**.

**Files amended (live, in place):**

| File | Before | After |
|---|---|---|
| `data/content/constitutions/lesson_plan/science/secondary/lesson_plan_constitution.txt` | v1.0 | **v1.1** |
| `data/content/constitutions/assessment/science/secondary/assessment_constitution.txt` | v1.1 | **v1.2** |

**Artefacts** (all in `genon/out/stage_prep_science_secondary/`): pre-amendment copies
`lesson_plan_constitution_v1.0_pre.txt` · `assessment_constitution_v1.1_pre.txt`; diffs
`lp_v1.0_to_v1.1.diff` (109 lines) · `assess_v1.1_to_v1.2.diff` (45 lines);
`apply_s3_amendments.py`, the reproducible edit script — every edit asserts exactly-one
occurrence, so the amended texts re-derive byte-identically. `CHANGELOG.md` sidecars written
beside both constitutions.

---

## Per-item verdict

| Item | Verdict | Evidence |
|---|---|---|
| **A1** — exactly ONE standard period row | **PRESENT** | INPUTS 4 was "one or more rows of {duration_minutes, count}"; now one row at the class-standard duration (50 for IX) × the count. TIME integrity restated as `duration × count` / `total period count = count`, replacing the sum-over-rows form. A3 gains `period_schedule: exactly one row …` and the schema comment `integer — the class-standard duration`. `grep "one or more rows"` = 0. **Declared deviation:** the reference's closing clause says "handled downstream at *partition time*"; the partition engine was retired 2026-07-31, so this file says **serve time**. This is S2's finding 2, fixed here instead of propagated. |
| **A5 + A7** — the register, ONE block, v1.10 three-ban re-cut | **PRESENT** | Single block after VOCABULARY, headed `THE SELF-CONTAINED REGISTER (binds Rules 7 and 10)`: clock quantity · forward reference/completion · calendar time, plus the "backward continuity is welcome" closing line. Not scattered — Rule 7 (prohibition 6, band text) and Rule 10 (prohibition 4, teacher notes) each *reference* it. Consequential edits follow the reference: VOCABULARY drops its positional cross-reference examples and gains the "session" exclusion; Rule 10's continuity link becomes position-free. **Declared deviation:** the reference's illustrative example is SS content ("Having traced the Vedic political vocabulary…"); a Vedic example inside a Science constitution would be a defect in kind, so the example alone is substituted with a Science one. The three bans and the closing rule are verbatim. |
| **A6** — items carry their anchor unit | **PRESENT VIA THE SUBJECT'S EQUIVALENT — deviates from the reference field, by ruling** | Science secondary's unique link is the **section**, not the unit: LOs are per-section (Rule 6), the handoff is one entry per section, and a section may be taught across several units (Rule 4). There is no single unit for the model to name, so `period_ref` is **not** ported. Instead both constitutions gain one integrity line recording that the platform derives the anchor from `section_number` through `coverage_handoff.period_numbers`, and forbidding the model emitting `period_ref` or any unit number. Founder ruling 2026-08-05: derive the link, never demand it — the same doctrine as compile v0.5's derived band ids. `grep -c phase_ref` = **0** in both files; the reversed v1.2-era band-level anchoring was never here and was not introduced. |
| **A9** — MCQ option order | **PRESENT, in the v1.7 form** | Rule 7 mandate gains "Option order carries no meaning and is not yours to set…"; prohibitions numbered; new prohibition 2 bans by-label references. The MEMORY-item-18 position prohibition ("is_correct MUST be distributed across A–D … MUST NOT repeat on the same label across consecutive items or cluster on one letter") is **struck**. `grep -i "alphabetic\|never led with\|vary in position\|consecutive items\|distribute"` = **0 hits** — no arrangement sentence came back. |
| **P3** — Group B schema conversion | **N/A (Group A)** | `grep -c "phases\["` = 0 and `grep -c '"description"'` = 0 in both files; A3 already emits `time_bands[{minutes, activity}]`. Nothing to convert — matches the §3 stage table. |
| **P4** — history to the sidecar | **DONE** | `CHANGELOG.md` created beside each amended file. Neither constitution carried an in-file version-history block, so nothing was lifted out; both keep their `VERSION` line and their footer version string (updated). Pre-v1.1/v1.2 history is honestly marked as unrecorded (git only). |
| **No cancelled amendment crept in** | **CLEAN** | `grep -ci` across both files for `band_id`, `band_refs`, `phase_ref`, `role_handoff`, `unit_handoff`: **0 / 0** on every term. |
| **No V-rule in a constitution** | **CLEAN** | `grep -ci` for "variant brief", "section registry", "synthesis", "precedence": 0 in both, except one hit on "precedence" in LP Rule 2 ("the cognitive demand of the implied task takes precedence over surface vocabulary") — pre-existing pedagogical prose, not a V-series precedence line. The V-series stays in `variant_plans.briefs_for`. |
| **No pedagogical rule changed** | **CONFIRMED** | LP diff touches only: VERSION, VOCABULARY, the register block, INPUTS 4, Rule 7 prohibition 6, Rule 10's continuity phrasing + prohibition 4, two integrity lines, two A3 schema comments, footer. Rules 1–6, 8, 9 and Amendment A4 are byte-identical. Assessment diff touches only VERSION, Rule 7's option clause, one integrity line, footer — Rules 1–6, 8–11 and the whole A1 schema are byte-identical. |

---

## The blocker — ✅ C1-gating work LANDED 2026-08-05; two items remain for C6/C12

> **The carrier seam is built** (`aruvi_core/genon/carriers.py`, new). Genon read
> `result["assessment_items"]` directly and assumed a flat list of item dicts carrying
> `period_ref` — true of Social Sciences and TWAU and of nothing else. **Science secondary
> wraps its items under a `"questions"` key**, so iterating the wrapper yielded its KEY NAMES
> as bare strings: measured on `ch_08_20260612_151832.json`, `compile_stream` returned
> **8 strings** (`'grade'`, `'subject'`, …) instead of 11 questions and reported no error,
> and `normalize_options` then died on `'str' object has no attribute 'get'`. Every chapter
> genon had ever processed was Social Sciences, so the assumption was invisible.
>
> The app never had this bug — it goes through the subject plugin, which knows each subject's
> shape. Genon skipped that layer, in breach of CLAUDE.md §3. `carriers.py` is that layer for
> genon: it asks the plugin, keeps `link_resolver`'s three verified carrier families, and
> refuses (`CarrierNotImplemented`, naming the owing stage) for mathematics and english rather
> than returning something plausible and wrong.
>
> **Landed:** `carriers.py` · `ScienceSubject.genon_assessment` (handoff-bridged, both stages)
> · `compile._anchor_items` now VALIDATES an anchor rather than deciding it ·
> `generate_canonical.validate` accepts the handoff bridge · `normalize_options._items_of`
> and `build_library.item_census` route through the seam's mutation-safe accessor.
> **Verified on the real Grade IX file:** STEP 6 scans 3 MCQs and moves 2 (was: crash) ·
> `item_census` returns `C-1.1 × 11` (was: crash) · `validate` reports **0** anchor problems
> (was: one per item) · `compile_stream` yields **11 dict items anchored U1…U11** (was: 8
> strings). **No regression:** both certified SS libraries (S1 ch 3, S2 ch 3) compile with
> every item anchored exactly as before, and the five suites still failing are the same five
> that failed beforehand — missing `fastapi` and missing english/science saved-plan data —
> none of which reference genon. New suite `tests/test_genon_carriers.py`, 16 tests, green.

**Why this was the P-ordering rule biting in a new place:** for S3 the precondition to C1 was
not only constitutional, it was **engine work**. Four changes were identified; **1 and 2 are
now done**, 3 and 4 remain and gate later steps. None is a per-stage branch — all make the
engine speak the 8-rule contract it already documents:

1. ✅ **DONE — `aruvi_core/genon/compile.py::_anchor_items`** — derive `unit_ref` from `section_number`
   through the handoff's `period_numbers` when `period_ref` is absent. This is the same join
   `link_resolver.handoff_period_index` already performs for the screen; it belongs in one
   place. Per the anchoring ruling below, `unit_ref` is the **last** unit teaching the section
   — `max(period_numbers)`, the same value `link_resolver` already uses as `anchor_period`.
2. ✅ **DONE — `genon/generate_canonical.py::validate`** — accept that resolution instead of demanding
   `period_ref`, so a section-carrier canonical certifies on its own terms.
3. ⬜ **OPEN — `aruvi_core/genon/serve.py`, handoff remap** — it does `for c in handoff.values()` and
   reads `c["los"]`, which is the SS shape (dict keyed by c_code, LO rows inside). Science
   secondary's handoff is a **JSON array** of section entries with no `los` key: this is an
   `AttributeError` on the first science serve, not a subtle mis-anchoring. Per the
   no-bespoke-logic rule the fix belongs in the science normalizer — normalize to the one
   shape serve already speaks — not in a branch inside serve.
4. ⬜ **OPEN — `aruvi_core/genon/compile.py`, the unit projection** — three more fields of the same
   kind, found at verification, so the list above was an undercount. `compile` reads
   `pedagogical_approaches` (**plural**) while this stage's A3 emits `pedagogical_approach`
   (singular), so every served science unit would carry an empty approaches list and the
   Overview "Pedagogy" row would render blank — the exact symptom SS·middle's finding 3
   flagged, arriving here for a different reason. It also reads `section_context` and
   `competency_edges` off the **period**, and LP Rule 6 prohibition 2 forbids both inside a
   period object at this stage (they live in the handoff), so both are structurally always
   empty. None of this errors; it silently empties the teacher-facing Overview.

Items 1–2 gated C1 and are landed. Item 3 gates C6, item 4 gates C12 — both still open. None of them changes a constitution, so
none triggers the §9 cascade. The shape of all four is identical: **the engine currently knows
only the SS carrier family**, and the 8-rule table's per-subject normalizer is where each
belongs — not as branches inside `serve`.

*(A fifth item — deduping the two lender append loops in `serve.py` — was withdrawn: under the
anchoring ruling below, `unit_ref` is a singleton, so an item can match the borrow loop or the
dropped-unit loop but never both, and the duplication cannot fire.)*

---

## P5 — stage inputs (class IX, ch 8)

**P5.1 Floor — ACCEPTED at the standing ratio, unchanged.** `round(0.6 × 12) = 7`; the row
carries `floor_minutes: 360.0`, `floor_periods_at_standard: 7`. Equal dispersion over [7, 12]
gives A−C = 5 ≥ 4 → `{12, ⌈19/2⌉ = 10, 7}`, and `canonical_periods` is exactly `[12, 10, 7]`.
No per-chapter override; §0.7's open-dial flag stands.

**P5.2 Section registry — a real cut to make, and it is not automatic.** Science is
section-anchored from the summary, so the *model* is obvious; the **granularity is not**.
`ch_08_summary.txt` carries 20 candidate headings: 16 numbered (8.1 · 8.2 · 8.2.1 · 8.2.2 ·
8.2.3 · 8.3 · 8.3.1 · 8.4 · 8.5 · 8.6 · 8.7 · 8.7.1 · 8.8 · 8.9 · 8.9.1 · 8.9.2) and 4
lettered sub-blocks (A/B/C under 8.2.2 — Rutherford's model, its limitations, discovery of
the proton — and A. Average atomic mass under 8.9.1).

**Recorded choice: the registry is the 16 NUMBERED sections; the four lettered blocks are
content within their parent, not registry entries.** Reason: a registry entry must be a
string the model reproduces verbatim and a teacher can locate in the book, and "B. Limitations
of Rutherford's model" is not independently numbered in the textbook. 16 sections against the
standard's 11 body units (12 minus the mandated `synthesis`) averages 1.45 sections per unit,
which leaves the Xth-unit choice set real granularity to work with. Reversible until C1; if the
sweep reads thin at the human gate, splitting 8.2.2 back into its three blocks is the first
dial to turn.

**Warning carried forward from the prototype run — corrected at verification.**
`backup/saved_plans/science/ix/ch_08_20260612_151832.json` (2026-06-12, pre-registry) anchors
several units to slash-joined strings such as "8.4 Symbols of Elements / 8.5 Atomic Number /
8.6 Mass Number". **That is not the defect it first looks like:** `serve._ANCHOR_JOINER` is
exactly `" / "` and `_unit_anchors` splits on it, so a slash-joined anchor is the engine's
*native* multi-section encoding — those three split into three verbatim registry entries and
pass the gate. A unit covering several sections is legitimate and `unit_range` spans it.

The file's real registry failures are two different things, and they are what the brief must
guard: (1) **a truncated heading** — unit 11 anchors "8.7 How Are Electrons Distributed"
against the registry's "8.7 How Are Electrons Distributed in Different Energy Levels?", which
fails the verbatim check; and (2) **anchors on lettered sub-blocks** — units 4 and 10 anchor
"B. Limitations" and "A. Average atomic mass", which the 16-section registry recorded above
deliberately excludes. Anchors must be verbatim and must be registry entries; joining several
with " / " is allowed and is how a compact unit covers a span.

**P5.3 Pilot chapter — CONFIRMED.** `data/content/chapters/science/ix/` has both
`ch_08_summary.txt` and `ch_08_mapping.json` (all 13 chapters do). The `master_plan.json` row
is `placeholder: false`, `recommended_periods: 12`, `standard_duration_minutes: 50`,
`weight: 8`. The `canonical_plan` is present but **`provisional: true`, `basis: "arithmetic"`,
`registry_sections: null`, `authored: []`** — it finalizes at C1 once the registry is authored
(compare S2, where the row read `provisional: false`, `basis: "authored_standard"`,
`registry_sections: 11`). Provisional is the expected pre-C1 state and does not block.

**P5.4 Three test identities — OPEN (amber).** All three still carry Social Sciences profiles
left over from S1/S2: `kumar1` SS VIII-A + IX-A/B · `kumar2` SS VIII-B + IX-C/E · `kumar3`
SS VIII-C + IX-A/Y. They must be rebuilt for **Science IX**, through the app's own first-run /
profile flow (the setup doubles as a live check of that flow), with **different sections per
identity** and **one longer duration alongside the 50-min standard** so C6's mixed-duration
matrix has something real to draw on. Provisional sign-off is permitted with only P5.4 open
(founder ruling 2026-08-02); **C6 is the hard stop.**

---

## The anchoring ruling (founder, 2026-08-05)

**An item's anchor is the LAST unit teaching its section — not the full unit set.**

The reasoning is a principle, not an implementation detail: an item tests the section's whole
`implied_lo`, so it becomes available only when the section **completes**. If the section was
not taught in full, the class cannot be tasked on any of it. The alternative — full-set
membership, where any fragment of the section entitles the plan to the whole question — would
hand a class a question two thirds of whose material they never saw, and a question that cannot
be answered is worse than a question that is absent.

**The engine's own preference order protects the rule.** A unit that teaches a split section has
`reach == M`, so it falls into the **M-alone** class and loses to any forward-reaching candidate
from another canonical *before* self-preference or pacing distance is ever consulted. With three
canonicals in the library, a split-section unit rarely wins the Xth slot.

**What C9 must MEASURE, because the failure is deterministic rather than probabilistic.** When
the winning Xth-unit candidate *is* a split-section unit, its item is **always** lost —
`first_dealing_unit` returns the section's FIRST unit, and the item is pinned to its last, which
is neither borrowed nor eligible as a dropped unit (a unit teaching a covered section fails the
`⊆ uncovered` test). So C9 counts serves whose fill candidate belonged to a multi-unit section;
that number is the rule's real cost on a certified library, not an inference from two prototype
files.

**Rider still owed.** The invariant — *an item appears iff its section completed* — is currently
**emergent** from `max()` in `link_resolver`, not stated anywhere. It must be written down: in
`variant_canonical_architecture.md`, and as a line in the assessment constitution beside the
anchoring line already added, so the next section-carrier stage (science·middle,
mathematics·secondary) inherits a rule rather than rediscovering a behaviour.

**Side effect — the engine list shrinks.** With a singleton `unit_ref`, an item can match the
borrow loop or the dropped-unit loop but never both, so the two-loop duplication risk cannot
fire and that fix is withdrawn. The blocker list stands at four.

---

## Two smaller things, recorded rather than fixed

- **The LP's new ITEM ANCHORING line addresses an output the LP does not produce.** It tells
  the model not to emit `period_ref` on an assessment item, but the LP constitution's OUTPUTS
  list carries no assessment items — the assessment-side line is the operative one. Kept
  deliberately: both files are read in the same system prompt when LP and assessment are
  generated in one call, and the LP is where the handoff (the thing the anchor resolves
  through) is defined. Harmless duplication, not a contradiction.
- **INPUTS 4's duration parenthetical stops at IX, but this constitution governs `ix · x`.**
  Ported verbatim from the reference, which has the same gap. There is no class-X content in
  any subject and no class-X row in `master_plan.json`, so nothing breaks today; it is a real
  hole for the second grade this file governs and should be closed campaign-wide, not here.

---

## Still open before the stage is signed

1. Engine items **3 and 4** above (items 1–2 landed 2026-08-05). Item 3 gates C6, item 4 gates C12.
2. **P5.4** — the three Science IX profiles, built through the app.
3. **P5.2's registry cut** — recorded as a choice above; confirm or overturn before C1.
4. The **HUMAN GATE**, after the C-cycle.

**One thing this stage owes the campaign.** A6 has been discharged here in a form the
reference does not carry — section anchoring with a derived unit — and **Science middle and
Mathematics secondary have the same section-carrier shape**. Whatever is settled here will be
copied three more times. It belongs on MEMORY.md's "★ AMENDMENTS TO BE TESTED" list, due at
this stage's C9, not at a later stage's human gate.
