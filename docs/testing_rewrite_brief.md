# Brief: rewrite testing.md for the variant-canonical era

2026-08-01 · Founder + Claude. This is the INPUT for a future session that rewrites
`docs/testing.md` (currently the 25-combo partition-era template, VERSION 1.0
2026-07-29). Read alongside: `docs/variant_canonical_architecture.md` (the spec),
`docs/partition_constitution_rollout.md` (what still ports), `genon/build_library.py`
(the driver), `.claude/skills/canonical/SKILL.md` (the session flow), and MEMORY.md's
2026-07-31 / 08-01 entries. Everything below is settled founder decision, not proposal.

## 1. The headline structural change: 11 stage rows, not 25 class rows

**Certification is per subject·STAGE, one randomly chosen class per stage.**
Constitutions are per stage; classes within a stage share them, so testing every class
re-proved the same constitution at 2–3× cost. The new matrix is the 11 stages
(S1–S11 as already tabled in old §3): english prep/mid/sec, mathematics prep/mid/sec,
science mid/sec, social_sciences mid/sec, TWAU prep. Per stage: pick ONE class at
random, record the pick (and how it was made) in the tracker; that class's one pilot
chapter carries the full cycle. Residual risk to handle in the rewrite: a stage can
span two standard durations (middle = 40 min for VI–VII but 45 for VIII) — the random
pick may miss one. Cover it deterministically, not with more generation: the serve
sweep and API checks run at BOTH durations (free), and note in the tracker which
duration the generated library used.

## 2. What replaced the partition engine (test object changed entirely)

- A chapter = a LIBRARY of variant canonicals: `ch_NN_canonical.json` (top, at
  master_plan `recommended_periods` × class-standard duration) + compact variants
  `ch_NN_canonical_pKK.json`, counts and mandated closing-synthesis spans solved per
  chapter into master_plan.json's `variant_plan` row (genon/variant_plans.py;
  provisional until the top exists, finalized after; re-run it after any
  master_plan.py regeneration — that wipes the rows).
- Serving = SELECTION (serve.py v1.1, engine e08): next-highest variant, first X−1
  units verbatim (one WHOLE unit per sitting), slot X from the fill ladder
  (exact > superset > longest-suffix > truncation; plus `synthesis` mode when the
  frontier already covers every section), FRONTIER arithmetic (backward-anchored
  synthesis tails are legal), proportional per-unit duration scaling (the only
  arithmetic), weekly dispersion of mixed matrices (kept from v0.4), surrender only
  above the top variant (declared). Identity requests (matrix == any variant's
  standard row) register that file, no copy. Cache keyed by CHOSEN variant's version.
- Assessments are per-variant, unit-anchored: items carry `period_ref` (compile v0.5
  normalizes `unit_ref`; legacy `phase_ref` maps through as fallback); a borrowed fill
  unit brings its own items re-anchored to the fill sitting; items whose anchor unit
  is unserved carry the scheduling note.
- GONE and never tested again: DP cuts, CUT_COST, compression regimes (stretch /
  rescale / role-weighted / unit-drop), COVERAGE_FLOOR 0.6 mechanics, seam text,
  role_handoff, unit_handoff, wide spans, mid_unit_openings, band_id/band_refs/
  phase_ref as declarations (band ids are DERIVED internally). polish long gone.

## 3. Constitutional state (what P-prep now amends)

- Reference pair: SS·secondary LP **v1.10** · assessment **v1.5**.
- Per-stage carry-forward is EXACTLY: **A1** (single standard row) · **A5/A7** (the
  v1.10 SELF-CONTAINED REGISTER re-cut: three bans only — clock quantity, forward
  reference/completion language, calendar time; backward references are now LEGAL,
  content-named continuity is best practice not prohibition) · **A6-confirm** (items
  carry their anchor unit — verify, amend only if absent) · **A9** (MCQ arrangement
  convention, all 11 assessment constitutions; item-18 files first; corpus-repair debt
  stands) · **P3** (Group B `phases[]`→`time_bands[{minutes,activity}]` — no band_id)
  · **P4** (sidecar changelogs). **A2/A3/A4 cancelled; X3 void.**
- **The V-series is NOT constitutional** (founder ruling): the variant brief is
  post-constitution — platform-composed, prepended to the prompt, invisible to the
  constitution; `build_library.py`'s certifier enforces it in code. No V-rules, no
  INPUTS acknowledgment, no precedence line, anywhere. Brief wording iterates freely
  (no §9 cascade).

## 4. The execution machinery (what a combo's cycle actually runs)

