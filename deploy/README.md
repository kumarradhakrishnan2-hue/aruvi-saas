# Deploying the Meyy API (Track A — Render)

One Docker web service + one persistent disk. `render.yaml` at the repo root is the
blueprint; this folder holds the container entrypoint and a smoke test. Full context and
the tracks that follow: `docs/mobile_migration_plan.md`.

## First deploy (once, ~15 min)

1. Push `main` to GitHub (the blueprint deploys from the branch it names).
2. Render dashboard → **New → Blueprint** → pick `aruvi-saas` → it reads `render.yaml`.
   Region Singapore, plan Starter (a disk needs a paid instance).
3. Fill the `sync: false` secrets when prompted: `ARUVI_SMTP_HOST/USER/PASSWORD`,
   `ARUVI_MAIL_FROM` — the same values as your local `.env`. Leave them blank to run
   with the file outbox (nothing sends; the log says so at boot).
4. Wait for the build (pip + an 81 MB content copy — a few minutes). The service is up
   when `https://meyy-api.onrender.com/health` answers.
5. `deploy/smoke.sh https://meyy-api.onrender.com` — eight routes, including one that
   writes to the disk. It leaves a `smoke-test` account; the last line prints the erase
   command.

Every later `git push` to `main` rebuilds and redeploys (a few seconds' restart — the
disk pins the service to one instance).

## What lives where in the container

| Path | What | Survives redeploy? |
|---|---|---|
| `/app/aruvi_core`, `/app/api` | code | rebuilt from git |
| `/app/data/cloud/content` | Bucket A-serve (`ARUVI_DATA_DIR`) | rebuilt from git; the served-plan cache written here is lost, and warms from zero |
| `/var/aruvi/state` | Bucket B (`ARUVI_STATE_DIR`) — the DISK | **yes** — every teacher's rows |
| `/app/seed/state` | the three seller-side stores, copied to the disk **only when absent** | n/a |

`data/authoring/`, `data/testing/`, `textbooks/`, `genon/`, `web/`, `tests/` are never in
the image — the Dockerfile copies named paths only and `.dockerignore` refuses them.

## Env vars the service reads

`ARUVI_DATA_DIR` · `ARUVI_STATE_DIR` · `ARUVI_CORS_ORIGINS` (comma-separated web origins;
`*` = open) · `ARUVI_ENTITLEMENT_ENFORCED` · `ARUVI_LP_YEAR` · `ARUVI_SMTP_*` /
`ARUVI_MAIL_FROM` / `ARUVI_SUPPORT_ADDRESS` · `PORT` (Render sets it). Everything else in
`api/config.py` keeps its default.

## Pointing a client at it

Web: `lib/format.js` derives the API host from `window.location` today — set it to the
Render URL for a deployed web build. Mobile: `EXPO_PUBLIC_API_URL`. Identity is still the
`X-Aruvi-User` header until Track B (Supabase Auth) lands.

## Local rehearsal (what was verified 2026-09-09)

Docker Hub was unreachable from the sandbox, so the image was not built there; instead the
Dockerfile's layers were replayed on Python 3.12 + dash: pip resolve, entrypoint seeding
onto an empty `/var/aruvi/state`, second boot not re-seeding, smoke green, a plan serve
(SS·ix ch 4, 16×60 → 200 in 34 ms), DOCX export, erase leaving only the seller-side stores
+ erasure log, and CORS refusing a foreign origin while allowing the configured one.
The first real `docker build` happens on Render — watch that log once.

Run it yourself against a scratch disk:

    ARUVI_SEED_DIR=$PWD/data/cloud/state ARUVI_STATE_DIR=/tmp/aruvi-disk/state PORT=8765 \
      sh deploy/entrypoint.sh &
    deploy/smoke.sh http://localhost:8765
