#!/usr/bin/env python3
"""Write S7 (mathematics · middle) W2 + the stage's spend into the campaign tracker.

Run from the repo root:
    python3 genon/out/stage_prep_mathematics_middle/update_tracker_s7_w2.py
Restart the API afterwards, or just reload docs/testing_tracker.html.
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "mathematics/middle"

W2 = """S7 · classes vi/vii/viii · 2026-08-19. <b>73 compacts</b> (msgbatch_0188xEyeHkH3nB3svDRNYFny; vii ch 7's p10/p07 correctly skipped as installed), <b>₹1,057.00 at ₹14.48/run</b> against a ₹990 estimate. 71 installed on the first pass. <b>Library complete on all 39 chapters — 114 canonicals on disk against 114 in the master plan — and the closing certify returns ALL PASS on every one, zero FAIL lines.</b>

<b>REGISTER: 18 hits over 16 of 112 files — 0.16/file, against wave 1's 0.54 and S2·middle's 2.3. THE COMPACTS ARE BETTER BEHAVED THAN THE STANDARDS THEY WERE CUT FROM</b>, which reverses both S2·middle (wave 2 = wave 1) and the prediction: a compact asserts "having covered every section" on a plan carrying fewer of them, so COMPLETION was expected to rise. It did not — 2 hits, the same as wave 1. Distribution: 14 forward · 2 clock · 2 completion · zero calendar, zero meta-leak. Clock returns after wave 1 swept it to zero and both hits are ONE defect authored twice (vi ch 5's p15 U14 and p20 U17, same Special Numbers box, same brainstorm minute). 17 declared repairs applied by assertion, <b>15 pure deletions and 2 substitutions</b> (vii ch 12 p10, where the early-finisher guidance is the point of the sentence and survives; vii ch 6 p05, where deleting the clause would have left a dangling em dash, so the pair is closed instead). Library re-scans at <b>0 ban hits</b>.

<b>ONE HIT WAS A SCANNER FALSE POSITIVE AND WAS FIXED AT THE SCANNER, NOT IN THE TEXT</b> (runbook trap 4). viii ch 3 p04 U2 opens "Bridge to the Egyptian system FROM SECTION 3.3.I" — and U2 anchors 3.3.I itself; "from section X" is provenance, the opposite of a pointer at what follows. The ban pattern's 60-char gap ran through "Egyptian system from " and reached the word "section". `register_scan.py`'s gap may no longer swallow "from" — the same narrowing as the 2026-08-18 Law-of-Large-Numbers ruling. Verified both ways: ARV-D-038's own phrase stays banned, the LLN case stays advisory.

<b>TWO COMPACTS WERE QUARANTINED, each for ONE item, both repaired rather than re-bought</b> (~₹27 saved, but the point is that neither defect was structural). ARV-D-179 — vi ch 9 p14 Q-C-5 declared `number_line:` on a four-step process strip; the FIELD goes, not just the tag, because Rule 7 forbids a tick line from being the grid the item needs and the strip restated the item's own method_one_line, turning an `apply` item into an instruction to follow. ARV-D-180 — viii ch 12 p13 Q-C-10 was a declared MCQ that asked nothing; the question was AUTHORED (founder ruling) on the counterexample to its anchor exercise's statement (ii). <b>Two drafts of that question were rolled back from backup/c3_repair/ rather than patched</b>: the first named option letters in the guide prose, which STEP 6's arrangement invalidated on install; the second keyed the reveals against the arranged order instead of the declared one, so the remap carried a mismatch through. Standing rule from it: a label is the platform's to assign — guide text names the PAIR, never the letter beside it. Certification sees neither error.

<b>CLOSING CHECKLIST (runbook §5), seven lines:</b> (1) 114 canonicals expected, 114 on disk ✓ (2) quarantine holds 2 files, both with live counterparts, both defects closed ✓ (3) zero register ban hits stage-wide ✓ (4) all 39 chapters ALL PASS including C5 check 11; not a prose subject, so no advisory shortlist to rule on ✓ (5) every chapter serves across its band — certification's own sweep runs X = floor−2 … top+2 on all 39 ✓ (6) <b>TWO DERIVED PLANS REMAIN ON DISK</b> for viii ch 12 (one derived from the p13 that was repaired), and the sandbox cannot delete under saved_plans/ — <b>owed to Kumar's machine, and it is ARV-D-034's exact shape: a repair does not move canonical_version, so the cache would serve pre-repair bytes</b> (7) spend reconciled from token_log.csv, see SPEND.

<b>ALSO LANDED IN THIS WAVE, and it is the stage's real finding — ARV-D-181.</b> Assessment anchored by SECTION on a stage whose sections are banners: 199 of 540 sittings carried a question (37%) at 2.8 apiece, and a three-quarter-length serve kept only 57% of its items. Founder's diagnosis: this stage indexes on COMPLEXITY, marked by the anchor exercise, and LP Rule 3 already assigns one anchor per period. Implemented as a single `anchor_resolver` called by BOTH the display and the serve paths (english's S11 lesson — two joins are one drift from disagreeing): an item anchors where its handoff anchor is FIRST worked, with the section rule as backstop for the 25 capstones (anchor worked only in the closer) and the 12 with no companion. <b>Result: 454 of 540 sittings (84%), 1.2 items each, retention at three-quarter length 57% → 77%; vi ch 5 goes from 4 sittings to one question per sitting across U1–U20.</b> Verified contained: swept the whole corpus with the resolver on and off — <b>8,376 items across nine other subject·stages, not one moved.</b> test_genon_carriers 132 → 134, green.

<b>OWED:</b> F1 (C8 across the batch) and F2 (C14), each with its sample size and stratification written into the step comment BEFORE the reading starts."""

SPEND = {
    "cost_inr": 2080.94,
    "comment": """S7 all-in <b>₹2,080.94 · 124 metered runs</b>, pilot and re-runs included, from <code>runtime_data/token_log.csv</code>.

<b>Split:</b> pilot (2026-08-10, vii ch 7's C-cycle, the top authored TWICE across the LP v3.6 re-author) 8 runs ₹239.88 → <b>₹29.98/run synchronous</b> · W1 standards 38 runs ₹704.15 → <b>₹18.53/run</b> · W1 re-authors (the four synthesis-only-section chapters) 5 runs ₹79.91 · W2 compacts 73 runs ₹1,057.00 → <b>₹14.48/run</b>.

<b>The batch-vs-sync spread is the number worth carrying:</b> ₹29.98 synchronous against ₹18.53 (standards) and ₹14.48 (compacts) — compacts are cheaper because they are shorter, mean 9.9 periods against the standards' 13.9, and output tokens track period count. A corpus projection built on the pilot's ₹29.98 would overstate by ~70%.

<b>TWO ARTEFACTS WERE RECOVERED FREE RATHER THAN RE-BOUGHT</b> (~₹33 that does not appear here because it was never spent twice): viii ch 2 and vi ch 10 both streamed to completion and failed to parse on the naked-inner-quote hazard. MAX_REPAIR_SPAN 300 → 400 rescued the first (it refused a 319-char pair by nineteen characters); a new `_structural_escape` last resort — a quote closes a string only if the next non-space character is one of <code>: , } ]</code>, exhaustive for well-formed JSON — rescued the second, which the pair heuristic could not see. <b>Standing finding: LP v3.9 removed that hazard by mandating curly quotes but wrote itself relaxation-only ("the straight-quoted form remains valid and is not a defect"), so the hazard is still live and took 2 of 42 runs.</b>""",
}

RULING_ADDENDUM = """<br><br><b>ADDENDUM 2026-08-19 (founder) — why the 25 exist, which is a better explanation than the one above.</b> They are the SECOND item the handoff carries for a section: some sections get two entries, one at a shallower goal and one at `apply`, and the second is by construction the deeper of the pair. Its anchor is therefore the culminating exercise, which the closing unit is the only sitting to work. So the section's end is the natural place for them and the section rule was right about these all along — not a concession to avoid an untested borrow path, though that reason stands too."""

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_s7_w2"))

row = state.setdefault("batch", {}).setdefault(KEY, {})
row["W2"] = {"status": "pass", "by": "Kumar (ran) · Claude (triaged, repaired, recorded)",
             "at": NOW, "comment": W2, "files": 75}
row["spend"] = {"status": None, "by": "Claude (reconciled from runtime_data/token_log.csv)",
                "at": NOW, **SPEND}

for d in state.get("defects", []):
    if d.get("id") == "ARV-D-181-RULING" and "ADDENDUM" not in (d.get("evidence") or ""):
        d["evidence"] = (d.get("evidence") or "") + RULING_ADDENDUM
    if d.get("id") == "ARV-D-181":
        d["status"] = "fixed-awaiting-recheck"
        d["notes"] = ("IMPLEMENTED 2026-08-19: aruvi_core/subjects/mathematics/anchor_resolver.py, "
                      "called from subject.py::_middle_assess (display) and "
                      "subject.py::_anchor_then_section (serve). Awaiting the live app read.")

state["updated_at"] = NOW
STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
b = state["batch"][KEY]
print(f"{KEY}: " + " · ".join(f"{k}={v.get('status')}" for k, v in b.items() if isinstance(v, dict)))
print(f"  W1 files {b['W1'].get('files')} · W2 files {b['W2'].get('files')} · ₹{b['spend']['cost_inr']}")
