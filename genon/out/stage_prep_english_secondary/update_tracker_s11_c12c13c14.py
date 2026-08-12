#!/usr/bin/env python3
"""S11 — C12 + C13 green (founder attestation), C14 checked, ARV-D-138 filed."""
import datetime, json, pathlib, shutil
ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/secondary"

C12 = """PASS 2026-08-12 - FOUNDER ATTESTATION. Kumar ran the online view and the export surfaces for this chapter and reports them correct; recorded on his word rather than on an inspection of mine, which is the honest provenance. Not independently verified in this session: the e09 split (dropped units render online via view.dropped_lp and are omitted from exports), the chapter-notes and bookmark sub-checks (C12.3/C12.4), and C9's one carried item - that exports omit exactly the `unscheduled` items, which for this chapter means the single beyond_text question on the X=9 serve."""

C13 = """PASS 2026-08-12 - FOUNDER RULING, on cross-stage evidence. C13 has been run in full at earlier stages (science-IX ch 8, maths-IX ch 4, SS-middle) and the founder judges that sufficient for this stage: the renderers are subject-agnostic and english introduces no new stimulus format - its Rule 9 permits only a pipe table or a verbatim extract block, and this library carries ONE stimulus, an extract block on the EXTRACT_ANALYSIS item, which is plain prose lines. No SVG, no number_line, no new branch. Recorded as attested rather than independently re-run here."""

C14 = """CHECKED 2026-08-12 - PASS on the pilot, ONE DEFECT AGAINST THE STAGE (ARV-D-138, S2). Full table: docs/testing_artefacts/c14_english_ix_ch07.md. This is the stage that OWNS the campaign's sole open copyright finding (NCERT_copyright_review v1.1, F2 - 'English verbatim task-text in served plans').

METHOD, and it is not a spot-check: the chapter PDF was extracted (textbooks/english/ix/chapter 04 - Vitamin-M.pdf, 1,602 lines) and for EVERY teacher-facing string in the top canonical - 66 bands, 17 titles, 17 notes, 20 briefs, 6 stems, 1 stimulus, 20 rubric bullets - the longest word-run appearing verbatim in the PDF was computed (normalised case/whitespace, minimum 6 words).

1 VERBATIM REPRODUCTION - PASS, subjective on two strings. Exactly TWO surfaces in 17 units carry a >=6-word run, both exercise instructions rather than literary text: U1 'an elderly person at home or in' (7w) and U7 'one advantage and one disadvantage of' (6w). EVERY ASSESSMENT ITEM HAS ZERO runs of 6+ words.
2 THIRD-PARTY MATERIAL - PASS. 'The Lost Child' by Mulk Raj Anand is referenced, never reproduced: author named, pp.120-125 given, not a line quoted. No lyrics, brand text or images.
3 ATTRIBUTION - PASS.

THE EXTRACT_ANALYSIS STIMULUS EXONERATES THE DESIGN ON A PROSE CHAPTER. Rule 9 asks for 'a short passage copied VERBATIM', which sounds like the F2 conduit; it is not, because the extract is verbatim from ARUVI'S OWN prose_summary - longest shared run with the summary 12 words, and ZERO 6-word runs shared with the textbook. The chain is NCERT text -> Aruvi's paraphrase -> the item, so what reaches the cloud is Aruvi's prose.

ARV-D-138: THE SAME RULE READS DIFFERENTLY ON A POEM, AND 9 OF THIS CLASS'S 16 CHAPTERS ARE POEMS. Rule 9's [SECONDARY DELTA] permits the extract block to be drawn from poem_text, and Rule 3 licenses an item to use 'a specific line, image, or phrase from poem_text'. poem_text is NOT a paraphrase - it is the poem. Measured on ch 2 'Bharat Our Land': the summary carries 16 poem lines and 13 OF THEM APPEAR VERBATIM IN THE NCERT PDF. So a poem chapter's item would place 3-8 lines of an NCERT-published poem into a canonical, and canonicals are exactly what the v1.1 ruling sends to the cloud. Nothing in THIS library is affected (ch 7 is prose) - the exposure is in the constitution, not the artefact. THE CHEAP FIX IS ALREADY IN THE FILE: poem sections carry poem_appreciation_summary, Aruvi's own writing, which is what makes the prose path safe. One clause in Rule 9 - the extract block is drawn from prose_summary / drama_summary / poem_appreciation_summary, and poem_text may be cited by line reference but never reproduced - closes it without touching the item type or the pedagogy. A P2 amendment, so it would re-author any poem-chapter library authored before it; NONE EXISTS YET, which is why doing it now is free."""

