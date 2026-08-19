#!/usr/bin/env python3
"""Record the S7 assessment-anchoring findings (2026-08-19) on the defect register.

Run from the repo root:
    python3 genon/out/stage_prep_mathematics_middle/record_s7_anchor_defects.py
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()

DEFECTS = [
 {"id": "ARV-D-179", "combo": "mathematics/middle", "step": "W2", "severity": "S3",
  "status": "closed",
  "title": "vi ch 9 p14 Q-C-5 declares `number_line:` on a four-step process strip, not a tick line",
  "evidence": "Certification: '4 cell(s) exceed 16 chars'. The stimulus read 'number_line: Original L (5 sq) | + vertical mirror | + horizontal mirror | = Complete figure' — narration, not labels. Two faults, so the FIELD goes rather than the tag: (a) the item asks how many squares complete an L so it gains both lines of symmetry, and what would help is the L on squared paper with the mirror lines marked — Rule 7 forbids a tick line from being that ('the ticks are drawn as an ordered line, never as a grid') and bans SVG at this stage, so no permitted format can carry it; (b) the strip restates the item's own method_one_line, converting an `apply` item into an instruction to follow. Rule 7's stated DEFAULT for geometry is '' with the figure reached through the `exercise` companion — which this item already carries (Figure it Out Q12, section 9.1 p.229). Repaired by declaration, repair_c3.py ('mathematics','vi')."},

 {"id": "ARV-D-180", "combo": "mathematics/middle", "step": "W2", "severity": "S2",
  "status": "closed",
  "title": "viii ch 12 p13 Q-C-10 is a declared MCQ that asks nothing — empty prompt, options, answer and method",
  "evidence": "Only the `exercise` companion was filled (Figure it Out Q5, section 5.2 p.127 — the three average/multiple statements). Nothing to substitute, so the question was AUTHORED under founder ruling 2026-08-19 ('generate an equivalent question') rather than the compact re-bought. Built on statement (ii) and asking for the counterexample: an MCQ cannot carry the exercise's 'with algebraic justification', all three statements are false in general (5,10 -> 7.5 · 2,4 -> 3 · 5,5,5,5,10 -> 6) so 'which is true?' would need a banned by-label option, and a counterexample is the algebra in miniature (5a,5b average to 5(a+b)/2). `verified` left false. TWO DRAFTS WERE ROLLED BACK from backup/c3_repair/ rather than patched: the first named option letters in the guide prose, which STEP 6's arrangement invalidated the moment it installed (it remaps the reveals dict KEYS, normalize_options.py:180-182, but cannot rewrite prose); the second keyed the reveals against the arranged order instead of the declared order, so the remap faithfully carried a mismatch through. Standing rule recorded in the declaration: a label is the platform's to assign — guide text names the PAIR ('5 and 10'), never the letter beside it. Certification cannot see either error; it checks arrangement order, not whether a reveal describes the option beside it."},

 {"id": "ARV-D-181", "combo": "mathematics/middle", "step": "W2", "severity": "S2",
  "status": "open",
  "title": "assessment anchors by SECTION on a stage whose sections are banners — questions cluster at the close and a shortened plan loses them faster than it loses teaching",
  "evidence": "MEASURED over the 39 standard canonicals, 553 items. Only 199 of 540 sittings carry an Assess tab (37%) at 2.8 items each; maths SECONDARY is 76%/1.3, SS middle 71%/1.3, TWAU 100%/1.0. Worst: vii ch14 = 15 items on U11 and 7 on U16, nothing else in 17 sittings; vi ch5 = 24 items on U21-U24 of 25; viii ch12 = two sittings carrying 7 and 9. SERVE LOSS is the real cost (founder, 2026-08-19): a plan served at three-quarter length keeps 57% of items and at half length 35% — worse than proportional — and THREE chapters hand a half-length class ZERO questions (vi ch5, vi ch8, vii ch14). CAUSE: the rule holds an item until its section closes, correct where a section is a topic (SS, TWAU) but not here — maths middle sections are banners over a fortnight (median 6 per chapter vs secondary's 10), and the real progression is COMPLEXITY, marked by the anchor exercise (LP Rule 3 assigns one anchor per period from that period's own textbook items). The prototype's single-chapter review could not surface this."},

 {"id": "ARV-D-182", "combo": "mathematics/middle", "step": "W1", "severity": "S3",
  "status": "open",
  "title": "four chapters teach a section in two non-contiguous runs — Rule 1 has forbidden it since v3.6 and the certifier check owed with that amendment was never built",
  "evidence": "vi ch5 (6 sections revisited, e.g. 5.1 at U1-5 then U21), vi ch8 (6 sections, 9 revisits, 8.4 at U6-10 / U17-18 / U21), vii ch5 (5.8 at U9-12 then U14), viii ch14 (7.6 at U10-11 then U13). All authored under LP v3.9, which is ARV-D-089's shape after v3.6 aligned Rules 1/2 and v3.8 deleted the surplus bullet as 'the cause, not the cure'. The v3.6 CHANGELOG records the gap in terms: 'Owed with this, and free: a certifier check that no section appears in two non-contiguous runs. Rule 1 has forbidden interleaving all along and nothing ever tested it — which is why three revisits reached a paid artefact and were found by eye.' Had it existed, vi ch5 and vi ch8 would have FAILED W1 certification instead of passing clean, before their compacts were bought. Consequence under the section rule: a revisit unit silently becomes the last unit of every section it re-touches and swallows the whole chapter's questions — which is exactly ch5's shape."},

 {"id": "ARV-D-183", "combo": "mathematics/middle", "step": "W1", "severity": "S3",
  "status": "open",
  "title": "the tightened synthesis clause binds on the section TOKEN, so a re-author can satisfy it by moving the label without moving the teaching",
  "evidence": "vi ch3 was re-authored 2026-08-19 under the new clause ('THE SYNTHESIS UNIT INTRODUCES NOTHING') and passed the check I ran, which asked only whether a body unit NAMES section 3.12. It does — U11 carries the token and one exercise (E-57, Figure it Out Q10 p.73). But FIVE of 3.12's six exercises are still worked in U12, the synthesis (E-48, E-53, E-54, E-55, E-56, all p.72-73). The label moved; the teaching did not. Verified structurally, not substantively, and I recorded 'all four came back correct on the first try' on that basis — too generous. Owed: check the other three re-authors (vi ch10, vii ch3, viii ch3) the same way, and consider binding the clause on EXERCISES rather than on section tokens."},

 {"id": "ARV-D-184", "combo": "mathematics/middle", "step": "W2", "severity": "S4",
  "status": "open",
  "title": "eleven assessment items carry an empty `exercise` companion",
  "evidence": "`{\"book_ref\": \"\", \"description\": \"\"}` on 11 items across viii ch1 (x2), ch7 (x3), ch9, ch10, ch11 (x2), vii ch5; a twelfth (viii ch12 Q-C-13) names an exercise that is not one of the chapter's handoff anchors. The assessment constitution asks for the companion on every item (Rule 9) — it is the teacher's parallel-practice pointer and, on geometry items, the route to the figure that Rule 7's empty-stimulus default depends on. FOUNDER RULING 2026-08-19: these fall back to the section rule; recorded as a generation-quality signal, not repaired."},
]

RULING = {
 "id": "ARV-D-181-RULING", "combo": "mathematics/middle", "step": "W2", "severity": "S4",
 "status": "closed",
 "title": "RULING on ARV-D-181 — anchor via the handoff anchor's FIRST working, with the section rule as backstop",
 "evidence": "Founder, 2026-08-19, after enumerating all 553 items. THE RULE: an item anchors at the sitting where its handoff anchor exercise is FIRST worked. Derivation only, nothing demanded of the model — the item's `exercise.book_ref` IS a handoff `anchor_book_ref` on 541 of 553 items, the handoff carries `anchor_id`, and LP Rule 3 assigns each anchor to a period from that period's own textbook items. First-working is unique by construction, so there is no disambiguation problem (the reconstruction machinery I built for repeated anchors was unnecessary). MEASURED: 82% of sittings carry an Assess tab against 37%, 1.2 items each against 2.8, and retention at three-quarter length rises 57% -> 77%. 98% of first appearances are genuine in-class work, so the first working IS the teaching moment. TWO CLASSES FALL BACK TO THE SECTION RULE, both settled: (a) the 25 items whose anchor is worked ONLY in the synthesis unit — 23 of 25 are C-band `apply` on the chapter's LAST section, i.e. the capstone, and the section rule already places 20 of them one sitting before the closer, so the two rules differ by a single sitting and it is not worth becoming the first stage in the campaign to put assessment on a synthesis unit (a borrow path never once exercised: ZERO items anchor to a synthesis anywhere in the corpus, 3,115 items over 225 chapters); (b) the 12 of ARV-D-184. CONSEQUENCE: the synthesis exclusion in carriers.items_by_period_field is UNTOUCHED, so english — the only other user of that helper — is unaffected, and no other family ever had the filter. SCOPE: mathematics middle AND preparatory (same shape under other names — handoff `tasks[].task_id` against period `tasks_in_class[].id`; measured 7% -> 86% on iii ch5). NOT DONE, deliberately: exercise-text matching (an earlier proposal of mine, wrong — it placed 68% of items before their section closed) and any change to what the model is asked to author."}

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_anchor_defects"))
have = {d.get("id") for d in state["defects"]}
added = []
for d in DEFECTS + [RULING]:
    if d["id"] in have:
        continue
    d = dict(d)
    d["opened"] = NOW
    d["closed"] = NOW if d.get("status") == "closed" else None
    d["owner"] = "Kumar"
    state["defects"].append(d)
    added.append(d["id"])
state["updated_at"] = NOW
STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
print("added:", ", ".join(added) or "(none — already present)")
print("defects on register:", len(state["defects"]))
