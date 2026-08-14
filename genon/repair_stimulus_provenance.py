#!/usr/bin/env python3
"""repair_stimulus_provenance.py — say truthfully where an item's stimulus came from
(v1.0, 2026-08-14, S11 · F2).

THE FINDING, from F2 on english·ix. An `EXTRACT_ANALYSIS` item carries its passage in
`visual_stimulus`, and across the stage that field is used two incompatible ways:

  * VERBATIM — 56 to 92 words of the NCERT text, reproduced, with no page locator. The
    copyright review's sole open finding, now quantified.
  * COMPOSITE — Aruvi's own third-person précis ("The mother argues that… She then
    cautions that…"), while the stem calls it "an extract from the letter". Accurate, in
    the cases checked, but labelled as something it is not.

Both are cured by telling the truth about provenance, and they need OPPOSITE cures:

  MODE "reference"  (verbatim ≥50%): the passage is DELETED and replaced by a pointer in
                    the pattern english's own poem items already use —
                    `Read the extract on p.109, beginning "Grandpa hated the noise"`.
                    Nothing is reproduced, and the student reads the real text.
  MODE "relabel"    (composite <50%): the passage STAYS — it is our prose and there is
                    nothing verbatim to point at — but the stem stops calling it an
                    extract and starts calling it a summary, and gains the page range so
                    the teacher can reach the source.

WHY NOT PARAPHRASE THE VERBATIM ONES: paraphrase is what produced the composites, and
ch 11 shows where that ends — an invented line, the play's title line dropped, and an
ordinary speech relabelled an "aside" in the one chapter that teaches the aside
convention. For EXTRACT_ANALYSIS the item type depends on the author's words; a
paraphrase cannot be analysed for craft. FOUNDER RULING 2026-08-14: reference, don't
paraphrase; and where the text is already ours, say so.

WHY RELABELLING IS ENOUGH FOR THE COMPOSITES (founder, 2026-08-14): not every LO needs
the author's words. english·ix ch 15's LO is "analyses authorial purpose, tone, and
persuasive structure", and its three questions ask what a claim reveals, how a shift
serves persuasion, and what a disclosure adds to authority — all properties of the
ARGUMENT, which a faithful summary preserves. The exception is TONE, which lives in the
words: a summary that asserts the tone ("warm, direct encouragement") makes a tone
question circular. None of the affected items asks one; the constitution should say so.

WHAT IS ASSERTED, and it is asserted against the TEXTBOOK, not just the artefact:
  * the current stimulus/stem matches the declaration verbatim (the usual guard);
  * for "reference", the quoted opening phrase is FOUND IN THE BOOK PDF, on the declared
    page — so a wrong page or a misquoted opening refuses instead of shipping;
  * for "relabel", the passage is NOT substantially in the book (<50% of its 6-word
    windows), which is what makes "summary" the honest word rather than a euphemism.

    python3 genon/repair_stimulus_provenance.py --list
    python3 genon/repair_stimulus_provenance.py --apply
"""
from __future__ import annotations

import glob
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "genon"))

TEXTBOOKS = REPO / "textbooks" / "english" / "ix"
SAVED = REPO / "data" / "content" / "saved_plans" / "english" / "ix"


def norm(s):
    return re.sub(r"[^a-z0-9 ]", " ", str(s).lower()).split()


def _book_ch(ch):
    """english chapters are SPLIT out of textbook units, so the plan's chapter number is
    not the book's — the mapping lives in the summary's `_source_unit` (ARV-D-155)."""
    p = REPO / "data/content/chapters/english/ix/summaries" / f"ch_{ch:02d}_summary.json"
    try:
        src = (json.load(open(p)) or {}).get("_source_unit") or {}
        return int(src["unit_chapter_number"]) if src.get("unit_chapter_number") else ch
    except Exception:                                              # noqa: BLE001
        return ch


_PAGES = {}


