#!/usr/bin/env python3
"""Remove the JSON quote hazard from the five band/phase-narration formats.

CROSS-STAGE amendment, 2026-08-11, after S8's C1 lost a paid compact to it.

THE HAZARD. Five LP constitutions mandate a narration format that puts a DOUBLE-QUOTED
phrase inside a value the model emits as JSON:

    Format: book_ref ("description up to 10 words....")

A plan is JSON, and JSON strings are delimited by `"`. So the model must write the inner
pair as `\\"`, and nothing enforces that — it is a habit it either keeps for a whole run
or drops for a whole run. maths III ch 5 proved both halves on consecutive calls: the
standard canonical escaped all 45 of its pairs and parsed clean; the 11-period compact
escaped none of its 42, blew past the repair bound, and cost ₹40.72 for a file that had
to be recovered by hand.

THE FIX IS TO REMOVE THE HAZARD, NOT TO REPAIR IT. Raising the repair bound (done, 500)
catches the mistake after the fact with a heuristic carrying its own magic numbers. Curly
quotation marks (U+201C/U+201D) have no meaning in JSON, need no escaping, and cannot
truncate a file. The teacher-facing text is unchanged in substance and reads better in
print. The mistake stops being possible rather than being caught.

WHY CURLY AND NOT STRAIGHT SINGLE QUOTES. Single quotes are equally JSON-safe but collide
with apostrophes, which this content is full of: ('Make Amma's rangoli on the dots given
below.') is worse to read than (“Make Amma's rangoli on the dots given below.”). The
corpus already carries en-dashes, ellipses and middots, and every writer uses
`ensure_ascii=False`, so non-ASCII delimiters are already proven through the pipeline.

§9 — THIS IS DELIBERATELY WORDED AS RELAXATION-ONLY, AND THE WORDING IS THE POINT.
A bare substitution of one mandated format for another would be a constitution change in
the full sense: output authored under the old text would breach the new one, and
mathematics·middle (library authored, ch 7) plus mathematics·preparatory (ch 5, mid-build)
would both re-open at roughly ₹106 and ₹120. So each amendment LICENSES rather than
switches: the curly form is what the Format and Example lines now show, and one sentence
records that the straight-quoted form remains valid and is not a defect. Nothing is
tightened, no new obligation is created, and every existing artefact satisfies the new
text by construction — §9's relaxation-only carve-out, which the guards below check by
asserting the `MUST NOT` count is unchanged in every file.

SCOPE — five files, and ONLY the narration formats. The same `("...")` shape appears
elsewhere in these documents as PROSE: the register block's illustrations, prohibition
examples, English's `"<Subheading> (p.NN): <plain brief>"`. Those are the document
quoting a string to its reader, not an instruction to emit quotes inside a value, and
they carry no hazard. They are left alone.
"""
from __future__ import annotations

import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).resolve().parent
C = ROOT / "data/content/constitutions/lesson_plan"

LDQ, RDQ = "“", "”"          # “ ”

NOTE = (
    "\n"
    "Use the CURLY quotation marks shown (" + LDQ + " " + RDQ + "), never straight double\n"
    "quotes. The plan is emitted as JSON, where a straight \" inside a string value must\n"
    "be escaped; an unescaped one ends the string early and destroys the file. Curly\n"
    "marks need no escaping and read better in print. (Plans authored before this\n"
    "version used straight quotes here; that form remains valid and is not a defect.)\n"
)

