# Aruvi-SaaS — Cloud / Supabase Data Model & Migration Boundary

Single source of truth for **what data lives where** when Aruvi goes online (Phase 4 — Auth +
DB + multi-tenancy on Supabase). The point of this document is that the migration is a
*mechanical* job, not a redesign: everything that must move is already enumerated here, with
its current home, its future home, and the table shape it maps to.

Read alongside `CLAUDE.md` §9 (roadmap) and §11 (web architecture). This doc supersedes the
scattered porting notes for the data question specifically.

Last updated: 2026-07-04 (§2.4 refreshed to the now-server-backed section teaching-state;
added §2.6 the plan archive — a per-tenant flag, since Aruvi never hard-deletes a lesson plan).

---

## 0. The one rule

> **Two kinds of data, kept strictly apart:**
> **(A) shared, read-only CONTENT** — the IP. Same for every user. Moves to shared/object
> storage (or a vector store), never per-tenant.
> **(B) per-user / per-tenant STATE** — what a teacher entered or produced. Moves to the
> Supabase Postgres DB, every row keyed by `tenant_id` + `user_id`.
>
> Nothing in (A) is ever written at runtime by a teacher. Nothing in (B) is ever shared
> across tenants. If a new piece of data doesn't fit cleanly in one bucket, stop and decide
> before building — that decision is the whole game for clean multi-tenancy.

---

## 1. Bucket A — shared read-only CONTENT (the IP)

