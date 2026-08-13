# CHANGELOG — Assessment Constitution · English · Preparatory Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).

---

## v1.5 — 2026-08-13 · S9 · english · preparatory — A6 confirmed, A9 added, and a history block lifted out

Drawn class **III**. Reference: SS·secondary assessment v1.7, read through english·secondary
v1.5 and english·middle v3.7.

**A6 — a genuine CONFIRMATION, the second in the campaign and for the same reason as the
first.** P2 asks for a confirmation and an amendment only where absent. **Rule 8A already
carries it in full**, having landed a day early with the cross-stage PAIR pass (v1.4,
2026-08-12): the anchor is the (section × spine) **CELL**, borne by the item's own
`source_section_id` + `source_spine` — 8-rule **row 7**, the table's only PAIR key — the
platform resolves it against each period's `section_id` + `spines_taught[]`, and
`period_ref` / `period_number` / `unit_ref` MUST NOT be emitted. The v1.2-era band-level
`phase_ref` is absent and was not reintroduced (`grep -c phase_ref` = 0). **Nothing was
amended for A6.** Asserted by guard, not by eye.

**A9 — the REMOVAL is N/A; the two lines are purely additive.** This file never carried the
MEMORY item-18 position prohibition — testing.md P2 names the four files that do (SS and
Science, middle and secondary) and this is not one; `consecutive items`, `same label` and
`vary in position` all assert 0. The fifth stage running where the removal is N/A. **ADDED**,
in the v1.7 wording, in **Rule 4** where english states its MCQ semantics — the site
english·secondary chose at v1.4 and middle at v3.7, for the same reason (Rule 5 is an indented
bullet list a two-paragraph block reads oddly inside): the *"order carries no meaning and is
not yours to set"* mandate, and the by-label option-reference prohibition ("both A and B",
"none of the above", "all of the above", "either B or C"). Purely additive — preparatory
carried no prior "none of the above" ban to absorb. **NOT re-added:** `alphabetic`,
`never led with`, `first word at which they differ` all assert 0.

**P4 had a removal of its own here, the same one S10 had to make.** v1.4 had written its
seven-line changelog **INTO** the constitution, above DESIGN PRINCIPLE — which is exactly what
P4 forbids. It is lifted out and back-filled below as the v1.4 entry; the `VERSION` line stays
in the file. Guard asserts `v1.4 (2026-08-12)` = 0 in the constitution.

**Confirmed present and untouched:** the poem locator (Rule 3, ARV-D-138, carried 2026-08-12 —
`REPRODUCING THE POEM` and the eight-word incipit cap), Rule 2's slot table and the PAIR. The
pilot chosen for this stage is a **poem** (III ch 11 *The Big Laddoo*, `poem_text` 13 verbatim
lines, section B, pp. 70–77), so preparatory's half of the copyright fix is proved by live
generation at C3 rather than inherited untested — the same reasoning S10 applied to its own.

**§9 — costs nothing.** No english·preparatory library exists; nothing re-opens.

Artefacts: `genon/out/stage_prep_english_preparatory/` — `apply_s9_assessment.py` ·
`assess_english_preparatory_v1.4_pre.txt` · `assess_english_preparatory_v1.4_to_v1.5.diff`.

---

## v1.4 — 2026-08-12 · THE PAIR (cross-stage; lifted out of the constitution at v1.5)

*Back-filled here at S9's P4. This text was written into the constitution itself above DESIGN
PRINCIPLE, which P4 forbids; it is recorded verbatim and removed from the file.*

> v1.4 (2026-08-12) — THE PAIR. Rule 2 now emits TWO items per spine-cell, not one, on a
> prescriptive per-spine slot table; a new Rule 8A scopes them in two stages across the cell's
> teaching span. Amended in step with english/middle v3.6 and english/secondary v1.6. At THIS
> stage the pair is deliberately light — slot 1 is recognition, slot 2 is a single short
> production — never two long tasks. Reasoning: `docs/english_secondary_item_density.md`.

