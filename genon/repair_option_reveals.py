#!/usr/bin/env python3
"""repair_option_reveals.py — re-key stale MCQ diagnostics onto the options they describe,
and drop the correct option's entry (v1.0, 2026-08-10, S7 · C3).

WHAT WENT WRONG (ARV-D-092). `genon/normalize_options.py` (STEP 6) sorts an item's options
and relabels them, then remaps the label-keyed guide so the diagnostics follow. It looked for
that guide at `guide[QUESTION_TYPE].what_each_option_reveals` — the constitution-family path,
used by science, social_sciences, TWAU and maths SECONDARY. Mathematics MIDDLE and
PREPARATORY keep it at `teacher_guide.what_each_option_reveals`. So on those two stages the
options moved and the diagnostics did not: the teacher's "what this choice reveals" line
described a different option than the one printed beside it, and on ch 7's item 2 the CORRECT
answer carried "Same misconception as A — the student picks the other adjacent side."

The cause is fixed at source in normalize_options.py (both paths remapped, by shape). This
tool repairs the files that were already written, because re-running STEP 6 cannot: the
options are already in sorted order, so its remap is now the identity and it has nothing to
undo. The permutation that WOULD invert it is returned by `normalize_item` but deliberately
never written to the artefact (founder, 2026-08-04), so it is not recoverable from disk.

WHY A REPAIR IS LEGITIMATE HERE, when repair_register.py refuses structural and pedagogical
defects: nothing is authored and nothing is judged by this tool. Each diagnostic is a STATED
(old_label -> new_label) pair, declared below by a human who read the diagnostic against the
options; the tool only applies it, and only if every assertion holds. It is the
repair_register pattern — stated pairs, applied by assertion, recorded in the artefact —
not a generated rewrite.

WHAT IT ENFORCES, from assessment v3.4 (middle) / v1.2 (preparatory): the reveal key set must
equal EXACTLY the set of non-correct labels. The correct option's entry is DROPPED, not moved,
because under the amended rule it may not exist. That is also the invariant that makes this
class of bug machine-detectable from now on.

    python3 genon/repair_option_reveals.py --list
    python3 genon/repair_option_reveals.py --apply
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CONFORM_ROOT = REPO / "data/content/saved_plans/mathematics/vii"

# ── the declared re-keyings ──────────────────────────────────────────────────────
# `moves` maps the diagnostic's CURRENT key -> the label of the option it actually
# describes. Read off the text against the options, item by item; `evidence` records the
# reading so the next person can check it without re-deriving it.
REPAIRS = [
 {"file": "data/content/saved_plans/mathematics/vii/ch_07_canonical.json",
  "item": 2,
  "why": ("STEP 6 sorted this item (the correct option moved from label C to label B) and left "
          "the diagnostics keyed to the pre-sort labels."),
  "moves": {"A": "A", "B": "D", "C": "B", "D": "C"},
  "evidence": (
    "Options now: A) AB adjacent · B) AC (CORRECT) · C) all three sides · D) BC adjacent.\n"
    "  A 'confuses opposite-the-right-angle with a side MEETING it'  -> an adjacent side -> stays A (AB)\n"
    "  B 'Same misconception as A — the OTHER adjacent side'         -> the other adjacent  -> D (BC)\n"
    "  C 'correctly locates the hypotenuse as the side that does not touch…' -> the correct one -> B (AC)\n"
    "  D 'believes ORIENTATION changes which side is the hypotenuse' -> 'any side depending on orientation' -> C\n"
    "Every diagnostic lands on the option whose text it names; the mapping is a bijection."),
 },
 {"file": "data/content/saved_plans/mathematics/vii/ch_07_canonical_p10.json",
  "item": 2,
  "why": "Same cause; the correct-answer diagnostic sits on D while the correct option is C.",
  "moves": {"A": "D", "B": "B", "C": "A", "D": "C"},
  "evidence": (
    "Q: which combination is IMPOSSIBLE? Options: A) acute+equilateral · B) obtuse+isosceles · "
    "C) right+equilateral (CORRECT) · D) right+isosceles.\n"
    "  A 'knows right-angled ISOSCELES triangles exist (two 45° and one 90°)' -> describes D\n"
    "  B 'knows obtuse isosceles triangles exist'                             -> stays B\n"
    "  C 'knows equilateral triangles have three 60° angles'                  -> the reason A is possible -> A\n"
    "  D 'correctly identifies that an equilateral triangle cannot have a right angle' -> the correct one -> C\n"
    "Bijection again; the correct option's entry (now C) is then dropped per v3.4."),
 },
]


def items_of(doc):
    r = doc.get("result", doc)
    ai = r.get("assessment_items")
    out = []
    if isinstance(ai, dict):
        out = ai.get("questions") or []
    else:
        for grp in ai or []:
            out += grp["items"] if isinstance(grp, dict) and "items" in grp else [grp]
    return out


def apply_one(doc, spec):
    items = items_of(doc)
    n = spec["item"]
    if not (1 <= n <= len(items)):
        raise SystemExit(f"ABORT: item {n} out of range (file has {len(items)})")
    it = items[n - 1]
    if it.get("question_type") != "MCQ":
        raise SystemExit(f"ABORT: item {n} is {it.get('question_type')}, not MCQ")
    tg = it.get("teacher_guide") or {}
    rev = tg.get("what_each_option_reveals")
    if not isinstance(rev, dict) or not rev:
        raise SystemExit(f"ABORT: item {n} has no teacher_guide.what_each_option_reveals")

    labels = [o["label"] for o in it["options"]]
    correct = {o["label"] for o in it["options"] if o.get("is_correct")}
    moves = spec["moves"]
    if sorted(moves) != sorted(rev) or sorted(moves.values()) != sorted(labels):
        raise SystemExit(f"ABORT: item {n} declared moves are not a bijection over "
                         f"{sorted(labels)} (keys {sorted(rev)} -> {sorted(moves.values())})")
    if len(correct) != 1:
        raise SystemExit(f"ABORT: item {n} has {len(correct)} correct options")

    remapped = {moves[k]: v for k, v in rev.items()}
    dropped = {lab: remapped.pop(lab) for lab in list(remapped) if lab in correct}
    tg["what_each_option_reveals"] = {lab: remapped[lab] for lab in labels if lab in remapped}

    if set(tg["what_each_option_reveals"]) != set(labels) - correct:
        raise SystemExit(f"ABORT: item {n} key set != the non-correct labels after repair")
    return {"item": n, "moves": moves, "dropped_correct_entry": list(dropped)}


def conform(doc):
    """Drop every CORRECT option's diagnostic. Purely mechanical — no judgement, no mapping.
    Asserted per item: the key set must end up exactly the non-correct labels."""
    done = []
    for n, it in enumerate(items_of(doc), 1):
        if not isinstance(it, dict) or it.get("question_type") != "MCQ":
            continue
        tg = it.get("teacher_guide") or {}
        rev = tg.get("what_each_option_reveals")
        if not isinstance(rev, dict) or not rev:
            continue
        labels = [o["label"] for o in it["options"]]
        correct = {o["label"] for o in it["options"] if o.get("is_correct")}
        dropped = [lab for lab in rev if lab in correct]
        if not dropped:
            continue
        tg["what_each_option_reveals"] = {lab: rev[lab] for lab in labels
                                          if lab in rev and lab not in correct}
        assert set(tg["what_each_option_reveals"]) == set(labels) - correct, \
            f"item {n}: key set != the non-correct labels after conform"
        done.append({"item": n, "dropped_correct_entry": dropped})
    return done


def main() -> int:
    listing = "--list" in sys.argv
    if not listing and "--apply" not in sys.argv:
        print("usage: repair_option_reveals.py --list | --apply")
        return 2
    by_file = {}
    for spec in REPAIRS:
        by_file.setdefault(spec["file"], []).append(spec)
    for rel, specs in by_file.items():
        path = REPO / rel
        print(f"\n=== {rel}")
        for s in specs:
            print(f"    item {s['item']}: {s['moves']}\n    why: {s['why']}")
            for line in s["evidence"].splitlines():
                print(f"      {line}")
        if listing:
            continue
        if not path.is_file():
            print("    SKIPPED — not on disk")
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        if any(r.get("kind") == "option_reveals"
               for r in (doc.get("genon_canonical") or {}).get("repairs", [])):
            print("    SKIPPED — already repaired (the declaration is stale by design once applied)")
            continue
        shutil.copy2(path, path.with_suffix(".json.bak_pre_reveals"))
        done = [apply_one(doc, s) for s in specs]
        doc.setdefault("genon_canonical", {}).setdefault("repairs", []).append({
            "tool": "repair_option_reveals.py", "kind": "option_reveals",
            "at": datetime.now().isoformat(timespec="seconds"),
            "why": "ARV-D-092 — STEP 6 relabelled the options without remapping "
                   "teacher_guide.what_each_option_reveals; correct-option entry dropped per "
                   "assessment v3.4 (distractors-only).",
            "items": done,
        })
        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"    APPLIED — {done}")

    # ── the rule, applied to every OTHER file of the same library ────────────
    # The re-keyings above are where the judgement is. This is the amended rule enforced on
    # the items whose mapping was right all along: assessment v3.4 (middle) / v1.2 (prep)
    # make the key set exactly the non-correct labels, so a correct-option diagnostic is
    # forbidden, not merely redundant. Mechanical, and asserted per item.
    for path in sorted(CONFORM_ROOT.glob("ch_*_canonical*.json")):
        rel = str(path.relative_to(REPO))
        if rel in by_file or ".bak" in path.name:
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        if any(r.get("kind") == "option_reveals"
               for r in (doc.get("genon_canonical") or {}).get("repairs", [])):
            continue
        done = conform(doc)
        if not done:
            continue
        print(f"\n=== {rel}  (conform only)")
        shutil.copy2(path, path.with_suffix(".json.bak_pre_reveals"))
        doc.setdefault("genon_canonical", {}).setdefault("repairs", []).append({
            "tool": "repair_option_reveals.py", "kind": "option_reveals",
            "at": datetime.now().isoformat(timespec="seconds"),
            "why": "assessment v3.4 distractors-only: the correct option's diagnostic is "
                   "dropped. The mapping on these items was already correct.",
            "items": done,
        })
        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"    APPLIED — {done}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
