#!/usr/bin/env python3
"""S11 · english · secondary — C8 (the X-1 -> X transition inspection) into the tracker."""
import datetime, json, pathlib, shutil
ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/secondary"

C8 = """INSPECTED 2026-08-12 - SIX TRANSITIONS READ, FOUR CLEAN, TWO JUMPY (one defect, ARV-D-136). Each read as the teacher meets it: sitting X-1 and sitting X in full, consecutively - titles, materials, every band, notes. Full evidence: docs/testing_artefacts/c8_english_ix_ch07.md

  X=8  fill/forward -2s   p10 self   VocGram -> Listening+Speaking      CLEAN
  X=9  fill/single -1s    p10 self   Listening+Speaking -> Writing      CLEAN   (below floor)
  X=11 SYNTHESIS BORROW   p10 <- 17  Beyond-the-Text -> Synthesis       JUMPY
  X=12 fill/single        p14 self   Writing -> Beyond-the-Text         CLEAN
  X=15 SYNTHESIS BORROW   p14 <- 17  Beyond-the-Text -> Synthesis       JUMPY
  X=16 fill/single        p17 self   Speaking+Writing -> Beyond-the-Text CLEAN
  fill/backward: N/A - the band produces none.
X=8 was not in the C6 serve set (no 8-period request was made), so it was derived in-process with serve_plan - deterministic, no API call - to cover the fill/forward class the sweep exercises.

THE TWO JUMPY ARE ONE DEFECT SEEN TWICE, AND IT IS THE BORROWED CLOSER. Sitting X opens model-grade in both: '...drawing freely on any part of the chapter they have read' and 'Students need not have covered every task to participate: the chapter's content is now the shared ground.' Then its third band - TWENTY OF THE FIFTY MINUTES - says 'Students COMPLETE THE DRAFT ARTICLE (Paragraphs 3 and 4)', with materials listing "Students' draft article". In the standard that is coherent: U15 drafts paragraphs 1-2 and U17 completes 3-4. BUT BOTH COMPACTS WRITE THE WHOLE ARTICLE IN ONE SITTING - p10's U9 'plan and draft their article ... they write the title at the top and their name and grade below it', p14's U11 'write their four-paragraph article independently' - so every borrowing class arrives with a FINISHED article and is told to write the two paragraphs it wrote two sittings ago. The hedge ('Those who have already completed the draft review it') was written for a few fast finishers and here covers the whole class. THE BORROWED UNIT IS COHERENT IN EXACTLY ONE OF THE THREE PLANS IT CAN APPEAR IN - ITS OWN.

THE FOUR CLEAN ONES, and a heuristic worth keeping: every clean opening move is either a text the teacher reads aloud or a structure the teacher models on the board (X=9 'Teacher models the four-paragraph article structure on the board', materials 'Writing paper or notebooks' - a blank; X=12 'Teacher asks students to recall the description of Grandpa's walking stick from the story', which assumes CHAPTER CONTENT and is exactly what a borrowed unit may assume; X=8 'Teacher reads the meditation podcast transcript aloud twice', whose notes go further and say 'treat the two activities as independent'). EVERY JUMPY OPENING MOVE REACHES FOR SOMETHING THE STUDENTS ARE HOLDING. That matches what the artefact rule already says and is a cheap way to read a transition.

REMEDY, IN C8's OWN ORDER. (1) Does the lender first-deal the section? N/A - Case 1 has one candidate by construction, the standard's synthesis. (2) Re-examine the tie-break? Nothing to re-examine, same reason. (3) HARDEN THE BRIEF - landed. The brief already said the synthesis 'must NOT assume any particular earlier activity, reading, discussion, homework or material actually happened'; the model obeyed that in its discussion bands and broke it in the last one, because CONTINUING a piece of work does not read as 'assuming an activity' - it reads as ordinary teaching. So top_brief_for now says the quiet part, the same treatment the artefact rule needed at S5: 'THE SYNTHESIS UNIT STARTS AND FINISHES ITS OWN WORK. It may DRAW ON what the chapter taught; it must not CONTINUE, complete, revise or hand back a piece of student work another unit began - no "complete the draft", no "finish the poster", no "return to the essay you started". A borrowing class may have done that work in one sitting, or in a different form, or not yet at all. Any writing, making or performing in this unit begins and ends inside its own minutes.' Standard-canonical brief only - it is the only plan carrying a travelling closer. A BRIEF CHANGE IS NOT A CONSTITUTION CHANGE: it triggers a --certify-only re-run, not the section 9 cascade, and no other stage's library re-opens. It does NOT repair this library - that is the founder's call at the human gate, alongside ARV-D-132.

DETECTOR ALREADY IN PLACE from C7: the scoped artefact patterns flag materials possessives and completion verbs, so the next library carrying this shape is visible at BUILD time rather than by reading two sittings side by side. tests/test_genon_carriers.py still 113 green after the brief change.

WHAT THE HUMAN GATE SHOULD READ: the C5 sweep table, the standard's synthesis unit, and THE X=11 PAIR specifically - a class that finished its article in sitting 9 being asked, in sitting 11, to write paragraphs 3 and 4 of it."""

