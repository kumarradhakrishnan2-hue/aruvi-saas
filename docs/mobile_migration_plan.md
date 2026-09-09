# Mobile migration plan — the external stack, and the order of work

*Decided 2026-09-09. Companion to `mobile_migration_assessment.md` (the measurement, 2026-09-04);
this is the plan. Supersedes the assessment's §7 phasing where the two differ.*

## 0. The stack (founder, 2026-09-09)

| Concern | Choice | Behind which port |
|---|---|---|
| API host | **Render** — one Docker web service + one persistent disk | — |
| Database | **Supabase Postgres** | the 15 `*Repository` ports in `ports.py` |
| Identity | **Supabase Auth**, phone OTP | `AuthProvider` (`_current_identity()` is the ONE caller) |
| OTP delivery | **an Indian SMS provider** (Textlocal native in Supabase; MSG91/Kaleyra/Exotel via the Send-SMS hook) | inside Supabase Auth |
| RLS / backups / admin | Supabase | — |
| Payments | **deferred** — beta on `ManualBillingProvider` grants, no purchase screen in the app (assessment §5B) | `BillingProvider` |
| Content (Bucket A-serve) | in the image for the beta; Supabase Storage later | `Storage` (five methods) |

**What this changes in the assessment:** its Step 0 was "container + volume, Supabase can
follow." Choosing Supabase now folds Phase 4 (Auth + DB, CLAUDE.md §9 item 1) into the mobile
track. It stays *under* the screens: the rule from assessment §8 — **each step ships a screen
against the live API** — is kept, and the Postgres move happens port by port underneath.

## 1. Two decisions taken as defaults (say so if either is wrong)

1. **The web channel switches to Supabase Auth at the same time as the app.** One identity
   path; `HeaderAuthProvider` survives only behind an env flag for local dev and the stdlib
   tests.
2. **First mobile screens ship against the Render disk, not against Postgres.** The ports
   guarantee the screens cannot tell; waiting on 15 adapters before the first screen would
   invert the assessment's own rule.

## 2. Tracks

### Track A — deployed API on Render ★ BUILT 2026-09-09 (not yet deployed)

`Dockerfile` · `.dockerignore` · `render.yaml` · `deploy/entrypoint.sh` · `deploy/smoke.sh` ·
`deploy/README.md` (the deploy steps). `api/config.CORS_ORIGINS` (env `ARUVI_CORS_ORIGINS`,
comma-separated; `*` = today's open behaviour) replaces the hardcoded `*`; the middleware
also exposes `ETag` and `Content-Disposition`, which cross-origin JS could not read before.

Three facts the repo settled while building it:
- **`data/cloud/` is tracked in git** (CLAUDE.md §5's "everything under data/ is git-ignored"
  was stale — `.gitignore` says so itself). So Render's clone already carries the 81 MB
  content tree and no sync step exists. **`data/authoring/` is tracked too**, which is why the
  image copies NAMED paths only and `.dockerignore` refuses the founder-secure roots twice.
- State is never in the image. The disk at `/var/aruvi` holds Bucket B; the entrypoint seeds
  ONLY the three seller-side stores outside the tenant shape (`invoices/_series`,
  `support/_series`, `consents/_ledger`) and only onto an empty disk — numbering continues
  (MEY/2026-27/78xx, MEY-S-…) rather than restarting. A production disk starts with no teachers.
- The served-plan cache is written into the container's own content tree and is lost on
  redeploy — a reconstructible ~ms cache, warm-from-zero (CLOUD_DATA_MODEL §1).

Verified (Python 3.12 + dash, the image's runtime; Docker Hub was unreachable from the
sandbox so the first real `docker build` is Render's): seeding, no re-seed on second boot,
smoke green, plan serve 34 ms, DOCX export, erase, CORS fencing. **Owed: the deploy itself,
then `deploy/smoke.sh https://meyy-api.onrender.com`.**

### Track B — Supabase Auth + Indian OTP (start the paperwork FIRST)

- **DLT is the long pole.** Transactional SMS in India needs TRAI DLT entity registration, a
  sender header and an approved OTP template — days to weeks, regardless of provider. File
  it before writing code.
- Supabase issues/verifies/rate-limits the OTP; the provider only delivers. Textlocal is a
  native Supabase option; MSG91/Kaleyra/Exotel go through the *Send SMS* auth hook.
- Backend: `SupabaseAuthProvider.verify_token()` verifies the Supabase JWT (JWKS),
  `user_id = sub`, `tenant_id = sub` (the individual-teacher stub carries over);
  `_current_identity()` reads `Authorization: Bearer …`. The `0000` stub dies here, not at the
  assessment's step 5.
- Client: `supabase-js` `signInWithOtp` → `verifyOtp`; the access token goes to FastAPI.
- `Account.privacy_notice` stamping at `/onboarding/verified` and the consent ledger are
  keyed by the identity — they move unchanged; the ONLY thing that changes is what an id IS.

### Track C — Postgres adapters, in beta-flow order, under the screens

Follow `CLOUD_DATA_MODEL.md` table shapes. Each adapter sits behind its existing port, is
swapped in the one wiring block of `api/main.py`, and must pass the existing suite. Order =
the order a teacher meets them:

1. `accounts`, `academic_years` — identity lands → account row
2. `readiness`, `allocations` — FirstRun
3. `section_state`, `section_history`, `prepared_plans`, `plan_archive`, `plan_notes` — the teaching loop
4. `consents`, `entitlements`, `support`, `invoices`, `erasure_log`, `outbox` — Settings/admin
5. the three outside-the-shape stores get their own tables the erase traversal cannot reach —
   same rule, new home

`aruvi-scripts/migrate_state_to_postgres.py`, idempotent like `migrate_cloud_layout.py`.
RLS on every table, keyed `tenant_id, user_id` — and be plain about it: FastAPI holds the
service-role key, so RLS is defence in depth; **the fence stays `_current_identity()`.**
Point-in-time recovery on for the beta. When group 5 lands, the Render disk goes.

### Track D — Expo (unchanged from the assessment)

Assessment §7 steps 1–4: `packages/shared` + the synchronous MMKV storage shim (web stays
green), scaffold + tokens + fonts, **LessonView first**, then the two list screens, FirstRun,
Settings/Ask Meyy/share-sheet exports. One difference: Login/OTP in step 1 is Supabase.

## 3. Phasing

| Wk | Backend | Mobile |
|---|---|---|
| 1 | Render live on disk; DLT filed | `packages/shared` + storage shim |
| 2 | `SupabaseAuthProvider`; SMS hook | Expo scaffold, tokens, fonts, Login via Supabase OTP |
| 3–4 | Postgres groups 1–3 | LessonView · My Classes · My Lessons |
| 5 | Postgres groups 4–5, RLS, backups | FirstRun → PrepareLesson → profile |
| 6 | Content → Supabase Storage (optional) | Settings · Ask Meyy · exports |
| 7 | — | TestFlight / Play internal |

Payments stay parked; `BillingProvider` is the seam when it is settled.
