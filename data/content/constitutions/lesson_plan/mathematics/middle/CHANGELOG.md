# CHANGELOG — Lesson Plan Constitution · Mathematics · Middle Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).

---

## v3.8 — 2026-08-10 · the SURPLUS bullet is deleted — it was the cause, not the cure (S7 · C9)

Founder's question, on seeing p10's closing unit hoard 4 of 10 assessment items: *"despite in
constitution we are asking it to deal in contiguous periods, why is this happening? did our
instruction to deal in depth if more time available cause this problem? do we have similar
provision in maths IX?"* All three answers are in the artefacts, and the last one settles it.

**The plans were authored under v3.6**, which already carried the contiguity sentence — so this
was not a stale-rule breach. **And only ONE of the three maths constitutions carried a surplus
provision.** `grep -cio "surplus|deepen|more time|extra time"`: middle **1**, preparatory **0**,
secondary **0**. Maths IX's Rule 7 says only *"A section may span more than one period where its
content warrants it"* — a permission, with no notion of leftover budget — and maths IX produces
zero revisits.

The deleted bullet read: *"Where the period budget exceeds what the sections need one-for-one,
the surplus is spent by DEEPENING sections inside their own runs — more practice, a harder case,
a second representation, a contextual application — never by adding a unit that returns to a
section the plan has already left (Rule 1)."*

It did two harmful things, both authored here at v3.6 and both now removed:

- **It created the frame.** "The budget exceeds what the sections need" tells the model it holds
  *spare units to place*, which makes placement a decision separate from teaching. A unit
  conceived as an add-on has no run to belong to, and its natural home is the end. p10's U10 is
  that frame made concrete — a composite anchoring 7.4/7.5, belonging to no single run, sitting
  after both closed (ARV-D-089).
- **Its prohibition arrived last, as a subordinate clause** after four attractive examples, and
  delegated to another rule by cross-reference. The same reading failure diagnosed hours earlier
  on the top's U11: the model takes the permission and drops the tail.

**Nothing is lost by deleting it.** The permission it appeared to grant is already in the bullet
above (*"A section MAY span as many ADJACENT periods as its content warrants"*), and the
prohibition it appeared to add is already Rule 1's contiguity sentence, which is the real one.
The bullet's only distinct contribution was the frame. Rule 2 now says what maths·secondary's
Rule 7 says, in middle's own words, with nothing about spare capacity.

**One honest confound, recorded rather than buried:** maths IX also had slack under the old cap
(14 body units against 8 sections). That no longer separates the stages — under v3.6 middle has
no cap either, and ch 7's top had room to place contiguously and revisited anyway. The remaining
structural difference between the two stages is this clause.

**§9: RELAXATION-ONLY.** A redundant permission and a redundant prohibition are removed; nothing
is tightened and no obligation is created (`MUST NOT` count unchanged — the deleted clause said
"never"). No re-author. Whether ch 7 is re-authored to test the fix is a separate decision on its
own merits.

Artefacts: `genon/out/stage_prep_mathematics_middle/lesson_plan_constitution_v3.7_pre.txt` ·
`lp_v3.7_to_v3.8.diff`.

---

## v3.7 — 2026-08-10 · Rule 1 aligned with Rule 2 — the other direction of the same cap (S7 · C3)

C3's rule-by-rule audit failed the top canonical's closing unit against Rule 1: it names five
sections, and Rule 1 said *"Each period anchors to one or at most two adjacent sections"* (the
schema likewise capped `textbook_segments` at `// 1–2 entries`).

**The two rules cap the same many-to-many relation in opposite directions, and v3.6 only widened
one of them.** Rule 2 governs one SECTION across many PERIODS — amended at v3.6 to "as many
ADJACENT periods as its content warrants". Rule 1 governs one PERIOD across many SECTIONS, and
still carried a fixed number. So a unit that legitimately draws several sections together was
capped at two while a section that legitimately runs long was not capped at all.

Rule 1 now reads *"A period anchors to as many ADJACENT sections as its content warrants."* —
Rule 2's wording, from the other side. Adjacency is kept and is load-bearing: it stops a period
naming 7.1 and 7.4 while skipping what lies between, which is what the serve engine's registry
and first-visit arithmetic read off this field. No count is named, in either rule.

**Deliberately NOT written: the synthesis unit.** An earlier draft carved it out by name. That
would have put a V-series fact into a constitution, which testing.md §3 forbids — the closing
synthesis is mandated by the platform brief, not by any constitution. "As its content warrants"
covers it without naming it: five adjacent sections is what that unit's content warrants.
"usually one" was also dropped at the founder's instruction — Rule 2 already elaborates the
expectation (light sections merge; emphasis follows substance), so repeating it here would be
a second, weaker statement of a rule that already has a good one.

