# S9 · english · preparatory — stage preparation sign-off

**Date:** 2026-08-13 · **Template:** `docs/testing.md` v2.10
**Drawn class:** III (seed `english|preparatory|2026-08-02`, candidates iii · iv · v) ·
**standard duration:** 40 min
**Reference pair:** SS·secondary LP v1.10 · assessment v1.7, read through english·secondary
v1.2 / v1.5 and english·middle v1.7 / v3.7 — S9 is the THIRD and last stage of the
period-field family's english branch, so the carry-forward ports from its two siblings
rather than from the reference directly
**Landed pair:** english·preparatory LP **v1.1 → v1.2** · assessment **v1.4 → v1.5**
**Pilot chapter:** III · ch 11 · *The Big Laddoo* (section **B**, type **poem** ·
1 main_section · 5 spines · 11 tasks · pp. 70–77 · rec 12 · floor 7 · counts **[12, 10, 7]**)

Written by Claude. Status in the tracker is set by Kumar.

---

## 0. The headline — S9 is CLEAR to enter C1, with **no gate at all**

P1 · P2 · P3 · P4 · P5.1–P5.5 are **all complete**. P5.4 was closed by the founder during this
session, so unlike every other stage this one does not even carry the amber. **S9 enters its
C-cycle with nothing open.**

Four things characterise this prep:

1. **A1 was not the usual one-row edit — the constitution named the wrong duration band
   outright.** INPUTS 3 read *"`period_duration_minutes` is 30 or 35 at prep (35 default)"*
   against a master plan that carries english III, IV and V at **40**. Three sites carried it.
   §4(a) — this is the finding of the pass.
2. **The carrier was the LAST entry in `_NOT_YET`, and deleting it emptied the table.** Every
   subject·stage in the 11-stage matrix is now carried. No new code; the one difference the
   note named — preparatory's spine set is **five**, not six — was real and cost nothing. §3.
3. **The prompt BUILDER was still saying one item per cell.** Found by the dry pre-flight, not
   by reading a constitution: `genon/prompt_assembly.py` contradicted assessment Rule 2's PAIR
   in three places, at all three english stages. Fixed free, before C1. §5.
4. **The pilot is a poem**, deliberately, so preparatory's half of the copyright fix is proved
   by live generation rather than inherited untested. §6.

**Two defects are raised** (§7): two class-V chapter summaries are **not parseable JSON**, and
the `assessment_items` prompt contradiction above is recorded against S10 and S11 as well.

---

## 1. Per-item verification (testing.md §3, the Claude sign-off)

