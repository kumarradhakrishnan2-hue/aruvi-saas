#!/usr/bin/env python3
"""batch_stats.py — the F1 and F2 evidence record for a subject·stage (2026-08-13).

WHY IT EXISTS, and why the numbers are the deliverable rather than the verdict. F1 and F2
are the two batch steps a machine cannot decide: whether a borrowed lesson READS, and
whether a quotation is short enough. What a machine can do is establish, exactly and
reproducibly, **what was examined** — and that is the half a legal review needs, because
"we reviewed a sample" and "we reviewed every at-risk item" are different claims and only
one of them survives being asked how many.

So this tool asserts nothing about quality. It answers three questions per stage:

    F1  — how many joins existed, how many could carry the defect, how many were read
    F2  — how much of the teacher-facing text matches the textbook, where, and how much
          of that carries a locator
    both — what the instrument could not see

THE COVERAGE CLAIM IS THE POINT OF THE F1 BLOCK. A borrowed unit is only at risk when it
comes from a DIFFERENT canonical (a self-fill's priors are the serving plan's own units),
so the denominator that matters is the cross-canonical borrows, not the serves. Printing
all four numbers — serves swept, no-borrow, self-fill, cross-canonical — is what makes
"100% of at-risk joins were read" checkable by someone who does not trust us.

THE F2 BLOCK'S FIRST LINE IS `books resolved`, and it is first deliberately. The PDF
resolver was wrong for english until 2026-08-13 (ARV-D-155) and a wrong or missing book
scores ~0% overlap, which reads as a clean pass. A copyright statistic computed against no
source is worse than no statistic, so the record refuses to print a percentage without
saying how many chapters it actually had a book for.

WHAT IT CANNOT SEE, printed in every record so it is never implied away: paraphrase. A
passage reworded sentence by sentence scans clean. Every percentage here is a floor.

    python3 genon/batch_stats.py the_world_around_us iii iv v
    python3 genon/batch_stats.py social_sciences ix --out docs/batch_evidence/
"""
from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO))

from aruvi_core.genon import compile_stream, serve_plan                  # noqa: E402
from api.data import standard_duration_minutes                          # noqa: E402
from aruvi_core.genon.carriers import raw_item_list      # noqa: E402
from borrowed_seams import library                                       # noqa: E402
from copyright_scan import (                                             # noqa: E402
    item_fields, load_source, longest_runs, lp_fields, norm_words, shingles,
)

SAVED = REPO / "data" / "content" / "saved_plans"
# pdfplumber costs 0.5s on a text PDF and over 90s on an image-heavy one — SS·IX ch 2 and
# ch 3 are 37 MB and 29 MB and time out a whole-stage run on their own. The extracted words
# are a pure function of the file, so cache them keyed by (path, size, mtime): a stage-wide
# re-run then costs seconds, which is what makes this usable as a REPEATABLE evidence record
# rather than a one-off someone has to be talked into re-running.
CACHE = REPO / "genon" / "out" / "book_text_cache"
# `pp.232–233` is a locator and `p.109` is a locator; the second alternative used to be
# `\bp\.` , which matches only the single-page form — so every MULTI-page citation read as
# UNLOCATED and the attribution rate was understated by half (2026-08-14, S11 F2).
LOCATOR = re.compile(r"\b(?:textbook|book)\b[^.]{0,25}?\bp{1,2}\.?\s*\d|\bpp?\.\s?\d+", re.I)
POEM_TEXT = re.compile(r"\b(?:stanza|couplet|refrain|lyrics)\b", re.I)
BRAND = re.compile(r"\b(coca[- ]?cola|pepsi|maggi|amul|nestl[eé]|cadbury|parle|britannia|"
                   r"samsung|nike|adidas|mcdonald)\b", re.I)
IMG = re.compile(r"https?://|\.jpe?g\b|\.png\b|\.gif\b", re.I)


