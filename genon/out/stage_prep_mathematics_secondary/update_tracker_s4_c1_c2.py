#!/usr/bin/env python3
"""S4 · C1 green + C2 cost/provenance for mathematics/secondary.

Writes combos["mathematics/secondary"] C1, C2 and the provenance block that the matrix's
last column (PROV) renders as the ₹ figure.

The ₹ shown is the CLEAN-PATH total — the runs that produced the files now on disk, reruns
excluded (founder ruling 2026-08-07, and what the tracker's own commitProv() computes). This
library had ZERO reruns, so clean-path and all-in are the same number: 106.52.

Run from the repo root:
    python3 genon/out/stage_prep_mathematics_secondary/update_tracker_s4_c1_c2.py
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "mathematics/secondary"

# From genon/ledger.csv (wall seconds; token_log.csv has no duration column) and
# runtime_data/token_log.csv (tokens, ₹). Three runs, no reruns, no superseded generations.
STAGES = {
    "top_canonical": {"wall_s": "392.5", "tokens_in": "22165", "tokens_out": "25230",
                      "cost_inr": "40.93"},
    "variant_a":     {"wall_s": "317.7", "tokens_in": "22222", "tokens_out": "21387",
                      "cost_inr": "35.65"},   # p11
    "variant_b":     {"wall_s": "267.4", "tokens_in": "22222", "tokens_out": "17253",
                      "cost_inr": "29.94"},   # p08
    "variant_c":     {"wall_s": "", "tokens_in": "", "tokens_out": "", "cost_inr": ""},
    "variant_d":     {"wall_s": "", "tokens_in": "", "tokens_out": "", "cost_inr": ""},
    "reruns":        {"wall_s": "0", "tokens_in": "0", "tokens_out": "0", "cost_inr": "0"},
}
CLEAN_TOTAL = round(40.93 + 35.65 + 29.94, 2)          # 106.52

PROVENANCE = {
    "klass": "ix",
    "draw": "seed 'mathematics|secondary|2026-08-02' over ['ix'] -> ix (single-candidate stage)",
    "chapter": "4 — Exploring Algebraic Identities",
    "duration": "50",
    "model": "claude-sonnet-4-6",
    "date": "2026-08-08",
    "lp_ver": "1.1",
    "as_ver": "1.1",
    "engine": "12",
    "canonical_plan": ("counts [14, 11, 8] · provisional false · basis authored_standard · "
                       "registry_sections 8 · authored [14, 11, 8] (v2.0 equal dispersion "
                       "over [floor 8, standard 14]; A-C = 6 >= 4 so three counts)"),
    "brief": ("variant_plans.top_brief_for + briefs_for. FIRST library authored against the "
              "SYNTHESIS HANDOFF-ROW line (added 2026-08-08, emitted only where "
              "carriers.item_anchor_is_derived) — it worked on first use: sec#9 "
              "ref='synthesis' period_numbers [14], total_sections correctly still 8, and one "
              "item anchored to unit 14. Also the first library on the mathematics genon "
              "carrier (8-rule row 6)."),
    "ledger_ts": ("top 20260808_173726 · p11 20260808_174359 · p08 20260808_174917 "
                  "(first cert report 20260808_175345 FAILED on 6 register hits; repaired "
                  "at Rs 0 by repair_register.py v1.4; ALL PASS at 20260808_204619; "
                  "re-certified 20260808_210228 with the new handoff/anchor check)"),
    "report": "genon/out/library_reports/mathematics_ix_ch04_20260808_210228.md",
    "files": "(none yet — C6 not run; no served plan written)",
    "durations_run": "(C6 not run yet; authored at 50, kumar3's profile carries 60 for the mixed matrix)",
    "stages": STAGES,
    "total_cost_inr": CLEAN_TOTAL,
    "partition_wall_s": "",
    "c5_split": "k1: identities / k2: between+floor−1+top+1 / k3: mixed week",
    "by": "Claude",
    "at": NOW,
}

C1 = """PASS — library built 2026-08-08 (Kumar, Terminal, metered). Three canonicals on disk matching canonical_plan.counts [14, 11, 8]:
  ch_04_canonical.json      14 units x 50 min
  ch_04_canonical_p11.json  11 units x 50 min
  ch_04_canonical_p08.json   8 units x 50 min
The master_plan row finalized as expected: provisional false, basis authored_standard, authored [14, 11, 8], registry_sections 8.

