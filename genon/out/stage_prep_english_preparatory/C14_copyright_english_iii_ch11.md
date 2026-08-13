# C14 · Copyrights review — english · III · ch 11 *The Big Laddoo*

Scanned: **11 files** — 3 canonicals + 8 C6 served plans — **24,705 teacher-facing words**,
including `result.dropped_units` and the exports. Source: the correct textbook,
`textbooks/english/iii/chapter 07 - The Big Laddoo.pdf` (886 words), `--book-only` so Aruvi's own
summary cannot be mistaken for the protected work.

**Verdict: checks 1, 2 and 3 pass, with two subjective calls quoted and one Rule-3 defect. And
the step found a tooling defect that invalidates a CERTIFIED stage's C14 result.**

---

## 0 · THE HEADLINE IS THE SCANNER, NOT THE PLAN

`genon/copyright_scan.py` resolved the textbook by globbing `chapter\s*0*{ch}` against the PDF
names — assuming the plan's chapter number is the book's. The copyright review records the
consequence for english as *"the glob matches nothing … the book contributes ZERO words"*.

**At two of the three english stages it is worse than nothing: it matches a DIFFERENT
CHAPTER'S BOOK.**

| stage · chapter | old glob resolved to | correct book | failure |
|---|---|---|---|
| english **III ch 11** (this pilot) | `chapter 11 - Chanda Mama Counts the Stars.pdf` | `chapter 07 - The Big Laddoo.pdf` | **WRONG BOOK** |
| english VI ch 8 (S10) | *(none)* | `Chapter 03 - Nurturing Nature.pdf` | no book (as documented) |
| english **IX ch 7** (S11, **CERTIFIED**) | `chapter 07 - Carrier of Words.pdf` | `chapter 04 - Vitamin-M.pdf` | **WRONG BOOK** |
| english VII ch 1 · VIII ch 1 | correct by coincidence | same | first chapter of a unit |

A wrong book scores ~0% and reads as a **confident clean pass** — the most expensive way for
this check to fail. Measured on S11's own certified canonical:

| S11 · english IX ch 7 scored against | book words | matched | % | runs | longest |
|---|---|---|---|---|---|
| `Carrier of Words` (what it actually used) | 5,936 | **0** | **0.00%** | 0 | — |
| `Vitamin-M` (the real chapter) | 8,634 | **51** | **1.18%** | 4 | **20 words** |

And the real scan surfaces a run S11 never saw — 13 words of narrative prose in an **assessment
item's** `visual_stimulus`: *"off he went twirling his walking stick jauntily leaving Ravi in a
dilemma"*. **S11's C14 result is not evidence and its C14 should be re-run.**

**Fixed here.** The mapping was in the split summary all along — `_source_unit.unit_chapter_number`.
The resolver reads it and falls back to the plan's own number, so the change is additive.
Verified across the corpus: all three english stages now resolve correctly (VI ch 8 → 5,373
book words, **exactly the figure the copyright review obtained by pointing at the PDF by hand**),
and mathematics · social_sciences · science · TWAU are byte-for-byte unchanged with no split
annotation.

---

## 1 · No verbatim reproduction beyond short quotation — **PASS, with two subjective calls**

| | |
|---|---|
| teacher-facing words | **24,705** |
| book-matched words (runs ≥ 8) | **573 = 2.32%** |
| runs ≥ 8 words | 60 — **46 lesson-plan, 14 assessment** |
| **DISTINCT matched strings** | **8** |
| longest run | **18 words** |
| brands · external images · URLs | 0 · 0 · 0 |

Against the benchmarks: english·middle 1.64% / longest 14, maths·middle 1.15% / longest 18. **This
is the highest percentage measured so far — and the denominator is why.** The book is **886
words**, a sixth of middle's 5,373, so the same handful of prompts covers proportionally far more
of it. The honest measure is the **eight distinct strings**; the 60 runs are those eight recurring
across 11 files.

| words | ×  | where | string | ruling |
|---|---|---|---|---|
| 18 | 3 | **assessment** `visual_stimulus` | *"a piece of paper, a small stone, a green leaf, a pencil, an eraser, a feather, a spoon"* | **APPARATUS — not expression.** §2 |
| 17 | 6 | lesson plan, band | *"Have you seen a big laddoo? How big was it? Did you eat it all by yourself?"* | **DEFECT — LP Rule 3.** §3 |
| 9 | 9 | lesson plan, band | *"Oh! What a BIG SPLISH-SPLASH it would be!"* | **the F2 residual** — the poem's closing line, quoted, used as a chant cue |
| 8 | 19 | both | *"That can be eaten / That cannot be eaten"* | **TABLE COLUMN HEADERS.** The sorting task cannot be set without them |
| 8 | 5 | lesson plan | *"what do you think happened to the laddoo"* | quoted discussion prompt, subheading named |
| 8 | 6 | lesson plan | *"how did you know it was a laddoo"* | same |
| 8 | 6 | lesson plan | *"what different kinds of laddoos have you eaten"* | same |
| 8 | 6 | lesson plan | *"some sweets and dishes prepared on that day"* | same |

