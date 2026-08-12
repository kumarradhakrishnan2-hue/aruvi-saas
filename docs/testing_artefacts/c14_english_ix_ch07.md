# C14 — copyrights review · english · IX · ch 7 *Vitamin-M*

**Date:** 2026-08-12 · Reference: `docs/NCERT_copyright_review.md` v1.1, where **F2 — English
verbatim task-text in served plans — is the sole open finding**. This is the stage that owns it.
· Sources compared: `textbooks/english/ix/chapter 04 - Vitamin-M.pdf` (1,602 lines, extracted)
and the chapter summary · Surfaces: the 3 library canonicals, the 4 served plans, and
`result.dropped_units`.

**Method:** for every teacher-facing string, the **longest word-run that appears verbatim in the
NCERT PDF** was computed (normalised whitespace and case, minimum 6 words). Not a spot-check —
every band, note, title, brief, stem, stimulus and rubric bullet in the top canonical.

---

## The pilot chapter is clean

| check | result |
|---|---|
| **1 · verbatim reproduction beyond short quotation** | **PASS (subjective on two strings).** Across all 17 units — 66 bands, 17 titles, 17 notes, 20 briefs — exactly **two** surfaces carry a ≥6-word run from the textbook, and both are exercise instructions rather than literary text: U1 *"an elderly person at home or in"* (7 w) and U7 *"one advantage and one disadvantage of"* (6 w). Naming which exercise the class is doing is hard to do without them. **Every assessment item — 6 stems, 1 stimulus, 20 rubric bullets — has ZERO runs of 6 words or more.** |
| **2 · third-party copyrighted material** | **PASS.** The chapter's supplementary text, *'The Lost Child'* by Mulk Raj Anand, is **referenced, never reproduced**: "Teacher reads 'The Lost Child' by Mulk Raj Anand (pp.120–125) aloud". Author named, page range given, not a line quoted. No lyrics, brand text or images anywhere. |
| **3 · quoted source text attributed** | **PASS.** Nothing is quoted without naming its source; the two fragments above are exercise phrasing, not quotation. |

**The EXTRACT_ANALYSIS stimulus is the interesting one, and it exonerates the design.** The
assessment constitution's Rule 9 calls for "a short passage/stanza copied **verbatim**" — which
sounds like the F2 conduit. It is not, on a prose chapter: the extract is verbatim from
**Aruvi's own `prose_summary`**, not from NCERT. Measured — the longest run it shares with the
summary is 12 words, and it shares **no** 6-word run with the textbook PDF:

> *"Grandpa craftily manoeuvred a confession from Ravi that he had received no such instruction,
> then strides out with his mahogany walking stick — brass handle carved as an eagle's head —
> and yellow cap."*

The chain is NCERT text → Aruvi's paraphrase (the chapter summary) → the item. **What reaches
the cloud is Aruvi's prose.** For prose chapters, F2's conduit is closed by construction.

---

## The finding: F2 is open on this stage, and it is in the POEM chapters — ARV-D-138 (S2)

The same Rule 9 sentence reads differently when the section is a poem. `[SECONDARY DELTA]`
permits the stimulus to be a "verbatim extract block … **3–8 lines**" drawn from
`prose_/drama_summary` **or `poem_text`**, and Rule 3 licenses an item to draw on "a specific
line, image, or phrase from **poem_text**".

**`poem_text` is not Aruvi's paraphrase — it is the poem.** Measured on ch 2 *Bharat Our Land*:

- the summary carries `poem_text` of **16 lines**;
- **13 of those 16 lines appear verbatim in the NCERT chapter PDF.**

So a poem chapter's EXTRACT_ANALYSIS item would place **3–8 lines of an NCERT-published poem
into a canonical** — and canonicals are precisely what the v1.1 ruling sends to the cloud. That
is F2 as written: *"the verbatim conduit must be either closed (substitute a paraphrase + page
ref) or licensed before English plans are served commercially."*

**Scale on this class alone: 8 of the 16 chapters in english IX are poems** — chs 2, 4, 6, 8,
10, 12, 14 and 16, carrying 10 to 33 lines of `poem_text` each. This chapter is prose, so **nothing in this library is
affected**; the exposure is in the constitution, not in the artefact.

---

## CLOSED THE SAME DAY — assessment v1.4 → v1.5, the poem locator

Founder ruling 2026-08-12: fix it now rather than accept or defer. Two things were checked
before drafting, and both changed the design from my first proposal.

**Is `poem_appreciation_summary` the safe substitute?** Mostly, but not cleanly. Measured across
all eight poem chapters: it is Aruvi's own critical prose (108–189 words), with a **longest
verbatim run against the textbooks of zero words in seven of eight** and a five-word fragment in
ch 10. But three chapters quote short lines inside the commentary — ch 2 *"she's peerless, let's
praise her!"*, ch 8 the refrain *"I cannot remember my mother"* (×3), ch 16 *"Step up to the
challenge"*. Four to six words each, attributed, embedded in criticism. Pointing the extract
block at it would **narrow** the conduit, not close it — and it would also cost the pedagogy,
because an extract-analysis question on a poem *is* "read these lines closely".

**So the fix is the one the copyright review itself names — paraphrase + page ref.** The student
is holding the textbook; the stimulus does not have to reproduce the poem to point at it.

**And the incipit is part of the design, not a hedge.** NCERT prints **no line numbers** on its
poems, and ch 2's stanzas break across a page boundary mid-poem — "lines 5–8" alone would have a
student counting. A few words of the first line find it at once, it identifies rather than
substitutes, and it is the convention of every citation index and exam paper. The cap is hard
and in the rule: **at most eight words, one line, no ellipsis, no second fragment.**

**Five edit sites, not the one I first claimed** — the permission was written in five places,
and two of them I had missed: Rule 4's type definition (which also carried an "or inline"
escape into `item_stem`) and the schema comment.

| # | site | change |
|---|---|---|
| 1 | Rule 4 · type definition | drops "verbatim"; poem branch closes the inline escape |
| 2 | Rule 3 · REQUIRED | "a specific line … from `poem_text`" → identified by location, not reproduced |
| 3 | Rule 9 · opening | stimulus = extract block (prose · drama) **or locator (poem)** |
| 4 | Rule 9 · permitted formats | one bullet splits in two; the **poem locator** is the only form for a poem |
| 5 | schema comment | the format list, which repeated the old wording |

**Reading is untouched.** INPUTS §2, Rule 2(a) and Rule 6 still name `poem_text` as a content
source — reading the poem is what makes a good question possible, and the summary never leaves
the machine. Only reproduction into the artefact is closed; the edit script asserts `poem_text`
survives in exactly those three read sites and nowhere else.

**§9 — re-authors nothing.** A constitution change normally re-opens the stage; this one
restricts a path the installed library does not use. ch 7 is prose, its single stimulus is a
prose extract from `prose_summary`, no locator applies — so it satisfies v1.5 exactly as it
satisfied v1.4, checked rather than assumed. No poem-chapter library exists anywhere, which is
why this was free today and would not have been after the first poem chapter was generated.

---

## Exit

**Zero unattributed or wholesale reproductions in the pilot library and its served plans**;
checks 1–3 pass for ch 7. **ARV-D-138 is CLOSED by assessment v1.5** — F2's English conduit is
shut at this stage for both prose (already, by construction) and poems (now, by rule). S9 and
S10 inherit the pattern and should carry the same five edits at their own P2, before any poem
chapter of theirs is authored.
