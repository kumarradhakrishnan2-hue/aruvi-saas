#!/usr/bin/env bash
# C12 — The online view and the exports · science · secondary (IX) · ch 8
# Library {12, 10, 7} · floor 7 · authored 50 min · engine e16
#
#   bash docs/testing_artefacts/c12_runbook_science_ix_ch08.sh
#
# C12 is "[Kumar runs, Claude inspects]". This runbook covers everything that is reachable
# from the API — the view, the eight export files, and the BOOKMARK half of the writable
# marks (which round-trips to the server by design). The CHAPTER-NOTES half is localStorage
# only, so it stays Kumar's to run in a browser; the artefact says exactly what to do.
#
# The two plans under test are not interchangeable:
#   BELOW-FLOOR   ch_08_50m6_e16_c20260806101157.json   — the only one with dropped_units
#   MIXED+BORROW  ch_08_60m4-50m7_e16_c20260806100029.json — mixed durations AND a borrowed
#                 sitting (C6 row 6; NOT 60m3-45m9, whose total is a canonical count and
#                 which therefore borrows nothing — the trap C6 and C11 both recorded).
set -u
API=http://localhost:8000
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="$ROOT/docs/testing_artefacts/c12_exports"
BELOW=ch_08_50m6_e16_c20260806101157.json
MIXED=ch_08_60m4-50m7_e16_c20260806100029.json
mkdir -p "$OUT"

say() { printf '\n\033[1m== %s\033[0m\n' "$*"; }
cleanup() { [ -n "${APIPID:-}" ] && kill "$APIPID" 2>/dev/null; return 0; }
trap cleanup EXIT

if [ "${NO_START:-0}" != "1" ]; then
  ( cd "$ROOT" && python3 -m uvicorn api.main:app --port 8000 > /tmp/c12_api.log 2>&1 ) &
  APIPID=$!
  for _ in $(seq 1 30); do curl -s -o /dev/null "$API/genon/science/ix/chapters" && break; sleep 1; done
fi

say "1 · the VIEW — dropped_lp on the below-floor plan"
curl -s -o "$OUT/view_below_floor.json" -w '   GET view (%s): HTTP %{http_code}\n' "$API/plans/science/ix/$BELOW/view"
curl -s -o "$OUT/view_mixed.json"       -w '   GET view (mixed): HTTP %{http_code}\n'  "$API/plans/science/ix/$MIXED/view"

say "2 · the EIGHT exports"
for f in lesson assessment integrated; do
  for fmt in pdf docx; do
    q="format=$fmt"
    [ "$f" = "lesson" ] || q="$q&answers=1"
    curl -s -o "$OUT/mixed_${f}.${fmt}" -w "   ${f}/${fmt}: HTTP %{http_code}  %{size_download} bytes\n" \
      "$API/api/plans/science/ix/$MIXED/export/$f?$q"
  done
done

# the allocation report needs the allocate output as its body; build it from the API
python3 - "$API" "$OUT" <<'PY'
import json, sys, urllib.request
api, out = sys.argv[1], sys.argv[2]
ch = json.load(urllib.request.urlopen(f"{api}/subjects/science/ix/chapters"))
rows = ch["chapters"] if isinstance(ch, dict) else ch
body = {"subject": "science", "grade": "ix", "period_types": [{"minutes": 50, "count": 245}],
        "chapters": []}
for c in rows:
    p = c.get("recommended_periods") or 0
    body["chapters"].append({
        "chapter_number": c.get("chapter_number"), "chapter_title": c.get("chapter_title"),
        "periods_by_duration": {"50": p}, "total_periods": p, "total_minutes": p * 50,
        "weight": c.get("weight") or c.get("effort_index"),
    })
json.dump(body, open(f"{out}/_allocation_body.json", "w"), ensure_ascii=False, indent=1)
print(f"   allocation body: {len(body['chapters'])} chapters, "
      f"{sum(c['total_periods'] for c in body['chapters'])} periods")
PY
for kind in pdf docx; do
  curl -s -o "$OUT/allocation_report.$kind" -w "   allocation/$kind: HTTP %{http_code}  %{size_download} bytes\n" \
    -X POST "$API/api/allocation/export-$kind" -H 'Content-Type: application/json' \
    -d @"$OUT/_allocation_body.json"
done

say "4 · BOOKMARK — server round-trip and per-teacher isolation"
# The real key shape, read off kumar1's existing row — `{subject}_{grade}_{section}`.
# NOTE `chapter` is a STRING on SectionStateRequest and it carries the PLAN FILENAME, not the
# chapter number or title; posting an int is a 422, which is how this runbook first failed.
SEC="science_ix_9A"
CHT="$MIXED"
echo "   kumar1's row BEFORE this step:"
python3 -c "import json;print('     ',json.load(open('$ROOT/data/section_state/kumar1/kumar1/state.json')).get('$SEC'))" 2>/dev/null
post_bm() {  # post_bm <user> <unit> <phase>
  curl -s -o /dev/null -w "   POST /section-state [$1] unit=$2 phase=$3 → HTTP %{http_code}\n" \
    -X POST "$API/section-state" -H 'Content-Type: application/json' -H "X-Aruvi-User: $1" \
    -d "{\"section_key\":\"$SEC\",\"chapter\":\"$CHT\",\"unit_index\":$2,\"done\":false,\"bookmark_unit\":$2,\"bookmark_phase\":$3}"
}
show_bm() {
  curl -s "$API/section-state" -H "X-Aruvi-User: $1" -o "$OUT/section_state_$1.json"
  python3 - "$OUT/section_state_$1.json" "$1" <<'PY'
import json, sys
d = json.load(open(sys.argv[1])).get("states") or {}
print(f"   GET /section-state [{sys.argv[2]}]: {len(d)} section(s)")
for k, v in d.items():
    print(f"      {k!r:24s} unit_index={v.get('unit_index')} "
          f"bookmark_unit={v.get('bookmark_unit')} bookmark_phase={v.get('bookmark_phase')}")
PY
}
post_bm kumar1 3 2
show_bm kumar1
echo "   -- move it (must REPLACE, not accumulate) --"
post_bm kumar1 5 0
show_bm kumar1
echo "   -- kumar2 must see no trace of kumar1's section --"
show_bm kumar2
echo "   -- on-disk paths (separate per tenant/user, CLOUD_DATA_MODEL §2.4) --"
find "$ROOT/data/section_state" -name state.json 2>/dev/null | sed "s|$ROOT/||;s|^|      |"
echo "   -- a row with NO bookmark must not be rejected (the legitimate clear) --"
curl -s -o /dev/null -w "   POST without bookmark fields → HTTP %{http_code}\n" \
  -X POST "$API/section-state" -H 'Content-Type: application/json' -H "X-Aruvi-User: kumar1" \
  -d "{\"section_key\":\"$SEC\",\"chapter\":\"$CHT\",\"unit_index\":5,\"done\":false}"
show_bm kumar1

say "done"
