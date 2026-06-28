# Aruvi-SaaS — Project Context for Cowork Sessions

Standing briefing for every Cowork session on this repo. Update it whenever meaningful
progress is made. A fresh session starts cold — this file is how context carries forward.

---

## 1. What this is

The greenfield rebuild of **Aruvi** (NCF-aligned lesson planning + assessment for Indian
K–12 teachers) as a cloud-hosted, multi-tenant SaaS. It **lifts the proven IP** out of the
prototype monolith (`../Project Aruvi`, frozen at git tag `prototype-final`) into a clean,
plugin-based architecture. The prototype is the **proven spec + data source**; this repo is
the future product.

Builder context: solo founder + Claude. Architecture favours **managed/serverless** services
and **validation-first** sequencing (ship the visible product on saved data; defer scale).

---

## 2. Architecture & data flow

```
teacher → web (Next.js) → HTTP → FastAPI (api/) → aruvi_core (Python engine)
```
- **`aruvi_core`** = the engine (UI-free, vendor-neutral). Generates/normalizes, allocates.
- **Generate flow:** engine asks the subject plugin to build a prompt → LLM → the SAME
  plugin normalizes the raw JSON into the **canonical view model** → renderer shows it.
  (Live LLM generation is wired but DEFERRED; the API serves saved plans as previews.)
- **Allocate flow:** read each chapter's weight via the plugin → distribute a multi-row
  period schedule across chapters (per-duration columns, remainder method, exact totals).

---

## 3. Conventions (the rules — keep these)

- **Subjects are plugins, not conditionals.** Each subject is a package under
  `aruvi_core/subjects/{name}/` implementing the `Subject` interface; importing it registers
  it in the registry. The engine never branches on subject. Add a subject = implement the
  interface + drop in data; zero edits to shared code.
- **One renderer, many subjects.** Subjects normalize to ONE structure-preserving view model
  (`aruvi_core/view_model.py`). Subject/stage differences (progression-stage vs A/B/C vs
  section→spine vs competency) live as typed/labeled/nestable Groups — NOT in the renderer.
  Visual stimuli are typed (svg / table / prose); never dump raw markup as text.
- **Stage is derived from grade, never a separate input.** Single source:
  `aruvi_core/grades.stage_for(grade)`. Everyone calls it; nobody re-implements the mapping.
- **Ports & adapters** (`aruvi_core/ports.py`): core depends only on `LLMClient`,
  `OutputCache`, `Storage`, `Repository`, `AuthProvider`, `BillingProvider`. Each vendor is a
  thin adapter → no lock-in.
- **Allocate UX:** show the *answer* (periods), not the raw weight number. The flow is four
  explicit steps in `web/app/page.jsx`'s `Allocate` component, gated by its `step` state
  (`"periods" | "select" | "adjust" | "final"`, 2026-06-21): (1) **periods** — define period
  types/durations; (2) **select** — plain checkbox list of chapters, default all selected, no
  allocation numbers yet; the LRM does NOT run live as checkboxes toggle. "Allocate Periods"
  runs it once for whatever is checked; (3) **adjust** — shows the suggested allocation table
  scoped ONLY to the chapters chosen in step 2 (unselected chapters are never displayed, not
  just greyed out), with a collapsible "How are periods allocated?" note
  (`Subject.allocation_basis(grade)`, no numbers, deeper "why" deferred to Ask Aruvi) and a
  binary choice — **Accept Allocation** (saves as-is, Δ=0, no edit UI ever shown) vs **Modify
  Allocation** (styled `.modify-btn`, solid `--ochre` fill, to visually flag the temporary/
  unsaved state before it reveals per-chapter Δ columns, live balance check, Save Allocation
  bar); (4) **final** — read-only Final Period Allocation table. The "Why did Aruvi allocate
  periods this way?" card (`.howbox`) uses fixed copy (not the per-subject factors list as
  bullets) pointing teachers to the Ask Aruvi "How time is allocated across chapters" tab.
  Every period-duration column header is two lines — teacher's chosen name (`.sub-h-name`)
  stacked over its minutes (`.sub-h-min`), e.g. "Core" / "45 min" — in both the suggested and
  Δ column groups, and the Δ group header no longer uses a distinct clay/red color (matches
  the suggested-periods group styling).
