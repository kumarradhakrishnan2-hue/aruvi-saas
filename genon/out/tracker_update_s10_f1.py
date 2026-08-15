#!/usr/bin/env python3
"""S10 · english·middle — record F1 (C8 across the batch: the borrowed X−1→X seams).

    python3 genon/out/tracker_update_s10_f1.py
"""
import json
from pathlib import Path

STATE = Path(__file__).resolve().parents[2] / "data" / "testing" / "campaign_state.json"
NOW = "2026-08-15T17:05:00"

F1 = """S10 · classes vi/vii/viii · 2026-08-15. <b>ENUMERATED, NOT SAMPLED.</b> \
<code>borrowed_seams.py</code> swept all 46 chapters over X in [floor−2, top+2]; self-fills are \
excluded by definition (the serving plan's own priors, nothing foreign to read), leaving \
<b>44 cross-canonical borrowed seams</b> — vi 9 · vii 15 · viii 20. The largest F1 in the \
campaign (S11 read 21, S5 read 30) and still a FULL read, so there is no sample and no rate to \
defend.<br><br>

<b>METHOD, stated because it differs from earlier stages.</b> Dossiers were built by RE-SERVING \
each seam (<code>genon/out/f1_seam_dossiers.py</code>) rather than by inferring the borrowed unit \
from the lender's last period — correct only for the synthesis modes and wrong for every \
<code>fill/*</code>. Each dossier is asymmetric on purpose: the host prefix as unit TITLES (all \
the borrowed unit is entitled to assume) against the borrowed unit's full assumption surface — \
notes, MATERIALS, every band, homework. ARV-D-119's lesson: the dependency arrives through \
<code>materials</code>, not the prose. Read against the SHORTEST prefix in every case. Three \
readers took one grade each against a fixed rubric; <b>every non-CLEAN rating was then verified \
against the source file</b>, and the JUMPY was traced into the lender canonical to confirm its \
provenance.<br><br>

<b>RESULT: 38 CLEAN · 5 SERVICEABLE · 1 JUMPY.</b> All five SERVICEABLE are join REDUNDANCY — \
the host prefix's last unit and the borrowed unit working the same textbook pages back to back \
(vi ch7, vii ch7, vii ch10 X=2, viii ch2, viii ch4) — no continuity break in any of them. Every \
MATERIALS line across all 44 was checked individually: not one lists an artefact another unit \
produces. The units carrying an explicit portability sentence in NOTES ("not a continuation of \
any earlier draft", "no written artefact from an earlier sitting is needed or assumed") were \
<b>without exception clean</b> — the V-series discipline is visibly landing in authored text, and \
that sentence is a usable certification signal.<br><br>

<b>THE ONE JUMPY — viii ch 01 X=6, and it is ARV-D-136 recurring.</b> The class receives p05's \
five units plus the TOP's synthesis U8. Band 0: <i>"Students draft their narrative essay in full \
(p.15–16) <b>using the outline they formed</b> — introduction, body with a turning point, and a \
conclusion that draws a lesson."</i> The outline is made in the top's U7 (<i>"draft an outline \
(opening sentence, two or three body points, closing lesson)"</i>) — a sitting this class never \
had. The unit is TRUE in its home plan at X=8 and false the moment it is borrowed: anchoring is \
not teaching (e11 / ARV-D-023).<br>
It is worse than a missing artefact. The prefix's last sitting is <b>U5 "Narrative Essays and a \
Limerick of Their Own"</b> — the class has already written the essay AND the limericks — and the \
borrowed unit then asks them to draft the essay and introduces limericks as new (<i>"Teacher \
introduces limericks from 'Let us explore' (p.16): reads the sample aloud, pointing out the AABBA \
rhyme scheme"</i>). Two consecutive sittings doing the same two tasks, the second pretending the \
first did not happen.<br>
<b>Same shape as english·IX ch 7: a TOP synthesis that touches the writing spine.</b> Not \
repairable in place — the fix is that U8 must stop doing the writing spine, which is a teaching \
change, and <code>repair_register.py</code> exists precisely to refuse laundering those as text \
hygiene. S11's remedy was a re-author of the top at ₹28.74 with both compacts staying verbatim \
against the new registry.<br><br>

<b>KNOWN LIMITATION, RECORDED RATHER THAN GATED (founder ruling 2026-08-15).</b> The reading \
surfaced a defect CLASS the certifier cannot see, and the ruling is to record it, not to build a \
check that fingers it. <b>Six borrowed units name a prior ACTIVITY rather than content, and are \
true only because THIS prefix happens to contain it:</b><br>
&nbsp;&nbsp;• vi ch7 "the leaf presentations" (prefix U3) · vi ch9 "whether modal verbs appeared \
in both" (U6) · vi ch11 "their own playtime paragraphs" (U5)<br>
&nbsp;&nbsp;• vii ch5 X=8 "using at least one phrasal verb" (U6) — and ch5's OWN X=5 prefix drops \
that spine entirely<br>
&nbsp;&nbsp;• vii ch14 "the gratitude note they wrote" (U3) — <b>directly under a NOTES line \
claiming "no particular earlier activity or written piece is assumed to exist"</b><br>
&nbsp;&nbsp;• viii ch4 X=6 "their oral presentations … using their chosen theme from the Let us \
speak task" (U3)<br>
All rated CLEAN or SERVICEABLE because they are true HERE. They are clean by luck, not by \
construction. <b>Nothing in the pipeline can catch them:</b> the register bans FORWARD \
references, and v1.10 legalised backward ones deliberately — a backward activity reference is \
legal prose that happens to be false for some prefixes. The shape to watch if it is ever taken \
up: a possessive activity reference in a borrowed unit, verified against the host prefix's actual \
units. <b>Not scheduled. Recorded so the next stage's F1 reads for it by eye.</b><br><br>

Dossiers: <code>genon/out/f1_english_middle/f1_{vi,vii,viii}.txt</code>."""

s = json.loads(STATE.read_text())
b = s["batch"]["english/middle"]
b["F1"] = {"status": "pending", "by": "Claude (read) · Kumar (rulings)",
           "comment": F1, "at": NOW, "files": 46}
s["updated_at"] = NOW
STATE.write_text(json.dumps(s, ensure_ascii=False, indent=1))
print("F1 recorded · status pending (awaiting the viii ch 01 ruling)")
print(f"  44 seams · 38 CLEAN · 5 SERVICEABLE · 1 JUMPY")