| Item | Verdict | Evidence |
|---|---|---|
| **A1** — one standard row | **PRESENT, and it corrected a WRONG NUMBER as well as a wrong shape** | INPUTS 3 read *"Period schedule: `{ period_duration_minutes, period_count }`. `period_count = B` from the Allocate tab. `period_duration_minutes` is 30 or 35 at prep (35 default)."* Now: *"exactly ONE row … the class-standard duration (40 min for classes up to VII, 45 for VIII, 50 for IX–X — the master-plan calibration bands, not NCF's flat 40) × the period count … Preparatory is classes III–V, so every preparatory plan is authored at 40 MINUTES. There is no 30- or 35-minute preparatory period."* `master_plan.json` carries `english\|III`, `english\|IV` and `english\|V` at `standard_duration_minutes: 40`. Rule 2 STEP 1's ceiling table and the schema comment carried the same wrong band and both follow. **Declared deviation:** "serve time", not the reference's "partition time" — carried by S3, S4, S6, S7, S8, S11, S10. **Naming only 40 is deliberate** — preparatory spans one class-standard, unlike middle, so a table of alternatives would invite the author to branch on a number A1 has already fixed. §4(a). |
| **A5 + A7** — register as ONE block | **PRESENT, verbatim in substance** | One block after VOCABULARY, in the v1.10 **three-ban** re-cut, binding Rule 9 and `teacher_notes` by reference and never as scattered prohibitions. Not S6's two-ban exception: preparatory units anchor to cells and travel between plans under the Xth-unit choice set, so ban 2 binds in full. **Declared deviation:** the illustrative strings are prep-english and pilot-appropriate — *"a quick paired chant"*, *"now that we have recited the whole poem"*, *"Having chanted the laddoo rhyme together, …"*. **The same two consequential edits every english stage has had to make.** VOCABULARY was *teaching* the positional cross-reference — its worked examples were literally `"the previous unit"` and `"this unit"` — and the `teacher_notes` schema comment asked for *"transition from prior unit; **preview into next**"*, which testing.md P1 names by hand as the english family's known direct contradiction. `grep -c "the previous unit"` = 0, `grep -c "preview into next"` = 0. |
| **A6** — item anchoring | **CONFIRMED, not amended** | P2 asks for a confirmation and an amendment only where absent. **Rule 8A already carries it in full**, having landed a day early with the cross-stage PAIR pass (v1.4, 2026-08-12): the anchor is the (section × spine) **CELL**, borne by the item's own `source_section_id` + `source_spine` — 8-rule **row 7**, the table's only PAIR key — resolved by the platform against each period's `section_id` + `spines_taught[]`, with `period_ref` / `period_number` / `unit_ref` prohibited and TWO-STAGE SCOPING declared by SLOT. The v1.2-era band-level `phase_ref` is absent and was not reintroduced (`grep -c phase_ref` = 0 in both files). The **second genuine confirmation of the campaign**, after S10's, and for the same reason. Asserted by guard, not by eye. |
| **A9** — option order | **PRESENT as two lines; the removal is N/A, and no arrangement sentence** | **REMOVAL — N/A.** This file never carried the MEMORY item-18 position prohibition; testing.md P2 names the four files that do (SS + Science, middle and secondary) and this is not one. Confirmed by grep: `consecutive items`, `same label`, `vary in position` all **0**. The **fifth** stage running where the removal is N/A (after S4, S7, S8, S5, S11, S10). **ADDED**, v1.7 wording, in **Rule 4** where english states its MCQ semantics — the site secondary chose at v1.4 and middle at v3.7, for the same reason (Rule 5 is an indented bullet list a two-paragraph block reads oddly inside): the "order carries no meaning and is not yours to set" mandate, and the by-label option-reference prohibition ("both A and B", "none of the above", "all of the above", "either B or C"). **Purely additive** — no prior "none of the above" ban existed here to absorb. **NOT re-added:** `alphabetic`, `never led with`, `first word at which they differ` all assert **0** in the edit script's guards. |
| **P3** — Group B conversion | **APPLIED — real, not N/A** | Sixth stage where this was not N/A (after S6, S7, S8, S11, S10). Array and key both renamed, with Rule 5, Rule 2A's "explicit timed phase" and its re-recite band, Rule 3's narration sentence and **its two listening bands** (the prep-specific site — listening rides inside `oracy` as timed segments, which no sibling has), Rule 8's locator mirror, Rule 9's heading (`PHASE NARRATION` → `BAND NARRATION`), the lint-scope line and the schema all following. **No `band_id`.** Guards: `grep -c 'phases\['` = 0, `'"phases"'` = 0, `band_id` = 0, `time_bands` = 2, `"activity": string` present, **and the word "phase" reaches ZERO occurrences**, matching middle and secondary. **This stage needed NO plugin work** — `english/subject.py::_bands` has read both keys, newest first, since S11 landed it on 2026-08-12. Third time a display debt one stage paid has made a successor's P3 free. |
| **P4** — history to the sidecar | **DONE, and it included a removal** | Both constitutions already had a `CHANGELOG.md` and each gains its entry. **The assessment constitution carried an in-document history block** — v1.4 wrote its own seven-line changelog above DESIGN PRINCIPLE, exactly what P4 forbids; lifted out and back-filled as the v1.4 sidecar entry. Guard asserts `v1.4 (2026-08-12)` = 0 in the file. The same removal S10 made on its own file the same week. **One extra correction:** the LP footer read *"Version 1.0"* against a v1.1 header — stale since the 2026-08-11 bump; now tracks, with the family's `· Internal Document` suffix. |
| **Rule 10** — the item-count line (v1.2) | **AMENDED — the third discovery, and the one S10 predicted** | §4(c). |
| **Rule 2 STEP 3** — full spine coverage (v1.2) | **AMENDED, founder ruling, and the corpus does it** | §4(b). |
| **Rule 1** — the closing-unit exception (v1.2) | **AMENDED, free** | v2.0 mandates the standard canonical's whole-chapter synthesis unit; Rule 1's "exactly ONE main_section and one or two adjacent spines" — with preparatory's **extra clause (d)**, *the secondary spine carries 1 task only*, tighter than any sibling — cannot describe it. S7 met it live at C3 (ARV-D-094) and amended mid-cycle; S8, S11 and S10 applied it free. Applied free here. The constitution still names no V-rule: the exception describes a closing unit's SHAPE and never mandates one. |
| **Rule 9** — WHICH SUBHEADING (v1.2) | **AMENDED, and at this stage it is the majority case** | §4(d). |
| **`task_brief` — no cap → ≤ 18 words** (v1.2) | **ADDED, on measurement** | §4(e). |
| **`activity_title` ≤ 10 → ≤ 12 · `section_context` 10–15 → 10–18** (v1.2) | **AMENDED, family alignment** | §4(e). The `section_context` move is recorded as **unforced** by preparatory's own corpus. |
| **Cancelled amendments A2/A3/A4, X3** | **ABSENT** | None introduced. Asserted by guard: `role_handoff`, `unit_handoff`, `band_ref`, "role weighting", `phase_ref`, `band_id` all 0 in both files. |
| **V-rules in a constitution** | **NONE** | No section registry, no verbatim-anchor mandate, no first-visit-order rule, no closing-synthesis mandate, no per-variant assessment rule, no INPUTS acknowledgment, no precedence line — asserted by guard (`section registry`, `reserved token`, `synthesis unit`, `closing synthesis` all 0). Worth restating because Rule 1's new closing-unit exception sits one sentence away from the brief's synthesis mandate and deliberately does not become it. |

---

## 2. P5 — stage inputs