- **Output caching** keyed by (subject, grade, chapter, period_profile, constitution_version)
  is the #1 economic lever at seasonal scale — wire it at the service layer when live gen lands.

---

## 4. Design system — "scholarly planner on warm paper"

Calm, credible, academic-but-warm, content-first (the plan is the hero). Defined in
`web/app/globals.css` (CSS variables). Keep new UI consistent with this — don't drift to a
generic look.

- **Type:** Fraunces (`--f-display`, headings/titles) · Newsreader (`--f-body`, lesson prose)
  · IBM Plex Mono (`--f-mono`, structural labels/kickers/numbers). No Inter/system fonts.
- **Palette tokens:** `--paper` warm cream + subtle grain · `--ink` warm near-black ·
  `--pine` (primary accent) · `--clay` + `--ochre` (warm highlights) · hairline `--line` rules.
- **Signature patterns:** a **marginal numbering rail** (period `01`, question `Q1` in the
  margin); **mono uppercase kickers** for structure (PROGRESSION STAGE / SPINE / COMPETENCY /
  SECTION); ledger hairlines; italic-serif sub-labels.
- The on-screen plan/assessment view is a React renderer in `web/app/page.jsx`
  (`ViewModelView` and friends). `aruvi_core/render/html.py` is the separate **export/PDF**
  renderer — keep the two visually aligned.
- **Mobile compatibility is a standing requirement — check it on a regular basis (VERY
  IMPORTANT).** Many Indian K–12 teachers will reach Aruvi on a phone, so the web UI must
  stay usable on small screens, not just desktop. Treat mobile as a first-class viewport:
  - **Every UI change must be verified at a mobile width before it is considered done** —
    use the Cowork preview `preview_resize` (e.g. 390×844, iPhone-class) and `preview_snapshot`
    in addition to the desktop check. No layout regression ships unverified on mobile.
  - Watch for the usual breakages: horizontal overflow / sideways scroll, fixed-width tables
    (Allocate period columns, competency tables), the marginal numbering rail crowding text,
    tap targets too small, and font sizes that don't scale down.
  - Keep responsive rules in `web/app/globals.css` (`@media` breakpoints); don't hardcode
    desktop-only widths in component styles.
- **The Monday-morning feel (design principle, not yet built).** The product still reads as
  planner-centric — built around the plan as artifact, not the teacher's morning as
  experience. The opening moment should land emotionally before it lands technically. A
  teacher opens Aruvi at 8:20 AM; the first five seconds shouldn't show a dashboard, they
  should feel like being met. Something like: "Good morning. Today you teach three classes."
  followed by a short, scannable list —
  - 7A → Period 4
  - 7B → Period 6
  - 8A → Start Chapter 3

  — and one tap from there into the actual lesson. This is a north star for a future
  home/landing view (not yet specced or scheduled — see §9), but every screen built between
  now and then should be judged against it: does this feel like a planner serving the
  teacher's day, or like the teacher serving the tool's structure? When the home view is
  eventually designed, keep it consistent with §4's "scholarly planner on warm paper" system
  (Fraunces/Newsreader/mono kickers) — warmth comes from the words and pacing, not a
  different visual language.

---

## 5. Repo layout

```
aruvi_core/            engine (Python, no UI deps)
  view_model.py        canonical structure-preserving contract
  subjects/            base.py (Subject interface) + __init__.py (registry) + one pkg/subject
  ports.py  engine.py  normalize.py  grades.py  allocate.py  render/html.py
  adapters/            file impls of the ports (allocation + readiness repos; Supabase later)
api/                   FastAPI service (main.py, data.py, config.py) — wraps the engine
web/                   Next.js app (app/page.jsx = login gate + 2 tabs: My Plans + Generate; see §11; app/globals.css = design)
tests/                 test_*.py + fixtures/ (real saved plans + mappings as parity fixtures)
data/                  ★ the single data root (everything that migrates to cloud) — see §7
  content/             Bucket A: read-only CONTENT (chapters, constitutions, framework, sample plans)
  readiness/           Bucket B: per-tenant teaching profiles  → {tenant}/{user}/profile.json
  allocations/         Bucket B: per-tenant allocation registers → {tenant}/{user}/{subject}/{grade}/
docs/                  architecture-plan.md, ALLOCATION_REPORT_*.md, flow PNG, mockups/ (design refs, not loaded by code)
CLAUDE.md MEMORY.md CLOUD_DATA_MODEL.md   standing docs (stay at root by convention)
```

