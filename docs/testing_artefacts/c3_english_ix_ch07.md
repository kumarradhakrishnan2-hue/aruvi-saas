# C3 — rule-by-rule compliance · english · IX · ch 7 *Vitamin-M*

**Date:** 2026-08-12 · **Files:** `ch_07_canonical.json` (17 units, the standard) and
`ch_07_canonical_p10.json` (10 units, the floor compact) · **Constitutions:** LP **v1.2** ·
assessment **v1.4** · **Engine:** 19 · **Model:** claude-sonnet-4-6

The compact chosen is the **floor**, deliberately: it is where every stated number is under
most pressure, and where S11's own amendment (full spine coverage) actually binds.

**Maths sub-check: N/A.** English carries no `expected_answer` on any item — its closed items
are FILL_IN and TRUE_FALSE verified against the section text, and everything else is judged by
rubric. Same reason recorded at S1, S2, S3, S5 and S6.

---

> **FOUNDER RULING, 2026-08-12 (same day): all eight findings ACCEPTED AS AUTHORED.** No
> repair pass, no re-author, no constitution amendment. C3 is green on the library as it
> stands — none of the eight is structural and none gated the step. The six defect rows
> (ARV-D-128 … ARV-D-133) are marked `accepted` on the register rather than deleted, so the
> rate stays readable when S9 and S10 meet the same caps. **One item is accepted here but not
> settled:** ARV-D-132 is an authoring judgement at C3 and a SERVE question at C8, which
> inspects exactly that transition — acceptance here is not acceptance there.

## Verdict

**8 findings, none of them structural, and the library stands.** The two files obey the two-axis
model, the register, full spine coverage, the anchoring rule and the whole assessment answer
layer. What failed is almost entirely **numbers**: three word caps and a band-count minimum,
which is the same class of finding S4, S7 and S8 each met at their own C3 — and, in one case, a
cap this stage widened only this morning and live generation still overshot.

The one finding that is not about a number is **the synthesis unit's dependence on a draft
another unit produced** (§4). It breaches the platform brief rather than the constitution, and
it lands on precisely the unit the serve engine borrows.

| # | Finding | File(s) | Rule | Severity | Defect |
|---|---|---|---|---|---|
| 1 | Synthesis unit requires U15's draft article as `materials` | top | brief (V-series) | S2 | ARV-D-132 |
| 2 | Internal question-type codes (`MCQ`, `SCR`) in teacher-facing text | both | LP Rule 9 | S3 | ARV-D-130 |
| 3 | `shared-reading` runs three consecutive units | top | LP Rule 4 | S3 | ARV-D-129 |
| 4 | `expected_elements` bullets over 12 words (8 of 30) | both | Assess Rule 11 | S3 | ARV-D-131 |
| 5 | `section_context` 19 w and 23 w against 10–18 | p10 | LP Rule 10 | S3 | ARV-D-131 |
| 6 | One `task_brief` at 20 words against ≤ 18 | top | LP Rule 9 | S3 | ARV-D-131 |
| 7 | 2 bands on 4 of 10 units, minimum 3 | p10 | LP Rule 5 | S3 | ARV-D-128 (filed at C2) |
| 8 | `total_items` absent; `period_schedule` a dict here, a list there | both | Assess Rule 12 | S4 | ARV-D-133 |

---

## 1. Lesson Plan Constitution v1.2 — every rule, both files

