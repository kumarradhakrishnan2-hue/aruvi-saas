# S8 · mathematics · preparatory — stage preparation sign-off

**Date:** 2026-08-11 · **Template:** `docs/testing.md` v2.9
**Drawn class:** III (seed `mathematics|preparatory|2026-08-02`) · **standard duration:** 40 min
**Reference pair:** SS·secondary LP v1.10 · assessment v1.7, via the mathematics·middle
v3.4 / v3.3 adaptation (same subject vocabulary, one stage up, **and the same 8-rule
family**)
**Landed pair:** mathematics·preparatory LP **v1.1 → v1.3** (v1.2 the carry-forward, v1.3 the Rules 1–2 alignment) · assessment **v1.2 → v1.3**
**Pilot chapter:** III · ch 5 · *Fun with Shapes* (8 sections · rec 14 · floor 8 · counts
[14, 11, 8])

Written by Claude. Status in the tracker is set by Kumar.

---

## 0. The headline — S8 is CLEAR to enter C1, and it is the cheapest stage prep of the campaign

P1–P5.5 are complete. Nothing is owed and no gate is carried into the C-cycle. **P5.4 (the
three test identities' teaching profiles for class III) is open by design** — it needs the
live app, it is not consumed by generation or certification, and the founder ruling of
2026-08-02 permits a provisional signature with it open. C6 is its hard stop.

**Two facts made this stage cheap, and both were paid for at S7.** Preparatory is
mathematics' *third* stage and the second in the period-field carrier family, so the P1/P2
amendment set ported almost mechanically from middle's own adaptation. And S7 wrote both
halves of the seam this stage needed — `items_by_period_field` (the family helper) and
`genon_unit_anchor`'s preparatory branch — leaving them deliberately unexercised with a note
saying so. **P5.5 was therefore three lines of delegation plus a deletion**, and the S7 note
turned out to be exactly right about where the work would land.

**The one real finding is §4, and it went to a second round.** Rule 2's two-adjacent-periods
cap is the same numeric limit that cost S7 a re-author at LP v3.6. This note first recommended
leaving it, on the grounds that the pilot dodges the binding case; the founder challenged that
and the data broke it — **the real prep corpus already exceeds the cap on a plan with slack**
(maths IV ch 8 runs one section across three periods). Rules 1 and 2 are now aligned with
middle and secondary at **LP v1.3**, free, before anything is authored.

---

## 1. Per-item verification (testing.md §3, the Claude sign-off)

| Item | Verdict | Evidence |
|---|---|---|
| **A1** — one standard row | **PRESENT** | INPUTS 4 was `"Period schedule: {duration, count} rows; total = B."` — one line, which licensed exactly the mixed-duration plan the variant engine cannot use. Now: *"exactly ONE row {duration_minutes, count}: the class-standard duration (40 min for classes up to VII, 45 for VIII, 50 for IX–X — the master-plan calibration bands, not NCF's flat 40) × the period count; total = B. Teacher timetable variation never reaches generation; it is handled downstream at serve time."* Class III's standard is **40 min**, matching `master_plan.json`'s `mathematics\|III` row. **Declared deviation:** "serve time", not the reference's "partition time" — the partition engine was retired 2026-07-31. Same correction S3, S4, S6 and S7 made. |
| **A5 + A7** — register as ONE block | **PRESENT, verbatim in substance** | One block after VOCABULARY in the v1.10 **three-ban** re-cut. This stage is *not* S6's two-ban exception: prep-maths units anchor to textbook sections (`section_refs[]`) and travel between plans, so ban 2 binds in full. Bound at **Rule 6** (band narration) and at the **`teacher_notes`** schema comment by reference, never as scattered prohibitions. **Declared deviation:** illustrative strings are prep-maths ones — "a quick count round the class", "an unhurried making activity", "now that we have weighed everything", "The children have grouped in tens to count large collections, …". **Two consequential edits, both the same two S7 made:** VOCABULARY was *teaching* the forward reference ban 2 forbids (its cross-reference examples were literally `"the previous unit"`, `"this unit"`) so the examples are dropped and "session" joins the excluded register; and the `teacher_notes` comment asked for positional continuity ("Recap prior unit") and now asks for content-named continuity, citing ban 2. |
| **A6** — item anchoring | **CONFIRMED, not amended; one integrity block added** | Items already carry `section_ref`, copied verbatim from the LP handoff entry (LP Rule 8 emits it; assessment Rule 2 consumes it). Preparatory mathematics is the **PERIOD-FIELD** family, **8-rule row 5**: the platform resolves `section_ref` ("S3") against each period's own **`section_refs[]`** — **not** middle's `textbook_segments[].ref` (row 4) and **not** secondary's handoff (row 6) — with no `coverage_handoff` in the path and no LO. The new ANCHORING block records four things: `section_ref` IS the anchor and is pass-through; a section spanning several units anchors at the **LAST** of them (founder 2026-08-05); `period_ref` / `period_number` / any unit number MUST NOT be emitted, because declaring the link would freeze an arrangement the platform varies per teacher; and `task_id` is not an anchor in this sense (Rule 8) — it seeds the exercise companion only. Same shape as science·secondary v1.2, science·middle v1.4 and maths·middle v3.3: derive the link, never demand it. `grep -c phase_ref` = 0 in both files. |
| **A9** — option order | **PRESENT as two lines; the removal is N/A, and no arrangement sentence** | **REMOVAL — N/A.** This file never carried the MEMORY-item-18 position prohibition; testing.md P2 names four files that do (SS + Science, middle and secondary) and this is not one. Confirmed by grep: `consecutive`, `same label`, `vary in position` all **0**. Nothing was struck. **ADDED**, v1.7 wording, in Rule 9's MCQ block: the "order carries no meaning and is not yours to set" mandate, and the by-label option-reference prohibition ("both A and B", "none of the above", "all of the above"). This file carried no prior "none of the above" ban, so the addition is purely additive. **NOT re-added:** `alphabetically` · `never led with` · `first word at which they differ` all assert **0** in the edit script's guards. |
| **P3** — Group B conversion | **APPLIED — real, not N/A** | Third stage where this was not N/A (after S6 and S7). Array and key both renamed, with Rule 5, Rule 6's heading (`PHASE NARRATION` → `BAND NARRATION`) and prose, Rule 7 and the schema following. **No `band_id`** in the target shape. `grep -c 'phases\['` = 0, `'"phases"'` = 0, `band_id` = 0, `time_bands` = 2, `"activity": string` present. This leaves the existing preparatory saved-plan corpus on the old `phases` shape; the plugin's tolerant read still covers display (`subject.py:211-219` reads **both keys, newest first**, and says why). |
| **P4** — history to the sidecar | **DONE** | `CHANGELOG.md` created beside both constitutions (neither had one). Neither carried an in-document version-history block, so nothing had to be lifted out. The **assessment footer was two bumps stale** ("Version 1.1" after the v1.2 distractors pass) and is corrected to 1.3; the LP footer likewise to 1.2. The assessment sidecar also back-fills a **v1.2 entry** for the S7 collateral bump, which had no record anywhere. |
| **Rules 1 + 2** — alignment (v1.3) | **AMENDED, on founder challenge** | Not part of the carry-forward set, and raised here because §4's measurement said it should be. Both numeric caps removed and replaced with middle's post-v3.8 wording; contiguity sentence and secondary's two prohibitions added; coverage mandate moved from Rule 1 into Rule 2. Middle's **end state** was ported, not its v3.6 text (the SURPLUS bullet v3.8 deleted never arrives), and its two `section_goal` paragraphs were left behind because preparatory has no per-period goal. Three residues of the removed cap were fixed with it — the DESIGN PRINCIPLE, Rule 2A's stale cross-reference, and the **schema comment**, which is the surface the model copies from. Full reasoning in §4. |
| **Cancelled amendments A2/A3/A4, X3** | **ABSENT** | None introduced. Asserted by guard: `role_handoff`, `unit_handoff`, `band_ref`, "role weighting" all 0 in both files. |
| **V-rules in a constitution** | **NONE** | No section registry, no verbatim-anchor mandate, no first-visit-order rule, no closing-synthesis mandate, no per-variant assessment rule, no INPUTS acknowledgment, no precedence line — asserted by guard ("section registry", "synthesis unit", "reserved token" all 0). Worth stating because the synthesis mandate sits in visible tension with LP **Rule 1** (*"Every section in the summary MUST appear in at least one period's `section_refs`. Dropping a section is FORBIDDEN"*) and with Rule 1's *"one — or at most two adjacent — sections"* cap, since a synthesis unit anchors to no section at all and middle's equivalent named five. The brief overrides, the constitution is deliberately left alone, and `carriers.is_synthesis` + the certifier's token exemption are where that is handled. Identical to the tension S7 recorded against middle's Rules 1 and 2. |

**One repair rode along, and it is recorded as a repair rather than an amendment.** The
assessment schema's `what_each_option_reveals` example read `{ "A", "C", "C", "D" }` — four
keys, `"C"` twice, `"B"` missing — and contradicted its own prose. S7's
`apply_s7_distractors_only.py` (2026-08-10) rewrote the FIRST line of the two-line example
in this file and left the second; prep was collateral to a middle amendment and nobody read
the result. It now shows three keys and says why.

---

## 2. P5 — stage inputs

**P5.1 · The floor.** Accepted at the standing ratio `round(0.6 × recommended_periods)`, no
override. For ch 5 that is `round(0.6 × 14) = round(8.4) = 8`, matching
`floor_periods_at_standard` on the row. Equal dispersion over [8, 14]: A−C = 6 ≥ 4, so counts
are `{A, ⌈(A+C)/2⌉, C}` = **[14, 11, 8]** — three canonicals, three authoring runs.

**P5.2 · The section registry.** Preparatory mathematics' section model is **obvious and
needs no definition** — the summary carries an explicit `sections[]` spine of
`{ref, title, prose_summary, tasks[]}`, and the period's `section_refs[]` reproduces the ref
verbatim (LP Rule 1: *"copied from summary sections[].ref"*). For ch 5 the registry is the
eight refs in summary order:

```
S1 Shapes in rangoli · S2 Shapes from boxes — cuboid faces · S3 Rectangles — properties
and drawing · S4 Same to Same — squares vs rectangles · S5 Square corners — right angles ·
S6 Triangles — three sides, three corners · S7 Circus with circles — circle and centre ·
S8 Comparing and composing shapes
```

**The token is the bare code `"S1"`, not `"section 5.1"`** — that is what the summary carries
and what real saved plans emit, and the mediated anchor returns it **verbatim** rather than
normalising it. This is the one place preparatory differs from middle in kind rather than
degree: middle's codes are chapter-prefixed (`"section 7.1"`), prep's are chapter-local
(`"S1"`). `link_resolver.norm_code` strips the word "section" and collapses spacing, so
`"S1"` → `"s1"` on both sides and there is no collision with middle's forms. Consistency
across the library is guaranteed by construction: `standard_registry()` reads the registry
off the AUTHORED standard canonical and `briefs_for()` prints it verbatim into each compact's
brief.

**P5.3 · The pilot chapter.** `mathematics|III` ch 5 *Fun with Shapes*. Summary and mapping
both on disk (`data/content/chapters/mathematics/iii/{summaries,mappings}/ch_05_*.json`),
`placeholder: false`, `canonical_plan` present. The row:

```json
{"chapter": 5, "title": "Fun with Shapes", "weight": 13, "exact_share": 14.15,
 "recommended_periods": 14, "canonical_minutes": 560, "floor_minutes": 336.0,
 "floor_periods_at_standard": 8, "canonical_periods": [14, 11, 8], "placeholder": false,
 "canonical_plan": {"counts": [14, 11, 8], "provisional": true, "basis": "arithmetic",
                    "registry_sections": null, "authored": []}}
```

`provisional: true` / `basis: "arithmetic"` is the expected pre-C1 state; it finalizes to
`authored_standard` when `variant_plans.py annotate` runs inside C1. Chosen (founder, this
session) over ch 9 and ch 7 on section-to-period ratio: 8 sections against 14 periods gives
the compacts real condensation room, where ch 7's 13 sections against 14 periods leaves
almost none.

**P5.4 · The three test identities' teaching profiles for class III.** **OPEN — the stage is
signed provisionally.** Not consumed by generation or certification; first needed at C6, which
is its hard stop. Give the three identities *different sections*, and include one duration
longer than 40 alongside the class standard so C6's mixed-duration matrix has something real
to draw on. Set up through the app's own first-run / profile flow, never by hand-editing JSON
— the setup doubles as a live check of that flow.

**P5.5 · THE CARRIER — the one-line trace.**

> **rule 5 · period-field family · item `section_ref` ("S3") → period `section_refs[]` ·
> container: a list of A/B/C/D INTENT groups each carrying `items[]` · plugin method
> `MathematicsSubject._middle_assess` (its `prep` branch, shipping for the app since before
> the campaign) · `genon_assessment` present as of 2026-08-11 · not in `_NOT_YET`.**

Landed as a **delegation**, exactly as the doctrine requires. Row 5 was already specified in
the 8-rule table and `_middle_assess`'s preparatory branch already ran it for the app; only
genon's door was shut. Three lines opened it — `items_by_period_field(result, items=flat,
item_key="section_ref", extract=lambda p: p.get("section_refs"))` — and the
`("mathematics", "preparatory")` entry was deleted from `_NOT_YET`. **Mathematics is now
carried at all three stages**; the four remaining `_NOT_YET` entries are english's three
stages (rows 7, owed by S9–S11).

**The stage discriminator is the load-bearing part, and it now carries weight in both
directions.** `genon_assessment` receives only `result`, so it cannot read the grade (the S4
trap: a grade read there is `None` on the very call the carrier makes). Middle and preparatory
share a container shape — a list of dicts carrying `items[]` — and are separated the way the
prototype's `_regroup_middle_maths_by_section` separates them: **middle items carry `goal`,
preparatory items carry `intent`.** Before this session the `intent` branch raised; it now
returns row 5's join, and the no-`goal`-and-no-`intent` case still refuses rather than
guessing, with a message naming both fields and both rows.

**Verified on the real saved shape**, not on a fixture invented for the purpose:
`backup/saved_plans/mathematics/iii/ch_06_20260603_180712.json` — 9 periods over S1–S11, 26
items in four intent groups. All 26 resolve, **zero orphans**, every `unit_ref` a singleton,
and every anchor equal to the independently computed *"last period that lists this section"*
(S3 spans periods 2–3 → anchors at 3; S8 spans 6–7 → anchors at 7). Raw fields survive the
seam (`teacher_guide`, `visual_stimulus`, `exercise`, `options`). `genon_unit_anchor`'s
preparatory branch — written unexercised at S7 — is exercised for the first time here and
returns `"S1"` and `"S2 / S3"` verbatim, joined with the V2 multi-section joiner.

`tests/test_genon_carriers.py`: **82 tests with 4 failures → 92 tests, green.** The four
failures were the S7-era assertions that preparatory is still owed, which is precisely what
this step invalidates; they are replaced by a `TestMathematicsPreparatoryLanded` class of
eleven, plus a middle-side test that a middle file is not diverted onto prep's field.

---

## 3. Deviations from the reference, declared

1. **"serve time", not "partition time"** in A1 (the partition engine was retired
   2026-07-31). Carried by S3, S4, S6, S7.
2. **A9's removal half is N/A** — this file never carried the item-18 prohibition. Carried by
   S4 and S7.
3. **A6 is the DERIVED period-field anchor**, not the reference's declared `period_ref`
   field — and specifically **`section_refs[]`**, which is this stage's field and no other's.
4. **The register's illustrative strings are prep-maths ones.** The three bans and the closing
   backward-continuity rule are verbatim in substance.
5. **No new field was invented** to feed the serve engine (founder ruling 2026-08-10):
   `section_anchor` is not added to the period and no `period_number` is added anywhere. Both
   are asserted absent by the edit script's guards so a later pass cannot reintroduce them by
   drift.

---

## 4. RESOLVED — Rules 1 and 2 aligned with middle and secondary (LP v1.3)

**This section opened as a recommendation to leave both numeric caps alone. The founder
challenged it, the data did not support it, and the amendment landed.** The reasoning is
preserved here because the way the first read went wrong is the reusable part.

**What the first read got right.** Preparatory carries two numeric caps — Rule 1's *"one — or
at most two adjacent — sections"* and Rule 2's *"a heavy section MAY split across two adjacent
periods"* — and Rule 2's is arithmetically unsatisfiable when **body units > 2 × sections**,
which is true of **4 of this class's 14 chapters**:

| ch | title | sections | counts | body | cap = 2×S | |
|---|---|---|---|---|---|---|
| 1 | What's in a Name? | 4 | [7, 4] | 6 | 8 | slack |
| 2 | Toy Joy | 4 | [8, 5] | 7 | 8 | slack |
| **3** | **Double Century** | **5** | **[14, 11, 8]** | **13** | **10** | **BINDS** |
| 4 | Vacation with My Nani Maa | 6 | [11, 9, 7] | 10 | 12 | slack |
| **5** | **Fun with Shapes (PILOT)** | **8** | **[14, 11, 8]** | **13** | **16** | **slack** |
| 6 | House of Hundreds - I | 11 | [13, 11, 8] | 12 | 22 | slack |
| 7 | Raksha Bandhan | 13 | [14, 11, 8] | 13 | 26 | slack |
| **8** | **Fair Share** | **4** | **[10, 8, 6]** | **9** | **8** | **BINDS** |
| 9 | House of Hundreds - II | 9 | [13, 11, 8] | 12 | 18 | slack |
| **10** | **Fun at Class Party!** | **6** | **[14, 11, 8]** | **13** | **12** | **BINDS** |
| 11 | Filling and Lifting | 5 | [10, 8, 6] | 9 | 10 | slack |
| 12 | Give and Take | 8 | [8, 5] | 7 | 16 | slack |
| **13** | **Time Goes On** | **6** | **[14, 11, 8]** | **13** | **12** | **BINDS** |
| 14 | The Surajkund Fair | 9 | [10, 8, 6] | 9 | 18 | slack |

**The pilot dodges that case** (ch 5: 13 body against a cap of 16).

**What the first read got wrong — three things, and the first is decisive.**

1. **It treated the arithmetic case as the only failure case.** It is not. The real prep
   corpus already breaks the cap *with slack in hand*:
   `backup/saved_plans/mathematics/iv/ch_08_*.json` runs section S5 across periods **6, 7 and
   8** on a plan of 9 body units against a cap of 12. Nothing forced it; the content did. The
   cap breaks whenever a heavy section warrants a third period — a property of the section,
   not of the budget — so the pilot dodging the arithmetic buys nothing at all.
2. **Its pedagogical premise was half-wrong.** "Prep sections are small and task-dense" holds
   for the median (3 tasks, mean 4.2 across class III's 98 sections) and fails at the tail:
   max 13, and **nine sections above eight tasks**. Those are exactly the sections a two-period
   cap mis-sizes. The argument was true of the sections that were never the problem.
3. **It missed that preparatory had become the sole outlier in the maths family.** Secondary
   never had the cap; middle's went at v3.6. S7's own changelog named the tell — *"the only one
   of the three that named a number"* — and after v3.6 that tell pointed here.

**And Rule 1's cap was never a risk — it was a certainty.** The platform brief mandates a
closing whole-chapter synthesis unit; *"one or at most two adjacent sections"* cannot describe
one. S7 met exactly this at C3 (ARV-D-094) and had to amend mid-cycle. Knowing that and
authoring anyway would have been paying twice for the same finding.

**Landed as LP v1.2 → v1.3** — Rule 1 widened plus the contiguity sentence; Rule 2 renamed
FULL-SECTION COVERAGE, cap removed, emphasis-follows-substance and secondary's two prohibitions
added, the coverage mandate moved in from Rule 1. **Middle's END STATE (v3.8) was ported, not
its v3.6 text**: v3.6's SURPLUS bullet was deleted at v3.8 as the cause of the hoarding it
tried to cure, so porting it verbatim would have imported a clause its own stage had already
retired. Middle's two `section_goal` paragraphs were also left behind — preparatory has no
per-period goal, and inventing one is the thing the 2026-08-10 ruling forbids.

**Three residues, and they are the transferable lesson of this amendment: grep the NUMBER, not
the rule.** Removing a cap from Rule 1 left it standing in the DESIGN PRINCIPLE (*"each period
anchors to one or two adjacent sections"*), in Rule 2A's stale cross-reference (*"Before
bin-packing"*), and — worst — **in the schema comment**, `"section_refs": [...] // 1–2, e.g.
["S3"]`, which is the surface the model actually copies from. S7's v3.7 hit the identical
schema residue in middle. All three are fixed and asserted.

**§9: a full constitution change** — two relaxations against **three new obligations** (the
contiguity sentence plus the two prohibitions; the edit script asserts the count exactly, and
caught my own miscount of two on its first run). It costs **nothing**, because no library for
this stage exists. S7 paid ~₹106 and a C1–C3 re-run for the same conclusion.

**The standing rule this leaves for S9–S11:** at P-prep, take every number a constitution
states and check it against the whole class's `sections × canonical_plan.counts` **and** against
any real saved plan for that stage. The corpus check is the one that mattered here — the
arithmetic sweep alone would have let this through.

## 5. What the C-cycle inherits

- **C1 is unblocked.** P5.5 is closed, so `build_library.py`'s STEP 0 pre-flight will pass
  and no metered call is at risk from a missing carrier.
- **P5.4 is amber and C6 is its hard stop.** Three profiles for class III, different sections,
  one longer duration.
- **The `number_line:` renderer debt is now owed twice.** Rule 7 permits a `number_line:`
  stimulus at both prep and middle and prohibits SVG at prep. Confirm at C13 that both
  renderers (screen and PDF) still carry a `number_line:` detection branch — a permitted
  format with no branch is a known failure mode.
- **The saved-plan corpus for this stage is still on `phases`,** not `time_bands`. Display is
  covered by the plugin's both-keys read; anything new must emit `time_bands`.
- **§4's table is now history, not a warning.** Rules 1 and 2 are aligned at LP v1.3, so the
  four binding chapters (3, 8, 10, 13) are no longer constrained by a rule they could not
  satisfy. What survives is the *check*: at C3, read the top canonical against Rule 1's
  contiguity sentence specifically — S7's revisit defect is the failure this rule now forbids,
  and nothing tests it deterministically yet.
- **A certifier check is owed and is free** (inherited from S7, still unbuilt): no section may
  appear in two non-contiguous runs. Rule 1 has forbidden interleaving at both stages and
  nothing tests it, which is why three revisits reached a paid artefact at S7 and were found
  by eye.
