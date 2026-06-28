# Aruvi — Greenfield SaaS Architecture Plan

## Context

The prototype has served its purpose: it proved the organizing logic generalizes across
subjects and stages (secondary maths rode on secondary science). It is, by design,
patchwork — a 9,100-line `app.py` monolith with subject logic duplicated across 3–4 layers,
file-based storage, Streamlit-coupled UI, and in-process threading. Reforming it in place
would inherit every patch.

Decision: **build a clean, robust architecture that treats the prototype as a proven
specification** — lift the durable IP (constitutions, `mirror/` data, the `llm_client`
seam, PDF generators, prompt-assembly logic) and leave the scaffolding behind.

Constraints that shape every choice:
- **Target:** cloud-hosted, **multi-tenant** SaaS; robust **web (HTML/React)** + **native
  mobile**; **seasonal high-volume** spikes.
- **Builder:** solo founder + Claude Code → architecture must **minimize ops** (lean on
  fully-managed / serverless services; little to run by hand).
- Prototype is **safe**: committed `d0b9b22`, pushed to `origin/main`; textbook PDFs archived.

---

## Guiding principles

1. **Lift, don't drag.** Reuse proven Python logic as a clean library; discard the monolith.
2. **Managed-first.** Every stateful/ops-heavy concern (DB, auth, queue, storage, payments)
   is a managed service, because the team is one person + AI.
3. **Multi-tenant and cache-first from day one** — not retrofitted. Tenant isolation and
   output caching are foundations, not later levers.
4. **Async by default.** Generation takes minutes; it never blocks a request.
5. **Subjects are data + plugins, not conditionals.** The #1 lesson from the prototype.
6. **No vendor lock-in — ports & adapters.** Core logic talks to abstract interfaces
   (`LLMClient`, `AuthProvider`, `Storage`, `Queue`, `BillingProvider`, `Repository`); each
   vendor is a thin adapter behind its port (the same pattern `llm_client.py` already
   proves). Swapping a provider = write one adapter, never touch the engine or app.
7. **One renderer, many subjects.** Subjects differ in *prompt / validation / structure*,
   not in *presentation*. Every subject normalizes its output into one **canonical view
   model**; a single **shared renderer** turns that into HTML / PDF / DOCX / mobile. Rule:
   curriculum changes touch one subject package; styling/branding/mobile-layout changes
   touch one renderer — never the reverse.
8. **Validation-first; don't overbuild.** The spine to paying schools is
   `aruvi_core → API → Auth → DB → Web`. Everything else — pgvector/semantic retrieval,
   heavy worker orchestration, and **mobile** — is deferred until there is repeatable paid
   traction. The biggest risk is building a Series-A architecture before customers pay, not
   scaling too late. Mobile stays a designed-for target (the API + view model keep it cheap
   to add via Expo later), but is not built pre-traction.

### Substitutability (how cheaply each component can be swapped later)

| Component | Swap cost | Note |
|---|---|---|
| `aruvi_core`, frontend (web/mobile), compute host, object storage, queue/cache | **Cheap** | Pure-Python core; frontend speaks only the HTTP API; containerized compute is host-agnostic; storage/queue behind adapters. |
| Database (Postgres) | **Cheap with discipline** | Use Supabase as "just Postgres" — avoid proprietary features; data/schema move to any Postgres. |
| **Auth, Payments** | **Code cheap, DATA sticky** | App sits behind adapters, but these hold *user identities / live subscriptions* — migrating that data is a real operational exercise. Design these adapters most deliberately; keep entitlement + cost truth in **our own** Postgres, with the provider as just the mechanism. |

Three habits that preserve this freedom: **(1)** containerize everything; **(2)** keep a
clean HTTP API between frontend and backend; **(3)** every external service behind an
adapter, with our own DB as source of truth for users, entitlements, and the cost ledger.

---

## Target architecture

**`aruvi_core` (Python library — the lift).** Extract the generation engine out of `app.py`
into a standalone, UI-agnostic package: constitution loading, prompt assembly, `llm_client`
seam, JSON normalization, and PDF generation. Clean interface, e.g.
`generate_lesson_plan(subject, grade, chapter, period_profile) -> Plan`. No Streamlit, no
file-path assumptions — inputs in, artifacts out. This is reused identically by API workers,
batch jobs, and tests.

**Subject abstraction (redesign).** Replace scattered `if subject == ...` / `is_mathematics`
flags with a `Subject` interface + registry. Each subject is a **self-contained package**
(`subjects/{subject}/` holding its constitution, `prompt_builder`, `validator`, and a
`to_view_model` normalizer). The engine stays tiny — it asks the registry for a subject and
calls the interface; it never learns what "Science" or "English" is. Adding subject N+1 =
implement the interface + drop in constitution/data — zero edits to shared code. Directly
kills the "shotgun surgery" debt and the silent per-subject breakage class.

