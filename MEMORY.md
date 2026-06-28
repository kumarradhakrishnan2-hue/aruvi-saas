# Aruvi-SaaS — Accumulated Learnings & Carry-Forward Notes

## 2026-06-28 — Persistence + tenanting + self-contained `data/` + repo cleanup

### What changed (big session — see CLAUDE.md §5/§7/§9/§11)
- **User-ID login portal** (`web/app/components/Login.jsx`) now gates the app. No password
  yet: the ID is stored in localStorage and sent as the **`X-Aruvi-User`** header on every
  API call (`format.js` `withUser()` wraps fetch). Server `_current_identity()` reads it;
  `tenant_id == user_id` (one teacher = one individual tenant). Phase-4 swaps for Supabase Auth.
- **Readiness is now server-persisted** (was front-end only — that gap is closed). New
  `ReadinessRepository` port + file adapter; `/readiness` GET/POST/DELETE. Profile survives
  refresh/restart/new browser. Stores ONLY canonical `subjects[]`; the denormalized projection
  is stripped on save and regenerated on read via `projectReadiness()` (format.js).
- **Allocation register made tenant-keyed** (it was NOT — a real multi-tenancy hole: all
  teachers shared one register per subject·grade). Threaded `tenant_id/user_id` through the
  `AllocationRepository` port → file adapter → engine fns → API routes. Path is now
  `allocations/{tenant}/{user}/{subject}/{grade}/allocation.json`.
- **Self-contained `data/` root.** Content copied prototype-mirror → `data/content/`
  (`ARUVI_DATA_DIR` default); state at `data/` (`ARUVI_STATE_DIR` default). Both repo-derived,
  no machine hardcoding. **App no longer reads the prototype mirror at runtime.** Two seams in
  `api/config.py`: `DATA_DIR` (Bucket A content) vs `STATE_DIR` (Bucket B state).
- **Repo cleanup/reorg.** Purged junk (`out/`, `web/.next/`, caches, `.DS_Store`, `others/`);
  consolidated design docs under `docs/` (incl. `docs/mockups/`, `docs/architecture-plan.md`).
  All moved-file references were comment/doc-only (no code paths) — rewritten to new paths.
- **Tests:** added `test_readiness.py` + rewrote `test_allocation.py` (tenant isolation, new
  signatures, redraw-ready record schema); fixed stale `/health` assert in `test_api.py`.
  **Full suite 11/11 green.**

### Key decisions / carry-forwards
- **`tenant_id == user_id` is the deliberate stub** until Supabase Auth. Every Bucket-B record
  already carries both keys, so Phase-4 is a value swap in `_current_identity()`, not a schema
  change. Grep invariant (CLOUD_DATA_MODEL §5): no teacher data without a tenant key.
- **Never persist the readiness active-subject projection** (subject/grades/grids/durations/
  budget top-level keys) — derived sugar, regenerated on read. The file adapter strips it
  defensively even if the frontend sends it.
- **Sandbox cannot DELETE files in the mounted repo** (`Operation not permitted`) — only
  create/overwrite. So destructive cleanup must be a script the USER runs on their Mac
  (`tidy_repo.sh` was the vehicle this session). `clear_*` adapter methods fall back to
  overwriting-empty when unlink is blocked, so resets never 500.
- Current dev data is under user **`Kumar1`** (`data/readiness/Kumar1/…`, `data/allocations/Kumar1/…`).

