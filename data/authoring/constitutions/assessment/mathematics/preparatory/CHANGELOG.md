# CHANGELOG — Assessment Constitution · Mathematics · Preparatory Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).

---

## v1.4 — 2026-08-11 · `number_line:` becomes a TICK LINE — labels may be words

Founder-directed at S8's C4, on the first live use of the tag. maths III ch 5 Q-C-4 tagged an
alternating SHAPE pattern — `number_line: line | curve | line | curve | … ` — for
*"draw the next two repeat units"*. That is the right picture for the question, and the rule as
written forbade it (*"each cell a number … endpoints must be numbers"*), so the stimulus failed
its own declared type, fell through to TABLE, and printed the literal token `number_line: line`
to the teacher on screen and in the PDF (ARV-D-113).

**Founder ruling: the tick line IS the better representation, so the rule follows the practice.**
Without this the next generation doing the wanted thing is technically in breach and C3 re-raises
it at every chapter.

**What the rule now says.** A tick line is an ordered line of at least three cells; each cell is
a LABEL — a number, or a short word naming what sits at that tick — or `...` for a blank tick the
student fills. A label is a label, not a sentence. Ticks are drawn as a line, never a grid. Both
the numeric and the word form are shown as examples.

**Three things moved with it, and the third is what makes this a guarantee rather than a
convention:**

- `assessment_norm._nl_block` now validates STRUCTURE (single row, ≥3 cells, labels ≤16 chars)
  instead of cell TYPE. The numeric test predated the tag, from when typing had to be *guessed*
  from a bare pipe row; once intent is declared, re-deriving it from the cells is redundant — and
  was wrong. Both renderers were already label-agnostic, so word labels needed no display work.
- A tagged stimulus that fails the contract no longer degrades silently: the tag is **stripped**
  from the fallback content and a single row falls to PROSE rather than TABLE. An internal token
  can no longer reach a teacher under any fallback.
- `build_library.py` gained a **DECLARED-TYPE GATE** — a stimulus that declares a type it does not
  satisfy now fails certification by name. Q-C-4 was found by hand at C4; C3 had read the item and
  passed it, because "tag present, no SVG" is what a human checks. Verified to fire on a
  deliberately broken artefact and to pass on the real one.

**§9: RELAXATION-ONLY.** Every edit widens — a form is permitted that was not; nothing is
tightened and no obligation is created (`MUST NOT` / `PROHIBITED` counts asserted unchanged). A
numeric tick line is still a tick line, so output authored under the old text satisfies the new by
construction. **No library re-authors.** ch 5's Q-C-4 is the only tagged stimulus in this stage's library and it now resolves as intended — no back-fill was needed, the engine fix alone corrected it.

Artefacts: `genon/out/stage_prep_mathematics_preparatory/` — `assess_preparatory_v1.3_pre_tickline.txt`
· `tickline_preparatory.diff` · `apply_tick_line_rule7.py`.

---

## v1.3 — 2026-08-11 · A6-confirm + A9, and one repair (S8 · P2)

Landed at S8's P-prep, before any canonical for this stage was authored. Paired with LP
v1.2. Nothing pedagogical changed; Rules 1–9 keep their force and their wording apart from
the additions below.

- **A9 — MCQ option order is not the model's to set.** Two lines added to Rule 9's MCQ
  block, in the reference's v1.7 wording: order carries no meaning and is not the
  generator's to set (emit options as authored; uneven letters across a chapter are
  coincidence, not a defect), and a prohibition on an option that refers to another option
  **by its label** ("both A and B", "none of the above", "all of the above") — the one
  construction the downstream sort cannot reorder without rewriting.
  **The REMOVAL half of A9 was N/A here.** This file never carried the MEMORY item-18
  position prohibition; testing.md P2 names four files that do (SS + Science, middle and
  secondary) and this is not one. Confirmed by grep — `consecutive`, `same label`,
  `vary in position` all 0 — so nothing was struck, and A9 landed as the two lines alone,
  the same shape it took at S4 and S7. The struck arrangement sentence ("alphabetically",
  "never led with", "first word at which they differ") is asserted absent by the edit
  script's guards and must never be re-added: ordering is a pipeline stage
  (`genon/normalize_options.py`, STEP 6 of `build_library.py`), and naming arrangement at
  all keeps position salient to a model that should never reason about it.

- **A6 — the anchor, CONFIRMED and written down as an integrity block** rather than amended
  into the item schema. Preparatory mathematics is the PERIOD-FIELD family (verified 8-rule
  table **row 5**): the item's `section_ref` ("S3") is copied verbatim from the LP handoff
  entry it was generated from, and the platform resolves it to the teaching unit(s) by
  matching it against each period's own `section_refs[]` — a **different field from
  middle's** `textbook_segments[].ref`, which is why the two stages are separate rows of the
  table and why neither may borrow the other's join. The new block states four things the
  generator must not get wrong: that `section_ref` IS the anchor and is pass-through; that
  where a section spans several units the item anchors at the LAST of them (founder,
  2026-08-05 — an item tests what its section teaches, so it becomes available only once the
  section completes); that `period_ref` / `period_number` / any unit number MUST NOT be
  emitted on an item, because declaring the link would freeze an arrangement the platform
  varies per teacher; and that `task_id` is not an anchor in this sense — it seeds the
  exercise companion only (Rule 8). The v1.2-era band-level `phase_ref` is not reintroduced
  (`grep -c phase_ref` = 0).

- **REPAIR, not an amendment: the `what_each_option_reveals` example.** The schema block read
  `{ "A": string, "C": string, "C": string, "D": string }` — four keys, "C" twice, "B"
  missing. S7's distractors-only pass (2026-08-10, this file's v1.1 → v1.2) rewrote the
  first line of the two-line example and left the second, and the result contradicted its own
  prose, which has mandated one entry per NON-CORRECT option since that bump. The example now
  shows three keys and says so.

**No new field.** The anchoring block describes a link that is DERIVED from data the file
already carries. Nothing was added to the item schema, and the constitution asks the
generator for nothing it was not already emitting — see the LP sidecar's note on the founder
ruling of 2026-08-10 and the prototype precedent behind it.

Artefacts: `genon/out/stage_prep_mathematics_preparatory/` —
`assessment_constitution_v1.2_pre.txt` · `assess_v1.2_to_v1.3.diff` ·
`apply_s8_amendments.py`.

**Standing debt, flagged for the C-cycle rather than the constitution.** Rule 7's permitted
`visual_stimulus` formats at this stage are the pipe-table and the `number_line:` form, with
inline SVG explicitly prohibited. Confirm at C13 that both renderers (screen and PDF) still
carry a `number_line:` branch; a permitted format with no detection branch is the failure
mode the prototype's §7 note warns about. This is the same debt S7 recorded for middle, and
it is now owed twice.

---

## v1.2 — 2026-08-10 · distractor keys only (S7 collateral)

`what_each_option_reveals` narrowed to ONE ENTRY PER NON-CORRECT option, keyed to that
option's label, with the correct option omitted — it is already marked by `is_correct`.
Applied to this file by S7's `apply_s7_distractors_only.py` while amending middle. The prose
landed correctly; the schema example did not, and is repaired at v1.3 above.
Artefacts: `genon/out/stage_prep_mathematics_middle/prep_assessment_constitution_v1.1_pre.txt`
· `prep_assess_v1.1_to_v1.2.diff`.

---

## v1.1 and earlier

No sidecar was kept before this file existed, and the constitution carried no in-document
version-history block to lift out. Earlier history is in git.
