# S10 · english · middle — stage preparation sign-off

**Date:** 2026-08-13 · **Template:** `docs/testing.md` v2.9
**Drawn class:** VI (seed `english|middle|2026-08-02`, candidates vi · vii · viii) ·
**standard duration:** 40 min
**Reference pair:** SS·secondary LP v1.10 · assessment v1.7, read through english·secondary
v1.2 / v1.4 — S10 is the SECOND stage of the period-field family's english branch, so the
carry-forward ports from its own sibling rather than from the reference directly
**Landed pair:** english·middle LP **v1.6 → v1.7** · assessment **v3.6 → v3.7**
**Pilot chapter:** VI · ch 8 · *What a Bird Thought* (section **B**, type **poem** ·
1 main_section · 6 spines · 18 tasks · rec 12 · floor 7 · counts **[12, 10, 7]**)

Written by Claude. Status in the tracker is set by Kumar.

---

## 0. The headline — S10 is CLEAR to enter C1, and it is the cheapest prep of the campaign

P1–P5.5 are complete except **P5.4** (the three teaching profiles), which is amber by design
and gates **C6**, not C1. **No gate is carried into the C-cycle.**

Three things characterise this prep, and all three are consequences of S11 having gone first:

1. **The carrier was a one-line deletion.** No new code. `carriers._NOT_YET`'s english note
   asked a successor to *confirm* three things rather than re-derive them; all three held on
   the real corpus, and the note was right that "the deletion is the whole job". §3.
2. **The constitutional work was the S11 pass again, with one addition the sibling did not
   have to make:** the LP's Rule 10 was contradicting the assessment constitution outright —
   it said ONE item per cell where assessment v3.6 emits TWO. §4.
3. **The pilot is a poem, chosen deliberately** (founder, this session) so the poem-locator
   rule carried into v3.5 on 2026-08-12 — the campaign's sole open copyright finding, F2 —
   is proved by live generation instead of inherited untested. Ch 8's summary carries the
   NCERT poem in full, 17 lines verbatim. §5.

**One live defect is recorded against a certified stage** (§6): english·**secondary**'s LP
Rule 10 still carries the same "one item per cell" line this pass struck at middle.

---

## 1. Per-item verification (testing.md §3, the Claude sign-off)

