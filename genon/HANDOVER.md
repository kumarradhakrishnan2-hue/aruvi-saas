# GENON HANDOVER — sessions of 2026-07-23 / 2026-07-24 (read this first in the next session)

Gen-on-gen: one certified canonical LP+assessment per chapter, adapted to any
teacher timetable by deterministic code. This file is the complete state; the
architecture rationale is in README.md alongside.

## UPDATE 2026-07-24 — step 3 DONE for SS-secondary, applied LIVE

The genon amendments were applied DIRECTLY to the live SaaS constitutions
(founder decision) at data/content/constitutions/.../social_sciences/secondary/:

- **LP → v1.1**: Rule 14 (band_id / role / band_refs + handoff copy), A1/A2
  schema edits, AND the Decision-2 time-input simplification (INPUTS 4 =
  exactly one standard row, 40/45/50 by class; TIME integrity = duration ×
  count; single-row note in A1). The 2026-07-23 drafts lacked the time-input
  change — it is now in.
- **Assessment → v1.2, not v1.1**: the live assessment was ALREADY v1.1 (the
  MCQ answer-distribution rule, absent from the prototype mirror the old
  drafts were cut from — copying those drafts would have silently dropped it).
  phase_ref amendment applied on top; MCQ rule preserved. One precision fix
  beyond the draft: "implied_lo, cognitive_demand, and band_refs were copied
  verbatim from the edge" (band_refs is edge-sourced).
- **make_amendments.py rebased**: now reads amended/originals/ (the archived
  pre-amendment live texts) and reproduces the deployed texts byte-identically
  (verified by diff). amended/ holds lesson_plan_constitution_v1.1.txt +
  assessment_constitution_v1.2.txt = exact copies of the live files; the stale
  2026-07-23 assessment_constitution_v1.1.txt draft moved to _superseded/.
- All generation for SS-secondary (chapter skill included) now runs on the
  genon constitutions. Amendments remain verified only by live generation —
  that is step 4's control test + first v1.1 canonical (SS IX at N × 50).
- Other subject families' constitutions: still v1.0, step 3 pending per combo.

## UPDATE 2026-07-24 (later) — step 2 DONE + step 4 harness BUILT

**Step 2 master plan** (genon/master_plan.{py,json,md}): budgets sourced from
data/content/allocation_norms/ncf_chapterwise_period_allocation.xlsx (the
founder's realistic budget sheet, cleaned this session: duplicate class-VI rows
removed; Summary!B6 XLOOKUP → COUNTIFS/SUMIFS). 25 combos, 4,275 annual periods
portfolio-wide; per-chapter recommended periods via largest remainder over
effort weights; floors at the 0.6 drop threshold. **SS IX ch 5 → 21 × 50 min
(canonical 1050 min), floor 630 min ≈ 13 standard periods.** SS IX chs 10–18
are NCERT placeholders (flat weight 12, 108/215 of total weight) — numbers WILL
shift when real chapters land; generate_canonical REFUSES placeholder chapters.
Class X: budgets exist, no chapters yet — skipped.

