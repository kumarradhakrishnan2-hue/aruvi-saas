# S11 · english · secondary — stage preparation sign-off

**Date:** 2026-08-12 · **Template:** `docs/testing.md` v2.9
**Drawn class:** IX (the only eligible class; seed `english|secondary|2026-08-02`) ·
**standard duration:** 50 min
**Reference pair:** SS·secondary LP v1.10 · assessment v1.7, read through the
mathematics middle/preparatory adaptation — english is the THIRD stage-family in the
**period-field** carrier family, so the anchoring block ports from rows 4/5 changing only
the join key and the code vocabulary
**Landed pair:** english·secondary LP **v1.1 → v1.2** · assessment **v1.3 → v1.4**
**Pilot chapter:** IX · ch 7 · *Vitamin-M* (1 main_section · 6 spines · 23 tasks · rec 17 ·
floor 10 · counts **[17, 14, 10]**)

Written by Claude. Status in the tracker is set by Kumar.

---

## 0. The headline — S11 is CLEAR to enter C1, and it found the largest structural
## question of any prep since S6

P1–P5.5 are complete. Nothing is owed and **no gate is carried into the C-cycle**.

**P5.4 closed the same day** (2026-08-12): the three identities' class-IX English profiles were
set up through the app's own first-run flow, so **S11 enters its C-cycle with a clean P5** — the
fourth stage to do so, after S6, S8 and S5. Details in §2.

Three things make this stage unlike the seven before it, and all three were found by reading
rather than by spending:

1. **English's section axis is not a section.** Post-split every english chapter is ONE
   `main_section`, so `section_id` is a constant and looks like no axis at all. The axis is
   the **(section × spine) CELL** the constitution's own DESIGN PRINCIPLE names — "period
   bin-packing is across (section × spine) cells, NOT across spines alone" — and the spines
   are walked in strict, never-re-sequenced textbook order (Rule 1). That is a real
   first-visit axis, so a prefix of a canonical is a valid plan and this stage stays at
   **UNIT granularity**; it does not join science·middle's plan-granularity exception. §2's
   P5.2 records the registry.