**P5.1 · The floor.** Accepted at the standing ratio `round(0.6 × recommended_periods)`, **no
override anywhere in the class, or anywhere in the stage**. For ch 11 that is
`round(0.6 × 12) = 7`, matching `floor_periods_at_standard` on the row. Equal dispersion over
[7, 12]: A−C = 5 ≥ 4, so counts are `{A, ⌈(A+C)/2⌉, C}` = **[12, 10, 7]** — three canonicals,
three authoring runs.

> **The full-coverage arithmetic was swept before the rule was accepted** (the S8 rule: check
> every stated number against the whole stage's `cells × canonical_plan.counts`). A prep chapter
> with N cells needs **1 + ⌈(N−1)/2⌉** periods — `word_work` occupies a period alone (STEP 4),
> the rest pack at ≤ 2 adjacent — so a full 5-cell chapter needs **3**. Swept across **all 39
> preparatory chapters**, III, IV and V, not only the drawn class: **nothing binds, anywhere.**
> The lowest counts in the stage are the 2-period picture-reading chapters (III ch 5, 10, 14),
> and they carry 1–2 cells against a need of 1–2. The second stage running (after S10) where
> the sweep found nothing to raise, and the first where the whole three-class stage is clear.

**P5.2 · THE SECTION REGISTRY — inherited from S11, evidenced by S10, and unchanged here.**

The registry member is the **(section × spine) CELL**, token `"<section_id>|<spine_key>"`, both
halves closed authored vocabulary, joined for a multi-cell unit with the V2 joiner
(`B|writing / B|word_work`). First-visit order is the summary's on-page spine order, which
Rule 1 already forbids re-sequencing — **and it is NOT the canonical enumeration order the
handoff is keyed by; a C5 check that compares one against the other will fail a good plan.**

**What preparatory changes is the VOCABULARY, not the definition.** The spine set is **five**,
and three of the five keys differ from middle's:

| preparatory | middle / secondary |
|---|---|
| `reading` | `reading_for_comprehension` |
| `oracy` (listening **and** speaking merged) | `listening` · `speaking` |
| `writing` | `writing` |
| `word_work` | `vocabulary_grammar` |
| `beyond_text` | `beyond_text` |

Listening is not a spine at prep: it rides **inside `oracy`** as per-task `transcript_ref` +
`transcript_text`, and Rule 3 gives it its own timed bands. A C5 or C9 check written against
middle's six keys is wrong for every chapter of this stage.

**The registry for the pilot**, in first-visit order, is these five:

```
1. B|reading      (Let us recite, 1 task)
2. B|oracy        (Let us think + Let us speak, 2 tasks)
3. B|writing      (Let us think + Let us write, 4 tasks)
4. B|word_work    (Let us learn + Let us write, 3 tasks)
5. B|beyond_text  (Let us explore, 1 task)
```

Three notes carried into the C-cycle:

- **The section id is `B`, not `A`.** English III is fully split — 17 chapters, one
  `main_section` each — and the split kept each section's position in its original textbook
  unit, so the ids run A, B across a unit's chapters. Five of the seventeen are `B`, and the
  pilot is one. The same trap S10 recorded for VI, at a different ratio.
- **Three of the pilot's five cells carry a MERGED `section_name`** — *"Let us think + Let us
  speak"*, *"Let us think + Let us write"*, *"Let us learn + Let us write"*. Rule 9's new WHICH
  SUBHEADING clause is what makes them locatable; see §4(d).
- **Coverage feasibility at all three counts.** Five cells against 12 · 10 · 7 units: the
  richest cell (writing, 4 tasks) can fill 2–3 units at 12 and 1 at the floor, so the spread is
  comfortable at every count. **Five registry members against twelve units is the DENSEST
  cell-to-unit ratio in the english family** — secondary's pilot was six against seventeen —
  which makes the Xth-unit borrow at C8 more often a cell's *closing* unit than its opening
  one. Named here so C8 reads it as expected rather than as a finding.

**P5.3 · The pilot chapter.** `english|III` ch 11 *The Big Laddoo*. Summary and mapping both on
disk (`data/content/chapters/english/iii/{summaries,mappings}/ch_11_*.json`),
`placeholder: false`, `canonical_plan` present. The row:

```json
{"chapter": 11, "title": "The Big Laddoo (The Big Laddoo)", "weight": 11.5,
 "exact_share": 12.43, "recommended_periods": 12, "canonical_minutes": 480,
 "floor_minutes": 288.0, "floor_periods_at_standard": 7, "canonical_periods": [12, 10, 7],
 "placeholder": false,
 "canonical_plan": {"counts": [12, 10, 7], "provisional": true, "basis": "arithmetic",
                    "registry_sections": null, "authored": []}}
```

`provisional: true` / `basis: "arithmetic"` is the expected pre-C1 state; it finalizes to
`authored_standard` when `variant_plans.py annotate` runs inside C1.

**Chosen (founder, this session) for the POEM**, over ch 3 *Badal and Moti* (prose, section A,
identical band [12, 10, 7]) and the picture-reading chapters. The reasoning is §6's. **The cost
of the choice is named:** ch 11 is tied for the largest chapter in the class, so three authoring
runs at 12/10/7 are among the stage's most expensive; and the **picture_narrative** section
type — preparatory's own, four of III's seventeen chapters and exercised nowhere else in the
campaign — is **not** the pilot, and is left to the pre-warm sweep, the same way S11 left drama
and S10 left prose. Ch 11's band is the joint-widest, so C8 loses nothing.

**P5.4 · The three test identities' teaching profiles for class III. CLOSED** (founder, this
session, through the app's own first-run flow — not by hand-editing JSON). Verified on disk:

| identity | section | durations | ppw by duration | anchor |
|---|---|---|---|---|
| kumar1 | **3C** | [40] | {40: 5} | 40 |
| kumar2 | **3B** | [40] | {40: 5} | 40 |
| kumar3 | **3E** | **[40, 50]** | {40: 3, 50: 2} | 40 |

Sections are **disjoint**, which is the whole of X1's evidence. The mixed duration on kumar3 is
a **1.25× stretch (40 → 50)** — a canonical authored at 40 min served into a 50-minute sitting,
the ordinary Indian-timetable case, so C6 gets a realistic scaling test rather than an exotic
one; the same stretch S10 drew, where S11's was 1.2×. **So S9 enters its C-cycle with a clean
P5 and no amber at all** — the sixth stage to do so, after S6, S8, S5, S11 and S10, and the
first for which nothing was left open at sign-off. The "nothing left over from an earlier
stage" clause stays waived per the founder ruling of 2026-08-07 (S6); the residue touches no
english-III key.

**P5.5 · THE CARRIER — the one-line trace.**

> **rule 7 · period-field family · item (`source_section_id` + `source_spine`) → period
> (`section_id` + `spines_taught[]`) · container: a list of SPINE groups each carrying
> `items[]` · plugin method `EnglishSubject.assessment_to_view`, whose join, N-to-N pairing and
> section-wide fallback live in `english/subject.py::cell_resolver` · `genon_assessment`
> present (stage-agnostic, landed at S11) · **not in `_NOT_YET` as of 2026-08-13 — and
> `_NOT_YET` is now EMPTY**.**

Part 5 (where does the PERIOD keep its section anchor): `grep -c section_anchor` is **0** in the
english·preparatory LP constitution, so the read is mediated — `genon_unit_anchor` builds the
composite cell token (verified returning `'A|reading'` on a real saved period) and
`genon_anchor_field_present` returns **False**. The expensive half of that is visible in the
generated brief (§8): it asks for the `"synthesis": true` **boolean** and says in terms *"this
stage's periods have no field to hold a reserved token, so do not invent one"* — which is
precisely the metered-STEP-1 failure the S5 note was written to prevent. §3 is the confirmation
in full.

---

## 3. P5.5 in detail — the last entry, and the note that did the work again

`carriers._NOT_YET` did not say "english·preparatory is owed" and stop. S11 wrote it, S10
confirmed it, and it named **three things to confirm, not re-derive**, plus **one difference
specific to this stage**. All were checked against the REAL saved preparatory corpus by
`verify_s9_carrier.py`, which is re-runnable and is the P5.5 artefact:

| condition | result |
|---|---|
| the stage's **spine SET** matches the summary's — *"preparatory carries fewer than six"* | **37 readable chapters, 167 taught cells** across III/IV/V use the **five** prep keys and **nothing else**; all five are exercised; no middle-only key (`reading_for_comprehension`, `listening`, `speaking`, `vocabulary_grammar`) appears in the constitution as a KEY |
| the **assessment container** is still the spine-grouped list | all **4** saved preparatory plans: `{spine_code, spine_title, items[]}`, no other shape |
| the LP still emits **`coverage_handoff` as a spine-keyed DICT** | all 4: keys ⊆ the five spines, every value a `section_contributions` block — the shape `_ENGLISH_SPINE_CELL` round-trips |
| part 5 — the unit ANCHOR | `section_anchor` count **0**; `genon_unit_anchor` present and returning the composite token; `genon_anchor_field_present("english","iii")` is **False** |

**End to end on the real saved preparatory shape:** 4 plans, **18 items, ZERO orphans**, every
anchor equal to the independently computed *last unit teaching that cell*, with the N-to-N
pairing intact where a cell's item count equals its unit count.

**Why a different spine set costs nothing, and why that is now a test rather than a comment.**
No part of the carrier reads a spine NAME: `cell_resolver` joins whatever `spines_taught[]`
holds against whatever `source_spine` holds, and `genon_unit_anchor` composes the cell token
from both halves without a vocabulary. A carrier that had hard-coded the six middle keys — the
obvious shortcut when secondary was the only stage — would have passed S11 and S10 and failed
every chapter of this one. **So the deletion was again the whole job. No new code landed.**

**`_NOT_YET` IS NOW EMPTY, and the table is kept anyway.** The comment above it says why: an
empty table is not a dead switch but the pre-flight that makes `carrier_gap()` free, and the
next subject·stage brought into genon belongs in it **before** it is authored, not after it is
paid for.

**Tests.** `tests/test_genon_carriers.py` went **122 with 6 failures → 131, green.** The six
failures were exactly the "preparatory is still owed" assertions this step invalidates, spread
across four classes. Rather than delete the properties they protected, three were **kept alive
against an empty table by a synthetic entry** — the refusal machinery
(`TestUnimplementedFamiliesFailLoudly`), the stage/row reporting contract, and the conservative
gradeless read — because emptying the table would otherwise retire the pre-flight silently, and
the next subject would find out at certification, after paying. A new `TestEnglishPreparatoryLanded`
class of eight replaces them, on a **new fixture** (`tests/fixtures/english_iv_ch01_saved.json`,
a real saved IV plan). Its centrepiece is what neither sibling fixture has: **one plan
exercising both anchoring branches** — `word_work` taught across units 4 AND 5 with TWO items
(N-to-N: 4 and 5, not 5 and 5) beside `oracy` taught across units 2–3 with ONE item (the
last-unit rule: 3). Plus the explicit assertion that no middle spine key ever resolves here.

---

## 4. The constitutional findings — a wrong number, a licence, a contradiction, and three caps

**(a) A1 IS THE FINDING OF THIS PREP: the duration band was simply wrong.** Every other stage's
A1 replaced "one or more rows" with one row — a shape correction. This file needed that too,
but its real defect was the *number*. Three sites said 30/35:

- INPUTS 3: *"`period_duration_minutes` is 30 or 35 at prep (35 default)"*
- Rule 2 STEP 1: *"A 30-min period holds at most 2–3 tasks; a 35-min period holds 2–4."*
- the schema: `"period_duration_minutes": integer, // 30 or 35`

`master_plan.json` carries **english|III, english|IV and english|V at
`standard_duration_minutes: 40`** — the calibration band this campaign authors at, and the band
`FirstRun.jsx` and `YearPlan.jsx` already show a teacher. So the constitution named a duration
the platform does not use, and a library authored under it would have been at the wrong minute
count throughout — 12 × 35 = 420 minutes against the row's `canonical_minutes: 480`.

**It was live, not theoretical.** Three of the four saved preparatory plans carry MIXED
durations inside a single plan:

| plan | durations |
|---|---|
| iii ch 2 | 2 × 40 + 2 × 35 |
| iv ch 1 | 5 × 35 + 2 × 40 |
| v ch 1 | 3 × 35 + 2 × 40 + 1 × 30 |

That is exactly the shape A1 exists to make impossible, and it is the reason A1 is described in
testing.md as *doubly* load-bearing under the variant engine. STEP 1 now states the 40-minute
ceiling **alone** (2–3 tasks); naming no alternative is deliberate, because preparatory spans
one class-standard and a table of alternatives invites the author to branch on a number A1 has
already fixed. Verified downstream: the dry pre-flight assembles at **12 × 40 min**.

**(b) FULL SPINE COVERAGE replaces Rule 2 STEP 3's drop licence.** STEP 3 said: *"When the
section's allocated periods are exhausted, stop. Remaining spines/tasks are NOT forced into a
period … This is an honest reflection of available time, not a defect."* Under architecture
v2.0 that licenses a chapter's compacts to be a **different chapter** from its standard: a
library shares ONE registry, `briefs_for()` prints the standard's registry verbatim into every
compact's brief, and the Xth-unit choice set borrows *the unit that FIRST deals the next-due
cell* — which a compact whose registry is a subset does not have.

**The preparatory corpus does it.** `backup/saved_plans/english/iii/ch_01_*.json` is a 3-unit
plan whose handoff carries **3 of its summary's 5 cells** — writing and beyond_text never
arrive at all. Nothing forced it; the periods ran out and the rule permitted the stop. The
teacher-facing version of why that is wrong is the sentence now in the rule: *a class given
seven periods instead of twelve should still read, talk, write and play with words; it should
do less of each.* Curation moves to TASK level, where Rule 3 already governs it; unfitted TASKS
still go to homework or ride as flagged self-study pointers, because that half was always
honest. Rule 10 gained the matching corollary — **absent from the summary is a state, dropped
for time is a defect.**

**(c) Rule 10's item-count line was the third discovery of the same stale sentence.** It read
*"Total assessment items = total `section_contributions` across all spines (one item per
(section × spine) cell)"*. This stage's **own** assessment constitution v1.4 (2026-08-12) emits
**TWO**. S10 struck it at middle, filed secondary's as a §7 defect against a certified stage,
and wrote in its sign-off that *"preparatory carries the same line free and should strike it at
S9's P1 rather than let it be found a third time."* Struck, with the corollary the assessment
file already carries: **the item count does not vary with the period count** — a shorter plan
yields the same items tested on less anchored practice.

