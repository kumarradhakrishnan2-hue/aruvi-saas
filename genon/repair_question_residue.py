#!/usr/bin/env python3
"""repair_question_residue.py — questions and mark schemes left pointing at deleted text
(v1.0, 2026-08-14, S11 · F2 follow-up).

WHAT HAPPENED. `repair_passage_fidelity.py` replaced eight passages with the textbook's
actual words. Two question edits travelled with them and were declared there. THREE MORE
RESIDUES SURVIVED, found by the founder reading the items rather than by any check:

  ch 09 p07  Q2 asks why she could switch to para-athletics "using a detail from the
             passage" — the swimming detail moved to p.140, outside the new p.139 quote.
             Q3 asks about the 2016 Rio "breakthrough", also outside it. And guide element
             0 still keys on 'decision' and 'defining moment', phrases that existed ONLY in
             the invented text that was deleted.
  ch 15 p05  Q3 quotes 'the prospect of success provides the necessary momentum' as the
             mother's words. That was the paraphrase. The letter says "When stamina is
             running out, the prospect of success will keep you on track."
  ch 09 p09  Q3 says "in the light of the two choices she describes" — the two-choices
             sentence went with the splice. Guide element 3 carries the same residue.

THE LESSON, which is worth more than the three fixes: **a passage and the questions about
it are one object.** Editing the passage alone leaves questions quoting text that is no
longer there — a defect worse than the one repaired, because it is invisible to every
check we have and visible to every teacher who opens the item. `repair_passage_fidelity`
declared two such edits and missed three, which is a 40% miss rate on a hand pass.

TWO DIFFERENT CURES, and the choice is not arbitrary:

  EXTEND THE PASSAGE  where the questions were right and the quote was cut too short.
                      ch 09 p07's original passage ran surgery → Rio; the fidelity pass
                      replaced it with p.139 alone because that is where the *paraphrase*
                      matched. pp.139–140 is one continuous span in the book, so quoting
                      both restores the item's own scope without inventing anything.
  EDIT THE QUESTION   where the question quoted our prose. ch 15's Q3 and ch 09 p09's Q3
                      are re-grounded on what the book actually says.

    python3 genon/repair_question_residue.py --list
    python3 genon/repair_question_residue.py --apply
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

B = "data/content/saved_plans/english/ix/"

# ch 09, pp.139–140 — one continuous span, the item's original scope restored.
CH09_P07_STIMULUS = (
    "From the interview (pp.139–140):\n"
    "“I was 29, an awful tragedy struck me when I was diagnosed with spine tumour. I "
    "underwent a surgery, but misfortune raised its ugly head again. The doctors declared "
    "that I would be bound to a wheelchair for the rest of my life, as I was paralysed waist "
    "down. I had two choices—squander my life in remorse or transform it to a world of "
    "limitless possibilities. I love sports and had been a swimmer too, so I decided to "
    "switch to para-athletics. This is how my Paralympics journey began. My breakthrough "
    "moment came in the 2016 Rio Paralympic Games, when I secured the silver medal in the "
    "shot-put event. In hindsight, I feel it was a moment of personal victory and a step "
    "forward in changing perceptions.”"
)

REPAIRS = [
 {"file": B+"ch_09_canonical_p07.json", "item_id": "Q-RFC-A-1",
  "why": "Q2 and Q3 were written for a passage running surgery → Rio. The fidelity pass cut "
         "it to p.139 because that is where the PARAPHRASE matched, leaving both questions "
         "pointing outside the quote. pp.139–140 is one continuous span in the book, so the "
         "fix is to quote the whole of it — the questions were never wrong.",
  "stimulus": CH09_P07_STIMULUS,
  "element_edits": [
    {"index": 0,
     "before": "Identifies 'decision' and 'defining moment' as signalling agency, not victimhood.",
     "after": "Identifies the framing as a CHOICE — 'I had two choices' — as signalling "
              "agency rather than victimhood.",
     "why": "'decision' and 'defining moment' were ours; the book's own framing device is "
            "the two choices, which Q1 now quotes."}]},

 {"file": B+"ch_15_canonical_p05.json", "item_id": "Q-RFC-A-2",
  "why": "Q3 quoted our paraphrase as the mother's words.",
  "question_edits": [
    {"before": "3. The mother writes that when stamina falters, 'the prospect of success "
               "provides the necessary momentum.' Evaluate whether this claim is adequately "
               "supported elsewhere in the letter, citing a specific detail.",
     "after":  "3. The mother writes that “When stamina is running out, the prospect of "
               "success will keep you on track.” Evaluate whether this claim is adequately "
               "supported elsewhere in the letter, citing a specific detail.",
     "why": "The quotation is now the letter's own sentence (p.233). Q1 and Q2 are left "
            "alone deliberately: they SUPPLY their detail (Raffles College, the "
            "book-publishing disclosure) and ask about its purpose, so they stay answerable "
            "even though those details sit beyond the quoted span."}]},

 {"file": B+"ch_09_canonical_p09.json", "item_id": "Q-RFC-A-2",
  "why": "Q3 and guide element 3 referred to the two-choices sentence, which left with the "
         "splice. Both are re-grounded on the first extract, which IS in the stimulus.",
  "question_edits": [
    {"before": "3. Dr. Malik says the Paralympics “has given me a new lease of life”. "
               "Explain what this phrase means, in the light of the two choices she describes.",
     "after":  "3. Dr. Malik says the Paralympics “has given me a new lease of life”. "
               "Explain what this phrase means, in the light of the journey she describes in "
               "the first extract.",
     "why": "The first extract runs swimmer → para-athletics → Rio silver, which is the "
            "transformation the phrase names."}],
  "element_edits": [
    {"index": 3,
     "before": "Evaluates the title: 'limitless possibilities' mirrors the two-choices moment "
               "and her philosophy of ability beyond disability.",
     "after": "Evaluates the title: 'limitless possibilities' mirrors the journey the first "
             "extract describes — swimmer to Paralympic medallist — and her philosophy of "
             "ability beyond disability.",
     "why": "Same residue as Q3."}]},
]


def items_of(doc):
    from aruvi_core.genon.carriers import raw_item_list          # noqa: E402
    return raw_item_list(doc.get("result", doc))


def apply_one(doc, spec):
    hit = [i for i in items_of(doc)
           if isinstance(i, dict) and i.get("id") == spec["item_id"]]
    if len(hit) != 1:
        raise SystemExit(f"ABORT: {spec['item_id']} matched {len(hit)} items")
    it = hit[0]
    out = {"item_id": spec["item_id"]}

    if spec.get("stimulus"):
        cur = it.get("visual_stimulus") or ""
        if not cur.startswith("From the interview (p.139)"):
            raise SystemExit(f"ABORT: {spec['item_id']} stimulus is not the p.139-only "
                             f"version this extension expects")
        it["visual_stimulus"] = spec["stimulus"]
        out["stimulus_extended"] = {"from": len(cur.split()), "to": len(spec["stimulus"].split())}

    for qe in spec.get("question_edits", []):
        stem = it.get("item_stem") or ""
        if qe["before"] not in stem:
            raise SystemExit(f"ABORT: {spec['item_id']} question not found:\n"
                             f"  {qe['before'][:100]!r}")
        it["item_stem"] = stem.replace(qe["before"], qe["after"], 1)
        out.setdefault("questions_edited", []).append(qe["after"][:40])

    for ee in spec.get("element_edits", []):
        els = (it.get("teacher_guide") or {}).get("expected_elements") or []
        i = ee["index"]
        if i >= len(els) or els[i] != ee["before"]:
            raise SystemExit(f"ABORT: {spec['item_id']} element[{i}] is "
                             f"{els[i][:70] if i < len(els) else '<missing>'!r}, expected "
                             f"{ee['before'][:70]!r}")
        els[i] = ee["after"]
        out.setdefault("elements_edited", []).append(i)
    return out


def main() -> int:
    listing = "--list" in sys.argv
    if not listing and "--apply" not in sys.argv:
        print("usage: repair_question_residue.py --list | --apply")
        return 2
    for spec in REPAIRS:
        path = REPO / spec["file"]
        print(f"\n=== {spec['file']}  ·  {spec['item_id']}")
        print(f"    why: {spec['why']}")
        if spec.get("stimulus"):
            print(f"    STIMULUS EXTENDED -> {spec['stimulus'][:88]}…")
        for qe in spec.get("question_edits", []):
            print(f"    Q  -  {qe['before'][:92]}")
            print(f"       +  {qe['after'][:92]}")
            print(f"      why: {qe['why']}")
        for ee in spec.get("element_edits", []):
            print(f"    ELEMENT[{ee['index']}]  -  {ee['before'][:88]}")
            print(f"                   +  {ee['after'][:88]}")
            print(f"      why: {ee['why']}")
        if listing:
            continue
        if not path.is_file():
            print("    SKIPPED — not on disk")
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        if any(r.get("kind") == "question_residue"
               for r in (doc.get("genon_canonical") or {}).get("repairs", [])):
            print("    SKIPPED — already applied")
            continue
        shutil.copy2(path, path.with_suffix(".json.bak_pre_residue"))
        done = apply_one(doc, spec)
        doc.setdefault("genon_canonical", {}).setdefault("repairs", []).append({
            "tool": "repair_question_residue.py", "kind": "question_residue",
            "at": datetime.now().isoformat(timespec="seconds"),
            "why": "Questions and mark-scheme elements were left pointing at text the "
                   "passage-fidelity pass had removed. A passage and its questions are one "
                   "object; editing the passage alone leaves the questions quoting nothing.",
            "items": [done]})
        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"    APPLIED — {json.dumps(done, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