| Rule | `ch_07_canonical.json` (17) | `ch_07_canonical_p10.json` (10) | Evidence |
|---|---|---|---|
| **VOCABULARY** | PASS | PASS | Zero occurrences of "period" or "session" in any `activity_title`, `teacher_notes`, band `activity` or `task_brief` across 27 units. The teacher-facing word is "unit" or nothing. |
| **REGISTER ban 1** — clock quantity | PASS | PASS | `register_scan` read 54 / 26 bands plus titles, notes, materials and homework: **0 ban hits**. Read by eye too: durations appear only in the band labels, never in prose. |
| **REGISTER ban 2** — forward reference / completion | PASS | PASS (soft note) | No "the next unit", no "as we will see", no completion claim. Backward continuity is legal at v1.10/v1.2 and is used well — U17: *"Grandpa's resentment of infantilisation, Ravi's comic surveillance, the birthday twist"* names CONTENT. **Soft note (p10 U10):** *"Having written about inspiring elders in the writing unit…"* names a unit by role rather than its content — legal (backward), below the stated best practice, and false for any serve that truncates below U9. |
| **REGISTER ban 3** — calendar time | PASS | PASS | No "today", "this week", "next class" anywhere. |
| **DESIGN PRINCIPLE** — two axes | PASS | PASS | One `main_section` (A · *Vitamin-M* · prose) at both counts; bin-packing is across (section × spine) cells, never across spines alone. |
| **INPUTS 3 (A1)** — one standard row | PASS | PASS **with a shape drift** | Top: `[{"period_duration_minutes": 50, "period_count": 17}]`. p10: `{"period_duration_minutes": 50, "period_count": 10}` — **a bare dict where its sibling has a list of one**. Same library, two shapes. → ARV-D-133 |
| **Rule 1** — two-axis anchoring | PASS | PASS | Exactly one `section_id` on every unit in both. Body units carry 1–2 spines adjacent in the on-page sequence. **U17 carries `[reading_for_comprehension, writing]` — NOT adjacent — and that is the v1.2 closing-unit exception firing on its first live run**, exactly as written ("may name as many spines as it genuinely revisits"). Without this morning's amendment the standard's mandated closer would have been unauthorable. |
| **Rule 1** — no re-sequencing | PASS | PASS | First-visit order = the summary's on-page order on both files (RFC → VocGram → Listening → Speaking → Writing → Beyond). Body runs are contiguous: top 1–8 / 9–12 / 13 / 14–15 / 15 / 16; p10 1–5 / 6–7 / 8 / 8 / 9 / 10. The only re-entries (RFC and Writing at U17) are the closing unit's revisit. |
| **Rule 2 STEP 1** — task budget | PASS | PASS | Ceiling at 50 min is 3–4 (the line added at v1.2). Top runs 0–2 tasks/unit; p10 runs 1–3. Neither approaches the ceiling — the constraint at this stage is text length, not task count. |
| **Rule 2 STEP 2** — proportional by page_count | PASS (vacuous) | PASS (vacuous) | One section, so the distribution is the whole budget. Recorded rather than skipped because a multi-section english chapter would exercise it and none in class IX does. |
| **Rule 2 STEP 3** — FULL SPINE COVERAGE | **PASS** | **PASS** | **The amendment this stage exists for, and it held at the floor.** All six spines taught in both files; six handoff cells; six items. The corpus plan that prompted the amendment (`ch_12`, 4 periods) had dropped `beyond_text` outright. |
| **Rule 2 STEP 4** — VocGram isolation | PASS | PASS | `vocabulary_grammar` appears alone in every unit that carries it (top U9–U12, p10 U6–U7). |
| **Rule 2A** — text reading is class time | PASS | PASS | Top U3 `[5–30]` *"Unhurried reading aloud of the story, pp.97–102"*, plus extract reads at U6/U7 and 'The Lost Child' at U16 `[10–30]`. p10 reads the story across U2 `[0–25]`, U3 `[0–20]`, U4 `[0–15]`. Sized to text length in both. `materials` carries a textbook page range on **27 of 27** units. |
| **Rule 3** — curate, don't exhaust | SUBJECTIVE PASS | SUBJECTIVE PASS | 21 of 23 summary tasks anchored (top), 19 of 23 (p10); every `task_index` in range; no task anchored twice. **The subjective half:** the rule asks that an unfitted task be flagged in `teacher_notes`, and neither file names its two/four unanchored tasks explicitly. The notes are content-rich rather than admin-rich, which reads better and satisfies the rule's spirit less literally. Not raised as a defect — the rule says "flag briefly", and at 21/23 there is little to flag. |
| **Rule 4** — one method per spine, from the permitted list | **FAIL** | PASS | Keys equal `spines_taught` on all 27 units; every method is drawn from that spine's permitted list (top uses 6 of the 9 permitted Reading methods). **The diversity clause fails on the top:** *"no spine's method may repeat across more than two consecutive periods"* — `shared-reading` runs **U3, U4, U5**. p10 is clean (5 distinct Reading methods over 5 units). → ARV-D-129 |
| **Rule 5** — time constraint | PASS | **FAIL** | Top: 17 of 17 units tile 0→50 exactly with ≥3 bands. p10: tiling exact everywhere, but **U2, U4, U5, U8 carry two bands** against a stated minimum of three. → ARV-D-128 (filed at C2) |
| **Rule 6** — chapter header | PASS | PASS | The MODEL emitted `grade · subject · stage · chapter_number · chapter_title · main_sections_inventory · periods_allocated` — verified in the raw output. **Note:** the installer reshapes into the saved-plan envelope and drops `stage`, `main_sections_inventory` and `periods_allocated`; nothing reads them (the port builds sections from the periods), so this is recorded, not raised. |
| **Rule 7** — no C-codes | PASS | PASS | `C-N.N` regex over the whole result: **0 hits** in both. |
| **Rule 8** — homework optional, located | PASS | PASS | 2 homework items per file, all within the 1–2 cap, every one carrying a page locator. |
| **Rule 9** — band narration | **FAIL ×2** | **FAIL** | **(a) Internal question-type codes in teacher-facing text**, which Rule 9 forbids by name: top U6 band 2 *"the emotion word choice (MCQ)"*, U6 band 3 *"unpacks both MCQ items"*, U7 band 2 *"the tone MCQ, why Ravi is confused and embarrassed (SCR)"*, U12 notes *"The four MCQ items on sentence type…"*; p10 U4 notes *"The MCQ on emotion — nostalgic vs. wistful vs. regretful"*. The rule's own remedy is in the rule: write "multiple-choice". → ARV-D-130. **(b)** One `task_brief` at **20 words** against the ≤18 cap this stage set this morning: *"Learning Beyond the Text (p.120–125): read 'The Lost Child' by Mulk Raj Anand; discuss with class — attachment vs. desire."* → ARV-D-131. Otherwise clean: 44 briefs, **all** carrying the `(p.NN)` locator, no task indices, no rule numbers, no schema keys. |
| **Rule 10** — coverage handoff | PASS | **FAIL (word cap)** | Both files emit all six spines in canonical enumeration order — which is deliberately NOT the walking order, and both orders are present and correct in both files. Every contribution carries all six fields; `implied_lo` follows the "Student …" form 6/6 in both; `tasks_anchored` populated; contributions = items = 6. **p10's `section_context` runs 19 w and 23 w against 10–18** (`beyond_text`: *"Mulk Raj Anand's 'The Lost Child' — a child's suppressed desires at a festival fair and his desperate attachment when separated from parents."*). The top is clean at 14–15 w. → ARV-D-131 |

