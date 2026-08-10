# S7 · mathematics · middle — stage preparation sign-off

**Date:** 2026-08-10 · **Template:** `docs/testing.md` v2.9
**Drawn class:** VII (seed `mathematics|middle|2026-08-02`) · **standard duration:** 40 min
**Reference pair:** SS·secondary LP v1.10 · assessment v1.7, via the mathematics·secondary
v1.3 / v1.2 adaptation (same subject vocabulary, one stage up)
**Landed pair:** mathematics·middle LP **v3.3 → v3.4** · assessment **v3.2 → v3.3**
**Pilot chapter:** VII · ch 7 · *A Tale of Three Intersecting Lines*

Written by Claude. Status in the tracker is set by Kumar.

---

## 0. The headline — S7 is CLEAR to enter C1, and the stage's whole difficulty was a naming one

P1–P5 are complete. Nothing is owed, nothing is blocked, and — unlike S4 and S6 — no gate is
carried into the C-cycle.

The stage looked at first like it needed three new fields. It needed none.
**Founder ruling, 2026-08-10:** maths·middle already carries every fact the serve engine wants,
under other names — the period's `textbook_segments[].ref` is the section anchor, and the
handoff entry's `section_ref` is the item's route to its unit. The precedent is the prototype,
which resolved exactly this shape variance at the READ boundary and said so in terms:

- `Project Aruvi/app/aruvi_streamlit/lp_pdf_generator.py:2583-2592` — *"Middle/prep maths use
  `textbook_segments` (list of {ref,title} dicts); secondary maths uses a flat `section_anchor`
  string. Prefer textbook_segments when present, else section_anchor."* Ten lines below, the
  same tolerance for `phases` vs `time_bands`.
- `assessment_pdf_generator.py:117-192`, `_regroup_middle_maths_by_section` — re-buckets
  middle-maths items onto the chapter-section axis from each item's own `section_ref`,
  *"The constitution / generated JSON is NOT changed — this runs at render time."*
  Detection is by SHAPE (`goal` present, `intent` absent), never by subject name.

The SaaS keeps that answer and moves it to the sanctioned seam — `aruvi_core/genon/carriers.py`
and the subject plugin (CLAUDE.md §3) — instead of scattering it across renderers. So the
anchor and the handoff were **P5.5 work, not P1 work**, and the constitutions were left alone
on both counts. The edit script asserts both absences as guards so a later pass cannot
reintroduce them by drift.

**The one exception, and it is a real one: P3.** `phases[{minutes, description}]` →
`time_bands[{minutes, activity}]` could NOT be absorbed by a tolerant read, because `compile.py`
does not merely read the bands — it rebuilds the timed spine from `p["time_bands"]` (`:124`) and
asserts an inventory invariant over `tb["activity"]` (`:208-210`). Founder called it for the
amendment, following testing.md P3 and S6's 2026-08-07 conversion.

---

## 1. Per-item verification (testing.md §3, the Claude sign-off)

