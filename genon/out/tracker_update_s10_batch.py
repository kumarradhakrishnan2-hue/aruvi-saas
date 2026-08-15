#!/usr/bin/env python3
"""S10 · english·middle — record the BATCH RELEASE row after W2 collected + certified.

Updates batch["english/middle"]: spend (the stage total, all three dates), W1 (pass),
W2 (pass, with the brief-fix measurement that is the point of this wave).

    python3 genon/out/tracker_update_s10_batch.py
"""
import json
from pathlib import Path

STATE = Path(__file__).resolve().parents[2] / "data" / "testing" / "campaign_state.json"
NOW = "2026-08-15T16:20:00"

SPEND = """All metered spend across vi + vii + viii, from <code>runtime_data/token_log.csv</code>. \
<b>STAGE TOTAL ₹1,441.13 over 120 runs — both waves complete, zero canonicals re-bought.</b><br><br>
• <b>₹73.54</b> · 3 runs · 2026-08-13 — the PILOT (VI ch 8 <i>What a Bird Thought</i>, the poem \
chapter chosen to put the 2026-08-12 poem-locator amendment under live generation). ₹24.51/run: \
sync pricing, and the reason the batch route exists.<br>
• <b>₹513.39</b> · 45 runs · 2026-08-14 — <b>W1, the top canonicals</b>. ₹11.41/run.<br>
• <b>₹854.19</b> · 72 runs · 2026-08-15 — <b>W2, the compacts</b>. ₹11.86/run against a ₹10.8 \
pre-submit estimate (worst case, zero cache); 473 compact periods.<br><br>
Both batch waves land inside the runbook's ₹12–15/run band and BELOW it. 46 chapters · 118 \
canonicals on disk."""

W1 = """S10 · classes vi/vii/viii · 2026-08-14. <b>46 chapters, 45 top canonicals, ₹513.39</b> \
(VI ch 8 correctly skipped — the 2026-08-13 pilot was already installed). Largest stage in the \
campaign by chapter count.<br><br>
<b>The v3.7 PAIR amendment fired everywhere.</b> <b>45/45 chapters satisfy items = 2 × \
<code>section_contributions</code></b> exactly — 544 items over 266 cells. Density ~1.1 items/unit \
against english·secondary's pre-amendment 0.35. This is the first english library authored under \
the pair rule at middle, and it held without exception; the four chapters with 4- and 6-item cells \
(vi ch 4, vi ch 7, viii ch 9, viii ch 12) are extra CONTRIBUTIONS on one spine, not extra items \
per cell.<br><br>
<b>C5 check 11: 46/46 PASS</b> — no summary section left unanchored, on the check that caught \
science·ix ch 8 on an already-certified library. Synthesis-anchor gate 46/46 PASS. Quarantine \
carried nothing from this build.<br><br>
<b>FAIL census: 36 register ban hits across 22 of 46 chapters, nothing else</b> (~1 breach per 2 \
files, against S5's 1-per-3). Families — and this is the finding the stage is remembered for: \
<b>meta-leak 17</b> · forward 11 · clock 8. <b>The first library in the campaign where meta-leak \
is the LARGEST family.</b><br><br>
<b>36 repairs declared and applied</b> (<code>repair_register.py</code> v1.6, free, all \
old→new by assertion, none hand-edited, none regenerated). 31 were flagged; <b>5 were found by \
READING the full teacher_notes once a flagged sibling was located</b> — every one a second \
disclaimer in the same note (vi ch 9 U11, vii ch 4 U12, viii ch 5 U9, viii ch 11 U11, viii ch 12 \
U9). That is runbook trap 1's shape in a new place, and it is why the census is read per FILE, \
not per hit. One edit is a REPLACEMENT not a deletion, declared as such (viii ch 12 U2: deleting \
"are addressed in a later unit" leaves "are addressed", asserting the opposite of the truth).<br><br>
<b>Re-certified free: 44 library-complete FAILs (between-waves arithmetic) + 4 register FAILs, \
which are the 5 hits ruled IGNORE.</b> 18 of the 22 breached chapters went to zero; no check that \
passed before now fails."""

