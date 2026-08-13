#!/usr/bin/env python3
"""copyright_scan.py — the deterministic floor under C14's copyright review (v1.0, 2026-08-06).

WHY THIS EXISTS. `docs/NCERT_copyright_review.md` §6 recommendation 4 asks for exactly this:
"add a scan that n-gram matches served-plan text against the summary verbatim fields and the
chapter summary itself, surfacing long matches for judgment. C14's manual spot-check then
audits the gate rather than being the gate — the same maturation C7 went through." Until this
existed, C14 was a human reading a 12-unit plan beside a 30-page PDF and hoping to notice.

WHAT IT DOES. Shingles the SOURCE (the chapter's textbook PDF, plus the chapter summary) into
overlapping n-word windows, then slides the same window over every teacher-facing string in a
plan and reports the MAXIMAL RUNS of consecutive matching windows. A run of length L means L
consecutive words appear verbatim in the source. Sorted longest first, because length is the
whole question: a 6-word collision is the English language, a 40-word collision is a lifted
passage.

WHAT IT DOES NOT DECIDE, stated plainly. It does not decide whether a hit is a defect. "How
much quotation is short" and "is this paraphrase too close" are the subjective calls C14 sends
to the human gate by design. This tool's job is to make sure nobody has to FIND them by eye.
It also cannot see paraphrase — a passage reworded sentence by sentence scans clean, which is
the same blind spot register_scan.py documents. The scanner carries the floor; judgment sits
on top of it.

EXEMPTIONS, and why each is safe:
  * `section_anchor` — drawn verbatim from the section registry BY DESIGN (V2). Structural
    references, not reproduced content; the copyright review says so at §5.
  * `section_context` and LO rows — internal, never teacher-facing (same rule as register_scan).
  * Chemical names, formulae, unit names and the like will collide and should: "the mass number
    is the sum of protons and neutrons" is a definition, not an expression. Short runs are
    reported but the report's own threshold is what a reader should look at.

    python3 genon/copyright_scan.py science ix 8 [--n 8] [--min-run 12]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO))

CONTENT = REPO / "data" / "content"
TEXTBOOKS = REPO / "textbooks"

WORD = re.compile(r"[a-z0-9]+")


def norm_words(text: str) -> list:
    """Lowercase word list — punctuation, casing and whitespace are not the question."""
    return WORD.findall(str(text or "").lower())


def shingles(words: list, n: int) -> set:
    return {tuple(words[i:i + n]) for i in range(len(words) - n + 1)}


def longest_runs(words: list, source: set, n: int):
    """Maximal runs of consecutive matching n-grams → [(start_word, run_length_in_words)]."""
    if len(words) < n:
        return []
    hit = [tuple(words[i:i + n]) in source for i in range(len(words) - n + 1)]
    runs, i = [], 0
    while i < len(hit):
        if hit[i]:
            j = i
            while j + 1 < len(hit) and hit[j + 1]:
                j += 1
            runs.append((i, (j - i) + n))     # words covered by the run
            i = j + 1
        else:
            i += 1
    return runs


# ── the teacher-facing surface ────────────────────────────────────────────────────────────
def lp_fields(plan: dict):
    """Every teacher-facing string in a lesson plan, dropped units INCLUDED (C14 says so)."""
    result = plan.get("result", plan)
    buckets = [("served", result.get("lesson_plan", {}).get("periods") or []),
               ("dropped", result.get("dropped_units") or [])]
    for origin, periods in buckets:
        for u in periods:
            un = u.get("period_number")
            yield f"{origin} u{un} activity_title", u.get("activity_title")
            yield f"{origin} u{un} teacher_notes", u.get("teacher_notes")
            for h in (u.get("homework") or []):
                yield f"{origin} u{un} homework", h
            for i, b in enumerate(u.get("time_bands") or u.get("phases") or [], 1):
                yield f"{origin} u{un} band{i}", b.get("activity") or b.get("description")
            # visual_aids is a STRING on science·secondary and a LIST elsewhere. Iterating a
            # string yields CHARACTERS — 3 769 one-letter "fields" on this chapter, every one
            # scanning clean, which is the silent-miss failure register_scan.py warns about.
            # Normalise the shape before iterating, never after.
            va = u.get("visual_aids")
            for v in ([va] if isinstance(va, str) else (va or [])):
                yield f"{origin} u{un} visual_aid", (v if isinstance(v, str)
                                                     else json.dumps(v, ensure_ascii=False))
            # section_anchor is EXEMPT (registry-verbatim by design)


def item_fields(plan: dict):
    """Every teacher- or student-facing string in an assessment item, through the carrier seam."""
    from aruvi_core.genon import carriers
    result = plan.get("result", plan)
    for n, it in enumerate(carriers.raw_item_list(result), 1):
        if not isinstance(it, dict):
            continue
        yield f"item{n} question_text", it.get("question_text")
        yield f"item{n} task", it.get("task")
        yield f"item{n} scaffold", it.get("scaffold")
        for o in (it.get("options") or []):
            yield f"item{n} option", (o if isinstance(o, str) else o.get("text") or json.dumps(o, ensure_ascii=False))
        vs = it.get("visual_stimulus")
        if vs:
            yield f"item{n} visual_stimulus", (vs if isinstance(vs, str)
                                               else json.dumps(vs, ensure_ascii=False))
        for k in ("expected_elements", "look_for"):
            for e in (it.get(k) or []):
                yield f"item{n} {k}", e


def _json_strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from _json_strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from _json_strings(v)


def load_source(subject: str, grade: str, ch: int, book_only: bool = False) -> tuple:
    """The chapter's textbook PDF text + the chapter summary — the two things a plan could lift.

    BOTH SUMMARY SHAPES, and this was a silent hole (fixed 2026-08-11, at S7's C14). This
    read only `ch_NN_summary.txt`. Science and social_sciences carry `.txt`; mathematics,
    english and the_world_around_us carry `.json` — SEVEN of the eleven stages — so on every
    one of those the summary contributed ZERO words and the scan reported a confident clean
    against the PDF alone. Nothing said so.

    `book_only` keeps the two APART when the question is copyright. The textbook is the
    protected work; the summary is Aruvi's own derived asset, so a run matching the summary
    but not the book is the pipeline quoting itself. Merging them makes the two
    indistinguishable in the report — scan twice and diff, rather than once and guess.
    """
    words, parts = [], []
    # THE SPLIT-CHAPTER RESOLVER (fixed 2026-08-13, at S9's C14) ─────────────────────────
    # This globbed `chapter\s*0*{ch}` against the PDF names and assumed the PLAN's chapter
    # number is the BOOK's. English breaks that everywhere, because its chapters were split
    # out of textbook UNITS: VI/VII/VIII PDFs are named per unit ("Chapter 03 - Nurturing
    # Nature.pdf" contains chapters 7, 8 and 9) and IX keeps the original section numbering
    # ("chapter 04 - Vitamin-M.pdf" is chapter 7). The copyright review recorded the
    # consequence as "matches nothing on all 101 English chapters, so the book contributes
    # ZERO words and the scan reports a confident result against Aruvi's own summary".
    #
    # AT PREPARATORY IT IS WORSE THAN NOTHING, and that is why this is now fixed rather than
    # worked around by hand a fourth time. English III has 12 unit-chapters and 17 split
    # chapters, so the two numbering spaces COLLIDE: the glob resolves split ch 11
    # ("The Big Laddoo", unit ch 7) to "chapter 11 - Chanda Mama Counts the Stars.pdf" — a
    # DIFFERENT CHAPTER'S BOOK — and scores against it. A wrong book scores ~0% overlap and
    # reads as a clean pass, which is the most expensive way for this check to fail.
    #
    # The mapping needed was in the split summary all along: `_source_unit.unit_chapter_number`.
    # Read it first and fall back to the plan's own number for every unsplit subject, so this
    # is additive — no non-english stage changes behaviour.
    book_ch = ch
    for ext, load in ((".json", lambda p: json.load(open(p))),):
        s = CONTENT / "chapters" / subject / grade / "summaries" / f"ch_{ch:02d}_summary{ext}"
        if s.exists():
            try:
                src = (load(s) or {}).get("_source_unit") or {}
                if src.get("unit_chapter_number"):
                    book_ch = int(src["unit_chapter_number"])
            except Exception:                                    # noqa: BLE001
                pass
    pdfs = sorted(p for p in (TEXTBOOKS / subject / grade).glob("*.pdf")
                  if re.match(rf"chapter\s*0*{book_ch}\b", p.name, re.I))
    if book_ch != ch:
        parts.append(f"[split chapter: plan ch {ch} -> textbook unit ch {book_ch}]")
    for p in pdfs:
        import pdfplumber
        with pdfplumber.open(p) as doc:
            t = "\n".join((pg.extract_text() or "") for pg in doc.pages)
        words += norm_words(t); parts.append(f"{p.name} ({len(norm_words(t))} words)")
    if book_only:
        return words, parts
    base = CONTENT / "chapters" / subject / grade / "summaries" / f"ch_{ch:02d}_summary"
    for s, reader in ((base.with_suffix(".txt"), lambda p: p.read_text(encoding="utf8",
                                                                      errors="replace")),
                      (base.with_suffix(".json"),
                       lambda p: " ".join(_json_strings(json.load(open(p)))))):
        if s.exists():
            t = reader(s)
            words += norm_words(t); parts.append(f"{s.name} ({len(norm_words(t))} words)")
    return words, parts


def scan_plan(path: Path, source: set, n: int, min_run: int) -> list:
    plan = json.load(open(path))
    hits = []
    for label, text in list(lp_fields(plan)) + list(item_fields(plan)):
        w = norm_words(text)
        for start, length in longest_runs(w, source, n):
            if length >= min_run:
                hits.append({"file": path.name, "field": label, "words": length,
                             "text": " ".join(w[start:start + length])})
    return sorted(hits, key=lambda h: -h["words"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("subject"); ap.add_argument("grade"); ap.add_argument("chapter", type=int)
    ap.add_argument("--n", type=int, default=8, help="shingle width in words")
    ap.add_argument("--min-run", type=int, default=12, help="report runs at least this long")
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--book-only", action="store_true",
                    help="textbook PDF alone — the copyright question, without Aruvi's own summary")
    a = ap.parse_args()

    src_words, parts = load_source(a.subject, a.grade, a.chapter, book_only=a.book_only)
    if not src_words:
        print("NO SOURCE FOUND — cannot scan. Looked for "
              f"{TEXTBOOKS / a.subject / a.grade} and the chapter summary."); return 2
    source = shingles(src_words, a.n)
    print(f"source: {' + '.join(parts)}  →  {len(source)} distinct {a.n}-grams")

    d = CONTENT / "saved_plans" / a.subject / a.grade
    files = sorted(p for p in d.glob(f"ch_{a.chapter:02d}_*.json"))
    print(f"scanning {len(files)} file(s) in {d}\n")

    all_hits, scanned = [], 0
    for p in files:
        try:
            hits = scan_plan(p, source, a.n, a.min_run)
        except Exception as e:                       # a malformed file must be loud, not skipped
            print(f"   !! {p.name}: {type(e).__name__}: {e}"); continue
        scanned += 1
        all_hits += hits
        print(f"   {p.name:44s} {len(hits):3d} run(s) ≥ {a.min_run} words")

    print(f"\n{len(all_hits)} hit(s) across {scanned} file(s), longest first:\n")
    for h in all_hits[:a.top]:
        print(f"   {h['words']:3d} words · {h['file']} · {h['field']}")
        print(f"        \"{h['text'][:220]}\"")
    if not all_hits:
        print("   NONE — no run of "
              f"{a.min_run}+ words in any teacher-facing field appears verbatim in the source.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
