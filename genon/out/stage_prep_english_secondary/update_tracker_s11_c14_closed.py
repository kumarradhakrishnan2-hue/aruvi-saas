#!/usr/bin/env python3
"""S11 — ARV-D-138 closed by assessment v1.5 (the poem locator); C14 comment updated."""
import datetime, json, pathlib, shutil
ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/secondary"

ADD = """

--- ARV-D-138 CLOSED 2026-08-12: ASSESSMENT v1.4 -> v1.5, THE POEM LOCATOR. ---
Founder ruling: fix now rather than accept or defer. Two checks changed the design from the first proposal.

(a) IS poem_appreciation_summary THE SAFE SUBSTITUTE? Mostly, not cleanly. Measured across all eight poem chapters: it is Aruvi's own critical prose (108-189 words) with a longest verbatim run against the textbooks of ZERO words in seven of eight and a five-word fragment in ch 10 - but THREE chapters quote short lines inside the commentary (ch 2 "she's peerless, let's praise her!", ch 8 the refrain "I cannot remember my mother" x3, ch 16 "Step up to the challenge"). Four to six words each, attributed, embedded in criticism. Pointing the extract block at it would NARROW the conduit, not close it, and would also cost the pedagogy, because an extract-analysis question on a poem IS 'read these lines closely'.

(b) SO THE FIX IS THE ONE THE COPYRIGHT REVIEW ITSELF NAMES - paraphrase + page ref. The student is holding the textbook; the stimulus does not have to reproduce the poem to point at it. AND THE INCIPIT IS PART OF THE DESIGN, NOT A HEDGE: NCERT prints NO line numbers on its poems and ch 2's stanzas break across a page boundary mid-poem, so 'lines 5-8' alone would have a student counting. A few words of the first line find it at once, identify rather than substitute, and are the convention of every citation index and exam paper. The cap is hard and in the rule: AT MOST EIGHT WORDS, one line, no ellipsis, no second fragment.

FIVE EDIT SITES, not the one I first claimed - the permission was written in five places and I had missed two (Rule 4's type definition, which also carried an 'or inline' escape into item_stem, and the schema comment): Rule 4 type definition | Rule 3 REQUIRED | Rule 9 opening | Rule 9 permitted formats (one bullet splits into extract block for prose/drama and POEM LOCATOR) | the visual_stimulus schema comment.

READING IS UNTOUCHED. INPUTS section 2, Rule 2(a) and Rule 6 still name poem_text as a content source - reading the poem is what makes a good question possible, and the summary never leaves the machine. Only REPRODUCTION into the artefact is closed; the edit script asserts poem_text survives in exactly those three read sites and nowhere else.

SECTION 9 - RE-AUTHORS NOTHING. A constitution change normally re-opens the stage; this one restricts a path the installed library does not use. ch 7 is PROSE, its single stimulus is a prose extract from prose_summary, no locator applies - so it satisfies v1.5 exactly as it satisfied v1.4, checked clause by clause rather than assumed. No poem-chapter library exists anywhere, which is why this was free today and would not have been after the first poem chapter was generated.

INHERITED BY S9 AND S10: the same five edits belong in english preparatory and middle at their own P2, before any poem chapter of theirs is authored. Artefacts: assessment_constitution_v1.4_pre_poem_locator.txt, assess_v1.4_to_v1.5.diff, apply_s11_poem_locator.py."""


def main():
    st = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s11_c14_closed"))
    c = st["combos"][KEY]
    c["C14"]["comment"] += ADD
    c["C14"]["at"] = NOW
    # the stage's landed pair moves with it
    c["provenance"]["as_ver"] = "1.5"
    for d in st["defects"]:
        if d.get("id") == "ARV-D-138":
            d["status"] = "closed"; d["closed"] = NOW; d["at"] = NOW
            d["evidence"] += (
                "\n\nCLOSED 2026-08-12 BY ASSESSMENT v1.5 — the poem locator. Rule 9 now "
                "carries two stimulus forms: the verbatim extract block, restricted to "
                "`prose_summary` / `drama_summary` (Aruvi's own prose, which is what makes "
                "reproducing it safe), and — the ONLY permitted form for a poem section — a "
                "LOCATOR: `Read lines N–M on p.PP, beginning \"<incipit>\".`, incipit capped at "
                "EIGHT WORDS, no ellipsis, no second fragment, and the poem's lines copied into "
                "no field at all. Rule 4's type definition, Rule 3's REQUIRED list and the "
                "schema comment carry the matching edits; the 'or inline' escape into "
                "`item_stem` is closed for poems.\n\n"
                "THE APPRECIATION-SUMMARY ROUTE WAS MEASURED AND REJECTED as the primary fix: "
                "it is Aruvi's prose (zero verbatim runs in seven of eight chapters) but three "
                "chapters quote 4–6 word lines inside the commentary, so it narrows the conduit "
                "rather than closing it — and it costs the pedagogy, since an extract-analysis "
                "question on a poem is 'read these lines closely'. The locator keeps the "
                "reading and removes the reproduction.\n\n"
                "Reading `poem_text` is deliberately still permitted (INPUTS §2, Rule 2(a), "
                "Rule 6) — the summary never leaves the machine. §9 re-authors nothing: ch 7 is "
                "prose and satisfies v1.5 unchanged, and no poem-chapter library exists.")
    st["updated_at"] = NOW
    STATE.write_text(json.dumps(st, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"ARV-D-138 closed · C14 comment updated · landed pair now LP v1.2 / assessment v1.5 · {NOW}")


if __name__ == "__main__":
    main()
