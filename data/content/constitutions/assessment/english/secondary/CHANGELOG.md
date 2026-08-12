# CHANGELOG — Assessment Constitution · English · Secondary Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).

---

## v1.4 — 2026-08-12 · S11 stage prep — A6 as a rule of its own, A9 as two lines

The campaign carry-forward for this stage (testing.md §3, P2). The constitution carried no
in-document version-history block, so nothing had to be lifted out; this sidecar is new.

- **A6 — ITEM ANCHORING, added as Rule 8A.** A *confirmation* in substance and an amendment
  in form: the two fields that carry the anchor (`source_section_id` + `source_spine`) were
  already mandated by Rule 8, but nothing said they WERE the anchor, nothing said what the
  platform does with them, and nothing forbade the model emitting a unit number beside them.
  English is **8-rule row 7**, the period-field family: the pair resolves against each
  period's own `section_id` + `spines_taught[]` — no `coverage_handoff` in the path. The new
  rule records four things: the cell is the anchor and there is no third field to emit; a
  cell taught across several units anchors at the LAST of them (founder 2026-08-05); and
  `period_ref` / `period_number` / `unit_ref` MUST NOT be emitted, because declaring the link
  would freeze an arrangement the platform varies per teacher. Same shape as science·secondary
  v1.2, science·middle v1.4, maths·middle v3.3 and maths·preparatory v1.3 — derive the link,
  never demand it. `grep -c phase_ref` = 0.
- **A9 — MCQ option order.** The **removal is N/A**: this file never carried the MEMORY-item-18
  position prohibition (testing.md names the four files that do — SS and Science, middle and
  secondary — and this is not one of them; `consecutive`, `same label`, `vary in position` all
  grep 0). It landed as the two v1.7 lines alone, in Rule 4 where the MCQ semantics live: order
  carries no meaning and is not the model's to set (`genon/normalize_options.py`, STEP 6 of
  `build_library.py`, arranges deterministically after generation), and no option may refer to
  another **by its label** — "both A and B", "none of the above", "all of the above",
  "either B or C". This file carried no prior "none of the above" ban, so the prohibition is
  purely additive. **No arrangement sentence was added**: `alphabetically`, `never led with`
  and `first word at which they differ` are asserted 0 by the edit script's guards.
- **Item-count invariance**, following the LP's new FULL SPINE COVERAGE mandate: the item
  count does not vary with the period count. A shorter plan yields the same cells and the same
  items, tested on less anchored practice — never a shorter assessment. Stated here because
  Rule 2's count formula is the place a reader would otherwise infer the opposite.

Artefacts: `genon/out/stage_prep_english_secondary/` — `assessment_constitution_v1.3_pre.txt` ·
`assess_v1.3_to_v1.4.diff` · `apply_s11_amendments.py`.

---

## v1.3 and v1.2 — dates unrecorded

**Both bumps are undocumented.** No sidecar existed, the constitution carries no in-document
history, MEMORY.md's constitution inventory records this file only up to v1.1, and `data/` is
git-ignored, so there is no trail to reconstruct from. Recorded as a gap rather than guessed
at — the third stage running where a version moved without a record (S8 found the same on both
mathematics·preparatory files). Nothing in the v1.4 pass depends on knowing what they were.

---

## v1.1 — 2026-07-13 · Rule 4 gains "NAME THE REFERENCED WORD"

Applied to middle (v3.1 → v3.2) and secondary (v1.0 → v1.1) together; preparatory deliberately
excluded. When an item requires a cognitive act on a specific word within a larger sentence,
the stem MUST state that word explicitly in parentheses — never indicate it by underlining,
bold or italics, which have no representation in the item JSON and are silently lost, leaving
the question unanswerable. Prompted by `english/vii/ch_01_20260510_175736.json` item `Q-VG-A-1`,
which says "the underlined word", carries no underline and an empty `visual_stimulus`, and is
stamped `verified: true`. (MEMORY.md, "★ AMENDMENTS TO BE TESTED" item 10 — still owed a live
generation check.)

---

## v1.0 — 2026-07-13 · forked from English Assessment Constitution v3.1 (Middle)

Every secondary-only addition tagged `[SECONDARY DELTA]`: the **EXTRACT_ANALYSIS** question
type (a verbatim extract in `visual_stimulus` plus 1–3 analytical sub-questions, mirroring the
textbook's "Critical Reflection"); EXTRACT_ANALYSIS / ECR preferred for analytical LOs, with
MCQ and TRUE_FALSE reserved for factual outcomes; drama anchors (character arc, dialogue
subtext, stage directions, thematic conflict); and the **listening transcript baked into the
summary**, so the generator never opens the appendix booklet.