W2 = """Compacts landed 2026-08-15. <b>72 requests, ₹854.19, 0 re-bought; \
<code>library complete</code> went to ZERO FAILs</b> — every compact installed. 118 canonicals \
on disk across 46 chapters.<br><br>
<b>THIS WAVE WAS A CONTROLLED TEST, AND IT PASSED.</b> W1's 17 meta-leaks traced to the BRIEF, \
not the constitutions: <code>variant_plans._serving_block()</code> stated self-containment as \
three prohibitions with their rationale attached, and the model echoed the rationale back as \
teacher-facing prose. <b>Founder ruling 2026-08-15: "let us not touch a constitution for an \
issue the brief created."</b> Evidence that decided it — the PRE-BRIEF corpus \
(<code>backup/saved_plans/</code>, 47 prototype-era plans, 385 units) carries <b>ZERO</b> \
self-containment disclaimers against <b>67 in 2297</b> authored units. Nothing else differs \
between the two corpora. The same measurement vindicates the brief on its own terms: forward \
references fell 88.3 → 19.2 per 1000 units under it.<br><br>
The block was reworded positively and gained one new line ("THE SERVE MODEL IS NEVER THE \
TEACHER'S BUSINESS … if a sentence would be pointless to a teacher who had never heard of \
variant plans, cut it"). <b>These 72 compacts are the first files authored under it, and \
meta-leak fell 40.5 → 2.1 per 1000 units — 17 hits became 1.</b> All families: 85.7 → 29.6 per \
1000. Scoped to the 72 authored today; VI ch 8's pre-fix compact pair excluded. Caveat kept \
honestly: the wave changed as well as the brief (compacts are shorter and structurally \
different), so some of the drop in the OTHER families is composition — the meta-leak collapse \
is far too large to be.<br><br>
<b>FAIL census: 14 register hits over 11 files, nothing else</b> — forward 7 · clock 3 · \
meta-leak 1 · completion 1 · calendar 1. <b>12 repairs declared and applied</b> \
(<code>repair_register.py</code> v1.7). 11 flagged + 1 found by reading (viii ch 14 p09 U6's \
closing sentence names a later sitting AND tells the teacher what the plan is withholding; the \
scanner had stopped at "bridge to the" three clauses earlier).<br><br>
<b>TWO OF THE 14 WERE NOT REPAIRED — put to the founder as false positives</b> rather than \
struck, per runbook trap 4: vii ch 2 p06 U1 "foreshadow" (the pictures foreshadow the poem's \
spider metaphor and the poem is READ IN THAT SAME UNIT — the pattern has no same-unit \
exemption), and vii ch 3 p07 U3 "tomorrow" (Helen Keller's OWN argument, "use their eyes as if \
tomorrow they might be blind", paraphrased from p.33 — the word is the essay's, and it misses \
the scanner's quoted-content exemption by its punctuation alone).<br><br>
<b>OPEN AT THE CLOSING CHECKLIST: 8 ban hits survive library-wide, and §5 item 3 asks for \
zero.</b> All 8 are rulings, not omissions — 4 × <code>bridge to the</code> firing where nothing \
points forward (founder: "ignore it, no repair needed", 2026-08-15), 2 × the meta-leak \
disclaimer regex spanning a semicolon into an unrelated clause (objects are "prepared \
specimens" and "revision time"), plus the two false positives above. <b>Each needs a recorded \
waiver or a scanner change before this stage closes</b> — the gap must be a decision on the \
record, not something the next reader re-derives."""

