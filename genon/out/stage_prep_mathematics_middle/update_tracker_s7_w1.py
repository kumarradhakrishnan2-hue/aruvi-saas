#!/usr/bin/env python3
"""Write S7 (mathematics · middle) W1 into the campaign tracker's BATCH RELEASE tab.

Run from the repo root:
    python3 genon/out/stage_prep_mathematics_middle/update_tracker_s7_w1.py
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

W1 = """S7 · classes vi/vii/viii · 2026-08-19. <b>39 chapters, 39 standards on disk, all 39 master-plan rows annotated</b> (provisional false, basis authored_standard). 43 logged runs — 38 in the wave (msgbatch_01Tp7skXwTKtgUqH698wRXDo) plus 4 re-authors — <b>₹784.07 at ₹18.23/run</b>, against a ₹664 estimate for the wave alone. Certify at 12:59 returns 39 reports whose ONLY failure is `library complete`, which is arithmetic between the waves. <b>Register: 0 ban hits library-wide.</b>

<b>DEFECT FAMILY 1 — the synthesis unit as sole teacher of a section (4 chapters, ₹70).</b> vi ch 3 (3.12), vi ch 10 (10.5), vii ch 3 (3.8), viii ch 3 (3.4.IV) each taught the chapter's LAST section only in the closing unit and then wrote an item on it. `carriers.items_by_period_field` indexes non-synthesis units only (the S7 fix that stopped items collapsing onto the closer), so the item anchored nowhere, compile raised, and the row stayed provisional. NOT the maths·secondary case, though the authoring error is identical: at secondary the LABEL (section_anchor) and the ROUTING (coverage_handoff.period_numbers) are different fields, which is what let the 2026-08-18 V2/registry-carry repair widen one and leave the other; at middle they are ONE field (textbook_segments[].ref serves both), so widening the label drags the item onto a unit that does not teach the section — simulated on vi ch 3 and confirmed. Founder ruling 2026-08-19: <b>harden the brief and re-author</b>, not an engine fallback. `variant_plans.top_brief_for` gains THE SYNTHESIS UNIT INTRODUCES NOTHING — the old line ("all registry sections first-appear across units 1..N−1") is circular from the model's seat, since the registry is derived from what the body units name. The new clause names the trap (the chapter's last section), states the cost (no shorter plan can teach it; an item on it resolves to no unit) and says what to do instead (teach a slight final section in unit N−1). <b>All four came back correct on the first try.</b>

<b>DEFECT FAMILY 2 — the JSON quote hazard, twice, both recovered FREE.</b> viii ch 2 and vi ch 10 streamed to completion and did not parse. Neither was re-bought. (a) viii ch 2: 41 inner-quote pairs, 40 repaired, the 41st refused at <b>319 characters against MAX_REPAIR_SPAN 300</b> — nineteen characters cost a whole chapter. Constant raised to 400, with the measurements in the comment; recover_from_raw installed it clean (register 0 hits). (b) vi ch 10 (the re-author): a legal narration in a shape the pair heuristic cannot see — `p.251 (both sets: "…" and "…")`, two quoted phrases in one parenthetical — so the pairing walked past it, thrashed 417 "repairs" and corrupted a correct file. New <b>`_structural_escape` last resort</b> in generate_canonical.py: a quote closes a string only if the next non-space char is one of `: , } ]` (exhaustive for well-formed JSON — a string is a key, an array element or an object value, nothing else). Escaped 125 inner quotes, parsed first try, 16 periods, validate ok. It runs ONLY after the certified path fails and ONLY on the original text, so every file that installs today installs byte-identically (verified on viii ch 2, which never touches it); its one false positive breaks structure, so the parse fails and nothing installs. <b>Standing finding: LP v3.9 removed this hazard by mandating curly quotes but wrote itself relaxation-only ("the straight-quoted form remains valid and is not a defect"), so the hazard is still live and took 2 of 42 runs.</b>

<b>DEFECT FAMILY 3 — register, 21 hits over 15 of 41 files (0.54/file).</b> Well under S2·middle's 2.3 and roughly TWAU's rate. DISTRIBUTION: <b>16 forward · 4 completion · 1 meta-leak · ZERO clock, zero calendar</b> — the clean sweep on clock quantities is the notable number, since that family dominated every earlier stage (58 of 134 at S2·middle) and is the first thing maths·middle's LP v3.4 register block names. Forward reference is now the whole problem, and its shape is consistent: a trailing sentence or appositive at the END of a unit's last band or note. All 21 declared in repair_register.py and applied by assertion — <b>19 pure deletions, 2 substitutions</b> (vii ch 7 p10 U4 and viii ch 11 U15, both because deleting the clause would have taken real teaching with it). Derived plans purged; re-scan clean at 0.

<b>TWO OPEN DEFECTS CLOSE WITH THIS PASS.</b> vii ch 7 is the C-cycle pilot, certified 2026-08-10 as "register clean (0 ban hits)" because the scanner had no [completion] pattern then. Its U11 hit IS <b>ARV-D-100</b> (found by eye at C5 — the reason that defect exists) and its p10 U4 hit is one of the five in <b>ARV-D-125</b>'s corpus sweep. Both repaired here. That is the recheck those defects were waiting for, not a new finding.

<b>ALSO LANDED, free, no behaviour change:</b> `variant_plans.standard_registry` no longer discards the compile exception. A standard that is on disk and does not compile used to report "Row is provisional — author and certify the standard canonical", which reads as "the file is missing" and sent this session's triage hunting four files that were there all along. It now prints the cause. Runbook trap 5's lesson one level lower.

<b>OWED TO W2:</b> the compacts, whose briefs read the registries this wave annotated; then the closing checklist. Tests green at close: test_lp_standard, test_genon_carriers, test_view_model, test_calibrated_defaults."""


state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_s7_w1"))

row = state.setdefault("batch", {}).setdefault(KEY, {})
row["W1"] = {"status": "pass", "by": "Kumar (ran) · Claude (triaged + recorded)",
             "at": NOW, "comment": W1, "files": 39}
row.setdefault("spend", None)
state["updated_at"] = NOW

STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{KEY}: wrote W1 = {row['W1']['status']}  (backup: {STATE.name}.bak_pre_s7_w1)")