def book_pages(ch):
    """[{printed, words}] for the chapter's textbook PDF. Printed page numbers are read off
    the page and interpolated for the few pages that carry none."""
    bc = _book_ch(ch)
    if bc in _PAGES:
        return _PAGES[bc]
    import pdfplumber
    out = []
    for p in sorted(glob.glob(str(TEXTBOOKS / "*.pdf"))):
        if not re.match(rf"chapter\s*0*{bc}\b", os.path.basename(p), re.I):
            continue
        with pdfplumber.open(p) as doc:
            for pg in doc.pages:
                t = pg.extract_text() or ""
                nums = (re.findall(r"(?m)^\s*(\d{2,3})\s*$", t)
                        + re.findall(r"(?m)^(\d{2,3})\s", t)
                        + re.findall(r"(?m)\s(\d{2,3})\s*$", t))
                out.append({"printed": int(nums[0]) if nums else None, "w": norm(t)})
    known = [(i, g["printed"]) for i, g in enumerate(out) if g["printed"]]
    for i, g in enumerate(out):
        if g["printed"] is None and known:
            j, v = min(known, key=lambda kv: abs(kv[0] - i))
            g["printed"] = v + (i - j)
    _PAGES[bc] = out
    return out


def verbatim_share(ch, text, k=6):
    """Share of the passage's 6-word windows that appear in the chapter's textbook PDF."""
    W = norm(text)
    wins = [tuple(W[i:i + k]) for i in range(0, max(1, len(W) - k), 2)]
    best = 0
    for pg in book_pages(ch):
        S = {tuple(pg["w"][i:i + k]) for i in range(len(pg["w"]) - k + 1)}
        best = max(best, sum(1 for w in wins if w in S))
    return (100 * best) // max(len(wins), 1)


def phrase_on_page(ch, page, phrase):
    """Is `phrase` on the declared printed page of the chapter's textbook?"""
    w = norm(phrase)
    for pg in book_pages(ch):
        if pg["printed"] != page:
            continue
        pw = pg["w"]
        for i in range(len(pw) - len(w) + 1):
            if pw[i:i + len(w)] == w:
                return True
    return False


# ── THE DECLARATIONS ─────────────────────────────────────────────────────────────
# Generated against the artefacts and the textbook PDFs on 2026-08-14, then asserted at
# apply time — `page` and `opening` are checked against the book, and `verbatim_pct`
# against the same 6-word-window measure that produced the split. A wrong page refuses.
#
# OUT OF SCOPE, deliberately: the 40 MATCH/table stimuli (Column A|B word- and
# sentence-matching grids). They are grammar and vocabulary exercise scaffolding, not
# passages presented as the author's text — founder, 2026-08-14: "a third person
# narration of the book in English is unavoidable unless it is vocabulary/grammar or
# listening". Also out: the 35 poem-section stimuli, which already carry the reference
# pattern this tool extends to prose.

