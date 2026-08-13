#!/usr/bin/env python3
"""S9 · english · preparatory — write C4 into the tracker, plus its three defect rows.

    python3 genon/out/stage_prep_english_preparatory/update_tracker_s9_c4.py

Item table: genon/out/stage_prep_english_preparatory/C4_memory_items_english_iii_ch11.md

NOTE THE SCOPE: C-steps live under `combos`, NOT `stages` — the tracker renders the C-cycle
matrix from cellHtml("combos", comboKey(c), ...) while the P-steps come from
cellHtml("stages", ...). The two keys are the same string, so writing a C-step to `stages`
yields a state file that looks right and renders nothing (fixed for C1-C3 by
fix_s9_c_steps_scope.py).
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/preparatory"

C4 = ("pass", "Claude", """MEMORY.md AMENDMENT ITEMS READ LIVE 2026-08-13, across ALL THREE canonicals (12/10/7) rather than the C3 pair, because several items are per-file contracts and each compact authors its own assessment. Full table: genon/out/stage_prep_english_preparatory/C4_memory_items_english_iii_ch11.md

VERDICT: 8 PASS, 2 FAIL, 7 N/A, 2 already closed. Two of the fails were already visible from C3 and are recorded here against the item they actually belong to; ONE IS NEW - and it is this stage's own item, never exercised by anything before today.

PASSES WORTH NAMING.
- ITEM 4 (split chapters) - GRADE III WAS OWED BY S9 AND IS NOW CONFIRMED. Title 'The Big Laddoo (The Big Laddoo)' in the <section> (<unit>) form; main_sections_inventory a single {B, 'The Big Laddoo', poem}; section_id 'B' on ALL 29 UNITS across the three files; the singleton-section collapse putting SPINES at the top of coverage_handoff; period spread 12 for an 8-page section, consistent with effort_index 11.5. B NOT A - the second stage to confirm S10's trap (III is fully split, 17 chapters, ids running A/B across a Unit's chapters, five of seventeen being B). GRADES VII AND VIII REMAIN OWED - both are true multi-section classes, which neither IX nor VI nor III exercises.
- ITEM 2 (MCQ keyed reveals) - all 5 MCQ/TRUE_FALSE items carry what_each_option_reveals as a dict keyed to EXACTLY the incorrect labels, correct one omitted, note='' and suggested_answer='' throughout. The item's standing worry was that mirroring the rewrite into the GENERATION PROMPT WRAPPERS was 'explicitly still deferred'; the prompt now produces the keyed shape unaided, so the deferred mirror is no longer owed for this stage.
- ITEM 11 (homework locator) - all 4 homework briefs across the three files carry a locator, and since NO task in this chapter carries a page_ref, all four exercise the SECTION-RANGE FALLBACK the rule specifies. That is the exact path the item asks to confirm, confirmed rather than inferred. Zero locator-less homework briefs.
- ITEM 12 (FILL_IN table anti-duplication) - ZERO pipe characters in any item_stem across all three files; every table lives entirely in visual_stimulus; one table per item; stems instruction-only.
- ITEM 3 (exact counts) - 5 contributions -> 10 items in all three. AND THE SS-SECONDARY PARALLEL HOLDS EXACTLY: its C4 found 'counting is solved... slot-type resolution is a separate deterministic pre-step the model does not run', and C3 here found the same split - counts perfect, SLOT TABLE breached 4x (ARV-D-146). Counting is solved at english too; slotting is not.
- ITEM 22 (poem locator) - preparatory's half confirmed on its first poem chapter: no poem line in item_stem, visual_stimulus, suggested_answer or any rubric field in any of the three files; the one locator-bearing item carries a SEVEN-word incipit against a cap of eight; no ellipsis.
- ITEM 9 (Jul 12-13 wave, the assessment/english/preparatory v1.0 bullet) - all four check-bullets pass live. The Rule-7 FAILED-ITEM path is the one exception and is NOT exercised: no verification failure occurred, so item_stem:'' emission is still untested.
- ITEM 7 (Period.approach) - N/A by scope (maths prep + SS) but checked anyway because english is a joiner stage: pedagogical_methods is populated on every unit of every file with keys equal to spines_taught, so the port's join has something to read on all 29 units. No empties.

