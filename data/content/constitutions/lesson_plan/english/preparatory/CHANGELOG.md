# CHANGELOG — Lesson Plan Constitution · English · Preparatory Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).

---

## v1.2 — 2026-08-13 · S9 · english · preparatory — the P1/P3 carry-forward, and a duration band that was simply wrong

Drawn class **III** (standard duration **40 min**). Reference: SS·secondary LP v1.10, read
through english·middle v1.7 — preparatory is the THIRD and last stage of the period-field
carrier family's english branch, so the carry-forward ports from its two siblings rather than
from the reference directly.

**A1 — and at this stage A1 is not the usual one-row edit.** Every other stage's A1 replaced
"one or more rows" with one row. This file did that too, but its real defect was the number:
INPUTS 3 read *"`period_duration_minutes` is 30 or 35 at prep (35 default)"*, Rule 2 STEP 1's
ceiling table was stated for 30- and 35-minute periods and named no 40 at all, and the schema
comment read `// 30 or 35`. `master_plan.json` carries **english|III, english|IV and
english|V at `standard_duration_minutes: 40`** — the master-plan calibration band this
campaign authors at. So the constitution named a duration the platform does not use, in three
places, and the variant library would have been authored at the wrong minute count throughout.
It was live rather than theoretical: **three of the four saved preparatory plans carry MIXED
durations inside one plan** (iii ch 2 = 2×40 + 2×35 · iv ch 1 = 5×35 + 2×40 · v ch 1 =
3×35 + 2×40 + 1×30), which is exactly the shape A1 exists to make impossible. INPUTS 3 now
reads *"exactly ONE row … the class-standard duration (40 min for classes up to VII, 45 for
VIII, 50 for IX–X — the master-plan calibration bands, not NCF's flat 40) × the period count
… Preparatory is classes III–V, so every preparatory plan is authored at 40 MINUTES"*, STEP 1
states the 40-minute ceiling alone (2–3 tasks), and the schema follows. Naming only 40 is
deliberate: preparatory spans one class-standard, unlike middle, so a table of alternatives
would invite the author to branch on a number A1 has already fixed.

**A5 + A7 — THE SELF-CONTAINED REGISTER**, one block after VOCABULARY, in the v1.10 three-ban
re-cut (clock quantity · forward reference or completion · calendar time), with backward
continuity welcomed and best carried by naming the content built on. Two consequential
removals came with it, the same two every english stage has had to make: VOCABULARY was
*teaching* the positional cross-reference — its worked examples were literally
`"the previous unit"` and `"this unit"`, which is a unit's position and precisely what ban 2
strikes — and the `teacher_notes` schema comment asked for *"transition from prior unit;
**preview into next**"*, the clause testing.md's P1 names by hand as the english family's known
direct contradiction. `grep -c "the previous unit"` = 0, `grep -c "preview into next"` = 0.

**P3 — `phases[{minutes, description}]` → `time_bands[{minutes, activity}]`**, array and key,
with Rule 5, Rule 2A's "explicit timed phase" and its re-recite band, Rule 3's narration
sentence and its two listening bands, Rule 8's locator mirror, Rule 9's heading
(`PHASE NARRATION` → `BAND NARRATION`), the lint-scope line and the schema all following.
**No `band_id`.** The file now carries **zero occurrences of "phase"**, matching english·middle
and english·secondary. **No plugin work was owed** — `english/subject.py::_bands` has read both
keys, newest first, since S11 landed it on 2026-08-12, which is what keeps the four saved
preparatory plans rendering with a timed spine after the rename. Third time a display debt one
stage paid has made a successor's P3 free.

**Four measured edits, taken here because P-prep is where they are free.**

1. **FULL SPINE COVERAGE replaces Rule 2 STEP 3's drop licence.** STEP 3 said: *"When the
   section's allocated periods are exhausted, stop. Remaining spines/tasks are NOT forced into
   a period … This is an honest reflection of available time, not a defect."* Under
   architecture v2.0 that licenses a chapter's compacts to be a **different chapter** from its
   standard: a library shares ONE registry, `briefs_for()` prints the standard's registry
   verbatim into every compact's brief, and the Xth-unit choice set borrows the unit that FIRST
   deals the next-due cell — which a compact whose registry is a subset does not have. **The
   preparatory corpus does it:** `backup/saved_plans/english/iii/ch_01_*.json` is a 3-unit plan
   whose handoff carries **3 of its summary's 5 cells** — writing and beyond_text simply never
   arrive. Curation moves to TASK level, where Rule 3 already governs it; unfitted TASKS still
   go to homework or ride as flagged self-study pointers, because that half was always honest.
   Rule 10 gained the matching corollary — **absent from the summary is a state, dropped for
   time is a defect.**
2. **Rule 1 gains the closing-unit exception.** v2.0 mandates the standard canonical's
   whole-chapter synthesis unit; Rule 1's "exactly ONE main_section and one or two adjacent
   spines" — with preparatory's extra clause (d), *the secondary spine carries 1 task only* —
   cannot describe it. S7 met this live at C3 (ARV-D-094) and amended mid-cycle; S8, S11 and
   S10 applied it free. Applied free here too. The constitution still names no V-rule: the
   exception describes a closing unit's SHAPE and never mandates one.
