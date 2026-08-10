#!/usr/bin/env bash
# Set up / tear down the two failure cases you can actually SEE on the phone.
#
#   bash docs/testing_artefacts/mobile_error_demo.sh on     # arm the demo
#   bash docs/testing_artefacts/mobile_error_demo.sh off    # put everything back
#
# The API must be running. After "on", pull-to-refresh (or reopen) the app so the
# chapter list reloads.

set -uo pipefail
PLANS="data/content/saved_plans/mathematics/ix"
SCRATCH="$PLANS/ch_99_canonical.json"
QUAR="backup/quarantine/mathematics/ix"

case "${1:-}" in
on)
  # ── CASE A · a chapter whose canonical is broken → the 500 path ──────────────
  # Chapter 99 will APPEAR in her chapter list (it has a library), so she can pick
  # it — unlike an unauthored chapter, which the picker never offers.
  cp "$PLANS/ch_04_canonical.json" "$SCRATCH"
  python3 - "$SCRATCH" <<'PY'
import json,pathlib,sys
p=pathlib.Path(sys.argv[1]); d=json.loads(p.read_text())
d['chapter_number']=99; d['chapter_title']='Demo · Broken Chapter'
def items(o):
    if isinstance(o,dict):
        if isinstance(o.get('questions'),list): yield from o['questions']
        for v in o.values(): yield from items(v)
    elif isinstance(o,list):
        for v in o: yield from items(v)
it=list(items(d['result']))[3]; it['period_ref']=[99]; it['section_number']=99
p.write_text(json.dumps(d,indent=1,ensure_ascii=False))
PY
  echo "ARMED."
  echo
  echo "  A · THE BROKEN CHAPTER (500)"
  echo "     Chapter 99 'Demo · Broken Chapter' now exists for Mathematics · Class IX."
  echo "     On the phone: Prepare Lesson → Mathematics → Class 9 → chapter 99 → prepare."
  echo "     EXPECT: the generic line, not the item-naming message the API returns."
  echo
  echo "  B · TOO MANY PERIODS (400)"
  echo "     No setup needed. Allocate → Modify Allocation → set chapter 4 to 61 periods"
  echo "     → Save → prepare it."
  echo "     EXPECT: the same generic line, though the API says 'Period count implausibly large.'"
  echo
  echo "  C · CONDEMNED VARIANT (no error at all — the control)"
  echo "     bash docs/testing_artefacts/mobile_error_demo.sh quarantine"
  echo "     Then ask for 8 periods on chapter 4. EXPECT: a normal plan, served from the 12."
  echo
  echo "  Not reachable from the app: the 404. The chapter picker only offers chapters that"
  echo "  have a library, so she can never ask for one we have not authored."
  echo
  echo "  When done:  bash docs/testing_artefacts/mobile_error_demo.sh off"
  ;;
quarantine)
  mkdir -p "$QUAR"
  mv "$PLANS/ch_04_canonical_p09.json" "$QUAR/" 2>/dev/null \
    && echo "p09 condemned. Ask for 8 periods on chapter 4 — expect a normal plan from the 12." \
    || echo "p09 already condemned (or missing)."
  ;;
off)
  rm -f "$SCRATCH" && echo "scratch chapter 99 removed."
  if [ -f "$QUAR/ch_04_canonical_p09.json" ]; then
    mv "$QUAR/ch_04_canonical_p09.json" "$PLANS/" && echo "p09 restored."
  fi
  echo "Refresh the app; chapter 99 should be gone from the list."
  ;;
*)
  echo "usage: bash docs/testing_artefacts/mobile_error_demo.sh {on|quarantine|off}"; exit 1;;
esac
