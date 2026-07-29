# Prompt for Fable 5 — author the Aruvi SaaS test campaign plan

---

You are writing `docs/testing.md` for the Aruvi SaaS repository: a **professional test plan
that will be executed repeatedly, once per subject·class combination**, by two actors working
iteratively — Kumar (runs the product, supplies artefacts) and Claude (inspects artefacts,
checks compliance, reports). The document is a **template with numbered steps**, not a
narrative; the same numbered cycle is run 25 times.

Read the repository before you write. Everything below is verified as of 2026-07-28, but
verify anything you rely on — and if you find it has changed, say so in the document rather
than silently writing to the old fact.

---

## 1. What Aruvi does, in the two paragraphs you need

A chapter is authored ONCE into a **canonical lesson plan** by an LLM, at one standard period
duration (40 min for classes up to VII, 45 for VIII, 50 for IX–X), under a **constitution** —
a long prompt of numbered MANDATE/PROHIBITION rules held in
`data/content/constitutions/lesson_plan/<subject>/<stage>/lesson_plan_constitution.txt`. A
companion **assessment constitution** governs the assessment items.

Every individual teacher's plan is then produced **deterministically, with no LLM**, by the
**partition engine** (`aruvi_core/genon/partition.py`): it compiles the canonical into a phase
stream (`aruvi_core/genon/compile.py`), cuts that stream to her duration matrix via a
role-aware DP, compresses through three regimes, and selects container text for sittings that
span a unit boundary. This is the money-saving architecture — one paid generation per chapter,
free partitions forever. The test campaign exists to prove it holds across every subject and
class.

Key documents to read first:
- `docs/partition_constitution_rollout.md` — the amendment programme this campaign executes
- `CLAUDE.md`, `MEMORY.md` — project conventions and history
- `data/CLOUD_DATA_MODEL.md` — storage and tenancy design
- `data/content/constitutions/lesson_plan/social_sciences/secondary/` — the reference
  constitution (v1.5) plus its `CHANGELOG.md`; every other constitution is amended toward it

---

## 2. Ground truth (verified — use it, but re-check before relying)

**Test matrix: 25 subject·class combinations** that have chapter content, spanning classes
III–IX across ~317 chapters:

| Subject | Classes with content | Chapters |
|---|---|---|
| english | iii, iv, v, vi, vii, viii, ix | 103 |
| mathematics | iii, iv, v, vi, vii, viii, ix | 90 |
| science | vi, vii, viii, ix | 50 |
| social_sciences | vi, vii, viii, ix | 42 |
| the_world_around_us | iii, iv, v | 32 |

Class X maps to the secondary stage in `aruvi_core/grades.py` but **has no content in any
subject** — out of scope, note it as a content gap.

**Constitutions are per STAGE, classes are not.** 11 LP + 11 assessment constitutions over
5 subjects × 3 stages (preparatory III–V, middle VI–VIII, secondary IX–X). Only
`social_sciences/secondary` has been amended for partition. This asymmetry drives the plan's
structure: amendment work is per-stage, test execution is per-class.

**The compiler's hard contract** (`compile.py::_check_declarations` — any miss raises
`GenonDeclarationError` and the chapter cannot be prepared at all):
`time_bands[]` on every period, each band carrying `band_id` + `minutes` ("a-b") + `activity`;
a role in `{hook, development, consolidation}` from `role_handoff[band_id]` or inline; every
`competency_edges[]` entry carrying `band_refs` within its own unit; every assessment item
carrying `phase_ref`. Soft: `unit_handoff`, N−1 adjacent pairs (degrades to a mechanical join,
logged in `genon.handoff_missing`).

Six constitutions currently emit `phases[{minutes, description}]` and must be amended to
`time_bands[{band_id, minutes, activity}]`: english ×3, mathematics middle + preparatory,
science middle.

**Compression regimes** (`plan_compression`, ratio = requested minutes ÷ canonical minutes):
stretch (>1.0) · rescale (0.8–1.0) · role-weighted (0.6–0.8, `DEV_PACE_FLOOR` 0.8, trailing
consolidations demote to homework below 0.35) · unit-drop below `COVERAGE_FLOOR` 0.6, which
must populate `section_coverage_note`.

**Current engine:** partition v0.5, `GENON_ENGINE_VERSION = "06"` in `api/data.py`. Plan
filenames are cache keys: `ch_NN_<matrix>_e<engine>_c<canonical version>[_p].json`.

