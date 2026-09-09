#!/usr/bin/env bash
# Smoke-test a deployed (or local) Meyy API. Usage: deploy/smoke.sh https://meyy-api.onrender.com [user]
# Exercises: health · public content · one signed-in state route (X-Aruvi-User stub, until
# Track B swaps it for a Supabase token) · a write that lands on the persistent disk.
# Exits non-zero on the first failure and says which route.
set -uo pipefail
BASE="${1:?usage: deploy/smoke.sh <base-url> [user]}"
USER_ID="${2:-smoke-test}"
H="X-Aruvi-User: $USER_ID"
FAIL=0

check() {  # label, then curl args
  local label="$1"; shift
  printf '%-36s' "$label"
  local out
  if out=$(curl -fsS -m 60 "$@" 2>&1); then
    echo "ok  $(printf '%s' "$out" | tr -d '\n' | cut -c1-80)"
  else
    echo "FAIL  $(printf '%s' "$out" | tail -1)"; FAIL=1
  fi
}

check "GET /health"                  "$BASE/health"
check "GET /subjects"                "$BASE/subjects"
check "GET /subjects/science/grades" "$BASE/subjects/science/grades"
check "GET /legal/privacy (open)"    "$BASE/legal/privacy"
check "GET /readiness (signed in)"   -H "$H" "$BASE/readiness"
check "GET /entitlement"             -H "$H" "$BASE/entitlement"
check "GET /ask-aruvi (ETag)"        -o /dev/null -D - -H "$H" "$BASE/ask-aruvi"
check "GET /section-history (state)" -H "$H" "$BASE/section-history"

echo
if [ "$FAIL" = 0 ]; then
  echo "All green. The signed-in calls JIT-created account '$USER_ID' on the disk —"
  echo "erase it with: curl -X POST -H '$H' -H 'Content-Type: application/json' -d '{\"confirm\":\"erase\",\"downloaded_confirmed\":true}' $BASE/data-rights/erase"
else
  echo "Some routes failed — see above."; exit 1
fi
