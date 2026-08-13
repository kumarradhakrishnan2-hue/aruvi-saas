# C3 · Rule-by-rule read — english · III · ch 11 *The Big Laddoo*

**Files read:** `ch_11_canonical.json` (the standard, 12 units) and **`ch_11_canonical_p07.json`**
(the floor compact, 7 units). The floor was chosen as the C3 compact deliberately: it is where
FULL SPINE COVERAGE binds hardest and where a constitution that only holds at full length would
show. `ch_11_canonical_p10.json` is read only where a rule is swept across all three (Rule 2's
slot table, below) — each compact authors its own assessment, so a type rule is a three-file
question.

**Constitutions:** LP **v1.2** · assessment **v1.5** (both landed at this stage's P-prep,
2026-08-13; this library is the first authored under either).

**Maths sub-check (determinate answers):** **N/A** — english ships `expected_elements` /
`answer_key`, not `expected_answer`; the 2026-08-09 sweep scoped that check to S4/S7/S8.

**Verdict: 4 FAILS, 2 subjective fails, everything else passes.** No fail is structural — the
serve engine, the registry, the register and the anchoring are all clean (that is C1's report).
Three of the four point at a RULE rather than at the plan, and two of those are cross-stage.

---

## 1 · LP constitution v1.2

| # | Rule | top (12u) | p07 (7u) | Evidence |
|---|---|---|---|---|
| — | VOCABULARY + **THE SELF-CONTAINED REGISTER** (3 bans) | **PASS** | **PASS** | 0 hits on clock quantity, forward reference/completion, and calendar time, on both an independent scan and the certifier's own (49 and 34 bands read, plus `activity_title`, `materials`, `teacher_notes`, `homework`). Backward continuity is carried by CONTENT, as the register asks: *"Having heard the poem recited together, the class chants the final line…"* — never by a unit's position. |
| — | INPUTS 3 (**A1**) | **PASS** | **PASS** | `period_rows_snapshot` = one row `{40, 12}` / `{40, 7}`; every unit at 40 min. `period_schedule_display`: *"Row 1: 40 minutes × 12 periods = 480 minutes"*. |
| 1 | TWO-AXIS ANCHORING | **PASS** | **PASS** | `section_id` is `B` on every unit of both — no straddle. Top: 10 single-spine units; **u11 is the only ordinary two-spine unit** and it satisfies clause (d) exactly — `{reading: 1, oracy: 1}` in-class tasks, adjacent in the spine walk. **u12 uses the new CLOSING-UNIT EXCEPTION as written**: all five spines, `tasks_in_class: []`, teaching no cell of its own. p07 is single-spine throughout. |
| 2 · STEP 1 | task budget ≤ 2–3 per 40-min unit | **PASS** | **PASS** | Top task counts `[1,1,1,1,1,1,1,1,1,1,2,0]`; p07 `[1,1,2,2,1,2,1]`. Ceiling is 3; maximum reached is 2. |
| 2 · STEP 2 | proportional to `page_count` | **PASS (vacuous)** | **PASS (vacuous)** | The chapter is ONE `main_section` (B, pp. 70–77, `page_count` 8), so all periods go to it and "no section gets zero" is trivially met. Recorded as vacuous rather than passed — this rule is untested by a split-chapter stage and will stay so at preparatory. |
| 2 · STEP 3 | **FULL SPINE COVERAGE** (new at v1.2) | **PASS** | **PASS — and this is the one that mattered** | 5 of 5 summary cells carried in both, and in `p10` too. **Zero drops at the floor.** For contrast, the stage's own legacy saved plan `backup/saved_plans/english/iii/ch_01_*.json` carries 3 of 5 under the old drop licence. Task-level curation is where the pressure went, as the rule intends: p07 anchors 10 of the 11 summary tasks (`word_work` 2 of 3), the top anchors 11 of 11. |
| 2 · STEP 4 | word_work isolation | **PASS** | **PASS** | Top: `word_work` alone in u7 and u8. p07: alone in u6. It appears beside other spines only in the top's u12, which is the closing unit and teaches no cell. |
| 2A | TEXT ENCOUNTER IS CLASS TIME | **PASS** | **PASS** | Top u1 band `5–20`: *"Let us recite — teacher reads the poem aloud with full expression, once at normal pace and once slowly…"* — 15 min, in the FIRST unit, not a `tasks_in_class` slot. p07 u1 band `0–8` is the same act at 8 min. Rule 2A asks 6–10 min for a short prep poem; **the top's 15 min exceeds that band**, which reads as generous rather than wrong for a first encounter with a 10-line cumulative poem — recorded as a subjective pass, not a fail. `materials` carries a page range on **every unit of both files**. |
| 3 | TASK SELECTION | **PASS** | **PASS** | Every `{spine, task_index}` is in range against the summary's `tasks_verbatim[]` (0 out-of-range in either). No invented tasks. Band activities reference tasks by subheading + brief and do not restate `task_text`. **Listening clause does not fire**: the summary's two `oracy` tasks carry `transcript_ref: None` and empty `transcript_text`, so no listening band is owed. |
| 4 | PEDAGOGICAL METHOD | **PASS** | **PASS** | Every method in both files is drawn from its own spine's permitted list — 16 distinct methods in the top, 7 in p07, **zero outside the lists** (incl. `word-games`, which the list carries with its parenthetical). `pedagogical_methods` keys equal `spines_taught` on every unit. Diversity holds: no method repeats across more than two consecutive units in either file. ECR absent. |
| 5 | TIME CONSTRAINT | **PASS** | **PASS** | All 19 units tile 0..40 **exactly** — no gaps, no overlaps, no overrun. Band counts: top `[4×11, 5]`, p07 `[5,5,5,5,4,5,5]`. Minimum 3 satisfied; "typically 4–6" satisfied. |
| 6 | CHAPTER HEADER | **PASS** | **PASS** | The model emitted the full header — `chapter_number`, `chapter_title`, `stage: "preparatory"`, `grade`, `main_sections_inventory[{B, The Big Laddoo, poem}]`, `periods_allocated: 12`. **Note for readers of the installed file:** `build_library.py`'s install rewraps into the app's saved-plan shape, so these sit on the WRAPPER (or are dropped) rather than inside `result`. Read the ledger file in `genon/out/canonical/` to audit Rule 6, not the installed one. |
| 7 | COMPETENCIES DO NOT DRIVE LP | **PASS** | **PASS** | `grep -c 'C-\d'` = 0 across both whole files. |
| 8 | HOMEWORK IS OPTIONAL AND LIGHT | **PASS** | **PASS** | Top: 2 homework items across 12 units (u5, u8), max 1 each. p07: 1 (u4). **Every homework brief carries a page locator**, as the rule mandates — e.g. *"Let us learn (p.75–77): read the informational passage on festival foods…"*. |
| 9 | BAND NARRATION — the **Format** | **FAIL** | **FAIL** | See §3(a). The mandated shape `<spine_section_name> (“brief ≤ 10 words”)` appears in **1 of 49** bands (top) and **1 of 34** (p07), and both are incidental parentheticals rather than the format. **Cross-stage:** 1 of 47 at english·middle and 1 of 69 at english·**secondary**, which is certified. |
| 9 | BAND NARRATION — anchor naming (the rule's *requirement*) | **PASS** | **PASS** | What the model does instead satisfies "names the task by anchor location": 15 of 49 bands (top) and 9 of 34 (p07) name a `Let us …` subheading inline. **Every task-bearing unit of the top has at least one band naming its subheading**; p07 has one exception, u2. |
| 9 | **WHICH SUBHEADING** (new at v1.2) | **PASS** | **PASS** | Three of this chapter's five cells carry a MERGED `section_name` (*"Let us think + Let us speak"*, *"Let us think + Let us write"*, *"Let us learn + Let us write"*). **The merged string is used verbatim ZERO times** in either file; briefs name the single subheading — *"Let us think (p.72)"*, *"Let us write A (p.74)"*, *"Let us write B (p.74)"*. The clause added at P1 did exactly the job it was added for. |
| 9 | curly quotation marks | **advisory** | **advisory** | 0 curly marks in either file, but **0 straight DOUBLE quotes** too — the model used straight singles (`'SPLISH-SPLASH'`). The JSON hazard the v1.1 amendment exists to close is fully closed; only the stated mark is not the one used. The amendment is worded as a licence ("the straight form remains valid and is not a defect"), so this is advisory. For contrast, english·VI used 15 curly marks and english·IX used 0 — the family is inconsistent. |
| 9 | teacher-prose leaks | **FAIL (1)** | **PASS** | Top u6 `teacher_notes`: *"The blend words (pl-, cl-, bl-) connect to the **word-work spine** content…"* — `spine` is a schema key (`spines_taught`, `source_spine`) and Rule 9 bans "schema keys or planner identifiers" from teacher-facing prose. One occurrence; 0 in p07. |
| 10 | COVERAGE HANDOFF | **PASS** | **PASS** | All 5 spine keys present in both; every contribution carries `section_id`, `section_title`, `section_type`, `implied_lo`, `section_context`, `tasks_anchored[]`. `implied_lo` matches the mandated *"Student … using … as the vehicle."* form in all 10 contributions across the two files. `section_context` lengths 13–17 words (top) and inside 10–18 in both — the band widened at P1. **The PAIR corollary holds:** 10 items against 5 contributions in every file. |
| — | `task_brief` ≤ 18 words (added at v1.2) | **FAIL (2)** | **PASS** | §3(c). Top: 20 words — *"Let us think (p.72): write one sentence about what happened to the laddoo after it was thrown into the sea."* — and 19 words at u8. **Both are HOMEWORK briefs.** In-class briefs max at 14. |
| — | `activity_title` ≤ 12 (relaxed at v1.2) | **PASS** | **PASS** | Maximum 10 words (*"Think and Discuss — Chores, Gratitude, and Words for Father"* is from the legacy corpus; this library's longest is *"What Did Meena Say? — Guided Conversation and Role Play"*, 10). The relaxation from 10 to 12 was not needed by this chapter but is not contradicted by it. |

---

## 2 · Assessment constitution v1.5

| # | Rule | top | p07 | Evidence |
|---|---|---|---|---|
| 1 | PRESENT SPINES ONLY | **PASS** | **PASS** | Spines with contributions == spines emitting items, in both: all five. |
| 2 | **TWO ITEMS PER SPINE-CELL** — count, order, shared LO | **PASS** | **PASS** | 10 items = 2 × 5 contributions in **all three** canonicals, at 12, 10 and 7 units — assessment v1.4's invariance line proved live. Both items of every pair share `source_lo` and `source_context`. Slot 1 precedes slot 2 in every group; no interleaving. No pair shares a `question_type`. |
| 2 | **THE SLOT TABLE** | **FAIL (1)** | **FAIL (2)** | §3(b). Swept across all three files: `writing` slot 1 is **FILL_IN in 3 of 3** where the table prescribes SCR; p07's `beyond_text` slot 1 is FILL_IN where the table permits MATCH only; p10's `reading` slot 2 is ORAL_PROMPT where the table prescribes SCR. The DEMAND axis is satisfied in every case (recognition then production) — it is the TYPE column that is breached. |
| 3 | RICHNESS — grounding | **PASS** | **subjective FAIL (1)** | Top: every item names a character, image or concept from the section. p07 `Q-WORD-B-2`: *"Think about a laddoo you have seen or eaten. Say two sentences that describe it… Use words that tell us more about the laddoo."* — this is **answerable without reading the section** (Rule 3's first prohibition) and does not NAME the word_work concept as the rule requires for that spine. The top's counterpart does both: *"Think of the giant laddoo in the poem — round, sweet, and enormous. Choose TWO **describing words**…"*. Subjective because "grounded" is a judgement; the quoted strings are what it rests on. |
| 3 | **THE POEM LOCATOR** (ARV-D-138) | **PASS** | **PASS — and this is the item the pilot was chosen for** | p07 `Q-READ-B-1` is the mandated form exactly: *`Read the stanza on page 70 beginning "If all the laddoos were one Laddoo". What does the poet imagine in this stanza?`* — page reference ✓, incipit in double quotes ✓, **7 words** against a cap of 8 ✓, no ellipsis ✓, and no poem line reaches `visual_stimulus`, `suggested_answer` or any rubric field in either file. **A nuance worth carrying:** this poem's lines run 4–9 words, so a *compliant* 8-word incipit can BE a whole line. A scanner looking for reproduced lines flags this item; reading clears it. That is the mirror of the copyright review's own caveat ("an 8-gram scan is blind to a compliant incipit") and it means **C14 on a preparatory poem chapter cannot be automated in either direction.** |
| 4 | QUESTION TYPE | **PASS** | **PASS** | All types in the permitted set; **ECR absent** from both. TRUE_FALSE vs MCQ disambiguation respected (the top's one TRUE_FALSE judges a declarative statement; MCQs do not). |
| 4 | **A9** — option order | **PASS** | **PASS** | Zero by-label option references ("both A and B", "none of the above", "all of the above", "either B or C") anywhere. Every MCQ carries exactly 4 options with exactly one `is_correct`. See §3(d) for what the arrangement pass found. |
| 5 | ANSWER LAYER | **PASS** | **PASS** | MCQ `suggested_answer` is `""` in every case, with `what_each_option_reveals` keyed to **exactly the three incorrect labels** and omitting the correct one. MATCH carries a structured `answer_key` array of `{left, right}` plus a short string fallback. No CLOSED item carries `expected_elements`; no OPEN item carries `suggested_answer`. |
| 6 | ANSWER VERIFICATION | **PASS** | **PASS** | `verified: true` on all 20 items across the two files. (Standing caveat from ARV-D-084: `verified` is the model's claim about itself. English carries no determinate `expected_answer`, so the maths re-derivation sub-check does not apply — but the claim is not independent evidence.) |
| 7 | FALLBACK | **N/A** | **N/A** | No verification failure; `note` is `""` on every item, which is correct — `note` is reserved for the fallback only. |
| 8 | SOURCE TAGGING | **PASS** | **PASS** | All six source fields populated on all 20 items. |
| 8A | **ITEM ANCHORING** | **PASS** | **PASS** | The anchor is the CELL, carried by `source_section_id` + `source_spine` alone. **`period_ref`, `period_number` and `unit_ref` are emitted nowhere** — the prohibition A6 confirmed at P2 holds on its first live outing. |
| 9 | VISUAL STIMULUS | **PASS** | **PASS** | Three items per file carry a visual, and every one is a pipe-table (`Q-WRIT-B-1`, `Q-WORD-B-1`, `Q-BEXT-B-1`). No other stimulus form appears. |
| 10 | TRANSCRIPT REF | **PASS (vacuous)** | **PASS (vacuous)** | The summary's `oracy` tasks carry `transcript_ref: None` and empty `transcript_text`, so both oracy items correctly carry `transcript_ref: ""`. **The listening path is untested by this pilot** — a chapter with a real transcript is owed to the pre-warm sweep. |
| 11 | RUBRIC DEPTH | **FAIL (2)** | **PASS** | §3(c). Top `Q-ORAL-B-2` bullet at **10 words**, `Q-WORD-B-2` bullet at **9**, against Rule 11's *"3 bullets, each ≤ 8 words"*. Bullet COUNT is 3 everywhere in both files. p07's six open items are all inside 8. |
| 12 | HEADER | **partial** | **partial** | Everything present except **`total_items`, which the model never emitted at all** (`grep -c total_items` = 0 in the raw generation output). §3(e). |
| 13 | NO INTERNAL IDS IN TEACHER PROSE | **PASS** | **PASS** | No `Q-…` identifier appears in any stem, suggested answer, expected element or note. |

---

## 3 · The findings, and which of them are about the RULE

### (a) Rule 9's narration FORMAT has never been followed by any english library — including a certified one

Rule 9 mandates `Format: <spine_section_name> (“brief ≤ 10 words”)`. Measured:

| library | bands | bands in the mandated format |
|---|---|---|
| english III ch 11 top (this) | 49 | **1** (incidental) |
| english III ch 11 p07 (this) | 34 | **1** (incidental) |
| english VI ch 8 top (S10, mid-cycle) | 47 | **1** |
| english IX ch 7 top (S11, **CERTIFIED**) | 69 | **1** |

Four libraries, three stages, 199 bands, essentially zero compliance. What the model writes
instead is the anchor named inline in prose — *"Let us recite — teacher reads the poem aloud
with full expression…"*, *"Under “Let us read,” students recite the poem aloud together…"* —
which satisfies the rule's stated *requirement* ("names the task by anchor location + brief")
but not its stated *Format*.

**This is the S4 lesson, and the evidence points at the rule.** `time_bands[].activity` is the
narrative of what happens in those minutes; a rule demanding it be `Let us recite (“choral echo
reading”)` would empty the timed spine of content. The Format line reads like a spec for a
terse label and plausibly predates the field's current role — it survived P3's rename
unexamined, at this stage and at both siblings. **Filing it, not repairing the plan.**

### (b) The assessment slot table is breached in one consistent place and two one-offs

| file | spine | emitted | table |
|---|---|---|---|
| top · p10 · p07 | `writing` slot 1 | **FILL_IN** ×3 | SCR |
| p07 | `beyond_text` slot 1 | **FILL_IN** | MATCH |
| p10 | `reading` slot 2 | **ORAL_PROMPT** | SCR |

The `writing` breach is **3 of 3** and content-driven: this section's writing tasks *are* sorting
and column-filling (*"write round things in 'can eat' or 'cannot eat' columns"*), so a FILL_IN
tests what was taught and an SCR would have to invent a different task. The DEMAND axis is
satisfied everywhere — slot 1 recognises, slot 2 produces — and Rule 2's own demand wording
includes "completes", which is what FILL_IN is. So the table and the demand axis disagree with
each other on this cell.

The two one-offs are different: p10's `reading` slot 2 as ORAL_PROMPT loses the written response
the reading spine is meant to elicit, and p07's `beyond_text` FILL_IN is simply not in the set.
**Recorded as a fail with the rule-vs-plan question named**; the founder's call is whether
`writing` slot 1 should admit FILL_IN or whether the model should be held to SCR.

### (c) Three numeric limits, first live test — and two of the three bent

- **`task_brief` ≤ 18** (added at P1, where the constitution had NO cap): **2 breaches, at 19 and
  20 words, and both are HOMEWORK.** In-class briefs max at 14. A homework brief has to stand
  alone without the teacher's voice, which is exactly why it runs longer — and P1's simulation
  measured in-class briefs only. The cap is one word short of the evidence, and the evidence
  says homework wants its own number.
- **Rule 11 `expected_elements` ≤ 8 words**: 2 of 6 open items in the top at 9 and 10.
  Preparatory's ≤ 8 is the **narrowest rubric cap in the english family** (middle 3–4 / ≤ 10,
  secondary 3–5 / ≤ 12) and had never been exercised. It bends immediately, by 1–2 words, on
  bullets that are not padded: *"Describes at least one sense — taste, smell or texture."*
- **`activity_title` ≤ 12** (relaxed from 10 at P1): **not needed** — this library's longest is
  10. The relaxation stands unexercised, which is the honest record of it.

### (d) A9 got emphatic evidence, and it belongs in this table too

Across the whole library the correct option was authored at **position B in five of five**
MCQ/TRUE_FALSE items; the deterministic sort scattered them to C, D, B, C, B. The model cannot
produce the randomness the removed MEMORY item-18 prohibition asked for — which is the whole
argument for A9's removal-plus-two-lines and for the sort being a pipeline stage.

### (e) `total_items` was never emitted

Rule 12 asks for it; `grep -c total_items` on the raw generation output is **0**. Nothing
downstream reads it (the certifier counts items itself), so it costs nothing today — but a rule
nothing enforces and nothing consumes should either be enforced or struck, and this is the first
time anyone has looked.

---

## 4 · What C4 onward inherits

- **The listening path is untested** — this chapter's `oracy` tasks carry no transcript, so
  Rule 3's listening-band mandate and Rule 10's `transcript_ref` are both vacuous passes. A
  transcript-bearing chapter is owed at pre-warm.
- **Rule 2 STEP 2 (proportional allocation) is untestable at preparatory** — every chapter here
  is one `main_section`.
- **`picture_narrative` is unexercised**, as P5.3 recorded when the poem was chosen.
- **Read Rule 6 / Rule 12 headers in the LEDGER file**, not the installed one: the install
  rewraps into the app's saved-plan shape and moves or drops header fields.