FAIL 1 - ITEM 8's FILL_IN HALF, AND THIS ITEM HAD NEVER BEEN TESTED BY ANYTHING. MEMORY records that there was 'in fact NO English-prep saved-plan corpus on disk to have even back-checked it against'. THE MATCH HALF PASSES CLEANLY, 5 of 5: structured answer_key [{left,right}] of 4-6 pairs PLUS the short fallback string ('1-Hen, 2-Lioness, 3-Peahen, 4-Cow, 5-Duck.'), pipe-table entirely in visual_stimulus, instruction-only stem, never a prose paragraph or inline-glossed pairs. THE FILL_IN HALF FAILS on the answer shape: the rule says suggested_answer must be 'each blank's answer NUMBERED TO ITS BLANK', and all four FILL_INs emit column-grouped or object-keyed prose instead ('That can be eaten: Apple, Orange, Grape. That cannot be eaten: Football, Globe, Coin.'). THERE IS NOTHING TO NUMBER, BECAUSE THESE ARE NOT CLOZE ITEMS - they are a two-column sorting table and a predict-and-record grid. IT TRACES TO THE SAME ROOT AS ARV-D-146: FILL_IN was chosen for writing slot 1 in 3 of 3 files (where the slot table says SCR) because the content IS a sort, and the type choice then drags in an answer contract the content cannot satisfy. ONE DECISION, TWO RULE BREACHES - whatever is decided about ARV-D-146 decides this too.

FAIL 2 - ITEM 19's CURLY-QUOTE FORMAT, AND THE ITEM'S OWN ESCALATION CLAUSE FIRES. Curly marks emitted: 0/0/0 in this library's three files, 21 at english VI (S10), 0 at english IX (S11). Straight DOUBLE quotes: 0 everywhere. The model wrote 111/168/71 straight SINGLE quotes instead. SO THE AMENDMENT'S PURPOSE IS FULLY MET - the JSON escape hazard that cost maths III ch 5 Rs 40.72 cannot occur in any english library - AND ITS FORMAT IS NOT, at two of the three english stages. Item 19 states its own escalation in terms: 'If it comes back with straight quotes anyway, the Format line is not where the model is taking its cue and the amendment needs RE-SITING, not re-wording.' It came back with straight quotes. The operative cue is 'do not put a double quote inside a JSON string', which the model obeys perfectly - not 'use U+201C'.

AND ITEMS 18 AND 19 ARE THE SAME FINDING AT THE SAME SITE, FROM OPPOSITE DIRECTIONS. C3's ARV-D-145 found Rule 9's NARRATION FORMAT followed by 1 of 199 bands across three stages; item 19 finds Rule 9's QUOTATION MARK ignored at two of three stages. The curly marks and the parenthetical shape are THE SAME TWO LINES OF THE SAME RULE. Two independent measurements now say Rule 9's Format block is not load-bearing on generation, and anything it is relied on to guarantee should be re-sited into a line the model does read.

ITEM 18 (MCQ position) - CLOSED BY THE PIPELINE, and this library is the sharpest evidence in the campaign: the correct option was authored at position B in FIVE OF FIVE MCQ/TRUE_FALSE items and STEP 6 scattered them to C, D, B, C, B. The original item was written because SS and Science clustered on one letter per chapter, and english was dismissed then as having 'too few MCQs per chapter to judge'; five of five is a small sample but a perfect one, and it says the clustering is not subject-specific - it is what the model does. NOTE THE RECORDED CLOSURE IN MEMORY.md IS A VERSION STALE: it describes A9 as a CONVENTION ('arrange alphabetically, never led with'), which was struck at assessment v1.7 on 2026-08-03 when ordering became normalize_options.py STEP 6. The closure holds; its stated mechanism does not.

