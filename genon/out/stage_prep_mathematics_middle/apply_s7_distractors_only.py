#!/usr/bin/env python3
"""S7 · mathematics MIDDLE + PREPARATORY — `what_each_option_reveals` becomes
DISTRACTORS-ONLY, aligning the last two outliers with the other nine constitutions.

WHY (founder, 2026-08-10, at S7's C3).
Nine of the eleven assessment constitutions already say one entry per NON-CORRECT option:

    english × 3          "ONE entry per INCORRECT option … Omit the correct option"
    science × 2          "one entry per non-correct option"
    social_sciences × 2  "non-correct labels only"
    the_world_around_us  "one entry per non-correct option label"
    mathematics·secondary "one entry per non-correct option, naming its mathematical error"

Mathematics MIDDLE and PREPARATORY are the two that do not. Middle asks for a dict keyed
"A","B","C","D" and licenses "the student UNDERSTANDING (or misconception) that option
reveals" — which is what produced ch 7's "The student correctly locates the hypotenuse…"
entry. Preparatory keys "A".."D" while describing only "the MISCONCEPTION that option
reveals", so it contradicts itself in one sentence.

WHAT IT BUYS, beyond consistency — and this is the real reason (founder's insight):
a distractors-only rule makes the correct/incorrect split MACHINE-CHECKABLE. The reveal keys
must equal exactly the set of non-correct labels, so after STEP 6 has sorted the options a
one-line assertion catches any mis-mapping — no content judgement required. That check is
what would have caught ARV-D-092 the instant it happened: ch 7's item 2 has `is_correct` on
B and a reveal ON B, which under this rule is impossible.

It also removes the failure mode outright. If a correct-option diagnostic cannot exist, no
"the student correctly identifies…" sentence can ever be printed against a wrong choice.

HONEST LIMIT, recorded so nobody over-trusts it: this does NOT fix the remapping — the keys
are still keyed by label and STEP 6 still has to move them (fixed separately, same day, so it
now remaps `teacher_guide` as well as `guide[TYPE]`). And a permutation purely AMONG the three
distractors still passes the key-set check; only a reader catches that. Small residue, and the
same one the other nine stages already live with.

§9: MIDDLE is a TIGHTENING (a licensed entry becomes forbidden), so the relaxation-only
carve-out does not apply — but the installed ch 7 library is REPAIRED rather than re-authored
(genon/repair_option_reveals.py), because the repair is deterministic and regeneration is a
lottery. PREPARATORY has no authored library, so it costs nothing there.
"""
from __future__ import annotations

import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).resolve().parent
MID = ROOT / "data/content/constitutions/assessment/mathematics/middle/assessment_constitution.txt"
PREP = ROOT / "data/content/constitutions/assessment/mathematics/preparatory/assessment_constitution.txt"

MID_OLD = """  teacher_guide.what_each_option_reveals:
    For MCQ items only — a JSON object keyed by option label
    ("A", "B", "C", "D"), each value a one-sentence diagnostic of
    what the student understanding (or misconception) that option
    reveals. For non-MCQ items, this is an empty object {}.
"""
MID_NEW = """  teacher_guide.what_each_option_reveals:
    For MCQ items only — a JSON object with ONE ENTRY PER NON-CORRECT
    OPTION, keyed to that option's `label` in `options[]`, each value a
    one-sentence diagnostic of the misconception a student who chose it
    likely holds. OMIT THE CORRECT OPTION: the object carries exactly
    three entries, and the correct answer is already marked by
    `is_correct` and read from `teacher_guide.expected_answer`. For
    non-MCQ items, this is an empty object {}.

    The omission is not a style preference. Option order is set
    downstream, and a key set that must equal the non-correct labels
    exactly is the platform's only mechanical check that the relabelling
    carried the diagnostics with it. A diagnostic written for the correct
    option destroys that check and, when the labels move, prints
    "the student correctly …" against a wrong choice.
"""

MID_SCHEMA_OLD = """    teacher_guide.what_each_option_reveals:
        {A:..., B:..., C:..., D:...}
"""
MID_SCHEMA_NEW = """    teacher_guide.what_each_option_reveals:
        {A:..., C:..., D:...}   // the three NON-CORRECT labels only;
                                // the correct option is omitted
"""

PREP_OLD = """  what_each_option_reveals: MCQ only — object keyed "A".."D", each a
                     one-sentence diagnostic of the misconception that
                     option reveals. {} for non-MCQ.
"""
PREP_NEW = """  what_each_option_reveals: MCQ only — ONE ENTRY PER NON-CORRECT option,
                     keyed to that option's label, each a one-sentence
                     diagnostic of the misconception that option reveals.
                     OMIT THE CORRECT OPTION (three entries, not four):
                     it is already marked by `is_correct`. {} for non-MCQ.
"""


def sub(text, old, new, label):
    n = text.count(old)
    assert n == 1, f"{label}: expected exactly 1 occurrence, found {n}"
    return text.replace(old, new)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    m0, p0 = MID.read_text(encoding="utf-8"), PREP.read_text(encoding="utf-8")
    shutil.copy2(MID, OUT / "assessment_constitution_v3.3_pre.txt")
    shutil.copy2(PREP, OUT / "prep_assessment_constitution_v1.1_pre.txt")

    m1 = sub(m0, "ARUVI — MATHEMATICS ASSESSMENT CONSTITUTION · VERSION 3.3",
             "ARUVI — MATHEMATICS ASSESSMENT CONSTITUTION · VERSION 3.4", "middle version")
    m1 = m1.replace("Mathematics Assessment Constitution · Version 3.3 · Internal Document",
                    "Mathematics Assessment Constitution · Version 3.4 · Internal Document")
    m1 = sub(m1, MID_OLD, MID_NEW, "middle Rule 6 reveals")
    m1 = sub(m1, MID_SCHEMA_OLD, MID_SCHEMA_NEW, "middle Rule 10 schema")

    p1 = sub(p0, "ARUVI — MATHEMATICS ASSESSMENT CONSTITUTION (PREPARATORY) · VERSION 1.1",
             "ARUVI — MATHEMATICS ASSESSMENT CONSTITUTION (PREPARATORY) · VERSION 1.2",
             "prep version")
    p1 = sub(p1, PREP_OLD, PREP_NEW, "prep reveals")
    p1 = p1.replace('            "what_each_option_reveals": { "A": string, "B": string,',
                    '            "what_each_option_reveals": { "A": string, "C": string,')

    for name, t in (("middle", m1), ("preparatory", p1)):
        assert "NON-CORRECT" in t, f"GUARD {name}: the rule did not land"
        assert "OMIT THE CORRECT OPTION" in t, f"GUARD {name}: the omission is not explicit"
        # the A9 lines from v3.3 must survive untouched
        if name == "middle":
            assert "Option order carries no meaning" in t, "GUARD: A9 mandate lost"
            assert "by its label" in t, "GUARD: A9 by-label prohibition lost"
            assert "ANCHORING (PLATFORM INTEGRITY" in t, "GUARD: A6 block lost"
    assert '"A", "B", "C", "D"), each value a one-sentence' not in m1, "GUARD: old middle text survived"
    assert 'object keyed "A".."D"' not in p1, "GUARD: old prep text survived"

    MID.write_text(m1, encoding="utf-8")
    PREP.write_text(p1, encoding="utf-8")
    print("middle      assessment v3.3 -> v3.4")
    print("preparatory assessment v1.1 -> v1.2")
    return 0


if __name__ == "__main__":
    sys.exit(main())
