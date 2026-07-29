# Aruvi SaaS — Test Campaign Plan (the 25-combo certification sweep)

VERSION 1.0 · 2026-07-29 · Actors: **[Kumar]** (runs the product, supplies artefacts) ·
**[Claude]** (inspects artefacts, checks compliance, reports)

This is a working template. The numbered per-combo cycle in §4 is executed once per
subject·class combination — 25 times. Results are recorded in the campaign tracker
(`docs/testing_tracker.html`, backed by `/api/testing/*` — see §6a), never in this file.
This file changes only when the *template* changes, and any such change triggers the
regression rule in §9.

---

## 1. Purpose and scope

**What is being proven.** One paid LLM generation per chapter (summary → competency mapping →
LP canonical → assessment), then unlimited free deterministic partitions of that canonical by
`aruvi_core/genon/partition.py` (v0.5, `GENON_ENGINE_VERSION` bumped at step 0) — across every
subject and class that has content. Secondary aims: prove the 18 synthetically-validated
amendments in `MEMORY.md` §"★ AMENDMENTS TO BE TESTED" against live generation, price the
~317-chapter pre-warm in rupees, and prove tenancy on every surface built so far.

**The 25-combo matrix** (subject·class combinations with chapter content):

| Subject | Stage: preparatory (III–V) | middle (VI–VIII) | secondary (IX) | Chapters |
|---|---|---|---|---|
| english | iii, iv, v | vi, vii, viii | ix | 103 |
| mathematics | iii, iv, v | vi, vii, viii | ix | 90 |
| science | — | vi, vii, viii | ix | 50 |
| social_sciences | — | vi, vii, viii | ix | 42 |
| the_world_around_us | iii, iv, v | — | — | 32 |

Chapter counts are as recorded 2026-07-28; step 0.6 re-verifies them before the sweep.

**Out of scope.**
- **Class X** — maps to secondary in `aruvi_core/grades.py` but has no content in any
  subject. Recorded as a content gap, not tested.
- The seam-polish path — **removed at step 0**, not tested around (scope decision, closed).
- Live generation *inside the API* (`POST /subjects/{s}/{g}/generate` is an intentional 501
  stub); generation runs through the cowork chapter pipeline, outside the API.
- Supabase/Phase-4 adapters — everything here tests the file-backed repositories.

**Certification unit.** A combo is *certified* when every C-step in §4 is Pass (or N/A with a
recorded reason), under one constitution version and one engine version, with provenance (§6)
recorded for every artefact. The tracker is the register of record.

---

## 2. Step 0 — campaign preconditions (run once, before anything else)

Every step: actor · action · **exit criterion** · artefact.

**0.1 [Kumar] Remove the polish path.** Strip from the codebase:
- `api/main.py`: the `polish` field on `GenonPlanRequest`; `_seam_polish_allowed()` and the
  `ARUVI_SEAM_POLISH` env gate; the `want_polish` block in `genon_make_plan` (including the
  `run_polish` import and the `seam_polish` token-log call); the `polish` key in all three
  response shapes (identity / cached / fresh).
- `api/data.py`: the `polished` parameter of `genon_plan_filename` and the `'_p'` suffix.
- `web/app/lib/format.js`: `SEAM_POLISH_ENABLED` and every read of it.
- `aruvi_core/genon/polish.py` may remain on disk but nothing may import it.
**Exit:** `grep -rn "polish\|_p'" api/ web/app/lib/format.js aruvi_core/genon/__init__.py`
shows no live reference (comments about the removal are fine); API starts clean;
`pytest tests/` green. **Artefact:** the diff.

