# C3 — rule-by-rule compliance: social_sciences · ix · chapter 3 (Atmosphere and Climate)

Canonical: `ch_03_canonical.json` · ledger `20260729_192438` · handoff_rev 1 (title backfill)
Checked against: **LP constitution v1.7** · assessment constitution v1.2 · mapping `ch_03_mapping.json`
Checker: Claude · 2026-07-29 · method: programmatic battery + judged reads (quotes given for every judgement)

Verdicts: **PASS** (checked, clean) · **PASS·subj** (subjective judgement, evidence quoted) ·
**FAIL** (defect filed) · **OBS** (observation, no defect).

## Lesson-plan constitution v1.7

| Rule | Verdict | Evidence |
|---|---|---|
| VOCABULARY | PASS | No "period"/"session" in teacher-facing prose; units named as units. |
| SELF-CONTAINED REGISTER | **FAIL** | P8 teacher_notes: "The monsoon mechanism explored in **the previous unit** now grounds…" — position reference, banned explicitly. → **ARV-D-002**. Word-list survivors judged compliant: P1.2 "your earlier list" (refers to an artefact students hold; survives any re-cut), P4.2 "hour-to-hour and day-to-day" (the text's own definition of weather — content, not the sitting's clock). |
| INPUTS 4 / TIME | PASS | `period_schedule` = exactly `[{50, 12}]`; every period 50 min; bands tile 0→50 contiguously in all 12 units. |
| R1 age calibration | PASS·subj | Tasks calibrated to summary's demand (pie-diagram reading, layer mapping, cause-table analysis); no pedagogy-document leakage detected. |
| R2 cognitive floor | PASS·subj | Sampled bands demand application/analysis, e.g. P1.2: students classify which named function explains each predicted consequence — not recall. |
| R3 section anchoring | PASS | All 12 units carry a named `section_anchor` traceable to the summary (Introduction → Composition → Structure → Weather and Climate → Elements → Seasons → Monsoon ×2 → Climate Change ×2 → Punjab Floods ×2). |
| R4 full coverage | PASS | 9 substantive sections all covered across 12 units; long sections (Monsoon, Climate Change, Floods) correctly span 2 units with distinct `section_context` slices; `section_coverage_note` null (no shortfall). Note: summary carries no machine-readable headings, so coverage was judged from anchors vs summary prose, not a mechanical diff. |
| R5 edges unforced | PASS | 22 edges; every c_code ⊆ mapping; zero weight drift; no vocabulary-only pairings detected on sample. |
| R6 implied_lo | PASS·subj | All 22 LOs "Students can …" with explicit demand (3 Und / 4 App / 9 Ana / 6 Eval); no internal-state verbs. "Earth" appears in one LO — generic scientific term, not a chapter-specific proper noun; judged compliant. |
| R7 section_context | PASS | All 12 in the 10–12-word band (7–16 tolerance applied); data-work units name their artefact (pie diagram P2, cause table P11). |
| R8 emphasis, no force-fit | PASS | Weights steer depth only (Central C-4.2 owns 6 edges); `competency_gap_note` = "" and every mapped competency has ≥1 genuine edge. |
| R9 approach diversity | PASS·subj | Labels drawn from the Pedagogy set; no banned "Conversations…" tag. P1–P3 all tagged `Inquiry`, but the *activities* differ in type (thought experiment / diagram reading / mapping) — prohibition targets activity type, judged compliant. |
| R10 teacher notes | **FAIL** | All 12 non-blank, 3–5 sentences, no "Transition" openers. Two violations: P8 position reference (above) and P10 "…deliberately bridges **C-4.5 and C-4.6**" — c-codes cited in a teacher-facing note, banned verbatim. → **ARV-D-002**. |
| R11 homework | PASS | `[]` by default; single item at P6 (within 1–2 allowance). |
| R12 coverage handoff | PASS | Present as sibling; competencies in exact mapping order (C-4.2 … C-4.6); 22 LO rows = 22 edges; every field byte-identical to its source edge/period; no zero-edge competency included. |
| R13 band substance | PASS·subj | Bands are teaching script: content named, task stated, questions given (P1.2 quotes the classification question verbatim). No pointing-without-carrying detected on sample. |
| R14 band identity | PASS | All 36 band_ids exactly `P<n>.<ordinal>` in sequence; every `band_refs` ⊆ its own unit; no all-bands defaults on 3+-band units; handoff copies verbatim. |
| R15 role handoff | PASS + OBS | Covers exactly the 36 band_ids, in plan order, values all valid. **OBS:** mix is perfectly uniform — 12 hook / 12 development / 12 consolidation, one per unit. Consistent with honest 3-phase pedagogy, but also consistent with shaping-in-anticipation (proh 1), which is unprovable from output alone. Watch across combos: if every chapter emits exactly H-D-C ×N, the anticipation ban is being violated structurally. |
| R16 unit handoff | **FAIL** (marginal) + OBS | 11/11 adjacent entries in order; titles post-backfill derived per v1.6/v1.7. Two notes exceed the 90-word cap: 3-4 (92), 10-11 (93) → **ARV-D-005 (S4)**. OBS: 3 validator title flags are "and" inside disciplinary collocations ("weather and climate", "advancing and retreating monsoon") — judged false positives; validator refinement pending (ARV-D-001 thread). Title lengths 61–83 chars, 5 over the soft 70 (see ARV-D-001 discussion). |
| INTEGRITY | PASS | Mapping settled (no add/drop/re-weight); LOs are outputs; single standard row; anchoring absolute; teaching-layer fields never enter handoff; handoff verbatim. |
| A1 schema | PASS | Every required field populated; edges carry no period_number; visual_aids null where none. |
| A2 schema | PASS | Verbatim regrouping verified programmatically (0 mismatches across 22 rows). |