Landed ahead of this stage's own P-prep, on the reasoning that §9 re-authors nothing while no
english library exists. Rule 8A is what makes A6 a confirmation rather than an amendment at
v1.5 above.

---

## v1.3 — 2026-08-12 · the poem is addressed, not reproduced (ARV-D-138, carried from S11)

**Landed ahead of this stage's own P-prep**, because the window closes the moment a poem
chapter is authored.

**The finding, measured at S11's C14 on english·secondary.** `poem_text` in a chapter summary
is not a paraphrase — it is the NCERT poem. On english IX ch 2 *Bharat Our Land*, **13 of the
summary's 16 poem lines appear verbatim in the textbook PDF**. An item that quotes them puts
published verse into a **canonical**, and canonicals are the one artefact class the copyright
review's v1.1 ruling sends to the cloud (summaries and PDFs never leave the machine). That is
finding **F2** of `docs/NCERT_copyright_review.md`, the campaign's sole open copyright finding.

**Why this stage's edit is small.** Secondary needed five edit sites because its Rule 9 carries
an EXTRACT_ANALYSIS "verbatim extract block, 3–8 lines" — the sharp end of the conduit.
**Preparatory has no such block**: `visual_stimulus` is `"" | pipe-table`, and EXTRACT_ANALYSIS
is not in its type set at all. The only open door was Rule 3's REQUIRED line — *"A specific
line, image, or phrase from `poem_text`"* — which invites the poem into `item_stem`, where
nothing caps it.

**Two edits, both in Rule 3.**

1. **REQUIRED** — "A specific line, image, or phrase from `poem_text`" becomes "A specific
   image, sound-pattern or phrase in the poem — **ADDRESSED BY ITS PLACE, NOT COPIED OUT**: a
   stanza or line reference plus an incipit of **at most eight words** in double quotes."
2. **Prohibited** — a positive ban: the poem's lines are not copied into `item_stem`,
   `visual_stimulus`, `suggested_answer` or any rubric field, beyond the eight-word incipit,
   and never with an ellipsis continuing the quotation. A REQUIRED clause tells a model what it
   may do; a PROHIBITED clause is what it checks itself against, so both are needed.

**The wording deliberately echoes this file's own Rule 9**, which already carries the doctrine
for pictures: *"do NOT introduce a separate visual format. Instead, reference the textbook page
in `item_stem` itself — 'Look at the picture on Textbook page 6…'. The teacher has the book; the
image lives there."* The poem clause is that sentence applied to verse, which is why it reads
native rather than imported.

**Why an incipit at all.** NCERT prints **no line numbers** on its poems and a stanza can break
across a page, so a bare line reference makes a child count. A few words of the first line find
it at once, identify rather than substitute, and are the convention of every citation index.
The cap is hard and in the rule because the only real risk is drift.

**Reading is untouched.** INPUTS, the grounding rule and the verification rule still name
`poem_text` as a content source — reading the poem is what makes a good question possible, and
the summary never leaves the machine. Only reproduction into the artefact is closed.

**§9 — re-authors nothing.** This stage has no library, no canonical and no certified chapter;
it is pre-C1. Free today, ~₹80 a library once poem chapters exist.

Artefacts: `genon/out/stage_prep_english_secondary/` —
`assess_english_preparatory_v1.2_pre.txt` · `assess_english_prep_v1.2_to_v1.3.diff` ·
`apply_s9_s10_poem_locator.py`. Origin: `docs/testing_artefacts/c14_english_ix_ch07.md`.

---

## v1.2 and earlier — unrecorded

No sidecar existed before this file, and the constitution carries no in-document version
history. From MEMORY.md's constitution inventory: **v1.0** (2026-07-13) is the original
preparatory assessment constitution — types MCQ · SCR · MATCH · FILL_IN · TRUE_FALSE ·
ORAL_PROMPT · WRITING_TASK · PROJECT, **ECR banned**; **v1.1** (2026-07-13) added the FILL_IN
table anti-duplication clause (checklist item 12); **v1.2** (2026-07-13) narrowed the
"no Part A/B" ban to the visual case (item 13). Completing this history is **S9's own P4**.