- **Generation is Terminal-only**: the Cowork sandbox blocks credentialed API calls in
  every mode. One command per chapter: `python3 genon/build_library.py <subject>
  <grade> <ch>` — top canonical → annotate → briefs (genon/out/briefs/) → compact
  variants (each with its brief, own assessment) → re-annotate → deterministic
  certification → report in `genon/out/library_reports/`. `--certify-only` re-runs
  the free steps. Model pinned claude-sonnet-4-6; key at `runtime_data/anthropic.key`;
  every run logged to token_log.csv (`canonical_generation` / `variant_generation`).
- **Quarantine doctrine**: certification FAILures are MOVED to
  `backup/quarantine/<subject>/<grade>/` (the fix worklist); passing files stay live;
  a failed TOP takes its whole library. The defect register should link to it.
- **The canonical skill** (account + .claude/skills/canonical): session does
  preflight → hands the user the command → reads the report → runs the HUMAN GATE
  (adaptation diff, borrowed seams read in full, each closing synthesis, register
  scan). The gate never self-approves; in batch mode it samples but never disappears.
- Deterministic certifier checks (already implemented — the rewrite should cite, not
  respecify): library complete vs variant_plan counts; anchors verbatim in top
  registry; first-visit order; coverage reaches the final section; closing units
  anchor their mandated spans; serve sweep (floor−2 .. top+2) with expected outcome
  per X; projected-vs-actual table diff.

## 5. Pilot evidence to fold in (SS·IX ch 3, complete, 2026-08-01)

- Library {12, 9, 7} (σ=2, floor 7 — floors now round-to-NEAREST; 143 rows corrected;
  master_plan.md retired, JSON is the single artifact).
- Costs: top ₹39.43, variants ₹36.51 + ₹35.05, one defect rerun ₹34.71 → ₹145.70
  all-in. Extrapolation: ~₹120–190 per library sync; corpus ≈ ₹30–40k sync / ₹15–20k
  batch (batch mode deferred until the mass pre-warm).
- The first 7-variant SILENTLY DROPPED a section (no coverage note) — caught by the
  first-visit check, NOT by the serve sweep (X=7 identity would have served it).
  Fix was brief wording (total-coverage clause) + one rerun. Lessons the rewrite must
  encode: certification catches what serving cannot; briefs iterate at failure speed;
  Rule-4's shortfall note is not available to variants.
- Final serve table (all PASS): X=5,6 suffix (below floor — honest partials by
  design); 7 identity; 8 superset (runway); 9 identity; 10 exact; 11 synthesis;
  12 identity; 13–14 surrender.

## 6. Concrete guidance for the rewrite of testing.md

Keep: the tracker (§6a surface, adapted to 11 rows), provenance discipline (§6 — add
brief content/git identity and variant_plan row to the per-run fields), the defect
register + severities (§7), the pilot-first doctrine (§10 — SS·secondary stage is the
pilot and is DONE for its C-steps in substance), the ordering rule (amend stage
constitutions before certifying the stage), the template-change regression note.

Rewrite: §1 matrix → 11 stage rows with the random-class rule; §3 P-prep checklist →
the §3 list above (A2/A3/A4 struck); §4 the per-stage cycle → roughly:
  C1 run build_library for the chosen chapter (Terminal) · C2 cost the LIBRARY from
  token_log (per generation + total) · C3 canonical + one compact vs the stage
  constitution, rule by rule · C4 MEMORY amendment items (list unchanged; item
  applicability re-checked per stage) · C5 read the certification report (ALL PASS
  required; quarantine empty) · C6 API serve checks: identity per variant, one
  between-variant X, one above-top surrender, one below-floor, and a mixed-duration
  weekly matrix — at BOTH stage durations where the stage spans two · C7 register
  scan on teacher-facing text (three bans of v1.10 — the old word-list loses its
  positional entries) · C8 LLM-need flags (unchanged) · C9 assessment anchoring:
  period_ref remap + borrowed-unit items + scheduling notes on a below-floor serve ·
  C10 storage: e08 filenames, chosen-variant cache keys, `_pKK` variants, no-overwrite,
  determinism diff · C11 serve wall time (<5s, expect ms) · C12 exports on one served
  plan incl. a borrowed-fill sitting · C13 failure paths (no canonical → 404; matrix
  >60 → 400; unresolvable item anchor → named 500; plus: quarantined variant absent
  from serving) · HUMAN GATE as combo sign-off.
Drop: the five-regime C5 matrix, seam/wide-span checks, handoff checks, X3, all
role/band assertions, the e07 bump plan (engine is already e08).
§9 regression gains a distinction: constitution change → stage re-certifies (as now);
engine/brief/certifier change → `build_library --certify-only` re-run + report diff
across certified chapters (free); master_plan regeneration → re-run variant_plans.py
before trusting any row.

X1 (tenancy) and X2 (effort index) survive as cross-cutting checks; note the
2026-08-01 archive fix (archived plans excluded from the section-attach chooser and
the tour) plus the two open judgment calls beside it (Prepare's "already prepared"
treatment of archived plans; Year Plan counting archived periods).
