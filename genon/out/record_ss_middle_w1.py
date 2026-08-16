#!/usr/bin/env python3
"""Record SS·middle batch wave 1 in the testing tracker (2026-08-16).

Written because the campaign state file is never hand-edited (docs/testing.md §6a) — every
observation goes through the API. Run it with uvicorn up:

    python3 -m uvicorn api.main:app --port 8000        # if not already running
    python3 genon/out/record_ss_middle_w1.py           # idempotent per (scope,key,step) / defect id

Posts: the W1 step row, plus three defect rows (the meta-leak family, the Jallianwala clock
false positive, and the duplicate-key shadowing found while declaring the repairs).
"""
import json
import urllib.request

BASE = "http://127.0.0.1:8000/api/testing"
KEY = "social_sciences/middle"


def post(path: str, payload: dict) -> dict:
    req = urllib.request.Request(
        f"{BASE}/{path}",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "X-Aruvi-User": "Kumar1"},
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)


W1_COMMENT = (
    "S2 · classes vi/vii/viii · 2026-08-15/16. <b>41 chapters, 40 standards bought</b> in one "
    "job (msgbatch_012rg61LP1SVF4ay2JM34bt2), <b>₹881.64</b>, 40/40 ok, zero errors, zero "
    "canonicals re-bought; viii ch 3 correctly skipped as the C-cycle pilot. Est. was ₹760 at "
    "the runbook's fit — SS runs longer than TWAU per period (~₹22/run vs ₹12–15).<br><br>"
    "<b>Structurally the wave is spotless.</b> Across all 41 chapters, zero failures on "
    "synthesis-token placement, anchors verbatim in the registry, first-visit order, coverage "
    "reaching the final registry section before synthesis, stimulus-type resolution, "
    "question-type validity, stems, and MCQ arrangement order; every X in every sweep returned "
    "a non-empty choice set. The only FAIL families are <i>library complete</i> (×40 — "
    "arithmetic, the compacts do not exist until W2) and <i>register clean</i>.<br><br>"
    "<b>Register: 90 ban hits over 34 of 40 files</b> (~2.25/file, against S5's ~1 per 3). "
    "42 clock · 33 forward · <b>10 meta-leak (new family, ARV-D-161)</b> · 2 ids · 2 calendar · "
    "1 completion. Plus 8 artefact-dependency advisories, which certification cannot gate and "
    "which are owed a read at F1.<br><br>"
    "<b>87 repairs declared</b> in genon/repair_register.py under ("
    "social_sciences, vi/vii/viii) — every one a deletion, none hand-edited, none regenerated. "
    "Verified by applying the full set to a copy of the library: 87/87 resolve verbatim and the "
    "residual is exactly the 3 deliberate exclusions (ARV-D-162 and the two calendar hits, "
    "founder ruling 2026-08-16 to leave them). <b>The library is therefore NOT yet at zero ban "
    "hits</b> — closing-checklist item 3 is met only once those three are ruled or the scanner "
    "is narrowed.<br><br>"
    "Also worth carrying to W2: <i>options arranged 15 of 16 on a first pass</i> — this is a "
    "freshly generated library, the only pass where that number means anything, and it confirms "
    "the model still does not arrange MCQ options unaided. Two items were SKIPPED by the "
    "arranger because they cross-reference an option label; those need a human."
)

# NOTE: /campaign/item takes an ItemPatch — the recorded fields go UNDER `patch`, not at the
# top level. Posted flat on the first run (2026-08-16) and the row saved with only its
# server-stamped `at`, silently: unknown top-level keys are dropped, not rejected.
post("campaign/item", {
    "scope": "batch", "key": KEY, "step": "W1",
    "patch": {
        "status": "pass", "by": "Kumar (ran) · Claude (recorded)",
        "comment": W1_COMMENT, "files": 41,
    },
})

post("campaign/defect", {
    "id": "ARV-D-161",
    "combo": KEY, "step": "W1", "severity": "S3", "owner": "Kumar (founder)",
    "status": "open",
    "title": "meta-leak: the model narrates its own register compliance inside the artefact "
             "(10 hits / 40 files, new defect family)",
    "evidence": "teacher_notes across 8 chapters, e.g. viii ch_11 U11 \"…shows how the "
                "chapter's sections connect WITHOUT REQUIRING ANY EARLIER UNIT TO HAVE "
                "HAPPENED\"; vii ch_10 U17 \"…sets up the synthesis unit without requiring any "
                "specific prior activity to have occurred\"; vi ch_07 U17, vi ch_09 U5, vi ch_10 "
                "U15, vii ch_06 U18, vii ch_10 U14/U18, viii ch_08 U5. viii ch_11 U11 is the "
                "sharp case: the same sentence carries a BACKWARD unit dependency (\"as "
                "established in the earlier unit on Supreme Court jurisdiction\") and then "
                "asserts it requires no earlier unit.",
    "notes": "Not a teaching defect and not the 2026-08-02 lottery case — the constitution "
             "states the register and the model is OBEYING it, out loud, in prose addressed to "
             "the constitution rather than to the teacher. So this is brief-side: the next "
             "SS·middle constitution pass should say that self-containment is demonstrated by "
             "the unit working, never by asserting it. Same shape as the S4 finding (repair "
             "v1.4) where the model paraphrased the brief's own description of the synthesis "
             "unit. Repaired in place for this wave at the founder's instruction 2026-08-16; "
             "the row stays open against the brief, not the artefacts.",
})

