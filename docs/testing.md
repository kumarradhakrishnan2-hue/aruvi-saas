# Aruvi SaaS — Test Campaign Plan (the 11-stage certification sweep)

VERSION 2.0 · 2026-08-01 · Actors: **[Kumar]** (runs the pipeline in Terminal, supplies
artefacts) · **[Claude]** (inspects artefacts, checks compliance, reports)

**Supersedes VERSION 1.0 (2026-07-29), the 25-combo partition-era template.** The engine it
certified no longer exists: the deterministic partition engine was retired on 2026-07-31 and
replaced by the variant-canonical serve engine (`docs/variant_canonical_architecture.md`).
Two things changed as a result — the *test object* (a chapter is now a library of authored
variants, served by selection) and the *certification unit* (per subject·**stage**, not per
class). This file is the input brief `docs/testing_rewrite_brief.md` made executable; that
brief and the architecture spec remain the reasoning of record.

This is a working template. The numbered per-stage cycle in §4 is executed once per
subject·stage — 11 times. Results are recorded in the campaign tracker
(`docs/testing_tracker.html`, backed by `/api/testing/*` — see §6a), never in this file.
This file changes only when the *template* changes, and any such change triggers §9.

Read alongside: `docs/variant_canonical_architecture.md` (the spec) ·
`docs/partition_constitution_rollout.md` (what still ports) · `genon/build_library.py` (the
driver) · `.claude/skills/canonical/SKILL.md` (the session flow) · MEMORY.md 2026-07-31.

---

## 1. Purpose and scope

**What is being proven.** That a chapter authored ONCE as a small **library of variant
canonicals** — the top canonical at the master-plan `recommended_periods` plus two (rarely
one or three) compact variants, each a complete plan with its own assessment, all at the
class-standard duration — can be served to any teacher's real timetable **deterministically,
free, in milliseconds, by selection alone**, under every subject's live constitutions.
Secondary aims: prove the synthetically-validated amendments in `MEMORY.md`
§"★ AMENDMENTS TO BE TESTED" against live generation; price the corpus pre-warm in rupees;
prove tenancy on every surface built so far.

**The certification unit is the subject·STAGE.** Constitutions are per stage; classes within a
stage share them, so certifying every class re-proved the same constitution at 2–3× the cost.
Each stage is certified on **ONE randomly chosen class**, whose **one pilot chapter** carries
the full cycle.

