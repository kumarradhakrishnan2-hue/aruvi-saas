#!/usr/bin/env python3
"""ARV-D-086 — the approach line did not survive a serve. Found at S4's C6, fixed, engine
bumped 17 -> 18 (2026-08-09).
"""
import datetime, json, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()

TITLE = ("served plans rendered an EMPTY pedagogical approach line on 8 of 11 stages — the "
         "canonicals were correct throughout, only the artefact the teacher receives was wrong")

EVIDENCE = """FOUND 2026-08-09 at S4's C6, on kumar2's and kumar3's served plans. Every ch 4
canonical carries pedagogical_method on all 15/12/9 units and C4's item 7 measured 0 empty
through the real port. Every SERVED plan measured 100% empty.

MECHANISM, two links in one chain:
 . compile.py's _MODELLED listed all five approach key names, which is what EXCLUDES a key
   from unit["extra"]. So serve._period_from_unit spliced none of them back.
 . the only approach key the served period then carried was the NORMALIZED
   pedagogical_approaches, computed by carriers.unit_approaches - which read three of the
   five names and returned [] for maths, english and TWAU. Its docstring claimed
   pedagogical_approach covered "Science, Maths"; maths emits pedagogical_method.
Each subject port reads the key ITS OWN constitution emits, so only social_sciences - whose
authored key happens to share the normalized name - rendered anything.

MEASURED BEFORE THE FIX (served, through each subject's real port):
  mathematics/ix ch4  X=13  EMPTY 13/13      science/ix   ch8 X=13  EMPTY 12/12
  mathematics/ix ch4  X=8   EMPTY  8/8       science/viii ch6 X=11  EMPTY 11/11
  social_sciences/ix  ch3   X=11  EMPTY 0/11 (unaffected)
Scope by key: maths (pedagogical_method) x2 stages · science (pedagogical_approach) x2 ·
english (pedagogical_methods) x3 · TWAU (dominant_mode) x1 = EIGHT stages. SS x2 unaffected;
maths-preparatory has no source field and is legitimately empty (MEMORY item 7).

SEVERITY: this is CLAUDE.md 3(b)'s single canonical "how do I run this?" line, and it was
missing from every served plan on a CERTIFIED stage - science-middle carries a signed human
GATE. Filed against science/middle and science/secondary as well as this stage.

WHY NOTHING CAUGHT IT: C1-C5 read canonicals and reports. No step before C6 reads a served
plan, and C6 is described in the template as the first step that "tests the path a teacher
actually takes". It did exactly that on its first outing.

FIX (2026-08-09): the approach keys are no longer modelled, so each subject's own key rides
in extra verbatim and is spliced back - no port change and no subject branching, which is
what extra exists for. carriers.unit_approaches now reads all five names (english's dict
shape included) and its docstring is corrected. VERIFIED: 0 empty on all six served plans
across three subjects; tests/test_genon_approach_survives_serve.py added, locking BOTH the
unit-level key reading AND the end-to-end compile->serve->port property - the second is the
one that would have caught this, since the ports never read the normalized key.

ENGINE 17 -> 18 (served bytes change for maths, science, english, TWAU). Per testing.md 9 an
engine change is corpus-wide and cheap: --certify-only re-run on all five chapters with a
library, reports diffed line by line against the previous run - ZERO diff lines on every one,
all five still DETERMINISTIC CHECKS ALL PASS, serve sweeps identical. So no stage loses
certification. All five genon suites green. Every _e17_ plan file is stale by construction
and stays on disk as C10.3 evidence."""

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_arvd086"))

if not any(d["id"] == "ARV-D-086" for d in state["defects"]):
    state["defects"].append({
        "id": "ARV-D-086", "combo": "mathematics/secondary", "step": "C6",
        "severity": "S2", "owner": "founder", "status": "closed",
        "opened": NOW, "closed": NOW, "at": NOW,
        "title": TITLE, "evidence": EVIDENCE,
        "also_affects": ["science/secondary", "science/middle", "english/preparatory",
                         "english/middle", "english/secondary",
                         "the_world_around_us/preparatory", "mathematics/middle"],
        "resolution": "Fixed in aruvi_core/genon/compile.py (_MODELLED) + carriers.py "
                      "(unit_approaches); GENON_ENGINE_VERSION 17 -> 18; regression test "
                      "tests/test_genon_approach_survives_serve.py.",
    })

for combo in ("mathematics/secondary", "science/secondary", "science/middle"):
    c = state["combos"].get(combo)
    if c:
        c.setdefault("provenance", {})["genon_engine_version"] = "18"
        c["provenance"]["engine_bumped_at"] = NOW
        c["provenance"]["engine_bump_reason"] = (
            "ARV-D-086 — approach line now survives a serve. certify-only re-run diffed "
            "ZERO lines against the pre-bump report; sweeps identical; certification stands "
            "(testing.md §9, engine-change path).")

state["updated_at"] = NOW
STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
print("ARV-D-086 filed + closed · engine 18 recorded on maths·sec, science·sec, science·middle")