| Item | Verdict | Evidence |
|---|---|---|
| **A1** — one standard row | **PRESENT** | INPUTS 4 was "Period schedule: {duration, count} **rows**; total = B" — which licensed exactly the mixed-duration plan the variant engine cannot use. Now "exactly ONE row {duration_minutes, count}: the class-standard duration (40 min for classes up to VII, 45 for VIII, 50 for IX–X — the master-plan calibration bands, not NCF's flat 40) × the period count; total = B. Teacher timetable variation never reaches generation; it is handled downstream at serve time." The schema's `period_duration_minutes` carries the same constraint where it is actually read. **Declared deviation:** "serve time", not the reference's "partition time" — the partition engine was retired 2026-07-31. Same correction S3, S4 and S6 made. |
| **A5 + A7** — register as ONE block | **PRESENT, verbatim in substance** | One block after VOCABULARY in the v1.10 **three-ban** re-cut (this stage is not S6's two-ban exception — its units anchor to textbook sections and travel between plans, so ban 2 binds in full). Bound at **Rule 10** (band narration) and at the **`teacher_notes`** schema comment by reference, never as scattered prohibitions. **Declared deviation:** illustrative strings are middle-maths ones — "a quick mental calculation", "an extended construction", "having covered all three angle pairs", "Having established that vertically opposite angles are equal, …". The three bans and the closing backward-continuity rule are verbatim in substance. **Two consequential edits, both following the reference:** VOCABULARY was *teaching* the forward reference ban 2 forbids (its cross-reference examples were literally "the previous unit", "this unit") so the examples are dropped and "session" is added to the excluded register; and the `teacher_notes` continuity bullet ("briefly recap what the previous unit covered") is now position-free — carry continuity by naming the content built on. |
| **A6** — item anchoring | **CONFIRMED, not amended; one integrity block added** | Items already carry `section_ref`, copied verbatim from the LP handoff entry. Middle mathematics is the **PERIOD-FIELD** family (8-rule row 4): the platform resolves `section_ref` against each period's own `textbook_segments[].ref`, with **no `coverage_handoff` in the path** — so the reference's `period_ref` field is not ported, and neither is secondary's `section_number`. The new ANCHORING block records four things: `section_ref` IS the anchor and is pass-through; a section spanning several units anchors at the **LAST** of them (founder 2026-08-05); `period_ref` / `period_number` / any unit number MUST NOT be emitted, because declaring the link would freeze an arrangement the platform varies per teacher; and `anchor_id` is not an anchor in this sense (Rule 8) — it seeds the exercise companion only. Same shape as science·secondary v1.2 and science·middle v1.4: derive the link, never demand it. `grep -c phase_ref` = 0 in both files. |
| **A9** — option order | **PRESENT as two lines; the removal is N/A, and no arrangement sentence** | **REMOVAL — N/A.** This file never carried the MEMORY-item-18 position prohibition; testing.md P2 names four files that do (SS + Science, middle and secondary) and this is not one. Confirmed by grep: `consecutive`, `same label`, `vary in position` all 0. Nothing was struck. **ADDED**, v1.7 wording, in Rule 10's MCQ block: the "order carries no meaning and is not yours to set" mandate, and the by-label option-reference prohibition ("both A and B", "none of the above", "all of the above") — the one construction a downstream sort cannot reorder without rewriting. This file carried no prior "none of the above" ban, so the addition is purely additive. **NOT re-added:** `alphabetically` · `never led with` · `first word at which they differ` all assert 0 in the edit script's guards. |
| **P3** — Group B conversion | **APPLIED — real, not N/A** | Second stage where this was not N/A (after S6). Array and key both renamed, with Rule 6, Rule 8, Rule 10's heading and prose, Rule 11's guard case and the schema following. **No `band_id`** in the target shape. `grep -c 'phases\['` = 0, `'"phases"'` = 0, `band_id` = 0, `time_bands` = 2. Note this leaves the existing maths·middle/prep saved-plan corpus on the old shape; the prototype's tolerant read still covers display, and the fixture used in the new tests renames the bands in a deep copy for exactly this reason (§3.4). |
| **P4** — history to the sidecar | **DONE** | `CHANGELOG.md` created beside both constitutions. Neither carried an in-document version-history block, so nothing was lifted out. The LP's stale footer ("Version 3.1", left behind through the 3.2 and 3.3 bumps) is corrected to 3.4 in the same pass. The assessment sidecar also carries a standing renderer note: Rule 7 permits a `number_line:` stimulus at this stage and prohibits SVG — confirm both renderers still carry a `number_line:` branch at C13, since a permitted format with no detection branch is a known failure mode. |
| **Cancelled amendments A2/A3/A4, X3** | **ABSENT** | None introduced. |
| **V-rules in a constitution** | **NONE** | No section registry, no verbatim-anchor mandate, no first-visit-order rule, no closing-synthesis mandate, no per-variant assessment rule, no INPUTS acknowledgment, no precedence line. All of it stays in the platform-composed brief. Worth stating because the synthesis mandate sits in visible tension with LP **Rule 2** ("Every section listed in the summary MUST appear in at least one period's `textbook_segments`. Dropping a section is FORBIDDEN") and **Rule 1** ("each period anchors to one or at most two adjacent sections") — a synthesis unit anchors to no section at all. The brief overrides, the constitution is deliberately left alone, and `carriers.is_synthesis` + the certifier's token exemption are where that is handled. §3.3 below is how that was made to work on a stage with no `section_anchor` field. |

---

## 2. P5 — stage inputs

**P5.1 · The floor.** Accepted at the standing ratio `round(0.6 × recommended_periods)`, no
override. For ch 7 that is `round(0.6 × 12) = round(7.2) = 7`, matching
`floor_periods_at_standard` on the row. Equal dispersion over [7, 12]: A−C = 5 ≥ 4, so counts
are `{A, ⌈(A+C)/2⌉, C}` = **[12, 10, 7]** — three canonicals, three authoring runs.

**P5.2 · The section registry.** Middle mathematics' section model is **obvious and needs no
definition** — the summary carries an explicit `sections[]` spine of `{ref, title, section_goal}`,
and the period's `textbook_segments[].ref` reproduces the ref verbatim. For ch 7 the registry is
the five refs in summary order:

```
section 7.1 Equilateral Triangles · section 7.2 Constructing a Triangle When its Sides
are Given · section 7.3 Construction of Triangles When Some Sides and Angles are Given ·
section 7.4 Constructions Related to Altitudes of Triangles · section 7.5 Types of Triangles
```

**The token is `"section 7.1"`, with the word, not `"7.1"`** — that is what the summary carries
and what real saved plans emit, and the mediated anchor returns it **verbatim** rather than
normalising it. Verbatim is the whole point: the certifier compares the anchor against a registry
drawn from the summary, and both sides are the same string by construction. (The LP schema's
illustrative examples still read `"§5.3"` — a cosmetic residue from an earlier notation, inert
because the model copies from the summary, not from the example. `link_resolver.norm_code`
collapses all three forms anyway.) Consistency across the library is guaranteed by construction:
`standard_registry()` reads the registry off the AUTHORED standard canonical and `briefs_for()`
prints it verbatim into each compact's brief.

**P5.3 · The pilot chapter — mathematics · VII · ch 7, "A Tale of Three Intersecting Lines".**
All 15 chapters of the class are eligible (summary + mapping on disk, none `placeholder: true`),
so this was a shape choice, not a availability one. Ch 7 is mid-book, has five clean numbered
sections, `recommended_periods` 12, floor 7, counts [12, 10, 7], `core_cg` CG-3,
`effort_index` 8.0, `canonical_plan` present with `basis: "arithmetic"` and
`provisional: true` (expected until the standard is authored). Chosen over ch 5 (9 sections,
15 periods — richer but the most expensive in the class) and ch 12 (4 sections). Two shape
notes carried forward to the C-cycle rather than treated as blockers:

- **12 units over 5 sections** is the S4 consolidation condition — there is no legal anchor
  token for a unit that consolidates rather than teaches a new section, so the model will pick
  the least-wrong registry entry for the surplus units. Expect the certifier's *advisory* (a
  unit wearing a label the handoff does not route through), and do **not** repair it by
  extending the routing; S4's §3.3 measured that fix and it costs a question and buys nothing.
