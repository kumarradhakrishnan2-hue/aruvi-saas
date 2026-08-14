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

REPAIRS = [
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
        if m:
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