Cleanup/reorg done 2026-06-28: junk purged (out/, .next/, caches, others/), docs consolidated
under `docs/`. `data/` is now the self-contained root (§7). Everything under `data/` except
the README is git-ignored.

---

## 6. How to run

Two dev servers (use the Cowork preview, configs in `.claude/launch.json`):
- **API:** `python3 -m uvicorn api.main:app --port 8000`  (preview name `aruvi-api`)
- **Web:** `npm --prefix web run dev`  → http://localhost:3000  (preview name `aruvi-web`)

First time: `pip install -r api/requirements.txt` and `npm --prefix web install`.
Web fonts load via a Google Fonts `@import` (needs internet, else serif fallbacks).

---

## 7. Data source — self-contained under `data/` (rebuilt 2026-06-28)

The app no longer reads from the prototype mirror at runtime. **All data lives under
`data/`**, the single root that migrates to the cloud. `api/config.py` exposes two seams,
kept strictly apart (the Bucket A / Bucket B split in `CLOUD_DATA_MODEL.md §0`):

- **`DATA_DIR`** (env `ARUVI_DATA_DIR`) — **Bucket A**, shared read-only CONTENT (chapter
  summaries/mappings, constitutions, framework, sample saved plans). Defaults to
  `data/content/` (a self-contained copy lifted from the prototype mirror). The app never
  writes here. Cloud home: object/vector store.
- **`STATE_DIR`** (env `ARUVI_STATE_DIR`) — **Bucket B**, per-user/tenant STATE the app
  writes at runtime. Defaults to `data/` (subfolders `readiness/`, `allocations/`). Cloud
  home: Supabase Postgres.

Both default-derive from the repo root (never hardcoded to a machine). So a fresh clone is
runnable with **no env vars and no sibling `Project Aruvi` folder**. The prototype is still
the *authoring* source for new content (§10), but it is not a runtime dependency.

**Tenanting (no auth yet).** The teacher's user ID arrives in the **`X-Aruvi-User`** request
header (set by the login portal, §11); the API's `_current_identity()` reads it, with
`tenant_id == user_id` (one teacher = one individual tenant — the ICP). Both readiness and
allocations are keyed `{tenant}/{user}/…` on disk, so two teachers never share or overwrite
state. Phase 4 swaps the header read for the Supabase auth token — that one function is the
only change. (Current dev data is under user **`Kumar1`**.)

---

## 8. Tests

Stdlib only; run any directly, e.g. `python3 tests/test_render.py`. Suites: view_model,
science/english/maths/ss/twau ports, render, allocate, **allocation (tenant-keyed register
merge + isolation), readiness (per-tenant persistence + projection-stripping)**, api. Each
subject's parity test runs a REAL saved prototype plan through its normalizers — fixtures are
the acceptance spec. Full suite is **11/11 green** (2026-06-28; the two previously-stale
allocation/api tests were fixed). `test_*` that hit content need `ARUVI_DATA_DIR=$PWD/data/content`.

Tooling note: the Cowork browser preview only rasterizes the first viewport, so scrolled
screenshots can come back blank — verify via DOM (`preview_eval`) or bring content to the top.

**Mobile check is part of "tested" (see §4):** for any UI work, after the desktop pass, run
`preview_resize` to a phone width (~390×844) and re-snapshot to confirm no horizontal overflow,
broken tables, or unreadable text. Do this every session that touches the web UI — mobile
parity is verified routinely, not just at the eventual Expo milestone.

---

## 9. Status & roadmap

