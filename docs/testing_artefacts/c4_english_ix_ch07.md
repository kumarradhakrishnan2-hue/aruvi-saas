# C4 — MEMORY.md amendment items, live · english · IX · ch 7 *Vitamin-M*

**Date:** 2026-08-12 · **Artefacts:** all THREE canonicals (17 / 14 / 10 — C4 reads the whole
library, not C3's pair, because each compact authors its own assessment) · LP **v1.2** ·
assessment **v1.4** · engine 19

Testing.md §4's applicability map, re-checked against the current checklist. Eleven of the
twenty-one items touch this stage.

| Item | Applies | Verdict | Evidence |
|---|---|---|---|
| **1** guide.{TYPE} nesting | SS + TWAU | **N/A** | Not an english shape — its guide is flat (`suggested_answer` / `expected_elements` / `answer_key` / `what_each_option_reveals`), which is what its own schema mandates. |
| **2** MCQ keyed reveals | **english** | **N/A HERE — and the item stays owed** | **The library contains zero MCQ items.** All 18 items across the three canonicals are EXTRACT_ANALYSIS · TRUE_FALSE · FILL_IN · SCR · ORAL_PROMPT · WRITING_TASK · ECR. Rule 4 prefers EXTRACT_ANALYSIS/ECR for analytical Reading LOs at secondary, and the other five spines default to non-MCQ types, so a six-cell english chapter can legitimately produce none. The keyed-reveals contract is therefore untested at S11; **S9/S10 or the first MCQ-bearing english chapter must carry it.** |
| **3** exact item counts | all subjects | **PASS** | 6 contributions → 6 items in **all three** files. English's count rule is structural ("one item per (section × spine) cell", Rule 2) rather than a per-type slate, so there is no slot-type question of the kind S1 found at ARV-D-028. **The v1.4 invariance line held live:** the 10-period canonical produced the same six cells and six items as the 17. |
| **4** split chapters regenerate | **english prep/mid/sec** | **PASS — first live test of the split** | ch 7 IS a split chapter. All three regenerations reproduce the split contract exactly: title `"Vitamin-M (Vitamin-M)"` in the `<section> (<unit>)` form; `main_sections_inventory` = one entry `{A, "Vitamin-M", prose}`; every unit anchors `section_id: "A"`; and the port's singleton-section collapse puts **spines at the top level**. Period spread 17 for a 29-page section, consistent with the effort index (9.6, the class's highest) that set `recommended_periods`. **The english·secondary third of item 4 is discharged; VI/VII/VIII and III remain.** |
| **5** task_density cutoffs | english **middle** | **N/A** | A Grade-VI-calibrated tier boundary reused at VII/VIII. Secondary has its own effort signals; ch 7's `effort_index` 9.6 produced 17 periods against a class mean of ~10, which is a sane spread, but this stage does not exercise the cutoffs. |
| **6** time as a duration vector | — | **CLOSED BY DESIGN** | Recorded here per testing.md's instruction to note the closure the first time it comes up. A1 fixes ONE standard row (50 × N) and the serve engine owns every timetable variation; there is nothing left for a constitution to receive. Confirmed live: all three canonicals carry exactly one row and a single `period_duration_minutes` of 50 on every unit. |
| **7** `Period.approach` populates | maths prep, SS — **and english was the last unchecked family** | **PASS — the item can now close** | `unit_approaches` returns non-empty for **41 of 41 units** across the three files, and the port's `Period.approach` is non-empty for all 41 (`pedagogical_methods` is a `{spine: method}` dict, joined in first-seen order — "comprehension-discussion", "listen-and-respond; oral-presentation"). Zero empties. **Mathematics·preparatory is now the only legitimate empty in the portfolio**, and this item has no unchecked family left. |
| **8** FILL_IN/MATCH shapes | english **prep** | **N/A** | Preparatory's ECR ban and MATCH contract; secondary permits ECR and produced one. |
| **9** Jul 12–13 constitution wave | per file list | **PASS (partial)** | The wave's two english·secondary entries. **LP v1.0** — *"Rule 3 task selection + Rule 4 methods carry secondary additions … check those methods appear and stay within the permitted list"*: every method on all 41 units is drawn from its spine's permitted list, and the secondary additions do appear — `grammar-in-writing` on the reported-speech unit, `domain-vocabulary`, `critical-reading`, `literary-analysis`. **Assessment v1.0** — *"check the deltas actually fire on a secondary drama/poem chapter"*: EXTRACT_ANALYSIS fired in all three files with a verbatim 4-line extract in `visual_stimulus`, and the listening item verified against the summary's baked-in `transcript_text` without opening the appendix. **The drama/poem half did NOT fire — ch 7 is prose**, so `drama_summary`, act-anchored Reading items and role-assigned reading remain untested. ch 11 *Twin Melodies* is class IX's only drama. |
| **10** the referenced word is NAMED | english mid+sec | **PASS** | Zero items across the library say "underlined", "circled", "highlighted", "in bold" or "in italics". The word-level grammar items quote their sentences in full instead — e.g. p10 `Q-VG-A-1`: *"Rewrite each sentence in reported speech… 1. Grandpa said, …"*. The defect this item was written from (`vii/ch_01` `Q-VG-A-1`, "the underlined word" with no underline) does not recur. |
| **11** homework `(p.NN)` locator | english (all) | **PASS** | 6 homework items across the three files, **every one** carrying a locator — `Reflect and Respond (p.98)`, `Learning Beyond the Text (p.119)`, `Vocabulary and Structures in Context (p.113)`, and one using the **section-range fallback** the rule specifies (`p.97–98`) where the task carries no `page_ref`. Zero locator-less briefs. The in-class half is stronger still: 44 of 44 briefs located (C3). |
| **12** FILL_IN table anti-duplication | english (all) | **PASS (vacuously, and say so)** | Four FILL_IN items across the library; **none carries a `visual_stimulus` at all** — the cloze sets are prose with inline blanks, so there is no table to duplicate. No pipe characters in any stem. The rule is satisfied, but by absence: the table-bearing FILL_IN case that produced `vii/ch_02` `Q-VG-B-1` is still unexercised. |
| **13** narrowed A/B ban | english (all) | **PASS — and this is the item's vindication** | p14's `Q-VGR-A-1` emits **Part A (reported speech) + Part B (prepositions), both purely textual, `visual_stimulus: ""`** — exactly the case item 13 narrowed the ban to permit. Under the old blanket "no Part A/B" this well-formed, cleanly rendering item would have been a failure. The hard half also holds: ≤1 visual, no inlining, no part needing its own table. |
| **14–17** number_line · homework book_ref · inclusivity · SS teacher_notes | maths / SS | **N/A** | Other subjects. |
| **18** MCQ position spread | — | **CLOSED BY THE PIPELINE** | Recorded here per testing.md. The position prohibition was struck at P2 (it asks for randomness a model cannot produce) and ordering is deterministic in `normalize_options.py` (STEP 6). The generation-quality signal replacing it is STEP 6's own line: **`options arranged: 1 of 1 item re-ordered` on the first pass** — the library's single options-bearing item (the TRUE_FALSE) needed re-ordering, which is the expected reading, not evidence of a defect. |
| **19** curly-quote narration | 5 LP constitutions | **PASS** | The hazard this closed is a JSON parse failure, and there was none: three generations, `status: ok` on all three, **zero auto-repairs** in the ledger. Note the format itself is not exercised — the band narration in these files does not use the quoted-brief form (see C3's standing note on Rule 9's ≤10-word brief). |
| **20** TWAU mode-vs-type | TWAU | **N/A** | Its `question_type` census is TWAU's. The equivalent check for english — every type in the closed set — passed at C1's item-shape gate on all three files. |
| **21** english·secondary LP v1.2 + assessment v1.4 | **this stage** | **PASS with the four accepted findings** | The item I filed at P-prep, now answered by C1 and C3: full spine coverage held at every count including the floor; the closing-unit exception fired (U17); `time_bands`/`activity` arrived with zero `phases` residue; briefs carried the locator. **The four numeric caps drifted** (`task_brief` 20 w, `section_context` 19/23 w, `expected_elements` 8 of 30 bullets, `time_bands` ≥3 on 4 of 10 floor units) — all four ACCEPTED as authored by founder ruling 2026-08-12, recorded as ARV-D-128/131. **The drama branch remains untested**, as this item predicted. |