| Item | Verdict | Evidence |
|---|---|---|
| **A1** — one standard row | **PRESENT** | INPUTS 3 read `"{ period_duration_minutes, period_count } where period_count = B is supplied at generation time (allocation tab suggests, user may override)"` — the same clause S11 found at secondary, licensing exactly the teacher-chosen, mixed-duration plan the variant engine cannot use. Now: *"exactly ONE row … the class-standard duration (40 min for classes up to VII, 45 for VIII, 50 for IX–X — the master-plan calibration bands, not NCF's flat 40) × the period count … handled downstream at serve time."* Class VI's standard is **40 min**, matching `master_plan.json`'s `english\|VI` row (`standard_duration_minutes: 40`). **Declared deviation:** "serve time", not the reference's "partition time" — carried by S3, S4, S6, S7, S8, S11. |
| **A5 + A7** — register as ONE block | **PRESENT, verbatim in substance** | One block after VOCABULARY, in the v1.10 **three-ban** re-cut, binding Rule 9 and `teacher_notes` by reference and never as scattered prohibitions. This stage is *not* S6's two-ban exception: english units anchor to cells and travel between plans under the Xth-unit choice set, so ban 2 binds in full. **Declared deviation:** the illustrative strings are middle-english ones and pilot-appropriate — *"having now read the whole poem"*, *"Having read the bird's complaint aloud, …"*. **Two consequential edits, the same two S7, S8 and S11 had to make, and one of them is the clause testing.md P1 names by hand.** VOCABULARY was *teaching* the positional cross-reference — its examples were literally `"the previous unit"` and `"this unit"`, which is a unit's position, exactly what ban 2 strikes — and now names the CONTENT built on, with "session" joining the excluded register. The `teacher_notes` schema comment asked for *"Transition from prior unit; **preview into next**"*; testing.md P1 names this constitution's forward-preview clause as the known direct contradiction, and the forward half is gone. `grep -c "preview into next"` = 0, `grep -c "the previous unit"` = 0. |
| **A6** — item anchoring | **CONFIRMED, not amended** | P2 asks for a confirmation and an amendment only where absent. **Rule 8A already carries it**, having landed a day early with the PAIR amendment (v3.6, 2026-08-12): the anchor is the (section × spine) **CELL**, carried by the item's own `source_section_id` + `source_spine` — 8-rule **row 7**, the table's only PAIR key — the platform resolves it against each period's `section_id` + `spines_taught[]`, and `period_ref` / `period_number` / `unit_ref` MUST NOT be emitted. The v1.2-era band-level `phase_ref` is absent and was not reintroduced (`grep -c phase_ref` = 0 in both files). Asserted by guard, not by eye. |
| **A9** — option order | **PRESENT as two lines; the removal is N/A, and no arrangement sentence** | **REMOVAL — N/A.** This file never carried the MEMORY-item-18 position prohibition; testing.md P2 names the four files that do (SS + Science, middle and secondary) and this is not one. Confirmed by grep: `consecutive`, `same label`, `vary in position` all **0**. Nothing was struck — the fourth stage running where the removal is N/A (after S4, S7, S8, S5, S11). **ADDED**, v1.7 wording, in **Rule 4** where english states its MCQ semantics — the site english·secondary chose at v1.4, for the same reason (Rule 5 is an indented bullet list a two-paragraph block reads oddly inside): the "order carries no meaning and is not yours to set" mandate, and the by-label option-reference prohibition ("both A and B", "none of the above", "all of the above", "either B or C"). **Purely additive** — no prior "none of the above" ban existed here to absorb. **NOT re-added:** `alphabetic`, `never led with`, `first word at which they differ` all assert **0** in the edit script's guards. |
| **P3** — Group B conversion | **APPLIED — real, not N/A** | Fifth stage where this was not N/A (after S6, S7, S8, S11). Array and key both renamed, with Rule 5, Rule 2A's "explicit timed phase", Rule 3's two task-reference sentences, Rule 7's C-code surface list, Rule 8's locator mirror, Rule 9's heading (`PHASE NARRATION` → `BAND NARRATION`), the lint-scope line, INPUTS 1 and the schema all following. **No `band_id`.** Guards: `grep -c 'phases\['` = 0, `'"phases"'` = 0, `band_id` = 0, `time_bands` = 2, `"activity": string` present. **This stage needed NO plugin work** — `english/subject.py::_bands` has read both keys, newest first, since S11 landed it on 2026-08-12, which is what keeps the whole english saved-plan corpus rendering with a timed spine after the rename. |
| **P4** — history to the sidecar | **DONE, and it included a removal** | Both constitutions already had a `CHANGELOG.md` (created 2026-08-11 and 2026-08-12 by the cross-stage passes) and each gains its entry. **The assessment constitution carried an in-document history block** — v3.6 wrote its own five-line changelog above DESIGN PRINCIPLE — which is exactly what P4 forbids; it is lifted out and back-filled as the v3.6 sidecar entry. Guard asserts `v3.6 (2026-08-12)` = 0 in the file. Both footers tracked their headers correctly before the pass and track the new versions now. |
| **Rule 10** — the item-count line (v1.7) | **AMENDED — a live contradiction, not a risk** | Covered in §4. |
| **Rule 2 STEP 3** — full spine coverage (v1.7) | **AMENDED, founder call** | Covered in §4. |
| **Rule 1** — the closing-unit exception (v1.7) | **AMENDED, and it was a certainty not a risk** | "Exactly ONE main_section and one or two adjacent spines" cannot describe the whole-chapter closing unit the platform brief mandates of the standard canonical. S7 met it live at C3 (ARV-D-094) and amended mid-cycle; S8 recorded the lesson; S11 applied it free. Applied here free, before authoring. The constitution still names no V-rule: the exception describes a closing unit's SHAPE and never mandates one. |
| **`task_brief` ≤ 12 → ≤ 18 words** (v1.7) | **AMENDED, on measurement** | §4. |
| **`section_context` 10–15 → 10–18 words** (v1.7) | **AMENDED, on measurement** | §4. Lower bound kept — the field is useless at two words. |
| **Rule 2 STEP 1** — the 45-minute budget (v1.7) | **ADDED** | The ceiling table named a 40-min and a 60-min period but **not 45**, which is the VIII class standard and therefore the authored duration for a third of this stage's classes — the one duration A1 now fixes. Reads ≤ 3 tasks, interpolated from the same per-spine rates the rule already states. Same class of gap as S11's missing 50-min line. |
| **Cancelled amendments A2/A3/A4, X3** | **ABSENT** | None introduced. Asserted by guard: `role_handoff`, `unit_handoff`, `band_ref`, "role weighting", `phase_ref`, `band_id` all 0 in both files. |
| **V-rules in a constitution** | **NONE** | No section registry, no verbatim-anchor mandate, no first-visit-order rule, no closing-synthesis mandate, no per-variant assessment rule, no INPUTS acknowledgment, no precedence line — asserted by guard ("section registry", "reserved token", "synthesis unit", "closing synthesis" all 0). Worth restating because Rule 1's new closing-unit exception sits one sentence away from the brief's synthesis mandate and deliberately does not become it. |

---

## 2. P5 — stage inputs

**P5.1 · The floor.** Accepted at the standing ratio `round(0.6 × recommended_periods)`, **no
override anywhere in the class**. For ch 8 that is `round(0.6 × 12) = round(7.2) = 7`, matching
`floor_periods_at_standard` on the row. Equal dispersion over [7, 12]: A−C = 5 ≥ 4, so counts
are `{A, ⌈(A+C)/2⌉, C}` = **[12, 10, 7]** — three canonicals, three authoring runs.

> **The full-coverage arithmetic was swept before the rule was accepted** (the S8 rule: check
> every stated number against the whole class's `sections × canonical_plan.counts` AND against
> a real saved plan). A six-spine chapter needs **≥ 4 periods**: VocGram occupies a period alone
> (STEP 4) plus ⌈5/2⌉ for the other five at ≤ 2 adjacent. Swept across **all 46 middle
> chapters** — VI, VII and VIII, not only the drawn class — **no chapter binds.** VI's floors run
> 5, 4, 6, 7, 7, 7, 4, **7 (pilot)**, 7, 5, 5, 4, 5, 5, 5, 2; the three that sit exactly at 4
> (ch 2, ch 7, ch 12) are saturated but feasible, and ch 16 carries only two spines against a
> floor of 2. **Unlike english·secondary, which owes ch 12 a floor override at pre-warm, the
> middle stage owes none.** The pilot has slack at every count.

**P5.2 · THE SECTION REGISTRY — inherited from S11, and this is the stage that proves it.**

The definition is english·secondary's, unchanged, because it was written for the family and not
for one stage: **the registry member is the (section × spine) CELL**, token
`"<section_id>|<spine_key>"`, both halves closed authored vocabulary, joined for a multi-cell
unit with the V2 joiner (`B|listening / B|speaking`). First-visit order is the summary's on-page
spine order, which Rule 1 already forbids re-sequencing — **and it is NOT the canonical
enumeration order the handoff is keyed by; a C5 check that compares one against the other will
fail a good plan.**

**What middle adds is the evidence.** S11 recorded that at secondary the pair key could not be
*disproved* — every english IX chapter is one `main_section`, so joining on the spine alone
gives correct answers across the whole certified class. **Middle's corpus is genuinely
multi-section**: `tests/fixtures/english_vii_ch01_saved.json` teaches Reading in sections A
(units 1–2), B (6–7) and C (10), and a spine-only join collapses all three cells onto unit 10.
That case is now a test (§3).

**The registry for the pilot**, in first-visit order, is these six:

```
1. B|reading_for_comprehension   (Let us read + Let us discuss + Let us think and reflect, 11 tasks)
2. B|listening                   (Let us listen, 1 task)
3. B|speaking                    (Let us speak, 1 task)
4. B|writing                     (Let us write, 1 task)
5. B|vocabulary_grammar          (Let us learn, 2 tasks)
6. B|beyond_text                 (Let us explore, 2 tasks)
```

Two notes carried into the C-cycle:

- **The section id is `B`, not `A`.** English VI is fully split — 16 chapters, one
  `main_section` each — and the split kept each section's position in its original textbook
  unit, so the ids run A, B, C, D across a unit's chapters. A check that assumes `A` is wrong
  for eleven of the sixteen.
- **Coverage feasibility at all three counts.** The tail cells carry 1–2 tasks each and cannot
  fill more than a unit apiece, so the spread is `RFC ~6 · VG 2 · listening 1 · speaking 1 ·
  writing 1 · beyond 1` at **12**, and `RFC ~2 · VG 1 · four tail cells 1 each` at the floor of
  **7** — feasible with slack at both ends, which is the difference from secondary's ch 7 (tight
  at its floor).

