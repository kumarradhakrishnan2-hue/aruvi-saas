# C4 — MEMORY.md amendment items, live · mathematics · IX · chapter 4

**Artefacts:** `ch_04_canonical.json` (15×50, 14 items) · `ch_04_canonical_p12.json` (12×50,
13 items) · `ch_04_canonical_p09.json` (9×50, 9 items) — **all three**, not the C3 pair, since
each compact authors its own assessment.
**Checked against:** `MEMORY.md` §"★ AMENDMENTS TO BE TESTED", applicability map in
testing.md C4, re-read against the live list on 2026-08-09.
**Constitutions of record:** LP **v1.3** · assessment **v1.2**.
**Method:** programmatic battery over all three files; `Period.approach` measured through the
real port (`MathematicsSubject.lesson_plan_to_view`), not by reading the JSON field.

Verdicts: **PASS** · **N/A** (with the reason) · **CLOSED** (no check owed) · **FAIL**.

---

## Applicability — which of the 18 items reach mathematics · secondary

| Item | Scope in the map | Here |
|---|---|---|
| 1 `guide.{TYPE}` nesting | SS + TWAU | **N/A** — maths was never flat; nesting verified anyway at C3 (1 block per item, 0 empty fields) |
| 2 MCQ keyed reveals | english | **N/A** |
| 3 exact item counts | **all subjects** | **PASS** |
| 4 split chapters regenerate | english | **N/A** |
| 5 task_density cutoffs | english middle | **N/A** |
| 6 time vector | — | **CLOSED by design** |
| 7 empty `approach` acceptable | maths **prep**, SS | **PASS** (the "every other stage populates" half) |
| 8 FILL_IN / MATCH shapes | english prep | **N/A** |
| 9 Jul 12–13 constitution wave | **per its file list — maths·secondary IS listed** | **PASS** |
| 10 named referenced word | english mid+sec | **N/A** |
| 11 homework `(p.NN)` | english | **N/A** (english bakes it at generation; maths is item 15) |
| 12 FILL_IN table dedup | english | **N/A** |
| 13 narrowed A/B ban | english | **N/A** |
| 14 `number_line:` stimulus | maths **prep + middle** | **N/A** — secondary already permits SVG figures (VS-2) and was deliberately not changed |
| 15 maths homework locator | **maths, all 3 stages** | **PASS** |
| 16 inclusivity `{support, challenge}` | maths **middle** | **N/A** — prep/secondary left as string by design; shape confirmed below |
| 17 SS `teacher_notes` | SS middle | **N/A** |
| 18 MCQ position spread | — | **CLOSED by STEP 6** |

Five items owed a live check here. All five pass. Two closures recorded.

---

## Item 3 · exact item counts — PASS

Maths·secondary's count rule is Rule 5's PER-LO COUNT: *"Emit exactly ONE item per
implied_lo … does NOT add bonus / mixed-review / chapter-wrap items, and does NOT split one LO
into two items."*

| File | implied_lo | items | per-section mismatches |
|---|---|---|---|
| std | 14 | 14 | none |
| p12 | 13 | 13 | none |
| p09 | 9 | 9 | none |

Checked both directions — not just the totals, but that **every handoff row got exactly as many
items as it declared LOs**. A two-LO section yields two, a one-LO section one, in all three
files. No bonus item, no wrap item, no split.