**Done:** engine + all 5 subjects (parity-tested) · grade→stage · allocate (multi-row
schedule) · FastAPI · HTML redesign (warm-editorial) · factors note · allocation-report
PDF/DOCX export.

**Editable teaching-profile drill-down — `MyClasses.jsx` (2026-06-28).** The "wizard-as-profile"
pattern (re-launching `Readiness` to edit) is RETIRED. Profile editing now uses a new focused
drill-down: **Subject → Grade → Section**, view-first, one level in focus at a time (back +
breadcrumb). The grade screen is **three tabs** (Annual budget · Duration · Sections →) styled
like the top tabs. **Editing is gated behind an explicit Edit toggle — nothing mutates in view
mode** (every mutator early-returns when `!editing`; budget/durations/day-grid are read-only
displays until Edit); switching grade tabs cancels an in-progress edit. Weekly days are **per
section** (no schema change — the readiness `grids[gradeIdx][secIdx][dayIdx]` was always
per-section). Guided **add** flows (subject → grades multi → sections multi, paged 3/4 at a time
in 5-min duration steps) reuse the readiness "Let us begin" patterns; **delete** warns about
downstream children. The component operates DIRECTLY on the canonical `readiness.subjects[]`,
deep-clone-mutates, `POST /readiness {subjects}` (full replace, same as first-time setup), and
calls `onChange(projectReadiness(...))` so MyPlans/Allocate consumers stay in sync. Budget edits
are stored as `{method:"periods", value}`. Wired in `page.jsx`'s `editFlow` slot (both sidebar
"Edit profile"/"Edit calendar" links land here); `Readiness` is now used ONLY for first-time
setup (in `MyPlans`). Design spec/source: `docs/mockups/editable-profile-tree.html` (the
iterated mockup). **STATICALLY verified only** (babel-parse clean, CSS balanced, pure data-helper
unit tests pass) — per §11 the sandbox can't `next dev`; **live render + mobile (~390px) check is
the immediate must-do before further work.**

**Persistence + tenanting groundwork (2026-06-28) — the front-end-only state is now
server-persisted and per-tenant, ahead of full Phase-4 auth.** Built: (a) a **user-ID login
portal** (`web/app/components/Login.jsx`) gating the app — no password yet; the ID travels as
the `X-Aruvi-User` header (§7). (b) **Readiness persistence** — a `ReadinessRepository` port +
file adapter (`/readiness` GET/POST/DELETE); the teaching profile (subjects/grades/sections/
durations) survives refresh/restart/new browser, keyed `{tenant}/{user}`. (c) **Allocation
register made tenant-keyed** — the `AllocationRepository` port + adapter + engine fns + API
routes all thread `tenant_id/user_id`; path is now `{tenant}/{user}/{subject}/{grade}/`, so
teachers are isolated (was a real multi-tenancy hole). (d) **Self-contained `data/` root**
(§7) — content copied to `data/content/`, state to `data/`; no runtime dependency on the
prototype mirror. All keyed `tenant_id==user_id` today (stub), a clean drop-in for Supabase.
Repo cleanup/reorg also done (§5). NOTE: front-end still verified statically only (see below).

