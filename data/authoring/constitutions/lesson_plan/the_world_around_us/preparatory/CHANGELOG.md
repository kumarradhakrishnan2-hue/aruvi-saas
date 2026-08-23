# CHANGELOG — Lesson Plan Constitution · The World Around Us · Preparatory Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).

---

## v1.5 — 2026-08-12 · Rule 5's `section_context` word cap is REMOVED (ARV-D-121)

**Third setting of this number, second time a live run has disproved it.**

| version | cap | what the evidence said |
|---|---|---|
| ≤ v1.2 | 10–15 | 14 of 24 real corpus periods above it |
| v1.4 (yesterday) | 10–25 | widened on exactly that evidence |
| the run that evening | — | **12 of 39 units above 25** (top 20–31 · p13 13–35 · p10 18–32) |

The founder accepted it at C3 rather than repairing, with a note: *"if it is ever revisited,
DROP the upper bound rather than raise it a third time — S4's lesson is about numbers, and this
one has now failed twice."* This is that revisit.

**Why the number was always the wrong instrument.** `section_context` is a LABEL, not prose: it
names the objects, phenomena or tasks a unit drew from, and the assessment reads it to ground
what its question is about. Its length is a property of the **unit's content**, not of good
writing — a unit that handled two objects has a short label, one that handled eight has a long
one, and both are correct. A cap asks the model to choose between naming what it used and
hitting a number, and on a dense unit the only way to satisfy it is to **drop an object**, which
silently degrades the assessment's grounding to protect nothing. v1.4 already said so in its own
sentence (*"do not drop an object to fit a length"*) — the number and the sentence were in
contradiction, and the sentence is the one doing the work.

**What replaces it: the rule in kind.** It is a LIST of what the period handled, not a sentence
about it — name every object actually used, name nothing that was not, add no commentary, and
let length follow content. Checkable by eye at C3, no arithmetic. The do-not-drop instruction is
restated as the file's one new `MUST NOT`.

**§9: RELAXATION-ONLY.** A constraint is removed and none is added — the single new `MUST NOT`
restates an instruction v1.4 already carried as prose, and the edit script asserts the delta is
exactly +1 so a later pass cannot smuggle a second in behind it. Every artefact authored under
10–15 or 10–25 satisfies the new text by construction. **No library re-authors, no stage
re-opens.**

**The transferable rule, for S9–S11 and for the pre-warm:** when a constitution states a number
about the LENGTH OF A FIELD WHOSE LENGTH IS SET BY CONTENT, the number is the defect. Widening it
buys one run. Ask instead what the field is *for* — if the answer is "so something downstream can
read it", the honest constraint is completeness, not size.

Artefacts: `genon/out/stage_prep_twau_preparatory/` —
`lp_twau_preparatory_v1.4_pre_dropcap.txt` · `lp_v1.4_to_v1.5.diff` ·
`apply_s5_rule5_dropcap.py`.

---

## v1.4 — 2026-08-11 · Rule 5's `section_context` cap widened to 10–25 words (S5 · P-prep)

Not part of the constitutional carry-forward set, and raised because S8's standing rule for
the remaining stages says to: *at P-prep, take every number a constitution states and check
it against the whole class's `sections × canonical_plan.counts` **and** against any real
saved plan for that stage.* The corpus check is the one that found this, exactly as it was
at S8.

**Measured, on all three real TWAU saved plans — 24 periods, 14 of them above the cap:**

| plan | periods | `section_context` words | above 15 |
|---|---|---|---|
| ch 1 · III | 7 | 15–26 | 6 |
| ch 7 · IV | 8 | 10–28 | 2 |
| ch 5 · V | 9 | 15–20 | 6 |