**The 11-stage matrix** (the tracker's rows; classes are the *sample*, not the unit):

| # | Subject · stage | Eligible classes | Std duration(s) | Chapters (mappings) |
|---|---|---|---|---|
| S1 | social_sciences · secondary | ix | 50 | 9 |
| S2 | social_sciences · middle | vi, vii, viii | **40 / 45** | 40 |
| S3 | science · secondary | ix | 50 | 13 |
| S4 | mathematics · secondary | ix | 50 | 16 |
| S5 | the_world_around_us · preparatory | iii, iv, v | 40 | 32 |
| S6 | science · middle | vi, vii, viii | **40 / 45** | 37 |
| S7 | mathematics · middle | vi, vii, viii | **40 / 45** | 39 |
| S8 | mathematics · preparatory | iii, iv, v | 40 | 43 |
| S9 | english · preparatory | iii, iv, v | 40 | 39 |
| S10 | english · middle | vi, vii, viii | **40 / 45** | 46 |
| S11 | english · secondary | ix | 50 | 16 |

Corpus totals (re-counted 2026-08-01 from `data/content/chapters/<subject>/<grade>/mappings/`):
english 101 · mathematics 98 · science 50 · social_sciences 49 · TWAU 32 = **330 chapters**.
`master_plan.json` carries **339** chapter rows — the excess are `placeholder: true` rows
(mathematics IX 8, social_sciences IX 9, social_sciences VIII 7) where the calibration
workbook expects a chapter that has no authored content yet. Class X has no content anywhere.

**The random class pick (hard procedure).** For each stage, pick one class from the eligible
list *before* the cycle starts, and record in the tracker **the method, the seed, the
candidate list and the result** — a pick nobody can reproduce is not a random sample, it is a
preference. The standard method:

```bash
python3 -c "import random; s='social_sciences|middle|2026-08-01'; \
c=['vi','vii','viii']; print(s, c, random.Random(s).choice(c))"
```

Eligibility filter, applied before the draw: the class must have at least one chapter with
**both** a summary and a mapping on disk, and a **non-placeholder** `master_plan.json` row for
the chapter that will be used. (Known content gaps to respect at draw time: mathematics/ix has
16 mappings but only 8 `*_summary.json`; science and social_sciences carry `.txt` summaries,
not `.json` — both shapes count.)

**The two-duration residual (S2, S6, S7, S10).** The middle stage spans two standard durations
— 40 min for VI–VII, 45 for VIII — so a random pick can miss one. This is covered
**deterministically, never with more generation**: the certifier's serve sweep and the C6 API
checks run at BOTH durations against the same library (free), and the tracker records which
duration the library was *authored* at. Preparatory (40) and secondary (50) stages are
single-duration; their C6 runs at that duration only.

**Out of scope.**
- **Class X** — maps to secondary in `aruvi_core/grades.py`; no content in any subject.
- The retired partition engine and everything it needed: DP cuts, `CUT_COST`, the three
  compression regimes, `COVERAGE_FLOOR`/`DEV_PACE_FLOOR`, seam text, `role_handoff`,
  `unit_handoff`, wide spans, `mid_unit_openings`, and `band_id`/`band_refs`/`phase_ref` as
  *declarations* (band ids are derived internally). Never tested again; never reintroduced —
  `variant_canonical_architecture.md` §1 records why they failed.
- Live generation *inside the API* (`POST /subjects/{s}/{g}/generate` is an intentional 501
  stub). All generation runs in the founder's Terminal via `genon/build_library.py` (§4, C1).
- Supabase/Phase-4 adapters — everything here tests the file-backed repositories.

**Certification.** A stage is *certified* when every C-step is Pass (or N/A with a recorded
reason) **and the human gate is signed**, under one LP+assessment constitution pair and one
engine version, with provenance (§6) recorded. Deterministic ALL PASS is a precondition, not a
verdict: `build_library.py` never self-approves. The tracker is the register of record.

---

## 2. Step 0 — campaign preconditions (run once, before anything else)

Every step: actor · action · **exit criterion** · artefact.

**0.1 [Kumar] The generation environment (Terminal only).** The Cowork sandbox proxy blocks
credentialed API calls in every mode (proven 2026-08-01: bogus and real keys return identical
plain-text 401s), so every metered run happens on the founder's machine. Confirm:
`runtime_data/anthropic.key` present (git-ignored; never printed or logged),
`runtime_data/token_log.csv` present with its header
(`timestamp,call_type,subject,grade,chapter_number,chapter_title,input_tokens,output_tokens,total_tokens,cost_inr,cache_write_input_tokens,cache_read_input_tokens`),
model pinned `claude-sonnet-4-6` in `genon/generate_canonical.py`.
**Exit:** `python3 genon/build_library.py social_sciences ix 3 --certify-only` runs to a report
without spending a rupee. **Artefact:** the report path + the CSV header line.

**0.2 [Claude] Engine + code state.** Assert `GENON_ENGINE_VERSION = "08"` (`api/data.py`);
`aruvi_core/genon/` contains exactly `compile.py` (v0.5), `serve.py` (v1.1) and
`variant_solver.py` — the retired `partition.py`/`polish.py` are gone from the engine package;
the repo-root `genon/` lab keeps historical copies (`partition.py`, `polish_plan.py`,
`polish_seams.py`) that nothing live imports. **Exit:** `grep -rn "partition\|polish" api/
aruvi_core/ web/app/lib/format.js` shows no live import. **Artefact:** the grep output.

**0.3 [Kumar] Variant plans fresh.** `python3 genon/variant_plans.py` — every chapter row of
`master_plan.json` carries `variant_plan {sigma, counts, closing_spans, provisional, basis,
registry_sections, full_coverage, partials_at}`. **Runbook pair (hard):** `genon/master_plan.py`
regeneration WIPES these rows; `variant_plans.py` must be re-run immediately after it, before
any row is trusted. **Exit:** the annotate pass reports rows written; the campaign's pilot
chapters show `basis: "authored_canonical"` once their tops exist. **Artefact:** the run output.

**0.4 [Kumar] Deploy the campaign tracker.** `api/testing_campaign.py` merged + included in
`api/main.py`; open `docs/testing_tracker.html` (or `GET /api/testing/tracker`) against the
running API. **Exit:** a tick made in the browser survives an API restart (state at
`data/testing/campaign_state.json`). **Artefact:** the state file.

**0.5 [Kumar] Provision the three test identities.** `kumar1`, `kumar2`, `kumar3` (sent as
`X-Aruvi-User`; `tenant_id == user_id`; all-lowercase is the standard — the local filesystem is
case-insensitive and mixed-case variants would collide). Each gets a readiness profile covering
the subjects under test. **Exit:** `GET /readiness` with each header returns `ready: true`.
**Artefact:** the three readiness JSONs.

**0.6 [Claude] Re-verify the matrix and draw the classes.** Recount chapters per subject·class
from `mappings/`; confirm eligibility (§1) per stage; run the eleven draws and record method +
seed + candidates + result per stage. **Exit:** the §1 table matches disk (or is corrected here
with a dated note) and all 11 picks are recorded under step 0 in the tracker. **Artefact:** the
count table + the pick log.

**0.7 [Kumar, founder inputs] Floor and σ per subject·stage.** The solver needs two founder
dials before a stage's library can be solved: `floor_periods_at_standard` (currently derived as
`round(0.6 × recommended_periods)` — the 0.6 ratio is partition-era and open to pedagogical
re-setting) and **σ**, the widest closing synthesis a compact variant may be mandated to anchor
(`SIGMA_DEFAULT = 2` in `genon/variant_plans.py`, per-stage overrides in the `SIGMA` table).
Set both per stage at its P-prep (§3, P5) — this step only confirms the dials exist and the
defaults are consciously accepted. **Exit:** a recorded per-stage floor/σ decision, or an
explicit "default 2 accepted". **Artefact:** the SIGMA table diff (where changed).

**0.8 [Kumar] Quarantine hygiene.** `backup/quarantine/` exists and is EMPTY at campaign start
(a non-empty quarantine is an open fix worklist, and a quarantined file must never be servable).
**Exit:** `find backup/quarantine -name "*.json"` returns nothing.
**Artefact:** the (empty) listing.

---

## 3. Per-stage preparation (P-steps; run before that stage's C-cycle)

> **ORDERING RULE (hard):** every amendment for a stage completes — P1 through P5, versions
> bumped, changelog written — **before that stage's chapter is generated**. Amending a
> constitution after the library is authored invalidates the library (it was authored under the
> older version; see §9). This rule is the whole reason the P-steps are a separate list.

**The constitutional carry-forward is EXACTLY this and nothing more** (founder ruling
2026-08-01; `partition_constitution_rollout.md` §3): **A1 · A5/A7 · A6-confirm · A9 · P3 · P4**.
**A2, A3 and A4 are cancelled; X3 is void.** The reference pair is SS·secondary
**LP v1.10 · assessment v1.5**.

**The V-series is NOT constitutional.** V1 (the variant brief) · V2 (shared section registry,
verbatim anchors, first-visit order) · V3 (the closing-synthesis mandate) · V4 (per-variant
assessment) are carried entirely by the platform-composed **variant brief**
(`genon/variant_plans.py briefs_for`, prepended to the prompt) and enforced in code by the
certifier in `genon/build_library.py`. No constitution carries a V-rule, an INPUTS
acknowledgment, or a precedence line. Brief wording therefore iterates freely at failure speed
— **a brief change is not a constitution change and does not trigger the §9 cascade** (it
triggers the cheaper `--certify-only` re-run; see §9).

