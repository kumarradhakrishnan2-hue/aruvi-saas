# CHANGELOG — Lesson Plan Constitution · English · Middle Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).

---

## v1.7 — 2026-08-13 · S10's P-prep — the carry-forward (A1 · A5/A7 · P3) plus four edits the corpus and the sibling constitution forced

Campaign step: `docs/testing.md` §3, stage **S10 · english · middle**, drawn class **VI**
(standard duration 40 min), pilot chapter **ch 8 *What a Bird Thought*** — a poem section,
chosen so the poem-locator rule carried at v3.5 is exercised by live generation rather than
inherited untested. Script, pre-file and diff: `genon/out/stage_prep_english_middle/`.

**A1 — INPUTS 3 is exactly ONE row at the class-standard duration.** It read
`{ period_duration_minutes, period_count } where period_count = B is supplied at generation
time (allocation tab suggests, user may override)` — which licensed precisely the
teacher-chosen, mixed-duration plan the variant-canonical engine cannot use. Every canonical is
now authored at the class standard (40 min for classes up to VII, 45 for VIII, 50 for IX–X —
the master-plan calibration bands, not NCF's flat 40) and all timetable variation is handled
downstream at serve time.

**A5/A7 — THE SELF-CONTAINED REGISTER, one block after VOCABULARY**, in the v1.10 three-ban
re-cut: no clock quantity, no forward reference or completion claim, no calendar time; backward
continuity welcome and best carried by naming the content built on. Two consequential edits came
with it, both places where this file was *teaching* what the register forbids. VOCABULARY's own
examples of a cross-reference were literally `"the previous unit"` and `"this unit"` — a unit's
position, which is exactly what ban 2 strikes — and now name the CONTENT built on, with
"session" joining the excluded register. And the `teacher_notes` schema comment asked for
*"Transition from prior unit; **preview into next**"*; testing.md P1 names this clause by hand as
the known direct contradiction in this constitution, and the forward half is gone.

**P3 — `phases[{minutes, description}]` → `time_bands[{minutes, activity}]`**, array and key,
with Rule 5, Rule 2A's "explicit timed phase", Rule 3's two task-reference sentences, Rule 7's
surface list, Rule 8's locator mirror, Rule 9's heading (`PHASE NARRATION` → `BAND NARRATION`),
the lint-scope line, INPUTS 1 and the schema all following. **No `band_id`** — the band layer
left the declaration surface when the partition engine was retired. The middle saved-plan corpus
stays on the old shape, which is covered: `english/subject.py::_bands` has read both keys,
newest first, since S11 landed it on 2026-08-12.

**Four measured edits, taken here because P-prep is where they are free** (the S4 lesson: a
limit stated as a number is the kind of rule live generation most often disproves, and catching
one at P1 costs nothing).

1. **FULL SPINE COVERAGE replaces Rule 2 STEP 3's drop licence.** STEP 3 said *"When the
   section's allocated periods are exhausted, stop — remaining spines and tasks in that section
   are not anchored … This is not a defect."* Under architecture v2.0 that makes a chapter's
   compacts a **different chapter** from its standard: a library shares ONE registry, the Xth-unit
   choice set borrows *the unit that FIRST deals the next-due cell*, and a compact whose registry
   is a subset of the standard's has no such unit. The corpus does exactly this —
   `backup/saved_plans/english/vii/ch_06_*.json` is a one-unit plan carrying **one** of the
   section's six spines, and `ch_03` carries three. Coverage is now mandatory at every period
   count; curation moves to TASK level, where Rule 3 already governs it, and unfitted TASKS still
   go to homework or ride as flagged self-study pointers. **Absent from the summary is a state;
   dropped for time is a defect.** Rule 10 gained the matching corollary.
   *The arithmetic was swept before the rule was accepted* (the S8 rule): a six-spine chapter
   needs ≥ 4 periods (VocGram alone per STEP 4, plus ⌈5/2⌉ for the rest at ≤ 2 adjacent).
   Sweeping all 46 middle chapters against their `canonical_plan.counts` — VI, VII and VIII —
   **no chapter binds**, and the three VI floors that sit exactly at 4 (ch 2, ch 7, ch 12) are
   saturated but feasible. Unlike english·secondary, which owes ch 12 a floor override, the
   middle stage needs none.
2. **Rule 1 gains the closing-unit exception.** "Exactly ONE main_section and one or two adjacent
   spines" cannot describe the whole-chapter closing unit the platform brief mandates of the
   standard canonical. S7 met this at C3 as a live defect and amended mid-cycle; S8 recorded the
   lesson; S11 applied it for free. Applied here for free too. The constitution still names no
   V-rule — the exception describes a closing unit's SHAPE and never mandates one.
3. **Rule 10's item-count line was contradicting the assessment constitution.** It said *"one
   item per (section × spine) cell"*; assessment v3.6 (2026-08-12) emits **two**. Corrected to
   the pair, with the corollary that the item count does not vary with the period count.
   *(The same stale line is still live in english·secondary's LP Rule 10 — recorded as a
   cross-stage follow-up, not fixed here.)*
4. **`task_brief` ≤ 12 → ≤ 18 words and `section_context` 10–15 → 10–18**, both on measurement
   against the real middle corpus (123 briefs, 26 contributions across VI/VII/VIII). Rule 9
   mandates the brief carry `"<Subheading> (p.NN): <plain brief>"`, and only **13 of 123** saved
   briefs carry a locator at all — the mandate postdates them. Simulating the locator at its real
   cost (+4 words: a 3-word subheading such as "Let us read" plus "(p.NN):") puts **44 of 123**
   over 12 and **0 of 123** over 16; 18 is the same number english·secondary settled on, so the
   family carries one cap. `section_context` runs 16, 16 and 17 words on three VIII contributions.
   `activity_title` stays ≤ 12 — the corpus maximum is 11.
   **Rule 9 also now says WHICH subheading to name**: 16 of VI's 96 cells carry a MERGED
   `section_name` ("Let us read + Let us discuss + Let us think and reflect" — 13 words, more
   than the whole cap by itself), and the brief names the single subheading the task sits under,
   not the merged string. The merged form is the cell's identity, not a location a teacher can
   turn to.

Also added: **Rule 2 STEP 1 now states the 45-minute budget**, the VIII class standard, which the
ceiling table named neither before nor after 40 and 60 — the one duration A1 fixes for a third of
this stage's classes.

**§9.** A full constitution change: two relaxations (`task_brief`, `section_context`) and three
new obligations (full spine coverage, the register, the 45-min line). It **costs nothing** — no
english·middle library exists, so nothing re-opens.

---

## v1.6 — 2026-08-11 · the narration format loses its JSON quote hazard (cross-stage)

Cross-stage amendment made after S8's C1 lost a paid compact to it. Landed ahead of this stage's own P-prep (S10), which is free — no library exists — and means the fix cannot be forgotten when that prep comes round.

**The hazard.** This rule mandated a narration format that puts a double-quoted phrase
inside a value the model emits as JSON — `Format: <spine_section_name> ("brief description up to 10 words....")`. JSON strings are
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

Artefacts: `genon/out/stage_prep_mathematics_preparatory/` — `lp_english_middle_v1.5_pre.txt` ·
`curlyquote_english_middle.diff` · `apply_curly_quote_narration.py` (one script, all five
constitutions, exactly-one-occurrence asserts plus a guard that the obligation count is
unchanged in every file).

---

## v1.5 and earlier

No sidecar was kept before this file existed, and the constitution carried no in-document version-history block to lift out. Earlier history is in git.