# (path, old VERSION, new VERSION, [(label, old, new), ...])
JOBS = [
    ("mathematics/middle", "3.8", "3.9",
     "Mathematics Lesson Plan Constitution · Version {v} · Internal Document", [
         ("format+example",
          'Format: book_ref ("description up to 10 words....")\n'
          'Example: Activity 1 (p.107) ("draw two lines on a plain sheet that intersect....")\n',
          f'Format: book_ref ({LDQ}description up to 10 words....{RDQ})\n'
          f'Example: Activity 1 (p.107) ({LDQ}draw two lines on a plain sheet that '
          f'intersect....{RDQ})\n' + NOTE),
     ]),
    ("mathematics/preparatory", "1.3", "1.4",
     "Mathematics Lesson Plan Constitution (Preparatory) · Version {v} · Internal Document", [
         ("format+example",
          'Format: book_ref ("description up to 10 words....")\n'
          'Example: Let us Do Q4 (p.67) ("fill the blanks with the correct numbers....")\n',
          f'Format: book_ref ({LDQ}description up to 10 words....{RDQ})\n'
          f'Example: Let us Do Q4 (p.67) ({LDQ}fill the blanks with the correct '
          f'numbers....{RDQ})\n' + NOTE),
     ]),
    ("english/middle", "1.5", "1.6",
     "English Lesson Plan Constitution · Version {v} · Internal Document", [
         ("format",
          'Format: <spine_section_name> ("brief description up to 10 words....")\n',
          f'Format: <spine_section_name> ({LDQ}brief description up to 10 words....{RDQ})\n'
          + NOTE),
     ]),
    # english·preparatory needs the Example folded into the same edit, for two reasons:
    # the note must land AFTER the example rather than splitting it from its format line,
    # and the example never demonstrated the format it sits under — it showed a bare
    # section name with no quoted brief at all, so a model copying it would have produced
    # the one thing the rule does not ask for. Made self-consistent here.
    ("english/preparatory", "1.0", "1.1", None, [
         ("format+example",
          'Format: `<spine_section_name> ("brief ≤ 10 words")`\n'
          'Example: `Let us Learn — A. Consonant-cluster blend-and-say drill`\n',
          f'Format: `<spine_section_name> ({LDQ}brief ≤ 10 words{RDQ})`\n'
          f'Example: `Let us Learn — A. ({LDQ}consonant-cluster blend-and-say drill{RDQ})`\n'
          + NOTE),
     ]),
    ("english/secondary", "1.0", "1.1",
     "English Lesson Plan Constitution · Version {v} (Secondary) · Internal Document", [
         ("format+example",
          'Format: <spine_section_name> ("brief ≤10 words").\n'
          'Example: Critical Reflection ("night-terrace extract, close-reading +\n'
          'paired discussion").\n',
          f'Format: <spine_section_name> ({LDQ}brief ≤10 words{RDQ}).\n'
          f'Example: Critical Reflection ({LDQ}night-terrace extract, close-reading +\n'
          f'paired discussion{RDQ}).\n' + NOTE),
     ]),
]


def sub(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    assert n == 1, f"{label}: expected exactly 1 occurrence, found {n}"
    return text.replace(old, new)


def main() -> int:
    for stage, oldv, newv, footer, edits in JOBS:
        p = C / stage / "lesson_plan_constitution.txt"
        t0 = t = p.read_text(encoding="utf-8")
        slug = stage.replace("/", "_")
        shutil.copy2(p, OUT / f"lp_{slug}_v{oldv}_pre.txt")

        head = t.splitlines()[0]
        assert f"VERSION {oldv}" in head, f"{stage}: head is {head!r}, expected VERSION {oldv}"
        t = sub(t, f"VERSION {oldv}", f"VERSION {newv}", f"{stage} version line")
        for label, old, new in edits:
            t = sub(t, old, new, f"{stage} {label}")
        if footer:
            t = sub(t, footer.format(v=oldv), footer.format(v=newv), f"{stage} footer")

        # ── guards ──────────────────────────────────────────────────────────
        assert 'Format: book_ref ("' not in t and 'name> ("' not in t, \
            f"{stage}: a straight-quoted narration format survived"
        assert LDQ in t and RDQ in t, f"{stage}: curly marks absent"
        assert t.count("MUST NOT") == t0.count("MUST NOT"), \
            f"{stage}: an obligation was added — this must stay RELAXATION-ONLY (§9)"
        assert "remains valid and is not a defect" in t, \
            f"{stage}: the licensing sentence is what keeps §9's carve-out; it is missing"
        assert len(t) > len(t0), f"{stage}: nothing was added"
        p.write_text(t, encoding="utf-8")
        print(f"  {stage:<26} v{oldv} -> v{newv}")
    print("\n5 constitutions amended; relaxation-only, no library re-opens.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
