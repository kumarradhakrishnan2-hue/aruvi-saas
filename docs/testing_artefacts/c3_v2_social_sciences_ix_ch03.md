# C3 — rule-by-rule compliance (v2.0 library) · social_sciences · IX · chapter 3

**Files checked (both, every rule):**
`ch_03_canonical.json` — the STANDARD, 12 × 50, ledger `20260803_141938`
`ch_03_canonical_p07.json` — the FLOOR compact, 7 × 50, ledger `20260803_143426`
*(p07 chosen over p10 deliberately: the constitution is easiest to keep at full length, so the
shortest canonical is the honest test of whether it holds under compaction.)*

**Checked against:** LP constitution **v1.10** · assessment constitution **v1.6** ·
mapping `ch_03_mapping.json` (6 competencies: C-4.2 Central; C-4.3/C-4.4/C-4.5 Substantive;
C-4.1/C-4.6 Present) · summary `ch_03_summary.txt` (9 substantive sections)
**Engine:** e12 · **Checker:** Claude, 2026-08-03 · **Method:** programmatic battery over both
files + judged reads; every judgement quotes its evidence.
**Supersedes** `c3_social_sciences_ix_ch03.md` (2026-07-29, LP v1.7, pre-v2.0 library).

Verdicts: **PASS** · **PASS·subj** (judgement, evidence quoted) · **FAIL** (defect filed) ·
**OBS** (observation, no defect).

---

## A. Lesson-plan constitution v1.10