**Common view model + shared renderer (the rendering seam).** Subjects emit wildly different
shapes today (Maths A/B/C sections, Science progression stages, English main_sections×spines,
SS competency mappings). Each subject's `to_view_model` collapses its shape into ONE canonical
view model (e.g. `periods[]`, `assessment_groups[]`, `teacher_notes[]`, typed
`visual_stimulus`). A single shared renderer consumes only the view model to produce HTML /
PDF / DOCX / mobile. This is what prevents re-importing the prototype's worst debt — the
SVG / pipe-table / prose / drama branches duplicated across `lpa_page.html` *and*
`assessment_pdf_generator.py`. Visual-format handling (SVG, tables, etc.) lives once, in the
renderer, keyed off the view model's typed fields.

**Guardrail — the view model is structure-PRESERVING, not flattening.** The common view model
must NOT equalize the subject-specific organizing structures developed iteratively in the
prototype. It unifies *visual style* (fonts, spacing, cards, branding, print/mobile layout)
while *preserving organizing structure* as data. Each subject's distinctions survive as typed,
labeled, nestable groups carrying their own metadata — and the renderer is **structure-driven**
(renders whatever groups/labels/metadata the model declares; never `if subject == ...`):
- **English** → two nested axes: `section` groups containing `spine` groups.
- **Social Science** → `competency` groups (c_code, description, weight).
- **Mathematics (middle)** → `section` assessment groups labeled A / B / C.
- **Mathematics (secondary)** → `section` assessment groups each carrying `implied_lo`.
- **Science** → `progression_stage` groups.

Two safeguards keep this from silently drifting to a flat model:
1. **Parity spec.** The prototype's current per-subject outputs (English Ch1, SS, Maths-middle,
   Maths-secondary, Science) are the acceptance tests. The new pipeline must reproduce each
   layout's structure. If the view model cannot express a distinction, the *view model* is
   wrong and gets enriched — the subject is never bent to fit a poor model.
2. **Typed-block escape hatch.** For genuinely bespoke visuals (e.g. a special geometry
   widget), the view model carries a *typed block* and the renderer has a handler keyed on
   block *type* (still never on subject). Only if a thing resists all generalization may a
   subject ship its own render component — kept exceptional by design.

Rule: expressing a subject's distinct structure is *data the renderer honors*, not a violation;
the violations to prevent are cross-subject coupling (English change forcing a Science edit)
and cross-concern coupling (restyling forcing an English edit).

**API (FastAPI).** Stateless web tier. Validates, authenticates, enforces tenant scope and
usage limits, enqueues generation jobs, serves results. Wraps `aruvi_core`.

**Async generation (queue + workers).** API enqueues → autoscaling Python workers run
`aruvi_core` → artifacts to object storage, metadata to DB → client notified (poll / SSE /
push). Queue absorbs seasonal bursts; workers scale out and to zero. Idempotent jobs,
retries with backoff on Anthropic errors, dead-letter queue.

**Data layer (multi-tenant):**
- **Managed Postgres** — tenants (school / individual teacher), users, saved plans
  metadata, feedback, **per-tenant token/cost ledger**, subscriptions. Every row carries
  `tenant_id`; enforce with row-level security.
- **Object storage** — generated PDFs/JSON artifacts.
- **Content store (read-only)** — constitutions, framework, summaries, mappings. Start as
  versioned files/object storage; evolve to **pgvector** (semantic retrieval at scale —
  keeps it inside Postgres, less to manage).
- **Redis (managed)** — cache, rate-limit counters, queue backing.

**Auth & tenancy.** Managed auth (Supabase Auth or Clerk). Model: Organization (school) →
Users; individual teacher = org-of-one. JWT → API. Roles: teacher, school-admin.

**Payments.** Razorpay (India-first: UPI, cards, subscriptions); Stripe optional later for
intl. Subscription plans + **usage metering tied to the cost ledger** (protects margins
under seasonal load).

**Web frontend.** Next.js (React) multi-tenant SPA + SSR for marketing/SEO. Allocate,
Generate, My Plans, Ask Aruvi. Renders from the **canonical view model** the backend
produces — so the web app, PDF/DOCX export, and a future mobile app all consume the same
shape (the prototype's HTML/template logic is lifted as a behavioral spec for the shared
renderer, not as per-subject code).

**Native mobile (deferred until web traction).** **Expo / React Native (recommended)** so the
mobile app shares language, components, and API contracts with the web React stack — the only
realistic path for a solo + AI build (vs. separate Swift + Kotlin codebases). Flutter is the
alternative if native feel outranks web code-sharing. Not built until schools actively use
the web app and subscription/renewal behaviour is validated (teachers plan mostly on laptops);
the API + view model keep it cheap to add when that day comes.

