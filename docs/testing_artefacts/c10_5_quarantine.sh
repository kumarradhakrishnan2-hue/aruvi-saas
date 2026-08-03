#!/usr/bin/env bash
# C10.5 — a quarantined variant is INVISIBLE to serving.
#
#   bash docs/testing_artefacts/c10_5_quarantine.sh
#
# What it does: moves the 9-period variant into quarantine, re-runs a request that
# p09 had been serving (50m x 8, whose closing unit p09 supplies), checks the serve
# falls through to the next surviving variant without error and without ever naming
# the quarantined file — then RESTORES p09 and confirms serving returns to normal.
#
# Safety: p09 is an AUTHORED artefact (~Rs 37), never regenerable byte-for-byte. It is
# only ever MOVED here, never deleted, and an EXIT trap restores it even on Ctrl-C or
# an early failure. Verify the last line reads RESTORED before walking away.

set -u
API=http://localhost:8000
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
LIB="$REPO/data/content/saved_plans/social_sciences/ix"
Q="$REPO/backup/quarantine/social_sciences/ix"
P09="$LIB/ch_03_canonical_p09.json"
TS=$(date +%Y%m%d_%H%M%S)
QFILE="$Q/ch_03_canonical_p09_${TS}.json"
USER_ID=kumar2                      # already holds a 50m x 8 plan — the one under test

say() { printf '\n\033[1m== %s\033[0m\n' "$*"; }

restore() {
  if [ -f "$QFILE" ] && [ ! -f "$P09" ]; then
    mv "$QFILE" "$P09"
    printf '\n\033[32mRESTORED\033[0m  %s is back in the library\n' "$(basename "$P09")"
  elif [ -f "$P09" ]; then
    printf '\nRESTORED  %s already in place\n' "$(basename "$P09")"
  else
    printf '\n\033[31mWARNING\033[0m  p09 is in NEITHER location — look in %s\n' "$Q"
  fi
}
trap restore EXIT

ask() {   # ask <label> — POST 50m x 8 and print what came back
  local label=$1
  curl -s -X POST "$API/genon/social_sciences/ix/3/plan" \
    -H 'Content-Type: application/json' -H "X-Aruvi-User: $USER_ID" \
    -d '{"rows":[{"duration":50,"count":8}]}' \
  | python3 -c "
import json,sys
d=json.load(sys.stdin)
if 'detail' in d: print('   HTTP ERROR:', d['detail']); raise SystemExit(1)
s=d.get('serve') or {}; f=s.get('slot_fill') or {}
print('   filename    :', d.get('filename'))
print('   library seen:', s.get('library'))
print('   variant_used:', s.get('variant_used'), '| mode:', f.get('mode'),
      '| borrowed_from:', f.get('borrowed_from'))
print('   coverage    :', (d.get('coverage_note') or '(none)')[:150])
print('   RAW-NAMES-P09:', 'ch_03_canonical_p09' in json.dumps(d))
"
}

say "0 · baseline — p09 present"
[ -f "$P09" ] || { echo "STOP: $P09 not found."; exit 1; }
ask baseline
BEFORE=$(ls "$LIB" | sort)

say "1 · quarantine p09"
mkdir -p "$Q"
mv "$P09" "$QFILE"
echo "   moved -> ${QFILE#$REPO/}"
echo "   library now: $(ls "$LIB" | grep -c canonical) canonical file(s)"

say "2 · re-request 50m x 8 with p09 quarantined"
echo "   expect: 200, library [12, 7], the serve falls to the TOP, a DIFFERENT filename"
echo "   (the key carries the chosen variant's ledger_ts, so it re-keys by construction),"
echo "   and RAW-NAMES-P09 must be False — no response may name a quarantined file."
ask quarantined
NEW=$(ls "$LIB" | sort | comm -13 <(echo "$BEFORE") -)
echo "   new file(s) written while quarantined: ${NEW:-none}"

say "3 · restore p09"
restore
trap - EXIT

say "4 · re-request 50m x 8 — serving must return to the p09-keyed plan"
ask restored

say "5 · cleanup"
if [ -n "${NEW:-}" ]; then
  for n in $NEW; do
    rm -f "$LIB/$n"
    python3 - "$REPO" "$USER_ID" "$n" <<'PY'
import json,sys,os
repo,uid,name=sys.argv[1],sys.argv[2],sys.argv[3]
p=os.path.join(repo,"data","prepared_plans",uid,uid,"prepared.json")
if os.path.isfile(p):
    d=json.load(open(p)); k=f"social_sciences/ix/{name}"
    if d.pop(k,None) is not None:
        json.dump(d,open(p,"w"),indent=1)
        print(f"   register: dropped {k} from {uid}")
PY
    echo "   removed $n (produced under a library state that no longer exists)"
  done
fi
echo "   quarantine dir now: $(ls "$Q" 2>/dev/null | wc -l | tr -d ' ') file(s) — MUST be 0"
ls "$LIB" | sort | diff -q <(echo "$BEFORE") - >/dev/null \
  && echo "   library identical to baseline — PASS" \
  || { echo "   library DIFFERS from baseline:"; ls "$LIB" | sort | diff <(echo "$BEFORE") -; }
