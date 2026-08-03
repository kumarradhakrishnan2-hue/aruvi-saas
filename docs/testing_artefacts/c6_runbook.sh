#!/usr/bin/env bash
# C6 — API serve checks · social_sciences · ix · ch 3
# Library {12, 9, 7} · floor 7 · authored duration 50 min · engine e10
#
#   bash docs/testing_artefacts/c6_runbook.sh
#
# Precondition: P5.4 done (the three identities have Social Sciences IX profiles),
# and the API is up:  python3 -m uvicorn api.main:app --port 8000
#
# Every response is saved under docs/testing_artefacts/c6_responses/ — those files
# are the artefact for C6 and the input for C7, C9, C10, C11 and C12.

set -u
API=http://localhost:8000
OUT="$(cd "$(dirname "$0")" && pwd)/c6_responses"
LIB="$(cd "$(dirname "$0")/../.." && pwd)/data/content/saved_plans/social_sciences/ix"
mkdir -p "$OUT"

say()  { printf '\n\033[1m== %s\033[0m\n' "$*"; }
fail() { printf '   \033[31mCHECK FAILED: %s\033[0m\n' "$*"; }

# serve <label> <user> <json-rows>
serve() {
  local label=$1 user=$2 rows=$3
  local f="$OUT/$label.json"
  local t
  t=$(curl -s -o "$f" -w '%{time_total}' -X POST \
        "$API/genon/social_sciences/ix/3/plan" \
        -H 'Content-Type: application/json' -H "X-Aruvi-User: $user" \
        -d "{\"rows\": $rows}")
  printf '%s  [%s]  %ss\n' "$label" "$user" "$t"
  python3 - "$f" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
if "detail" in d:
    print("   HTTP error body:", d["detail"]); raise SystemExit
s=d.get("serve") or {}
fill=s.get("slot_fill") or {}
print("   identity   :", d.get("identity"), "| cached:", d.get("cached"))
print("   filename   :", d.get("filename"))
print("   periods    :", d.get("periods"), "| variant_used:", s.get("variant_used"))
print("   mode       :", ("identity" if d.get("identity")
                          else "surrender" if s.get("surrendered_periods")
                          else fill.get("mode")))
print("   surrendered:", s.get("surrendered_periods"))
print("   coverage   :", (d.get("coverage_note") or "(none)")[:220])
if s.get("surrender_note"): print("   surrender_note:", s["surrender_note"][:200])
PY
}

# ── 0 · preconditions ─────────────────────────────────────────────────────────
say "0 · preconditions"
curl -s -o /dev/null -w '   API /genon chapters: HTTP %{http_code}\n' \
     "$API/genon/social_sciences/ix/chapters"
for u in kumar1 kumar2 kumar3; do
  printf '   %s readiness: ' "$u"
  curl -s "$API/readiness" -H "X-Aruvi-User: $u" \
   | python3 -c "import json,sys;d=json.load(sys.stdin);print('ready',d.get('ready'),'| subjects',[(s.get('name'),[g.get('grade') for g in s.get('grades',[])]) for s in d.get('subjects',[])])"
done
echo "   -> all three MUST read ready True with social_sciences / ix. If not, stop: P5.4 first."
ls "$LIB" > "$OUT/_lib_before.txt"; echo "   library snapshot -> _lib_before.txt"

# ── 1 · identity · kumar1 · X = each variant's own count, at 50 min ────────────
say "1 · identity (kumar1) — expect identity:true, the variant's OWN filename, no new file"
serve identity_50m12 kumar1 '[{"duration":50,"count":12}]'
serve identity_50m9  kumar1 '[{"duration":50,"count":9}]'
serve identity_50m7  kumar1 '[{"duration":50,"count":7}]'
ls "$LIB" > "$OUT/_lib_after_identity.txt"
if diff -q "$OUT/_lib_before.txt" "$OUT/_lib_after_identity.txt" >/dev/null; then
  echo "   PASS  no new file written by the three identity requests"
else
  fail "identity wrote a file:"; diff "$OUT/_lib_before.txt" "$OUT/_lib_after_identity.txt"
fi

# ── 2 · between-variant fills · kumar2 · at 50 min ─────────────────────────────
say "2 · between-variant fills (kumar2)"
echo "   X=8  expect mode superset (runway) + a coverage note naming the re-crossed sections"
serve fill_50m8  kumar2 '[{"duration":50,"count":8}]'
echo "   X=10 expect mode exact, no coverage note needed"
serve fill_50m10 kumar2 '[{"duration":50,"count":10}]'
echo "   X=11 expect mode synthesis (recorded; not required by the C6 table)"
serve fill_50m11 kumar2 '[{"duration":50,"count":11}]'

