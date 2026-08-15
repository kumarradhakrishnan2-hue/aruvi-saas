#!/usr/bin/env python3
"""S11 · english·preparatory — record the BATCH RELEASE row after W2 collected + certified.

Updates batch["english/preparatory"]: spend (stage total, all three dates), W1 (pass),
W2 (pass), and the waiver for the 4 register hits ruled IGNORE rather than repaired.

    python3 genon/out/tracker_update_s11_prep_batch.py
"""
import json
from pathlib import Path

STATE = Path(__file__).resolve().parents[2] / "data" / "testing" / "campaign_state.json"
NOW = "2026-08-15T19:00:00"

SPEND = """All metered spend across iii + iv + v, from <code>runtime_data/token_log.csv</code>. \
<b>STAGE TOTAL ₹1,165.13 over 110 runs — both waves complete, zero canonicals re-bought, one \
re-authored.</b><br><br>
• <b>₹63.86</b> · 3 runs · 2026-08-13 — the PILOT (III ch 11 <i>The Big Laddoo</i>, the poem \
chapter chosen so preparatory's half of the poem-locator amendment was proved by live generation \
rather than inherited untested). ₹21.29/run at sync pricing — <b>2.1× the batch rate</b>, which \
is the clearest per-stage measurement of what the batch route buys.<br>
• <b>₹375.43</b> · 38 runs · 2026-08-15 — <b>W1, the top canonicals</b>. ₹9.88/run \
(₹3.51–13.79), against a ₹450–550 pre-submit estimate. 408 periods.<br>
• <b>₹718.21</b> · 68 runs · 2026-08-15 — <b>W2, the compacts</b>. ₹10.56/run \
(₹4.64–14.57); 542 compact periods.<br>
• <b>₹7.63</b> · 1 run · 2026-08-15 — the iv ch 3 p07 RE-AUTHOR (see W2).<br><br>
Both batch waves land BELOW the runbook's ₹12–15/run band. <b>₹0.92 per authored period</b>, \
flat across waves — the most stable unit yet measured, and a better projection base than ₹/run \
because compacts and tops differ in length but not in rate. 39 chapters · 109 canonicals on disk."""

