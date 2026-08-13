#!/usr/bin/env python3
"""S10 · english · middle — C3, C6, C7, C12, C13 into the tracker (founder rulings 2026-08-13)."""
import datetime, json, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/middle"

C3 = """PASS 2026-08-13 — every numbered rule of BOTH constitutions checked against the standard (12 units) and the floor compact (7 units), rule by rule with quoted evidence. Seven findings, ALL DISMISSED BY THE FOUNDER on the day; two defects stand open from the same read.

LP v1.7 — PASS on the register (0 ban hits, 112 bands), INPUTS/A1 (one row, 40 min), Rule 1 (every unit 1 spine, all section_id B, the closing exception used exactly once on u12 with synthesis: true), Rule 2 STEP 1 (max 3 tasks against the 2-3 ceiling), STEP 3 FULL SPINE COVERAGE (6/6 at 12 AND at the floor of 7 — the first live proof of this stage's own P1 amendment), STEP 4 (VocGram isolated), Rule 2A (aloud bands present, every unit's materials carry a page range), Rule 3 (32 task refs, all in range, none invented), Rule 4 (every method inside its spine's permitted list, keys == spines_taught, no method 3x consecutive), Rule 5 (0-40 tiling exact, >=3 bands, all 19 units), Rule 7 (0 C-codes), Rule 8 (<=2 homework per unit, every brief carrying a page locator), Rule 10 (6 contributions, implied_lo format, section_context 10-18, tasks_anchored present). Rule 2 STEP 2 is N/A — one main_section post-split.
  SUBJECTIVE-PASS, Rule 6: the model emitted chapter_number, stage, main_sections_inventory and periods_allocated correctly; the INSTALLER relocates them onto the saved-plan wrapper, so `result` alone lacks them. A pipeline transformation, not a generation defect.

Assessment v3.7 — PASS on Rule 1 (canonical spine order), Rule 4 (types known, MCQ 4 options / 1 correct, A9's by-label prohibition clean at 0), Rule 5 (answer-layer discipline clean: no OPEN carrying suggested_answer, no CLOSED carrying expected_elements, MCQ suggested_answer empty with what_each_option_reveals populated, MATCH carrying answer_key), Rule 6 (all verified true), Rule 8 (all source tags present), RULE 8A (no period_ref / period_number / unit_ref / phase_ref emitted anywhere — the anchoring rule this stage's P2 confirmed), Rule 9 (pipe-tables only, no inlined options), Rule 13 (no internal IDs in prose). Rule 7 N/A — no verification fallbacks.

THE SEVEN FINDINGS, ALL DISMISSED (founder, 2026-08-13):
  1. task_brief >18 words, 3 of 32 (19w, 20w, 22w) — DISMISSED, ARV-D-141 closed as "not a defect, do not track". What the cap protects is the Rule 9 page locator, and ALL 32 briefs carry one against 13 of 123 in the historical corpus.
  2. LP Rule 9 machinery leak — p07 u2 writes the internal code "MCQ" into teacher_notes AND a band. DISMISSED ("no big issue"). Recorded for its cause, which is the more useful half: Rule 9 mandates a VERIFICATION PASS against `aruvi-scripts/lint_lp_teacher_prose.py`, and THAT SCRIPT DOES NOT EXIST — no aruvi-scripts/ directory, nothing of that name anywhere, nothing in build_library.py calling it. The constitution has been naming a gate that has never run, on every stage.
  3. Assessment Rule 3 — p07's writing item quotes 12 words of verse ('small and round and made of pale, blue shell') past the 8-word incipit cap. DISMISSED: a short lift in quotation marks framing a question, meaningless without the whole poem, not reproduction.
  4. Assessment Rule 10 — both files echo the listening transcript into the slot-1 item (2 lines in the standard, a 3-line cloze in p07) where the rule says it is "not inlined... not echoed". DISMISSED on the same reasoning.
     Measured for the record: the poem is 17 lines / 102 words and 12-18% of it appears across the three files; the transcript is 8 lines / 56 words and 25-27% appears. The transcript is the higher PROPORTION only because it is short. FOUNDER RULING: no amendment — the model already draws the line where it should, and looser prose would only give it room to drift.
  5. Assessment Rule 2 slot table — p07's listening slot 1 is FILL_IN, a slot-2 type. DISMISSED.
  6. Assessment Rule 12 — `total_items` absent. DISMISSED. Recorded: it is a MODEL omission, not the installer's — `None` in the raw output too.
  7. `role_handoff` / `unit_handoff` present as empty dicts. NOT dismissed — ACTED ON: removed from the pipeline and stripped from all 140 installed canonicals (see the C7 note).

STILL OPEN FROM THIS READ: ARV-D-139 (assessment Rule 11's rubric cap, disproved by the run AND by 47 of 95 corpus bullets, never once 3 bullets) and ARV-D-140 (one advisory calendar word). Both accepted by the founder, neither blocking."""