REPAIRS = [
 {"file": "data/content/saved_plans/english/ix/ch_03_canonical.json",
  "item_id": "Q-RFC-A-2", "mode": "reference", "chapter": 3,
  "page": 43, "verbatim_pct": 88, "words_removed": 92,
  "opening": "Onula saw her taking out some clay and",
  "stimulus_after": "Read the extract on p.43, beginning “Onula saw her taking out some clay and”."},
 {"file": "data/content/saved_plans/english/ix/ch_03_canonical_p11.json",
  "item_id": "Q-RFC-A-2", "mode": "reference", "chapter": 3,
  "page": 43, "verbatim_pct": 88, "words_removed": 92,
  "opening": "Onula saw her taking out some clay and",
  "stimulus_after": "Read the extract on p.43, beginning “Onula saw her taking out some clay and”."},
 {"file": "data/content/saved_plans/english/ix/ch_07_canonical_p10.json",
  "item_id": "Q-RFC-A-2", "mode": "reference", "chapter": 7,
  "page": 110, "verbatim_pct": 75, "words_removed": 83,
  "opening": "I had a quiet morning, but I don’t",
  "stimulus_after": "Read the extract on p.110, beginning “I had a quiet morning, but I don’t”."},
 {"file": "data/content/saved_plans/english/ix/ch_07_canonical_p14.json",
  "item_id": "Q-RFC-A-1", "mode": "reference", "chapter": 7,
  "page": 109, "verbatim_pct": 95, "words_removed": 87,
  "opening": "Grandpa hated the noise and bustle of city",
  "stimulus_after": "Read the extract on p.109, beginning “Grandpa hated the noise and bustle of city”."},
 {"file": "data/content/saved_plans/english/ix/ch_09_canonical.json",
  "item_id": "Q-RFC-A-1", "mode": "reference", "chapter": 9,
  "page": 140, "verbatim_pct": 76, "words_removed": 78,
  "opening": "I love sports and had been a swimmer",
  "stimulus_after": "Read the extract on p.140, beginning “I love sports and had been a swimmer”."},
 {"file": "data/content/saved_plans/english/ix/ch_09_canonical_p09.json",
  "item_id": "Q-RFC-A-2", "mode": "reference", "chapter": 9,
  "page": 145, "verbatim_pct": 64, "words_removed": 83,
  "opening": "Honestly, I feel sports, especially Paralympics, have the",
  "stimulus_after": "Read the extract on p.145, beginning “Honestly, I feel sports, especially Paralympics, have the”."},
 {"file": "data/content/saved_plans/english/ix/ch_13_canonical.json",
  "item_id": "Q-RFC-A-2", "mode": "reference", "chapter": 13,
  "page": 211, "verbatim_pct": 78, "words_removed": 71,
  "opening": "There is one letter delivery he dreads. The",
  "stimulus_after": "Read the extract on p.211, beginning “There is one letter delivery he dreads. The”."},
 {"file": "data/content/saved_plans/english/ix/ch_13_canonical_p09.json",
  "item_id": "Q-RFC-A-2", "mode": "reference", "chapter": 13,
  "page": 211, "verbatim_pct": 100, "words_removed": 56,
  "opening": "There is one letter delivery he dreads. The",
  "stimulus_after": "Read the extract on p.211, beginning “There is one letter delivery he dreads. The”."},
 {"file": "data/content/saved_plans/english/ix/ch_13_canonical_p12.json",
  "item_id": "Q-RFC-A-2", "mode": "reference", "chapter": 13,
  "page": 211, "verbatim_pct": 100, "words_removed": 56,
  "opening": "There is one letter delivery he dreads. The",
  "stimulus_after": "Read the extract on p.211, beginning “There is one letter delivery he dreads. The”."},
]

