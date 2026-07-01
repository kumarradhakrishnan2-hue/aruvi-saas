# `data/` — the single migration root (everything that goes to the cloud/Supabase)

This folder is the **one place** all Aruvi data lives until it migrates to the managed
cloud. Both kinds of data sit under here, kept strictly apart per `CLOUD_DATA_MODEL.md §0`.
Everything below is **git-ignored** except the docs/README in this folder; the data itself
is never committed.

```
data/
├── content/      ← Bucket A: shared, read-only CONTENT (the IP)
├── readiness/    ← Bucket B: per-user/tenant STATE (teaching profiles)
├── allocations/  ← Bucket B: per-user/tenant STATE (allocation registers)
├── runtime_data/ ← cost/usage logs (token_log.csv, ask_aruvi.csv, api_rates.json) —
│                   lifted from the prototype 2026-07-01, NOT yet wired into any SaaS
│                   endpoint (no live generation or Ask Aruvi yet); provenance + the rate
│                   table/log schema to reuse once generation lands
├── (saved_plans/, pointers/  ← Bucket B, added as those features land)
└── *.md, *.png   ← design docs (CLOUD_DATA_MODEL.md, flow chart, etc.) — tracked
```

## Bucket A — `content/` (read from `ARUVI_DATA_DIR`)

Shared, read-only content the app serves to every user: chapter summaries + competency
mappings, constitutions, framework text, and the prototype's authored sample saved plans
and Ask-Aruvi KB. **Lifted from the prototype mirror so the SaaS app is self-contained** —
it no longer reads from `../Project Aruvi` at runtime. Regenerable from the prototype's
authoring pipeline, hence git-ignored. The app never writes here.

Cloud home: object store / vector store. Same bytes for every tenant; no tenant key.

## Bucket B — per-user/tenant STATE (written via `ARUVI_STATE_DIR`)

Data a teacher creates. Today written as files under `data/`; each record is keyed by
tenant/user.

| Subfolder | Written by | Keyed by | Cloud home |
|---|---|---|---|
| `readiness/{tenant}/{user}/profile.json` | `/readiness` endpoints | tenant + user (today `tenant==user`) | `readiness_*` tables |
| `allocations/{subject}/{grade}/allocation.json` | allocation register endpoints | subject·grade (tenant key added at Phase 4 — see CLOUD_DATA_MODEL §2.2) | `allocation_register` table |
| `saved_plans/`, `pointers/` | *(later)* | tenant + user | their tables |

Today there is no auth: the user ID arrives in the `X-Aruvi-User` header and
`tenant_id == user_id`. Phase 4 derives both from the Supabase auth token.

## Config (`api/config.py`)

- `ARUVI_DATA_DIR` → Bucket A content. Default: `data/content/`.
- `ARUVI_STATE_DIR` → Bucket B state. Default: `data/`.

Both default under `data/`, so the whole folder is the single migration unit: the cloud
move swaps content reads to the object/vector store and state writes to Supabase, and
nothing outside `data/` is involved.
