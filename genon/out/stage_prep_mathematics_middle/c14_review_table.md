# S7 · mathematics · middle — C14 COPYRIGHTS REVIEW

Chapter under test: **mathematics / VII / ch 7 — "A Tale of Three Intersecting Lines"**
(Ganita Prakash, Grade 7). Run 2026-08-11. Reference: `docs/NCERT_copyright_review.md` v1.1.

Artefacts: `c14_copyright_review.py` (re-runnable) · `c14_report.txt` (its full output).

---

## The surface actually read

| | |
|---|---|
| Plans | **13** — 3 canonicals on disk (12/10/7) + **all 10 C6 matrix rows served fresh in memory** |
| Why served fresh | the identity rows write no file, and only 3 of the C6 files survived the ARV-D-107 purge; C7 read the served set for the same reason |
| Strings | **1,193** teacher- and student-facing, `dropped_units` INCLUDED |
| Fields | activity_title · teacher_notes · time_bands[].activity · homework · visual_aids · item prompt/task/scaffold/options/stimulus/expected_elements/look_for |
| Exempt | `section_anchor` (registry-verbatim by design) · `section_context` and LO rows (never teacher-facing) |
| Source | textbook PDF **7,687 words / 34 pages**, no empty page; chapter summary JSON 1,987 words, held **separately** |

Two method notes, both of which changed the answer:

- **The summary is NOT the copyright source and is scored apart.** The textbook is the
  protected work; `ch_07_summary.json` is Aruvi's own asset. Merged, the longest "verbatim"
  run reads **45 words**; against the book alone it is **18**. The 45 was the pipeline
  quoting itself.
- **The shared scanner was silently reading no summary at all** and, wrapped naively, saw no
  served plan either. Both fixed; see the tooling note below.

**Detector control:** a 20-word passage lifted from the PDF is detected at 20 words. The
check-2 regexes fire on planted brand / poem / URL strings. A clean result is what a broken
scanner returns, so both were proved before any of it was believed.

---

## Check 1 — no verbatim textbook reproduction beyond short quotation · **PASS**

| Measure (vs the TEXTBOOK) | Value |
|---|---|
| Strings sharing nothing at 8 words | **1,033 of 1,193 (86.6%)** |
| Plan words inside any 8-word shared run | 1,916 of 39,240 — **4.9%** |
| Distinct book 8-grams reached by any plan string | **82 of 7,143 — 1.15% of the chapter** |
| Distinct runs ≥ 12 words | **10** |
| Longest run, any kind | **18 words** |
| Longest run that is PROSE | **16 words** |
| Of the 10, also carried in full by Aruvi's summary | **10 of 10** |

The ten, classified:

| Words | Kind | Run |
|---|---|---|
| 18 | measurement data | `(a) 3 cm, 75°, 7 cm; (b) 6 cm, 25°, 3 cm; (c) 3 cm, 120°, 8 cm` |
| 16 | measurement data | `(a) 1, 100, 100; (b) 3, 6, 9; (c) 1, 1, 5; (d) 5, 10, 12` |
| 16 | **prose** | `circles: (a) touch each other at a point; (b) do not intersect. Frame a complete procedure` |
| 15 | measurement data | `(a) 75°, 5 cm, 75°; (b) 25°, 3 cm, 60°; (c) 120°, 6 cm, 30°` |
| 14 | measurement data | `angles are (a) 36°, 72°; (b) 150°, 15°; (c) 90°, 30°; (d) 75°, 45°` |
| 13 | **prose** | `exist for every combination of two angles and the included side. Find examples` |
| 13 | label + data | `triangle ABC with BC 5 cm, AB 6 cm, CA 5 cm. Construct` |
| 12 | label + data | `triangle TRY with RY 4 cm, TR 7 cm, ∠R 140°. Construct` |
| 12 | **prose** (subset of the 16) | `circles: (a) touch each other at a point; (b) do not intersect` |
| 12 | **prose** | `altitude from the top vertex to the base. Justify why the crease` |

**Five of the ten are measurement data** — the numbers a construction exercise IS. They
survive normalisation as "words" because `3 cm, 75°, 7 cm` becomes six tokens. Facts, not
expression; there is no other way to set the same exercise.

**Four distinct prose runs remain, the longest 16 words**, each a condensation carrying a
locator. Against the book's own sentences they are demonstrably paraphrase, not lifting:

