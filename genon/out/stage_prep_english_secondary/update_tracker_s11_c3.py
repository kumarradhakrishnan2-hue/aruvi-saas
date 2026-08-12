#!/usr/bin/env python3
"""S11 · english · secondary — C3 into the campaign tracker, with its five defects.

Run from the repo root:
    python3 genon/out/stage_prep_english_secondary/update_tracker_s11_c3.py

Full rule table: docs/testing_artefacts/c3_english_ix_ch07.md
"""
import datetime
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/secondary"

C3 = """CHECKED 2026-08-12 - PASS WITH FINDINGS. Both files rule by rule against LP v1.2 and assessment v1.4: ch_07_canonical.json (17 units, the standard) and ch_07_canonical_p10.json (10 units, the FLOOR compact - chosen deliberately, since that is where every stated number is under most pressure and where S11's own coverage amendment binds). Full table: docs/testing_artefacts/c3_english_ix_ch07.md. Maths determinate-answer sub-check: N/A (english carries no expected_answer on any item; same reason as S1/S2/S3/S5/S6).

WHAT HELD, and it is the part the P-prep was about:
- FULL SPINE COVERAGE HELD AT THE FLOOR. All six spines taught, six handoff cells, six items - in the 17 AND the 10. The corpus plan that prompted the amendment (ch 12, 4 periods) had dropped beyond_text outright.
- RULE 1'S CLOSING-UNIT EXCEPTION FIRED ON ITS FIRST LIVE RUN. U17 carries [reading_for_comprehension, writing], which are NOT adjacent in the on-page sequence; without this morning's amendment the standard's mandated closer would have been unauthorable (the certainty S8 recorded and S7 paid for).
- RULE 8A HELD ON ITS FIRST LIVE TEST: zero items emit period_ref, period_number or unit_ref in either file. The anchor is the (source_section_id + source_spine) pair and the platform resolves it.
- Register clean by scanner AND by eye on all 27 units; first-visit order equals the on-page order in both files while the handoff keeps canonical enumeration order - the two orders that are deliberately different both present and both right.
- Rule 2A honoured: the story is read aloud in explicit timed bands sized to text length (top U3 pp.97-102 over 25 min; p10 across U2/U3/U4), and materials carry a page range on 27 of 27 units.
- Assessment: types inside their spine's default map, answer layer exactly right (open carries expected_elements and no suggested_answer, closed the reverse, none carries both), source_lo and source_context byte-identical to the handoff, transcript_ref on the listening item only, extract blocks 4 lines within the 3-8 rule, zero internal ids in prose.

EIGHT FINDINGS, SEVEN OF THEM NUMBERS. Six of eight are a stated cap live generation did not respect, and TWO ARE CAPS THIS STAGE SET THIS MORNING: task_brief widened 12 -> 18 on a corpus max of 19, and generation produced 20; section_context widened 10-15 -> 10-18 on a corpus max of 17, and the compact produced 19 and 23. Rule 11's untouched 12-word bullet cap is breached by 8 of 30 bullets, and Rule 5's minimum-3-bands by 4 of p10's 10 units (ARV-D-128, filed at C2). THE LESSON, and it is the reusable part: the corpus used as evidence was authored UNDER the old caps and had been pulled toward them, so its maximum understates the free distribution - widen above the observed maximum by the margin the corpus was compressed by, or state the cap as guidance and let the certifier count breaches. Worth noting what did NOT drift: every FORMAT obligation held (the (p.NN) locator on 44 of 44 briefs, the 'Student ...' LO form on 12 of 12, the 3-5 bullet count, one section per unit, VocGram isolation). Format obligations hold; length obligations drift.

THE ONE FINDING THAT IS NOT A NUMBER - ARV-D-132, S2, and it lands on the borrowed unit. The synthesis unit U17 lists 'Students' draft article (notebooks or draft sheets)' in materials and asks students to COMPLETE the draft (Paragraphs 3 and 4) that U15 started. The standard brief forbids exactly this ('NO UNIT MAY DEPEND ON A PHYSICAL ARTEFACT ANOTHER UNIT PRODUCES'), and U17 is the Case-1 borrow: a teacher on 11 units gets p10's ten plus this unit, and p10's writing unit asks for the whole article in one sitting. The model half-obeyed - the band hedges and the teacher note says outright that students need not have covered every task - so the prose understood the independence requirement and materials did not. register_scan cannot catch it: this is a BACKWARD dependency, which the register permits; the artefact rule lives only in the brief and nothing enforces it. Flagged for C8, which inspects this exact transition.

THREE CERTIFIER CHECKS ARE NOW OWED, all free and all subject-agnostic: artefact language in materials/opening bands (this finding), band COUNT and tiling (ARV-D-128; normalize.phase_tiling_issues already exists), and the non-contiguous-section check inherited from S7/S8.

ALSO RECORDED, not raised: the installer drops stage / main_sections_inventory / periods_allocated from result into the saved-plan envelope (the model emitted them correctly - verified in the raw), and nothing reads them. And the MCQ path is untested at this stage: neither file contains an MCQ, so A9's arrangement, the keyed what_each_option_reveals and the four-option contract are all unexercised here."""

