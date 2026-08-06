#!/usr/bin/env bash
# C10 — Storage conventions · science · secondary (IX) · ch 8
# Library {12, 10, 7} · floor 7 · authored at 50 min · engine e16
#
#   bash docs/testing_artefacts/c10_runbook_science_ix_ch08.sh
#
# Starts its own API on :8000 (the Cowork sandbox does not keep a server alive between
# shell calls, so every step needing HTTP has to live inside ONE process group) and stops
# it again. With uvicorn already up, run with NO_START=1 to reuse yours.
#
# Checks (docs/testing.md §4 C10):
#   1 filenames · 2 cache hit + purge · 3 no overwrite across engines
#   4 determinism · 5 quarantine invisible to serving
#
# ORDER MATTERS. Check 3's evidence is the e15 files sitting beside the e16 ones — and
# check 2b's purge deletes EVERY derived plan for the chapter, e15 included (correctly:
# a repaired canonical invalidates them all). So 3 is recorded BEFORE the purge, the whole
# derived set is copied to /tmp first, and the e15 half is restored afterwards from that
# copy — this run simulates a repair, it does not perform one, so the older-engine evidence
# is not the purge's to take. Stated in the artefact; do not quietly drop it.
#
# SAFETY: check 5 MOVES a library canonical into backup/quarantine and restores it on an
# EXIT trap — never deleted. The library canonicals are never rewritten by any step.
set -u
API=http://localhost:8000
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="$ROOT/docs/testing_artefacts/c10_responses"
LIB="$ROOT/data/content/saved_plans/science/ix"
QUAR="$ROOT/backup/quarantine/science_ix_ch08"
BAK=/tmp/c10_derived_backup
mkdir -p "$OUT" "$QUAR" "$BAK"

say() { printf '\n\033[1m== %s\033[0m\n' "$*"; }