Same bytes for every customer. No tenant key. Today these are local files read via
`ARUVI_DATA_DIR` (defaults to the prototype's `mirror/`). In cloud they become shared object
storage and/or a vector store; the engine reaches them only through the `ports.py` adapters,
so the swap is an adapter change, not an engine change.

| Content | Today (local) | Cloud home | Notes |
|---|---|---|---|
| Subject constitutions (LP / assessment / mapping) | `mirror/constitutions/...` | Object store (versioned) | Keyed by `constitution_version` — feeds the output-cache key. |
| Framework text (CG + pedagogy) | `mirror/framework/...` | Object store → vector store | Vector store is the scale play for retrieval. |
| Chapter summaries | `mirror/chapters/{subject}/{grade}/summaries/` | Object store / vector store | Pre-computed once, reused forever. |
| Competency mappings / effort index | `mirror/chapters/.../mappings/` | Object store | Drives Allocate weights. |
| Generated-plan output cache | (not yet wired) | Supabase table OR object store, keyed by `(subject, grade, chapter, period_profile, constitution_version)` | **Shared, not per-tenant** — same chapter → same plan. #1 economic lever (CLAUDE.md §3). Cache is content, NOT user state. |

Migration action: stand up the object store / vector store, write `Storage` + (future)
`Repository` adapters in `aruvi_core/adapters/`, point `ARUVI_DATA_DIR`'s replacement at them.
No schema, no tenant key.

---

## 2. Bucket B — per-user / per-tenant STATE (→ Supabase Postgres)

Everything a teacher enters or produces. **Every table below carries `tenant_id` + `user_id`**
(RLS row-level-security policies enforce isolation). Today these live in front-end React
state, browser `localStorage`, or local JSON files with **no tenant key** — that absence is
the only real migration work.

### 2.1 Teaching profile — the readiness payload (NEW, from setup steps 1–4 + grid + budget)

Emitted by `web/app/components/Readiness.jsx` via `onComplete(payload)`. **This is the
canonical per-teacher setup object.** Today it lives only in `page.jsx` state (`readiness`)
and is lost on refresh. It is the single biggest item Phase 4 must persist.

The component already emits a **persist-ready shape**: the canonical `subjects[]` array
(self-contained per subject), plus a denormalized "active subject" projection that exists
ONLY for current consumers and must **not** be stored as its own table.

Canonical shape (`payload.subjects[]`, one element per subject):

```
{
  name: "Science",
  durations: [45, 60],                       // minutes, this subject
  grades: [
    { grade: "VI", sections: [ {tag:"6A",sec:"A"}, {tag:"6B",sec:"B"} ] },
    { grade: "VII", sections: [ {tag:"7A",sec:"A"} ] }
  ],
  grids:  [ /* [gradeIdx][sectionIdx][dayIdx] = durationIndex | -1 */ ],
  budget: { 0: {method:"weeks", value:36}, 1: {method:"periods", value:210} }
}
```

Proposed Supabase tables (JSONB columns keep it a near-drop-in of the array above; normalize
later only if reporting needs it):

```
readiness_profile        (tenant_id, user_id, created_at, updated_at)            -- one per teacher
readiness_subject        (id, tenant_id, user_id, subject, durations jsonb)      -- one per subject
readiness_subject_grade  (id, subject_id, grade, sections jsonb,                 -- one per subject·grade
                          weekly_grid jsonb,                                     -- the [section][day] grid
                          budget_method text, budget_value int)
```

The front-end `ready` boolean and `activeSubjectIndex` are session UI state, NOT persisted —
`ready` is derived server-side as "a completed `readiness_profile` exists for this user".

> **Do NOT persist** `payload.subject / payload.grades / payload.grids / payload.durations /
> payload.budget` (the top-level keys). They are a derived active-subject projection for
> `MyPlans.classesFromReadiness` and `Allocate.weeklyRatioFromReadiness`. Regenerate them on
> read from the tables above.

### 2.2 Annual allocation register (already has a clean seam)

Periods allocated across chapters per subject·grade. **Already** behind a ports/adapters seam:
`AllocationRepositoryFileImpl` (file-based) implements the `Repository` port; `api/main.py`
notes "Supabase adapter comes later".

| Today | Cloud |
|---|---|
| `mirror/.../allocation register` JSON via `AllocationRepositoryFileImpl` | `allocation_register` table; write `AllocationRepositorySupabaseImpl` against the same port |
| Browser cache `localStorage["allocations_{subject}_{grade}"]` | Stays as a client cache; server register remains source of truth (it already "wins" on reconcile — Allocate.jsx) |

Table: `allocation_register (tenant_id, user_id, subject, grade, allocation jsonb, updated_at)`.
Migration action: implement the Supabase adapter; **no engine or API-route change** (the route
already calls through `engine.get_allocation_register(..., allocation_repo=...)`).

### 2.3 Saved lesson plans + assessments

| Today | Cloud |
|---|---|
| `mirror/saved_plans/{subject}/{grade}/*.json` (no tenant key) | `saved_plan` table, JSONB `result`, keyed by tenant/user |

Table: `saved_plan (id, tenant_id, user_id, subject, grade, chapter_number, chapter_title,
result jsonb, created_at)`. Read path `api/main.py:/plans/...` swaps its `data.py` file reads
for DB reads behind the same `Repository` port.

### 2.4 Section teaching-state (lesson execution) — ALREADY server-backed

Per section: which chapter it tracks, how far along (the "current Learning Unit" pointer), and
whether it's done. The only true execution state (CLAUDE.md §11: "status is execution, and lives
in My Plans"). **As of 2026-07-03 this is no longer localStorage-only** — it's persisted through
the `SectionStateRepository` port (`SectionStateRepositoryFileImpl`, at
`STATE_DIR/section_state/{tenant}/{user}/state.json`), so tracking + progress already follow a
teacher across devices; `localStorage` is now just an optimistic cache reconciled from the server
on load. The file adapter is tenant-keyed today (`tenant_id == user_id` stub).

| Today | Cloud |
|---|---|
| `SectionStateRepositoryFileImpl` → `state.json` `{section_key: {chapter, unit_index, done, updated_at}}`, plus a `localStorage` mirror | `lesson_pointer` table |

Table: `lesson_pointer (tenant_id, user_id, section_key, chapter, unit_index, done, updated_at)`
(the pointer extended with `chapter` + `done` to match the file shape). Migration action: write
`SectionStateRepositorySupabaseImpl` behind the existing port — no API-route or component change.

### 2.5 Feedback, token/cost log, Ask-Aruvi log (operational telemetry)

From the prototype runtime (`runtime_data/`, `mirror/feedback/`). Per-tenant once online.

Tables: `feedback (tenant_id, user_id, kind, payload jsonb, created_at)`,
`usage_log (tenant_id, user_id, model, tokens_in, tokens_out, cost_inr, at)`.

### 2.6 Plan archive — a per-tenant flag (Aruvi never hard-deletes a plan) — ALREADY server-backed

**Decision (2026-07-04):** a lesson plan is **archived, never deleted**. Rationale: a generated
plan is the most expensive artifact a teacher owns, and the teacher-specific state wrapped around
it (section attachments, the §2.4 pointer, notes) is irreplaceable even when the plan content
itself is cheaply regenerable from the shared output cache (§1). So the only removal affordance is
a reversible **archive** — a per-tenant FLAG, not a move. The plan asset stays exactly where it
lives (today it's shared read-only sample content in `DATA_DIR`; once live-gen lands it's the
per-tenant `saved_plan` of §2.3); archiving only records the plan's identity in this per-tenant
store, and My Lessons filters it out of the active list. **Attached plans cannot be archived** (the
UI shows no archive control), so an archived plan is always detached — nothing to reconcile on
restore, which is lossless.

Persisted through the `PlanArchiveRepository` port (`PlanArchiveRepositoryFileImpl`, at
`STATE_DIR/plan_archive/{tenant}/{user}/archive.json`) as `{plan_key: archived_at_iso}`, where
`plan_key = "{subject}/{grade}/{filename}"` (the same identity used to load the plan). API:
`GET/POST/DELETE /plan-archive`; `GET /plans/...` annotates each listing with `archived` +
`archived_at`.

| Today | Cloud |
|---|---|
| `PlanArchiveRepositoryFileImpl` → `archive.json` `{plan_key: archived_at}` | Either an `archived_at timestamptz null` **column on `saved_plan`** (cleanest once §2.3 plans are per-tenant), OR a standalone `plan_archive (tenant_id, user_id, plan_key, archived_at)` table while plans are still shared content |

Migration action: write `PlanArchiveRepositorySupabaseImpl` behind the existing port. Prefer the
`saved_plan.archived_at` column when live-gen makes plans per-tenant (§2.3) — then "restore" is
just nulling the column and there is no separate table to keep in sync. There is deliberately **no
purge / TTL**: the archive is permanent-until-restored (the economics argue for keeping it). A
future explicit, gated "empty archive" would be the ONLY place a true hard delete could ever live.

---

## 3. Identity & tenancy (the new top layer)

Does not exist today (single local user). Phase 4 introduces it via Supabase Auth.

```
tenant   (id, name, type 'individual'|'school', plan, created_at)
app_user (id, tenant_id, email, role, auth_uid)        -- auth_uid = Supabase auth.users.id
```

ICP mapping (CLAUDE.md / prototype §2): an **individual teacher** = a tenant of type
`individual` with one `app_user`; a **CBSE school** = a tenant with many `app_user`s.
Every Bucket-B table FK's to `tenant_id` (+ `user_id` where row-owned). **RLS policy on every
Bucket-B table: `tenant_id = auth.tenant_id()`** — the single guard that makes multi-tenancy
safe.

---

## 4. Migration checklist (do in this order)

1. **Auth + tenancy**: Supabase Auth; create `tenant` / `app_user`; derive `ready` from a
   persisted `readiness_profile` instead of the front-end flag.
2. **Persist the teaching profile** (§2.1): create `readiness_*` tables; have the shell call a
   `POST /readiness` on `onComplete` and load it on sign-in. Drop the lost-on-refresh state.
3. **Swap repositories behind existing ports** (§2.2–2.6): `AllocationRepositorySupabaseImpl`,
   saved-plan adapter, `SectionStateRepositorySupabaseImpl` (§2.4), `PlanArchiveRepositorySupabaseImpl`
   (§2.6 — or fold into a `saved_plan.archived_at` column). Engine/API routes unchanged — all four
   already call through their ports.
4. **Move shared content** (§1) to object/vector store via the `Storage` adapter; retire
   `ARUVI_DATA_DIR`.
5. **Wire the output cache** as shared (NOT per-tenant), keyed by content version (§1 last row).
6. **Telemetry tables** (§2.5).
7. **Enable RLS** on every Bucket-B table and test cross-tenant isolation before launch.

---

## 5. Invariants to keep checking (grep-able)

- No teacher-entered data without a `tenant_id` (+ `user_id` for row-owned data).
- No shared content carrying a tenant key (would break the cache economics and the IP model).
- Core/engine never talks to Supabase directly — only through `aruvi_core/ports.py` adapters
  (mirrors the prototype's "provider seam" rule).
- The denormalized readiness projection (§2.1) is never persisted as its own table.
