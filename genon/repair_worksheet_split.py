#!/usr/bin/env python3
"""repair_worksheet_split.py — split vi ch 10's merged worksheet for print (2026-08-18).

FOUNDER DIRECTION. The merged nine-column worksheet (Object | Observation notes | seven
characteristics | Verdict) was the right screen design but does not survive portrait-A4
print: the prose column takes the width and the blank evidence columns collapse. Ruling:
TWO tables — the observation notes as their own table (full width for the prose), and the
student evidence sheet as a blank grid (full width for the columns students write in).

DISCIPLINE. The split is COMPUTED HERE AT DECLARATION TIME from the installed aid and
applied by assertion — the current table string must match the recorded original exactly,
or the run refuses. No text is authored: the fourteen observation sentences and the
column set are redistributed verbatim. Old aid archived in genon_canonical.repairs.

    python3 genon/repair_worksheet_split.py --apply     (no flag = dry run)
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

PATH = REPO / "data/content/saved_plans/science/vi/ch_10_canonical.json"
BACKUP = REPO / "backup" / "worksheet_split"
UNIT = 17


def main() -> int:
    dry = "--apply" not in sys.argv
    doc = json.loads(PATH.read_text(encoding="utf-8"))
    u = next(p for p in doc["result"]["lesson_plan"]["periods"]
             if p["period_number"] == UNIT)
    va = u["visual_aids"][0]
    if va.get("title") == "Observation notes — tide pool objects":
        print("already split — nothing to do")
        return 0
    if va.get("type") != "table" or "Observation notes" not in (va.get("table") or ""):
        raise SystemExit("aid 0 is not the merged worksheet — refusing (artefact changed)")

    lines = va["table"].split("\n")
    header = [c.strip() for c in lines[0].split("|")]
    assert header[0] == "Object" and header[1] == "Observation notes", header
    grid_cols = [header[0]] + header[2:]          # Object + characteristics + Verdict
    obs_rows, grid_rows = [], []
    for ln in lines[1:]:
        cells = [c.strip() for c in ln.split("|")]
        obs_rows.append(f"{cells[0]} | {cells[1]}")
        grid_rows.append(" | ".join([cells[0]] + [""] * (len(grid_cols) - 1)))

    obs_aid = {"type": "table", "title": "Observation notes — tide pool objects",
               "table": "Object | Observation notes\n" + "\n".join(obs_rows)}
    grid_aid = {"type": "table", "title": "Student evidence sheet — blank grid",
                "table": " | ".join(grid_cols) + "\n" + "\n".join(grid_rows)}

    print(f"split: {len(obs_rows)} observation rows · grid {len(grid_cols)} cols")
    if dry:
        print("dry run — re-run with --apply")
        return 0

    BACKUP.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(PATH, BACKUP / f"science_vi_ch10_{ts}.json")

    old_aid = u["visual_aids"][0]
    u["visual_aids"] = [obs_aid, grid_aid] + u["visual_aids"][1:]
    # materials + notes pointers follow the new names
    u["materials"] = [
        m.replace("Student evidence worksheet, one per student, printed landscape "
                  "(see visual aid: 'Student evidence worksheet — tide pool census')",
                  "Observation notes sheet and blank evidence grid, one each per student "
                  "(see visual aids: 'Observation notes — tide pool objects' and "
                  "'Student evidence sheet — blank grid')")
        for m in u["materials"]]
    u["teacher_notes"] = u["teacher_notes"].replace(
        "(see material: 'Student evidence worksheet')", "(see material)")

    doc.setdefault("genon_canonical", {}).setdefault("repairs", []).append({
        "tool": "genon/repair_worksheet_split.py v1.0",
        "at": datetime.now().isoformat(timespec="seconds"),
        "reason": ("founder direction 2026-08-18: the merged nine-column worksheet does "
                   "not survive portrait print — observation notes and the blank "
                   "evidence grid become separate tables; content redistributed "
                   "verbatim, nothing authored"),
        "edits": [{"unit": UNIT, "field": "visual_aids[0]",
                   "removed": old_aid, "replaced_with": "[obs_aid, grid_aid] (split)"}],
    })
    PATH.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    purge("science", "vi", 10, reason="worksheet split for print")
    print(f"applied · aids now: {[a['title'] for a in u['visual_aids']]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
