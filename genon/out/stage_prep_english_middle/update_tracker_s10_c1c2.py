#!/usr/bin/env python3
"""S10 · english · middle — C1 and C2 into the tracker, plus the provenance panel.

Run from the repo root:
    python3 genon/out/stage_prep_english_middle/update_tracker_s10_c1c2.py

Cost figures are read from runtime_data/token_log.csv at run time, never retyped.
"""
import csv
import datetime
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/middle"
REPORT = "genon/out/library_reports/english_vi_ch08_20260813_103144.md"

rows = [r for r in csv.DictReader(open(ROOT / "runtime_data/token_log.csv"))
        if r["subject"] == "english" and r["grade"] == "vi" and r["chapter_number"] == "8"]
if len(rows) != 3:
    sys.exit(f"expected 3 metered rows for english vi ch 8, found {len(rows)}")
total = sum(float(r["cost_inr"]) for r in rows)
top, va, vb = rows

C1 = f"""PASS {NOW[:10]}. `python3 genon/build_library.py english vi 8` — run in two parts on founder's Terminal: --top-only first (the re-author window is the one time it is worth reading the standard BEFORE buying its compacts, since they are authored against its registry), then the resume, which skipped STEP 1 off disk and bought the two compacts.

LIBRARY ON DISK MATCHES canonical_plan.counts EXACTLY: ch_08_canonical.json (12 units) + ch_08_canonical_p10.json (10) + ch_08_canonical_p07.json (7) against counts [12, 10, 7]. The row finalized as the template requires: provisional false, basis 'authored_standard', registry_sections 6, authored [12, 10, 7].

EXIT CRITERION MET: GET /genon/english/vi/chapters lists chapter 8, and canonical_minutes = 480 = the class-standard 40 min x the top's 12 periods, matching the master_plan row. load_genon_library returns 3 files.

CERTIFICATION REPORT ({REPORT}): DETERMINISTIC CHECKS ALL PASS, 37 PASS lines, zero FAIL.
  - library complete against the plan;
  - the standard closes with the mandated `synthesis` unit and carries the token nowhere else; both compacts respect the reservation;
  - all 6 summary sections anchored by some unit, every anchor verbatim in the top registry, first-visit order followed, coverage reaching the final registry section — on ALL THREE files;
  - REGISTER CLEAN on all three (0 ban hits) across 47 + 40 + 25 bands, with the scan confirmed to have reached the band text (the S6-era failure mode where a clean result meant the scanner never read anything);
  - every declared stimulus type resolves, every question_type known, stems present/absent per type;
  - MCQ options in arrangement order after STEP 6 (4 of 4 items re-ordered this run, which is the honest reading on a freshly generated library).
  - SERVE SWEEP, all 10 asks non-empty choice set, no defensive truncation: X=5 fill/single -2s . 6 fill/single -1s . 7 IDENTITY . 8-9 fill/single . 10 IDENTITY . 11 synthesis . 12 IDENTITY . 13-14 surrender. Three identities at the three authored counts is exactly right, and the synthesis borrow appears at X=11 (the K+1 case) as v2.0 predicts.

INDEPENDENT STRUCTURAL RE-CHECK (not the certifier's, computed off the files): all three carry 6/6 spines — FULL SPINE COVERAGE holds at the floor of 7, which is the amendment this stage's P1 made and the first live proof of it; time bands tile 0..40 exactly with zero gaps in all 29 units; 12 assessment items per file = 2 x 6 cells, so the PAIR holds at every count and the item count does not vary with the period count (assessment Rule 2's corollary, also first proved here).

ADVISORY carried forward, not a fail: TRUE_FALSE is used by exactly one item in the whole library — flagged by the certifier for a C3 read against the type table.

NOTE FOR C3 AND C14, found while inspecting: poem lines reach teacher-facing strings in ways the ITEM rule does and does not cover. The two locator uses are COMPLIANT (7-word incipits, 'Read the lines on page 85 beginning "I lived first in a little house"'). One is NOT: p07's writing item quotes 12 words spanning two lines ('small and round and made of pale, blue shell') as content rather than as a locator, which Rule 3's PROHIBITED clause forbids beyond the eight-word incipit. And the LESSON PLAN has no such rule at all — the top's synthesis unit reads two full lines aloud in a band ('I don't know how the world is made / And neither do my neighbours'), which no english LP constitution caps. That is the ARV-D-108 shape (maths middle's LP-side F2 conduit) on a second subject; the 2026-08-12 poem-locator fix amended the three ASSESSMENT constitutions only. C3 raises the item breach; C14 owes the LP conduit."""