Stage state (from `partition_constitution_rollout.md` §2 — re-read the live VERSION lines
before starting each stage):

| # | Subject · stage | LP ver | Band shape | A1 | Register | A9 |
|---|---|---|---|---|---|---|
| S1 | social_sciences · secondary | **1.10 — reference** | time_bands | ✓ | ✓ | ✓ |
| S2 | social_sciences · middle | 2.7 | time_bands | — | — | — (item-18 prohibition to replace) |
| S3 | science · secondary | 1.0 | time_bands | — | — | — (item-18 prohibition to replace) |
| S4 | mathematics · secondary | 1.0 | time_bands | — | — | — |
| S5 | the_world_around_us · preparatory | 1.2 | time_bands | — | — | — |
| S6 | science · middle | 2.1 | phases[] → P3 | — | — | — (item-18 prohibition to replace) |
| S7 | mathematics · middle | 3.3 | phases[] → P3 | — | — | — |
| S8 | mathematics · preparatory | 1.1 | phases[] → P3 | — | — | — |
| S9 | english · preparatory | 1.0 | phases[] → P3 | — | — | — |
| S10 | english · middle | 1.5 | phases[] → P3 | — | — | — |
| S11 | english · secondary | 1.0 | phases[] → P3 | — | — | — |

**P1 [Kumar] Amend the LP constitution** from the SS·secondary v1.10 reference
(`data/content/constitutions/lesson_plan/social_sciences/secondary/lesson_plan_constitution.txt`):
- **A1** — the period schedule is exactly ONE standard row `{duration_minutes, count}` at the
  class-standard duration (40 ≤VII · 45 VIII · 50 IX–X — the master-plan calibration bands, not
  NCF's flat 40). Ports verbatim; doubly load-bearing now, because every variant is authored at
  the standard duration and the serve engine handles all timetable variation. Ten constitutions
  still say "one or more rows" or a subject equivalent.
- **A5 + A7 — THE SELF-CONTAINED REGISTER, ported as ONE block** beside VOCABULARY (never as
  scattered prohibitions), in the **v1.10 re-cut**: three bans only — (1) **clock quantity**
  (proportional scaling silently falsifies stated numbers), (2) **forward reference /
  completion language** (X varies per teacher, so ANY unit may be terminal or may precede a
  companion variant's unit — this ban is global, not a tail concern), (3) **calendar time**
  (Calendar Purge doctrine). **Backward references are now LEGAL**; content-named continuity is
  stated best practice, not prohibition. Known direct contradiction to strike where present:
  english·middle's schema comment "Transition from prior unit; preview into next" (the forward
  half is still banned).
**Exit:** the amended file carries A1 + the one-block register; `VERSION` bumped; a diff against
the pre-amendment file shows no pedagogical rule changed. **Artefact:** amended file + diff.

**P2 [Kumar] The assessment constitution — A6-confirm + A9.**
- **A6 is a CONFIRMATION, not an amendment:** every item must carry its anchor **unit**
  (`period_ref`, or that subject's equivalent, copied from the LO row consumed). Verify; amend
  only where absent. The v1.2-era band-level `phase_ref` is reversed and must not be
  reintroduced.
- **A9 — MCQ option order is a convention, not a choice:** options arranged alphabetically from
  the first word at which they differ (ascending where numeric) as the LAST step before
  emission, correct answer never led with. Applies to all eleven assessment constitutions;
  **replaces** the MEMORY-item-18 position prohibition outright in the four files that carry it
  (SS + Science, middle and secondary) — do those four first, their prohibition is known not to
  hold. **Standing corpus-repair debt:** already-saved SS and Science plans carry clustered
  answers; the repair pass reorders into convention order, never shuffles.
**Exit:** `VERSION` bumped; anchor requirement present; A9 clause present.
**Artefact:** amended file + diff.

**P3 [Kumar] Group B only — schema conversion.** Convert `phases[{minutes, description}]` →
`time_bands[{minutes, activity}]` (rename both the array and the `description` key). **No
`band_id` in the target shape** — the conversion shrank when the band layer left the
declaration surface. The compiler reads exactly `time_bands` and `activity`; the decision
stands to amend constitutions, not to teach `compile.py` an adapter.
**Exit:** the schema block emits `time_bands` with both keys; no `phases[` remains.
**Artefact:** diff.

**P4 [Kumar] History to the sidecar.** The amendment note goes to `CHANGELOG.md` beside the
constitution, never into the file; the `VERSION` line stays in the file.
**Exit:** no version-history block in the constitution; `CHANGELOG.md` lists every bump with
date and one-line rationale. **Artefact:** the changelog.

**P5 [Kumar + Claude] Stage inputs for the solver (pipeline, not constitution).**
1. **Floor and σ** for this stage (§0.7) — set or default-accepted, recorded.
2. **The section registry definition where the section model is non-obvious.** English's
   split-chapter / spine model must have its registry defined *before* its variants are
   authored — the fill ladder is string arithmetic on `section_anchor` values drawn verbatim
   from the chapter summary's section list. This decision lands in the pipeline (summary +
   brief), never in a constitution.
3. Confirm the drawn class's pilot chapter has summary + mapping and a non-placeholder
   `master_plan.json` row with a `variant_plan`.
**Exit:** all three recorded. **Artefact:** the note + the chapter's `variant_plan` row.

**[Claude] Stage sign-off:** read the amended pair against the reference and the rollout brief;
confirm A1 lands, the register is ONE block in the v1.10 three-ban form, A6 anchors are present,
A9 is in, P3 converted (Group B), and no cancelled amendment (A2/A3/A4) or V-rule has crept into
a constitution. **Exit:** a written note per item — present / absent / deviates-with-reason.
**Artefact:** the note; the stage's C-cycle is then unblocked.

---

## 4. The per-stage cycle (the repeating numbered template — run 11 times)

Precondition: P1–P5 signed off for this stage; the class is drawn and recorded; the pilot
chapter is chosen (prefer a mid-book chapter with ≥3 sections, non-placeholder row).

All API calls: base `http://localhost:8000`, identity via `X-Aruvi-User`. The C6 serve requests
split across identities as the standard: **kumar1 runs the identity requests; kumar2 runs the
between-variant and below-floor requests; kumar3 runs the mixed-duration weekly matrix** — this
is what makes C10 and X1 meaningful.

**C1 [Kumar] Build the library (Terminal, metered).** One command:

```bash
python3 genon/build_library.py <subject> <grade> <chapter>
```

which runs, stopping on the first failure and idempotent to re-run: top canonical (LP +
assessment, `ch_NN_canonical.json`) → `variant_plans.py` annotate (the row finalizes:
`provisional: false`, `basis: "authored_canonical"`) → briefs written to `genon/out/briefs/`
→ each compact variant with its brief (own assessment; installs `ch_NN_canonical_pKK.json`) →
re-annotate → deterministic certification → report in `genon/out/library_reports/`.
`--certify-only` re-runs the free steps. **Never author an installable plan in a Cowork
session** — a session-authored plan is a draft on an uncalibrated model.
**Exit:** the library on disk matches `variant_plan.counts`; `GET /genon/{subject}/{grade}/chapters`
lists the chapter and `canonical_minutes` = standard duration × top period count.
**Artefact:** the library files + the report path.

**C2 [Claude] Cost the LIBRARY.** From `runtime_data/token_log.csv`, record per generation
(`canonical_generation` for the top, `variant_generation` per compact, plus any rerun) —
timestamp, input tokens, output tokens, cost ₹ — and the **library total ₹**, including failed
runs that had to be redone (a rerun is part of what the chapter cost). **Exit:** every row for
this chapter is attributed; the total is in the provenance panel; a missing cell is recorded as
missing, not blank. **Artefact:** the cost table. *Benchmark from the SS·IX ch 3 pilot
(2026-08-01): top ₹39.43 + variants ₹36.51 and ₹35.05 + one defect rerun ₹34.71 = **₹145.70**
all-in; ~₹120–190 per library is the working expectation, so the 330-chapter corpus is
≈ ₹30–40k synchronous / ₹15–20k at batch pricing (batch mode deferred to the mass pre-warm).*

**C3 [Claude] Canonical + one compact variant vs the stage constitution, rule by rule.** Check
both files against every numbered rule of the stage's current LP constitution (and the
assessment constitution for the item files), citing rule numbers — a table `rule # → pass /
fail / subjective-pass with quoted evidence`, not a general impression. Register and tone
judgements are subjective: say so, and quote the strings the judgement rests on. Checking a
compact variant too is deliberate — the variants are authored under the SAME constitution plus
the brief, and a constitution that only holds at full length has not been proven.
**Exit:** every rule number appears in the table for both files; every fail becomes a defect
(§7). **Artefact:** the rule table.