The LOWER bound is never breached (min 10, exactly on the boundary once). So this is the
**mirror** of S4's finding rather than a repeat of it: S4 found maths·secondary's lower
bounds too HIGH (live output ran short — `activity_title` 10–13 → 6–13, `section_context`
10–12 → 6–12 at LP v1.3, paid for with a C3 re-author). TWAU's evidence says the UPPER bound
is too LOW. Widening the top alone is what the data supports; adding lower-end headroom this
stage has never needed would be inventing a fix.

**Why the field tolerates it.** `section_context` is a descriptive LABEL — "the specific
objects, phenomena, or tasks this period drew from" — read by the assessment constitution to
ground what the question is about (its INPUTS 1 and TWO-FIELD READING RULE). It is not a
pedagogical constraint, and TWAU periods routinely name several objects at once, which is
exactly why the real output sits at 15–28. A cap that truncates it degrades the assessment's
grounding to protect nothing. A sentence was added with the number, so the intent is not left
to be inferred: name every object the period actually used, and where a period draws on
several the label runs to the upper end and that is correct.

**Both surfaces moved.** The rule AND the JSON schema comment — the schema is what the model
copies from, and it is the third stage in a row where a number left a residue there (S7 at
v3.7, S8 at v1.3, and this file's own A1 pass earlier today).

**§9: RELAXATION-ONLY.** The edit widens; nothing is tightened and no obligation is created
(the `MUST NOT` count is asserted unchanged at 24 by the edit script). Output authored under
the old text satisfies the new by construction. **No library re-authors** — and none exists
for this stage, which is the whole point of catching it at P-prep, free, rather than at C3.

**The three numbers that were checked and LEFT:** Rule 3's *"MUST NOT use the same
dominant_mode for more than two consecutive periods"* (the corpus never exceeds a run of 2,
and with five modes over a 16-unit canonical it is trivially satisfiable); Rule 8's *"at
least three bands"* (corpus minimum is 4, and every one of the 24 periods tiles its duration
exactly, 0 mismatches); and Rule 4's activity-per-period rule, which states in terms that it
is type-based and *"not a numerical count cap"*. Rule 1 states no cap at all — it permits a
section to span multiple consecutive periods without limit, which is the clause maths
preparatory had to be amended INTO at S8.

Artefacts: `genon/out/stage_prep_twau_preparatory/` —
`lp_twau_preparatory_v1.3_pre_wordcap.txt` · `lp_v1.3_to_v1.4.diff` ·
`apply_s5_rule5_wordcap.py`.

---

## v1.3 — 2026-08-11 · A1 + the self-contained register (S5 · P1)

Landed at S5's P-prep, before any canonical for this stage was authored, so the ordering
rule is satisfied and §9 costs nothing. Paired with assessment v1.4. Nothing pedagogical
changed: Rules 1–10, the five `dominant_mode` values, the DESIGN PRINCIPLE and the JSON
schema keep their force and their wording apart from the additions below.

- **A1 — the period schedule is exactly ONE standard row.** INPUTS 4 read *"Period
  schedule — one or more rows of {duration_minutes, count}"*, which licensed the
  mixed-duration plan the variant-canonical serve engine cannot use: every variant is
  authored at the class-standard duration and all timetable variation is handled
  downstream by proportional per-unit scaling. It now reads *exactly ONE row
  {duration_minutes, count}: the class-standard duration (40 min for the Preparatory
  stage — the master-plan calibration band) × the period count*. The Preparatory band is
  **40 minutes**, matching `master_plan.json`'s `the_world_around_us|III/IV/V` rows.

  **Declared deviation from the SS·secondary v1.10 reference:** "serve time", not the
  reference's "partition time" — the deterministic partition engine was retired
  2026-07-31. The same correction S3, S4, S6, S7 and S8 made.

  **Two residues moved with it, and the second is the one that matters.** The INTEGRITY
  CONSTRAINTS `TIME:` line still summed "per schedule row" over "row counts", which
  restates the plural shape A1 had just removed; and the JSON schema's `period_schedule`
  array carried no row-count comment at all. **The schema block is the surface the model
  actually copies from** — S7 hit the identical residue in maths·middle at v3.7 and S8 in
  maths·preparatory at v1.3, and it is now three stages in a row. Grep the SHAPE, not just
  the rule.

  *Naming note:* the campaign's "Amendment A1" (one standard row) is not this file's own
  `AMENDMENT A1 — FULL LP JSON SCHEMA`, which is a different thing that happens to share
  the label. The campaign amendment lands in INPUTS 4, where the reference puts it; this
  file's A1 block is untouched apart from the `period_schedule` comment above.

