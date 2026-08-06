#!/usr/bin/env bash
# C11 — Serve wall time · science · secondary (IX) · ch 8
# Library {12, 10, 7} · floor 7 · authored at 50 min · engine e16
#
#   bash docs/testing_artefacts/c11_runbook_science_ix_ch08.sh
#
# The step: time a CACHE-MISS C6-style request with curl -w '%{time_total}'. Exit < 5 s.
#
# The sandbox cannot unlink, so the miss is produced the other way the step allows — a FRESH
# MATRIX. Every matrix below is one no file exists for, chosen to cover a different serve
# class, so the timing is not one number for one happy path. Each is then re-requested
# immediately to time the HIT beside it; the pair is the interesting figure.
#
# RESIDUE: each fresh matrix writes a served plan this run cannot delete. They are listed at
# the end and named in the artefact — valid plans, but C11 artefacts rather than stage
# evidence. 45m12 is a deliberate choice: it restores the scaled identity-shape row the C6
# record lists and the e14 purge took.
set -u
API=http://localhost:8000
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="$ROOT/docs/testing_artefacts/c11_responses"
LIB="$ROOT/data/content/saved_plans/science/ix"
mkdir -p "$OUT"

say() { printf '\n\033[1m== %s\033[0m\n' "$*"; }
cleanup() { [ -n "${APIPID:-}" ] && kill "$APIPID" 2>/dev/null; return 0; }
trap cleanup EXIT

if [ "${NO_START:-0}" != "1" ]; then
  ( cd "$ROOT" && python3 -m uvicorn api.main:app --port 8000 > /tmp/c11_api.log 2>&1 ) &
  APIPID=$!
  for _ in $(seq 1 30); do curl -s -o /dev/null "$API/genon/science/ix/chapters" && break; sleep 1; done
fi

# time_one <label> <user> <rows> <phase>
time_one() {
  local label=$1 user=$2 rows=$3 phase=$4
  local t
  t=$(curl -s -o "$OUT/${label}_${phase}.json" -w '%{time_total}' -X POST \
        "$API/genon/science/ix/8/plan" \
        -H 'Content-Type: application/json' -H "X-Aruvi-User: $user" \
        -d "{\"rows\": $rows}")
  python3 - "$OUT/${label}_${phase}.json" "$label" "$phase" "$t" <<'PY'
import json, os, sys
d = json.load(open(sys.argv[1]))
if "detail" in d:
    print(f"   {sys.argv[2]:16s} {sys.argv[3]:5s} ERROR: {d['detail']}"); raise SystemExit
s = d.get("serve") or {}; f = s.get("slot_fill") or {}
mode = ("identity" if d.get("identity") else "surrender" if s.get("surrendered_periods")
        else "full" if not f else f.get("mode"))
kb = os.path.getsize(sys.argv[1]) / 1024
print(f"   {sys.argv[2]:16s} {sys.argv[3]:5s} {float(sys.argv[4])*1000:7.1f} ms   "
      f"cached={str(d.get('cached')):5s} chosen={str(s.get('variant_used')):4s} "
      f"mode={mode:16s} resp={kb:5.1f} KB  {d.get('filename')}")
PY
}

# pair <label> <user> <rows>   — miss then hit
pair() { time_one "$1" "$2" "$3" miss; time_one "$1" "$2" "$3" hit; }

say "0 · preconditions"
curl -s -o /dev/null -w '   /genon/science/ix/chapters: HTTP %{http_code}\n' "$API/genon/science/ix/chapters"
( cd "$LIB" && ls ch_08_*.json > "$OUT/_lib_before.txt" )
echo "   files before: $(wc -l < "$OUT/_lib_before.txt")"

say "1 · cache-miss timings on FRESH matrices, one per serve class (miss, then hit)"
printf '   %-16s %-5s %9s\n' label phase total
pair identity45_45m12 kumar1 '[{"duration":45,"count":12}]'          # identity shape, scaled
pair fill_45m11       kumar2 '[{"duration":45,"count":11}]'          # single fill off the top
pair rescue_45m8      kumar2 '[{"duration":45,"count":8}]'           # Case 1b complete rescue
pair belowfloor_45m6  kumar2 '[{"duration":45,"count":6}]'           # below floor, drops
pair mixed_60m3_45m9  kumar3 '[{"duration":60,"count":3},{"duration":45,"count":9}]'
pair surrender_45m14  kumar2 '[{"duration":45,"count":14}]'          # above the top

say "2 · the identity path (no file written) for contrast"
time_one identity_50m12 kumar1 '[{"duration":50,"count":12}]' hit

say "3 · engine-only medians, 7 runs per matrix — where the time actually goes"
( cd "$ROOT" && python3 - <<'PY'
import json, os, statistics, sys, time
os.environ.setdefault("ARUVI_DATA_DIR", os.path.join(os.getcwd(), "data", "content"))
sys.path.insert(0, os.getcwd())
from api import data
from aruvi_core.genon import serve_plan

cases = [("identity45_45m12", [(45,12)]), ("fill_45m11", [(45,11)]),
         ("rescue_45m8", [(45,8)]),      ("belowfloor_45m6", [(45,6)]),
         ("mixed_60m3_45m9", [(60,3),(45,9)]), ("surrender_45m14", [(45,14)])]

t0 = time.perf_counter()
streams = data.load_genon_streams("science", "ix", 8)
load_ms = (time.perf_counter() - t0) * 1000
print(f"   load_genon_streams (3 canonicals, disk → compiled): {load_ms:.1f} ms  [once per request]")
for label, mx in cases:
    ts = []
    for _ in range(7):
        a = time.perf_counter(); plan = serve_plan(streams, mx); ts.append((time.perf_counter()-a)*1000)
    kb = len(json.dumps(plan, ensure_ascii=False)) / 1024
    print(f"   {label:16s} median {statistics.median(ts):6.2f} ms  "
          f"(min {min(ts):.2f} / max {max(ts):.2f})  payload {kb:.0f} KB")
PY
)

say "4 · residue — files this run created and cannot delete"
( cd "$LIB" && ls ch_08_*.json > "$OUT/_lib_after.txt" )
diff "$OUT/_lib_before.txt" "$OUT/_lib_after.txt" | grep '^>' | sed 's/^> /   NEW  /'
echo "   files after: $(wc -l < "$OUT/_lib_after.txt")"

say "done"