W1 = """S11 · classes iii/iv/v · 2026-08-15. <b>39 chapters, 38 top canonicals, ₹375.43</b>, \
38/38 <code>ok</code> (III ch 11 correctly skipped — the 2026-08-13 pilot was already installed \
with its full ladder 12/10/7).<br><br>
<b>THE FIRST ENGLISH LIBRARY EVER AUTHORED UNDER THE PAIR RULE AT PREPARATORY</b> (assessment \
v1.5). It held, and was asserted by measurement rather than by eye: <b>186 of 188 cells carry \
exactly 2 items</b>; <b>0 pairs disagree on <code>source_lo</code></b>; and \
<code>unit_ref</code> / <code>period_ref</code> / <code>period_number</code> / \
<code>phase_ref</code> appear on <b>ZERO items</b> — the Rule 8A prohibition verified across the \
whole corpus, not sampled. Density <b>0.87 items/unit</b> against english·secondary's \
pre-amendment 0.35. The two 4-item cells (III ch 3 <code>A|oracy</code>, III ch 15 \
<code>B|word_work</code>) are TWO correct pairs sharing one (section × spine) address — the cell \
key is coarser than <code>source_lo</code> — not a rule breach.<br><br>
<b>C5 check 11 caught a defect class nothing else was looking for.</b> It first read 37/39, with \
V ch 8 and V ch 9 reporting "no section list readable". The cause was not a missing marker: \
<b>both chapter summaries were UNPARSEABLE JSON</b> — 12 and 4 unescaped <code>"</code> inside \
quoted dialogue (<i>"I sold only the well, not the water."</i>; <i>"Bangles, crystal bangles!"</i>), \
each duplicated across <code>tasks_verbatim</code> and a <code>question_bank</code> stem. \
<b>Generation never noticed</b>, because <code>prompt_assembly.read_file</code> embeds the summary \
as raw TEXT — so the plans are sound and every anchor check passes. Only JSON-parsing consumers \
went blind, and check 11 <i>advised</i> rather than failed, so it would have entered the tracker as \
"unreadable" rather than "broken". Repaired to <code>\\"</code> (the convention every other summary \
already uses), verified as pure escaping — strip backslashes from backup and repaired file and the \
diff is <b>0 lines</b>, +12 and +4 bytes exactly. <b>39/39 PASS after.</b> A JSON-parse assertion \
belongs in the chapter pipeline; two of 39 shipped broken and nothing caught it.<br><br>
<b>FAIL census: 17 register ban hits across 14 of 39 files</b> — 1 per 2.8 files, dead on the \
runbook's expected 1-in-3. Families: <b>clock 8</b> · forward 6 · meta-leak 2 · calendar 1. The \
clock family has a preparatory-specific shape worth carrying: every hit is a duration inside a \
READING or DISCUSSION instruction ("re-read silently for two minutes"), never the "for the \
remaining time" boilerplate the middle-stage sets struck — at classes III–V the model bounds a \
task because young children need it bounded.<br><br>
<b>16 repairs declared and applied</b> (<code>repair_register.py</code> v1.8, free, all old→new by \
assertion). 1 struck: III ch 13 U2 <code>foreshadows</code> — narrative structure inside the story, \
both warning and trouble read in the same unit; founder ruling <i>ignore, handle as it arises</i>. \
One edit REPLACES rather than deletes (IV ch 6 U11 "do tomorrow" → "start doing").<br><br>
<b>Two engine findings this wave produced.</b> (1) <b>2 STARVED assessment cells</b> — \
<code>cell_resolver</code>'s dispersion guard is M≥N, and everything failing it fell to the \
shared-span branch, collapsing every item onto the closing unit while the earlier sittings that \
teach the cell showed no Assess tab. Fixed by <code>_backfill()</code> (founder: back-fill to \
close, do not touch the constitution), 132 carrier tests green. (2) 1 Rule 2 breach — IV ch 4 \
<code>A|oracy</code> emitting ORAL_PROMPT twice where the slot table prescribes MCQ/TRUE_FALSE at \
slot 1; founder ruled IGNORE."""

