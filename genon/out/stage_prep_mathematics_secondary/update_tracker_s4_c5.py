#!/usr/bin/env python3
"""S4 · C5 — certification report read (2026-08-09). PASS.

Artefact: docs/testing_artefacts/c5_mathematics_ix_ch04.md
"""
import datetime, json, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()

C5 = """PASS — 2026-08-09. Report: genon/out/library_reports/mathematics_ix_ch04_20260809_154113.md
— DETERMINISTIC CHECKS ALL PASS. Library [15,12,9], basis authored_standard, registry 8
sections, floor 9, granularity unit, section axis true. Artefact:
docs/testing_artefacts/c5_mathematics_ix_ch04.md

ALL TEN CHECKS PASS. Sweep range verified against master_plan rather than assumed: floor is 9
and top 15, so floor-2..top+2 = 7..17, and the report covers exactly 7..17 — nothing sampled
short. Check 2 was RE-RUN independently (compile_stream v0.5 -> 15/12/9 units) rather than taken
on the report's word. Quarantine: 0 json files campaign-wide.

SERVE SWEEP: 7 fill/single · 8 fill/single · 9 IDENTITY · 10 fill/single · 11 synthesis ·
12 IDENTITY · 13 fill/single · 14 synthesis · 15 IDENTITY · 16 surrender · 17 surrender.
Three identities at exactly the authored counts, so every canonical is reachable as itself;
surrender only above the top; NO truncation mode anywhere and NO row carries a drop count,
including the two below-floor requests at X=7 and X=8 — this chapter's compacts cover all
eight sections, so a short serve loses units but never a section.

THREE THINGS THAT NEEDED READING RATHER THAN TICKING:

(a) The handoff/anchor ADVISORY is the EXPECTED CONSEQUENCE of the ARV-D-074 repair and must
NOT be undone. It names std U9=4.6 and U12=4.7 (plus one closing unit in each compact) as
wearing a section label the handoff does not route items through — precisely the two units C3
removed from period_numbers because they consolidate rather than teach. The certifier's own
parenthesis forbids the 'fix' a future reader would reach for: 'do NOT extend period_numbers
to fix this — it moves the item to a later unit and loses it on short serves.' Recorded so it
is never mistaken for a regression.

(b) CHECK 9 PASSES, AND C3 PROVED A PASS HERE DOES NOT MEAN THE REGISTER IS CLEAN. When C3 ran,
register_scan reported 'register clean (0 ban hits)' on files carrying FOURTEEN register
breaches — 'will recur', 'once section 4.7 has been taught', 'after section 4.7 is covered',
'a final unit', and a 'today' classified advisory by design. The scan's coverage line shows it
reached the text (60 bands read across activity_title/teacher_notes/time_bands/homework), so
the gap is in the PATTERNS, not the reach. The register is clean today because C3 repaired
those strings by hand, not because this gate found them. This is the weakest PASS in the
report and is carried to the standing C5 tooling gap alongside the self-correction regex.

(c) CHECK 10 IS INERT AT THIS STAGE BY CONSTRUCTION, AND SHOULD STAY THAT WAY. EXACT_ITEM_COUNTS
carries one row, (social_sciences, secondary), so maths falls to the modal fallback and compares
each file to its siblings (14v14, 13v13, 9v9) — self-consistent and uninformative. This is NOT a
missing constitution row to fill: the check compares items to a fixed count per competency
WEIGHT LABEL, and maths-secondary has no weight slate — Rule 5 sets the count as one item per
implied_lo, which varies per chapter by design. The real check exists and passed at C4 (item 3),
per file AND per section. Adding a maths row would encode a slate the constitution does not have.

No defect filed."""

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_c5"))
state["combos"]["mathematics/secondary"]["C5"] = {
    "status": "pass", "by": "Claude", "at": NOW, "comment": C5,
    "artefact": "docs/testing_artefacts/c5_mathematics_ix_ch04.md",
}
state["updated_at"] = NOW
STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
combo = state["combos"]["mathematics/secondary"]
print("C5 = pass")
print("S4 steps:", {k: v.get("status") for k, v in combo.items()
                    if isinstance(v, dict) and k.startswith("C")})
