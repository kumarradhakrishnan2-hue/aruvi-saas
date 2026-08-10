# CHANGELOG — Lesson Plan Constitution · Mathematics · Middle Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).

---

## v3.5 — 2026-08-10 · Rule 5's consecutive-method cap gains an exception (S7 · C1)

Found on ch 7's top canonical, the first artefact ever generated at this stage: units 10, 11
and 12 are all Problem-solving, a run of three against a cap of two. This is **ARV-D-072's
twin** — the same defect, at the same place in the chapter, for the same reason S4 measured at
its own C3. The tail genuinely converges on problem work (extended construction practice →
applying triangle geometry in a real context → the whole-chapter synthesis), and satisfying the
cap there means labelling a unit with a method its content does not support. The evidence points
at the RULE, not the plan.

Ported in substance from mathematics·secondary LP v1.3 (2026-08-09). `MUST NOT` relaxes to
`SHOULD NOT`, and the exception carries its own limits so it cannot be read as a licence: the
cap yields only where the anchored sections genuinely converge, a run produced for convenience
remains forbidden, the default goal→method mapping still binds, and a chapter whose every period
carries one method is a defect rather than an exception.

**§9: RELAXATION-ONLY, so this costs nothing.** Every edit only widens; nothing is tightened and
no new obligation is created. Output authored under v3.4 satisfies v3.5 by construction, and the
clause amended is the very one ch 7's top breached — so the installed canonical becomes compliant
rather than breaching. No re-author. **Timed deliberately: this landed BEFORE STEP 4 bought the
two compacts**, so they are authored against the corrected rule instead of inheriting the breach
and needing the same finding raised twice.

Artefacts: `genon/out/stage_prep_mathematics_middle/lesson_plan_constitution_v3.4_pre.txt` ·
`lp_v3.4_to_v3.5.diff` · `apply_s7_rule5_exception.py` (whose guards assert that exactly one
`MUST NOT` relaxed and that A1, the register and the P3 shape are untouched).

**The standing lesson, now twice-confirmed:** a limit stated as a number is what live generation
most often disproves. S4's other three numeric findings (`activity_title`, `section_context`) did
NOT recur here — ch 7 held every bound this constitution states. Only the consecutive-method cap
broke, in both stages, at the chapter tail.

---

## v3.4 — 2026-08-10 · the campaign carry-forward (S7 · P1 + P3)

Landed at S7's P-prep, before any canonical for this stage was authored (testing.md §3
ordering rule). Ported from the SS·secondary v1.10 reference via the mathematics·secondary
v1.3 adaptation, so the subject's own vocabulary is used throughout. No pedagogical rule
changed: Rules 1–5, 7–9 and 11 are untouched in force, and every edit below is either a
platform fact the model must know or a rename of a field the platform reads.

- **A1 — the period schedule is exactly ONE standard row.** INPUTS 4 was
  "{duration, count} rows; total = B", which licensed the mixed-duration plans the variant
  serve engine cannot use. It now names one row at the class-standard duration (40 min for
  classes up to VII, 45 for VIII, 50 for IX–X — the master-plan calibration bands, not NCF's
  flat 40) and says where timetable variation is handled instead: downstream, at serve time.
  The schema's `period_duration_minutes` carries the same constraint where it is actually
  read.
- **A5 + A7 — THE SELF-CONTAINED REGISTER, as ONE block beside VOCABULARY**, in the v1.10
  three-ban re-cut: no clock quantity, no forward reference or completion claim, no calendar
  time; backward continuity welcome, carried by naming the content built on. Bound by
  reference at Rule 10 (band narration) and at the `teacher_notes` schema comment — never as
  scattered prohibitions. Illustrative strings are middle-maths ones ("a quick mental
  calculation", "having covered all three angle pairs", "Having established that vertically
  opposite angles are equal, …").
- **Two consequential edits the register forced.** VOCABULARY was *teaching* the forward
  reference ban 2 forbids — its cross-reference examples were "the previous unit", "this
  unit" — so the examples are dropped and "session" is added to the excluded register, as at
  secondary. And the `teacher_notes` continuity bullet ("briefly recap what the previous unit
  covered") is now position-free: carry continuity by naming the content built on.
- **P3 — `phases[{minutes, description}]` → `time_bands[{minutes, activity}]`.** The array
  and the key are both renamed, with Rule 6, Rule 8, Rule 10's heading and prose, Rule 11's
  guard case and the schema following. No `band_id` in the target shape — the band layer left
  the declaration surface when the partition engine was retired. `compile.py` reads exactly
  `time_bands` / `activity`: it rebuilds the timed spine from them (`:124`) and asserts an
  inventory invariant over the activity text (`:208-210`), which is why this one could not be
  absorbed by a tolerant read the way the anchor and the handoff are (founder, 2026-08-10).
  `grep -c 'phases\['` = 0, `time_bands` = 2.
- **Footer version corrected** — it had been left at 3.1 through the 3.2 and 3.3 bumps.

**What this pass deliberately did NOT do — founder ruling, 2026-08-10.** No field was
invented to feed the serve engine. `section_anchor` was NOT added to the period object, and
no `period_number` was added to the coverage handoff. Both facts are already in the authored
file — the period's `textbook_segments[].ref` and the handoff entry's `section_ref` — and the
prototype resolved exactly this shape variance at the READ boundary rather than by amendment
(`app/aruvi_streamlit/lp_pdf_generator.py:2583-2592`, and
`assessment_pdf_generator.py:117-192`, which states in terms that "the constitution /
generated JSON is NOT changed — this runs at render time"). The SaaS keeps that answer and
moves it to the sanctioned seam: `aruvi_core/genon/carriers.py` and the mathematics plugin
(CLAUDE.md §3). That is P5.5's work, not this constitution's. The edit script asserts both
absences as guards so a later pass cannot reintroduce them by drift.

Artefacts: `genon/out/stage_prep_mathematics_middle/` —
`lesson_plan_constitution_v3.3_pre.txt` · `lp_v3.3_to_v3.4.diff` ·
`apply_s7_amendments.py` (the reproducible edit script; every edit asserts exactly one
occurrence, and the run closes on guards for the struck A9 arrangement strings, the retired
`phases` shape, `band_id`, `phase_ref`, and the two absences above).

**§9: this is a constitution change in the full sense** — bounds are tightened (one row, not
rows) and new obligations are created (the register's three bans), so the relaxation-only
carve-out does not apply. It costs nothing today because no library for this stage has been
authored yet; that is exactly what the §3 ordering rule buys.

---

## v3.3 and earlier

No sidecar was kept before this file existed, and the constitution carried no in-document
version-history block to lift out. Earlier history is in git.
