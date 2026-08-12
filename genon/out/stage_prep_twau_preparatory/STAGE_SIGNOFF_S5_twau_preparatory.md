# S5 · the_world_around_us · preparatory — stage preparation sign-off

**Date:** 2026-08-11 · **Template:** `docs/testing.md` v2.9
**Drawn class:** V (seed `the_world_around_us|preparatory|2026-08-02`) · **standard duration:** 40 min
**Reference pair:** SS·secondary LP v1.10 · assessment v1.7 — taken DIRECTLY, not through an
adaptation. TWAU shares SS's carrier family (item-self-sufficient, rows 3 and 8) and, like SS,
already emits `time_bands`, so this is the closest any stage has sat to the reference since S2.
**Landed pair:** TWAU·preparatory LP **v1.2 → v1.4** (v1.3 the carry-forward, v1.4 the Rule 5
word cap) · assessment **v1.3 → v1.4**
**Pilot chapter:** V · ch 5 · *Our Vibrant Country* (6 sections · 27 tasks · rec 16 · floor 10 ·
counts [16, 13, 10])

Written by Claude. Status in the tracker is set by Kumar.

---

## 0. The headline — S5 is CLEAR to enter C1, and the one real finding was in the ENGINE, not a constitution

P1–P5.5 are complete. Nothing is owed and no gate is carried into the C-cycle. **P5.4 (the three
test identities' teaching profiles for class V) is open by design** — it needs the live app, it is
not consumed by generation or certification, and the founder ruling of 2026-08-02 permits a
provisional signature with it open. C6 is its hard stop.

**The constitutional half was the cheapest of the campaign so far, and for a structural reason.**
TWAU is the reference's own carrier family and already emits `time_bands`, so **P3 is genuinely
N/A** (not converted — never needed converting) and **A6 is a pure confirmation**: `period_ref[]`
was already in the schema, already correct, already the mechanism. A9's removal half is N/A too.
What actually landed is A1, the register, and two blocks of writing-down.

**The one real finding is §4, and it is not in a constitution at all.** `carriers.unit_anchor`
reads `period["section_anchor"]`; TWAU periods carry **`section_ref`**, and `grep -c
section_anchor` is 0 in its LP constitution. So every TWAU chapter would have died with a
`KeyError` on its first period at compile — **after** metered STEP 1 and STEP 4 had already run.
This is the P5.5 warning firing on a stage that was never in `_NOT_YET`, because `_NOT_YET`
tracks the *assessment* half of the seam and this is the *lesson-plan* half. It is closed, on the
plugin, as a mediation — and `tests/test_genon_carriers.py` had it written down as an open gap
against S5's name all along.

**One numeric limit was widened, free, before authoring** — LP Rule 5's `section_context` cap
(§5). S8's standing rule found it, exactly as S8 said it would.

---

## 1. Per-item verification (testing.md §3, the Claude sign-off)

| Item | Verdict | Evidence |
|---|---|---|
| **A1** — one standard row | **PRESENT** | INPUTS 4 was *"Period schedule — one or more rows of {duration_minutes, count}."* — which licensed exactly the mixed-duration plan the variant engine cannot use. Now: *"exactly ONE row {duration_minutes, count}: the class-standard duration (40 min for the Preparatory stage — the master-plan calibration band) × the period count … Teacher timetable variation never reaches generation; it is handled downstream at serve time."* The Preparatory band is **40 min**, matching `master_plan.json`'s `the_world_around_us\|V` row (`standard_duration_minutes: 40`). **Declared deviation:** "serve time", not the reference's "partition time" — the partition engine was retired 2026-07-31. Same correction S3, S4, S6, S7 and S8 made. **Two residues moved with it:** the INTEGRITY CONSTRAINTS `TIME:` line still summed "per schedule row" over "row counts", and the JSON schema's `period_schedule` array carried no row-count comment — **the schema is the surface the model copies from**, and this is now three stages running (S7 v3.7, S8 v1.3, here). *Naming note:* the campaign's "A1" is not this file's own `AMENDMENT A1 — FULL LP JSON SCHEMA`, which shares the label and is a different thing; the campaign amendment lands in INPUTS 4 where the reference puts it. |
| **A5 + A7** — register as ONE block | **PRESENT, verbatim in substance** | One block after VOCABULARY in the v1.10 **three-ban** re-cut. This stage is **not** S6's two-ban exception: LP Rule 1 is titled SINGLE-AXIS SECTION ANCHORING and walks `sections[]` in reading order, and TWAU units travel between canonicals under the serve engine, so ban 2 binds in full. Bound at the two fields it governs **by reference, never as scattered prohibitions** — Rule 5's `time_bands` prose and its `teacher_facilitation_note` (Rule 10's IKS prompt lives inside that note and is covered by the same binding). **Declared deviation:** the illustrative strings are TWAU ones. **One consequential edit, the same one S7 and S8 made:** VOCABULARY was *teaching* the positional cross-reference ban 2 forbids — its examples were literally `"the previous unit"` / `"this unit"` — so the examples are dropped, the rule is restated as *cross-reference by the CONTENT built, never by position*, and "session" joins the excluded register. **One carve-out stated explicitly, and it is new to this stage:** ban 1 governs PROSE, and the band's own `"minutes"` field (`{ "minutes": "0-5", "activity": … }`) is schema. Without the sentence a literal reading of "no clock quantity" collides head-on with Rule 8's mandate that bands sum exactly to the period duration. |
| **A6** — item anchoring | **CONFIRMED, not amended; one integrity block added** | TWAU preparatory is **8-rule row 8**, the **ITEM-SELF-SUFFICIENT** family — the same family as social_sciences and, unlike every stage since S2, the same family as the reference. The item carries `period_ref[]` DIRECTLY and its own `implied_lo` inline; there is no handoff bridge and no period-field join. The field was already in the schema and already correct, so **nothing was added to the item**. The new ANCHORING block records three things: `period_ref` IS the anchor and is emitted directly; where an item reaches several units it anchors at the **LAST** of them (founder 2026-08-05); and anchoring is UNIT-level, so no band-level reference may be emitted (`grep -c phase_ref` = 0 in both files). **Worth stating because the neighbouring stage went the other way:** maths·preparatory v1.3 had to write down that `period_ref`/`period_number` MUST NOT be emitted, because on a period-field stage declaring the link freezes an arrangement the platform varies. On row 8 the declaration IS the mechanism. Same field, mandatory here and prohibited there — a property of the family, not an inconsistency, and the block says so. |
| **A9** — option order | **PRESENT as two lines; the removal is N/A, and no arrangement sentence** | **REMOVAL — N/A.** This file never carried the MEMORY item-18 position prohibition; testing.md P2 names four files that do (SS + Science, middle and secondary) and this is not one. Confirmed by grep: `consecutive`, `same label`, `vary in position` all **0**. Nothing was struck. **ADDED**, v1.7 wording, in Rule 6 (MCQ DISTRACTOR DESIGN): the "order carries no meaning and is not yours to set" mandate, and the by-label option-reference prohibition ("both A and B", "none of the above", "all of the above"). This file carried no prior "none of the above" ban, so the addition is **purely additive** — not an absorption as at S4. **NOT re-added:** `alphabetically` · `never led with` · `first word at which they differ` all assert **0** in the edit script's guards. |
| **P3** — Group B conversion | **N/A — and genuinely so** | TWAU has emitted `time_bands` with an `activity` key since before the campaign, which is what the §1 matrix records. `grep -c 'phases\['` = **0**, `'"phases"'` = **0**, `time_bands` = **7**. Nothing to convert, and — unlike the maths and english stages — **no saved-plan corpus is left behind on the old shape**, because there was never an old shape. This is the first stage since S2 where P3 costs nothing and leaves no debt. |
| **P4** — history to the sidecar | **DONE** | `CHANGELOG.md` created beside both constitutions (neither had one). Neither carried an in-document version-history block, so the P4 exit criterion was already met on arrival and nothing had to be lifted out. Both sidecars back-fill what was recoverable: the LP's pre-1.2 history is git only; the assessment's **v1.3** entry is reconstructed from MEMORY.md §"AMENDMENTS TO BE TESTED" item 1 (the 2026-07-10 `guide.{TYPE}` nesting bump) **and carries its standing debt forward** — see §6. |
| **Rule 5** — `section_context` cap (v1.4) | **AMENDED, on measured evidence** | Not part of the carry-forward set; raised because S8's standing rule says to. 10–15 → **10–25 words**, both in the rule and in the schema comment. Full reasoning and the measurement in §5. |
| **Cancelled amendments A2/A3/A4, X3** | **ABSENT** | None introduced. Asserted by guard: `role_handoff`, `unit_handoff`, `band_ref`, `band_id`, "role weighting" all **0** in both files. |
| **V-rules in a constitution** | **NONE** | No section registry, no verbatim-anchor mandate, no first-visit-order rule, no closing-synthesis mandate, no per-variant assessment rule, no INPUTS acknowledgment, no precedence line — asserted by guard ("section registry", "synthesis unit", "reserved token" all **0**). Also **`section_anchor` = 0**, and that absence is deliberate rather than incidental: the founder ruling of 2026-08-10 forbids inventing a field to feed the serve engine, so the anchor stays `section_ref` and the READ is mediated (§4). Worth stating because the synthesis mandate sits in visible tension with LP **Rule 1** (*"Every named section receives at least one period … MUST NOT reorder, merge out of sequence, or skip any named section"*), since a synthesis unit anchors to no section at all. The brief overrides, the constitution is deliberately left alone, and `carriers.is_synthesis` + the certifier's exemption are where that is handled. Identical to the tension S7 and S8 recorded. |

---

## 2. P5 — stage inputs

**P5.1 · The floor.** Accepted at the standing ratio `round(0.6 × recommended_periods)`, no
override. For ch 5 that is `round(0.6 × 16) = round(9.6) = 10`, matching
`floor_periods_at_standard` on the row. Equal dispersion over [10, 16]: A−C = 6 ≥ 4, so the
counts are `{A, ⌈(A+C)/2⌉, C}` = **[16, 13, 10]** — three canonicals, three authoring runs.

**P5.2 · The section registry.** TWAU's section model is obvious and needs no *definition*, but
its TOKEN is unlike every stage certified so far and that fact is load-bearing. The summary
carries `sections[]` of `{title, content_summary, tasks[]}` with **no `ref` code at all**, and
the period's `section_ref` reproduces the section **TITLE** verbatim. So the registry token is a
full natural-language title:

```
A Special Day in School · Finding India in Currency Notes · Symbols that Speak ·
Our Vibrant Culture · Diversity Everywhere · Spirit of Togetherness
```

Compare: SS uses a section label, maths·middle a chapter-prefixed code (`"section 7.1"`),
maths·prep a chapter-local code (`"S1"`). **TWAU is the first stage whose registry token is
prose.** The consequence is that "verbatim" stops being a formality and becomes the whole
guarantee — a dropped subtitle, a re-cased word or a straightened em dash silently
manufactures a registry miss that the choice-set arithmetic then reads as an uncovered section.
`genon_unit_anchor` therefore returns the string untouched (§4), and consistency across the
library is guaranteed by construction anyway: `standard_registry()` reads the registry off the
AUTHORED standard canonical and `briefs_for()` prints it verbatim into each compact's brief.

**Verified on the real corpus, not asserted.** `backup/saved_plans/.../v/ch_05_*` compiles to 9
units over these 6 sections; **every anchor is a byte-identical member of the registry** and the
sections **first-appear in registry order**, with no interleaving. That is C5's checks 3 and 4
passing on a pre-campaign artefact, which is the strongest evidence available before C1.

**P5.3 · The pilot chapter.** `the_world_around_us|V` ch 5 *Our Vibrant Country*. Summary and
mapping both on disk (`data/content/chapters/the_world_around_us/v/{summaries,mappings}/ch_05_*.json`),
`placeholder: false`, `canonical_plan` present. The row:

```json
{"chapter": 5, "title": "Our Vibrant Country", "weight": 12, "exact_share": 15.7,
 "recommended_periods": 16, "canonical_minutes": 640, "floor_minutes": 384.0,
 "floor_periods_at_standard": 10, "canonical_periods": [16, 13, 10], "placeholder": false,
 "canonical_plan": {"counts": [16, 13, 10], "provisional": true, "basis": "arithmetic",
                    "registry_sections": null, "authored": []}}
```

`provisional: true` / `basis: "arithmetic"` is the expected pre-C1 state; it finalizes to
`authored_standard` when `variant_plans.py annotate` runs inside C1. The mapping carries **7
competencies** (C-1.2, C-2.2, C-4.2, C-4.7, C-5.3, C-6.1, C-6.2), all Weight 1 per the TWAU
flattened-CG structure, which is what feeds the assessment constitution's COMPETENCY
DESCRIPTIONS block. Chosen (founder, this session) over ch 4, 6 and 7 on section-to-period
ratio: 6 sections against 15 body units gives the compacts real condensation room, where ch 4's
10 sections against the same 15 leaves almost none — the same criterion S8 applied.

**P5.4 · The three test identities' teaching profiles for class V.** **OPEN — the stage is signed
provisionally.** Not consumed by generation or certification; first needed at C6, which is its
hard stop. Give the three identities *different sections*, and include one duration longer than
40 alongside the class standard so C6's mixed-duration matrix has something real to draw on. Set
up through the app's own first-run / profile flow, never by hand-editing JSON — the setup doubles
as a live check of that flow.

**P5.5 · THE CARRIER — the one-line trace.**

> **rule 8 · item-self-sufficient family · item `period_ref[]` read DIRECTLY off the item (no
> mediating row) · container: a bare flat list, 1:1 with units · plugin method
> `TheWorldAroundUsSubject.assessment_to_view` (item-self-sufficient, stamped directly — its
> comment has cited "Rule 8" since before the campaign) · `genon_assessment` **not needed**,
> `carriers.assessment_items` falls through to `items_by_period_ref` · not in `_NOT_YET`.**

The assessment half of the seam has always been right, which is why this subject was never in
`_NOT_YET` and why S3's `questions`-wrapper defect could not touch it. **The other half was
missing, and it is §4.**

---

## 3. Deviations from the reference, declared

1. **"serve time", not "partition time"** in A1 (the partition engine was retired 2026-07-31).
   Carried by S3, S4, S6, S7, S8.
2. **A9's removal half is N/A** — this file never carried the item-18 prohibition. Carried by
   S4, S7 and S8. Here the by-label prohibition is also purely additive, with no prior
   "none of the above" ban to absorb.
3. **A6 is a CONFIRMATION on the reference's own field.** Unlike every stage since S2, no
   translation was needed: TWAU declares `period_ref[]` exactly as SS does.
4. **The register's illustrative strings are TWAU ones**, and it carries **one extra sentence**
   the reference does not: the schema carve-out for the band's own `minutes` field. That is an
   addition to the reference's wording, declared here because P1 asks for the block "verbatim
   in substance" and this sentence is not in the reference at all.
5. **No new field was invented** to feed the serve engine (founder ruling 2026-08-10):
   `section_anchor` is not added to the period. Asserted absent by the edit script's guards so
   a later pass cannot reintroduce it by drift.

---

## 4. THE FINDING — the LP anchor had no owner, and the gate is post-payment

**What was wrong.** `aruvi_core/genon/carriers.py::unit_anchor` reads `period["section_anchor"]`,
falls back to the plugin's `genon_unit_anchor`, and — on a stage that `has_section_axis` reports
True for — **raises `KeyError`** when neither produces anything. TWAU has a section axis (LP Rule
1) and spells its anchor **`section_ref`**. It implemented no genon hooks at all. So:

- **every TWAU chapter would have failed to compile on its first period**, and
- the failure lands where every carrier failure lands — inside `load_library`'s `except`,
  reported as `FAIL <file>: does not compile` for every file, ending at `STOP: no library on disk
  to certify`, **after** metered STEP 1 and STEP 4 had run. testing.md's P5.5 warning, on a stage
  its `_NOT_YET` inventory could not see.

**Why `_NOT_YET` could not catch it.** `_NOT_YET` tracks the ASSESSMENT half of the seam — how an
item finds its unit. TWAU's assessment half is row 8 and has always worked. This is the LESSON
PLAN half — how a unit finds its section — and there is no inventory for it. The evidence that it
was known and unowned is in the test suite: `test_known_LP_SHAPE_gaps_are_recorded_not_hidden`
carried the line *"TWAU — periods carry `textbook_anchor` / `section_ref`, no `section_anchor`.
TWAU's registry join has no owner yet; **S5 owes it**."* That docstring promised the test would
FAIL when the gap closed. It did, and this is that update.

**How it landed — as a mediation, exactly as the doctrine requires.** Four hooks on
`TheWorldAroundUsSubject`, no new field in any constitution:

| hook | value | why |
|---|---|---|
| `genon_has_section_axis` | `True` | the platform default; the axis is real (Rule 1) |
| `genon_unit_anchor` | `period["section_ref"]`, **verbatim** | the third field name in the seam, after maths·middle's `textbook_segments[].ref` and maths·prep's `section_refs[]` |
| `genon_anchor_field_present` | `False` | `grep -c section_anchor` = 0, so the synthesis mandate must be the `"synthesis": true` boolean, not the reserved token |
| `genon_item_anchor_family` | `"item"` | row 8, declared rather than inferred — so `item_anchor_is_derived` is False and `top_brief_for` does not ask for a synthesis handoff row this stage has no use for |

**`genon_anchor_field_present` is the one that would otherwise have cost money.** Without it
`top_brief_for` writes *"its `section_anchor` is exactly the single word: `synthesis`"* into the
standard canonical's brief — demanding, **at metered STEP 1**, a field this constitution does not
define. The certifier's synthesis gate would then have found no synthesis unit in the library it
had already paid for. This is the identical defect S7 met on maths·middle, on a third field name,
and it is now covered by a test of its own.

**Verified on the real saved shape**, not a fixture invented for the purpose:
`backup/saved_plans/the_world_around_us/v/ch_05_20260531_122055.json` — **9 units over 6
sections, 9 items** (Rule 2's 1:1), every unit anchored, **zero orphans**, every anchor a
byte-identical member of the summary's registry, sections first-appearing in registry order.
`tests/test_genon_carriers.py`: **92 tests with 3 failures → 95, green.** The three failures were
the S5-era "TWAU is still owed" assertions, which is precisely what this step invalidates; they
are replaced by `test_twau_preparatory_declares_it_absent`,
`test_twau_preparatory_is_asked_for_the_BOOLEAN`, and
`test_twau_preparatory_compiles_through_the_mediated_anchor`.

**The standing lesson for S9–S11 (english, all three stages).** P5.5's four-part read covers the
ASSESSMENT half only. **Add a fifth part: where does this stage's period keep its section
anchor, and does `carriers.unit_anchor` find it?** English is the last family owed, its LP is
spine-structured (`section_id` + `spines_taught[]`), and `grep -c section_anchor` in its three LP
constitutions is the two-second check that decides whether three more stages need mediation. Do
it at P-prep, where it is free.

---

## 5. Rule 5's word cap — measured, then widened (LP v1.4)

S8 left a standing rule for the remaining stages: *at P-prep, take every number a constitution
states and check it against the whole class's `sections × canonical_plan.counts` **and** against
any real saved plan for that stage. The corpus check is the one that mattered.* It mattered again.

**The four numbers in this LP, and what the corpus says about each:**

| rule | the number | verdict |
|---|---|---|
| Rule 5 · `section_context` | 10–**15** words | **BREACHED — 14 of 24 real periods above it** |
| Rule 3 · same `dominant_mode` | ≤ 2 consecutive periods | safe — corpus max run is 2; trivially satisfiable with 5 modes over 16 units |
| Rule 8 · time bands | ≥ 3 per period | safe — corpus minimum is 4, and all 24 periods tile their duration exactly (0 mismatches) |
| Rule 4 · activities | *"a type-based rule, not a numerical count cap"* | states in terms that it is not a number |

Rule 1 states **no cap at all** — it permits a section to span multiple consecutive periods
without limit, which is precisely the clause maths·preparatory had to be amended INTO at S8.

**The measurement:**

| plan | periods | `section_context` words | above 15 |
|---|---|---|---|
| ch 1 · III | 7 | 15–26 | 6 |
| ch 7 · IV | 8 | 10–28 | 2 |
| ch 5 · V | 9 | 15–20 | 6 |

**This is the MIRROR of S4's finding, not a repeat of it.** S4 found maths·secondary's lower
bounds too HIGH — live output ran short, `activity_title` 10–13 → 6–13 and `section_context`
10–12 → 6–12 at LP v1.3, paid for with a C3 re-author. TWAU's lower bound is never breached
(min 10, on the boundary once); it is the UPPER bound that is wrong. Widening the top alone is
what the data supports; adding lower-end headroom this stage has never shown a need for would be
inventing a fix.

**Why the field tolerates the length.** `section_context` is a descriptive LABEL — "the specific
objects, phenomena, or tasks this period drew from" — read by the assessment constitution to
ground what the question is about. It is not a pedagogical constraint, and TWAU periods routinely
name several objects at once, which is exactly why the real output sits at 15–28. A cap that
truncates it degrades the assessment's grounding to protect nothing. A sentence went in with the
number so the intent is not left to be inferred: name every object the period actually used, and
where a period draws on several the label runs to the upper end and **that is correct**.

**Both surfaces moved** — the rule and the schema comment. Third stage running where a number
left a residue in the schema (S7 v3.7, S8 v1.3, and this file's own A1 pass earlier today).

**§9: RELAXATION-ONLY.** The edit widens; nothing is tightened and no obligation is created (the
`MUST NOT` count is asserted unchanged at 24 by the edit script). Output authored under the old
text satisfies the new by construction. **No library re-authors** — and none exists for this
stage, which is the entire point of catching it here rather than at C3.

**One caveat, stated rather than hidden.** The three corpus plans date from 2026-05-31 and may
predate the current Rule 5 wording, so they are evidence of *what this generator naturally emits
for this field on this subject* rather than proof of a breach of the rule as written. That is
still the right evidence for the question being asked, and the amendment is relaxation-only, so
being wrong about the provenance costs nothing.

---

## 6. What the C-cycle inherits

- **C1 is unblocked.** P5.5 is closed on both halves, `build_library.py`'s STEP 0 pre-flight
  passes, and the LP anchor now compiles — verified end-to-end on a real chapter, so no metered
  call is at risk.
- **P5.4 is amber and C6 is its hard stop.** Three profiles for class V, different sections, one
  duration longer than 40.
- **C4 pays a debt that has been owed for a month.** MEMORY.md §"AMENDMENTS TO BE TESTED" item 1
  — the `guide.{TYPE}` nesting mandate (TWAU assessment v1.3, 2026-07-10) — was validated
  **synthetically only**: the saved plans were migrated in place and the constitution text has
  never been exercised by a live generation run. Both SS stages have since had one (113 items,
  zero flat placements). **TWAU is the last of the three still owed**, and S5's C4 is where it is
  paid. Check every item nests under exactly its own `question_type` key, with zero flat
  placements of `what_each_option_reveals` / `expected_elements` / `look_for`, and
  `observation_rubric` present on every `performance_task: true` OPEN_TASK.
- **C4 also owes the `Period.approach` check for this stage.** TWAU's `dominant_mode` must arrive
  spelled out — "Hands-on Investigation", never "HI" (`_MODE_FULL` in the plugin; CLAUDE.md §3's
  standard LP display rule (b)). `tests/test_lp_standard.py` asserts exactly this and currently
  **StopIterations** on it, because `data/content/saved_plans/the_world_around_us/{iii,iv,v}/` are
  all EMPTY — the three TWAU plans live under `backup/saved_plans/` only. **Pre-existing, not
  caused by this prep** (english is empty there too), and it resolves the moment C1 installs the
  library. Re-run `tests/test_lp_standard.py` after C1 and expect it to go green.
- **The registry token is PROSE, and that is C5's sharpest risk on this stage.** Six
  natural-language titles, not codes. C5's checks 3 and 4 are string comparison, so read the
  anchors against `sections[].title` character by character — a dropped subtitle or a straightened
  em dash is a registry miss the choice set reads as an uncovered section. The pre-campaign
  chapter passes this cleanly, which is the baseline to hold.
- **Rule 2 of the assessment is 1:1** — exactly one item per unit, total items = total periods.
  That makes C9 unusually cheap to check on this stage (a count comparison), and unusually
  unforgiving: a single missing item is visible as arithmetic.
- **A C13 debt, TWAU's analogue of the `number_line:` one.** Rule 10 defaults `visual_stimulus`
  to `""` and introduces no new rendering branch, permitting the existing pipe-table convention
  "rarely and not expected". Confirm at C13 that a TWAU item which *does* take a pipe table
  renders on both surfaces. A permitted format no stage has exercised is the same failure mode as
  a permitted format with no branch.
- **The synthesis unit will carry `"synthesis": true`, not a token.** Anything downstream that
  looks for the reserved string on this stage is looking in a field that does not exist; read
  `carriers.is_synthesis`.