- **Zero worked examples** (1 activity, 30 exercises). Rule 11's anchor priority is
  exercise → worked_example → activity, so the anchor pool is comfortable. But Rule 10's
  optional `teacher_notes` self-study pointer — "book_ref of a worked example NOT walked through
  in class" — is **unsatisfiable for this chapter**. It is optional, so this is a C3 watch item:
  a fabricated `WE-n` here would be an internal-ID leak, not a nicety.

**P5.4 · The three test identities' profiles for class VII. OPEN — the stage is signed
PROVISIONALLY.** Founder ruling 2026-08-02 permits it; **C6 is the hard stop**. When set up,
do it through the app's own first-run / profile flow (the setup doubles as the live check of
that flow), give the three identities *disjoint* sections so X1's tenancy evidence is
unambiguous, and put one longer duration on **kumar3** — the identity §4 assigns the
mixed-duration weekly matrix to — alongside the 40-minute class standard.

**P5.5 · The carrier trace.** Mathematics·middle's row of the verified 8-rule table:

> **rule 4** · period-field join · item `section_ref` ("section 7.1") → period
> `textbook_segments[].ref` · **no handoff in the path** · **no LO** (structural link only —
> `linked_lo` is null at this stage and the 3b renderer omits the line, by design) ·
> container: a LIST of `{section_code, section_title, note, items[]}` groups ·
> app-side method **`_middle_assess`** (`subjects/mathematics/subject.py:242`, parity-tested,
> already serving the app) · `genon_assessment` **ABSENT** at start · **in `_NOT_YET`.**

**CLOSED 2026-08-10.** Delegated, never re-invented — see §3 for what landed and what it found.

---

## 3. What was found along the way — four items, all fixed, none constitutional

### 3.1 `raw_item_list` returned the GROUPS, not the items (the ARV-D-060 class, latent)