> **The general lesson has now cost three stages to learn once:** a cross-stage amendment that
> moves three assessment constitutions and none of the three LPs beside them leaves the pair
> disagreeing, and the LP's half is the one the generator reads while it writes the handoff.
> §5 shows the same amendment left a **fourth** copy outside both constitutions.

**(d) Rule 9 names WHICH SUBHEADING a merged cell uses — and at preparatory this is the
majority case.** S10 found this at middle, where **16 of 96** cells carry a MERGED
`section_name` (17%). At preparatory it is **93 of 167 (55%)**, and the longest runs to **28
words**:

> *"Let us Read + Let us Think A + Let us Think B + Let us Think C + Let us Think D + Let us
> Think E"*

That is longer by itself than any brief cap, before the brief begins. **The pilot's own writing
and word_work cells are both merged**, so this is not a tail risk for ch 11 — it is the rule's
ordinary operating condition. Left unsaid, Rule 9 is unsatisfiable on the richest cells in the
stage.

**(e) Three caps, and only one of them was forced.** Recorded separately because the discipline
matters (S4's lesson: a limit stated as a number is what live generation most often disproves,
and catching one at P1 is free):

- **`task_brief`: NO cap → ≤ 18 words INCLUDING the Rule 9 locator. FORCED, and it was a hole
  rather than a relaxation.** Preparatory stated no `task_brief` cap anywhere in the schema,
  against a Rule 9 that *mandates* the `"<Subheading> (pp.NN–MM): <plain brief>"` locator. Only
  **2 of 29** saved briefs carry a locator at all — the mandate postdates the corpus — so the
  raw distribution understates the real length. Simulating the locator at its true cost
  (+4 words: a 3-word subheading such as "Let us Learn" plus "(p.NN):") gives **max 16, 14 of
  29 over 12, 0 over 16**. So middle's *old* cap of 12 would have been unreachable, and 18 is
  the number secondary and middle both settled on independently. The family now carries one
  number.