RELABELS = [
 {"file": "data/content/saved_plans/english/ix/ch_01_canonical.json",
  "item_id": "Q-RFC-A-2", "mode": "relabel", "chapter": 1, "verbatim_pct": 22,
  "lead_before": "Read the following passage and answer the questions below.",
  "lead_after": "Read the following summary of the story (the story is on pp.10–13) and answer the questions below.",
  "locator": "pp.10–13", "note": ""},
 {"file": "data/content/saved_plans/english/ix/ch_01_canonical_p08.json",
  "item_id": "Q-RFC-A-2", "mode": "relabel", "chapter": 1, "verbatim_pct": 5,
  "lead_before": "Read the following extract from the story and answer the questions below.",
  "lead_after": "Read the following summary of the story (the story is on pp.10–13) and answer the questions below.",
  "locator": "pp.10–13", "note": ""},
 {"file": "data/content/saved_plans/english/ix/ch_01_canonical_p11.json",
  "item_id": "Q-RFC-A-2", "mode": "relabel", "chapter": 1, "verbatim_pct": 4,
  "lead_before": "Read the passage below and answer the questions that follow.",
  "lead_after": "Read the following summary of the story (the story is on pp.10–13) and answer the questions below.",
  "locator": "pp.10–13", "note": ""},
 {"file": "data/content/saved_plans/english/ix/ch_03_canonical_p08.json",
  "item_id": "Q-RFC-A-1", "mode": "relabel", "chapter": 3, "verbatim_pct": 0,
  "lead_before": "Read the passage below and answer the questions that follow.",
  "lead_after": "Read the following summary of the story (the story is on pp.33–45) and answer the questions below.",
  "locator": "pp.33–45", "note": ""},
 {"file": "data/content/saved_plans/english/ix/ch_05_canonical.json",
  "item_id": "Q-RFC-A-2", "mode": "relabel", "chapter": 5, "verbatim_pct": 3,
  "lead_before": "Read the following passage from the chapter and answer the three questions below it.",
  "lead_after": "Read the following summary of the chapter text (the chapter text is on pp.69–76) and answer the questions below.",
  "locator": "pp.69–76", "note": ""},
 {"file": "data/content/saved_plans/english/ix/ch_05_canonical_p06.json",
  "item_id": "Q-RFC-A-2", "mode": "relabel", "chapter": 5, "verbatim_pct": 3,
  "lead_before": "The chapter argues that celebrating pankha culture through workshops and exhibitions is the key strategy for preserving the craft. Evaluate this argument. In your response, consider: (1) what specific evidence from the chapter supports this claim, (2) what the chapter says about the relationship between artisan livelihood and craft preservation, and (3) whether restricting pankhas to a decorative role strengthens or weakens the case for workshops as a solution.",
  "lead_after": "The chapter argues that celebrating pankha culture through workshops and exhibitions is the key strategy for preserving the craft. Evaluate this argument. In your response, consider: (1) what specific evidence from the chapter supports this claim, (2) what the chapter says about the relationship between artisan livelihood and craft preservation, and (3) whether restricting pankhas to a decorative role strengthens or weakens the case for workshops as a solution.",
  "locator": "pp.69–76", "note": "stem makes no provenance claim (an evaluate-the-argument prompt) — locator only"},
 {"file": "data/content/saved_plans/english/ix/ch_05_canonical_p08.json",
  "item_id": "Q-RFC-A-2", "mode": "relabel", "chapter": 5, "verbatim_pct": 3,
  "lead_before": "Read the following passage carefully and answer the questions below.",
  "lead_after": "Read the following summary of the chapter text (the chapter text is on pp.69–76) and answer the questions below.",
  "locator": "pp.69–76", "note": ""},
 {"file": "data/content/saved_plans/english/ix/ch_07_canonical.json",
  "item_id": "Q-RFC-A-1", "mode": "relabel", "chapter": 7, "verbatim_pct": 23,
  "lead_before": "Read the passage below and answer the questions that follow.",
  "lead_after": "Read the following summary of the story (the story is on pp.97–111) and answer the questions below.",
  "locator": "pp.97–111", "note": ""},
 {"file": "data/content/saved_plans/english/ix/ch_09_canonical_p07.json",
  "item_id": "Q-RFC-A-1", "mode": "relabel", "chapter": 9, "verbatim_pct": 21,
  "lead_before": "Read the following passage and answer the questions below.",
  "lead_after": "Read the following summary of Dr. Malik's interview (Dr. Malik's interview is on pp.137–147) and answer the questions below.",
  "locator": "pp.137–147", "note": ""},
 {"file": "data/content/saved_plans/english/ix/ch_11_canonical.json",
  "item_id": "Q-RFC-A-2", "mode": "relabel", "chapter": 11, "verbatim_pct": 26,
  "lead_before": "Read the passage below and answer the questions that follow.",
  "lead_after": "Read the following summary of the play (the play is on pp.170–184) and answer the questions below.",
  "locator": "pp.170–184", "note": ""},
 {"file": "data/content/saved_plans/english/ix/ch_11_canonical_p08.json",
  "item_id": "Q-RFC-A-2", "mode": "relabel", "chapter": 11, "verbatim_pct": 0,
  "lead_before": "Read the passage below and answer the questions that follow.",
  "lead_after": "Read the following summary of the play (the play is on pp.170–184) and answer the questions below.",
  "locator": "pp.170–184", "note": ""},
 {"file": "data/content/saved_plans/english/ix/ch_11_canonical_p11.json",
  "item_id": "Q-RFC-A-2", "mode": "relabel", "chapter": 11, "verbatim_pct": 10,
  "lead_before": "Read the following extract from Act III of the play and answer the questions that follow.",
  "lead_after": "Read the following summary of the play (the play is on pp.170–184) and answer the questions below.",
  "locator": "pp.170–184", "note": ""},
 {"file": "data/content/saved_plans/english/ix/ch_15_canonical.json",
  "item_id": "Q-RFC-A-2", "mode": "relabel", "chapter": 15, "verbatim_pct": 0,
  "lead_before": "Read the passage below and answer the questions that follow.",
  "lead_after": "Read the following summary of the letter (the letter is on pp.232–234) and answer the questions below.",
  "locator": "pp.232–234", "note": ""},
 {"file": "data/content/saved_plans/english/ix/ch_15_canonical_p05.json",
  "item_id": "Q-RFC-A-2", "mode": "relabel", "chapter": 15, "verbatim_pct": 36,
  "lead_before": "Read the following passage from the letter and answer the questions below.",
  "lead_after": "Read the following summary of the letter (the letter is on pp.232–234) and answer the questions below.",
  "locator": "pp.232–234", "note": ""},
 {"file": "data/content/saved_plans/english/ix/ch_15_canonical_p07.json",
  "item_id": "Q-RFC-A-2", "mode": "relabel", "chapter": 15, "verbatim_pct": 0,
  "lead_before": "The following passage is an extract from the letter. Read it carefully and answer the questions that follow.",
  "lead_after": "Read the following summary of the letter (the letter is on pp.232–234) and answer the questions below.",
  "locator": "pp.232–234", "note": ""},
]