---

## 2. Assessment Constitution v1.4 — every rule, both files

| Rule | Top | p10 | Evidence |
|---|---|---|---|
| **Rule 1** — present spines, canonical order | PASS | PASS | `[reading_for_comprehension, listening, speaking, writing, vocabulary_grammar, beyond_text]` in both; one section, so the within-spine `section_id` ordering is trivially satisfied. |
| **Rule 2** — one item per spine-cell LO | PASS | PASS | 6 contributions → 6 items in both. **The v1.4 invariance line held:** the floor canonical produced the same six cells and the same six items as the standard, tested on less anchored practice. |
| **Rule 3** — richness / grounding | SUBJECTIVE PASS | SUBJECTIVE PASS | Every item names a character, scene or line. Strongest: *"The story is titled 'Vitamin-M'. By the end of the narrative, Grandpa suggests that Ravi's mother is the one who needs it. What does this reversal reveal…"* — unanswerable without the story, which is the test. No generic stems, no textbook wording reproduced. |
| **Rule 4** — question type | PASS | PASS | Every type is in the closed set and inside its spine's default map: Reading → EXTRACT_ANALYSIS (both), Listening → TRUE_FALSE / FILL_IN, Speaking → ORAL_PROMPT, Writing → WRITING_TASK, VocGram → FILL_IN / SCR, Beyond → ECR. The TRUE_FALSE is correctly a TRUE_FALSE and not an MCQ — four independently judgeable declarative statements, `is_correct` per statement. |
| **Rule 4 / A9** — option order | PASS (barely exercised) | N/A | The A9 lines landed this morning and **this library contains no MCQ at all** — one options-bearing item across both files, the TRUE_FALSE, which STEP 6 re-ordered on the first pass. No option refers to another by label. So A9's prohibition is *satisfied* but its arrangement half is essentially untested here; the first MCQ-bearing english chapter is where to read it. |
| **Rule 5** — answer layer | PASS | PASS | Open items (EXTRACT_ANALYSIS, ORAL_PROMPT, WRITING_TASK, ECR) carry `expected_elements` and no `suggested_answer`; closed items (TRUE_FALSE, FILL_IN, factual SCR) carry a verified `suggested_answer` and no `expected_elements`. No item carries both. |
| **Rule 6** — verification | SUBJECTIVE PASS | SUBJECTIVE PASS | `verified: true` on 12 of 12. The listening item is answerable from the summary's baked-in `transcript_text` (the [SECONDARY DELTA] path) and I checked its four statements against that text; the rest are rubric-judged, where `verified` is true by rule. **Not re-derived** — english has no determinate-answer exposure (see the maths sub-check note). |
| **Rule 7** — fallback | N/A | N/A | No item failed verification, so no `[Verification failed]` stem exists. Recorded as N/A rather than pass. |
| **Rule 8** — source tagging | PASS | PASS | All six fields on all 12 items; `source_lo` and `source_context` **byte-identical** to the handoff cell they came from in every case. |
| **Rule 8A** — item anchoring (new at v1.4) | **PASS** | **PASS** | **The rule's first live test, and it held:** zero items emit `period_ref`, `period_number` or `unit_ref` in either file. The anchor is the pair `source_section_id` + `source_spine`, and the platform resolves it — which is what the carrier verified at P5.5 and what C1's serve sweep exercised. |
| **Rule 9** — visual stimulus | PASS | PASS | One `visual_stimulus` per file, both on the EXTRACT_ANALYSIS item, both verbatim extract blocks of 4 lines (within the 3–8 rule), no pipe characters, no SVG. Sub-questions are a numbered list in the stem, line by line. No lettered options inside any stem. |
| **Rule 10** — transcript reference | PASS | PASS | The listening item carries `transcript_ref` in both; no other item does. |
| **Rule 11** — rubric depth | **FAIL** | **FAIL** | Bullet counts are right (3–5 everywhere). **Word cap is not: 8 of 30 bullets exceed 12 words** — top 5 (2 in Q-RFC, 1 in Q-WRT, 2 in Q-BYT), p10 6. Example (16 w): *"The reversal shows Vidya, not Grandpa, misjudges — Vitamin-M targets assumption, not age."* → ARV-D-131 |
| **Rule 12** — header | **FAIL (partial)** | **FAIL (partial)** | `chapter_number`, `chapter_title`, `stage` and the inventory were emitted; **`total_items` was not**, in either file. → ARV-D-133 |
| **Rule 13** — no internal ids in prose | PASS | PASS | `Q-RFC-A-1`-style ids appear only in `id` fields; zero occurrences in any stem, answer, bullet or note. |

