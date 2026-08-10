#!/usr/bin/env python3
"""C3 maths sub-check — mathematics · VII · ch 7 · FILLED 2026-08-10.

29 determinate items across the three installed canonicals; 40 CHECKS (a stem asking for two
things is two — testing.md C3: "Count CHECKS, not items").

THE ORDERING RULE WAS FOLLOWED. Every `target` was transcribed from the QUESTION STEM and
re-derived before the verdict was written down; `method_one_line` was not read until after.
That is the point of the check: at S4 the wrong answer sat beside a method line that had
already derived the right one, so a checker who transcribes the method confirms the file
against itself and sees nothing (ARV-D-084).

`claimed` is the shipped `teacher_guide.expected_answer`. Where the answer is a sentence — an
explanation, a construction, a classification — it is not symbolically expressible: `target` is
None, the verdict is recorded in the note, and the item still counts as checked.
"""
import sympy as sp

CHECKS = []
CHECKS.append((
    'top #1',
    None,   # claimed
    None,   # target — from the STEM
    "JUDGED — 5,6,5: exactly two sides equal -> isosceles. Shipped 'B — Isosceles'; is_correct is B. CORRECT. (Distractor C claims 5^2+5^2 = 6^2, i.e. 50 = 36 — correctly wrong.)",
))

CHECKS.append((
    'top #2',
    None,   # claimed
    None,   # target — from the STEM
    "JUDGED — angle B = 90, so the hypotenuse is the side opposite B = AC; is_correct is B (AC). CORRECT. The shipped prose originally led with the stale label 'C — '; repaired under ARV-D-092.",
))

CHECKS.append((
    'top #3 no-triangle',
    True,   # claimed
    True,   # target — from the STEM
    '4+5 = 9 < 11 -> no triangle.',
))

CHECKS.append((
    'top #4',
    None,   # claimed
    None,   # target — from the STEM
    'JUDGED — 175 < 180 so a very flat triangle CAN form. Shipped opens on the 180 limiting case and only later concedes it; correct but buries the lede.',
))

CHECKS.append((
    'top #5',
    None,   # claimed
    None,   # target — from the STEM
    'JUDGED — parallel-line proof of the 180 angle sum via alternate interior angles on a straight line. Complete and correct.',
))

CHECKS.append((
    'top #6 AC',
    6,   # claimed
    6,   # target — from the STEM
    'C is on the 6 cm arc centred at A -> AC = 6.',
))

CHECKS.append((
    'top #6 BC',
    6,   # claimed
    6,   # target — from the STEM
    'C is on the 6 cm arc centred at B -> BC = 6.',
))

CHECKS.append((
    'top #7 (a)',
    True,   # claimed
    True,   # target — from the STEM
    '7+9 = 16 > 15 -> possible.',
))

CHECKS.append((
    'top #7 (b)',
    True,   # claimed
    True,   # target — from the STEM
    '6+6 = 12 > 6 -> possible (equilateral).',
))

CHECKS.append((
    'top #7 (c)',
    False,   # claimed
    False,   # target — from the STEM
    '3+8 = 11 < 12 -> impossible.',
))

CHECKS.append((
    'top #8',
    False,   # claimed
    False,   # target — from the STEM
    'r=5, r=3, centres 9 apart: 5+3 = 8 < 9 -> the circles do not meet.',
))

CHECKS.append((
    'top #9 angle F',
    39,   # claimed
    39,   # target — from the STEM
    '48 + 93 + F = 180 -> F = 39.',
))

CHECKS.append((
    'top #9 exterior F',
    141,   # claimed
    141,   # target — from the STEM
    'Exterior at F = 180 - 39 = 141, and 48 + 93 = 141. Both routes agree.',
))

CHECKS.append((
    'top #10 angle Z',
    40,   # claimed
    sp.sympify("40"),   # target — from the STEM
    'X = 2Z, Y = 60 -> 3Z = 120 -> Z = 40.',
))

CHECKS.append((
    'top #10 angle X',
    80,   # claimed
    sp.sympify("80"),   # target — from the STEM
    'X = 2Z = 80. Check 80+60+40 = 180.',
))

CHECKS.append((
    'top #11',
    None,   # claimed
    None,   # target — from the STEM
    'JUDGED — the crease from A meeting BC at a right angle is the ALTITUDE; the fold makes equal adjacent angles on a straight line, so each is 90. Correct.',
))

CHECKS.append((
    'top #12 diagonal',
    13,   # claimed
    sp.sympify("13"),   # target — from the STEM
    'Flat 12x5 sheet -> shortest surface path is the diagonal sqrt(169) = 13. VALUE correct; the METHOD is out-of-chapter (ARV-D-098, accepted).',
))

CHECKS.append((
    'p07 #1',
    None,   # claimed
    None,   # target — from the STEM
    "JUDGED — all sides equal -> equilateral, each angle 180/3 = 60 -> acute. Shipped 'A'; is_correct is A. CORRECT.",
))