post("campaign/defect", {
    "id": "ARV-D-162",
    "combo": KEY, "step": "W1", "severity": "S3", "owner": "Kumar (founder)",
    "status": "open",
    "title": "register_scan clock ban fires on a narrated HISTORICAL duration — repairing it "
             "would falsify the history",
    "evidence": "viii ch_09 (India's Long Road to Independence) U11 band:0: \"Brigadier-General "
                "Dyer sealed the main exit and fired approximately 1,650 rounds FOR ABOUT TEN "
                "MINUTES, deliberately aiming at the thickest parts of the crowd.\" The "
                "quantity is the duration of the Jallianwala Bagh massacre, not the pacing of a "
                "classroom activity.",
    "notes": "Runbook trap 4: a false positive is fixed at the scanner, not in the text. The "
             "clock ban exists because a band's minutes are rescaled per sitting, which has "
             "nothing to say about a duration inside narrated content. Deliberately NOT "
             "declared in the repair set — striking it to satisfy a regex is the wrong "
             "direction. Suggested narrowing: exempt a clock quantity whose sentence subject is "
             "not the class/teacher/students. Until then this keeps the library at 1 ban hit "
             "and blocks closing-checklist item 3.",
})

post("campaign/defect", {
    "id": "ARV-D-163",
    "combo": KEY, "step": "W1", "severity": "S4", "owner": "Claude",
    "status": "fixed-awaiting-recheck",
    "title": "repair_register.py: a second live (\"social_sciences\",\"viii\") key silently "
             "shadowed the new batch set",
    "evidence": "The 2026-08-04 VIII ch 3 pilot set sat at the live 2-tuple key. Adding the "
                "batch wave-1 set under the same key made it a duplicate in one dict literal; "
                "Python keeps the LAST, so --grade viii ran the already-applied pilot "
                "declarations and died on its own \"declared text not found\" guard.",
    "notes": "Fixed by moving the pilot set to (\"social_sciences\",\"viii\",\"APPLIED-20260804\") "
             "— the pattern the file already uses for ix/APPLIED-20260803 and mathematics·IX "
             "v1.5. The guard caught it, which is the guard working; the key layout is what "
             "made it possible. Worth a one-line check in the tool that no 2-tuple key is "
             "declared twice.",
})

post("campaign/defect", {
    "id": "ARV-D-164",
    "combo": "campaign", "step": "W2", "severity": "S2", "owner": "Claude",
    "status": "fixed-awaiting-recheck",
    "title": "genon/master_plan.py rebuilt master_plan.json AT IMPORT, erasing every "
             "canonical_plan annotation portfolio-wide",
    "evidence": "2026-08-16 09:48. A verification script did `import master_plan` to reach the "
                "pure helper canonical_periods() for checking the W2 dry-run counts. The "
                "module's body ran, including `with open(master_plan.json,'w')`, regenerating "
                "the plan from the workbook. `canonical_plan` vanished from ALL 340 chapter "
                "rows across all five subjects — including RELEASED stages (TWAU·preparatory, "
                "SS·secondary). Surfaced as the W2 compact submit refusing all 40 SS·middle "
                "chapters with \"Row is provisional — author and certify the standard "
                "canonical\", which points at the standards rather than at the erasure.",
    "notes": "Recovered free and exactly: `python3 genon/variant_plans.py` re-annotated 188 "
             "authored rows, and a field-by-field diff against git HEAD showed the ONLY "
             "remaining difference was the 40 SS·middle rows going provisional true→false — "
             "which is W1's own annotation, i.e. correct. Every count, budget and pin "
             "identical. FIX: the write and its prints now sit under `if __name__ == "
             "'__main__'`, so a rebuild is an explicit act and an import is inert (verified: "
             "artefact byte-identical after import, canonical_periods still callable). "
             "Standing lesson for the campaign: a module that mutates a data artefact at "
             "import will eventually be imported by something that only wanted a helper, and "
             "the damage shows up somewhere else entirely. Worth grepping the other genon "
             "scripts for module-level writes.",
})

print("recorded: W1 + 4 defect rows")