---

## 3. The pattern in the failures — and it is the campaign's standing lesson, again

Six of the eight findings are **a number the constitution states and live generation did not
respect**. Two of them are numbers *this stage set this morning*:

| cap | set at | corpus evidence used | live result |
|---|---|---|---|
| `task_brief` ≤ 18 w | S11's P1 (was ≤ 12) | 28 real IX briefs, max **19** | one brief at **20** |
| `section_context` 10–18 w | S11's P1 (was 10–15) | 11 real IX contributions, max **17** | **19** and **23** on the compact |
| `expected_elements` ≤ 12 w | untouched since v1.0 | never measured | **8 of 30** over, up to 16 |
| `time_bands` ≥ 3 | untouched since v1.0 | never measured | 4 of 10 units at 2, floor only |

**The P-prep measurement was right about the direction and short on the margin.** Widening from
the observed maximum is not the same as widening to what generation will do: the corpus was
authored under the OLD caps and had been pulled toward them, so its maximum understates the free
distribution. **The rule to carry to S9/S10: when a cap is widened on corpus evidence, set it
above the observed maximum by the margin the corpus itself was compressed by — or state the cap
as guidance and let the certifier count breaches instead of the constitution forbidding them.**

Note also what did NOT fail: every cap the model could satisfy structurally (the `(p.NN)` locator
on 44 of 44 briefs, the "Student …" LO form on 12 of 12, the 3–5 bullet count, one section per
unit, VocGram isolation). **Format obligations hold; length obligations drift.** That is a
usable distinction for every remaining constitution.