**0.2 [Kumar] Bump the engine version.** `GENON_ENGINE_VERSION = "06"` → `"07"` in
`api/data.py`, with a dated comment ("07: polish path removed; cache-key shape loses the
`_p` variant"). **Caveat, stated deliberately:** this changes the cache-key shape — every
existing `e06` plan file is stale by construction and every plan produced in this campaign is
keyed `..._e07_c<canonical-version>.json`. All filename assertions in C10 use `e07`.
**Exit:** a fresh partition writes a `_e07_` file; no new file carries `_p`.
**Artefact:** the diff + one sample filename.

**0.3 [Kumar] Archive the surviving legacy polished file.** Exactly one exists:
`data/content/saved_plans/social_sciences/ix/ch_05_50m16_e03_c20260726112240_p.json`. Move it
to `backup/` (it must leave the saved-plans library so listings and exports can never reach
it). **Exit:** `find data/content/saved_plans -name "*_p.json"` returns nothing.
**Artefact:** the moved file's new path.

**0.4 [Kumar] Deploy the campaign tracker.** Merge `api/testing_campaign.py` + the two-line
include in `api/main.py`; open `docs/testing_tracker.html` (or `GET /api/testing/tracker`)
against the running API. **Exit:** a tick made in the browser survives an API restart
(state at `data/testing/campaign_state.json`). **Artefact:** the state file.

**0.5 [Kumar] Provision the two test identities.** `Kumar1` and `Kumar23` (sent as
`X-Aruvi-User`; tenant_id == user_id). Each gets a readiness profile covering the subjects
under test. **Exit:** `GET /readiness` with each header returns `ready: true` and the two
profiles differ. **Artefact:** the two readiness JSONs.

**0.6 [Claude] Re-verify the matrix.** Count chapters per combo from
`data/content/chapters/<subject>/<grade>/summaries/` (or mappings) and confirm the 25 combos
and ~317 chapters; confirm class X has no content anywhere. **Exit:** the table in §1 matches
the disk, or is corrected here with a dated note. **Artefact:** the count table, recorded in
the tracker under step 0.

**0.7 [Kumar] Cost baseline.** Confirm `runtime_data/token_log.csv` exists with its header
and that `ANTHROPIC_API_KEY` is present in the generation environment. **Exit:** a test row
can be appended and read back. **Artefact:** the CSV header line.

After 0.1–0.3, this document never mentions polish again. The surviving requirement is C8:
Claude flags anywhere an LLM call would be needed, so a deterministic route is sought first.

---

## 3. Per-stage preparation (once per subject·stage, 10 of 11 outstanding)

Constitutions are per **stage**; test execution is per **class**. This asymmetry is the main
thing this document manages, so the two lists are kept strictly apart.

> **ORDERING RULE (hard):** every amendment for a stage completes — P1 through P4, versions
> bumped, changelog written — **before any class in that stage enters the §4 cycle**.
> Amending a stage's constitution after certifying one of its classes invalidates that
> class's canonical (the canonical was authored under the older version; see §9).

Stages and their current state (from `docs/partition_constitution_rollout.md` §2, verified
2026-07-28 — re-check the version lines before starting each stage):

| # | Subject · stage | LP ver | Band shape | Skill layer | Group |
|---|---|---|---|---|---|
| S1 | social_sciences · secondary | **1.5 — DONE (reference)** | time_bands | competency_edges | — |
| S2 | social_sciences · middle | 2.7 | time_bands | competency_edges | A |
| S3 | science · secondary | 1.0 | time_bands | implied_lo | A |
| S4 | mathematics · secondary | 1.0 | time_bands | implied_lo | A |
| S5 | the_world_around_us · preparatory | 1.2 | time_bands | implied_lo | A |
| S6 | science · middle | 2.1 | phases[] | implied_lo | B |
| S7 | mathematics · middle | 3.3 | phases[] | core_/adjunct_competencies | B |
| S8 | mathematics · preparatory | 1.1 | phases[] | core_/adjunct_competencies | B |
| S9 | english · preparatory | 1.0 | phases[] | implied_lo | B |
| S10 | english · middle | 1.5 | phases[] | implied_lo | B |
| S11 | english · secondary | 1.0 | phases[] | implied_lo | B |

Per-stage checklist (tracker keys P1–P4 under the stage):

**P1 [Kumar] Amend the LP constitution** from the SS·secondary v1.5 reference
(`data/content/constitutions/lesson_plan/social_sciences/secondary/lesson_plan_constitution.txt`),
per `docs/partition_constitution_rollout.md` §3:
- **A1** — period schedule = exactly ONE standard row `{duration_minutes, count}` at the
  class-standard duration (40 ≤VII · 45 VIII · 50 IX–X). Ports verbatim.
- **A2** — Rule 14: `band_id = "P<period_number>.<ordinal>"` on every band; the skill layer
  names the band_id(s) of its own unit. **Does NOT copy-paste** outside Social Sciences:
  only SS carries `competency_edges`. For each other subject, decide and record *which
  object carries the band reference* (`implied_lo` rows, or `core_/adjunct_competencies`),
  and note that `compile.py::_check_declarations` currently iterates `competency_edges`
  only — the C5 gate is vacuous for those subjects until it is generalised (see the
  standing engine item in §5, X3).
- **A3** — Rule 15: `role_handoff` (flat `band_id → hook|development|consolidation`,
  emitted after the plan, with the no-anticipation prohibition).
- **A4** — Rule 16: `unit_handoff` (N−1 adjacent-pair `{title, teacher_notes}` entries; no
  splice, no abstraction, no completion language).
- **A5 + A7** — THE SELF-CONTAINED REGISTER, ported as **ONE shared block** beside
  VOCABULARY (never as three separate prohibitions), with duration independence (A7) folded
  in; the notes rule, band rule and handoff rule reference it in one line each.
**Exit:** the amended file carries all of the above; `VERSION` bumped; a diff against the
pre-amendment file shows no pedagogical rule changed. **Artefact:** the amended
constitution + diff.

**P2 [Kumar] Amend the matching assessment constitution** (A6): every item carries
`phase_ref` (a band_id of the unit it anchors to; `band_ref` naming per the reference,
`assessment/social_sciences/secondary` v1.2). Depends on P1/A2 — the band ids must exist
first. **Exit:** `VERSION` bumped; the schema block mandates `phase_ref`.
**Artefact:** amended file + diff.

**P3 [Kumar] Group B only — schema conversion.** Convert
`phases[{minutes, description}]` → `time_bands[{band_id, minutes, activity}]` (rename both
the array and the `description` key; the compiler reads exactly `time_bands` and
`activity`). The decision is already taken in the rollout brief: amend the constitutions,
do NOT teach `compile.py` an adapter. **Exit:** the schema block emits `time_bands` with
all three keys; no `phases[` remains in the file. **Artefact:** diff.

**P4 [Kumar] History to the sidecar.** The amendment note goes to `CHANGELOG.md` beside the
constitution, never into the file; the `VERSION` line stays in the file. **Exit:** the
constitution contains no version-history block; `CHANGELOG.md` lists every bump with date
and one-line rationale. **Artefact:** the changelog.

**[Claude] Stage sign-off:** read the amended pair against the reference and the rollout
brief; confirm A1–A7 land, the register is one block, and the per-subject A2 decision is
recorded. **Exit:** a written note per amendment: present / absent / deviates-with-reason.
Recorded in the tracker; the stage's classes are then unblocked.

---

## 4. The per-combo cycle (the repeating numbered template — run 25 times)

Precondition: the combo's stage shows P1–P4 signed off in the tracker.
Chapter selection: one chapter per combo carries the full cycle (prefer a mid-book chapter
with ≥3 sections); C1–C4 may additionally be run on more chapters when pre-warming, but
certification is on the cycle chapter. Record the chapter number in the tracker.

All API calls: base `http://localhost:8000`, identity via `X-Aruvi-User`. The five partition
runs (C5) split across identities: **Kumar1 runs two, Kumar23 runs three** — this is what
makes C10/X1 meaningful. Record which ran which.

**C1 [Kumar] Generate the chain.** Run the chapter pipeline (summary → competency mapping),
then the LP canonical, then the assessment, under the stage's amended constitutions. Install
the canonical at
`data/content/saved_plans/<subject>/<grade>/ch_NN_canonical.json` (`plan_status:
"canonical"`, `genon_canonical.ledger_ts` stamped). Supply all four JSONs to Claude.
**Exit:** `GET /genon/{subject}/{grade}/chapters` lists the chapter, and
`canonical_minutes` equals standard-duration × period-count. **Artefact:** the four JSONs.

**C2 [Claude] Cost the chain.** From the run logs / `runtime_data/token_log.csv`, record per
stage (summary, mapping, LP canonical, assessment): wall seconds, input tokens, output
tokens, cost ₹ — and the chapter total ₹. **Exit:** all 4×4 cells + total are recorded in
the tracker's provenance panel; any missing cell is recorded as missing (a gap, not a
blank). **Artefact:** the provenance record. *This rupee total is the number that decides
whether pre-warming ~317 chapters is affordable — it falls out of the template here, never
reconstructed later.*

