#!/usr/bin/env bash
# C13 — failure paths, mathematics IX ch 4. Runs all four checks and marks each PASS/FAIL.
#
# Everything it creates, it removes. The cleanup runs even if you Ctrl-C halfway or a
# check fails, so the repo cannot be left with a scratch chapter or a quarantined variant.
#
#   cd ~/main/kumar/AI/aruvi-saas
#   bash docs/testing_artefacts/c13_run.sh
#
# The API must be running in another Terminal tab:
#   python3 -m uvicorn api.main:app --port 8000

set -uo pipefail
API="${API:-http://localhost:8000}"
USER_HDR="X-Aruvi-User: kumar1"
PLANS="data/content/saved_plans/mathematics/ix"
QUAR="backup/quarantine/mathematics/ix"
SCRATCH="$PLANS/ch_99_canonical.json"
PASS=0; FAIL=0

cleanup() {
  rm -f "$SCRATCH"
  if [ -f "$QUAR/ch_04_canonical_p09.json" ]; then
    mv "$QUAR/ch_04_canonical_p09.json" "$PLANS/" 2>/dev/null
    echo "  (restored ch_04_canonical_p09.json from quarantine)"
  fi
}
trap cleanup EXIT INT TERM

say()  { printf '\n\033[1m%s\033[0m\n' "$*"; }
check() { # check <label> <expected-code> <expected-substring> <code> <body>
  local label="$1" wantc="$2" wants="$3" gotc="$4" body="$5"
  if [ "$gotc" = "$wantc" ] && printf '%s' "$body" | grep -qF "$wants"; then
    printf '  \033[32mPASS\033[0m  %s  [%s]\n' "$label" "$gotc"; PASS=$((PASS+1))
  else
    printf '  \033[31mFAIL\033[0m  %s\n        want %s containing %s\n        got  %s  %s\n' \
      "$label" "$wantc" "$wants" "$gotc" "$body"; FAIL=$((FAIL+1))
  fi
  # a traceback must never reach the response body, whatever the code
  if printf '%s' "$body" | grep -qE 'Traceback|File "'; then
    printf '  \033[31mFAIL\033[0m  %s — TRACEBACK IN BODY\n' "$label"; FAIL=$((FAIL+1))
  fi
}
post() { # post <chapter> <json-rows>  -> sets CODE and BODY
  local out
  out=$(curl -s -w '\n%{http_code}' -X POST "$API/genon/mathematics/ix/$1/plan" \
        -H 'Content-Type: application/json' -H "$USER_HDR" -d "$2")
  CODE=$(printf '%s' "$out" | tail -1)
  BODY=$(printf '%s' "$out" | sed '$d')
}

if ! curl -s -o /dev/null --max-time 3 "$API/docs"; then
  echo "The API is not answering on $API — start it first:"
  echo "    python3 -m uvicorn api.main:app --port 8000"
  exit 1
fi

say "1 · a chapter we have not authored yet  →  404, in her language"
post 16 '{"rows":[{"duration":50,"count":10}]}'
check "no library" 404 "No underlying chapter yet." "$CODE" "$BODY"
if printf '%s' "$BODY" | grep -qi 'canonical'; then
  printf '  \033[31mFAIL\033[0m  the body says "canonical" — our word, not hers\n'; FAIL=$((FAIL+1))
fi

say "2 · a period count that cannot be real  →  400"
post 4 '{"rows":[{"duration":50,"count":61}]}'
check "over the ceiling"       400 "Period count implausibly large."      "$CODE" "$BODY"
post 4 '{"rows":[{"duration":40,"count":31},{"duration":60,"count":30}]}'
check "over the ceiling (sum)" 400 "Period count implausibly large."      "$CODE" "$BODY"
post 4 '{"rows":[]}'
check "nothing to serve"       400 "At least one duration row is required." "$CODE" "$BODY"

say "3 · a chapter whose question points at a lesson that does not exist  →  500 naming it"
cp "$PLANS/ch_04_canonical.json" "$SCRATCH"
python3 - "$SCRATCH" <<'PY'
import json,pathlib,sys
p=pathlib.Path(sys.argv[1]); d=json.loads(p.read_text()); d['chapter_number']=99
def items(o):
    if isinstance(o,dict):
        if isinstance(o.get('questions'),list): yield from o['questions']
        for v in o.values(): yield from items(v)
    elif isinstance(o,list):
        for v in o: yield from items(v)
it=list(items(d['result']))[3]; it['period_ref']=[99]; it['section_number']=99
p.write_text(json.dumps(d,indent=1,ensure_ascii=False))
print("  (scratch chapter 99 created, one question pointed at a lesson that isn't there)")
PY
post 99 '{"rows":[{"duration":50,"count":10}]}'
check "names the broken question" 500 "Canonical cannot be compiled" "$CODE" "$BODY"
printf '  body: %.190s\n' "$BODY"
rm -f "$SCRATCH"

say "4 · a variant we have condemned must be invisible  →  serves from another, never names it"
mkdir -p "$QUAR"
mv "$PLANS/ch_04_canonical_p09.json" "$QUAR/"
post 4 '{"rows":[{"duration":50,"count":8}]}'
if [ "$CODE" = "200" ] && ! printf '%s' "$BODY" | grep -qF 'p09'; then
  printf '  \033[32mPASS\033[0m  quarantined variant invisible  [200, never named]\n'; PASS=$((PASS+1))
  printf '  served from: %s\n' "$(printf '%s' "$BODY" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("filename"))' 2>/dev/null)"
else
  printf '  \033[31mFAIL\033[0m  quarantine  got %s  %.190s\n' "$CODE" "$BODY"; FAIL=$((FAIL+1))
fi
mv "$QUAR/ch_04_canonical_p09.json" "$PLANS/"

say "RESULT"
printf '  %d passed, %d failed\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ] && echo "  C13 exit met: readable details, correct codes, no traceback in any body."
ls "$SCRATCH" >/dev/null 2>&1 && echo "  WARNING: scratch file still present — remove $SCRATCH"
exit $(( FAIL > 0 ))
