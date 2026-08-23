# CHANGELOG — Lesson Plan Constitution · English · Secondary Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).

---

## v1.2 — 2026-08-12 · S11 stage prep — A1, the register, P3, and four measured edits

The campaign carry-forward for this stage (testing.md §3, P1/P3), plus four amendments that
are not part of it and were taken at P-prep on measured evidence, where they are free.

**The carry-forward.**

- **A1** — INPUTS 3 was `{ period_duration_minutes, period_count }` with the count "supplied
  at generation time (allocation tab suggests; user may override)". It is now **exactly ONE
  row** at the class-standard duration (50 min at IX–X — the master-plan calibration band,
  not NCF's flat 40), with the note that teacher timetable variation never reaches
  generation and is handled downstream at serve time.
- **A5 + A7 — THE SELF-CONTAINED REGISTER**, one block after VOCABULARY, in the v1.10
  three-ban re-cut (clock quantity · forward reference or completion claim · calendar time),
  with english illustrative strings and the closing backward-continuity sentence. Two
  consequential edits came with it, both the ones S7 and S8 also had to make: VOCABULARY was
  *teaching* the positional cross-reference ban 2 forbids (its examples were literally "the
  previous unit", "this unit") and now names the CONTENT built on instead; and the
  `teacher_notes` schema comment asked for "transition from prior / **preview next**" — the
  forward half being the direct contradiction testing.md P1 names for this family. "session"
  joins the excluded register.
- **P3 — Group B schema conversion.** `phases[{minutes, description}]` →
  `time_bands[{minutes, activity}]`, array and key both, with Rule 5, Rule 9's heading
  (`PHASE NARRATION` → `BAND NARRATION`) and every prose reference following. No `band_id`
  in the target shape — the compiler reads exactly `time_bands` and `activity`. This leaves
  the existing english saved-plan corpus on the old `phases` shape; the english plugin was
  given the same both-keys-newest-first read mathematics has (`subject.py`), which is what
  covers display.

**The four measured edits, all founder calls of 2026-08-12.**

1. **FULL SPINE COVERAGE (Rule 2 STEP 3).** The rule licensed a short plan to stop when a
   section's periods ran out and leave the remaining spines unanchored. The corpus does
   exactly that: `backup/saved_plans/english/ix/ch_12_*.json` (4 periods) carries no
   `beyond_text` contribution at all. Under architecture v2.0 a chapter's canonicals must
   share ONE section registry — a compact is the same chapter in fewer periods, not a
   smaller chapter — so an authoring-time drop breaks the Xth-unit choice set before serve
   ever runs. Coverage is now mandatory at every period count and curation stays at TASK
   level, where Rule 3 already governs it. Rule 10's "a spine with no anchored tasks" clause
   was rewritten to match: absent-from-the-summary is a state, dropped-for-time is a defect.
2. **Rule 1 gains the closing-unit exception.** "Exactly ONE main_section and one or two
   ADJACENT spines" cannot describe a closing unit that draws the whole section together,
   which the platform brief mandates of the standard canonical. S8's lesson applied without
   paying for it twice ("Rule 1's cap was never a risk, it was a certainty"); the
   constitution still names no V-rule and no synthesis mandate.
3. **`task_brief` ≤ 12 → ≤ 18 words**, the locator counted in. Rule 9 mandates the brief
   carry `"<Subheading> (p.NN): <plain brief>"`, which eats 3–4 words of the 12. Measured on
   the real IX corpus: **17 of 28** briefs exceed 12 words as authored; 27 of 28 fit 18.
4. **`section_context` 10–15 → 10–18 words.** Measured: 3 of 11 IX contributions run 16, 16
   and 17. The lower bound is kept — the field is useless at two words.

Also: Rule 2 STEP 1's task budget named a 40-minute and a 60-minute period but not the
**50-minute class standard** this stage authors at. It now does (≤ 3–4 tasks).

**§9.** A full constitution change — but no library for this stage exists, so it costs
nothing. S7 paid ~₹106 and a C1–C3 re-run for the same class of finding.

Artefacts: `genon/out/stage_prep_english_secondary/` — `lesson_plan_constitution_v1.1_pre.txt` ·
`lp_v1.1_to_v1.2.diff` · `apply_s11_amendments.py` (exactly-one-occurrence asserts on every
edit, plus closing guards for the strings that must not come back).

---

## v1.1 — 2026-08-11 · the narration format loses its JSON quote hazard (cross-stage)

Cross-stage amendment made after S8's C1 lost a paid compact to it. Landed ahead of this stage's own P-prep (S11).

**The hazard.** This rule mandated a narration format that puts a double-quoted phrase
inside a value the model emits as JSON — `Format: <spine_section_name> ("brief ≤10 words").`. JSON strings are
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

Artefacts: `genon/out/stage_prep_mathematics_preparatory/` — `lp_english_secondary_v1.0_pre.txt` ·
`curlyquote_english_secondary.diff` · `apply_curly_quote_narration.py` (one script, all five
constitutions, exactly-one-occurrence asserts plus a guard that the obligation count is
unchanged in every file).

---

## v1.0 and earlier

No sidecar was kept before this file existed, and the constitution carried no in-document version-history block to lift out. Earlier history is in git.