**API surface:** 31 routes in `api/main.py`. Tenanted state lives in `plans-prepared`,
`plan-archive`, `section-state` (progress + bookmark), `readiness`, and allocation. Exports at
`/api/plans/{subject}/{grade}/{filename}/export/{lesson|assessment|integrated}` plus allocation
PDF/DOCX.

**`MEMORY.md` line 5** carries `## ★ AMENDMENTS TO BE TESTED — the pre-warming checklist`,
**18 numbered items**. Each records a change validated only *synthetically* (corpus rewritten
by hand) and never proven against a live generation run. This campaign is where they get
proven — but they are not one checkbox: several are themselves per-combo tests.

---

## 3. Scope decisions already taken (do not re-open)

1. **The plan covers the whole chain** — chapter summary → competency mapping → LP canonical →
   assessment — not just the LP. Time, cost and tokens are recorded at each stage, and each
   chapter gets a rupee total. That total is the number that decides whether pre-warming ~317
   chapters is affordable, so it must fall out of the template, not be reconstructed later.
2. **Class X is excluded**, recorded as a content gap.
3. **The polish path is removed before testing begins**, not tested around. Strip the polish
   call, the `_p` filename suffix, and both kill switches (`ARUVI_SEAM_POLISH`,
   `SEAM_POLISH_ENABLED` in `web/app/lib/format.js`); bump the engine version; archive the one
   surviving legacy `_p` file. Write this as **step 0 of the campaign**, with the caveat that
   it changes the cache-key shape. After it, the template never mentions polish — the surviving
   requirement is that Claude flags anywhere an LLM call would be needed, so a deterministic
   route can be sought first.

---

## 4. What the plan must cover

Kumar's original twelve requirements, restated so nothing is lost, plus the additions agreed
in review. Organise them as you judge best — the numbering below is a checklist of coverage,
not a required order.

### Per-stage preparation (runs once per subject·stage, before any class in it is certified)

- **P1.** Amend the LP constitution using `docs/partition_constitution_rollout.md`, drawing
  text from the SS·secondary reference: A1 (single standard period row), A2 (Rule 14 —
  band_id + band_refs; note this does NOT copy-paste, because only Social Sciences has
  `competency_edges`), A3 (Rule 15 role_handoff), A4 (Rule 16 unit_handoff), A5 (the register —
  **port as one shared block, never as three separate prohibitions**), A7 (duration
  independence, folded into the register block).
- **P2.** Amend the matching assessment constitution for `phase_ref` / `band_ref` (A6).
- **P3.** For the six `phases[]` subjects, convert the schema to
  `time_bands[{band_id, minutes, activity}]`.
- **P4.** Keep the amendment note out of the constitution file — history goes to a sidecar
  `CHANGELOG.md`, the `VERSION` line stays.
- **Ordering rule the plan must state explicitly:** every amendment for a stage completes
  BEFORE any class in that stage is certified. Amending a stage's constitution after certifying
  a class invalidates that class's canonical.

### Per subject·class cycle (the repeating numbered template)

- **C1.** Kumar runs the chapter pipeline (summary → mapping) and then the LP canonical;
  supplies the JSON to Claude.
- **C2.** Claude reports wall time, token counts and cost for each stage and the chapter total.
- **C3.** Claude checks the canonical against every rule of the current constitution and raises
  issues — rule by rule, citing rule numbers, not a general impression.
- **C4.** Claude checks which of the 18 `MEMORY.md` amendment items apply to this combo and
  whether the live generation actually exhibits them.
- **C5.** Kumar runs partitions at **115%, 100% (identity), 85%, 75% and 55%** of the
  canonical's period budget — one per compression regime plus the identity path, which takes a
  separate route in `api/main.py` (registers the canonical, saves no copy, returns
  `identity: true`). Two of the 5 are run from one user profile and 3 from another. 
- **C6.** Kumar runs at least one **mixed-duration matrix** in a realistic weekly ratio for that
  class among the above 5.
- **C7.** Claude checks partition compliance: teacher notes and titles in register, unit order
  preserved, band minutes tiling each sitting exactly, `section_coverage_note` present at 55%,
  the weekly cycle repeating with long periods interior and non-adjacent at C6, and
  `genon.wide_spans` populated where sittings hold 3+ units — with the container title naming
  the heaviest pair, not a 3-minute scrap.
- **C8.** Claude flags any point where an LLM call would be needed, so a deterministic
  alternative can be explored first.
- **C9.** Claude confirms assessment items anchor to the correct units after re-cutting, and
  that an item whose anchor unit was dropped at 55% carries its scheduling note rather than
  mis-anchoring.
