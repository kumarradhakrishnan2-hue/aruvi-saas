# CHANGELOG — Assessment Constitution · Mathematics · Middle Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).

---

## v3.3 — 2026-08-10 · A6-confirm + A9 (S7 · P2)

Landed at S7's P-prep, before any canonical for this stage was authored. Paired with LP
v3.4. Nothing pedagogical changed; Rules 1–9 keep their force and their wording apart from
the two additions below.

- **A9 — MCQ option order is not the model's to set.** Two lines added to Rule 10's MCQ
  block, in the reference's v1.7 wording: order carries no meaning and is not the
  generator's to set (emit options as authored; uneven letters across a chapter are
  coincidence, not a defect), and a prohibition on an option that refers to another option
  **by its label** ("both A and B", "none of the above", "all of the above") — the one
  construction the downstream sort cannot reorder without rewriting.
  **The REMOVAL half of A9 was N/A here.** This file never carried the MEMORY item-18
  position prohibition; testing.md P2 names four files that do (SS + Science, middle and
  secondary) and this is not one. Confirmed by grep — `consecutive`, `same label`,
  `vary in position` all 0 — so nothing was struck, and A9 landed as the two lines alone,
  the same shape it took at S4. The struck arrangement sentence ("alphabetically", "never
  led with", "first word at which they differ") is asserted absent by the edit script's
  guards and must never be re-added: ordering is a pipeline stage
  (`genon/normalize_options.py`, STEP 6 of `build_library.py`), and naming arrangement at
  all keeps position salient to a model that should never reason about it.

- **A6 — the anchor, CONFIRMED and written down as an integrity block** rather than
  amended into the item schema. Middle mathematics is the PERIOD-FIELD family (verified
  8-rule table row 4): the item's `section_ref` is copied verbatim from the LP handoff entry
  it was generated from, and the platform resolves it to the teaching unit(s) by matching it
  against each period's own `textbook_segments[].ref`. The new block states four things the
  generator must not get wrong — that `section_ref` IS the anchor and is pass-through; that
  where a section spans several units the item anchors at the LAST of them (founder,
  2026-08-05: an item tests the section's whole goal, so it becomes available only once the
  section completes); that `period_ref` / `period_number` / any unit number MUST NOT be
  emitted on an item, because declaring the link would freeze an arrangement the platform
  varies per teacher; and that `anchor_id` is not an anchor in this sense — it seeds the
  exercise companion only (Rule 8). The v1.2-era band-level `phase_ref` is not
  reintroduced (`grep -c phase_ref` = 0).

**No new field.** The block describes a link that is DERIVED from data the file already
carries. Nothing was added to the item schema, and the constitution asks the generator for
nothing it was not already emitting — see the LP sidecar's note on the founder ruling of
2026-08-10 and the prototype precedent behind it.

Artefacts: `genon/out/stage_prep_mathematics_middle/` —
`assessment_constitution_v3.2_pre.txt` · `assess_v3.2_to_v3.3.diff` ·
`apply_s7_amendments.py`.

**Standing debt, flagged for the C-cycle rather than the constitution.** Rule 7's permitted
`visual_stimulus` formats at this stage are the pipe-table and the `number_line:` form, with
SVG explicitly prohibited — unlike secondary, which permits it. Confirm at C13 that both
renderers (screen and PDF) still carry a `number_line:` branch; a permitted format with no
detection branch is the failure mode the prototype's §7 note warns about.