**P5.3 · The pilot chapter.** `english|VI` ch 8 *What a Bird Thought*. Summary and mapping both
on disk (`data/content/chapters/english/vi/{summaries,mappings}/ch_08_*.json`),
`placeholder: false`, `canonical_plan` present. The row:

```json
{"chapter": 8, "title": "What a Bird Thought (Nurturing Nature)", "weight": 16.5,
 "exact_share": 12.66, "recommended_periods": 12, "canonical_minutes": 480,
 "floor_minutes": 288.0, "floor_periods_at_standard": 7, "canonical_periods": [12, 10, 7],
 "placeholder": false,
 "canonical_plan": {"counts": [12, 10, 7], "provisional": true, "basis": "arithmetic",
                    "registry_sections": null, "authored": []}}
```

`provisional: true` / `basis: "arithmetic"` is the expected pre-C1 state; it finalizes to
`authored_standard` when `variant_plans.py annotate` runs inside C1.

**Chosen (founder, this session) for the POEM**, over ch 6 *The Chair* (narrative, identical
band [12, 10, 7], 22 tasks) and ch 4 (23 tasks, narrower band). The reasoning is §5's: ch 8
carries `poem_text` in full — 17 verbatim lines — so it is the chapter that actually exercises
the poem-locator rule, and S11's pilot deliberately did NOT exercise its own delta branch
(drama) and left it to the pre-warm sweep. **The cost of the choice is named:** it is tied for
the largest chapter in the class, so three authoring runs at 12/10/7 periods are among the most
expensive; and the ORDINARY prose/narrative path — eleven of VI's sixteen chapters — is not the
pilot. Ch 8's band is the joint-widest, so C8's transition inspection loses nothing.