| Rule | STANDARD (12u) | p07 (7u) | Evidence |
|---|---|---|---|
| VOCABULARY | PASS | PASS | Zero occurrences of "period"/"session" in any activity title, band, note, or homework across 48 + 28 bands. |
| REGISTER · clock | **FAIL** | PASS | Standard U1 band 0-10: "Students jot individual responses **for two to three minutes**, then share aloud." The 18:07 repair pass removed three clock quantities and missed this one — `register_scan` matches `for two minutes` but not `for two to three minutes`. → **ARV-D-026** |
| REGISTER · forward | **FAIL** (1) | **FAIL** (2) | Standard U6 notes: "Connecting India's tropical position to the monsoon regime **that will follow** prepares students conceptually." p07 U3 notes: "…intentionally plants the relief-climate interlinkage **that the Monsoon unit will extend**." p07 U3 band 40-50 — **in band text**, which Rule 13 makes the core teacher-facing product: "This sets up the interlinkage of relief and climate **explored in upcoming units**." All survive certification — no pattern covers any of the three phrasings. **Borderline, founder call:** p10 U1 notes "the three functions **the whole chapter unpacks**". → **ARV-D-026** |
| REGISTER · completion | PASS·subj / gap | PASS | Standard U12 notes: "This unit **assumes all chapter sections have been taught**". Literally a completion claim, but U12 is the mandated synthesis unit and the claim is true by construction (architecture §0.3). The constitution carries no synthesis exception → **ARV-D-029** (doc). |
| REGISTER · calendar | PASS | PASS | No "tomorrow / next class / this week". Standard U5 homework's "two-week observation grid" is the summary's own LET'S ANALYSE span (textbook content, not a schedule) — OBS, not a breach. |
| REGISTER · ids | PASS | PASS | No `C-4.x` in any teacher-facing text (the U9 leak of the pre-v2.0 library, ARV-D-013, did not recur). |
| INPUTS 4 / TIME | PASS | PASS | `period_schedule` exactly `[{50, 12}]` / `[{50, 7}]`; every unit 50 min; bands tile 0→50 contiguously with no gap or overlap in all 19 units. |
| R1 age calibration | PASS·subj | PASS·subj | Demand drawn from the summary's own apparatus: pie-diagram reading (Fig. 3.2), wind-speed table work (Table 3.1), the six-ṛtu comparison. No pedagogy-document vocabulary leakage found. |
| R2 cognitive floor | PASS·subj | PASS·subj | Sampled bands require construction or analysis, e.g. standard U1: "Students construct a three-column organiser… Pairs compare organisers and reconcile any disagreement." No recall-only band found. |
| R3 section anchoring | PASS + gap | PASS | 11 of 12 anchors are named summary sections; U12 anchors the reserved token **`synthesis`**, which is not a summary section. Rule 3 P1 and the Integrity Constraint ("no exceptions for… review units") forbid it in terms; architecture §0.3 mandates it. Constitution gap, not a plan defect → **ARV-D-029**. |
| R4 full coverage | PASS | PASS | All 9 substantive sections reached in both. Standard: Intro·Composition·Structure·Weather+Elements·Seasons·Elements·Monsoon×2·Climate Change×2·Floods·synthesis. p07: Intro+Composition·Structure·Weather+Elements·Seasons·Monsoon·Climate Change·Floods. `section_coverage_note` null in both — correct, no shortfall. Long sections span units with distinct `section_context` slices. |
| R5 edges unforced | PASS | PASS | 23 edges (standard) / 17 (p07); every `c_code` ∈ mapping, zero weight drift, zero `cg` drift. Distribution follows weight without arithmetic: C-4.2 (Central) 7 edges, C-4.6 (Present) 1. No vocabulary-only pairing found on sampled reads. |
| R6 implied_lo form | PASS | PASS | 40/40 LOs open "Students can"; zero internal-state verbs; `cognitive_demand` always in enum. |
| R6 P1 proper nouns | **FAIL** | **FAIL** | 6 LOs in each file carry chapter-specific proper nouns, e.g. standard U7: "Students can trace the spatial progression of the advancing and retreating monsoon across **India**…"; p07 U7: "…which human practices amplified the **Punjab** flood disaster…". Recurrence of **ARV-D-015** under v1.10 — the rule has now failed across three generations. |
| R7 section_context | **FAIL** (2/12) | **FAIL** (4/7) | Mandate is 10–12 words. Standard: U1 = 8, U10 = 13. p07: U2 = 9, **U3 = 16**, U5 = 14, U7 = 15 — e.g. "Weather vs climate; insolation, temperature zones Fig. 3.6; Table 3.1 wind speeds; land-sea breeze Fig. 3.8". Compaction pushes the label toward an inventory (Rule 7's own prohibition). → **ARV-D-030** |
| R7 source naming | PASS | PASS | Data/source units name their artefact inside the budget: "Fig. 3.2 pie diagram", "Table 3.1 wind speeds", "Table 3.2 six-ritu traditional calendar", "Figs. 3.10 and 3.11". This is what makes source-slot resolution possible downstream. |
| R8 emphasis | PASS | PASS | `competency_gap_note` = "" and every mapped competency owns ≥ 1 genuine edge in both files; no evidence of weight arithmetic (C-4.3 and C-4.4 share weight 2 but carry 4 and 5 edges). |
| R9 approach source | PASS | PASS | Every label verbatim in `pedagogy_secondary_social_sciences.txt`: Inquiry · Issues-based learning · Authentic tasks/performance-based tasks · Project work · Reflective essays. Prohibition 4 respected — no "Conversations, discussions, and debates". |
| R9 P1 diversity | **FAIL** | PASS·subj | Standard runs `Inquiry` on U1·U2·U3·U4 — four consecutive — and `Issues-based learning` on U8·U9. p07 alternates and uses multi-label units (U5 `Inquiry; Project work`, U6 `Issues-based learning; Reflective essays`), honouring P5. The prohibition targets activity *type*, and the standard's four Inquiry units do differ in vehicle (organiser / pie reading / layer template / cause chain) — but four in a row is the pattern the rule exists to prevent. Recurrence of **ARV-D-014**. |
| R10 teacher notes | PASS | PASS | Every unit non-blank and exactly **3 sentences** in both files (19/19, measured with abbreviation-aware splitting); no "Transition"/label openers; one confusion each, all traceable to the summary (e.g. "placing the ozone layer in the troposphere"). |
| R10 continuity by content | PASS·subj (1 marginal) | PASS | Notes name the content built on — "Having established the atmosphere's layered structure…", "Having traced India's seasonal framework…". One marginal: standard U3 "Having mapped atmospheric composition **in the previous unit**" adds a position reference to an otherwise content-named link. Advisory in `register_scan`; noted, no defect. |
| R11 homework | PASS | PASS | `[]` by default; exactly one item each (standard U5, p07 U4), both at the Rule 2 floor ("identify which IMD season the data represents and write two sentences justifying your choice"). **ARV-D-012's cross-unit dependency did not recur** — no unit's materials or opening band consumes another unit's homework. |
| R12 coverage handoff | **FAIL** | **FAIL** | Present, mapping order exact (`C-4.2, C-4.3, C-4.4, C-4.5, C-4.1, C-4.6`), row counts identical to edge counts (23/23, 17/17), every `implied_lo`/`cognitive_demand`/`section_context` verbatim, no zero-edge competency. **But `section_anchor` is stale** on 2 rows (standard, U4) and 3 rows (p07, U3): handoff says "Weather and Climate**;** Elements of Weather and Climate", the period says "… **/** …". `repair_anchors.py v1.0` fixed the period and never walked the handoff. p10 identical (3 rows). → **ARV-D-027** |
| R13 band substance | PASS·subj | PASS·subj | Bands are teachable script, not stage direction: "Using Table 3.1: a wind recorded as a 'strong breeze' versus a 'storm' — what specific effects does the chapter associate with each?" Questions are stated verbatim where students answer them. No pointing-without-carrying found. |
| R13 sentence ceiling | **FAIL** (4/48) | **FAIL** (4/28) | Standard U3 band 10-35 runs **7 sentences** walking all five layers — by the rule's own test ("a band that needs more is two moves") it is two moves. Also U4 (6), U5 (5), U11 (5); p07 U1/U3/U5/U7 (5 each). → **ARV-D-031** (S4) |
| R13 apparatus box use | PASS | PASS | The chapter's own boxes are used as scaffolds, not replaced: 9 references in the standard, 6 in p07 (THINK ABOUT IT, LET'S RECALL, LET'S EXPLORE, My Carbon Footprint). Notes reinforce it: "The activity is the chapter's own structured checklist, not a teacher-designed substitute — use it exactly as written." |
| INTEGRITY | PASS | PASS | Mapping never reopened; LOs are outputs; single standard row; full budget is teaching only (no assessment time in any band); teaching-layer fields absent from the handoff. |
| A1 schema | PASS + OBS | PASS + OBS | All 12 period keys present on every unit, no extra keys, `visual_aids` null where none. **OBS:** `result` still carries vestigial `role_handoff: {}` and `unit_handoff: {}` from the retired Rules 15/16 — recurrence of **ARV-D-017**. |
| A2 schema | PASS (with R12 above) | PASS (with R12 above) | LO rows carry exactly the five mandated keys; no extra fields; no authored content. |

---

## B. Assessment constitution v1.6 (items ride in the same file)

| Rule | STANDARD | p07 | Evidence |
|---|---|---|---|
| INPUTS / R2 inheritance | PASS | PASS | All 18 + 18 items: `implied_lo` verbatim against a handoff row for the same competency AND unit; `cognitive_demand` identical to that row; `cg`/`weight_label` consistent with the mapping. Zero drift. |
| R1 governing purpose | PASS·subj | PASS·subj | Every stem demands a visible product — classification, justification, annotated map, pledge evaluation. No "did you understand" framing. |
| R3 executability | PASS | PASS | All tasks are single-session and classroom-bounded; no field visits, craft materials or outside coordination. |
| R4 exact counts | PASS | PASS | 18 items in each = Central 5 (C-4.2) + Substantive 3 × 3 + Present 2 × 2; the advisory count check in `build_library.py` agrees (18 vs 18 expected on all three files). |
| R4 / R5.3 source-slot resolution | **FAIL** (1) | **FAIL** (2) | Substantive's third slot must be SOURCE_INTERPRETATION when the competency owns a source-capable LO. The three misfilled slots, exactly: **standard item #8** (C-4.3, U7 Monsoon, Analysis, "…evaluate whether this description is accurate") — the competency owns three source-capable LOs (U4 "Fig. 3.6 temperature zones; Table 3.1 wind speeds; Fig. 3.8 land-sea breeze", U6 "Fig. 3.6 — torrid, temperate, frigid zones", U7 "Figs. 3.10 and 3.11"). **p07 item #8** (C-4.3, U3 Elements, Analysis, "Trace the chain of physical environmental linkages…") — same competency, three source-capable LOs (U3 Fig. 3.6/Table 3.1/Fig. 3.8, U4 Table 3.2, U5 Figs. 3.10/3.11). **p07 item #11** (C-4.4, U6 Climate Change, Analysis, "Trace the causal chain from the burning of fossil fuels…") — owns U5 "advancing Fig. 3.10 and retreating Fig. 3.11 monsoon maps". Correctly resolved where it should be: C-4.5's ECR (standard #14, p07 #14) is right — that competency owns no source-capable LO in either file. Net: the library ships 3 SOURCE_INTERPRETATION items where the constitution mandates 6. → **ARV-D-028** |
| R5.1/5.2 saturate & spread | PASS | PASS | Standard probes 10 distinct units across 18 items; p07 all 7. No first-LOs-first clustering. |
| R5.4 demand ceiling | PASS | PASS | No item exceeds its LO's demand in either file. |
| R5 demand floor | PASS (waived) | PASS (waived) | Every competency carries an Analysis-or-higher item except **C-4.1**, whose LOs top out at Application (standard) and Application (p07) — the constitution's explicit waiver ("the ceiling prevails"), correctly applied rather than breached upward. |
| R6 one item ← one LO → one unit | PASS | PASS | `period_ref` is a length-one array on all 36 items; every referenced unit exists. |
| R7 MCQ structure | PASS | PASS | 6 MCQs each: exactly 4 options, exactly one `is_correct`, three diagnostically named distractors; no true/false; no Recall-level MCQ (all Understanding+). |
| R7 arrangement order | **FAIL** (5/6) | **FAIL** (5/6) | Measured across the whole library (18 MCQs, p12 + p10 + p07): **15 of 18 are not in arrangement order**, worse than the 10/18 the pre-v2.0 library scored under v1.5. Standard Q1: "**L**and heats faster… **low**-pressure" labelled A, "**L**and heats… **high**-pressure" labelled B — *high* sorts before *low*, so the order is inverted; the break sits at word 2–4 in 11 of the 15. Consequence: the correct option lands at **B 10 times and A 6 times out of 18 — 89% at A or B, none at D**; under the mandated arrangement it would be A4·B6·C4·D4. → **ARV-D-032**, continuing **ARV-D-018** |
| R8 SI design | PASS | PASS | 3 sub-questions each (within 2–4), labelled, ascending demand, stimulus typed `table` and drawn from the anchored section (atmospheric composition; Punjab flood causes/effects), stem orients only ("Refer to the table provided…") and never describes the stimulus. No map used as stimulus. |
| R8 P4 sub-question ceiling | **FAIL** (1) | PASS | Standard item 11 (C-4.4, U11) sits at **Analysis** while its sub-questions run Recall → Analysis → **Evaluation** — sub-question (c) exceeds the source LO's demand. → **ARV-D-033** |
| R9 open task menu | PASS | PASS | Exactly one OPEN_TASK per assessment, assigned to the Central competency: "Cause-effect map" (standard), "Comparison table" (p07) — both on the menu, both with the teacher-substitution note in the guide, `question_text` correctly "". |
| R10 guide layer | PASS | PASS | All 36 items nest under exactly their own `question_type` key; MCQ `what_each_option_reveals` covers exactly the non-correct labels on every MCQ; SI carries `stimulus_rationale` + one expectation per sub-question. |
| R11 inclusivity | PASS | PASS | Populated where it earns its place (4/18 standard, 7/18 p07), empty elsewhere — no boilerplate. |
| R12 scope | PASS | PASS | Chapter-scoped formative only; nothing summative, cross-chapter, or portfolio-shaped. |
| A1 schema | PASS + note | PASS | Every field present on every item, non-applicable ones `[]`/`""`, no added fields. **Note:** standard items anchored to U4 carry `chapter_section: "Weather and Climate; Elements of Weather and Climate"` — the same stale semicolon form as the handoff (ARV-D-027). |

---

## C. Defects opened

| id | sev | title | remedy |
|---|---|---|---|
| ARV-D-026 | S2 | Register: **4** breaches survive certification (+1 borderline) — `register_scan` pattern gaps ("for two to three minutes", "that will follow", "the Monsoon unit will extend", "explored in upcoming units") | add the patterns, declare the fixes in `repair_register.py`, `--certify-only` |
| ARV-D-027 | S3 | `repair_anchors.py` fixed `section_anchor` on the period only — `coverage_handoff` (all 3 files) and standard `assessment_items.chapter_section` keep the stale `;` form | **ACCEPTED** 2026-08-03 (founder): the `;` slip is a one-off, not a tool-class defect — no fix bought |
| ARV-D-028 | S3 | Rule 4 source-slot resolution not run: 3 Substantive slots took ECRs though the competency owned source-capable LOs | brief clause naming the deterministic pre-step; structural — not textually repairable |
| ARV-D-029 | S4 | Constitution has no synthesis exception — Rule 3 P1 + Integrity Constraint forbid the very unit architecture §0.3 mandates (and its completion claim) | amend LP v1.10 → v1.11 at the stage's P2 |
| ARV-D-030 | S4 | Rule 7 word budget: 4 of 7 `section_context` labels in p07 outside 10–12 words (worst 16) | brief note on compaction pressure |
| ARV-D-031 | S4 | Rule 13 sentence ceiling exceeded in 8 bands across the two files (worst 7) | brief note; the worst are genuinely two moves |
| ARV-D-032 | S3→**S2 proposed** | Rule 7 MCQ arrangement: **15 of 18** MCQs library-wide not arranged; correct option at A or B on 16 of 18, none at D. Third measurement of the same failure (v1.1 → v1.5 10/18 → v1.6 15/18) | **enforce in code** — the arrangement is declared "a convention, never a choice", so sort options + relabel + remap the guide at build time; see §E |
| ARV-D-033 | S3 | Rule 8 P4: standard SI item 11 has an Evaluation sub-question under an Analysis LO | brief/regeneration; not textually repairable |

**Recurrences of open defects** (evidence refreshed, no new id): ARV-D-014 (approach repeats — four consecutive `Inquiry` in the standard), ARV-D-015 (proper nouns in 12 LOs), ARV-D-017 (vestigial `role_handoff`/`unit_handoff`).

**Resolved by the v2.0 re-author:** ARV-D-012 — the U6-homework → U8-materials cross-unit
dependency is gone; no unit consumes another unit's homework in either file. ARV-D-013
(competency codes in band text) did not recur. ARV-D-016 is superseded by the reserved
`synthesis` anchor (now ARV-D-029, a constitution gap rather than a plan defect).

---

## D. What this reads as, overall

**The constitution holds at both lengths, and the compact is not the weaker file.** p07 matches
the standard rule for rule and beats it on approach diversity (multi-label units, honouring
P5), while losing ground only on the two rules that compaction squeezes — `section_context`
word budget and one extra source slot. The v2.0 free-authoring brief has not degraded compact
quality; the pre-v2.0 fear that a shortened plan would read as a summary is not visible here.

**Every failure this pass falls into one family: a deterministic pre-step the model is asked to
carry in prose and does not.** MCQ arrangement (Rule 7), source-slot resolution (Rule 4/5.3),
the sub-question ceiling (Rule 8 P4), the word budget (Rule 7), the sentence ceiling (Rule 13)
are all mechanically checkable and mechanically fixable. The register defects are the same
shape one level down — the gate exists but its pattern list is short. This is the
`register_scan` lesson generalising: **a rule that can be checked in code should not be
enforced by asking a 26k-token generation to remember it.** ARV-D-032 in particular should be
closed by sorting options at build time, not by another brief clause.

**S2 status:** one S2 (ARV-D-026) is open, so per §7 the stage cannot certify until it is fixed
or founder-accepted. It is a same-day fix — four declared repairs and a `--certify-only` run,
₹0.

---

## E. The MCQ arrangement failure, measured across three constitution versions

The library-wide measurement (all 18 MCQs, p12 + p10 + p07):

| | v1.1 (2026-07-16) | v1.5 library (2026-08-01) | **v1.6 library (2026-08-03)** |
|---|---|---|---|
| Rule shape | "vary the correct position; never the same label consecutively" | arrangement + "never led with" (v1.4) | arrangement only, ban struck |
| Not arranged | n/a (no arrangement rule) | 10 / 18 | **15 / 18** |
| Correct option position | 5 of 6 at B | B-cluster moved to A | **B ×10, A ×6, C ×2, D ×0** |
| Under a correct arrangement | — | — | A ×4, B ×6, C ×4, D ×4 |

Three amendments (v1.1 → v1.3 → v1.4 → v1.6), one ₹6 probe, three weeks — and the failure rate
rose. The break sits at word 2–4 of the option text in 11 of the 15, i.e. exactly where
lexicographic comparison stops being visual and becomes an algorithm.

**Why prose cannot win this.** The rule asks a generation, 26k output tokens deep, to sort four
40-word strings by their first differing word and relabel them — a mechanical operation with a
single correct answer, run as the last step of a long creative task. The ₹6 probe passed 2 of 6
in isolation and stated its own caveat; the full runs have now failed it three times at three
different wordings. Nothing about the wording is the problem.

**Why it is teacher-visible (the S2 case).** 16 of 18 correct answers sit at A or B; none at D.
A student who always guesses B scores 56%. That is not contract drift a teacher would not see —
it is an assessment artefact whose answer key is guessable, which is precisely what the
convention was introduced to prevent.

**The fix is a sort.** Option texts and `is_correct` are never touched; only the array order and
the A–D labels change, with `guide.MCQ.what_each_option_reveals` keys remapped to follow. It is
idempotent, applies retroactively to every artefact already on disk, costs ₹0, and — unlike a
brief clause — cannot regress. Once it exists, the constitution's arrangement sentence should
be **struck** at the stage's next P2: a rule the pipeline enforces does not need to spend tokens
in the prompt, and a rule the model reasons about is a rule that reintroduces position as a
salient thing to think about (the founder's own v1.6 reasoning).

### Where the sort lives (the seam question)

The existing pipeline keeps a hard line: **`register_scan.py` is a CHECKER that runs inside
`build_library.py`'s `certify()`; `repair_register.py` is a WRITER the founder runs separately,
then re-certifies.** The option sort belongs on the writer side of that line — but it is *not*
the same kind of writer. A register fix needs a human to decide what clause to delete, so its
edits are declared old→new pairs. An option sort needs no judgement at all: the output is a
pure function of the input. So it should be an **automatic normalizer, not a declared-edit
tool**.

| Seam | What it gives | What it costs |
|---|---|---|
| (a) `generate_canonical.py`, post-parse | every artefact born correct; the model's raw order survives in `out/canonical/*_raw.txt` as evidence | doesn't touch the three files already on disk — needs a one-off backfill; misses any other install path |
| (b) inside `certify()` | one command, retroactive via `--certify-only` | breaks the check/fix boundary the doctrine rests on — a checker that silently fixes can never report a rate |
| **(c) `genon/normalize_options.py`, called by `build_library.py` as an explicit STEP before `certify()`** ← recommended | keeps `certify()` a pure reader; records into `genon_canonical.repairs[]` like the other repair tools; runs under `--certify-only`, so the existing library is fixed for ₹0; `certify()` gains an "options arranged" gate that must now always pass — which is the proof the stage ran | one more file; must be written subject-neutral for the other ten stages |

Implementation, stated so it can be checked: sort key `[w.lower() for w in text.split()]`
(word-wise — "the first word at which they differ"), ascending numeric where all four options
parse as numbers; relabel A–D in the new order with `is_correct` riding its own option; remap
`guide.MCQ.what_each_option_reveals` keys old→new; abort and report any item whose option text
references another label ("both A and B") rather than reordering it; idempotent.

### Outcome (same day, ₹0)

Built and applied. `genon/normalize_options.py` v1.0 is **STEP 6** of `build_library.py`;
certification gained a ninth check, "MCQ options in arrangement order".

- **15 of 18 moved** — the independent measurement and the tool agree exactly.
- Correct-option distribution **A6·B10·C2·D0 → A3·B7·C4·D4**.
- Verified: option texts and `is_correct` byte-identical to the pre-run backup, and every guide
  entry still describes its own option after relabelling. Second run moves 0 (idempotent).
- Library re-certified `20260803_192911` — **ALL PASS**, no re-author.
- Constitution: SS·secondary assessment **v1.6 → v1.7**, arrangement sentence struck;
  prohibition 3 repointed at options that reference another option by label ("both A and B"),
  the one construction a downstream sort cannot reorder without rewriting. Relaxing amendment,
  so no §9 stage re-open.
- One bug caught in the writing: the first draft's numeric key skipped leading non-digits, so
  "Arctic Circle (66.5°N) and…" read as numeric and a correctly-arranged prose item was re-sorted
  by a latitude buried mid-sentence. The key now fires only when an option *opens* with a number.

**The normalizer must count what it moved.** Once options are sorted automatically, the
generation-quality signal disappears unless it is recorded — so the report gains a line
("options arranged: 15 of 18 items re-ordered") and the repairs block carries the per-file
count. Otherwise we lose the only evidence that would tell us whether the model ever learns to
do it unaided.

**The general principle this is the third instance of.** ARV-D-028 (source-slot resolution),
ARV-D-033 (sub-question demand ceiling) and ARV-D-032 are all deterministic pre- or post-steps
carried in prose. The constitution should carry **judgement** — what makes a good distractor,
what a competency genuinely realises. The pipeline should carry **arithmetic** — sorting,
counting, ceilings, budgets. Every rule currently written in prose that a five-line function
could check is a rule that will fail somewhere across 926 authoring runs.
