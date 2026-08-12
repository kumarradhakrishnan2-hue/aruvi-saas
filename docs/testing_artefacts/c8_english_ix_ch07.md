# C8 — the X−1 → X transition inspection · english · IX · ch 7 *Vitamin-M*

**Date:** 2026-08-12 · Six transitions read, each as the teacher meets them: **sitting X−1 and
sitting X in full, consecutively** — titles, materials, every band, teacher notes.

| X | class | host prefix | borrowed from | X−1 → X | **rating** |
|---|---|---|---|---|---|
| 8 | `fill/forward` −2s | p10 | 10 (self) | VocGram → Listening+Speaking | **clean** |
| 9 | `fill/single` −1s (below floor) | p10 | 10 (self) | Listening+Speaking → Writing | **clean** |
| 11 | **Case-1 synthesis borrow** | p10 | **17** | Beyond-the-Text → Synthesis | **JUMPY** |
| 12 | `fill/single` | p14 | 14 (self) | Writing → Beyond-the-Text | **clean** |
| 15 | **Case-1 synthesis borrow** | p14 | **17** | Beyond-the-Text → Synthesis | **JUMPY** |
| 16 | `fill/single` | p17 | 17 (self) | Speaking+Writing → Beyond-the-Text | **clean** |
| — | `fill/backward` | — | — | the band produces none | **N/A** |

*(X = 8 is not in the C6 serve set — no 18-period or 8-period request was made — so it was
derived in-process with `serve_plan`, deterministically and without an API call, to cover the
`fill/forward` class the sweep exercises.)*

**Zero jumpy on the four self-fills. Both synthesis borrows are jumpy, and they are the same
defect seen twice.**

---

## The two JUMPY transitions — ARV-D-136

### X = 11 · p10's ten units → borrowed U17

**Sitting 10** (p10's own closer) ends the chapter's comparative work:

> *"Whole-class discussion compares the child's bond with his parents to Ravi's bond with
> Grandpa… "* — notes: *"…The photograph slide-show task is set as homework and **does not
> require any classroom artefact from an earlier unit**."*

**Sitting 11** (the borrowed synthesis) opens well and closes badly. Its first two bands are
model-grade for a travelling unit:

> `[0–15]` *"…invites students to respond briefly in turn, **drawing freely on any part of the
> chapter they have read**…"*
> notes: *"**Students need not have covered every task to participate**: the chapter's content
> is now the shared ground…"*

Then the third band, twenty of the fifty minutes:

> `[30–50]` *"Students **complete the draft article** 'Our Inspiring Elderly' (**Paragraphs 3 and
> 4** — overcoming challenges and concluding comment), working independently. **Those who have
> already completed the draft** review it against the four-paragraph structure…"*
> materials: *"**Students' draft article** (notebooks or draft sheets)"*

**Why that is jumpy and not merely a register shift.** In the standard canonical this is
coherent: U15 drafts Paragraphs 1 and 2, U17 completes 3 and 4. **The host here is p10, whose
writing unit U9 writes the whole four-paragraph article in one sitting** — *"Students plan and
draft their article… following the four-paragraph scaffold; they write the title at the top and
their name and grade below it"*, then peer-exchange and revise. So the class arrives at sitting
11 with a **finished** article and is told to write the two paragraphs it wrote two sittings
ago. Forty per cent of the borrowed unit instructs work already done, and the hedge —
*"Those who have already completed the draft review it"* — covers the whole class rather than a
few fast finishers, which is not what it was written for.

### X = 15 · p14's fourteen units → borrowed U17

**Identical, and this is the part that matters:** p14's writing unit (U11) also writes the
article whole — *"Students write their four-paragraph article independently, including title,
name, and grade"* — and its sitting 14 is the Beyond-the-Text unit. So the same closer lands on
the same contradiction from the other host.

**Both compacts write the article in one sitting; only the standard splits it.** The borrowed
unit is therefore coherent in exactly one of the three plans it can appear in — its own.

