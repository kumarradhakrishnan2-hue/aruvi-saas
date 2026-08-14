#!/usr/bin/env python3
"""repair_stem_direction.py — point the stem the way the page is actually laid out
(v1.0, 2026-08-14, S11).

THE DEFECT. Every english·ix EXTRACT_ANALYSIS item tells the student to read "the
FOLLOWING passage" or "the passage BELOW" — and the passage renders ABOVE the stem, in
every renderer we have. So the one instruction the student reads first points the wrong
way.

WHY IT RENDERS ABOVE, which is deliberate and correct:

    assessment_norm._finish, line 294
        if n.question_type in ("EXTRACT_ANALYSIS", "SOURCE_INTERPRETATION") and n.visual_stimulus:
            n.passage, n.visual_stimulus = n.visual_stimulus, None

    LessonView.jsx AQuestionPanel
        {/* T6c (EXTRACT_ANALYSIS): the extract is set off BEFORE the multi-part stem. */}
        {n.template === "passage" ? <ATyped b={n.passage} passage /> : null}
        …then the stem…

    export_assessment_pdf.py:461
        # EXTRACT_ANALYSIS: the extract is set off BEFORE the multi-part stem.
        if template == "passage": parts.append(_stimulus_html(n.get("passage")))

An extract SHOULD sit above the questions about it — that is how every exam paper in the
world is set. The renderers are right; the authored stems inherited "the following
passage" from a prose habit and nobody reconciled the two. FOUNDER, 2026-08-14: "if it is
above in reading, it is 'above'; if below, 'below'."

WHAT IS AND IS NOT REWRITTEN, because the same stem usually contains BOTH directions:

    "Read the passage below and answer the questions that follow."
              └ the PASSAGE — wrong, it is above        └ the QUESTIONS — right, they follow

Only a direction word attached to the passage moves. "answer the questions below" and
"answer the questions that follow" are left exactly as they are: the questions really are
below, in the same stem, underneath this line. Rewriting those would introduce the very
error being removed.

ALSO LEFT ALONE — the poem items ("Read the third stanza on p.87, beginning …"). Those
direct the reader to the TEXTBOOK, not to anything on the page, so they carry no on-screen
direction to be wrong about. 23 items move; the 12 poem references do not.

    python3 genon/repair_stem_direction.py --list
    python3 genon/repair_stem_direction.py --apply
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

# The stimulus routes to `passage` for these types, and `passage` renders BEFORE the stem.
ABOVE_TYPES = {"EXTRACT_ANALYSIS", "SOURCE_INTERPRETATION"}

# Ordered, longest-first. Each pair moves a direction word that modifies the PASSAGE.
# Nothing here touches "questions below" / "questions that follow".
SUBS = [
    ("The following passage is an extract", "The passage above is an extract"),
    ("Read the following passage from the chapter",
     "Read the passage above from the chapter"),
    ("Read the following passage from the narrative",
     "Read the passage above from the narrative"),
    ("Read the following passage from the letter",
     "Read the passage above from the letter"),
    ("Read the following passage carefully", "Read the passage above carefully"),
    ("Read the following extract from the story", "Read the extract above from the story"),
    ("Read the following extract from Act III of the play",
     "Read the extract above from Act III of the play"),
    ("Read the following passage", "Read the passage above"),
    ("Read the passage below", "Read the passage above"),
]


def items_of(doc):
    from aruvi_core.genon.carriers import raw_item_list          # noqa: E402
    return raw_item_list(doc.get("result", doc))


def rewrite_lead(lead):
    """(new_lead, rule_used) or (lead, None) when nothing applies."""
    for old, new in SUBS:
        if old in lead:
            return lead.replace(old, new, 1), (old, new)
    return lead, None


def scan():
    """Every item that needs the change, found live rather than declared — the rule is
    mechanical and the population is whatever currently matches it."""
    out = []
    for path in sorted((REPO / "data/content/saved_plans/english/ix").glob(
            "ch_*_canonical*.json")):
        if ".bak" in path.name:
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        for it in items_of(doc):
            if not isinstance(it, dict):
                continue
            if it.get("question_type") not in ABOVE_TYPES:
                continue
            if not str(it.get("visual_stimulus") or "").strip():
                continue                     # nothing renders above; nothing to point at
            stem = it.get("item_stem") or ""
            lines = stem.split("\n")
            new, rule = rewrite_lead(lines[0])
            if rule:
                out.append({"path": path, "id": it["id"], "before": lines[0],
                            "after": new, "rule": rule})
    return out


def main() -> int:
    listing = "--list" in sys.argv
    if not listing and "--apply" not in sys.argv:
        print("usage: repair_stem_direction.py --list | --apply")
        return 2
    todo = scan()
    print(f"{len(todo)} item(s) point down at a passage that renders above\n")
    by_path = {}
    for t in todo:
        by_path.setdefault(t["path"], []).append(t)
    for path, specs in by_path.items():
        print(f"=== {path.name}")
        for s in specs:
            print(f"    {s['id']}")
            print(f"      -  {s['before']}")
            print(f"      +  {s['after']}")
        if listing:
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        if any(r.get("kind") == "stem_direction"
               for r in (doc.get("genon_canonical") or {}).get("repairs", [])):
            print("    SKIPPED — already applied")
            continue
        shutil.copy2(path, path.with_suffix(".json.bak_pre_direction"))
        done = []
        for s in specs:
            it = [i for i in items_of(doc)
                  if isinstance(i, dict) and i.get("id") == s["id"]][0]
            lines = (it.get("item_stem") or "").split("\n")
            if lines[0] != s["before"]:
                raise SystemExit(f"ABORT: {s['id']} lead moved under us")
            lines[0] = s["after"]
            it["item_stem"] = "\n".join(lines)
            done.append({"item_id": s["id"], "before": s["before"], "after": s["after"]})
        doc.setdefault("genon_canonical", {}).setdefault("repairs", []).append({
            "tool": "repair_stem_direction.py", "kind": "stem_direction",
            "at": datetime.now().isoformat(timespec="seconds"),
            "why": "EXTRACT_ANALYSIS routes its stimulus to `passage`, which every "
                   "renderer places BEFORE the stem. The stems said 'the following "
                   "passage' / 'the passage below'. Only the passage-facing direction was "
                   "changed; 'the questions below' and 'the questions that follow' are "
                   "correct and untouched.",
            "items": done})
        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"    APPLIED — {len(done)} item(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
