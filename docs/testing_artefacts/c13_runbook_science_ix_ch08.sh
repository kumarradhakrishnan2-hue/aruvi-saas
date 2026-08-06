#!/usr/bin/env bash
# C13 — Failure paths · science · secondary (IX) · ch 8
# Library {12, 10, 7} · floor 7 · engine e16
#
#   bash docs/testing_artefacts/c13_runbook_science_ix_ch08.sh
#
# Every check asks the same question: does a broken request come back as something a TEACHER
# can read, with no stack trace in the body?
#
# HOW CASE 3 IS ISOLATED, and why it matters. The step says "copy the canonical to a scratch
# chapter number … remove the scratch file afterwards". The Cowork sandbox cannot unlink on the
# mounted repo (C10.2b), so a scratch file written into data/content/ would be PERMANENT — and
# worse than clutter: `genon_chapters()` lists any ch_NN_canonical.json it finds, so a broken
# scratch chapter would advertise itself as certified content forever. Instead the whole check
# runs against a THROWAWAY CONTENT ROOT under /tmp (symlinks to the real content, with a private
# saved_plans/ holding copies), served by a second API on :8001 via ARUVI_DATA_DIR. Nothing is
# written into the repo, and the scratch tree is deleted at the end — where deletion works.
set -u
API=http://localhost:8000
SCRATCH_API=http://localhost:8001
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="$ROOT/docs/testing_artefacts/c13_responses"
TMP=/tmp/c13_content
mkdir -p "$OUT"

say() { printf '\n\033[1m== %s\033[0m\n' "$*"; }
cleanup() {
  [ -n "${APIPID:-}"  ] && kill "$APIPID"  2>/dev/null
  [ -n "${API2PID:-}" ] && kill "$API2PID" 2>/dev/null
  rm -rf "$TMP" && echo "   scratch content root removed: $TMP"
  return 0
}
trap cleanup EXIT

# probe <label> <expected-code> <curl args...>
probe() {
  local label=$1 want=$2; shift 2
  local code
  code=$(curl -s -o "$OUT/$label.json" -w '%{http_code}' "$@")
  python3 - "$OUT/$label.json" "$label" "$code" "$want" <<'PY'
import json, re, sys
path, label, code, want = sys.argv[1:5]
raw = open(path, encoding="utf8", errors="replace").read()
try:
    body = json.loads(raw); detail = body.get("detail", body)
except Exception:
    detail = raw[:200]
TB = re.compile(r"Traceback \(most recent|File \"/|, line \d+, in |\.py\", line")
tb = bool(TB.search(raw))
ok = "OK " if code == want else "!! "
print(f"   {ok}{label:26s} HTTP {code} (want {want})  traceback in body: {tb}")
print(f"      detail: {str(detail)[:190]}")
PY
}

if [ "${NO_START:-0}" != "1" ]; then
  ( cd "$ROOT" && python3 -m uvicorn api.main:app --port 8000 > /tmp/c13_api.log 2>&1 ) &
  APIPID=$!
  for _ in $(seq 1 30); do curl -s -o /dev/null "$API/genon/science/ix/chapters" && break; sleep 1; done
fi

say "0 · what the real library actually holds"
curl -s "$API/genon/science/ix/chapters" | sed 's/^/   chapters with a library: /'

say "1 · no canonical — a chapter with no library"
probe no_canonical_ch3  404 -X POST "$API/genon/science/ix/3/plan" \
  -H 'Content-Type: application/json' -H 'X-Aruvi-User: kumar1' -d '{"rows":[{"duration":50,"count":10}]}'
probe no_canonical_ch99 404 -X POST "$API/genon/science/ix/99/plan" \
  -H 'Content-Type: application/json' -H 'X-Aruvi-User: kumar1' -d '{"rows":[{"duration":50,"count":10}]}'

say "2 · implausible matrix, and the empty one"
probe too_many_periods  400 -X POST "$API/genon/science/ix/8/plan" \
  -H 'Content-Type: application/json' -H 'X-Aruvi-User: kumar1' -d '{"rows":[{"duration":50,"count":61}]}'
probe too_many_split    400 -X POST "$API/genon/science/ix/8/plan" \
  -H 'Content-Type: application/json' -H 'X-Aruvi-User: kumar1' \
  -d '{"rows":[{"duration":50,"count":40},{"duration":60,"count":40}]}'
probe empty_rows        400 -X POST "$API/genon/science/ix/8/plan" \
  -H 'Content-Type: application/json' -H 'X-Aruvi-User: kumar1' -d '{"rows":[]}'
probe zero_count_rows   400 -X POST "$API/genon/science/ix/8/plan" \
  -H 'Content-Type: application/json' -H 'X-Aruvi-User: kumar1' -d '{"rows":[{"duration":50,"count":0}]}'