2. **The LP legally dropped spines, and the corpus proves it did.** Rule 2 STEP 3 licensed a
   short plan to stop when a section's periods ran out. `backup/saved_plans/english/ix/
   ch_12_*.json` (4 periods) carries **no `beyond_text` contribution at all**. Under
   architecture v2.0 a chapter's canonicals must share ONE registry, so that licence breaks
   the Xth-unit choice set before serve ever runs. Amended at LP v1.2, free. §4.
3. **The carrier is the first PAIR key in the 8-rule table, and delegating it naively would
   have silently undone a fix the app already carries.** §3.

---

## 1. Per-item verification (testing.md §3, the Claude sign-off)

| Item | Verdict | Evidence |
|---|---|---|
| **A1** — one standard row | **PRESENT** | INPUTS 3 was `"{ period_duration_minutes, period_count }, where period_count = B is supplied at generation time (allocation tab suggests; user may override)"` — which licensed exactly the mixed-duration, teacher-chosen plan the variant engine cannot use. Now: *"exactly ONE row { period_duration_minutes, period_count }: the class-standard duration (40 min for classes up to VII, 45 for VIII, 50 for IX–X — the master-plan calibration bands, not NCF's flat 40) × the period count … handled downstream at serve time."* Class IX's standard is **50 min**, matching `master_plan.json`'s `english\|IX` row. **Declared deviation:** "serve time", not the reference's "partition time" — carried by S3, S4, S6, S7, S8. |
| **A5 + A7** — register as ONE block | **PRESENT, verbatim in substance** | One block after VOCABULARY in the v1.10 **three-ban** re-cut. This stage is *not* S6's two-ban exception: english units anchor to cells and travel between plans under the X−1+1 fill, so ban 2 binds in full. Bound to **Rule 9** (band narration) and `teacher_notes` by reference, never as scattered prohibitions. **Declared deviation:** illustrative strings are english ones — "a quick paired exchange", "an unhurried reading aloud", "having now heard the whole play", "Having read the terrace scene aloud, …". **Two consequential edits, the same two S7 and S8 had to make:** VOCABULARY was *teaching* the positional cross-reference (its examples were literally `"the previous unit"`, `"this unit"`) and now names the CONTENT built on, with "session" joining the excluded register; and the `teacher_notes` schema comment asked for *"transition from prior / **preview next**"* — the forward half being the exact contradiction testing.md P1 names for this constitution family (it names english·middle's; secondary carries the same clause in a different form). |
| **A6** — item anchoring | **CONFIRMED in substance, AMENDED in form — new Rule 8A** | The two fields that carry the anchor (`source_section_id`, `source_spine`) were already mandated by Rule 8, but nothing said they WERE the anchor, nothing said what the platform does with them, and nothing forbade a unit number beside them. Rule 8A records: the CELL is the anchor and there is no third field to emit; the platform resolves it against each period's `section_id` + `spines_taught[]`; a cell taught across several units anchors at the **LAST** of them (founder 2026-08-05); and `period_ref` / `period_number` / `unit_ref` MUST NOT be emitted. Same shape as science·secondary v1.2, science·middle v1.4, maths·middle v3.3, maths·prep v1.3 — derive the link, never demand it. `grep -c phase_ref` = 0 in both files. |
| **A9** — option order | **PRESENT as two lines; the removal is N/A, and no arrangement sentence** | **REMOVAL — N/A.** This file never carried the MEMORY-item-18 position prohibition; testing.md P2 names the four files that do (SS + Science, middle and secondary) and this is not one. Confirmed by grep: `consecutive`, `same label`, `vary in position` all **0**. Nothing was struck. **ADDED**, v1.7 wording, in **Rule 4** where the MCQ semantics live (not Rule 5's answer-layer bullet list, which is an indented block the lines would have read oddly inside): the "order carries no meaning and is not yours to set" mandate, and the by-label option-reference prohibition ("both A and B", "none of the above", "all of the above", "either B or C"). No prior "none of the above" ban existed here, so the addition is purely additive. **NOT re-added:** `alphabetically` · `never led with` · `first word at which they differ` all assert **0** in the edit script's guards. |
| **P3** — Group B conversion | **APPLIED — real, not N/A** | Fourth stage where this was not N/A (after S6, S7, S8). Array and key both renamed, with Rule 5, Rule 9's heading (`PHASE NARRATION` → `BAND NARRATION`) and every prose reference following — including Rule 2A's "explicit timed phase", which is the one place the word carried pedagogical weight. **No `band_id`.** `grep -c 'phases\['` = 0, `'"phases"'` = 0, `band_id` = 0, `time_bands` = 2, `"activity": string` present. This leaves the whole english saved-plan corpus on the old shape, so the english plugin was given the same both-keys-newest-first read mathematics has (`english/subject.py::_bands`) — **without it every existing english plan would have rendered with no timed spine the moment a new one arrived**, which is a display regression P3 does not otherwise announce. |
| **P4** — history to the sidecar | **DONE** | The LP had a `CHANGELOG.md` (created 2026-08-11 by the cross-stage curly-quote pass) and gains a v1.2 entry. The assessment had **none** and gains one, back-filling v1.0 (the fork from middle v3.1) and v1.1 (Rule 4's "NAME THE REFERENCED WORD", MEMORY item 10) from the only surviving record. **v1.2 and v1.3 are undocumented and are recorded as a gap, not guessed at** — no sidecar, no in-document history, MEMORY's inventory stops at v1.1, and `data/` is git-ignored. Third stage running where a version moved without a record. Neither constitution carried an in-document version-history block. **Both footers were already correct** (the first stage in four where they had not drifted) and now track the new headers. |
| **Rule 2 STEP 3** — full spine coverage (v1.2) | **AMENDED, founder call** | Not part of the carry-forward set; raised here because §4's measurement said it must be. Covered in full in §4. |
| **Rule 1** — the closing-unit exception (v1.2) | **AMENDED, and it was a certainty not a risk** | "Exactly ONE main_section and one or two ADJACENT spines" cannot describe a whole-chapter closing unit, which the platform brief mandates of the standard canonical. S8 recorded this as the lesson ("Rule 1's cap was never a risk, it was a certainty" — S7 met it at C3 as ARV-D-094 and amended mid-cycle). Applied here for free, before authoring. The constitution still names no V-rule: the exception describes a closing unit's SHAPE and never mandates one. |
| **`task_brief` ≤ 12 → ≤ 18 words** (v1.2) | **AMENDED, on measurement** | Rule 9 mandates the brief carry `"<Subheading> (p.NN): <plain brief>"`; the locator eats 3–4 words of the 12. Measured on the real IX corpus (`ch_11`, `ch_12`): **17 of 28** briefs exceed 12 words as authored, max 19; **27 of 28** fit 18. Founder chose the single whole-string cap over capping only the text after the locator, so there is one number and it governs what is rendered. |
| **`section_context` 10–15 → 10–18 words** (v1.2) | **AMENDED, on measurement** | 3 of 11 IX contributions run 16, 16 and 17. Lower bound kept — the field is useless at two words. |
| **Rule 2 STEP 1** — the 50-minute budget (v1.2) | **ADDED** | The task-budget ceiling named a 40-min and a 60-min period but **not the 50-min class standard this stage authors at** — the one duration A1 now fixes. It reads ≤ 3–4 tasks, interpolated from the same per-spine rates the rule already states. |
| **Cancelled amendments A2/A3/A4, X3** | **ABSENT** | None introduced. Asserted by guard: `role_handoff`, `unit_handoff`, `band_ref`, "role weighting", `phase_ref` all 0 in both files. |
| **V-rules in a constitution** | **NONE** | No section registry, no verbatim-anchor mandate, no first-visit-order rule, no closing-synthesis mandate, no per-variant assessment rule, no INPUTS acknowledgment, no precedence line — asserted by guard ("section registry", "synthesis unit", "reserved token" all 0). Worth stating because the closing-unit exception at Rule 1 sits one sentence away from the brief's synthesis mandate and deliberately does not become it. |

---

## 2. P5 — stage inputs

**P5.1 · The floor.** Accepted at the standing ratio `round(0.6 × recommended_periods)`, no
override **for the pilot**. For ch 7 that is `round(0.6 × 17) = round(10.2) = 10`, matching
`floor_periods_at_standard` on the row. Equal dispersion over [10, 17]: A−C = 7 ≥ 4, so counts
are `{A, ⌈(A+C)/2⌉, C}` = **[17, 14, 10]** — three canonicals, three authoring runs.

> **ONE OVERRIDE IS OWED ELSEWHERE IN THE CLASS, and it is a consequence of §4.** Full spine
> coverage has an arithmetic minimum: VocGram occupies a period alone (Rule 2 STEP 4) and the
> other five spines take at most two adjacent per period, so a six-spine chapter needs
> **≥ 4 periods**. Sweeping the class's 16 chapters against their `canonical_plan.counts`,
> exactly one floor falls below it: **ch 12 *A Friend Found in Music*, counts [5, 3]**. Its
> floor must be raised to 4 (dispersion over [4, 5] gives A−C = 1 < 4, so counts become
> **[5, 4]**) with this note as the recorded reason. Not applied to `master_plan.json` now,
> deliberately: ch 12 is not the pilot, `master_plan.py` regeneration wipes these rows
> (the runbook pair at testing.md 0.3), and the override belongs immediately before ch 12 is
> authored at pre-warm. **Recorded here so it is not met as a surprise then.**

**P5.2 · THE SECTION REGISTRY — the step testing.md names english explicitly for.**

English's section model is the one the template flagged as non-obvious, and this is the
definition it asked for.

- **The registry member is the (section × spine) CELL**, not the main_section and not the
  spine. The constitution's DESIGN PRINCIPLE already says so — *"Period bin-packing is across
  (section × spine) cells, NOT across spines alone"* — and Rule 1 makes the order strict:
  main_sections in textbook order, spines within each in **on-page order**, never reordered,
  interleaved or re-sequenced. That is precisely V2's first-visit-order requirement, satisfied
  by the constitution rather than by a new rule.
- **The token is `"<section_id>|<spine_key>"`** — e.g. `A|reading_for_comprehension` — built
  from the two authored fields, verbatim, and joined for a multi-cell unit with the V2 joiner:
  `A|listening / A|speaking`. Both halves are closed vocabulary (the six spine keys are fixed
  by the constitution; the section id comes from the summary's inventory), so the registry is
  **stable across a chapter's canonicals by construction** — which is the property the
  Xth-unit choice set depends on and the reason not to use the on-page `section_name`, whose
  value for ch 7's reading cell is the 9-word merged string *"Reflect and Respond + Reading
  for Meaning + Check Your Understanding + Critical Reflection"*.
- **Why the pair and not the spine alone:** the constitution permits 1–3 main_sections, and
  the middle-stage fixture (`tests/fixtures/english_vii_ch01_saved.json`) is a live example —
  sections A, B and C each teach Reading, and joining on the spine alone collapses all three
  onto one cell. Asserted as a test.
- **The registry for the pilot**, in first-visit order, is these six:

```
1. A|reading_for_comprehension   (Reflect and Respond + Reading for Meaning + …, 10 tasks)
2. A|vocabulary_grammar          (Vocabulary and Structures in Context, 6 tasks)
3. A|listening                   (Listen and Respond, 1 task)
4. A|speaking                    (Speaking Activity, 2 tasks)
5. A|writing                     (Writing Task, 1 task)
6. A|beyond_text                 (Learning Beyond the Text, 3 tasks)
```

- **This is the campaign's THINNEST registry — six members against seventeen units** (2.8
  units per cell, where SS·IX ch 3 runs about two). It is not a defect, but it changes what
  C8 has to look at: most units are not first-exposure, so the choice set's "unit that FIRST
  deals the next-due cell M" resolves to a small number of candidates, and the borrowed unit
  will usually be the opening unit of a cell. Flagged in §5.
- **Coverage feasibility at all three counts**, checked because §4 now makes it mandatory:
  the tail cells carry 1–3 tasks each and cannot fill more than a unit apiece, so the spread
  is `RFC ~10 · VG ~3 · listening 1 · speaking 1 · writing 1 · beyond 1` at **17**, and
  `RFC ~4 · VG ~2 · four tail cells 1 each` at the floor of **10** — feasible, and tight at
  the floor rather than impossible. At 4 periods it would be exactly saturated, which is why
  the minimum is 4 and why ch 12 needs its override.

**P5.3 · The pilot chapter.** `english|IX` ch 7 *Vitamin-M*. Summary and mapping both on
disk (`data/content/chapters/english/ix/{summaries,mappings}/ch_07_*.json`),
`placeholder: false`, `canonical_plan` present. The row:

```json
{"chapter": 7, "title": "Vitamin-M (Vitamin-M)", "weight": 9.6, "exact_share": 17.18,
 "recommended_periods": 17, "canonical_minutes": 850, "floor_minutes": 510.0,
 "floor_periods_at_standard": 10, "canonical_periods": [17, 14, 10], "placeholder": false,
 "canonical_plan": {"counts": [17, 14, 10], "provisional": true, "basis": "arithmetic",
                    "registry_sections": null, "authored": []}}