---

## Two items change state beyond this stage

**Item 7 has no unchecked family left.** It was written as "confirm the empties are acceptable
live", and its own text named english (S9–S11) as the last stage-family unchecked. English is
now measured — 41 of 41 units carry an approach — so the item reduces to a single standing fact:
**mathematics·preparatory is the only legitimate empty in the portfolio**, and an empty approach
anywhere else is a defect. Nothing is owed by S9/S10 for it: `pedagogical_methods` is the same
field at all three english stages.

**Item 4 is two-thirds owed rather than wholly owed.** english·secondary's split chapters
regenerate coherently; VI/VII/VIII and III have not been tested and are S9/S10's to close.

## One thing C4 recovered that P4 could not

The P4 changelog recorded english·secondary assessment **v1.2 and v1.3 as undocumented** — no
sidecar, no in-document history, MEMORY's inventory stopping at v1.1. **Items 12 and 13 name
both bumps:** v1.1 → v1.2 is the FILL_IN table anti-duplication clause (2026-07-13), and
v1.2 → v1.3 is the narrowed A/B ban (2026-07-13, founder-directed). The changelog gap is now
closed from the checklist rather than guessed at, and both bumps were tested live above.

## What C5 inherits

- **The MCQ path is untested at this stage** (item 2, and C3 said the same of A9's arrangement).
  It is not a defect and not a gap in the library — six cells at secondary legitimately produce
  no MCQ. It is a gap in the *evidence*, and it belongs to whichever english chapter first
  produces one.
- **The drama branch is untested** (item 9). ch 11 is the only drama in class IX.
- **The table-bearing FILL_IN is untested** (item 12) — satisfied vacuously here.