W2 = """Compacts landed 2026-08-15. <b>68 requests, ₹718.21, 68/68 <code>ok</code>, 0 re-bought; \
<code>library complete</code> went to 39/39 PASS</b> — 109 canonicals on disk (39 tops + 70 \
compacts).<br><br>
<b>ONE FILE WAS QUARANTINED, AND THE DIAGNOSIS IS THE FINDING.</b> IV ch 3 p07 failed \
<code>first-visit order follows the registry</code>. Its cell order is registry positions \
<b>[0, 2, 3, 4] — strictly ascending</b>. Nothing is taught early. It failed because \
<code>build_library.py:421</code> treats a GAP in the frontier (<code>r[0] &gt; seen_hi + 1</code>) \
as a skipped section, so <b>dropping a middle cell trips the ORDER check</b>. The same file \
produced the batch's only <code>OMITS</code> line — the check built precisely to report drops as \
<i>"reported, not gated — rule at the human gate"</i>, above a comment saying a compact \
legitimately teaches less. <b>The two checks contradict each other</b>, and the ORDER message \
misdiagnoses.<br><br>
<b>Recurrence was measured before re-authoring, not assumed.</b> Every other compact on disk \
teaches all 5 cells at every size — <b>17 of 17 other 7-period compacts, and the 5-period ones \
too</b> — so 7 periods is not a squeeze. The brief is sound and identical in shape to the one that \
produced the passing p09. <b>The latent cause: the compact brief never says every registry cell \
must be TAUGHT</b> — only that references be verbatim and first appear in registry order. The \
model broke no instruction it was given. Re-authored for <b>₹7.63</b>: 7 units, all 5 cells \
including oracy, positions [0,1,2,3,4] ascending AND gapless, 0 register hits. The quarantined copy \
is kept as the cost record and carries 0 register hits, so runbook trap 1 does not bite.<br><br>
<b>FAIL census: 32 ban hits across 24 of 70 compacts</b> — 1 per 2.9 files, statistically identical \
to W1's 1-per-2.8. Families: <b>clock 19</b> · forward 9 · completion 2 · meta-leak 2.<br><br>
<b>CLOCK ROSE FROM 8-of-17 TO 19-of-32 BETWEEN WAVES</b>, same shape both times. A shorter plan \
makes every band feel tighter, so the model reaches for a duration more often. This is a BRIEF \
problem, not a model problem, and the next preparatory stage should say so upfront rather than pay \
for 27 repairs twice.<br><br>
<b>COMPLETION APPEARED FOR THE FIRST TIME AT THIS STAGE — and it can only ever appear on \
compacts.</b> Both hits are in a compact's CLOSING unit ("built across the chapter"). A top's \
closing unit is the mandated <code>synthesis</code>, which the completion ban EXEMPTS by design; \
a compact is FORBIDDEN a synthesis anchor, so its last unit does the same summing-up job with none \
of the licence. Expect this family on every compact wave; it will never show on a top.<br><br>
<b>META-LEAK HELD AT 2</b> — on 70 files against W1's 2 on 38, i.e. 0.9 per 1000 units. Third \
corpus confirming the corrected <code>variant_plans._serving_block()</code>.<br><br>
<b>29 repairs declared and applied</b> (v1.9); 3 struck (see WAIVER). One REPLACES rather than \
deletes (V ch 6 p08 U1 — deleting the sentence would lose "unhurried", the actual instruction).<br><br>
<b>The <code>_backfill</code> fix earned its keep here:</b> <b>18 cells</b> would have collapsed \
onto their closing unit under the old rule, against 2 in W1 — exactly as predicted for shorter \
plans. Library-wide assessment coverage <b>808/972 units = 83.1%</b>.<br><br>
<b>CLOSING CHECKLIST (runbook §5) — all seven lines true.</b> library complete 39/39 · quarantine \
holds nothing without a live counterpart · register hits stage-wide = 4, all RULED (see WAIVER), \
not repaired-to-zero · every chapter ALL PASS incl. C5 check 11 39/39 · anchors, order, coverage, \
question types 109/109 · serve sweep 358/358 choice sets non-empty at top/middle/floor/below-floor \
· 0 derived plans on disk · spend reconciled."""

WAIVER = """<b>4 register ban hits ruled IGNORE rather than repaired</b>, founder \
2026-08-15 (<i>"ignore the 3 'bridge' related issues. accept and close"</i>; and separately, on the \
fourth, <i>"ignore it, we will handle as it arises"</i>). Recorded so the gap is a DECISION on the \
record. Deliberately NOT fixed at the scanner, so the next english library re-raises them and the \
ruling is re-made with evidence rather than inherited silently.<br><br>
<b>GROUP A — <code>bridges? (toward|towards|to) the</code> firing where nothing points forward \
(3).</b> Each destination checked individually:<br>
&nbsp;&nbsp;• <code>iv/ch_11_canonical_p09.json</code> U6 band:2 — "Bridge to the body-part task". \
That task is <b>band:3 OF THE SAME UNIT</b>, 18–20 → 20–35. Two minutes later, same sitting.<br>
&nbsp;&nbsp;• <code>iv/ch_05_canonical_p08.json</code> U8 — "a natural bridge to the adverb work \
explored <b>EARLIER</b> in the chapter": a BACKWARD reference, legal since v1.10. The pattern \
matches "bridge to the" and never reads the direction word four tokens on.<br>
&nbsp;&nbsp;• <code>iii/ch_09_canonical_p07.json</code> U3 — "an oral bridge to the story's \
<b>THEME</b>, not an assessed task": the destination is a theme, not a unit, and the clause says in \
terms that nothing is deferred.<br>
The 2026-08-15 bridge ruling is NOT disturbed — viii ch 14 p09 U6's "bridge to the space-travel \
speaking task" named a real later sitting and rightly stands. These three do not. This is the \
<b>second stage running</b> where the bridge pattern produces only false positives (english·middle \
struck 4 under the same reasoning).<br><br>
<b>GROUP B — content the scanner cannot tell from a forward reference (1).</b><br>
&nbsp;&nbsp;• <code>iii/ch_13_canonical.json</code> U2 [forward] "foreshadows" — "the tree's \
warning foreshadows Madhu's trouble" is narrative structure INSIDE the story; both the warning and \
the trouble are read in this same unit's comprehension work. Identical in shape to vii ch 2 p06 U1, \
struck at S10. <b><code>foreshadow\\w*</code> has now produced four hits across three stages and no \
true positive</b> (english iii ch 13, english vii ch 2, maths vii ch 7 ×2), while \
<code>previewing</code> — banned by the SAME regex at <code>register_scan.py:85</code> — caught a \
real one here (V ch 9 U10, repaired). The case for splitting them is now evidential, not \
theoretical.<br><br>
<b>NOT WORD-SWAPPED TO DODGE THE REGEX.</b> "bridge" → "link" would have cleared all three of \
Group A while leaving the pattern broken for the next stage to rediscover — runbook trap 4's point \
exactly. <b>Scope:</b> these 4 strings in these 4 files. Not a standing exemption for either \
pattern, and it does not travel: english·secondary and english·middle ruled on their own hits with \
their own evidence, and the next stage must too."""