3. **Rule 10's item-count line said ONE item per (section × spine) cell.** This stage's own
   assessment constitution **v1.4** (2026-08-12) emits **TWO** — a PAIR on a prescriptive
   per-spine slot table. The two halves of the same stage's pair disagreed on the count, and
   the LP's half is the one the generator reads while it writes the handoff. **S10's sign-off
   predicted this line would be here and free** ("Preparatory carries the same line and is
   free … it should be struck at S9's P1 rather than left for a third discovery"), and it was.
   Corrected to the pair, with the corollary the assessment file already carries: the item
   count does not vary with the period count.
4. **Rule 9 names WHICH SUBHEADING a merged cell uses.** S10 found this at middle, where
   **16 of 96** cells carry a MERGED `section_name`. At preparatory it is not the exception but
   the ordinary case: **93 of 167 cells (55%)** are merged, and the longest is **28 words** —
   *"Let us Read + Let us Think A + Let us Think B + Let us Think C + Let us Think D + Let us
   Think E"* — longer by itself than any brief cap. The pilot's own writing and word_work cells
   are both merged. Without this clause Rule 9 is unsatisfiable at any cap on the richest cells
   in the stage.

**Three numbers moved.** `task_brief` gains the family cap of **≤ 18 words INCLUDING the
Rule 9 locator** — preparatory stated **no cap at all**, against a Rule 9 that mandates the
locator, which is a hole rather than a licence; simulating the locator at its true cost
(+4 words: a 3-word subheading such as "Let us Learn" plus "(p.NN):") puts **14 of 29** saved
briefs over 12 and **0 over 16**, so 12 would have been unreachable and 18 is the number
secondary and middle both settled on. `activity_title` **≤ 10 → ≤ 12** and `section_context`
**10–15 → 10–18**: both are family alignment. The `activity_title` corpus sits *exactly* on the
old cap (max 10 of 20 titles), which is saturation; `section_context` maxes at 13 and does
**not** force its move — recorded as unforced, taken so the english family carries one number
per field rather than three.

**One housekeeping correction.** The footer read *"Version 1.0"* against a v1.1 header — stale
since the 2026-08-11 bump. Now tracks, with the family's `· Internal Document` suffix.

**§9 — costs nothing.** A full constitution change: two relaxations (`task_brief` where none
existed, `activity_title`, `section_context`) and four new obligations (full spine coverage,
the register, the 40-minute single row, the PAIR count). **No english·preparatory library
exists**, so nothing re-opens. S7 paid ~₹106 and a C1–C3 re-run for the same class of finding.

Artefacts: `genon/out/stage_prep_english_preparatory/` — `apply_s9_amendments.py` (27 guarded
replacements, 22 absence guards, 16 presence guards) · `lp_english_preparatory_v1.1_pre.txt` ·
`lp_english_preparatory_v1.1_to_v1.2.diff` ·
`STAGE_SIGNOFF_S9_english_preparatory.md`.

---

## v1.1 — 2026-08-11 · the narration format loses its JSON quote hazard (cross-stage)

Cross-stage amendment made after S8's C1 lost a paid compact to it. Landed ahead of this stage's own P-prep (S9). **One extra correction here:** the Example under this Format line never demonstrated the format — it showed a bare section name with no quoted brief — so a model copying the example would have produced the one shape the rule does not ask for. Made self-consistent.

**The hazard.** This rule mandated a narration format that puts a double-quoted phrase
inside a value the model emits as JSON — `Format: `<spine_section_name> ("brief ≤ 10 words")``. JSON strings are
delimited by `"`, so the inner pair has to be written `\"`, and nothing enforces that.
It is a habit the model keeps for a whole run or drops for a whole run: mathematics III
ch 5 proved both halves on consecutive calls, the standard escaping all 45 of its pairs
and parsing clean, the 11-period compact escaping none of its 42, blowing past the
pipeline's repair bound and costing ₹40.72 for a file that had to be recovered by hand.

**The fix removes the hazard rather than repairing it.** The repair bound was raised the
same day (10 → 500, `genon/generate_canonical.py::parse_with_repair`), but that catches
the mistake after the fact with a heuristic carrying its own magic numbers. Curly
quotation marks (U+201C/U+201D) have no meaning in JSON, need no escaping, and cannot
truncate a file — the mistake stops being possible. Straight *single* quotes would be
equally safe but collide with apostrophes, which this content is full of:
`('Make Amma's rangoli')` reads worse than `(“Make Amma's rangoli”)`. The teacher-facing
text is unchanged in substance and reads better in print.

**§9 — RELAXATION-ONLY, and the wording is what makes it so.** A bare substitution of one
mandated format for another would be a constitution change in the full sense, and would
re-open every stage already authored under the old text. So this amendment *licenses*
rather than switches: the curly form is what the Format and Example lines now show, and
one sentence records that the straight-quoted form **remains valid and is not a defect**.
Nothing is tightened, no new obligation is created (`MUST NOT` count asserted unchanged),
and every existing artefact satisfies the new text by construction. **No library
re-opens.**

**Scope is the narration format only.** The same `("…")` shape appears elsewhere in this
document as prose — register illustrations, prohibition examples — where it is the
document quoting a string to its reader rather than an instruction to emit quotes inside
a value. Those carry no hazard and are untouched.

Artefacts: `genon/out/stage_prep_mathematics_preparatory/` — `lp_english_preparatory_v1.0_pre.txt` ·
`curlyquote_english_preparatory.diff` · `apply_curly_quote_narration.py` (one script, all five
constitutions, exactly-one-occurrence asserts plus a guard that the obligation count is
unchanged in every file).

---

## v1.0 and earlier

No sidecar was kept before this file existed, and the constitution carried no in-document version-history block to lift out. Earlier history is in git.