def cached_source(subject, grade, ch):
    """load_source(book_only) with the PDF extraction memoised on disk."""
    CACHE.mkdir(parents=True, exist_ok=True)
    key = CACHE / f"{subject}_{grade}_ch{ch:02d}.json"
    stamp = sorted((p.name, p.stat().st_size, int(p.stat().st_mtime))
                   for p in (REPO / "textbooks" / subject / grade).glob("*.pdf")) \
        if (REPO / "textbooks" / subject / grade).is_dir() else []
    if key.exists():
        try:
            blob = json.loads(key.read_text())
            if blob.get("stamp") == json.loads(json.dumps(stamp)):
                return blob["words"], blob["parts"]
        except Exception:                                                # noqa: BLE001
            pass
    words, parts = load_source(subject, grade, ch, book_only=True)
    key.write_text(json.dumps({"stamp": stamp, "words": words, "parts": parts}))
    return words, parts


def chapters_of(subject, grade):
    return sorted({int(re.search(r"ch_(\d+)", Path(p).name).group(1))
                   for p in glob.glob(str(SAVED / subject / grade / "ch_*_canonical*.json"))})


# ── F1: what existed, what was at risk, what was read ────────────────────────────

def f1_stats(subject, grades):
    s = Counter()
    per_chapter = []
    for grade in grades:
        dur = standard_duration_minutes(grade, subject)
        for ch in chapters_of(subject, grade):
            lib = library(subject, grade, ch)
            if not lib:
                continue
            streams = [x for _, x in lib]
            counts = sorted((len(x["units"]) for x in streams), reverse=True)
            s["chapters"] += 1
            s["canonicals"] += len(lib)
            borrowed = 0
            for x in range(max(1, counts[-1] - 2), counts[0] + 3):
                s["serves_swept"] += 1
                try:
                    g = serve_plan(streams, [(dur, x)])["genon"]
                except Exception:                                        # noqa: BLE001
                    s["serve_errors"] += 1
                    continue
                f = g.get("slot_fill") or {}
                if not f.get("borrowed_from"):
                    s["no_borrow"] += 1
                elif f.get("self_fill"):
                    s["self_fill"] += 1
                else:
                    s["cross_canonical"] += 1
                    borrowed += 1
            per_chapter.append((grade, ch, len(lib), counts, borrowed))
    return s, per_chapter


# ── F2: how much of the teacher-facing text is the book's ────────────────────────

def f2_stats(subject, grades, n=8, min_run=10):
    s = Counter()
    runs = []
    for grade in grades:
        for ch in chapters_of(subject, grade):
            src, _ = cached_source(subject, grade, ch)
            s["chapters"] += 1
            if not src:
                s["books_missing"] += 1
                continue
            s["books_resolved"] += 1
            s["book_words"] += len(src)
            S = shingles(src, n)
            for p in sorted(glob.glob(str(SAVED / subject / grade
                                          / f"ch_{ch:02d}_canonical*.json"))):
                plan = json.load(open(p))
                s["files"] += 1
                blob = json.dumps(plan.get("result") or {})
                s["brand_hits"] += len(BRAND.findall(blob))
                s["image_refs"] += len(IMG.findall(blob))
                s["verse_words"] += len(POEM_TEXT.findall(blob))
                # THROUGH THE CARRIER SEAM. Reading `assessment_items` directly counts the
                # SPINE GROUPS on english, which carry no `visual_stimulus`, so this
                # reported 0 while 85 items had one — the single number a legal reader
                # would rely on (2026-08-14, S11 F2).
                for it in raw_item_list(plan.get("result") or {}):
                    if isinstance(it, dict) and str(it.get("visual_stimulus") or "").strip():
                        s["visual_stimulus"] += 1
                for label, text in list(lp_fields(plan)) + list(item_fields(plan)):
                    w = norm_words(text)
                    s["words"] += len(w)
                    for st, ln in longest_runs(w, S, n):
                        s["matched_words"] += ln
                        if ln >= min_run:
                            runs.append({"grade": grade, "chapter": ch, "file": Path(p).name,
                                         "field": label, "len": ln,
                                         "text": " ".join(w[st:st + ln]),
                                         # attribution is judged on the FIELD the run sits
                                         # in — a locator two fields away is not a citation
                                         # the teacher can see
                                         "located": bool(LOCATOR.search(str(text)))})
    return s, sorted(runs, key=lambda r: -r["len"])


