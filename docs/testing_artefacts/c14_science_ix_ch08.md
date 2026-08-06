# C14 — Copyright review · science · secondary (IX) · ch 8

**Library** {12, 10, 7} · **engine** e16 · **Run** 2026-08-06
**Reference:** `docs/NCERT_copyright_review.md` v1.1 (F1 closed by founder ruling; **F2** —
English verbatim task-text — the sole open finding) ·
**Source of truth:** `textbooks/science/ix/chapter 08 - Journey Inside the Atom.pdf`
**New tool:** `genon/copyright_scan.py` (v1.0, written for this step)

**Verdict: PASS on all three checks. Zero unattributed quotations, zero wholesale
reproductions, no defect filed.** Surfaces covered: all 3 library canonicals, all 22 served
plans, `result.dropped_units`, and the 8 exported files from C12 — i.e. every teacher-facing
surface the step names.

> *Standing caveat, carried from the review: this is an informed compliance check, not legal
> advice. Before commercial launch it should be read by Indian IP counsel.*

---

## 14.0 · The step got a tool, because it was the step's own recommendation

`NCERT_copyright_review.md` §6.4 asks for exactly this: *"add a scan that n-gram matches
served-plan text against the summary verbatim fields and the chapter summary itself, surfacing
long matches for judgment. C14's manual spot-check then audits the gate rather than being the
gate — the same maturation C7 went through."*

Until now C14 was a human reading a 12-unit plan beside a 30-page PDF and hoping to notice.
`genon/copyright_scan.py` shingles the source into 8-word windows, slides the same window over
every teacher-facing string, and reports **maximal runs of consecutive matching windows** —
so a hit is reported as *"N consecutive words appear verbatim in the source"*, sorted longest
first. Length is the whole question: a 6-word collision is the English language, a 40-word
collision is a lifted passage.

It exempts `section_anchor` (registry-verbatim by design, §5 of the review) and the internal
`section_context`/LO rows. It cannot see paraphrase — the same blind spot `register_scan.py`
documents. The scanner carries the floor; the judgement below sits on top of it.

