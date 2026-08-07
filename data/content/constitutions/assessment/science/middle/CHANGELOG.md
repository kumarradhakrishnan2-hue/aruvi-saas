# CHANGELOG — Chapter Assessment Constitution · Science · Middle Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).
Nothing in this file is read at generation time.

---

## v1.5 — 2026-08-07 · ARV-D-065, raised at S6 · C3

**Rule 4's per-stage item minimums were never stated as a mandate.** The pilot library came
in at 13 / 15 / 14 / 12 items against a mandated floor of 15 (2 first + 3+3+3 middle +
4 final) — three of four canonicals short, and the worst offender was the 12-unit TOP, which
had the most room. Not a room problem: the requirement sat at the very top of the model's
natural range, so compliance depended on a run reaching its own ceiling.

- **Why it was not binding.** `grep -ci "must.*at least|must.*minimum"` over v1.4 returned
  **0**. The minimums existed only as a column header ("Minimum") in a whitespace-aligned
  sub-table nested inside a cell of the outer ASCII table. The two MUST sentences in Rule 4
  governed question FORMAT and stage-label leakage — neither one a count. A model emitting
  two items in a middle stage had broken no mandate; it had under-filled a table column.

- **EDIT 1 — the counts are now MUST prose in the MANDATE**, one bullet per stage position,
  with the arithmetic stated ("an assessment over N stages carries at least 2 + 3(N-2) + 4
  items"). The table stays as the summary, never as the source. The middle-stage bullet also
  closes the observed rationalisation: *"however few periods it spans — item count is set by
  stage POSITION, never by how many periods the stage was given in the lesson plan."*

- **EDIT 2 — the licence phrasing is re-scoped.** v1.4 read "Stage position is a relational
  test — **never a fixed integer**. Assessment length is uncapped." — two lines above a table
  of fixed integers. In context that was about `stage_position` being computed against
  `total_stages` rather than hardcoded; next to that table it read as permission on counts.
  It now says the relational rule "governs POSITION only; the item counts below are fixed
  minimums and are not subject to it", and "uncapped" moved beside the floors so the two are
  read together: more than the minimum is always acceptable, fewer never is.

- **EDIT 3 — an under-count PROHIBITION**, the gap that let this pass silently: no emitting
  fewer than the minimums, no trading a shortfall in one stage against a surplus in another
  (they are per stage, not per assessment), and no question type outside the set its stage
  position allows — one of the three breaches on the top canonical was an ECR in a middle
  stage, which the old prohibition on deriving format from LO type did not reach.

- **Not repaired in the artefacts.** testing.md §7 forbids hand back-filling; the fix is
  regeneration, and that is a founder call on cost. The four existing canonicals remain as
  authored, and are the before-evidence for whether prose fixes it.

Paired change outside this file: `genon/build_library.py` gains `STAGE_ITEM_MINIMUMS` +
`stage_item_report()`, so certification reports the per-stage census as an ADVISORY. The
existing weight-based check could not see this defect — it compares each file to the
library's own MODAL count, and these four disagreed with the constitution, not with each
other. The new block reproduces C3's hand-count exactly.

Artefacts: `genon/out/stage_prep_science_middle/` — `assessment_constitution_v1.4_pre.txt`,
`assess_v1.4_to_v1.5.diff`, `apply_s6_rule4_counts.py`.

---

## v1.4 — 2026-08-07 · S6 stage preparation (P2)

**No pedagogical rule changed.** The diff touches the title and VERSION lines, Rule 7's
MANDATE and PROHIBITION cells, and one new integrity block. Rules 1–6 and 8–10, the
stage-position architecture (Rule 4), the guide layer (Rule 9) and the whole A1 schema —
including the `visual_stimulus` VS-1…VS-4 rules — are byte-identical.

- **A9 — MCQ option order is not the model's to set.** One removal and two additions, and
  never an arrangement rule. Ordering is a pipeline stage: `genon/normalize_options.py`,
  STEP 6 of `build_library.py`, subject-agnostic, gated at certification (C3 gate 9a).
  - **REMOVED** the MEMORY-item-18 position prohibition — "The system MUST NOT place the
    correct answer at the same label across consecutive items; is_correct MUST be
    distributed across A-D so no single letter dominates a chapter." It is known not to
    hold, and it asks for randomness the model cannot produce. Nothing replaces it in kind.
  - **ADDED**, in the v1.7 wording: option order carries no meaning and is not the model's
    to set (emit as authored; uneven letters across a chapter are coincidence, not a
    defect); and the prohibition on an option referring to another option by its label
    ("both A and B", "none of the above") — the one construction a downstream sort cannot
    reorder without rewriting.
  - **NOT re-added**, and must never be: the alphabetical arrangement sentence, "never led
    with", or any rule naming a label position. Naming arrangement at all keeps position
    salient to a model that should never reason about it. The script asserts their absence.

- **A6 — confirmed present via the subject's equivalent; one integrity block added.** Every
  item already carries `progression_stage`, and the LP's `coverage_handoff` maps each stage
  to `period_numbers`. Science middle's unique link is the STAGE, not the unit — a stage
  spans several units by Rule 2 — so the reference's `period_ref` field is not ported. The
  new block records that the platform resolves the anchor from `progression_stage` to the
  LAST unit of that stage (an item tests the stage's whole implied LO, so it becomes
  available only when the stage completes — the 2026-08-05 anchoring ruling), and forbids
  the model emitting `period_ref`, `phase_ref` or any unit number. Founder ruling,
  2026-08-05: derive the link, never demand it. The file had no integrity section at all
  before this; two settled facts already stated in the rules (handoff is committed;
  stage numbers never surface to users) are restated there beside the anchoring line.
  - The reversed v1.2-era band-level `phase_ref` was absent and was not reintroduced —
    the sole occurrence in the file is inside the new prohibition.

- **Not changed, deliberately: the synthesis unit carries its own assessment items.**
  Founder ruling 2026-08-07, taken after an audit found the installed libraries already
  behave this way (SS·VIII ch 3 anchors items to synthesis unit 12; SS·IX ch 3 to unit 16),
  and that C9.2 mandates a borrowed unit bring its own items. Science middle is aligned
  with the rest of the platform rather than excepted, so no rule was written.

- **Header.** The file was titled "Chapter Assessment Constitution — Science" with no stage
  marker, though it is the middle-stage file; it now says "· Middle Stage". Cosmetic,
  recorded because it is in the diff.

Artefacts: `genon/out/stage_prep_science_middle/` — `assessment_constitution_v1.3_pre.txt`,
`assess_v1.3_to_v1.4.diff`, `apply_s6_amendments.py`.

---

## v1.3 — pre-2026-08-07

Carried the MCQ answer-distribution rule (the item-18 position prohibition) that v1.4
removes. Earlier history was never kept in a sidecar and is not reconstructed here; git is
the record. The file carried no in-document version-history block, so nothing was lifted
out of it by P4.
