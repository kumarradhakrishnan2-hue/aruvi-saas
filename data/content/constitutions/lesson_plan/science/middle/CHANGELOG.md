# CHANGELOG — Lesson Plan Constitution · Science · Middle Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).
Nothing in this file is read at generation time.

---

## v2.2 — 2026-08-07 · S6 stage preparation (P1 + P3)

The genon constitutional carry-forward from the SS·secondary v1.10 reference — **partial
by founder ruling**, because this stage is the campaign's one structural exception. **No
pedagogical rule changed:** the diff touches the VERSION line, INPUTS 4, the vocabulary
line, a new register block, Rule 6, one Rule 10 constraint, and two A3 lines. Rules 1–5,
7–9, Amendment A4 and every other period field are byte-identical.

- **A1 — the period schedule is exactly ONE standard row.** INPUTS 4 was "one or more rows
  of {duration in minutes, period count}"; it is now one row at the class-standard duration
  (40 min for VI–VII, 45 for VIII — the master-plan calibration bands, not NCF's flat 40)
  × the period count. Every canonical is authored at the standard duration and the serve
  engine handles all timetable variation, so a multi-row input has no meaning any more.
  Rule 6's TIME statement is restated as `duration × count` rather than a sum over rows,
  and A3 gains the matching field constraint.
  - Following science·secondary v1.1, the closing clause reads **serve time**, not the
    reference's "partition time" — the deterministic partition engine was retired
    2026-07-31.

- **A5 + A7 — THE SELF-CONTAINED REGISTER, as ONE block, in a TWO-BAN cut.** Added after
  VOCABULARY: (1) no clock quantity, (2) no calendar time. Bound at Rule 6 (band text) and
  Rule 10 (teacher notes) by reference, never restated as scattered bans.
  - **The reference's third ban — forward reference and completion language — is
    DELIBERATELY NOT PORTED.** Founder ruling, 2026-08-07. It is the only such omission in
    the campaign and it is not an oversight: science·middle is the one subject·stage whose
    lesson plan is organised by the cognitive progression arc rather than by textbook
    sections, and an arc is taught whole or not at all. Every unit of a canonical is
    therefore served with every other unit of that canonical, so "in the next unit" is
    never wrong for anyone, and a closing unit's completion claim is simply true. The block
    says so explicitly rather than leaving the omission silent, and VOCABULARY keeps its
    positional cross-reference examples ("the previous unit", "this unit") and Rule 10 its
    position-linked continuity — both of which the other stages had to strike.
  - **Bans 1 and 3 are untouched by that reasoning and stand in full.** Ban 1 exists
    because the platform scales every band's minutes to the sitting that carries it, which
    is universal and unaffected by the serve model — a 45-authored band served into a
    60-minute sitting falsifies any stated number. Ban 3 is Calendar Purge doctrine. The
    argument for dropping ban 2 reaches neither.
  - One residue of ban 2 survives outside this file: the chapter's closing synthesis unit
    can be served into a companion canonical's plan, so its self-containment is mandated by
    the platform-composed variant brief. Per testing.md §3 the V-series is not
    constitutional, so it is not stated here.

- **P3 — Group B schema conversion, applied.** `phases[{minutes, description}]` →
  `time_bands[{minutes, activity}]` in the A3 schema, with Rule 6's prose following. No
  `band_id` in the target shape — the band layer left the declaration surface at compile
  v0.5 and ids are derived internally. `roles[]` is untouched (carried, ignored downstream
  for now).

- **Header.** The file was titled "· SCIENCE · VERSION 2.1" with no stage marker, unlike
  every sibling; it now reads "· SCIENCE · MIDDLE STAGE · VERSION 2.2". Cosmetic, recorded
  because it is in the diff.

Artefacts: `genon/out/stage_prep_science_middle/` — `lesson_plan_constitution_v2.1_pre.txt`,
`lp_v2.1_to_v2.2.diff`, `apply_s6_amendments.py` (the reproducible edit script; every edit
asserts exactly-one occurrence).

---

## v2.1 — pre-2026-08-07

The stage's original constitution. Its history before v2.2 was never kept in a sidecar and
is not reconstructed here; git is the record. The file carried no in-document version-history
block, so nothing was lifted out of it by P4.