`carriers.raw_item_list` returns `raw` whenever `result["assessment_items"]` is a list. Maths
middle and preparatory store a list of **section-code groups**, each wrapping its own `items[]`
— so the function handed back group dicts. STEP 6 (`normalize_options`) and
`generate_canonical.validate` would both have iterated groups instead of items: option ordering
silently no-ops, the item-anchor validator silently sees zero items, and a paid canonical
installs looking clean.

This is the same defect science's `questions` wrapper produced at S3 and that `item_container`
was written for at S4 — third recurrence, third container shape. Fixed **shape-based, never
subject-based**: a list every element of which is a dict carrying an `items` list is a group
container; `raw_item_list` flattens to the LIVE item objects (field mutation still reaches the
file; appends and removals do not, and the docstring says so), `item_container` captures the
group shells, and `from_engine_items` re-buckets served items back into their A/B/C groups —
emitting an empty group rather than dropping it, since LP Rule 11 and assessment Rule 1 both
require the empty cluster to exist.

### 3.2 The goal-cluster handoff fell through `to_engine_handoff` unfiltered

`serve.py` speaks one handoff shape: `{key: {…, "los": [{"period_number": N}]}}`. Maths middle's
handoff is a dict of three goal clusters whose entries carry no period number at all, so it
passed through unchanged, `c.get("los", [])` returned `[]`, nothing was filtered, and a served
plan would have carried handoff rows for units it does not contain.

Fixed with a second carrier marker beside science's, on the same lossless
normalise-in / restore-out contract: one engine block per goal **entry**, `los` derived from the
same period-field index the items join through, restored into `section_a`/`section_b`/`section_c`
in authored order with dead entries dropped and empty clusters kept. **No field was added to
the handoff** — the period set is derived from the entry's own `section_ref`, and an entry
survives iff at least one period teaching its section is served. That is the same semantics
science's section rows already have.

### 3.3 The synthesis mandate named a field this stage does not have (pre-C1, paid if missed)

Architecture v2.0 requires the STANDARD canonical to close with a whole-chapter synthesis unit,
and `variant_plans.top_brief_for` mandates it by naming `section_anchor` — a field maths·middle's
constitution never defines. The brief would have asked the model for something it cannot emit, at
metered STEP 1, and the certifier would then have found no synthesis unit. This is S7's analogue
of S4's synthesis-handoff defect: a **V-series / brief matter, and it must not enter a
constitution.**

The answer already existed: `carriers.is_synthesis` reads a `"synthesis": true` boolean as well
as the token, and `_arc_brief` already asks science·middle for the boolean *"(this stage has no
section_anchor field, so the boolean is how the platform recognises it)"*. That was generalised —
the boolean form is now for any stage whose anchor is **mediated**, declared as
`genon_anchor_field_present` on the plugin rather than sniffed. **And chasing it turned up two
live engine bugs that the token had been hiding:** `serve.section_registry` filtered the synthesis
unit out by matching the anchor TEXT, and `serve.unit_range` was rangeless only incidentally — so
with a boolean-carried synthesis whose anchor is a real section string, the synthesis unit could
have entered the registry and been picked by `first_dealing_unit` as somebody's Xth unit. Both now
short-circuit on `is_synthesis_unit`. A third: `carriers.unit_anchor` raised `KeyError` on a
mediated synthesis unit (section axis True, no `textbook_segments`) and now returns `None` — not
the token, because manufacturing an anchor string would write into a field this constitution does
not define. Behaviour on the ten token stages is unchanged **by proof, not by inspection**: 50
standard briefs and 5 compact brief sets were snapshotted before the edit; only the six mediated
mathematics combos differ.

### 3.4 Two smaller things, recorded so nobody re-derives them

- **The `maths_vi_ch05_saved.json` fixture predates P3** — its periods carry `phases[]`, so it
  cannot compile as authored. The new end-to-end test renames the bands in a deep copy and says
  why; everything else (anchors, items, handoff) is the file as authored. This is the corpus-wide
  consequence of P3 and is expected, not a defect.
- **`build_library.py mathematics vii 7 --certify-only` does not reach the certify branch.**
  STEP 0's carrier pre-flight now passes, but STEP 2 (`variant_plans.py` annotate) runs even under
  `--certify-only` and exits with `Row is provisional — author and certify the standard
  canonical…`. That is the correct downstream gate and the same place S4 stopped, but it means
  the free `--certify-only` smoke test is unavailable on a chapter whose row is not yet
  annotated. Worth knowing before it reads as a failure.

