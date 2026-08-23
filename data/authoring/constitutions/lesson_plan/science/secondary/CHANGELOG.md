# CHANGELOG — Lesson Plan Constitution · Science · Secondary Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).
Nothing in this file is read at generation time.

---

## v1.1 — 2026-08-05 · S3 stage preparation (P1)

The genon constitutional carry-forward from the SS·secondary v1.10 reference. **No
pedagogical rule changed** — the diff touches the VERSION line, the vocabulary register,
the new register block, INPUTS 4, Rule 7's prohibition list, Rule 10's continuity phrasing,
two integrity lines and two A3 schema comments. Rules 1–6, 8, 9, Amendment A4 and every
period field are byte-identical.

- **A1 — the period schedule is exactly ONE standard row.** INPUTS 4 was "one or more rows
  of {duration_minutes, count}"; it is now one row at the class-standard duration (50 min
  for IX) × the period count. Every canonical is authored at the standard duration and the
  serve engine handles all timetable variation, so a multi-row input has no meaning any
  more. The TIME integrity constraint is restated as `duration × count` rather than a sum
  over rows, and the A3 schema comment names the standard duration.
  - Deviation from the verbatim port, declared: the reference's closing clause reads
    "handled downstream at **partition time**". The deterministic partition engine was
    retired 2026-07-31, so this file says **serve time**. Raised at S2 as finding 2 and
    fixed here rather than propagated.

- **A5 + A7 — THE SELF-CONTAINED REGISTER, as ONE block.** Added after VOCABULARY in the
  v1.10 three-ban re-cut: (1) no clock quantity, (2) no forward reference or completion
  claim, (3) no calendar time — plus the closing line that backward continuity is welcome
  when carried by naming the content rather than a unit's position. Bound at Rule 7
  (prohibition 6, the band text) and Rule 10 (prohibition 4, teacher notes) by reference,
  never restated as scattered bans.
  - Deviation from the verbatim port, declared: the reference's illustrative example is
    Social Sciences content ("Having traced the Vedic political vocabulary, …"). A Vedic
    example inside a Science constitution would be a defect in kind, so the example alone
    is substituted with a Science one. The three bans and the closing rule are verbatim.
  - Consequential edits: VOCABULARY dropped its positional cross-reference examples
    ("the previous unit", "this unit") and gained the "session" exclusion; Rule 10's
    continuity link is now position-free, naming the content built on. Both follow the
    reference; the old wording instructed exactly what ban 2 and the position doctrine
    now forbid.

- **A6 — item anchoring, stated as DERIVED.** Science secondary's assessment is anchored
  per SECTION, not per unit: a section may be taught across several units (Rule 4), so
  there is no single unit for the model to name. A new integrity line records that the
  platform resolves an item's anchor unit from its `section_number` through this handoff's
  `period_numbers`, and forbids the model emitting `period_ref`. This is the subject's
  equivalent of the reference's A6, not an addition of the reference's field. Founder
  ruling, 2026-08-05: derive the link, never demand it — the same doctrine as compile
  v0.5's derived band ids.

- **P3 — N/A.** Group A: the schema already emits `time_bands[{minutes, activity}]`; no
  `phases[` or `"description"` anywhere in the file.

Artefacts: `genon/out/stage_prep_science_secondary/` — `lesson_plan_constitution_v1.0_pre.txt`,
`lp_v1.0_to_v1.1.diff`, `apply_s3_amendments.py` (the reproducible edit script; every edit
asserts exactly-one occurrence).

---

## v1.0 — pre-2026-08-05

The stage's original constitution. Its history before v1.1 was never kept in a sidecar and
is not reconstructed here; git is the record. The file carried no in-document version-history
block, so nothing was lifted out of it by P4.
