#!/usr/bin/env python3
"""S11 · english·preparatory — record F1 (C8 across the batch) after the founder's ruling.

    python3 genon/out/tracker_update_s11_prep_f1.py
"""
import json
from pathlib import Path

STATE = Path(__file__).resolve().parents[2] / "data" / "testing" / "campaign_state.json"
NOW = "2026-08-15T19:30:00"

F1 = """S11 · english·preparatory · 2026-08-15. <b>ZERO JUMPY across 22 borrowed seams. \
Founder ruling: accept and close.</b><br><br>
<b>ENUMERATED, NOT SAMPLED</b> — so there is no sample size to defend, per the step's own \
standing instruction. <code>borrowed_seams.py english iii iv v</code> swept every X in \
[floor−2 … top+2] at the class-standard 40 min across all 39 chapters:<br>
&nbsp;&nbsp;• <b>358 serves swept</b><br>
&nbsp;&nbsp;• <b>187</b> produced no borrow at all (identity / truncation / surrender)<br>
&nbsp;&nbsp;• <b>149 SELF-FILLS excluded</b> — the Xth slot filled from the plan being served, so \
the borrowed unit's priors are that plan's OWN earlier units. No foreign prior, nothing to read. \
This is 87% of all borrows, which is the e14 SELF-FIRST tie-break working exactly as designed.<br>
&nbsp;&nbsp;• <b>22 cross-canonical seams — every one read in FULL</b>, X−1 and X back to back as \
a teacher meets them on two consecutive days. Dump preserved at \
<code>genon/out/f1_english_preparatory_seams.txt</code> (103k chars, 1,171 lines).<br><br>
<b>RATINGS: CLEAN 12 · SERVICEABLE 10 · JUMPY 0.</b><br><br>
<b>TWO CONSTRAINTS HELD PERFECTLY.</b> (1) <b>Zero positional references</b> in all 22 borrowed \
units — not one "last unit", "next lesson", "as we saw in the previous sitting". (2) The self-guard \
clause is doing real work: ten borrowed units carry an explicit one (<i>"by name and concept rather \
than by reference to any earlier activity"</i>; <i>"no specific earlier activity needs to have \
occurred"</i>), and every unit carrying one rated CLEAN bar two.<br><br>
<b>ALL TEN SERVICEABLES ARE ONE CONSTRUCTION, and it lives in the TEACHER NOTE, not the bands:</b> \
a "this synthesis draws on…" list that opens with content strands and slides into a named \
<i>activity</i> — <i>"the food-basket sort"</i> (iii ch 13) · <i>"the Spellathon"</i> and <i>"the \
noun sorting"</i> (v ch 07) · <i>"the outdoor-play discussion"</i> (iii ch 07) · <i>"the clue-word \
writing from the park activity"</i> (iii ch 09) · <i>"the 'difficult side' writing theme explored \
earlier"</i> (v ch 09). Because it is framing copy rather than an instruction it never blocks a \
teacher — it only tells her the class did something it may not have. <b>The remedy is ONE authoring \
rule, upstream in the brief, not ten repairs: in the draws-on list, name the IDEA, never the \
TASK.</b> Carried to the next stage rather than repaired here (founder).<br><br>
<b>THE ONE CASE THAT WAS FIRST RATED JUMPY, AND WHY IT WAS DOWNGRADED — the founder's read, and \
it is the methodological point of this step.</b> iv ch 1 X=9: the served 10p plan gives U1–U8 and \
the borrowed 12p synthesis REPLACES the 10p plan's own U9, which is <i>"Craft — Creating a Symbol \
of Togetherness"</i>. The borrowed unit's note says <i>"the three strands of the chapter (poem, \
word work, <b>craft</b>)"</i> and its closing riddle answers <i>"the paper figure"</i> — so the \
text points at the very lesson the serve arithmetic removed (units 1–8 contain zero occurrences of \
paper / fold / craft / figure). Claude rated this JUMPY. <b>Founder: the PHASES do not require the \
activity to have happened</b> — corroborated on three independent checks: <code>materials</code> \
lists only <i>Textbook pp. 1–8, notebooks, blackboard</i> with no artefact (a genuine dependency \
would appear there); band 2 reads <i>"one thing they made <b>or talked about</b>"</i>, and the \
disjunction gives every class a legal path; and band 4's riddle is teacher-posed with the answers \
supplied, so a missing third answer deflates but never halts. <b>The defect is ASSERTION, not \
DEPENDENCY</b> — text stating something false for this serve, not an instruction a teacher cannot \
carry out — which is SERVICEABLE by the rubric. Worth keeping the distinction: a unit that NAMES a \
prior activity is not the same failure as one that NEEDS it, and only the second is what killed the \
earlier architectures. One nuance recorded against the eventual fix: iv ch 1 is the only case where \
the leaked list-item reached a CLASS-FACING line (the riddle clue <i>"I show togetherness when you \
unfold me"</i>), not merely the teacher's note. <b>Accepted as authored, unrepaired, founder \
2026-08-15.</b><br><br>
<b>ONE NON-JUMPINESS FINDING, ACCEPTED: a REPETITION risk no check looks for.</b> english iv ch 12 \
carries a fort-jigsaw craft in all three canonicals — 10p U9 <i>"Fact Paragraph and Fort Puzzle"</i> \
· 8p U8 <i>"Fort Jigsaw Puzzle: Make and Play"</i> · 6p U6 <i>"Fort Jigsaw Craft"</i>. At X=9 the \
10p plan borrows the 8p's jigsaw unit, so a class can meet the same craft as both its own U9 and \
the borrowed U10. Not a continuity breach and not in F1's remit — the serve is structurally correct \
— but nothing in certification tests whether a borrowed unit DUPLICATES one the prefix already \
taught. Recorded as a standing gap; accepted for this stage."""

s = json.loads(STATE.read_text())
b = s["batch"]["english/preparatory"]
b["F1"] = {"status": "pass",
           "by": "Claude (enumerated + read) · Kumar (ruled)",
           "comment": F1, "at": NOW, "files": 22}
s["updated_at"] = NOW
STATE.write_text(json.dumps(s, ensure_ascii=False, indent=1))
print(f"written -> {STATE}")
print(f"  F1 {b['F1']['status']} ({b['F1']['files']} seams read; 358 serves swept, 149 self-fills excluded)")
