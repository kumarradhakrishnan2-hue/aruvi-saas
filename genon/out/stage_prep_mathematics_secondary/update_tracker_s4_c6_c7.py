#!/usr/bin/env python3
"""S4 · C6 and C7 recorded (2026-08-09). Both PASS."""
import datetime, json, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()

C6 = """PASS — 2026-08-09. Serve requests run on iPhone against the live app, split per
testing.md §4: kumar1 identity · kumar2 between-variant + below-floor · kumar3 mixed duration.
Sections deliberately distinct (kumar1 B/D · kumar2 F · kumar3 H/I) so X1's tenancy evidence is
unambiguous. Runbook: docs/testing_artefacts/c6_runbook_mathematics_ix_ch04.md

EVERY ROW AS PREDICTED. Expected values were computed from the installed engine BEFORE the runs,
so these are matches, not observations fitted afterwards:
  kumar1  15 / 12 / 9  -> identity; returned ch_04_canonical.json / _p12 / _p09 and WROTE NO NEW
          FILE, which is the property this row exists to prove. An identity serve is a lookup.
  kumar2  13 -> fill/single from the 15, 13 units, 11 items
          11 -> synthesis from the 12, 11 units, 12 items, note verbatim: "Every section is
                covered; the closing sitting draws the chapter together in one synthesis."
          16 -> surrender 1 period; 15 units served; schedule PRINTS 15, not 16; note: "1
                period(s) (50 minutes) exceed this chapter's fullest plan and return to your
                budget."
          8  -> fill/single from the 9, 8 units, 9 items, 0 drops
  kumar3  4x60 + 10x50 -> 14 sittings, synthesis from the 15, 12 items.

MIXED DURATION VERIFIED IN FULL (kumar3): all 14 units tile 0->their own duration exactly, 4
bands each, no gaps or overlaps; total 740 min = 4x60 + 10x50 exactly; scale 1.2 on the 60s with
integerised contiguous bands closing on 60; served_matrix reordered longest-first per the C10
filename convention. DISPERSION IS WEEK-PERIODIC, which is what it should be and initially reads
as a flaw: with ppw=7 the two weeks are byte-identical [50,50,60,50,50,60,50], so the apparent
run of three 50s at sittings 7-9 is week 1's tail meeting week 2's opening. Shortest opens each
week, 60s interior, never adjacent.

THE DROPPED-SECTION ROW IS EXERCISED AFTER ALL — the runbook recorded it N/A and that was WRONG.
X=5 (run beyond the plan) drops 3 units with uncovered_sections ['4.7','4.8'], each flagged
unscheduled:true, and the note reads "Time budget short of the chapter's full span: 4.7; 4.8
could not be scheduled — the material is included for you to share as guided self-study or
homework." The drop boundary for this chapter is 6, NOT the master-plan floor of 9: coverage
survives to 6 and breaks at 5. Recorded because the same assumption (floor == coverage boundary)
appears in the C6 spec, in the PrepareLesson copy and in the floor itself. Note also
below_floor:false at X=5 while 3 units drop — the flag tracks something other than the floor.

TWO THINGS FOUND HERE AND CARRIED ELSEWHERE: (1) ARV-D-086, the approach line not surviving a
serve — found on these very plans, fixed, engine 17 -> 18. (2) prepared.json accumulates rows
pointing at files deleted by a re-author (kumar2 holds one for ch_04_canonical_p11.json) and
identity filenames carry no version stamp while served ones do — both belong to C10/X1.

FOUNDER ACCEPTS THE ARTEFACT STALENESS: the eight served files on disk are _e17_, written before
the ARV-D-086 fix, so they render no approach line. Modes, unit counts, question counts, notes
and dispersion are unaffected by the bump (the certify-only diff was zero lines on every
chapter), so the C6 verdict stands on them. The files should be re-served as _e18_ at the next
convenient restart; the _e17_ ones stay on disk as C10.3 no-overwrite evidence."""

