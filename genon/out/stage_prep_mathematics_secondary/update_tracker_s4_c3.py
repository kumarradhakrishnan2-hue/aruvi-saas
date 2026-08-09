#!/usr/bin/env python3
"""S4 · C3 — rule-by-rule compliance, mathematics IX ch 4 (2026-08-09).

Writes the C3 verdict into the campaign tracker and opens the defect rows the C3 artefact
files. Artefact of record: docs/testing_artefacts/c3_mathematics_ix_ch04.md

Run from the repo root:
    python3 genon/out/stage_prep_mathematics_secondary/update_tracker_s4_c3.py
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "mathematics/secondary"
COMBO = "mathematics/secondary"

C3 = """FAIL — 2026-08-09. Files: ch_04_canonical.json (STANDARD, 15x50, 14 items) and
ch_04_canonical_p12.json (MID compact, 12x50, 13 items), each checked against every numbered
rule of LP v1.2 and assessment v1.1. Artefact: docs/testing_artefacts/c3_mathematics_ix_ch04.md
(full rule table with quoted evidence, the serve-exposure bound, and the defect list).
Method: programmatic battery over both files (band tiling, sentence/word counts, register
regexes, id leakage, guide shape, field discipline, A4 verbatim diff against the summary) +
judged reads + independent symbolic re-derivation of all 27 determinate answers.

TWO S1 DEFECTS, both in the STANDARD, both teacher-facing:

ARV-D-084 — item 4 ships a WRONG verified answer. expected_answer '8(3m - 2n)^2' expands to
72m^2-96mn+32n^2, not the stem's 72m^2-48mn+8n^2; correct is 8(3m-n)^2. And method_one_line
carries the model's own deliberation verbatim: 'Extract the common factor 8 to get
8(9m^2-12mn+n^2) - wait, verify: ... Let me re-check. ... So the answer is 8(3m-n)^2.' The model
FOUND the error and the wrong value shipped anyway with verified: true. Breaches Rule 11
(both prohibitions) and Rule 9's ban on exposing verification reasoning. 26 of 27 answers are
otherwise correct, including the three-variable ECR whose givens are mutually consistent
(e1=6, e2=11, e3=6 -> roots 1,2,3 -> sum of cubes 36).

ARV-D-081 — guides reference options by LETTER in 4 places (std #2 'option A', std #7
'option A', p12 #3 'option C', p12 #7 'option A'); STEP 6 caught exactly one (its report line
'#3 SKIPPED - cross-references an option label'), so a future re-sort would silently falsify
the other three. Worse, std #7's guide names the WRONG option as correct: the answer is C
(2a^2+2b^2+2c^2-4bc, re-derived) and the guide tells the teacher to 'confirm option A'.
Rule 7 P2 bans the construction in options[]; the falsification it prevents is being caused by
the guide, which the ban does not reach.

ELEVEN S2/S3 DEFECTS: ARV-D-069 register forward-reference in p12 notes AND homework plus
'final unit' and a 'today' in the standard, all passing register_scan; ARV-D-070 continuity by
position ('in the previous unit', p12 x4); ARV-D-071 'Problem Solving' != the Pedagogy
document's 'Problem solving' (standard only, 8 units); ARV-D-072 Rule 5 P1 (>2 consecutive
methods) breached in ALL THREE canonicals - std x4, p12 x3 twice, p09 x3; ARV-D-030 recurrence,
section_context outside 10-12 words (std 4/9, p12 2/8); ARV-D-073 31 internal E-N/WE-N ids in
the standard's bands and homework against Rule 9 P5, p12 has zero; ARV-D-074 period_numbers
still lists non-teaching units on 2 standard rows - the exact defect LP v1.2 was written for
eight days ago off this chapter, recurring in the post-v1.2 re-author; ARV-D-075 c_code C-9.3
stamped on 4.5 where the mapping ties it to 4.6 (three canonicals give three answers);
ARV-D-076 activity_title below A3's 10-13 words on 24 of 27 units; ARV-D-077 textbook item
description not verbatim (E-3 loses '(asterisked parts (v)-(vi) excluded)', the clause Rule 8
leans on); ARV-D-078 standard item 1 tests 4.3's algebraic proof while owned by 4.1 and
duplicates item 5 (p12 does this correctly); ARV-D-079 p12 item 9 tagged Analysis on an
Application LO; ARV-D-080 OPEN_TASK emitted against Evaluation/Analysis tags with
co_central false and no declared lift, and p12's format_type is off-menu in substance;
ARV-D-082 Rule 8's 'teacher may substitute any menu format' statement missing from both
OPEN_TASK guides; ARV-D-083 p12 emits all five guide sub-blocks on every item with empty
strings - 112 empty required fields against A1's explicit ban.

WHAT PASSED AND IS WORTH RECORDING: band tiling exact on all 27 units; INPUTS 4 one standard
row; zero fabricated textbook ids; full section coverage with section_coverage_note null; one
item per implied_lo (14/14, 13/13); reasoning floor met without a lift; MCQ structure and
distractor diagnosis clean; A1 field discipline clean; no period_ref on any item, so the
derived-anchor rule holds; and the synthesis handoff row works - std sec#9 ref 'synthesis',
period_numbers [15], item 14 anchors to it. That last one CLOSES the S3 defect (a mandated
synthesis unit that can carry no items on a derived-anchor stage) on this stage, second outing.