> **Book (p.168):** "Cut out a paper triangle. Fix one of the sides as the base. Fold it in
> such a way that the resulting crease is an altitude from the top vertex to the base.
> Justify why the crease formed should be perpendicular to the base."
>
> **Plan:** "Altitudes Using Paper Folding: cut out a paper triangle, fix one side as the
> base, and fold so the crease is the altitude from the top vertex to the base. Justify why
> the crease is perpendicular to the base."

Verdict: **no reproduction beyond short quotation.** 1.15% of the chapter is reached at all,
nothing exceeds 18 words, nothing prose exceeds 16, and every long string is attributed.

---

## Check 2 — no third-party copyrighted material · **PASS**

| Probe | Hits |
|---|---|
| Brand / trademark (30 Indian and global marks) | **0** |
| Poem · stanza · verse · lyric · excerpt-from · © · rights markers | **0** |
| External image or URL (`http`, `www.`, `<img`, `xlink:href`, `.jpg/.png/.svg`) | **0** |
| `visual_stimulus` values populated | **0** of **114** items across the 13 plans |

Stated plainly rather than as a hollow pass: this chapter is ruler-and-compass geometry.
Its content — cardboard boxes, paper folding, set squares, a spider — is NCERT's own subject
matter used as subject matter, and no poem, lyric or story excerpt is in scope. The F2 risk
class lives in English.

---

## Check 3 — quoted source text is attributed · **PASS**

| | |
|---|---|
| Quoted passages (≥25 chars) in field values | 519 occurrences, **90 distinct** |
| Carrying a locator in the same field | 81 of 90 |
| **Without** a locator | **9** |
| Of those 9, sharing ANY 8-word run with the book | **0** |

The nine are Aruvi's own teacher prompts in the LP's quotation convention — *"State the
angle-sum property in one sentence"*, *"What do you notice about the three numbers in each
row?"* — plus two apostrophe-split regex artefacts. Nothing is presented as a quotation of
the book without naming where it comes from, and **41 of the 90 carry the `....` truncation
marker**, which says on the face of it that text was cut.

The compliant pattern the review's T5 answer depends on holds: **97 distinct strings carry a
book locator** (`Figure it Out Q1, section 7.2 p.159`). A locator points INTO a book the
school already owns and reproduces nothing of it.

---

## F2 — the campaign's sole open finding

F2 is the ENGLISH inline-substitution conduit that carries textbook TASK TEXT verbatim into
served plans. **Mathematics·middle is the nearest thing to it outside English and is still
not it** — and that is worth saying precisely rather than filing another "N/A":

Maths·middle's **Rule 10 mandates an inline quotation** (`book_ref ("description…")`), where
maths·SECONDARY mandates a bare locator. So this stage does have a conduit. What keeps it
clear of F2 is that the text flowing through it is the **summary's condensation**, not the
book's sentences — 1.15% of the chapter reached, 16-word prose ceiling. F2 stays open and
stays owed by S9/S10/S11.

---

## One defect raised — ARV-D-108, and it is a compliance defect, not a copyright one

**Rule 10 caps the inline quotation at 10 words. 75 of 88 band quotations (85%) exceed it.**
Median 18.5 words, maximum 39.

The copyright verdict above is PASS on the evidence. But the rule that GUARANTEES short
quotation is being breached at 85%, and on this chapter it holds only because the summary
paraphrases. Set a chapter whose summary quotes its source more closely and the same 85%
breach lands on the book's own words. **C14 polices the guarantee, not just today's outcome**,
so it is raised here and referred to C3. Severity S3; free to fix (the cap is a repair pass,
not a regeneration).

---

## Tooling note — `genon/copyright_scan.py`, two silent holes, both fixed 2026-08-11

1. **`load_source` globbed only `ch_NN_summary.txt`.** Science and social_sciences carry
   `.txt`; **mathematics, english and the_world_around_us carry `.json` — seven of the eleven
   stages** — so on every one of those the summary contributed zero words and the tool
   reported a confident clean against the PDF alone, saying nothing. Now reads both shapes,
   and a new `--book-only` flag keeps the textbook separable, because merging the protected
   work with Aruvi's own asset is what turned an 18-word run into a 45-word one.
   **S4's C14 verdict is unaffected** — it measured against the PDF, which is the copyright
   source — but its summary dimension was never measured.
2. **`lp_fields` yields nothing on a naively-wrapped served plan.** `serve_plan` already
   returns the saved-plan envelope; wrap it in another `{"result": …}` and `lesson_plan` is
   `None`, so the scan yields zero strings and reports clean. This review now prints a
   per-plan field count and refuses to continue on a zero. Recommended for the shared tool.
