#!/usr/bin/env python3
"""repair_courier_table.py — fill vii ch 8's courier table template (2026-08-18).

FOUNDER DIRECTION. The polish preserved the courier journey as a TEMPLATE ("[blank or
value]" placeholders + a design note telling the teacher to construct the numbers) — the
one aid of its kind besides vi ch 10's cards, both predating the licensed-gap-fill
ruling. The template also carried a latent flaw: its row 1 left distance AND speed
blank, but Distance = Speed × Time needs the speed given.

THE FILL IS ARITHMETIC, NOT AUTHORSHIP — computed against every constraint the design
note itself states, and verifiable: two uniform legs (1, 3: steady descriptions), three
non-uniform (2, 4, 5), one distance gap on a uniform leg (leg 1: D = S×T with S given),
one time gap on a non-uniform leg (leg 2: T = D÷S with avg S given), totals 17.2 km in
85 min → average 12.14 km/h, just above the promised 12 — the deadline verdict stays
genuinely contestable. A Description column replaces the template's unjudgeable
Motion-type evidence gap. The answer key (per-leg speeds, totals, verdict) lands in the
answer-sheet guide aid; the teacher design note is retired (its constraints are
preserved here and in the repair record).

    python3 genon/repair_courier_table.py --apply     (no flag = dry run)
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

PATH = REPO / "data/content/saved_plans/science/vii/ch_08_canonical.json"
BACKUP = REPO / "backup" / "courier_fill"
UNIT = 14

NEW_TABLE = (
    "Leg | What the courier does | Distance (km) | Time (min) | Speed (km/h)\n"
    "1 | pedals at a steady pace throughout | ______ | 15 | 14 (given)\n"
    "2 | weaves through market traffic, speed changing | 3.0 | ______ | 12 (average, given)\n"
    "3 | steady cruise along the ring road | 5.0 | 20 | ______\n"
    "4 | stop-start past signals and a school gate | 3.2 | 25 | ______\n"
    "5 | downhill stretch, speed rising then easing | 2.5 | 10 | ______"
)

ANSWER_KEY = (
    "\n\nANSWER KEY (teacher only). Leg 1: D = 14 × 0.25 h = 3.5 km. Leg 2: T = 3.0 ÷ 12 "
    "= 0.25 h = 15 min. Leg 3: 15 km/h. Leg 4: 7.68 km/h. Leg 5: 15 km/h. Motion type: "
    "legs 1 and 3 uniform (steady descriptions, constant speed), legs 2, 4, 5 non-uniform "
    "(changing speed). Totals: 17.2 km in 85 min = 1.417 h → average 12.14 km/h — just "
    "above the promised 12, so the delivery is on time, but only barely: expect and "
    "welcome arguments about rounding and about whether an average this close honours "
    "the promise."
)

DESIGN_NOTE = (
    "Design note for teacher: populate the table with five legs so that two legs have a "
    "constant speed across equal time intervals (uniform linear motion) and three do not "
    "(non-uniform linear motion). Leave the distance blank for one of the uniform legs "
    "(students apply Distance = Speed × Time) and the time blank for one of the "
    "non-uniform legs (students apply Time = Distance ÷ Speed), ensuring both "
    "rearrangements are required. Set the numbers so that the overall average speed "
    "lands just above or just below 12 km/h, making the deadline verdict genuinely "
    "contestable."
)


def main() -> int:
    dry = "--apply" not in sys.argv
    doc = json.loads(PATH.read_text(encoding="utf-8"))
    u = next(p for p in doc["result"]["lesson_plan"]["periods"]
             if p["period_number"] == UNIT)
    card, tmpl, guide = u["visual_aids"][0], u["visual_aids"][1], u["visual_aids"][2]
    if "[blank or value]" not in (tmpl.get("table") or ""):
        print("template already filled — nothing to do")
        return 0
    if DESIGN_NOTE not in card.get("text", ""):
        raise SystemExit("design note not found verbatim — artefact changed, refusing")
    if "ANSWER KEY" in guide.get("text", ""):
        raise SystemExit("answer key already present — refusing")

    print("fill: 5 legs · 17.2 km / 85 min · avg 12.14 km/h (just above 12)")
    if dry:
        print("dry run — re-run with --apply")
        return 0

    BACKUP.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(PATH, BACKUP / f"science_vii_ch08_{ts}.json")

    old_tmpl = dict(tmpl)
    tmpl["title"] = "Courier journey — distance-time table"
    tmpl["table"] = NEW_TABLE
    card["text"] = card["text"].replace("\n" + DESIGN_NOTE, "").replace(DESIGN_NOTE, "")
    guide["text"] = guide["text"] + ANSWER_KEY

    doc.setdefault("genon_canonical", {}).setdefault("repairs", []).append({
        "tool": "genon/repair_courier_table.py v1.0",
        "at": datetime.now().isoformat(timespec="seconds"),
        "reason": ("licensed gap-fill (founder rulings 2026-08-18): the courier table "
                   "template's numbers are supplied, computed against the design note's "
                   "own constraints; the note retires with its constraints preserved "
                   "here; answer key added to the guide aid"),
        "edits": [
            {"unit": UNIT, "field": "visual_aids[1]", "removed": old_tmpl,
             "replaced_with": "filled table (see artefact)"},
            {"unit": UNIT, "field": "visual_aids[0].text",
             "removed": DESIGN_NOTE, "replaced_with": "(retired — numbers supplied)"},
            {"unit": UNIT, "field": "visual_aids[2].text",
             "removed": "", "replaced_with": "ANSWER KEY appended"},
        ],
    })
    PATH.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    purge("science", "vii", 8, reason="courier table filled")
    print("applied · aids:", [a["title"] for a in u["visual_aids"]])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
