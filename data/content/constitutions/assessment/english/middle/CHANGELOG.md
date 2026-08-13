# CHANGELOG — Assessment Constitution · English · Middle Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).

---

## v3.7 — 2026-08-13 · S10's P-prep — A6 confirmed, A9 added, and the history moved to this file

Campaign step: `docs/testing.md` §3, stage **S10 · english · middle**. Artefacts (script,
pre-file, diff): `genon/out/stage_prep_english_middle/`.

**A6 — CONFIRMED, not amended.** P2 asks that every item carry its anchor unit, or the subject's
equivalent, copied from the LO row consumed. **Rule 8A already says it**, having landed a day
early with the PAIR amendment: the anchor is the (section × spine) **CELL**, carried by the
item's own `source_section_id` + `source_spine` — the 8-rule table's **row 7**, and its only PAIR
key — the platform resolves it against each period's `section_id` + `spines_taught[]`, and
`period_ref` / `period_number` / `unit_ref` MUST NOT be emitted. The v1.2-era band-level
`phase_ref` is absent (`grep -c` = 0) and was not reintroduced. Nothing to amend; asserted by
guard.

**A9 — the two lines, and the removal is N/A.** This file never carried the MEMORY-item-18
position prohibition — testing.md P2 names the four files that do (SS and Science, middle and
secondary) and this is not one; `consecutive`, `same label` and `vary in position` all assert 0.
So A9 lands as the addition alone, in the v1.7 wording, **purely additive** because there was no
prior "none of the above" ban to absorb:

- MCQ option order carries no meaning and is not the model's to set — emit them as authored;
  uneven letters across a chapter are coincidence, not a defect, and the platform arranges them
  deterministically after generation (`genon/normalize_options.py`, STEP 6 of `build_library.py`).
- An option MUST NOT refer to another option **by its label** — "both A and B", "none of the
  above", "all of the above", "either B or C" — the one construction a downstream sort cannot
  reorder without rewriting the item.

They sit in **Rule 4**, where english states its MCQ semantics, rather than in Rule 5's indented
answer-layer list where a two-paragraph block reads as part of a bullet. Same site
english·secondary chose at v1.4, for the same reason. **No arrangement sentence was added** —
`alphabetic`, `never led with` and `first word at which they differ` all assert 0, and re-adding
any rule that names a label position is forbidden (v1.6 and v1.7 both).

**P4 — the version history left the constitution.** v3.6 wrote its own five-line changelog into
the top of the file, above DESIGN PRINCIPLE. P4 puts history in this sidecar and leaves only the
`VERSION` line in the file; the block is lifted out and its content is the v3.6 entry below.

---

## v3.6 — 2026-08-12 · THE PAIR (carried from S11, back-filled here at P4)

*Recorded from the block that stood at the top of the constitution until v3.7 lifted it out.*

**Rule 2 now emits TWO items per spine-cell, not one**, on a prescriptive per-spine slot table:
slot 1 at the comprehension/application rung, slot 2 at inference/analysis/creation, the two
types MUST differ (sole exception Speaking and Writing, whose spines permit exactly one type
each and which differ by mode or form instead). Both items carry the SAME `source_lo` — they
sample one outcome twice rather than splitting it into two — and where the `implied_lo` is
compound they must take different strands of it. Item count per chapter = 2 × total
`section_contributions`.

**A new Rule 8A scopes the pair in two stages** across the cell's teaching span: slot 1 is
answerable once the cell's early teaching has happened, slot 2 presumes the whole cell. That
declaration is what licenses the platform to DISPERSE a cell's items across the units that
taught it, in slot order, instead of anchoring both at the close — which is why Rule 2 forbids
emitting slot 2 first. Scoping is declared by SLOT, never by number.

Amended in step with english/secondary v1.6 and english/preparatory v1.4. Reasoning:
`docs/english_secondary_item_density.md` — english was the only subject whose assessment axis is
capacity-bounded (the six spines, fixed) rather than content-bounded, so post-split its grid
collapsed to 1×6 and the item ceiling was 6 at any period count.

---

## v3.5 — 2026-08-12 · the poem is addressed, not reproduced (ARV-D-138, carried from S11)

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
**Middle has no such block**: its `visual_stimulus` is `"" | pipe-table` only, non-empty solely
for tabular data. The one open door was Rule 3's REQUIRED line — *"A specific line, image, or
phrase from poem_text"* — which invites the poem into `item_stem`, where nothing caps it.

**Two edits, both in Rule 3.**

1. **REQUIRED** — "A specific line, image, or phrase from poem_text" becomes "A specific image,
   phrase or turn in the poem — **ADDRESSED BY ITS PLACE, NOT COPIED OUT**: a stanza or line
   reference plus an incipit of **at most eight words** in double quotes."
2. **PROHIBITED** — a positive ban: the poem's lines are not copied into `item_stem`,
   `visual_stimulus`, `suggested_answer` or any rubric field, beyond the eight-word incipit,
   and never with an ellipsis continuing the quotation — *"the student is holding the book; the
   poem lives there, and the item's work is the analysis, not the transcription."* A REQUIRED
   clause tells a model what it may do; a PROHIBITED clause is what it checks itself against.

**Why an incipit at all.** NCERT prints **no line numbers** on its poems and a stanza can break
across a page, so a bare line reference makes a student count. A few words of the first line
find it at once, identify rather than substitute, and are the convention of every citation
index and exam paper. The cap is hard and in the rule because the only real risk is drift.

**Reading is untouched.** This stage names `poem_text` in six places; four of them are READ
sites (INPUTS, the grounding rule, the no-foothold exception for skill-type spines, and
verification) and they are all intact. Reading the poem is what makes a good question possible,
and the summary never leaves the machine. Only reproduction into the artefact is closed.

**§9 — re-authors nothing.** This stage has no library, no canonical and no certified chapter;
it is pre-C1. Free today, ~₹80 a library once poem chapters exist.

Artefacts: `genon/out/stage_prep_english_secondary/` — `assess_english_middle_v3.4_pre.txt` ·
`assess_english_middle_v3.4_to_v3.5.diff` · `apply_s9_s10_poem_locator.py`. Origin:
`docs/testing_artefacts/c14_english_ix_ch07.md`.

---

## v3.4 and earlier — unrecorded

No sidecar existed before this file, and the constitution carries no in-document version
history. From MEMORY.md's constitution inventory: **v3.1** (2026-07-13) is the middle
assessment constitution as the campaign first found it — prep's shapes plus ECR and PROJECT;
**v3.2** (2026-07-13) added Rule 4's "NAME THE REFERENCED WORD"; **v3.3** (2026-07-13) added
the FILL_IN table anti-duplication clause (checklist item 12); **v3.4** (2026-07-13) narrowed
the "no Part A/B" ban to the visual case (item 13). Completing this history is **S10's own P4**.