TWO FIRSTS, both held:
  1. The first library authored on the MATHEMATICS GENON CARRIER (8-rule row 6, landed at P5.5 the same day). Items resolve section_number -> coverage_handoff -> period_numbers, anchored at the section's LAST unit.
  2. The first library authored against the SYNTHESIS HANDOFF-ROW brief line. It worked on first use — the top emitted sec#9 ref='synthesis' with period_numbers [14], kept total_sections at 8 as instructed, and anchored one item to unit 14. That is C9.2 ('a borrowed unit brings its own items') satisfiable on a derived-anchor stage for the first time.

CERTIFICATION HISTORY — the first pass FAILED, and the failure was free to fix:
  20260808_175345  FAIL — register clean: 6 ban hit(s), ALL forward reference (5 in the top, 1 in p11; p08 clean). Zero clock quantities across 132 bands, which is a distribution no earlier stage produced (SS VIII was 3 forward / 4 clock; science IX 1 / 2).
  repair_register.py v1.4 --apply — six declared pure DELETIONS, no text authored, Rs 0. Backups in backup/register_repair/, edits recorded in genon_canonical.repairs[], derived plan cache purged (ARV-D-034).
  20260808_204619  ALL PASS.
  20260808_210228  ALL PASS again, now including the new handoff/anchor check added at C1 (see C5).

NOTE ON THE BREACHES, carried to the human gate rather than acted on: every hit was a pedagogical SIGNPOST, not the boilerplate the ban's examples name ('the companion identity to be derived in the factorisation unit', 'the following unit will formalise'). The register was in the constitution at authoring (LP v1.1) AND in the brief, so this is not a not-told case. One hit — U13's 'Preview that the synthesis unit will connect all such proof moves' — is the model paraphrasing its own brief, which describes unit 14 to it in detail and then forbids naming it. Founder view 2026-08-08: the brief is not the lever; repair is the route (2026-08-02 ruling: regenerating is a lottery).

EXIT criteria met: files match counts; the row is finalized; canonical_minutes = 50 x 14 = 700."""

C2 = """PASS — costed 2026-08-08 from genon/ledger.csv (wall seconds) + runtime_data/token_log.csv (tokens, rupees). Every row attributed; nothing missing.

  top_canonical (14u)  392.5s  in 22165  out 25230  Rs 40.93
  variant_a     (11u)  317.7s  in 22222  out 21387  Rs 35.65
  variant_b     ( 8u)  267.4s  in 22222  out 17253  Rs 29.94
  reruns                    —         0       0     Rs  0.00
  ------------------------------------------------------------
  CLEAN PATH                                        Rs 106.52
  ALL-IN                                            Rs 106.52

THE TWO FIGURES ARE THE SAME HERE — zero reruns and zero superseded generations, so the chapter cost exactly what is on disk. The tracker's Rs column shows the clean-path total (founder 2026-08-07), which is also what a 330-chapter extrapolation may multiply. The six register breaches cost Rs 0 to fix: repair_register.py is deterministic, so a defect that would have been a Rs 106 re-author was a free edit.

AGAINST THE BENCHMARK: SS IX ch 3 (v2.0 re-author) was Rs 116.46 across 3 runs = Rs 38.82/run. This library is Rs 106.52 across 3 runs = Rs 35.51/run, about 9% cheaper per run.

COST SHAPE, and it confirms the standing warning: INPUT IS FLAT — 22165 / 22222 / 22222 tokens, i.e. the constitution, summary, mapping and brief are paid in full on every run regardless of length. OUTPUT falls with period count (25230 -> 21387 -> 17253). So the 8-period compact costs 73% of the 14-period standard despite being 57% of its length. BUDGET PER RUN, NEVER PER UNIT.

Note the input is ~45% higher than SS IX ch 3's 15.3-15.6k. Mathematics secondary carries 18 enumerated worked examples and 21 exercises in its summary plus a longer assessment constitution (VS-1..VS-6 + graph_paper), so its fixed per-run input is structurally larger. If that holds across maths chapters, the corpus projection should use a per-subject rate rather than one blended Rs 37/run — worth confirming at S7/S8 before the pre-warm is priced."""

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_s4_c1c2"))

row = state.setdefault("combos", {}).setdefault(KEY, {})
row["C1"] = {"status": "pass", "by": "Kumar", "at": NOW, "comment": C1}
row["C2"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C2}
row["provenance"] = PROVENANCE
state["updated_at"] = NOW

STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{KEY}: C1={row['C1']['status']}  C2={row['C2']['status']}  "
      f"PROV=Rs {PROVENANCE['total_cost_inr']}")
