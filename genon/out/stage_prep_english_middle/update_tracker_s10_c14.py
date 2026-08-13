#!/usr/bin/env python3
"""S10 · english · middle — C14 (copyrights review) into the tracker."""
import datetime, json, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/middle"

C14 = """PASS 2026-08-13 — measured against the TEXTBOOK, on all 8 files (3 canonicals + 5 served plans), 19,355 teacher-facing words. Zero unattributed reproductions, zero wholesale lifts. One TOOLING DEFECT found and worked around; it is the most important thing in this note.

★ THE TOOLING DEFECT — `copyright_scan.py` COULD NOT FIND THE BOOK, AND SAID NOTHING.
Run as documented (`python3 genon/copyright_scan.py english vi 8`) it reports "source: ch_08_summary.json (1664 words)" and a confident 5 hits. THE TEXTBOOK CONTRIBUTED ZERO WORDS. Its PDF resolver globs `chapter\\s*0*{ch}` against textbooks/{subject}/{grade}/, i.e. it assumes the plan's chapter number is the PDF's chapter number. THE ENGLISH SPLIT BREAKS THAT ASSUMPTION EVERYWHERE: english VI/VII/VIII PDFs are named per UNIT ("Chapter 03 - Nurturing Nature.pdf", which contains chapters 7, 8 and 9), and english IX PDFs keep the ORIGINAL section numbering ("chapter 04 - Vitamin-M.pdf" is chapter 7). So for all 101 english chapters the glob matches nothing and the scan silently measures the plan against OUR OWN SUMMARY — which is Aruvi's derived asset, not the protected work. A clean report means only that the pipeline is not quoting itself.
THIS IS THE SAME CLASS OF SILENT HOLE S7 FIXED ON THE OTHER INPUT (2026-08-11: .txt-only summary loading made the summary count as zero on seven stages). Same failure, opposite side, and it means S11's C14 on english·secondary was also run without an automatic book comparison — its ARV-D-138 poem finding came from reading, not from this scanner. The mapping the resolver needs already exists in the summary: `_source_unit.unit_chapter_number` (3 for this chapter). Recorded for the founder; NOT fixed here, since C7's ruling was "amend the notes, nothing else".
C14 WAS THEREFORE RUN BY POINTING AT THE BOOK DIRECTLY: textbooks/english/vi/Chapter 03 - Nurturing Nature.pdf, 5,373 words, shingled at n=8, against every teacher-facing field via the scanner's own lp_fields + item_fields.

CHECK 1 — NO VERBATIM REPRODUCTION BEYOND SHORT QUOTATION. PASS.
  BOOK-ONLY overlap: 317 of 19,355 words matched by a run of >=8 words = 1.64%. 36 runs, 12 distinct strings, longest 14 words.
  Benchmark: maths·middle's C14 (2026-08-10) read 1.15% with a longest run of 18 words. So english·middle reaches slightly more of the chapter in aggregate and its longest lift is SHORTER.
  ALL 36 RUNS ARE IN LESSON-PLAN FIELDS. ZERO ARE IN ASSESSMENT ITEMS. That is the constitutional firewall holding against the book itself: the assessment generator is forbidden to read tasks_verbatim[] / question_bank[], and across 36 items in three canonicals not one 8-word sequence of the textbook appears. C3 had already shown no item recycles an EXERCISE; this shows none reproduces the BOOK.
  THE LONGEST RUN, and the only quotation of protected verse: 14 words in the standard's synthesis unit —
      "Teacher closes by reading the poem's final stanza once more — "I don't know how the world is made / And neither do my neighbours" — and invites one volunteer to share what they find beautiful or surprising about that ending."
  Two lines of a 17-line poem (13.7% of it), in curly quotation marks, named as "the poem's final stanza", framing a read-aloud. It is the same construction the founder ruled on at C3 ("a small lift taken out of the overall poem context within inverted commas with clear intent to frame a question around it... reading that line will mean nothing if the overall poem is not seen"). Consistent with that ruling, NOT a defect.
  THE OTHER ELEVEN are 8-10 word fragments of TEXTBOOK TASK AND QUESTION text — "the bird thought the world was made of straw", "how is a home different from a house", "with rhyming words at the end of each line", "and write the matching line from the poem". This is F2's exact shape, and it is what the constitution REQUIRES: LP Rule 9 mandates naming each task by its anchor plus a brief, and Rule 3 draws the tasks from the summary's tasks_verbatim. A plan that did NOT contain these strings could not tell a teacher which task to run. Eight to ten words of an instruction is a reference; none is a reproduction.
  TWO I LOOKED AT HARDEST, both read as legitimate in context:
    * the WORD BANK — "Teacher introduces the describing-words task on p.90 — words such as 'pointed', 'green', 'thin', 'brown', 'small', 'wooden', 'hanging', 'round'." The whole eight-word box, verbatim. But it is quoted, attributed to p.90, and the task is unusable without it — a teacher cannot run a describing-words exercise while withholding the words.
    * the DISTRACTOR — teacher_notes quoting 'The bird becomes blind due to leaves' to explain a predictable misreading. Nine words of one textbook option, quoted, for a pedagogical reason.

CHECK 2 — NO THIRD-PARTY MATERIAL THE TEXTBOOK DOES NOT CARRY. PASS. Zero brand or third-party names across all 8 files (scanned for the usual set), zero external image references, zero URLs, zero inline markup (<img>, <svg>, .jpg, .png). 13 populated visual_stimulus fields, every one a pipe-delimited table built from the section's own content (verified at C3). The poem and the listening transcript both come from the textbook itself, so the plan may reference them; the question is only how much it reproduces, which is check 1.

CHECK 3 — QUOTED SOURCE TEXT IS ATTRIBUTED. PASS. Every quotation carries its locator: the poem lines are "the poem's final stanza", the word bank is "the describing-words task on p.90", the distractor is named as a distractor, and all 32 task_briefs across the library carry a (p.NN) page locator — 100%, against 13 of 123 in the historical corpus. No unattributed quotation anywhere.

★ ONE STRUCTURAL LIMIT OF THIS MEASUREMENT, worth recording because it changes what C14 can promise on english. An 8-gram scan is BLIND TO A COMPLIANT POEM INCIPIT BY CONSTRUCTION: assessment Rule 3 caps the incipit at EIGHT WORDS, and this poem's lines run 4-7 words, so a correctly-cited line can never form an 8-word run. The scanner found zero poem lines in assessment items; reading found three (one in p10, two in p07 — the two locator incipits and the 12-word writing quotation, all ruled on by the founder at C3). The two mechanisms are complementary rather than redundant: the scanner catches wholesale lifting, and ONLY READING catches the poem rule. That is the honest reason C14 on a poem chapter cannot be automated away.

F2 STATUS. `docs/NCERT_copyright_review.md`'s sole open finding is "English verbatim task-text in served plans". This is the first english·middle library ever measured against its book. The finding is REAL but bounded: task-text fragments do appear, at 8-10 words, in the LESSON PLAN only, always with a page locator, and never in the assessment. Whether that bounded form closes F2 or merely characterises it is the founder's call at the human gate — it is a judgement about how much reference is reproduction, which is exactly the class C14 sends upward by design.

EXIT MET: zero unattributed or wholesale reproductions. No defect raised."""


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s10_c14"))
    state["combos"][KEY]["C14"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C14}
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    row = state["combos"][KEY]
    done = sorted((k for k in row if k != "provenance"), key=lambda x: int(x[1:]))
    print(f"tracker updated · {KEY} · C14 pass · {NOW}")
    print(f"  C-steps: {done}")


if __name__ == "__main__":
    main()