**C4 [Claude] MEMORY.md amendment items, live.** From the checklist in `MEMORY.md`
§"★ AMENDMENTS TO BE TESTED", test the items that apply to this stage — several are themselves
per-stage tests. Applicability map (re-check against the current list before use; items
summarised):

| Item | Applies to | Item | Applies to |
|---|---|---|---|
| 1 guide.{TYPE} nesting | SS + TWAU (assessment) | 10 named referenced word | english mid+sec |
| 2 MCQ keyed reveals | english | 11 homework (p.NN) | english (all) |
| 3 exact item counts | all subjects | 12 FILL_IN table dedup | english (all) |
| 4 split chapters regenerate | english prep/middle/sec | 13 narrowed A/B ban | english (all) |
| 5 task_density cutoffs | english middle (see X2) | 14 number_line stimulus | maths prep+mid |
| 6 time vector — closed by design* | (see note) | 15 homework book_ref | maths (all 3 stages) |
| 7 empty approach OK | maths prep, SS | 16 inclusivity {support, challenge} | maths middle |
| 8 FILL_IN/MATCH shapes | english prep | 17 SS teacher_notes | SS middle |
| 9 Jul 12–13 wave contracts | per its file list | 18 MCQ position spread | **superseded by A9** |

\* Item 6 ("wire time into the constitutions" as a duration vector) is **closed by design**: A1
fixes one standard row and the serve engine owns every timetable variation. Item 18 is
**superseded by A9** (a convention replaces a prohibition) — check the convention, not the
spread. Record both closures in MEMORY.md the first time they come up.
**Exit:** each applicable item gets pass / fail / n-a-here with one line of evidence from the
live artefacts; fails become defects. **Artefact:** the item table.

**C5 [Claude] Read the certification report — ALL PASS required.** Open the newest
`genon/out/library_reports/<subject>_<grade>_chNN_<ts>.md` and confirm each deterministic check
(implemented in `genon/build_library.py::certify` — cite it, do not re-specify it):
1. **library complete** — the files on disk match `variant_plan.counts`;
2. every file **compiles** (`compile_stream`, v0.5);
3. **anchors verbatim** — every unit's `section_anchor` resolves in the top canonical's registry;
4. **first-visit order** — new sections appear in registry order (synthesis tails that revisit
   earlier sections are legal; skipping a section is not);
5. **coverage reaches the final registry section**;
6. **closing mandate** — each compact variant's last unit anchors exactly its mandated last-k
   span from `variant_plan.closing_spans`;
7. **serve sweep** — X from `floor − 2` to `top + 2`, each X producing a mode
   (`identity | exact | superset | suffix | synthesis | truncation | surrender`) with no
   exception raised;