def items_of(doc):
    from aruvi_core.genon.carriers import raw_item_list          # noqa: E402
    return raw_item_list(doc.get("result", doc))


def _find(doc, item_id):
    hit = [i for i in items_of(doc) if isinstance(i, dict) and i.get("id") == item_id]
    if len(hit) != 1:
        raise SystemExit(f"ABORT: {item_id} matched {len(hit)} items, expected 1")
    return hit[0]


def apply_reference(doc, spec):
    """Delete a reproduced passage; leave a pointer to it. Asserted AGAINST THE BOOK."""
    it = _find(doc, spec["item_id"])
    cur = it.get("visual_stimulus") or ""
    if not isinstance(cur, str) or len(cur.split()) < 25:
        raise SystemExit(f"ABORT: {spec['item_id']} stimulus is {len(cur.split())} words "
                         f"— already converted, or a different file")
    pct = verbatim_share(spec["chapter"], cur)
    if pct < 50:
        raise SystemExit(f"ABORT: {spec['item_id']} is {pct}% verbatim, under the 50% bar "
                         f"— it is a composite and belongs in RELABELS, not here")
    if not phrase_on_page(spec["chapter"], spec["page"], spec["opening"]):
        raise SystemExit(f"ABORT: {spec['item_id']} opening {spec['opening']!r} is NOT on "
                         f"p.{spec['page']} of the textbook — refusing to print a wrong "
                         f"page number into a teacher's plan")
    it["visual_stimulus"] = spec["stimulus_after"]
    return {"item_id": spec["item_id"], "mode": "reference", "page": spec["page"],
            "verbatim_pct": pct, "words_removed": len(cur.split()),
            "replaced_with": spec["stimulus_after"]}


