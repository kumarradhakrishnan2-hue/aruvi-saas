#!/usr/bin/env python3
"""repair_stem_option_echo.py — delete the option list a stem repeats (v1.0, 2026-08-14).

FOUNDER, 2026-08-14: "in simple MCQs this does not happen." An item's options live in
`options[]`, and that array is what the renderer prints. When the model ALSO writes the
options into `item_stem` as an A–D list, the teacher sees them twice — and after STEP 6 she
sees them twice with DIFFERENT LETTERS, because `normalize_options.py` sorts and relabels
the array and cannot reach into prose. On english·ix ch 6, 8 and 15 the stem's echo names a
different letter as the answer than the array does. That is not cosmetic duplication; it is
a wrong answer key printed next to the right one, and it is the same failure mode as
ARV-D-092 (diagnostics left behind by the sort) in a third container.

The stem is the wrong place for the list in every case, so the fix is DELETION, never
re-lettering: one source of truth, and it is the array.

WHAT MAKES THE DELETION SAFE, and why this is a repair rather than authoring. Nothing is
written. Each removed line is asserted to be a VERBATIM echo of an option already on disk —
strip the "A. " prefix and the remainder must equal some `options[i]["text"]` exactly — so a
line that carries any prose of its own cannot be deleted by this tool. And the stem that
remains after the echoes are dropped must equal the declared `stem_after` character for
character, so the declaration cannot quietly rewrite the question while it is in there.

NOT IN SCOPE. ch 16 `Q-RFC-B-1` (EXTRACT_ANALYSIS) also prints an A–D list in its stem, but
its `options[]` is EMPTY — the list in the stem is the only option set there is, and its
second sub-question has none at all. Deleting that list would destroy the item. It needs the
amend_item_options.py treatment (authored), not this one, and is left untouched deliberately.

    python3 genon/repair_stem_option_echo.py --list
    python3 genon/repair_stem_option_echo.py --apply
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

ECHO = re.compile(r"^\s*([A-D])[.)]\s+(.*)$")

# THE SAME ECHO, ALL ON ONE LINE (2026-08-14). ch 11 p11 writes its four choices as
#   "A. Sitar   B. Sarod   C. Veena   D. Santoor"
# — one line, four markers. The line-based ECHO above captures that as a single body
# ("Sitar   B. Sarod   …"), matches no option, and the tool correctly REFUSES the file
# rather than deleting prose it cannot account for. Failing safe is right; failing safe
# forever is not. This splits a run of inline markers so each piece can be checked against
# the options individually, and the line is dropped only if EVERY piece is a verbatim echo.
INLINE = re.compile(r"(?:(?<=^)|(?<=\s))([A-D])[.)]\s+")


def inline_echo_bodies(line):
    """(lead, [(label, body), …]) for a line holding a RUN of inline options, else None.

    `lead` is any prose before the first marker and is always preserved — a line reading
    "Choose one:  A. x  B. y" keeps its instruction and loses only the choices.
    """
    marks = list(INLINE.finditer(line))
    if len(marks) < 2:                     # a single marker is the line-based case
        return None
    lead = line[:marks[0].start()].strip()
    out = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(line)
        out.append((m.group(1), line[m.end():end].strip()))
    return lead, out

REPAIRS = [
 # ── WAVE 2 COMPACTS (2026-08-14). Same three shapes as the tops, one wave later. The two
 # compound items use a DIFFERENT grouped notation from wave 1 ("Q1-A" vs "1A") — see
 # aruvi_core/compound_options.py; the display layer matches the shape, not the spelling,
 # so nothing here depends on which one a run invents.
 {"file": "data/content/saved_plans/english/ix/ch_05_canonical_p06.json",
  "item_id": "Q-LIS-A-1",
  "why": ("Compound listening MCQ (labels Q1-A…Q2-D): both sub-questions' choices are printed "
          "in the stem AND carried in options[]. STEP 6 correctly REFUSED this item — the "
          "grouped-label guard held and the option texts still agree with the stem verbatim, "
          "so nothing is being recovered here, only de-duplicated."),
  "stem_after": (
    "Listen to the dialogue between Rohan and Priya. Then choose the correct answer for each "
    "question below.\n\n"
    "(1) Who first mentions that Grandma likes sitting in the verandah in the evenings?\n\n"
    "(2) What type of pankha does Priya suggest after they narrow down their options?"),
 },
 {"file": "data/content/saved_plans/english/ix/ch_11_canonical_p11.json",
  "item_id": "Q-LIS-A-1",
  "why": ("Same shape, and the reason the tool needed the INLINE branch: this stem writes all "
          "four choices on ONE line ('A. Sitar   B. Sarod   C. Veena   D. Santoor'), which the "
          "line-based matcher read as a single unmatched body and refused."),
  "stem_after": (
    "Listen to the musician's description of the yazh. Then select the correct option for each "
    "question below.\n\n"
    "(1) The yazh is described as the ancestor of which modern Indian instrument?\n\n"
    "(2) According to the description, what material were the strings of the yazh made from?"),
 },
 {"file": "data/content/saved_plans/english/ix/ch_05_canonical_p08.json",
  "item_id": "Q-RFC-A-1",
  "why": ("Simple MCQ whose stem echoes its own options, and the letters DISAGREE with the "
          "array after STEP 6 sorted it: stem A is array D, stem C is array A, stem D is array "
          "C. Only B agrees — and B is the answer, so the key is not wrong, but three of the "
          "four letters mislead a teacher reading the stem."),
  "stem_after": (
    "Which of the following statements best explains why pankhas from different regions of "
    "India can be distinguished from one another?"),
 },
 {"file": "data/content/saved_plans/english/ix/ch_05_canonical.json",
  "item_id": "Q-LST-A-1",
  "why": ("Compound listening item: both sub-questions' option sets are printed in the stem "
          "AND carried in options[] as 1A–2D. The stem's copy was the evidence used to "
          "restore the authored map (repair_compound_mcq.py, ARV-D-156); that job is done "
          "and the evidence is preserved in that tool's declaration and in "
          "ch_05_canonical.json.bak_pre_compound. The echo now only duplicates."),
  "stem_after": (
    "After listening to the conversation between Rohan and Priya, choose the correct answer "
    "for each question.\n"
    "1. Which of the following best describes the pankha Priya proposes as a suitable gift?\n"
    "2. Why does Rohan raise a concern about the brass fans Priya first mentions?"),
 },
 {"file": "data/content/saved_plans/english/ix/ch_06_canonical.json",
  "item_id": "Q-RFC-B-1",
  "why": ("The stem's echo contradicts the array: it letters 'Just as brushstrokes leave "
          "marks…' as B, and that text is D in options[]. STEP 6 sorted the array; the prose "
          "kept the pre-sort letters."),
  "stem_after": (
    "In the poem, the poet compares seeds to brushstrokes. Which of the following statements "
    "best explains why this comparison works?"),
 },
 {"file": "data/content/saved_plans/english/ix/ch_08_canonical.json",
  "item_id": "Q-RFC-B-1",
  "why": ("Same contradiction: the stem letters 'Stanza 1 — visual; Stanza 2 — auditory; "
          "Stanza 3 — olfactory' as C, and that text is D in options[]."),
  "stem_after": (
    "In Tagore's poem, each of the three stanzas is anchored to a different human sense. "
    "Which of the following correctly pairs the stanza with its dominant sense?"),
 },
 {"file": "data/content/saved_plans/english/ix/ch_15_canonical.json",
  "item_id": "Q-RFC-A-1",
  "why": ("Same contradiction: the stem letters 'To establish that greatness requires "
          "sustained effort, not passion alone' as B, and that text is C in options[]."),
  "stem_after": (
    "In her letter to Ming, the mother states that world-class mastery in any field demands "
    "at least ten years of singular, intensive pursuit. Which of the following best explains "
    "why she includes this claim at the opening of her argument?"),
 },
]


def items_of(doc):
    from aruvi_core.genon.carriers import raw_item_list        # noqa: E402
    return raw_item_list(doc.get("result", doc))


def apply_one(doc, spec):
    hit = [i for i in items_of(doc) if isinstance(i, dict) and i.get("id") == spec["item_id"]]
    if len(hit) != 1:
        raise SystemExit(f"ABORT: {spec['item_id']} matched {len(hit)} items, expected 1")
    it = hit[0]
    opts = it.get("options") or []
    if not opts:
        raise SystemExit(f"ABORT: {spec['item_id']} has no options[] — the stem's list would "
                         f"be the only option set; this tool must not delete it")
    texts = {o["text"] for o in opts}

    kept, dropped = [], []
    for line in (it.get("item_stem") or "").splitlines():
        m = ECHO.match(line)
        if m and m.group(2).strip() in texts:
            dropped.append((m.group(1), m.group(2).strip()))
            continue
        run = inline_echo_bodies(line)
        if run and all(body in texts for _, body in run[1]):
            lead, pieces = run
            dropped += pieces
            if lead:                       # an instruction before the choices survives
                kept.append(lead)
            continue
        if m or (run and any(body in texts for _, body in run[1])):
            raise SystemExit(f"ABORT: {spec['item_id']} stem line {line.strip()[:60]!r} looks "
                             f"like an option but matches no option text — it may carry prose "
                             f"of its own; refusing to delete it")
        kept.append(line)
    if not dropped:
        raise SystemExit(f"ABORT: {spec['item_id']} has no echoed option lines to remove")

    rebuilt = "\n".join(kept).strip()
    rebuilt = re.sub(r"\n{3,}", "\n\n", rebuilt)
    if rebuilt != spec["stem_after"]:
        raise SystemExit(f"ABORT: {spec['item_id']} stem after removal is not the declared "
                         f"text.\n  computed: {rebuilt!r}\n  declared: {spec['stem_after']!r}")
    it["item_stem"] = rebuilt

    if len(dropped) != len(opts):
        # Not fatal — a compound item echoes each sub-question's set — but it must be seen.
        print(f"    NOTE: removed {len(dropped)} echoed line(s) against {len(opts)} option(s)")
    return {"item_id": spec["item_id"],
            "removed": [f"{lab}. {txt[:48]}" for lab, txt in dropped]}


def main() -> int:
    listing = "--list" in sys.argv
    if not listing and "--apply" not in sys.argv:
        print("usage: repair_stem_option_echo.py --list | --apply")
        return 2
    by_file = {}
    for spec in REPAIRS:
        by_file.setdefault(spec["file"], []).append(spec)
    for rel, specs in by_file.items():
        path = REPO / rel
        print(f"\n=== {rel}")
        for s in specs:
            print(f"    {s['item_id']}\n    why: {s['why']}")
            print(f"    stem after:\n      " + s["stem_after"].replace("\n", "\n      "))
        if listing:
            continue
        if not path.is_file():
            print("    SKIPPED — not on disk")
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        if any(r.get("kind") == "stem_option_echo"
               for r in (doc.get("genon_canonical") or {}).get("repairs", [])):
            print("    SKIPPED — already repaired")
            continue
        shutil.copy2(path, path.with_suffix(".json.bak_pre_stem_echo"))
        done = [apply_one(doc, s) for s in specs]
        doc.setdefault("genon_canonical", {}).setdefault("repairs", []).append({
            "tool": "repair_stem_option_echo.py", "kind": "stem_option_echo",
            "at": datetime.now().isoformat(timespec="seconds"),
            "why": "The stem repeated the item's own options as an A–D list. After STEP 6 "
                   "sorted and relabelled options[], that echo named a different letter as "
                   "the answer. Deleted; options[] is the single source of truth. Every "
                   "removed line was a verbatim echo of an option on disk.",
            "items": done,
        })
        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"    APPLIED — {json.dumps(done, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