**The most frequent match (×19) is a pair of table column headers**, and the second-largest is a
list of seven ordinary objects. Neither is creative expression; both are the apparatus a child
needs in front of her to do the task at all.

### The assessment-side runs, and why they are not middle's result reversed

Middle's C14 reported **0 runs in assessment items** and called the constitutional firewall
proven. Preparatory reports **14** — and that difference deserves precision rather than alarm,
because **every one of the 14 is apparatus**: the seven-object list and the two column headers.
No assessment stem, `suggested_answer` or rubric field reproduces book prose.

**I checked whether the firewall had actually broken, because it looked like it had.** The object
list exists in the summary *only* in `beyond_text.tasks_verbatim[0].task_text` — a field the
generator is forbidden to read. But the LP's handoff `section_context` names the objects as bare
nouns —

> *"Float-or-sink test with seven everyday objects: paper, stone, leaf, pencil, eraser, feather,
> spoon."*

— and `section_context` is a **permitted** input (Rule 2: it "determines what the question is
about"). The item re-articled the bare list into *"a piece of paper, a small stone…"*, which is
simply how one writes that list in English for a Grade III worksheet. **The firewall held; the
overlap is convergent, not copied.** Recorded at length because a scanner will flag it on every
future run and the reasoning should not have to be rediscovered.

## 2 · No third-party material the textbook does not carry — **PASS**

Zero. The only third-party work in play is the NCERT poem, which the textbook carries. Its
treatment:

- **assessment: addressed by locator, never reproduced** — *`Read the stanza on page 70 beginning
  "If all the laddoos were one Laddoo"`*, a **7-word** incipit against the 8-word cap, no
  ellipsis, and no poem line in any stem, `visual_stimulus`, `suggested_answer` or rubric field.
  **This is what the pilot was chosen to test, and it is the rule working.**
- **lesson plan: two quoted single lines** — the closing line (9 words, ×9 files) and a 5-word
  fragment — both inside quotation marks, both used as a chant cue. Covered by the founder's
  ruling of 2026-08-13 (S10's C3): *a short lift inside quotation marks that frames a question is
  reference, not reproduction.*

**The scanner cannot settle the poem question in either direction, and this chapter proves both
halves.** Its lines run 4–9 words, so (a) an 8-gram scan is blind to a *compliant* incipit, and
(b) a line-level scan flags one. The C3 read had to clear the compliant item by eye; this scan
catches the LP's chant line at 9 words. **C14 on a preparatory poem chapter cannot be automated
in either direction** — recorded at C3, confirmed here with the measurement in hand.

## 3 · Attribution — **PASS in form; one Rule-3 defect**

Every quoted run sits inside quotation marks, its band names the textbook subheading, and
`task_brief`s carry `(p.NN)` locators — 32 of 32 across the library. There is no formal "NCERT"
credit line anywhere, which is true of every stage in the campaign and is a campaign-level
question, not this stage's.

**The one breach is a rule breach, not a copyright one.** LP Rule 3: *"Band activities reference
tasks by `spine_section_name` + brief; they do not restate `task_text` or enumerate sub-items
verbatim."* Top u3 band 1:

> *"Let us think — teacher poses the first prompt: **'Have you seen a big laddoo? How big was it?
> Did you eat it all by yourself?'** Children think for a moment, then share with a partner."*

That is the task text restated verbatim — 17 words, the largest lesson-plan-side book match in
the library, and it propagates into 6 of the 11 files because it rides in u3.

**It is one band of 133.** Every other band references its task by subheading + brief as the rule
asks, and the four remaining 8-word matches are prompt *fragments*, which is the reference form.
So this is an isolated slip, not a pattern — filed, repairable in place, and the rule that
governs it is already on the books.

---

## Filed

1. **The resolver defect** — wrong-book resolution at two of three english stages; **S11's
   certified C14 result is invalid** and should be re-run. Tooling fixed here.
2. **The Rule 3 restating** — one band, 17 words.

**No wholesale reproduction, no unattributed quotation, no third-party material the textbook does
not carry. C14's exit is met.**