def apply_relabel(doc, spec):
    """Keep our prose; stop calling it an extract, and say where the real text is."""
    it = _find(doc, spec["item_id"])
    stem = it.get("item_stem") or ""
    cur = it.get("visual_stimulus") or ""
    pct = verbatim_share(spec["chapter"], cur)
    if pct >= 50:
        raise SystemExit(f"ABORT: {spec['item_id']} is {pct}% verbatim — calling it a "
                         f"SUMMARY would be a euphemism; it belongs in REPAIRS")
    lines = stem.split("\n")
    if lines[0] != spec["lead_before"]:
        raise SystemExit(f"ABORT: {spec['item_id']} lead line is {lines[0]!r}, declaration "
                         f"expects {spec['lead_before']!r}")
    lines[0] = spec["lead_after"]
    it["item_stem"] = "\n".join(lines)
    if spec["locator"] not in it["item_stem"] and spec["locator"] not in cur:
        it["visual_stimulus"] = f"[{spec['locator']}] {cur}"
    return {"item_id": spec["item_id"], "mode": "relabel", "verbatim_pct": pct,
            "locator": spec["locator"], "lead_after": spec["lead_after"],
            "note": spec.get("note", "")}


def main() -> int:
    listing = "--list" in sys.argv
    if not listing and "--apply" not in sys.argv:
        print("usage: repair_stimulus_provenance.py --list | --apply")
        return 2
    by_file = {}
    for s in REPAIRS + RELABELS:
        by_file.setdefault(s["file"], []).append(s)
    total = {"reference": 0, "relabel": 0, "words_removed": 0}
    for rel, specs in by_file.items():
        path = REPO / rel
        print(f"\n=== {rel}")
        for s in specs:
            if s["mode"] == "reference":
                print(f"    {s['item_id']}  REFERENCE  ({s['verbatim_pct']}% verbatim, "
                      f"{s['words_removed']} words removed)")
                print(f"       -> {s['stimulus_after']}")
            else:
                print(f"    {s['item_id']}  RELABEL    ({s['verbatim_pct']}% verbatim)")
                print(f"       -  {s['lead_before']}")
                print(f"       +  {s['lead_after']}")
                if s.get("note"):
                    print(f"       note: {s['note']}")
        if listing:
            continue
        if not path.is_file():
            print("    SKIPPED — not on disk")
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        if any(r.get("kind") == "stimulus_provenance"
               for r in (doc.get("genon_canonical") or {}).get("repairs", [])):
            print("    SKIPPED — already applied")
            continue
        shutil.copy2(path, path.with_suffix(".json.bak_pre_provenance"))
        done = []
        for s in specs:
            d = apply_reference(doc, s) if s["mode"] == "reference" else apply_relabel(doc, s)
            done.append(d)
            total[s["mode"]] += 1
            total["words_removed"] += d.get("words_removed", 0)
        doc.setdefault("genon_canonical", {}).setdefault("repairs", []).append({
            "tool": "repair_stimulus_provenance.py", "kind": "stimulus_provenance",
            "at": datetime.now().isoformat(timespec="seconds"),
            "why": "F2. A verbatim textbook passage is replaced by a page reference (the "
                   "pattern english's poem items already use); a composite passage keeps "
                   "its text but stops being called an extract and gains a locator. "
                   "Founder ruling 2026-08-14: reference, do not paraphrase.",
            "items": done})
        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"    APPLIED — {len(done)} item(s)")
    print(f"\n=== {total['reference']} referenced · {total['relabel']} relabelled · "
          f"{total['words_removed']} words of textbook text removed ===")
    return 0




