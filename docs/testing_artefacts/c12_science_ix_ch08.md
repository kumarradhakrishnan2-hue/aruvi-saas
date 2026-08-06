# C12 — The online view and the exports · science · secondary (IX) · ch 8

**Library** {12, 10, 7} · **floor** 7 · **authored 50 min** · **engine e16**
**Run** 2026-08-06 · **Runbook** `docs/testing_artefacts/c12_runbook_science_ix_ch08.sh` ·
**Files** `docs/testing_artefacts/c12_exports/`

**Verdict: PASS on every exit condition except one — the coverage note, which is
ARV-D-039 re-confirmed, not a new finding.** 15 export files produced and inspected as
extracted text; the view checked field by field; the bookmark half of the writable marks
tested against the live API. The chapter-notes half is localStorage-only and stays Kumar's to
run in a browser — §12.5 says exactly what to do.

**Two plans under test, and they are not interchangeable:**

| Role | File | Why this one |
|---|---|---|
| below-floor | `ch_08_50m6_e16_c20260806101157.json` | the only plan with `dropped_units` |
| mixed + borrow | `ch_08_60m4-50m7_e16_c20260806100029.json` | mixed durations **and** a borrowed sitting |

Not `60m3-45m9` (the C11 timing matrix): its total is 12, the top's own count, so it borrows
nothing. Same trap C6 recorded when its first mixed matrix came to 10.

---

## 12.1 · The view — `dropped_lp` — PASS

`GET /plans/science/ix/ch_08_50m6_e16_c…101157.json/view` → **HTTP 200**, and
`view.dropped_lp` is present with **the identical top-level shape** as `view.lesson_plan`
(`subject · grade · chapter_number · chapter_title · total_periods · groups · meta`) — it went
through the same subject adapter, which is what "adapter-shaped" means and what makes it
render with the served units' own layout.

| | served `lesson_plan` | `dropped_lp` |
|---|---|---|
| units | 6 (numbered **1–6**) | 1 (numbered **7**) |
| groups | 6 section-anchored, flat | 1 |
| last / only anchor | 8.8 Combining Capacity of an Atom: Valency | **8.9 A Deeper Look into Atomic Structure** |
| phases on the unit | 4 each | **5** — a whole unit, not a stub |

`view.dropped_sections` = `["8.9 A Deeper Look into Atomic Structure"]`, exactly the one
uncovered section and nothing else. The dropped unit is numbered **after** the served six, so
it pages last by construction.

`LessonView.jsx` honours it: `droppedUnits` are appended after `units`, the pager reads
**"Dropped n / N"** instead of "Unit n / N", the last served unit's forward button becomes
**"Dropped sections →"**, and back from the first dropped unit returns to unit 6. They are
never counted in pointer or completion arithmetic. Code-verified; the visual pass is Kumar's.

This is the science·ix **section-anchored flat** shape (§3d), and the "Stage None" phantom is
absent — no group carries a null label.

## 12.2 · The eight exports — PASS

All eight required files returned **HTTP 200** and open cleanly. Seven more were produced for
the checks that need a contrast:

| File | pdf | docx |
|---|---|---|
| mixed · lesson | 114 KB / 7 pp | 49 KB |
| mixed · assessment (`answers=1`) | 109 KB / 6 pp | 46 KB |
| mixed · integrated (`answers=1`) | 145 KB / 12 pp | 56 KB |
| allocation report (science · IX) | 106 KB / 6 pp | 46 KB |
| *(extra)* mixed · assessment `answers=0` | 98 KB | — |
| *(extra)* below-floor · lesson / assessment / integrated | 100 / 96 / 116 KB | 44 / 42 / 48 KB |

**Structure — PASS.** All **11 section anchors** of the mixed plan appear in all six of its
files. Zero JSON-ish leakage in any file (scanned for `{"`, `[{`, `":[`, bare `None`/`null`).
Zero triple-blank runs in the PDFs. 55 band markers (`"8 min"`, `"12 min"` …) in the lesson
PDF — the timed spine is rendering, not just unit headers.