8. **projected-vs-actual** — every X the solver projected as full coverage is served by a
   full-coverage mode.
**Also:** `backup/quarantine/<subject>/<grade>/` must be EMPTY for this chapter. Failed files
are moved there automatically (founder doctrine 2026-08-01: passing files stay live, only
failures move; a failed TOP takes its whole library with it). If `partials_at` is non-empty in
the master-plan row, raise it — that is a σ / variant-count decision, not something to paper
over. **Exit:** report says ALL PASS; quarantine empty; `partials_at` empty or founder-accepted.
**Artefact:** the report + the sweep table.
*Pilot lesson to keep in view: the first 7-period variant of ch 3 silently DROPPED a section
with no coverage note; the **first-visit check caught it, the serve sweep did not** (X=7 is an
identity request and served the defect happily). Certification catches what serving cannot.*

**C6 [Kumar] API serve checks — the teacher-facing path.** `POST /genon/{subject}/{grade}/{ch}/plan`
with `{"rows": [{"duration": D, "count": X}, …]}`. For a library `{A_top … A_mid … A_low}` run,
at the class-standard duration:

| Request | Identity | Expect |
|---|---|---|
| X = each variant's own count | kumar1 | `identity: true`, that variant's own filename, **no new file saved** |
| X between two variants (superset/runway) | kumar2 | 200; `serve.slot_fill.mode` = `superset`; coverage note names the re-crossed sections |
| X between two variants (exact fill) | kumar2 | 200; `mode` = `exact`; no coverage note needed |
| X = A_top + 1 | kumar2 | 200; `serve.surrendered_periods` ≥ 1 and `surrender_note` names the returned minutes |
| X = floor − 1 (below floor) | kumar2 | 200; `mode` = `suffix` or `truncation`; `coverage_note` names exactly what was not scheduled |
| mixed-duration weekly matrix | kumar3 | 200; the plan this stage's C7/C9/C12 inspect |

**Where the stage spans two durations (S2/S6/S7/S10), run the whole table at BOTH 40 and 45**
against the same library, and record which duration the library was authored at. Note the
nuance: **identity only fires at the authored duration** — at the other duration the same X
serves the variant whole with proportional scaling and writes a file; assert scaling + exact
tiling there, not identity.
**Mixed matrix (weekly dispersion, the one keeper from v0.4):** assert from `genon.duration_sequence`
that the shortest sitting opens the week and long sittings sit interior and never adjacent.
**Exit:** every row returns as expected; responses recorded. **Artefact:** the responses + files.

**C7 [Claude] Register scan on teacher-facing text.** On the C6 plan files (and the library
files), every teacher-facing title and note is checked against the **v1.10 three bans**:
1. **clock quantity** — any stated number of minutes/hours/fractions of a period in band or note
   text (proportional scaling would falsify it);
2. **forward reference / completion language** — "next period", "we will finish", "in the final
   session", "by the end of this chapter you will have…";
3. **calendar time** — days, weeks, "yesterday", "tomorrow", "last week".
**Backward references are legal now** — the old word-list's positional entries (previously,
earlier, first/second half, "the last class") are RETIRED as automatic hits; a backward
reference is a defect only if it also names a clock quantity or a calendar word. Mechanical
first pass is a case-insensitive scan (minute, hour, half an hour, day \d, yesterday, tomorrow,
next class|period|week, "we will complete", "by the end of the chapter"); subjective second pass
on survivors, quoting every judged string.
**Exit:** zero live-ban hits, or a defect per hit. **Artefact:** the scan table.

**C8 [Claude] LLM-need flags.** Note every point in the stage's flow where output quality begs
an LLM call (e.g. a borrowed closing unit whose note reads oddly beside the prefix it lands
after). **Exit:** a (possibly empty) list, each entry with the deterministic alternative to try
first — the constraint is unchanged: **no LLM in the request path.**
**Artefact:** the list, in the tracker comment.

**C9 [Claude] Assessment anchoring across the serve.** Anchoring is UNIT-level: `compile.py`
normalizes `period_ref` (the identity) — legacy `phase_ref` as fallback — onto `unit_ref`, and
`serve.py` remaps unit → sitting. On the C6 plans check:
1. **Prefix remap** — every chosen-variant item whose anchor unit is served carries a
   `period_ref` pointing at that unit's SITTING number;
2. **Borrowed unit brings its own items** — on a fill serve, the fill unit's items come from
   its HOME variant and are anchored to the fill sitting (last sitting), not to a
   chosen-variant unit;
3. **Unserved anchors** — on the below-floor serve, an item whose anchor unit was not scheduled
   carries `scheduling_note: "anchor unit not scheduled in this plan (time budget)"` and an
   empty `period_ref`, rather than mis-anchoring to a surviving unit;
4. **No cross-variant references** of any other kind.
**Exit:** zero mis-anchored items; every unserved-anchor item carries the note.
**Artefact:** the anchor table per plan.

**C10 [Claude] Storage conventions.**
1. Library files: `ch_NN_canonical.json` + `ch_NN_canonical_pKK.json` (KK = the variant's
   period count, zero-padded). Served plans: exactly
   `ch_NN_<matrix>_e08_c<chosen-variant-version>.json`, `<matrix>` duration-aggregated
   longest-first (`50m10`, `60m3-45m9`) and the version being the **chosen variant's**
   `ledger_ts` — not the top canonical's (`api/data.py::genon_plan_filename`).
2. **Cache hit** — repeat one C6 non-identity request: response has `cached: true` and the
   file's mtime did not change.
3. **No overwrite across engine versions** — any pre-campaign `_e06_`/`_e07_` file for this
   chapter is still on disk untouched beside the new `_e08_` files.