# ── SECOND PASS (same day): after `reference`, the STEM still promised a passage that
# is no longer there ("Read the passage below…" over a pointer). Separate `kind` so it
# applies to files the first pass already stamped.
LEADS = [
 {
  "file": "data/content/saved_plans/english/ix/ch_03_canonical.json",
  "item_id": "Q-RFC-A-2",
  "lead_before": "Read the passage below and answer the questions that follow.",
  "lead_after": "The extract for this question is in your textbook, identified below. Answer the questions that follow."
 },
 {
  "file": "data/content/saved_plans/english/ix/ch_03_canonical_p11.json",
  "item_id": "Q-RFC-A-2",
  "lead_before": "Read the passage below and answer the questions that follow.",
  "lead_after": "The extract for this question is in your textbook, identified below. Answer the questions that follow."
 },
 {
  "file": "data/content/saved_plans/english/ix/ch_07_canonical_p10.json",
  "item_id": "Q-RFC-A-2",
  "lead_before": "Read the passage below and answer the questions that follow.",
  "lead_after": "The extract for this question is in your textbook, identified below. Answer the questions that follow."
 },
 {
  "file": "data/content/saved_plans/english/ix/ch_07_canonical_p14.json",
  "item_id": "Q-RFC-A-1",
  "lead_before": "Read the following passage and answer the questions below.",
  "lead_after": "The extract for this question is in your textbook, identified below. Answer the questions that follow."
 },
 {
  "file": "data/content/saved_plans/english/ix/ch_09_canonical.json",
  "item_id": "Q-RFC-A-1",
  "lead_before": "Read the passage below and answer the questions that follow.",
  "lead_after": "The extract for this question is in your textbook, identified below. Answer the questions that follow."
 },
 {
  "file": "data/content/saved_plans/english/ix/ch_09_canonical_p09.json",
  "item_id": "Q-RFC-A-2",
  "lead_before": "Read the passage below and answer the questions that follow.",
  "lead_after": "The extract for this question is in your textbook, identified below. Answer the questions that follow."
 },
 {
  "file": "data/content/saved_plans/english/ix/ch_13_canonical.json",
  "item_id": "Q-RFC-A-2",
  "lead_before": "Read the following passage from the chapter and answer the questions below.",
  "lead_after": "The extract for this question is in your textbook, identified below. Answer the questions that follow."
 },
 {
  "file": "data/content/saved_plans/english/ix/ch_13_canonical_p09.json",
  "item_id": "Q-RFC-A-2",
  "lead_before": "Read the following passage from the narrative and answer the three questions below.",
  "lead_after": "The extract for this question is in your textbook, identified below. Answer the questions that follow."
 },
 {
  "file": "data/content/saved_plans/english/ix/ch_13_canonical_p12.json",
  "item_id": "Q-RFC-A-2",
  "lead_before": "Read the following passage and answer the questions below.",
  "lead_after": "The extract for this question is in your textbook, identified below. Answer the questions that follow."
 }
]


def apply_lead(doc, spec):
    it = _find(doc, spec["item_id"])
    vs = it.get("visual_stimulus") or ""
    if not vs.startswith("Read the extract on p."):
        raise SystemExit(f"ABORT: {spec['item_id']} stimulus is not a reference — run the "
                         f"reference pass first")
    lines = (it.get("item_stem") or "").split("\n")
    if lines[0] != spec["lead_before"]:
        raise SystemExit(f"ABORT: {spec['item_id']} lead is {lines[0]!r}, expected "
                         f"{spec['lead_before']!r}")
    lines[0] = spec["lead_after"]
    it["item_stem"] = "\n".join(lines)
    return {"item_id": spec["item_id"], "lead_after": spec["lead_after"]}


def run_leads():
    by = {}
    for s in LEADS:
        by.setdefault(s["file"], []).append(s)
    n = 0
    for rel, specs in by.items():
        path = REPO / rel
        doc = json.loads(path.read_text(encoding="utf-8"))
        if any(r.get("kind") == "stimulus_lead" for r in
               (doc.get("genon_canonical") or {}).get("repairs", [])):
            continue
        done = [apply_lead(doc, s) for s in specs]
        doc["genon_canonical"]["repairs"].append({
            "tool": "repair_stimulus_provenance.py", "kind": "stimulus_lead",
            "at": datetime.now().isoformat(timespec="seconds"),
            "why": "The stem said 'Read the passage below' over what is now a page "
                   "reference. Reworded so the item does not promise text it no longer "
                   "carries.",
            "items": done})
        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
        n += len(done)
    print(f"=== lead pass: {n} stem(s) reworded ===")


if __name__ == "__main__":
    if "--leads" in sys.argv:
        run_leads()
        sys.exit(0)
    sys.exit(main())