**Worth contrasting with SS·secondary's C4 result.** There, counting passed but *slot types*
failed (ARV-D-028: three Substantive slots took ECR where Rule 4 mandated SOURCE_INTERPRETATION).
Maths has no per-competency slate to mis-fill — its format is decided item-by-item by the
cognitive-demand hinge — so the SS failure mode has no analogue here, and the hinge itself is
checked under item 9 below. The item-3 split recorded at SS ("counting is solved, slot-type
resolution is separate") does not reproduce.

## Item 7 · `Period.approach` populates — PASS

The premise to confirm is the *other* half of this item: maths-**preparatory** may legitimately
render no approach line; every other subject·stage must carry one. Measured through the port,
so it tests the normalization path the teacher actually sees:

| File | units | empty `approach` | values |
|---|---|---|---|
| std | 15 | **0** | Problem solving ×8 · Deductive ×5 · Discovery/Inquiry ×2 |
| p12 | 12 | **0** | Deductive ×5 · Problem solving ×5 · Discovery/Inquiry ×2 |
| p09 | 9 | **0** | Problem solving ×5 · Discovery/Inquiry ×2 · Deductive ×2 |

Every value is verbatim from the Pedagogy document. (The capital-S `Problem Solving` variant
that made this table disagree with itself was ARV-D-071, repaired at C3.)

## Item 9 · the Jul 12–13 wave, `assessment/mathematics/secondary` v1.0 — PASS

The file's line in the wave list names five contracts. All five hold in all three canonicals:

- **MCQ shape** — every MCQ has exactly 4 options, exactly one `is_correct`, and a
  `what_each_option_reveals` with exactly 3 entries (one per incorrect option). 0 exceptions.
- **NUM guide** — every NUM item carries a populated `expected_answer` **and**
  `method_one_line`. 0 missing. (Their *correctness*, not just their presence, is C3's
  determinate-answer worksheet: 25/25.)
- **Cognitive-demand hinge drives format** — Recall/Understanding → MCQ, Application → NUM/SCR,
  Analysis/Evaluation → ECR: **0 violations** across the three files, with the two known
  OPEN_TASK exceptions excluded and both already dispositioned — std item 14 is now LICENSED by
  assessment v1.2's synthesis clause, and p12 item 9 is the accepted ARV-D-079. Recording that
  explicitly so this PASS is not read as wider than it is.
- **Exactly one item per `implied_lo`** — item 3 above.
- **`effort_index` does NOT leak into assessment format/count/demand** — the explicit
  prohibition. Scanned each whole file for `effort_index`, `conceptual_demand`, `reasoning_load`,
  `exec_load`: **0 occurrences anywhere**, not merely absent from the format fields.

## Item 15 · maths homework locator — PASS

The amendment covers all three stages **by shape, not by stage-branch**: middle/prep emit
homework as dicts needing `book_ref` re-attached at render; **secondary emits strings with the
page already baked in, and must pass through untouched.**

| File | homework items | shape | without a `p.NN` locator |
|---|---|---|---|
| std | 6 | all `str` | **0** |
| p12 | 10 | all `str` | **0** |
| p09 | 6 | all `str` | **0** |

So the secondary branch of `_hw_line` is exercised and correct: 22 of 22 homework items are
strings carrying their own locator, and none needs the middle-stage repair. The dict path stays
owed at S7 (maths·middle) and S8 (maths·preparatory).

## Item 16 · inclusivity shape — N/A, and confirmed N/A

Structured `{support, challenge}` was applied to **middle** only; prep and secondary were
"left as string for now". Confirmed: 36 of 36 guide blocks carry `inclusivity` as a **string**
in all three files. This is the expected shape, so nothing is owed — but it is recorded because
a reviewer meeting a string here after reading the middle-maths amendment would reasonably
suspect a regression. It is not one. S7 owes the object form.

## Item 6 · CLOSED by design — no check owed

The duration vector will never be wired: A1 fixes one standard period row and the serve engine
owns every timetable variation. Already recorded at SS·secondary's C4; re-recorded here as
testing.md C4's footnote directs. Do not reopen.

## Item 18 · CLOSED by the pipeline — census recorded instead

The position prohibition was struck at P2 and ordering is now deterministic
(`normalize_options.py`, STEP 6), so there is no spread to check and no convention to check
either. The census is recorded because **mathematics was the corpus's healthy counter-example**
in the original 2026-07-16 audit — the subject that proved single-letter clustering was a
generation artifact rather than a schema constraint:

| File | correct-option labels |
|---|---|
| std | B ×1, C ×1 |
| p12 | C ×2, B ×1 |
| p09 | no MCQs |

Genuinely mixed, and never A — which is the opposite of the SS/Science clustering that provoked
the rule. Read STEP 6's `options arranged: N of M` line as the generation-quality signal
instead; on this library's first pass it reported 5 items re-ordered with **one SKIPPED**
(p12 #3, cross-references an option label) — the residue of the accepted ARV-D-081.

---

## Verdict

**C4 = PASS.** Five applicable items tested live, all pass; two closures re-recorded; eleven
N/A with the scope reason stated.

Nothing new was filed. The two items that could have produced defects here — the count/slot
question (item 3) and the demand-hinge contract (item 9) — are exactly where SS·secondary
failed at its own C4, and maths passes both, for a structural reason worth carrying: maths has
no per-competency slot slate to mis-fill, because its format is decided item-by-item from the
LO's own demand.

**Owed elsewhere, noted so it is not met as a surprise:** item 15's dict path (S7, S8),
item 16's `{support, challenge}` object (S7), and item 14's `number_line:` stimulus (S7, S8) —
all three are maths items that this stage cannot exercise.