```

`provisional: true` / `basis: "arithmetic"` is the expected pre-C1 state; it finalizes to
`authored_standard` when `variant_plans.py annotate` runs inside C1. Chosen (founder, this
session) over ch 13 (15 periods), ch 11 (drama) and ch 3 on band width: 17 → 10 is the widest
canonical band in the class, so the compacts have the most condensation room and C8's
transition inspection has the most to look at. **The cost of that choice is named:** it is
also the class's largest chapter, so three authoring runs at 17/14/10 periods are the most
expensive in the class, and it is a prose chapter, so the **drama** delta (`drama_summary`,
role-assigned reading, act-splitting — a whole [SECONDARY DELTA] branch of Rules 1, 2A, 3 and
4) is **NOT exercised by the pilot**. That branch is left to the pre-warm sweep; ch 11 is the
only drama in the class.

**P5.4 · The three test identities' teaching profiles for class IX.** **CLOSED 2026-08-12** —
set up by Kumar through the app's own first-run / profile flow, not by hand-editing JSON, so the
setup is itself the live check of that flow. Verified on disk at
`data/readiness/{u}/{u}/profile.json`:

| identity | section | durations | ppw_by_duration | budget |
|---|---|---|---|---|
| kumar1 | **9A** | [50] | {50: 6} | weeks × 27 |
| kumar2 | **9D** | [50] | {50: 6} | weeks × 27 |
| kumar3 | **9F** | **[50, 60]** | {50: 5, 60: 1} | weeks × 27 |

- **Sections are disjoint** (9A · 9D · 9F), which is what makes X1's tenancy evidence
  unambiguous: a section appearing under two identities cannot prove which tenant a served plan
  belongs to.
- **The mixed duration is on the right identity.** §4 of the template assigns C6's
  mixed-duration matrix to kumar3, and kumar3 is the one carrying [50, 60] — a real week of five
  50-minute sittings and one 60, anchor 50. kumar1 and kumar2 are 50-only at the class standard
  and serve as the control. This is the same shape S4 and S5 closed on.
- **Budget is identical across the three** (27 weeks), so any difference C6 finds cannot have
  come from the budget.
- **Tenancy shape intact:** three separate `{tenant}/{user}/` directories, `tenant_id ==
  user_id` on each.
- **Leftover history, accepted.** The profiles also carry SS VIII/IX, Science VIII/IX, Maths
  III/VII/IX and TWAU V from S1–S8. The template's "nothing left over from an earlier stage" was
  **waived by the founder at S6 (2026-08-07)** and the waiver holds here for the same reasons:
  the residue is harmless — it describes a teacher who teaches more than one thing, which is the
  real ICP — it touches no english-IX key, and clearing it would cost a fresh pass through the
  first-run flow for no evidence gained.

**P5.5 · THE CARRIER — the one-line trace.**

> **rule 7 · period-field family · item (`source_section_id` + `source_spine`) → period
> (`section_id` + `spines_taught[]`) · container: a list of SPINE groups each carrying
> `items[]` · plugin method `EnglishSubject.assessment_to_view` (shipping for the app since
> before the campaign; its cell join and N-to-N pairing now factored out as
> `english/subject.py::cell_resolver`) · `genon_assessment` present as of 2026-08-12 · not in
> `_NOT_YET`.**

Landed as a **delegation**, and §3 is why that word had to be taken literally here.
`("english", "secondary")` is deleted from `_NOT_YET`; **preparatory and middle remain**,
with their entries rewritten to say the code is in place and to name the three things S9 and
S10 must confirm before deleting a line (spine set, container shape, spine-keyed handoff).

**Part 5 of the check — where does this stage's period keep its section anchor?** (The
question S5 added.) `grep -c section_anchor` is **0 in all three english LP constitutions**,
so the answer is: nowhere, and the read is mediated. `genon_unit_anchor` builds the cell token
from `section_id` + `spines_taught[]`, and `genon_anchor_field_present` returns **False** —
the expensive half, because without it `top_brief_for` would demand `section_anchor` at
metered STEP 1 and the certifier would then find no closing unit in a library already paid
for. One grep answered it for the whole family; S9 and S10 inherit the answer.

**Verified end-to-end on the real saved shape**, not on a fixture invented for the purpose
(`backup/saved_plans/english/ix/ch_11_20260608_213837.json` — 7 units, one main_section, 6
items in 6 spine groups):

- **6 items, zero orphans, every `unit_ref` a singleton**, and every anchor equal to the
  independently computed *"last unit teaching this cell"*: RFC spans units 1–3 → anchors at 3;
  VocGram spans 4–5 → anchors at 5; listening and speaking share unit 6; writing and
  beyond_text share unit 7. Two genuinely spanning cells, so the anchoring rule is exercised
  rather than assumed.
- `genon_unit_anchor` returns `A|reading_for_comprehension` and `A|listening / A|speaking`,
  and the anchor equals `period_section_codes` split on the joiner for every unit — the anchor
  and the join code are **one expression, not two agreeing ones**.
- The plan compiles (`compile_stream`) once its bands are in the P3 shape: **30 phases, 7
  units, 6 items anchored, registry = the six cells in first-visit order.** On its authored
  `phases[]` shape it raises `KeyError: 'time_bands'`, which is correct and expected — compile
  v0.5 is declared-only, the corpus predates P3, and only newly authored canonicals reach it.
- The spine-keyed **handoff round-trips and filters**: a serve keeping units 1–4 comes back
  with `reading_for_comprehension` and `vocabulary_grammar` only, contributions verbatim.
- The **container round-trips on `spine_code`**, not on list position, and no `_genon_group`
  residue reaches the rebuilt artefact.

`tests/test_genon_carriers.py`: **97 tests with 8 failures → 113, green.** The eight failures
were the "english is a declared-field stage / english is still owed" assertions, which is
exactly what this step invalidates; they are replaced by a `TestEnglishSecondaryLanded` class
of thirteen plus three brief-carrier tests. Full suite otherwise unchanged and green
(`test_api` fails on a missing `fastapi` in the sandbox — pre-existing, environmental).

---

## 3. The one finding that would have cost money — and it is about the word "delegation"

The family helper `items_by_period_field` looks like the obvious thing to delegate to: english
is the period-field family, the helper is the family's join, S7 and S8 both used it. **Running
it on english would have been wrong twice over, and the second way is silent.**

1. It joins ONE code against one period field. English's key is a **pair**; passing either
   half alone is a different join. (Passing `source_spine` alone is the one that would have
   *looked* right — every english IX chapter has a single section, so it would have produced
   correct anchors on the whole certified class and gone wrong only on a multi-section
   chapter, which is what the middle and preparatory stages are full of.)
2. It anchors every item of a group at the group's last unit. English's display path has
   carried a refinement since 2026-07-11 that this would undo: when N items share a cell
   taught over exactly N units, they pair **positionally**, one per unit, because they are
   different topics of the same cell (the defect it fixed was a collective-nouns item
   surfacing under the prepositions unit). Anchoring them all at the close is precisely that
   defect, re-created on the served side, where a teacher would meet it.

So the delegation was made literal: the join, the pairing and the section-wide fallback were
**lifted out of `assessment_to_view` into `cell_resolver`, and both paths now call it** —
the screen and the served file cannot disagree, because there is one resolver. What genon adds
is the anchoring RULE, which comes from `carriers` (`items_with_units`, the third family's
second helper) and not from the plugin. That split is the doctrine restated: the subject knows
how its items find their units; the platform knows that an item anchors at its cell's close.

**Two smaller things landed with it**, both platform rather than stage:

- **`carriers.group_key`** — `item_container` and `_stamp_group_keys` keyed groups on
  `section_code` and fell back to the list INDEX. English's groups are keyed `spine_code`, so
  every english group would have taken a positional key — safe only while both sides of a
  serve are the same list in the same order, which is exactly what stops being true when a
  unit and its item are borrowed from a companion canonical.
- **`_ENGLISH_SPINE_CELL`** — english's `coverage_handoff` is a spine-keyed DICT of
  `section_contributions[]`, a **third** handoff shape. It fell through `to_engine_handoff`
  unchanged, `serve` read `c["los"]` as empty and filtered nothing, so a served 8-unit plan
  would have carried the full six-cell coverage of the 17-unit canonical — claiming spines the
  class never met. Identical defect to the one `_MATHS_GOAL_CLUSTER` was written for at S7,
  third shape, same seam. One difference recorded in the code: a spine left with no surviving
  cell is **dropped**, where a maths goal cluster is kept empty — assessment Rule 1 omits a
  spine with zero contributions, so an empty block would be a shape the constitution does not
  describe.
- **The closing unit reads "Synthesis" on screen.** `TestSynthesisReadsAsSynthesisOnScreen`
  carried a docstring saying english had no carrier yet and that when it landed someone should
  decide which shape it is. It is a section-grouped port, so it is now in the probe: without
  the fix a whole-chapter closer would have been filed under whichever spines it revisits
  ("Listening + Writing") — ARV-D-016's and ARV-D-101's shape on a fourth port.

---

## 4. FULL SPINE COVERAGE — the amendment the corpus forced

**Rule 2 STEP 3 said:** *"When the section's periods are exhausted, stop — remaining
spines/tasks are unanchored. Do not force a spine into a period merely because it exists."*
Read against the v2.0 serve model, that is a licence for a chapter's compacts to be a
**different chapter** from its standard.

**The corpus does it, and at exactly the count a compact would use.**
`backup/saved_plans/english/ix/ch_12_*.json` is a 4-period plan whose `coverage_handoff`
carries five spines — `beyond_text` is absent entirely. Nothing forced it; the periods ran out
and the rule permitted the stop. Its assessment therefore has 5 items where the chapter's
fuller plan would have 6.

**Why that breaks before serve ever runs.** Architecture v2.0 §0 makes a chapter a LIBRARY of
canonicals over ONE ordered registry: the Xth-unit choice set borrows *"the unit that FIRST
deals the next-due section M"* from another canonical, `standard_registry()` reads the registry
off the authored standard, and `briefs_for()` prints it verbatim into every compact's brief.
A compact whose registry is a *subset* of the standard's has no unit that first deals the
missing cell, so the borrow either fails or lands on a cell the compact never taught. The
teacher-facing version of the same fact is simpler: **a shorter plan is the same chapter taught
in fewer periods, not a smaller chapter.** A class that gets 10 periods instead of 17 should
still listen, speak and write — it should do less of each.

**What replaced it.** Coverage is mandatory at every period count; curation moves to TASK
level, where Rule 3 already governs it ("curate, don't exhaust"). Unfitted TASKS still go to
homework or ride as flagged self-study pointers — that sentence is kept, because it was always
the honest half. Rule 10's "a spine with no anchored tasks is emitted empty" was rewritten to
match: **absent from the summary is a state, dropped for time is a defect.** The assessment
constitution gained the corollary at Rule 2 — the item count does not vary with the period
count, so a shorter plan yields the same items tested on less anchored practice.

**The arithmetic it introduces, swept before it was accepted** (the S8 rule: check every
stated number against the whole class's `sections × canonical_plan.counts` AND against a real
saved plan). Minimum periods for a six-spine chapter = 1 (VocGram alone, STEP 4) +
⌈5/2⌉ (the rest at ≤ 2 adjacent) = **4**. All 16 chapters carry six spines. Floors in the
class: 8, 4, 8, 4, 6, 4, **10 (pilot)**, 4, 7, 5, 8, **3**, 9, 5, 5, 5 — **one chapter binds,
ch 12**, and P5.1 records the override. The pilot has slack at every count.

**§9.** A full constitution change — two relaxations (`task_brief`, `section_context`) and
three new obligations (full coverage, the 50-min budget line, Rule 1's exception being a
narrowing of nothing but a widening of one). It costs **nothing**: no library for this stage
exists. S7 paid ~₹106 and a C1–C3 re-run for the same class of finding, and S8 recorded the
lesson this pass acted on.

---

## 5. Deviations from the reference, declared

1. **"serve time", not "partition time"** in A1 (the partition engine was retired
   2026-07-31). Carried by S3, S4, S6, S7, S8.
2. **A9's removal half is N/A** — this file never carried the item-18 prohibition. Carried by
   S4, S7, S8, S5.
3. **A9's two lines sit in Rule 4, not Rule 5.** The reference's MCQ mandate lives in its
   answer-layer rule; english's Rule 5 is an indented bullet list where a two-paragraph block
   would read as part of the MATCH bullet. Rule 4 is where english states its MCQ semantics.
4. **A6 is a NEW RULE (8A), not an edit to an existing one** — the anchoring facts had no home
   in this file, and Rule 8 (SOURCE TAGGING) is a field inventory rather than a rule about
   linkage.
5. **A6's anchor is a PAIR**, the only one in the 8-rule table.
6. **The register's illustrative strings are english ones.** The three bans and the closing
   backward-continuity sentence are verbatim in substance.
7. **No new field was invented** to feed the serve engine (founder ruling 2026-08-10):
   `section_anchor` is not added to the period and no `period_number` is added anywhere. Both
   asserted absent by the edit script's guards.

---

## 6. What the C-cycle inherits

- **C1 is unblocked.** P5.5 is closed, so `build_library.py`'s STEP 0 pre-flight passes and no
  metered call is at risk from a missing carrier.
- **P5 is green** — P5.4 closed on the day of the prep, so C6 inherits three real class-IX
  profiles (9A · 9D · 9F, kumar3 at [50, 60]) rather than a row to fill in first.
- **C5's registry checks read CELLS.** The registry members are `A|<spine>` tokens, six of
  them; "verbatim anchors" means the token equals `section_id` + a constitution spine key, and
  "first-visit order" means the summary's on-page spine order — which for ch 7 is Reading,
  VocGram, Listening, Speaking, Writing, Beyond, NOT the canonical enumeration order the
  handoff is keyed by. **Those two orders are deliberately different** (LP Rule 2 STEP 3 says
  so: walking is editorial fidelity, enumeration is a downstream contract), and a check that
  compares one against the other will fail a good plan.
- **C8 is the step to spend time on, for the reason §2 gives.** Six registry members against
  seventeen units is the thinnest ratio in the campaign, so the Xth-unit borrow will nearly
  always be the opening unit of a cell, and the transition to inspect is "17-unit plan's
  opening Writing unit dropped into a 10-unit plan that has just finished Speaking".
- **C9.2's "a borrowed unit brings its own items" is vacuous for the closing unit at this
  stage**, and that is inherited rather than new: a closing unit teaches no cell, so no item
  anchors to it (maths·middle and maths·prep are in the same position). What C9 must check
  here instead is that the standard's six items and a compact's six items are the SAME six
  cells — which is what §4's amendment is for.
- **The pilot does not exercise the drama branch.** `drama_summary`, role-assigned reading and
  act-splitting are a whole [SECONDARY DELTA] path through Rules 1, 2A, 3, 4 and the assessment
  Rule 3/4 anchors, and ch 11 is the only drama in class IX. The pre-warm sweep owes it a run.
- **The english saved-plan corpus is on `phases`,** not `time_bands`. Display is covered by
  `_bands`' both-keys read; anything new must emit `time_bands`, and `compile_stream` will
  refuse anything that does not.
- **Two numeric limits are still untested by live generation:** Rule 9's `≤10-word brief`
  inside band narration (the corpus does not use the quoted-brief format at all, so it has
  never been exercised) and Rule 11's `expected_elements` "3–5 bullets, each ≤ 12 words". Read
  them at C3 with the S4 lesson in hand.
- **ch 12's floor override is owed at pre-warm**, not now (§2, P5.1).