**P5.4 · The three test identities' teaching profiles for class VI.** **OPEN — amber, and it
gates C6, not C1** (testing.md §3's provisional sign-off). Nothing else in P5 waits on it.
What it needs, from the same shape S4, S5 and S11 closed on:

| identity | section | durations | why |
|---|---|---|---|
| kumar1 | a VI section | [40] | identity requests; the control |
| kumar2 | a **different** VI section | [40] | between-variant and below-floor requests |
| kumar3 | a **third** VI section | **[40, 55 or 60]** | C6's mixed-duration weekly matrix |

Sections must be **disjoint** — a section appearing under two identities cannot prove which
tenant a served plan belongs to, which is the whole of X1's evidence. Set up through the app's
own first-run / profile flow, not by hand-editing JSON: the setup doubles as the live check of
that flow. The "nothing left over from an earlier stage" clause stays waived per the founder
ruling of 2026-08-07 (S6) — the profiles carry S1–S8's and S11's classes and the residue touches
no english-VI key.

**P5.5 · THE CARRIER — the one-line trace.**

> **rule 7 · period-field family · item (`source_section_id` + `source_spine`) → period
> (`section_id` + `spines_taught[]`) · container: a list of SPINE groups each carrying
> `items[]` · plugin method `EnglishSubject.assessment_to_view`, whose join, N-to-N pairing and
> section-wide fallback live in `english/subject.py::cell_resolver` · `genon_assessment`
> present (stage-agnostic, landed at S11) · **not in `_NOT_YET` as of 2026-08-13**.**

Part 5 (where does the PERIOD keep its section anchor): `grep -c section_anchor` is **0** in the
english·middle LP constitution, so the read is mediated — `genon_unit_anchor` builds the
composite cell token and `genon_anchor_field_present` returns **False**. Both are stage-agnostic
and both were verified rather than assumed. §3 is the confirmation in full.

---

## 3. P5.5 in detail — the note that did a successor's work

`carriers._NOT_YET` did not say "english·middle is owed" and stop. It said the code is in place
and named **three things to confirm, not re-derive**, before deleting a line. All three were
checked against the REAL saved corpus — never a fixture invented for the purpose — by
`verify_s10_carrier.py`, which is re-runnable and is the P5.5 artefact:

| condition | result |
|---|---|
| the stage's **spine SET** matches the summary's | **46 chapters, 272 taught cells** across VI/VII/VIII use the six constitution spine keys and **nothing else**; all six are exercised |
| the **assessment container** is still the spine-grouped list | all **12** saved middle plans: `{spine_code, spine_title, items[]}`, no other shape |
| the LP still emits **`coverage_handoff` as a spine-keyed DICT** | all 12: keys ⊆ the six spines, every value a `section_contributions` block — the shape `_ENGLISH_SPINE_CELL` round-trips |

**End to end on the real saved middle shape:** 12 plans, **53 items, ZERO orphans**, every
anchor equal to the independently computed *last unit teaching that cell*, with the N-to-N
pairing intact wherever a cell's item count equals its unit count. The gate then opened for all
three middle classes and **preparatory stayed shut** — which is the stage-granular table doing
the job S4 built it for.

**So the deletion was the whole job. No new code landed with this stage.** That is worth
recording as the outcome, because it is the first carrier in the campaign where the previous
stage's note reduced the work to a confirmation. S8 was the previous cheapest (three lines of
delegation); this one is zero.