DEFECTS = [
    {
        "id": "ARV-D-129", "combo": KEY, "step": "C3", "severity": "S3",
        "owner": "founder", "status": "open",
        "title": ("LP Rule 4's diversity clause breached on the standard: `shared-reading` runs "
                  "three consecutive units"),
        "evidence": (
            "Rule 4: 'no spine's method may repeat across more than two consecutive periods "
            "(evaluated per spine)'. ch_07_canonical.json units 3, 4 and 5 all carry "
            "`reading_for_comprehension: shared-reading`.\n\n"
            "Everything else in Rule 4 holds on both files: `pedagogical_methods` keys equal "
            "`spines_taught` on all 27 units, every value is drawn from that spine's permitted "
            "list, and the top uses six of the nine permitted Reading methods. The floor "
            "compact is clean — five distinct Reading methods over five units — which is the "
            "useful detail: the breach is on the LONG canonical, where a single spine runs for "
            "eight units and the model settles into a groove.\n\n"
            "Reads as generation variance rather than a rule that cannot be met: pp.97–107 is "
            "a long read and shared-reading is the honest method for three sittings of it. The "
            "founder call is whether to accept (like ARV-D-019's slot miss), repair in place, "
            "or let Rule 4's clause stand and price the re-run."),
    },
    {
        "id": "ARV-D-130", "combo": KEY, "step": "C3", "severity": "S3",
        "owner": "founder", "status": "open",
        "title": ("internal question-type codes (MCQ, SCR) appear in teacher-facing band text "
                  "and teacher_notes, which LP Rule 9 forbids by name"),
        "evidence": (
            "Rule 9: 'no internal question-type codes (MCQ, SCR, ECR, EXTRACT_ANALYSIS, MATCH, "
            "FILL_IN, TRUE_FALSE, ORAL_PROMPT, WRITING_TASK, PROJECT — write these in plain "
            "words, e.g. \"multiple-choice\")'. Five hits:\n"
            "  top U6 band 2 — 'the emotion word choice (MCQ), completing the sentence …'\n"
            "  top U6 band 3 — 'Teacher-led discussion unpacks both MCQ items'\n"
            "  top U7 band 2 — 'the tone MCQ, why Ravi is confused and embarrassed (SCR)'\n"
            "  top U12 notes — 'The four MCQ items on sentence type are stepping stones …'\n"
            "  p10 U4 notes — 'The MCQ on emotion — nostalgic vs. wistful vs. regretful …'\n\n"
            "Note what the model was doing: it is describing the TEXTBOOK's own exercise items, "
            "not Aruvi's, and 'MCQ' is the shortest true label for them. The rule's remedy is "
            "in the rule ('multiple-choice'), so this is a wording repair, not a re-author.\n\n"
            "Rule 9 also mandates a lint — 'run aruvi-scripts/lint_lp_teacher_prose.py over the "
            "produced LP … a run is not complete until the lint passes'. Nothing in "
            "`build_library.py` runs it, so the mandated verification pass has never executed "
            "on a genon canonical. That is the real gap here: a rule with a tool attached, and "
            "no wiring."),
    },
    {
        "id": "ARV-D-131", "combo": KEY, "step": "C3", "severity": "S3",
        "owner": "founder", "status": "open",
        "title": ("three word caps breached by live generation — two of them widened at this "
                  "stage's P-prep the same morning, on corpus evidence that understated the "
                  "free distribution"),
        "evidence": (
            "  task_brief ≤ 18 w (LP Rule 9, widened from 12 at P1 today on a corpus max of "
            "19): one brief at 20 w — \"Learning Beyond the Text (p.120–125): read 'The Lost "
            "Child' by Mulk Raj Anand; discuss with class — attachment vs. desire.\"\n"
            "  section_context 10–18 w (LP Rule 10, widened from 10–15 today on a corpus max "
            "of 17): p10 runs 19 w and 23 w — \"Mulk Raj Anand's 'The Lost Child' — a child's "
            "suppressed desires at a festival fair and his desperate attachment when separated "
            "from parents.\" The standard is clean at 14–15 w.\n"
            "  expected_elements ≤ 12 w per bullet (assessment Rule 11, untouched since v1.0 "
            "and never measured): 8 of 30 bullets over, up to 16 w — e.g. 'The reversal shows "
            "Vidya, not Grandpa, misjudges — Vitamin-M targets assumption, not age.'\n\n"
            "THE REUSABLE FINDING, and it is about method rather than about english. P-prep "
            "measured the corpus and widened each cap just past the observed maximum. But the "
            "corpus was AUTHORED UNDER THE OLD CAPS and had been pulled toward them, so its "
            "maximum understates what generation does when freed. Widen above the observed "
            "maximum by the margin the corpus was compressed by — or state the cap as guidance "
            "and let the certifier count breaches instead of the constitution forbidding them.\n"
            "The counter-evidence is worth keeping too: every FORMAT obligation held on the "
            "same run (the (p.NN) locator on 44 of 44 briefs, the 'Student …' LO form 12 of 12, "
            "the 3–5 bullet count, one section per unit, VocGram isolation). Format obligations "
            "hold; length obligations drift.\n\n"
            "Founder call: relax all three to what generation actually produces (the S4 "
            "precedent), repair the six strings in place, or accept and price. Nothing here is "
            "teacher-visible as an error — the briefs and contexts read well at their length."),
    },
    {
        "id": "ARV-D-132", "combo": KEY, "step": "C3", "severity": "S2",
        "owner": "founder", "status": "open",
        "title": ("the mandated SYNTHESIS unit depends on a physical artefact another unit "
                  "produced — and it is the unit the serve engine borrows"),
        "evidence": (
            "ch_07_canonical.json U17 (the closing synthesis):\n"
            "  materials: \"Students' draft article (notebooks or draft sheets)\"\n"
            "  band [30–50]: 'Students COMPLETE the draft article \"Our Inspiring Elderly\" "
            "(Paragraphs 3 and 4 …)'\n"
            "The draft is produced at U15: 'Students draft Paragraphs 1 and 2 independently.'\n\n"
            "The standard-canonical brief forbids exactly this: 'NO UNIT MAY DEPEND ON A "
            "PHYSICAL ARTEFACT ANOTHER UNIT PRODUCES … A unit that lists \"prepared "
            "previously\", \"their charts from earlier\" or \"the models they built\" in "
            "`materials` is asking for a sitting that may not have happened.' U17 is the CASE-1 "
            "BORROW: a teacher on X=11 receives p10's ten units plus this one, and p10's writing "
            "unit (U9) asks for the WHOLE four-paragraph article in a single sitting — so the "
            "borrowed closer tells that class to finish paragraphs they either never started or "
            "already finished.\n\n"
            "TWO THINGS MAKE IT PRECISE. (1) The model half-obeyed: the band hedges ('Those who "
            "have already completed the draft review it …') and the teacher note says outright "
            "'Students need not have covered every task to participate: the chapter's content "
            "is now the shared ground.' The prose understood the independence requirement; "
            "`materials` did not. (2) `register_scan` CANNOT catch it — this is a BACKWARD "
            "dependency, which the register explicitly permits since v1.10; the artefact rule "
            "lives only in the brief and nothing enforces it.\n\n"
            "Same family as ARV-D-023 (e11, found at S1's C7): a borrowed unit assuming a "
            "sitting the host class never had. Flagged for C8, which inspects this transition "
            "directly. The cheap fix is a certifier check over `materials` and the opening band "
            "for artefact language — free, subject-agnostic, and the third such check now owed "
            "alongside band-count/tiling (ARV-D-128) and the non-contiguous-section check "
            "inherited from S7/S8."),
    },
    {
        "id": "ARV-D-133", "combo": KEY, "step": "C3", "severity": "S4",
        "owner": "Claude", "status": "open",
        "title": ("assessment Rule 12's `total_items` was never emitted, and the two canonicals "
                  "disagree on the SHAPE of `period_schedule`"),
        "evidence": (
            "(a) Rule 12 requires the assessment header to carry `total_items`. Neither file "
            "emits it. Nothing reads it — the count is derivable and the platform derives it — "
            "so this is a constitution/artefact mismatch rather than a functional defect: "
            "either the model should emit it or Rule 12 should drop it.\n\n"
            "(b) A1 says 'exactly ONE row {period_duration_minutes, period_count}'. The "
            "standard emits `[{...}]` (a list of one); the p10 compact emits `{...}` (a bare "
            "dict). Same chapter, same library, two shapes — from the same prompt. Nothing "
            "downstream breaks (the serve path reads `genon.matrix` / `served_matrix`, and the "
            "display reads `period_rows_snapshot`), which is exactly why it would survive "
            "unnoticed until something did read it.\n\n"
            "Both are cheap to close and neither justifies a re-author on its own; fold them "
            "into whatever pass repairs ARV-D-130/131."),
    },
]


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s11_c3"))
    state["combos"][KEY]["C3"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C3}

    have = {d.get("id") for d in state["defects"] if isinstance(d, dict)}
    for d in DEFECTS:
        assert d["id"] not in have, f"{d['id']} already filed"
        d.update({"opened": NOW, "closed": None, "at": NOW})
        state["defects"].append(d)

    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"tracker updated · {KEY} · C3 pass · defects "
          f"{', '.join(d['id'] for d in DEFECTS)} · {NOW}")


if __name__ == "__main__":
    main()