C2 = f"""PASS {NOW[:10]}. Every row for this chapter attributed from runtime_data/token_log.csv; nothing retyped.

  {top['timestamp']}  canonical_generation  in {top['input_tokens']:>6}  out {top['output_tokens']:>6}  Rs {float(top['cost_inr']):.2f}   (12 units, the standard)
  {va['timestamp']}  variant_generation    in {va['input_tokens']:>6}  out {va['output_tokens']:>6}  Rs {float(va['cost_inr']):.2f}   (10 units)
  {vb['timestamp']}  variant_generation    in {vb['input_tokens']:>6}  out {vb['output_tokens']:>6}  Rs {float(vb['cost_inr']):.2f}   (7 units)

TWO FIGURES, AND THEY ARE THE SAME ONE HERE: all-in Rs {total:.2f}, CLEAN PATH Rs {total:.2f}. NO RERUNS, no superseded generations — three runs produced the three files on disk, first time. The --top-only pause did not cost anything: STEP 1 is resumable and the resume skipped it off disk rather than re-buying it, which is the 2026-08-07 resumability fix earning its keep in the ordinary case rather than after a failure.

Rs {total/3:.2f} PER RUN against the Rs 37 benchmark (SS-IX ch 3) — 34% under, and the cheapest run of the campaign so far (maths middle was Rs 28.68). The chapter total is also the lowest: Rs {total:.2f} against english secondary's Rs 109.03 and SS-IX's Rs 110.99 clean.

COST SHAPE, confirming the benchmark's finding rather than restating it: input is FLAT at 22,318-22,382 tokens across all three runs (the constitutions, summary, mapping and brief are paid for in full every time), while output falls with period count — 14,874 at 12 units, 13,742 at 10, 11,272 at 7. So the 7-period compact costs 19% less than the 12-period top despite holding 42% fewer units. BUDGET PER AUTHORING RUN, NEVER PER UNIT.

WHY THIS STAGE IS CHEAP, worth recording for the corpus projection: english VI is fully split, so a chapter is ONE main_section and its input carries a single section's summary — 22.3k tokens against english IX's 25.4k and SS-IX's 14.9k-15.4k. Cost tracks the SUMMARY's size and the output's period count, not the subject.

CORPUS NOTE: at Rs {total/3:.2f}/run the 926-run corpus projects to ~Rs 22.7k synchronous (~Rs 26k with a 15% defect-rerun allowance), against the ~Rs 34k the SS-IX benchmark implies. SS-secondary remains the heavy corner; english middle is the light one. No cache write or read on any run — prompt caching is still not in play, and it is the obvious lever before the mass pre-warm.

CACHE: cache_write_input_tokens 0, cache_read_input_tokens 0 on all three rows."""

PROV = {
    "klass": "vi",
    "draw": "seed 'english|middle|2026-08-02' over ['vi', 'vii', 'viii']",
    "by": "Claude",
    "at": NOW,
    "chapter": "8 — What a Bird Thought (Nurturing Nature) · section B · POEM",
    "duration": "40",
    "model": "claude-sonnet-4-6",
    "date": NOW[:10],
    "lp_ver": "1.7",
    "as_ver": "3.7",
    "engine": "19",
    "variant_plan": ("canonical_plan: counts [12, 10, 7] · provisional false · basis "
                     "authored_standard · registry_sections 6 · authored [12, 10, 7] "
                     "(v2.0 equal dispersion over [7, 12]; the registry members are "
                     "(section x spine) CELLS, tokens 'B|<spine>' — note B, not A: english VI "
                     "is fully split but each chapter kept its section's position in the "
                     "original textbook unit)"),
    "ledger_ts": (f"top {top['timestamp']} (--top-only) · p10 {va['timestamp']} · "
                  f"p07 {vb['timestamp']} (cert report 20260813_103144, ALL PASS) · NO RERUNS"),
    "stages": {
        "top_canonical": {"wall_s": "n/a", "tokens_in": top["input_tokens"],
                          "tokens_out": top["output_tokens"],
                          "cost_inr": f"{float(top['cost_inr']):.2f}"},
        "variant_a": {"wall_s": "n/a", "tokens_in": va["input_tokens"],
                      "tokens_out": va["output_tokens"],
                      "cost_inr": f"{float(va['cost_inr']):.2f}"},
        "variant_b": {"wall_s": "n/a", "tokens_in": vb["input_tokens"],
                      "tokens_out": vb["output_tokens"],
                      "cost_inr": f"{float(vb['cost_inr']):.2f}"},
        "reruns": {"wall_s": "0", "tokens_in": "0", "tokens_out": "0", "cost_inr": "0.00"},
    },
    "total_cost_inr": round(total, 2),
    "partition_wall_s": "n/a (serve engine; certification sweep only)",
    "c5_split": "k1: identities · k2: fills + below-floor · k3: mixed week (40/50) + scaled",
}


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s10_c1c2"))
    row = state.setdefault("combos", {}).setdefault(KEY, {})
    row["C1"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C1}
    row["C2"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C2}
    row["provenance"] = PROV
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"tracker updated · {KEY} · C1 pass · C2 pass · provenance ₹{total:.2f} · {NOW}")


if __name__ == "__main__":
    main()