**Tests.** `tests/test_genon_carriers.py` went **116 with 3 failures → 122, green.** The three
failures were precisely the "english·middle is still owed" assertions this step invalidates:
`TestCarrierPreFlight.test_owed_stages_report_their_stage_and_row`,
`TestEnglishSecondaryLanded.test_the_stage_is_no_longer_owed_and_its_siblings_still_are`, and
`TestUnimplementedFamiliesFailLoudly.test_english_raises_with_the_owing_stage_named` — the last
of which was **moved to preparatory rather than deleted**, so the family keeps a live test that
an owed stage still refuses. A new `TestEnglishMiddleLanded` class of six replaces them, and its
centrepiece is the one thing secondary structurally could not test: **the multi-section join**,
asserting the three Reading cells of the VII fixture reach three different units (2, 7, 10)
where a spine-only join would put all three on 10.

Full suite otherwise unchanged. Four suites fail for reasons that predate this pass and were
confirmed pre-existing by re-running them against the unmodified files: `test_api` (no `fastapi`
in the sandbox — environmental), `test_link_resolver` (a fixture path under
`data/content/saved_plans/` that is not on disk), `test_normalized_item` (a TWAU·III canonical
with an MCQ carrying no correct option) and `test_genon_plan_key`.

---

## 4. The constitutional findings — one contradiction, one licence, two numbers

