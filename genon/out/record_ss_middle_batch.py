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

# THE ₹ COLUMN IS ITS OWN ITEM, not a number parsed out of a comment. testing_tracker.html
# reads `item("batch", key, "spend").cost_inr` for the Total ₹ column and for the corpus
# totals row; W1/W2 comments are rendered as NOTES and are never scanned for figures. Posting
# the cost inside the wave comments therefore left the column blank while the data was on
# record — which is how it looked on 2026-08-16 until the tracker source was read.
# The column is ALL METERED SPEND on the stage, pilot and reruns included (its own tooltip
# says so), so it is NOT the batch total: the VIII ch 3 pilot on 2026-08-04 adds ₹149.28.
post("campaign/item", {
    "scope": "batch", "key": KEY, "step": "spend",
    "patch": {
        "cost_inr": 2481.92,
        "comment": "₹2,481.92 = all metered SS·middle spend, 124 runs, from "
                   "runtime_data/token_log.csv. SPLIT: ₹149.28 pilot (VIII ch 3, 2026-08-04, "
                   "pre-batch) + ₹2,332.64 batch (2026-08-16) — the batch itself being "
                   "₹881.64 wave 1 (40 standards) + ₹1,422.83 wave 2 (80 compacts) + ₹28.17 "
                   "for the single re-author (VIII ch 15 p14). Reconciled to the rupee against "
                   "the three collected manifests. Per-run: ~₹22 at wave 1, ~₹18 at wave 2. "
                   "ONE file regenerated in the whole stage; every other defect was repaired "
                   "by declaration at ₹0 — 232 declared edits across 90 files.",
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

W2_COMMENT = (
    "S2 · wave 2 · 2026-08-16. <b>80 compacts, ₹1,422.83</b> (msgbatch_011ezdQUpviWiYgZmANzzDp4), "
    "80/80 ok, plus a <b>₹28.17</b> re-author of viii ch 15 p14. <b>Stage total ₹2,332.64.</b><br><br>"
    "<b>Certification: 36 of 41 chapters ALL PASS.</b> `library complete` cleared for every "
    "chapter except viii ch 8 (see below). The five remaining failures are: four chapters "
    "carrying one ruled-exclusion register hit each (vii ch 3, vii ch 11, viii ch 9, viii ch 14) "
    "and viii ch 8 on `library complete`, because its p08 is held in quarantine by design.<br><br>"
    "<b>Structural defects, all closed without re-authoring except one.</b> The compacts "
    "produced the failures wave 1 could not — 10 first-visit-order, 6 anchor-verbatim, 3 "
    "coverage — and the diagnosis inverted the obvious reading in three of five cases: "
    "<i>vi ch 7</i> (coverage) was an anchor-GRANULARITY defect, its U18–U21 wearing "
    "first-exposure anchors on revisit units; re-anchoring took the registry 21→17 and cleared "
    "p13 with no teaching change. <i>vii ch 3</i> (order, 2 files) was ONE under-labelled token "
    "— U6 is titled 'Winds AND TOPOGRAPHY' and anchored only Winds, which pushed Topography's "
    "first exposure to U16 and made two correct compacts look like they jumped. <i>vii ch 8 "
    "p13</i> was a genuine transposition, fixed by declared permutation. <i>viii ch 15 p14</i> "
    "was re-authored (₹28.17): its worst defect — [2] Regional saints first taught in the "
    "CLOSING unit — is gone, and it drew two milder breaks instead, one fixed by permutation. "
    "<i>viii ch 7/10/12</i> were nine anchor token-drops.<br><br>"
    "<b>229 repair edits recorded across 90 files today</b> — 87 register (wave 1) + 126 "
    "register (wave 2) + 9 anchor token-drops + 5 anchor re-grains + 2 permutations. Every one "
    "declared (old→new) and applied by assertion; none hand-edited; one file regenerated in the "
    "whole stage.<br><br>"
    "<b>CLOSING CHECKLIST — items 1,2,3,6,7 MET as of 2026-08-16 12:20.</b> (1) 123 canonical "
    "files on disk = exactly 41 chapters × 3, none missing. (2) nothing quarantined without a "
    "live counterpart. (3) <b>zero register ban hits stage-wide</b> — the last five were "
    "cleared at the SCANNER, never in the text (ARV-D-162/167): every calendar hit across all "
    "five stages was content, and the clock ban now requires a classroom actor. (6) no derived "
    "plans on disk. (7) spend reconciled to the rupee — ₹2,332.64 from the three collected "
    "manifests AND from 121 rows of runtime_data/token_log.csv. Item 4 (every chapter ALL "
    "PASS) confirmed chapter-by-chapter; item 5 (serves at top/middle/floor/below-floor) is "
    "the remaining deterministic step before the human gate."
)

F1_COMMENT = (
    "<b>SAMPLING PLAN — recorded before any reading begins</b> (runbook §5 / testing.md §6a).<br><br>"
    "<b>The runbook's own stratification rule does not survive this wave and is deliberately "
    "replaced.</b> It says include 100% of any chapter that took a repair — written at S5, "
    "where 28 repairs were unusual. Here <b>40 of 41 chapters took one</b> (232 edits), so that "
    "rule selects the whole corpus and stops being a sample. The replacement splits by WHAT was "
    "repaired: a register edit is a text deletion and cannot move a borrow seam, whereas anchor "
    "and order edits are precisely what the X−1→X math reads.<br><br>"
    "<b>MANDATORY — 8 chapters whose STRUCTURE was touched, read at 100%:</b> vi ch 7 (anchor "
    "re-grain, registry 21→17) · vii ch 3 (anchor re-grain, Topography's first visit moved) · "
    "vii ch 8 (unit permutation, 2 transpositions) · viii ch 7, ch 10, ch 12 (anchor "
    "token-drops) · viii ch 8 (two orphan units re-anchored to the parent section) · viii ch 15 "
    "(re-author + permutation).<br><br>"
    "<b>RANDOM SAMPLE — 25% of the remaining 33, stratified by top-canonical period band</b>, "
    "seed <code>social_sciences|middle|F1|2026-08-16</code>, "
    "<code>random.Random(seed).sample(sorted(pool), k)</code> per band, drawn in band order "
    "small→mid→large: <b>small ≤11p</b> (pool 6, k=2): vi ch 13, viii ch 13 · <b>mid 12–17p</b> "
    "(pool 16, k=4): vi ch 4, vi ch 8, viii ch 2, viii ch 5 · <b>large ≥18p</b> (pool 11, k=3): "
    "vi ch 6, vii ch 1, vii ch 10.<br><br>"
    "<b>TOTAL: 17 of 41 chapters (41%).</b> Read at each chapter's borrow boundary — X just "
    "above a canonical count, where the Xth unit is borrowed — not at the identity counts, "
    "since identity serves cannot jump.<br><br>"
    "<b>Carried into the reading as known items, not defects:</b> viii ch 15 p14 U7 anchors [6] "
    "Gardens and [9] Vocational education jointly, pulling 9 ahead of 7 and 8 — no permutation "
    "fixes it and 9 is taught nowhere else in that compact; and the 8 artefact-dependency "
    "advisories from W1 (a unit reaching for something a previous sitting produced), which "
    "certification cannot gate and which only a reader can rule on."
)

F1_VERDICT = (
    "<br><br><b>VERDICT — PASS (founder, 2026-08-16).</b> All 17 chapters presented at both "
    "borrow boundaries (34 serves). Census: 17 synthesis · 10 complete_rescue · 7 fill · "
    "<b>zero dropped sections</b>. Only the 7 FILL seams borrow an ordinary teaching unit and "
    "are therefore the only places jumpiness can enter; the founder read all seven — some were "
    "addressed in-session (below), the rest read clean.<br><br>"
    "<b>THREE DEFECTS FOUND, none of which any deterministic check could see — which is the "
    "case for this gate existing:</b><br>"
    "1. <b>viii ch 8's STANDARD was mislabelled</b> (ARV-D-170): seven of thirteen units "
    "carried the section BEFORE the one they taught — a unit anchored `North America` titled "
    "\"Australia's Deserts, the Spinifex People, and Antarctica\". It certified ALL PASS "
    "because the registry is DERIVED from the standard, so a self-consistent mislabelling is "
    "invisible. Re-anchored (Fable 5 against a constrained prompt, verified before applying); "
    "registry 12 -> 15; three earlier compact repairs REVERTED because they had been "
    "compensating for it.<br>"
    "2. <b>Coverage was counted as a FRONTIER, not a set</b> (ARV-D-168) — found by the "
    "founder asking why a borrowed unit that skips sections declares no drops. Fixed.<br>"
    "3. <b>The coverage registry was re-derived from the SERVED variant</b> (ARV-D-169), so a "
    "compact could never appear to drop what was never on its own list. Fixed.<br><br>"
    "<b>The pattern is one mistake in three places</b> — the code repeatedly asked \"how far "
    "did we get?\" where the question is \"what did we cover?\". The same shape sits in C5's "
    "coverage check (`seen_hi >= len(reg)-1`) and in check 11, both still open."
)

post("campaign/item", {
    "scope": "batch", "key": KEY, "step": "F1",
    "patch": {"status": "pass", "by": "Claude (presented) · Kumar (ruled)",
              "comment": F1_COMMENT + F1_VERDICT, "files": 17},
})

post("campaign/defect", {
    "id": "ARV-D-168", "combo": "campaign", "step": "F1", "severity": "S2",
    "owner": "Claude", "status": "fixed-awaiting-recheck",
    "title": "serve.py counted coverage as a FRONTIER, so a borrowed unit with non-contiguous "
             "anchors silently swallowed the sections inside its own span",
    "evidence": "SS·VIII ch 15 X=11: the borrowed unit anchors [12, 15]; `unit_range` collapses "
                "it to (12,15) and `uncovered = list(registry[b+1:])` concluded 13 and 14 were "
                "taught. Served plan omitted Cultural Exchange — Food and Clothing with "
                "uncovered_sections: [], dropped_units: NONE. 43 of 1,519 SS·middle units have "
                "non-contiguous anchors; the docstring ASSUMED otherwise ('Contiguity (V2) "
                "makes every co-dealt section adjacent to M').",
    "notes": "Found at F1 by the founder, not by any check. FIXED with a new `unit_sections()` "
             "returning a SET, and uncovered computed as a set difference; selection and "
             "preference deliberately untouched so the change is measurable on its own. "
             "OUTCOME BETTER THAN A DECLARED DROP: honest counting made Case 2's fill show "
             "uncovered sections, which is Case 1b's trigger, so X=11 now serves the 10-period "
             "canonical COMPLETE plus the synthesis — 16/16 sections, zero drops. The bug had "
             "been suppressing a better branch by making a torn fill look complete. Verified "
             "corpus-wide: 1,444 serves, 0 errors, mode distribution intact.",
})

post("campaign/defect", {
    "id": "ARV-D-169", "combo": "campaign", "step": "F1", "severity": "S2",
    "owner": "Claude", "status": "fixed-awaiting-recheck",
    "title": "serve.py judged coverage against the SERVED variant's registry, not the top's",
    "evidence": "`serve_plan` computes `registry_top` and then the unit-granularity branch "
                "re-derived `registry = section_registry(chosen)` for `fill_slot`. SS·VIII ch 8 "
                "X=7 picks the 8-period compact, whose own registry omits Ocean currents and "
                "Ocean trenches, so it reported full coverage of a chapter it teaches 13 of 15 "
                "sections of.",
    "notes": "Founder's call: the architecture establishes the registry ONCE from the top. "
             "Measured before changing — on 1,398 of 1,400 serves the two registries are "
             "IDENTICAL, so this corrects a real hole without moving the common case; both "
             "exceptions are ch 8. Now passes `registry_top`. Consequence: ch 8 X=7 declares "
             "all three uncovered sections where it previously declared one. NOTE the residual "
             "— only Australia has a unit able to ride as a dropped unit, because the lender "
             "(p08) never teaches currents or trenches, so `section_coverage_note` promises "
             "material for two sections it does not ship. p08's brief was itself built from "
             "the mislabelled registry (ARV-D-170), so re-authoring it closes both.",
})

post("campaign/item", {
    "scope": "batch", "key": KEY, "step": "W2",
    # `files` on W1/W2 is CANONICALS ON DISK, not chapters — the tracker's two columns are
    # "top canonicals" and "compact canonicals". Posted as 41/41 first time round, which read
    # as though wave 2 had bought one file per chapter instead of two.
    "patch": {
        "status": "pass", "by": "Kumar (ran) · Claude (diagnosed + declared)",
        "comment": W2_COMMENT, "files": 82,        # 82 compacts (41 chapters x 2)
    },
})

post("campaign/defect", {
    "id": "ARV-D-165",
    "combo": KEY, "step": "W2", "severity": "S2", "owner": "Kumar (founder)",
    "status": "open",
    "title": "15 of 41 standards omit a real chapter-summary section from their registry (46 "
             "sections, 14 of the 15 in class VIII) — and C5 check 11's SS matcher cannot see it",
    "evidence": "Found because six compacts were quarantined for anchoring sections the top "
                "registry lacks — every one of those anchors is a real summary heading "
                "(viii ch 8 'Ocean currents'/'Ocean trenches'/'Smaller water bodies'; ch 10 "
                "'Churches in India'/'Colonial Architecture'; ch 12 'Right to life'/'Right "
                "against exploitation'/'Right to constitutional remedies'; ch 7 'Factors of "
                "Production'/'People as a resource'). Check 11's advisory for viii ch 7 claims "
                "the summary does not name 'Introduction', 'Land (natural resources)', 'Labour "
                "(human resources)' — all three are verbatim headings — and it found 6 summary "
                "sections where there are 14, offering 'The section' and 'This section' as "
                "unmatched leads.",
    "notes": "FOUNDER RULING 2026-08-16: the top's editorial selection IS the contract; a "
             "section the top folds in is in all likelihood integrated into the lesson anyway; "
             "the only concern is jump risk from compact-top anchor misalignment. So the 46 are "
             "accepted and the compacts were aligned to the registry (teaching untouched, only "
             "the section CLAIM withdrawn). What remains open is the GATE, not the content: "
             "check 11 is the mechanism meant to catch this at W1, before money is spent on "
             "compacts cut against short registries, and on SS it is not fit to be ruled on — "
             "which is what closing-checklist item 4 requires of it. Fixing the matcher is free "
             "and should precede the next SS batch.",
})

post("campaign/defect", {
    "id": "ARV-D-166",
    "combo": KEY, "step": "F1", "severity": "S2", "owner": "Kumar (founder)",
    "status": "open",
    "title": "Two ORPHAN units — the wave's only genuine jump risk — held in quarantine for F1",
    "evidence": "viii ch 8 p08 (one unit anchored solely to 'Smaller water bodies and "
                "waterways') and viii ch 8 p11 (one unit anchored solely to 'Ocean currents / "
                "Ocean trenches'). Unlike the nine token-drop units, neither carries ANY "
                "registry anchor, so the engine cannot compute the unit's range and cannot "
                "reason about what a borrower assumes at that slot.",
    "notes": "Deliberately not repaired and not re-authored (founder ruling 2026-08-16: take "
             "the jump risk to F1). Consequence to keep visible: viii ch 8 will FAIL `library "
             "complete` on every certify run until this is ruled, and closing-checklist item 2 "
             "cannot be met meanwhile. Also at F1: viii ch 15 p14's U7 anchors [6] Gardens and "
             "[9] Vocational education jointly, pulling 9 ahead of 7 and 8 — no permutation "
             "fixes it (moving the unit just makes 6 late) and 9 is taught nowhere else in that "
             "compact, so the token cannot be dropped either. Plus the 8 artefact-dependency "
             "advisories from W1, which certification cannot gate.",
})

post("campaign/defect", {
    "id": "ARV-D-167",
    "combo": "campaign", "step": "W2", "severity": "S2", "owner": "Claude",
    "status": "fixed-awaiting-recheck",
    "title": "register_scan: a possessive apostrophe broke quote detection, so the "
             "\"calendar hit inside quotes is advisory\" rule protected almost nothing",
    "evidence": "_QUOTED treated every ' as a delimiter, so in \"residents' quality of life. "
                "Teacher asks: 'If you were appointed urban planner for your own town "
                "tomorrow…'\" it paired residents' with the prompt's opening quote. Every span "
                "shifted by one and the quoted prompt fell OUTSIDE a quoted span — reported as "
                "a hard ban hit (SS·VIII ch 14 U10). Any band using a possessive before a "
                "quoted prompt lost its protection, which is most of them.",
    "notes": "FIXED: an opening quote must now sit at a boundary (start, whitespace, : ( - —); "
             "closers are unrestricted. Verified corpus-wide in both directions — it cleared "
             "ch 14 AND exposed two hits the bug had been WRONGLY SUPPRESSING in released "
             "stages (SS·IX ch 4 U16, TWAU·V ch 10 U7), both hypotheticals, both now correctly "
             "advisory under the calendar narrowing below. Same change set: `tomorrow` and "
             "`this|next|last week|month` dropped from BAN to ADVISORY (every hit across all "
             "five stages was content — a definition of weather, a credit-timing question, an "
             "idiom, two hypotheticals; `(next|last) class` stays a ban because it names a "
             "SITTING), and the clock ban now fires only when the sentence carrying the "
             "quantity names a classroom actor, which closes ARV-D-162 without touching the "
             "Jallianwala text and without weakening the 58 real pacing hits.",
})

post("campaign/defect", {
    "id": "ARV-D-162", "combo": KEY, "step": "W2", "severity": "S3",
    "owner": "Kumar (founder)", "status": "closed",
    "title": "register_scan clock ban fires on a narrated HISTORICAL duration — repairing it "
             "would falsify the history",
    "evidence": "viii ch 9 U11: \"Brigadier-General Dyer sealed the main exit and fired "
                "approximately 1,650 rounds FOR ABOUT TEN MINUTES\" — the duration of the "
                "Jallianwala Bagh massacre, not the pacing of a classroom activity.",
    "notes": "CLOSED 2026-08-16 at the scanner, never in the text (runbook trap 4). The clock "
             "ban now requires a classroom actor in the sentence carrying the quantity. Kept "
             "deliberately crude: if a sentence mentions the class at all the ban still fires, "
             "so the gate can only release a sentence that is about somebody else entirely.",
})

post("campaign/defect", {
    "id": "ARV-D-166",
    "combo": KEY, "step": "W2", "severity": "S2", "owner": "Kumar (founder)",
    "status": "closed",
    "title": "Two orphan units in viii ch 8 — resolved by re-anchoring to the parent section, "
             "not by re-authoring",
    "evidence": "viii ch 8 p08 U3 (\"Smaller water bodies and waterways\") and p11 U3 (\"Ocean "
                "currents / Ocean trenches\") carried no registry anchor at all.",
    "notes": "CLOSED 2026-08-16, and the closing is the lesson. Claude classified both as "
             "unfixable — drop the label and the unit is unplaceable, so re-author (~₹27) or "
             "rule accepted — and sent them to F1. The founder pointed at the registry, which "
             "already carries the parent section: 'The Blue of the Blue Planet, the Oceans' / "
             "'The oceans'. Currents, trenches and smaller water bodies are that section's "
             "material, so the label is REPLACED rather than dropped. Both files then returned "
             "0 unknown anchors, 0 order-breaks, 12/12 coverage, and viii ch 8 is ALL PASS. "
             "These eleven units were always ONE fix; they had been split into two categories "
             "on the accident of whether a valid anchor happened to sit alongside the stray.",
})

post("campaign/defect", {
    "id": "ARV-D-170", "combo": KEY, "step": "F1", "severity": "S2",
    "owner": "Kumar (founder)", "status": "closed",
    "title": "viii ch 8's STANDARD carried the wrong section on seven of thirteen units — and "
             "certified ALL PASS",
    "evidence": "U7 anchored `Asia` taught the Urals/European Plain/Alps; U8 `Europe` taught "
                "the Sahara/Savannah/Nile; U11 `North America` was titled \"Australia's "
                "Deserts, the Spinifex People, and Antarctica\"; U12 `The Australian Continent` "
                "taught, by its own band text, \"the chapter's dedicated mountain-roles passage "
                "in the Asia section\". The chapter's own compacts were labelled CORRECTLY, so "
                "standard and compacts disagreed about what every unit was.",
    "notes": "CLOSED 2026-08-16. Invisible to certification by construction: the registry is "
             "DERIVED from the standard, so anchors were 'verbatim in the registry' (the one "
             "they themselves created), order held, coverage reached the end. Surfaced only "
             "when the F1 seam pack printed an anchor beside its unit's title. Re-anchored by "
             "Fable 5 against a constrained prompt (docs/testing_artefacts/"
             "PROMPT_reanchor_ss_viii_ch08.md); every `old` verified verbatim and the chain "
             "simulated on copies first. Registry 12 -> 15. THE LESSON WORTH KEEPING: three "
             "compact repairs made earlier the same day were REVERTED, because 'align the "
             "compact to the top' had been quietly compensating for a top that was wrong — "
             "that rule holds only while the top is trustworthy, and nothing deterministic "
             "tells you when it is not. Residual: p08 now covers 13/15 (its brief was built "
             "from the mislabelled registry) and C5's coverage check cannot see the gap "
             "because it too tests a frontier.",
})

F2_COMMENT = (
    "<b>SAMPLING PLAN — recorded before reading.</b> The scanner is free, so the whole stage "
    "was scanned and the SAMPLING is of the READING, by evidence rather than by chapter: "
    "<code>copyright_scan.py --book-only</code>, 8-gram shingles, runs ≥12 words, over "
    "<b>all 41 chapters × 3 canonicals</b> against each chapter's own textbook PDF.<br><br>"
    "<b>RESULT: 790,321 teacher-facing words scanned · 2,426 inside a run ≥12 · 0.31% reach · "
    "longest run 28 words · 14 of 41 chapters produce no run ≥12 at all.</b> Cleaner than "
    "english·middle (1.64%) and mathematics·middle (1.15%); the longest run is longer than "
    "either (28 vs 14 and 18). Read: 100% of the 11 runs ≥20 words, plus 15 of the 159 in the "
    "12–19 band, seed <code>social_sciences|middle|F2|2026-08-16</code> — 26 runs in full. "
    "Pack: <code>docs/testing_artefacts/F2_ss_middle_copyright_20260816.md</code>.<br><br>"
    "<b>VERDICT — PASS (founder, 2026-08-16).</b><br><br>"
    "Three things the reading should be remembered for:<br>"
    "1. <b>The long runs are institutional prose</b>, not narrative lifting — the 28-word top "
    "hit is judicial appointment procedure (\"appointed by the President of India in "
    "consultation with the Chief Justice…\"), which recurs 3× across two ch 11 files and once "
    "inside an assessment question_text. Constitutional and procedural language is where "
    "paraphrase is genuinely constrained.<br>"
    "2. <b>Class VIII carries 126 of 170 runs (74%)</b> — the THIRD time in this stage that "
    "VIII concentrated a defect, after the registry omissions (ARV-D-165) and the ch 8 "
    "mis-anchoring (ARV-D-170). Worth asking whether VIII's SUMMARIES quote the book more "
    "closely than VI/VII's, which would make it upstream of generation.<br>"
    "3. <b>SECTION NAMES ARE EXEMPT</b> (copyright_scan line 102, per NCERT_copyright_review "
    "§5): anchors are registry-verbatim by design and counted as structural references, not "
    "reproduction. So 0.31% is reach across teacher-facing PROSE, excluding headings — and "
    "every chapter does ship its section headings verbatim, ~60 words per canonical on a "
    "15-section chapter. Defensible, but the figure must not be quoted as \"0.31% of our words "
    "match the book\"."
)

post("campaign/item", {
    "scope": "batch", "key": KEY, "step": "F2",
    "patch": {"status": "pass", "by": "Claude (presented) · Kumar (ruled)",
              "comment": F2_COMMENT, "files": 41},
})

# WAIVER — the tracker's own channel for "closing-checklist §5 item 3 was met by DECISION".
post("campaign/item", {
    "scope": "batch", "key": KEY, "step": "waiver",
    "patch": {
        "comment": "Item 3 (zero register ban hits stage-wide) is met at ZERO, but the last "
                   "five hits were cleared by NARROWING THE SCANNER, not by repairing text — "
                   "runbook trap 4, and the record belongs here rather than in a passing "
                   "sentence. (a) `tomorrow` and `this|next|last week|month` dropped from BAN "
                   "to ADVISORY: measured across all five stages, every hit they produced was "
                   "CONTENT — the chapter's own definition of weather (\"rain today, sunshine "
                   "tomorrow\"), a credit-timing question, an idiom, two hypotheticals. "
                   "`(next|last) class` stays a ban: it names a SITTING, which is what the rule "
                   "is for. (b) The clock ban now requires a classroom actor in the sentence "
                   "carrying the quantity, so it no longer fires on Jallianwala Bagh's "
                   "\"fired approximately 1,650 rounds for about ten minutes\" (ARV-D-162) "
                   "while keeping all 58 real pacing hits. (c) A possessive-apostrophe bug in "
                   "quote detection was fixed in the same change (ARV-D-167), which also "
                   "EXPOSED two hits it had been wrongly suppressing in released stages. "
                   "No artefact text was altered to reach zero.",
    },
})

post("campaign/defect", {
    "id": "ARV-D-171", "combo": KEY, "step": "F2", "severity": "S3",
    "owner": "Kumar (founder)", "status": "open",
    "title": "VI ch 1 has NO textbook chapter on disk — C14 cannot be run on it, and the "
             "scanner would have passed it clean against the wrong book",
    "evidence": "textbooks/social_sciences/vi/ holds 14 numbered PDFs, but the book's "
                "\"Chapter 01\" is \"Why Social Science\" (a themes/contents page) while our "
                "ch 1 is \"Locating Places on the Earth\". Extracted and checked: that PDF "
                "mentions \"Locating Places\" twice, both in the theme map, and carries none "
                "of the chapter's text. No other VI PDF contains it. The scanner's glob "
                "resolves ch 1 -> \"Chapter 01 - Why Social Science.pdf\" and scored 0.2% "
                "overlap — a wrong book scores ~0% and reads as a clean pass, which "
                "load_source's own docstring calls \"the most expensive way for this check to "
                "fail\".",
    "notes": "EXCLUDED from the F2 pack rather than passed silently; F2's result covers 40 of "
             "41 chapters. Close the content gap (obtain the missing PDF) before the next VI "
             "batch. Worth a guard in copyright_scan.py: refuse, rather than report, when the "
             "matched PDF's title does not resemble the chapter's — the title check is what "
             "caught this, and it cost nothing.",
})

print("recorded: W1 + W2 + F1 + F2 + waiver + spend + 12 defect rows — stage RELEASED")
