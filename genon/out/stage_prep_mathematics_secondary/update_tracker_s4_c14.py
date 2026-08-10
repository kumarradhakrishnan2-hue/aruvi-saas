#!/usr/bin/env python3
"""S4 · C14 — copyrights review (2026-08-10). PASS."""
import datetime, json, pathlib, shutil
ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()

C14 = """PASS — 2026-08-10. Reviewed against docs/NCERT_copyright_review.md v1.1, over ALL TEN
files on disk for this chapter (3 canonicals + 7 served plans), every teacher- and
student-facing string: activity titles, teacher notes, time bands, homework, question stems,
tasks, scaffolds, expected_elements, look_for and visual_stimulus — 964 strings in total.
Source of truth: textbooks/mathematics/ix/'chapter 04 - Exploring Algebraic identities.pdf',
24 pages, 32,596 characters extracted.

1 NO VERBATIM REPRODUCTION — PASS, and measured rather than eyeballed. Method: for every
string, the LONGEST RUN OF CONSECUTIVE WORDS also present in the chapter text, after
whitespace/punctuation/case normalisation.
  RESULT: zero strings share an 8+ word run with the textbook, in any of the ten files.
  DETECTOR VALIDATED FIRST, because a clean zero is exactly what a broken check returns: a
  sentence copied out of the PDF ('In this chapter, we will take the next step by exploring
  algebraic identities.') is detected at a 10-word run. The detector works; the zero is real.
  The full distribution across the three canonicals, at a 4-word floor: 7 words x2, 6 x1,
  5 x12, 4 x35, and 339 strings sharing nothing. The longest overlaps are unavoidable
  mathematical phrasing — 'find possible expressions for the length and', 'add the smallest
  and the largest', 'draw a square of side' — not lifted prose. Nothing approaches the
  short-quotation threshold, let alone passes it.

2 NO THIRD-PARTY MATERIAL — PASS. Zero brand or trademark mentions across all ten files
(scanned for the usual Indian and global marks). visual_stimulus: 0 items carry one on this
chapter, so 0 externally-sourced images, and no url/<img>/xlink reference anywhere. This
chapter is algebra — no poem, lyric or story excerpt is in scope, which is worth stating
plainly rather than reporting a hollow pass: the F2 risk lives in ENGLISH, not here.

3 QUOTED TEXT IS ATTRIBUTED — PASS, vacuously and correctly. Zero passages appear in
typographic quotes in any real field value, so nothing is presented as a quotation and there
is nothing to attribute. (An initial scan reported 2,382 'quotations' — that was the regex
matching JSON string delimiters in the serialised blob, not the field values. Corrected;
recorded because the false positive is an easy one to repeat.)
References into the book are LOCATORS, which is the compliant pattern the review's T5 answer
depends on: 'Exercise 4.1 Q1 (i)-(iii) from p.71', 'Examples 5 and 6 (pp.72...)', 'End of
Chapter Q8 and Q9 (pp.90...)'. A locator points INTO a book the school already owns and
reproduces nothing of it.

F2 — THE SOLE OPEN CAMPAIGN FINDING — IS NOT ENGAGED BY THIS STAGE. F2 is the English
inline-substitution conduit that carries textbook task text verbatim into served plans.
Mathematics·secondary has no such conduit: its textbook references are book_ref locators by
constitutional rule (LP Rule 9 P5, reinforced when ARV-D-073 stripped 27 internal ids at C3),
and the measurement above confirms the rule holds in fact and not just on paper. F2 stays
open and stays owed by S9/S10/S11.

Section titles drawn verbatim into section_anchor are EXEMPT by the review's own reasoning
(structural references, below the originality threshold) and were excluded from the runs above,
as C14 check 1 directs."""

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_c14"))
c = state["combos"]["mathematics/secondary"]
c["C14"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C14}
state["updated_at"] = NOW
STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
print("C14 = pass")
print("S4:", {k: v.get("status") for k, v in c.items() if isinstance(v, dict) and k.startswith("C")})