- **`activity_title` ≤ 10 → ≤ 12. Family alignment on a SATURATED cap.** The preparatory corpus
  maxes at exactly **10** words of a 10-word cap; middle and secondary allow 12 against a
  corpus max of 11. A cap the corpus already sits on is one live generation away from being a
  defect report, and prep periods routinely name two spines.
- **`section_context` 10–15 → 10–18. Family alignment, and UNFORCED.** Preparatory's own corpus
  maxes at **13 of 15** and does not force the move. Taken so the field carries one number
  across the three english stages rather than three; recorded here as unforced so C3 does not
  read it as evidence-backed. Lower bound kept — the field is useless at two words.

**§9 — costs nothing.** A full constitution change on both files: three relaxations
(`task_brief` where none existed, `activity_title`, `section_context`) and four new obligations
(full spine coverage, the register, the 40-minute single row, the PAIR count). **No
english·preparatory library exists**, so nothing re-opens. S7 paid ~₹106 and a C1–C3 re-run for
the same class of finding.

---

## 5. The finding the dry pre-flight caught — the PROMPT BUILDER was still saying "one item per cell"

This one is not in a constitution and would not have been found by reading one. The dry run's
assembled prompt was swept for stale strings, and `one item per` came back **twice**, from
`genon/prompt_assembly.py` — the english LP+A prompt builder S11 lifted from the prototype:

