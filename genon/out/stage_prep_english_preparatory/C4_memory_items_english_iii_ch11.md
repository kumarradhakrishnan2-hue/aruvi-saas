# C4 · MEMORY.md amendment items, live — english · III · ch 11

Read across **all three canonicals** (12 · 10 · 7), since several items are per-file contracts
and each compact authors its own assessment. Applicability taken from testing.md §4's map and
re-checked against the live `MEMORY.md` §"★ AMENDMENTS TO BE TESTED" text.

**Verdict: 8 items pass, 1 fails, 1 fails-with-its-own-escalation-clause, 7 N/A, 2 already
closed.** Two of this stage's three fails were already visible from C3 and are recorded here
against the item they actually belong to; one — item 8's FILL_IN answer contract — is new, and
it is **this stage's own item, never exercised by anything before today.**

---

## The table

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | `guide.{TYPE}` nesting | **N/A** | SS + TWAU only. |
| 2 | English MCQ option-reveals — keyed map, not prose `note` | **PASS** | All **5** MCQ/TRUE_FALSE items across the three files carry `what_each_option_reveals` as a **dict keyed to exactly the incorrect labels**, with the correct one omitted; `note` is `""` on every one and `suggested_answer` is `""` on every MCQ. The item's worry was that "mirroring the rewrite into the generation prompt wrappers is explicitly still deferred" — **the generation prompt now produces the keyed shape unaided**, so the deferred mirror is no longer owed for english·preparatory. |
| 3 | Constitution exact-counts audit | **PASS** | 5 contributions → **10 items in all three files**. English's count rule is structural (2 × contributions), so there is no per-competency slate to miss. **But note the SS·secondary parallel exactly holds:** its C4 found *"counting is solved… slot-type resolution is a separate deterministic pre-step the model does not run"* — and this stage's C3 found the same split, with counts perfect and the SLOT TABLE breached 4× (ARV-D-146). Counting is solved at english too; slotting is not. |
| 4 | English Unit→true-chapter splits — **grade III** | **PASS — and III was owed by S9** | The split contract is reproduced on all three canonicals: title **`"The Big Laddoo (The Big Laddoo)"`** in the `<section> (<unit>)` form; `main_sections_inventory` a single entry `{B, "The Big Laddoo", poem}`; **`section_id: "B"` on all 29 units** across the three files; the singleton-section collapse putting SPINES at the top of `coverage_handoff`. Period spread 12 for an 8-page section, consistent with `effort_index` 11.5. **`B`, not `A` — the second stage to confirm S10's trap** (III is fully split, 17 chapters, ids running A/B across a Unit's chapters; five of the seventeen are `B`). **Grades VII and VIII remain owed** — both are true multi-section classes, which neither IX, VI nor III exercises. |
| 5 | English-middle Step 7d effort-index | **N/A** | english·middle only. |
| 6 | "Wire time into the constitutions" | **CLOSED BY DESIGN** | Already recorded in MEMORY.md at SS·secondary's C4 (2026-08-02). A1 fixes one standard row; the serve engine owns every timetable variation. This library is the ordinary case: one `{40, 12}` row, and X=5→14 all served from it. |
| 7 | `Period.approach` empties | **N/A (checked anyway)** | Scoped to maths·prep + SS. Checked regardless because english is a joiner stage: `pedagogical_methods` is populated on **every unit of every file** with keys equal to `spines_taught`, so the port's join into `Period.approach` has something to read on all 29 units. No empties. |
| **8** | **English (preparatory) FILL_IN + MATCH shapes** | **MATCH PASS · FILL_IN FAIL** | **This stage's own item, and the first time anything has tested it** — MEMORY records *"there is in fact NO English-prep saved-plan corpus on disk to have even back-checked it against"*. See §2. |
| 9 | Jul 12–13 wave — `assessment/english/preparatory` v1.0 bullet | **PASS** | Its four check-bullets, live: MATCH structured `answer_key` + fallback string ✓ (5 of 5); FILL_IN one cloze set, no Part A/B ✓ (4 of 4); MCQ `suggested_answer: ""` + `what_each_option_reveals` one per incorrect option, `note` reserved ✓ (5 of 5); Rule-7 failed-item path **not exercised** — no verification failure occurred, so `item_stem: ""` emission is still untested. ECR banned and absent. |
| 10 | "NAME THE REFERENCED WORD" | **N/A** | english middle + secondary only. |
| 11 | English LP homework `(p.NN)` locator | **PASS — including the fallback the item names** | All **4** homework briefs across the three files carry a locator: `(p.72)`, `(p.75–77)`, `(p.74)`, `(p.77)`. **No task in this chapter carries a `page_ref`**, so all four exercise the *section-range fallback* the rule specifies — the exact path the item asks to confirm, and it is confirmed rather than inferred. Zero locator-less homework briefs. |
| 12 | FILL_IN table anti-duplication | **PASS** | **Zero pipe characters in any `item_stem`** across all three files; every FILL_IN and MATCH table lives entirely in `visual_stimulus`; one table per item. The stems are instruction-only (*"Match each male animal on the left with its female counterpart on the right."*). See §2 for an inconsistency *adjacent* to this rule that does not breach it. |
| 13 | Narrowed "no Part A/B" ban | **PASS (vacuous)** | No FILL_IN in any file splits into parts at all — `grep 'Part [AB]'` = 0 — so the narrowed rule is satisfied trivially. **The narrowing is therefore still unexercised:** nothing here tests whether a legitimately multi-part *textual* FILL_IN is produced and permitted. Owed to the pre-warm sweep. |
| 14 | Maths number-line stimulus | **N/A** | maths prep + middle. |
| 15 | Maths homework `book_ref` | **N/A** | maths. |
| 16 | Maths middle `inclusivity` | **N/A** | maths middle. |
| 17 | SS middle `teacher_notes` | **N/A** | SS middle. |
| 18 | MCQ position spread | **CLOSED BY THE PIPELINE — and this library is the sharpest evidence yet** | See §3. |
| 19 | The CURLY-QUOTE narration format | **FAIL, and the item's own escalation clause fires** | See §3. |
| 20 | TWAU assessment v1.5 | **N/A** | TWAU. |
| 21 | english·secondary LP v1.2 + assessment v1.4 | **N/A** | S11's stage. |
| 22 | POEM LOCATOR carried early (prep + middle) | **PASS** | The item asks C1/C3 of *the first POEM chapter at either stage* to confirm three things. Middle confirmed at S10; **preparatory confirms here**: no poem line in `item_stem`, `visual_stimulus`, `suggested_answer` or any rubric field in any of the three files; the one locator-bearing item carries a **7-word** incipit against a cap of 8; no ellipsis continuation. Full evidence in the C3 table. |
| 23 | THE PAIR, all three stages | **PASS on every clause except the slot table** | See §4. |

