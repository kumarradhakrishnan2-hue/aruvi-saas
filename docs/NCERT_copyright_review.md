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
backup, PDFs local forever — **one finding remains open: F2**, the English inline
task-text substitution that can carry verbatim textbook text into a served (and eventually
cloud-hosted) canonical. It is closable by an authoring change already within the pipeline's
normal way of working, or by licence. Written permission from NCERT remains the decisive
mitigation and should be pursued independently of the fix.