### Verification limitation (unchanged, still important)
- Web/React changes are verified **statically only** (sandbox can't run `next dev`). The full
  login→readiness→allocate→teach loop must be smoke-tested locally at desktop + mobile widths.
  Local run is now `python3 -m uvicorn api.main:app --port 8000; npm --prefix web run dev`
  with **no `ARUVI_DATA_DIR` needed** (defaults to `data/content/`).

## 2026-06-27 — Planning-layer rebuild (web app restructured to the finalized flow)

### What changed
- Web app went from **3 sibling tabs** (Allocate / Generate / My Plans) to the finalized
  **two-tab, readiness-gated, hub-and-spoke** flow. Spec: `docs/mockups/index.html`
  + `docs/aruvi_saas_full_lifecycle_flow.png`. Full architecture documented in **CLAUDE.md §11**.
- New components: `Readiness.jsx` (ported from `readiness-grid-flow.html`), `GenerateTab.jsx`
  (readiness gate + folds in Allocate), `LessonView.jsx` (Learning-Unit lesson view +
  assessment artifact). Rebuilt: `MyPlans.jsx` (weekly dashboard). Reshaped: `Allocate.jsx`
  (added G2 hub `final` step, G7 `generate` spoke, G4 total-periods model, G5 howbox).
- `Generate.jsx` (old thin component) is now **dead code** — not imported; safe to delete later.

### Key decisions / carry-forwards
- ~~**Readiness state is front-end only**~~ **(SUPERSEDED 2026-06-28: now server-persisted +
  tenant-keyed via `/readiness`; see top entry.)** Original note: lived in `page.jsx`, threaded
  to GenerateTab/MyPlans. Still front-end-only: the **LU pointer** (`localStorage` key
  `lu_pointer_{sectionKey}`) — next to migrate.
- **G4 weekly ratio** comes from the readiness grid (`weeklyRatioFromReadiness`) and splits the
  single total-periods input via `splitByRatio` (largest-remainder — unit-tested, always sums
  exactly). Falls back to period-rows when readiness data absent. Internally still writes into
  `rows` so the engine allocate call + persist + export path is unchanged.
- **Status belongs in My Plans, not Generate** (deliberate): started/in-progress/locked is
  execution state (the LU pointer); Generate only knows allocated vs. plan-made.
- **G7 generate spoke serves saved-plan previews** — live generation still deferred.

### Verification limitation (important, recurring)
- **The Cowork sandbox cannot run `next dev`/`next build`** — Next.js's arm64 SWC native
  binary fails to load, and the Google-Fonts `@import` stalls the build. So all web work this
  session was verified **statically only** (brace/export/prop-contract greps, CSS brace
  balance, unit-testing pure helpers). **None of Phases 1/2/3/5 has been live-rendered.**
  A local smoke test of the whole loop at desktop + mobile is the must-do before more UI work:
  `export ARUVI_DATA_DIR="../Project Aruvi/app/mirror"; python3 -m uvicorn api.main:app
  --port 8000; npm --prefix web run dev`.

### Deferred / parked
- **G6 selective-reset screen** not yet aligned to the mockup (still the old modal, not the
  G2-styled select-to-clear danger-zone screen).
- **Sample-plans pre-readiness surface** parked — it exposes only an LP, not the execution/
  My-Plans value; needs a better approach (mockups Screen S note).

## 2026-06-22  *(allocations note below SUPERSEDED 2026-06-28 — register is now file-persisted AND tenant-keyed; only the Supabase swap remains)*

### Allocations persistence (accumulation model)
- **What was built:** The Allocate tab now accumulates allocations — when a teacher allocates a second set of chapters, both sets persist in the Final view, not just the latest one.
- **Current scope:** In-memory during the session (state-based). Survives page navigation but resets on browser refresh.
- **Portability note:** When moving to Supabase, allocations must be persisted to the DB keyed by (subject, grade, user/teacher_id). Each allocation set should be a row with (chapter_numbers[], period_rows[], final_allocation_data). The UI `allAllocations` array becomes a DB query + cache in the API layer.
- **Migration path:** Add a `POST /subjects/{subject}/{grade}/save-allocation` endpoint in the FastAPI layer (api/main.py) that writes to Supabase. The web component calls it instead of just updating local state. Keep the in-memory `allAllocations` as a display cache during the session.

### Text updates (2026-06-22)
- Changed "AI Suggested Allocation" → "Suggested allocation" (line 248, Allocate.jsx)
- Changed period-definition subtitle to "To begin, set the total number of periods available and how long each period type lasts below." (line 370, Allocate.jsx)