C6 = """PASS 2026-08-13 — all six rows of the request matrix verified, with one artefact caveat recorded below.

IDENTITY (kumar1) — three registrations pointing at ch_08_canonical.json, _p10 and _p07, i.e. all three authored counts (12, 10, 7), with NO new file written for any of them. The absence is the evidence.

BETWEEN-VARIANT FILLS (kumar2) — X=8 and X=9, both mode fill / fill_class single from the 10-canonical, uncovered_sections empty, zero drops.

PREFIX COMPLETES COVERAGE EARLY (kumar2) — X=11, mode synthesis, borrowed_from 12 which IS the standard's count as the row demands, note "Every section is covered; the closing sitting draws the chapter together in one synthesis."

BELOW FLOOR (kumar2) — X=6, mode fill with uncovered_sections ['B|beyond_text'], coverage note naming it and offering it as guided self-study, result.dropped_units carrying the lost unit verbatim flagged unscheduled. Checked the e12 rule specifically: the lender is the 7-canonical, its unit 7 IS B|beyond_text, and the dropped unit is that one — SOURCED FROM THE LENDING PLAN, not the chosen one.

X = A_top + 1 (kumar2) — X=13. This row was OUTSTANDING when C6 was first read and has since been run; verified at C10. All of its e10 assertions hold, and they are the ones the certifier's internal sweep cannot make: requested 13, served_matrix [{40, 12}], 12 units served, surrendered_periods 1, the surrender sentence in BOTH coverage_note and genon.surrender_note, period_schedule_display printing "Total: 12 periods", and THE ASK SURVIVING in period_rows_snapshot as {duration 40, count 13}.

MIXED-DURATION WEEKLY MATRIX (kumar3) — 50m2 + 40m9 for 11 sittings. Verified when served: duration_sequence [40,40,40,50,40,40,40,50,40,40,40] — shortest opens the week, the two 50s interior at positions 4 and 8, never adjacent — and proportional scaling exact, every one of the 11 units tiling to ITS OWN duration (the 50s to 50, the 40s to 40), zero broken.

THE CAVEAT, recorded rather than glossed: the mixed-matrix FILE no longer exists. C7's clock repair purged all five derived plans (correctly — they carried pre-repair text), and four have since been re-served while the mixed one has not. So the row is VERIFIED but its artefact is absent, and anything downstream that wants to READ that plan — C12's view/export inspection, the human gate — needs one re-serve to recreate it. It is deterministic and free (~2 ms, C11) and will come back byte-identical apart from saved_at.

ALSO RECORDED, unexercised rather than failed: fill_class came back `single` on every fill in the band, so FORWARD and BACKWARD fills never fired on this library — which means a backward fill's "runway" coverage note has no live instance here. And the "identity fires only at the authored duration" nuance (ask an authored count at a different length: expect NOT identity, a whole-variant serve with proportional scaling, and a file written) was not run."""