- **A5 + A7 — THE SELF-CONTAINED REGISTER, as ONE block** beside VOCABULARY, in the v1.10
  **three-ban** re-cut: (1) no clock quantity in prose — the platform scales every band's
  minutes in proportion to the sitting that carries it, so a stated number is falsified
  silently; (2) no forward reference or completion claim — a teacher's plan may end, or
  hand over to a companion variant's unit, after any unit; (3) no calendar time — Aruvi
  keeps no calendar and sittings do not map to days. Backward continuity is welcome and is
  best carried by naming the content built on rather than a unit's position.

  **This stage is NOT S6's two-ban exception.** science·middle drops ban 2 because its
  units belong to a cognitive progression arc that is taught whole or not at all, so
  forward reference is never wrong for anyone. TWAU anchors units to textbook sections in
  reading order (Rule 1) and its units travel between canonicals under the serve engine, so
  ban 2 binds in full, exactly as it does at the other nine stages.

  Bound at the two fields it governs **by reference, never as scattered prohibitions** —
  Rule 5's `time_bands` prose and its `teacher_facilitation_note`. Rule 10's IKS prompt
  lives inside `teacher_facilitation_note` and is covered by the same binding.

  **Declared deviation:** the illustrative strings are TWAU ones ("a quick look round the
  classroom", "an unhurried sorting activity", "now that we have named every landform",
  "The children have already watched water change state, …"). The three bans and the
  closing backward-continuity rule are verbatim in substance.

  **One consequential edit rode with it, and it is the same one S7 and S8 made.**
  VOCABULARY was *teaching* the positional cross-reference ban 2 forbids — its examples
  were literally `"the previous unit"` and `"this unit"` — so the examples are dropped, the
  rule is restated as *cross-reference by the CONTENT built, never by position*, and
  "session" joins the excluded register (the reference excludes it; this file did not).

  **A carve-out is stated explicitly** because this stage's band schema makes it live: ban 1
  governs PROSE, and the band's own `"minutes"` field (`{ "minutes": "0-5", "activity": … }`)
  is schema, not prose. Without the sentence a literal reading of "no clock quantity"
  collides with Rule 8's mandate that bands sum exactly to the period duration.

- **P3 — Group B schema conversion: N/A.** This constitution has emitted `time_bands` with
  an `activity` key since before the campaign (`grep -c 'phases\['` = 0, `'"phases"'` = 0,
  `time_bands` = 7), which is what the §1 matrix records. Nothing to convert.

- **No cancelled amendment and no V-rule entered the file.** `role_handoff`, `unit_handoff`,
  `band_id`, `band_ref`, `phase_ref`, "role weighting", "section registry", "reserved token"
  and `section_anchor` are all asserted absent by the edit script's guards. `section_anchor`
  in particular: founder ruling 2026-08-10 forbids inventing a field to feed the serve
  engine, so this stage's anchor stays `section_ref` and the READ is mediated on the plugin
  (see the S5 sign-off, P5.5).

Artefacts: `genon/out/stage_prep_twau_preparatory/` —
`lp_twau_preparatory_v1.2_pre.txt` · `lp_v1.2_to_v1.3.diff` · `apply_s5_p1_lp.py`.

---

## v1.2 and earlier

No sidecar was kept before this file existed, and the constitution carried no in-document
version-history block to lift out — so nothing had to be moved here, and the P4 exit
criterion ("no version-history block in the constitution") was already met on arrival.
Earlier history is in git.