SERVE EXPOSURE OF ARV-D-074, bounded honestly: the standard's shortest served prefix is 12
units (at X=13) and its two over-long rows anchor at U9 and U12, so the breach costs NOTHING on
this library today - the remedy is a declared repair of two arrays, not a re-author. Margin is
one unit. Separately, and for C6/C9 rather than C3: the serve is NON-MONOTONE in questions -
X=12 yields 13 items, X=13 yields 11, because X=13 switches to the standard whose 4.8 row
anchors at U14. A teacher asking for one more period gets two fewer questions.

TOOLING GAPS SURFACED (for C5): register_scan misses 'will recur', 'once section N has been
taught', 'after section N is covered' and 'final unit', and classifies 'today' as advisory;
certification checks no Rule 5 P1, no id leakage, no activity_title length, no description
verbatim, no guide-shape/empty-field rule, no c_code-against-mapping consistency;
normalize_options' label-reference guard reads options[] only, not the guide. Also noted, not a
C3 item: the installed engine reports serve v2.2 / e17 while testing.md 0.2 still asserts e12.

THE FINDING TO CARRY TO THE HUMAN GATE is not any single defect. The compact is BETTER than the
standard on item ownership, id leakage, the method label, c_code and Rule 12; WORSE on the
register, guide shape and format selection. So neither 'the constitution holds at full length
and breaks under compaction' nor its opposite is true here. What the pair shows is that the
rules with no machine check behind them are satisfied at roughly coin-flip rate per file,
independent of length."""

DEFECTS = [
    ("ARV-D-084", "S1", "std item 4 ships a wrong verified answer, with the model's own "
     "'wait, verify... let me re-check' deliberation left in method_one_line beside it"),
    ("ARV-D-081", "S1", "guides reference options by letter in 4 places (STEP 6 caught 1 of 4), "
     "and std item 7's guide names the wrong option as correct"),
    ("ARV-D-069", "S2", "register: forward reference in p12 notes AND homework, 'final unit', "
     "and 'today' in the standard - all pass register_scan"),
    ("ARV-D-070", "S3", "continuity carried by position ('in the previous unit') where Rule 10 "
     "says never by position"),
    ("ARV-D-071", "S3", "'Problem Solving' != the Pedagogy document's 'Problem solving'; "
     "differs between canonicals of one chapter"),
    ("ARV-D-072", "S2", "Rule 5 P1 (no method on >2 consecutive units) breached in all three "
     "canonicals; nothing in the pipeline checks it"),
    ("ARV-D-030", "S3", "RECURRENCE: section_context outside the mandated 10-12 words "
     "(std 4/9, p12 2/8)"),
    ("ARV-D-073", "S2", "31 internal E-N/WE-N ids in the standard's band text and homework "
     "against Rule 9 P5; p12 has zero, so it is variance not inevitability"),
    ("ARV-D-074", "S2", "period_numbers still lists non-teaching units on 2 standard rows - the "
     "exact defect LP v1.2 was written for, recurring in the post-v1.2 re-author"),
    ("ARV-D-075", "S2", "c_code C-9.3 stamped on section 4.5 against a mapping that ties it to "
     "4.6; three canonicals give three answers for the same two sections"),
    ("ARV-D-076", "S3", "activity_title below A3's stated 10-13 words on 24 of 27 units - reads "
     "as a constraint the prompt never surfaces"),
    ("ARV-D-077", "S3", "textbook item description not verbatim; E-3 loses '(asterisked parts "
     "(v)-(vi) excluded)', the clause Rule 8 leans on"),
    ("ARV-D-078", "S2", "std item 1 tests 4.3's algebraic proof while owned by 4.1 and "
     "duplicates item 5; p12 does this correctly"),
    ("ARV-D-079", "S3", "p12 item 9 tagged Analysis on an Application LO - the mis-tag that "
     "licenses the wrong format"),
    ("ARV-D-080", "S2", "OPEN_TASK emitted against Evaluation/Analysis tags with co_central "
     "false and no declared lift; p12's format_type is off-menu in substance"),
    ("ARV-D-082", "S3", "Rule 8's 'teacher may substitute any other menu format' statement "
     "missing from both OPEN_TASK guides"),
    ("ARV-D-083", "S2", "p12 emits all five guide sub-blocks on every item with empty strings - "
     "112 empty required fields against A1's explicit ban"),
]

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_c3"))

state["combos"][KEY]["C3"] = {
    "status": "fail",
    "by": "Claude",
    "at": NOW,
    "comment": C3,
    "artefact": "docs/testing_artefacts/c3_mathematics_ix_ch04.md",
}

existing = {d["id"] for d in state["defects"]}
opened = []
for did, sev, title in DEFECTS:
    if did in existing:
        # ARV-D-030 is a recurrence of an SS.IX row; annotate rather than duplicate.
        for d in state["defects"]:
            if d["id"] == did:
                d.setdefault("recurrences", []).append(
                    {"combo": COMBO, "step": "C3", "at": NOW, "note": title})
                d["status"] = "open"
        continue
    state["defects"].append({
        "id": did, "combo": COMBO, "step": "C3", "severity": sev,
        "owner": "founder", "status": "open",
        "opened": NOW, "closed": None, "at": NOW,
        "title": title,
        "evidence": "See docs/testing_artefacts/c3_mathematics_ix_ch04.md — the rule table "
                    "quotes the evidence for every row and section C lists the defects.",
    })
    opened.append(did)

state["updated_at"] = NOW
STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{KEY}: C3=fail · {len(opened)} defects opened ({', '.join(opened)}) · "
      f"ARV-D-030 annotated as a recurrence · backup at {STATE.with_suffix('.json.bak_pre_c3').name}")
