#!/usr/bin/env python3
"""S4 · C3 repair pass — ten defects closed on ch 04, five escalated (2026-08-09).

Everything here was repaired IN PLACE at zero cost by genon/repair_c3.py, which separates
GENERIC passes (value derived from the summary, the Pedagogy document or the schema — these
run corpus-wide at the pre-warm) from DECLARED per-instance edits (register phrasings and
word-count labels, which need language and do not generalise).

CLOSED (10): 069 · 070 · 071 · 073 · 074 · 075 · 077 · 082 · 083 · 030(over-length half)
ESCALATED (5): 072 · 076 · 078 · 079 · 080 — each needs a founder decision or re-authored
content, and three of them are arguments about the RULE rather than the plan.

Run from the repo root:
    python3 genon/out/stage_prep_mathematics_secondary/update_tracker_s4_c3_repair_pass.py
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
TOOL = "genon/repair_c3.py v1.0"

CLOSED = {
    "ARV-D-069": "Register repaired. std U3 'the focal error today' -> 'the focal error to "
                 "watch for' (ban 3). p12 U7 'will recur when simplifying rational "
                 "expressions' -> 'also underpin the simplification of ...'; 'may be set for "
                 "later self-study once section 4.7 has been taught' -> '... by students who "
                 "have already met the cube identities'; the HOMEWORK line 'after section 4.7 "
                 "is covered' -> 'which draw on the cube identities'; U12 'a final unit' -> 'a "
                 "unit' (ban 2). Each rewrite states the same fact as a property of the "
                 "CONTENT rather than of the sequence, which is what the register asks for. "
                 "Verified: 0 hits on a scan of all three canonicals.",
    "ARV-D-070": "Continuity by position removed in all three canonicals (std 2, p12 4, p09 2 "
                 "- p09's two were outside C3's sampled pair and are repaired here too). In "
                 "every case the CONTENT was already named, so the repair is deletion of the "
                 "positional clause: 'Having derived (a+b)^2 in the previous unit' -> 'Having "
                 "derived (a+b)^2'. Rule 10 satisfied without losing a single continuity link.",
    "ARV-D-071": "8 units in the standard: 'Problem Solving' -> 'Problem solving', the "
                 "Pedagogy document's exact spelling. All three canonicals now agree. Generic "
                 "pass - the method table is the authority, so this runs corpus-wide.",
    "ARV-D-073": "27 internal ids deleted from the standard's teacher-facing text. Two forms "
                 "were present, '(E-3)' and the narrated '(from E-1)' - the second was missed "
                 "by C3's count of 31, which had over-counted elsewhere; 0 remain on a fresh "
                 "scan. The book_ref always precedes the id, so this is pure deletion and no "
                 "teacher loses a reference.",
    "ARV-D-074": "std sec#6 [8,9] -> [8] and sec#7 [10,11,12] -> [10,11]. U9 ('Middle-Term "
                 "Splitting Extended: Applications') and U12 ('Finding New Identities by "
                 "Combining Results') consolidate a section already taught and deliver none of "
                 "its implied_lo, so Rule 12 excludes them. SERVE EFFECT, re-measured after "
                 "the edit: both item anchors move EARLIER (U9->U8, U12->U11), the sweep is "
                 "unchanged at every X from 6 to 17, and C3's one-unit margin at X=13 is now "
                 "wider. sec#8 [13,14] was checked and is CORRECT - U14 teaches the applied "
                 "LO, so it stays.",
    "ARV-D-075": "Resolved against the mapping's own words: C-9.3's justification names 'the "
                 "middle-term-splitting method in section 4.6'. So 4.6 carries C-9.3 and every "
                 "other section carries the core C-3.1. std sec#5 and p09 sec#5 lose C-9.3; "
                 "p09 sec#6 gains it; p12 was already correct. All three canonicals now give "
                 "the SAME answer, which was the substance of the defect. Note left standing: "
                 "the adjunct C-7.2 (named for 4.2/4.4/4.7 in the mapping) is used by no "
                 "canonical - not repaired, because A4 does not require an adjunct to be used.",
    "ARV-D-077": "16 descriptions (std 10, p12 6) overwritten verbatim from the chapter "
                 "summary, including E-3's '(asterisked parts (v)-(vi) excluded)' - the clause "
                 "Rule 8's exclusion leans on. Generic pass: the summary is the authority, so "
                 "this runs corpus-wide.",
    "ARV-D-082": "Rule 8's substitution statement appended to both OPEN_TASK guides. Fixed "
                 "sentence, so computable. NOTE: if ARV-D-080 is resolved by re-formatting "
                 "those items to ECR, these guides disappear and this repair goes with them - "
                 "harmless either way.",
    "ARV-D-083": "52 empty required fields removed from p12: the four guide sub-blocks that do "
                 "not match the item's question_type are set to null, which is the shape std "
                 "and p09 already use. Each pruned block held only a duplicate "
                 "learning_outcome plus empty strings; the pass refuses to prune any block "
                 "carrying real content. Every item in all three canonicals now has exactly "
                 "one guide block and zero empty required fields.",
    "ARV-D-030": "PARTIAL - the over-length half only, which is what Rule 6 actually guards "
                 "('it is a label, not content'). Three labels shortened into the 10-12 band: "
                 "std sec#7 (15w) and sec#9 (14w), p09 sec#5 (15w). 0 over-length remain. The "
                 "UNDER-length half (8-9 words) is escalated with ARV-D-076 as one question "
                 "about word-count minimums, since the same argument governs both.",
}

ESCALATED = {
    "ARV-D-072": "NOT REPAIRED - a founder call, and it is about the RULE. Streaks: std "
                 "Problem solving x4 (U12-U15), p12 Deductive x3 and Problem solving x3, p09 "
                 "Problem solving x3. Every streak sits at a chapter TAIL, where the content "
                 "genuinely converges on problem work: U13 simplifies rational expressions, "
                 "U14 solves applied area problems, U15 synthesises. Breaking the streak means "
                 "labelling one of those units with a method its content does not support - "
                 "gaming a counting rule at the cost of the plan. Two options: amend Rule 5 P1 "
                 "to permit a longer run where the sections themselves converge (with the "
                 "weighting rule still binding), or accept per chapter. Recommend amending: "
                 "the rule is breached by all three canonicals of the only maths chapter "
                 "tested, which is evidence about the rule.",
    "ARV-D-076": "NOT REPAIRED - a founder call, and it is about the SPEC. activity_title is "
                 "specified at 10-13 words in an A3 schema comment; the model writes 6-10 "
                 "across all three canonicals (31 of 36 units outside the band, in the SHORT "
                 "direction only). The titles are good: 'Reversing the Identity: Factorising "
                 "Perfect-Square Trinomials' is 6 words and cannot be improved by padding it "
                 "to 10. When a spec is missed in one direction by three independent "
                 "generations, the spec is the likelier defect. Recommend widening A3 to 6-13 "
                 "words, or dropping the minimum. Pairs with ARV-D-030's under-length half - "
                 "same argument, same decision.",
    "ARV-D-078": "NOT REPAIRED - needs authored content, and a Cowork session must not install "
                 "one (testing.md C1). std item 1 is owned by 4.1, whose LO is 'verify and "
                 "conjecture the invariant', but the item demands the full algebraic argument "
                 "- which is 4.3's LO and is what item 5 already asks. DRAFT REPLACEMENT, for "
                 "founder approval, not installed: keep the ECR and the Analysis tag but stop "
                 "at conjecture - 'Priya notices that for 5, 6, 7 the expression 5^2+7^2-2x6^2 "
                 "equals 2. Test the pattern on two further triples of consecutive integers, "
                 "state what you think is always true, and explain what about the arithmetic "
                 "makes you expect it to hold - you are not asked to prove it.' That restores "
                 "4.1's own LO and removes the overlap with item 5.",
    "ARV-D-079": "NOT REPAIRED - merged with ARV-D-080; see that row. Fixing the tag alone "
                 "would CREATE an inconsistency: p12 item 9's LO ('factorise a quadratic by "
                 "finding two integers whose sum is p and product is q') is Application under "
                 "Rule 4's reading guide, and Rule 5 maps Application to NUM or SCR - so "
                 "correcting Analysis -> Application leaves an OPEN_TASK the tag no longer "
                 "licenses. Tag and format must move together, which means re-authoring.",
    "ARV-D-080": "NOT REPAIRED - and it surfaced a CONSTITUTIONAL TENSION worth more than the "
                 "defect. Rule 5 reserves OPEN_TASK for 'Integrative / cross-operational "
                 "(co_central)' and this chapter has co_central FALSE; Rule 6 permits a lift "
                 "to OPEN_TASK only when no LO already reaches Analysis or Evaluation, and "
                 "both files have ECR items, so no lift is licensed either. Yet architecture "
                 "v2.0 MANDATES a whole-chapter synthesis unit on the standard canonical, "
                 "whose LO is integrative by construction ('select and apply the appropriate "
                 "identity across the full chapter repertoire'). So on every co_central=false "
                 "chapter - which is most of the corpus - the synthesis unit's item must be "
                 "ECR, and a model reading its own LO will keep reaching for OPEN_TASK. This "
                 "is a V-series / brief matter or a Rule 5 clause, not a per-chapter defect, "
                 "and it will recur at S7, S8 and every stage that mandates a synthesis unit. "
                 "Also here: p12 item 9's format_type 'Procedure / argument evaluation' is not "
                 "on Rule 8's menu at all.",
}

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_c3_repair_pass"))
by_id = {d["id"]: d for d in state["defects"]}

for did, resolution in CLOSED.items():
    d = by_id[did]
    if did == "ARV-D-030":
        d.setdefault("recurrences", [])
        d["recurrences"][-1]["resolution"] = resolution
        d["status"] = "open"        # the SS-IX parent row stays open on its own stage
    else:
        d["status"] = "closed"
        d["closed"] = NOW
    d["at"] = NOW
    d["resolution"] = resolution
    d["repaired_by"] = TOOL

for did, note in ESCALATED.items():
    d = by_id[did]
    d["status"] = "escalated"
    d["at"] = NOW
    d["owner"] = "founder"
    d["resolution"] = note

state["combos"]["mathematics/secondary"]["C3"]["comment"] += f"""