**C3 [Claude] Canonical vs constitution, rule by rule.** Check the canonical against every
numbered rule of the stage's current LP constitution, citing rule numbers — a table
`rule # → pass / fail / subjective-pass with quoted evidence`, not a general impression.
Register/tone judgements are subjective: say so, and quote the specific strings the
judgement rests on (e.g. any band text naming minutes, position, or calendar). **Exit:**
every rule number in the constitution appears in the table; every fail becomes a defect
(§7). **Artefact:** the rule table (attach in tracker comment or link).

**C4 [Claude] MEMORY.md amendment items, live.** From the 18-item checklist (`MEMORY.md`
§"★ AMENDMENTS TO BE TESTED"), test the items that apply to this combo — they are not one
checkbox; several are themselves per-combo tests. Applicability map (verify against the
current list; items summarised):

| Item | Applies to | Item | Applies to |
|---|---|---|---|
| 1 guide.{TYPE} nesting | SS + TWAU (assessment) | 10 named referenced word | english mid+sec |
| 2 MCQ keyed reveals | english | 11 homework (p.NN) | english (all) |
| 3 exact item counts | all subjects | 12 FILL_IN table dedup | english (all) |
| 4 split chapters regenerate | english iii, vi–ix | 13 narrowed A/B ban | english (all) |
| 5 task_density cutoffs | english vi–viii (see X2) | 14 number_line stimulus | maths prep+mid |
| 6 time vector — superseded* | (see note) | 15 homework book_ref | maths (all 3 stages) |
| 7 empty approach OK | maths prep, SS | 16 inclusivity {support, challenge} | maths middle |
| 8 FILL_IN/MATCH shapes | english prep | 17 SS teacher_notes | SS middle |
| 9 Jul 12–13 wave contracts | per its file list | 18 MCQ position spread | science + SS mid/sec |

