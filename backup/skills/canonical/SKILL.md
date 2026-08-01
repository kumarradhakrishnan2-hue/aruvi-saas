---
name: canonical
description: "Run the Aruvi canonical-library pipeline for one chapter: generate the top canonical (LP + assessment) under the current constitutions, solve and finalize its variant plan, author the compact variants from platform-computed briefs, and certify the library. Picks up where the 'chapter' skill ends (requires summary + mapping on disk). Use when the user asks to generate a canonical, author variants, build a chapter's library, or pre-warm a chapter."
---

# Canonical Library Pipeline

Builds one chapter's complete VARIANT LIBRARY per `docs/variant_canonical_architecture.md`:
the top canonical + compact variants (each a complete plan with its own assessment), the
finalized variant plan in `master_plan.json`, and a certification report. The serve engine
(`aruvi_core/genon/serve.py`) picks the files up with no wiring; the FastAPI is never
invoked and need not be running.

**Read first, every run:** `docs/variant_canonical_architecture.md` (§3 the serving rules,
§4 frontier arithmetic + registry, §5 reverse deduction, §7 the V-series). The constitution
files are the prompt — read the live files fresh each run, never quote them from memory.

## Step 0 — Scope and preconditions (stop on any failure)

1. Confirm subject, grade, chapter number with the user.
2. Preconditions on disk — check, do not create:
   - chapter summary + competency mapping exist (else: run the `chapter` skill first);
   - `data/content/constitutions/lesson_plan/<subject>/<stage>/lesson_plan_constitution.txt`
     and the matching assessment constitution exist; record both VERSION lines;
   - the chapter's row exists in `data/content/allocation_norms/master_plan.json`
     (note `recommended_periods`, `floor_periods_at_standard`, `variant_plan`).
3. If a `ch_NN_canonical.json` already exists for this chapter, ask the user whether this
   run REPLACES it (regeneration re-keys every derived plan — offered, never substituted)
   or should stop.

## Generation runs in the USER'S TERMINAL — never in-session, never in this sandbox

All certified artifacts come from `genon/generate_canonical.py`: pinned
`claude-sonnet-4-6` (the model every constitution was calibrated against), token-logged
to `runtime_data/token_log.csv`, key read automatically from `runtime_data/anthropic.key`
(git-ignored; never print, echo, or log it).

**The Cowork sandbox cannot make credentialed API calls in ANY mode** — the proxy
intercepts `x-api-key` requests (proven 2026-08-01: bogus and real keys return identical
plain-text 401s). Do not retry, tunnel, or work around this, and NEVER author an
installable plan in-session — a session-authored plan is a draft on an uncalibrated
model. The whole mechanical pipeline is therefore ONE command the user runs in their
own Terminal:

    cd <repo root>
    python3 genon/build_library.py <subject> <grade> <chapter>
    # e.g. python3 genon/build_library.py social_sciences ix 3

That driver does everything in order and stops on any failure: top canonical (metered) →
`variant_plans.py` annotate (row finalizes) → briefs written to `genon/out/briefs/` →
each compact variant with its brief (metered, own assessment, installs
`ch_NN_canonical_pKK.json`) → re-annotate → deterministic certification (compile;
anchors verbatim in registry; first-visit order; closing units anchor their mandated
spans; serve sweep across the X range; projected-vs-actual diff) → a report in
`genon/out/library_reports/`. `--certify-only` re-runs the deterministic steps without
spending a rupee. FAILED files are QUARANTINED automatically — moved out of the served
library into `backup/quarantine/<subject>/<grade>/` (the fix worklist; founder doctrine
2026-08-01: good files stay live, only failures move; a failed TOP takes its whole
library with it). Regenerate quarantined variants, then `--certify-only` again.

## The session's flow

1. Run Step 0 (below). If all preconditions pass, give the user the exact one-command
   invocation for their chapter and STOP — tell them to run it in Terminal and come
   back when it finishes (a full library takes a few minutes; every run lands in
   token_log.csv, so C2 costing stays honest).
2. When they return: read the newest report for this chapter in
   `genon/out/library_reports/`. If it says FAILURES, walk the FAIL lines with the
   user and stop — fixes happen upstream (regenerate, adjust sigma, re-run), never by
   hand-editing artifacts. If `partials_at` is non-empty in the master-plan row, raise
   it — that is a sigma / variant-count decision, not something to paper over.
3. If deterministic checks ALL PASS: proceed to the human gate. That gate is the
   session's real work.

## Step 6 — HUMAN GATE (do not skip, do not self-approve; runs AFTER the report passes)

Present to the user and wait for their verdict before calling the chapter certified:
- the projected-vs-actual adaptation table diff;
- the full text of 2–3 borrowed-seam sittings (a prefix unit followed by a borrowed
  closing unit) read as a teacher would meet them;
- each compact variant's closing-synthesis unit in full;
- any register scan hits (clock quantities, forward references, calendar words) in
  teacher-facing text.
Record the verdict. Only after approval, report the library as certified and summarize:
files written, versions used (constitutions + engine), and the serve table.

## Constraints

- Never regenerate the summary or mapping here — that is the `chapter` skill's ground.
- Never edit constitutions mid-run; if a constitution changed since Step 1, the run is
  invalid (the §9 regression rule in `docs/testing.md`) — stop and say so.
- `master_plan.py` regeneration wipes variant plans: if it ran, run `variant_plans.py`
  again before trusting any row.
- One chapter per run unless the user explicitly asks for a batch; in batch mode, the
  Step 6 gate may sample (user chooses the sampling rate) but never disappears.
