# Aruvi SaaS — Test Campaign Plan (the 11-stage certification sweep)

VERSION 2.9 · 2026-08-09 · Actors: **[Kumar]** (runs the pipeline in Terminal, supplies
artefacts) · **[Claude]** (inspects artefacts, checks compliance, reports)

*2.9 (2026-08-09, after S4's C3): **C3 gains a MATHS-ONLY sub-check — every determinate answer
is re-derived, and it is re-derived from the STEM.** S4's C3 found one wrong answer in 23
(ARV-D-084: `8(3m − 2n)^2` against a stem asking for `72m^2 − 48mn + 8n^2`), shipped with
`verified: true` and with the model's own "wait, verify… Let me re-check" aside left in
`method_one_line` — where it had already reached the right answer. Nothing in the pipeline
looks at answer VALUES: the certifier checks structure, STEP 6 checks option order, and
`verified` is the model's claim about itself. **Mathematics is the only subject with exposure**
— a sweep of all 16 installed canonicals found science and social_sciences carry zero items
with an `expected_answer` (they ship `expected_elements`/`look_for`, which are judged, not
computed), so the check is scoped to S4/S7/S8 and costs the other eight stages nothing.
Mechanism: `genon/extract_determinate.py` writes a per-chapter sympy worksheet (extraction is
mechanical); the checker fills in `claimed` and `target` and runs it (transcription is
judgement). **The ordering rule is the whole check** — transcribe from the question, read
`method_one_line` only after the verdict is recorded, or you confirm the file against itself.
Filled worksheets are C3 artefacts. The same sweep found a SECOND leak of the same kind —
science·IX ch 8 `p07` item 4, in the student-facing stem, on a stage already green at C3
(ARV-D-085) — so a `--certify-only`-time regex for self-correction markers is recorded as a
C5 tooling gap. §9 applies and costs nothing: no stage carries a signed human GATE.*

*2.8 (2026-08-08, at S4's P-prep): **two per-stage preconditions on C1 are promoted into §3,
both found at P-prep, neither constitutional.** (a) **The CARRIER, and it is a PAID gate, not a
free one.** `aruvi_core/genon/carriers.py`'s `_NOT_YET` table still lists **mathematics and
english**, and `assessment_items()` raises `CarrierNotImplemented` on a listed subject — so six
of the eleven stages cannot be certified. But the raise fires at `certify()`
(`build_library.py:514`), **after** metered STEP 1 and STEP 4, and `generate_canonical.validate`
swallows it into a silent pass on the way, so a full library is authored and paid for first and
the failure is then misreported as "does not compile" for every file. `_NOT_YET` must now be
read BEFORE every stage's C1 and a listed subject treated as a hard gate on SIGN → C-cycle,
tracked like S6's engine gate — the build is not a safety net. The entries are keyed by SUBJECT,
so deleting one opens every stage of that subject, including stages in a different carrier
family. (b) **The synthesis unit's handoff row.** On a DERIVED-anchor stage (science·secondary,
mathematics·secondary, science·middle) an item reaches its unit only through
`coverage_handoff.period_numbers`, so the v2.0-mandated synthesis unit can carry no items unless
it has a handoff entry — which makes C9.2 unsatisfiable on exactly the Case-1 borrow C8
inspects. Verified on the CERTIFIED science·IX ch 8 library: the model invented a synthesis
handoff entry and **no item anchors to it** (item `section_number`s run 1–10; stamped
`unit_ref`s never reach 12), so this is a live defect against S3, not only an S4 risk.
`top_brief_for` was silent on it. **Both (a) and (b) are FIXED in this same pass** — the carrier
landed as a delegation of 8-rule row 6, the pre-flight became a real gate, `validate` stopped
swallowing the refusal, and the brief now asks for the synthesis row on derived-anchor stages
only; `tests/test_genon_carriers.py` went 25 → 36 green. No constitution moved, so being V-series
none of it enters one. **(c) §3 gains a new P-step, `P5.5` — THE CARRIER**, so (a) is never met as a
surprise again. It writes down the settled doctrine that genon does not invent linkage: the
**verified 8-rule table** (`docs/architecture-plan.md` §"Link resolution", restated in
`link_resolver.py`) is the single source of truth, `carriers.py` is that table exposed to genon,
and a stage's carrier work is a DELEGATION of what the subject plugin already does for the app —
which is how S1, S3 and S6 were done and how S4 (rule 6) proceeds. P5.5 requires a four-part
trace, gates **C1** (not C6, as P5.4 does), and carries the two warnings that make it a
pre-flight READ rather than a run: `_NOT_YET` is keyed by subject so one deletion opens sibling
stages in another family, and the build spends the money before it checks. The [Claude] sign-off
checklist now fails a stage note that does not mention the carrier. §3 also gains S4's landed
pair (LP v1.1 · assessment v1.1) and the note that
**A9's removal was N/A for S4** — the first stage whose assessment constitution never carried
the item-18 prohibition, so A9 landed as the two lines alone. Housekeeping in the same pass:
`docs/testing_tracker.html`'s P2 step description still carried the arrangement sentence v2.5
struck (it was instructing the one thing A9 forbids) and is rewritten. §9 applies and costs
nothing: no stage carries a signed human GATE.*

*2.7 (2026-08-07, at S6's P-prep): **S6 · science·middle is certified against a DIFFERENT
SERVE LAW, and the C-steps say so.** The stage anchors units to the cognitive progression arc,
not to textbook sections, so it has no `section_anchor`, no registry, and no valid prefix of a
canonical — it is served by whole-canonical selection (engine **e17**; spec
`docs/science_middle_stage_serve.md`). Per-step consequences, applying to the S6 row ONLY:
**C5** — checks 3, 4 and 5 (anchors verbatim · first-visit order · registry coverage) report
**N/A**, because they are section arithmetic against an empty registry; check 6 (the synthesis
gate) stands but reads the explicit `synthesis` boolean instead of the reserved anchor token;
**check 8 is redefined** — truncation is LEGAL below the floor and a FAILURE inside the band,
and a second gate fails any surrender inside the band (both indicate an under-dense library);
check 7's sweep modes reduce to four — `identity | synthesis | truncation -Nu | surrender`.
Checks 1, 2, 9, 9a and 10 are unchanged. **C6**'s request matrix loses the between-variant and
below-floor *fill* rows and gains `X = K+1` (that canonical whole, closed by the top's synthesis)
and `X < lowest K` (truncation with declared drops). **C7** is unchanged in bans 1 and 3; ban 2
(forward reference / completion) is struck for this stage, so a forward reference between the
units of one plan is NOT a hit. **C8** has exactly one joint to inspect — arc-complete into
borrowed synthesis — which makes it the sharpest and cheapest transition test in the campaign.
**C9** collapses: every served plan is a whole canonical carrying its own assessment, so there is
no prefix remap; the borrowed synthesis brings its own items (founder 2026-08-07, after an audit
found SS·VIII ch 3 and SS·IX ch 3 already do this), and only the below-floor case has drops.
Everything else in this template is untouched, and the other ten stages are certified exactly as
before. §9 applies and costs nothing: no stage carries a signed human GATE, so nothing re-opens.*

*2.6 (2026-08-05, founder): **the teacher's own marks are now checked per stage, not once.**
C12 gains sub-checks 3 and 4 — **chapter notes** (usage, privacy, persistence) and the
**lesson-plan bookmark** (privacy, persistence) — because both are per-teacher writes on the
plan surface C12 already opens, and a stage's serve is the only place their asset/section keys
are exercised against real filenames. X1.3 and X1.7 remain the DEFINITION of the tenancy
property; C12 is the per-stage re-verification and points back at them. No new tracker column
(C12 already has one). §9 applies: no stage is certified yet, so nothing re-opens.*

*2.5 (2026-08-04, at S2's P-prep): **the stale A9 is removed.** P2 still said "options arranged
alphabetically from the first word at which they differ … correct answer never led with" — a
sentence the reference struck a day earlier (SS·secondary assessment v1.6 → v1.7, 2026-08-03,
ARV-D-032) when ordering moved into `genon/normalize_options.py`, STEP 6 of `build_library.py`.
Porting it would have put every remaining stage in contradiction with the pipeline that enforces
it. A9 is now stated as **one removal (the item-18 position prohibition) plus two lines (order
carries no meaning · no by-label option references)**, with an explicit ban on re-adding any
arrangement rule; the reference pair reads **LP v1.10 · assessment v1.7**; C13's item 18 is
closed by STEP 6 rather than "superseded by a convention"; the §3 stage table gains S2's landed
versions. §9 applies: no stage is certified yet, so nothing re-opens.*

*2.4 (2026-08-04): **C14 added — copyrights review**, run per stage like every other C-step
(each of the 11 tracker rows gains a C14 column before GATE). §9 applies: no stage is
certified yet, so nothing re-opens.*

*2.3 (2026-08-03): aligned to **architecture v2.0** (`variant_canonical_architecture.md §0`
— read it first). σ, the solver, and the mandated closing spans are RETIRED (ARV-D-025:
a mandated closing synthesis in a compact imported the lending plan's priors — the jumpy
Xth unit); canonicals are authored FREE at equal-dispersion counts, the standard alone
closes with the reserved `synthesis` unit, and slot X is filled by the first-exposure
choice set (engine e12). Template consequences: §0.7's σ machinery struck (floor stands);
C1/C5/C6 updated to `canonical_plan`, the synthesis-anchor gate and the e12 sweep modes;
**C8 replaced** — LLM-need flags give way to the X−1→X transition inspection, the direct
probe of the defect that forced v2.0; the HUMAN GATE reads the sweep table, the standard's
synthesis unit and C8's worst transition. §9 applies: no stage is certified yet, so
nothing re-opens.*

*2.2 (2026-08-02, at the pilot's C3): the register moves from prohibition to MACHINE GATE.
`genon/register_scan.py` runs inside `build_library.py`'s certification; `genon/repair_register.py`
backfills declared edits into authored artefacts; the TOP canonical now gets a platform brief of
its own. C5, C7, §6 and §7 updated. Founder ruling behind it: regenerating is a lottery — ch 3
breached the register nine times while authored under v1.10, which bans it in terms.*

*2.1 (2026-08-02, during step 0): two template corrections. (a) At 0.2 — the engine ladder
e08 → **e10** folded in: dropped sections (e09) and served-schedule prints (e10) are now asserted
in C6, C7, C10 and C12. (b) At 0.6 — the **"two-duration residual" is struck** (founder): the
constitution takes duration as an INPUT and no rule branches on 40 vs 45, so the class draw
cannot under-sample a stage; serve-time duration variance is universal and already lives in C6's
mixed matrix. §9 applies to both: no stage is certified yet, so nothing re-opens.*

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
| S2 | social_sciences · middle | vi, vii, viii | 40 (VI–VII) · 45 (VIII) | 40 |
| S3 | science · secondary | ix | 50 | 13 |
| S4 | mathematics · secondary | ix | 50 | 16 |
| S5 | the_world_around_us · preparatory | iii, iv, v | 40 | 32 |
| S6 | science · middle | vi, vii, viii | 40 (VI–VII) · 45 (VIII) | 37 |
| S7 | mathematics · middle | vi, vii, viii | 40 (VI–VII) · 45 (VIII) | 39 |
| S8 | mathematics · preparatory | iii, iv, v | 40 | 43 |
| S9 | english · preparatory | iii, iv, v | 40 | 39 |
| S10 | english · middle | vi, vii, viii | 40 (VI–VII) · 45 (VIII) | 46 |
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
the chapter that will be used. Counted that way (2026-08-02), **315 of the 330 mapped chapters
are eligible**; the two content gaps are **mathematics/ix** (16 mappings, 8 summaries) and
**social_sciences/viii** (14 mappings, 7 summaries) — draw pilot chapters from the covered half
in both. Science and social_sciences carry `.txt` summaries, not `.json`; both shapes count.

**The draws (run at step 0.6, 2026-08-02)** — seed `"<subject>|<stage>|2026-08-02"`,
`random.Random(seed).choice(sorted(candidates))`:

| Stage | Candidates | Drawn | Std duration | Eligible chapters |
|---|---|---|---|---|
| S1 social_sciences · secondary | ix | **ix** | 50 | 9 |
| S2 social_sciences · middle | vi, vii, viii | **vii** | 40 | 12 |
| S3 science · secondary | ix | **ix** | 50 | 13 |
| S4 mathematics · secondary | ix | **ix** | 50 | 8 |
| S5 the_world_around_us · preparatory | iii, iv, v | **v** | 40 | 10 |
| S6 science · middle | vi, vii, viii | **viii** | 45 | 13 |
| S7 mathematics · middle | vi, vii, viii | **vii** | 40 | 15 |
| S8 mathematics · preparatory | iii, iv, v | **iii** | 40 | 14 |
| S9 english · secondary | ix | **ix** | 50 | 16 |
| S10 english · middle | vi, vii, viii | **vi** | 40 | 16 |
| S11 english · preparatory | iii, iv, v | **iii** | 40 | 17 |

**Duration is an input, not a stage property** (founder, 2026-08-02 — this replaces the
"two-duration residual" the rewrite brief carried). A stage's constitution names the duration
only in INPUTS 4 ("the class-standard duration … × the period count") and its band rule is
arithmetic on whatever that duration is — nothing branches on 40 vs 45, so drawing VII rather
than VIII samples the same constitution. What *is* real is serve-time duration variance, and it
belongs to every stage equally: no teacher's timetable matches the authored standard, so a
40-authored plan routinely lands in 45- and 60-minute sittings. That is C6's mixed-duration
matrix plus the certifier's tiling check, run for all eleven stages — not a special rule for
four of them. Across the campaign the draws happen to exercise all three durations anyway
(40 at the preparatory stages, 45 at science·VIII, 50 at every secondary stage).

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

**0.2 [Claude] Engine + code state.** Assert `GENON_ENGINE_VERSION = "12"` (`api/data.py`);
`aruvi_core/genon/` contains exactly `compile.py` (v0.5) and `serve.py` (v2.0/e12) — the
retired `partition.py`/`polish.py`/`variant_solver.py` sit in `_to_delete/`; the repo-root
`genon/` lab keeps historical copies (`partition.py`, `polish_plan.py`, `polish_seams.py`)
that nothing live imports. **Exit:** `grep -rn "partition\|polish\|variant_solver" api/
aruvi_core/ web/app/lib/format.js` shows no live import, and the three genon suites
(`test_genon_serve`, `test_genon_plan_key`, `test_genon_duration_order`)
are green. **Artefact:** the grep output + the test run.

> **Engine ladder, recorded here because the campaign's assertions key on it** (`api/data.py`
> carries the full dated comment block): **e08** the variant-serve pivot · **e09** (2026-08-01)
> **dropped sections** — a below-floor serve carries its unreached units verbatim in
> `result.dropped_units` (flagged `unscheduled`, authored minutes as guidance), rendered
> online only via `/view` → `view.dropped_lp` and deliberately omitted from exports; surrender
> now files in `section_coverage_note`, the same channel as drops, with
> `genon.surrender_note` kept as provenance · **e10** (2026-08-01) **served-schedule prints** —
> `period_schedule_display` and the duration label build from `genon.served_matrix` (the
> periods actually used), so a 13-period ask on a 12-period top prints 12; the request survives
> in `genon.matrix` / `period_rows_snapshot` · **e11** (2026-08-02) **lendable unit** — the fill
> ladder no longer offers a variant's trailing SYNTHESIS unit. A unit that only re-anchors
> sections an earlier unit of its own plan already taught is written to be met at the END of its
> own arc, so borrowing it into a foreign prefix produced sittings assuming lessons the class
> never had (ARV-D-023, found at C7 — the 50m×10 serve carried NO coverage note because section
> coverage was formally complete; **anchoring is not teaching**). `serve.lendable_unit()` walks
> back to the unit that first introduced those sections; synthesis mode still borrows `units[-1]`,
> where a synthesis assumes nothing false. Certification check 6 moves to the lendable unit, and
> the variant brief's closing mandate now says the closing unit must TEACH its span and forbids a
> trailing synthesis. Side effect: the TOP canonical becomes lendable for the first time ·
> **e12** (2026-08-03, architecture v2.0) **the Xth-unit CHOICE SET** — the exact/superset/
> suffix ladder and `lendable_unit()` are replaced outright by first-exposure selection
> (§0.4): slot X borrows the unit that FIRST deals the next-due section (forward reach >
> M-alone > backward; e11's insight promoted to the selection principle); Case 1 borrows the
> standard's mandated `synthesis` unit; drops re-source from the LENDER; Case-3 truncation
> asks for the reference canonical's count. σ, `closing_spans` and `variant_solver.py` retired
> with the mandate they served (ARV-D-025).
> Every e08–e11 plan file is stale by construction and stays on disk as the C10.3
> no-overwrite evidence.

**0.3 [Kumar] Canonical plans fresh.** `python3 genon/variant_plans.py` — every chapter row of
`master_plan.json` carries `canonical_plan {counts, provisional, basis, registry_sections,
authored}` (counts by equal dispersion; stale v1.x `variant_plan` keys are purged by the
pass). **Runbook pair (hard):** `genon/master_plan.py` regeneration WIPES these rows;
`variant_plans.py` must be re-run immediately after it, before any row is trusted.
**Exit:** the annotate pass reports rows written; the campaign's pilot chapters show
`basis: "authored_standard"` once their standards exist. **Artefact:** the run output.

**0.4 [Kumar] Deploy the campaign tracker.** `api/testing_campaign.py` is now **included in
`api/main.py`** (2026-08-02 — the router had never been wired in, which is why the page sat
"offline": it loads from `file://` fine, but every `/api/testing/*` fetch 404'd). Open
`docs/testing_tracker.html` or, better, `GET /api/testing/tracker` (same origin as the API).
The v1.0 campaign state is archived under `backup/testing/` and the register restarted for
this template, carrying only the defect rows — step keys `0.x` and `P1–P4` were REDEFINED by
this rewrite, so a v1.0 tick under them would have read as evidence for a different step.
**Exit:** a tick made in the browser survives an API restart (state at
`data/testing/campaign_state.json`). **Artefact:** the state file.

**0.5 [Kumar] Provision the three test identities — EMPTY.** `kumar1`, `kumar2`, `kumar3` (sent
as `X-Aruvi-User`; `tenant_id == user_id`; all-lowercase is the standard — the local filesystem
is case-insensitive, so a mixed-case variant aliases to the same directory on macOS and would
split into two tenants the moment this runs on Linux or Supabase).

**Founder decision, 2026-08-02: the identities start with NO teaching profile, and each stage's
profile is set up at its P5** — so the profile only ever describes the class actually drawn, and
setting it up exercises the real first-run flow rather than a hand-written JSON. All prior
history is cleared: readiness, prepared plans, section state, plan archive and allocations.
**Exit:** for each identity, `GET /readiness` returns `ready: false` with `subjects: []`, and
`/plans-prepared`, `/plan-archive`, `/section-state` all return empty. **Artefact:** the three
readiness JSONs + the backup path of the cleared history.

**0.6 [Claude] Re-verify the matrix and draw the classes.** Recount chapters per subject·class
from `mappings/`; confirm eligibility (§1) per stage; run the eleven draws and record method +
seed + candidates + result per stage. **Exit:** the §1 table matches disk (or is corrected here
with a dated note) and all 11 picks are recorded under step 0 in the tracker. **Artefact:** the
count table + the pick log.

**0.7 [Kumar, founder inputs] The floor (σ is GONE — struck at template 2.3).**

> ★ **Struck 2026-08-03 (architecture v2.0 §0).** Everything this step said about σ — the
> ceiling, the sizing rule, the corpus projection, per-stage calibration, the escalation
> ladder — described the solver-mandated closing spans, and those are RETIRED (ARV-D-025).
> Canonical counts are now pure arithmetic (equal dispersion over [floor, standard],
> `master_plan.py canonical_periods`); there is nothing to calibrate and no `SIGMA` table.
> The condensation judgment the ceiling tried to formalize now lives where it belongs:
> at authoring time, in the free compact's own hands — and is *inspected*, not mandated,
> at C8 and the human gate. The prior text survives in git and in template 2.2.

**The floor stands, unchanged:** `round(0.6 × recommended_periods)` — "the fewest periods
at which this chapter still tells a coherent story." It is now also the LOWEST canonical's
count on wide-enough bands (§0.2). Left as-is for this campaign; flagged as the open dial.

**Exit:** the floor ratio recorded as accepted-unchanged. **Artefact:** this record.

**0.8 [Kumar] Quarantine hygiene.** `backup/quarantine/` exists and is EMPTY at campaign start
(a non-empty quarantine is an open fix worklist, and a quarantined file must never be servable).
**Exit:** `find backup/quarantine -name "*.json"` returns nothing.
**Artefact:** the (empty) listing.

---

## 3. Per-stage preparation (P-steps; run before that stage's C-cycle)

> **ORDERING RULE (hard, and it is about CONSTITUTIONS):** every constitutional amendment for a
> stage completes — **P1–P4, versions bumped, changelog written — before that stage's chapter is
> generated**, along with the solver inputs P5.1–P5.3 that the generation itself consumes.
> Amending a constitution after the library is authored invalidates the library (it was authored
> under the older version; see §9). This is the whole reason the P-steps are a separate list.
>
> **Provisional sign-off (founder, 2026-08-02).** P5.4 — the three test identities' teaching
> profiles — is *not* consumed by generation or certification: it is first needed at **C6**, the
> API serve checks. So a stage may be **signed provisionally with P5.4 still open**: SIGN goes
> green, the C-cycle opens, and P5 stays **amber** in the tracker until the profiles exist.
> C6 is the hard stop for it. A stage may NEVER be signed with a constitutional item (P1–P4)
> or a solver input (P5.1–P5.3) open — those are what the ordering rule protects.
>
> **P5.5 (the carrier, added 2026-08-08) sits between the two.** It is not consumed by
> generation *authoring* either, but it IS consumed by the compile/certify half of C1, so it
> gates **C1**, not C6. A stage may be signed provisionally with P5.5 open provided the tracker
> records it as a C1 gate — as S4 does — but it may never enter C1 with it open, and unlike P5.4
> the failure is not a clean stop: the build spends the money first (P5.5's second warning).

**The constitutional carry-forward is EXACTLY this and nothing more** (founder ruling
2026-08-01; `partition_constitution_rollout.md` §3): **A1 · A5/A7 · A6-confirm · A9 · P3 · P4**.
**A2, A3 and A4 are cancelled; X3 is void.** The reference pair is SS·secondary
**LP v1.10 · assessment v1.7**. **A9 is now a REMOVAL, not an addition** — the arrangement
sentence was struck at v1.7 (2026-08-03) and the sort lives in `genon/normalize_options.py`;
see P2.

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

| # | Subject · stage | LP ver | Band shape | A1 | Register | A9 (option order) |
|---|---|---|---|---|---|---|
| S1 | social_sciences · secondary | **1.10 — reference** | time_bands | ✓ | ✓ | ✓ (assess v1.7) |
| S2 | social_sciences · middle | **2.8 ✓** | time_bands | ✓ | ✓ | ✓ (assess v2.4, 2026-08-04) |
| S3 | science · secondary | **1.1 ✓** | time_bands | ✓ | ✓ | ✓ (assess v1.2, 2026-08-05) |
| S4 | mathematics · secondary | **1.3 ✓** | time_bands | ✓ | ✓ | ✓ (assess v1.2, 2026-08-09) |
| S5 | the_world_around_us · preparatory | **1.4 ✓** | time_bands ✓ (never converted) | ✓ | ✓ | ✓ (assess v1.4, 2026-08-11) |
| S6 | science · middle | **2.2 ✓ CERTIFIED** | time_bands ✓ | ✓ | ✓ **two-ban** | ✓ (assess v1.5, 2026-08-07) |
| S7 | mathematics · middle | **3.9 ✓** | time_bands ✓ | ✓ | ✓ | ✓ (assess v3.4) |
| S8 | mathematics · preparatory | **1.4 ✓** | phases[] → **time_bands ✓** | ✓ | ✓ | ✓ (assess v1.3, 2026-08-11) |
| S9 | english · preparatory | 1.1 (quote-format only) | phases[] → P3 | — | — | — |
| S10 | english · middle | 1.6 (quote-format only) | phases[] → P3 | — | — | — |
| S11 | english · secondary | 1.1 (quote-format only) | phases[] → P3 | — | — | — |

> ★ **CROSS-STAGE, 2026-08-11 — the narration format's JSON quote hazard is closed on all
> five LP constitutions that carried it** (maths middle v3.9 · maths prep v1.4 · english
> prep/middle/secondary v1.1/v1.6/v1.1). `book_ref ("brief")` put a straight double quote
> inside a value emitted as JSON, leaving the escape to the model — which does it for a whole
> run or not at all. maths III ch 5 proved both halves on consecutive calls and the second
> cost ₹40.72. The Format and Example lines now show CURLY marks (“ ”), which need no
> escaping. **Worded as a licence, not a switch** — the straight form "remains valid and is
> not a defect" — so it is relaxation-only under §9 and **no authored library re-opens**. The
> S9–S11 rows below are bumped by this alone; their P-prep is otherwise untouched. Pipeline
> half of the same fix: `parse_with_repair`'s bound 10 → 500, plus
> `genon/recover_from_raw.py`, so a parse failure never costs a re-generation again.

> ★ **S6 · science · middle is the campaign's ONE STRUCTURAL EXCEPTION** (2026-08-07, at its
> P-prep; spec `docs/science_middle_stage_serve.md`, read it before any S6 work). It anchors
> learning units to the COGNITIVE PROGRESSION ARC, not to textbook sections. So it has no
> `section_anchor`, no section registry, and — because arcs are derived freshly per generation
> and may differ between a chapter's own canonicals — **no cross-canonical registry of any
> kind and no borrowing of stages, ever**. A stage is taught whole or not at all, so no prefix
> of a canonical is a valid plan: truncation dies, and borrowing with it. Two consequences for
> the P-steps below. **P1's register is a TWO-BAN cut for this stage alone** — the
> forward-reference / completion ban is deliberately NOT ported (founder ruling; every unit of
> a canonical is served with every other unit of that canonical, so forward reference is never
> wrong for anyone, and a completion claim is true). Bans 1 and 3 stand in full — duration
> scaling and the Calendar Purge are orthogonal to the serve model. **P5.2's registry question
> is answered negatively** for this stage; the arc's terminus (Rule 1's dissolution-test
> operation) is the only shared fact, and the only thing a borrowed synthesis unit may assume.
> The stage serves at PLAN granularity — identity · K+1 synthesis borrow · below-floor
> truncation with drops · above-top surrender — on canonicals spaced exactly 2 apart, which
> removes surrender inside the band. That engine work GATES S6's C1 and the C5–C9 rewrite
> below (template → v2.7); the constitutional P-steps do not wait on it. §9 costs nothing:
> no stage carries a signed human GATE.

> ★ **ADDED 2026-08-08, at S4's P-prep — the CARRIER is a per-stage precondition on C1, and
> it is not constitutional.** `aruvi_core/genon/carriers.py` carries a `_NOT_YET` table, and
> `assessment_items()` RAISES `CarrierNotImplemented` for any subject still in it. Only
> `science` implements `genon_assessment`; social_sciences and TWAU ride the
> item-self-sufficient default; **mathematics and english are both still listed** ("owed by
> S4/S7/S8" and "owed by S9/S10/S11"). So six of the eleven stages cannot be certified. S4 found
> this at its P-prep, exactly as S3 found the `questions`-wrapper bug that created the seam in
> the first place.
>
> **Read the scope precisely, or this looks bigger than it is** (founder challenge, 2026-08-08).
> A listed subject is NOT a subject whose assessment links are unresolved. The APP resolves them
> and always has — `subjects/mathematics/subject.py::_secondary_assess` runs the handoff-bridged
> join today and is parity-tested, which is why maths·secondary LPs and assessments render
> correctly. The app reaches the plugin through `assessment_to_view`, which returns DISPLAY
> objects; genon needs the RAW item dicts (options, `is_correct`, guide, `visual_stimulus`
> intact, for served files and exports) and so asks for **`genon_assessment`** — a second door
> that only `science` has opened. So each remaining stage's carrier work is a **delegation** of
> logic the plugin already contains: for maths·secondary, a ~6-line call to `items_by_handoff`
> with the identical arguments science·secondary passes. Budget it that way. What makes it a
> gate is not its size but the two properties below.
>
> **The gate is POST-PAYMENT, and this is the part worth internalising.** `certify()` is called
> at `build_library.py:514`, *after* metered STEP 1 (`:482-484`) and metered STEP 4
> (`:497-501`) — the full library is authored and billed before the carrier is consulted. And
> STEP 1 does not fail either: `generate_canonical.py:154-159` calls the carrier inside a bare
> `except Exception` and falls back to `parsed.get("assessment_items")`, a key the
> `questions`-wrapper subjects do not have, so the item-anchor validator degrades to a **silent
> no-op** and a paid canonical installs with every item anchored to nothing. The raise finally
> surfaces inside `load_library`'s `except` (`:196-199`) and is reported as
> `FAIL <file>: does not compile` for EVERY library file, ending at
> `STOP: no library on disk to certify` — naming neither the carrier nor the subject, and
> skipping quarantine.
>
> Four standing consequences: (a) **this check is now a P-step — `P5.5`, below** — so it is read
> before every stage's C1 and a listed subject is a hard gate, recorded in the tracker like S6's
> engine gate; **do not rely on the build to stop the run**; (b) `validate` must stop swallowing
> `CarrierNotImplemented` into a pass — a subject with no carrier should refuse to generate;
> (c) the `_NOT_YET` entries are keyed by SUBJECT, not subject·stage, so deleting one opens every
> stage of that subject at once, including stages in a different carrier family — making the
> table stage-aware is the smaller fix and keeps the campaign's stage-at-a-time discipline;
> (d) a `--certify-only` run on an empty library is safe and is the cheap way to test (b).
> None of it touches a constitution, so §9 does not fire.
>
> ★ **ADDED 2026-08-08, also at S4's P-prep — the SYNTHESIS unit has no home in a
> DERIVED-anchor handoff.** v2.0 mandates the standard canonical's closing synthesis unit
> (`section_anchor` = the reserved token, excluded from the registry). Where items anchor by
> `period_ref` that is harmless. Where the anchor is **derived** — science·secondary,
> mathematics·secondary, and science·middle via `progression_stage` — an item's only route to a
> unit is its group number → `coverage_handoff` → `period_numbers`, so a synthesis unit with no
> handoff entry can carry NO items and **C9.2 ("a borrowed unit brings its own items") becomes
> unsatisfiable on precisely the Case-1 synthesis borrow C8 exists to inspect**. The installed
> science·IX ch 8 library shows the model inventing an entry (`section_label: "synthesis"`,
> `period_numbers: [12]`, `total_sections: 11`) — **and it rescues nothing: no item uses it.**
> Verified 2026-08-08 — ch 8's item `section_number`s run 1–10 and `assessment_items()` stamps
> `unit_ref` 1,2,4,5,6,7,8,9,10,11, never 12. So C9.2 is already unsatisfiable on a **certified**
> library, which makes this a defect against S3 (§7), not only an S4 precondition. Nothing asked
> for the invented entry, and
> maths·secondary's A4 is stricter (`section_ref`/`section_title` are specified as copied
> VERBATIM from the summary, and there is no summary section to copy). `top_brief_for` mandates
> the unit and says nothing about its handoff row. One brief line closes it for every
> derived-anchor stage; **it is a V-series / brief matter and must NOT enter a constitution**,
> so it iterates at failure speed and triggers only a `--certify-only` re-run, never §9.
>
> **CLOSED 2026-08-08.** `top_brief_for` now asks for the row explicitly, and only where it is
> needed: the line is emitted when `carriers.item_anchor_is_derived()` is true — verified present
> for mathematics·IX and science·IX, absent for social_sciences·IX (item-self-sufficient) and for
> science·VIII (the plan-granularity arc brief). No constitution moved. **S3 should still take a
> §7 defect row:** its installed library predates the line, so its synthesis unit's questions do
> not exist, and a re-author is the only thing that creates them.

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
- **A9 — MCQ option order is NOT the model's to set.** *Rewritten 2026-08-04: the arrangement
  convention this item used to mandate was struck from the reference at assessment v1.7
  (2026-08-03, ARV-D-032) — prose could not carry a sort, and the v1.6 library came in 15 of 18
  unarranged. Ordering is now a pipeline stage:* `genon/normalize_options.py` (STEP 6 of
  `build_library.py`, subject-agnostic) sorts, relabels and remaps the guide keys
  deterministically, and C3's gate 9a proves it ran. **So A9 at P2 is one removal and one
  addition, and never an arrangement rule:**
  - **REMOVE** the MEMORY-item-18 position prohibition ("the correct option must vary in
    position / never the same label across consecutive items") in the four files that carry it
    (SS + Science, middle and secondary) — it is known not to hold, and it asks for randomness
    the model cannot produce. Nothing replaces it in kind.
  - **ADD**, in the v1.7 wording: a mandate line saying option order carries no meaning and is
    not the model's to set (emit them as authored; uneven letters across a chapter are
    coincidence, not a defect), and the prohibition on an option that refers to another option
    **by its label** ("both A and B", "none of the above") — the one construction a downstream
    sort cannot reorder without rewriting.
  - **MUST NOT** re-add the alphabetical arrangement sentence, "never led with", or any rule
    that names a label position — naming arrangement at all keeps position salient to a model
    that should never reason about it (founder, v1.6 and v1.7 both).
  Applies to all eleven assessment constitutions; do the four item-18 files first. **Standing
  corpus-repair debt:** already-saved SS and Science plans carry clustered answers; STEP 6
  normalises them in place at ₹0, never shuffles, and records the count in
  `genon_canonical.repairs[]`.
**Exit:** `VERSION` bumped; anchor requirement present; item-18 prohibition gone; the "order
carries no meaning" line and the label-reference prohibition present; no arrangement sentence.
**Artefact:** amended file + diff.
**Done for S2 (2026-08-04):** SS·middle assessment **v2.3 → v2.4**; artefacts and the per-item
sign-off in `genon/out/stage_prep_ss_middle/`.
**Done for S3 (2026-08-05):** science·secondary assessment **v1.1 → v1.2**; A6 as the DERIVED
`section_number` anchor, not the reference's `period_ref` field. `genon/out/stage_prep_science_secondary/`.
**Done for S6 (2026-08-07):** science·middle assessment **v1.3 → v1.4**; A6 as the DERIVED
`progression_stage` anchor resolving to the stage's LAST unit. `genon/out/stage_prep_science_middle/`.
**Done for S4 (2026-08-08):** mathematics·secondary assessment **v1.0 → v1.1**; A6 as the DERIVED
`section_number` anchor (the science·secondary shape). **The REMOVAL was N/A** — this file never
carried the item-18 prohibition, so A9 landed as the two lines alone, and the pre-existing
"none/all of the above" ban was absorbed into the by-label prohibition rather than duplicated.
`genon/out/stage_prep_mathematics_secondary/`.
**Done for S7 (2026-08-10):** mathematics·middle assessment **v3.2 → v3.3**; A6 as the
PERIOD-FIELD anchor (8-rule row 4) — `section_ref` resolved against the period's
`textbook_segments[].ref`, with no `coverage_handoff` in the path. Removal N/A.
`genon/out/stage_prep_mathematics_middle/`.
**Done for S5 (2026-08-11):** the_world_around_us·preparatory assessment **v1.3 → v1.4**; A6 as
the reference's OWN declared `period_ref[]` (8-rule **row 8**, item-self-sufficient — the first
stage since S2 needing no translation, because it shares SS's family). Removal N/A, and the
by-label prohibition purely additive (no prior "none of the above" ban to absorb).
`genon/out/stage_prep_twau_preparatory/`.
**Done for S8 (2026-08-11):** mathematics·preparatory assessment **v1.2 → v1.3**; A6 as the
PERIOD-FIELD anchor on **`section_refs[]`** (8-rule **row 5** — the same family as middle on a
DIFFERENT field, which is why neither may borrow the other's join). Removal N/A. One defect
repaired alongside: the `what_each_option_reveals` example had lost `"B"` and gained a second
`"C"` when S7's distractors-only pass rewrote one of its two lines in this file.
`genon/out/stage_prep_mathematics_preparatory/`.
**AMENDED AGAIN for S4 (2026-08-09, at C3 — the first stage to amend AFTER authoring):**
LP **v1.2 → v1.3** (Rule 5 P1's consecutive-method cap gains a content-driven exception ·
`activity_title` 10–13 → **6–13** words · `section_context` 10–12 → **6–12** words, upper bound
untouched) and assessment **v1.1 → v1.2** (Rule 5's OPEN_TASK row extended to a whole-chapter
**synthesis LO**, which v2.0 mandates but `co_central: false` forbade — the trap most of the
corpus sits in). All four came from ch 4's live output at C3, where the evidence pointed at the
RULE, not the plan; no prohibition was removed and nothing pedagogical changed. Diffs +
pre-files in `genon/out/stage_prep_mathematics_secondary/`; rationale in both CHANGELOGs.
**§9 fires: S4 re-opens** — the library was authored under LP v1.2 / assessment v1.1 and is
re-authored under the new pair, C1–C3 re-run. Paid once, on one chapter, before the stage's
remaining eleven C-steps. **The general lesson for S5–S11: a limit stated as a number
(word counts, consecutive caps) is the kind of rule live generation most often disproves —
read the numeric limits at P1 with that in mind, because catching one there is free.**

**P3 [Kumar] Group B only — schema conversion.** Convert `phases[{minutes, description}]` →
`time_bands[{minutes, activity}]` (rename both the array and the `description` key). **No
`band_id` in the target shape** — the conversion shrank when the band layer left the
declaration surface. The compiler reads exactly `time_bands` and `activity`; the decision
stands to amend constitutions, not to teach `compile.py` an adapter.
**Exit:** the schema block emits `time_bands` with both keys; no `phases[` remains.
**Artefact:** diff.
**Done for S6 (2026-08-07)** — the first stage where this was not N/A: science·middle
Amendment A3 converted, Rule 6's prose following. `grep -c 'phases\['` = 0, `time_bands` = 2.
**Done for S7 (2026-08-10)** — mathematics·middle: Rule 6, Rule 8, Rule 10's heading and prose,
Rule 11's guard case and the schema all followed the rename.
**Done for S8 (2026-08-11)** — mathematics·preparatory: Rule 5, Rule 6's heading
(`PHASE NARRATION` → `BAND NARRATION`) and prose, Rule 7 and the schema followed. Note this
leaves the middle/preparatory saved-plan corpus on the old shape; the mathematics plugin reads
**both keys, newest first** (`subject.py:211-219`), which is what covers display.
**N/A for S5 (2026-08-11)** — the_world_around_us·preparatory has emitted `time_bands` with an
`activity` key since before the campaign (`grep -c 'phases\['` = 0, `'"phases"'` = 0,
`time_bands` = 7). Recorded because it is the first stage since S2 where the N/A is genuine
rather than a conversion already done: nothing was converted, and — unlike the maths and english
stages — **no saved-plan corpus is left behind on the old shape**, so P3 leaves no display debt.

**P4 [Kumar] History to the sidecar.** The amendment note goes to `CHANGELOG.md` beside the
constitution, never into the file; the `VERSION` line stays in the file.
**Exit:** no version-history block in the constitution; `CHANGELOG.md` lists every bump with
date and one-line rationale. **Artefact:** the changelog.

**P5 [Kumar + Claude] Stage inputs for the pipeline (never the constitution).**
1. **The floor** for this stage — accepted at the standing ratio (§0.7) or overridden per
   chapter with a recorded reason. (σ is struck at template 2.3: canonical counts are
   arithmetic, there is nothing to calibrate. A chapter whose serve band reads badly at C8
   escalates the v2.0 way: a fourth canonical between the dispersion points, raise the
   floor, or accept the declared drops — founder call, recorded.)
2. **The section registry definition where the section model is non-obvious.** English's
   split-chapter / spine model must have its registry defined *before* its canonicals are
   authored — the choice set is string arithmetic on `section_anchor` values drawn verbatim
   from the chapter summary's section list. This decision lands in the pipeline (summary +
   brief), never in a constitution.
3. Confirm the drawn class's pilot chapter has summary + mapping and a non-placeholder
   `master_plan.json` row with a `canonical_plan`.
4. **Set up the three test identities' teaching profiles for THIS stage's drawn class** (0.5
   leaves them empty by design). Do it through the app's own first-run / profile flow, not by
   hand-editing JSON — the setup doubles as a live check of that flow, and the profile then
   describes exactly the class under test. Give the three identities *different sections* so
   X1's tenancy evidence is unambiguous, and include one longer duration alongside the class
   standard so C6's mixed-duration matrix has something real to draw on.
5. **THE CARRIER — genon's door onto the verified 8-rule table.** Added 2026-08-08 at S4's
   P-prep, where its absence was met as a surprise instead of a checklist item. See below.
**Exit:** all five recorded; `GET /readiness` now returns `ready: true` for each identity, and
its subjects list contains this stage's class and nothing left over from an earlier stage.
**Artefact:** the note + the chapter's `canonical_plan` row + the three profiles + the carrier
trace.

**P5.5 in full — the carrier (founder doctrine, settled; do not re-litigate it per stage).**

> **Genon does not invent linkage, and no stage may design a new way to link an assessment item
> to its unit.** The single source of truth is the **verified 8-rule table** in
> `docs/architecture-plan.md` §"Link resolution — verified 8-rule table" (also restated in
> `aruvi_core/link_resolver.py`'s docstring): one row per subject·stage, giving the join method,
> the LO source and the item-container shape, each corrected against real saved files.
> `aruvi_core/genon/carriers.py` **is that same table exposed to genon** — its three families are
> the table's three families, and it says so in its own docstring. A stage's carrier work is
> therefore a **DELEGATION of what the subject plugin already does for the app**, never a fresh
> join. This is how S1 (SS·secondary, rule 3-shape), S3 (science·secondary, rule 2) and S6
> (science·middle, rule 1) were done, and S4 (mathematics·secondary, **rule 6**) follows it
> unchanged.

The per-stage check, all four parts by READING (never by "run it and see" — see the warning
below):

1. **Name the stage's row** in the 8-rule table: its number, family, join key, handoff key (or
   period field), and item container. For maths·secondary that is **rule 6** — item
   `section_number` → handoff `section_number` → `period_numbers`, **never** `section_anchor`
   text, items under a `{…, questions: []}` dict.
2. **Confirm the subject plugin already implements it for the app** (it almost always does —
   that is why the app renders correctly). Cite the method.
3. **Confirm `genon_assessment` exposes the SAME rule to genon.** The app reaches the plugin
   through `assessment_to_view`, which returns *display* objects; genon needs the RAW item dicts
   (options, `is_correct`, guide, `visual_stimulus` intact, for served files and exports), so it
   asks for `genon_assessment` instead. That second door is the only thing usually missing. For
   a handoff-bridged stage it is a few lines delegating to `carriers.items_by_handoff` with the
   row's two keys.
4. **Confirm the subject is absent from `carriers._NOT_YET`.**

**Two hard warnings, both learned at S4:**

- **`_NOT_YET` is keyed by SUBJECT, not subject·stage.** Deleting one entry opens every stage of
  that subject at once — including sibling stages in a *different* family (mathematics spans
  handoff-bridged at secondary and period-field at middle/prep). Either implement all of that
  subject's rows, or make the table stage-aware. A stage-granular gate is the smaller change and
  keeps the campaign's stage-at-a-time discipline.
- **The build will NOT catch this for you, and it is not free.** `certify()` runs *after* the
  metered steps, and `generate_canonical.validate` calls the carrier inside a bare
  `except Exception` whose fallback reads a key the `questions`-wrapper subjects do not have —
  so the item-anchor check silently sees zero items and passes. A missing carrier therefore
  yields a **paid, clean-looking, wrongly-anchored library** and a final error that names neither
  the carrier nor the subject. P5.5 is a **pre-flight read**, which is the whole point of it
  being a P-step.

**Exit for P5.5:** a one-line trace — *"rule N · family · join_key → handoff_key/period field ·
container · plugin method · `genon_assessment` present · not in `_NOT_YET`"* — plus, where a
door had to be opened, the diff. **P5.5 GATES C1** (unlike P5.4, which gates C6), so a stage may
be signed provisionally with P5.5 open only if the tracker records it as a C1 gate; it may never
*enter* C1 with it open.
**Done for S4 (2026-08-08) — and this is the step's worked example.** Rule 6 was already
specified and `_secondary_assess` already ran it for the app; only genon's door was shut. Closed
as a **delegation**: `genon_assessment` on the mathematics plugin calls
`carriers.items_by_handoff` with row 6's two keys, and middle/preparatory RAISE naming their own
family so they cannot borrow a rule that is not theirs. Three things landed with it and are now
part of the platform rather than the stage: **`_NOT_YET` re-keyed by subject·STAGE** (it was per
subject, so `mathematics` was one entry spanning two families); **`carrier_gap()` /
`require_carrier()` plus a STEP 0 pre-flight in `build_library.py`**, which turns this step from
a read into a gate that stops with `STOP before spending — …` before any metered call; and
**`generate_canonical.validate` no longer swallowing `CarrierNotImplemented`**, which is what had
made a missing carrier a *paid* failure. `tests/test_genon_carriers.py` 25 → 36 tests, green.
One trap recorded for S7–S11: `genon_assessment` receives only `result`, and the grade lives on
the enclosing saved plan, so **branch on container shape, not `stage_for(grade)`** — a grade read
there is `None` on the very call the carrier makes.
**Done for S7 (2026-08-10):** row 4, the period-field family's FIRST stage — it wrote
`items_by_period_field` plus three shape adapters (mediated anchor, goal-cluster handoff,
group-nested container), and deliberately left preparatory's branches written-but-shut with a
note saying so.
**Done for S8 (2026-08-11) — the cheapest carrier of the campaign, and it shows what a
well-left note is worth.** Row 5 needed no new code: S7's family helper and
`genon_unit_anchor`'s preparatory branch were already on disk, so the whole step was three
lines of delegation (`items_by_period_field` with `section_refs[]`) plus deleting the
`_NOT_YET` entry. **Mathematics is now carried at all three stages**; the four remaining
entries are english's (row 7, S9–S11). The stage discriminator earns its keep in both
directions now — middle and preparatory share a container and are told apart by `goal` vs
`intent`, never by `stage_for(grade)`, which is `None` on the very call the carrier makes.
Verified on the real saved shape (`backup/saved_plans/mathematics/iii/ch_06_*.json`): 26 items,
zero orphans, every anchor equal to the independently computed last-period-teaching-the-section.
`tests/test_genon_carriers.py` 82 (4 failing, all of them S7-era "preparatory is still owed"
assertions) → **92, green**.
**Done for S5 (2026-08-11) — and it adds a FIFTH part to the check above.** The four-part read
passed on sight: row 8, item-self-sufficient, `period_ref[]` off the item, bare flat list, and
the_world_around_us was never in `_NOT_YET` — its assessment half has always been right, which is
why S3's `questions`-wrapper defect could not touch it. **The LESSON-PLAN half was missing and
nothing in P5.5 looked at it.** `carriers.unit_anchor` reads `period["section_anchor"]`; TWAU
periods carry **`section_ref`** and `grep -c section_anchor` is 0 in its LP constitution, so every
TWAU chapter would have raised `KeyError` on its first period at compile — post-payment, reported
as `does not compile` on every file, naming nothing. Closed as a mediation (four hooks on the
plugin, no constitution touched; the anchor is a **prose section TITLE**, returned verbatim), and
verified end-to-end on the real saved shape: 9 units, 9 items, zero orphans, every anchor a
byte-identical registry member in first-visit order. `tests/test_genon_carriers.py` 92 with 3
failures → **95, green** — the three were the "TWAU is still owed" assertions, one of which had
carried the words *"S5 owes it"* in its own docstring.

> ★ **P5.5 GAINS PART 5, from S5 (2026-08-11): WHERE DOES THIS STAGE'S PERIOD KEEP ITS SECTION
> ANCHOR, AND DOES `carriers.unit_anchor` FIND IT?** Parts 1–4 audit how an ITEM finds its unit.
> Nothing audited how a UNIT finds its section, and `_NOT_YET` cannot see it — it is an inventory
> of the assessment seam only. Three field names are already in use (`section_anchor`,
> `textbook_segments[].ref`, `section_refs[]`) and S5 found a fourth. The check is
> `grep -c section_anchor <the stage's LP constitution>`: **0 means the stage needs
> `genon_unit_anchor` + `genon_anchor_field_present: False` on its plugin**, and the second of
> those is the expensive one — without it `top_brief_for` demands the reserved token in a field
> the constitution never defines, **at metered STEP 1**, and the certifier then finds no synthesis
> unit in the library it has already paid for. **Owed by S9–S11**: english is the last family, its
> LP is spine-structured (`section_id` + `spines_taught[]`), and one grep across its three LP
> constitutions decides whether three more stages need mediation. Free at P-prep; a full library
> at C1.

**Retro-note for S1/S3/S6:** all three satisfied P5.5 in substance before it existed — S3 is
where `carriers.py` was created (the `questions`-wrapper defect) and S6 extended it with
`progression_stage`. Nothing re-opens.

**[Claude] Stage sign-off:** read the amended pair against the reference and the rollout brief;
confirm A1 lands, the register is ONE block in the v1.10 three-ban form, A6 anchors are present,
A9 landed as the v1.7 removal-plus-two-lines (**and no arrangement sentence came back**), P3
converted (Group B), and no cancelled amendment (A2/A3/A4) or V-rule has crept into
a constitution. **Then state the P5.5 carrier trace explicitly** — the stage's 8-rule row, the
plugin method that already serves the app, whether `genon_assessment` exposes it, and whether the
subject is still in `_NOT_YET`. A sign-off that does not mention the carrier is incomplete: this
is the one item the ordering rule does not protect and the build does not catch.
**Exit:** a written note per item — present / absent / deviates-with-reason.
**Artefact:** the note; the stage's C-cycle is then unblocked, or the C1 gate is named.

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

which runs, stopping on the first failure and idempotent to re-run: **the standard-canonical
brief** (`variant_plans.top_brief_for` → `genon/out/briefs/ch_NN_top.txt`, passed with
`--brief`: the serve contract in plain terms, per-unit independence of materials/opening
moves/homework, no completion claim — added 2026-08-02, when the top turned out to be the
only artefact generated without a brief and the one that breached the register nine times —
**plus, since v2.0, the synthesis mandate**: final unit anchored exactly the reserved token
`synthesis`, coverage complete by unit A−1) → standard canonical (LP + assessment,
`ch_NN_canonical.json`) → `variant_plans.py` annotate (the row finalizes:
`provisional: false`, `basis: "authored_standard"`) → compact briefs written to
`genon/out/briefs/` (FREE authoring: registry discipline + total coverage, NO closing
mandate, token forbidden) → each compact canonical with its brief (own assessment; installs
`ch_NN_canonical_pKK.json`) → re-annotate → deterministic certification → report in
`genon/out/library_reports/`.
`--certify-only` re-runs the free steps. **Never author an installable plan in a Cowork
session** — a session-authored plan is a draft on an uncalibrated model.
**Exit:** the library on disk matches `canonical_plan.counts`; `GET /genon/{subject}/{grade}/chapters`
lists the chapter and `canonical_minutes` = standard duration × top period count.
**Artefact:** the library files + the report path.

**C2 [Claude] Cost the LIBRARY.** From `runtime_data/token_log.csv`, record per generation
(`canonical_generation` for the top, `variant_generation` per compact, plus any rerun) —
timestamp, input tokens, output tokens, cost ₹ — and the **library total ₹**, including failed
runs that had to be redone (a rerun is part of what the chapter cost). **Exit:** every row for
this chapter is attributed; the total is in the provenance panel; a missing cell is recorded as
missing, not blank. **Artefact:** the cost table.

**TWO FIGURES, and the tracker's ₹ column is the first one** (founder, 2026-08-07): the
**clean-path** cost is the runs that produced the files now on disk — reruns and superseded
generations EXCLUDED — and it is what a chapter costs, so it is what the 330-chapter
extrapolation multiplies. The **all-in** cost includes every rupee actually spent, and it is
what prices a defect. Record both; the panel's `reruns` row keeps the difference visible. The
column excluding reruns is deliberate: a defect rerun inflates a corpus projection by however
often defects happened during a pilot, which is not a property of the corpus.

*Benchmark, measured on the SS·IX ch 3 pilot (2026-08-01): top ₹39.43 + variants ₹36.51 and
₹35.05 + one defect rerun ₹34.71 = **₹145.70** all-in; **₹110.99** on the clean path.
**Cost shape:** input is flat across runs (14.9–15.4k tokens — the constitution, summary, mapping
and brief are paid for in full every time) while output falls with period count (25.6k at 12
units → 22.1k at 7), so a compact variant costs only ~11% less than the top. Budget per
authoring RUN, never per unit.*

*Corpus extrapolation, on the real variant-plan distribution rather than a flat ×3: the 315
non-placeholder chapters carry plans of size 3 (296 chapters) or 2 (19) = **926 authoring runs**.
At ~₹37/run that is **≈ ₹34k synchronous, ≈ ₹39k with a 15% defect-rerun allowance**, halving to
roughly ₹17–20k at batch pricing (batch deferred to the mass pre-warm). SS·secondary is the
heaviest corner, so treat ₹37/run as upper-middle. **Count runs, not chapters** — that is the
unit the bill is charged in.*

*Keep superseded work out of the extrapolation: ch 3 also carries ₹54.35 of partition-era
canonical and probe spend (chapter total ever: ₹200.05). Folding R&D into the pre-warm figure
would inflate it by ~37%.*

**C3 [Claude] Canonical + one compact variant vs the stage constitution, rule by rule.** Check
both files against every numbered rule of the stage's current LP constitution (and the
assessment constitution for the item files), citing rule numbers — a table `rule # → pass /
fail / subjective-pass with quoted evidence`, not a general impression. Register and tone
judgements are subjective: say so, and quote the strings the judgement rests on. Checking a
compact variant too is deliberate — the variants are authored under the SAME constitution plus
the brief, and a constitution that only holds at full length has not been proven.
**Exit:** every rule number appears in the table for both files; every fail becomes a defect
(§7). **Artefact:** the rule table.

**C3 · maths sub-check — DETERMINATE ANSWERS ARE RE-DERIVED (S4, S7, S8 only; added 2026-08-09).**
Mathematics is the only subject whose items carry an answer that is right or wrong rather than
judged: science and social_sciences ship `expected_elements` / `look_for`, and a sweep of all 16
installed canonicals on 2026-08-09 found **zero** items with an `expected_answer` outside maths.
So this sub-check is scoped to the three maths stages, and the other eight record it N/A with
that reason. It exists because **nothing else in the pipeline reads an answer's VALUE** — the
certifier checks structure, STEP 6 checks option order, and `verified: true` is the model's
claim about itself, which at S4 was false (ARV-D-084).

Procedure, run over **every** installed canonical of the pilot chapter — the top and all
compacts, not the C3 pair, since each compact authors its own assessment:

```bash
python3 genon/extract_determinate.py mathematics <grade> <chapter>
# → genon/out/answer_checks/mathematics_<grade>_chNN_check.py
#   fill in `claimed` and `target` per item, then:
python3 genon/out/answer_checks/mathematics_<grade>_chNN_check.py
```

Extraction is mechanical; **transcription is judgement and stays with the checker** — stems are
prose ("Compute 312^2 by writing 312 = 300 + 10 + 2 and applying the identity …"), so a parser
that guessed at them would fail silently, which is the failure this check exists to prevent.

**The one rule that makes it work: transcribe the target from the QUESTION STEM, and do not
read `method_one_line` until the verdict is written down.** At S4 the wrong answer sat beside a
method line that had already derived the right one; a checker who transcribes the method
confirms the file against itself and sees nothing. Where an answer is not symbolically
expressible (a sentence, a units-bearing quantity), set the target `None` and record the judged
verdict in the note — a judged item is still checked, but it must say so. Count CHECKS, not
items: a stem asking for both an expansion and a numerical value is two.

**Exit:** the worksheet runs with 0 WRONG, and its item count reconciles against the library's
determinate items. Any WRONG is an **S1 defect** — a wrong answer is teacher- and student-facing
and cannot be accepted the way a register phrasing can. **Artefact:** the filled worksheet,
committed beside the C3 markdown. *Worked example: `genon/out/answer_checks/mathematics_ix_ch04_check.py`
(25 checks over 19 items across three canonicals; 1 WRONG on first run → ARV-D-084 → repaired in
place by `genon/repair_leaked_deliberation.py`, and the worksheet is now that repair's regression
test).*

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
| 9 Jul 12–13 wave contracts | per its file list | 18 MCQ position spread | **closed by STEP 6** |

\* Item 6 ("wire time into the constitutions" as a duration vector) is **closed by design**: A1
fixes one standard row and the serve engine owns every timetable variation. Item 18 is **closed
by the pipeline**: the position prohibition is struck at P2 and ordering is done deterministically
by `normalize_options.py` (STEP 6), so there is no spread to check and no convention to check
either — read STEP 6's `options arranged: N of M` line as the generation-quality signal instead
(C3 gate 9a). Record both closures in MEMORY.md the first time they come up.
**Exit:** each applicable item gets pass / fail / n-a-here with one line of evidence from the
live artefacts; fails become defects. **Artefact:** the item table.

**C5 [Claude] Read the certification report — ALL PASS required.** Open the newest
`genon/out/library_reports/<subject>_<grade>_chNN_<ts>.md` and confirm each deterministic check
(implemented in `genon/build_library.py::certify` — cite it, do not re-specify it):
1. **library complete** — the files on disk match `canonical_plan.counts`;
2. every file **compiles** (`compile_stream`, v0.5);
3. **anchors verbatim** — every unit's `section_anchor` resolves in the top canonical's
   registry (the reserved `synthesis` token is exempt — it is not a section);
4. **first-visit order** — new sections appear in registry order (revisit tails are legal;
   skipping a section is not; the synthesis unit is skipped by the walk);
5. **coverage reaches the final registry section** (for the standard: by unit A−1, before
   the synthesis unit);
6. **the synthesis-anchor gate** (v2.0, replaces the closing-span check) — the STANDARD's
   last unit anchors exactly `synthesis` and carries the token nowhere else; NO compact
   uses the token anywhere;
7. **serve sweep** — X from `floor − 2` to `top + 2`, each X producing a mode
   (`identity | fill/forward | fill/single | fill/backward | synthesis | truncation |
   surrender`, fills annotated with their drop count `-Ns`) with no exception raised;
8. **no defensive truncation** — Case 3 is structurally impossible on a well-formed
   library (§0.4); any non-synthesis-only truncation inside the band FAILS certification;
9. **register clean** (`genon/register_scan.py`, added 2026-08-02) — zero *ban* hits per file
   across `activity_title`, `teacher_notes`, `time_bands[].activity` and `homework[]`: forward
   reference · completion claim · calendar schedule · clock quantity · competency-code leakage.
   A register hit FAILS certification but does NOT quarantine (founder call: quarantine is for
   structure that breaks serving; a register breach makes serving *wrong*, not impossible, and
   is repairable in place). `today`/`yesterday` and backward-positional phrasings surface as
   ADVISORY — a gate that failed on "Will it rain today?" would be switched off in a week.
9a. **MCQ options in arrangement order** (added 2026-08-03 at SS·secondary C3, ARV-D-032) —
   every item's options sorted word-wise (ascending numeric only where an option OPENS with a
   number), labels in sequence. This gate should ALWAYS pass: **STEP 6**
   (`genon/normalize_options.py`) sorts them deterministically before certification, so the
   check exists to prove the stage ran, not to catch the model. The step's own report line —
   `options arranged: N of M item(s) re-ordered` — is printed and **nowhere stored**: the
   `genon_canonical.repairs[]` record was removed on 2026-08-04 (founder ruling: four
   constitution versions moved the rate the wrong way, there is no outside reporting duty and no
   route from the data back into the model, so it was weight in every canonical). Read the count
   on the FIRST pass of a freshly generated library; on a `--certify-only` re-run a 0 means only
   that nothing was left to move. `repairs[]` itself stays in use for `repair_register.py` and
   `repair_anchors.py`, whose edits are declared judgements rather than a pure sort. Items whose
   option text references another option by label are skipped and reported rather than reordered.
10. **item counts per competency — ADVISORY, DOES NOT GATE** (added 2026-08-02 at SS·secondary
   C4). Each file's items are grouped by competency and compared to the mandated count for that
   weight label: `EXACT_ITEM_COUNTS[(subject, stage)]` where the stage's assessment constitution
   has been read at its P2, otherwise the modal count across the library's own variants — which
   still catches a variant disagreeing with its siblings without knowing any constitution. A
   competency the handoff carries but the assessment never touches reports as 0. **It reports and
   never fails** (founder ruling, ARV-D-019: slot misses are generation variance priced below a
   ~₹37 regeneration, hand back-fill is forbidden by §7, and nothing downstream reads item
   counts) — the purpose is to turn a silent miss into a visible rate across 926 authoring runs.
   Read the advisory block at C5 and carry any miss into the stage's C4 record; promote it to a
   gate only if the founder later prices the rate.
**Also:** `backup/quarantine/<subject>/<grade>/` must be EMPTY for this chapter. Failed files
are moved there automatically (founder doctrine 2026-08-01: passing files stay live, only
failures move; a failed TOP takes its whole library with it). Sweep rows carrying drop
counts (`fill/... -Ns`) inside [floor, top] are not failures — they are the declared cost
of that period count, read again at C8 and the human gate.
**Exit:** report says ALL PASS; quarantine empty.
**Artefact:** the report + the sweep table.
*Pilot lesson to keep in view: the first 7-period variant of ch 3 silently DROPPED a section
with no coverage note; the **first-visit check caught it, the serve sweep did not** (X=7 is an
identity request and served the defect happily). Certification catches what serving cannot.*

**C6 [Kumar] API serve checks — the teacher-facing path.** `POST /genon/{subject}/{grade}/{ch}/plan`
with `{"rows": [{"duration": D, "count": X}, …]}`. For a library `{A_top … A_mid … A_low}` run,
at the class-standard duration:

| Request | Identity | Expect |
|---|---|---|
| X = each canonical's own count | kumar1 | `identity: true`, that canonical's own filename, **no new file saved** |
| X between two canonicals (complete fill) | kumar2 | 200; `serve.slot_fill.mode` = `fill` with a `fill_class` (`forward`/`single`/`backward`); `uncovered_sections` empty; a `backward` fill's coverage note names the re-crossed sections as runway, otherwise no note needed |
| X where the prefix completes coverage early | kumar2 | 200; `mode` = `synthesis`; **the borrowed unit is the STANDARD's `synthesis` unit** (`slot_fill.borrowed_from` = the standard's count); note says the closing sitting draws the chapter together |
| X = A_top + 1 | kumar2 | 200; `serve.surrendered_periods` ≥ 1; the surrender sentence appears in **`coverage_note`** (e09 folded it into the same channel as drops), with `serve.surrender_note` kept as provenance; and the **served schedule prints the served count, not the ask** (e10: `period_schedule_display` + the duration label from `genon.served_matrix`; the request survives in `genon.matrix` / `period_rows_snapshot`) |
| X = floor − 1 (below floor) | kumar2 | 200; `mode` = `fill` with non-empty `uncovered_sections`; `coverage_note` names exactly what was not scheduled; **`result.dropped_units`** carries the lost units verbatim, each flagged `unscheduled: true` — **sourced from the LENDING plan's subsequent units** (e12; was: from the chosen plan) |
| mixed-duration weekly matrix | kumar3 | 200; the plan this stage's C7/C8/C9/C12 inspect |

Record the duration the library was authored at. One nuance worth asserting deliberately:
**identity only fires at the authored duration** — ask for the same X at any other duration and
the variant is served whole with proportional scaling, writing a file; assert scaling and exact
tiling there, not identity. (This is the ordinary teacher case, not an edge: her periods rarely
match the authored standard.)
**Mixed matrix (weekly dispersion, the one keeper from v0.4):** assert from `genon.duration_sequence`
that the shortest sitting opens the week and long sittings sit interior and never adjacent.
**Exit:** every row returns as expected; responses recorded. **Artefact:** the responses + files.

**C7 [Claude] Register — audit the gate, judge what it cannot.** Since 2026-08-02 the
mechanical pass is C5's machine gate, so C7 is no longer a word-list sweep. It is three things:
(a) confirm the report's register lines read `0 ban hit(s)` for every file; (b) rule on every
ADVISORY hit — quoted calendar words are usually chapter content, a backward-positional phrase
in a band usually belongs in `teacher_notes`; (c) **read for what regex cannot see** — paraphrased
forward reference ("later in this chapter we shall meet…"), a unit whose opening move assumes
another unit happened, a closing unit that implies completion without saying so. Anything found
here is a new PATTERN for `register_scan.py`, added with a dated note — that feedback loop is
what keeps the gate honest at batch scale, where nobody reads every chapter.

*The original manual procedure, retained as the definition of what is being enforced:* On the C6 plan files (and the library
files) — **including any `result.dropped_units`, which a teacher reads on screen** — every
teacher-facing title and note is checked against the **v1.10 three bans**:
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

**C8 [Claude] The X−1→X transition inspection (v2.3 — replaces LLM-need flags).** The
handover into the borrowed slot is the exact joint that killed two architectures (seam
composition, then mandated closing spans — ARV-D-025), so it is inspected DIRECTLY, on
served plans, every stage. Take the C6 serve set and cover the choice-set classes the
sweep actually exercised — at minimum one plan each of `fill/forward`, `fill/single`,
`fill/backward` (where the band produces one) and the Case-1 `synthesis` borrow, plus the
below-floor serve. For each: read **sitting X−1 and sitting X in full, consecutively, as
the teacher meets them** — titles, teacher notes, opening move, bands, homework — and rate
the transition:
- **clean** — sitting X opens on its own ground; nothing it says presumes a unit the
  prefix didn't contain; any re-crossed section reads as runway, not repetition;
- **serviceable** — a visible register shift (pace, voice, assumed familiarity) a teacher
  absorbs without preparation loss; note it, no defect;
- **jumpy** — sitting X presumes exposure the prefix never gave (the ARV-D-025 profile),
  or re-teaches at a depth that insults what X−1 just did.
Quote the exact strings each verdict rests on — the rating is subjective, the evidence is
not. **Every `jumpy` is a defect (§7)**, and its remedy is deterministic first: check the
lender actually first-deals the section (a certification gap), re-examine the tie-break
that picked this lender over another, harden the brief's self-containment wording — the
constraint is unchanged: **no LLM in the request path.**
**Exit:** a rating per inspected transition, quoted evidence attached; zero `jumpy`, or a
defect per hit. **Artefact:** the transition table, in the tracker comment.

**C9 [Claude] Assessment anchoring across the serve.** Anchoring is UNIT-level: `compile.py`
normalizes `period_ref` (the identity) — legacy `phase_ref` as fallback — onto `unit_ref`, and
`serve.py` remaps unit → sitting. On the C6 plans check:
1. **Prefix remap** — every chosen-variant item whose anchor unit is served carries a
   `period_ref` pointing at that unit's SITTING number;
2. **Borrowed unit brings its own items** — on a fill serve, the fill unit's items come from
   its HOME variant and are anchored to the fill sitting (last sitting), not to a
   chosen-variant unit;
3. **Unserved anchors (REWRITTEN at e13, 2026-08-03 — ARV-D-037).** The old rule here was that
   such an item stays with an empty `period_ref` and a `scheduling_note`. That state was
   neither in nor out: the screen anchors items to units so it rendered nowhere, while the
   EXPORT walks `assessment_items` flat and printed it — 7 of 20 questions on the 8-period
   serve, about units the class never had. The rule now: **an item whose unit is not in the
   plan is not in the plan.** Check (a) no item carries an empty `period_ref`, anywhere;
   (b) items whose anchor unit was not served are ABSENT, and their number is reported in
   `genon.assessment_items_unserved`; (c) on a below-floor serve the DROPPED units' items ARE
   present, anchored to the dropped unit's sitting number in this plan (never the lender's own
   numbering) and flagged `unscheduled: true`, with their handoff rows restored and flagged;
   (d) exports omit exactly the `unscheduled` items, as they omit the dropped units themselves;
4. **No cross-variant references** of any other kind.
**Exit:** zero mis-anchored items; every unserved-anchor item carries the note.
**Artefact:** the anchor table per plan.

**C10 [Claude] Storage conventions.**
1. Library files: `ch_NN_canonical.json` + `ch_NN_canonical_pKK.json` (KK = the variant's
   period count, zero-padded). Served plans: exactly
   `ch_NN_<matrix>_e<ENGINE>_c<chosen-variant-version>.json`, `<matrix>` duration-aggregated
   longest-first (`50m10`, `60m4-50m6`) and the version being the **chosen variant's**
   `canonical_version` — not the top canonical's (`api/data.py::genon_plan_filename`). Live
   proof of the chosen-variant rule on disk: SS·IX ch 3's `50m8` keys on p10 and `50m6` on
   p07, each the variant that served it. The version token is the ledger timestamp and nothing
   else: a repair fingerprint was added 2026-08-03 and **reverted 2026-08-04** (founder — it
   hung an unreadable hash tail off every filename); invalidation moved to the repair tools
   instead, see check 2.
2. **Cache hit, and the purge that keeps it honest** — two halves, and the second is why the
   first is safe: (a) repeat one C6 non-identity request: response has `cached: true` and the
   file's mtime did not change; (b) after any in-place repair of a canonical, the chapter's
   derived plans must be GONE — `genon/purge_derived.py` runs from `repair_register`,
   `repair_anchors` and `normalize_options`, so the next request rebuilds (~11 ms) instead of
   serving pre-repair bytes (ARV-D-034: the pilot served repaired-away text for four hours
   because the key did not move, and only a manual delete dislodged it). Check the purge
   PRINTED what it removed, and that no `ch_NN_<matrix>_e*_c*.json` survives a repair run.
   Cost, accepted: a teacher holding a purged plan loses that file and re-prepares — the
   listing walks the directory, so her dangling register key is skipped, not an error.
3. **No overwrite across engine versions** — every earlier-engine file for this chapter is
   still on disk untouched beside the current ones (a bump re-keys the cache by construction,
   so nothing is ever rewritten in place).
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

**C12 [Kumar runs, Claude inspects] The online view and the exports — the e09 split.** First
the **view**: `GET /api/plans/{s}/{g}/{filename}/view` on the below-floor plan must carry
`dropped_lp` (the unreached units, adapter-shaped), and `LessonView` must page them AFTER the
served units, visibly unscheduled — this is the "give her access to it" ruling. Then the
**exports**, which deliberately OMIT dropped units: for the C6 mixed-duration plan — and it must be
one that includes a **borrowed fill sitting** — all three plan exports
(`GET /api/plans/{s}/{g}/{filename}/export/{lesson|assessment|integrated}`) in both
`format=pdf` and `format=docx`, plus the allocation report (`POST /api/allocation/export-pdf`
and `export-docx`) for this subject·grade. View-model shapes differ by subject (science·ix
section-anchored flat; science middle stage-grouped; english spine-nested) — the export must
render this stage's shape cleanly. **Exit:** `dropped_lp` present and paged last in the view; 8 files open
without error; no blank sections, no raw JSON leaking, unit/phase structure visible and matching
the plan, the borrowed sitting reading as a whole unit, `answers=1` rendering the answer layer,
the coverage note carried through, and **no dropped unit anywhere in any exported file**.

**Also on the mixed-duration plan (added 2026-08-07, ARV-D-066):** the duration line must read
IDENTICALLY wherever the same plan is drawn — the My Lessons card, the proposed/busy card during a
prepare, and the export header. The two renderings had drifted to different separators (" + " vs
" · "), invisible on a single-row matrix and visible the moment a 60+45 week is served. One helper
now (`MyLessonPlans.matrixLabel`, in the server's phrasing); check it holds on a MIXED matrix,
which is the only case that can catch it.

Then, on that same open plan, the teacher's TWO writable marks — the only per-teacher writes on
an otherwise read-only surface. X1.3 and X1.7 state the tenancy property; these are the per-stage
re-verification of it against this stage's real filenames and section keys.

3. **Chapter notes — usage, privacy, persistence.** The notes tab in the axis gutter
   (`LessonView.jsx`, `ChapterNotesModal`) writes localStorage key
   `chapter_notes_{subject}_{grade}_{chapter_title}` through `userKey()`, i.e. suffixed with the
   signed-in user. Check, as kumar1: (a) **usage** — open the notebook from the served plan, write
   a note, close; the tab shows the has-note state and its `title` carries the text; reopening the
   plan restores it. (b) **asset-keying, deliberately section-independent** — the SAME note
   surfaces in preview (My Lessons) and in tracking, and from every section bound to this
   chapter (the per-unit section note was removed 2026-07-23 — one notebook per chapter, and a
   note appearing under only one of two bound sections is a defect). Confirm the key does NOT
   move when the served *matrix* changes: a 50m10 and a 60m4-50m6 serve of this chapter share one
   notebook. (c) **privacy** — sign in as kumar2 on the same browser profile and open the same
   chapter: the notebook is EMPTY, and kumar1's key is still on disk untouched
   (`userKey` suffix is the whole isolation mechanism — a bare `chapter_notes_…` key without a
   user suffix is an S2 defect). (d) **persistence and its limit** — the note survives reload and
   restart, but there is **no notes endpoint**: it stays in the browser profile that wrote it and
   does not follow the teacher to another device. Record as the known limitation (X1.7), not a
   tenancy defect; re-record it each stage so it is never silently assumed fixed. Also confirm
   clearing a note to blank REMOVES the key rather than storing an empty string.
4. **Bookmark — privacy and persistence.** The teacher's ONE phase bookmark per section
   (`web/app/lib/sectionState.js`, cache key `lu_bookmark_{sectionKey}`, server field
   `bookmark_unit`/`bookmark_phase` on `POST /section-state`). Check: (a) set a bookmark on a
   phase of the served plan as kumar1; `GET /section-state` returns both fields (0-based) on that
   section's row, i.e. it **round-trips to the server**, not localStorage alone — this is what
   makes it survive a new browser. (b) **persistence** — reload, and sign in from a second browser
   profile as kumar1: the bookmark reconciles back onto the same unit·phase from the server row.
   (c) **privacy** — as kumar2, `GET /section-state` shows no trace of kumar1's section key or
   bookmark, and the two states live under separate
   `data/section_state/{tenant}/{user}/state.json` paths. (d) **the one legitimate clear** — only
   unbind/bind deletes the row; verify a server row that carries NO bookmark does not wipe a
   locally-held one (the reconcile rule in `sectionState.js`), and that moving the bookmark
   replaces rather than accumulates (one per section, always).
**Exit (3–4):** notes shared across sections and matrices for one teacher and invisible to
another; bookmark round-trips to the server, survives a new browser, isolated per user; the
no-notes-endpoint limitation recorded. **Artefact:** the view response + the 8 files; for 3–4,
the paired kumar1/kumar2 evidence (localStorage keys + `GET /section-state` bodies).

**C13 [Kumar breaks, Claude reads] Failure paths.** Each must surface a message a teacher can
read, with no stack trace in the body:
1. **No canonical** — a chapter number with no library → **404** `"No underlying chapter
   yet."` (wording changed 2026-08-04, founder: "canonical" is our word, not hers — engine
   vocabulary in a teacher-facing string is a defect even when the string is correct)
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

**C14 [Claude] Copyrights review (added at template 2.4, 2026-08-04).** Campaign-level
reference: `docs/NCERT_copyright_review.md` (the formal review against the NCERT copyright
statement, v1.1: F1 closed by founder ruling — private personal backup, canonicals-only to
cloud, PDFs local forever; **F2 — English verbatim task-text in served plans — is the sole
open finding** this step polices). On the library files
and the C6 served plans — every teacher-facing surface, including the exports and any
`result.dropped_units`:
1. **No verbatim textbook reproduction beyond short quotation** — spot-check band text,
   teacher notes, homework and assessment stems/stimuli against the chapter's source
   (`textbooks/{subject}/{grade}/` PDF and the chapter summary). Paraphrase and original
   activity design are the expectation; a lifted passage is a defect. Anchors drawn verbatim
   from the section registry (`section_anchor` titles) are exempt — they are structural
   references, not reproduced content.
2. **No third-party copyrighted material** — poems, song lyrics, story excerpts, brand text
   or images embedded in stimuli/activities that the textbook itself does not carry; where
   the textbook carries it, the plan may reference it (page/task refs, e.g. English's
   `(p.NN)` homework convention) but must not reproduce it wholesale.
3. **Quoted source text is attributed** — anything deliberately quoted names its source;
   an unattributed quotation is a defect even when short.
Subjective calls (how much quotation is "short", whether a paraphrase is too close) are
flagged as such with the strings quoted, and land at the human gate — same doctrine as C3's
register judgements. **Exit:** zero unattributed or wholesale reproductions, or a defect per
hit (§7). **Artefact:** the review table, in the tracker comment.

**HUMAN GATE [Kumar decides, Claude presents] — the stage's sign-off.** Deterministic ALL PASS
is a precondition; this is the verdict. Claude presents, and the founder rules on:
- the **serve-sweep table** (C5.7): what every period count in the band buys, drops named —
  the adaptation table of record now that there is no solver projection to diff;
- **C8's transition table, with the worst-rated X−1→X handover read aloud in full** — the
  founder meets the joint exactly as a teacher would;
- **the STANDARD's `synthesis` unit in full** — does it draw the chapter together as a real
  unit-arc while assuming only section content, never a particular activity? (It is the
  Case-1 borrow: every class that meets it arrived through a different prefix.)
- **each compact's own ending** — freely authored now: does the count's natural condensation
  still teach, or has it collapsed into a summary lecture? (No σ to feed back — the remedy
  is P5's escalation: a fourth canonical, a raised floor, or accepted drops.)
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
3. `GET/POST/DELETE /section-state` — progress + bookmark isolated per user. (This is the
   DEFINITION; **C12.4 re-verifies it per stage** on that stage's served plan — privacy,
   server round-trip, survival into a new browser, and the unbind/bind-only clear.)
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
   Isolation across teachers on one browser is the `userKey()` suffix on
   `chapter_notes_{subject}_{grade}_{chapter_title}`, and nothing else. Record the missing
   endpoint as a known limitation, not a tenancy defect — but a note visible to a second
   signed-in user IS a defect. (**C12.3 re-verifies this per stage**, adding usage and the
   asset-keying rule: one notebook per chapter, shared across sections and matrices.)
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
`GET /subjects/{s}/{g}/chapters` (which also carries `canonical_plan` per chapter now — confirm
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
| `GENON_ENGINE_VERSION` | `api/data.py` (**13** — e13, 2026-08-03: an assessment item whose unit is not in the served plan is dropped, and a dropped unit's questions ride with it; ARV-D-037. See the ladder in §2, 0.2) |
| **Canonical plan row** | `master_plan.json` → `canonical_plan {counts, provisional, basis, registry_sections, authored}` |
| **Brief identity** | the brief files in `genon/out/briefs/` for this chapter — record the git commit of `genon/variant_plans.py` (which composes them) and keep the brief text as an artefact; brief wording is version-bearing even though it is not constitutional |
| Canonical + variant `ledger_ts` | `genon_canonical` block of each library file |
| Certification report path | `genon/out/library_reports/…` |
| **Repairs applied** | `genon_canonical.repairs[]` on each file — tool, reason,each edit's rule and removed text, ban-hit count before/after |
| Plan filename(s) | C6 responses |
| Model | pinned `claude-sonnet-4-6` (record if it ever differs) |
| Date · wall time | run date; per-serve timing (C11) |
| Tokens in / out · cost ₹ | per generation + **library total** (C2) |

## 6a. Recording surface

**No step artefacts (founder, 2026-08-03).** A C-step's record is its **tracker comment plus its
defect rows** — not a `docs/testing_artefacts/*.md` file. Write findings straight into the
tracker: brief, quoted where it matters, one defect per failure. Long-form artefacts are written
only when the founder asks for one. (`docs/testing_artefacts/` keeps what already exists as
history; nothing new lands there by default.)

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

**Repair in place is legitimate — as a pipeline stage, never as an edit session** (founder,
2026-08-02). Some defects are text (a forward-referencing clause, a leaked competency code) and
regenerating to remove them is a lottery at ~₹37 a run. These are fixed by
`genon/repair_register.py`: every edit is a **declared (old → new) pair in code**, applied by
assertion — if `old` is not found verbatim the file is left untouched and the run fails — and
recorded in the artefact at `genon_canonical.repairs[]`, so corpus statistics can still separate
generation quality from repair quality. What may NOT be repaired this way: anything structural or
pedagogical — a cross-unit materials dependency, approach-diversity repeats, a wrong section
anchor. Repairing those would launder content changes as text hygiene; they go to the human gate
or a regeneration decision. Hand-editing an artefact remains forbidden in all cases.

**Quarantine is the fix worklist for generation defects:** a defect on a library file links to
its quarantined path under `backup/quarantine/<subject>/<grade>/`, and closes only when the
regenerated file passes `--certify-only` and the quarantine entry is cleared. Fixes happen
upstream — regenerate, harden the brief, adjust the canonical set (P5.1) — **never by
hand-editing an artefact**.

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

`P1 P2 P3 P4 P5 · stage-sign-off` — then `C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 C13 C14 · GATE`.
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
  version, so the stage **re-certifies in full** — C1 regenerates the whole library and C1–C14 +
  the gate re-run. This is the cost the §3 ordering rule exists to avoid: amend first, certify
  after.
- **RELAXATION-ONLY amendment (stage-scoped, FREE — added 2026-08-09, founder):** where every
  edit in an amendment only **widens or permits** — a bound loosened, an exception added, a
  format licensed — and **nothing is tightened and no new obligation is created**, the installed
  library cannot have been invalidated by it: output that satisfied the stricter text satisfies
  the looser text by construction, and the clauses at issue are usually the very ones the old
  library breached. Such a stage does **NOT** re-author. It runs `--certify-only` and a written
  **clause-by-clause compliance check** of the installed library against each amended clause,
  recorded in the tracker; any clause the library fails is then a defect in the ordinary way.
  **One tightening anywhere in the amendment forfeits this** and it is a constitution change in
  the full sense above — the carve-out is not a judgement about how big the change feels.
  *Worked example, S4 2026-08-09: LP v1.2 → v1.3 (method-cap exception · `activity_title`
  10–13 → 6–13 · `section_context` 10–12 → 6–12, upper bound untouched) and assessment
  v1.1 → v1.2 (OPEN_TASK extended to a synthesis LO) are relaxation-only. The installed library
  was checked against all four and passes three outright; the fourth (OPEN_TASK licensing) it
  passes on the standard's synthesis item and fails on one compact item, which stays open as
  the ordinary defect it always was. No re-author; ~₹111 not spent. The reasoning that settled
  it is worth keeping: **regeneration is a lottery, and the installed library had already been
  repaired.** A re-author would have discarded verified-clean output for a fresh draw on nine
  defect classes that recurred in both prior generations of this chapter — internal-id leakage
  alone went 0 → 31 between them.*
- **Engine / brief / certifier change (corpus-wide, cheap):** the authored artefacts are still
  valid. Re-run `python3 genon/build_library.py <subject> <grade> <ch> --certify-only` across
  every certified chapter and **diff the reports** — same checks, same serve sweep, no rupees.
  Identical sweeps → stages stay certified with the new version recorded in provenance. Any
  changed line → re-run C6–C12 on that chapter. (An engine change that alters served bytes also
  bumps `GENON_ENGINE_VERSION`, which re-keys the cache: every prior `_eNN_` plan file is stale
  by construction, never overwritten.)
- **`master_plan.py` regeneration (data, silent):** it **wipes every `canonical_plan`
  annotation**. Re-run `python3 genon/variant_plans.py` immediately; until then no row —
  counts, floor, authored list — may be trusted, and no certification that cites one is
  valid.

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

> ★ **v2.0 note (2026-08-03).** The record above is the pilot as run — under the mandated
> closing spans the pilot itself helped retire (ARV-D-025 was found in ITS served plans:
> the mandated synthesis in the compacts imported the lending plan's priors — the jumpy
> Xth unit). Its library is PRE-v2.0 on every axis: the plan now reads `{12, 10, 7}` (equal
> dispersion; p09 is orphaned), the standard carries no `synthesis` unit, and the compacts
> carry the old mandated closers — so v2.0 certification rightly fails it. **The pilot
> re-authors under the v2.3 template** (one `build_library.py` run) before its C-steps are
> re-read; its old serve table's `exact/superset/suffix` modes no longer exist.

What the pilot still owes before the template is declared portable: the **re-authored v2.0
library** certified ALL PASS, the **human gate** read in full (C8's worst transition + the
standard's synthesis + each compact's ending), C7/C9/C10/C12/C13 recorded against the
tracker, and a **template retro** — every step whose instruction was ambiguous or whose exit
criterion was uncheckable gets rewritten here before stage 2.

---

## 11. Suggested execution order (after the pilot)

Ordered to retire the riskiest portable assumptions earliest and spend the five Group-B schema
conversions late; one stage fully signed off before the next stage's prep begins.

1. **social_sciences · middle** (S2, time_bands, same subject family as the pilot) — the
   cheapest proof that the template ports at all. Carries MEMORY item 17 and the
   A9-strikes-item-18 case. *P1–P4 done 2026-08-04 (LP v2.8 · assessment v2.4); P5 open.*
2. **science · secondary** (S3, time_bands) — first stage outside the SS family; the
   section-anchored flat export shape (C12).
3. **mathematics · secondary** (S4, time_bands) — confirms the port generalises; the
   cognitive-demand hinge (item 9); note its content gap (8 of 16 chapters have no summary —
   draw the pilot chapter from the eight that do).
4. **the_world_around_us · preparatory** (S5, time_bands) — completes the time_bands group;
   first preparatory stage; item 1 applies.
5. **science · middle** (S6, first Group B) — the cheapest `phases[]` → `time_bands`
   conversion (P3); stage-grouped export shape.
6. **mathematics · middle** (S7), then **mathematics · preparatory** (S8) — Group B with the
   `core_/adjunct_competencies` skill layer; items 14, 15, 16.
7. **english last: secondary (S11) → middle (S10) → preparatory (S9)** — deliberately final:
   three separate stage preps, the largest chapter count (101), the spine-nested export shape,
   the heaviest MEMORY burden (items 2, 4, 5, 8–13), the open X2 calibration question, and the
   one **registry-definition decision** (P5.2) the choice set depends on. By the time English
   starts, the template is boring and only the subject is hard.

Rationale in one line: the pilot proves the template; SS·middle proves it ports and covers the
dual-duration case; science·secondary proves it ports off the pilot's subject family; the rest
is repetition with known risk retired in order of cost.

---

## Corrections note (repository vs brief, checked 2026-08-01)

Verified against the repo (re-checked at step 0.2, 2026-08-02): `GENON_ENGINE_VERSION = "10"`
(`api/data.py`) — the brief was written at e08 and two bumps landed after it, e09 (dropped
sections + surrender folded into `section_coverage_note`) and e10 (served-schedule prints);
the C-steps above carry the added assertions;
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

**Re-checked 2026-08-03 (template 2.3 / architecture v2.0) — the paragraphs above are the
2026-08-01 snapshot; where they disagree with this line, this line wins:**
`GENON_ENGINE_VERSION = "12"`; `aruvi_core/genon/` holds `compile.py` v0.5 · `serve.py`
v2.0/e12 (`variant_solver.py` moved to `_to_delete/`, its test with it; the serve.py
docstring stale-version item is closed by the rewrite); certification implements the C5
list AS REVISED (synthesis-anchor gate, e12 sweep modes, the no-Case-3 gate; no
projected-vs-actual); fill modes are `fill/{forward|single|backward} | synthesis |
truncation` plus `identity` and `surrender`; rows carry `canonical_plan {counts,
provisional, basis, registry_sections, authored}`; SS·IX ch 3's plan reads `{12, 10, 7}`
and its on-disk pre-v2.0 library awaits re-authoring (§10's v2.0 note).