---

## 4. The finding that is not about a number — the synthesis unit imports a draft

**Top canonical, U17** (the mandated closing synthesis, and therefore the unit the serve engine
lends to other plans):

- `materials`: **`"Students' draft article (notebooks or draft sheets)"`**
- band `[30–50]`: *"Students **complete the draft article** 'Our Inspiring Elderly' (Paragraphs 3
  and 4 — overcoming challenges and concluding comment)… Those who have already completed the
  draft review it against the four-paragraph structure…"*

That draft is produced in **U15**: *"Students draft Paragraphs 1 and 2 independently."*

The standard-canonical brief is explicit: *"NO UNIT MAY DEPEND ON A PHYSICAL ARTEFACT ANOTHER
UNIT PRODUCES… A unit that lists 'prepared previously', 'their charts from earlier' or 'the
models they built' in `materials` is asking for a sitting that may not have happened."* U17 is
the Case-1 borrow: a teacher on 11 units receives p10's ten plus **this** unit, and p10's writing
unit (U9) asks for the *whole* four-paragraph article in one sitting. The borrowed closer would
tell that class to finish paragraphs they either never started or already finished.

**Two things make this precise rather than a general worry.** First, the model half-obeyed: the
band hedges ("Those who have already completed the draft…") and the teacher note says outright
*"Students need not have covered every task to participate: the chapter's content is now the
shared ground."* The prose understood the independence requirement; `materials` did not.
Second, `register_scan` cannot see it — the register bans clock quantities, forward references
and calendar time, and this is a **backward** dependency, which the register explicitly permits.
The artefact rule lives only in the brief, and nothing enforces it.

Filed as **ARV-D-132 (S2)**, flagged for **C8**, which inspects exactly this transition. The
cheap fix is a certifier check over `materials` and the opening band for artefact language —
free, subject-agnostic, and the third such check now owed (S7/S8's non-contiguous-section check
and C2's band-count check are the other two).

---

## 5. What C4 and C8 inherit

- **C4** should read MEMORY item 21's list against this run: the two word caps and Rule 11's
  bullets are now measured (§3), the `time_bands` conversion is confirmed live (54 / 26 bands,
  zero `phases` residue), and **the drama branch is still untested** — ch 7 is prose.
- **C8** has one joint to inspect and §4 names it: p10's ten units → the borrowed U17.
- **The MCQ path is untested at this stage.** No MCQ in either file, so A9's arrangement, the
  keyed `what_each_option_reveals` and the four-option contract are all unexercised. The first
  english chapter that produces one is where to look.