**(a) Rule 10 was contradicting the assessment constitution outright.** It read *"Total
assessment item count equals the total number of `section_contributions` entries … **one item
per (section × spine) cell**"*. Assessment **v3.6**, landed 2026-08-12, emits **two** — a PAIR
per cell on a prescriptive slot table. The two halves of the same stage's pair disagreed on the
count, and the LP's half is the one the generator reads while it writes the handoff. Corrected
to the pair, with the corollary the assessment file already carries: **the item count does not
vary with the period count**, so a shorter plan yields the same items tested on less anchored
practice. This is the kind of drift a cross-stage amendment leaves behind when it moves three
assessment constitutions and none of the three LPs beside them.

**(b) FULL SPINE COVERAGE replaces Rule 2 STEP 3's drop licence.** STEP 3 said: *"When the
section's allocated periods are exhausted, stop — remaining spines and tasks in that section are
not anchored. Do not force a spine into a period simply because it exists … This is not a
defect — it is an honest reflection of available time."* Under architecture v2.0 that is a
licence for a chapter's compacts to be a **different chapter** from its standard: a library
shares ONE registry, `briefs_for()` prints the standard's registry verbatim into every compact's
brief, and the Xth-unit choice set borrows *the unit that FIRST deals the next-due cell* — which
a compact whose registry is a subset simply does not have.

**The middle corpus does it, and worse than secondary's.**
`backup/saved_plans/english/vii/ch_06_*.json` is a **one-unit** plan carrying **one** of its
section's six spines; `ch_03` (2 units) carries three; `ch_06` at VIII (2 units) carries two.
Nothing forced them — the periods ran out and the rule permitted the stop. The teacher-facing
version of why that is wrong is the sentence now in the rule: *a class given six periods instead
of twelve should still listen, speak and write; it should do less of each.* Curation moves to
TASK level, where Rule 3 already governs it; unfitted TASKS still go to homework or ride as
flagged self-study pointers, because that half was always honest. Rule 10 gained the matching
corollary — **absent from the summary is a state, dropped for time is a defect.**

**(c) `task_brief` ≤ 12 → ≤ 18 words, measured.** Rule 9 mandates the brief carry
`"<Subheading> (p.NN): <plain brief>"`. **Only 13 of 123** saved middle briefs carry a locator at
all — the mandate postdates the corpus — so the raw distribution understates the real length.
Simulating the locator at its true cost (+4 words: a 3-word subheading such as "Let us read"
plus "(p.NN):") puts **44 of 123 over 12** and **0 of 123 over 16**. Eighteen is the number
english·secondary settled on, so the family carries one cap rather than two.

> **The measurement forced a second edit, and it is the more useful one.** 16 of VI's 96 cells
> carry a **MERGED** `section_name` — *"Let us read + Let us discuss + Let us think and
> reflect"*, **13 words**, more than the whole cap by itself, and the pilot's Reading cell is one
> of them. Rule 9 now says **which** subheading to name: the single one the task actually sits
> under, not the merged string. *The merged form is the cell's identity, not a location a
> teacher can turn to.* Left unsaid, the rule is unsatisfiable at any cap on exactly the
> richest cell in the chapter.

**(d) `section_context` 10–15 → 10–18 words.** Three VIII contributions run 16, 16 and 17. VI and
VII's saved plans predate the field entirely and carry it empty, so VIII is the only evidence —
recorded as thin, and it agrees with secondary's independent measurement.

**`activity_title` stays ≤ 12** — the corpus maximum is 11, so nothing forces it. Recorded so
that C3 does not re-open a number that was checked.

**§9.** A full constitution change on both files: two relaxations (`task_brief`,
`section_context`) and four new obligations (full spine coverage, the register, the 45-min line,
the by-label option ban). It **costs nothing** — no english·middle library exists, so nothing
re-opens. S7 paid ~₹106 and a C1–C3 re-run for the same class of finding.