**Mixed durations survive — PASS.** Both `60 min` and `50 min` print, matching
`duration_sequence [50, 60, 50, 50, 60, 50, 50, 60, 50, 60, 50]`, and each unit header
carries its own figure.

**The borrowed sitting reads as a whole unit — PASS.** Sitting 11 prints with its section
header (`Section 10 · 8.9 A Deeper Look into Atomic Structure`), its title (*Isotopes,
Isobars, and Weighted Average Atomic Mass*), `Period 11 · 50 min`, its **Materials** line, its
full multi-sentence **Teacher notes**, its four bands and its own homework. Nothing about it
reads as grafted on.

**The answer layer — PASS, and the contrast is clean.** In `answers=1` the correct MCQ option
carries a **✓** and the paper adds `Expected elements` (×5), `Look for` (×2) and `Answer`
(×12). In `answers=0` the *identical* question block prints the same stem and the same four
options **with no tick and none of those markers** — count zero for every one. The class-facing
paper gives nothing away.

**The allocation report — PASS.** Header reads `13 chapters · 245 periods · 204h 10min ·
245×50min`, the executive summary explains the effort index in teacher language, all 13
chapters are named. No leakage.

**The e09 split — the dropped unit reaches NO export — PASS.** This is the clause the mixed
plan cannot test (it has no drops), so it was run on the below-floor plan's six files:

| File | dropped anchor `8.9 …` | dropped title *Isotopes, Isobars* |
|---|---|---|
| below · lesson pdf / docx | absent | absent |
| below · assessment pdf / docx | absent | absent |
| below · integrated pdf / docx | absent | absent |

Six for six. Her printed artefact is the plan she was served.

## 12.3 · The one exit condition NOT met — ARV-D-039, re-confirmed

**The coverage note reaches no export and no view field.** On the below-floor plan the note
exists and is well written:

> *"Time budget short of the chapter's full span: 8.9 A Deeper Look into Atomic Structure could
> not be scheduled — the material is included for you to share as guided self-study or
> homework."*

It is in the saved plan as `result.section_coverage_note`. It is in **none** of the six
below-floor exports (searched for `could not be scheduled`: zero hits in all six). It is not
in the view response either — `GET …/view` returns `dropped_sections` (a bare list of names,
no sentence, no explanation) and nothing else.

Traced to source: `_plan_view_bundle` (`api/main.py:1109`) never passes the note to any
exporter, and **no exporter references `section_coverage_note` at all** — `grep` across
`aruvi_core/export_*.py` and `render/html.py` returns nothing. The only place the sentence
surfaces is the `POST /genon/…/plan` response, read by `PrepareLesson.jsx:322` and
`FirstRun.jsx:435` — i.e. **at the moment she prepares, once.** Reopen the plan tomorrow and
it is gone; print it and it was never there.

So the printed below-floor plan is a **silent partial**: six units, no mention that a section
was left out, no hint that the material exists for self-study. Exports rightly omit the
dropped unit (§12.2) — but with the note omitted too, the omission is undisclosed.

**This is ARV-D-039 (S2), opened at SS·secondary C12 on 2026-08-04, reproducing identically
on a second stage and a different subject.** It is in shared API code, so it is campaign-wide,
not a science defect.

**A register gap found while checking it, worth its own line.** ARV-D-039 is described in the
SS·secondary C12 comment but **has no row in `defects[]`** — nor do **038** or **040**. A
defect that lives only in a step comment does not appear in the tracker's defect view and
cannot be tracked to closure; ARV-D-039 has now been written in properly, carrying its
original opening date. 038 and 040 are unrecoverable from here and are flagged for the
founder: if they were real, they are currently invisible.

## 12.4 · The bookmark — server round-trip, isolation, replacement — PASS