cleanup() {
  for f in "$QUAR"/*.json; do
    [ -e "$f" ] || continue
    mv "$f" "$LIB/" && echo "   TRAP RESTORED $(basename "$f")"
  done
  [ -n "${APIPID:-}" ] && kill "$APIPID" 2>/dev/null
  return 0
}
trap cleanup EXIT

if [ "${NO_START:-0}" != "1" ]; then
  ( cd "$ROOT" && python3 -m uvicorn api.main:app --port 8000 > /tmp/c10_api.log 2>&1 ) &
  APIPID=$!
  for _ in $(seq 1 30); do
    curl -s -o /dev/null "$API/genon/science/ix/chapters" && break
    sleep 1
  done
fi

# serve <label> <user> <rows-json>
serve() {
  local label=$1 user=$2 rows=$3
  curl -s -o "$OUT/$label.json" -w "   HTTP %{http_code} %{time_total}s  " -X POST \
    "$API/genon/science/ix/8/plan" \
    -H 'Content-Type: application/json' -H "X-Aruvi-User: $user" \
    -d "{\"rows\": $rows}"
  python3 - "$OUT/$label.json" "$label" "$user" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
if "detail" in d:
    print("ERROR:", d["detail"]); raise SystemExit
g = d.get("genon") or {}; f = g.get("slot_fill") or {}
print(f"{sys.argv[2]} [{sys.argv[3]}] cached={d.get('cached')} identity={d.get('identity')} "
      f"chosen={g.get('variant_used')} library={g.get('library')} mode={f.get('mode')} "
      f"borrowed_from={f.get('borrowed_from')} file={d.get('filename')}")
PY
}

say "0 · preconditions and snapshot"
curl -s -o /dev/null -w '   /genon/science/ix/chapters: HTTP %{http_code}\n' "$API/genon/science/ix/chapters"
( cd "$LIB" && ls > "$OUT/_lib_before.txt" && md5sum ./*.json > "$OUT/_lib_before.md5" )
cp "$LIB"/ch_08_*_e*_c*.json "$BAK"/ 2>/dev/null
echo "   snapshot -> _lib_before.txt / _lib_before.md5 ; derived set copied to $BAK"

say "3 · no overwrite across engine versions (recorded BEFORE the purge)"
( cd "$LIB" && ls ch_08_*_e15_*.json | wc -l | xargs echo "   e15 files on disk:" )
( cd "$LIB" && ls ch_08_*_e16_*.json | wc -l | xargs echo "   e16 files on disk:" )
( cd "$LIB" && ls -l --time-style=+%F_%T ch_08_*_e15_*.json | awk '{printf "     %s  %s\n", $6, $7}' )

say "2a · cache hit — same matrix, the owner then a second teacher"
F="$LIB/ch_08_50m11_e16_c20260806100029.json"
echo "   BEFORE mtime=$(stat -c %y "$F") md5=$(md5sum "$F" | cut -d' ' -f1)"
serve cache_50m11_kumar2 kumar2 '[{"duration":50,"count":11}]'
echo "   AFTER  mtime=$(stat -c %y "$F") md5=$(md5sum "$F" | cut -d' ' -f1)"
serve cache_50m11_kumar1 kumar1 '[{"duration":50,"count":11}]'
echo "   AFTER  mtime=$(stat -c %y "$F") md5=$(md5sum "$F" | cut -d' ' -f1)"

say "4 · determinism — delete one plan, re-serve, diff without saved_at"
cp "$LIB/ch_08_50m9_e16_c20260806100653.json" /tmp/c10_50m9_before.json
rm "$LIB/ch_08_50m9_e16_c20260806100653.json"
serve determinism_50m9 kumar2 '[{"duration":50,"count":9}]'
python3 - "$LIB/ch_08_50m9_e16_c20260806100653.json" <<'PY'
import json, sys
a = json.load(open("/tmp/c10_50m9_before.json")); b = json.load(open(sys.argv[1]))
sa, sb = a.pop("saved_at", None), b.pop("saved_at", None)
print("   saved_at before/after:", sa, "/", sb)
print("   diff (saved_at removed):", "EMPTY — identical" if a == b else "DIFFERS")
for k in sorted(set(a) | set(b)):
    if a.get(k) != b.get(k): print("     differs at:", k)
PY

say "2b · purge — a repair invalidates every derived plan for the chapter"
( cd "$LIB" && ls ch_08_*_e*_c*.json | wc -l | xargs echo "   derived plans before purge:" )
( cd "$ROOT" && python3 - <<'PY'
import importlib.util, pathlib
spec = importlib.util.spec_from_file_location("pd", pathlib.Path("genon/purge_derived.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
removed = m.purge("science", "ix", 8, reason="C10.2b — simulated repair of science IX ch 8")
print("   purge returned:", len(removed), "file(s)")
PY
)
echo "   derived plans after purge: $(cd "$LIB" && ls ch_08_*_e*_c*.json 2>/dev/null | wc -l)"
( cd "$LIB" && ls ch_08_canonical*.json | tr '\n' ' ' | xargs echo "   library canonicals still present:" )

say "2b · rebuild — the next request rebuilds from the canonical"
serve rebuild_50m11 kumar2 '[{"duration":50,"count":11}]'
serve rebuild_50m9  kumar2 '[{"duration":50,"count":9}]'
serve rebuild_50m8  kumar2 '[{"duration":50,"count":8}]'
serve rebuild_50m6  kumar2 '[{"duration":50,"count":6}]'
serve rebuild_mixed kumar3 '[{"duration":60,"count":4},{"duration":50,"count":7}]'
python3 - "$LIB" "$BAK" <<'PY'
import json, pathlib, sys
lib, bak = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
same = diff = 0
for p in sorted(bak.glob("ch_08_*_e16_*.json")):
    q = lib / p.name
    if not q.exists():
        print("   (not rebuilt this run:", p.name, ")"); continue
    a = json.load(open(p)); b = json.load(open(q))
    a.pop("saved_at", None); b.pop("saved_at", None)
    ok = a == b
    same += ok; diff += (not ok)
    print(f"   {p.name:44s} rebuilt == pre-purge bytes: {ok}")
print(f"   -> identical {same}, differing {diff}")
PY

say "2b · restore the e15 evidence set (this run simulated a repair, it did not do one)"
cp "$BAK"/ch_08_*_e15_*.json "$LIB"/ && echo "   e15 files restored from $BAK"
python3 - "$LIB" "$OUT" <<'PY'
import hashlib, pathlib, sys
lib, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
before = dict(l.split()[::-1] for l in open(out / "_lib_before.md5") if l.strip())
bad = 0
for name, md5 in before.items():
    n = name.lstrip("./")
    if "_e15_" not in n: continue
    got = hashlib.md5((lib / n).read_bytes()).hexdigest()
    if got != md5: print("   CHANGED:", n); bad += 1
print("   e15 fingerprints identical to the pre-run snapshot:", bad == 0)
PY

say "5 · quarantine — p10 withheld, the serve it fed must fall through"
serve quarantine_baseline_50m9 kumar1 '[{"duration":50,"count":9}]'
mv "$LIB/ch_08_canonical_p10.json" "$QUAR/" && echo "   QUARANTINED ch_08_canonical_p10.json"
serve quarantine_withheld_50m9 kumar1 '[{"duration":50,"count":9}]'
serve quarantine_withheld_50m8 kumar1 '[{"duration":50,"count":8}]'
serve quarantine_withheld_50m10 kumar1 '[{"duration":50,"count":10}]'
python3 - "$OUT" <<'PY'
import pathlib, sys
o = pathlib.Path(sys.argv[1])
for lbl in ("quarantine_withheld_50m9", "quarantine_withheld_50m8", "quarantine_withheld_50m10"):
    raw = (o / f"{lbl}.json").read_text()
    print(f"   {lbl}: 'p10' anywhere in payload: {'p10' in raw} | 'quarantine': {'quarantine' in raw}")
PY
mv "$QUAR/ch_08_canonical_p10.json" "$LIB/" && echo "   RESTORED ch_08_canonical_p10.json"
serve quarantine_restored_50m9 kumar1 '[{"duration":50,"count":9}]'

say "5 · clean-up verification"
( cd "$LIB" && md5sum ./*.json > "$OUT/_lib_after.md5" )
for f in ch_08_canonical.json ch_08_canonical_p10.json ch_08_canonical_p07.json; do
  b=$(grep -F "./$f" "$OUT/_lib_before.md5" | cut -d' ' -f1)
  a=$(grep -F "./$f" "$OUT/_lib_after.md5"  | cut -d' ' -f1)
  [ "$b" = "$a" ] && echo "   $f  SAME" || echo "   $f  CHANGED  $b -> $a"
done
echo "   quarantine dir entries (must be 0): $(ls -A "$QUAR" | wc -l)"
( cd "$LIB" && ls ch_08_*_e15_*.json | wc -l | xargs echo "   e15 files:" )
( cd "$LIB" && ls ch_08_*_e16_*.json | wc -l | xargs echo "   e16 files:" )

say "done"
