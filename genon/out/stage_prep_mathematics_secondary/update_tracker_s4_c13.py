#!/usr/bin/env python3
"""S4 · C13 — failure paths (2026-08-10). PASS, 6/6."""
import datetime, json, pathlib, shutil
ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()

C13 = """PASS — 2026-08-10, 6 of 6, run by the founder against the live API via
docs/testing_artefacts/c13_run.sh (one command, self-cleaning; runbook
docs/testing_artefacts/c13_runbook_mathematics_ix_ch04.md).

1 NO LIBRARY -> 404 "No underlying chapter yet." on maths/ix/ch 16. The script also fails the
  check if the body contains the word "canonical" anywhere — it did not. That is the whole point
  of the 2026-08-04 founder wording: engine vocabulary in a teacher-facing string is a defect
  even when the sentence is true.
2 IMPLAUSIBLE MATRIX -> 400 x3. Single row over the ceiling (50x61), the SUM path
  (40x31 + 60x30 = 61 across two rows), and an empty rows[] -> "At least one duration row is
  required." The sum path is worth having: a per-row check would have passed it.
3 UNRESOLVABLE ITEM ANCHOR -> 500, naming the item, verbatim:
  "Canonical cannot be compiled: canonical plan is not v1.1-declared (1 problem): assessment
   item #4 NUM / C-3.1: no resolvable anchor unit (period_ref/phase_ref) — it names [99]"
  Not a bare 500, and the script's traceback guard (grep for 'Traceback' or 'File \"') fired on
  no body in the whole run.
4 QUARANTINED VARIANT INVISIBLE -> 200, and p09 named nowhere in the response.

CHECK 4 PROVED TWO C10 RULES LIVE, which is more than it was asked to do. With p09 condemned,
the 8-period request fell to the 12-unit canonical AND WROTE A DIFFERENT FILENAME:
ch_04_50m8_e18_c20260809101448.json, keyed on p12's version token rather than p09's. So the
chosen-variant naming rule (C10.1) and the no-overwrite property (C10.3) both hold under
quarantine, not just under an engine bump — the substitute serve cannot collide with the
condemned one's cache entry. Side effect worth knowing: that file is a real artefact of the
test and will be served again only if p09 is condemned again. Harmless, and correct.

HYGIENE VERIFIED AFTER THE RUN: scratch chapter 99 gone, p09 restored to the library,
backup/quarantine empty (0 json files). The script's trap cleans up even on Ctrl-C or a failing
check, which is why it was written as one command rather than four curls.

RECORDED, NOT FILED — two adjacent gaps found while preparing this, both needing a
hand-corrupted canonical that certification's compile check would catch at build time. The
handler catches GenonDeclarationError and ServeError only, so a period missing section_anchor
(KeyError: "period 3 has no section_anchor, and Mathematics·Grade IX anchors units to sections")
and a malformed time band (ValueError: "not enough values to unpack (expected 2, got 1)") both
escape as an unhandled 500. C13's exit still holds — FastAPI's default body is
{"detail":"Internal Server Error"} with the traceback going to the log — but the second message
names nothing useful. One more except clause would fold both into the readable shape."""

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_c13"))
c = state["combos"]["mathematics/secondary"]
c["C13"] = {"status": "pass", "by": "Kumar+Claude", "at": NOW, "comment": C13,
            "artefact": "docs/testing_artefacts/c13_runbook_mathematics_ix_ch04.md"}
state["updated_at"] = NOW
STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
print("C13 = pass (6/6)")
print("S4:", {k: v.get("status") for k, v in c.items() if isinstance(v, dict) and k.startswith("C")})
