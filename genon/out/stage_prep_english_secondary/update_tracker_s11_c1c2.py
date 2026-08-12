#!/usr/bin/env python3
"""S11 · english · secondary — provenance + C1 + C2 into the campaign tracker (2026-08-12).

Run from the repo root:
    python3 genon/out/stage_prep_english_secondary/update_tracker_s11_c1c2.py
Then reload docs/testing_tracker.html.

Also files two defects: ARV-D-127 (the item-shape gate's field-name blindness — found and
fixed here) and ARV-D-128 (LP Rule 5's minimum-3-bands breached on the floor canonical —
open, for C3).
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/secondary"

PROVENANCE = {
    "klass": "ix",
    "draw": "seed 'english|secondary|2026-08-02' over ['ix'] (the only eligible class)",
    "by": "Claude",
    "at": NOW,
    "chapter": "7 — Vitamin-M (Vitamin-M)",
    "duration": "50",
    "model": "claude-sonnet-4-6",
    "date": "2026-08-12",
    "lp_ver": "1.2",
    "as_ver": "1.4",
    "engine": "12",
    "variant_plan": ("canonical_plan: counts [17, 14, 10] · provisional false · basis "
                     "authored_standard · registry_sections 6 · authored [17, 14, 10] "
                     "(v2.0 equal dispersion over [10, 17]; the registry members are "
                     "(section x spine) CELLS, tokens 'A|<spine>')"),
    "ledger_ts": ("top 20260812_141916 · p14 20260812_142352 · p10 20260812_142824 "
                  "(cert report 20260812_143511, ALL PASS)"),
    "stages": {
        "top_canonical": {"wall_s": "275.1", "tokens_in": "25412", "tokens_out": "16041",
                          "cost_inr": "29.15"},
        "variant_a":     {"wall_s": "271.5", "tokens_in": "25467", "tokens_out": "15466",
                          "cost_inr": "28.37"},
        "variant_b":     {"wall_s": "186.0", "tokens_in": "25467", "tokens_out": "11405",
                          "cost_inr": "22.77"},
        "reruns":        {"wall_s": "0", "tokens_in": "0", "tokens_out": "0",
                          "cost_inr": "0.00"},
    },
    "total_cost_inr": 80.29,
    "partition_wall_s": "n/a (serve engine; certification sweep only)",
    "c5_split": "k1: identities · k2: fills + below-floor · k3: mixed week (50/60) + scaled",
}

C1 = """LIBRARY BUILT AND CERTIFIED - english IX ch 7 'Vitamin-M', counts [17, 14, 10], all three at 50 min, engine 12, claude-sonnet-4-6, LP v1.2 / assessment v1.4. Deterministic checks ALL PASS (report genon/out/library_reports/english_ix_ch07_20260812_143511.md). Library installed at data/content/saved_plans/english/ix/; canonical_minutes 850 = 50 x 17, matching the C1 exit criterion.

THE GATES WORTH NAMING, because they are the ones S11's P-prep was about:
- EVERY ANCHOR VERBATIM IN THE TOP REGISTRY on all three files. This stage's registry token is a COMPOSITE the platform builds rather than a field the model writes - 'A|reading_for_comprehension', joined 'A|listening / A|speaking' - so the check is really asking whether section_id + spines_taught[] came out clean on 41 units. It did.
- FIRST-VISIT ORDER follows the registry on all three, and the walking order (on-page: Reading, VocGram, Listening, Speaking, Writing, Beyond) is NOT the handoff's enumeration order. Both are present in every file and they differ, exactly as LP Rule 2 STEP 3 says they must.
- THE STANDARD CLOSES WITH THE MANDATED SYNTHESIS UNIT (unit 17) and carries the marker nowhere else; both compacts carry it nowhere. The mandate reached the model as the BOOLEAN, which is what genon_anchor_field_present=False buys - a token mandate would have asked for a field english's constitution does not define.
- REGISTER CLEAN on all three (0 ban hits over 54 / 57 / 26 bands), on a constitution that received the three-ban block this morning.
- FULL SPINE COVERAGE HELD AT EVERY COUNT, which is the amendment this stage exists for: all six spines taught, all six handoff cells emitted and 6 items produced in the 17, the 14 AND the 10. The corpus plan that prompted the amendment (ch 12, 4 periods) had dropped one outright.
- Serve sweep non-empty across X = 8..19: identity 10/14/17 | fill/single 9,12,13,16 | fill/forward 8 | rescue/complete 11 (from 14), 15 (from 17) | surrender 18,19.