- the output sketch's `assessment_items` block: *"<one item per section_contribution in
  coverage_handoff for this spine (Assessment Constitution Rule 2)>"*
- CRITICAL CONSTRAINTS: *"Total assessment item count = number of section_contributions … (one
  item per spine-cell implied_lo, per Assessment Rule 2) … Generate one original item per cell"*

Both cite Rule 2 **while contradicting it**. The 2026-08-12 PAIR amendment moved three
assessment constitutions; S10 and S9 moved two of the three LPs beside them; **nobody moved the
builder**, which sits between both and the model and is the text closest to the output schema.

**It is stage-agnostic**, dispatching on `subject_to_folder(subject)`, so it said this to
english·secondary and english·middle too.

**It did not bite at S10 — and that is the argument for fixing it, not against.** S10's authored
library came in at **12 items across 6 cells** in all three canonicals: the model followed the
constitution over the builder. That is a coin-flip resolved favourably once, on one chapter,
and the same file has already shown (curly quotes, ARV-D-1xx) that a model keeps a habit for a
whole run or drops it for a whole run.

**Fixed here, free, before C1**, and worded so it cannot go stale again: the builder now defers
to Rule 2 and its slot table as the sole authority on the count and the slot order, and says in
terms *"do not assume one"*. **This is a V-series / pipeline change, not a constitutional one,
so §9 does not fire** and no authored library re-opens — the fix makes the builder AGREE with
the constitutions S10 and S11 were authored under. Re-verified in a second dry run: `one item
per` and `Generate one original item per cell` both reach 0, `ASSESSMENT RULE 2` and `do not
assume one` present. Filed as a defect row so S10 and S11 can read it against their own C3/C4
item counts (§7).

---

## 6. The pilot is a poem, and that is the point — again

`docs/NCERT_copyright_review.md` finding **F2** is the campaign's sole open copyright finding:
`poem_text` in a chapter summary is the NCERT poem, not a paraphrase, and an item that quotes it
puts published verse into a **canonical** — the one artefact class that reaches the cloud. It
was closed on all three english assessment constitutions on 2026-08-12 (ARV-D-138): a poem
section's stimulus is a LOCATOR, `Read lines N–M on p.PP, beginning "<incipit>"`, incipit capped
at **eight words**, no ellipsis, lines copied into no field. Reading `poem_text` stays legal;
only reproduction is closed.

**Preparatory's half of that fix has never been exercised.** It was carried early, ahead of this
P-prep, on the reasoning that §9 re-authors nothing while no english library exists. Ch 11 is
the chapter that tests it: section B is a **poem**, `poem_text` carries **13 verbatim lines**
(*"If all the laddoos were one Laddoo, / What a great Laddoo it would be! …"*), and the summary
sits at **pp. 70–77**.