C7 = """PASS 2026-08-13 — 0 live ban hits after repair; every advisory ruled on; the read-for-what-regex-cannot-see half found a real breach in the highest-risk place.

(a) THE MACHINE GATE — 0 ban hit(s) on all eight files (3 canonicals + 5 served plans), with the scan confirmed to have REACHED the text (47 / 40 / 25 bands plus activity_title, teacher_notes, materials and homework) rather than reporting clean because it read nothing.

(b) ADVISORIES — six, two distinct strings, both calendar-advisory: "one row each from today's extracts" (standard u3, inherited into the X=11 and mixed serves) and "the same close-reading method used in class today" (p10 u2, inherited into X=8 and X=9). RULED: neither is chapter content — both mean THIS SITTING, so both are ban-3 in intent. But `register_scan.py` deliberately grades today/yesterday advisory-not-ban with a recorded rationale ("a gate that failed on 'Will it rain today?' would be switched off in a week"), and the founder dismissed ARV-D-140. Accepted deviation, consistent with that ruling. It is a constitution-versus-scanner WORDING divergence, not a scanner gap.

(c) WHAT THE REGEX CANNOT SEE — ONE REAL BREACH, and it was in the standard's SYNTHESIS unit, the one unit v2.0 designs to be borrowed. Its teacher_notes read: "Any student encountering the poem for the first time in this unit has everything they need WITHIN THESE FORTY MINUTES". That is a clock quantity, ban 1, and the exact falsification the ban exists to prevent — the platform scales every unit to the sitting that carries it. Demonstrated live rather than argued: served at 40 the sentence is true; at 50 and at 60 the teacher is told forty minutes for a fifty- and sixty-minute sitting. It had already travelled into the X=11 serve and kumar3's mixed week, both of which happened to land it on a 40-minute sitting, so it was accidentally true and would have lied to the next teacher with 45-minute periods.
  A SECOND of the same shape in p10 u9: "genuinely philosophical AND WORTH FIVE MINUTES".
  WHY THE GATE MISSED BOTH: register_scan.py's clock patterns all key on a digit or a fixed phrase ("for N minutes", "the remaining time", "half the session", "in the first/last N minutes"). A spelled-out number attached to anything else sails through.
  MEASURED ACROSS THE WHOLE CORPUS before deciding anything: 17 hits of that shape in 15 of the 140 installed canonicals, read individually, ZERO false positives — all genuine clock quantities in teacher-facing text, none of them chapter content. Five are in social_sciences IX and VIII, i.e. stages already through their C-cycles. So the ban has been leaking campaign-wide.

FOUNDER RULING 2026-08-13: "just amend the teacher notes, nothing else to be done." Applied exactly — no new scanner pattern, no defect rows, and the 15 other canonicals deliberately untouched.
  BOTH EDITS DONE THROUGH `repair_register.py`, not by hand: declared (old -> new) pairs applied by assertion (a drifted artefact refuses the repair rather than being force-edited), each recorded in genon_canonical.repairs[] with its reason, both PURE DELETIONS of an appositive clause. "has everything they need" survives; "genuinely philosophical" survives. The trailing "all within the unit's own minutes" was deliberately LEFT — it names no quantity, scales with the sitting, and is the honest form of what the removed clause was reaching for.
  Consequence handled: a repaired canonical invalidates everything derived from it (ARV-D-034), so purge_derived removed all five served plans. It first FAILED with "Operation not permitted" and STOPPED rather than reporting success — the correct behaviour, and the exact failure mode ARV-D-034 documents. Re-run with delete access; five files removed by name. Re-certification after repair: ALL PASS."""