---

## 2 · Item 8 — the FILL_IN half fails, and it fails for the same reason C3's slot breach happened

This item has been on the checklist since 2026-07-13 with the note that it could not even be
back-checked, there being no english-prep corpus. It is now tested.

**MATCH — PASS, cleanly, 5 of 5.** Every MATCH item carries a structured
`answer_key: [{left, right}, …]` (4–6 pairs) **plus** the short fallback string the rule asks for
(`"1-Hen, 2-Lioness, 3-Peahen, 4-Cow, 5-Duck."`), with the pipe-table living entirely in
`visual_stimulus` and the stem carrying only the instruction. Never a prose paragraph, never
inline-glossed pairs. That is the whole MATCH contract, satisfied on first contact.

**FILL_IN — FAIL on the answer shape.** The rule: *"`teacher_guide.suggested_answer` = each
blank's answer **numbered to its blank**."* What all four FILL_INs actually emit is
**column-grouped or object-keyed prose**:

> `That can be eaten: Apple, Orange, Grape. That cannot be eaten: Football, Globe, Coin.`
> `Typical results: paper — float (initially), stone — sink, leaf — float, pencil — float, …`

**There is nothing to number, because these are not cloze items.** They are a two-column sorting
table and a predict-and-record grid. "Each blank's answer numbered to its blank" presumes a
numbered cloze; the content the model was given has none.

**This traces to the same root as ARV-D-146.** FILL_IN was chosen for `writing` slot 1 in 3 of 3
files where the slot table prescribes SCR — because this section's writing tasks *are* sorting
and column-filling. The type choice then drags in FILL_IN's own answer contract, which the
content cannot satisfy either. **One decision, two rule breaches.** Whatever is decided about
ARV-D-146 decides this too: if `writing` slot 1 legitimately admits FILL_IN for sorting content,
then item 8's "numbered to its blank" needs a second permitted shape for non-cloze FILL_INs.