s = json.loads(STATE.read_text())

# ── CORRECTION to a neighbouring row, found while verifying this one ────────────────
# The batch tab's two count columns are defined as ON-DISK FACTS: "top canonicals on
# disk" and "compact canonicals on disk". Counted against data/content/saved_plans/,
# three of the four recorded stages agree exactly (TWAU 32/61, SS·IX 9/16, english·IX
# 16/26). english/middle recorded 46/46 — the CHAPTER count in both columns, where its
# compacts number 74 (vi 24 · vii 24 · viii 26). batchTotalsRow() sums W1+W2, so the
# corpus figure has been understating by 28 canonicals since 2026-08-15.
# Only the NUMBER is corrected here. S10's comment prose is left exactly as written:
# it is that session's record of what it measured, and rewriting another session's
# narrative to match a later count would destroy the evidence rather than fix it.
_mid = s["batch"].get("english/middle", {}).get("W2")
if _mid is not None and _mid.get("files") == 46:
    _mid["files"] = 74
    _mid["files_corrected"] = ("46 -> 74 on 2026-08-15 (S11): 46 was the chapter count; "
                               "the column is compact canonicals on disk. Comment prose "
                               "left as S10 wrote it.")
    print("corrected english/middle W2 files 46 -> 74")

b = s["batch"].setdefault("english/preparatory", {})
b["waiver"] = {"status": "pass", "by": "Kumar (ruling) · Claude (measured + recorded)",
               "comment": WAIVER, "at": NOW, "files": 4}
b["spend"] = {"cost_inr": 1165.13, "comment": SPEND,
              "by": "Claude (runtime_data/token_log.csv)", "at": NOW}
b["W1"] = {"status": "pass", "by": "Kumar (ran) · Claude (repaired + recorded)",
           "comment": W1, "at": NOW, "files": 39}
b["W2"] = {"status": "pass", "by": "Kumar (ran) · Claude (repaired + recorded)",
           "comment": W2, "at": NOW, "files": 70}
s["updated_at"] = NOW
STATE.write_text(json.dumps(s, ensure_ascii=False, indent=1))
print(f"written -> {STATE}")
print(f"  spend  ₹{b['spend']['cost_inr']}")
print(f"  W1     {b['W1']['status']}  ({b['W1']['files']} top canonicals)")
print(f"  W2     {b['W2']['status']}  ({b['W2']['files']} compacts)")
print(f"  waiver {b['waiver']['status']}  ({b['waiver']['files']} ruled hits)")