C12 = """PASS 2026-08-13 — verified by Kumar (this is a [Kumar runs, Claude inspects] step and the founder ran and checked it directly). Recorded on the founder's verification; no Claude inspection note is attached.

WHAT C12 COVERS: the e09 split — the online view carries the below-floor plan's dropped units (result.dropped_units -> /view -> vm["dropped_lp"] with vm["dropped_sections"] beside it) while the EXPORTS omit them, "her printed artifact stays as decided at generation; online is an option, not an imposition". Plus C12.3 chapter notes and C12.4 the lesson-plan bookmark (usage, privacy, persistence), added at template 2.6 because both are per-teacher writes on the surface C12 already opens.

TWO THINGS FROM THIS STAGE'S OWN WORK THAT BEAR ON IT, carried here so they are not lost:
  1. The EXPORT half is independently confirmed by C9's check 3d, exercised through the API's own code path (api/main.py:1179): a 5-period serve carries 12 items of which 4 are unscheduled, and the export renders exactly 8 with zero leaks; the 6-period serve renders 10 of 12. The filter lives once, in the API, through the carrier seam — no subject plugin knows the word `unscheduled`, which is the right place for it.
  2. AN ASYMMETRY WORTH A LOOK ON THE SCREEN HALF, found at C9 and not a C12 failure: a below-floor plan renders all twelve questions on screen, the four belonging to dropped units among them, with nothing marking which. The dropped LESSONS are cleanly separated into dropped_lp; their QUESTIONS sit in the ordinary assessment list, and the `unscheduled` flag does not survive into the view item's meta. Defensible under e09, but the lesson and its questions are held to opposite standards, and a teacher on a 5-period plan sees four questions for two sittings she was told she is not getting.

NOTE FOR WHOEVER RE-READS THIS: kumar3's mixed-duration plan was purged by C7's repair and has not been re-served (see the C6 note), so if C12 was checked against that file it was checked before the purge."""

C13 = """PASS 2026-08-13 — founder ruling: the failure paths are done, having been exercised on earlier subjects, and are not re-run per stage.

WHY THAT HOLDS, stated so the pass is readable rather than merely asserted: paths 1 and 2 are SUBJECT-AGNOSTIC API guards, not stage behaviour. "No underlying chapter yet." (404) fires from the genon chapter lookup before any subject plugin is reached, and "Period count implausibly large." / "At least one duration row is required." (400) are matrix validation on the request body. Neither can behave differently for english·middle than for the stages that proved them, because neither reaches the library.

PATH 4 WAS EXERCISED LIVE IN THIS STAGE, at C10 check 5, and its transcript is the C13.4 artefact: ch_08_canonical_p10.json was moved into backup/quarantine/english/vi/, the library glob then reported [12, 7] instead of [12, 10, 7], an X=9 request FELL to variant 12 instead of erroring, `genon.library` reported [12, 7] honestly, and the whole serialized response was searched for the quarantined filename and did not contain it. Nothing 500'd; the response named only live files. The variant was restored and X=9 returned to variant 10.

PATH 3 (unresolvable item anchor -> 500 "Canonical cannot be compiled: ..." naming the item, never a bare 500) is the one that is genuinely subject-shaped, since the anchor resolution differs per carrier family — english is 8-rule row 7, the (section x spine) PAIR key, the only pair in the table. It is covered by the founder's ruling and NOT re-run here. Recorded as the one path whose evidence is inherited rather than local, in case a later reader wants it exercised on the pair key specifically.

NOTHING RESEMBLING A TRACEBACK reached any body in the paths that were run."""


ROWS = {"C3": C3, "C6": C6, "C7": C7, "C12": C12, "C13": C13}


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s10_c3c6c7c12c13"))
    row = state["combos"][KEY]
    for step, comment in ROWS.items():
        by = "Kumar" if step in ("C6", "C12", "C13") else "Claude"
        row[step] = {"status": "pass", "by": by, "at": NOW, "comment": comment}
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    done = sorted((k for k in row if k != "provenance"), key=lambda x: int(x[1:]))
    print(f"tracker updated · {KEY} · {', '.join(ROWS)} pass · {NOW}")
    print(f"  C-steps now recorded: {done}")
    print(f"  statuses: {[row[k]['status'] for k in done]}")


if __name__ == "__main__":
    main()
