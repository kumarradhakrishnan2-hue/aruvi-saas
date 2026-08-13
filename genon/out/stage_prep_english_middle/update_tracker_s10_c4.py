#!/usr/bin/env python3
"""S10 · english · middle — C4 (MEMORY.md amendment items, live) into the tracker."""
import datetime, json, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/middle"

C4 = """PASS 2026-08-13. Every applicable item from MEMORY.md's "AMENDMENTS TO BE TESTED" checked against the live ch 8 library {12, 10, 7}. Eight applicable, eight pass; nine N/A with a recorded reason. TWO ITEMS ARE MATERIALLY ADVANCED BY THIS STAGE — one of them could not be tested anywhere before now.

ITEM 2 - ENGLISH MCQ KEYED REVEALS: PASS, AND THIS IS THE CAMPAIGN'S FIRST LIVE TEST OF IT. S11 recorded the item as NOT TESTABLE at secondary for a structural reason - english IX ch 7 produced ZERO MCQ items across all three canonicals, because Rule 4 prefers EXTRACT_ANALYSIS/ECR for analytical Reading LOs - and re-assigned its owner from a stage to "the first MCQ-bearing english chapter". THAT CHAPTER IS THIS ONE: ch 8 carries an MCQ in every canonical (Q-RFC-B-1 x3, the Reading slot-1 item the PAIR table mandates). All three emit `what_each_option_reveals` keyed to EXACTLY the incorrect option labels and never the correct one (A,B,D against correct C in the standard and p10; A,C,D against correct B in p07 - the labels differ because STEP 6 re-ordered them, which is itself the check working); `suggested_answer` is empty on all three as Rule 5 requires for MCQ; `note` is empty on all three, so nothing fell back to the old prose-note shape. The generation prompt wrapper produces keyed reveals unaided. ITEM 2 IS DISCHARGED FOR ENGLISH MIDDLE; preparatory (whose type set is MCQ-heavier) is the last stage owing it.

ITEM 4 - ENGLISH SPLIT CHAPTERS REGENERATED: PASS, AND THIS IS THE HALF S10 OWED. The item's condition is that a chapter cut out of a Unit by split_english_chapters.py can be regenerated from scratch and still honour the split contract. All three canonicals do: chapter_title "What a Bird Thought (Nurturing Nature)" in the <section> (<unit>) form; main_sections_inventory a single entry {B, "What a Bird Thought", poem}; section_id "B" on all 29 units across the three files; the port's singleton-section collapse putting SPINES at the top level. NOTE THE SECTION ID IS B, NOT A - the split kept each chapter's position in its original textbook unit (ch 8 is the second section of "Nurturing Nature"), which is a live demonstration of the trap P5.2 recorded. Period spread 12 for an 8-page section, consistent with effort_index 16.5. GRADE VI IS NOW DISCHARGED; VII and VIII are owed by the pre-warm sweep and III by S9.

ITEM 3 - EXACT ITEM COUNTS: PASS. 6 section_contributions x 2 = 12 mandated, 12 emitted, on all three files. No file is over or short. This is the PAIR arithmetic (assessment v3.6) holding at every period count, which is also the corollary that the item count does not vary with the plan length.

ITEM 9 - THE JUL 12-13 CONSTITUTION WAVE: PASS, and it closes a defect the item itself recorded. The item flagged `lesson_plan/english/middle` as "header v1.5 / footer still says v1.4 - STALE FOOTER, fix it". Both now read v1.7 and match; the assessment pair both read v3.7 and match. Its named check bullets also hold: Rule 4 methods drawn STRICTLY from the per-spine NCF list with no spine's method repeating across more than two consecutive units (verified at C3 across all 29 units, zero violations); Rule 2 allocation capacity-first. The middle-specific assessment contracts hold too - TRUE_FALSE answers are one numbered line per option carrying a verdict and a justification ("1. True - the poem says ...", 4 lines / 4 options) with NO grouping of the "Statements 2, 3 and 4 are TRUE" kind the rule forbids; MATCH carries a structured answer_key of 4 {left,right} pairs plus a short fallback string, with the columns living only in visual_stimulus.

ITEM 10 - NAME THE REFERENCED WORD: PASS. Zero items anywhere in the library rely on typographic emphasis - no "underlined", "circled", "highlighted", "bold" or "italic" in any stem. The VocGram items name their target words explicitly in quotation marks ('nestled', 'blind', 'pale'), which is exactly the fix. The defect this rule was written for - english/vii/ch_01 Q-VG-A-1, "the underlined word" with no underline and an empty visual_stimulus, still sitting `verified: true` in the corpus - does not recur.

ITEM 11 - HOMEWORK (p.NN) LOCATOR: PASS. 6 homework items across the three canonicals, 100% carry a page locator in the mandated "<Subheading> (p.NN): <plain brief>" form. Worth stating against the baseline: only 13 of 123 briefs in the historical middle corpus carried one at all, so this is the mandate's first real demonstration.

ITEM 12 - FILL_IN TABLE ANTI-DUPLICATION: PASS. Two FILL_IN items in the library; both keep the table entirely in visual_stimulus with an instruction-only stem, and no pipe markup appears in any stem in any file. One item per table, no reproduction.

ITEM 13 - THE NARROWED A/B BAN: PASS BUT UNSTRESSED. No FILL_IN item splits into parts at all, so the narrowed rule ("multiple parts ONLY if every part is textual") is satisfied trivially rather than exercised. Recorded as untested rather than proven - the rule still owes a live case where a model actually wants two parts.

N/A, each with its reason: ITEM 1 (SS + TWAU only; fully CLOSED 2026-08-12). ITEM 5 (task_density tier cutoffs) - N/A HERE, and the distinction matters: this item belongs to the chapter-AUTHORING pipeline (the cowork prompt that computes effort_signals), which C1 does not run - C1 consumes the summary, it does not produce one. Recorded for whoever does own it: Grade VI's tiers distribute 5/6/5 across tiers 1/2/3 with effort_index spanning 4.5-16.5, which is a healthy non-binary signal - but VI is the grade the cutoffs were CALIBRATED on, so it cannot validate them, and VII (untested) and VIII (admittedly weak fit, pins most chapters at tier 3) remain the real question. ITEM 6 (closed by design - A1 fixes one standard row and the serve engine owns timetable variation). ITEM 7 (Period.approach - CLOSED for the whole english family at S11; the field is identical at all three stages, so S10 inherits the answer and owes nothing). ITEM 8 (english preparatory). ITEMS 14, 15, 16 (mathematics). ITEM 17 (SS middle). ITEM 18 (closed by the pipeline - STEP 6 does the ordering; C3 read its "4 of 4 re-ordered" line as the generation-quality signal instead).

ZERO FAILS, so no defect is raised by C4."""


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s10_c4"))
    state["combos"][KEY]["C4"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C4}
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"tracker updated · {KEY} · C4 pass · {NOW}")


if __name__ == "__main__":
    main()