---

## The four CLEAN transitions, with the evidence

- **X = 8 · VocGram → Listening+Speaking.** Sitting 8 opens *"Teacher reads the meditation
  podcast transcript aloud twice at a natural pace"* — a self-contained opening move. Its notes
  go further and mark the independence explicitly: *"treat the two activities as independent"*,
  and *"the intonation practice… is available for paired self-study alongside this unit"*.
  Sitting 7's backward reference (*"Having worked with the story's movement and sound vocabulary
  in the previous vocabulary unit"*) is legal at v1.10 and names content. The two dropped cells
  are declared in the coverage note.
- **X = 9 · Listening+Speaking → Writing.** Sitting 9 opens by modelling the article structure
  on the board from scratch — *"Teacher models the four-paragraph article structure… and
  discusses what 'inspiring' means"* — and materials are `Writing paper or notebooks`, a blank.
  Nothing presumes the prefix.
- **X = 12 · Writing → Beyond-the-Text.** Sitting 12 opens *"Teacher asks students to recall the
  description of Grandpa's walking stick from the story"* — an assumption about the CHAPTER'S
  CONTENT, which is exactly what a borrowed unit is licensed to assume, and true for any prefix
  that read the story. `materials: [Textbook pp.119–125, Exercise books]` — no produced artefact.
- **X = 16 · Speaking+Writing → Beyond-the-Text.** Same closer from the top canonical, same
  self-contained opening (*"Teacher displays or describes the four walking stick images"*).
  Sitting 15 drafts Paragraphs 1–2 and sitting 16 does not touch the draft, so the seam is clean
  even though the plan stops one unit short of the synthesis.

**A pattern worth naming:** every clean opening move is either a text the teacher reads aloud or
a structure the teacher models on the board. Every jumpy one reaches for something the students
are holding. That is a cheap heuristic for reading a transition and it matches what the artefact
rule already says.

---

## Remedy — deterministic first, in C8's own order

1. **Does the lender actually first-deal the section?** N/A. This is the Case-1 borrow, where
   the lender is fixed by §0.4: the standard's synthesis. There is no first-deal question.
2. **Re-examine the tie-break that picked this lender.** Nothing to re-examine — Case 1 has one
   candidate by construction.
3. **Harden the brief's self-containment wording.** ← this is the applicable remedy, and it is
   landed.

The standard brief already said the synthesis *"must NOT assume any particular earlier activity,
reading, discussion, homework or material actually happened"*. The model obeyed that in its
discussion bands and broke it in the last one, because **continuing a piece of work does not read
as "assuming an activity"** — it reads as ordinary teaching. So the brief now says the quiet
part, exactly as the artefact rule had to at S5:

> **"THE SYNTHESIS UNIT STARTS AND FINISHES ITS OWN WORK.** It may DRAW ON what the chapter
> taught; it must not CONTINUE, complete, revise or hand back a piece of student work another
> unit began — no 'complete the draft', no 'finish the poster', no 'return to the essay you
> started'. A borrowing class may have done that work in one sitting, or in a different form, or
> not yet at all. Any writing, making or performing in this unit begins and ends inside its own
> minutes."

Added to `variant_plans.top_brief_for` (standard-canonical brief only — it is the only plan that
carries a travelling closer). **A brief change is not a constitution change**: it triggers a
`--certify-only` re-run, not the §9 cascade, and no other stage's library re-opens. It does not
repair *this* library — that is the founder's call at the human gate, alongside ARV-D-132.

**Detector already in place from C7:** the scoped `artefact` patterns flag `materials`
possessives and completion verbs, so a future library carrying this shape is visible at build
time rather than by reading two sittings side by side.

---

## What the human gate should read

The sweep table (C5), the standard's synthesis unit — and **the X = 11 pair specifically**. It is
the sharpest single question this chapter poses: a class that finished its article in sitting 9
being asked, in sitting 11, to write paragraphs 3 and 4 of it.