def render(subject, grades, f1, per_chapter, f2, runs, min_run):
    L = []
    A = L.append
    A(f"# Batch evidence record · {subject} · grade(s) {', '.join(grades)}")
    A(f"\nGenerated {datetime.now().isoformat(timespec='seconds')} by `genon/batch_stats.py`. "
      "Counts only — no verdict. Every figure is reproducible by re-running the command.\n")

    A("## F1 — the borrowed-seam review (C8 across the batch)\n")
    A("| measure | count |\n|---|---|")
    A(f"| chapters with a library on disk | {f1['chapters']} |")
    A(f"| canonicals | {f1['canonicals']} |")
    A(f"| period counts served (floor−2 … top+2) | {f1['serves_swept']} |")
    A(f"| … no borrowed slot (identity · truncation · surrender) | {f1['no_borrow']} |")
    A(f"| … SELF-fill — borrowed from the plan being served | {f1['self_fill']} |")
    A(f"| **… cross-canonical borrow — AT RISK** | **{f1['cross_canonical']}** |")
    if f1["serve_errors"]:
        A(f"| serve errors (excluded) | {f1['serve_errors']} |")
    atrisk = f1["cross_canonical"]
    A(f"\n**Coverage claim:** the at-risk population is the {atrisk} cross-canonical borrows, "
      f"not the {f1['serves_swept']} serves. A self-fill's borrowed unit takes its priors from "
      "the serving plan's own earlier units, so no foreign prior exists and there is nothing to "
      "inspect. Read the ratings recorded against F1 in the campaign tracker for the outcome; "
      "this record establishes only the denominator.\n")

    A("## F2 — the copyright review (C14 across the batch)\n")
    A("| measure | count |\n|---|---|")
    A(f"| chapters | {f2['chapters']} |")
    A(f"| **textbook PDFs resolved** | **{f2['books_resolved']}** |")
    A(f"| textbook PDFs NOT found | {f2['books_missing']} |")
    if f2["books_missing"]:
        A("| | ⚠ a chapter with no book scores 0% and reads as a clean pass — see ARV-D-155 |")
    A(f"| canonicals scanned | {f2['files']} |")
    A(f"| source words (textbook only, no Aruvi summary) | {f2['book_words']:,} |")
    A(f"| teacher-facing words scanned | {f2['words']:,} |")
    A(f"| words inside a book-matching run | {f2['matched_words']:,} |")
    pct = (f2["matched_words"] / f2["words"] * 100) if f2["words"] else 0
    A(f"| **share of teacher-facing text matching the book** | **{pct:.2f}%** |")
    A(f"| runs ≥ {min_run} words | {len(runs)} |")
    A(f"| longest run | {runs[0]['len'] if runs else 0} words |")
    loc = sum(1 for r in runs if r["located"])
    A(f"| … carrying a page locator in the same field | {loc} "
      f"({loc * 100 // len(runs) if runs else 0}%) |")
    A(f"| populated `visual_stimulus` on assessment items | {f2['visual_stimulus']} |")
    A(f"| external image references / URLs | {f2['image_refs']} |")
    A(f"| brand-name occurrences | {f2['brand_hits']} |")
    A(f"| verse-structure words (stanza · couplet · refrain · lyrics) | {f2['verse_words']} |")

    A("\n**What this instrument cannot see:** paraphrase. A passage reworded sentence by "
      "sentence produces no match, so every percentage above is a FLOOR, not a measurement of "
      "borrowing. `section_anchor` values are exempt by design (structural references drawn "
      "verbatim from the registry, per the copyright review §5) and are excluded from the "
      "teacher-facing word count.\n")

    if runs:
        A(f"### Every run of {max(14, min_run)}+ words, longest first\n")
        A("| words | chapter | field | locator | text |\n|---|---|---|---|---|")
        for r in runs:
            if r["len"] < max(14, min_run):
                continue
            A(f"| {r['len']} | {r['grade']}/ch{r['chapter']:02d} | {r['field']} | "
              f"{'yes' if r['located'] else '—'} | {r['text'][:150]} |")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("subject")
    ap.add_argument("grades", nargs="+")
    ap.add_argument("--min-run", type=int, default=10)
    ap.add_argument("--out", default="docs/batch_evidence")
    a = ap.parse_args()

    f1, per_chapter = f1_stats(a.subject, a.grades)
    f2, runs = f2_stats(a.subject, a.grades, min_run=a.min_run)
    md = render(a.subject, a.grades, f1, per_chapter, f2, runs, a.min_run)
    out = REPO / a.out / f"{a.subject}_{'-'.join(a.grades)}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(md)
    print(f"\n\nwritten: {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