**§9: RELAXATION-ONLY, so it costs nothing.** Every edit widens; `grep -c "MUST NOT"` is
unchanged, no obligation is added, and the v3.6 contiguity paragraph, v3.5's Rule 5 exception,
A1, the register and the P3 shape are all asserted untouched by the edit script. Output authored
under v3.6 satisfies v3.7 by construction — and the clause amended is the one ch 7's synthesis
unit breached, so the installed library becomes compliant rather than breaching. No re-author.
**Closes ARV-D-094.**

Artefacts: `genon/out/stage_prep_mathematics_middle/lesson_plan_constitution_v3.6_pre.txt` ·
`lp_v3.6_to_v3.7.diff`.

---

## v3.6 — 2026-08-10 · Rules 1 and 2 aligned with SECONDARY — the revisit fix (S7 · C1)

Ch 7's top revisited sections 7.2, 7.3 and 7.5 after moving past them, so three of its
twelve units taught nothing new — and because an item anchors at its section's LAST unit,
the assessment landed on those revisits rather than on the sittings that actually taught the
section. A teacher skips a revisit; she then misses the assessment with it. Founder, on
seeing the unit/section table: *"Revisits are a wasted opportunity."*

**The cause was Rule 2's own cap, and it is arithmetic.** Rule 2 let a heavy section split
across "two adjacent periods". Five sections × 2 = 10 body units; ch 7's top needs 11. The
model could not place its eleventh unit without breaking something, so it broke both rules
available to it — one run of three on 7.3 (Rule 2) and three returns (Rule 1). The
constraint binds exactly when **body units > 2 × sections**, and the corpus tracks it:

| plan | body / sections | test | revisits |
|---|---|---|---|
| maths VII ch 7 top | 11 / 5 | 11 > 10 **binds** | 3 sections |
| maths VII ch 7 p10 | 10 / 5 | 10 = 10 marginal | 1 |
| maths VII ch 7 p07 | 7 / 5 | 7 < 10 slack | 0 |
| maths IX ch 4 top | 14 / 8 | 14 < 16 slack | **0** |
| science IX ch 8 | 11 / 10 | slack | 0 |

**Maths secondary has no such cap** — which is why maths IX never revisits. Its Rule 7
("FULL-SECTION COVERAGE") says a section "may span more than one period where its content
warrants it; emphasis follows the substance of the section", and forbids any numerical
allocation formula across sections; its Rule 2 is not a packing rule at all. Middle's
"PERIOD BIN-PACKING" was the outlier in the maths family, and the only one of the three
that named a number.

So this is a **port, not an invention**: secondary's Rule 7 discipline moved down one stage,
where S4 has already exercised it.

- **Rule 1** gains one sentence making "interleave" concrete — a section's periods are
  CONTIGUOUS, and a later period MUST NOT re-anchor a section an earlier run completed.
  Consolidation belongs inside the section's own run.
- **Rule 2** is renamed FULL-SECTION COVERAGE. The two-period cap is gone: a section may
  span as many ADJACENT periods as its content warrants, emphasis following substance and
  never the effort_index. Surplus budget is spent by DEEPENING a section inside its run.
  Secondary's two prohibitions are ported verbatim in substance (no numerical allocation
  formula across sections; no front-loading). The two-goal split generalises from "period N
  and period N+1" to the earlier and later periods of the run, and a multi-period single-goal
  run carries one goal throughout. Full coverage and the ban on dropping a section are
  untouched.

**§9: a CONSTITUTION CHANGE IN THE FULL SENSE — the relaxation-only carve-out does NOT
apply.** Removing the cap and generalising the goal-split wording are relaxations, but Rule
1's contiguity sentence and Rule 2's two ported prohibitions are tightenings, and one
tightening anywhere forfeits the carve-out. **S7 re-opens: ch 7's three canonicals re-author
under LP v3.6 (~₹106) and C1–C3 re-run.** The installed library breaches the amended text in
both directions, so it could not have been carried forward on a compliance check either.

Artefacts: `genon/out/stage_prep_mathematics_middle/lesson_plan_constitution_v3.5_pre.txt` ·
`lp_v3.5_to_v3.6.diff` · `apply_s7_rules_1_2_alignment.py` (guards assert the cap is gone in
every form, the port arrived intact, and that A1, the register, the P3 shape and v3.5's Rule 5
exception are untouched).

**Owed with this, and free:** a certifier check that no section appears in two non-contiguous
runs. Rule 1 has forbidden interleaving all along and nothing ever tested it — which is why
three revisits reached a paid artefact and were found by eye.

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
