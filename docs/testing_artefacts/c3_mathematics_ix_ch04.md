# C3 — rule-by-rule compliance · mathematics · IX · chapter 4 "Exploring Algebraic Identities"

**Files checked (both, every numbered rule):**
`ch_04_canonical.json` — the STANDARD, 15 × 50 min, 14 items
`ch_04_canonical_p12.json` — the MID compact, 12 × 50 min, 13 items
*(p12 chosen over p09 deliberately: it is the compact the serve sweep uses most — identity at
X=12, prefix at X=10/11 — and it is the file STEP 6 flagged. p09 is quoted only where it
corroborates or contradicts a pattern.)*

**Checked against:** LP constitution **v1.2** (2026-08-08) · assessment constitution **v1.1**
(2026-08-08) · `ch_04_summary.json` (8 sections, 18 worked examples, 21 exercises) ·
`ch_04_mapping.json` (core_cg CG-3; core C-3.1; adjuncts C-7.2, C-9.3; co_central false) ·
`pedagogy_secondary_mathematics.txt`.
**Library:** re-authored 2026-08-09, counts [15, 12, 9], report
`genon/out/library_reports/mathematics_ix_ch04_20260809_102753.md` — DETERMINISTIC CHECKS ALL PASS.
**Engine as run:** serve **v2.2 / e17** (testing.md §0.2 still asserts e12 — step-0 drift, noted, not a C3 item).
**Checker:** Claude, 2026-08-09 · **Method:** programmatic battery over both files (band tiling,
sentence/word counts, register regexes, id leakage, guide shape, field discipline, A4 verbatim
diff against the summary) + judged reads + independent arithmetic re-derivation of every
determinate answer. Every judgement quotes its evidence.

Verdicts: **PASS** · **PASS·subj** (judgement, evidence quoted) · **FAIL** (defect filed) ·
**OBS** (observation, no defect).

**Headline.** The two files fail in *complementary* ways, which is the case for checking a
compact. The STANDARD leaks 31 internal item ids into teacher-facing text and ships one
arithmetically **wrong** verified answer with the model's own deliberation left in the field.
The COMPACT is clean on both counts but breaches the register's forward-reference ban four
times and emits every guide sub-block as empty strings. Neither failure was caught by
certification.

---

## A. Lesson-plan constitution v1.2