ITEM 6 - CLOSED BY DESIGN, already recorded at SS-secondary's C4. This library is the ordinary case: one {40,12} row, X=5 to 14 all served from it.

ITEM 23 (THE PAIR) - PASSES EVERY CLAUSE EXCEPT THE SLOT TABLE, across 15 pairs: exactly 2 per contribution 15/15; slot 1 before slot 2 with no interleaving (the platform's dispersion depends on it); types differ 15/15; same source_lo and source_context 15/15; the pair takes DIFFERENT strands of a compound implied_lo (clean on word_work - 'identifies describing words AND matches male-female animal pairs' split MATCH->pairs, ORAL_PROMPT->describing words; weaker on reading, where both slots lean structure); and the preparatory LIGHTNESS clause holds - zero double-WRITING_TASK pairs, slot 2 is ORAL_PROMPT in 11 of 15. LIVE DENSITY: 10 items / 12 units = 0.83 at the top and 10/7 = 1.43 at the floor, against the 0.35 that caused the amendment and above TWAU's 1.0.

TWO ITEMS REMAIN OWED ELSEWHERE and are recorded so they are not mistaken for done: item 4's GRADES VII AND VIII (the true multi-section classes, exercised by no stage yet) and item 13's NARROWING (no multi-part textual FILL_IN was produced here, so the narrowed A/B rule is satisfied only vacuously).""")

DEFECTS = [
    dict(combo="english/preparatory", step="C4", severity="S3", owner="founder", status="open",
         title="p10's homework item carries only `task_brief` — no `spine`, no `task_index`, "
               "so it cannot be traced to a summary task",
         evidence=(
             "FOUND AT C4, which reads all three canonicals; C3 read the top and p07 and did "
             "not see it.\n\n"
             "`ch_11_canonical_p10.json` u6 homework: keys are `['task_brief']` alone. The LP "
             "schema says `\"homework\": [ <same shape as tasks_in_class entry> ]`, i.e. "
             "`{spine, task_index, task_brief}`. The other three homework items in the library "
             "(top u5, top u8, p07 u4) all carry the full triple.\n\n"
             "NOTHING BREAKS TODAY: `tasks_anchored[]` is LP-audit-only and the assessment "
             "generator does not read homework, so no downstream consumer misses the keys. What "
             "is lost is the traceability the pair exists for — a homework item with no "
             "`{spine, task_index}` cannot be resolved back to the summary task it came from, "
             "which is the difference between a homework line and a homework REFERENCE.\n\n"
             "Its locator is present and correct (`(p.74)`), so item 11 is unaffected. "
             "Repairable in place; one item, one file."
         )),
    dict(combo="english/preparatory", step="C4", severity="S3", owner="founder", status="open",
         title="MEMORY item 8's FILL_IN answer contract ('numbered to its blank') is "
               "unsatisfiable on this content — 4 of 4 — and it traces to ARV-D-146",
         evidence=(
             "MEMORY item 8 is english·PREPARATORY's own item, on the checklist since "
             "2026-07-13 with the note that there was 'in fact NO English-prep saved-plan "
             "corpus on disk to have even back-checked it against'. This is its first test "
             "ever.\n\n"
             "THE MATCH HALF PASSES CLEANLY, 5 of 5 — structured `answer_key: [{left, right}]` "
             "of 4–6 pairs plus the short fallback string, table entirely in `visual_stimulus`, "
             "instruction-only stem.\n\n"
             "THE FILL_IN HALF FAILS. The rule: `teacher_guide.suggested_answer` = 'each blank's "
             "answer NUMBERED TO ITS BLANK'. All four FILL_INs emit column-grouped or "
             "object-keyed prose instead:\n"
             "  'That can be eaten: Apple, Orange, Grape. That cannot be eaten: Football, "
             "Globe, Coin.'\n"
             "  'Typical results: paper — float (initially), stone — sink, leaf — float, …'\n\n"
             "THERE IS NOTHING TO NUMBER, BECAUSE THESE ARE NOT CLOZE ITEMS — they are a "
             "two-column sorting table and a predict-and-record grid. The rule presumes a "
             "numbered cloze; the content has none.\n\n"
             "SAME ROOT AS ARV-D-146. FILL_IN was chosen for `writing` slot 1 in 3 of 3 files "
             "(the slot table prescribes SCR) because this section's writing tasks ARE sorting "
             "and column-filling. The type choice then drags in FILL_IN's own answer contract, "
             "which the content cannot satisfy either. ONE DECISION, TWO RULE BREACHES: if "
             "`writing` slot 1 legitimately admits FILL_IN for sorting content, item 8 needs a "
             "SECOND permitted answer shape for non-cloze FILL_INs. Decide them together.\n\n"
             "ADJACENT, NOT A BREACH, but recorded because the two files disagree: the top puts "
             "the word box in `item_stem` while p07 puts it inside `visual_stimulus`. Item 12's "
             "rule governs THE TABLE and neither file reproduces a table in a stem, so nothing "
             "is violated — but p07's is the better artefact, and it also gives real blank rows "
             "where the top gives a single '(write words here)' placeholder."
         )),
    dict(combo="campaign", step="C4", severity="S3", owner="founder", status="open",
         title="MEMORY item 19's curly-quote format is not emitted at 2 of 3 english stages — "
               "the item's own 're-site, don't re-word' escalation fires",
         evidence=(
             "MEASURED ACROSS THE ENGLISH FAMILY:\n"
             "  english III ch 11 (S9, this)   curly 0 / 0 / 0   straight-double 0 / 0 / 0\n"
             "  english VI  ch 8  (S10)        curly 21          straight-double 0\n"
             "  english IX  ch 7  (S11)        curly 0           straight-double 0\n"
             "The model wrote 111 / 168 / 71 straight SINGLE quotes in the three S9 files "
             "instead.\n\n"
             "THE AMENDMENT'S PURPOSE IS FULLY MET AND ITS FORMAT IS NOT. Zero straight DOUBLE "
             "quotes in any english library means the JSON escape hazard — the one that cost "
             "maths III ch 5 ₹40.72 and forced a hand recovery — cannot occur. But the mandated "
             "mark (U+201C/U+201D) is emitted at only one of the three stages.\n\n"
             "ITEM 19 WROTE ITS OWN VERDICT IN ADVANCE: 'If it comes back with straight quotes "
             "anyway, the Format line is not where the model is taking its cue and the "
             "amendment needs RE-SITING, not re-wording.' It came back with straight quotes. "
             "The operative cue is 'do not put a double quote inside a JSON string', which the "
             "model obeys perfectly — not 'use the curly mark shown'.\n\n"
             "MERGE-WORTHY WITH ARV-D-145, AND THAT IS THE POINT. ARV-D-145 found Rule 9's "
             "NARRATION FORMAT followed by 1 of 199 bands across three stages; this finds "
             "Rule 9's QUOTATION MARK ignored at two of three. They are THE SAME TWO LINES OF "
             "THE SAME RULE, measured independently. The conclusion is one conclusion: Rule 9's "
             "Format block is not load-bearing on generation, and anything relied on to be "
             "guaranteed by it should be re-sited into a line the model demonstrably reads.\n\n"
             "NO §9 COST TO FIXING THE PREP COPY (no signed gate); english·middle and "
             "·secondary are the expensive ones, as with ARV-D-145."
         )),
]


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s9_c4"))

    status, by, comment = C4
    state.setdefault("combos", {}).setdefault(KEY, {})["C4"] = {
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
    print(f"tracker updated · combos[{KEY!r}] · C4 · {NOW}")
    print(f"defects added   · {', '.join(added)}")


if __name__ == "__main__":
    main()