say "2b · neighbouring bad input (not in the step; cheap, and the same promise)"
probe unknown_subject   404 -X POST "$API/genon/astrology/ix/8/plan" \
  -H 'Content-Type: application/json' -H 'X-Aruvi-User: kumar1' -d '{"rows":[{"duration":50,"count":10}]}'
probe path_traversal    400 "$API/plans/science/ix/..%2F..%2Fetc%2Fpasswd/view"
probe missing_plan      404 "$API/plans/science/ix/ch_08_50m99_e16_cdeadbeef.json/view"

say "3 · unresolvable item anchor — on a scratch chapter in a THROWAWAY content root"
python3 - "$TMP" "$ROOT" <<'PY'
import json, os, pathlib, shutil, sys
tmp, root = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir(parents=True)
content = root / "data" / "content"
for d in content.iterdir():                       # symlink the real content, cheap and read-only
    if d.name != "saved_plans":
        (tmp / d.name).symlink_to(d)
sp = tmp / "saved_plans" / "science" / "ix"; sp.mkdir(parents=True)
src = json.load(open(content / "saved_plans" / "science" / "ix" / "ch_08_canonical.json"))

# Science·secondary is the HANDOFF-BRIDGED family: carriers.py resolves an item's unit through
# the coverage_handoff row matching its section LABEL, not through a period_ref. So the way to
# make an item unresolvable is to name a section the chapter does not teach.
scratch = json.loads(json.dumps(src))
scratch["chapter_number"] = 90
q = scratch["result"]["assessment_items"]["questions"][0]
q["section_number"] = 99
q["section_label"] = "8.99 A Section This Chapter Does Not Teach"
q.pop("unit_ref", None); q.pop("period_ref", None)
json.dump(scratch, open(sp / "ch_90_canonical.json", "w"), ensure_ascii=False, indent=1)

# and a clean copy at another number, to prove the scratch root itself is not the problem
ctrl = json.loads(json.dumps(src)); ctrl["chapter_number"] = 91
json.dump(ctrl, open(sp / "ch_91_canonical.json", "w"), ensure_ascii=False, indent=1)
print(f"   scratch root built: {tmp}  (ch 90 broken, ch 91 control)")
PY

( cd "$ROOT" && ARUVI_DATA_DIR="$TMP" python3 -m uvicorn api.main:app --port 8001 > /tmp/c13_api2.log 2>&1 ) &
API2PID=$!
for _ in $(seq 1 30); do curl -s -o /dev/null "$SCRATCH_API/genon/science/ix/chapters" && break; sleep 1; done
curl -s "$SCRATCH_API/genon/science/ix/chapters" | sed 's/^/   scratch root chapters: /'
probe broken_anchor_ch90 500 -X POST "$SCRATCH_API/genon/science/ix/90/plan" \
  -H 'Content-Type: application/json' -H 'X-Aruvi-User: kumar1' -d '{"rows":[{"duration":50,"count":11}]}'
probe control_ch91       200 -X POST "$SCRATCH_API/genon/science/ix/91/plan" \
  -H 'Content-Type: application/json' -H 'X-Aruvi-User: kumar1' -d '{"rows":[{"duration":50,"count":11}]}'

say "4 · quarantined variant absent from serving — the C10.5 transcript re-read"
python3 - "$ROOT/docs/testing_artefacts/c10_responses" <<'PY'
import json, pathlib, sys
o = pathlib.Path(sys.argv[1])
for lbl in ("quarantine_withheld_50m9", "quarantine_withheld_50m8", "quarantine_withheld_50m10"):
    p = o / f"{lbl}.json"
    if not p.exists(): print(f"   {lbl}: (missing — re-run C10)"); continue
    raw = p.read_text(); d = json.loads(raw)
    s = d.get("serve") or {}
    print(f"   {lbl:26s} status={d.get('status')} library={s.get('library')} "
          f"chosen={s.get('variant_used')} | 'detail' in body: {'detail' in d} | "
          f"names p10: {'p10' in raw}")
PY

say "5 · traceback sweep across every body this run produced"
python3 - "$OUT" <<'PY'
import pathlib, re, sys
TB = re.compile(r"Traceback \(most recent|File \"/|, line \d+, in |\.py\", line|Error\(")
bad = []
for p in sorted(pathlib.Path(sys.argv[1]).glob("*.json")):
    t = p.read_text(encoding="utf8", errors="replace")
    if TB.search(t): bad.append(p.name)
print("   bodies scanned:", len(list(pathlib.Path(sys.argv[1]).glob('*.json'))))
print("   bodies containing anything traceback-shaped:", bad or "NONE")
PY

say "done"