**What C3 must read on this pilot, specifically:**

- every poem-grounded item addresses the poem **by place plus an ≤ 8-word incipit**, never by
  transcription, and never with an ellipsis continuing the quotation;
- no poem line reaches `item_stem`, `visual_stimulus`, `suggested_answer` or any rubric field;
- the incipit cap holds under the **PAIR** — two items per cell means two chances to drift, and
  the slot-2 (production) item is the one with a reason to quote a line to work from;
- **the locator is a page number, and NCERT prints no line numbers on its poems** — ch 11's
  section is pp. 70–77, so a bare "lines 5–8" with no page is unusable and is a defect, not a
  style note;
- **preparatory's `reading` cell for a poem is `Let us recite`, a single task.** The
  recitation-shaped cell is the likeliest place for a stem to reproduce the verse "so the child
  can say it back", and it is the one cell where a locator feels least natural to write. Read it
  first.

**Preparatory needed only two edit sites where secondary needed five**, because it has no
EXTRACT_ANALYSIS "3–8 line verbatim extract" block — `visual_stimulus` is `"" | pipe-table` and
EXTRACT_ANALYSIS is not in its type set. So the surface being tested here is narrower than
secondary's, and correspondingly the whole of it: Rule 3's REQUIRED clause and its PROHIBITED
clause.

---

## 7. Defects and follow-ups raised by this prep

**ARV — two english·V chapter summaries are NOT PARSEABLE JSON.**
`data/content/chapters/english/v/summaries/ch_08_summary.json` (*The Decision of the Panchayat*,
line 50) and `ch_09_summary.json` (*Vocation*, line 14) both carry **unescaped straight double
quotes inside a JSON string value** — dialogue in the first (*`Who said to whom: a. "I sold only
the well, not the water."`*), a poem's own quoted speech in the second (*`the hawker crying,
"Bangles, crystal bangles!"`*). `json.load` fails on both, so **neither chapter can be read at
all** — not by the pipeline, not by the app, not by any check in this campaign. It is the exact
hazard the 2026-08-11 cross-stage curly-quote amendment closed on the LP *output* side, showing
up on the *input* side, in authored content, where no constitution reaches it. **Does not block
S9** — the drawn class is III and both files are class V — but it blocks those two chapters at
pre-warm and it means the P5.1 floor sweep covered 37 of 39 preparatory chapters, not all 39.
The repair is mechanical (escape or curl the inner quotes) and is a content fix, not a
constitutional one.

**ARV — `genon/prompt_assembly.py` contradicted assessment Rule 2's PAIR at all three english
stages** (§5). Fixed in this pass; recorded because **S10 is mid-cycle and S11 is CERTIFIED**,
and both authored under the stale text. S10's library happens to carry 12 items across 6 cells,
so it complied anyway; **S11's should be read at its own item count** before this is closed. No
§9 cascade — the builder is V-series.

**ARV (minor, standing) — kumar1's readiness path is tracked in git as `Kumar1/Kumar1/`.** The
directory on disk is lowercase and resolves correctly, but the git index carries the mixed-case
path from before testing.md §0.5 standardised on lowercase. Harmless on macOS, which is
case-insensitive; on Linux or Supabase it is the two-tenant split §0.5 warns about. Not caused
by this pass; noted because P5.4 was closed in it.

**The english prompt builder needs no lift.** S11 met `NotImplementedError` from
`prompt_assembly.build_lpa_prompts` at its C1 and lifted `_build_lpa_prompts_english` from the
prototype. It dispatches on `subject_to_folder(subject)`, not on stage, so S9 inherits it whole
— including the `phases` → `time_bands` rename P3 forces. **Verified free, before spending**, by
the dry pass (§8).

---

## 8. Dry pre-flight — C1 is unblocked at ₹0

`python3 genon/generate_canonical.py one english iii 11 --dry` assembles the real prompt without
an API call:

```
English · Grade III · ch 11 — 12 × 40 min (LP+A; constitution serve-era)
  schedule : Total: 12 periods · 8h 0min
  system   : 53,588 chars   user: 23,383 chars
