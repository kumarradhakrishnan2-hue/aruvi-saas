# Cowork Session — Competency Mapping (Social Sciences · Secondary Stage)


## What this session does

Reads one or more secondary-stage Social Sciences chapter summaries (Grade
IX / X) and the NCF Curricular Goals document, applies the
subject-specific Competency Mapping Constitution, and writes the competency
mapping JSON for each chapter.

Chapter summaries must already exist before this session runs.
Run `step_1_chapter_summary.md` first if they are absent.

This session uses Cowork's own context. No API call is made.
No scripts from aruvi-scripts/ are invoked.

---

## Run Scope

Specify subject, grade, and chapter scope at the start of the session:

```
Single chapter  : map chapter 3 only
Multiple        : map chapters 1, 4, 8
All chapters    : map all chapters for this subject and grade
```

---

## Paths

All paths are relative to the **aruvi-saas** repo root.

| Item | Path |
|------|------|
| Content root | data/content/ |
| Chapter summaries | data/content/chapters/social_sciences/{grade}/summaries/ch_NN_summary.txt |
| Curricular Goals | data/content/framework/social_sciences/secondary/cg_secondary_social_sciences.txt |
| Constitution | data/content/constitutions/competency_mapping/social_sciences/secondary/mapping_constitution_social_sciences.txt |
| Mapping output (per chapter) | data/content/chapters/social_sciences/{grade}/mappings/ch_NN_mapping.json |

The constitution is stage-agnostic (its header declares both the Middle and
Secondary stages) and is identical to the middle-stage copy; the
secondary-routed path above is the one this session loads.

---

## Step 1 — Load inputs

For each chapter, load ONLY the two inputs Pass 1 is permitted to see:
1. **Resolve `chapter_title` first (mandatory).** Read the first line
   of `ch_NN_summary.txt` — the title is written there as a plain text
   heading. Use that line verbatim as `chapter_title`. Do not infer
   the title from section headers or body content further into the file.
   If the first line is absent or blank, log a warning and halt for
   that chapter.
2. Read `ch_NN_summary.txt` — this is the sole chapter
   content reference. Do not read the chapter PDF.
3. Read the mapping constitution for the subject — the stage-routed
   `social_sciences/secondary/mapping_constitution_social_sciences.txt`.

**Do NOT open the Curricular Goals reference (`cg_secondary_social_sciences.txt`)
here.** Rule 1 requires Pass 1 to be C-code-blind, and a model cannot
reliably ignore C-codes already sitting in its context. The CG reference is
loaded only at the start of Pass 2 (Step 2), after the transformation
inventory is complete.

If `ch_NN_summary.txt` is absent, log a warning and skip that chapter.
Do not attempt to generate the summary here — run
`step_1_chapter_summary.md` first.

---

## Step 2 — Apply the constitution

Apply the subject-specific Competency Mapping Constitution exactly.
The constitution is the governing document — all mapping decisions
must follow its rules without exception. Run Pass 1 (the C-code-blind
transformation inventory) first; only at the start of Pass 2 open the
Curricular Goals reference `cg_secondary_social_sciences.txt` — this is the
first point at which C-codes enter the session. This step produces a
verified in-memory competency list (cg, c_code, weight, justification)
ready for Step 3 to transcribe into JSON. No file is written here.

**Secondary-stage note.** The secondary CG document spans the same four
Social Sciences sub-disciplines as the middle stage — History (CG-1, CG-2,
CG-3), Geography (CG-4), Political Science (CG-5), and Economics (CG-7,
CG-8), with CG-6 (social/cultural life) and CG-9 (India's integrated
contribution) cutting across them. Rule 7's sub-discipline disambiguation —
restricting Weight 3 to the C-codes of the sub-discipline governing the
chapter's primary structural activity — applies unchanged. The CG and
C-code labels themselves differ from the middle stage; always match against
the codes present in `cg_secondary_social_sciences.txt`, never carry over
middle-stage codes from memory.

**Prohibited documents for all subjects:**
Learning Outcomes, Pedagogy documents, Syllabus documents, Assessment
Framework documents, Position Papers — constitutionally excluded.

---

## Step 3 — Write the mapping JSON

Write one JSON record per chapter to:
`data/content/chapters/social_sciences/{grade}/mappings/ch_NN_mapping.json`

**Field sourcing rules — every field must be derived as specified below:**

| Field | Source | Rule |
|-------|--------|------|
| `stage` | Run scope declared at session start | Map grade to stage: III–V → `"foundational"`, VI–VIII → `"middle"`, IX–X → `"secondary"` |
| `subject` | Folder path | The `{subject}` segment of `data/content/chapters/{subject}/{grade}/summaries/` |
| `grade` | Folder path | The `{grade}` segment of `data/content/chapters/{subject}/{grade}/summaries/` |
| `chapter_number` | Summary filename | Parse `NN` from `ch_NN_summary.txt`; strip leading zero; write as integer |
| `chapter_title` | First line of `ch_NN_summary.txt` | Read the title heading from the top of the summary file; used verbatim |
| `summary_path` | Constructed | `data/content/chapters/{subject}/{grade}/summaries/ch_NN_summary.txt` using derived values |
| `cg` | Step 2 output | Transcribe verbatim from the competency list produced in Step 2 |
| `c_code` | Step 2 output | Transcribe verbatim from the competency list produced in Step 2 |
| `weight` | Step 2 output | Transcribe verbatim from the competency list produced in Step 2 |
| `justification` | Step 2 output | Transcribe verbatim from the competency list produced in Step 2 |
| `chapter_weight` | Calculated | Sum of all `weight` values across all entries |

**Post-write verification (mandatory):**
After writing the JSON file, read it back and confirm:
1. Every `cg`, `c_code`, `weight`, and `justification` in the file exactly matches the competency list produced in Step 2.
2. `chapter_title` matches the first line of `ch_NN_summary.txt`.
3. `chapter_weight` equals the sum of all weight values.

If any discrepancy is found, overwrite the file with the correct values before proceeding to the next chapter.

---

## Step 4 — Print verification summary

After each chapter, print one confirmation line:

```
ch_03 | Nazism and the Rise of Hitler | primary: C-2.4 (W3), C-2.5 (W2) | chapter_weight: 8
```

If any chapter summary was missing, list all skipped chapters at the end.

---

## Constraints

- Do not read chapter PDFs. The chapter summary is the sole content input.
- Do not consult Learning Outcomes, Pedagogy, Syllabus, Assessment
  Framework, or Position Papers — constitutionally prohibited.
- Do not call the Claude API. Cowork reads all inputs directly.
- Do not invoke any scripts from aruvi-scripts/.
- Process chapters in the order specified.
- All files written in UTF-8 encoding.
- If a mapping file already exists for a chapter, overwrite it.
