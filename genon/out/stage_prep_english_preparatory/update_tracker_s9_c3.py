#!/usr/bin/env python3
"""S9 · english · preparatory — write C3 into the tracker, plus its five defect rows.

    python3 genon/out/stage_prep_english_preparatory/update_tracker_s9_c3.py

Rule table: genon/out/stage_prep_english_preparatory/C3_rule_table_english_iii_ch11.md
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/preparatory"

C3 = ("pass", "Claude", """RULE-BY-RULE READ DONE 2026-08-13 on the standard (12u) AND the FLOOR compact p07 (7u) - the floor chosen deliberately as the C3 compact because it is where FULL SPINE COVERAGE binds hardest and where a constitution that only holds at full length would show. Rule 2's slot table is swept across all THREE files (each compact authors its own assessment). Full table with quoted evidence: genon/out/stage_prep_english_preparatory/C3_rule_table_english_iii_ch11.md

MATHS SUB-CHECK: N/A - english ships expected_elements / answer_key, never expected_answer; the 2026-08-09 sweep scoped the re-derivation to S4/S7/S8.

VERDICT: 4 FAILS + 2 SUBJECTIVE FAILS, everything else passes. NO FAIL IS STRUCTURAL - registry, register, anchoring, coverage and the serve engine are all clean (C1's report). THREE OF THE FOUR POINT AT A RULE RATHER THAN AT THE PLAN, and two of those are cross-stage.

WHAT THE P-PREP'S OWN AMENDMENTS DID, LIVE.
- FULL SPINE COVERAGE (new at v1.2) HELD AT THE FLOOR: 5 of 5 cells in all three canonicals, ZERO drops at 7 periods. The stage's legacy saved plan (iii ch 1) carries 3 of 5 under the old drop licence. Pressure went to TASK level exactly as the rule intends - p07 anchors 10 of 11 summary tasks, the top 11 of 11.
- RULE 9's WHICH SUBHEADING clause did precisely the job it was added for: three of this chapter's five cells carry a MERGED section_name ('Let us think + Let us speak' etc.) and the merged string is used verbatim ZERO times in either file - briefs name the single subheading ('Let us think (p.72)', 'Let us write A (p.74)').
- RULE 1's CLOSING-UNIT EXCEPTION is used as written: u12 names all five spines with tasks_in_class empty, teaching no cell of its own. Every OTHER unit stays inside the one-or-two bound, and the single ordinary two-spine unit (u11) satisfies clause (d) exactly - one task each.
- A1: one row {40,12} / {40,7}, every unit at 40, all 19 units tiling 0..40 EXACTLY.
- A6/RULE 8A: period_ref, period_number and unit_ref emitted NOWHERE. The prohibition confirmed at P2 holds on its first live outing.
- THE PAIR: 10 items = 2 x 5 contributions in all three files, at 12, 10 and 7 units - v1.4's invariance line proved live.

FAIL 1 (cross-stage, points at the RULE) - RULE 9's NARRATION FORMAT HAS NEVER BEEN FOLLOWED BY ANY ENGLISH LIBRARY, INCLUDING A CERTIFIED ONE. The mandated shape '<spine_section_name> (“brief <= 10 words”)' appears in 1 of 49 bands (top), 1 of 34 (p07), 1 of 47 (english VI ch 8, S10) and 1 of 69 (english IX ch 7, S11, CERTIFIED) - four libraries, three stages, 199 bands, essentially zero compliance, and every hit is an incidental parenthetical rather than the format. What the model writes instead satisfies the rule's stated REQUIREMENT ('names the task by anchor location + brief') but not its stated FORMAT: 'Let us recite - teacher reads the poem aloud with full expression...'. time_bands[].activity is the NARRATIVE of the minutes; a rule demanding it be 'Let us recite (“choral echo reading”)' would empty the timed spine of content. The Format line reads like a spec for a terse label and plausibly predates the field's current role - it survived P3's rename unexamined at this stage and at both siblings. FILED, NOT REPAIRED.

FAIL 2 (points at the RULE, with the founder's call named) - THE ASSESSMENT SLOT TABLE IS BREACHED IN ONE CONSISTENT PLACE AND TWO ONE-OFFS. writing slot 1 is FILL_IN in 3 of 3 files where the table prescribes SCR; p07's beyond_text slot 1 is FILL_IN where the table permits MATCH only; p10's reading slot 2 is ORAL_PROMPT where the table prescribes SCR. THE DEMAND AXIS IS SATISFIED EVERYWHERE (recognition then production) - it is the TYPE column that is breached, and Rule 2's own demand wording includes 'completes', which is what FILL_IN is, so the table and the demand axis disagree on this cell. The writing breach is content-driven: this section's writing tasks ARE sorting and column-filling ('write round things in can eat / cannot eat columns'), so FILL_IN tests what was taught and an SCR would have to invent a different task. The two one-offs are weaker: p10's reading slot 2 as ORAL_PROMPT loses the written response the reading spine is meant to elicit.

FAIL 3 - RULE 11's <= 8-WORD RUBRIC BULLETS BENT ON FIRST CONTACT. Top: Q-ORAL-B-2 at 10 words, Q-WORD-B-2 at 9, against '3 bullets, each <= 8 words'. Bullet COUNT is 3 everywhere. Preparatory's <= 8 is the NARROWEST rubric cap in the english family (middle 3-4 / <= 10, secondary 3-5 / <= 12) and had never been exercised; it bends by 1-2 words on bullets that are not padded ('Describes at least one sense - taste, smell or texture.'). p07's six open items are all inside 8.

FAIL 4 - task_brief <= 18 BREACHED TWICE, AND BOTH ARE HOMEWORK. 20 words ('Let us think (p.72): write one sentence about what happened to the laddoo after it was thrown into the sea.') and 19 at u8. IN-CLASS briefs max at 14. A homework brief has to stand alone without the teacher's voice, which is why it runs longer - and P1's simulation that set 18 measured IN-CLASS briefs only. The cap is one word short of the evidence, and the evidence says homework wants its own number. THIS IS THE S4 LESSON LANDING ON A NUMBER SET THE SAME DAY.

SUBJECTIVE FAIL 1 - p07's Q-WORD-B-2 IS ANSWERABLE WITHOUT READING THE SECTION. 'Think about a laddoo you have seen or eaten. Say two sentences that describe it... Use words that tell us more about the laddoo.' That is Rule 3's first prohibition, and it also fails the word_work clause requiring the concept be NAMED in the stem. The top's counterpart does both: 'Think of the giant laddoo in the poem - round, sweet, and enormous. Choose TWO describing words...'. Subjective because 'grounded' is a judgement; the quoted strings are what it rests on.

SUBJECTIVE FAIL 2 (minor) - ONE TEACHER-PROSE LEAK. Top u6 teacher_notes: 'The blend words (pl-, cl-, bl-) connect to the WORD-WORK SPINE content'. 'spine' is a schema key (spines_taught, source_spine) and Rule 9 bans schema keys and planner identifiers from teacher-facing prose. One occurrence; zero in p07.

THE POEM LOCATOR PASSED, AND IT IS THE ITEM THE PILOT WAS CHOSEN FOR. p07's Q-READ-B-1 is the mandated form exactly: 'Read the stanza on page 70 beginning \"If all the laddoos were one Laddoo\". What does the poet imagine in this stanza?' - page reference, incipit in double quotes, SEVEN words against a cap of eight, no ellipsis. No poem line reaches visual_stimulus, suggested_answer or any rubric field in either file. A NUANCE WORTH CARRYING TO C14: this poem's lines run 4-9 words, so a COMPLIANT eight-word incipit can BE a whole line - a scanner looking for reproduced lines flags this item and reading clears it. That is the mirror of the copyright review's own caveat ('an 8-gram scan is blind to a compliant incipit'), and together they mean C14 ON A PREPARATORY POEM CHAPTER CANNOT BE AUTOMATED IN EITHER DIRECTION.

RULE 12 PARTIAL: total_items was NEVER EMITTED (grep -c total_items = 0 in the raw generation output). Nothing downstream reads it - the certifier counts items itself - so it costs nothing today, but a rule nothing enforces and nothing consumes should either be enforced or struck.

TWO READING NOTES FOR LATER C-STEPS. (a) Rule 6 / Rule 12 HEADERS must be audited in the LEDGER file (genon/out/canonical/), not the installed one: build_library.py's install rewraps into the app's saved-plan shape and moves header fields to the wrapper or drops them. The model emitted the full header correctly. (b) Three rules are VACUOUS PASSES at this stage and should not be read as evidence: Rule 2 STEP 2 (proportional allocation - every preparatory chapter is one main_section), Rule 3's listening bands and Rule 10's transcript_ref (this chapter's oracy tasks carry no transcript). A transcript-bearing chapter is owed at pre-warm.

A9 GOT EMPHATIC EVIDENCE AND IT BELONGS IN THE RULE TABLE TOO: across the library the correct option was authored at position B in FIVE OF FIVE MCQ/TRUE_FALSE items, and the deterministic sort scattered them to C, D, B, C, B. The model cannot produce the randomness the removed item-18 prohibition asked for.""")

DEFECTS = [
    dict(combo="campaign", step="C3", severity="S3", owner="founder", status="open",
         title="LP Rule 9's narration FORMAT has never been followed by any english library — "
               "1 of 199 bands across three stages, including a certified one",
         evidence=(
             "FOUND AT S9's C3, and swept across the family before filing.\n\n"
             "Rule 9 mandates `Format: <spine_section_name> (“brief ≤ 10 words”)`. "
             "Measured compliance:\n"
             "  english III ch 11 top  (S9, this)          49 bands  ->  1\n"
             "  english III ch 11 p07  (S9, this)          34 bands  ->  1\n"
             "  english VI  ch 8  top  (S10, mid-cycle)    47 bands  ->  1\n"
             "  english IX  ch 7  top  (S11, CERTIFIED)    69 bands  ->  1\n"
             "Four libraries, three stages, 199 bands, and every 'hit' is an incidental "
             "parenthetical rather than the format.\n\n"
             "WHAT THE MODEL DOES INSTEAD satisfies the rule's stated REQUIREMENT and not its "
             "stated FORMAT: it names the anchor inline in prose — 'Let us recite — teacher "
             "reads the poem aloud with full expression…', 'Under “Let us read,” "
             "students recite the poem aloud together…'. Every task-bearing unit of the S9 "
             "top has at least one band naming its subheading.\n\n"
             "THE EVIDENCE POINTS AT THE RULE (the S4 lesson). `time_bands[].activity` is the "
             "NARRATIVE of what happens in those minutes; a rule demanding it be `Let us recite "
             "(“choral echo reading”)` would empty the timed spine of content. The Format "
             "line reads like a spec for a terse LABEL and plausibly predates the field's current "
             "role — it survived P3's phases->time_bands rename unexamined at all three stages.\n\n"
             "NOT REPAIRED IN ANY PLAN. The decision is whether to restate Rule 9 as what it "
             "actually requires (name the anchor + a brief, inline) and drop the parenthetical "
             "Format, or to hold generation to the Format. NOTE THE §9 COST OF THE FIRST: "
             "english·secondary is CERTIFIED and english·middle is mid-cycle, so amending "
             "their Rule 9 re-opens them. Preparatory is free until its human gate is signed."
         )),
    dict(combo="english/preparatory", step="C3", severity="S2", owner="founder", status="open",
         title="Assessment Rule 2's SLOT TABLE breached 4× across the library — `writing` slot 1 "
               "is FILL_IN in 3 of 3 files where the table prescribes SCR",
         evidence=(
             "Swept across all three canonicals, since each authors its own assessment.\n\n"
             "  writing     slot 1   FILL_IN  x3 (top, p10, p07)   table: SCR\n"
             "  beyond_text slot 1   FILL_IN  (p07)                table: MATCH\n"
             "  reading     slot 2   ORAL_PROMPT (p10)             table: SCR\n\n"
             "THE DEMAND AXIS IS SATISFIED EVERYWHERE — slot 1 recognises, slot 2 produces, and "
             "no pair shares a type. It is the TYPE column that is breached.\n\n"
             "THE `writing` BREACH IS 3 OF 3 AND CONTENT-DRIVEN. This section's writing tasks ARE "
             "sorting and column-filling ('write round things in can eat / cannot eat columns'), "
             "so FILL_IN tests what was taught and an SCR would have to invent a different task. "
             "AND RULE 2 DISAGREES WITH ITSELF HERE: its DEMAND wording defines slot 1 as 'the "
             "child picks, matches, judges or COMPLETES' — which is what FILL_IN is — while the "
             "table's writing row admits SCR only.\n\n"
             "THE TWO ONE-OFFS ARE WEAKER and read as plan defects rather than rule defects: "
             "p10's `reading` slot 2 as ORAL_PROMPT loses the written response the reading spine "
             "exists to elicit, and p07's `beyond_text` FILL_IN is simply outside the set.\n\n"
             "FOUNDER'S CALL: whether `writing` slot 1 should admit FILL_IN (aligning the table "
             "with its own demand wording) or whether generation should be held to SCR. Free "
             "today — no english·preparatory human gate is signed."
         )),
    dict(combo="english/preparatory", step="C3", severity="S3", owner="founder", status="open",
         title="Two numeric caps bent on first live contact — `task_brief` ≤ 18 (breached "
               "twice, both HOMEWORK) and Rule 11's ≤ 8-word rubric bullets (twice)",
         evidence=(
             "Both caps are this stage's own, and both were first exercised by this library.\n\n"
             "`task_brief` ≤ 18 words, ADDED at P1 where the constitution had NO cap at all. "
             "Two breaches, at 20 and 19 words, AND BOTH ARE HOMEWORK BRIEFS:\n"
             "  'Let us think (p.72): write one sentence about what happened to the laddoo after "
             "it was thrown into the sea.'  (20)\n"
             "  'Let us learn (p.75–77): read the informational passage on festival foods and "
             "khichdi by different regional names as self-study.'  (19)\n"
             "IN-CLASS briefs max at 14. A homework brief has to stand alone without the "
             "teacher's voice, which is why it runs longer — and P1's simulation that produced "
             "the number 18 measured IN-CLASS briefs only (14 of 29 over 12, 0 over 16). The cap "
             "is one word short of its own evidence, and the evidence says HOMEWORK WANTS ITS OWN "
             "NUMBER. This is the S4 lesson landing on a limit set the same day.\n\n"
             "Assessment Rule 11, '3 bullets, each ≤ 8 words': top `Q-ORAL-B-2` at 10 words "
             "('Describes at least one sense — taste, smell or texture.') and `Q-WORD-B-2` at "
             "9. Bullet COUNT is 3 everywhere in both files, and p07's six open items are all "
             "inside 8. Preparatory's ≤ 8 is the NARROWEST rubric cap in the english family "
             "(middle 3–4 / ≤ 10, secondary 3–5 / ≤ 12) and had never been "
             "exercised. Neither offending bullet is padded.\n\n"
             "RECORDED TOGETHER because the decision is one decision: whether a cap the corpus "
             "misses by 1–2 words on unpadded prose is a plan defect or a number to move. "
             "Both are free to move now. For the record, the third cap this P-prep touched — "
             "`activity_title` 10 -> 12 — was NOT needed: this library's longest is 10."
         )),
    dict(combo="english/preparatory", step="C3", severity="S2", owner="founder", status="open",
         title="p07 `Q-WORD-B-2` is answerable without reading the section, and does not name its "
               "word_work concept (assessment Rule 3)",
         evidence=(
             "A single-item plan defect, in the FLOOR compact only.\n\n"
             "  'Think about a laddoo you have seen or eaten. Say two sentences that describe it "
             "— what it looks like, how it feels, or how it tastes. Use words that tell us "
             "more about the laddoo.'\n\n"
             "Rule 3's first prohibition is 'stems answerable without reading the section', and "
             "this one is: a child who has never opened the book can answer it. Rule 3 also "
             "requires that a word_work item NAME its concept explicitly in the stem "
             "('describing words', 'action words', \"consonant blend 'gr'\"); this gestures at it "
             "('words that tell us more') without naming it.\n\n"
             "THE TOP'S COUNTERPART DOES BOTH, which is what makes this a plan defect rather than "
             "a rule defect: 'Think of the giant laddoo in the poem — round, sweet, and "
             "enormous. Choose TWO DESCRIBING WORDS of your own for the laddoo and use each one in "
             "a short sentence.'\n\n"
             "Subjective — 'grounded' is a judgement, and the quoted strings are what the "
             "judgement rests on. Repairable in place; does not touch the registry, the anchoring "
             "or the serve."
         )),
    dict(combo="english/preparatory", step="C3", severity="S4", owner="founder", status="open",
         title="Assessment Rule 12's `total_items` is never emitted, and nothing consumes it",
         evidence=(
             "`grep -c total_items` on the raw generation output = 0. The rest of Rule 12's "
             "header IS emitted correctly (chapter_number, chapter_title, stage, grade, "
             "main_sections_inventory).\n\n"
             "Nothing downstream reads it — the certifier counts items itself — so it costs "
             "nothing today. Filed because a rule that nothing enforces and nothing consumes "
             "should either be enforced or struck, and this is the first time anyone has looked "
             "at it. Likely true at the sibling english stages too; not swept.\n\n"
             "RELATED READING NOTE, filed here so it is not rediscovered: Rule 6 / Rule 12 "
             "headers must be audited in the LEDGER file (`genon/out/canonical/`), NOT the "
             "installed saved plan. `build_library.py`'s install rewraps into the app's "
             "saved-plan shape and moves header fields onto the wrapper or drops them, so an "
             "auditor reading `result` concludes the header is missing when the model emitted it "
             "in full."
         )),
]


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s9_c3"))

    status, by, comment = C3
    # C-steps live under `combos`, not `stages` — see fix_s9_c_steps_scope.py.
    state.setdefault("combos", {}).setdefault(KEY, {})["C3"] = {
        "status": status, "by": by, "at": NOW, "comment": comment}

    defects = state.setdefault("defects", [])
    nums = [int(d["id"].rsplit("-", 1)[1]) for d in defects
            if isinstance(d.get("id"), str) and d["id"].startswith("ARV-D-")
            and d["id"].rsplit("-", 1)[1].isdigit()]
    nxt = (max(nums) if nums else 0) + 1
    added = []
    for d in DEFECTS:
        d = dict(d, id=f"ARV-D-{nxt:03d}", raised_at=NOW)
        defects.append(d)
        added.append(f"{d['id']} {d['severity']}")
        nxt += 1

    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"tracker updated · {KEY} · C3 · {NOW}")
    print(f"defects added   · {', '.join(added)}")


if __name__ == "__main__":
    main()