---

## 5. The pilot is a poem, and that is the point

`docs/NCERT_copyright_review.md` finding **F2** is the campaign's sole open copyright finding:
`poem_text` in a chapter summary is the NCERT poem, not a paraphrase, and an item that quotes it
puts published verse into a **canonical** — the one artefact class that reaches the cloud. It
was closed on all three english assessment constitutions on 2026-08-12 (ARV-D-138): a poem
section's stimulus is a LOCATOR, `Read lines N–M on p.PP, beginning "<incipit>"`, incipit capped
at **eight words**, no ellipsis, lines copied into no field. Reading `poem_text` stays legal;
only reproduction is closed.

**Middle's half of that fix has never been exercised.** It was carried early, ahead of this
P-prep, on the reasoning that §9 re-authors nothing while no english library exists. Ch 8 is the
chapter that tests it: section B is a poem, `poem_text` carries the full 17 lines (*"I lived
first in a little house, / And lived there very well, …"*), and its Reading cell has 11 tasks —
the richest cell in the chapter and the one most likely to reach for a quotation.

**What C3 must read on this pilot, specifically:**

- every poem-grounded item addresses the poem **by place plus an ≤8-word incipit**, never by
  transcription, and never with an ellipsis continuing the quotation;
- no poem line reaches `item_stem`, `visual_stimulus`, `suggested_answer` or any rubric field;
- the incipit cap holds under the **PAIR** — two items per cell means two chances to drift, and
  the slot-2 item (inference/analysis) is the one with a reason to quote;
- **the locator is a page number, and NCERT prints no line numbers on its poems** — ch 8's
  section is `p.85-92`, so a bare "lines 5–8" with no page is unusable and is a defect, not a
  style note.

**Middle needed only two edit sites where secondary needed five**, because middle has no
EXTRACT_ANALYSIS "3–8 line verbatim extract" block — its `visual_stimulus` is `"" | pipe-table`
only. So the surface being tested here is narrower than secondary's, and correspondingly the
whole of it: Rule 3's REQUIRED clause and its PROHIBITED clause.

---

## 6. Defects and follow-ups raised by this prep

**ARV — english·secondary LP Rule 10 still says "one item per (section × spine) cell".**
Against a **certified** stage (S11). The 2026-08-12 PAIR amendment moved all three english
*assessment* constitutions and none of the three *LP* constitutions beside them; middle's copy
was struck in this pass, secondary's is live. It is a §7 defect row rather than a fix taken here
because S11's library is authored and touching its LP re-opens it under §9 — and the question of
whether the stale line reached the authored handoff is a C3 read, not a P-prep read.
**Preparatory carries the same line and is free** (no library, S9 has not run); it should be
struck at S9's P1 rather than left for a third discovery.

**The english prompt builder is stage-agnostic and needs no lift.** S11 met
`NotImplementedError` from `prompt_assembly.build_lpa_prompts` at its C1 and lifted
`_build_lpa_prompts_english` from the prototype. It dispatches on `subject_to_folder(subject)`,
not on stage, so S10 inherits it whole — including the `phases` → `time_bands` rename P3 forces.
**Verified free, before spending**, by the same dry pass S11 used (§7).

---

## 7. Dry pre-flight — C1 is unblocked at ₹0

`python3 genon/generate_canonical.py one english vi 8 --dry` assembles the real prompt without
an API call:

```
English · Grade VI · ch 8 — 12 × 40 min (LP+A; constitution serve-era)
  schedule : Total: 12 periods · 8h 0min
  system   : 59,381 chars   user: 30,130 chars
```

(Against english·IX ch 7's 53.8k / 48.7k: the system prompt is larger — middle's constitutions
are longer after this pass — and the user prompt smaller, ch 8 being a 12-period poem against a
17-period prose chapter.)

**Present in the assembled prompt**, asserted rather than eyeballed: **LP v1.7** ·
**assessment v3.7** · THE SELF-CONTAINED REGISTER · A1's "exactly ONE row" and the master-plan
bands · FULL SPINE COVERAGE · Rule 1's closing-unit exception · the 45-min budget line ·
Rule 9's WHICH SUBHEADING clause · A9's "MCQ OPTION ORDER IS NOT YOURS TO SET" · RULE 8A ·
the PAIR (TWO ITEMS PER SPINE-CELL) · the poem locator (AT MOST EIGHT WORDS) and REPRODUCING
THE POEM · `time_bands` in the output sketch · the pilot's `poem_text` (correctly — reading is
legal, reproducing is not).