DEFECT = {
    "id": "ARV-D-136", "combo": KEY, "step": "C8", "severity": "S2",
    "owner": "founder", "status": "open",
    "title": ("the borrowed SYNTHESIS unit continues a piece of student work another unit "
              "began — coherent in the standard, wrong in both plans that borrow it"),
    "evidence": (
        "C8 rated six transitions; the four self-fills are clean and BOTH Case-1 synthesis "
        "borrows (X=11 host p10, X=15 host p14) are jumpy, for one reason.\n\n"
        "The borrowed unit (the standard's U17) spends its last band — 20 of 50 minutes — on "
        "\"Students COMPLETE THE DRAFT ARTICLE 'Our Inspiring Elderly' (Paragraphs 3 and 4)\", "
        "with `materials: [\"Students' draft article (notebooks or draft sheets)\"]`.\n\n"
        "In its own plan that is coherent: U15 drafts Paragraphs 1 and 2, U17 completes 3 and "
        "4. BOTH COMPACTS WRITE THE WHOLE ARTICLE IN ONE SITTING — p10's U9 (\"plan and draft "
        "their article … they write the title at the top and their name and grade below it\", "
        "then peer-exchange and revise) and p14's U11 (\"write their four-paragraph article "
        "independently\"). So a borrowing class arrives with a FINISHED article and is "
        "instructed to write the two paragraphs it completed two sittings earlier. The hedge "
        "\"Those who have already completed the draft review it\" was written for a few fast "
        "finishers and here describes the entire class.\n\n"
        "The unit is coherent in exactly one of the three plans it can appear in — its own — "
        "which is the ARV-D-025 profile (a closing unit importing the lending plan's priors) "
        "arriving through student WORK rather than through prose.\n\n"
        "WHAT MAKES IT S2: it is 40% of a sitting, it is teacher-facing, and it lands on the "
        "one unit the engine is guaranteed to move between plans.\n\n"
        "REMEDY LANDED (deterministic, C8's step 3): `variant_plans.top_brief_for` now carries "
        "\"THE SYNTHESIS UNIT STARTS AND FINISHES ITS OWN WORK … it must not CONTINUE, "
        "complete, revise or hand back a piece of student work another unit began.\" The "
        "existing sentence forbade ASSUMING an earlier activity, which the model obeyed in its "
        "discussion bands — continuing work does not read as assuming an activity. Brief-level, "
        "so it triggers a `--certify-only` re-run and no §9 cascade; it does not repair THIS "
        "library. C7's scoped artefact patterns are the detector at build time.\n\n"
        "Related and distinct: ARV-D-132 is the same unit's `materials` line read at C3 as an "
        "authoring defect (accepted as authored). This row is the SERVE consequence, which the "
        "founder's C3 acceptance explicitly left open for C8."),
}


def main():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s11_c8"))
    state["combos"][KEY]["C8"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C8}
    assert ARVD_ID not in {d.get("id") for d in state["defects"]}
    DEFECT.update({"opened": NOW, "closed": None, "at": NOW})
    state["defects"].append(DEFECT)
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"tracker updated · {KEY} · C8 pass · defect {DEFECT['id']} · {NOW}")


ARVD_ID = DEFECT["id"]

if __name__ == "__main__":
    main()