WAIVER = """<b>REGISTER WAIVER · english·middle · founder ruling 2026-08-15.</b> Closing \
checklist §5 item 3 asks for ZERO register ban hits library-wide. This stage closes with \
<b>8</b>, and every one is a scanner false positive that was ruled rather than repaired. \
Recorded here so the gap is a DECISION on the record, not something the next reader re-derives \
— and deliberately NOT fixed at the scanner, so the next english library re-raises them and the \
ruling is re-made with evidence rather than inherited silently.<br><br>

<b>GROUP A — <code>bridges? (to|toward) the</code> firing where nothing points forward (4).</b> \
Founder: <i>"ignore it, no repair needed."</i> The pattern was added 2026-08-03 (ARV-D-038) for \
"bridges toward the … sections that follow"; it matches the bare phrase.<br>
&nbsp;&nbsp;• <code>vi/ch_01_canonical.json</code> U6 — "a bridge to the phonics work FROM the \
speaking unit": a BACKWARD reference, legal since v1.10.<br>
&nbsp;&nbsp;• <code>vii/ch_02_canonical.json</code> U10 — "a genuine bridge to the science \
curriculum": cross-curricular, names no unit.<br>
&nbsp;&nbsp;• <code>viii/ch_06_canonical.json</code> U1 — "bridge to the text": into this \
unit's own text.<br>
&nbsp;&nbsp;• <code>viii/ch_14_canonical_p09.json</code> U6 — "conceptual bridge to the \
space-travel speaking task", that unit's own task. (Its REAL breach, the closing sentence naming \
a later sitting, WAS repaired under v1.7.)<br><br>

<b>GROUP B — the meta-leak disclaimer regex spanning a semicolon into an unrelated clause (2).</b> \
Founder: no preference expressed; left as authored on the same reasoning as Group A. The pattern's \
window is <code>[^.]{0,70}</code>, which crosses clause boundaries to reach OUR vocabulary in a \
sentence that was never about it.<br>
&nbsp;&nbsp;• <code>vii/ch_02_canonical.json</code> U9 — "closes within its own minutes without \
requiring prepared specimens; the homework folk-song task…": the disclaimer's object is \
MATERIALS.<br>
&nbsp;&nbsp;• <code>vii/ch_06_canonical.json</code> U7 — "without requiring revision time the \
unit does not have": the object is TIME, and the sentence is a scheduling judgement about this \
unit's own budget.<br><br>

<b>GROUP C — content the scanner cannot tell from scheduling (2).</b> Flagged by Claude at W2 \
rather than repaired, because striking either would falsify chapter content (runbook trap 4).<br>
&nbsp;&nbsp;• <code>vii/ch_02_canonical_p06.json</code> U1 [forward] "foreshadow" — the \
pre-reading pictures foreshadow the poem's spider metaphor, and the poem is READ IN THAT SAME \
UNIT. The pattern has no same-unit exemption.<br>
&nbsp;&nbsp;• <code>vii/ch_03_canonical_p07.json</code> U3 [calendar] "tomorrow" — Helen \
Keller's own argument ("use their eyes as if tomorrow they might be blind"), paraphrased from \
p.33. The word is the ESSAY'S. A calendar hit inside quotation marks drops to advisory; this \
close paraphrase misses the exemption by its punctuation alone.<br><br>

<b>WHAT THIS WAIVER DOES NOT COVER.</b> It is scoped to these 8 strings in these 7 files. It is \
not a standing exemption for the four patterns, and it does not travel to another stage: \
english·preparatory and english·secondary must rule on their own hits with their own evidence. \
<b>The upstream remedy, if the rate persists, is at the scanner</b> — a forward object required \
on the bridge pattern, a clause boundary on the disclaimer window, a same-unit exemption, a \
wider quoted-content test — and that is a free change under §9. It was NOT taken here because \
four patterns narrowed on one stage's evidence is how a gate stops catching things."""

s = json.loads(STATE.read_text())
b = s["batch"]["english/middle"]
b["waiver"] = {"status": "pass", "by": "Kumar (ruling) · Claude (measured + recorded)",
               "comment": WAIVER, "at": NOW, "files": 7}
b["spend"] = {"cost_inr": 1441.13, "comment": SPEND,
              "by": "Claude (runtime_data/token_log.csv)", "at": NOW}
b["W1"] = {"status": "pass", "by": "Kumar (ran) · Claude (repaired + recorded)",
           "comment": W1, "at": NOW, "files": 46}
b["W2"] = {"status": "pass", "by": "Kumar (ran) · Claude (repaired + recorded)",
           "comment": W2, "at": NOW, "files": 46}
s["updated_at"] = NOW
STATE.write_text(json.dumps(s, ensure_ascii=False, indent=1))
print(f"written -> {STATE}")
print(f"  spend  ₹{b['spend']['cost_inr']}")
print(f"  W1     {b['W1']['status']}  ({b['W1']['files']} files)")
print(f"  W2     {b['W2']['status']}  ({b['W2']['files']} files)")
