# CHANGELOG — Chapter Assessment Constitution · Mathematics · Secondary Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).
Nothing in this file is read at generation time.

---

## v1.1 — 2026-08-08 · S4 stage preparation (P2)

**No pedagogical rule changed.** The diff touches the VERSION line, Rule 7's option-order
clause and prohibition, one integrity line, and the footer. Question counts and format
matching (Rule 5), the reasoning floor (Rule 6), the open-task menu (Rule 8), the guide
layer (Rule 9), answer verification (Rule 11) and the whole A1 schema — including the VS-1
to VS-6 visual-stimulus rules and `graph_paper` — are byte-identical.

- **A9 — MCQ option order is not the model's to set.** Two additions and, for this file,
  **nothing to remove**. Ordering is a pipeline stage: `genon/normalize_options.py`, STEP 6
  of `build_library.py`, subject-agnostic, gated at certification (C3 gate 9a).
  - **REMOVAL — N/A.** This constitution never carried the MEMORY-item-18 position
    prohibition. testing.md P2 names four files that carry it (SS + Science, middle and
    secondary); mathematics·secondary is not one of them, confirmed by grep
    (`is_correct MUST` · `consecutive items` · `same label` all 0). Nothing was struck.
  - **ADDED**, in the v1.7 wording: option order carries no meaning and is not the model's
    to set (emit as authored; uneven letters across a chapter are coincidence, not a
    defect); and the prohibition on an option referring to another option by its label —
    the one construction a downstream sort cannot reorder without rewriting.
  - The pre-existing ban on "none of the above" / "all of the above" is **absorbed into
    that prohibition rather than duplicated** — it is the same ban, now carrying its reason,
    and Rule 7's prohibition is renumbered 1/2 to hold both. No scope was lost.
  - **NOT re-added**, and must never be: the alphabetical arrangement sentence, "never led
    with", or any rule naming a label position. Naming arrangement at all keeps position
    salient to a model that should never reason about it. Note that Rule 1's prohibition 3,
    Rule 4's and Rule 5's "never position" clauses, and the "Position carries no signal"
    integrity line all concern a SECTION's position in the chapter — a different subject
    entirely — and were left untouched.

- **A6 — confirmed present via the subject's equivalent, one clarifying line added.**
  Every item already carries `section_number` matching the handoff, and the LP's
  `coverage_handoff` maps it to `period_numbers`. Mathematics secondary's unique link is the
  SECTION, not the unit — LP Rule 7 lets a section be taught across several periods — so the
  reference's `period_ref` field is not ported. An integrity line now records that the
  platform resolves the anchor from `section_number`, and forbids the model emitting
  `period_ref` or any unit number. Founder ruling, 2026-08-05: derive the link, never demand
  it. The reversed band-level `phase_ref` is absent and was not reintroduced
  (`grep -c phase_ref` = 0).

Artefacts: `genon/out/stage_prep_mathematics_secondary/` —
`assessment_constitution_v1.0_pre.txt`, `assess_v1.0_to_v1.1.diff`,
`apply_s4_amendments.py`.

---

## v1.0 — pre-2026-08-08

The stage's original constitution. It never carried the item-18 position prohibition, so
v1.1's A9 is additive only. Earlier history was never kept in a sidecar and is not
reconstructed here; git is the record. The file carried no in-document version-history
block, so nothing was lifted out of it by P4.

Standing implementation debt, unchanged by v1.1 and not a constitutional item: the
RENDERER WIRING NOTE at the foot of the constitution. VS-2 (figure SVG) and VS-6
(green graph-paper backing) are permitted by this stage but not yet honoured by
`assessment_pdf_generator.py` or the online renderer. Carry it into the stage's C-cycle as
a defect if a pilot item needs a grid.
