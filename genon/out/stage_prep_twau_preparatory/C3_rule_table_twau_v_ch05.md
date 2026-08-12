# C3 · rule-by-rule — the_world_around_us · V · ch 5 *Our Vibrant Country*

**Files read:** `ch_05_canonical.json` (**TOP**, 16 units) and `ch_05_canonical_p13.json`
(**p13**, 13 units — the compact, read deliberately: the variants are authored under the SAME
constitution plus the brief, and a constitution that only holds at full length has not been
proven).
**Against:** LP constitution **v1.4** · assessment constitution **v1.4** — the versions both
files were authored under (LP 19:05, assessment 18:58; first generation 19:47, so the library
does not span versions).
**Date:** 2026-08-12 · **Template:** testing.md v2.9 C3.

**C3 · maths sub-check (determinate answers re-derived): N/A** — scoped to S4/S7/S8. TWAU ships
`expected_elements` / `look_for`, which are judged, not computed; the 2026-08-09 sweep found zero
`expected_answer` items outside mathematics, and this library carries none.

---

## Verdict

**3 FAILs, all on the TOP, and two of them are one item.** p13 is clean against every rule of
both constitutions except the `section_context` cap, which both files breach.

| defect | rule | TOP | p13 |
|---|---|---|---|
| ARV-D-120a — `question_type: "HI"` | assess R3 P1, A1 P1 | **FAIL** | pass |
| ARV-D-120b — `question_text: null` | assess A1 P2 | **FAIL** | pass |
| ARV-D-121 — `section_context` over cap | LP R5 | ~~FAIL~~ **CLOSED** (7 of 16) | ~~FAIL~~ **CLOSED** (2 of 13) |

> **ARV-D-121 · CLOSED BY FOUNDER RULING, 2026-08-12 — accepted as authored, no re-author, no
> amendment.** `section_context` length is not a defect worth spending on: the field is an
> internal label, every breach is an OVERSHOOT (the lower bound was never approached), and the
> v1.4 sentence that does the real work — "name every object the period actually used… do not
> drop an object to fit a length" — was obeyed in all 12 cases. The rule text is UNCHANGED, so
> the consequence is recorded rather than argued: LP Rule 5's 10–25 cap remains on the books and
> a future C3 on this stage will measure the same overshoot. Read a Rule 5 length FAIL as
> pre-ruled unless the breach is a *short* one. Nothing in the library was edited to close this.

Everything else passes, and several things pass in a way worth naming: **contiguity is perfect on
both files** (zero revisits, six runs in registry order), **the prose registry came back byte-identical**,
and **the guide nests correctly on 39 of 39 items across the library**, which pays a debt owed since
2026-07-10.

---

## 1 · LESSON PLAN CONSTITUTION v1.4