- **C10.** Claude confirms storage conventions: canonical and plan filenames, cache-key
  components, that a repeat request is a cache **hit** and not a re-partition, that an
  engine-version bump yields a new key rather than an overwrite, and that the same canonical
  and matrix produce a byte-identical plan.
- **C11.** Claude confirms partition wall time; anything over 5 seconds is a defect.
- **C12.** Exports: all three plan exports plus allocation PDF/DOCX render cleanly for this
  subject's view-model shape (they differ — science·ix is section-grouped, science·middle
  stage-grouped, english nested by spine).
- **C13.** Failure paths: a canonical that fails declarations, a matrix over 60 periods, a
  chapter with no canonical — each surfaces a message a teacher can read, with no stack leak.

### Cross-cutting (run once, and re-run on any material change)

- **X1.** Tenancy, every aspect built so far: prepared plans, plan archive, section-state
  (progress and bookmark), readiness, allocation. Two profiles (Kumar1, Kumar23) must each see
  only what they asked for, with archiving behaving correctly. **Include the authorization
  case, not just the visibility case:** can Kumar23 fetch Kumar1's plan by filename at
  `/plans/{subject}/{grade}/{filename}/view` or the three export routes? Those take a filename
  and may not consult the prepared-plans register.
  *Confirm before writing:* Kumar lists "chapter notes" as a tenanted surface; the API exposes
  `section-state` (bookmark + progress) but no notes endpoint. Establish whether notes are
  client-side only and test them accordingly.
- **X2.** Effort-index calculations on the Year Plan page of My Lessons match the calibrated
  standard. Note that `MEMORY.md` item 5 records English-middle's `task_density` cutoffs as
  calibrated on Grade VI and reused unchanged for VII and VIII with an admittedly weak fit —
  so for English the standard itself is in question, not merely conformance to it.

---

## 5. Required document structure

1. **Purpose and scope** — what is being proven, the 25-combo matrix, what is out of scope.
2. **Step 0 — campaign preconditions**, including the polish removal.
3. **The per-stage preparation checklist**, with the ordering rule.
4. **The numbered per-combo cycle** — the heart of the document. Every step must carry:
   - an **actor tag**: `[Kumar]` or `[Claude]`
   - a **measurable exit criterion** — what specifically must be true, checkable by a second
     person. "Compliant" is not a criterion; "every band_id matches `P<n>.<ordinal>` and every
     `band_refs` entry resolves within its own unit" is.
   - the **artefact** it produces or consumes
5. **The cross-cutting checklist.**
6. **Provenance block** — a fixed set of fields recorded for every run: constitution version,
   `GENON_ENGINE_VERSION`, canonical `ledger_ts` and `handoff_rev`, plan filename, model, date,
   wall time, tokens, cost. A result that cannot be attributed to a version is not a result.
7. **Defect register** — id, combo, step, severity scale with definitions, owner, status.
8. **Progress tracker** — the 25 combos as rows, per-stage prep and per-combo cycle as columns.
9. **Regression rule** — any constitution or engine change mid-campaign re-opens every combo
   already certified under the old version. Define the cheap re-check (re-run the partitions,
   diff against the recorded artefacts) as distinct from full re-certification.
10. **Pilot** — the whole template is executed once, end to end, on **social_sciences · ix ·
    chapter 5** (the only certified canonical, already at constitution v1.5) to debug the
    template itself before the 25-combo sweep begins. Template defects found here cost one
    chapter; found at combo 8 they cost eight.
11. **Suggested execution order** for the remaining combos, with reasoning.

---

## 6. Quality bar

- Write for someone who will execute this without you in the room. Every instruction is
  concrete: name the file, the endpoint, the field, the expected value.
- Prefer a checkable assertion to a description of intent, everywhere.
- Where the repository contradicts something in this prompt, follow the repository and say so
  in a "corrections" note at the end of the document.
- Where a step depends on something that does not yet exist, mark it BLOCKED with what is
  needed, rather than writing an instruction that cannot be followed.
- Keep it a working document. No preamble about the importance of testing; no restatement of
  what Aruvi is beyond what an executor needs.
- State honestly where a check is subjective (register and tone judgements largely are) and say
  what evidence the judgement must cite.

## 7. Do not

- Do not write the test *results*, or invent artefacts. This is the plan.
- Do not re-open the three scope decisions in §3.
- Do not collapse the per-stage and per-combo work into one list; the asymmetry between
  stage-level constitutions and class-level execution is the main thing the document exists to
  manage.
- Do not assume any subject other than Social Sciences has `competency_edges`. It does not, and
  A2 needs a per-subject decision about which object carries the band reference.