\* Item 6 ("wire time into the constitutions" as a duration vector) is **superseded by the
A1 single-standard-row architecture** — the partition engine took over duration handling.
Record it as closed-by-design in the tracker the first time it comes up, and say so in
MEMORY.md.
**Exit:** each applicable item gets pass / fail / n-a-here with one line of evidence from
the live artefacts; fails become defects. **Artefact:** the item table.

**C5 [Kumar] The five partitions.** Let the canonical be N periods × D minutes (canonical
minutes M = N·D). Run `POST /genon/{subject}/{grade}/{ch}/plan` with uniform matrices at D
minutes and counts `round(p·N)` for p = **115%, 100%, 85%, 75%, 55%** — one per compression
regime plus identity:

| % | Expected regime (`genon.compression.regime`) |
|---|---|
| 115 | stretch (ratio > 1.0) |
| 100 | **identity** — separate route: response `identity: true`, the canonical's own
filename, **no new file saved** |
| 85 | rescale (0.8–1.0) |
| 75 | role-weighted (0.6–0.8; `DEV_PACE_FLOOR` 0.8) |
| 55 | unit-drop (below `COVERAGE_FLOOR` 0.6) — must populate `section_coverage_note` |

Two runs from `Kumar1`, three from `Kumar23` (record which). **Exit:** five 200-responses;
each reports the expected regime; identity saved no copy; the other four wrote
`ch_NN_<matrix>_e07_c<ver>.json` files. **Artefact:** the five responses + four files.

**C6 [Kumar] Mixed-duration matrix.** At least one realistic weekly mix for this class among
the five budgets (e.g. VIII: 45-min standard + one/two longer periods; pick a real timetable
ratio and record it). **Exit:** 200; file written; ratio and regime recorded.
**Artefact:** response + file.

