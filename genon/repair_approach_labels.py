#!/usr/bin/env python3
"""repair_approach_labels.py — collapse essay-length pedagogical_approach to labels (2026-08-18).

THE DEFECT. The resynth wave authored `pedagogical_approach` free and the model wrote
62-word essays (max 125) into a field whose corpus norm is a 2-WORD LABEL — it feeds the
"40 min · {approach}" display line (CLAUDE.md §3b) and the export's period band, where a
paragraph is unreadable and, per the founder, unread: teachers are not guided by it.

THE REPAIR. Whole-field replacement with a read-derived label. Each declaration asserts
the current value's PREFIX (guard against drift — a re-authored unit refuses loudly),
then replaces the whole value; the full old text is archived in genon_canonical.repairs.
The labels were written by READING all 37 essays — each names the essay's own first
device, no label was invented against its text. Upstream fix rides with this: the
resynth brief now demands a 2–5 word label and validate_resynth enforces it.

    python3 genon/repair_approach_labels.py --list
    python3 genon/repair_approach_labels.py --apply
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))
from purge_derived import purge                                    # noqa: E402

SAVED = REPO / "data" / "content" / "saved_plans"
BACKUP = REPO / "backup" / "approach_labels"

# (grade, chapter, unit, current-prefix assertion, new label)
EDITS = [
    ("vi",  1,  3, "Error-detection and reconstruction",   "Error Detection and Reconstruction"),
    ("vi",  2, 21, "Collaborative inquiry with evidence",  "Collaborative Evidence-based Classification"),
    ("vi",  3, 16, "Problem-based collaborative inquiry",  "Problem-based Collaborative Inquiry"),
    ("vi",  4, 14, "Collaborative evidence-based reason",  "Collaborative Evidence-based Reasoning"),
    ("vi",  5, 14, "Structured individual and paired",     "Structured Scenario Analysis"),
    ("vi",  6, 14, "Collaborative argumentation",          "Collaborative Argumentation"),
    ("vi",  7, 13, "Problem-based learning",               "Problem-based Learning"),
    ("vi",  8, 20, "Collaborative data-interpretation",    "Collaborative Data Interpretation"),
    ("vi",  9, 20, "Problem-based learning",               "Problem-based Learning"),
    ("vi", 10, 17, "Inquiry approach",                     "Evidence-based Inquiry"),
    ("vi", 11, 14, "Problem-based collaborative inquiry",  "Problem-based Collaborative Inquiry"),
    ("vi", 12, 14, "Collaborative sense-making",           "Role-cast Explanatory Writing"),
    ("vii",  1,  7, "Inquiry approach",                    "Primary-source Inquiry"),
    ("vii",  2, 15, "Collaborative pair work",             "Collaborative Pair Analysis"),
    ("vii",  3, 18, "Design-brief task",                   "Design-brief Task"),
    ("vii",  4, 17, "Students apply the chapter's integrated", "Integrated Fault Analysis"),
    ("vii",  5, 15, "Case-based analysis",                 "Case-based Analysis"),
    ("vii",  6, 11, "Collaborative artefact construction", "Collaborative Artefact Construction"),
    ("vii",  7, 14, "Problem-based collaborative reason",  "Problem-based Collaborative Reasoning"),
    ("vii",  8, 14, "Collaborative problem-solving",       "Collaborative Problem-solving"),
    ("vii",  9, 17, "Collaborative inquiry with structured", "Collaborative Data Inquiry"),
    ("vii", 10, 20, "Collaborative inquiry",               "Collaborative Structured Inquiry"),
    ("vii", 11, 18, "Scenario-based collaborative reason", "Scenario-based Group Reasoning"),
    ("vii", 12, 14, "Collaborative annotation and diagram", "Collaborative Annotation and Diagramming"),
    ("viii",  1,  6, "Collaborative inquiry with structured", "Structured Collaborative Inquiry"),
    ("viii",  2, 17, "Problem-based learning",              "Problem-based Learning"),
    ("viii",  3,  9, "Collaborative annotation and peer",   "Collaborative Annotation and Peer Critique"),
    ("viii",  4, 15, "Students work as pairs on a structured", "Structured Fault Diagnosis"),
    ("viii",  5, 18, "Problem-based learning",              "Problem-based Learning"),
    ("viii",  6, 12, "Collaborative writing-to-learn",      "Collaborative Writing-to-learn"),
    ("viii",  7, 18, "Problem-based learning",              "Problem-based Design Task"),
    ("viii",  8, 14, "Evidence-based reasoning",            "Evidence-based Reasoning"),
    ("viii",  9, 17, "Problem-based learning",              "Problem-based Data Analysis"),
    ("viii", 10, 15, "Design-brief inquiry",                "Design-brief Inquiry"),
    ("viii", 11, 15, "Design-based learning",               "Design-based Learning"),
    ("viii", 12, 12, "Collaborative annotation",            "Collaborative Annotation"),
    ("viii", 13, 12, "Problem-based learning",              "Problem-based Learning"),
]


def main() -> int:
    dry = "--apply" not in sys.argv
    now = datetime.now().isoformat(timespec="seconds")
    ts = now.replace("-", "").replace(":", "").replace("T", "_")
    if not dry:
        BACKUP.mkdir(parents=True, exist_ok=True)
    n = 0
    touched = set()
    for grade, ch, unum, prefix, label in EDITS:
        path = SAVED / "science" / grade / f"ch_{ch:02d}_canonical.json"
        doc = json.loads(path.read_text(encoding="utf-8"))
        ps = doc["result"]["lesson_plan"]["periods"]
        u = next(p for p in ps if p["period_number"] == unum)
        cur = u.get("pedagogical_approach") or ""
        if cur == label:
            print(f"  vi… {grade} ch{ch:02d} U{unum}: already labelled — skipped")
            continue
        if not cur.startswith(prefix):
            raise SystemExit(
                f"{path.name} U{unum}: prefix assertion failed — the artefact has "
                f"changed since this repair was written.\n  wanted prefix: {prefix!r}"
                f"\n  found: {cur[:80]!r}")
        print(f"  {grade} ch{ch:02d} U{unum}: {len(cur.split())}w -> {label!r}"
              + ("  (DRY)" if dry else ""))
        if dry:
            n += 1
            continue
        shutil.copy2(path, BACKUP / f"science_{grade}_ch{ch:02d}_{ts}.json")
        u["pedagogical_approach"] = label
        doc.setdefault("genon_canonical", {}).setdefault("repairs", []).append({
            "tool": "genon/repair_approach_labels.py v1.0",
            "at": now,
            "reason": ("resynth wrote essay-length pedagogical_approach into a 2-word "
                       "label field (founder, 2026-08-18); label read from the essay's "
                       "own first device, full old text archived here"),
            "edits": [{"unit": unum, "field": "pedagogical_approach",
                       "removed": cur, "replaced_with": label}],
        })
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        purge("science", grade, ch, reason="approach label repair")
        n += 1
        touched.add((grade, ch))
    print(f"\n{n} edit(s)" + (" — dry run, re-run with --apply" if dry else
                              f" applied across {len(touched)} chapter(s)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