Tested against the live API on kumar1's real section key `science_ix_9A`.

| Step | Result |
|---|---|
| `POST /section-state` bookmark unit 3 / phase 2 | **200** |
| `GET /section-state` [kumar1] | `bookmark_unit=3, bookmark_phase=2` — **round-trips to the server** |
| move it: `POST` unit 5 / phase 0 | **200**; `GET` reads `5 / 0`, **still one row** — replaces, never accumulates |
| `GET /section-state` [kumar2] | only `social_sciences_ix_9C`; **no trace** of kumar1's section or bookmark |
| on-disk | three separate files — `data/section_state/{kumar1,kumar2,kumar3}/…/state.json` |
| `POST` with the bookmark fields omitted | **200**, row keeps `unit_index` and reads `bookmark_unit=None` |

That last row is the one to read carefully: the server storing `None` is correct, and the
protection lives client-side. `sectionState.js:159–167` only writes the local cache when
`st.bookmark_unit != null && st.bookmark_phase != null`, so **a server row with no bookmark
does not wipe a locally-held one** — the only legitimate clear is unbind/bind, which deletes
the whole row. Code-verified, exactly as the step words it.

Two gotchas for whoever repeats this, both of which failed the first run: the section key is
`{subject}_{grade}_{section}` with **underscores** (`science_ix_9A`), and `chapter` on
`SectionStateRequest` is a **string carrying the plan FILENAME** — posting the chapter number
as an int is a 422.

**kumar1's pre-C12 row was captured and restored** after the test
(`ch_08_canonical.json`, unit 1, bookmark 1/2, `updated_at 10:55:27`) — this step moved her
bookmark and put it back.

## 12.5 · Chapter notes — key audit done; the browser pass is owed to Kumar

The notes are localStorage-only, so the behavioural half cannot be run from here. What **can**
be settled statically is settled, and it is the part that would be an S2:

- **Per-user scoping — correct.** `LessonView.jsx:1336` builds
  `userKey("chapter_notes_" + subject + "_" + grade + "_" + chapter_title)`, and
  `format.js:46` appends `_{user}`. A bare `chapter_notes_…` key with no user suffix would be
  the S2; there isn't one.
- **Asset-keyed, section- and matrix-independent — correct by construction.** The key contains
  subject · grade · **chapter title** and nothing else — no section, no matrix, no filename. A
  `50m10` serve and a `60m4-50m6` serve of ch 8 therefore *cannot* key differently. One
  notebook per chapter, structurally.
- **Blank removes the key — correct.** `LessonView.jsx:1346–47`: `setItem` when
  `t.trim()` is truthy, `removeItem` otherwise. No empty strings stored.

**Owed to Kumar, in a browser, as kumar1 then kumar2 on the same profile:** (a) write a note
from the served plan, close, reopen — it comes back and the tab shows the has-note state;
(b) confirm the same note appears in the My Lessons preview, in tracking, and under **every**
section bound to ch 8 (a note visible under only one of two bound sections is a defect);
(c) sign in as kumar2 — the notebook is **empty** and kumar1's key is still on disk untouched;
(d) reload and restart — it survives, but **does not follow her to another device**, because
there is no notes endpoint.

**(d) is X1.7 and is re-recorded here, not assumed fixed: chapter notes are still
browser-local at science·secondary.** Unlike the bookmark, which round-trips to the server
(§12.4), a teacher who writes chapter notes on the staffroom PC will not see them on her
phone. Known limitation, not a tenancy defect.

---

## Status

**C12 PASS**, with the single exit condition it cannot meet re-filed rather than re-discovered:
the coverage note (ARV-D-039, S2, campaign-wide, now properly in the register). Owed: Kumar's
visual pass on the view and the eight files, and the four chapter-notes checks in §12.5.
Remaining in the stage: **C13** (failure paths — three of its four are runnable from here),
**C14** (copyright review), then the gate.
