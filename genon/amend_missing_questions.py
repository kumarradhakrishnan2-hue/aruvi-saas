#!/usr/bin/env python3
"""amend_missing_questions.py — write the questions an item forgot to ask
(v1.0, 2026-08-14, S11).

★ THIS TOOL AUTHORS TEXT, like amend_item_options.py and unlike every repair_*.py.

THE DEFECT. Four english·ix EXTRACT_ANALYSIS items carry a stimulus, carry a mark scheme,
and ask nothing at all:

    item_stem   "Read the following passage and answer the questions below."
    options     []
    questions   — none —
    teacher_guide.expected_elements   4 or 5 detailed criteria

ch 05's is the plainest: it promises "the three questions below it" and carries zero. The
student is told to answer questions that were never written; the teacher has a mark scheme
for an unasked question.

WHY CERTIFICATION PASSED THEM, and it is the interesting part. `build_library` checks
"every non-OPEN_TASK item carries a stem" — and the stem is non-empty, so it passes. **A
non-empty stem is not an answerable item.** Same shape as the `unarranged()` gap found
earlier the same day: a check that measures the letter of a contract while the substance
walks past it. A gate for this belongs in certification, and is the follow-up to this tool.

WHERE THE QUESTIONS COME FROM, and why this is recoverable rather than invention:

  1. THE MARK SCHEME. `expected_elements` states what a good answer contains, so it
     encodes what was meant to be asked. ch 07's "Notes Vidya's response is protective,
     not disrespectful, given the accident" is a question with its answer showing.
  2. THE CHAPTER SUMMARY. Each of these extracts is one the NCERT book itself sets
     questions on, in its Critical Reflection section, and those questions are carried in
     `data/content/chapters/english/ix/summaries/`. The authored questions follow the
     book's own focus for the same extract — ch 07's book asks about Grandpa's emotion and
     why he came to the city despite disliking it; ch 09's asks why she could switch to
     para-athletics "quite comfortably". Writing questions the textbook does not recognise
     would be a second defect, not a fix.
  3. THE LO, which fixes the analytical level.

THE DISCIPLINE THAT MAKES IT CHECKABLE. A question cannot be asserted correct by a machine.
What CAN be asserted is COVERAGE: every declared question names the `expected_elements` it
serves, by index, and the tool refuses unless every element is claimed by at least one
question. So a mark scheme can never end up with a criterion no question asks for — which
is precisely the failure being repaired, in miniature.

    python3 genon/amend_missing_questions.py --list
    python3 genon/amend_missing_questions.py --apply
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

NUMBERED = re.compile(r"(?m)^\s*\(?\d+[.)]\s")

AMENDMENTS = [
 # ── ch 05 · standard · U3 · Q-RFC-A-2 ────────────────────────────────────────────
 # The stem PROMISES THREE, so three are written, and the fourth element is folded into
 # the third question — the book's own Critical Reflection pairs the economic shift with
 # the preservation argument in the same breath ("How might pankha-making workshops
 # contribute to preservation?"), so they belong together rather than split.
 {"file": "data/content/saved_plans/english/ix/ch_05_canonical.json",
  "item_id": "Q-RFC-A-2",
  "lead": "Read the following passage from the chapter and answer the three questions below it.",
  "questions": [
    ("The passage says that pankhas “were considered exotic and stylish”. Is this "
     "statement a fact or an opinion? Give a reason for your answer.", [0]),
    ("The passage states that each region developed distinct varieties “defined by local "
     "materials and intricate designs”. Using one named example from the chapter, explain "
     "what this regional variety reveals about the cultural identity of a place.", [1]),
    ("Pankhas have shifted “from functional to decorative objects”. Explain how this "
     "shift changes the artisan’s economic relationship to the craft, and evaluate whether "
     "celebrating pankha culture is an adequate answer to the threat posed by technology.",
     [2, 3]),
  ],
  "book_basis": ("ch 05's Critical Reflection sets four questions on this same Extract 1, "
                 "including “The sentence 'They were considered exotic and stylish' is an "
                 "opinion and not a fact because…” and “Infer one reason for commonality "
                 "in the use of pankhas across India”; its ECR set asks “How might "
                 "pankha-making workshops contribute to preservation?” Q1 and Q3 follow "
                 "those directly.")},

 # ── ch 07 · p14 · U4 · Q-RFC-A-1 ─────────────────────────────────────────────────
 # The item the founder found. The book sets four questions on this exact extract — the
 # grandfather's emotion, why he hated city life, why he came anyway, and the meaning of
 # "you can even hear a leaf fall" — and the mark scheme's fourth element reaches past the
 # extract to Vidya, which is why Q3 asks the reader to judge her, not just report her.
 {"file": "data/content/saved_plans/english/ix/ch_07_canonical_p14.json",
  "item_id": "Q-RFC-A-1",
  "lead": "Read the following passage and answer the questions below.",
  "questions": [
    ("What does Grandpa’s description of his small brick house — the big mango tree, the "
     "quiet in which “you can even hear a leaf fall” — reveal about why he dislikes "
     "living in the city? Refer to two details from the passage.", [0, 1]),
    ("The passage turns from Grandpa’s longing for his old home to his fall in the garden. "
     "What tension does this turn set up between the independence Grandpa wants and what he "
     "can safely manage alone?", [2]),
    ("Given the accident described at the end of the passage, do you read Vidya’s "
     "insistence that Grandpa not go out alone as protective of him or as disrespectful "
     "towards him? Justify your view.", [3]),
  ],
  "book_basis": ("ch 07's Critical Reflection Extract 1 asks for the emotion Grandpa "
                 "displays, “Grandpa hated the busy and noisy city life because ___”, "
                 "“Why did Grandpa come to the city despite his dislike for city life?” "
                 "and the meaning of “you can even hear a leaf fall”. Q1 gathers the "
                 "first, second and fourth; Q3 answers the third from the other side.")},

 # ── ch 09 · p07 · U2 · Q-RFC-A-1 ─────────────────────────────────────────────────
 {"file": "data/content/saved_plans/english/ix/ch_09_canonical_p07.json",
  "item_id": "Q-RFC-A-1",
  "lead": "Read the following passage and answer the questions below.",
  "questions": [
    ("Dr. Malik calls the moment after her surgery “a defining moment — not a moment of "
     "despair, but one of decision”. What does this choice of words reveal about how she "
     "wants her situation to be understood?", [0]),
    ("Why was she able to switch to para-athletics rather than to some other pursuit? Answer "
     "using a detail from the passage.", [1]),
    ("She calls the 2016 Rio silver medal her “breakthrough”. Explain what it broke "
     "through — both in her own life and in the way others see disability.", [2, 4]),
    ("How would you describe the speaker’s tone in this passage? Support your answer with "
     "one phrase from it.", [3]),
  ],
  "book_basis": ("ch 09's Critical Reflection Extract 1 asks “Why could the speaker switch "
                 "to para-athletics quite comfortably?” and “The speaker calls the 2016 "
                 "Rio Paralympic Games a 'breakthrough moment' because ___”. Q2 and Q3 "
                 "follow those; Q4 mirrors the book's tone question on Extract 2.")},

 # ── ch 09 · p09 · U5 · Q-RFC-A-2 ─────────────────────────────────────────────────
 # This item's stimulus is Extract 2, on which the book asks about tone, the analogy
 # "preconceived notions", and "helped me push boundaries". Its LO is the broadest of the
 # four — fact/opinion, cause-effect, language, AND title — so Q2 is framed explicitly as
 # cause and effect, which is the chapter's own analytical vocabulary.
 {"file": "data/content/saved_plans/english/ix/ch_09_canonical_p09.json",
  "item_id": "Q-RFC-A-2",
  "lead": "Read the passage below and answer the questions that follow.",
  "questions": [
    ("What are the “preconceived notions” Dr. Malik refers to, and about whom are they "
     "held?", [0]),
    ("According to the passage, what causes people’s attitudes towards disability to "
     "change? State the cause and its effect in Dr. Malik’s argument.", [1]),
    ("Dr. Malik says the Paralympics “has given me a new lease of life”. Explain what "
     "this phrase means, in the light of the two choices she describes.", [2]),
    ("The text is titled ‘The World of Limitless Possibilities’. Using this passage — "
     "including what she says about having been a swimmer — explain how well that title "
     "captures Dr. Malik’s outlook.", [3, 4]),
  ],
  "book_basis": ("ch 09's Critical Reflection Extract 2 asks for the speaker's tone, the "
                 "analogy “ability : potential :: preconceived notions : ___” and “What "
                 "does 'helped me push boundaries' tell us about the speaker?”; its ECR set "
                 "asks students to “Rationalise the appropriateness of the title”. Q1 and "
                 "Q4 follow those directly.")},
]


def items_of(doc):
    from aruvi_core.genon.carriers import raw_item_list          # noqa: E402
    return raw_item_list(doc.get("result", doc))


def apply_one(doc, spec):
    hit = [i for i in items_of(doc)
           if isinstance(i, dict) and i.get("id") == spec["item_id"]]
    if len(hit) != 1:
        raise SystemExit(f"ABORT: {spec['item_id']} matched {len(hit)} items, expected 1")
    it = hit[0]
    stem = it.get("item_stem") or ""
    if stem.strip() != spec["lead"].strip():
        raise SystemExit(f"ABORT: {spec['item_id']} stem is {stem[:70]!r}, declaration "
                         f"expects {spec['lead'][:70]!r} — already amended, or another file")
    if NUMBERED.search(stem) or (it.get("options") or []):
        raise SystemExit(f"ABORT: {spec['item_id']} already carries questions or options — "
                         f"refusing to add a second set")

    elements = (it.get("teacher_guide") or {}).get("expected_elements") or []
    if not elements:
        raise SystemExit(f"ABORT: {spec['item_id']} has no expected_elements — there is "
                         f"nothing to derive the questions FROM, so this would be invention")
    claimed = {i for _, idxs in spec["questions"] for i in idxs}
    if any(i >= len(elements) for i in claimed):
        raise SystemExit(f"ABORT: {spec['item_id']} claims an element index that does not "
                         f"exist (has {len(elements)})")
    missing = set(range(len(elements))) - claimed
    if missing:
        raise SystemExit(f"ABORT: {spec['item_id']} leaves expected_elements {sorted(missing)} "
                         f"unasked — the exact defect being repaired: "
                         f"{[elements[i][:60] for i in sorted(missing)]}")
    # the stem's own promise, where it names a count, must match what is written
    m = re.search(r"\b(two|three|four|five)\b\s+questions", spec["lead"], re.I)
    if m:
        want = {"two": 2, "three": 3, "four": 4, "five": 5}[m.group(1).lower()]
        if want != len(spec["questions"]):
            raise SystemExit(f"ABORT: {spec['item_id']} stem promises {m.group(1)} questions "
                             f"but {len(spec['questions'])} are declared")

    body = "\n".join(f"{n}. {q}" for n, (q, _) in enumerate(spec["questions"], 1))
    it["item_stem"] = spec["lead"] + "\n\n" + body
    return {"item_id": spec["item_id"], "questions_added": len(spec["questions"]),
            "elements_covered": sorted(claimed),
            "coverage": {f"Q{n}": idxs for n, (_, idxs) in enumerate(spec["questions"], 1)}}


def main() -> int:
    listing = "--list" in sys.argv
    if not listing and "--apply" not in sys.argv:
        print("usage: amend_missing_questions.py --list | --apply")
        return 2
    for spec in AMENDMENTS:
        path = REPO / spec["file"]
        print(f"\n=== {spec['file']}  ·  {spec['item_id']}   ★ AUTHORED QUESTIONS")
        doc = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None
        elements = []
        if doc:
            hit = [i for i in items_of(doc)
                   if isinstance(i, dict) and i.get("id") == spec["item_id"]]
            if hit:
                elements = (hit[0].get("teacher_guide") or {}).get("expected_elements") or []
        print(f"    {spec['lead']}")
        for n, (q, idxs) in enumerate(spec["questions"], 1):
            print(f"      {n}. {q}")
            for i in idxs:
                if i < len(elements):
                    print(f"           └ serves element {i}: {elements[i]}")
        print(f"    book basis: {spec['book_basis']}")
        if listing:
            continue
        if not path.is_file():
            print("    SKIPPED — not on disk")
            continue
        if any(r.get("kind") == "authored_questions"
               for r in (doc.get("genon_canonical") or {}).get("repairs", [])):
            print("    SKIPPED — already amended")
            continue
        shutil.copy2(path, path.with_suffix(".json.bak_pre_questions"))
        done = apply_one(doc, spec)
        doc.setdefault("genon_canonical", {}).setdefault("repairs", []).append({
            "tool": "amend_missing_questions.py", "kind": "authored_questions",
            "at": datetime.now().isoformat(timespec="seconds"),
            "why": "The item's stem promised questions and carried none, while its "
                   "teacher_guide carried a full mark scheme. Questions AUTHORED from that "
                   "mark scheme and from the NCERT Critical Reflection questions the "
                   "chapter summary records for the same extract. Every expected_element is "
                   "asserted to be claimed by at least one question.",
            "items": [done]})
        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"    APPLIED — {json.dumps(done, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
