# C4 — MEMORY.md amendment items, live · social_sciences · secondary

**Stage** S1 social_sciences·secondary · **class drawn** ix · **pilot chapter** 3
("Climate — Weather, Climate and Climate Change")
**Artefacts read** `data/content/saved_plans/social_sciences/ix/ch_03_canonical.json` (12 units,
18 items) · `…_p09.json` (9 units, 18 items) · `…_p07.json` (7 units, **17 items**)
**Provenance** LP v1.10 · assessment v1.5 · engine e10 · ledger 20260801_143756 (+ register
repair 2026-08-02T11:16:56) · model claude-sonnet-4-6
**Date** 2026-08-02 · **Actor** Claude · **Verdict** **C4 CLOSED** — 2 pass · 1
pass-with-correction · 2 fail, both dispositioned by the founder the same day (ARV-D-018 resolved
in part by assessment v1.6; ARV-D-019 **accepted, no back-fill**). No item blocks the stage.

---

## 1. Applicability map

testing.md's C4 table re-checked against the live MEMORY.md list. Five items apply.

| Item | Subject of the amendment | Applies here? | Why |
|---|---|---|---|
| 1 | SS + TWAU assessment `guide.{TYPE}` nesting | **YES** | SS assessment constitution v1.5 Rule 10 |
| 2 | English MCQ keyed reveals | no | English only |
| 3 | Constitution exact item counts | **YES** | "all subjects" |
| 4 | English chapter splits | no | English only |
| 5 | English-middle `task_density` cutoffs | no | English middle only (X2 owns it) |
| 6 | Wire time into the constitutions | **CLOSED BY DESIGN** | A1 + serve engine; closure recorded in MEMORY.md today |
| 7 | `Period.approach` empties | **YES** | list names SS |
| 8 | English-prep FILL_IN / MATCH | no | English prep only |
| 9 | Jul 12–13 constitution wave | **N/A here** | its file list is 6 English + 3 maths + 2 science files; neither SS·secondary constitution is in it |
| 10 | Named referenced word | no | English mid+sec |
| 11 | English homework `(p.NN)` | no | English only |
| 12 | FILL_IN table dedup | no | English only |
| 13 | Narrowed A/B ban | no | English only |
| 14 | `number_line` stimulus | no | maths prep+mid |
| 15 | Homework `book_ref` | no | maths |
| 16 | `inclusivity {support, challenge}` | no | maths middle |
| 17 | SS `teacher_notes` introduced | **N/A here** | amendment was to SS **middle** v1.6; SS·secondary carried teacher notes already (S2's C4 owns it) |
| 18 | MCQ correct-answer position | **SUPERSEDED BY A9** | check the convention, not the spread — closure recorded in MEMORY.md today |

---

## 2. Item 1 — `guide.{TYPE}` nesting · **PASS** (3/3 files, 53/53 items)

Every item's `guide` is a dict with **exactly one key, equal to its own `question_type`**; zero
items place a type's fields flat under `guide`. Inner field names match Rule 10 exactly:

| guide key | emitted fields | Rule 10 requires |
|---|---|---|
| `guide.MCQ` | `what_each_option_reveals` | same |
| `guide.SCR` | `expected_elements` | same |
| `guide.ECR` | `look_for` | same |
| `guide.SOURCE_INTERPRETATION` | `stimulus_rationale`, `sub_question_expectations` | same |
| `guide.OPEN_TASK` | `what_this_demonstrates`, `reading_the_scaffold`, `strong_vs_weak_markers`, `format_type`, `format_rationale` | same (5/5) |

Evidence (top canonical, item 1, C-4.2 MCQ):
`"guide": { "MCQ": { "what_each_option_reveals": { "A": "Confuses the mesosphere …", "C": …, "D": … } } }`
— one entry per non-correct option, correct label absent, as Rule 10 specifies.

**This is the first live exercise of the SS `guide.{TYPE}` mandate** (it had only ever been
validated by an in-place corpus migration). It holds. MEMORY item 1 is confirmed for SS; TWAU
still owes its half at S5.

---

## 3. Item 3 — exact item counts · **FAIL** (ARV-D-019)

Rule 4 counts are declared EXACT. Expected total for this competency mix
(1 Central + 3 Substantive + 2 Present) = **5 + 3×3 + 2×2 = 18**.

| Competency | Weight | top (12u) | p09 (9u) | p07 (7u) |
|---|---|---|---|---|
| C-4.2 | Central | 5 ✅ MCQ·SCR·SI·ECR·OPEN_TASK | 5 ✅ | 5 ✅ |
| C-4.3 | Substantive | 3 ✅ MCQ·SCR·ECR | 3 ✅ | 3 ✅ |
| C-4.4 | Substantive | 3 ✅ | 3 ✅ | 3 ✅ |
| C-4.5 | Substantive | 3 ✅ | 3 ✅ | **2 ❌ MCQ·SCR only** |
| C-4.1 | Present | 2 ✅ | 2 ✅ | 2 ✅ |
| C-4.6 | Present | 2 ✅ | 2 ✅ | 2 ✅ |
| **Total** | | **18 ✅** | **18 ✅** | **17 ❌** |
| OPEN_TASK count | (exactly 1) | 1 ✅ | 1 ✅ | 1 ✅ |

**The failure.** In `ch_03_canonical_p07.json`, C-4.5 is `weight: 2` (Substantive) in its own
`coverage_handoff` and its items carry `weight_label: "Substantive"`, yet only two items are
emitted — the mandated third slot (SOURCE_INTERPRETATION **or** ECR) is missing. No exemption
covers it: the competency owns 2 LOs against 3 slots, which is Rule 5 case 5 (SURPLUS — "fill
extra slots by reusing a single LO at a lower demand rung"), not a licence to drop a slot. Both
emitted items sit at Evaluation, so the missing slot is the ECR — the highest-demand item for the
chapter's climate-crisis competency has simply gone.

Teacher-visible: at 7 periods the climate-change/flood-case competency is assessed by recognition
and short response only. **S2.**

**FOUNDER RULING 2026-08-02 — ACCEPTED, NO BACK-FILL.** Slot misses of this kind are generation
variance, not a systematic breach: the model dropped one slot in one compact variant of one
chapter. Regenerating at ~₹37 a run to recover a single ECR is a lottery ticket priced above the
loss, and a hand-authored back-fill is forbidden outright (§7). The competency remains assessed by
two items at Evaluation demand; nothing downstream reads item counts, so no serve, export, anchor
or view path is affected. **ARV-D-019 → status `accepted`, owner founder.** It does not block
certification, and the p07 variant stands as authored at 17 items.

**Certification cannot see this.** `build_library.py::certify` runs eight structural checks
(completeness, compile, anchors, first-visit, coverage, closing mandate, serve sweep,
projected-vs-actual) plus the register scan — **none counts items per competency**. The p07 file
passed ALL PASS and shipped 17 items. A ninth deterministic check (weight → exact count, per
subject constitution) is the cheap fix; noted for C8.

**Side check, not a defect:** the Rule 5 DEMAND FLOOR shows no Analysis+ item for C-4.1 in all
three files — legitimately waived, because C-4.1's LOs top out at Application/Understanding in
every variant and "the ceiling always wins".

---

## 4. Item 7 — `Period.approach` · **PASS, with the item's premise corrected**

MEMORY item 7 predicted SS renders **no** approach line. That is now stale. SS·secondary LP v1.10
Rule 9 mandates `pedagogical_approaches` (a list, verbatim from the NCF Pedagogy document, `[]`
only where a unit is genuinely diffuse) and `SocialSciencesSubject.lesson_plan_to_view` joins it
with "; " into `Period.approach` — the same pattern English uses.

Measured through the real port on all **28 authored units** (12 + 9 + 7): **0 empty**.

| File | Approaches emitted |
|---|---|
| top | Inquiry ×4 · Issues-based learning ×4 · Project work ×2 · "Issues-based learning; Reflective essays" · Role plays and simulations |
| p09 | Inquiry ×3 · Issues-based learning ×4 · Project work · "Issues-based learning; Reflective essays" |
| p07 | Inquiry ×2 · Issues-based learning ×2 · two mixed pairs · "Issues-based learning; Reflective essays" |

All five distinct approaches appear verbatim in
`data/content/framework/social_sciences/secondary/pedagogy_secondary_social_sciences.txt`. The
Overview tab's Pedagogy row populates for this stage. **The only remaining legitimate empty is
mathematics·preparatory**; for SS an empty approach is now a defect, not an expected state.
MEMORY item 7 amended in place today.

---

## 5. Item 18 → Amendment A9 — MCQ option order · **FAIL** (ARV-D-018)

Item 18's prohibition (spread the correct position; no same-label runs) is replaced by A9's
convention, present verbatim in assessment v1.5 Rule 7: *author the four options first; then, as
the LAST step before emitting, arrange all four — the correct one included, never led with —
alphabetically from the first word at which they differ, ascending where numeric, label A–D in
that order.* Under A9 uneven letters are explicitly "coincidence, not a defect", so the checked
thing is **whether the ordering step ran**.

It largely did not. **10 of 18 MCQs are not in alphabetical order.** Robust under three
comparators (raw string, punctuation-stripped, word-token) — all three agree item-for-item.

| Variant | MCQs | Misordered | Items |
|---|---|---|---|
| top | 6 | 3 | C-4.3, C-4.4, C-4.1 |
| p09 | 6 | 2 | C-4.4, C-4.5 |
| p07 | 6 | **5** | C-4.3, C-4.4, C-4.5, C-4.1, C-4.6 |

Breaks are early and unambiguous, not tie-break subtleties:

- top · C-4.3 — B `"Hot land creates **low** pressure…"` precedes C `"Hot land creates **high**
  pressure…"`; they diverge at word 4, `high` < `low`. B is the correct option, so the deviation
  moved the answer one label earlier.
- top · C-4.4 — A `"A **weak** monsoon…"` precedes B `"A **strong** monsoon…"` (word 2).
- top · C-4.1 — C `"The **southern** tip (around Kerala)…"` precedes D `"The **northern**
  plains…"` (word 2); C is correct, again one label earlier than the convention gives.
- p07 · C-4.4 — the correct option is at **label A**, which Rule 7's "never led with" forbids
  outright; alphabetical would have placed a distractor (`"Accelerated evaporation…"`) first.

Correct-position distribution (recorded, but **not** a defect under A9): top {B:4, C:2} ·
p09 {B:3, C:2, D:1} · p07 {B:5, A:1} — 12 of 18 on B. This is what ARV-D-003 recorded as
clustering; under A9 the clustering is only a symptom, and the cause is the unrun ordering step.

**A rule conflict surfaced — RESOLVED 2026-08-02, assessment v1.5 → v1.6.** On 2 of the 18 (p07
C-4.3 and C-4.5), strict alphabetical order places the **correct** option at label A — which the
same sentence forbade ("never led with"). Rule 7 named no tie-break, and PROHIBITION 3 ("MUST NOT
depart from the arrangement to move the correct answer toward or away from any label") forbade the
only remedy. **Founder ruling: the ban is removed** — two words struck, nothing added. Rule 7 now
reads "arrange all four — the correct one included — alphabetically from the first word at which
they differ, ascending where they are numeric, and label them A–D in that order. Uneven letters
across a chapter are coincidence, not a defect." An affirmative replacement naming A as a legal
landing was drafted and rejected: naming label A in the rule at all makes A salient and invites
the model to reason about position, which is precisely what the convention exists to prevent. The
rule states only what the arrangement IS. Prohibition 3 unchanged and now carries the guard alone.
This partially reverses v1.4, whose probe evidence ("distractors sorted, correct answer pulled to
A") the ban was built on; that tell is deliberately surrendered.

**Consequences to record.**
- **Relaxing amendment** — no artefact authored under v1.5 becomes non-compliant. p07 C-4.4
  (correct at A) is compliant under v1.6. It remains a **misordering** failure on its own merits
  (alphabetical would place a distractor first), so the count is unchanged at **10/18**.
- **§9 applies but the cost is a decision, not an inevitability.** A constitution change nominally
  re-opens the stage in full (C1 regenerates, ~₹146). Because this amendment only removes a
  prohibition, the founder may instead **accept the v1.5-authored library under v1.6** — a
  recorded accept, not a silent one. Provenance for this stage now reads assessment **v1.6** while
  the library carries v1.5, so the tracker will show amber until that accept is entered.
- **P2 re-opens for the other ten stages in the good way:** they have not been amended yet, so
  each receives A9 in the **v1.6 wording**. No stage should ever be given the v1.4/v1.5 sentence.

---

## 6. Defects opened

| id | sev | step | status | title |
|---|---|---|---|---|
| ARV-D-018 | S3 | C4 | **open, owned** | Amendment A9's option-order step is not running — 10/18 MCQs not alphabetical. The clause collision half is CLOSED by assessment v1.6 ("never led with" struck). The ordering failure stands: it is a prompt-adherence problem, and the standing recommendation is to move the arrangement out of the constitution into `compile.py` as a deterministic relabel. S3 → does not block certification. |
| ARV-D-019 | S2 | C4 | **accepted (founder, 2026-08-02)** | p07 emits 17 items, not 18 — Substantive C-4.5 missing its mandated third slot. Ruled generation variance; no regeneration, no back-fill. Does not block certification. |

Neither is a `repair_register.py` candidate (§7: only declared text edits qualify; structural and
pedagogical defects go to the gate or to a regeneration decision). ARV-D-019 could not have been
repaired in place in any case — a missing ECR must be authored, and hand-authoring an artefact is
forbidden.

**The one follow-on, separated from the ruling — BUILT 2026-08-02.** Accepting the *outcome* and
detecting the *occurrence* are different decisions, and the founder approved the detector while
accepting the outcome. `certify()` now carries a **tenth check, item counts per competency,
ADVISORY** (`genon/build_library.py`, `EXACT_ITEM_COUNTS` + `item_census`; testing.md C5.10):
items are grouped by competency and compared to the mandated count for that weight label, read
from `EXACT_ITEM_COUNTS[(subject, stage)]` where the constitution has been read at P2 and
otherwise from the modal count across the library's own variants — the fallback catches a variant
disagreeing with its siblings without knowing any constitution, and reaches the same 5/3/2 here
independently. A handoff competency the assessment never touches reports as 0. It reports and
never fails, so ch 3 stays ALL PASS. Verified on the live library both ways:

```
item counts per competency — ADVISORY, does not gate; basis: constitution
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_03_canonical.json: 18 items vs 18 expected
      ch_03_canonical_p09.json: 18 items vs 18 expected
      ch_03_canonical_p07.json: 17 items vs 18 expected  <-- MISS
          C-4.5 (Substantive) has 2, constitution says 3
```

ARV-D-019 stays accepted; this only makes the rate visible.

## 7. MEMORY.md edits made (per testing.md C4's instruction to record closures)

1. **Item 6** — CLOSED BY DESIGN, with the reason (A1 + serve engine own all timetable variation;
   nothing left for a constitution to receive; do not reopen).
2. **Item 7** — tested live and its premise corrected: SS is no longer an empty-approach subject;
   maths·preparatory is the only legitimate empty remaining.
3. **Item 18** — SUPERSEDED BY A9, with the first live result (10/18 fail), the retirement of the
   old spread check, and the clause collision flagged for a founder ruling.
