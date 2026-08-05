# CHANGELOG — Chapter Assessment Constitution · Science · Secondary Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).
Nothing in this file is read at generation time.

---

## v1.2 — 2026-08-05 · S3 stage preparation (P2)

**No pedagogical rule changed.** The diff touches the VERSION line, Rule 7's option-order
clause, one integrity line, and the footer. Counts and format matching (Rule 5), the
reasoning floor (Rule 6), the open-task menu (Rule 8), the guide layer (Rule 9) and the
whole A1 schema are byte-identical.

- **A9 — MCQ option order is not the model's to set.** One removal and two additions, and
  never an arrangement rule. Ordering is a pipeline stage: `genon/normalize_options.py`,
  STEP 6 of `build_library.py`, subject-agnostic, gated at certification (C3 gate 9a).
  - **REMOVED** the MEMORY-item-18 position prohibition — "Answer position carries no
    signal: is_correct MUST be distributed across A–D within an assessment and MUST NOT
    repeat on the same label across consecutive items or cluster on one letter." It is
    known not to hold, and it asks for randomness the model cannot produce. Nothing
    replaces it in kind.
  - **ADDED**, in the v1.7 wording: option order carries no meaning and is not the model's
    to set (emit as authored; uneven letters across a chapter are coincidence, not a
    defect); and the prohibition on an option referring to another option by its label
    ("both A and B", "none of the above") — the one construction a downstream sort cannot
    reorder without rewriting.
  - **NOT re-added**, and must never be: the alphabetical arrangement sentence, "never led
    with", or any rule naming a label position. Naming arrangement at all keeps position
    salient to a model that should never reason about it.

- **A6 — confirmed present via the subject's equivalent, one clarifying line added.**
  Every item already carries `section_number`, and the LP's `coverage_handoff` maps it to
  `period_numbers`. Science secondary's unique link is the SECTION, not the unit — a
  section may be taught across several units — so the reference's `period_ref` field is
  not ported. An integrity line now records that the platform resolves the anchor from
  `section_number`, and forbids the model emitting `period_ref` or any unit number.
  Founder ruling, 2026-08-05: derive the link, never demand it. The reversed v1.2-era
  band-level `phase_ref` is absent and was not reintroduced (`grep -c phase_ref` = 0).

Artefacts: `genon/out/stage_prep_science_secondary/` — `assessment_constitution_v1.1_pre.txt`,
`assess_v1.1_to_v1.2.diff`, `apply_s3_amendments.py`.

---

## v1.1 — pre-2026-08-05

Carried the MCQ answer-distribution rule (the item-18 position prohibition) that v1.2
removes. Earlier history was never kept in a sidecar and is not reconstructed here; git is
the record. The file carried no in-document version-history block, so nothing was lifted
out of it by P4.