---

## 4. Verdict — **ALL P-STEPS CLOSED; S7 IS CLEAR TO ENTER C1**

**P1, P2, P3, P4 — complete and verified. P5.1–P5.3 — recorded. P5.5 — DONE (carrier landed,
tested). P5.4 — OPEN, and it is the only amber: the stage is signed PROVISIONALLY and C6 is the
hard stop.** All four §3 findings are fixed, not merely declared.

**Test state:** `tests/test_genon_carriers.py` **36 → 80 tests, all green**, covering the row-4
join at the section's LAST unit, zero orphans on a real saved plan, an unserved section resolving
to `[]` rather than a guess, raw item fields surviving, `raw_item_list` returning items not
groups and mutation reaching the structure, the A/B/C group round trip including an empty group,
the verbatim anchor and its `" / "` join on a two-segment period, the three-cluster handoff round
trip with a dead entry dropped, the brief carrier on both forms, the certifier holding on a
mediated-anchor stage, and the no-grade regression. `test_maths_port`, `test_genon_serve`,
`test_genon_plan_key`, `test_genon_duration_order`, `test_genon_plan_granularity`,
`test_borrowed_anchor`, `test_genon_approach_survives_serve`, `test_unit_order` and
`test_unitize` all green. Five suites fail **pre-existing and unrelated**, the same five the S4
sign-off recorded: `test_api` (no `fastapi`), `test_link_resolver` + `test_normalized_item`
(missing English saved plan), `test_lp_standard` (missing TWAU view), `test_stimulus` (16
fixtures against an asserted ≥20).

### The C1 command

```bash
python3 genon/build_library.py mathematics vii 7
```

It will not stop at the carrier. It **will** stop at STEP 2 with "Row is provisional" until the
standard canonical exists — the normal path for a fresh chapter, not a fault.

### Two housekeeping items for Kumar

1. **`rm .git/index.lock`** — a stale zero-byte lock sits in the repo (from a `git stash` a
   subagent attempted; the sandbox refuses writes inside `.git`, so no stash was created and
   `git stash list` is empty). Any `git add`/`commit` from the Mac side needs it removed first.
2. **Eight S4 served-plan files were deleted mid-session and have been restored** from HEAD
   (`data/content/saved_plans/mathematics/ix/ch_04_*_e17_*.json`, `*_e18_*.json`, and
   `ch_99_canonical.json`) — a subagent ran a `purge_derived` cleanup that took them with it.
   These are C10.3 no-overwrite evidence for a stage in mid-cycle, so their loss would have been
   real. `git status` now shows zero deletions; verify before committing.

### Disclosed residues (declared, not fixed)

1. **The LP schema's `"§5.3"` examples** — a notation the corpus does not use (real plans emit
   `"section 5.3"`). Inert, because the model copies the ref from the summary, not from the
   example, and `norm_code` collapses both. Left alone rather than patched per stage; if it is
   to be aligned, align it in the summary-side authoring prompt so all three maths stages agree.
2. **A4's `period_duration_minutes` is now over-specified** — under one standard row nothing can
   vary. Harmless and identical to the residue S4, S3 and S6 each disclosed.
3. **The class-X band.** INPUTS 4 names "50 for IX–X" in a middle-stage constitution whose grades
   are VI–VIII. Ported verbatim from the reference for consistency, inert here.
4. **The `"synthesis": true` boolean does not survive serving** — `synthesis` is in compile's
   `_MODELLED` set and `_period_from_unit` does not re-emit it. Pre-existing, identical for
   science·middle since S6, and nothing downstream reads it; noted only because the boolean now
   carries two stages instead of one.

Artefacts, all in `genon/out/stage_prep_mathematics_middle/`:
`lesson_plan_constitution_v3.3_pre.txt` · `assessment_constitution_v3.2_pre.txt` ·
`lp_v3.3_to_v3.4.diff` · `assess_v3.2_to_v3.3.diff` · `apply_s7_amendments.py` (the reproducible
edit script — every edit asserts exactly-one occurrence, and the run closes on guards for the
struck A9 arrangement strings, the retired `phases` shape, `band_id`, `phase_ref`, and the two
absences the founder ruling requires). Plus the two `CHANGELOG.md` sidecars.
