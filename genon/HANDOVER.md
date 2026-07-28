# GENON HANDOVER — sessions of 2026-07-23 → 2026-07-26 (read this first in the next session)

Gen-on-gen: one certified canonical LP+assessment per chapter, adapted to any
teacher timetable by deterministic code. This file is the complete state; the
architecture rationale is in README.md alongside.

**Where things stand (2026-07-26, end of day)** — SS IX ch 5 is the live proof: canonical
certified at 21×50 under LP v1.2.1, adapted 16×50 both raw and AI-polished, both in
Kumar1's My Lessons. Adapted plans are now content-addressed cache entries; the polish
retry, the progress indicator and the declaration-error message shipped today and need a
uvicorn restart. Read the LAST update section first, then Decisions LOCKED (both dates),
then Open tunings. Two live constraints that keep biting: **a .py edit is not live until
uvicorn restarts**, and **check `grep -c parse_failures aruvi_core/genon/polish.py` before
trusting a polish record** (the file was silently reverted once by a stale editor buffer).

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

## UPDATE 2026-07-25 (cost notebook) — unified token log restarted

Founder ask (corrected — SaaS repo, NOT Project Aruvi): aruvi-saas/runtime_data/
token_log.csv is the ONE cost notebook for the genon era. The prototype's log
(196 rows, chapter-pipeline era) is archived alongside as token_log_old.csv;
Project Aruvi's own runtime_data is untouched/restored. Fresh token_log.csv
seeded with the ch 5 canonical run (2026-07-25, 18,975/52,764, ₹78.05,
call_type canonical_generation).
Auto-appends henceforth, BEST-EFFORT (missing sibling repo never blocks a run):
- generate_canonical.py → call_type "canonical_generation" (alongside its own
  genon/ledger.csv, which stays as the genon-detail ledger);
- API seam polish (PrepareLesson checkbox) → call_type "seam_polish"
  (api/data.py append_token_log; env ARUVI_TOKEN_LOG overrides; file+header
  auto-created if missing).
Partition runs cost ₹0 and are deliberately NOT logged.

## UPDATE 2026-07-25 (role handoff) — LP → v1.2: roles leave the bands (founder design)

Two failed wordings (v1.1.1, v1.1.2 regen both 21/21 uniform 3-band h→d→c) proved
the corruption is INLINE declaration itself: forcing a role choice at each band's
write-moment makes the taxonomy the outline. Founder's fix mirrors coverage_handoff:
- **Rule 14** now carries band_id + band_refs + handoff copy ONLY (role clause and
  role prohibitions removed; title updated).
- **New Rule 15 · ROLE HANDOFF**: a flat role_handoff sibling of lesson_plan,
  emitted AFTER plan+handoff are complete, classifying every band_id from its
  finished text — autoregressively, all bands exist before any role token is
  written, so authoring is never shaped per-band. Same three definitions.
- A1: time_bands lose the inline role field; role_handoff sibling added.
- **Rejected alternatives**: two-pass API (works but +₹5-8 and more harness;
  fallback if v1.2 still collapses) and count/time anchors in Rule 13 (founder:
  unanticipated-issues risk).
- Harness: prompt_assembly's output sketch now lists role_handoff (declared
  deviation 4 — the sketch must track A1's top level); generate_canonical
  validator + compiler v0.3 accept role_handoff OR legacy inline (both verified,
  role parity identical on the current canonical).
- make_amendments.py reproduces v1.2 byte-identically.
**Verification = next regen**: pass criteria now (a) varied band counts/role
sequences (the actual test of the design), (b) zero band deixis, (c) role_handoff
complete. If (a) still fails → build two-pass; stop rejigging prose.

## UPDATE 2026-07-26 — LP → v1.2.1: teacher notes position-free (founder design)

