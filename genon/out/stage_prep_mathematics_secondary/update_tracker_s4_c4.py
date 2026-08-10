#!/usr/bin/env python3
"""S4 · C4 — MEMORY.md amendment items tested live (2026-08-09). PASS.

Artefact: docs/testing_artefacts/c4_mathematics_ix_ch04.md
"""
import datetime, json, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()

C4 = """PASS — 2026-08-09. All THREE canonicals checked (std 15x50/14 items, p12 12x50/13,
p09 9x50/9), not the C3 pair, since each compact authors its own assessment. Constitutions of
record LP v1.3 / assessment v1.2. Artefact: docs/testing_artefacts/c4_mathematics_ix_ch04.md

FIVE ITEMS APPLY AND ALL FIVE PASS:
 . item 3 exact item counts - Rule 5's one-item-per-implied_lo holds 14/14, 13/13, 9/9, and
   holds PER SECTION, not just in total: every handoff row got exactly as many items as it
   declared LOs. No bonus, wrap or split items.
 . item 7 Period.approach - measured through the real port, not off the JSON: 0 empty across
   all 36 units, every value verbatim from the Pedagogy document. Confirms the 'every stage
   other than maths-preparatory populates' half of the item.
 . item 9 the Jul 12-13 wave, assessment/mathematics/secondary v1.0 - all five contracts hold:
   MCQ exactly 4 options / exactly one is_correct / what_each_option_reveals with exactly 3
   entries; every NUM carries expected_answer AND method_one_line; the cognitive-demand hinge
   drives format with 0 violations; one item per implied_lo; and effort_index does NOT leak -
   0 occurrences of effort_index/conceptual_demand/reasoning_load/exec_load anywhere in any
   file, not merely absent from the format fields.
 . item 15 maths homework locator - the SECONDARY branch (strings, page baked in, pass through
   untouched) is exercised and correct: 22 of 22 homework items are strings and every one
   carries a p.NN locator. The dict path stays owed at S7/S8.
 . item 16 inclusivity - N/A by scope (middle only) and CONFIRMED N/A: 36 of 36 guide blocks
   carry inclusivity as a string, which is the intended shape for prep/secondary. Recorded
   because a reviewer meeting a string here after reading the middle amendment would
   reasonably suspect a regression. It is not one.

TWO CLOSURES RE-RECORDED: item 6 (duration vector, closed by design - A1 fixes one standard
row and the serve engine owns timetable variation) and item 18 (MCQ position, closed by STEP 6).
For 18 the census is recorded instead, because maths was the corpus's HEALTHY COUNTER-EXAMPLE
in the 2026-07-16 audit: std B/C, p12 C-C-B, p09 no MCQs - genuinely mixed and never A, the
opposite of the SS/Science clustering that provoked the struck rule.

ELEVEN ITEMS N/A with the scope reason stated in the artefact (english-only items, SS/TWAU
guide nesting, and the two maths items that belong to prep/middle - number_line stimulus and
the inclusivity object).

NOTHING NEW FILED. The structural observation worth carrying: the two items that could have
produced defects here, 3 and 9, are exactly where SS-secondary FAILED at its own C4
(ARV-D-028, slot types wrong though counts right). Maths passes both because it has no
per-competency slot slate to mis-fill - its format is decided item by item from the LO's own
demand, so the SS failure mode has no analogue at this stage.

HONEST SCOPE ON THE HINGE CHECK: the two OPEN_TASK items are excluded from it and both are
already dispositioned - std item 14 is LICENSED by assessment v1.2's new synthesis clause (it
is the item that provoked the amendment), and p12 item 9 is the accepted ARV-D-079. Recorded so
the PASS is not read as wider than it is."""

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_c4"))
state["combos"]["mathematics/secondary"]["C4"] = {
    "status": "pass", "by": "Claude", "at": NOW, "comment": C4,
    "artefact": "docs/testing_artefacts/c4_mathematics_ix_ch04.md",
}
state["updated_at"] = NOW
STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
combo = state["combos"]["mathematics/secondary"]
print("C4 = pass")
print("S4 steps:", {k: v.get("status") for k, v in combo.items()
                    if isinstance(v, dict) and k.startswith("C")})
