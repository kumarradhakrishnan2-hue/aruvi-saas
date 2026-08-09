#!/usr/bin/env python3
"""S4 · C1 + C2 + provenance, rewritten for the RE-AUTHORED ch 4 library (2026-08-09).

The previous C1/C2 asserted a [14,11,8] library that is now archived under
backup/superseded_libraries/. Leaving them would have the tracker certifying files that are
not on disk.

Run from the repo root:
    python3 genon/out/stage_prep_mathematics_secondary/update_tracker_s4_c1_c2_reauthor.py
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "mathematics/secondary"

STAGES = {
    "top_canonical": {"wall_s": "405.3", "tokens_in": "24469", "tokens_out": "26485",
                      "cost_inr": "43.30"},
    "variant_a":     {"wall_s": "370.0", "tokens_in": "24526", "tokens_out": "24660",
                      "cost_inr": "40.80"},   # p12
    "variant_b":     {"wall_s": "269.0", "tokens_in": "24526", "tokens_out": "17659",
                      "cost_inr": "31.14"},   # p09
    "variant_c":     {"wall_s": "", "tokens_in": "", "tokens_out": "", "cost_inr": ""},
    "variant_d":     {"wall_s": "", "tokens_in": "", "tokens_out": "", "cost_inr": ""},
    # SUPERSEDED, not a rerun in the defect sense: the [14,11,8] library was correct and
    # certified. It was replaced because its INPUTS changed (corrected summary, LP v1.2,
    # ch 3's re-weighting). Recorded here so the all-in figure is honest and the clean-path
    # figure — which the corpus extrapolation multiplies — is not inflated by it.
    "reruns":        {"wall_s": "977.6", "tokens_in": "66609", "tokens_out": "63870",
                      "cost_inr": "106.52"},
}
CLEAN = round(43.30 + 40.80 + 31.14, 2)     # 115.24

PROV = {
    "klass": "ix",
    "draw": "seed 'mathematics|secondary|2026-08-02' over ['ix'] -> ix (single-candidate stage)",
    "chapter": "4 — Exploring Algebraic Identities",
    "duration": "50",
    "model": "claude-sonnet-4-6",
    "date": "2026-08-09 (re-author; first build 2026-08-08, superseded)",
    "lp_ver": "1.2",
    "as_ver": "1.1",
    "engine": "12",
    "canonical_plan": ("counts [15, 12, 9] · provisional false · basis authored_standard · "
                       "registry_sections 8 · authored [15, 12, 9]. Was [14, 11, 8] until "
                       "ch 3's regeneration re-weighted the combo (effort_index 15 -> 13) and "
                       "moved ch 4 from 14 to 15 recommended periods."),
    "brief": ("variant_plans.top_brief_for + briefs_for, with the synthesis handoff-row line "
              "(2026-08-08). Second outing, correct again: sec#9 ref='synthesis', "
              "period_numbers [15], total_sections still 8."),
    "ledger_ts": ("top 20260809_094843 · p12 20260809_101448 · p09 20260809_102058 "
                  "(cert 20260809_102646 FAILED on 1 register hit in p12; repaired at Rs 0 by "
                  "repair_register.py v1.5; ALL PASS at 20260809_102753)"),
    "report": "genon/out/library_reports/mathematics_ix_ch04_20260809_102753.md",
    "files": "(none yet — C6 not run; no served plan written)",
    "durations_run": "(C6 not run; authored at 50, kumar3's profile carries 60 for the mixed matrix)",
    "stages": STAGES,
    "total_cost_inr": CLEAN,
    "partition_wall_s": "",
    "c5_split": "k1: identities / k2: between+floor−1+top+1 / k3: mixed week",
    "by": "Claude",
    "at": NOW,
}

C1 = """PASS — RE-AUTHORED 2026-08-09 at [15, 12, 9]. Three canonicals on disk matching canonical_plan.counts; row finalized provisional false, basis authored_standard, registry_sections 8.
  ch_04_canonical.json      15 units x 50 min
  ch_04_canonical_p12.json  12 units x 50 min
  ch_04_canonical_p09.json   9 units x 50 min

WHY RE-AUTHORED (the 2026-08-08 [14,11,8] library was correct and certified — it is superseded, not defective). Three of its inputs changed and none could be repaired into files already written:
  1. THE SUMMARY. Its nine end-of-chapter items were all attributed to section 4.1, because the authoring prompt required every enumerated item to name a real section and end-of-chapter questions belong to none. Units 10-12 therefore wore the '4.1' label and rendered to the teacher as 'Introduction (Revisit)'.
  2. LP v1.2's Rule 12 (period_numbers = teaching units only). p11's sec#1 listed [1,10,11] against an LO those units do not deliver.
  3. THE PERIOD COUNT. ch 3's regeneration re-weighted the combo and moved ch 4 from 14 to 15 periods.