Founder's merged-notes proof: stacked Rule-10 notes juggle N×("previous unit…
this unit…") anchors, and after a seam "the previous unit" can describe content
taught minutes earlier in the SAME sitting — anachronistic. Doctrine completed:
**NO positional language originates in generated text, anywhere.** Continuity
links now NAME the content they build on ("Having traced the Vedic political
vocabulary, …"); position words exist only in the engine's seam clause, computed
from the actual partition, hence always true.
- VOCABULARY: the sanctioned cross-reference example dropped.
- Rule 10 mandate: link "to the content already taught — named by that content
  itself, never by its position". Prohibition now bans positional references of
  ANY direction (previous/this/next unit, last time).
- polish.py SYSTEM: condensed notes strip positional refs the same way — so
  adapted plans cut from the current (pre-v1.2.1) canonical converge too.
- make_amendments.py reproduces v1.2.1 byte-identically.
The pending regeneration now tests FOUR criteria: varied band structure (Rule 15
role_handoff design) · zero band deixis · complete role_handoff · position-free
teacher notes.

## UPDATE 2026-07-26 — v1.2.1 canonical CERTIFIED + DEPLOYED; role-handoff verdict

Run 20260726_112240 (19,542/50,424, ₹74.98, 836s) initially saved RAW ONLY: 4
naked inner quotes broke strict JSON. Repaired by escaping (content
byte-identical), certified, DEPLOYED as saved_plans/.../ch_05_canonical.json.

**Four-criteria verdict**:
(A) Role-handoff design (Rule 15) SUBSTANTIALLY WORKED: 4 bands/period (was 3),
84 phases, avg 12.5 min (~v1.0 granularity). Still uniform h·d·d·c ×21 — the
taxonomy's pull survives at a distance, grip weakened. Partitioner impact real:
16×35 no longer needs split-fallback; 12×45 tiles at tol 0.18; 17×50
hook-opens/consolidation-closes 10/17 (was 9/17). FOUNDER + Claude verdict:
good enough — stop chasing variance; move to next chapters.
(B) Band deixis ×6 (sampling noise around small mean; was 2). (C) role_handoff
84/84 flawless; compiler consumes it ("declared (role_handoff)"). (D) Notes:
"previous unit" 19→2, but "this unit" self-reference persists ×22 — polish
strips at partition time (prompt line in place).

**Harness hardening**: generate_canonical.py now auto-repairs naked-inner-quote
JSON breaks (bounded ≤10, escape-only, ledger-noted "auto-repaired N naked
quotes"; any other defect still fails hard). Tested against the actual failed
raw: 4 repairs, parses, 84/84 roles.

## UPDATE 2026-07-26 (later) — first LIVE polish · 16×50 studied · plans become CACHE ENTRIES

**Stale-process lesson first** (cost an hour of debugging). After the canonical moved to
role_handoff, Prepare 17×50 failed with a bare 500. Cause: uvicorn was still holding the
pre-role_handoff compile.py, which demanded inline band `role`. `_stream_cache` is
mtime-keyed, so CONTENT swaps are picked up live — **CODE changes are not**. Rule:
restart uvicorn after any .py edit; a canonical swap needs no restart. Also fixed:
`GenonDeclarationError` now returns "Canonical cannot be compiled: …" from
genon_make_plan instead of escaping as an unreadable 500 (it was raised OUTSIDE the try).

**Band-count history settled** (founder question — corrects earlier updates). Every
LLM-authored SS plan is uniform WITHIN itself; only the minute split varies. From
backup/saved_plans:

| plan | bands/period | distinct minute patterns |
|---|---|---|
| IX ch5 14×40 v1.0 | 4 in all 14 | 6 |
| VIII ch4 v1.0 | 4 in all 11 | 5 |
| VII ch4 v1.0 | 4 in all 11 | 7 |
| VI ch6 v1.0 | 5 in all 11 | 5 |
| 120209 (v1.1) | 3 in all 21 | — |
| 112240 (v1.2.1, live) | 4 in all 21 | 7 |

So "v1.0 at 14×40 averaged 4 VARIED bands" (UPDATE 2026-07-25) was WRONG — v1.0 was a
flat 4 as well. Uniform band COUNT is the generator's lifelong behaviour, not a
Rule-14/15 artifact, and "varied band counts" was never a valid pass criterion. What
v1.2.1 actually did was restore the house norm (3 → 4). The 07-23 plans that show mixed
3/4/5 counts are PARTITION outputs — engine-made variety, not authored.

**16×50 studied** (`ch_05_20260726_120401.json`, first role-weighted regime run live):
- 800/1050 = ratio 0.762 → role-weighted. hooks ×0.684 (174→119 min), dev ×0.798
  (731→583; the 0.8 floor is still SOFT), consolidation ×0.676 (145→98). One band at the
  3-min floor. All 21 units kept, zero demotions, zero drops, every period exactly 50 min.
- Integrity clean: 84/84 band texts byte-identical and in order, band_ids preserved,
  29 assessment items all phase_ref'd, no `[Continued]` markers in activity text.
- **Seam density is the finding**: 11/16 periods open mid-unit; ALL 16 titles mechanical.
  Sweep at 50 min — 21→0 seams · 20→3 · 19→4 · 18→6 · 17→7 · **16→11** · 15→12 · 14→7 ·
  13→7 · 12→8 (+1 dropped unit). 16 is the WORST point in the range, worse than 13,
  because 84 bands ÷ 16 = 5.25 (packing rotates 5/5/6) while 14 divides evenly at 6.0.
  Uniform unit shape gives the DP no natural cut points — the downstream cost of the
  authoring uniformity above.
- Role consequence: 10 periods open on a development band, 1 opens on a CONSOLIDATION,
  and 5 CLOSE on a hook (bell immediately after a new unit opens) — the sharpest
  pedagogical cost of deep packing; candidate for a partition-time penalty later.
- **Tier-0 defects found (NOT yet fixed)**: `_first_clause` splits on ". ", so P2's seam
  quote truncated to "Display Fig." (source: "Display Fig. 5.2 and ask …"); and the
  tier-0 template itself writes "This period continues the unit begun last time" —
  period language + a calendar word, both of which polish.py's SYSTEM forbids the LLM
  from producing. The deterministic layer breaks its own rule.

**First live tier-1 polish** (`ch_05_20260726_123557.json`, sonnet-4-6): 15/16 polished,
P3 kept tier-0. Notes 2,663 → 1,372 words (52%), every one inside the 90w budget, named
confusions preserved; titles now human ("Saptāṁga Administration and Provincial
Governance" for "The Saptāṁga State and Its Administration — continued, then Provincial
Administration: Layers of Governance"). Band text and timings byte-identical. ALL
residual junk (`[Next unit]`, "last time", "this unit", one forward ref) is confined to
the single unpolished period, P3 — fix P3 and the plan is clean. **NOTABLE**: Sonnet
REPAIRED the broken "Display Fig." quote unaided, by reading
`previous_period_closing_activity` ("Last session closed on the manuscript-gap
question") — the tier-0 bug is currently MASKED by the model, not fixed. P3's rejection
reason is unknown because the run used a reverted polish.py (next para).

**polish.py REVERT INCIDENT — guard against this.** The validator/retry fixes were
committed (in HEAD), then an editor buffer wrote an older copy over the working file,
silently removing them while keeping the new SYSTEM paragraph. The live polish run
therefore ran the OLD retry. Before trusting any polish record:
`grep -c parse_failures aruvi_core/genon/polish.py` → 0 means reverted.

**Cost anatomy of one polish run** (16×50, 16 periods flagged — every title is a merge,
so the flagged set is 16, not the 11 seam periods):

| | tokens | ₹ |
|---|---|---|
| one clean call | 8,988 in / 2,626 out | **6.10** |
| actual (retry re-sent the full delta) | 17,977 / 5,252 | 12.21 |
| + double-clicked duplicate whose plan was never saved | 18,046 / 5,614 | 12.73 |
| **paid** | | **24.94** |

Input split: the 16 teacher notes 48% · the two activity excerpts 29% · JSON scaffolding
8% · SYSTEM 7% · titles 8%. Output is 59% of spend, which is why the MODEL choice beats
every payload optimisation. Diacritics (Saptāṁga, Ṛig, Arthaśhāstra) are a small
permanent token tax (~6.8 chars/word). Wall clock 108.5s for the double-called run;
~55–60s expected for one clean call. Levers: stop paying twice (DONE) → ₹6.10 ·
Haiku 4.5 (validator prerequisite now met) → ₹2.04 · trim excerpts, keeping the TAIL of
the closing activity and the HEAD of the opening one → ₹1.85 · cache hit → ₹0.

**DECISIONS LOCKED 2026-07-26 (founder)**

1. **Adapted plans are CACHE ENTRIES** in central storage (Supabase / object store in
   cloud), addressed by (subject, grade, chapter, NORMALISED duration matrix, canonical
   version, engine version, polished). Fresh request → key lookup → hit served at ₹0,
   miss generated. On a miss the only spend is polish; partition is already ₹0/ms.
2. **Reference-not-copy stands** (CLOUD_DATA_MODEL §2.3): the tenant index holds KEYS,
   not bytes. Opening My Lessons invokes THE CENTRAL PLAN, never a per-teacher copy.
   Personalisation stays tenanted (the plan_note overlay, §2.8) — which is exactly what
   lets plans stay immutable and shared.
3. **Polish is NOT stored separately from the plan.** The delta is a function of the same
   key (any change in period count or duration mix changes it), so there is no
   independent reuse and no cost advantage in splitting it. One artifact per key.
4. **A regenerated canonical yields a NEW key.** Old entries are never overwritten: a
   teacher mid-chapter never has her plan change underneath her. The new plan is
   OFFERED, not substituted.

**SHIPPED 2026-07-26 (restart uvicorn to load)**
- `aruvi_core/genon/polish.py` — fixes re-applied on top of the v1.2.1 SYSTEM paragraph:
  retry MERGES across attempts (round-1 wins survive a partial reply); the retry resends
  ONLY the failed periods (the old "return the full JSON delta again" wording is what
  doubled both input and output spend); an unparseable reply is counted and retried
  instead of reading as "nothing needed changing"; all-null entries no longer counted as
  polished. Record gains `flagged`, `tier0_reasons`, `parse_failures`.
  → `tests/test_genon_polish.py` (22 checks, stdlib, faked client — no spend).
- `api/data.py` — `GENON_ENGINE_VERSION = "03"` (BUMP when compile/partition/polish
  change the output); `norm_matrix()` aggregates rows by duration, longest first, so
  17×50 ≡ 10×50+7×50 ≡ 7×50+10×50; `canonical_version()` = `genon_canonical.ledger_ts`
  else a content hash; `genon_plan_filename()` → `ch_05_50m16_e03_c20260726112240[_p].json`;
  `save_generated_plan(..., filename=)` (legacy timestamp path retained).
  → `tests/test_genon_plan_key.py` (21 checks).
- `api/main.py` — cache-hit path BEFORE partition: registers her prepared entry and
  returns `cached: true` with the stored compression / seams / polish record, no
  partition and no polish spend; `cached: false` on the miss path; declaration errors
  named. Verified by simulation: 5 requests → 3 files (2nd identical = hit, split-row
  16×50 = hit, polished + 17×50 = new keys).
- `web/app/components/PrepareLesson.jsx` + `globals.css` — CTA disabled while in flight;
  spinner reading "Smoothing unit transitions…" when polish is ticked, with a hint that
  it can take two minutes; `inFlight` ref blocks re-entry (the modal "Prepare again"
  button too). esbuild-clean; LIVE RENDER STILL UNVERIFIED per CLAUDE.md §11.
- `genon/polish_plan.py` — CLI running the SAME `run_polish` over a plan already on disk:
  `--dry` dumps the payload with no spend, a live run writes the polished twin to
  `genon/out/polish_tests/`, prints a before/after report, and appends a `mode=polish`
  row to genon/ledger.csv. Inspection lab only; the checkbox remains the teacher path.
- The two pre-key plans (`ch_05_20260726_120401.json` unpolished, `…_123557.json`
  polished) are untouched and still registered to Kumar1 — keep them as the A/B pair.

**STORAGE / RETENTION RULE (founder, 2026-07-26)** — settled after a survey of the tree:

| what | where | git |
|---|---|---|
| certified plans: canonicals + adapted cache entries | `data/content/saved_plans/` | TRACKED |
| per-teacher index, section state, archive, readiness, allocations | `data/{prepared_plans,section_state,plan_archive,readiness,allocations}/{tenant}/{user}/` | TRACKED |
| permanent run record (tokens, cost, status, problems) | `genon/ledger.csv` | TRACKED |
| RAW model replies — the only evidence an auto-repair changed nothing but escapes | `genon/out/**/*_raw.txt` | **TRACKED** (~44 KB gzipped each; whole portfolio < 40 MB) |
| prompt dumps + parsed `_canonical.json` (duplicates the deployed file) + polish test twins | `genon/out/` | IGNORED, disposable once certified |

`.gitignore` changed accordingly: bare `out/` → `/out/` (anchored, so it no longer
swallows genon/out), plus explicit ignores for `genon/out/**/*_promptdump.json`,
`genon/out/**/*_canonical.json`, `genon/out/polish_tests/`. Verified with
`git check-ignore`. The idea of relocating artifacts to `runtime_data/genon_runs/` was
RAISED AND DROPPED: `out/` was already gitignored, so the move would have flipped ~425 KB
per run from ignored to committed — the opposite of the intended cleanup.

Also cleaned 2026-07-26: `data/content/feedback/` (38 files, ask_aruvi + forwarded
queries, all pre-July, written at runtime by users — Bucket B living inside Bucket A,
against §0) moved to `runtime_data/feedback_prototype/`; nothing in the codebase reads or
writes it (ports.py:58 classes feedback as tenant data). Stale `out/*.html` demo renders
moved to `_to_delete/out_html_stale/`. Empty `data/content/canonical/` and `out/` remain —
the Cowork bridge cannot delete, founder to remove along with `_to_delete/` itself.

**Next actions** — SUPERSEDED by the 2026-07-28 update below; the polish-tuning branch
(diagnose P3, fix `_first_clause`, decide Haiku, decide always-on) is CLOSED because polish
left the request path. Still owed regardless: **rotate the 07-23 API key**.

## UPDATE 2026-07-28 — LP → v1.3: UNIT HANDOFF. The LLM leaves the request path.

Founder design, and it retires tier-1 polish as a teacher-facing step. Container text for a
period that spans a unit boundary is no longer composed at request time and then repaired by
a model; it is **authored once inside the canonical and selected by index arithmetic**.

**The counting argument that makes it work.** The DP cuts a linear phase stream, so a period
is always a CONTIGUOUS run of units — non-contiguity is structurally impossible, not merely
unobserved. A plan of N units therefore has only N-1 adjacent joints, and every period is one
of three cases: one unit (its own authored text), two units (that pair's entry), three or more
(the LAST adjacent pair). **O(N), not O(N²)** — 20 entries for ch 5's 21 units, authored in the
canonical call, ~2.7k output tokens on a 50k run. Sweep over 46 matrices (50/45/40 × 12–24 plus
7 mixed; 810 periods): 48.1% single-unit · 49.9% pairs · 2.0% triples · **zero misses**, zero
partition failures. Among multi-unit periods that is 96.2% exact-fit.

**Triple rule (founder): use the LATER pair.** In a (6,7,8) span unit 7 is present in full by
construction, so the only question is which neighbour joins it; unit 6 contributes a tail
fragment while 8 carries the new substance. (7,8) names where the weight is. No triple entries,
no quads, no combinatorics.

**Cut-invariance is deliberate, and it is what the rule had to solve.** A pair note cannot know
how much of either unit the period holds — 81% of unit-appearances inside multi-unit periods are
partial. So the note never says where the teacher is; it says what the sitting pivots on, NAMED
BY CONTENT ("What kingship was supposed to be gives way to the apparatus that made it work").
That is v1.2.1's doctrine applied to container text, and it is true at every cut. The deterministic
seam clause is therefore **deleted, not fixed** — which closes both owed tier-0 defects by removal:
`_first_clause` (the ". " split that truncated to "Display Fig.") and the template's "This period
continues the unit begun last time" (period language + a calendar word, forbidden by the very
constitution the engine enforces on the model). The "\n\n[Next unit] " note concatenation goes too.

**Polish self-disables — no code change needed.** `build_polish_request` flags on `", then "` /
`"— continued"` in the title and `"This period continues"` in the notes. None of those strings can
now exist, so `flagged == []` and `run_polish` returns its labelled no-op. Verified across all 46
sweep matrices: **0 periods flagged, ₹0, 0s, no API key dependency in the request path.** The
checkbox, the two-minute spinner, the validator/retry/`parse_failures` machinery and the
tier-0-kept fallback all remain in the code but are now unreachable for a v1.3 canonical.
DECISION 1's rationale ("on a miss the only spend is polish") is spent: **adaptation is now
₹0 and deterministic end to end**, and the cache demotes to a latency nicety over a
millisecond partition.

**LP constitution → v1.3 (Rule 16 · UNIT HANDOFF).** Companion output, same shape as Rule 15's
role_handoff: emitted AFTER the plan, coverage handoff and role handoff are complete, so
autoregressive ordering guarantees the units are committed tokens before any handoff is written —
the handoff cannot bend the arcs it summarises. `unit_handoff` keyed `"<a>-<b>"` → {title,
teacher_notes}. Prohibitions worth knowing: **conjunctions banned outright in titles** ("and",
"&", "with", ", then", "into", "plus", "/", spliced dash) — a title reconstructable by
concatenating the two source titles has failed; no completion language (the platform may place
only part of either unit); Rule 10's calendar/positional ban applies unchanged; ≤90 words.
make_amendments.py reproduces v1.3 byte-identically from originals/ and the assessment
constitution still reproduces byte-identically (unchanged).

**Engine → e04.** `select_container_text` + `validate_unit_handoff` live together in
aruvi_core/genon/partition.py so the two halves of the contract cannot drift; compile.py carries
`unit_handoff` into the stream and reports `meta.unit_handoff_coverage`; generate_canonical's
certification gate now REJECTS a canonical with a missing pair, a non-adjacent pair, a
spliced title, or an over-budget note. A canonical predating Rule 16 still yields a plan —
degraded to a " / " join, every miss recorded in `genon.handoff_missing` and named in
`genon.container_text`, so a degraded plan can never be mistaken for a good one.
`GENON_ENGINE_VERSION` 03 → **04**: titles and notes change for every boundary-spanning period,
so every e03 key is stale by construction and the bump is what stops cache serving yesterday's
mechanical join. `genon.seam_periods_tier0_polished` → `mid_unit_openings` (reporting only now —
container text no longer varies with it); api/main.py's `seam_periods` reads the new key.

**ch 05 BACK-FILLED (20/20) and A/B VERIFIED against the Sonnet twin.** The 16×50 rebuild is
byte-identical to the e03 build in band text, timings, assessment items and coverage handoff —
only container text moved. Titles are the clearest win, because Sonnet was still conjoining:

| | tier-0 | sonnet ₹6.10 | Rule 16 ₹0 |
|---|---|---|---|
| P6 | The Saptāṁga State… — continued, then Provincial Administration… | Saptāṁga Administration **and** Provincial Governance | How Authority Reached the Village |
| P13 | Agriculture, Irrigation… — continued, then Trade Routes, Ports… | Irrigation and Agriculture **into** Trade Routes and Ports | What Surplus Made Possible |
| P16 | Unity in Diversity… — continued, then Chapter Synthesis… | Cultural Integration **into** Chapter Synthesis | Judging Continuity Against Change |

15 of Sonnet's 16 titles are "A and B" or "A into B" — the thin two-excerpt payload could not do
better. **P3 is the proof of the failure mode disappearing**: it was the one period Sonnet failed
to polish, so it shipped tier-0 with the truncated quote and a 179-word stacked note. Under Rule 16
it is a 75-word note and "Reading Politics Out of the Vedic Texts", like every other period — there
is no "unpolished" state left to fall into. Notes land at 68–78 words against Sonnet's 63–89.

**Back-fill provenance**: the 20 entries were authored 2026-07-28 against the certified canonical,
NOT emitted by run 20260726_112240; recorded in `genon_canonical.handoff_backfill`. Plan content
untouched. Canonicals generated under v1.3 emit unit_handoff in the authoring call. The A/B twins
(`…_e03_…json` and `…_p.json`) are KEPT as the control — do not delete them.

**Deliberately NOT done**: renaming band_id `P<unit>.<n>` → `U<unit>.<n>`. The smell is real and
cost this session a round trip ("P6.2" reads as period 6 band 2; it means unit 6 phase 2), but
band_id is load-bearing identity across band_refs, phase_ref, role_handoff and every assessment
item — a rename is a canonical-version bump across the whole portfolio, not a tidy-up. The Rule-16
key uses bare unit numbers ("6-7"), so the new surface does not inherit the smell.

**Next actions**: restart uvicorn (engine + api both changed) → live-render check on
PrepareLesson per CLAUDE.md §11 (the "Smoothing unit transitions…" spinner and its two-minute hint
are now dead copy for canonical chapters — decide whether the checkbox disappears or stays as a
no-op) → run the ch 5 regen under v1.3 to confirm the model emits unit_handoff in-call and passes
the gate → then Rule 16 into the remaining 24 subject·class constitutions as part of step 3.

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
- polish_plan.py — (2026-07-26) CLI that runs the PRODUCT `run_polish`
  (aruvi_core.genon.polish) over a plan already on disk: `--dry` prints the flagged
  payload and spends nothing; a live run writes the polished twin to
  genon/out/polish_tests/, prints a title/note before-after report with invariant checks,
  and appends a `mode=polish` row to ledger.csv. Inspection lab — the teacher path is the
  Prepare checkbox. NOTE polish_seams.py (the lab original) still carries the OLD retry
  loop; only the aruvi_core copy is fixed.
- out/ch05_stream.json + partitioned/stress outputs

**Product engine (aruvi-saas/aruvi_core/genon/)** — what the API actually runs:
compile.py (v0.3 strict, accepts roles from the Rule-15 `role_handoff` sibling OR inline),
partition.py (v0.3 three-regime + tier-0 seam text), polish.py (tier-1, validated with
one merge-preserving retry). Tests: tests/test_genon_polish.py, tests/test_genon_plan_key.py.

## Deployed to Aruvi SaaS for user Kumar1 — CURRENT as of 2026-07-26

data/content/saved_plans/social_sciences/ix/ holds exactly three files:
- ch_05_canonical.json — the CERTIFIED canonical, 21×50, run 20260726_112240, LP v1.2.1 /
  assessment v1.2, roles in `result.role_handoff` (84/84). plan_status "canonical".
- ch_05_50m16_e03_c20260726112240.json — 16×50 adapted, UNPOLISHED (tier-0 seams visible)
- ch_05_50m16_e03_c20260726112240_p.json — 16×50 adapted, TIER-1 POLISHED (15/16; P3 kept
  tier-0). Both RENAMED to the deterministic key on 2026-07-26 (from ch_05_20260726_120401
  / _123557; `genon.renamed_from` records the old name). The prepared register and section
  9A's state.json were repointed in the same pass; both are cache HITS for a fresh 16×50
  request, so re-running that matrix now costs nothing.
The last two are the A/B pair for judging polish — keep them. Both registered in
data/prepared_plans/Kumar1/Kumar1/prepared.json; both render through the real SS plugin
(17 periods / 29 items / 0 orphans verified on the 17×50 equivalent).
Everything from the 07-23 deployment and every pre-07-25 sample was cleared to
_to_delete/saved_plans_old/ (47 files) — those prepared entries now dangle harmlessly.
Dangling prepared entries for Kumar1 (files long gone, harmless — missing files simply
don't list): ch_05_20260715_215601, the three 07-23 plans, ch_05_20260725_154342, and
ch_05_20260726_123508 — the latter is the DOUBLE-CLICK duplicate: it registered, so the
₹12.73 did produce a plan, which was then removed.


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
- Polish validator — ✅ BUILT 2026-07-25, hardened 2026-07-26. The Haiku-vs-Sonnet question
  is now MOOT for the teacher path (no request-time model at all); the code stays for the
  degraded pre-v1.3-canonical case and for the lab CLI.
- Tier-0 seam text: ✅ CLOSED 2026-07-28 by DELETION, not repair — `_first_clause`, the
  "This period continues … begun last time" template and the "[Next unit]" note join are all
  gone with the tier-0 composer (LP v1.3 Rule 16). Nothing in the request path writes
  container text any more; it is selected from the canonical.
- Polish cost history is SPLIT across two files: the app path logs to
  runtime_data/token_log.csv (`seam_polish` rows), the CLI to genon/ledger.csv
  (`mode=polish`). Unify before the step-8 cost report.
- Partition-time penalty for periods that CLOSE on a hook (5 of 16 at 16×50) — open
  design question, not yet a rule.
- Back-fill script + compiler v0.3 (plugin-fed, strict) — not started.
- Pre-warm checklist entries owed: corpus back-fill; each constitution amendment
  (verified only by live generation); English MCQ etc. items already in MEMORY.md.
- Confusion-keyword survival check after note condensation (belt-and-braces).
- Founder should ROTATE the API key pasted in the 2026-07-23 chat.

## Key measured economics (SS IX ch 5, sonnet-4-6, ₹92/$)

Original generation: ₹67.6, minutes, 19.2k in / 45.1k out. Corpus median lpa ₹24.
Adaptation now: partition ₹0/ms + polish. MEASURED LIVE 2026-07-26 (16×50, 16 flagged
periods, sonnet-4-6): one clean call 8,988 in / 2,626 out = ₹6.10, ~60s; ₹2.04 on
Haiku 4.5; ₹0 on a cache hit. (The lab's ₹1.75–3.88 figures were smaller flagged sets.)
Cache key = (subject, grade, chapter, normalised matrix, canonical version, engine
version, polished) — see DECISIONS LOCKED 2026-07-26.
Recent-corpus cost split: output tokens ≈ 83% of spend — why delta/partition wins.
Batches API halves canonical authoring for the pre-warm sweep.