4. **Determinism** — delete one C6 plan file, re-run the same request: the new file is
   byte-identical except the top-level `saved_at`
   (`diff <(jq 'del(.saved_at)' a) <(jq 'del(.saved_at)' b)` empty).
5. **Quarantine is invisible to serving** — move one compact variant into
   `backup/quarantine/…` and re-run a request that had been served by it: the library glob no
   longer sees it, the serve falls to the next-highest surviving variant, and no response ever
   names the quarantined file. Restore it afterwards.
**Exit:** all five hold. **Artefact:** filenames + the empty diff + the quarantine transcript.

**C11 [Claude] Serve wall time.** Time a **cache-miss** C6-style request (delete the file first,
or use a fresh matrix): `curl -w '%{time_total}'`. **Exit:** total < 5 s — anything over is a
defect; record the actual figure either way (selection + one compile should be milliseconds).
**Artefact:** the timing.

**C12 [Kumar runs, Claude inspects] Exports.** For the C6 mixed-duration plan — and it must be
one that includes a **borrowed fill sitting** — all three plan exports
(`GET /api/plans/{s}/{g}/{filename}/export/{lesson|assessment|integrated}`) in both
`format=pdf` and `format=docx`, plus the allocation report (`POST /api/allocation/export-pdf`
and `export-docx`) for this subject·grade. View-model shapes differ by subject (science·ix
section-anchored flat; science middle stage-grouped; english spine-nested) — the export must
render this stage's shape cleanly. **Exit:** 8 files open without error; no blank sections, no
raw JSON leaking, unit/phase structure visible and matching the plan, the borrowed sitting
reading as a whole unit, `answers=1` rendering the answer layer, and the coverage note carried
through. **Artefact:** the 8 files.

**C13 [Kumar breaks, Claude reads] Failure paths.** Each must surface a message a teacher can
read, with no stack trace in the body:
1. **No canonical** — a chapter number with no library → **404** `"No canonical for this
   chapter yet."`
2. **Implausible matrix** — total periods > 60 → **400** `"Period count implausibly large."`
   (and an empty `rows` → **400** `"At least one duration row is required."`)
3. **Unresolvable item anchor** — copy the canonical to a scratch chapter number, point one
   assessment item's `period_ref` at a non-existent unit, request a plan → **500**
   `"Canonical cannot be compiled: …"` naming the item, not a bare 500. Remove the scratch
   file afterwards.
4. **Quarantined variant absent from serving** — the C10.5 transcript, read as a failure path:
   nothing 500s, and the response names only live files.
**Exit:** the codes + readable details; nothing resembling a traceback in any body.
**Artefact:** the four responses.

**HUMAN GATE [Kumar decides, Claude presents] — the stage's sign-off.** Deterministic ALL PASS
is a precondition; this is the verdict. Claude presents, and the founder rules on:
- the **projected-vs-actual adaptation table** diff;
- the **full text of 2–3 borrowed-seam sittings** (a prefix unit followed by the borrowed
  closing unit) read as a teacher would meet them;
- **each compact variant's closing-synthesis unit in full** — does it close the chapter as a
  real unit-arc, or is it a summary lecture wearing a unit's clothes? (That verdict is what
  feeds σ back to the solver.)
- any **register scan hits** from C7.
The gate never self-approves and never disappears; in a batch pre-warm it may sample at a rate
the founder chooses. **Exit:** a recorded verdict. The stage row turns green only after it.

---

## 5. Cross-cutting checklist (run once; re-run on any material change)

**X1 [both] Tenancy, every surface built so far.** With `kumar1`, `kumar2` and `kumar3` (each
having run their C6 share):
1. `GET /plans-prepared` — each sees exactly the keys they created; no overlap beyond plans both
   prepared. (Note the identity rule: an identity request registers the *variant file itself* as
   prepared — two teachers requesting the same variant legitimately share a filename.)
2. `GET /plan-archive` + archive/restore — kumar1 archives a plan; kumar2's listing is
   unaffected; restore returns it; `GET /plans/{s}/{g}` shows per-caller `archived` flags.
3. `GET/POST/DELETE /section-state` — progress + bookmark isolated per user.
4. `GET /readiness` — profiles stay distinct; the 409-cascade guard fires for a destructive edit
   and cascades only with `cascade: true`.
5. Allocation — `save_allocation` / `GET allocation` / `DELETE` isolated per user for the same
   subject·grade.
6. **The authorization case, not just visibility:** as kumar2, fetch a plan only kumar1 prepared,
   by filename: `GET /plans/{s}/{g}/{filename}/view` and the three export routes. These take a
   filename and do not consult the prepared-plans register. **Expected under the current design:**
   the fetch succeeds — plan files are shared Bucket-A content and per-teacher scoping is by
   register, not file ACL (CLOUD_DATA_MODEL). Record verbatim and put it to the founder as an
   explicit accept/reject: rejected → S2 defect; accepted → written into CLOUD_DATA_MODEL.md as
   a stated property.
7. **Chapter notes** — the API exposes `section-state` (bookmark + progress) and **no notes
   endpoint**. Notes are client-side only: they stay in the browser profile that wrote them.
   Record as a known limitation, not a tenancy defect.
8. **Archived plans stay out of circulation (fix landed 2026-08-01).** An archived plan is
   excluded from the section-attach chooser (`MyPlans.jsx`) and never fronts the guided tour.
   Verify both. **Two open judgment calls to put to the founder while here:** (a)
   `PrepareLesson.jsx` excludes archived plans from `committed`, so archiving a chapter makes it
   "not yet prepared" again on the Prepare screen — intended? (b) `YearPlan.jsx` still counts
   archived plans in "Your plan" periods — the two screens disagree, and one of them is wrong.
**Exit:** 1–5 show zero leakage; 6, 7, 8 recorded with founder decisions.
**Artefact:** paired-request evidence (request + header + response) per check; screenshots for 8.