**Observability & resilience.** Structured logging, error tracking (Sentry), uptime + cost
alerts, per-tenant rate limiting, autoscaling — the spike-resilience story.

---

## AI cost & scale strategy (the seasonal-spike core)

Unit economics at high volume is the make-or-break. In priority order:
1. **Output cache (the dominant lever)** keyed by `(subject, grade, chapter, normalized
   period_profile, constitution_version)` — identical requests served from storage, never
   re-hitting Anthropic. When 50 teachers all generate "Grade IX Science, Ch 3, 8 periods,"
   we generate once and serve variants. This is the single biggest determinant of whether
   Aruvi is a profitable or an expensive SaaS, and pre-warming popular chapters before a
   season turns most peak demand into cache hits.
2. **Prompt caching ON** (the built 1h-TTL lever) — ~90% savings on static constitutions for
   the generations that *do* hit the model.
3. **Per-tenant metering + plan limits + concurrency caps** — bounds cost and Anthropic
   rate-limit exposure.

---

## Recommended concrete stack (solo + AI, managed-lean)

Marked as recommendation — the **cloud-provider choice is the one decision worth confirming**
before Phase 0, since it anchors everything else.

| Concern | Recommendation |
|---|---|
| Core engine | Python package `aruvi_core` (lifted from prototype) |
| API | FastAPI (containerized) |
| Compute host | Render / Fly.io / Cloud Run (autoscale to zero + up) |
| Queue + cache | Managed Redis (Upstash) or Cloud Tasks |
| DB + Auth + Storage + vectors | **Supabase** (Postgres + Auth + Storage + pgvector) |
| Web | Next.js (React) |
| Mobile | Expo / React Native |
| Payments | Razorpay (+ Stripe later) |
| LLM | Anthropic, via the existing `llm_client` seam |

---

## Phased roadmap (realistic for solo + AI)

Phases 0–4 are the spine to paying schools and are the focus. Phase 5 (mobile, infra scale,
pgvector/advanced retrieval) is explicitly **gated on Phase 4's paid-validation exit** — do
not pull this work forward.

- **Phase 0 — Foundations & safety.** Tag prototype `prototype-final`. New clean repo.
  Extract `aruvi_core` from `app.py` + define the `Subject` interface (port 1 subject end-to-
  end as the reference). Stand up the chosen cloud project + managed-service skeleton +
  secrets. *Exit:* `aruvi_core` generates a plan for one subject outside Streamlit, in cloud.
- **Phase 1 — Core API + async generation.** FastAPI over `aruvi_core`; queue + worker;
  object storage for artifacts; Postgres schema (tenants/users/plans/cost); prompt + output
  caching on. *Exit:* end-to-end generate via API, cached, cost-logged.
- **Phase 2 — Auth + multi-tenancy + web.** Managed auth, tenant isolation (RLS), Next.js
  web app for all tabs, per-tenant saved plans/feedback. *Exit:* two isolated tenants using
  the web app.
- **Phase 3 — Payments + metering + admin.** Razorpay subscriptions, usage limits tied to
  the cost ledger, school-admin role. *Exit:* a tenant can subscribe and is metered.
- **Phase 4 — Harden for peak + launch slice.** Load test, autoscale tuning, retries,
  observability. Launch a narrow slice (1–2 subjects) to a small cohort in an off-peak
  window. *Exit:* real teachers paying; clean economics.
- **Phase 5 — Native mobile + scale.** Expo app on the same API; broaden subjects; scale
  infra and (if needed) move content to pgvector ahead of the high-volume season.

---

## Safety / migration

- Prototype repo frozen at `prototype-final`; it remains the **spec + data source**.
- New repo for the SaaS; `aruvi_core` is the bridge (proven logic, clean shape).
- `mirror/` data migrates into the content store / DB; constitutions versioned.
- No cutover risk: the prototype keeps running locally until the SaaS slice is proven.

---

## Decisions to confirm (recommendations marked above)

1. **Cloud provider / managed-service set** — the anchoring choice (Supabase + container
   host recommended). 
2. **Mobile framework** — Expo/React Native (recommended) vs. Flutter vs. fully-native.
3. **Seasonal peak date** — sets the runway working backward from the launch window.

## Verification / milestones

Each phase has an explicit *Exit* gate above. Earliest concrete proof point: **Phase 0** —
`aruvi_core` produces a correct lesson plan + assessment for one subject, invoked from a
plain script (no Streamlit) and running in the cloud project, with the prototype's output as
the golden reference for parity.
