# `data/` — per-user/tenant runtime STATE (Bucket B)

This folder holds **per-user / per-tenant state that the SaaS app writes at runtime** —
the data a teacher creates, not the IP. It is the local stand-in for the Supabase Postgres
database until Phase 4, and is the *only* thing the cloud migration swaps.

It is **git-ignored** (see root `.gitignore`); only this README is tracked. The contents
are real user data and must never be committed.

## What lives here

| Subfolder | Written by | Future cloud home |
|---|---|---|
| `readiness/{tenant_id}/{user_id}/profile.json` | the readiness setup flow (`/readiness`) | `readiness_*` tables |
| *(later)* saved plans, allocation registers, lesson pointers | their respective endpoints | their respective tables |

Today `tenant_id == user_id` (one teacher = one individual tenant; no auth yet — the user
ID arrives in the `X-Aruvi-User` header). Phase 4 derives both from the Supabase auth token.

## The boundary (why this is separate from the content mirror)

Per `CLOUD_DATA_MODEL.md §0`, there are two kinds of data kept strictly apart:

- **Bucket A — shared, read-only CONTENT** (mappings, constitutions, framework, sample
  plans). Read from `ARUVI_DATA_DIR` (the prototype's authored mirror). The app never
  writes it.
- **Bucket B — per-user/tenant STATE** (this folder). Written from `ARUVI_STATE_DIR`,
  which defaults to this `data/` directory (`api/config.py`).

Keeping content reads and state writes on two different paths is what makes the data layer
genuinely SaaS: nothing the app writes ever lands in the prototype mirror, and the Supabase
migration only has to replace `STATE_DIR`.

## Config

- `ARUVI_DATA_DIR` → Bucket A content (default: prototype mirror)
- `ARUVI_STATE_DIR` → Bucket B state (default: this `data/` folder)
