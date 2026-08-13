#!/usr/bin/env python3
"""S10 · english · middle — the three defects the TOP canonical's inspection raised.

Founder ruling 2026-08-13, taken BEFORE the compacts were bought (the cheap moment to
decide, since amending re-opens whatever exists): ALL THREE ACCEPTED AS DEFECT ROWS, no
constitution moved, compacts bought under the same pair. So the library stays whole under
LP v1.7 · assessment v3.7 and §9 does not fire.

Run from the repo root:
    python3 genon/out/stage_prep_english_middle/raise_s10_c3_defects.py
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
TODAY = NOW[:10]
COMBO = "english/middle"

DEFECTS = [
    {
        "id": "ARV-D-139",
        "combo": COMBO,
        "step": "C3",
        "severity": "S3",
        "owner": "founder",
        "status": "open",
        "title": ("assessment Rule 11's `expected_elements` cap — \"3–4 bullets, each ≤ 10 "
                  "words\" — has never once been satisfiable, and the whole corpus proves it"),
        "evidence": (
            "Found by inspecting the ch 8 TOP canonical before its compacts were bought. "
            "ALL SIX open items breach the rule: bullets per item are 4 or 5 (never 3, and "
            "five is outside the 3–4 range), and 13 of 25 bullets exceed 10 words, max 15 "
            "(\"Gives a reason for each material's advantage over straw — strength, weather "
            "resistance, fire safety\", Q-BT-B-1).\n\n"
            "THE CORPUS SETTLES WHETHER THIS IS THE PLAN OR THE RULE, and it is the rule. "
            "Across the 23 open items in the existing english VI/VII/VIII saved plans — all "
            "authored long before this campaign — 47 of 95 bullets breach ≤10 (median well "
            "over), the maximum is 18, and NO ITEM ANYWHERE HAS EVER CARRIED 3 BULLETS. Two "
            "independent generations, years apart, agree the rule cannot be met. This is the "
            "S4 pattern exactly: a limit stated as a number is the kind of rule live "
            "generation most often disproves, and testing.md's P1 note says to read the "
            "numeric limits with that in mind.\n\n"
            "MEASURED CAPS, for whenever this is settled: on the live run, ≤11 leaves 5/25 "
            "over, ≤12 leaves 2/25, ≤13 leaves 1/25, ≤15 clears all. On the corpus, ≤12 "
            "leaves 21/95 and ≤15 leaves 2/95. english·SECONDARY permits 3–5 bullets at ≤12 "
            "words — structurally right on the count, still short on the words — and S11's "
            "sign-off recorded ITS Rule 11 as untested by live generation too, so the family "
            "is unproven at both stages and a fix should move both together.\n\n"
            "FLAGGED AT P-PREP, BEFORE IT HAPPENED: the S10 sign-off §8 named this exact "
            "field as one of four numeric limits to read at C3, calling it \"narrower than "
            "secondary's 3–5 / ≤12 and never exercised by live generation\". The prediction "
            "is part of the evidence — the rule was suspect on inspection and is now "
            "disproved on output.\n\n"
            "FOUNDER RULING " + TODAY + ": ACCEPTED, not amended. The window was the cheap "
            "one — only the top existed, so amending would have cost a single ~₹40 re-author "
            "against three at C3 — and the call was still to proceed, because the rule "
            "governs a teacher-facing rubric whose bullets read well at 11–15 words, and "
            "because a cap that should probably move at TWO stages ought not be set from one "
            "chapter's evidence. Revisit with english·secondary's Rule 11 when S9 or a "
            "re-read of S11 puts a second stage's live output beside this one."
        ),
        "opened": TODAY,
        "closed": "",
        "at": NOW,
    },
    {
        "id": "ARV-D-140",
        "combo": COMBO,
        "step": "C3",
        "severity": "S4",
        "owner": "founder",
        "status": "open",
        "title": ("LP register ban 3 (calendar time) breached once in the ch 8 top — a band "
                  "says \"from today's extracts\""),
        "evidence": (
            "Unit 3's closing band: \"Teacher draws a quick two-column table on the board — "
            "'What the bird saw' and 'What it thought' — and invites two or three students to "
            "contribute one row each from today's extracts.\"\n\n"
            "\"today\" is named in terms by the SELF-CONTAINED REGISTER's third ban, landed at "
            "LP v1.7 this morning: Aruvi keeps no calendar and sittings do not map to days, so "
            "today / yesterday / this week / next class are unknowable at authoring. The fix "
            "is one word — \"these extracts\" or \"the two extracts\" — and the sentence loses "
            "nothing.\n\n"
            "SCOPE: ONE hit in 47 bands and 12 teacher_notes across the whole canonical. Bans "
            "1 (clock quantity) and 2 (forward reference / completion) are CLEAN — zero hits, "
            "which is the harder half and includes the closing synthesis unit, where a "
            "completion claim would have been the natural thing to write. The register scan "
            "at certification is a MACHINE GATE (`genon/register_scan.py`, template 2.2), so "
            "this will surface again there rather than being lost.\n\n"
            "FOUNDER RULING " + TODAY + ": ACCEPTED, and NOT hand-repaired. testing.md warns "
            "against hand-editing an installed artefact outside `repair_register.py`; a "
            "one-word edit made by hand puts the file out of step with what the model "
            "authored, for a breach that costs a teacher nothing."
        ),
        "opened": TODAY,
        "closed": "",
        "at": NOW,
    },
    {
        "id": "ARV-D-141",
        "combo": COMBO,
        "step": "C3",
        "severity": "S4",
        "owner": "founder",
        "status": "open",
        "title": "one `task_brief` of 18 runs to 19 words against LP v1.7's ≤ 18 cap",
        "evidence": (
            "Unit 8: \"Let us write (p.91): five sentences each on how the world looks to a "
            "baby and to a fish.\" — 19 words including the Rule 9 locator, against the ≤ 18 "
            "the cap was raised to this morning.\n\n"
            "CONTEXT THAT MAKES THIS A NEAR-MISS RATHER THAN A MISS: the cap was ≤ 12 until "
            "today, and P1 raised it to 18 on a measurement of the historical corpus "
            "(simulating the mandated locator put 44 of 123 briefs over 12 and 0 over 16). "
            "The live run lands 17 of 18 briefs inside 18 and ALL 18 carry the page locator "
            "Rule 9 mandates — which is the thing that was actually being tested, since only "
            "13 of 123 corpus briefs carried one at all. The new number is very nearly right "
            "and the locator mandate is fully honoured.\n\n"
            "FOUNDER RULING " + TODAY + ": ACCEPTED. Re-read at C3 across all three canonicals "
            "— if the compacts also land one or two at 19, the honest fix is 20, not a "
            "re-author. `activity_title` (≤ 12, corpus max 11) and `section_context` (10–18) "
            "are both CLEAN on this file: 0 of 12 and 0 of 6 outside range."
        ),
        "opened": TODAY,
        "closed": "",
        "at": NOW,
    },
    {
        "id": "ARV-D-142",
        "combo": "campaign",
        "step": "C6",
        "severity": "S2",
        "owner": "founder",
        "status": "closed",
        "title": ("PrepareLesson suggested MORE periods than the chapter's top canonical holds — "
                  "a per-chapter Math.round where the rest of the product apportions "
                  "(40 of 340 chapters, 5 subjects)"),
        "evidence": (
            "FOUND BY THE FOUNDER on the ch 8 top canonical: the library is authored at 12 "
            "periods and the Prepare Lesson screen was offering 13.\n\n"
            "TWO ROUNDING METHODS OVER THE SAME THREE NUMBERS. `genon/master_plan.py` computes "
            "`recommended_periods` by LARGEST REMAINDER, so a class's chapters sum to exactly "
            "its annual budget; `YearPlan.jsx` does the same client-side. "
            "`PrepareLesson.jsx::suggestionFor` instead re-derived its own figure as "
            "`Math.round(weight_c / Σweights × budget)`, independently per chapter. English VI "
            "ch 8: 16.5 / 182.5 × 140 = 12.658 → 13, where the master plan says 12 — eleven "
            "chapters were entitled to the +1 and ch 8's .658 remainder came twelfth. The "
            "screen's column summed to 142 against a 140 budget.\n\n"
            "WHY IT IS S2 AND NOT COSMETIC: 13 > the 12-period TOP canonical, so a teacher "
            "accepting the default asked for more periods than the library holds and was served "
            "the serve engine's ABOVE-THE-TOP SURRENDER path — a surrendered plan, by default, "
            "on the pilot chapter of the stage being certified. Two screens also contradicted "
            "each other for the same teacher on the same chapter: YearPlan said 12, Prepare "
            "Lesson said 13.\n\n"
            "SCOPE, measured across every master-plan combo: 39 of 323 non-placeholder chapters "
            "(12.1%) were offered a default different from the count their canonicals are "
            "authored at — english|V 4/10, mathematics|V 4/15, english|VIII 3/15, "
            "mathematics|VIII 3/14, science|IX 3/13, social_sciences|VII 3/12, "
            "social_sciences|IX 3/18. Not an english defect.\n\n"
            "FIX (" + TODAY + "): `largestRemainder` moved out of YearPlan.jsx into "
            "`web/app/lib/format.js` as the single exported method, with the reasoning in its "
            "docstring; both screens import it. PrepareLesson now apportions the teacher's own "
            "budget across the chapter list in one `useMemo` and reads its suggestion out of "
            "that map. The design intent is preserved — the suggestion still keys off HER budget, "
            "never NCF and never the master plan's — and when her budget equals the calibrated "
            "one the result reproduces `recommended_periods` exactly. This screen FILTERS OUT the "
            "master plan's placeholder ('Book awaited') rows, so the apportionment appends one "
            "synthetic bucket carrying the syllabus weight they hold and discards it, which keeps "
            "the founder's 2026-07-25 rule (divide by the FULL syllabus, never the listed subset) "
            "without a second denominator.\n\n"
            "MEASURED AFTER: disagreements with the authored count fall from 39/323 to 3/323 "
            "(0.9%), and english|VI ch 8 returns 12 with the column summing to exactly 140. The "
            "three residuals are all in the two combos that HAVE placeholder rows — "
            "mathematics|IX ch 6 (14 vs 15) and social_sciences|IX ch 3 and ch 5 (13 vs 12, "
            "22 vs 21) — where 79.5 and 108.0 units of syllabus weight are hidden behind "
            "unpublished books and the synthetic bucket can only approximate their share. That "
            "is inherent to suggesting from a partial book list and resolves itself as the "
            "content lands; it is not the rounding defect.\n\n"
            "STATIC VERIFICATION ONLY (§11 — the sandbox cannot run `next dev`): all three files "
            "babel-parse clean, the local copy is gone from YearPlan, both components import the "
            "shared helper, and the old expression is absent. A live check at C6 is owed.\n\n"
            "ONE THING SEEN AND NOT FIXED: `api/main.py` computes `ncf_estimated_periods` with "
            "the same non-conserving `round(w / syllabus_total_weight * ncf_total)`. It is left "
            "alone deliberately — that field is a published-norm reference shown beside ours and "
            "'drives nothing' (testing.md, 2026-07-26). Worth a look if it is ever promoted."
        ),
        "opened": TODAY,
        "closed": TODAY,
        "at": NOW,
    },
]


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s10_defects"))
    reg = state.setdefault("defects", [])
    have = {d.get("id") for d in reg}
    for d in DEFECTS:
        if d["id"] in have:
            print(f"  SKIP {d['id']} — already in the register")
            continue
        reg.append(d)
        print(f"  + {d['id']}  {d['severity']}  {d['title'][:74]}…")
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\ndefect register: {len(reg)} rows · {NOW}")


if __name__ == "__main__":
    main()