## Assessment constitution v1.2 (items ride in the same canonical)

| Rule | Verdict | Evidence |
|---|---|---|
| R1 purpose | PASS·subj | Sampled items demand observable products (classification, table completion, justified essay). |
| R2 edge inheritance | PASS | Every item's competency = its source LO's; `implied_lo` verbatim (18/18 matched to a handoff row). |
| R3 executability | PASS·subj | No multi-session/field/coordination tasks; Open Task is an in-class comparison table. |
| R4 weight architecture | PASS | Exact counts: Central C-4.2 = MCQ+SCR+SI+ECR+OPEN_TASK (5); Substantive C-4.3/4.4 = MCQ+SCR+ECR, C-4.5 = MCQ+SCR+SI (source-capable slot correctly resolved); Present C-4.1/4.6 = MCQ+SCR (2). 18 items total; exactly one Open Task, on the Central competency; weight labels never integers. |
| R5 LO-to-slot | PASS | Demand-match holds; demand floor: C-4.1 has no Analysis+ LO (both Application) → floor legitimately waived by the ceiling; every other competency carries Analysis+. |
| R6 one item ← one LO | **FAIL** (1 item) | `period_ref` singular everywhere; `implied_lo` verbatim. One `phase_ref` drift: C-4.2 item on P5 carries `["P5.2"]` where the LO's `band_refs` = `["P5.2","P5.3"]` — Rule 6 proh 4 requires a verbatim copy, never a subset. → **ARV-D-004 (S3)**. |
| R7 MCQ design | **FAIL** | 4 options / one correct / plausible distractors: yes. **Correct-answer position: B,B,B,B,C,B — 5 of 6 on B, four consecutive** — proh 3 violated live (this is MEMORY item 18's exact failure mode, recurring after the constitutional fix). → **ARV-D-003 (S2)**. |
| R8 SOURCE_INTERPRETATION | PASS·subj + OBS | Both SIs carry typed `table` stimuli from their anchored sections, 3 sub-questions, capped at LO demand. OBS: C-4.2 SI demands run Recall→Application→Application — non-decreasing but plateaued; "ascending" read strictly would fail the third sub-question. Judged acceptable; watch across combos. |
| R9 open-task menu | PASS | Comparison table — on the menu; guide notes teacher substitution right. |
| R10 guide layer | PASS | 18/18 guides keyed by exactly the item's own question_type. |
| R11 inclusivity | PASS·subj | Notes present where useful, no boilerplate detected. |
| R12 scope | PASS | Chapter-scoped formative only. |

## Defects filed

| Id | Sev | What |
|---|---|---|
| ARV-D-002 | S2 | Register/Rule 10 violations in teacher notes: P8 "the previous unit" (position), P10 "bridges C-4.5 and C-4.6" (c-codes). 2 of 12 notes. Text-repair backfill is cheap; generation-quality signal recorded for C4. |
| ARV-D-003 | S2 | MCQ correct answers cluster 5/6 on B with 4 consecutive — assessment Rule 7 proh 3 fails live despite the v1.1 amendment (MEMORY item 18 recurrence). |
| ARV-D-004 | S3 | One item's `phase_ref` is a subset of its LO's `band_refs` (P5, C-4.2) — verbatim-copy contract broken. |
| ARV-D-005 | S4 | unit_handoff notes 3-4 and 10-11 at 92/93 words vs ≤90. |

**Bottom line:** the partition-facing architecture (A1 schema, bands, tiling, Rule 14/15 declarations, handoff verbatim-ness) is **fully clean** — the engine contract held on the first live run. The failures are register discipline in prose (2 notes), MCQ position spread, one phase_ref subset, and two marginal word counts — all content-repairable without regeneration, and all recorded as live-generation quality signals for the C4 sweep.