| Rule | STANDARD (15u) | p12 (12u) | Evidence |
|---|---|---|---|
| VOCABULARY | PASS | PASS | Zero occurrences of "period"/"session" in any activity title, band, note or homework across 60 + 48 bands. "unit" used throughout. |
| REGISTER · clock | PASS | PASS | No stated clock quantity in either file. Brevity is expressed in kind, as the register asks: standard U15 "Quick individual write"; p12 U7 "Quick whole-class discussion". |
| REGISTER · forward / completion | PASS | **FAIL (4)** | p12 U7 notes: "two skills that **will recur** when simplifying rational expressions" and "End of Chapter Q1, p.88 (vii)–(ix) … may be set for later self-study **once section 4.7 has been taught**". p12 U7 **homework**: "complete any remaining parts (vii)–(ix) **after section 4.7 is covered**" — a forward dependency written into a *deliverable*. p12 U12 notes: "a natural place for a **final unit**". All four survive `register_scan` (report: "register clean (0 ban hit(s))") — no pattern covers them. → **ARV-D-069** |
| REGISTER · calendar | **FAIL (1)** | PASS | Standard U3 band 32-44: "flag any case where a student matches the middle term incorrectly — that is the focal error **today**." Ban 3 names `today` in terms; `register_scan` classifies it ADVISORY by design (testing.md C5.9), so it never gated. → **ARV-D-069** |
| REGISTER · backward by position | PASS·subj (2) | **FAIL (4)** | Backward reference is legal at v1.10/v1.2, but Rule 10 says the link is "named by that content itself, **never by its position**". p12 breaches it in four teacher_notes openers: U3 "Having derived (a+b)² **in the previous unit**", U6, U9, U11 identically. Standard confines it to two band texts (U12 "Students who judged the derivations **in the previous unit**", "not finished in the previous unit") — advisory there, since Rule 10 governs notes. This is not cosmetic: at X=13 the standard's U12 is the *borrowed* slot-X unit, and a borrowed unit's neighbour is not guaranteed. → **ARV-D-070** |
| INPUTS 4 / TIME | PASS | PASS | `period_schedule` exactly `[{50, 15}]` / `[{50, 12}]`; every unit 50 min; all 27 units tile 0→50 with no gap or overlap; ≥3 bands everywhere (all units carry exactly 4). No assessment time embedded in any band. |
| R1 section anchoring | PASS | PASS·subj | All content traces to a named section; the summary's own order is followed on first visit (certifier agrees). **p12 U7 anchors 4.4 after U6 anchored 4.6** — a second *teaching* unit for 4.4 placed out of source order. Rule 1 P3 forbids re-ordering "to fit a narrative shape the chapter does not contain"; here the motive is budget, not narrative, and the handoff row `sec#4 [4,7]` carries two LOs with one delivered in each. Judged a pass; recorded because it is the kind of move Rule 1 P3 exists to police. |
| R1 · anchor granularity | PASS·subj | PASS·subj | p12 U12 anchors the compound `"4.6 / 4.7 / 4.8"` (p09 U1 `"4.1 / 4.2"`, U9 four-way). A3's schema comment reads singular ("named section this period draws from"), but A3's own `source_sections` clause sanctions it — "A unit built on such items anchors on these sections" — and every part resolves in the registry. Pass. |
| R2 content-driven calibration | PASS·subj | PASS·subj | Demand read off the sections: U10 derives (a+b)³ "using the distributive property", U11 verifies the cube factorisations "by direct expansion rather than geometric argument, and students sometimes find this less intuitive than the square case". No invented hands-on padding; the algebra-tile unit is the summary's own 4.5. |
| R3 cognitive floor | PASS | PASS | No recall-only unit in either file. Every unit's bands require compute / derive / factorise / justify. Homework likewise (standard U3 hw: "find (79)², (193)², and (299)² using the (a-b)² identity"). |
| R4 think_reflect folded in | PASS·subj | PASS | 10 of the standard's units and 8 of p12's weave the section's think-and-reflect prompt into a band. **Standard imports the wrong section's prompt three times:** U7 (anchored 4.5) uses 4.6's, U10 and U12 (anchored 4.7) both use 4.6's debate — Rule 4 says weave "the anchored section['s]" note into "that period". p12 keeps every prompt with its own section (U1→4.1, U5→4.5, U6→4.6, U8→4.7, U10→4.8). Judged subjective-pass on the standard (the imports are pedagogically apt and the 4.5/4.6 pair is genuinely continuous), recorded as the weaker of the two. No prompt promoted to an exercise, homework or handoff anchor in either file. |
| R5 method named exactly | **FAIL** | PASS | The Pedagogy document's table (lines 144-148) names five methods verbatim: `Play-way`, `Discovery/Inquiry`, **`Problem solving`**, `Inductive`, `Deductive`. The standard writes **`Problem Solving`** (capital S) on **8** of its 15 units — U3, U6, U8, U9, U12, U13, U14, U15. p12 and p09 both write `Problem solving`. Rule 5 says "named **exactly** as written in the Pedagogy document". Cosmetic in effect, but it is the one field the rule makes literal, and it now differs *between canonicals of the same chapter*. → **ARV-D-071** |
| R5 P1 no >2 consecutive | **FAIL** | **FAIL** | Standard U12·U13·U14·U15 = Problem solving **× 4**. p12 U7·U8·U9 = Deductive **× 3** *and* U10·U11·U12 = Problem solving **× 3** (p09 U7·U8·U9 = Problem solving × 3 — all three canonicals breach it). The prohibition is absolute ("MUST NOT repeat the same method across more than two consecutive periods") and nothing in the pipeline checks it. Both runs are chapter tails, where the content genuinely converges on problem work — which is an argument for amending the rule, not for reading it as satisfied. → **ARV-D-072** |
| R5 weighting respected | PASS | PASS | Standard: Problem solving 8, Deductive 5, Discovery/Inquiry 2. p12: Deductive 5, Problem solving 5, Discovery/Inquiry 2. Play-way and Inductive unused — correct at LESS_OFTEN for a transition-to-proof chapter. Exactly one method per unit, never blank, none outside the document. |
| R6 LO count 1–2 | PASS | PASS | Standard: 1,2,2,2,1,1,2,2 + 1 (synthesis) = 14. p12: 1,2,2,2,1,1,2,2 = 13. Never three. |
| R6 LO form | PASS | PASS | All 27 LOs open "Students can" with an observable verb (verify, expand, compute, factorise, prove, apply, represent, simplify, select). Zero internal-state verbs; none restates the competency or dissolution_test; none binds to a worked example's numbers. |
| R6 section_context 10–12 words | **FAIL (4/9)** | **FAIL (2/8)** | Mandate is a 10–12 word label. Standard: sec#1 = 8, sec#7 = **15** ("binomial cube identities, sum and difference of cubes, three-variable cube identity, factorisation and numerical application"), sec#8 = 11 ✓, sec#9 = 14. p12: sec#1 = 9, sec#7 = 9. p09 is worse (sec#5 = 15). Same drift SS·IX showed at ARV-D-030 — under-length when the section is thin, inventory-length when it is rich. → **ARV-D-030 (recurrence)** |
| R6 P2 no LO in period objects | PASS | PASS | No `implied_lo`, `section_context` or `c_code` on any period object in either file. |
| R7 full coverage | PASS | PASS | All 8 sections receive ≥1 unit in both. `section_coverage_note` null in both — correct, no shortfall. No front-loading: the standard spends 2 units each on 4.3, 4.4, 4.6, 4.8 and 3 on 4.7, tracking substance not the effort_index. |
| R8 excluded material | PASS | PASS | No asterisked or sidebar item appears; every `textbook_items_in_class` id resolves in the summary (0 fabricated ids, 0 -a/-b suffixes across both files). E-3's own description names the exclusion. |
| R9 P5 no internal item ids | **FAIL (31)** | PASS (0) | The standard writes `WE-N`/`E-N` into teacher-facing text 31 times, in bands *and* homework: U3 band 32-44 "Exercise 4.2 Q1 parts (i)–(iv), p.74 **(E-3)**"; U3 hw "Exercise 4.2 Q2, p.75 **(E-4)**"; U11 "**(E-15)**", "**(E-14)**"; U15 "**(E-13)**", "**(E-14)**", "**(E-15)**", "**(E-16)**". Rule 9 P5 and A3's field constraint ("names textbook items by book_ref **only**") both forbid it. p12 has **zero** — it writes "End of Chapter Q1, p.88 (i)–(vi)" — so this is variance between canonicals of one chapter, not a prompt-level inevitability. Nothing in certification looks for it. → **ARV-D-073** |
| R9 P1–P4 no machinery | PASS | PASS | Zero C-codes, CG-codes, rule numbers, schema field names or effort-index terms in any teacher-facing field in either file. |
| R10 teacher_notes ≤3 sentences | **FAIL (1/15)** | PASS (0/12) | Standard U3 runs **4** sentences (abbreviation-aware split): "Having expanded (a+b)^2, students now run the process in reverse. / The most common slip is sign… / The geometric derivation of (a-b)^2 is best done with a labeled diagram… / Example 8, p.73 can be read as self-study…". p09 U3 also runs 4. Every other unit is exactly 3. No note opens with "Transition" or a section label. |
| R10 content · error · self-study | PASS | PASS | All 27 notes carry a named misconception traceable to the section — "students recognise x^2+4x+4 but miss that x^2-4x+4 also factors as a perfect square"; "confusing the sign in the quadratic factor: x³-y³ gives (x-y)(x²+xy+y²) where all three terms inside the bracket are positive". Self-study pointers are given by book_ref throughout. No fabrication found. |
| R11 homework | PASS | PASS | `[]` by default; never more than 2 (standard 6 units populated, p12 10, all with exactly 1). Every item is above the Rule 3 floor — no copying. **See the register row** for p12 U7's homework, whose *content* is fine and whose *framing* is forward-looking. |
| R12 handoff present, one row/section, order | PASS | PASS | Top-level sibling key in both; one row per section in summary order; no LO/context/competency duplicated into a period. `section_ref` and `section_title` are byte-verbatim against the summary on every real section (programmatic diff). |
| R12 · `period_numbers` = units that TEACH | **FAIL (2 rows)** | PASS | This is the rule v1.2 was written for, eight days ago, off this chapter — and it recurs in the post-v1.2 re-author. **sec#6 (4.6) = `[8, 9]`, one LO.** U8 "Splitting the Middle Term Without Tiles" delivers that LO in full; U9 "extends the method to applied contexts where the quadratic must be set up from a word problem" — a *different* operation the row never claims. Either Rule 6 owed a second LO or U9 is not a teaching unit for this one; under v1.2 the row should read `[8]`. **sec#7 (4.7) = `[10, 11, 12]`, two LOs.** U10 delivers LO1 (cube expansion / cube root), U11 delivers LO2 (sum & difference of cubes, three-variable); U12 "Finding New Identities by Combining Results" delivers neither — its own notes call it a consolidation of "the mixed-identity exercise". Should read `[10, 11]`. p12's multi-unit row `sec#4 [4, 7]` is **correct** — two LOs, one delivered in each. → **ARV-D-074** |
| R12 · synthesis row | PASS | n/a | The standard carries `sec#9 ref "synthesis", period_numbers [15]`, and item 14 anchors to it — the 2026-08-08 `top_brief_for` fix working on its second outing. This is the S3 defect (a mandated synthesis unit that can carry no items on a derived-anchor stage) **closed on this stage**. `total_sections` stays 8 while `section_number` is 9 — internally inconsistent but consistent with the brief; OBS. |
| A4 · c_code from the mapping | **FAIL (1 row)** | PASS | The mapping ties **C-9.3** to section **4.6** in terms ("The middle-term-splitting method in **section 4.6** … is the chapter's clearest instance"). The standard stamps C-9.3 on **4.5** (Algebra Tiles) *and* 4.6; p12 stamps C-3.1 on 4.5 and C-9.3 on 4.6 — correct; p09 stamps C-9.3 on 4.5 and C-3.1 on 4.6 — both wrong. Three canonicals of one chapter give three different answers for the same two sections, against a mapping the Integrity Constraints call settled. → **ARV-D-075** |
| A4 · adjunct C-7.2 unused | OBS | OBS | C-7.2 (geometric visualisation, justified against 4.2/4.4/4.7) is stamped nowhere in any canonical. A4 permits variation and does not require every adjunct to be used, so this is not a breach — but the chapter's geometric-proof strand is the thing the mapping calls out, and no item is attributed to it. |
| A3 · `activity_title` 10–13 words | **FAIL (14/15)** | **FAIL (10/12)** | The schema states 10–13 words. Standard titles run 6–10; only U11 ("Sum and Difference of Cubes, and the Three-Variable Cube Identity", 10) reaches the floor. p12 runs 7–10; only U5 and U9 reach it. No trailing periods (that half of the constraint holds). Systematic, both files, all three canonicals — this reads as a constraint the prompt never surfaces rather than a model lapse. → **ARV-D-076** |
| A3 · `description` verbatim | **FAIL (10)** | **FAIL (6)** | A3 requires `description` "verbatim from the summary". Both files silently truncate the tail: E-3 summary "…using the perfect-square identity **(asterisked parts (v)-(vi) excluded)**" → plan "…using the perfect-square identity."; E-10 summary lists all eight products "**: (41)^2, (27)^2, 23x17, (135)^2, (97)^2, 18x29, 34x43, (205)^2**" → plan drops them; E-9 drops "**including splitting the middle term of quadratics with leading coefficient other than 1**". The E-3 case is the one that bites: the plan's copy no longer records that (v)-(vi) are excluded, which is what Rule 8 relies on. → **ARV-D-077** |
| A3 · `source_sections` copied | PASS | PASS | Where the summary carries `source_sections` (the repaired end-of-chapter items E-13…E-16), both files copy it, and `source_section`/`book_ref` match the summary exactly on all items. The 2026-08-09 `fix_eoc_sections.py` repair is holding. |
| A3 · remaining fields | PASS | PASS | All 11 period keys present on every unit, no extra keys, `visual_aids` null where none (standard 6 populated, p12 6). |
| INTEGRITY | PASS·subj | PASS·subj | Mapping never reopened; LOs are outputs; single standard row; the full budget is teaching only; no `period_ref` on any assessment item (grep = 0), so the derived-anchor rule holds. **OBS:** `result` still carries vestigial `role_handoff: {}` and `unit_handoff: {}` from the retired rules — recurrence of **ARV-D-017**. |

