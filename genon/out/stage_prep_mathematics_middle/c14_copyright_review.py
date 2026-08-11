#!/usr/bin/env python3
"""c14_copyright_review.py — S7 (mathematics·middle) C14, mathematics/vii chapter 7.

Why this exists beside genon/copyright_scan.py rather than replacing it:

  1. The shared scanner's `load_source` reads ONLY `ch_NN_summary.txt`. Mathematics·VII
     carries `ch_07_summary.json`, so the summary silently contributed ZERO words to the
     source and the scan ran against the PDF alone. This script loads both shapes.
  2. Six files sit on disk but the C6 matrix has ELEVEN rows, and the identity rows write
     no file at all. C7 read the SERVED set fresh in memory under e19 for exactly this
     reason; C14 does the same, so every teacher-facing string the matrix can produce is
     scanned, not just the ones that happened to be persisted.
  3. The detector is VALIDATED before its zero (or its hits) are believed — a positive
     control lifted from the PDF must be detected, or a clean report means nothing.
  4. Checks 2 and 3 (third-party material, attribution) are run over the same string set,
     so all three C14 checks read one surface.

    python3 genon/out/stage_prep_mathematics_middle/c14_copyright_review.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "genon"))

import copyright_scan as cs                                            # noqa: E402
from aruvi_core.genon.serve import serve_plan                          # noqa: E402

SUBJECT, GRADE, CH = "mathematics", "vii", 7
CONTENT = REPO / "data" / "content"
PLANS = CONTENT / "saved_plans" / SUBJECT / GRADE
CANONICALS = ["ch_07_canonical.json", "ch_07_canonical_p10.json", "ch_07_canonical_p07.json"]

# The C6 matrix, verbatim from the C6 tracker entry. serve_plan takes [(duration, count)].
MATRIX = [
    ("identity X=7", [(40, 7)]),
    ("identity X=10", [(40, 10)]),
    ("identity X=12", [(40, 12)]),
    ("between X=8", [(40, 8)]),
    ("synthesis X=9", [(40, 9)]),
    ("synthesis X=11", [(40, 11)]),
    ("surrender X=13", [(40, 13)]),
    ("below floor X=5", [(40, 5)]),
    ("below floor X=6", [(40, 6)]),
    ("mixed 4x50+7x40", [(50, 4), (40, 7)]),
]


# ── source ────────────────────────────────────────────────────────────────────────────────
def json_strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from json_strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from json_strings(v)


def load_source():
    """TWO sources, kept APART on purpose.

    The copyright question is whether the NCERT TEXTBOOK's expression reaches a
    teacher-facing string. The chapter summary is Aruvi's own derived asset, and a run
    that matches the summary but NOT the book is the pipeline quoting itself. Merging
    them (as the shared scanner does when a .txt summary exists) makes the two
    indistinguishable, so this returns them separately and every hit is attributed.
    """
    pdf_words, parts = cs.load_source(SUBJECT, GRADE, CH)
    j = CONTENT / "chapters" / SUBJECT / GRADE / "summaries" / f"ch_{CH:02d}_summary.json"
    sum_words = []
    if j.exists():
        sum_words = cs.norm_words(" ".join(json_strings(json.load(open(j)))))
        parts.append(f"{j.name} ({len(sum_words)} words)")
    return pdf_words, sum_words, parts


# ── the string surface ────────────────────────────────────────────────────────────────────
def fields(plan):
    return list(cs.lp_fields(plan)) + list(cs.item_fields(plan))


def main():
    pdf_words, sum_words, parts = load_source()
    n = 8
    book = cs.shingles(pdf_words, n)                 # THE COPYRIGHT SOURCE
    summ = cs.shingles(sum_words, n)                 # Aruvi's own asset
    source = book | summ
    print("=" * 92)
    print(f"SOURCE: {' + '.join(parts)}")
    print(f"        textbook {len(pdf_words)} words -> {len(book)} {n}-grams · "
          f"summary {len(sum_words)} words -> {len(summ)} {n}-grams")
    print(f"        summary {n}-grams ALSO in the book: {len(summ & book)} "
          f"({100 * len(summ & book) / max(len(summ), 1):.1f}%)")

    # ── 0 · POSITIVE CONTROL ──────────────────────────────────────────────────────────────
    # A clean report is exactly what a broken detector returns. Lift a real run of source
    # words and require it to be found before anything below is believed.
    probe = " ".join(pdf_words[400:420])
    runs = cs.longest_runs(cs.norm_words(probe), book, n)
    ok = runs and max(r[1] for r in runs) >= 20
    print(f"\nDETECTOR CONTROL: 20-word passage lifted from the TEXTBOOK -> "
          f"detected at {max((r[1] for r in runs), default=0)} words · {'PASS' if ok else 'FAIL'}")
    if not ok:
        return 2

    # ── the corpus: 3 canonicals on disk + every C6 row served fresh ──────────────────────
    corpus = []
    for fn in CANONICALS:
        corpus.append((fn, json.load(open(PLANS / fn))))
    streams = None
    try:
        from api import data as apidata
        streams = apidata.load_genon_streams(SUBJECT, GRADE, CH)
    except Exception as e:
        print(f"\n!! could not load genon streams: {type(e).__name__}: {e}")
    if streams:
        for label, matrix in MATRIX:
            try:
                # serve_plan already returns the full saved-plan ENVELOPE (result inside).
                # Wrapping it again gives lp_fields a `result` whose `lesson_plan` is None —
                # it then yields zero strings and the scan reports a silent, confident clean.
                corpus.append((f"SERVED {label}", serve_plan(streams, matrix)))
            except Exception as e:
                print(f"   !! {label}: {type(e).__name__}: {e}")
    print(f"\nCORPUS: {len(corpus)} plan(s) — "
          f"{len(CANONICALS)} canonical(s) on disk + {len(corpus) - len(CANONICALS)} served fresh")
    # A plan contributing ZERO strings is the silent-clean failure mode; print the count so
    # it cannot pass as a pass.
    for label, plan in corpus:
        lp, it = len(list(cs.lp_fields(plan))), len(list(cs.item_fields(plan)))
        flag = "   <-- ZERO STRINGS, NOT A CLEAN SCAN" if lp + it == 0 else ""
        print(f"   {label:34s} lp {lp:4d} · items {it:4d}{flag}")
    if any(not (list(cs.lp_fields(p)) or list(cs.item_fields(p))) for _, p in corpus):
        return 3

    # ── 1 · VERBATIM REPRODUCTION ─────────────────────────────────────────────────────────
    # Measured against the BOOK. Each hit is then re-tested against the summary alone, so a
    # run that reaches the plan via Aruvi's own asset is not silently charged to the book.
    dist, hits, total_fields = {}, [], 0
    for label, plan in corpus:
        for fname, text in fields(plan):
            w = cs.norm_words(text)
            total_fields += 1
            best = 0
            for start, length in cs.longest_runs(w, book, n):
                best = max(best, length)
                if length >= 12:
                    run = w[start:start + length]
                    sum_runs = cs.longest_runs(run, summ, n)
                    hits.append({"plan": label, "field": fname, "words": length,
                                 "run": " ".join(run), "full": str(text),
                                 "in_summary": max((L for _, L in sum_runs), default=0)})
            dist[best] = dist.get(best, 0) + 1

    print(f"\n{'=' * 92}\nCHECK 1 · VERBATIM REPRODUCTION vs THE TEXTBOOK — "
          f"{total_fields} teacher-facing strings scanned")
    print("longest-shared-run distribution (0 = shares nothing with the book at 8 words):")
    for k in sorted(dist):
        print(f"   {k:3d} words · {dist[k]:5d} string(s)")

    seen = {}
    for h in sorted(hits, key=lambda x: -x["words"]):
        seen.setdefault(h["run"], []).append(h)
    both = sum(1 for r, g in seen.items() if g[0]["in_summary"] >= g[0]["words"])
    print(f"\n{len(hits)} run(s) >= 12 words, {len(seen)} DISTINCT string(s); "
          f"{both} of them are ALSO carried in full by the chapter summary\n")
    for run, group in sorted(seen.items(), key=lambda kv: -kv[1][0]["words"]):
        g = group[0]
        via = ("book+summary" if g["in_summary"] >= g["words"]
               else f"book only (summary carries {g['in_summary']})")
        print(f"   {g['words']:3d} words · {len(group)} occurrence(s) · {via} · fields: "
              f"{sorted({x['field'] for x in group})}")
        print(f"        run : \"{run}\"")
        print(f"        full: \"{g['full'][:400]}\"")
        print()

    # ── 2 · THIRD-PARTY MATERIAL ──────────────────────────────────────────────────────────
    BRANDS = r"\b(coca[- ]?cola|pepsi|amul|tata|reliance|maggi|nestl|parle|britannia|adidas|nike|" \
             r"samsung|apple inc|google|microsoft|whatsapp|facebook|instagram|youtube|disney|" \
             r"marvel|harry potter|pokemon|mcdonald|kfc|dominos|flipkart|amazon|jio|airtel)\b"
    LIT = r"\b(poem|poet|stanza|verse|lyric|song by|excerpt from|short story by|novel|copyright|©|" \
          r"all rights reserved|reproduced (with|by) permission)\b"
    EXT = r"(https?://|www\.|<img|xlink:href|\.jpg|\.jpeg|\.png|\.gif|\.svg\b)"
    print("=" * 92)
    print("CHECK 2 · THIRD-PARTY COPYRIGHTED MATERIAL")
    for name, pat in (("brand/trademark", BRANDS), ("literary/rights marker", LIT),
                      ("external image or url", EXT)):
        found = [(label, fname, text) for label, plan in corpus for fname, text in fields(plan)
                 if re.search(pat, str(text or ""), re.I)]
        print(f"   {name:24s} {len(found):3d} hit(s)")
        for label, fname, text in found[:12]:
            print(f"        {label} · {fname}: \"{str(text)[:180]}\"")
    vs = [(label, fname, text) for label, plan in corpus for fname, text in fields(plan)
          if "visual_stimulus" in fname]
    print(f"   visual_stimulus fields   {len(vs):3d}")
    for label, fname, text in vs[:8]:
        print(f"        {label} · {fname}: \"{str(text)[:200]}\"")

    # ── 3 · ATTRIBUTION ───────────────────────────────────────────────────────────────────
    # Quotation marks INSIDE a field value (the scanner's own recorded false positive was
    # matching JSON string delimiters in a serialised blob — this reads field values only).
    print("=" * 92)
    print("CHECK 3 · QUOTED SOURCE TEXT IS ATTRIBUTED")
    QUOTE = re.compile(r"[“\"']([^”\"']{25,})[”\"']")
    quoted, matched = [], []
    for label, plan in corpus:
        for fname, text in fields(plan):
            for m in QUOTE.finditer(str(text or "")):
                q = m.group(1)
                quoted.append((label, fname, q))
                w = cs.norm_words(q)
                if any(L >= 8 for _, L in cs.longest_runs(w, source, n)):
                    matched.append((label, fname, q))
    uniq = {q for _, _, q in quoted}
    print(f"   {len(quoted)} quoted passage(s) (>=25 chars) in field values, {len(uniq)} distinct")
    print(f"   of which sharing an 8+ word run with the source: {len(matched)}")
    for label, fname, q in matched[:15]:
        print(f"        {label} · {fname}: \"{q[:200]}\"")
    print("   sample of the quoted passages (to show WHAT is being quoted):")
    for q in sorted(uniq, key=len, reverse=True)[:10]:
        print(f"        \"{q[:170]}\"")

    # ── locators, the compliant pattern ───────────────────────────────────────────────────
    print("=" * 92)
    print("BOOK LOCATORS (references INTO the book, reproducing nothing)")
    LOC = re.compile(r"(p\.?\s?\d|page\s\d|exercise\s|figure\s\d|fig\.\s?\d|table\s\d)", re.I)
    locs = {str(text)[:160] for label, plan in corpus for fname, text in fields(plan)
            if LOC.search(str(text or ""))}
    print(f"   {len(locs)} distinct string(s) carry a locator; sample:")
    for s in sorted(locs)[:10]:
        print(f"        \"{s}\"")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