**C7 [Claude] Partition compliance.** On the C5/C6 plan files:
1. **Tiling** — in every sitting, band minutes sum exactly to the sitting's duration.
2. **Unit order preserved** — units appear in canonical order; no reordering, no loss above
   the coverage floor.
3. **Register** — every teacher-facing title and note is free of calendar time, position,
   and clock quantity. Mechanical first pass: case-insensitive scan for a stated word-list
   (minute, hour, half, yesterday, tomorrow, last/next class|period|week, previously,
   earlier, later, first/second half, begin/end of the period, day \d). Subjective second
   pass on survivors; quote every judged string.
4. **55% run** — `section_coverage_note` present and names the dropped content.
5. **C6 run** — the weekly cycle repeats with long periods interior and non-adjacent
   (partition v0.4 ordering).
6. **Wide spans** — every sitting holding 3+ units appears in `genon.wide_spans` with
   per-unit minutes; the container title names the heaviest adjacent pair, never a
   ≤5-minute scrap; units the title does not name are listed.
**Exit:** all six checks pass on every file, or defects filed. **Artefact:** the check
table per file.

**C8 [Claude] LLM-need flags.** Note every point in the combo's flow where output quality
begs an LLM call (e.g. a mechanical join reading badly, a container title that no
deterministic selector could get right). **Exit:** a (possibly empty) list, each entry with
the deterministic alternative to try first. **Artefact:** the list, in the tracker comment.

**C9 [Claude] Assessment anchoring after re-cut.** In the 75% and 55% plans: every
assessment item's anchor resolves to the unit its `phase_ref` band belongs to; in the 55%
plan, any item whose anchor unit was dropped carries its scheduling note rather than
mis-anchoring to a surviving unit. **Exit:** zero mis-anchored items; dropped-unit items
all carry the note. **Artefact:** anchor table for the two plans.

**C10 [Claude] Storage conventions.**
1. Canonical named `ch_NN_canonical.json`; adapted plans exactly
   `ch_NN_<matrix>_e07_c<canonical-version>.json` where `<matrix>` is
   duration-aggregated, longest-first (`50m16`, `60m3-45m9`) and `<canonical-version>` is
   the canonical's `ledger_ts` (+`h<rev>` when `handoff_rev` is set).
2. **Cache hit** — repeat one C5 request (either identity): response has `cached: true` and
   the file's mtime did not change.