# ── 3 · above the top · kumar2 ────────────────────────────────────────────────
say "3 · X = top + 1 = 13 (kumar2) — expect surrender"
echo "   surrendered_periods >= 1; the surrender sentence in coverage_note (e09);"
echo "   and the SERVED schedule must print 12, not the 13 asked for (e10)"
serve surrender_50m13 kumar2 '[{"duration":50,"count":13}]'
python3 - "$OUT/surrender_50m13.json" "$LIB" <<'PY'
import json,sys,pathlib
d=json.load(open(sys.argv[1])); fn=d.get("filename")
p=pathlib.Path(sys.argv[2])/fn if fn else None
if p and p.is_file():
    s=json.load(open(p)); g=s.get("genon") or {}
    print("   period_schedule_display :", s.get("period_schedule_display"))
    print("   genon.served_matrix     :", g.get("served_matrix"))
    print("   genon.matrix (the ask)  :", g.get("matrix"))
    print("   period_rows_snapshot    :", s.get("period_rows_snapshot"))
PY

# ── 4 · below the floor · kumar2 ──────────────────────────────────────────────
say "4 · X = floor - 1 = 6 (kumar2) — expect suffix or truncation + dropped_units"
serve belowfloor_50m6 kumar2 '[{"duration":50,"count":6}]'
python3 - "$OUT/belowfloor_50m6.json" "$LIB" <<'PY'
import json,sys,pathlib
d=json.load(open(sys.argv[1])); fn=d.get("filename")
p=pathlib.Path(sys.argv[2])/fn if fn else None
if p and p.is_file():
    s=json.load(open(p)); du=(s.get("result") or {}).get("dropped_units") or []
    print("   dropped_units:", len(du))
    for u in du:
        print("      unit", u.get("period_number"), "| unscheduled:", u.get("unscheduled"),
              "|", str(u.get("activity_title"))[:70])
    if not du: print("   CHECK: e09 expects the unreached units here, verbatim")
PY

# ── 5 · mixed-duration weekly matrix · kumar3 ─────────────────────────────────
say "5 · mixed-duration matrix (kumar3) — 3x60 + 7x50 = 10 periods"
echo "   Deliberately totals 10 so it lands on a FILL mode: C12 needs a plan that"
echo "   contains a BORROWED closing sitting. Identity cannot fire off 50 min."
serve mixed_60m3_50m7 kumar3 '[{"duration":60,"count":3},{"duration":50,"count":7}]'
python3 - "$OUT/mixed_60m3_50m7.json" "$LIB" <<'PY'
import json,sys,pathlib
d=json.load(open(sys.argv[1])); fn=d.get("filename")
p=pathlib.Path(sys.argv[2])/fn if fn else None
if p and p.is_file():
    s=json.load(open(p)); g=s.get("genon") or {}
    seq=g.get("duration_sequence") or []
    print("   duration_sequence:", seq)
    if seq:
        ok_open = seq[0]==min(seq)
        adj=[i for i in range(len(seq)-1) if seq[i]==seq[i+1]==max(seq)]
        interior=all(0<i<len(seq)-1 for i,v in enumerate(seq) if v==max(seq))
        print("   shortest opens the week :", ok_open)
        print("   long sittings interior  :", interior)
        print("   no two long adjacent    :", not adj)
    units=(s.get("result") or {}).get("lesson_plan",{}).get("periods") or []
    print("   sittings:", len(units), "| per-unit minutes:",
          [u.get("period_duration_minutes") for u in units])
PY

# ── 6 · same X, NON-authored duration — identity must NOT fire ────────────────
say "6 · X=9 at 45 min (kumar3) — the ordinary teacher case, NOT identity"
echo "   expect identity absent/false, a file written, proportional scaling, exact tiling"
serve scaled_45m9 kumar3 '[{"duration":45,"count":9}]'
python3 - "$OUT/scaled_45m9.json" "$LIB" <<'PY'
import json,sys,pathlib
d=json.load(open(sys.argv[1])); fn=d.get("filename")
p=pathlib.Path(sys.argv[2])/fn if fn else None
if p and p.is_file():
    s=json.load(open(p))
    for u in (s.get("result") or {}).get("lesson_plan",{}).get("periods") or []:
        tb=u.get("time_bands") or []
        ends=[]
        for b in tb:
            m=str(b.get("minutes","")).replace("–","-").split("-")
            ends.append(m[-1].strip())
        print("      unit",u.get("period_number"),"dur",u.get("period_duration_minutes"),
              "| bands end at", ends[-1] if ends else "?")
PY

say "done — responses in $OUT"
echo "Record in the tracker: every row's mode, filename, coverage note, and the"
echo "duration the library was authored at (50 min). Then C7 reads these same files."
