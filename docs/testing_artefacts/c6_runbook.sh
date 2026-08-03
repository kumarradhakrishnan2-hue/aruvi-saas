#!/usr/bin/env bash
# C6 — API serve checks · social_sciences · ix · ch 3
# REWRITTEN 2026-08-03 for the v2.0 library and engine e12. The previous version was
# written against {12, 9, 7} at e10 and its expectations (superset / exact / suffix modes,
# a p09 variant) no longer exist. Do not run the old one.
#
# Library {12, 10, 7} · floor 7 · top 12 · AUTHORED AT 50 MIN · engine e12
#
#   bash docs/testing_artefacts/c6_runbook.sh
#
# Preconditions, both hard:
#   1. P5.4 done — kumar1, kumar2, kumar3 each have a Social Sciences IX teaching profile.
#      Step 0 below prints each one; if any reads ready False, STOP and fix that first.
#   2. The API is up in another terminal:
#         python3 -m uvicorn api.main:app --port 8000
#
# Every response is saved under docs/testing_artefacts/c6_responses/. Those files are the
# C6 artefact and the input for C7, C9, C10, C11 and C12 — keep them.
#
# What the identity split is FOR: kumar1 runs identities, kumar2 the fills and the edges,
# kumar3 the mixed-duration week. Three tenants writing into the same chapter is what makes
# C10 (isolation) and X1 (tenancy) meaningful later.

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
                          else fill.get("mode")),
      "| fill_class:", fill.get("fill_class"), "| borrowed_from:", fill.get("borrowed_from"))
print("   uncovered  :", fill.get("uncovered_sections"))
print("   surrendered:", s.get("surrendered_periods"))
print("   coverage   :", (d.get("coverage_note") or "(none)")[:240])
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

# ── 1 · identity · kumar1 · X = each canonical's own count, at the authored 50 min ──
say "1 · identity (kumar1) — expect identity:true, the canonical's OWN filename, NO new file"
serve identity_50m12 kumar1 '[{"duration":50,"count":12}]'
serve identity_50m10 kumar1 '[{"duration":50,"count":10}]'
serve identity_50m7  kumar1 '[{"duration":50,"count":7}]'
ls "$LIB" > "$OUT/_lib_after_identity.txt"
if diff -q "$OUT/_lib_before.txt" "$OUT/_lib_after_identity.txt" >/dev/null; then
  echo "   PASS  no new file written by the three identity requests"
else
  fail "identity wrote a file:"; diff "$OUT/_lib_before.txt" "$OUT/_lib_after_identity.txt"
fi

# ── 2 · between-variant fills · kumar2 · at 50 min ─────────────────────────────
# The certified sweep (report 20260803_194610) predicts these exactly. A mode that
# disagrees with the sweep is the finding — the sweep runs the same engine offline,
# so a divergence means the API path differs from the certification path.
say "2 · between-variant fills (kumar2) — sweep predicts: X=8 fill/single, X=11 fill/single"
serve fill_50m8  kumar2 '[{"duration":50,"count":8}]'
serve fill_50m11 kumar2 '[{"duration":50,"count":11}]'
echo "   expect for both: mode fill · a fill_class · uncovered_sections EMPTY"
echo "   a backward fill_class must name the re-crossed sections as runway in coverage_note"

# ── 3 · early-coverage synthesis borrow · kumar2 ───────────────────────────────
say "3 · X=9 (kumar2) — sweep predicts SYNTHESIS: the prefix completes coverage early"
serve synthesis_50m9 kumar2 '[{"duration":50,"count":9}]'
echo "   ASSERT: mode synthesis · borrowed_from = 12 (the STANDARD's count — the borrowed"
echo "   unit must be the standard's own synthesis unit, not a compact's closer) ·"
echo "   coverage_note says the closing sitting draws the chapter together"

# ── 4 · above the top · kumar2 ────────────────────────────────────────────────
say "4 · X = top + 1 = 13 (kumar2) — expect surrender"
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
    print("   -> e10: the SERVED schedule must print 12, not the 13 asked for;")
    print("      the ask survives only in genon.matrix / period_rows_snapshot")
    print("   -> e09: the surrender sentence belongs in coverage_note, with")
    print("      serve.surrender_note kept as provenance")
PY

# ── 5 · below the floor · kumar2 ──────────────────────────────────────────────
say "5 · X = floor - 1 = 6 (kumar2) — honest partial: fill + uncovered_sections"
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
    if not du: print("   CHECK FAILED: e09 expects the unreached units here, verbatim")
    print("   -> e12: the dropped units must come from the LENDING plan's subsequent units,")
    print("      not the chosen plan's. Compare their titles against the lender named by")
    print("      slot_fill.borrowed_from in belowfloor_50m6.json.")
PY

# ── 6 · mixed-duration weekly matrix · kumar3 ─────────────────────────────────
say "6 · mixed-duration matrix (kumar3) — 3x60 + 7x50 = 10 sittings"
echo "   Totals 10 but at MIXED durations, so identity cannot fire and a file is written."
echo "   This is the plan C7/C8/C9/C12 inspect."
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
        longest=max(seq)
        print("   shortest opens the week :", seq[0]==min(seq))
        print("   long sittings interior  :", all(0<i<len(seq)-1 for i,v in enumerate(seq) if v==longest))
        print("   no two long adjacent    :", not [i for i in range(len(seq)-1) if seq[i]==seq[i+1]==longest])
    units=(s.get("result") or {}).get("lesson_plan",{}).get("periods") or []
    print("   sittings:", len(units), "| per-unit minutes:",
          [u.get("period_duration_minutes") for u in units])
PY

# ── 7 · same X, NON-authored duration — identity must NOT fire ────────────────
say "7 · X=10 at 45 min (kumar3) — the ordinary teacher case, NOT identity"
echo "   expect identity absent/false, a file written, proportional scaling, exact tiling"
serve scaled_45m10 kumar3 '[{"duration":45,"count":10}]'
python3 - "$OUT/scaled_45m10.json" "$LIB" <<'PY'
import json,sys,pathlib
d=json.load(open(sys.argv[1])); fn=d.get("filename")
p=pathlib.Path(sys.argv[2])/fn if fn else None
if p and p.is_file():
    s=json.load(open(p)); bad=[]
    for u in (s.get("result") or {}).get("lesson_plan",{}).get("periods") or []:
        dur=u.get("period_duration_minutes"); prev=0; ok=True
        for b in u.get("time_bands") or []:
            a,_,z=str(b.get("minutes","")).replace("–","-").partition("-")
            try: a,z=int(a.strip()),int(z.strip())
            except ValueError: ok=False; break
            if a!=prev or z<=a: ok=False; break
            prev=z
        if not ok or prev!=dur: bad.append(u.get("period_number"))
        print("      unit",u.get("period_number"),"dur",dur,"| tiles to",prev)
    print("   exact tiling on every unit:", not bad, bad or "")
PY

say "done — responses in $OUT"
cat <<'NOTE'
Then tell Claude, and it records C6 in the tracker. What it needs from this run:
  · every row's mode / fill_class / borrowed_from / filename / coverage note
  · confirmation that the three identity requests wrote NO file
  · the surrender row's served-vs-asked schedule
  · the below-floor row's dropped_units and which plan they came from
  · the mixed row's duration_sequence
  · whether any served mode disagreed with the certified sweep
    {5: fill/single -2s, 6: fill/single -1s, 7: identity, 8: fill/single, 9: synthesis,
     10: identity, 11: fill/single, 12: identity, 13-14: surrender}
NOTE
