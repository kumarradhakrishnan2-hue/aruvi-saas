#!/usr/bin/env python3
"""S11 · english·preparatory — record F2 (C14 copyright across the batch) after the founder's ruling.

    python3 genon/out/tracker_update_s11_prep_f2.py
"""
import json
from pathlib import Path

STATE = Path(__file__).resolve().parents[2] / "data" / "testing" / "campaign_state.json"
NOW = "2026-08-15T20:15:00"

F2 = """S11 · english·preparatory · 2026-08-15. <b>Founder ruling: ACCEPTED, F2 CLOSED for this \
stage</b> — <i>"they are short and within inverted commas"</i>, on the same reasoning as the \
extract-analysis precedent (a full paragraph quoted word-for-word was left standing because the \
analysis would have been incomplete without it).<br><br>
<b>FIRST ENGLISH STAGE EVER MEASURED AGAINST THE CORRECT TEXTBOOKS.</b> The copyright review \
records that <code>copyright_scan.py</code> "cannot find the book for ANY English chapter" — its \
PDF resolver assumed plan chapter number == PDF number, which the split breaks, and at preparatory \
it was worse than nothing (III has 12 unit-PDFs against 17 split chapters, so the numbering spaces \
COLLIDE and split ch 11 resolved to a DIFFERENT chapter's book, scoring ~0% and reading as a clean \
pass). <b>That resolver was fixed at S9</b> via <code>_source_unit.unit_chapter_number</code>, and \
this is the first stage to run under the fix. Verified before use: III ch 11 now resolves to \
<code>chapter 07 - The Big Laddoo.pdf</code>, III ch 17 to <code>chapter 12 - Chandrayaan.pdf</code>. \
S10's english·middle figures were obtained by pointing at the PDF by hand; these were not.<br><br>
<b>TEST 1 — verbatim reproduction. 109 canonicals, 243,371 teacher-facing words, shingled n=8 \
against the 39 chapter PDFs:</b><br>
<table><tr><td></td><td><b>maths·middle</b></td><td><b>english·middle</b></td><td><b>english·prep</b></td></tr>
<tr><td>book-matched words</td><td>1.15%</td><td>1.64%</td><td><b>1.59%</b></td></tr>
<tr><td>longest run</td><td>18w</td><td>14w</td><td><b>32w</b></td></tr>
<tr><td>runs in assessment items</td><td>—</td><td>0</td><td><b>44</b></td></tr></table>
369 runs total (325 LP · 44 item), 254 distinct strings. <b>The aggregate is in line with two \
subjects that carry no F2 finding; the two outliers are the longest run and the item count.</b><br><br>
<b>TEST 2 — third-party material: CLEAN.</b> 0 URLs, 0 brand mentions, 0 external images across all \
109 files.<br><br>
<b>TEST 3 — attribution: CLEAN.</b> <b>1,126 of 1,128</b> in-class tasks carry a \
<code>(p.NN)</code>/<code>pp.</code> locator = <b>99.8%</b>.<br><br>
<b>THE POEM RULE, MEASURED BY READING — because an 8-gram scan is blind to it by construction.</b> \
Measured against each summary's own <code>poem_text</code>: <b>79 hits across 30 plans in 14 poem \
chapters</b>; worst single file <b>III ch 7 top at 8 of 11 distinct lines (73%)</b>, then IV ch 7 \
top 41%, IV ch 7 p09 35%, III ch 15 top 44%, IV ch 1 top 40%. Field split: <b>band text 60 · \
teacher_notes 19 · homework 0</b>. Full coordinates, every line quoted, at \
<code>genon/out/f2_english_preparatory_lp_poem_coordinates.txt</code>.<br><br>
<b>WHY THE ASSESSMENT CAP DID NOT COVER THIS, and it is structural rather than a model failure.</b> \
The poem cap exists in exactly ONE place — assessment Rule 3, scoped by name to four ASSESSMENT \
fields (<code>item_stem</code>, <code>visual_stimulus</code>, <code>suggested_answer</code>, rubric). \
<b>The english LP constitutions carry no equivalent rule</b> (grepped for reproduc/verbatim/copy/ \
incipit/copyright: the only hit governs <code>task_text</code>, not verse). And the LP is HANDED the \
poem — <code>poem_text</code> is a declared input and Rule 160 directs "poem → read-aloud + \
repeated/choral reading". The split in the evidence follows the split in the rules exactly: <b>101 \
poem lines in LP fields against 11 in assessment items</b> (~9:1). The 2026-08-12 poem-locator \
amendment (ARV-D-138) landed in all three english ASSESSMENT constitutions and in none of the LP \
constitutions.<br><br>
<b>WHY IT PRESENTS WORSE HERE THAN AT MIDDLE.</b> The conduit did not widen — the denominator \
shrank. Preparatory poems run 36–132 words against middle's 17 lines, so identical behaviour \
consumes a far larger fraction of the work.<br><br>
<b>THE RULING, AND WHAT IT RESTS ON.</b> Claude first reported this as a probable F2 breach and \
recommended against closing. <b>The founder read the instances and ruled otherwise, and the reading \
supports the ruling:</b> every poem-line instance is QUOTED AND FUNCTIONAL — inside inverted commas, \
naming the lines the teacher must read, chant or point to, with a maximum of <b>3 lines (~12 words) \
in any single string</b>. Representative: <i>"highlights the paired lines: 'We run and skip / We \
jump and sway / We slide and swing.' Students repeat each pair twice"</i>; <i>"the poem says 'win \
or lose, we always share' — what does sharing a loss feel like?"</i>. There is no instance of a poem \
dumped as text for its own sake. Claude's earlier hypothesis of "distributed accumulation with no \
framing purpose" was advanced BEFORE reading the strings and is withdrawn on the record.<br><br>
<b>TWO MEASUREMENT CORRECTIONS, recorded so the numbers are not over-trusted.</b> (1) The first \
ranking counted REFRAINS once per occurrence, producing impossibilities (III ch 5 read "24 of 14 \
lines") and inflating IV ch 1 to "100%". Re-run on DISTINCT lines: III ch 5 falls from worst to \
11%, IV ch 1 to 40%, corpus worst case from ~100% to 73%. (2) The 44 assessment-item runs are NOT \
poem lines — reading them shows story facts in MCQ options and riddles in <code>visual_stimulus</code> \
(<i>"thirty white horses on a red hill…"</i>, IV ch 4); poem lines in items number <b>11, across 4 \
files</b>. The constitutional firewall bent, it did not break.<br><br>
<b>ONE FINDING CARRIED FORWARD, NOT ACTED ON (founder: close, it's fine).</b> The corpus's longest \
run — <b>32 words, III ch 8 p09 U3 band[2]</b> — is the poem <i>My Top</i> reproduced ENTIRE, inline, \
labelled "transcript": <i>"teacher recites the poem 'My Top' (Textbook p. 51, transcript: 'My Top. \
Red and green, … Along with it, I jump around.')"</i>. It differs from every other instance in two \
ways worth keeping on the record even under an accept ruling: it is <b>100% of the work</b> rather \
than an extract of a longer one (proportion-of-the-whole being the usual operative test), and it \
arrives through a <b>permission the constitution grants explicitly</b> — the oracy carve-out \
licensing the generator to read <code>transcript_text</code>. Note the poem is not in \
<code>poem_text</code> at all (ch 8's section is typed prose), so this is a SECOND conduit, \
independent of the poem-line one. <b>19 of 39 preparatory chapters carry a \
<code>transcript_text</code></b>, so it recurs by design. Accepted here; the natural remedy if it \
is ever taken up is one line mirroring assessment Rule 3 — a transcript is LOCATED, never \
TRANSCRIBED.<br><br>
<b>Campaign-level note:</b> the standing F2 finding in <code>docs/NCERT_copyright_review.md</code> \
is left OPEN and unedited — this step rules on english·preparatory, not on the campaign finding, \
which the review itself routes to §4.1 (licensing) rather than to engineering."""

s = json.loads(STATE.read_text())
b = s["batch"]["english/preparatory"]
b["F2"] = {"status": "pass",
           "by": "Claude (measured + read) · Kumar (ruled)",
           "comment": F2, "at": NOW, "files": 109}
s["updated_at"] = NOW
STATE.write_text(json.dumps(s, ensure_ascii=False, indent=1))
released = all((b.get(k) or {}).get("status") in ("pass", "na") for k in ("W1", "W2", "F1", "F2"))
print(f"written -> {STATE}")
print(f"  F2 {b['F2']['status']} (109 canonicals scanned against 39 textbook PDFs)")
print(f"  english/preparatory RELEASED = {released}")