**X2 [Claude] Effort index vs the calibrated standard.** On the Year Plan page of My Lessons:
per-chapter `recommended_periods` and effort weights must match
`data/content/allocation_norms/master_plan.json` (calibrated first,
`recommended_source: "master_plan"`; NCF fallback only where the master plan has no row — shown
alongside, never driving the default). Verify for one grade per subject against
`GET /subjects/{s}/{g}/chapters` (which also carries `variant_plan` per chapter now — confirm
the row shown is the finalized one, not a stale provisional after a `master_plan.py` run).
**English caveat (MEMORY item 5):** the `task_density` cutoffs (≤2.0 / 2.1–2.9 / ≥3.0) were
calibrated on VI and reused for VII and VIII with an admittedly weak fit — for English the
*standard itself* is in question, not merely conformance. For english middle, additionally
report the raw `task_density` distribution per grade; if a grade collapses to a near-binary tier
signal, file a defect against the *calibration*, owner founder.
**Exit:** page values == API values == master plan for the sampled grades; the English
distribution report exists. **Artefact:** comparison table + distribution note.

---

## 6. Provenance block (recorded for every run — a result that cannot be attributed to a version is not a result)

| Field | Source |
|---|---|
| Subject · stage · **class drawn** (+ seed/method) | the §0.6 pick log |
| Pilot chapter number | tracker |
| LP constitution version | `VERSION` line of the stage's LP constitution |
| Assessment constitution version | `VERSION` line, assessment side |
| `GENON_ENGINE_VERSION` | `api/data.py` (08) |
| **Variant plan row** | `master_plan.json` → `variant_plan {sigma, counts, closing_spans, basis, registry_sections, full_coverage, partials_at}` |
| **Brief identity** | the brief files in `genon/out/briefs/` for this chapter — record the git commit of `genon/variant_plans.py` (which composes them) and keep the brief text as an artefact; brief wording is version-bearing even though it is not constitutional |
| Canonical + variant `ledger_ts` | `genon_canonical` block of each library file |
| Certification report path | `genon/out/library_reports/…` |
| Plan filename(s) | C6 responses |
| Model | pinned `claude-sonnet-4-6` (record if it ever differs) |
| Date · wall time | run date; per-serve timing (C11) |
| Tokens in / out · cost ₹ | per generation + **library total** (C2) |

## 6a. Recording surface

State lives **in Aruvi itself**: `GET/PUT /api/testing/campaign` and
`POST /api/testing/campaign/item`, persisted at `data/testing/campaign_state.json` (atomic
writes). The UI is `docs/testing_tracker.html`, also served at `GET /api/testing/tracker`; it
renders §2–§5 as tickable steps with comments, the §7 register, the §8 matrix, and exports
comments/defects as CSV/JSON. Tracker item keys retired by this rewrite simply go unread; the
state file is never hand-edited.

---

## 7. Defect register

One row per defect, in the tracker (exportable):

`id` (ARV-D-001…) · `scope` (`stage:<subject>·<stage>` / `campaign`) · `step` (0.x/Pn/Cn/Xn) ·
`severity` · `title` · `evidence` (file/response/quote) · `owner` · `status`
(open / fixing / fixed-awaiting-recheck / closed / accepted) · `opened` / `closed` dates.

**Quarantine is the fix worklist for generation defects:** a defect on a library file links to
its quarantined path under `backup/quarantine/<subject>/<grade>/`, and closes only when the
regenerated file passes `--certify-only` and the quarantine entry is cleared. Fixes happen
upstream — regenerate, harden the brief, adjust σ — **never by hand-editing an artefact**.

Severity scale — definitions, not vibes:
- **S1** — the chain is broken: a library cannot be generated or certified, a serve is wrong or
  >5 s, data loss, tenancy leakage on a register. Stops the stage.
- **S2** — teacher-visible wrongness: a dropped section without a coverage note, mis-anchored
  assessment, register violation in teacher-facing text, export renders wrong/blank, a
  quarantined file reachable by serving. Stage cannot certify until fixed or founder-accepted.
- **S3** — contract drift a teacher wouldn't see: naming/key deviations, missing report fields,
  a stale `provisional` row. Certify allowed with the defect open and owned.
- **S4** — cosmetic / doc / advisory. Never blocks.

Fixes that touch a constitution, the engine, the brief or the master plan trigger §9.

---

## 8. Progress tracker (the 11 rows)

Maintained live in the tracker UI; the canonical column set per stage:

`P1 P2 P3 P4 P5 · stage-sign-off` — then `C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 C13 · GATE`.
Step 0 and the cross-cutting X1–X2 sit above the matrix.

Rows: social_sciences·secondary · social_sciences·middle · science·secondary ·
mathematics·secondary · the_world_around_us·preparatory · science·middle · mathematics·middle ·
mathematics·preparatory · english·preparatory · english·middle · english·secondary.
Each row's header carries the drawn class and the pilot chapter.

---

## 9. Regression rule

**A change mid-campaign re-opens what it invalidates — but the three kinds of change cost
wildly different amounts, and must never be conflated:**

- **Constitution change (stage-scoped, expensive):** the library was authored under the old
  version, so the stage **re-certifies in full** — C1 regenerates the whole library and C1–C13 +
  the gate re-run. This is the cost the §3 ordering rule exists to avoid: amend first, certify
  after.
- **Engine / brief / certifier change (corpus-wide, cheap):** the authored artefacts are still
  valid. Re-run `python3 genon/build_library.py <subject> <grade> <ch> --certify-only` across
  every certified chapter and **diff the reports** — same checks, same serve sweep, no rupees.
  Identical sweeps → stages stay certified with the new version recorded in provenance. Any
  changed line → re-run C6–C12 on that chapter. (An engine change that alters served bytes also
  bumps `GENON_ENGINE_VERSION`, which re-keys the cache: every prior `_eNN_` plan file is stale
  by construction, never overwritten.)
