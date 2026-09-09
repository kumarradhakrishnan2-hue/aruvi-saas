#!/usr/bin/env bash
# Smoke-test a deployed (or local) Meyy API. Usage: deploy/smoke.sh https://meyy-api.onrender.com [user]
# Exercises: health · public content · one signed-in state route (X-Aruvi-User stub, until
# Track B swaps it for a Supabase token) · a write that lands on the persistent disk.
set -euo pipefail
BASE="${1:?usage: deploy/smoke.sh <base-url> [user]}"
USER_ID="${2:-smoke-test}"
H="X-Aruvi-User: $USER_ID"

step() { printf '%-42s' "$1"; }
ok()   { echo "ok  $1"; }

step "GET /health";                 ok "$(curl -fsS "$BASE/health")"
step "GET /subjects";               ok "$(curl -fsS "$BASE/subjects" | cut -c1-80)…"
step "GET /subjects/science/grades"; ok "$(curl -fsS "$BASE/subjects/science/grades" | cut -c1-80)…"
step "GET /legal/privacy (open)";   ok "$(curl -fsS "$BASE/legal/privacy" | cut -c1-60)…"
step "GET /readiness (signed in)";  ok "$(curl -fsS -H "$H" "$BASE/readiness" | cut -c1-80)…"
step "GET /entitlement";            ok "$(curl -fsS -H "$H" "$BASE/entitlement" | cut -c1-80)…"
step "GET /ask-aruvi (ETag)";       ok "$(curl -fsS -o /dev/null -D - -H "$H" "$BASE/ask-aruvi" | grep -i '^etag' | tr -d '\r')"
step "GET /section-history (state)"; ok "$(curl -fsS -H "$H" "$BASE/section-history" | cut -c1-80)…"
echo
echo "All green. The signed-in calls JIT-created account '$USER_ID' on the disk —"
echo "erase it with: curl -X POST -H '$H' -H 'Content-Type: application/json' -d '{\"confirm\":\"erase\",\"downloaded_confirmed\":true}' $BASE/data-rights/erase"
