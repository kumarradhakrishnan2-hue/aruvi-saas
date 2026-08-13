# Formal Review — Aruvi vs the NCERT Copyright Statement

VERSION 1.1 · 2026-08-04 · Prepared by Claude at the founder's request. This is the
campaign-level reference for the per-stage **C14 copyrights review** (`docs/testing.md` §4,
template 2.4).

*1.1 (2026-08-04, founder rulings on the 1.0 findings): (a) **only the canonicals go to the
cloud** — summaries, mappings and the PDFs never migrate; (b) the **GitHub remote is a
personal private backup**, not distribution; (c) the **textbook PDFs remain on the local
hard disk permanently**. F1 is CLOSED on these terms (conditions recorded at §3-T3/T4);
**F2 is the sole open finding**, and it matters precisely because canonicals are what
reaches the cloud.*

> **Standing caveat.** This is an informed compliance review, not legal advice — Claude is
> not a lawyer, and the Indian Copyright Act, 1957 references below are informational.
> Before commercial launch (Razorpay milestone, roadmap §9), this review should be read by
> Indian IP counsel.

---

## 1. The instrument under review

The NCERT copyright and terms-of-use statement, quoted in its operative clauses:

| # | Clause (paraphrased minimally) | Character |
|---|---|---|
| T1 | The NCERT textbooks are copyrighted. | Assertion of right |
| T2 | Copies "may be downloaded and used as textbooks or for reference." | **Permission** |
| T3 | "Republication … by any other individual or agency is strictly prohibited." | Prohibition |
| T4 | "No agency or individual may make electronic or print copies of these books and redistribute them in any form whatsoever." | Prohibition |
| T5 | "Use of these online books as a part of digital content packages or software is also strictly prohibited." | Prohibition |
| T6 | "No website or online service is permitted to host these online textbooks." | Prohibition |
| T7 | "Links may however be provided with written permission from the NCERT." | Conditional permission |
| T8 | Watermarked copies must not be bought or sold; infringement should be reported. | Anti-piracy |

Statutory backdrop (informational): under the Copyright Act, 1957, NCERT's exclusive rights
(s.14) include reproduction, adaptation and abridgment. The fair-dealing exceptions (s.52)
most relevant to this domain — private/personal use including research (s.52(1)(a)) and
reproduction "by a teacher or a pupil in the course of instruction" (s.52(1)(i)) — attach to
the *teacher's* use, not to a commercial SaaS that prepares and distributes material. Aruvi
should therefore assume it **cannot lean on fair dealing** for anything it stores, generates
or serves, and must instead be clean on its own conduct.

---

## 2. What Aruvi actually does with NCERT material (verified on the repository, 2026-08-04)

**A. Downloaded textbook PDFs — `textbooks/{subject}/{grade}/` (~1.5 GB).** Authoring-time
reference for the `chapter` skill only. Verified: excluded from git (`.gitignore` `/textbooks/`,
"Authoring source only; do NOT commit"); no API route reads or serves them; they are not part
of `data/content/` and are not scheduled for the cloud migration (CLOUD_DATA_MODEL Bucket A).

**B. Chapter summaries and competency mappings — `data/content/chapters/…` (330 chapters).**
Derived analytical works authored by the chapter pipeline. Two distinct sub-classes on
inspection:
- **Paraphrase-class** (verified sample: SS·IX ch 3 summary) — descriptive prose in Aruvi's
  own words, referencing figures/tables by number ("Fig. 3.2", "Table 3.1") without
  reproducing them.
- **Verbatim-class fields (English)** — the English summary schema deliberately captures
  textbook text: `tasks_verbatim[].task_text`, `dialogue_text`, and picture-story dialogue
  (verified sample: english/iii ch 1, which carries the full duck-and-hen dialogue verbatim).
- These files are **git-tracked and pushed to a GitHub remote** (the 2026-07 backup decision:
  "everything under data/ … is now TRACKED so GitHub Desktop backs it up").