---

## B. Assessment constitution v1.1

| Rule | STANDARD (14 items) | p12 (13 items) | Evidence |
|---|---|---|---|
| R1 governing purpose | PASS | PASS | Every stem demands an observable demonstration — "Show every term of the expansion", "Write an algebraic argument that decides whether Rohan is right", "state the two numbers whose sum equals −9". No "did you understand" framing anywhere. |
| R1 P3 nothing from position | PASS | PASS | Format and demand track the tag, not the section index: sec#1 is ECR/Analysis in the standard and MCQ/Understanding in p12; sec#8 carries Application in both. |
| R2 inputs / inheritance | PASS | PASS | Every item's `implied_lo_assessed` and `section_context` are byte-verbatim against a handoff row of the same `section_number`; `total_sections` inherited; `chapter_cg` = "CG-3" once at chapter level (matches `core_cg`), never per question; `c_code` per item ∈ {C-3.1, C-9.3} with non-empty `competency_text`. No outside source referenced. |
| R3 summary supplies | PASS | PASS | Stems carry the summary's real material: "(a+b−c)² + (a−b+c)²"; "p+q+r=6, p²+q²+r²=14, pqr=6" (the summary's own three-variable application); "(x²−16)/(x²+x−20)". |
| R3 worked-example numbers not copied | PASS·subj | PASS·subj | Fresh instances throughout: 108² against the summary's 43²; 72m²−48mn+8n² against 50p²+60pq+18q²; (x+2)(x+6) against the summary's (x+3)(x+4). **One marginal in p12:** OPEN_TASK part (ii) `x² − 7x + 12` re-uses the summary's own `x²+7x+12` with one sign flipped. Method-shaped rather than copied; recorded, not filed. |
| R3 ADJACENT PULL — one owning section | **FAIL (1)** | PASS | Standard item 1 (sec#1, 4.1) and item 5 (sec#3, 4.3) ask the **same thing**: item 1 "Let the three consecutive integers be (n−1), n, (n+1). Expand each square and simplify"; item 5 "give a complete algebraic argument that settles the question definitively". The summary places the algebraic proof in **4.3** ("…and **proves the earlier consecutive-squares pattern algebraically using (n-1), n, and (n+1)**"); 4.1's own slice is the *numeric* surprise. So item 1's tested operation is drawn from a later section — "Which section does this test?" does not have one answer. p12 gets this right: its sec#1 item asks *why numerical evidence is not proof* (MCQ, Understanding), which is 4.1's own content, and leaves the proof to its sec#3 ECR. → **ARV-D-078** |
| R4 tag present & in-enum | PASS | PASS | All 27 items tagged within {Recall, Understanding, Application, Analysis, Evaluation}; none blank. Standard: Application 8, Analysis 2, Understanding 2, Evaluation 2. p12: Application 7, Understanding 3, Evaluation 2, Analysis 1. |
| R4 tag consistent with the LO | PASS·subj | **FAIL (1)** | p12 item 9's LO is "Students can **factorise** a quadratic x²+px+q by **finding** two integers…" — `factorise`/`find` sit squarely in Rule 4's Application row — and it is tagged **Analysis**. The task confirms the LO's reading: four routine factorisations plus one pattern sentence. The mis-tag is what licenses the wrong format below. Standard's item 11 is the mirror-image marginal (LO says "apply … to factorise and solve", tagged Analysis) and is judged a pass: its stem genuinely requires deriving pq+qr+rp before the identity can be used. → **ARV-D-079** |
| R5 demand→format | **FAIL (1)** | **FAIL (1)** | 25 of 27 map exactly. Both exceptions are the OPEN_TASK. **Standard item 14** is tagged **Evaluation**, which Rule 5 maps to **ECR**; it is emitted as OPEN_TASK. **p12 item 9** is tagged **Analysis** → also ECR; emitted as OPEN_TASK. Rule 5 reserves OPEN_TASK for the "Integrative / cross-operational (co_central)" band, and **`co_central` is false** for this chapter in the mapping and in every handoff row. Rule 6 allows an OPEN_TASK lift "only where the chapter genuinely integrates operations" — but `reasoning_floor_lift_applied` is **false** in both files, so neither is claiming the lift. The standard's case is defensible on content (its OPEN_TASK is the synthesis unit's item and genuinely spans four identity families) and indefensible on the letter; p12's is neither — its task is four middle-term splits. → **ARV-D-080** |
| R5 one item per implied_lo | PASS | PASS | Standard 14 items ↔ 14 LOs; p12 13 ↔ 13; positionally aligned, two-LO sections yielding two consecutive entries sharing section_number/ref/title with different `implied_lo_assessed`. No bonus, mixed-review or chapter-wrap item; no LO split. |
| R6 reasoning floor | PASS | PASS | Standard: 3 ECR + 1 OPEN_TASK. p12: 2 ECR + 1 OPEN_TASK. Floor met without a lift, so `reasoning_floor_lift_applied: false` is correct in both. Not all-MCQ/NUM/SCR. |
| R7 MCQ structure | PASS | PASS | Standard 2 MCQs, p12 3: each has exactly 4 options, exactly one `is_correct`, and exactly 3 named diagnostic distractors keyed to the non-correct labels. No true/false. Errors are nameable and in-chapter — "Omits the cross-term entirely — the classic (a−b)² = a²+b² error"; "Confuses the difference-of-squares factorisation with the perfect-square trinomial". |
| R7 P2 no by-label option text | PASS | PASS | No option text refers to another option. Zero "both A and B" / "none of the above" / "all of the above" across 20 option texts. |
| R7 P2 · **the guide does what the option may not** | **FAIL (2)** | **FAIL (2)** | The prohibition names options; the falsification it prevents is being caused by the **guide**. Four `guide.MCQ` blocks reference an option by letter: standard item 2 "substituting small integers for x and y in **option A**", standard item 7 "confirm **option A** by collecting all six cross-product terms", p12 item 3 "reducing to **option C**", p12 item 7 "verify **option A** by expanding (2x−3)²". STEP 6 caught exactly one — the report reads "`#3 SKIPPED — cross-references an option label — left untouched, needs a human`" — and passed over the other three, so a future re-sort would silently falsify them. The constitution's ban should extend from `options[].text` to the guide. → **ARV-D-081** |
| R7 · standard item 7 guide is wrong | **FAIL** | — | Same block, separate error: the correct answer is **C** ("2a²+2b²+2c²−4bc", which I re-derived: (a+u)²+(a−u)² = 2a²+2u² with u = b−c). The inclusivity text tells the teacher to "confirm **option A**". A teacher following the guide reaches the wrong answer. → **ARV-D-081** |
| R8 menu | PASS | **FAIL** | Standard's `format_type` "Model-and-solve" is on the menu and is the natural vehicle — a container scenario routing through four identity families. p12's is "**Procedure / argument evaluation**", which the menu defines as "judge a worked method or claim, identify the flaw, repair it"; its task judges nothing and repairs nothing — it factorises four quadratics and asks for a sign rule, which is the menu's "**Pattern generalisation**" almost verbatim. Rule 8 forbids selection that is not "the most natural vehicle". → **ARV-D-080** |
| R8 · substitution statement | **FAIL** | **FAIL** | Rule 8 requires the guide to "**state that the teacher may substitute any other menu format**". Neither `guide.OPEN_TASK` says so — both give `format_rationale` and stop. Same omission in both files, so it is a prompt gap, not a lapse. → **ARV-D-082** |
| R8 · one OPEN_TASK, unsplit | PASS | PASS | Exactly one per file. |
| R9 guide present, structured, by type | PASS | **FAIL (13/13)** | The standard emits the item's own sub-block and `null` for the other four. **p12 emits all five sub-blocks on every one of its 13 items, with empty strings**: 9 empty leaves on 12 items, 4 on the OPEN_TASK — `"NUM": {"learning_outcome": {"section": 2}, "inclusivity": ""}`, `"OPEN_TASK": {"format_type": "", "format_rationale": "", …}`. A1 states "Populate every field; **empty strings and empty arrays are not permitted for required fields**" and Rule 9 makes `inclusivity` "REQUIRED in every guide block". Read literally, p12 ships **112** empty required fields (12 × 9 + 4). → **ARV-D-083** |
| R9 · inclusivity substance | PASS | PASS | Where populated (all 27 items' own blocks), every one pairs a support with a challenge as the rule asks: "A student who is unsure can start by taking the cube root of the first term… A student who is comfortable can be asked to also verify the cube root by cubing (3x−2y) fully." |
| R9 P · no C-codes in the guide | PASS | PASS | Zero C-codes, CG-codes or competency labels inside any guide block in either file (programmatic grep). |
| R10 executability | PASS | PASS | Every task is self-contained and classroom-answerable; no field visit, external material or multi-session component. The algebra-tile items describe the tiles in the stem rather than requiring physical sets. |
| R11 answer verification | **FAIL (1)** | PASS | I re-derived every determinate answer independently and re-checked each symbolically with `sympy` (factorisations, expansions, cube roots, rational simplifications, both quadratic word problems). **26 of 27 are correct**, including the standard's three-variable ECR (e₁=6, e₂=11, e₃=6 ⇒ roots 1,2,3 ⇒ Σp³ = 36 ✓ — the givens are mutually consistent, which is more than the rule asks) and p12's whole set. **Standard item 4 is wrong.** `expected_answer` = "**8(3m − 2n)^2**", which expands to 72m² − **96**mn + **32**n², not the stem's 72m² − 48mn + 8n². The correct answer is **8(3m − n)²**. → **ARV-D-084** |
| R11 P · no verification working leaked | **FAIL (1)** | PASS·subj | Same item. `method_one_line` ships the model's deliberation verbatim: *"Extract the common factor 8 to get 8(9m^2 − 12mn + n^2) — **wait, verify:** 9m^2−12mn+n^2... **Let me re-check.** 72m^2−48mn+8n^2 = 8(9m^2−6mn+n^2). Check: … **So the answer is 8(3m−n)^2.**"* The field both leaks Rule 11's reasoning (Rule 9 P and Rule 11 P forbid it in terms) **and contradicts its own `expected_answer`** — the model found the error and the wrong value shipped anyway with `verified: true`. p12's marginal: item 6's `method_one_line` offers three decompositions ("— or more naturally 200+3 … alternatively, 203 = 100+100+3"), which is not one sentence and reads as retained deliberation; both routes are arithmetically right (41209 ✓) so it is filed as a style breach, not a wrong answer. → **ARV-D-084** |
| R12 scope | PASS | PASS | Chapter-scoped formative only; no summative/Board framing, portfolio or cross-chapter tracking; no asterisked material re-entering. |
| A1 · field discipline | PASS | PASS | Programmatic sweep: `expected_answer`/`method_one_line` populated on NUM only; `expected_elements` SCR only; `look_for` ECR only; `task`/`scaffold`/`format_of_output` OPEN_TASK only with `question_text` = ""; `options` MCQ only; `verified` true on all 27. Zero violations in either file (the guide-shape failure above is the only A1 breach). |
| A1 · VS-1…VS-6 | PASS·subj + OBS | PASS·subj + OBS | `visual_stimulus` is **null and `graph_paper` false on all 27 items**, and no stem says "the table below" or "in the figure" — so VS-3/VS-4/VS-5 are formally clean. **OBS worth carrying to the human gate:** the constitution says "Secondary mathematics at the transition-to-proof stage is figure-heavy; SVG is permitted and **expected** here", and this chapter's spine is geometric proof-without-words (the (a+b)² square partition, the nine-region figure, the cube decomposition, algebra tiles). The tile items describe a rectangle in ~60 words of prose that one figure would carry. Zero figures across a whole library is a signal about the prompt, not a rule breach — and it means the standing VS-2/VS-6 renderer debt (assessment CHANGELOG v1.0) was never exercised here. |
| A1 · section_number ≤ total_sections | **OBS** | PASS | Standard item 14 carries `section_number 9` against `total_sections 8` — the synthesis row's known inconsistency, inherited from the handoff. Harmless downstream (anchoring is by section_number, which resolves), but any consumer computing coverage as n/total will read 9/8. |

---

## C. Defects filed

| ID | Sev | File(s) | One line |
|---|---|---|---|
| ARV-D-069 | S2 | p12 (4), std (1) | Register: forward reference in notes **and homework**, "final unit", and `today` — all pass `register_scan`. |
| ARV-D-070 | S3 | p12 (4), std (2) | Continuity carried by position ("in the previous unit") where Rule 10 says never by position. |
| ARV-D-071 | S3 | std | `Problem Solving` ≠ the Pedagogy document's `Problem solving`; differs between canonicals of one chapter. |
| ARV-D-072 | S2 | std, p12, p09 | Rule 5 P1 breached in all three canonicals (×4, ×3+×3, ×3). Nothing checks it. |
| ARV-D-030 | S3 | std (4), p12 (2) | `section_context` outside 10–12 words — recurrence of the SS·IX defect. |
| ARV-D-073 | S2 | std (31) | `E-N`/`WE-N` internal ids in bands and homework; p12 has zero, so it is variance. |
| ARV-D-074 | S2 | std (2 rows) | `period_numbers` still lists non-teaching units — the exact defect LP v1.2 was written for, recurring in the post-v1.2 re-author. |
| ARV-D-075 | S2 | std, p09 | `c_code` C-9.3 stamped on 4.5 against a mapping that ties it to 4.6; three canonicals, three answers. |
| ARV-D-076 | S3 | std (14/15), p12 (10/12) | `activity_title` below A3's 10–13 words almost everywhere — prompt gap. |
| ARV-D-077 | S3 | std (10), p12 (6) | `description` not verbatim; E-3 loses "(asterisked parts (v)-(vi) excluded)", the clause Rule 8 leans on. |
| ARV-D-078 | S2 | std | Item 1 tests 4.3's proof while owned by 4.1; duplicates item 5. p12 does it correctly. |
| ARV-D-079 | S3 | p12 | Item 9 tagged Analysis on an Application LO — the mis-tag that licenses the wrong format. |
| ARV-D-080 | S2 | std, p12 | OPEN_TASK emitted against an Evaluation / Analysis tag with `co_central: false` and no declared lift; p12's `format_type` is off-menu in substance. |
| ARV-D-081 | S1 | std (2), p12 (2) | Guides reference options by letter — STEP 6 caught 1 of 4 — and standard item 7's guide names **the wrong option as correct**. |
| ARV-D-082 | S3 | std, p12 | Rule 8's "teacher may substitute any menu format" statement missing from both OPEN_TASK guides. |
| ARV-D-083 | S2 | p12 (13/13) | All five guide sub-blocks emitted with empty strings — 52 empty required fields against A1's explicit ban. |
| ARV-D-084 | **S1** | std | Item 4 ships a **wrong** `expected_answer` with `verified: true`, and `method_one_line` carries the model's own "wait, verify… let me re-check" deliberation that found the right answer. |

**Tooling gaps surfaced (not constitutional, recorded for C5):** `register_scan` misses "will
recur", "once section N has been taught", "after section N is covered" and "final unit", and
classifies `today` as advisory; certification checks no Rule 5 P1, no id leakage, no
`activity_title` length, no `description` verbatim, no guide-shape/empty-field rule, and no
`c_code`-against-mapping consistency. `normalize_options`' label-reference guard reads
`options[]` only, not the guide.

---

## D. Serve exposure of ARV-D-074 — the honest bound

Recorded because the rule breach reads worse than its current cost. Serving the library at
every X in the band (engine as installed):

| X | canonical used | units served | items | sections assessed |
|---|---|---|---|---|
| 8 | 9 | 8 | 9 | 4.1–4.8 |
| 9 | 9 | 9 | 9 | 4.1–4.8 |
| 10 | 12 | 10 | 11 | 4.1–4.7 |
| 11 | 12 | 11 | 12 | 4.1–4.7 + synthesis |
| 12 | 12 | 12 | 13 | 4.1–4.8 |
| 13 | **15** | 13 | **11** | 4.1–4.7 |
| 14 | 15 | 14 | 12 | 4.1–4.7 + synthesis |
| 15 | 15 | 15 | 14 | 4.1–4.8 + synthesis |

The standard's shortest served prefix is **12 units** (at X=13), and its two over-long rows
anchor at U9 and U12. Both are inside every prefix the standard is ever served as, so
**ARV-D-074 costs nothing on this library today** — the remedy is a declared repair of two
arrays, not a re-author. The margin is one unit: sec#7's item sits exactly on the X=13
boundary, and any future canonical at 13 or 14 units, or any change to the choice set, drops
4.7 out of the assessment.

**Separate observation for C6/C9, found here:** the serve is **non-monotone in questions** —
X=12 yields 13 items, X=13 yields **11**. A teacher who asks for one *more* period gets two
*fewer* questions, because X=13 switches to the standard, whose 4.8 row anchors at U14. Nothing
is wrong with any single step; the artefact is the interaction of next-highest selection with
per-section anchoring. Not filed as a C3 defect — it belongs to C6/C9 — but it should not be
met there as a surprise.

---

## E. Verdict

**C3 = FAIL**, on two S1 items and eleven S2/S3 items.

The two S1s are the gate: a **wrong verified answer** shipped with the model's own correction
visible in the field beside it (ARV-D-084), and a **guide that names the wrong option as
correct** (ARV-D-081). Both are teacher-facing and both are in the STANDARD canonical, which is
the file every serve at X ≥ 13 uses and the file every compact borrows from.

Everything else is repairable in place at ₹0 — the id leakage, the register phrasings, the
`period_numbers` arrays, the `c_code`, the guide shape, the descriptions. Only ARV-D-084 and
ARV-D-078 need generated content, and both are single items.

**The compact was worth checking, and the finding is symmetric, not one-directional.** p12 is
*better* than the standard on ownership (its 4.1 item tests 4.1), on ids (0 vs 31), on the
method label, on `c_code`, and on Rule 12. It is *worse* on the register, on guide shape, and on
format selection. So neither "the constitution holds at full length and breaks under
compaction" nor its opposite is true here: what the pair actually shows is that **the rules with
no machine check behind them are satisfied at roughly coin-flip rate per file**, independent of
length. That is the finding to carry to the human gate, not any single defect.