CHECKS.append((
    'p07 #2',
    False,   # claimed
    False,   # target — from the STEM
    'Counter-example 2,3,8: 2+3 = 5 < 8 -> the arcs fall short.',
))

CHECKS.append((
    'p07 #3',
    None,   # claimed
    None,   # target — from the STEM
    'JUDGED — two base angles summing to 180 make the arms parallel, so they never meet. Correct.',
))

CHECKS.append((
    'p07 #4 side',
    5,   # claimed
    5,   # target — from the STEM
    'Equilateral at 5 cm: C on both arcs -> AB = AC = BC = 5.',
))

CHECKS.append((
    'p07 #5 (a)',
    True,   # claimed
    True,   # target — from the STEM
    '7+11 = 18 > 15 -> exists.',
))

CHECKS.append((
    'p07 #5 (b)',
    False,   # claimed
    False,   # target — from the STEM
    '4+9 = 13 < 14 -> does not exist.',
))

CHECKS.append((
    'p07 #5 (c)',
    True,   # claimed
    True,   # target — from the STEM
    '6+6 = 12 > 11 -> exists.',
))

CHECKS.append((
    'p07 #6 angle R',
    65,   # claimed
    65,   # target — from the STEM
    '48 + 67 + R = 180 -> R = 65.',
))

CHECKS.append((
    'p07 #6 exterior R',
    115,   # claimed
    115,   # target — from the STEM
    'Exterior at R = 180 - 65 = 115, and 48 + 67 = 115.',
))

CHECKS.append((
    'p07 #7',
    None,   # claimed
    None,   # target — from the STEM
    'JUDGED — set-square altitude construction; in a right-angled triangle two altitudes are the legs. Correct.',
))

CHECKS.append((
    'p10 #1 acute test',
    True,   # claimed
    True,   # target — from the STEM
    '5,5,7: isosceles, and 49 < 50 so the largest angle is acute.',
))

CHECKS.append((
    'p10 #2',
    None,   # claimed
    None,   # target — from the STEM
    'JUDGED — an equilateral triangle has three 60 angles, so right+equilateral is impossible. is_correct is C. CORRECT.',
))

CHECKS.append((
    'p10 #3',
    False,   # claimed
    False,   # target — from the STEM
    "Longest side EQUAL to the sum of the other two is degenerate — the arcs touch at one point on the base line. The student's claim is wrong.",
))

CHECKS.append((
    'p10 #4 angle R',
    40,   # claimed
    40,   # target — from the STEM
    '65 + 75 + R = 180 -> R = 40. (The explanation re-letters PQR as ABC mid-way — a coherence wobble, not an error.)',
))

CHECKS.append((
    'p10 #5',
    False,   # claimed
    False,   # target — from the STEM
    '95 + 90 = 185 > 180 -> nothing left for the third angle.',
))

CHECKS.append((
    'p10 #6 side',
    6,   # claimed
    6,   # target — from the STEM
    'Equilateral at 6 cm: C on both arcs -> AC = BC = 6.',
))

CHECKS.append((
    'p10 #7',
    False,   # claimed
    False,   # target — from the STEM
    '8,5,14: 8+5 = 13 < 14 -> no triangle.',
))

CHECKS.append((
    'p10 #8 third angle',
    50,   # claimed
    50,   # target — from the STEM
    'Angles 50 and 80 given -> third = 50.',
))

CHECKS.append((
    'p10 #9',
    None,   # claimed
    None,   # target — from the STEM
    'JUDGED — set-square and paper-fold both give a perpendicular to the base. Correct.',
))

CHECKS.append((
    'p10 #10 (a)',
    True,   # claimed
    True,   # target — from the STEM
    '6,6,11: 12 > 11 -> exists, isosceles.',
))

CHECKS.append((
    'p10 #10 (b)',
    False,   # claimed
    False,   # target — from the STEM
    '4,7,12: 11 < 12 -> does not exist.',
))

CHECKS.append((
    'p10 #10 (c)',
    True,   # claimed
    True,   # target — from the STEM
    '9,9,9 -> exists, equilateral.',
))


# ---------------------------------------------------------------------------------------
if __name__ == "__main__":
    wrong = judged = 0
    for label, claimed, target, note in CHECKS:
        if claimed is None or target is None:
            judged += 1
            print(f"JUDGED    {label:22} | {note[:96]}")
            continue
        ok = (claimed == target) if isinstance(claimed, bool) \
            else sp.simplify(sp.sympify(claimed) - sp.sympify(target)) == 0
        if not ok:
            wrong += 1
        print(f"{'OK' if ok else 'WRONG':9} {label:22}" + ("" if ok else f" | {note}"))
    print(f"\n{len(CHECKS)} determinate checks · {judged} judged · {wrong} WRONG")
