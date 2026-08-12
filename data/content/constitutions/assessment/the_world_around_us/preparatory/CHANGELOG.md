# CHANGELOG — Assessment Constitution · The World Around Us · Preparatory Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).

---

## v1.4 — 2026-08-11 · A6-confirm + A9 (S5 · P2)

Landed at S5's P-prep, before any canonical for this stage was authored. Paired with LP
v1.3. Nothing pedagogical changed; Rules 1–11 keep their force and their wording apart from
the additions below.

- **A6 — the anchor, CONFIRMED and written down as an integrity block** rather than amended
  into the item schema. TWAU preparatory is the **ITEM-SELF-SUFFICIENT** family (verified
  8-rule table **row 8**, the same family as social_sciences): the item carries `period_ref[]`
  DIRECTLY and carries its own `implied_lo` inline beside it. There is no mediating handoff
  row and no period-field join — the Coverage Handoff supplies the material the item is
  built from, but the platform never joins through it to find the unit.

  The field was already in the schema and already correct, so **nothing was added to the
  item**; what lands is an ANCHORING block under Rule 2 stating three things a later pass
  must not get wrong: that `period_ref` IS the anchor and is emitted directly; that where an
  item legitimately reaches several units it anchors at the **LAST** of them (founder,
  2026-08-05 — an item tests its material's whole `implied_lo`, so it becomes available only
  once that material completes, and a class taught part of it cannot be tasked on any of
  it); and that anchoring is **UNIT-level**, so no band-level reference may be emitted. The
  v1.2-era band-level `phase_ref` is reversed and stays reversed (`grep -c phase_ref` = 0).

  **Why this is a confirmation and not an amendment**, stated because the two neighbouring
  stages went the other way: maths·preparatory (v1.3) had to write down that
  `period_ref`/`period_number` MUST NOT be emitted, because declaring the link on a
  period-field stage would freeze an arrangement the platform varies per teacher. On row 8
  the declaration IS the mechanism — it is the reference's own shape — so the same field is
  mandatory here and prohibited there. That is a property of the family, not an
  inconsistency, and the block says so.

- **A9 — MCQ option order is not the model's to set.** Two lines added to Rule 6 (MCQ
  DISTRACTOR DESIGN), in the reference's v1.7 wording: order carries no meaning and is not
  the generator's to set (emit options as authored; uneven letters across a chapter are
  coincidence, not a defect), and a prohibition on an option that refers to another option
  **by its label** ("both A and B", "none of the above", "all of the above") — the one
  construction the downstream sort cannot reorder without rewriting.

  **The REMOVAL half of A9 was N/A here.** This file never carried the MEMORY item-18
  position prohibition; testing.md P2 names four files that do (SS + Science, middle and
  secondary) and this is not one. Confirmed by grep — `consecutive`, `same label`,
  `vary in position` all 0 — so nothing was struck and A9 landed as the two lines alone, the
  same shape it took at S4, S7 and S8. The file also carried no prior "none of the above"
  ban, so the label-reference prohibition is purely additive rather than an absorption.

  The struck arrangement sentence ("alphabetically", "never led with", "first word at which
  they differ") is asserted absent by the edit script's guards and must never be re-added:
  ordering is a pipeline stage (`genon/normalize_options.py`, STEP 6 of `build_library.py`),
  and naming arrangement at all keeps position salient to a model that should never reason
  about it.

- **No cancelled amendment and no V-rule entered the file.** `phase_ref`, `band_ref`,
  `band_id`, `role_handoff`, `unit_handoff`, "section registry", "synthesis unit" and
  "reserved token" are all asserted absent by the edit script's guards.

**No new field.** The anchoring block describes a link the file already carries and asks the
generator for nothing it was not already emitting.

Artefacts: `genon/out/stage_prep_twau_preparatory/` —
`assess_twau_preparatory_v1.3_pre.txt` · `assess_v1.3_to_v1.4.diff` ·
`apply_s5_p2_assess.py`.

**Standing debt, flagged for the C-cycle rather than the constitution.** Rule 10 sets
`visual_stimulus` to `""` by default and introduces no new rendering branch, permitting the
existing pipe-table convention only "rarely and not expected". Confirm at C13 that a TWAU
item which does take a pipe table still renders on both surfaces (screen and PDF) — a
permitted format that no stage has exercised is the same failure mode as a permitted format
with no branch. This is the TWAU analogue of the `number_line:` debt S7 and S8 recorded.

---

## v1.3 — 2026-07-10 · `guide.{TYPE}` nesting made mandatory

Rule 9 and the JSON-schema blocks amended to MANDATE `guide.{question_type}` nesting
(matching Science and the registry), with a new prohibition against flat
`guide.what_each_option_reveals` placement; the population-table header became
"guide.{TYPE} keys required". Landed with the same-day SS·secondary bump to v1.7.

**Validated synthetically only.** All TWAU saved plans were migrated in place — a pure
structural relocation, deep-diff-clean — but the constitution TEXT has never been exercised
by a live generation run. Both SS stages have since had one (SS·secondary at S3's C4
2026-08-03, SS·middle at C4 2026-08-04, 113 items between them, zero flat placements);
**TWAU is the last of the three still owed**, and S5's own C4 is where that debt is paid.
See MEMORY.md §"AMENDMENTS TO BE TESTED" item 1.

---

## v1.2 and earlier

No sidecar was kept before this file existed, and the constitution carried no in-document
version-history block to lift out. Earlier history is in git.