```

**The `12 × 40 min` line is itself an A1 assertion** — under v1.1 the same command would have
assembled at a duration the master plan does not carry.

**Present in the assembled prompt**, asserted rather than eyeballed: **LP v1.2** ·
**assessment v1.5** · THE SELF-CONTAINED REGISTER · A1's "exactly ONE row", the master-plan
bands and "authored at 40 MINUTES" · FULL SPINE COVERAGE · Rule 1's CLOSING unit exception ·
Rule 9's WHICH SUBHEADING clause and BAND NARRATION · A9's "MCQ OPTION ORDER IS NOT YOURS TO
SET" · RULE 8A · the PAIR (TWO ITEMS PER SPINE-CELL) and its SLOT TABLE · "TWO per
`section_contributions`" · the poem locator (AT MOST EIGHT WORDS) and REPRODUCING THE POEM ·
`time_bands` / `"activity": string` in the output sketch · `≤ 18 words` · the builder's new
"ASSESSMENT RULE 2 … do not assume one" · and the pilot's `poem_text` (correctly — reading is
legal, reproducing is not).

**Absent:** `30 or 35` · `PHASE NARRATION` · any surviving `phases` key · `section_anchor` ·
`phase_ref` · `role_handoff` · `band_id` · `preview into next` · `the previous unit` ·
`one item per` · `alphabetic` · `never led with` · the middle-only spine keys
(`reading_for_comprehension`, `vocabulary_grammar`) · any stale VERSION 1.1 / 1.4 string.
The word **"phase"** survives once in the whole prompt, in the assessment constitution's DESIGN
PRINCIPLE — *"The English LP → Assessment arc has two phases"* — where it is the ordinary word
for a stage of a process and names no schema field. Left deliberately.

**`build_library.py`'s STEP 0 pre-flight passes** and `--certify-only` runs to *"Row is
provisional — author and certify the standard canonical"*, which is the expected pre-C1 state.
**The generated top brief is correct for a mediated-anchor stage:** it asks for
`"synthesis": true` as a **boolean** and says *"this stage's periods have no field to hold a
reserved token, so do not invent one"* — the metered-STEP-1 failure P5.5 part 5 exists to
prevent, visibly not happening.

**Test suites.** `test_genon_carriers` **131 green** (122 with 6 failures before) ·
`test_genon_serve` (all e14 assertions) · `test_genon_duration_order` · `test_lp_standard` ·
`test_calibrated_defaults` all pass. `test_genon_plan_key` fails — **confirmed pre-existing** by
re-running it against the stashed, unmodified tree.

---

## 9. What the C-cycle inherits

- **C1 is unblocked and carries NO gate.** P5.5 is closed, P5.4 is closed, STEP 0 passes, and
  the dry pass proves the prompt assembles under the new pair. Command:
  `python3 genon/build_library.py english iii 11`.
- **C3 has a named agenda beyond the rule table**: the poem locator under the PAIR (§6, and
  read `Let us recite` first); the three caps this pass moved or added — `task_brief` ≤ 18
  (new), `activity_title` ≤ 12 (was saturated), `section_context` 10–18 (**unforced**, so treat
  a breach as evidence about the number, not about the plan); and whether the builder fix
  actually produced **10 items for 5 cells** rather than 5 (§5 — this is the first library
  authored under the corrected text).
- **C5's registry checks read CELLS**, five of them, `B|<spine>` — **not `A|`**, and **not
  middle's six spine names**. First-visit order is the summary's on-page spine order, which is
  NOT the canonical enumeration order the handoff is keyed by; a check comparing one against the
  other will fail a good plan.
- **C5 check 11 (the summary reconciliation, new at template v2.10) GATES for this stage** —
  english summaries declare their sections in JSON `main_sections[]`, so it is one of the
  gating subjects, not an advisory one. The pilot declares exactly one, `B`.
- **C6's mixed-duration matrix has a 1.25× stretch** on kumar3 (40 → 50, ppw {40: 3, 50: 2}).
- **C8's transition inspection has five registry members against twelve units** — the DENSEST
  cell-to-unit ratio in the english family, so the Xth-unit borrow is more often a cell's
  closing unit than its opening one. Expected, not a finding.
- **C9.2's "a borrowed unit brings its own items" is vacuous for the closing unit**, inherited
  from S11 and S10 rather than new: a closing unit teaches no cell, so no item anchors to it.
  What C9 must check instead is that the standard's items and a compact's are the SAME five
  cells — which is what §4(b) is for.
- **The preparatory saved-plan corpus is on `phases`**, not `time_bands`. Display is covered by
  `_bands`' both-keys read; anything newly authored must emit `time_bands`, and `compile_stream`
  will refuse anything that does not.
- **The pilot does not exercise `picture_narrative`**, preparatory's own section type and four
  of III's seventeen chapters. Left to the pre-warm sweep, the way S11 left drama and S10 left
  prose.
- **No floor override is owed anywhere in this stage** (§2, P5.1) — the whole three-class sweep
  is clear.
- **Two class-V chapters cannot be read at all** until their summaries are repaired (§7).

---

## 10. Artefacts

| file | what it is |
|---|---|
| `apply_s9_amendments.py` | P1 + P3 + the measured edits — 27 guarded replacements, 22 absence guards, 16 presence guards |
| `lp_english_preparatory_v1.1_pre.txt` · `..._v1.1_to_v1.2.diff` | the LP before, and the diff |
| `apply_s9_assessment.py` | P2 (A6 confirm + A9) and P4's in-file half |
| `assess_english_preparatory_v1.4_pre.txt` · `..._v1.4_to_v1.5.diff` | the assessment before, and the diff |
| `verify_s9_carrier.py` | P5.5 — the three conditions, the spine-set difference, part 5, and the end-to-end run; re-runnable before and after the deletion |
| `tests/fixtures/english_iv_ch01_saved.json` | the new carrier fixture — one plan exercising both anchoring branches |
| `genon/out/canonical/english/iii/ch_11_*_promptdump.json` | the dry pre-flight (§8) |
| `genon/out/briefs/ch_11_top.txt` | the generated standard brief — the boolean-synthesis form |
| both `CHANGELOG.md` sidecars | P4 |
