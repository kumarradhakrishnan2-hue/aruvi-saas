# Cowork Session — Chapter Summary Generation (Social Sciences · Secondary Stage)

## What this session does

Reads one or more secondary-stage Social Sciences chapter PDFs (Grade IX / X)
and writes a grounded chapter summary for each. The summary is the content
reference used by the competency mapping session and by the runtime lesson
plan and assessment generation.

This session uses Cowork's own context to read the PDF and write the
summary. No API call is made.

---

## Run Scope

Specify which chapters to process at the start of the session:

```
Single chapter  : process chapter 3 only
Multiple        : process chapters 1, 4, 8
All chapters    : process all chapters in the textbook folder
```

Tell Cowork the subject, grade, and chapter scope before starting.

---

## Paths

| Item | Path |
|------|------|
| Project root | the **aruvi-saas** repo root |
| Chapter PDFs | textbooks/social_sciences/{grade}/ |
| Summary output | data/content/chapters/social_sciences/{grade}/summaries/ |

Files are named: `Chapter NN - Title.pdf` (match case-insensitively — the
Grade IX folder uses lowercase `chapter NN - Title.pdf`)
Output files are named: `ch_NN_summary.txt`

---

## Step 1 — Locate the PDF

Match chapter number to the correct file in the textbook folder.

---

## Step 2 — Extract chapter title

Read the chapter title exactly as it appears in the PDF (typically on the
opening page of the chapter). Record it verbatim — do not paraphrase or
normalise casing. This title is written as the first line of the output
file in the format:

```
Chapter NN: <Title>
```

followed by a blank line, before the summary text begins.

---

## Step 3 — Identify the scope boundary

Read the full chapter PDF. List, in the order they appear, every heading
that structures the chapter's instructional content. The heading list is the
scope boundary for the summary: no concept, phenomenon, process, person,
event, place, date, source, or example may appear in the summary unless it is
anchored to one of these headings. This rule is absolute — it prevents
content from outside this chapter (e.g. from a neighbouring chapter that
shares vocabulary, or middle-stage background the reader is assumed to
supply) appearing in the summary even if the topic is familiar.

**Two kinds of heading belong in the scope boundary:**

1. **Numbered headings and subsections** — e.g. `3.1`, `3.2`, `3.2.1`.
2. **Named content-blocks** — bold-titled blocks that introduce a distinct
   theme, source study, region, institution, or episode but carry no section
   number. These are part of the instructional spine and MUST be listed and
   covered.

   Distinguish a named content-block (introduces chapter content → include)
   from a pedagogical sidebar box (recurring furniture → never a heading; see
   below).

**Sidebar boxes are never headings.** No box enters the heading list; the
rules below govern only whether a box's task is captured inline (Step 4).

**In-flow boxes — capture inline.** Verified across the Grade IX textbook
(*Exploring Society: India and Beyond*, ch. 3–9), two boxes recur in the flow
of sections, consistently across all four sub-disciplines:
- **THINK ABOUT IT** — a short reflection / discussion prompt.
- **LET'S EXPLORE** — an enquiry / activity box (source reading, map- or
  data-interpretation, find-out task). Capture each inline; capture any other
  in-flow box the same way. (Reconfirm the labels when Grade X is added.)

**Exclude** — end-of-chapter, recap, and furniture: **Questions and
activities** (the numbered end-of-chapter block — questions, map tasks,
projects, and any `Activity:` items within it); **Before we move on...** (a
section recap checkpoint); and pure reference furniture with no task
(glossary, timeline strip, motivational biography sidebar).

**Tables and graphs are content, not boxes.** Economics (supply–demand
schedules) and Geography (climate graphs) chapters are figure-dense — cover
what a table or graph shows in its section's content sentences, and add an
inline activity sentence only if a box asks the student to work on it.

---

## Step 4 — Write the summary

Write the summary addressing every heading identified in Step 3 — both
numbered headings and named content-blocks — in the order they appear.

For each heading or named content-block write 2–4 sentences covering:
- What the section teaches
- The key concepts, terms, places, events, dates, or sources it introduces
- Any significant processes, source extracts, case studies, maps, or examples
  it uses
- Whether the section contains a numbered student `Activity` — note existence
  only, do not elaborate its steps

**Inline activity capture.** After a section carrying a captured in-flow box
(Step 3), append ONE sentence recording its task, prefixed with the box name —
e.g. "(LET'S EXPLORE) Students compare Palaeolithic and Neolithic tool kits
from the figure and infer what each says about daily life." Record the task,
not the procedure. These sentences are exempt from the word-count guide, do
not become headings, and are additional to the section's own 2–4 sentences.

**Length is content-driven, not capped.** Give every heading and named
content-block its 2–4 sentences; do not compress several themes or source
studies into a single clause to hit a word target, and do not pad to reach
one. Grade IX chapters are dense: a typical chapter lands at roughly
**1600–2500 words**. Compact chapters (the economics and the opening
*Understanding Social Science* chapters) may sit near 1300–1600, and the
densest history chapters (*Early Humans and Beginning of Civilisation*,
*State and Society up to 1000 CE*) may run to ~3000. These figures are
anchors derived from the summary-to-chapter ratio of the same textbook
series, not caps — coverage of every unit takes precedence over any word
figure.

**Rules:**
- Use the textbook's own headings and named content-blocks as the organising
  structure. Do not rename, merge, or reorder them. Inline activity sentences
  attach to their section but never become headings.
- Where the chapter spans more than one Social Sciences sub-discipline
  (History, Geography, Political Science, Economics), let the headings fall in
  the textbook's own order; do not regroup them by discipline.
- Do not describe end-of-chapter exercises, end-of-chapter questions, or
  standalone projects — these remain excluded from inline activity capture too
  (per Step 3).
- Do not introduce content from outside this chapter. If you find yourself
  writing about something the chapter does not cover, stop and delete it.
- Write in plain prose. No bullet points. No tables.
- Output summary text only. No preamble. No word count statement.

---

## Step 5 — Save the output

Save to: `data/content/chapters/social_sciences/{grade}/summaries/ch_NN_summary.txt`
(relative to the aruvi-saas repo root)
(NN = zero-padded chapter number, e.g. `ch_03_summary.txt`)

---

## Step 6 — Verification

After writing each summary, print one line to confirm:

```
ch_04_summary.txt — written — "Early Humans and Beginning of Civilisation" — 2480 words — units: 4.1, 4.2, 4.2.1, 4.3, 4.4 — inline activities: 3 (4.2, 4.3, 4.4)
```

List both numbered headings and named content-blocks under `units:`. Report
the count of inline activity boxes captured and the sections they attach to
under `inline activities:` (or `inline activities: 0` if the chapter has
none). If any chapter PDF is not found, log a warning and skip — do not halt.

---

## Constraints

- Do not call the Claude API. Cowork reads the PDF directly.
- Do not generate competency mappings or weights.
- Do not modify any existing mapping JSON.
- Process chapters in the order specified.
- All files written in UTF-8 encoding.
- If a summary file already exists for a chapter, overwrite it.