| rule | what it requires | TOP | p13 | evidence |
|---|---|---|---|---|
| **VOCABULARY** | "unit" in teacher-facing prose; "period"/"session" only in schema names and the scheduling budget | **PASS** | **PASS** | Regex `\b(periods?\|sessions?)\b` over every `activity_title`, band `activity` and `teacher_facilitation_note` → **0 hits in both files**. The amended clause ("cross-reference by the CONTENT it built, never by its position") is obeyed — see the register row. |
| **THE SELF-CONTAINED REGISTER** · ban 1 | no clock quantity in prose | **PASS** | **PASS** | 0 hits on `\d+ minutes`, "for three minutes", "the remaining time", "half the session". Brevity is expressed **in kind**, as the rule asks: TOP U15 *"Groups do a brief internal rehearsal"*; TOP U16 *"The teacher facilitates brief questions between presentations, keeping the exchange moving"*. The carve-out added at P1 holds: the band's own `"minutes"` field is schema and is untouched. |
| **THE SELF-CONTAINED REGISTER** · ban 2 | no forward reference, no completion claim | **PASS** | **PASS** | 0 hits. Two strings show the rule was understood rather than dodged. TOP U15 closes *"it is an inquiry that continues beyond this sitting, not something declared complete"* — a deliberate refusal of the completion claim. TOP U16, the synthesis, closes *"India's vibrancy is not despite its diversity — it is because of it"*, with its note instructing *"bring back specific content from across the chapter by name … **Name the content, not any particular earlier activity**"* — the register's own prescription, quoted back. TOP U15's *"The unit closes on its own ground"* is the brief's phrase verbatim. |
| **THE SELF-CONTAINED REGISTER** · ban 3 | no calendar time | **SUBJECTIVE-PASS** | **SUBJECTIVE-PASS** | `register_scan.py` reports 0, and an independent read agrees, **with one string a founder should see**. TOP U7 band 30–40: *"an inquiry the class is opening, not closing **today**."* The literal token is present; in context it means "in this sitting", not a calendar day, and asserts nothing unknowable at authoring. Recorded as a judgement because ARV-D-100 is precedent that the scanner under-reports. p13 U7's *"If your state had to choose a new symbol **today**…"* is a hypothetical addressed to students meaning "in the present day" — not a scheduling claim, and not a close call. |
| **INPUTS 4 (campaign A1)** | exactly ONE row `{duration_minutes, count}` at the class standard | **PASS** | **PASS** | `period_schedule` = `[{40, 16}]` and `[{40, 13}]`. 40 min is the Preparatory band on `master_plan.json`'s `the_world_around_us\|V` row. One row, no mixed durations. |
| **DESIGN PRINCIPLE** | sections in reading order are the single axis; `dominant_mode` is metadata, not an axis; both `dual_strand` halves developed through that same sequence; CG descriptions not attached to periods | **PASS** | **PASS** | The axis is the section order (Rule 1 row). No period carries a `cg_codes` field — confirmed by the R9 key-set check. Both strands run through the same six sections: the natural strand in TOP U2 *"Rivers and Mountains in the Anthem"*, U10 *"Forest, Garden, and the Strength of Variety"*, U12 *"Dance Forms on the Map of India"*; the human-cultural in U1, U4 *"School Rules and the Constitution"*, U9 *"Mango in Many Languages"*, U11 *"Headgear from Every Region"*. Neither strand is given units of its own. |
| **RULE 1** · single-axis section anchoring | walk `sections[]` in reading order; every section ≥1 unit; a section may span consecutive units; never reorder, merge out of sequence, skip, or front-load | **PASS** | **PASS** | TOP section index per unit: `1,1,1,1,2,2,3,3,4,5,5,5,6,6,6,6` — six runs `(1,4)(2,2)(3,2)(4,1)(5,3)(6,4)`, **zero revisits**, first-visit order == the registry, all six sections reached. p13: `1,1,1,1,2,2,3,3,4,5,5,5,6` — same shape, `(6,1)` at the tail, zero revisits, all six reached. **No front-loading:** the compact absorbs its three-unit reduction entirely from the LAST section (4 → 1), leaving sections 1–5 intact, which is the opposite failure mode from the one the rule guards. Every anchor is a byte-identical member of `sections[].title` — the property that matters most on this stage, since TWAU is the first stage whose registry token is prose. |
| **RULE 2** · content-driven age calibration | calibrate from the summary's own vocabulary and `conceptual_demand`, not the grade label or the Pedagogy doc | **SUBJECTIVE-PASS** | **SUBJECTIVE-PASS** | Judgement, and the strings it rests on: the register is concrete and local, rising to classification and systems as Grade V should — TOP U7 *"Riddles, Tigers, and Peacocks"*, U9 *"Mango in Many Languages"* at the concrete end; U10 *"Forest, Garden, and the Strength of Variety"* and U12's *"What do you notice about where the dance forms cluster?"* asking for pattern across a map. Vocabulary is the summary's own (saafa/pagri, topi, Ashoka Chakra, tricolour). Nothing is retrieved from the Pedagogy document beyond `dominant_mode`, which Rule 3 governs. |
| **RULE 3** · dominant mode | exactly one per unit, from the closed five; never >2 consecutive; never chosen for variety alone | **PASS** | **PASS** | All 29 values across both files are in `{O&R, HI, D&C, C&E, R&A}`; one per unit; **max consecutive run = 2 in both**, against a cap of 2. TOP spread `D&C 5 · O&R 4 · C&E 4 · HI 2 · R&A 1`; p13 `D&C 3 · O&R 3 · C&E 3 · HI 3 · R&A 1`. *Not for variety alone* is subjective and reads as content-fitted: C&E lands on the make-something units (U3 tableau, U6 emblem, U8 symbol, U14 poster), O&R on the read-and-record units (U2 anthem, U5 currency note, U12 map), R&A on the one values unit (U4 school rules and the Constitution). |
| **RULE 4** · activity-per-period | ONE hands-on activity per unit; a light discussion/reflection may be paired only if it consolidates the SAME activity; explicitly "not a numerical count cap" | **SUBJECTIVE-PASS** | **SUBJECTIVE-PASS** | Read unit by unit: each has a single centre with its discussion band serving it. TOP U12 is the clearest — mark the map, then colour and legend the same map, then a question about that map ("*Does this state share a border with the state whose dance form you marked just before it?*"). No unit runs two independent hands-on activities; U14 (prepare the fair) and U16 (hold it) are separate units, not one loaded unit — which is correct under this rule and is exactly what makes them a pair under ARV-D-119. |
| **RULE 5** · `implied_lo` | one per unit; format "Students can [skill verb phrase]"; observable verbs only; no specific objects or proper nouns | **PASS** | **PASS** | 29 of 29 match `^Students can `. No internal-state verb in either file. *One regex false positive worth recording so it is not re-raised:* p13 U2 reads *"…connect those features to their **knowledge** of the natural environment"* — "knowledge" is a noun, not an internal-state verb; the LO's actual verbs are *identify · record · connect*, all observable. |
| **RULE 5** · `section_context` | compact label of **10–25 words** naming the specific objects, phenomena or tasks | **FAIL** | **FAIL** | **ARV-D-121.** TOP 20–31 words, **7 of 16 over 25** (U5, U7, U12–U16); p13 13–35, **2 of 13 over** (U8, U13). Lower bound never approached in either file. This cap was widened from 10–15 at P-prep the same day on measured corpus evidence (24 periods, range 10–28) and the live run breached the new bound too. The mirror of S4's finding: S4 found the lower bounds too high and paid a C3 re-author; here the upper is too low, twice. **The evidence points at the RULE, not the plan** — the v1.4 sentence "name every object the period actually used… do not drop an object to fit a length" is the rule doing the real work, and the number may be worth dropping rather than raised again. |
| **RULE 5** · `textbook_anchor` | `<section_title> — <paraphrase> (p. N)`; title exactly a summary section; ONE task, ONE page, no ranges | **PASS** | **PASS** | 29 of 29 open with a registry section title verbatim and close with exactly one `(p. N)`. No ranges, no bundles. |
| **RULE 5** · no T-IDs | never reference tasks by internal identifier in any teacher-facing field | **PASS** | **PASS** | Regex `\bT-\d+\b` over the whole of both files → **0 hits**. |
| **RULE 5** · textbook citation in bands | bands that open or work from the textbook weave "Textbook p. N" naturally, page matching `textbook_anchor` | **PASS** | **PASS** | e.g. TOP U12 *"Students open Textbook p. 89 and read through the list of dance forms…"*, anchor `(p. 89)`. Setup/discussion/notebook-only bands carry no citation, as the rule permits. |
| **RULE 5** · `teacher_facilitation_note` | one brief note — open question, grouping, or pacing cue; pacing in KIND; obeys the register | **PASS** | **PASS** | One per unit, all three shapes present. Pacing is given in kind, never in number (see ban 1). |
| **RULE 7** · no period caps | use the full budget for teaching; no maximum; no budget reserved for assessment and no assessment tasks embedded | **PASS** | **PASS** | 16 units against `{40,16}` and 13 against `{40,13}` — the budget is fully spent on teaching. No assessment/test/quiz/marking task in any band. *(One regex false positive: TOP U12's "Each student **marks** the states on their outline map" is the verb "to mark on a map".)* |
| **RULE 8** · time discipline | bands sum EXACTLY to `period_duration_minutes`; at least three bands | **PASS** | **PASS** | TOP 3–4 bands per unit, p13 4–4. **Zero tiling mismatches across all 29 units** — every unit sums to exactly 40. |
| **RULE 9** · coverage handoff | one entry per unit; the eight named keys; `implied_lo` / `section_context` / `textbook_anchor` copied exactly; NO `cg_codes`; never omitted | **PASS** | **PASS** | 16↔16 and 13↔13. Key set is **exactly** the eight specified on every entry — no extra key, none missing. `cg_codes` absent everywhere. All three copied fields are byte-identical to their period's. |
| **RULE 10** · IKS integrated, not labelled | surfaces through faithful use of section content; a facilitation note draws it out where present; NEVER the words "IKS" or "Indian Knowledge Systems"; no dedicated band | **PASS** | **PASS** | The literal tokens appear **0 times** in either file. The summary carries IKS-ish material in *Diversity Everywhere* and *Spirit of Togetherness*, and six TOP notes draw on traditional/heritage material conversationally (U3, U6, U8, U9, U10, U11) — e.g. U11 *"Be prepared for students to name contributors from different communities, religions, and genders"*. No band is dedicated to it. |
| **INTEGRITY CONSTRAINTS** | mapping settled; Pedagogy the sole approach source; LO an output only; TIME = one row, whole budget teaching | **PASS** | **PASS** | No competency is reopened or altered (the mapping's 7 c_codes are consumed by the assessment, not the LP). No LO document is referenced. The amended TIME line (one row) matches the emitted schedule. |
| **AMENDMENT A1** · LP JSON schema | every field populated; no empty string/array on a required field; `visual_aids` null-or-real, never invented | **PASS** | **PASS** | All 12 required period fields populated on all 29 units — zero empties. `visual_aids` is a real, textbook- or class-sourced resource where present (TOP U16 *"Group-created posters and charts from all states represented"*). `period_schedule` carries the single row. |

**One documentation oddity, not a defect:** the LP has **no Rule 6** — Rule 5 is titled
*"(formerly Rule 6)"* and the numbering jumps 5 → 7. Every rule is present and binding; only the
sequence has a hole. Worth tidying at the next amendment so a future reader does not go looking
for a missing rule.

---

## 2 · ASSESSMENT CONSTITUTION v1.4

| rule | what it requires | TOP | p13 | evidence |
|---|---|---|---|---|
| **TWO-FIELD READING RULE** | read `implied_lo` (drives demand) and section content (drives subject-matter) together | **PASS** | **PASS** | Every item's `implied_lo` is byte-identical to its handoff entry's, and every `chapter_section` equals its unit's `section_ref` — so both fields come from the unit the item was built on, and neither is drifting. |
| **DESIGN PRINCIPLE** | one item per unit; text-based summative check; rich activity assessment stays in the LP | **PASS** | **PASS** | 16 and 13 items, 1:1. No item asks for an observation, artefact or project. |
| **RULE 1** · governing purpose | each item traceable to exactly one `implied_lo` (by unit) and one c_code; demonstration observable, never self-report | **PASS** | **PASS** | Every item anchors exactly one unit; every item one c_code. No item asks whether a student understood, appreciated or felt something. No item assesses the teacher or the plan. |
| **RULE 2** · quantity + competency selection | one item per unit, total == units; competency copied VERBATIM; c_code must be in the COMPETENCY DESCRIPTIONS block; no weight tiers | **PASS** | **PASS** | 16/16 and 13/13, `period_ref` covering `1..N` exactly with no unit doubled or skipped. Every c_code is one of the mapping's seven; **every `competency_text` byte-identical** to the mapping's canonical NCF description. No weight field anywhere. Spread is genuinely distributed (TOP: C-4.2 ×4, C-2.2 ×3, C-6.2 ×3, C-1.2 ×2, C-4.7 ×2, C-5.3 ×1, C-6.1 ×1). |
| **RULE 2 · ANCHORING** (A6, new at v1.4) | `period_ref` IS the anchor, emitted directly; multi-unit reach anchors at the LAST; UNIT-level only, no band-level reference | **PASS** | **PASS** | Every item carries `period_ref` as a single-element list. `grep -c phase_ref` = **0** in both files. The multi-unit clause is not exercised on this stage (1:1 by Rule 2) and correctly so. |
| **RULE 3** · question-type selection | type from `{MCQ, SCR, ECR, OPEN_TASK}` — the taxonomy is CLOSED; guidance from `dominant_mode` + CG theme is indicative | **FAIL** | **PASS** | **ARV-D-120a.** TOP's item on U11 carries `question_type: "HI"` — a `dominant_mode` code, not a question type, breaching PROHIBITION 1. **The cause is visible in the rule itself:** Rule 3's guidance table puts `dominant_mode` in the LEFT column and the type in the right (`HI / CG-6 inquiry steps, CG-2 cultural practice \| SCR`), and the model emitted the left. The item's SHAPE is a correct SCR — `guide.SCR` present, three `expected_elements`, `options: []`, `task`/`scaffold` empty — so only the label is wrong. p13's 13 items are all in taxonomy. Type spread otherwise sensible and mode-fitted: TOP `SCR 5 · MCQ 4 · OPEN_TASK 4 · ECR 2`; p13 `SCR 5 · MCQ 3 · OPEN_TASK 3 · ECR 2`. |
| **RULE 4** · cognitive demand | one of the five-point spectrum; metadata, not a question type | **PASS** | **PASS** | All 29 values in `{Recall, Understanding, Application, Analysis, Evaluation}`. Distribution is not recall-heavy: TOP `Application 6 · Understanding 5 · Recall 2 · Evaluation 2 · Analysis 1`; p13 `Understanding 4 · Application 4 · Analysis 2 · Evaluation 2 · Recall 1`. |
| **RULE 5** · OPEN_TASK + performance-task subtype | `performance_task = true` only where the outcome is a physical behaviour, and only on OPEN_TASK; `observation_rubric` required iff true | **PASS** | **PASS** | Zero `performance_task` items in either file, and none is forced. The rule names this subtype as *"common at Grade III"*; class V's OPEN_TASKs are drawing/writing/making products, so `false` throughout is the correct reading, not an omission. No non-OPEN_TASK item sets it. |
| **RULE 6** · MCQ distractor design | exactly four options A–D, exactly one correct; distractors diagnostically intentional and chapter-sourced; no true/false | **PASS** | **PASS** | 7 MCQs across the two files: all 4 options, labels exactly `A B C D`, exactly one `is_correct`, no true/false pair. Each has a `what_each_option_reveals` entry per non-correct label naming the engagement failure. |
| **RULE 6** · A9 (new at v1.4) | order carries no meaning; no option referring to another **by its label** | **PASS** | **PASS** | Zero options matching `both [ABCD] and` / `none of the above` / `all of the above` in either file. STEP 6 re-ordered 11 of 11 items on the library's first pass, which is the evidence that ordering is the pipeline's and not the model's. |
| **RULE 7** · regional-variation note | where an answer is genuinely region-dependent, the annotation says regionally varied answers are correct; not added where the answer is fixed | **PASS** | **PASS** | Applied exactly where it belongs. The U11 item: *"Regional variation note: students from Rajasthan or Himachal Pradesh may give more detailed personal knowledge of saafa/pagri or topi; students from other regions may name headgear from their own community. All are equally valid if they can explain the regional connection. Do not penalise for spelling variation in regional names."* Absent from the textbook-fixed items (flag colours, Constitution date). |
| **RULE 8** · executability boundary | completable in one classroom session; no outside coordination; output observable or collectable that session | **PASS** | **PASS** | No item requires a field visit, an external speaker, community involvement, or materials from outside. No multi-session project. |
| **RULE 9** · guide layer | structured object, never prose; **keyed by the item's own `question_type`**; type's mandated fields present; never flat | **FAIL** | **PASS** | **Consequential to ARV-D-120a, not a separate defect.** 29 of 29 guides are structured objects, **zero flat placements**, and every mandated field is present for its type. The single mismatch is the same U11 item: its guide key is `SCR` while its `question_type` says `HI`, so "keyed by the item's own question_type" fails by the label rather than by the structure — and the guide key is in fact the correct reading of what the item is. **This row is where the month-old debt is paid:** the v1.3 `guide.{TYPE}` mandate (2026-07-10) had been validated synthetically only; across the whole library it is **39 of 39 nested, 0 flat**, so the constitution text now has a live run behind it and TWAU is no longer the last of the three stages owing MEMORY item 1. |
| **RULE 10** · no visual-stimulus expansion | `visual_stimulus` defaults `""`; no new rendering branch; pipe-table rare and not expected | **PASS** | **PASS** | `visual_stimulus` is `""` on all 29 items. No SVG, no table, no new branch. *(This leaves the C13 debt recorded at P-prep untested by this chapter — no TWAU item exercises the pipe-table path, so whether it renders on both surfaces is still unknown rather than proven.)* |
| **RULE 11** · scope boundary | chapter-scoped only; no term/board tests, HPC inputs, portfolios, cross-chapter tracking | **PASS** | **PASS** | Every item is chapter-scoped. Nothing references a term, a board exam, the Holistic Progress Card, or another chapter. |
| **AMENDMENT A1** · item schema | every field present and populated; `""`/`[]` for non-applicable — **never omitted**; no extra fields; `implied_lo` verbatim | **FAIL** | **PASS** | **ARV-D-120b.** No field is *omitted* on any of the 29 items and no extra field appears — but TOP's U11 item carries **`question_text: null`**, and A1 permits `""` or `[]`, never `null`. For an SCR the stem IS the question, so as authored **there is nothing to ask**: the item has three `expected_elements` describing a good answer to a question that does not exist. `implied_lo` verbatim on all 29; `annotation` populated on all 29; `chapter_section` == the unit's `section_ref` on all 29. |

---

## 3 · What this C3 hands forward

**Two defect rows, both already filed.**

- **ARV-D-120** (TOP, U11) — the taxonomy label and the null stem. The type is deterministically
  repairable (`"HI"` → `"SCR"`, which the item's own `guide.SCR` key already declares); **the stem
  is not** — the question has to be written, so this needs a hand repair or a re-author. Note the
  repair must go through a tool that purges derived plans, for the reason S5 found the hard way.
- **ARV-D-121** (both files) — `section_context`. Founder's call whether to widen again or drop
  the upper bound; relaxation-only either way, so no library re-authors.

**Two free certifier gates this stage argues for, neither stage-specific.** Both defects are of
the class testing.md already records for mathematics at ARV-D-084: *nothing in the pipeline reads
the field*. (1) `question_type` must be a member of the subject's declared taxonomy. (2) a
non-OPEN_TASK item must carry a non-empty `question_text`, and an OPEN_TASK must carry `""`. Both
run at `--certify-only` time at ₹0, and both would have caught this item before it was read by eye.

**One thing C3 could not test, carried to C13.** No item in this library exercises Rule 10's
permitted pipe-table path, so the renderer question recorded at P-prep is still open rather than
answered.

**And the observation worth carrying to S9–S11:** the two rules that failed are the two that state
a **closed set or a number** — a taxonomy the model reached past and a word cap it exceeded — while
every rule expressed as a *property* (contiguity, verbatim copying, one-per-unit, exact tiling, no
forward reference) passed on both files without exception. S4's standing lesson about numeric
limits generalises: read the enumerations at P-prep too, and prefer a gate to a sentence wherever
the constitution names a fixed set.
