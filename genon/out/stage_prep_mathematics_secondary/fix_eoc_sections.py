#!/usr/bin/env python3
"""fix_eoc_sections.py — correct end-of-chapter `source_section` in the maths·IX summaries.

WHY (founder ruling 2026-08-09). The authoring prompt required end-of-chapter questions to be
enumerated AND every item's `source_section` to be a real section ref — jointly unsatisfiable,
because those questions belong to no numbered section. All 8 maths·IX summaries carry the
resulting false attribution (69 items). ch 4 collapsed onto 4.1, which put three consolidation
units under "Introduction" on the teacher's screen and is what surfaced it. The prompt is fixed
separately (apply_s4_source_sections.py); this repairs the data already on disk.

THE SHAPE (LP v1.2): `source_section` keeps the DOMINANT section — the one whose method the
question mainly exercises — and the new optional `source_sections` lists every section it
exercises, in section order, first element equal to `source_section`. Single-section questions
carry no `source_sections`.

SAFETY, same doctrine as repair_register.py:
  * every edit is DECLARED per item id, against the book_ref it must match. If the id is
    missing or its book_ref has changed, the run fails loudly and writes nothing.
  * only `source_section` / `source_sections` are touched. Descriptions, ids, book_refs,
    sections[], prose_summary and the effort signals are never written.
  * attribution is a reading of the QUESTION against the section that teaches its method,
    taken from the textbook PDF — recorded per item in `why` so it can be audited without
    re-opening the book.

    python3 genon/out/stage_prep_mathematics_secondary/fix_eoc_sections.py            # dry run
    python3 genon/out/stage_prep_mathematics_secondary/fix_eoc_sections.py --apply
    python3 ... --chapter 4                                                           # one chapter
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SUM = ROOT / "data/content/chapters/mathematics/ix/summaries"
BACKUP = ROOT / "backup/summary_eoc_repair"

# chapter -> { item_id: (book_ref_must_match, dominant, [all_sections] | None, why) }
#
# ── ch 4 · Exploring Algebraic Identities ─────────────────────────────────────
# Section->identity map read off the chapter (PDF pp.68-91):
#   4.2 (a+b)^2 · 4.3 factorising a^2±2ab+b^2 and (a-b)^2 · 4.4 (a+b+c)^2 AND the
#   difference of squares a^2-b^2=(a+b)(a-b) (introduced at the tail of 4.4, p.77) ·
#   4.5 algebra tiles, (x+a)(x+b) and (ax+b)(cx+d) as rectangles · 4.6 middle-term
#   splitting without tiles · 4.7 cubes: (a±b)^3, x^3±y^3, x^3+y^3+z^3-3xyz ·
#   4.8 rational expressions. 4.1 is the Introduction (consecutive-square invariant)
#   and teaches NO technique any end-of-chapter question uses — which is exactly why
#   parking all nine on it was wrong.
REPAIRS = {
    4: {
        "E-13": ("End of Chapter Q1, p.88", "4.4", ["4.2", "4.4", "4.7"],
                 "Q1's nine products split across three sections: (i)(vi) are binomial "
                 "squares (4.2); (ii)(iii)(iv) are difference-of-squares and (vii) is the "
                 "three-term square (4.4 — four parts, so dominant); (v)(viii)(ix) are cube "
                 "identities (4.7)."),
        "E-14": ("End of Chapter Q2, p.89", "4.7", ["4.4", "4.7"],
                 "Q2 computes eight values by identity: 17x21, 104x96, 24x16 use the "
                 "difference of squares (4.4); the five cubes 147^3, 199^3, 127^3, (-107)^3, "
                 "(-299)^3 use (a±b)^3 (4.7 — five of eight, so dominant)."),
        "E-15": ("End of Chapter Q3, p.89", "4.7", ["4.3", "4.4", "4.6", "4.7"],
                 "Q3's eleven factorisations: (i)(viii) perfect-square trinomials (4.3); "
                 "(ii) difference of squares and (x) the three-term square (4.4); (iv) "
                 "middle-term splitting (4.6); (iii)(v)(vi)(vii)(ix)(xi) the cube family "
                 "(4.7 — six parts, dominant)."),
        "E-16": ("End of Chapter Q4, p.89", "4.8", ["4.3", "4.4", "4.6", "4.7", "4.8"],
                 "Q4 is 4.8's own operation — simplify a rational expression by factoring "
                 "numerator and denominator and cancelling — but reaching the factors needs "
                 "the perfect square (i), difference of squares (i)(ii), the sum of cubes "
                 "(iii) and a middle-term split (iii). 4.8 dominates as the task being set."),
        "E-17": ("End of Chapter Q5, p.89", "4.3", ["4.3", "4.4"],
                 "Q5 recovers length and breadth from an area: (i) 25a^2-30ab+9b^2 is a "
                 "perfect square (4.3, dominant as the harder read); (ii) 36s^2-49t^2 is the "
                 "difference of squares (4.4)."),
        "E-18": ("End of Chapter Q6, p.89", "4.4", ["4.4", "4.6"],
                 "Q6 recovers three cuboid dimensions: (i) 6a^2-24b^2 is a common factor then "
                 "difference of squares (4.4); (ii) 3ps^2-15ps+12p is a common factor then a "
                 "middle-term split (4.6)."),
        "E-19": ("End of Chapter Q7, p.90", "4.2", None,
                 "Q7's path area is (40+2s)^2 - 40^2 — expanding the binomial square is the "
                 "whole method. Single section: 4.2."),
        "E-20": ("End of Chapter Q8, p.90", "4.6", None,
                 "Q8 (a number plus its reciprocal = 10/3) becomes 3x^2-10x+3 = 0 and is "
                 "solved by splitting the middle term. Single section: 4.6."),
        "E-21": ("End of Chapter Q9, p.90", "4.6", None,
                 "Q9 factors 2x^2+7x+3 given the width 2x+1 — a middle-term split with a "
                 "leading coefficient. Single section: 4.6."),
    },
}

# ── chapters 1-3 and 5-8, attributed from the textbook PDFs (2026-08-09) ──────
# Declared in sibling files so each chapter's reasoning stays readable; loaded here by
# literal_eval so this script remains the single point that WRITES.
_SIBLINGS = ("eoc_ch1_3.py", "eoc_ch5_8.py")

# HELD BACK, NOT REPAIRED — these two summaries are unsound beyond the attribution and a
# correct source_section on a fabricated item would be polish on a broken record. Both need
# re-running through the `chapter` skill; the EoC fix should follow, not precede, that.
#   ch 6 — the summary describes a DIFFERENT CHAPTER. Verified against the PDF: the book's
#          sections are 6.1 Perimeter of a Shape · 6.2 The C/D Ratio · 6.4 Length of an Arc ·
#          6.5 Problems, Puzzles and Paradoxes · 6.6 Area of a Rectangle · 6.7 Area of a
#          Parallelogram · 6.8 Area of a Triangle (6.8.1 Heron's) · 6.9 Squaring a Rectangle ·
#          6.10 Area of a Circle (6.10.1 Sector). The summary lists an NCERT-style
#          Heron's-formula chapter (6.4 Heron's Formula, 6.7 Brahmagupta, 6.8 pathways,
#          6.9 circular paths, 6.10 combinations). Only the chapter TITLE matches. Every
#          description and page number is invented, and the item count is wrong (9 vs 16).
#   ch 3 — sections[] and the item count are right, but every EoC description is fabricated
#          (summary Q1 = "classify numbers into natural/whole/integers"; the book's Q1 =
#          "convert 3/50 and 2/9 to a terminating or recurring decimal by long division") and
#          the page numbers run one low. Its subsection TITLES are also shifted against the
#          PDF at 3.4.x and 3.5.x.
HOLD = {3, 6}


def _load_siblings() -> dict:
    import ast
    out = {}
    for name in _SIBLINGS:
        p = Path(__file__).with_name(name)
        if not p.is_file():
            continue
        tree = ast.parse(p.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for ch, spec in ast.literal_eval(node.value).items():
                    out[int(ch)] = {k: tuple(v) for k, v in spec.items()}
    return out


for _ch, _spec in _load_siblings().items():
    REPAIRS.setdefault(_ch, {}).update(_spec)


def apply_chapter(ch: int, spec: dict, dry: bool) -> tuple[int, list]:
    path = SUM / f"ch_{ch:02d}_summary.json"
    if not path.is_file():
        raise SystemExit(f"missing summary: {path}")
    s = json.loads(path.read_text(encoding="utf-8"))
    refs = {x.get("ref") for x in (s.get("sections") or [])}
    by_id = {e.get("id"): e for e in (s.get("enumerated_exercises") or [])}
    done = []
    for item_id, (book_ref, dominant, all_secs, why) in spec.items():
        e = by_id.get(item_id)
        if e is None:
            raise SystemExit(f"ch{ch}: no exercise {item_id}")
        if e.get("book_ref") != book_ref:
            raise SystemExit(f"ch{ch} {item_id}: book_ref changed — declared {book_ref!r}, "
                             f"found {e.get('book_ref')!r}. Re-read, do not force.")
        for r in ([dominant] + (all_secs or [])):
            if r not in refs:
                raise SystemExit(f"ch{ch} {item_id}: {r!r} is not a section ref in this chapter")
        # `source_sections` is in SECTION ORDER; `source_section` is the DOMINANT one and is
        # often not the earliest, so it need not lead the list — only belong to it. (An earlier
        # draft demanded it lead, which contradicted section order the moment the dominant
        # section was not the first; this guard caught it on ch 4's E-13.)
        if all_secs:
            if dominant not in all_secs:
                raise SystemExit(f"ch{ch} {item_id}: source_section {dominant!r} must be one "
                                 f"of source_sections {all_secs}")
            order = [x.get("ref") for x in (s.get("sections") or [])]
            if [r for r in order if r in all_secs] != all_secs:
                raise SystemExit(f"ch{ch} {item_id}: source_sections must be in section order "
                                 f"— got {all_secs}")
        was = e.get("source_section")
        if not dry:
            e["source_section"] = dominant
            if all_secs:
                e["source_sections"] = all_secs
            else:
                e.pop("source_sections", None)
        done.append((item_id, was, dominant, all_secs, why))
    if not dry:
        s.setdefault("_repairs", []).append({
            "at": datetime.now().isoformat(timespec="seconds"),
            "tool": "genon/out/stage_prep_mathematics_secondary/fix_eoc_sections.py",
            "reason": ("end-of-chapter items were attributed to a section they do not belong "
                       "to, because the authoring prompt required a real section ref for every "
                       "enumerated item (founder ruling 2026-08-09; prompt fixed separately)"),
            "items": [{"id": i, "was": w, "now": d, "source_sections": a, "why": y}
                      for i, w, d, a, y in done],
        })
        path.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(done), done


def main():
    dry = "--apply" not in sys.argv
    only = None
    if "--chapter" in sys.argv:
        only = int(sys.argv[sys.argv.index("--chapter") + 1])
    force = "--include-held" in sys.argv
    chapters = [c for c in sorted(REPAIRS) if only is None or c == only]
    held = [c for c in chapters if c in HOLD]
    if held and not force:
        chapters = [c for c in chapters if c not in HOLD]
        print(f"HELD BACK (unsound summaries, see HOLD in this file): {held}"
              f"  — pass --include-held to override")
    if not chapters:
        raise SystemExit(f"nothing to do for {only if only else 'any chapter'}; "
                         f"declared {sorted(REPAIRS)}, held {sorted(HOLD)}")
    if not dry:
        BACKUP.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        for c in chapters:
            shutil.copy2(SUM / f"ch_{c:02d}_summary.json", BACKUP / f"ch_{c:02d}_{ts}.json")
        print(f"backed up {len(chapters)} summary(ies) -> {BACKUP.relative_to(ROOT)}/")
    total = 0
    for c in chapters:
        n, done = apply_chapter(c, REPAIRS[c], dry)
        total += n
        print(f"\n=== ch {c} — {n} end-of-chapter item(s)"
              f"{'  (DRY RUN, nothing written)' if dry else ''}")
        for i, was, dom, alls, why in done:
            shown = f"{dom} + {alls}" if alls else dom
            print(f"  {i:5} {str(was):5} -> {shown}")
            print(f"        {why[:150]}")
    print(f"\nTOTAL: {total} item(s) across {len(chapters)} chapter(s)")
    if dry:
        print("dry run — re-run with --apply to write.")


if __name__ == "__main__":
    main()