TWO FAILURES ON THE WAY, NEITHER OF THEM THE LIBRARY'S, AND NEITHER COST A RUPEE:
1. The first C1 attempt stopped at STEP 1 with NotImplementedError - english was the one subject whose prompt wrapper had never been lifted from the prototype, and the refusal named this exact moment as its condition ('lift it verbatim when the English combo enters step 3/4 - its constitution is not yet genon-amended'). It raised in prepare_job, BEFORE the API call. Lifted from Project Aruvi app/aruvi_streamlit/app.py 584-901 with 7 diff lines, all declared: phases -> time_bands in the period sketch and length constraints (FORCED by this morning's P3 - compile v0.5 is declared-only, so the verbatim string would have bought a canonical that does not compile), and the return annotation the prototype had wrong. Artefacts in genon/out/stage_prep_english_secondary/.
2. The first certification run FAILED and quarantined all three files on 'every non-OPEN_TASK item carries a stem (6 without)'. FALSE FAILURE - see ARV-D-127. The items all carry populated stems; the gate read `question_text`, which is not what english's constitution calls the field. Fixed, quarantine restored, re-certified free.

ADVISORIES (do not gate, read at C3): 'TRUE_FALSE used by exactly one item in the whole library' (top) and 'SCR used by exactly one item' (p10) - both legal for this stage's type set and expected when a library has six items per file, one per spine. The competency census reports 0 vs 0 on all three, which is correct and not a gap: english has no per-chapter competency mapping and C-codes are forbidden in its LP and assessment."""

C2 = """COSTED 2026-08-12 - PASS. Full artefact: docs/testing_artefacts/c2_english_ix_ch07.md

THE LIBRARY COST - 3 metered runs, Sonnet 4.6, each an LP AND its assessment in one call (source runtime_data/token_log.csv; wall time from genon/ledger.csv):
  14:19:16 -> 14:23:52  canonical_generation  in 25,412 / out 16,041  Rs 29.15  wall 275.1s  (top, 17 units)
  14:23:52 -> 14:28:24  variant_generation    in 25,467 / out 15,466  Rs 28.37  wall 271.5s  (p14)
  14:28:24 -> 14:31:30  variant_generation    in 25,467 / out 11,405  Rs 22.77  wall 186.0s  (p10)
  LIBRARY TOTAL: in 76,346 / out 42,912 / Rs 80.29 over 732.6s (12.2 min).

DEFECT RERUNS: ZERO. Every call returned ok with no problems and no auto-repair. Both failures this stage hit (the prompt-builder refusal, the false quarantine) landed on FREE paths - before the API call, and on --certify-only.

THE CHEAPEST LIBRARY OF THE CAMPAIGN SO FAR, AND IT AUTHORS THE MOST UNITS. Rs 26.76 per canonical against SS-secondary ch 3's Rs 38.82, on 41 units against 29. Cause, in order of size: (1) OUTPUT is what you pay for (5x input) and english emits little of it - its assessment is ONE ITEM PER (section x spine) CELL, six per canonical FIXED, where SS emits 18-29 against a per-competency slate; english's whole library emitted 42,912 output tokens, SS's single top canonical emitted 26,649. (2) Input is the largest in the campaign (~25.4k tokens vs SS's ~15.3k - two long constitutions plus the whole two-axis summary) and it costs about Rs 2.8 per call extra.

THE ESTIMATE WAS WRONG BY 3x AND THE REASON IS WORTH KEEPING: I projected Rs 200-250 from PROMPT CHARACTERS before the run. Prompt size is the input side; the bill is dominated by output. Project a corpus from output tokens per unit and per item, never from prompt size - the same mistake at portfolio scale would misprice the whole pre-warm.

PORTFOLIO IMPLICATION: at Rs 80.29 per 3-canonical library, english IX's 16 chapters project to ~Rs 1,285 and the English family's 101 chapters to ~Rs 8,100 - the cheapest subject per chapter, on the largest chapter count. Preparatory carries five spines and shorter texts, so its per-chapter figure should fall.

LEDGER HYGIENE, unchanged from the last C2 and now pinned: genon/ledger.csv rows are column-shifted by one from their header (an extra empty field around tag/subject), so aggregating it by subject returns nonsense. token_log.csv - what C2 costs from - is intact, and the ledger's wall-time column still lands correctly."""

DEFECTS = [
    {
        "id": "ARV-D-127", "combo": KEY, "step": "C1", "severity": "S2",
        "owner": "Claude", "status": "closed", "opened": NOW, "closed": NOW, "at": NOW,
        "title": ("the item-shape gate reads `question_text` only, so it FALSE-FAILED and "
                  "quarantined a clean english library — english's constitution names the "
                  "field `item_stem`"),
        "evidence": (
            "First certification of english IX ch 7 (report 20260812_143130) returned "
            "'every non-OPEN_TASK item carries a stem (6 without)' on ALL THREE canonicals — "
            "18 items, every one of them reported as having nothing to ask — and quarantined "
            "the whole library ('top canonical failed — the entire library is quarantined "
            "with it').\n\n"
            "Every one of those items carries a populated stem. English's assessment "
            "constitution names the field **`item_stem`** at all three stages (its JSON "
            "schema block, and the corpus agrees: 82 occurrences of `item_stem` across saved "
            "english plans). The gate — added the same morning at S5's C3 as ARV-D-123 — "
            "reads `question_text`, on a comment asserting that 'every schema in the corpus "
            "says the same two things': a census that missed english.\n\n"
            "WHAT MAKES IT S2 RATHER THAN S3: the gate QUARANTINES. A false positive here "
            "does not annoy a reader, it moves a paid library off disk and reports it as a "
            "fix worklist. Had this landed one stage earlier the same run would have read as "
            "'the model omitted every stem', which is a re-generation (~Rs 80) chasing a "
            "defect that does not exist.\n\n"
            "FIX (2026-08-12): `build_library.item_stem()` reads the stem under either name "
            "and the report names the field the item actually carries. `_STEM_FIELDS = "
            "('question_text', 'item_stem')` is the whole inventory, verified by census over "
            "every saved plan and canonical on disk; the prototype-era maths `prompt` (471 "
            "occurrences, no canonical) is recorded in the comment and deliberately not read. "
            "Quarantine restored, re-certified on the free path: ALL PASS.\n\n"
            "THE GENERAL LESSON, third instance in this campaign after the carrier seam and "
            "the handoff shapes: a check that names a FIELD is a check that branches on "
            "subject, whether or not it says so. The platform's own answer already existed — "
            "`carriers.period_section_codes` and `unit_approaches` read the same fact under "
            "five names each — and a new gate should reach for it rather than assume."),
    },
    {
        "id": "ARV-D-128", "combo": KEY, "step": "C3", "severity": "S3",
        "owner": "founder", "status": "open", "opened": NOW, "closed": None, "at": NOW,
        "title": ("the FLOOR canonical breaches LP Rule 5's 'minimum 3 bands' on 4 of its 10 "
                  "units, and nothing deterministic looks at band COUNT"),
        "evidence": (
            "english LP Rule 5: 'Each period's time bands sum EXACTLY to "
            "period_duration_minutes; minimum 3 bands.' Measured on the certified library:\n"
            "  ch_07_canonical.json    (17 units) — 0 breaches (54 bands, min 3)\n"
            "  ch_07_canonical_p14.json (14 units) — 0 breaches (57 bands)\n"
            "  ch_07_canonical_p10.json (10 units) — **4 breaches**: U2, U4, U5 and U8 carry "
            "TWO bands each ('0–25/25–50', '0–15/15–50', '0–20/20–50', '0–20/20–50').\n"
            "TILING IS CLEAN everywhere — every unit tiles 0..50 with no gap or overlap — so "
            "this is the count alone.\n\n"
            "It appears only on the FLOOR canonical, which is where the S8 lesson says a "
            "stated number gets tested: at 10 periods a whole (section × spine) cell lands in "
            "one unit and the model writes it as two long moves. Whether that is a defect or "
            "a rule that should relax is a C3 read and a founder call — the same shape as "
            "S4's word counts (relaxed) and S7's consecutive-method cap (relaxed with an "
            "exception).\n\n"
            "WHAT IS NOT ARGUABLE: nothing tests it. The certifier checks the register, the "
            "anchors, coverage, stimulus tags, item shape and MCQ order; band COUNT and band "
            "TILING are checked nowhere, though `normalize.phase_tiling_issues` already exists "
            "and would give both for free on every stage. Owed as a certifier check, in the "
            "same list as S7/S8's un-built 'no section appears in two non-contiguous runs'."),
    },
]


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s11_c1c2"))
    combo = state.setdefault("combos", {}).setdefault(KEY, {})
    combo["provenance"] = PROVENANCE
    combo["C1"] = {"status": "pass", "by": "Kumar", "at": NOW, "comment": C1}
    combo["C2"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C2}

    have = {d.get("id") for d in state.get("defects", []) if isinstance(d, dict)}
    for d in DEFECTS:
        assert d["id"] not in have, f"{d['id']} already filed"
        state["defects"].append(d)

    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"tracker updated · {KEY} · provenance + C1 pass + C2 pass · "
          f"defects ARV-D-127 (closed), ARV-D-128 (open) · {NOW}")


if __name__ == "__main__":
    main()
