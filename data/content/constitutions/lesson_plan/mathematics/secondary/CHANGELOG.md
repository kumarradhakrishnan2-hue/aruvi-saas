# CHANGELOG — Lesson Plan Constitution · Mathematics · Secondary Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).
Nothing in this file is read at generation time.

---

## v1.1 — 2026-08-08 · S4 stage preparation (P1)

The genon constitutional carry-forward from the SS·secondary v1.10 reference. **No
pedagogical rule changed** — the diff touches the VERSION line, the vocabulary register,
the new register block, INPUTS 4, Rule 9's prohibition list, Rule 10's continuity phrasing,
Rule 10's prohibition, two integrity lines and two A3 schema comments. Rules 1–8, 11, 12,
Amendment A4 and every period field are byte-identical.

- **A1 — the period schedule is exactly ONE standard row.** INPUTS 4 was "one or more rows
  of {duration_minutes, count}"; it is now one row at the class-standard duration — **50 min
  at this stage** — × the period count. Every canonical is authored at the standard duration and
  the serve engine handles all timetable variation, so a multi-row input has no meaning any
  more. The TIME integrity constraint is restated as `duration × count` rather than a sum
  over rows; the A3 schema comment names the standard duration and a new field constraint
  states the one-row rule where the schema is read.
  - Deviation from the verbatim port, declared: the reference's closing clause reads
    "handled downstream at **partition time**". The deterministic partition engine was
    retired 2026-07-31, so this file says **serve time** — the same correction S3 made.

- **A5 + A7 — THE SELF-CONTAINED REGISTER, as ONE block.** Added after VOCABULARY in the
  v1.10 three-ban re-cut: (1) no clock quantity, (2) no forward reference or completion
  claim, (3) no calendar time — plus the closing line that backward continuity is welcome
  when carried by naming the content rather than a unit's position. Bound at Rule 9
  (prohibition 6, teacher-facing text and band activity) and Rule 10 (teacher notes) by
  reference, never restated as scattered bans.
  - Deviation from the verbatim port, declared: the reference's illustrative strings are
    Social Sciences content (a Vedic continuity link, "having covered all four"). Those are
    substituted with mathematics ones — "a quick individual calculation", "an extended
    derivation", "having covered all three identities", "Having established the expansion
    of a binomial product, …". The three bans and the closing rule are verbatim in
    substance.
  - Consequential edits: VOCABULARY dropped its positional cross-reference examples
    ("the previous unit", "this unit") and gained the "session" exclusion; Rule 10's
    continuity bullet is now position-free, naming the content built on; and A3's
    `teacher_notes` schema comment, which echoed the OLD framing verbatim
    ("recap-and-connect"), now reads "continuity by content not position" — pointing at the
    rule rather than restating a framing that no longer exists, as science·secondary's A3
    comment does. All three follow the reference; the old wording instructed exactly what the
    position doctrine now discourages.

- **A6 — item anchoring, stated as DERIVED.** Mathematics secondary's assessment is
  anchored per SECTION, not per unit: Rule 7 lets a section span several periods, and the
  handoff (A4) carries `section_number` alongside `period_numbers`, so there is no single
  unit for the model to name. A new integrity line records that the platform resolves an
  item's anchor unit from its `section_number` through the handoff's `period_numbers`, and
  forbids the model emitting `period_ref`. This is the subject's equivalent of the
  reference's A6, not an adoption of the reference's field — the same shape science·secondary
  landed at v1.1 (founder ruling 2026-08-05: derive the link, never demand it).

- **P3 — N/A.** Group A: the schema already emits `time_bands[{minutes, activity}]`; no
  `phases[`, `"phases"` or `band_id` anywhere in the file.

- **Two residues disclosed, deliberately NOT fixed.** Both are inert, and both are shared with
  science·secondary v1.1 and science·middle v2.2 — patching mathematics alone would put four
  signed stages out of step for no gain. (a) A4's `period_duration_minutes` comment still reads
  "if mixed across this section's periods, the most common"; under one standard row nothing can
  be mixed. (b) INPUTS 4 names the bands "40 ≤VII · 45 VIII · 50 IX" verbatim from the
  reference, in a constitution whose grades are `ix · x`, where testing.md P1 writes the band as
  "50 IX–X". Practically inert — step 0.6 records that class X has no content in any subject —
  but if the wording is to change it should change in the REFERENCE and be ported, not be
  patched per stage.

Artefacts: `genon/out/stage_prep_mathematics_secondary/` —
`lesson_plan_constitution_v1.0_pre.txt`, `lp_v1.0_to_v1.1.diff`,
`apply_s4_amendments.py` (the reproducible edit script; every edit asserts exactly-one
occurrence, and the run ends on guard assertions for the struck arrangement strings).

---

## v1.0 — pre-2026-08-08

The stage's original constitution. Its history before v1.1 was never kept in a sidecar and
is not reconstructed here; git is the record. The file carried no in-document version-history
block, so nothing was lifted out of it by P4.