DEFECT = {
    "id": "ARV-D-138", "combo": KEY, "step": "C14", "severity": "S2",
    "owner": "founder", "status": "open",
    "title": ("assessment Rule 9 licenses a 3–8 line verbatim extract from `poem_text`, which "
              "is the NCERT poem itself — F2's conduit, open on 9 of this class's 16 chapters"),
    "evidence": (
        "C14 measured every teacher-facing string of the ch 7 library against the extracted "
        "chapter PDF and found the pilot CLEAN: two 6–7 word exercise-instruction fragments in "
        "17 units, zero verbatim runs in any assessment item, and an EXTRACT_ANALYSIS stimulus "
        "that is verbatim from Aruvi's own `prose_summary` (12-word overlap with the summary, "
        "ZERO 6-word runs shared with the textbook). On a prose chapter the conduit is closed "
        "by construction.\n\n"
        "ON A POEM IT IS OPEN. Rule 9's [SECONDARY DELTA] permits the extract block to be drawn "
        "from `poem_text`, and Rule 3 licenses 'a specific line, image, or phrase from "
        "poem_text'. `poem_text` is not a paraphrase — it is the poem. Measured on ch 2 "
        "'Bharat Our Land': the summary carries 16 poem lines and **13 appear verbatim in the "
        "NCERT chapter PDF**. A poem chapter's item would therefore place 3–8 lines of an "
        "NCERT-published poem into a CANONICAL, and canonicals are precisely what the "
        "copyright review's v1.1 ruling sends to the cloud.\n\n"
        "This is F2 landing where `docs/NCERT_copyright_review.md` predicted it would: 'the "
        "verbatim conduit must be either closed (substitute a paraphrase + page ref) or "
        "licensed before English plans are served commercially.'\n\n"
        "SCALE: 9 of the 16 chapters in english IX are poems. Nothing in the ch 7 library is "
        "affected — the exposure is in the constitution, not the artefact — so this blocks no "
        "certification check, but it should be ruled on before the STAGE is certified, because "
        "certifying a stage is a statement about its constitution.\n\n"
        "REMEDY, and it is one clause: poem sections already carry "
        "`poem_appreciation_summary`, Aruvi's own writing — the very thing that makes the prose "
        "path safe. Rule 9 becomes 'the extract block is drawn from `prose_summary` / "
        "`drama_summary` / `poem_appreciation_summary`; `poem_text` may be cited by line "
        "reference but never reproduced'. A P2 amendment, so §9 would re-author any "
        "poem-chapter library authored under the old text — none exists yet, which is why "
        "doing it now costs nothing."),
}


def main():
    st = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s11_c12c13c14"))
    c = st["combos"][KEY]
    c["C12"] = {"status": "pass", "by": "Kumar", "at": NOW, "comment": C12}
    c["C13"] = {"status": "pass", "by": "Kumar", "at": NOW, "comment": C13}
    c["C14"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C14}
    assert DEFECT["id"] not in {d.get("id") for d in st["defects"]}
    DEFECT.update({"opened": NOW, "closed": None, "at": NOW})
    st["defects"].append(DEFECT)
    st["updated_at"] = NOW
    STATE.write_text(json.dumps(st, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"C12 + C13 pass (attested) · C14 pass · {DEFECT['id']} opened · {NOW}")


if __name__ == "__main__":
    main()