**C. Generated canonicals and served plans — `data/content/saved_plans/`, the serve engine.**
Original pedagogical works generated from the summaries + constitutions. The design intent is
to *reference into* the teacher's own copy of the textbook (English homework `(p.NN)`
convention, maths `book_ref`, task refs) rather than reproduce it. One known verbatim conduit:
English's **inline task-ref substitution into phase text** (CLAUDE.md §3, standard-LP rule f)
can carry `tasks_verbatim` text into a served plan.

**D. The SaaS surface.** No route hosts, links to, or exports a textbook or any part of one.
Plans and assessments presuppose the teacher and class hold the physical textbook — Aruvi is
a companion to the book, not a substitute for it.

---

## 3. Clause-by-clause findings

**T2 (download and reference use) — COMPLIANT.** Holding the PDFs locally as the authoring
reference is squarely the permitted use. The permission is personal to the holder; it does not
extend to passing copies onward, which is why the git exclusion in finding A matters.

**T3/T4 (republication, copying + redistribution) — COMPLIANT; F1 closed by founder ruling.** The PDFs are never redistributed. However, pushing `data/content/chapters/`
to GitHub is *making an electronic copy and transmitting it to a third-party host*. For the
paraphrase-class summaries this is Aruvi's own expression and NCERT's rights are not engaged
beyond the ideas (which copyright does not protect). For the **verbatim-class English fields**
the question was repo visibility. **Finding F1 — CLOSED by founder ruling (v1.1): the GitHub
remote is a personal private backup, an extension of the permitted T2 reference use, not
redistribution.** Two conditions attach to the closure and are the standing rule: (1) the
repository stays **private** — making it public, or opening access beyond the founder's own
working set, re-opens F1 as a live T4 breach; (2) `/textbooks/` stays git-excluded (already
enforced in `.gitignore`).

**T5 (books inside digital content packages or software) — THE GOVERNING CLAUSE for the
product, currently defensible, with the same English caveat.** Aruvi's answer to T5 must be:
*no textbook content is embedded in the product; the product carries original plans that
point into a book the school already owns.* The paraphrase-class pipeline and the
`(p.NN)`-reference convention support that answer. The English inline-substitution conduit
(finding C) cuts against it: any served plan carrying a textbook task or dialogue verbatim is
textbook content inside a software package. **Finding F2: the verbatim conduit must be
either closed (substitute a paraphrase + page ref) or licensed (§4.1) before English plans
are served commercially.** This is exactly what C14 check 1 exists to police per stage.

