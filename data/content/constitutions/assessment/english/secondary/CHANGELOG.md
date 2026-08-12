# CHANGELOG — Assessment Constitution · English · Secondary Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).

---

## v1.5 — 2026-08-12 · the poem-text conduit is closed (ARV-D-138, at C14)

**What was open.** Rule 9 permitted the EXTRACT_ANALYSIS stimulus to be "a short
passage/stanza copied verbatim from `prose_/drama_summary` / **`poem_text`**", and Rule 3
licensed an item to draw on "a specific line, image, or phrase from `poem_text`". For prose
that is harmless and was measured so at C14: the extract is verbatim from **Aruvi's own
`prose_summary`** — 12-word overlap with the summary, **zero** six-word runs shared with the
NCERT PDF — so what reaches the cloud is Aruvi's prose.

`poem_text` is not a paraphrase. It is the poem. Measured on ch 2 *Bharat Our Land*: the
summary carries 16 poem lines and **13 appear verbatim in the NCERT chapter PDF**. A poem
chapter's item would therefore have placed 3–8 lines of an NCERT-published poem into a
**canonical**, and canonicals are precisely what the copyright review's v1.1 ruling sends to
the cloud (summaries and PDFs never leave the machine). That is finding **F2** of
`docs/NCERT_copyright_review.md` — the campaign's sole open copyright finding — landing on the
stage that owns it. **8 of english IX's 16 chapters are poems.**

**What changed — five sites, because the permission was written in five places.**

1. **Rule 4** (the type definition) — EXTRACT_ANALYSIS is no longer "a short *verbatim*
   extract"; and the poem branch closes the "or inline" escape, which would have put the lines
   in `item_stem` instead.
2. **Rule 3** (REQUIRED) — "a specific line, image, or phrase from `poem_text`" becomes "a
   specific image, phrase or turn in the poem — IDENTIFIED BY ITS LOCATION, NOT REPRODUCED".
3. **Rule 9** (opening sentence) — the stimulus is an extract block (prose · drama) **or a
   locator (poem)**.
4. **Rule 9** (permitted formats) — the single bullet splits in two. The extract block is
   restricted to `prose_summary` / `drama_summary`, with the reason stated in the rule. The new
   **poem locator** is the only permitted form for a poem section:
   `Read lines N–M on p.PP, beginning "<incipit>".`
5. **The schema comment** for `visual_stimulus`, which repeated the old format list.

**Why the incipit is part of the design rather than a hedge.** NCERT prints **no line numbers**
on its poems, and ch 2's stanzas break across a page boundary mid-poem — "lines 5–8" alone
would have a student counting. A few words of the first line find it at once. Legally it is the
smallest possible quotation: it identifies, it does not substitute, and it is the convention of
every citation index and every exam paper. The only real risk is drift, so the cap is hard and
in the rule — **at most eight words, one line, no ellipsis, no second fragment** — rather than
left to judgement.

**What did NOT change.** The item type, the item count, the sub-question structure, the
cognitive demand, and the whole prose/drama path. **Reading is untouched**: INPUTS §2, Rule 2(a)
and Rule 6 still name `poem_text` as a content source, because reading the poem is what makes a
good question possible and the summary never leaves the machine. Only *reproduction into the
artefact* is closed. The edit script asserts `poem_text` survives in exactly those three read
sites and nowhere else.

**§9 — a tightening, stage-scoped, and it re-authors nothing.** A constitution change normally
re-opens the stage. This one restricts a path the installed library does not use: ch 7 is a
**prose** chapter, its single stimulus is a prose extract drawn from `prose_summary`, and no
poem locator applies to it — so the library satisfies v1.5 exactly as it satisfied v1.4,
checked clause by clause rather than assumed. **No poem-chapter library exists anywhere**, which
is why this was free today and would not have been after the first poem chapter was generated.

Artefacts: `genon/out/stage_prep_english_secondary/` — `assessment_constitution_v1.4_pre_poem_locator.txt`
· `assess_v1.4_to_v1.5.diff` · `apply_s11_poem_locator.py` (exactly-one-occurrence asserts on
all five edits, plus guards that the three read sites are intact and the prose path is
unmoved). Review: `docs/testing_artefacts/c14_english_ix_ch07.md`.

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

## v1.3 — 2026-07-13 · the "no Part A/B" ban narrowed to the visual case

*Recovered at C4 (2026-08-12) from MEMORY.md's amendment checklist item 13, which names this
file's bump explicitly. It had been recorded here as undocumented; it is not.*

Founder-directed. The blanket "one skill, one task, no Part A/B" was traced to its origin: it
was never a pedagogical principle but the *mechanism* invoked to guarantee the real rendering
rule (a FILL_IN owns at most ONE `visual_stimulus`; the schema slot is single). It over-caught
purely TEXTUAL multi-part items, which render cleanly. Rule 4's FILL_IN line and Rule 9's
combination clause were rewritten to split the two: the hard rule (≤1 visual, no inlining) is
kept; the A/B ban is narrowed to *"a FILL_IN MAY carry multiple parts (A/B) ONLY if every part
is textual/prose; any part needing its own table or visual must be a separate item."* Applied to
all three stages together (prep 1.1→1.2, middle 3.3→3.4, secondary 1.2→1.3).

**Vindicated live at S11's C4:** the 14-period canonical's `Q-VGR-A-1` emits Part A (reported
speech) + Part B (prepositions), both prose, `visual_stimulus: ""` — exactly the case the
narrowing permits, and an item the old blanket ban would have failed.

---

## v1.2 — 2026-07-13 · FILL_IN table anti-duplication

*Also recovered at C4 from checklist item 12.*

Rule 9 gained an explicit FILL_IN clause paralleling the existing MATCH one: a FILL_IN item with
a `visual_stimulus` table must carry that table — header and every data/blank row — ENTIRELY in
`visual_stimulus`, never reproduced as pipe-markdown, plain text or a paraphrased list in
`item_stem`. Applied to all three stages (prep 1.0→1.1, middle 3.2→3.3, secondary 1.1→1.2).
Cause: the anti-duplication prohibition had only ever been written for MATCH and for MCQ /
TRUE_FALSE options, never FILL_IN, so `english/vii/ch_02` `Q-VG-B-1` inlined its antonym table
as pipe-markdown in the stem AND partially in `visual_stimulus`. Two saved items were back-filled
and the 41-file corpus re-scanned clean.

**Satisfied but not exercised at S11's C4:** the four FILL_IN items in the IX ch 7 library carry
no `visual_stimulus` at all — the cloze sets are prose with inline blanks — so the table-bearing
case remains untested by live generation.

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