- **`master_plan.py` regeneration (data, silent):** it **wipes every `variant_plan`
  annotation**. Re-run `python3 genon/variant_plans.py` immediately; until then no row —
  counts, closing spans, floor, coverage projection — may be trusted, and no certification that
  cites one is valid.

The tracker marks re-opened stages amber automatically when a provenance version differs from
the current campaign versions; it never silently keeps green.

---

## 10. Pilot — social_sciences · secondary (chapter 3), and what it already proved

The pilot doctrine stands: run the whole template end to end **once** before any other stage —
template defects found here cost one chapter; found at stage 8 they cost eight.

**The SS·secondary stage is the pilot, and its C-steps are done in substance** (2026-08-01,
chapter 3, class IX at 50 min):
- Library `{12, 9, 7}`, σ = 2, floor 7 (floors now round to **nearest**, not ceil — 143 rows
  corrected; `master_plan.md` retired, the JSON is the single artefact).
- Costs: ₹145.70 all-in including one defect rerun (C2 benchmark above).
- **The defect that taught the most:** the first 7-period variant silently dropped a section
  with no coverage note. The **first-visit check** caught it; the **serve sweep did not** (X=7
  is an identity request). The fix was **brief wording** — a total-coverage clause — plus one
  ₹35 rerun. Three lessons this template encodes: certification catches what serving cannot;
  briefs iterate at failure speed precisely because they are not constitutional; and Rule 4's
  shortfall note is not available to variants.
- Final serve table, all PASS: X=5, 6 suffix (below floor — honest partials by design) · 7
  identity · 8 superset (runway) · 9 identity · 10 exact · 11 synthesis · 12 identity · 13–14
  surrender.

What the pilot still owes before the template is declared portable: the **human gate** read in
full (borrowed seams + each closing synthesis), C7/C9/C10/C12/C13 recorded against the tracker,
and a **template retro** — every step whose instruction was ambiguous or whose exit criterion
was uncheckable gets rewritten here before stage 2.

---

## 11. Suggested execution order (after the pilot)

Ordered to retire the riskiest portable assumptions earliest and spend the five Group-B schema
conversions late; one stage fully signed off before the next stage's prep begins.

1. **social_sciences · middle** (S2, time_bands, same subject family as the pilot) — the
   cheapest proof that the template ports at all, and the first **two-duration** stage (40/45),
   so the dual-duration C6 procedure gets exercised while attention is fresh. Carries MEMORY
   item 17 and the A9-replaces-item-18 case.
2. **science · secondary** (S3, time_bands) — first stage outside the SS family; the
   section-anchored flat export shape (C12).
3. **mathematics · secondary** (S4, time_bands) — confirms the port generalises; the
   cognitive-demand hinge (item 9); note its content gap (8 of 16 chapters have no summary —
   draw the pilot chapter from the eight that do).
4. **the_world_around_us · preparatory** (S5, time_bands) — completes the time_bands group;
   first preparatory stage; item 1 applies.
5. **science · middle** (S6, first Group B) — the cheapest `phases[]` → `time_bands`
   conversion (P3); stage-grouped export shape; two durations.
6. **mathematics · middle** (S7), then **mathematics · preparatory** (S8) — Group B with the
   `core_/adjunct_competencies` skill layer; items 14, 15, 16.
7. **english last: secondary (S11) → middle (S10) → preparatory (S9)** — deliberately final:
   three separate stage preps, the largest chapter count (101), the spine-nested export shape,
   the heaviest MEMORY burden (items 2, 4, 5, 8–13), the open X2 calibration question, and the
   one **registry-definition decision** (P5.2) the fill ladder depends on. By the time English
   starts, the template is boring and only the subject is hard.

Rationale in one line: the pilot proves the template; SS·middle proves it ports and covers the
dual-duration case; science·secondary proves it ports off the pilot's subject family; the rest
is repetition with known risk retired in order of cost.

---

## Corrections note (repository vs brief, checked 2026-08-01)

Verified against the repo before writing: `GENON_ENGINE_VERSION = "08"` (`api/data.py`);
`aruvi_core/genon/` holds only `compile.py` v0.5 · `serve.py` v1.1 · `variant_solver.py`;
`genon/build_library.py` implements exactly the eight certification checks
listed in C5, quarantines to `backup/quarantine/<subject>/<grade>/` with a timestamp suffix,
and sweeps `floor − 2 … top + 2`; serve fill modes are `exact | superset | suffix | synthesis |
truncation` plus `identity` and `surrender`; the genon route's error strings are as quoted in
C13; served-plan filenames key on the **chosen variant**; `variant_plan` rows carry
`{sigma, counts, closing_spans, provisional, basis, registry_sections, full_coverage,
partials_at}` with `SIGMA_DEFAULT = 2`; SS·IX ch 3 is on disk as `{12, 9, 7}` with its report;
`token_log.csv` distinguishes `canonical_generation` / `variant_generation`; the archive
exclusions of X1.8 are in `MyPlans.jsx` (attach chooser + tour) and `PrepareLesson.jsx`, while
`YearPlan.jsx` has no archived filter.

Two corrections to the inputs, both minor: the certifier's serve sweep at the 14:57 pilot report
shows X=6 as `exact` where the brief's final table says `suffix` — the brief's table is from the
post-fix library and is the one to expect; and the "band ids namespaced F…" note carried in
CLAUDE.md no longer describes the code — borrowed items are appended anchored to the fill
sitting, with no band namespacing, because band ids left the declaration surface entirely.

Two stale version strings found in passing, each a one-line fix for whoever touches the file
next (neither changes anything above): `aruvi_core/genon/serve.py`'s module docstring still says
"v1.0" while the engine tag it emits in every response says v1.1; and
`lesson_plan/mathematics/middle`'s footer says "Version 3.1" against its authoritative header
VERSION 3.3 — fold that one into S7's P4.
