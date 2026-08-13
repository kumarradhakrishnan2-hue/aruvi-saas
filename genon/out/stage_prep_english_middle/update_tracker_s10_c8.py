#!/usr/bin/env python3
"""S10 · english · middle — C8 (the X-1 -> X transition inspection) into the tracker."""
import datetime, json, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/middle"

C8 = """PASS 2026-08-13 - zero JUMPY, one SERVICEABLE, no defect raised. Read on plans re-served from the REPAIRED canonicals (C7's clock repair purged the C6 files), every non-identity X in the sweep, sitting X-1 and sitting X in full and consecutively.

THE FIRST FINDING IS THAT THERE ARE ONLY TWO SEAMS TO INSPECT, AND IT IS A PROPERTY OF THE ENGINE RATHER THAN OF THIS CHAPTER. Of the seven non-identity asks, FIVE have no seam at all - the Xth unit the choice set picks is the one AUTHORED IMMEDIATELY AFTER the prefix's last unit, in the same canonical:
    X=5   p07 U4 -> p07 U5   adjacent (below floor, truncation of the 7)
    X=6   p07 U5 -> p07 U6   adjacent (below floor)
    X=9   p10 U8 -> p10 U9   adjacent
    X=13  full 12 served     surrender, no transition
    X=14  full 12 served     surrender, no transition
Every one reports self_fill: true. That is engine e14's SELF-PREFERENCE resolving the tie toward the plan being served, and on a dense registry (6 cells over 12 units) it resolves that way nearly always. C8 is correspondingly cheap here - the opposite of what S11 predicted for its own thin registry, where it expected the borrow to be a stranger's opening unit almost every time. WORTH CARRYING: a stage whose registry is dense makes this step cheap; the campaign should not read "C8 was quick" as "C8 was skipped".

TWO REAL SEAMS. Both skip exactly one authored unit.

JOINT 1 - X=8, fill/single, lender p10, SKIPS p10 U8. RATED **CLEAN**.
  X-1 is p10 U7 "Rhyming Words and Describing Words from the Poem" (Vocabulary/Grammar), closing with "Four or five students read their completed new stanzas aloud. The teacher notes on the board any creative rhyming pairs the class invented."
  The SKIPPED unit is p10 U8 "Picture-Poem Match and Word-Hunt Challenge" - fine-grained return to the poem's text, picture matching and a letter-pattern word hunt.
  X is p10 U9 "Homes and Materials: From Shell to Brick" (Beyond-the-Text), opening: "The teacher reads the 'Let us explore' prompt (p.91) aloud. Students think quietly for a moment about the bird's three homes - shell, straw nest, open sky - before the teacher asks: 'What is your home made of?'"
  WHY CLEAN: X opens on a fresh page and a fresh prompt, and its ONLY backward reference is to the POEM ("the bird's three homes - shell, straw nest, open sky"; its notes add "the poem's image of the straw nest" and "the poem's warm nest stanza"). All of that was taught in the reading units, which ARE in the prefix. Nothing in X refers to picture-matching, to the word hunt, or to anything U8 alone supplied. The register does shift - playful language work to reflective interdisciplinary discussion - but that shift belongs to the SPINE CHANGE (VocGram -> Beyond-text) and is present in the authored 10-unit plan too; it is not an artefact of the skip.

JOINT 2 - X=11, Case-1 SYNTHESIS borrow, lender 12, withholds top U11. RATED **SERVICEABLE**, and it is the one string in the stage that sits closest to the ARV-D-025 profile.
  X-1 is top U10 "From Shells to Homes: Materials and Meaning", whose closing band is unexpectedly helpful: "Teacher briefly notes the second part of 'Let us explore' on p.92 - different kinds of bird nests and the workers who build human homes - as an observation task students can pursue independently. No collected work is required." That p.92 material is EXACTLY what the withheld U11 teaches, so at X=11 the prefix's own last band hands it off as self-study. The seam is pre-absorbed. (In the full 12 it reads as mild redundancy - U10 says do it yourself, U11 then does it together - which is worth noting the other way round at the human gate.)
  The WITHHELD unit is top U11 "Bird Nests, Human Builders, and Community Workers".
  X is top U12, the mandated synthesis: reads the whole poem aloud, discusses the four stages against growing up, a sustained personal write, closes on the final stanza.
  THE ONE BREACH, AND IT IS ONE WORD: U12's teacher_notes say the unit "draws together the poem's central theme ... as discussed through reading, speaking, writing, and the beyond-text explorations of homes AND COMMUNITY". "Homes" is U10 and is in the prefix; "community" is U11 and is not. The teacher is told the class explored something it did not.
  WHY SERVICEABLE RATHER THAN JUMPY: nothing in the unit DEPENDS on it. All four bands are poem-only - read the poem, discuss its four stages, write about a chosen stanza, close on the final stanza - and not one task, question or material needs the community-workers content. The same note carries an explicit self-containment claim that HOLDS for everything it governs: "Any student encountering the poem for the first time in this unit has everything they need; the poem itself is the only text required." A teacher reads "and community", did not teach it, and proceeds identically: a visible assumption absorbed without preparation loss, which is the definition. Jumpy requires X to PRESUME exposure the prefix never gave; this MENTIONS it in a backward-looking summary and presumes nothing.
  REMEDY, recorded not applied (founder's call, and it is deterministic as C8 requires - no LLM in the request path): the mechanism worked and one word in an enumeration slipped past it. The synthesis unit is authored to close a plan where U11 exists and is then borrowed into one where it does not, so the fix is in `top_brief_for`'s self-containment wording - the brief already asks for a synthesis that assumes nothing, and could ask specifically that any recap of what the class has done name the POEM's own content rather than enumerate the units. Cheaper than a re-author and it protects every stage.

BELOW-FLOOR SERVES (X=5, X=6), inspected as C8 requires. Both are plain truncations of the 7-canonical with authored-adjacent units, so there is no seam to rate; the transition question there is how the plan ENDS. At X=6 the chapter closes on p07 U6, a Vocabulary/Grammar unit on rhyming and describing words, and the dropped p07 U7 (beyond_text) is declared in the coverage note and carried verbatim in result.dropped_units flagged unscheduled. So the plan ends on language work rather than on a reflective close - which is the honest declared cost of asking for one period below the floor, not a defect. The teacher is told exactly what she is not getting.

EXIT MET: a rating per inspected transition with quoted evidence; ZERO jumpy."""


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s10_c8"))
    state["combos"][KEY]["C8"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C8}
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"tracker updated · {KEY} · C8 pass · {NOW}")


if __name__ == "__main__":
    main()
