#!/usr/bin/env python3
"""S9 · english · preparatory — fill the tracker's PROVENANCE & COST panel (§6 + C2).

    python3 genon/out/stage_prep_english_preparatory/update_tracker_s9_provenance.py

This is the half of C1/C2 that lives in the drawer rather than the step comment: the tracker's
per-stage cost column reads `combos["english/preparatory"].provenance.total_cost_inr`, and §6's
rule is that a result which cannot be attributed to a version is not a result.

total_cost_inr is the CLEAN-PATH figure (founder, 2026-08-07) — every run row EXCEPT `reruns`.
There are no reruns here, so clean path == all-in == Rs 63.86.

Wall seconds are DERIVED (ledger start-timestamp -> the run's token_log write), not measured by
a stopwatch; labelled as such rather than presented as instrumented.
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/preparatory"

PROV = {
    "klass": "iii",
    "draw": "seed 'english|preparatory|2026-08-02' over ['iii', 'iv', 'v']",
    "chapter": "11 — The Big Laddoo (The Big Laddoo)",
    "duration": "40",
    "model": "claude-sonnet-4-6",
    "date": "2026-08-13",
    "lp_ver": "1.2",
    "as_ver": "1.5",
    "engine": "19",
    "canonical_plan": ("canonical_plan: counts [12, 10, 7] · provisional false · basis "
                       "authored_standard · registry_sections 5 · authored [12, 10, 7] "
                       "(v2.0 equal dispersion over [7, 12]; registry members are "
                       "(section × spine) CELLS, tokens 'B|<spine>' — section B, not A, and "
                       "FIVE prep spines: reading · oracy · writing · word_work · beyond_text)"),
    "brief": ("top brief ch_11_top.txt (synthesis mandate as the \"synthesis\": true BOOLEAN — "
              "genon_anchor_field_present is False for english, so no reserved token is "
              "demanded) · compacts ch_11_p10.txt / ch_11_p07.txt (registry verbatim, "
              "synthesis reserved to the standard)"),
    "ledger_ts": ("top 20260813_123304 · p10 20260813_124142 · p07 20260813_124508 — "
                  "no reruns, no superseded generations (3 log rows, 3 ledger files, "
                  "3 installed canonicals)"),
    "report": ("genon/out/library_reports/english_iii_ch11_20260813_124746.md — "
               "DETERMINISTIC CHECKS ALL PASS (the 20260813_123939 report is the --top-only "
               "pass, whose single FAIL was the not-yet-authored compacts)"),
    "files": ("data/content/saved_plans/english/iii/ch_11_canonical.json · "
              "ch_11_canonical_p10.json · ch_11_canonical_p07.json"),
    "durations_run": "authored 40 · C6 owes 40 (kumar1, kumar2) and the 40/50 mix (kumar3)",
    "stages": {
        "top_canonical": {"wall_s": "186*", "tokens_in": "19734", "tokens_out": "11739",
                          "cost_inr": "21.6464"},
        "variant_a":     {"wall_s": "206*", "tokens_in": "19659", "tokens_out": "12615",
                          "cost_inr": "22.8346"},
        "variant_b":     {"wall_s": "157*", "tokens_in": "19659", "tokens_out": "10113",
                          "cost_inr": "19.3818"},
        "variant_c":     {"wall_s": "", "tokens_in": "", "tokens_out": "", "cost_inr": ""},
        "variant_d":     {"wall_s": "", "tokens_in": "", "tokens_out": "", "cost_inr": ""},
        "reruns":        {"wall_s": "", "tokens_in": "", "tokens_out": "", "cost_inr": ""},
    },
    "total_cost_inr": 63.86,
    "partition_wall_s": "n/a (serve engine; certification sweep only)",
    "c5_split": ("k1: identities (3C) · k2: between-variant + below-floor (3B) · "
                 "k3: mixed week 40/50 (3E) — profiles closed at P5.4, sections disjoint"),
    "note": ("C2 — CLEAN PATH = ALL-IN = Rs 63.86 over 3 runs, mean Rs 21.29/run: the cheapest "
             "library of the campaign (SS·IX ch 3 benchmark Rs 110.99 clean / Rs 145.70 all-in). "
             "THE COST SHAPE INVERTS AGAINST THE BENCHMARK: input is flat as expected "
             "(19,734 / 19,659 / 19,659, the 75-token delta being top brief vs compact brief), "
             "but OUTPUT DOES NOT FALL WITH PERIOD COUNT — the 10-unit compact wrote MORE than "
             "the 12-unit standard (12,615 vs 11,739) and cost 5% MORE (Rs 22.83 vs Rs 21.65). "
             "Two structural reasons, both english-specific: (a) the assessment is "
             "COUNT-INVARIANT — Rule 2's PAIR is two items per cell and the cell count is a "
             "property of the CHAPTER, so all three files carry 10 items; (b) bands do not scale "
             "with units — the top has 49 bands over 12 units (4.08/unit, its closing synthesis "
             "being lean) against p10's 50 over 10 (5.00/unit). SO 'a compact costs ~11% less "
             "than the top' MUST NOT BE GENERALISED: price an english library as N runs x the "
             "flat rate, with no compact discount. Stage extrapolation: 39 non-placeholder "
             "chapters = 109 authoring runs; Rs 2,320 at this rate (Rs 2,668 with a 15% defect "
             "allowance), Rs 4,033 at the campaign's Rs 37/run. The pilot is NOT a flattering "
             "rate source — ch 11 is tied for the largest chapter in class III. "
             "* wall seconds are DERIVED from ledger start to token_log write, not instrumented."),
    "by": "Claude",
    "at": NOW,
}


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s9_prov"))
    combo = state.setdefault("combos", {}).setdefault(KEY, {})
    prov = combo.setdefault("provenance", {})
    prov.update(PROV)
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"provenance written · {KEY} · total_cost_inr = {PROV['total_cost_inr']} · {NOW}")


if __name__ == "__main__":
    main()
