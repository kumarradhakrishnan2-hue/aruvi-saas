#!/usr/bin/env python3
"""repair_compound_mcq.py — restore a COMPOUND MCQ's authored label→text map after STEP 6
flattened it (v1.0, 2026-08-14, S11 · english·secondary).

WHAT WENT WRONG. `genon/normalize_options.py` (STEP 6) implements Rule 7's arrangement as a
sort over `item["options"]` and a POSITIONAL relabel:

    labels   = sorted(o["label"] for o in opts)
    arranged = sorted(opts, key=lambda o: _word_key(o["text"]))
    for new_label, opt in zip(labels, arranged): opt["label"] = new_label

That is correct for the shape it was written for — one question, four options, labels A–D.
It is WRONG for an item that carries more than one sub-question, because such an item's
labels are not a flat sequence: they are GROUPED (`1A`–`1D` for sub-question 1, `2A`–`2D`
for sub-question 2), and the grouping is load-bearing. Sorting all eight texts as one list
moves options ACROSS the group boundary while the label sequence stays put, so sub-question
1's label set ends up holding sub-question 2's answers. The guide is re-keyed in the same
pass, so the damage is internally consistent and reads plausibly — and certification's "MCQ
options in arrangement order" check PASSES, because the options are, faithfully, in
arrangement order. That is what made it invisible.

english·ix ch 5 `Q-LST-A-1` is the only instance in the corpus (scanned through
`carriers.raw_item_list` across every saved plan, 2026-08-14). The cause is fixed at source
in normalize_options.py, which now REFUSES an item whose labels are not a flat A–D/1–4 set
or which declares more than one correct option. This tool repairs the file already written,
because re-running STEP 6 cannot: the options are in sorted order, so its remap is now the
identity, and the permutation that would invert it is deliberately not recorded in the
artefact (founder, 2026-08-04).

WHY THE ORIGINAL IS RECOVERABLE, AND WHY THAT MAKES A REPAIR LEGITIMATE RATHER THAN A
RE-BUY. STEP 6 never touches `item_stem`, and this item's stem prints both sub-questions
WITH their A–D options inline. So the authored map is not reconstructed by judgement or
inference — it is READ OFF the surviving stem, verbatim, and declared below as a stated
(label -> text) pair. The tool authors nothing. It asserts that every declared text is
present on disk exactly once, that the declaration is a bijection over the labels, and that
the two correct options land where the stem says they do; it refuses the file otherwise.

    python3 genon/repair_compound_mcq.py --list
    python3 genon/repair_compound_mcq.py --apply
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# ── the declared restorations ───────────────────────────────────────────────────
# `authored` is the label -> option text map READ OFF THE STEM, in authored order. The tool
# matches each text against the options on disk by exact string equality and rebuilds the
# array in this order, carrying `is_correct` with the text it belongs to. `correct` is
# declared separately and asserted, so a silent flip cannot pass.
REPAIRS = [
 {"file": "data/content/saved_plans/english/ix/ch_05_canonical.json",
  "item_id": "Q-LST-A-1",
  "why": ("ARV-D-156 — STEP 6 flattened a two-sub-question listening MCQ: it sorted all "
          "eight options alphabetically as one list and re-keyed the grouped labels "
          "positionally, so sub-question 1's label set (1A–1D) came to hold three of "
          "sub-question 2's answers and its correct answer moved to label 2D."),
  "authored": {
      "1A": "Lightweight bamboo with delicate beadwork",
      "1B": "Heavy brass fan from a craft fair",
      "1C": "Something medium-weight and decorative enough to show friends",
      "1D": "A small plain fan easy to store under a pillow",
      "2A": "He thinks brass fans are too expensive.",
      "2B": "He worries a heavy fan would be hard to move around.",
      "2C": "He believes Grandma does not like metal objects.",
      "2D": "He feels brass fans are not traditional enough.",
  },
  "correct": ["1C", "2B"],
  "evidence": (
    "The stem is untouched by STEP 6 and prints both sub-questions with their options:\n"
    "  '1. Which of the following best describes the pankha Priya proposes as a suitable gift?\n"
    "   A. Lightweight bamboo with delicate beadwork / B. Heavy brass fan from a craft fair /\n"
    "   C. Something medium-weight and decorative enough to show friends /\n"
    "   D. A small plain fan easy to store under a pillow'\n"
    "  '2. Why does Rohan raise a concern about the brass fans Priya first mentions?\n"
    "   A. He thinks brass fans are too expensive. / B. He worries a heavy fan would be hard\n"
    "   to move around. / C. He believes Grandma does not like metal objects. /\n"
    "   D. He feels brass fans are not traditional enough.'\n"
    "The eight `authored` texts above are those two lists, verbatim and in order.\n"
    "\n"
    "CORRECTNESS survives the flatten untouched (STEP 6 moves `is_correct` with its text),\n"
    "so the two options currently flagged name the authored answers directly:\n"
    "  on disk 2A = 'He worries a heavy fan would be hard to move around.'  -> authored 2B\n"
    "  on disk 2D = 'Something medium-weight and decorative enough to show friends' -> 1C\n"
    "One correct answer per sub-question, which is what a two-part item must have.\n"
    "\n"
    "The six diagnostics each name their own option's text, so re-keying them by the\n"
    "inverse of the flatten lands every one on the option it describes:\n"
    "  'bamboo fan is one of two choices, not Priya's proposal'      2C -> 1A\n"
    "  'recalls brass fans were mentioned…'                          2B -> 1B\n"
    "  'attached Rohan's detail about keeping things under the pillow' 1A -> 1D\n"
    "  'inferred a likely reason (cost) not stated in the dialogue'  1D -> 2A\n"
    "  'inferred a preference not mentioned by Rohan'                1B -> 2C\n"
    "  'background knowledge about brass being non-traditional'      1C -> 2D\n"
    "Key set after repair = {1A,1B,1D,2A,2C,2D} = exactly the non-correct labels."),
 },
]


def items_of(doc):
    """The LIVE item list, through the carrier seam."""
    sys.path.insert(0, str(REPO))
    from aruvi_core.genon.carriers import raw_item_list          # noqa: E402
    return raw_item_list(doc.get("result", doc))


def reveal_blocks(item):
    """Every label-keyed diagnostic dict on this item, whichever container holds it."""
    out = []
    for block in (item.get("teacher_guide"),
                  (item.get("guide") or {}).get(item.get("question_type"))):
        if isinstance(block, dict) and isinstance(block.get("what_each_option_reveals"), dict) \
                and block["what_each_option_reveals"]:
            out.append(block)
    return out


def apply_one(doc, spec):
    items = [i for i in items_of(doc) if isinstance(i, dict)]
    hit = [i for i in items if i.get("id") == spec["item_id"]]
    if len(hit) != 1:
        raise SystemExit(f"ABORT: {spec['item_id']} matched {len(hit)} items, expected 1")
    it = hit[0]
    if it.get("question_type") != "MCQ":
        raise SystemExit(f"ABORT: {spec['item_id']} is {it.get('question_type')}, not MCQ")

    authored, opts = spec["authored"], it.get("options") or []
    if len(opts) != len(authored):
        raise SystemExit(f"ABORT: {spec['item_id']} has {len(opts)} options, "
                         f"declaration has {len(authored)}")

    # ── the declaration must describe THIS file, exactly ────────────────────────
    by_text = {}
    for o in opts:
        by_text.setdefault(o["text"], []).append(o)
    for lab, text in authored.items():
        n = len(by_text.get(text, []))
        if n != 1:
            raise SystemExit(f"ABORT: declared text for {lab} matches {n} options on disk "
                             f"(expected exactly 1): {text[:60]!r}")
    if sorted(authored) != sorted(o["label"] for o in opts):
        raise SystemExit(f"ABORT: declared labels {sorted(authored)} != on-disk labels "
                         f"{sorted(o['label'] for o in opts)}")

    # ── correctness is asserted against the declaration, never inferred ─────────
    correct_now = {o["label"] for o in opts if o.get("is_correct")}
    correct_after = {lab for lab, text in authored.items() if by_text[text][0].get("is_correct")}
    if correct_after != set(spec["correct"]):
        raise SystemExit(f"ABORT: {spec['item_id']} correctness lands on {sorted(correct_after)}, "
                         f"declaration says {sorted(spec['correct'])}")

    # ── the restoration: labels follow their TEXT back to the authored slot ─────
    old_label = {id(o): o["label"] for o in opts}
    rebuilt = []
    for lab in authored:                       # dict order == authored order
        o = by_text[authored[lab]][0]
        o["label"] = lab
        rebuilt.append(o)
    it["options"] = rebuilt
    remap = {old_label[id(o)]: o["label"] for o in rebuilt}
    if sorted(remap) != sorted(remap.values()):
        raise SystemExit(f"ABORT: {spec['item_id']} restoration is not a bijection")

    # ── the diagnostics follow the same permutation ─────────────────────────────
    moved = {}
    for block in reveal_blocks(it):
        rev = block["what_each_option_reveals"]
        stale = [k for k in rev if k not in remap]
        if stale:
            raise SystemExit(f"ABORT: {spec['item_id']} diagnostics keyed to unknown "
                             f"labels {stale}")
        remapped = {remap[k]: v for k, v in rev.items()}
        for lab in list(remapped):
            if lab in correct_after:
                remapped.pop(lab)              # distractors only — the correct option's entry
        block["what_each_option_reveals"] = {lab: remapped[lab] for lab in authored
                                             if lab in remapped}
        if set(block["what_each_option_reveals"]) != set(authored) - correct_after:
            raise SystemExit(f"ABORT: {spec['item_id']} diagnostic key set != the "
                             f"non-correct labels after repair")
        moved.update({k: remap[k] for k in rev})

    return {"item_id": spec["item_id"], "relabelled": remap,
            "correct_before": sorted(correct_now), "correct_after": sorted(correct_after),
            "diagnostics_rekeyed": moved}


def main() -> int:
    listing = "--list" in sys.argv
    if not listing and "--apply" not in sys.argv:
        print("usage: repair_compound_mcq.py --list | --apply")
        return 2
    by_file = {}
    for spec in REPAIRS:
        by_file.setdefault(spec["file"], []).append(spec)
    for rel, specs in by_file.items():
        path = REPO / rel
        print(f"\n=== {rel}")
        for s in specs:
            print(f"    {s['item_id']}\n    why: {s['why']}")
            for line in s["evidence"].splitlines():
                print(f"      {line}")
        if listing:
            continue
        if not path.is_file():
            print("    SKIPPED — not on disk")
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        if any(r.get("kind") == "compound_mcq"
               for r in (doc.get("genon_canonical") or {}).get("repairs", [])):
            print("    SKIPPED — already repaired (the declaration is stale by design once applied)")
            continue
        shutil.copy2(path, path.with_suffix(".json.bak_pre_compound"))
        done = [apply_one(doc, s) for s in specs]
        doc.setdefault("genon_canonical", {}).setdefault("repairs", []).append({
            "tool": "repair_compound_mcq.py", "kind": "compound_mcq",
            "at": datetime.now().isoformat(timespec="seconds"),
            "why": "ARV-D-156 — STEP 6 flattened a grouped-label compound MCQ across its "
                   "sub-question boundary; the authored map was read off the surviving "
                   "item_stem and restored. normalize_options.py now refuses this shape.",
            "items": done,
        })
        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"    APPLIED — {json.dumps(done, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