**Absent:** `section_anchor` · `role_handoff` · `phase_ref` · any surviving `phases` key ·
`preview into next` · any stale VERSION 1.6 / 3.6 string.

---

## 8. What the C-cycle inherits

- **C1 is unblocked.** P5.5 is closed, `build_library.py`'s STEP 0 pre-flight passes, and the
  dry pass proves the prompt assembles under the new pair. Command:
  `python3 genon/build_library.py english vi 8`.
- **P5.4 is the one open item and it stops at C6**, not before. Three VI profiles on disjoint
  sections, kumar3 mixed-duration.
- **C3 has a named agenda beyond the rule table**: the poem locator under the PAIR (§5), and the
  four numeric limits this pass either moved or deliberately did not — `task_brief` ≤ 18,
  `section_context` 10–18, `activity_title` ≤ 12 (unmoved, corpus max 11) and assessment
  Rule 11's `expected_elements` "3–4 bullets, each ≤ 10 words", which is **narrower than
  secondary's 3–5 / ≤ 12 and has never been exercised by live generation**. Read them with the
  S4 lesson in hand.
- **C5's registry checks read CELLS**, six of them, `B|<spine>` — **not `A|`**. First-visit order
  is the summary's on-page spine order, which is NOT the canonical enumeration order the handoff
  is keyed by; a check comparing one against the other will fail a good plan.
- **C8's transition inspection** has six registry members against twelve units — two units per
  cell, twice as dense as secondary's pilot, so the Xth-unit borrow is less often a cell's
  opening unit and the choice set has more to choose between. The band [12, 10, 7] is the
  joint-widest in the class.
- **C9.2's "a borrowed unit brings its own items" is vacuous for the closing unit**, inherited
  from S11 rather than new: a closing unit teaches no cell, so no item anchors to it. What C9
  must check instead is that the standard's twelve items and a compact's twelve are the SAME six
  cells — which is what §4(b) is for.
- **The middle saved-plan corpus is on `phases`**, not `time_bands`. Display is covered by
  `_bands`' both-keys read; anything newly authored must emit `time_bands`, and `compile_stream`
  will refuse anything that does not.
- **The pilot does not exercise the prose/narrative path**, which is eleven of VI's sixteen
  chapters. Left to the pre-warm sweep, the same way S11 left drama.
- **No floor override is owed anywhere in this stage** (§2, P5.1) — the first stage since S6
  where the full-coverage sweep found nothing to raise.

---

## 9. Artefacts

| file | what it is |
|---|---|
| `apply_s10_amendments.py` | P1 + P3 + the measured edits — 25 guarded replacements, 16 absence guards, 12 presence guards |
| `lp_english_middle_v1.6_pre.txt` · `..._v1.6_to_v1.7.diff` | the LP before, and the diff |
| `apply_s10_assessment.py` | P2 (A6 confirm + A9) and P4's in-file half |
| `assess_english_middle_v3.6_pre.txt` · `..._v3.6_to_v3.7.diff` | the assessment before, and the diff |
| `verify_s10_carrier.py` | P5.5 — the three conditions, part 5, and the end-to-end run; re-runnable before and after the deletion |
| `genon/out/canonical/english/vi/ch_08_*_promptdump.json` | the dry pre-flight (§7) |
| both `CHANGELOG.md` sidecars | P4 |
