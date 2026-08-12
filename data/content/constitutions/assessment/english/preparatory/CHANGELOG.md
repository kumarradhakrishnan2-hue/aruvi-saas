# CHANGELOG — Assessment Constitution · English · Preparatory Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).

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