C7 = """PASS — 2026-08-09. Register audited on the C6 plan files AND the three canonicals — 11
files in total — plus result.dropped_units, which is teacher-facing.

(a) THE GATE FIRED: 'register clean (0 ban hit(s))' on all three canonicals, and the scan's own
coverage line proves it reached the text (60 + 48 + 36 bands across activity_title,
teacher_notes, time_bands, homework). Re-run independently here over all 11 files against the
v1.10 three bans: 0 clock quantity, 0 forward/completion, 0 calendar. Also 0 hits on paraphrase
probes for what regex cannot see ('later in this chapter', 'we shall meet', 'as we saw', 'by
now', 'now that they have', 'assumes they have'). CAVEAT KEPT IN VIEW: at C3 this same gate
reported clean on files carrying fourteen real breaches. It is clean today because C3 repaired
them by hand, not because the patterns improved.

(b) ADVISORIES RULED: the three in the report are all one kind — units wearing a section label
the handoff does not route items through (std U9/U12, p12 U12, p09 U9). Not register hits; they
are the expected end state of the ARV-D-074 repair, and the certifier's own text forbids
'fixing' them. Dismissed, not outstanding.

(c) THE JUDGED READ — founder, on served plans, unit by unit:
  X=5  the three dropped units are all borrowed from the 9 and read correctly standing alone,
       assessment items included. CLEAN.
  X=11 the Case-1 borrowed seam (p12's 10-unit prefix -> the 15's synthesis unit): nothing of
       concern. CLEAN — and it is the only cross-canonical borrow in the whole band.
  X=8, X=13  CLEAN.
  X=10 clean in text, but it stops at the FIRST sitting of the last container, so the two
       assessment items that sit under the second sitting at X=12 are not shown.
  X=7  accomplishes what X=8 does, with a twist: the 'Finding New Identities' container carries
       ONE sitting where X=9 carries two, and p7U7 is the same unit as p9U8 — one authored
       period is simply skipped mid-plan.

MECHANISM OF THE X=7 / X=10 OBSERVATION, established and then ruled on: no rule 'allowed' the
skip — it falls out of the X-1+1 serve form itself (§0.4). The engine takes the first X-1 units
as a prefix, then fills slot X from the choice set; at X=7 the prefix U1..U6 leaves 4.8 next due,
so slot 7 takes the unit that FIRST deals 4.8 (p09's U8), and U7 is in neither the prefix nor the
slot. Provenance: X=7 serves authored units [1,2,3,4,5,6,8]; X=10 serves [1..10] of the 12.
Consequences: the skipped units and their assessment items are lost silently — dropped_units 0,
section_coverage_note None, because reporting keys on uncovered SECTIONS, not skipped UNITS; and
withheld_units, which the engine populates in synthesis mode ([11,12] at X=11), is left empty in
fill mode though the engine plainly knows what it withheld. Item counts: X=7 -> 7 vs X=9 -> 9;
X=10 -> 11 vs X=12 -> 13. p12's handoff 4.8 -> [10,11] is CORRECT (both units teach, one LO
each), so the second item legitimately anchors at U11 and legitimately dies with it — the
pedagogy is defensible, only the silence is not.

FOUNDER RULING: IGNORED, not remedied. No defect row opened. Recorded here in full so it is a
decision rather than an omission, and so that a later stage meeting the same silence recognises
it. The cheap remedy, if it is ever wanted, is deterministic and needs no re-authoring: populate
withheld_units in fill mode and extend the coverage note to name withheld UNITS as well as
uncovered sections, so the material can be offered as self-study the way X=5's already is.

EXIT: zero live-ban hits, all advisories ruled, every judged transition rated. No new pattern is
owed to register_scan.py from this stage."""

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_c6c7"))
combo = state["combos"]["mathematics/secondary"]
combo["C6"] = {"status": "pass", "by": "Kumar+Claude", "at": NOW, "comment": C6,
               "artefact": "docs/testing_artefacts/c6_runbook_mathematics_ix_ch04.md"}
combo["C7"] = {"status": "pass", "by": "Kumar+Claude", "at": NOW, "comment": C7}
state["updated_at"] = NOW
STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
print("C6 = pass · C7 = pass")
print("S4 steps:", {k: v.get("status") for k, v in combo.items()
                    if isinstance(v, dict) and k.startswith("C")})
