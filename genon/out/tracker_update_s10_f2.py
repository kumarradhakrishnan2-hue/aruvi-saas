#!/usr/bin/env python3
"""S10 · english·middle — record F2 (C14 copyright across the batch) and its ruling.

    python3 genon/out/tracker_update_s10_f2.py
"""
import json
from pathlib import Path

STATE = Path(__file__).resolve().parents[2] / "data" / "testing" / "campaign_state.json"
NOW = "2026-08-15T17:45:00"

F2 = """S10 · classes vi/vii/viii · 2026-08-15. <b>THE RESOLVER GATE PASSED FIRST, and it was \
the thing that could have wasted the whole exercise: 46/46 chapters resolve to exactly ONE \
textbook PDF</b>, and all 46 carry <code>_source_unit.unit_chapter_number</code> — so the split \
mapping is real, not a silent fallback to the plan's own number. english·middle is the stage \
whose record originally said the resolver could find the book for NO english chapter \
(ARV-D-155); S11 fixed it and this run is middle's proof. A wrong book scores ~0% and reads as a \
clean pass, which is the most expensive way for this check to fail — so the count was verified \
BEFORE the scan, not after.<br><br>

<b>TEST 1 — verbatim reproduction. 121 canonicals · 471,898 teacher-facing words · 126 runs \
≥10 words · 1,540 matched words = 0.33%. Longest single run 24 words.</b> Against english·secondary's \
2.51% and longest-126, this stage is an order of magnitude cleaner. \
<code>copyright_scan.py --book-only</code> throughout, so the figure is against the PROTECTED \
WORK alone and never against Aruvi's own summary.<br><br>

<b>And most of the shortlist is not quotation at all.</b> Of the 31 runs ≥14 words: ~12 are \
textbook EXERCISE APPARATUS — the "24-word longest match" is fifteen separate contractions \
(<code>i'll it's don't i'm i'd he's…</code>) from a grammar drill, plus idiom lists, distance-word \
lists, verb lists, a list of Indian women's names, and fill-in sentence frames. Four are the \
textbook's own comprehension questions restated as the teacher's task; four are format templates \
(diary headers, a notice); ~11 are genuine short narrative quotations, <b>all attributed in their \
own sentence and none over 16 words</b>. The n-gram normaliser strips apostrophes and joins \
adjacent list items, which is what inflates a drill list into a "24-word run" — worth knowing \
before the next stage reads its own shortlist.<br><br>

<b>TEST 2 — third-party material: 0 URLs · 0 external-image instructions · 0 brand names</b> (the \
two brand hits were the verb "zoom in"). <b>TEST 3 — attribution: clean.</b><br><br>

<b>THE ONE FINDING — verse reproduced in MCQ OPTIONS, and it is a GAP in the poem-locator rule, \
not a breach of it.</b> <code>vi/ch_05_canonical_p09.json</code> item <code>Q-RFC-B-1</code> \
(<i>A Friend's Prayer</i>): the stem asks "Which line from the poem most clearly expresses this \
idea?" and three of four options are couplets copied verbatim — <i>"I'll try all that a friend \
can do / To make their wishes come true."</i>, <i>"Let me use my heart to see, / To realise what \
friends can be."</i>, <i>"May my friendships always be / The most important thing to me."</i> \
<b>41 words of published NCERT verse in one item, inside a canonical — the one artefact class \
that reaches the cloud, which is F2's whole concern.</b><br>
The 2026-08-12 amendment closed the STIMULUS (<code>Read lines N–M on p.PP, beginning \
"&lt;incipit&gt;"</code>, 8-word cap, lines copied into no field) and says nothing about OPTIONS. \
This item's question FORM structurally requires reproducing lines to work at all. Measured across \
the stage: <b>1 of 1,462 items</b> (231 option-bearing) — a narrow gap, not a systemic one.<br><br>

<b>RULING (founder, 2026-08-15): ACCEPT the item as authored, AND CLOSE THE GAP AT S9.</b> The \
item stands. The poem-locator rule is extended to OPTIONS at english·preparatory's P2 — where it \
is <b>free</b>, because no S9 library exists yet and its 39 chapters are unbought. No english \
stage carries a signed GATE, so §9 re-opens nothing today; done later it would cost a re-author \
per affected library. This is the same "do it while it is free" reasoning that put the original \
poem-locator amendment into all three english assessment constitutions on 2026-08-12 ahead of \
their P-preps.<br>
<b>OWED AT S9's P2, and it must not be lost: extend the poem-locator prohibition to cover \
OPTION text and any other item field that can carry a line, not just the stimulus.</b> The
"which line from the poem" question form should be re-expressed as a locator ("Which of the \
following ideas does the poem express in lines 5–6?") so the option text carries paraphrase, not \
verse.<br><br>

<b>NOT DEFECTS, ruled and recorded so they are not re-litigated.</b> \
<code>viii ch 8</code> quotes four imperative lines from <i>The Magic Brush</i> across three \
canonicals — but that unit TEACHES falling intonation on those lines, each is 3–5 words, and each \
is attributed ("the poem's own commands"). You cannot teach the intonation without saying the \
line. <code>vi ch 8</code>'s closing two-line stanza (<i>"I don't know how the world is made / \
And neither do my neighbours"</i>) is attributed as "the poem's final stanza" and was already \
cleared by that chapter's own C14 on 2026-08-13.<br><br>

Scan output: <code>genon/out/f2_english_middle/{vi,vii,viii}_N.txt</code> (46 reports)."""

s = json.loads(STATE.read_text())
s["batch"]["english/middle"]["F2"] = {
    "status": "pass", "by": "Claude (measured) · Kumar (ruling 2026-08-15)",
    "comment": F2, "at": NOW, "files": 46}
s["updated_at"] = NOW
STATE.write_text(json.dumps(s, ensure_ascii=False, indent=1))
print("F2 -> pass · 0.33% · one accepted item · the S9 amendment is owed and recorded")