[REPAIR PASS {NOW[:10]}. TEN CLOSED, FIVE ESCALATED, ZERO RUPEES.
 Tool: {TOOL} — GENERIC passes (method label · id leakage · verbatim descriptions · guide
 shape · Rule 8 clause) derive their value from the summary, the Pedagogy document or the
 schema and are the ones that run corpus-wide at the pre-warm; DECLARED edits (register,
 continuity, word-count labels, period_numbers, c_code) are hand-written per instance.
 All three canonicals repaired, not just C3's pair — p09 carried two unnoticed positional
 continuity breaches and a c_code error of its own.
 CLOSED: 069 070 071 073 074 075 077 082 083 + 030's over-length half.
 ESCALATED: 072 076 078 079 080.
 VERIFIED after the pass: 0 id leaks · 0 non-verbatim descriptions · 0 empty guide fields ·
 1 guide block per item · 0 register hits · 0 over-length labels · c_code identical across
 all three canonicals · 25/25 answer checks OK · certification ALL PASS · serve sweep
 identical at every X from 6 to 17, with 074's two anchors now landing EARLIER than before,
 so the X=13 margin is wider than C3 measured it.
 THREE OF THE FIVE ESCALATIONS ARE ARGUMENTS ABOUT THE RULE, NOT THE PLAN: 072 (all three
 canonicals breach the consecutive-method cap at chapter tails where content converges),
 076 (31 of 36 titles miss a schema word-count in the same direction), and 080 (the v2.0
 synthesis mandate wants an integrative item that Rule 5 forbids on any co_central=false
 chapter — this will recur on every stage that mandates a synthesis unit).]"""
state["combos"]["mathematics/secondary"]["C3"]["at"] = NOW

state["updated_at"] = NOW
STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")

still = [d["id"] for d in state["defects"]
         if d.get("combo") == "mathematics/secondary" and d.get("status") == "open"]
print(f"closed {len(CLOSED) - 1} · escalated {len(ESCALATED)} · "
      f"ARV-D-030 recurrence annotated (parent row stays open on SS·IX)")
print(f"still open on maths/secondary: {still or 'none'}")