WHAT THE RE-AUTHOR ACTUALLY CHANGED — the structural result is the headline:
  BEFORE (14u): 4.1 4.2 4.3 4.4 4.5 4.6 4.7 4.7 4.8 [4.1 4.1 4.1] 4.6 synthesis
  AFTER  (15u): 4.1 4.2 4.3 4.3 4.4 4.4 4.5 4.6 4.6 4.7 4.7 4.7 4.8 4.8 synthesis
The three consolidation units falsely anchored to 4.1 are GONE — correcting the summary removed the REASON for them, and the model spent the extra period deepening 4.3/4.4/4.7/4.8 instead of inventing consolidation blocks. The plan is monotonic; there is no revisit tail. Teacher screen carries ZERO '(Revisit)' labels (was three). Every handoff row lists exactly the units that anchor its section, so Rule 12 had no work to do here.

REGISTER: forward references fell 5 -> 2 in the standard canonical, on a plan one unit LONGER — the first evidence that the summary fix reduces register pressure rather than relabelling it. p09 scanned clean; p12 carried one. All three repaired at Rs 0 (repair_register.py v1.5). A fourth scanner hit was a FALSE POSITIVE and was fixed at source instead: U3's 'the square root of the last term' is a polynomial term, so register_scan.py now treats 'last term' as advisory rather than a calendar ban (verified next week / next month / next class still ban).

THE COMPACTS NOW CARRY HONEST MULTI-SECTION ANCHORS, which is the corrected summary showing through: p12 U12 = '4.6/4.7/4.8' and p09 U9 = '4.4/4.6/4.7/4.8', joined with ' / ' per V2. Both are correctly flagged ADVISORY by the new handoff/anchor check (a consolidation unit legitimately wears labels the handoff does not route items through) and neither gates.

EXIT criteria met: files match counts; row finalized; canonical_minutes = 50 x 15 = 750.
Report: genon/out/library_reports/mathematics_ix_ch04_20260809_102753.md — deterministic checks ALL PASS."""

C2 = """PASS — recosted 2026-08-09 for the re-authored library. Two figures, per the founder's 2026-08-07 rule.

  CLEAN PATH (what the files on disk cost — the figure this column shows, and the one a 330-chapter extrapolation may multiply):
    top  (15u)  405.3s  in 24469  out 26485  Rs  43.30
    p12  (12u)  370.0s  in 24526  out 24660  Rs  40.80
    p09  ( 9u)  269.0s  in 24526  out 17659  Rs  31.14
    ---------------------------------------------------
    3 runs                                    Rs 115.24     (Rs 38.41/run)

  SUPERSEDED (the 2026-08-08 [14,11,8] library, archived under backup/superseded_libraries/):
    Rs 106.52 across 3 runs.  ALL-IN EVER FOR CH 4: Rs 221.76.

  The superseded spend is booked in the `reruns` row so the tracker's Rs column excludes it. It is NOT a defect rerun — that library certified ALL PASS. It is the cost of changing the chapter's INPUTS after authoring, which is a different thing and worth counting separately: it is what the ordering rule (constitutions before authoring) exists to prevent, and it now has a price tag. Nothing in the campaign yet extends that rule to SUMMARIES or to MAPPINGS, which is how this happened.

  RATE MOVED, and the cause is structural not random. Rs 38.41/run here vs Rs 35.51/run on the 14/11/8 build and Rs 38.82 on SS IX ch 3. INPUT ROSE from 22165-22222 to 24469-24526 tokens (+10%) and stays there: the corrected summary carries source_sections and fuller descriptions, so every future maths run pays that. Output still falls with period count (26485 -> 24660 -> 17659), so the 9-unit compact costs 72% of the 15-unit standard despite being 60% of its length. BUDGET PER RUN, NEVER PER UNIT.

  CORPUS NOTE: maths·secondary's fixed per-run input is ~45% above SS IX ch 3's 15.3-15.6k — this chapter carries 18 worked examples and 21 exercises plus a longer assessment constitution (VS-1..VS-6, graph_paper). If that holds across maths, the pre-warm should be priced per subject rather than at one blended Rs 37/run. Worth confirming at S7/S8.

  DATA-QUALITY FINDING, not blocking: genon/ledger.csv rows for this chapter carry 18 fields against a 17-field header — an undeclared column holding the variant count sits between `model` and `subject`. Social Sciences rows have 17. csv.DictReader therefore mis-keys every maths row (subject reads '12', grade reads 'mathematics'). Figures above were taken positionally and cross-checked against runtime_data/token_log.csv, which agrees exactly (Rs 115.24). The header needs a column or the writer needs fixing before anyone parses the ledger by name."""

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_reauthor"))
row = state["combos"][KEY]
row["C1"] = {"status": "pass", "by": "Kumar", "at": NOW, "comment": C1}
row["C2"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C2}
row["provenance"] = PROV
state["updated_at"] = NOW
STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{KEY}: C1={row['C1']['status']} C2={row['C2']['status']} PROV=Rs {CLEAN} "
      f"(superseded Rs 106.52 booked under reruns)")