**A bug the tool found in itself, worth recording.** The first run reported **3 769
"visual_aid" fields** on three canonicals. `visual_aids` is a **string** on science·secondary
and a **list** elsewhere, so iterating it yielded *characters* — 3 769 one-letter fields, every
one scanning clean. That is precisely the silent-miss failure `register_scan.py`'s docstring
warns about ("a plan reporting 0 bans AND 0 band fields has not been scanned, it has been
skipped"). Fixed by normalising the shape before iterating; the review below is post-fix, and
the visual aids are read in §14.2.

## 14.1 · Check 1 — no verbatim textbook reproduction — PASS

**The decisive separation: textbook vs. summary.** The naive scan (both sources pooled) reports
7 distinct runs ≥12 words across the library. Scanned separately, **6 of the 7 match only the
chapter summary** — Aruvi's own derived artefact, which is *given to the generator as input*.
Matching it is the pipeline working, not reproduction. Only one run touches the textbook.

| Run | Words | Where | Matches |
|---|---|---|---|
| "nucleus is about 10 times smaller than the atom, comparable to a pepper grain at the centre of a cricket ground" | 21 | TOP u4 band1 | **summary only** |
| "whether Rutherford's conclusion about nuclear mass concentration is correctly explained by Thomson's model…" | 20 | TOP u4 band4 | **summary only** |
| "finding electrons, protons and neutrons given atomic number and nucleon count…" | 19 | TOP u8 band2 | **summary only** |
| "A as a superscript and Z as a subscript to the left of the…" | 14 | p07 u4 band3 | **summary only** |
| **"atoms of different elements with the same mass number but different atomic numbers"** | **13** | **TOP u11 band4** | **TEXTBOOK** |
| "Cl-35 75% and Cl-37 25% give a simple average of 36 u but…" | 13 | p07 u7 band3 | **summary only** |
| "neutrons are found in the nucleus of all atoms except ordinary hydrogen" | 12 | TOP u6 band2 | **summary only** |

**Textbook-only scan, threshold dropped to 10 words, across all 25 files on disk:
exactly ONE distinct run.** Zero in any assessment field — no stem, stimulus, option, task,
scaffold, expected element or look-for anywhere in the library matches the textbook at 10+
words.

**The one hit, read in context — and it is not reproduction.** It is the **definition of
isobars**, and the two sentences are not even the same sentence:

> **Textbook:** *"You have learnt that the two atoms that have the same atomic number but
> different mass numbers are called isotopes. What if they have the same mass number but
> different atomic numbers? What are such atoms called? Let us find out!"* — a rhetorical
> question opening a section.
>
> **Plan (TOP u11 band4):** *"Introduce isobars: atoms of different elements with the same mass
> number but different atomic numbers. Example: calcium (Z=20), potassium (Z=19), argon (Z=18),
> all with A=40. Students construct a comparison table: isotopes vs. isobars…"* — a
> teacher instruction with its own examples and its own activity.

The shared span is the standard definitional phrase for isobars — 13 words of scientific
definition, where the idea and its expression are effectively merged and no shorter phrasing
exists. Well inside short quotation, and the surrounding activity design is entirely original.
**Not a defect; recorded so the gate sees the exact string rather than a reassurance.**

**The exports add nothing.** Scanned as extracted text, C12's eight files carry the same single
13-word run plus two more — *"8.2.2 Testing Thomson's model: The gold foil experiment"* and
*"8.7 How Are Electrons Distributed in Different Energy Levels?"* Both are **`section_anchor`
values**, which C14 exempts by name. The scanner exempts them at the field level; the exporters
print them as headings, which is why they surface here and not in §14.1's table. Correct on
both sides. **Nothing new enters at the export boundary.**

## 14.2 · Check 2 — no third-party copyrighted material — PASS

**Brand text: zero hits** (scanned for a list of common Indian and global brands).
**Literary material: three apparent hits, all false positives** — every one is the word
"novel" used as an adjective ("a novel element X with Z=17", "three novel elements described
only by their electronic configuration"). No poem, lyric, story excerpt or dialogue anywhere.

**Visual aids — read in full, all 29 of them, and this is the check that matters.** Every one
is an instruction to the teacher to *draw or build* something:

> "Board timeline showing Kanada → Leucippus/Democritus → Dalton with dates and key claims" ·
> "Board diagram of cathode ray tube showing cathode, anode, deflection plates and ray path" ·
> "Board table comparing proton, electron, neutron: symbol, charge, relative mass, location" ·
> "Board concept map scaffold: nodes for philosophical atom → Dalton → Thomson → Rutherford → Bohr"

**Four reference the textbook's own figures, and reference is all they do:** TOP u3 *"Textbook
Figure showing the gold foil experimental setup"*, TOP u9 *"…textbook Fig. 8.11"*, p10 u7
*"Fig. 8.11 reference for H through Ar"*, p07 u2 *"Textbook figure of the gold foil experiment
setup"*. **No image data exists anywhere in any plan** — there is no figure to reproduce, only
a pointer into the book the school already owns. This is the compliant T2 pattern the review
endorses, and it is the same shape as English's `(p.NN)` homework convention.

**Assessment visual stimuli** are pipe-delimited data tables built by the generator — atomic
numbers, mass numbers, natural abundances (Cl-35 at 75%, B-11 at 80.1%, the argon isotopes).
Physical constants and periodic-table facts: not copyrightable expression in any arrangement,
and the arrangements here are the generator's own.

## 14.3 · Check 3 — quoted source text is attributed — PASS, vacuously, and that is the honest answer

**Zero quoted spans of 12+ characters exist anywhere in the three library canonicals** —
searched across every band, teacher note, homework line, stem, option, task, scaffold and
rubric field for straight and curly quote pairs. Nothing is quoted, so nothing is
unattributed. The check passes because the condition never arises, not because attributions
were found and verified — worth stating plainly so a later reader does not mistake this for
evidence that the attribution machinery works.

Related, and clean: this chapter shows **none** of the ARV-D-051 pattern (a trailing
one-cell "— Adapted from …" row inside a pipe payload) that SS·VIII and SS·IX carried.

## 14.4 · F2 — the campaign's one open copyright finding — NOT ENGAGED by this stage

F2 is the **English inline task-substitution conduit**: English served plans can carry textbook
task text verbatim, which is textbook content inside a software package, and it matters because
only canonicals migrate to the cloud.

**Science·secondary has no such conduit, and it is structural, not accidental.** The mechanism
F2 describes lives in `aruvi_core/subjects/english/subject.py` — `_task_lines()` reading
`tasks_in_class[].task_brief`, with `_strip_contamination()` removing `tasks_verbatim` /
`question_bank` from the summary before the prompt is assembled. **Science has no equivalent
path**: no `task_ref`, no substitution step, and its chapter summary carries neither
`tasks_verbatim` nor `question_bank` (checked directly on `ch_08_summary.txt`). There is no
verbatim field for a science plan to substitute *from*.

**F2 remains open campaign-wide and will be decided at English·preparatory / middle /
secondary — the last three stages in the §11 order.** Recorded here as not-engaged, not as
closed.

---

## Review table (the artefact the step asks for)

| # | Check | Surfaces scanned | Result |
|---|---|---|---|
| 1 | No verbatim textbook reproduction beyond short quotation | 3 canonicals · 22 served plans · dropped_units · 8 exports | **PASS** — 1 distinct textbook run in the whole corpus, 13 words, a scientific definition; 0 in any assessment field |
| 2 | No third-party copyrighted material | all bands, notes, homework, stems, options, tasks, 29 visual aids, all visual stimuli | **PASS** — 0 brand hits, 0 literary material, 0 embedded images; 4 figure *references*, which is the compliant pattern |
| 3 | Quoted source text is attributed | every teacher- and student-facing string | **PASS (vacuous)** — 0 quoted spans exist, so 0 unattributed |
| — | F2 (English verbatim conduit) | the science port and the ch 8 summary | **NOT ENGAGED** — no substitution path, no verbatim field to substitute from |

**Subjective calls sent to the human gate, per the step's doctrine — one, with the string
quoted:** whether *"atoms of different elements with the same mass number but different atomic
numbers"* (13 words, TOP u11 band4) reads as short quotation of a definition or as
reproduction. My reading is the former, with the textbook's own sentence quoted beside it in
§14.1 so the founder can judge the same two strings I did.

---

## Status

**C14 PASS.** No defect filed. `genon/copyright_scan.py` is now the deterministic floor and
should be re-run per stage — and, per the review's own recommendation, this manual pass has
become an audit *of* the gate rather than the gate itself.

**Every C-step for science·secondary is now recorded: C1–C14 all pass.** What stands between
this stage and green: the **HUMAN GATE** (the serve-sweep table, C8's worst transition read
aloud, the standard's synthesis unit in full, each compact's own ending, C7's register hits),
plus the browser work owed from C12 §12.5 and the residue clean-ups from C10.5 and C11.