**Step 4 harness (sync mode)**:
- genon/prompt_assembly.py — the prototype's prompt wrapper extracted VERBATIM
  from Project Aruvi app/aruvi_streamlit/app.py; mechanical parity VERIFIED
  line-by-line (builder body 96/96 content-identical; helpers byte-identical).
  Declared deviations only: mirror→data/content root, no streamlit, inline
  block wrapped as _build_lpa_prompts_standard. English builder deliberately
  NOT lifted yet (its constitution isn't genon-amended; raise on dispatch).
- genon/generate_canonical.py — `one <subject> <grade> <ch>` sync mode:
  defaults from master_plan.json + class-standard duration; --dry (prompt dump,
  no API); --lp-const/--assess-const overrides (the v1.0 control test:
  point both at genon/amended/originals/, --tag control_v10); v1.1 validation
  (band_id/role/band_refs/phase_ref presence, period count); appends to
  genon/ledger.csv (₹ at $3/$15 per M, ₹92/$). Batch mode still deferred.
- Dry-run PASSED for SS IX ch 5: 21×50 assembles with the live v1.1/v1.2
  constitutions; system 38.7k chars, user 39.0k chars.

## UPDATE 2026-07-25 — first v1.1 canonical GENERATED; Rule 14 tuned to v1.1.1

**First live v1.1 canonical (SS IX ch 5, 21×50)**: 18,975 in / 52,764 out,
₹78.05, 879.5s, status ok (ledger row 1; out/canonical/social_sciences/ix/
ch_05_20260725_120209_canonical.json). Deep inspection: all 63 bands correctly
band_id'd and tiled; 43 edges all with in-unit band_refs, ZERO defaulted to
all-bands; handoff 43 LO rows verbatim-identical; 32 assessment items all with
exact phase_ref identity; 21 sections, no gaps. The identity chain works.

**FINDING**: every period came out exactly 3-banded hook→dev→consolidation
(21/21/21) — Rule 14's arc-narrated role definitions + "exactly one of" acted
as a template during single-pass generation (v1.0 at 14×40 averaged 4 varied
bands). Phases now ~17 min vs ~10 — coarser partition granularity.

**v1.1.1 applied to the LIVE LP constitution (founder-approved minimal fix)**:
role definitions stripped to move-types (arc verbs removed), "exactly one of"
→ "based on the following guidance, applied on a best-effort basis", and the
exception-catalogue sentence dropped. Deliberately NO distribution statements
("most bands are development" would read as a quota) and NO new prohibition.
Per-band single-value guarantee still enforced by Prohibition 4 + A1 enum +
generate_canonical validator. make_amendments.py reproduces v1.1.1
byte-identically from amended/originals/.

**Verification owed**: regenerate ch 5 (same command) — pass = varied band
counts (~4–5/period at 50 min) and non-uniform role sequences; residual
uniformity would implicate the 40→50 duration change, not wording.

## UPDATE 2026-07-25 (later) — step 6 WIRED: genon inside Aruvi SaaS, end to end

- **aruvi_core/genon/** (new engine package): compile.py = compiler **v0.3 STRICT
  declared-only** (rejects pre-v1.1 plans — 171 named violations on the old ch 5;
  no inference code in the product); partition.py = the lab v0.3 ported verbatim
  (PartitionError instead of SystemExit); polish.py = tier-1 seam polish
  (pure build/apply + run_polish; skips gracefully without ANTHROPIC_API_KEY).
- **Canonical artifacts (Bucket A)**: data/content/canonical/social_sciences/ix/
  ch_05_canonical.json (the 21×50 v1.1 canonical + provenance block) and
  ch_05_stream.json (63 phases, declared). The API partitions the STREAM;
  recompile only on compiler version bumps.
- **API**: GET /genon/{subject}/{grade}/chapters (availability);
  POST /genon/{subject}/{grade}/{ch}/plan {rows:[{duration,count}], polish} —
  partitions in ms, saves into the saved-plans library (same-second filename
  uniquifier), registers in the caller's prepared-plans → **pops up in My
  Lessons**. Guards: 400 empty rows / >60 periods, 404 no canonical, 500 wrapped
  PartitionError. Polish failures never block the plan (skipped+reason).
- **Web (PrepareLesson.jsx + format.js postJSON)**: when the chosen chapter has a
  canonical, the periods stepper becomes a **duration-rows editor** (count ×
  minutes, add/remove rows, seeded from the profile's class durations × the
  effort-index suggestion; budget meter syncs to row totals) + "Smooth unit
  transitions with AI" checkbox (polish flag). Non-canonical chapters keep the
  old saved-plan path untouched. STATIC verification only (esbuild parse clean) —
  per CLAUDE.md §11 live render must be checked locally.
- **E2E TESTED in sandbox** (FastAPI TestClient, full engine + real SS plugin):
  compile→partition zones (21×50 rescale · 15×50/21×35 role-weighted · 12×45 at
  ratio 0.514 drops 3 trailing units · 10×40+4×30 drops 4) · plan appears
  prepared with correct periods · view model renders (12 periods, 32 items) ·
  tenant isolation holds. NOTE: 16×35 needed split-fallback — the 3-band
  coarseness of the current canonical biting; rerun after the v1.1.1 regen.
- Against the 21×50 canonical (1050 min), the old test matrices are now DEEP
  compression (12×45 = 0.514) — teachers near the recommended 21 periods sit in
  the comfortable zones; the master plan's floor (13×50) is where dropping begins.

## UPDATE 2026-07-25 (cleanup) — canonicals LIVE IN saved_plans; naming rules

Founder layout doctrine: **data/content/ holds all crucial server content; canonicals
are saved plans, so they live in data/content/saved_plans/{subject}/{grade}/ as
ch_NN_canonical.json (plan_status "canonical"). genon/ holds engine code ONLY —
no content.** Executed:
- ALL previous saved plans cleared (founder has backups; on-disk copies moved to
  _to_delete/saved_plans_old/ — 47 files incl. the three 07-23 hand-deployed genon
  plans and every subject's samples). Old prepared-register entries now dangle
  harmlessly (missing files simply don't list).
- SS IX ch 5 canonical (21×50, v1.1) restructured into saved-plan shape and placed
  at saved_plans/social_sciences/ix/ch_05_canonical.json. data/content/canonical/
  and genon/out content moved to _to_delete/ (empty dirs remain — delete cannot run
  over the bridge; remove them with _to_delete).
- **No stream artifact on disk**: api/data.py compiles the stream on demand from
  the canonical (strict v0.3) with an mtime-keyed memo cache.
- **Naming rules (simulation)**: a request whose duration matrix equals the
  canonical's standard row (rows aggregated by duration) registers THE CANONICAL
  itself as prepared — no copy, no prefix; it goes by its chapter name alone.
  Amended durations save an adapted copy whose card/picker shows the matrix in
  small letters below the name ("45 min × 12" / "40 min × 10 · 30 min × 4") —
  listing field duration_label, CSS .sc-durline.
- E2E re-verified: identity (incl. split same-duration rows) → canonical, no file;
  variations → labelled copies; canonical renders 21 periods through the view.

## UPDATE 2026-07-25 (allocation single-sourcing) — master plan moved to content; denominator fix

Bug found by founder: Prepare suggested 43 periods for SS IX ch 5 at budget 240 —
the app divided by the LISTED chapters' weight (107, only chs 1–9 have mappings)
instead of the FULL syllabus weight (215 incl. the 9 NCERT placeholders). Doctrine
locked: **master_plan.json lives in data/content/allocation_norms/ (with the
workbook + NCF norms) and is the single source for allocation numerators and
denominators. Suggestion = weight / syllabus_total_weight × the TEACHER'S OWN
annual budget. The canonical schedule (21×50) is ONLY the authoring golden rule —
it never drives her suggestion; what she actually allocates × her duration types
feeds the partition rules.** Implemented:
- genon/master_plan.py repathed: reads the workbook from, and writes
  master_plan.{json,md} to, data/content/allocation_norms/ (genon copies retired).
- /subjects/{s}/{g}/chapters: weights overridden from the master plan, response
  carries syllabus_total_weight; NCF estimates use the same full denominator.
- PrepareLesson: suggestion divides by syllabus_total_weight (240→21, 200→18);
  plus a coverage hint from /genon canonical_minutes — under 60% of the canonical's
  minutes warns that trailing sections drop (with the minimum period count at her
  duration), 60–80% notes compression.

## UPDATE 2026-07-25 (polish) — validator built; checkbox STAYS for testing

Founder decision: the "Smooth unit transitions with AI" checkbox remains OPT-IN
during the testing phase (always-on reconsidered later — the flip is a small
policy change in genon_make_plan). The owed **polish validator** is now built
into aruvi_core/genon/polish.run_polish: every delta is code-checked (teacher_note
within word budget +10%; where a seam note is needed, the note must OPEN with a
≤24-word continuation clause — exactly the failure modes that got Haiku
rejected). Invalid deltas get ONE retry naming the violations; periods still
failing keep tier-0 text (recorded in seam_polish.tier0_kept). This is the
prerequisite for reconsidering Haiku. Unit-tested; needs one live keyed run.

## UPDATE 2026-07-25 (deixis) — LP constitution → v1.1.2: temporal self-containment

Founder finding from the first partitioned plans: band text in the 21×50 canonical
carries deixis — "today" (P1.1, P4.1, P10.2) and 11 unit cross-references ("next
unit" P4.3/P5.3/P6.3/P14.3, "previous unit" P3.1/P6.1/P8.1/P13.1…) — which
re-orients the teacher from FLOW to DAY (against the calendar purge) and breaks
under repartition; forward promises are worst (the promised unit may merge or
drop). Doctrine locked: **content is timeless; navigation belongs to container
text the engine owns** (titles, seam notes, teacher notes).

v1.1.2 applied LIVE (founder-approved; register only, no pedagogical change):
- Rule 13 prohibition 5: band text MUST NOT use calendar words or cross-unit
  references — each band speaks in the present of its own activity; sequence
  lives in structure; unit linking lives only in teacher_notes.
- Rule 10 prohibition: teacher notes MUST NOT use calendar words or forward
  references — the previous-unit link is the ONLY cross-unit reference, always
  backward. (Backward links are safe: polish re-anchors them per partition.)
- A proposed deterministic deixis detector for the certification gate was
  DECLINED by founder — the constitution rule alone governs; the one-time
  canonical review catches residue.
- make_amendments.py reproduces v1.1.2 byte-identically from originals/.
- Current ch 5 canonical (generated under v1.1.1) still carries the 14 band
  instances — regeneration under v1.1.2 pairs with the pending v1.1.1
  band-structure verification: ONE run (`one social_sciences ix 5`) checks both
  (varied band counts + zero deixis).

**Next actions**: rotate the 07-23 API key → control test
(`one social_sciences ix 5 --lp-const genon/amended/originals/... --assess-const
... --tag control_v10`) → shape-check vs a historic saved plan → first v1.1
canonical `one social_sciences ix 5` (21×50) → compile → partition stress zones.

## Decisions LOCKED this session

1. **Phase-centric architecture**: canonical plan → compile (pure rewriter, verbatim,
   inventory-audited) → phase stream (stable phase IDs, roles, unit table = reference
   partition) → deterministic partition → teacher plan. LLM appears ONLY in (a) one-time
   canonical authoring, (b) optional seam/note polish.
2. **Canonical durations are class constants**: 40 min for classes ≤ VII, 45 for VIII,
   50 for IX. Single row N × duration. The teacher's duration MIX never reaches the
   generator — it is a partition-time input only. (Constitution time-input SIMPLIFIES;
   the old "mix without order" amendment idea is dead.)
3. **Compression doctrine (three regimes, no upper bound)**:
   - ratio > 1.0: stretch, uncapped (soft advisory only at extremes)
   - 0.8–1.0: uniform rescale
   - 0.6–0.8: role-weighted — dev bands floored at ×0.8 pacing; hooks/consolidations
     absorb evenly across units; trailing consolidations demote to homework when
     hc-scale < 0.35; band floor 3 min
   - < 0.6: drop TRAILING units until ≥ 0.6, Rule-4-style section_coverage_note names
     the uncovered sections; items of dropped units flagged "anchor unit not scheduled";
     their handoff LO rows removed from the derived plan (recorded in genon block)
   - Thresholds are engine constants, to be calibrated from the corpus sweep.
4. **Golden-8 link resolution relocates, unchanged**: runs once at compile-time via the
   subject plugins; stamped in phase coordinates (linked_phases/anchor_phase); period-level
   contract derived per partition by lookup. Renderer contract untouched.
5. **Corpus back-fill approved by founder**: historic saved plans in
   aruvi-saas/data/content/saved_plans WILL be back-filled (additive-only, deep-diff
   guarded) to the v1.1 schema (band_id, role; band_refs SS-only; phase_ref on items),
   so compiler v0.3 can be strict/declared-only. Prototype mirror stays untouched.
   NOT YET DONE. Log in pre-warm checklist when done.
6. **Polish**: tier-0 deterministic (continuation titles, content-quoted seam notes) +
   tier-1 LLM (titles, seam notes, teacher-note CONDENSATION to word budget
   75 + 15/extra-unit, cap 100, MUST open with ≤20-word continuation clause).
   Model: claude-sonnet-4-6. Haiku tested and REJECTED for now (drops continuation
   clause, busts word cap) — revisit only with a validate-and-retry wrapper.
   Polish attaches to (chapter, matrix) → cacheable; teacher notes are container-scoped
   text, hence polish-eligible; PHASE TEXT IS NEVER TOUCHED (verified by band diff).
7. **Roles matter measurably**: role-aware vs role-blind boundaries differ 10/11 (12×45)
   and 15/15 (16×35); consolidation-endings 6 vs 1 and 11 vs 2. Roles this session are
   compiler-INFERRED; declared roles come with v1.1 live generation.

## The agreed 8-step plan (step 1 DONE)

1. ✅ Partition v0.3 with three-regime compression (committed).
2. ⏳ Master plan with founder: realistic annual budget → per subject·class allocation
   (NOT the NCF numbers), durations 40/45/50 as above. **Founder to supply budget
   numbers.** Output: annual periods, recommended-per-chapter, computed per-chapter
   floors (floor = ratio where unit-dropping would begin).
3. 🟢 Per subject·class: rewrite constitution as genon version (Rule 14 equivalent adapted
   per family; time input = single standard row). **SS-secondary DONE 2026-07-24 and
   applied LIVE (LP v1.1, assessment v1.2 — see UPDATE above); other families pending.**
4. Live API generation of the canonical at standard duration (SS IX will be N × 50 —
   the current 14×40 test canonical retires).
5. Stress test 0.8–1.0 / 0.6–0.8 / <0.6 zones; Claude writes comparison report.
6. First combo's functionality moves into Aruvi SaaS (teacher-facing).
7. Repeat 3–5 per combo, step 5 running on SaaS.
8. Track cost + time throughout (start a genon ledger; polish runs so far:
   sonnet ₹1.75/13.9s, sonnet+condense ₹3.88/36.3s ×2, haiku ₹1.32/18s).

## Files (aruvi-saas/genon/)

- README.md — architecture + v0.2 test results table
- amended/lesson_plan_constitution_v1.1.txt, amended/assessment_constitution_v1.2.txt —
  exact copies of the now-LIVE SS-secondary constitutions (Rule 14: band_id/role/
  band_refs + single-standard-row time input; assessment phase_ref identity);
  reproduced by make_amendments.py (surgical, assert-guarded edits on the archived
  pre-amendment texts in amended/originals/)
- compile_stream.py — v0.2 compiler (SS shape only; INFERS roles/phase_refs).
  **v0.3 pending**: feed via subject plugins' lesson_plan_to_view (Science/Maths newer
  plans use time_bands, older used phases; English uses phases+description), strict
  declared-only after back-fill
- partition.py — v0.3, three-regime compression, role-aware DP, tier-0 polish
- polish_seams.py — tier-1 LLM polish (Sonnet), note condensation + hard continuation rule
- apply_delta.py / run_genon.py / dry_run_test.py / genon_adaptation_doc.md — v0.1
  delta-over-period approach, kept as baseline; superseded by phase pipeline
- out/ch05_stream.json + partitioned/stress outputs

## Deployed to Aruvi SaaS for user Kumar1 (this session)

data/content/saved_plans/social_sciences/ix/:
- ch_05_20260723_101245.json — 12×45, TIER-1 POLISHED (condensed notes, 69–99 words)
- ch_05_20260723_101635.json — 16×35, RAW (seam markers visible, for comparison)
- ch_05_20260723_101040.json — 10×40+4×30, zero seams
Registered in data/prepared_plans/Kumar1/Kumar1/prepared.json. All three verified
through the real SS plugin + ViewModel + golden-8 link resolution: 29 items, 0 orphans.
Titles carry "· genon <matrix>" suffixes. Original ch_05_20260715_215601.json untouched.


## Step 4 execution design — lifting the prototype generator (decided 2026-07-23, end of session)

"Same way" generation is earned by code extraction, not imitation:

- **prompt_assembly.py** — the prototype's generation prompt wrapper (document order,
  system/user placement, framing text; spec §7.4 wrappers) extracted VERBATIM from
  Project Aruvi. Zero creative edits. This module IS the same-way guarantee.
- **generate_canonical.py** — one CLI, two modes over that single assembly:
  - `one <subject> <grade> <ch>` — sync Messages API call, full price. For supervised
    runs: the v1.0 control test, first v1.1 canonical per combo, anything to inspect.
  - `batch <manifest> submit|collect` — Message Batches API at 50% discount (input AND
    output). One JSONL, one request per chapter (custom_id = subject/grade/chapter,
    up to 100k requests per batch → whole portfolio = one order). collect → validate →
    compile → floors → ledger; failures quarantined for sync re-run.
- **Control test before any v1.1 run**: generate once with the UNamended v1.0
  constitution through the script; check output shape against a historic saved plan.
  Shape parity proves the harness faithful; thereafter any v1.1 difference is
  attributable to the amendment alone.
- **Sequencing**: build sync mode first; wire batch mode only when entering the mass
  pre-warm sweep — async submit/collect is wrong for the iterate-and-inspect phase,
  right for the sweep.
- A thin Cowork skill (like the `chapter` skill) may later wrap the script for
  chat convenience — sugar only; the script is the single generation dialect for
  chat, terminal, cron, and batch alike.
- Note: "same way" = same distribution, not identical artifacts — sampling variance
  was always present (same chapter: 20k–58k output tokens across prototype runs).
  The one-time canonical review absorbs it.

## Open tunings / owed items

- Hook 3-min floor in deep compression (8→3 min): terse — judgment call for founder in
  step-5 report. Dev pacing can normalize to 0.79 (< 0.8 floor) — make invariant hard.
- Polish validator (continuation clause present, word cap) — build at productionization;
  prerequisite for reconsidering Haiku.
- Back-fill script + compiler v0.3 (plugin-fed, strict) — not started.
- Pre-warm checklist entries owed: corpus back-fill; each constitution amendment
  (verified only by live generation); English MCQ etc. items already in MEMORY.md.
- Confusion-keyword survival check after note condensation (belt-and-braces).
- Founder should ROTATE the API key pasted in the 2026-07-23 chat.

## Key measured economics (SS IX ch 5, sonnet-4-6, ₹92/$)

Original generation: ₹67.6, minutes, 19.2k in / 45.1k out. Corpus median lpa ₹24.
Adaptation now: partition ₹0/ms + polish ₹1.75–3.88/14–36s, cached per (chapter, matrix).
Recent-corpus cost split: output tokens ≈ 83% of spend — why delta/partition wins.
Batches API halves canonical authoring for the pre-warm sweep.