3. **Engine bump re-keys** — assert the C5 files are `_e07_` while any pre-campaign files
   for this chapter remain `_e06_` untouched (no overwrite). (Step 0.2 is the live proof;
   here it's an assertion on filenames.)
4. **Determinism** — delete one C5 plan file, re-run the same request: the new file is
   byte-identical except the top-level `saved_at` (compare `result` + `genon` sections;
   `diff <(jq 'del(.saved_at)' a) <(jq 'del(.saved_at)' b)` empty).
**Exit:** all four hold. **Artefact:** filenames + the empty diff.

**C11 [Claude] Partition wall time.** Time a **cache-miss** C5-style request (delete the
file first, or use a fresh matrix): `curl -w '%{time_total}'`. **Exit:** total < 5 s
(anything over 5 s is a defect; record the actual figure either way — the norm is
milliseconds plus one compile). **Artefact:** the timing.

**C12 [Kumar runs, Claude inspects] Exports.** For the C6 plan (the richest): all three plan
exports — `GET /api/plans/{s}/{g}/{filename}/export/{lesson|assessment|integrated}` — in
both `format=pdf` and `format=docx`, plus the allocation report
(`POST /api/allocation/export-pdf` and `export-docx`) for this subject·grade. View-model
shapes differ by subject (science·ix section-grouped; science middle stage-grouped; english
nested by spine) — the export must render this combo's shape cleanly. **Exit:** 8 files
open without error; no blank sections, no raw JSON leaking, unit/band structure visible and
matching the plan; assessment `answers=1` renders the answer layer. **Artefact:** the 8
files (spot-check pages attached for fails).

**C13 [Kumar breaks, Claude reads] Failure paths.** Three deliberate failures, each must
surface a message a teacher can read, with no stack trace in the response body:
1. **Declaration failure** — copy the canonical to a scratch chapter number, delete one
   `band_id`, request a partition → HTTP 500 with `"Canonical cannot be compiled: …"`
   naming the period/band, not a bare 500. Remove the scratch file after.
2. **Matrix over 60 periods** → HTTP 400 `"Period count implausibly large."`
3. **No canonical** — a chapter number with none → HTTP 404 `"No canonical for this
   chapter yet."`
**Exit:** the three status codes + readable details; nothing resembling a traceback in any
body. **Artefact:** the three responses.

**Combo sign-off [both]:** all C-steps Pass/N-A in the tracker, provenance panel complete,
defects either closed or accepted-with-owner. The combo row turns green.

---

## 5. Cross-cutting checklist (run once; re-run on any material change)

**X1 [both] Tenancy, every surface built so far.** With `Kumar1` and `Kumar23` (each having
run their C5 share):
1. `GET /plans-prepared` — each sees exactly the keys they created; no overlap beyond plans
   both prepared.
2. `GET /plan-archive` + archive/restore — Kumar1 archives a plan; Kumar23's listing is
   unaffected; restore returns it; `GET /plans/{s}/{g}` shows per-caller `archived` flags.
3. `GET/POST/DELETE /section-state` — progress + bookmark isolated per user; Kumar23 never
   sees Kumar1's bookmark.
4. `GET /readiness` — the two profiles stay distinct; the 409-cascade guard fires for a
   destructive edit and cascades only with `cascade: true`.
5. Allocation — `save_allocation` / `GET allocation` / `DELETE` isolated per user for the
   same subject·grade.
6. **The authorization case, not just visibility:** as Kumar23, fetch a plan only Kumar1
   prepared, by filename: `GET /plans/{s}/{g}/{filename}/view` and the three export routes.
   These take a filename and do not consult the prepared-plans register. **Expected under
   the current design:** the fetch succeeds — plan files are shared Bucket-A content and
   per-teacher scoping is by register, not by file ACL (CLOUD_DATA_MODEL). Record the
   result verbatim and put it to the founder as an explicit accept/reject: if rejected,
   it becomes an S2 defect; if accepted, it is written into CLOUD_DATA_MODEL.md as a
   stated property.
7. **Chapter notes** — *confirmed before writing:* the API exposes `section-state`
   (bookmark + progress) and **no notes endpoint** (all 31 routes in `api/main.py`
   enumerated 2026-07-29). Notes are client-side only. Test accordingly: notes stay in the
   browser profile that wrote them and survive nothing else; record this as a known
   limitation, not a tenancy defect.
**Exit:** checks 1–5 show zero leakage; 6 and 7 recorded with a founder decision.
**Artefact:** the paired-request evidence (request + header + response) per check.

**X2 [Claude] Effort index vs the calibrated standard.** On the Year Plan page of My
Lessons: per-chapter `recommended_periods` and effort weights must match
`data/content/allocation_norms/master_plan.json` (calibrated first,
`recommended_source: "master_plan"`; NCF fallback only where the master plan has no row —
and shown alongside, never driving the default). Verify for one grade per subject against
the API (`GET /subjects/{s}/{g}/chapters`). **English caveat (MEMORY item 5):** the
`task_density` cutoffs (≤2.0 / 2.1–2.9 / ≥3.0) were calibrated on VI and reused for VII and
VIII with an admittedly weak fit — for English the *standard itself* is in question, not
merely conformance. So for english vi–viii, additionally report the raw `task_density`
distribution per grade from the live pipeline runs; if a grade collapses to a near-binary
tier signal, file a defect against the *calibration*, owner founder.
**Exit:** page values == API values == master plan for the sampled grades; the English
distribution report exists. **Artefact:** comparison table + distribution note.

**X3 [Kumar] Standing engine item (from P1/A2, do once before the first non-SS stage
certifies):** generalise `compile.py::_check_declarations` beyond `competency_edges` so the
C5 gate inspects whichever object carries band refs per subject. This is an engine change →
engine version bumps → §9 regression rule applies (cheap re-check of anything already
certified). **Exit:** a canonical whose `implied_lo` (or equivalent) rows lack band refs
fails compilation with a named problem. **Artefact:** the diff + a failing fixture.

---

## 6. Provenance block (recorded for every run — a result that cannot be attributed to a version is not a result)

Fixed fields, captured in the tracker's provenance panel per combo (and per re-run):

| Field | Source |
|---|---|
| LP constitution version | `VERSION` line of the stage's LP constitution |
| Assessment constitution version | `VERSION` line, assessment side |
| `GENON_ENGINE_VERSION` | `api/data.py` (07 after step 0.2) |
| Canonical `ledger_ts` / `handoff_rev` | `genon_canonical` block of `ch_NN_canonical.json` |
| Plan filename(s) | C5/C6 responses |
| Model | generation run log (e.g. the model id used by the pipeline) |
| Date | run date |
| Wall time | per stage (C2) and per partition (C11) |
| Tokens in / out | per stage (C2) |
| Cost ₹ | per stage + chapter total (C2) |

## 6a. Recording surface

State lives **in Aruvi itself**: `GET/PUT /api/testing/campaign` and
`POST /api/testing/campaign/item`, persisted at `data/testing/campaign_state.json`
(Bucket-B-style, atomic writes). The UI is `docs/testing_tracker.html`, also served at
`GET /api/testing/tracker`; it renders §2–§5 as tickable steps with comments, the §7
register, the §8 matrix, and exports comments/defects as CSV/JSON for gathering later.

---

## 7. Defect register

One row per defect, in the tracker (exportable):

`id` (ARV-D-001…) · `combo` (or "stage:<s>" / "campaign") · `step` (0.x/Pn/Cn/Xn) ·
`severity` · `title` · `evidence` (file/response/quote) · `owner` · `status`
(open / fixing / fixed-awaiting-recheck / closed / accepted) · `opened` / `closed` dates.

Severity scale — definitions, not vibes:
- **S1** — the chain is broken: canonical cannot be generated/compiled, partition wrong or
  >5 s, data loss, tenancy leakage on a register. Stops the combo.
- **S2** — teacher-visible wrongness: mis-anchored assessment, register violation in
  teacher-facing text, export renders wrong/blank, missing coverage note. Combo cannot
  certify until fixed or founder-accepted.
- **S3** — contract drift that a teacher wouldn't see: naming/key deviations, missing
  report fields, soft-requirement gaps (handoff_missing). Certify allowed with the defect
  open and owned.
- **S4** — cosmetic / doc / advisory. Never blocks.

Fixes that touch a constitution or the engine trigger §9.

---

## 8. Progress tracker (the 25 rows)

Maintained live in the tracker UI; the canonical column set:

`stage-prep (P1–P4 + sign-off)` — shared per stage · then per combo: `C1 C2 C3 C4 C5 C6 C7
C8 C9 C10 C11 C12 C13 · sign-off`. Cross-cutting X1–X3 and step 0 sit above the matrix.

Rows: english iii · iv · v · vi · vii · viii · ix; mathematics iii · iv · v · vi · vii ·
viii · ix; science vi · vii · viii · ix; social_sciences vi · vii · viii · ix;
the_world_around_us iii · iv · v.

---

## 9. Regression rule

**Any constitution or engine change mid-campaign re-opens every combo already certified
under the old version.** Two distinct responses — never conflate them:

- **Cheap re-check** (sufficient when the *canonical is unchanged* — i.e. an engine bump or
  a partition-affecting change): re-run the five C5 partitions + the C6 mix against the
  existing canonical, and diff each new plan against the recorded artefact
  (`jq 'del(.saved_at, .filename)'` both sides). Empty diffs (beyond the expected key/
  engine-version fields) → the combo stays certified, with the new engine version recorded
  in provenance. Any non-empty content diff → full C7–C12 on the changed files.
- **Full re-certification** (required when the *stage's constitution* changed): the
  canonical was authored under the old version, so C1 regenerates it and the whole cycle
  C1–C13 re-runs. This is the cost the §3 ordering rule exists to avoid — amend first,
  certify after.

The tracker marks re-opened combos amber automatically when a provenance version differs
from the current campaign versions; it never silently keeps green.

---

## 10. Pilot — social_sciences · ix · chapter 5

The whole template, end to end, exactly once, **before** any other combo: step 0 → (stage
S1 prep already done, sign-off recorded retroactively) → C1–C13 → X1 → tracker round-trip.
Template defects found here cost one chapter; found at combo 8 they cost eight.

Notes specific to the pilot:
- SS·secondary is at constitution v1.5; the existing certified canonical
  (`ch_05_canonical.json`, ledger 2026-07-26) predates v1.4/v1.5 and carries the known
  P6.1 "three minutes" register violation — so the pilot's **C1 regenerates chapter 5
  under v1.5**, which also discharges the outstanding re-certification from the rollout
  brief. The C10 cache checks then run against the *new* `c<ledger_ts>` key; the old
  `_e06_`/older files remain as the no-overwrite evidence.
- C3 on the pilot doubles as the calibration of the rule-table format itself; C7's
  register word-list is frozen here for the rest of the campaign (extend it only with a
  dated note).
- The pilot ends with an explicit **template retro**: every step whose instruction was
  ambiguous or whose exit criterion was uncheckable gets rewritten here before combo 2.

---

## 11. Suggested execution order (after the pilot)

Ordered to prove the riskiest portable assumptions earliest and spend the six Group-B
schema conversions late, one stage fully certified before the next stage's prep begins:

1. **social_sciences vi → vii → viii** (stage S2, Group A) — the only other
   `competency_edges` subject: A2 is a true copy-paste, so this is the cheapest proof that
   the template ports at all. Also carries MEMORY items 17 and 18.
2. **science ix** (S3, Group A) — first `implied_lo` subject: forces the A2 per-subject
   decision and X3 (the generalised gate) on a single class before any multi-class stage.
   Also the section-grouped export shape (C12).
3. **mathematics ix** (S4, Group A) — second `implied_lo` port; confirms the A2 decision
   generalises. MCQ position spread (item 18) not applicable; cognitive-demand hinge (item
   9) is.
4. **the_world_around_us iii → iv → v** (S5, Group A) — completes Group A; first
   preparatory-stage classes; item 1 applies.
5. **science vi → vii → viii** (S6, first Group B) — the cheapest `phases[]` conversion
   (P3) because its skill layer is plain `implied_lo` and its constitution already bans
   role-embedding (A3 is a pure addition). Stage-grouped export shape.
6. **mathematics vi → vii → viii** (S7), then **mathematics iii → iv → v** (S8) — Group B
   with the `core_/adjunct_competencies` skill layer (a second A2 shape); items 14, 15, 16.
7. **english last: ix (S11) → vi → vii → viii (S10) → iii → iv → v (S9)** — deliberately
   final: three separate stage preps, the largest chapter count (103), the spine-nested
   export shape, the heaviest MEMORY burden (items 2, 4, 5, 8–13), and X2's open
   calibration question — by the time english starts, the template is boring and only the
   subject is hard. Secondary first within english so the fork-parent (middle v1.5-derived)
   deltas of item 9 are exercised while attention is fresh.

Rationale in one line: pilot proves the template; SS·middle proves it ports; science·ix
proves it ports *off* `competency_edges`; everything after is repetition with known risk
retired in order of cost.

---

## Corrections note (repository vs prompt, checked 2026-07-29)

Verified against the repo before writing: `GENON_ENGINE_VERSION = "06"` (`api/data.py`);
31 routes in `api/main.py`; exactly one legacy `_p` file
(`social_sciences/ix/ch_05_50m16_e03_c20260726112240_p.json`); both polish kill-switches in
place (`ARUVI_SEAM_POLISH` in `api/main.py`, `SEAM_POLISH_ENABLED = false` in
`web/app/lib/format.js`); SS·secondary LP at v1.5 with the sidecar `CHANGELOG.md`;
compression constants `COVERAGE_FLOOR = 0.6`, `DEV_PACE_FLOOR = 0.8`, `DEMOTE_BELOW =
0.35`, `CUT_COST {consolidation 0, development 2, hook 6}` (`partition.py`); no notes
endpoint (X1.7). No contradiction with the authoring prompt was found. One judgement call:
MEMORY item 6 is treated as superseded by A1 (see C4) rather than as a live amendment —
confirm with the founder at the pilot.
