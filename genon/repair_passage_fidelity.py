#!/usr/bin/env python3
"""repair_passage_fidelity.py — make every quoted passage the book's actual words, and mark
it as a quotation (v1.0, 2026-08-14, S11 · F2).

FOUNDER RULING, 2026-08-14, after visual clearance of
`docs/batch_evidence/english_ix_passage_transcriptions.md`:

    "Where it is textbook content involved, in all these cases place them in inverted
     commas. If it is paraphrasing don't. If it is textbook content and erroneous, replace
     with the text shown by you in the file."

So three states, and the tool applies exactly one to each passage:

  QUOTE    the passage already matches the book → wrap in inverted commas, name the page.
  REPLACE  the passage claims to be the book and is not → substitute the transcribed text,
           wrap, name the page.
  LEAVE    the passage is our own prose → no quotation marks, because quoting it would
           assert authorship the text does not have. Untouched by this tool.

THE TRANSCRIPTIONS ARE HAND-READ, NOT EXTRACTED, and that is load-bearing. `pdfplumber`
folds the marginal glossary into the body line by line — ch 11's "I realise that my fears
were baseless" comes out as "…my fears were root show baseless", picking up the gutter
entry `root: show support`. Every passage below was read off the page and typed. The
transcription file is the evidence record; this tool is its application.

NESTED QUOTATION. A block wrapped in “ ” whose dialogue also uses “ ” is unreadable, so
inner dialogue is set in ‘ ’ — the standard nesting convention, and the one the NCERT book
itself uses for speech inside speech. Punctuation is the only thing altered; no word moves.

★ THREE QUESTIONS MOVE WITH THEIR PASSAGE, and they are declared here rather than left to
be discovered. A question that quotes text the passage no longer contains is a worse defect
than the one being fixed:

  ch 13 std Q1 asked about "integral threads in India's social fabric" — OUR paraphrase.
        The book (p.210) says "part and parcel of our social fabric". The question is
        better for the change: it now asks about the author's actual idiom.
  ch 09 p07 Q1 quoted "a defining moment — not a moment of despair, but one of decision",
        which is our paraphrase of p.139. Re-grounded on the book's own "two choices".
  ch 09 p09 keeps BOTH of the book's numbered extracts, labelled as the book labels them,
        because Q3 and Q4 depend on Extract 1. The defect there was never that both were
        present — it was that they were spliced into one continuous quotation.

    python3 genon/repair_passage_fidelity.py --list
    python3 genon/repair_passage_fidelity.py --apply
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

D = "“"    # “
DD = "”"   # ”
S = "‘"    # ‘
SS = "’"   # ’


def q(body, source):
    """Wrap a passage as a quotation, nesting any inner dialogue in single marks."""
    body = body.replace(D, S).replace(DD, SS)
    return f"{source}\n{D}{body}{DD}"


# ── ch 01 · pp.8–9 ──────────────────────────────────────────────────────────────────
CH01 = (
    "The Dassara festival came as usual. Secretly I bought Kashi Yatre which had been "
    "published as a novel by that time. My grandmother called me to the puja place and made "
    "me sit down on a stool. She gave me a gift of frock material. Then she did something "
    "unusual. She bent down and touched my feet. I was surprised and taken aback. Elders "
    "never touch the feet of youngsters. We have always touched the feet of God, elders, and "
    "teachers. We consider that as a mark of respect. It is a great tradition but today the "
    "reverse had happened. It was not correct.\n"
    "She said, ‘I am touching the feet of a teacher, not my granddaughter; a teacher who "
    "taught me so well, with so much of affection that I can read any novel confidently in "
    "such a short period. Now I am independent. It is my duty to respect a teacher. Is it not "
    "written in our scriptures that a teacher should be respected, irrespective of the gender "
    "and age?’\n"
    "I did return her namaskara to her by touching her feet and gave my gift to my first "
    "student. She opened it and read immediately the title Kashi Yatre by Triveni and the "
    "publisher’s name. I knew then that my student had passed with flying colours."
)

# ── ch 07 · p.102 ───────────────────────────────────────────────────────────────────
CH07_STD = (
    "Off he went, twirling his walking stick jauntily, leaving Ravi in a dilemma. His "
    "grandfather would feel hurt if he insisted on accompanying him and his mother would be "
    "furious if she knew Ravi had let him go out on his own."
)

# ── ch 07 · pp.107–108 ──────────────────────────────────────────────────────────────
CH07_P10 = (
    "“I had a quiet morning, but I don’t know about Ravi. He just disappeared "
    "instead of staying at home to look after me like you told him to,” answered Grandpa "
    "coolly, while Ravi just looked confused and embarrassed.\n"
    "Grandpa had another surprise for Ravi. A gift-wrapped parcel!\n"
    "“But, Papa, Ravi’s birthday was three months ago. Have you forgotten?” "
    "exclaimed Ravi’s mother, impatiently.\n"
    "“No. But you know I always give a gift to every child in the house on my birthday. "
    "Have you forgotten?” countered Grandpa, very seriously."
)

# ── ch 09 · pp.139–140 (already exact) ──────────────────────────────────────────────
CH09_STD = (
    "I had two choices—squander my life in remorse or transform it to a world of "
    "limitless possibilities. I love sports and had been a swimmer too, so I decided to "
    "switch to para-athletics. This is how my Paralympics journey began. My breakthrough "
    "moment came in the 2016 Rio Paralympic Games, when I secured the silver medal in the "
    "shot-put event. In hindsight, I feel it was a moment of personal victory and a step "
    "forward in changing perceptions."
)

# ── ch 09 · p.139 ───────────────────────────────────────────────────────────────────
CH09_P07 = (
    "I was 29, an awful tragedy struck me when I was diagnosed with spine tumour. I underwent "
    "a surgery, but misfortune raised its ugly head again. The doctors declared that I would "
    "be bound to a wheelchair for the rest of my life, as I was paralysed waist down. I had "
    "two choices—squander my life in remorse or transform it to a world of limitless "
    "possibilities."
)

# ── ch 09 · p.145, BOTH numbered extracts, as the book sets them ────────────────────
CH09_P09 = (
    "1. I love sports and had been a swimmer too, so I decided to switch to para-athletics. "
    "This is how my Paralympics journey began. My breakthrough moment came in the 2016 Rio "
    "Paralympic Games, when I secured the silver medal in the shot-put event. In hindsight, I "
    "feel it was a moment of personal victory and a step forward in changing perceptions.\n"
    "2. Honestly, I feel sports, especially Paralympics, have the extraordinary ability to "
    "challenge stereotypes and change attitudes towards disability. When people witness the "
    "strength, skill, and competitive spirit of para-athletes, it breaks down preconceived "
    "notions. Paralympics has given me a new lease of life and helped me push boundaries."
)

# ── ch 11 · pp.180–181 ──────────────────────────────────────────────────────────────
CH11 = (
    "leela: Your own father, Shruti, had to go against his family’s wishes to play the "
    "violin. His was a family of vocalists. Your grandfather, his father, and your uncles were "
    "all vocalists belonging to a highly traditional school. They painstakingly nurtured the "
    "flame of musical heritage and kept it alive through thick and thin. Nabin’s desire "
    "to take up a Western instrument rather than cultivating his voice was painful to his "
    "father. You see, at that time the violin had not yet been incorporated into classical "
    "Indian music. Your grandfather saw this choice as a kind of betrayal of family values and "
    "tradition. But your father worked his fingers to the bone and see where the violin got "
    "him.\n"
    "nabIn: I underestimated the power of our own music. I was afraid you would be lost to us. "
    "I realise that my fears were baseless. After all each bay, its own wind. I trust you "
    "Shruti and I will root for your group at the concert!\n"
    "(Shruti hugs both of her parents)\n"
    "CURTAIN DOWN"
)

# ── ch 13 · pp.209–210 ──────────────────────────────────────────────────────────────
CH13 = (
    "There is one letter delivery he dreads. The envelope with the right corner torn off, "
    "which signifies that the missive bears news of death. “Ashubh Samachar cannot be "
    "carried into the house,” says Khetaram. So, he stands outside, reads out the letter "
    "twice, then tears it to bits. “Bad news must be destroyed,” he mutters "
    "philosophically.\n"
    "People like Khetaram are a part and parcel of our social fabric, and are a great support! "
    "Our salute to all the people like Khetaram!"
)

# ── ch 15 · pp.232–233 ──────────────────────────────────────────────────────────────
CH15 = (
    "It starts with a passion for a particular interest, then comes the conviction that it is "
    "imperative to realise it. Count the cost in years of effort, financial investments and "
    "sacrifice. Then if it is still burning in your blood and you are ready to commit yourself "
    "to the task, plunge. It could be in any field—sports, science, arts, business, or "
    "design. The road may be uphill most of the way and often you are buoyed up only by the "
    "knowledge that you are doing what you love best and are doing the right thing. When "
    "stamina is running out, the prospect of success will keep you on track."
)

B = "data/content/saved_plans/english/ix/"

REPAIRS = [
 # ── QUOTE ONLY — already the book's words ───────────────────────────────────────
 {"file": B+"ch_03_canonical.json", "item_id": "Q-RFC-A-2", "mode": "quote",
  "source": "From the story (p.43):", "why": "88% verbatim; differs only in page furniture."},
 {"file": B+"ch_03_canonical_p11.json", "item_id": "Q-RFC-A-2", "mode": "quote",
  "source": "From the story (p.43):", "why": "88% verbatim; differs only in page furniture."},
 {"file": B+"ch_07_canonical_p14.json", "item_id": "Q-RFC-A-1", "mode": "quote",
  "source": "From the story (p.109):", "why": "95% verbatim; differs only in page furniture."},
 {"file": B+"ch_13_canonical_p09.json", "item_id": "Q-RFC-A-2", "mode": "quote",
  "source": "From the chapter (p.209):",
  "why": "100% verbatim. NOTE the page: p.209 is the prose; p.211, which we had recorded, "
         "is the exercise page that re-quotes it."},
 {"file": B+"ch_13_canonical_p12.json", "item_id": "Q-RFC-A-2", "mode": "quote",
  "source": "From the chapter (p.209):", "why": "100% verbatim; page corrected 211 -> 209."},

 # ── REPLACE — claims to be the book and is not ──────────────────────────────────
 {"file": B+"ch_01_canonical.json", "item_id": "Q-RFC-A-2", "mode": "replace",
  "text": CH01, "source": "From the story (pp.8–9):",
  "why": "The middle was ours entirely. The book's actual middle is the feet-touching — "
         "which is what this item's own Q1 asks about, and which our passage omitted. The "
         "replacement makes an unanswerable question answerable."},
 {"file": B+"ch_07_canonical.json", "item_id": "Q-RFC-A-1", "mode": "replace",
  "text": CH07_STD, "source": "From the story (p.102):",
  "why": "The second sentence was ours and changed the meaning: the book's dilemma is "
         "Grandpa's feelings against his mother's fury, not dignity against an unsafe city."},
 {"file": B+"ch_07_canonical_p10.json", "item_id": "Q-RFC-A-2", "mode": "replace",
  "text": CH07_P10, "source": "From the story (pp.107–108):",
  "why": "The closing line was ours. The book has Grandpa COUNTERING — turning 'Have you "
         "forgotten?' back on her — which is the joke our version lost."},
 {"file": B+"ch_09_canonical.json", "item_id": "Q-RFC-A-1", "mode": "quote",
  "source": "From the interview (pp.139–140):",
  "why": "Already exact — the 76% score was an artefact of the span crossing a page "
         "break. Quotation marks only."},
 {"file": B+"ch_09_canonical_p07.json", "item_id": "Q-RFC-A-1", "mode": "replace",
  "text": CH09_P07, "source": "From the interview (p.139):",
  "why": "The opening 35 words were paraphrase, and dropped the tumour and her age.",
  "question_edit": {
     "before": "1. Dr. Malik calls the moment after her surgery “a defining moment — "
               "not a moment of despair, but one of decision”. What does this choice of "
               "words reveal about how she wants her situation to be understood?",
     "after":  "1. Dr. Malik says she ‘had two choices—squander my life in remorse "
               "or transform it to a world of limitless possibilities’. What does "
               "framing her situation as a choice reveal about how she wants it to be "
               "understood?",
     "why": "Q1 quoted our paraphrase, which the replacement removes. Re-grounded on the "
            "book's own sentence, which carries the same agency the question is after."}},
 {"file": B+"ch_09_canonical_p09.json", "item_id": "Q-RFC-A-2", "mode": "replace",
  "text": CH09_P09, "source": "From the interview (p.145):",
  "why": "Two non-contiguous extracts were spliced into one continuous quotation. Both are "
         "kept — Q3 and Q4 depend on the first — but numbered 1 and 2 exactly as "
         "the book sets them, so nothing claims to run on from anything else."},
 {"file": B+"ch_11_canonical.json", "item_id": "Q-RFC-A-2", "mode": "replace",
  "text": CH11, "source": "From the play, Act III (pp.180–181):",
  "why": "The worst of the nine: an invented line ('You never lost sight of the raga notes'), "
         "an invented stage direction, the play's title line dropped ('each bay, its own "
         "wind'), the speakers reversed, and Leela's ordinary speech relabelled an ASIDE — "
         "in the chapter whose textbook teaches the aside convention on p.184 using the play's "
         "ONE real aside, which is Shruti's."},
 {"file": B+"ch_13_canonical.json", "item_id": "Q-RFC-A-2", "mode": "replace",
  "text": CH13, "source": "From the chapter (pp.209–210):",
  "why": "Our own critical gloss was appended to the quotation. The book's own tribute "
         "sentence (p.210) replaces it.",
  "question_edit": {
     "before": "1. What does the phrase 'integral threads in India's social fabric' tell us "
               "about the author's view of workers like Khetaram? Identify the figure of "
               "speech used and explain its effect.",
     "after":  "1. What does the phrase ‘a part and parcel of our social fabric’ "
               "tell us about the author's view of workers like Khetaram? Identify the figure "
               "of speech used and explain its effect.",
     "why": "Q1 asked about OUR paraphrase. The book's idiom is 'a part and parcel of our "
            "social fabric' (p.210) — still a figure of speech, so the question works "
            "better against the author's actual words."}},
 {"file": B+"ch_15_canonical_p05.json", "item_id": "Q-RFC-A-2", "mode": "replace",
  "text": CH15, "source": "From the letter by Irene Chua (pp.232–233):",
  "why": "Three sentences were paraphrase carried under an EXPLICIT attribution, and the page "
         "range was wrong (we had 235–236; the letter is pp.232–234)."},
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
    cur = it.get("visual_stimulus") or ""
    # Only a QUOTE pass can be a no-op re-run; a REPLACE overwrites whatever is there, and
    # ch 15 p05 arrives already carrying an attribution line — "From the letter by Irene Chua
    # (p.235–236):" — which is itself part of the defect, since that page range is wrong and
    # the text under it is paraphrase. Blocking on the prefix refused the one item that most
    # needed replacing.
    if spec["mode"] == "quote" and (cur.lstrip().startswith("From ") or cur.lstrip().startswith(D)):
        raise SystemExit(f"ABORT: {spec['item_id']} already quoted")
    body = spec["text"] if spec["mode"] == "replace" else cur
    it["visual_stimulus"] = q(body, spec["source"])
    out = {"item_id": spec["item_id"], "mode": spec["mode"], "source": spec["source"],
           "words_before": len(cur.split()), "words_after": len(body.split())}
    qe = spec.get("question_edit")
    if qe:
        stem = it.get("item_stem") or ""
        if qe["before"] not in stem:
            raise SystemExit(f"ABORT: {spec['item_id']} question text to edit not found:\n"
                             f"  {qe['before'][:90]!r}")
        it["item_stem"] = stem.replace(qe["before"], qe["after"], 1)
        out["question_edited"] = True
    return out


def main() -> int:
    listing = "--list" in sys.argv
    if not listing and "--apply" not in sys.argv:
        print("usage: repair_passage_fidelity.py --list | --apply")
        return 2
    by_file = {}
    for s in REPAIRS:
        by_file.setdefault(s["file"], []).append(s)
    n_q = n_r = 0
    for rel, specs in by_file.items():
        path = REPO / rel
        print(f"\n=== {rel}")
        for s in specs:
            print(f"    {s['item_id']}  {s['mode'].upper()}  ->  {s['source']}")
            print(f"      why: {s['why']}")
            if s.get("question_edit"):
                print(f"      Q EDIT  -  {s['question_edit']['before'][:88]}")
                print(f"              +  {s['question_edit']['after'][:88]}")
                print(f"          why: {s['question_edit']['why']}")
            n_q += s["mode"] == "quote"
            n_r += s["mode"] == "replace"
        if listing:
            continue
        if not path.is_file():
            print("    SKIPPED — not on disk")
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        if any(r.get("kind") == "passage_fidelity"
               for r in (doc.get("genon_canonical") or {}).get("repairs", [])):
            print("    SKIPPED — already applied")
            continue
        shutil.copy2(path, path.with_suffix(".json.bak_pre_fidelity"))
        done = [apply_one(doc, s) for s in specs]
        doc.setdefault("genon_canonical", {}).setdefault("repairs", []).append({
            "tool": "repair_passage_fidelity.py", "kind": "passage_fidelity",
            "at": datetime.now().isoformat(timespec="seconds"),
            "why": "Founder ruling 2026-08-14 after visual clearance of "
                   "docs/batch_evidence/english_ix_passage_transcriptions.md: textbook "
                   "content is set in inverted commas with its page; where it claimed to be "
                   "the book and was not, it was replaced with the hand-transcribed text.",
            "items": done})
        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"    APPLIED — {len(done)} item(s)")
    print(f"\n=== {n_q} quoted · {n_r} replaced ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