**Planning-layer rebuild (2026-06-27) — the web app was restructured from 3 sibling tabs to
the finalized two-tab, readiness-gated, hub-and-spoke flow** (mocked in
`docs/mockups/index.html`; flow chart in `docs/aruvi_saas_full_lifecycle_flow.png`). See
§11 for the new web architecture. Phases done: 1 (two-tab shell + readiness lock), 2
(readiness setup flow), 3 (Generate hub G2 + generate spoke G7 + G4 total-periods model + G5
howbox), 5 (My Plans dashboard + Learning-Unit lesson view + assessment artifact).
**IMPORTANT — these phases are code-complete and STATICALLY verified only; they have NOT been
live-rendered** (the Cowork sandbox can't load Next.js's arm64 SWC binary, so `next dev`/
`build` don't run there). A local smoke test of the full loop — readiness → unlock Generate →
allocate → accept → hub → generate → My Plans dashboard → teach (Learning Units) → assessment
— at desktop AND mobile widths is the immediate must-do before further UI work.

**Next (in order):**
1. **Phase 4** — Auth + DB + multi-tenancy (Supabase). Groundwork now in place (2026-06-28):
   identity flows via `X-Aruvi-User`/`_current_identity()`; readiness + allocations are
   server-persisted and tenant-keyed behind ports. Remaining: real Supabase Auth (replace the
   header stub + `tenant_id==user_id`), write the Supabase adapters behind the existing
   `ReadinessRepository`/`AllocationRepository` ports, move the lesson pointer + `ready` flag
   off localStorage, enable RLS. See `CLOUD_DATA_MODEL.md §4` checklist (§2.1/§2.2 already
   half-done — tenant key landed early).
2. **Live generation** — Anthropic `LLMClient` adapter + output cache (prompt builders are
   already lifted per subject); wire it into the G7 generate spoke (which currently serves
   saved-plan previews).
3. **LP + assessment PDFs** (same language; screen ↔ print parity).
4. **Payments** (Razorpay) → **mobile** (Expo).
5. **Deferred polish:** G6 selective-reset screen still uses the old modal (not yet the
   G2-aligned select-to-clear danger-zone screen from the mockup); "sample plans" pre-readiness
   surface deliberately parked (it shows only an LP, not the execution/My-Plans value — needs
   a better approach, see mockups Screen S note).

---

## 10. Relationship to the prototype

`../Project Aruvi` (tag `prototype-final`) is the source of: the constitutions, the
`mirror/` data, and the behavioural spec for rendering. It still runs independently. Lift
from it; don't depend on its code. Authoring of new mirror data still happens with the
prototype's in-house pipeline.

---

## 11. Web app architecture (post 2026-06-27 planning-layer rebuild)

The visual + behavioural spec is `docs/mockups/index.html` (screen-by-screen
mockups) and `docs/aruvi_saas_full_lifecycle_flow.png` (the conceptual flow). The
`docs/mockups/readiness-grid-flow.html` is the interactive prototype the readiness
React component was ported from.

**Login gate first.** `page.jsx` renders `Login.jsx` (user-ID portal, no password) until a
user ID is set; the ID is stored in localStorage and sent as `X-Aruvi-User` on every API call
(`web/app/lib/format.js` `withUser()` wraps fetch). Sign-out clears it. `tenant_id == user_id`
server-side (§7).

**Two tabs, not three.** Once signed in, `web/app/page.jsx` renders **My Plans** (default) and
**Generate**. The old standalone "Allocate" tab is folded into Generate. `Generate.jsx` (the
old thin input-panel component) is now DEAD CODE — left on disk, not imported.

**Readiness gates Generate, and is now PERSISTED per user (2026-06-28).** `page.jsx` holds
`ready` + `readiness`, but these are **rehydrated on sign-in from `GET /readiness`** (not just
front-end state): on completing setup it `POST`s the canonical `subjects[]` to the server, and
`projectReadiness()` regenerates the active-subject projection on read. So the teaching profile
survives refresh/restart/new browser. Until readiness exists, Generate shows the locked G1
state (`GenerateTab.jsx`). **Phase 4** swaps the file store for Supabase behind the same
`/readiness` endpoints + `ReadinessRepository` port; the lesson pointer is still localStorage-
only (next to migrate).

**Component map (`web/app/components/`):**
- `Readiness.jsx` — ported from `readiness-grid-flow.html`. Three steps looped per grade:
  class durations (chips) → weekly grid (tap to mark a class at shortest duration, hold/
  right-click to cycle longer; clash detection) → annual budget (4 methods: weeks / periods /
  working days / estimate). **As of 2026-06-27 the flow opens with the conversational
  collection steps 1–4** (the missing piece between Screen 2a and the grid): (1) subjects —
  multi-select, "Tell us what you teach"; (2) grades per subject; (3) sections per subject·
  grade; (4) class durations per subject — then the existing weekly grid + annual budget loop
  PER grade WITHIN each subject, and the whole thing loops per subject. One question per
  screen, "Step N of 6" progress, reassurance microcopy. The hardcoded seeded grade plan is
  gone; the structure is collected. On finish calls `onComplete(payload)`. The payload's
  **canonical** shape is `payload.subjects[]` (self-contained per-subject record:
  name/durations/grades[{grade,sections[{tag,sec}]}]/grids/budget); it ALSO carries a
  denormalized active-subject projection `{subject, grades, durations, grids, budget}` purely
  for backward compat with `MyPlans.classesFromReadiness` + `Allocate.weeklyRatioFromReadiness`
  (do not persist that projection — see CLOUD_DATA_MODEL.md §2.1).
- **`CLOUD_DATA_MODEL.md` (root) is the single source of truth for the Supabase/cloud data
  boundary** (added 2026-06-27): which data is shared read-only CONTENT vs per-user/tenant
  STATE, the proposed tables (incl. the readiness teaching-profile), and the ordered migration
  checklist for Phase 4. Read it before any DB/persistence work.
- `GenerateTab.jsx` — readiness gate (G1) in front of `Allocate`; passes `readiness` through.
- `Allocate.jsx` — the Generate tab's working component. Steps: `periods` (G4) → `select`
  (G3) → `adjust` (G5) → `final` (G2 hub) → `generate` (G7). **G2 hub** = the `final` step:
  allocation table + budget bar + nav buttons (Continue to Allocate → `select`/G3 flow ·
  Continue to Generate → `generate`/G7 spoke · Reset in a danger zone). **G4** = single
  "periods in total" input split across period types by the weekly ratio
  (`weeklyRatioFromReadiness` + `splitByRatio`, largest-remainder; falls back to period-rows
  when readiness absent). Internally the split is written back into `rows` so the rest of the
  flow (engine allocate call, adjust, persist, export) is unchanged. **G5** howbox uses the
  live `allocation_basis` (basis + per-subject factors). The server-backed allocation register
  + PDF/DOCX export are preserved untouched. The `generate` spoke serves saved-plan previews
  (live gen deferred).
- `MyPlans.jsx` — when `!ready` shows the **Screen 2a welcome landing** first ("Let's get
  your week set up" + 1·Weekly grid / 2·Annual budget checklist; gated by local `setupStarted`
  state), and only on tapping "set up →" renders the `Readiness` grid flow. When ready renders
  the **weekly dashboard** (2c): classes from the readiness grid grouped by day, crossed with
  saved plans;
  populated rows show "On: Learning Unit N" (from the localStorage pointer) and open
  `LessonView` on tap; the 2b empty/forward state shows a single CTA to Generate. Falls back to
  a plans-list of openable cards when readiness has no schedule.
- `LessonView.jsx` — Screen 3 + 3b. Flattens `lesson_plan.groups[].periods[]` into Learning
  Units on a continuous rail (done/now/future); activities = phase rows (no fabricated
  minutes); Move-to-next / Stay; **pointer (current LU) persists per section in localStorage**
  key `lu_pointer_{sectionKey}`. "assessment here →" opens the dedicated green assessment
  artifact built from the view model's assessment items.
- `PeriodRows.jsx` (exports `Stepper`, `toPeriodRows`, `periodTypeNames`), `ViewModelView.jsx`
  (the document renderer — used by LessonView's flatten source), `StatePill.jsx`,
  `AllocationReportView.jsx` unchanged.

**Status is execution, and lives in My Plans — never in Generate.** Started / in-progress /
locked is teaching state (the LU pointer); Generate only knows allocated vs. plan-made. This
was a deliberate split during the rebuild.

**Verification reality in Cowork:** the sandbox cannot run `next dev`/`build` (arm64 SWC
binary won't load) and Google-Fonts `@import` stalls the build. So web changes here are
verified **statically** (balanced braces, default exports, prop-contract greps, CSS brace
balance, unit-testing pure helpers like `splitByRatio`). **Live render + mobile check must be
done locally:** `python3 -m uvicorn api.main:app --port 8000; npm --prefix web run dev` — no
`ARUVI_DATA_DIR` needed now (defaults to `data/content/`, §7). Sign in with any user ID
(e.g. `Kumar1`, which has seeded data) to pass the login gate.
