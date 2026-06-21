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
- **Allocate UX:** show the *answer* (periods), not the raw weight number. A collapsible
  "How are periods allocated?" note enumerates the factors (no numbers) via
  `Subject.allocation_basis(grade)`; deeper "why this chapter" is deferred to Ask Aruvi.
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

---

## 5. Repo layout

```
aruvi_core/            engine (Python, no UI deps)
  view_model.py        canonical structure-preserving contract
  subjects/            base.py (Subject interface) + __init__.py (registry) + one pkg/subject
  ports.py  engine.py  normalize.py  grades.py  allocate.py  render/html.py
api/                   FastAPI service (main.py, data.py, config.py) — wraps the engine
web/                   Next.js app (app/page.jsx = 3 tabs + renderer; app/globals.css = design)
tests/                 test_*.py + fixtures/ (real saved plans + mappings as parity fixtures)
```

---

## 6. How to run

Two dev servers (use the Cowork preview, configs in `.claude/launch.json`):
- **API:** `python3 -m uvicorn api.main:app --port 8000`  (preview name `aruvi-api`)
- **Web:** `npm --prefix web run dev`  → http://localhost:3000  (preview name `aruvi-web`)

First time: `pip install -r api/requirements.txt` and `npm --prefix web install`.
Web fonts load via a Google Fonts `@import` (needs internet, else serif fallbacks).

---

## 7. Data source

The API reads mappings + saved plans from `ARUVI_DATA_DIR` (see `api/config.py`), which
**defaults to the prototype's mirror**:
`/Users/kumar_radhakrishnan/main/kumar/AI/Project Aruvi/app/mirror`.
So keep the sibling `Project Aruvi` folder on disk, OR set `ARUVI_DATA_DIR` to a copy. This
local-disk access is the seam the cloud content store / DB replaces later.

---

## 8. Tests

Stdlib only; run any directly, e.g. `python3 tests/test_render.py`. Suites: view_model,
science/english/maths/ss/twau ports, render, allocate, api. Each subject's parity test runs a
REAL saved prototype plan through its normalizers — fixtures are the acceptance spec.

Tooling note: the Cowork browser preview only rasterizes the first viewport, so scrolled
screenshots can come back blank — verify via DOM (`preview_eval`) or bring content to the top.

---

## 9. Status & roadmap

**Done:** engine + all 5 subjects (parity-tested) · grade→stage · allocate (multi-row
schedule) · FastAPI · Next.js 3-tab app (Allocate live · Generate input panel + saved-plan
preview · My Plans live) · HTML redesign (warm-editorial) · factors note.

**Next (in order):**
1. **Allocation-report PDF** (carry the design language to print).
2. **LP + assessment PDFs** (same language; screen ↔ print parity).
3. **Live generation** — Anthropic `LLMClient` adapter + output cache (prompt builders are
   already lifted per subject).
4. **Auth + DB + multi-tenancy** (Supabase) → **payments** (Razorpay) → **mobile** (Expo).

---

## 10. Relationship to the prototype

`../Project Aruvi` (tag `prototype-final`) is the source of: the constitutions, the
`mirror/` data, and the behavioural spec for rendering. It still runs independently. Lift
from it; don't depend on its code. Authoring of new mirror data still happens with the
prototype's in-house pipeline.