**One inconsistency adjacent to item 12, recorded because the two files disagree with each
other.** The top puts the word box **in `item_stem`** (*"Look at the words in the box and sort
them… Apple Football Orange Globe Coin Grape"*) while p07 puts it **inside `visual_stimulus`**
(*"Word box: orange, football, balloon, …"*). Item 12's rule governs *the table*, and neither
file reproduces the table in a stem — so this is not a breach. But the same chapter answered the
same question two ways, and p07's is the better artefact: it also gives real blank rows
(`___ | ___` ×3) where the top gives a single placeholder row (`(write words here)`).

---

## 3 · Items 18 and 19 are the same finding at the same site, from opposite directions

**Item 18 — closed by the pipeline, and this library is the sharpest evidence in the campaign.**
Across the three files the correct option was authored at **position B in five of five**
MCQ/TRUE_FALSE items; STEP 6 scattered them to C, D, B, C, B. The original item was written
because SS and Science clustered on one letter per chapter; english was dismissed then as having
"too few MCQs per chapter to judge". Five of five is a small sample but a perfect one, and it
says the clustering is not subject-specific — it is what the model does. **Note the recorded
closure in MEMORY.md is a version stale:** it describes A9 as a *convention* ("arrange…
alphabetically, never led with"), which was struck at assessment v1.7 on 2026-08-03 when
ordering became `genon/normalize_options.py` STEP 6. The closure holds; its stated mechanism
does not.

**Item 19 — the curly-quote narration format FAILS live, and the item told us what that means.**

| library | curly `“` | straight double `"` |
|---|---|---|
| english III ch 11 top / p10 / p07 | **0 · 0 · 0** | **0 · 0 · 0** |
| english VI ch 8 (S10) | 21 | 0 |
| english IX ch 7 (S11) | 0 | 0 |

The model wrote **111 / 168 / 71 straight SINGLE quotes** instead. So:

- **The amendment's PURPOSE is fully met** — zero straight double quotes anywhere, in any english
  library. The JSON escape hazard that cost maths III ch 5 ₹40.72 cannot occur.
- **The amendment's FORMAT is not met**, at two of the three english stages.

Item 19 states its own escalation in terms: *"If it comes back with straight quotes anyway, the
Format line is not where the model is taking its cue and the amendment needs re-siting, not
re-wording."* **It came back with straight quotes.** The model's operative cue is "do not put a
double quote inside a JSON string", which it obeys perfectly — not "use U+201C".

**And this is the same conclusion C3 reached from the other end.** ARV-D-145 found Rule 9's
*narration Format* (`<subheading> (“brief ≤ 10 words”)`) followed by 1 of 199 bands across three
stages. The curly marks and the parenthetical shape are **the same two lines of the same rule**.
Two independent measurements now say Rule 9's Format block is not load-bearing on generation.
Anything that block is relied on to guarantee should be re-sited into a line the model does read.

---

## 4 · Item 23 — the PAIR, clause by clause

Every clause the item asks C1/C3 to confirm, checked across all three files (15 pairs):

| clause | result |
|---|---|
| exactly 2 items per contribution, never 1 or 3 | **PASS** — 15 of 15 |
| slot 1 emitted BEFORE slot 2; contributions never interleaved | **PASS** — the platform's dispersion depends on this |
| the two items differ in `question_type` | **PASS** — 15 of 15 |
| both carry the SAME `source_lo` / `source_context` | **PASS** — 15 of 15 |
| the pair takes DIFFERENT strands of a compound `implied_lo` | **subjective PASS** — clean where the LO is genuinely compound: `word_work`'s *"identifies describing words… **and** matches male-female animal pairs"* is split MATCH→animal pairs, ORAL_PROMPT→describing words. Weaker on `reading`, where slot 1 and slot 2 both lean structure/comprehension. |
| at preparatory the pair stays LIGHT — no two WRITING_TASKs, oral preferred for slot 2 | **PASS** — zero double-WRITING_TASK pairs; **slot 2 is ORAL_PROMPT in 11 of 15** |
| types drawn from the SLOT TABLE | **FAIL — ARV-D-146**, 4 breaches |

The simulation MEMORY recorded (ratio 0.35 → 0.71 etc.) predicted the density fix would work.
**Live, at preparatory, the ratio is 10 items / 12 units = 0.83 at the top and 10 / 7 = 1.43 at
the floor** — comfortably clear of the 0.35 that caused the amendment, and above TWAU's 1.0 at
the floor.

---

## 5 · What this C4 raises

Three defects (§7): the p10 homework schema breach, item 8's FILL_IN answer contract, and item
19's format failure. Two items remain **owed elsewhere** and are recorded so they are not
mistaken for done: item 4's grades **VII and VIII** (the true multi-section classes, which no
stage has exercised) and item 13's narrowing (no multi-part textual FILL_IN was produced here),
plus item 9's Rule-7 fallback path, which needs a verification failure to test and did not get one.