> ### ★ F2 MEASURED FOR THE FIRST TIME — S10 · english·middle · VI ch 8 (2026-08-13)
>
> F2 has been asserted since 2026-08-04 and never quantified: no English library existed to
> measure. This is the first one, and it was chosen to be the hardest case available — a POEM
> chapter (*What a Bird Thought*) whose summary carries the NCERT poem in full, 17 verbatim
> lines, plus an 8-line listening transcript.
>
> **Measured against the textbook itself** (`textbooks/english/vi/Chapter 03 - Nurturing
> Nature.pdf`, 5,373 words, shingled at n=8) across all 8 files — 3 canonicals and 5 served
> plans, **19,355 teacher-facing words**:
>
> | | |
> |---|---|
> | book-matched words (runs ≥ 8) | **317 = 1.64%** |
> | distinct matched strings | 12 |
> | longest run | **14 words** (the poem's closing two lines) |
> | runs in LESSON-PLAN fields | **36** |
> | runs in ASSESSMENT ITEMS | **0** |
> | brands · external images · URLs | 0 · 0 · 0 |
> | task_briefs carrying a (p.NN) locator | **32 of 32 = 100%** |
>
> **The conduit is real, and it is narrower than the finding assumed.** The verbatim task-text
> F2 names does appear — "the bird thought the world was made of straw", "how is a home
> different from a house", the eight-word describing-words bank from p.90 — but every instance
> is **8–10 words, in the lesson plan only, quoted, and carrying a page locator**. None is a
> dialogue or a passage. And the assessment, which is the half that would be hardest to defend
> as reference rather than reproduction, carries **not one 8-word sequence of the book**: the
> constitutional firewall (the generator is forbidden to read `tasks_verbatim[]` /
> `question_bank[]`) holds against the book itself, not merely against the exercise wording.
>
> **Why the fragments cannot simply be removed.** LP Rule 9 mandates that each task be named by
> its anchor plus a brief, and Rule 3 draws tasks from the summary's `tasks_verbatim`. A plan
> that contained none of these strings could not tell a teacher which task to run. So the
> remedy F2 proposes — "substitute a paraphrase + page ref" — is already what the plan does
> everywhere except at the point where naming the task IS the instruction. The residual is the
> irreducible part.
>
> **Founder rulings folded in (2026-08-13, at S10's C3).** A short lift inside quotation marks
> that frames a question is reference, not reproduction — "reading that line will mean nothing
> if the overall poem is not seen" — and applies equally to the poem (12–18% of it appears
> across the three canonicals) and to the listening transcript (25–27%, higher only because the
> transcript is 8 lines long). No constitution was amended: the model already draws the line
> where it should, and looser prose would give it room to drift.
>
> **Benchmark:** maths·middle's C14 (2026-08-10) read **1.15%** of its chapter with a longest
> run of **18 words**. English·middle reaches slightly more in aggregate and lifts a shorter
> longest string — so the English conduit, measured, is not worse than a subject with no F2
> finding against it.
>
> **TWO THINGS THIS MEASUREMENT DEPENDS ON, both recorded so the number is not over-trusted.**
>
> 1. **`genon/copyright_scan.py` cannot find the book for ANY English chapter.** Its PDF
>    resolver globs `chapter\s*0*{ch}` and assumes the plan's chapter number is the PDF's.
>    The English split breaks that everywhere: VI/VII/VIII PDFs are named per UNIT
>    ("Chapter 03 - Nurturing Nature.pdf" contains chapters 7, 8 and 9) and IX keeps the
>    original section numbering ("chapter 04 - Vitamin-M.pdf" is chapter 7). So on all **101
>    English chapters** the glob matches nothing, the book contributes ZERO words, and the scan
>    reports a confident result **against Aruvi's own summary** — which can only ever show the
>    pipeline quoting itself. Same class of silent hole as the `.txt`-only summary loader fixed
>    at S7, on the opposite input. **S11's C14 was run under it too**, which is why its poem
>    finding (ARV-D-138) came from reading rather than from the scanner. The mapping the
>    resolver needs already exists in every split summary: `_source_unit.unit_chapter_number`.
>    The figures above were obtained by pointing at the correct PDF by hand.
> 2. **An 8-gram scan is blind to a compliant poem incipit by construction.** Assessment Rule 3
>    caps the incipit at EIGHT words, and this poem's lines run 4–7, so a correctly-cited line
>    can never form an 8-word run. The scanner found zero poem lines in assessment items;
>    reading found three. The scanner catches wholesale lifting; **only reading catches the poem
>    rule.** C14 on a poem chapter cannot be automated away.
>
> **Status: F2 stays OPEN, now with a number against it.** What the measurement changes is the
> question — no longer "is there a conduit" (there is, bounded and locator-bearing) but "is an
> 8–10 word task reference, in the lesson plan, with a page number, reproduction or citation".
> That is a licensing judgement, not an engineering one, and it belongs at §4.1.

**T6 (hosting online textbooks) — COMPLIANT.** Nothing is hosted, and the migration boundary
is now ruled (v1.1): **only the canonicals go to the cloud** — summaries, mappings and the
PDFs never enter any served bucket; the PDFs remain on the local hard disk permanently.

**T7 (links require written permission) — COMPLIANT BY ABSENCE; a standing rule follows.**
Aruvi currently links to nothing. Note the clause is stricter than general web practice:
even *linking* to the online textbooks requires NCERT's written permission. **Rule: no
deep-links to NCERT-hosted textbook files anywhere in the product without written
permission** — page references in prose remain fine (a page number is a fact, not a link).

**T8 (watermarked copies, piracy) — NOT ENGAGED.** Aruvi neither buys nor sells copies. The
downloaded PDFs' watermarks are irrelevant to reference use.

**Section titles and structure.** `section_anchor` values are drawn verbatim from section
headings by design (V2, the registry). Titles and tables of contents are generally below the
originality threshold for protection, and their use as structural references (not reproduced
content) is the weakest possible engagement with NCERT's rights. **No action; the C14
exemption for registry anchors stands.**

---

## 4. Recommendations, in order of force

1. **Seek written permission from NCERT before commercial launch** (dceta.ncert@nic.in).
   The statement itself invites participation in the "Education for All mission," and Aruvi's
   posture — driving teachers *into* the prescribed textbook rather than away from it — is the
   strongest possible footing for that letter. A permission covering (a) reference use of the
   PDFs in authoring, (b) the derived-summary pipeline, and (c) page-referencing in served
   plans converts every residual risk below into a licensed activity. This is the single
   highest-value action and should precede the Razorpay milestone.
2. **F1 closed (v1.1)** — the GitHub remote is a personal private backup. Standing
   conditions: the repository stays private, and `/textbooks/` stays git-excluded. No
   further action unless access ever widens.
3. **Close finding F2 — the sole open finding, and the one the cloud boundary makes
   decisive** (only canonicals migrate, so a verbatim-carrying English canonical is exactly
   what would end up served from the cloud): amend the English canonical-authoring path so served plans carry a
   paraphrase and a `(p.NN)` pointer instead of substituted verbatim task text — or gate
   English serving on the §4.1 permission. Until closed, C14 check 1 must treat any verbatim
   task text in a served English plan as a defect, not an advisory.
4. **Mechanize what C14 samples:** add a scan (the `register_scan.py` pattern) that n-gram
   matches served-plan text against the summary verbatim fields and the chapter summary
   itself, surfacing long matches for judgment. C14's manual spot-check then audits the
   gate rather than being the gate — the same maturation C7 went through.
5. **Standing rules to carry into CLOUD_DATA_MODEL and the migration checklist (now founder
   rulings, v1.1):** only the canonicals migrate to the cloud; summaries and mappings stay in
   the private backup; the PDFs never leave the founder's local disk; no NCERT deep-links
   without written permission; exports never embed textbook imagery (figures are referenced
   by number, never reproduced).
6. **Record in the tracker:** this review files as a campaign-level item; F2 files as a
   defect (suggested severity S2 — a served verbatim plan is a compliance breach the founder
   must accept or fix; owner: founder). F1 is recorded closed with its conditions.

---

## 5. Summary verdict

Aruvi's architecture is fundamentally on the right side of the NCERT statement: the permitted
act (download for reference) is the only act performed on the books themselves, and the
product's value is original pedagogical work that *requires* the class to own the textbook.
With the v1.1 founder rulings — canonicals-only to the cloud, GitHub as private personal
backup, PDFs local forever — **one finding remains open: F2** (first MEASURED 2026-08-13 at
S10 · english·middle: 1.64% of teacher-facing text matches the book, longest run 14 words,
**zero** in assessment items, 100% of task briefs carrying a page locator — see the boxed note
at §3-T5), the English inline
task-text substitution that can carry verbatim textbook text into a served (and eventually
cloud-hosted) canonical. It is closable by an authoring change already within the pipeline's
normal way of working, or by licence. Written permission from NCERT remains the decisive
mitigation and should be pursued independently of the fix.
