# Second repair pass — teacher_notes on the closing units (S7 · F1, 2026-08-20)

Follows `docs/f1_maths_repair_brief.md`, which is done: 24 defects repaired, 39/39 ALL PASS,
zero register hits, no drafting scratch, every table three columns. **The mathematics in the
tables is sound** — an independent auditor re-solved 30 problems across 8 chapters without
reading the solutions first and found 30 of 30 answers correct.

What that audit also found is that `teacher_notes` is now the weakest layer in the set. Six
of its twelve findings were notes naming a method the problem does not use or warning about
an error the problem cannot produce, and one is a false statement a teacher would repeat
aloud. This pass fixes that layer across all 39 chapters.

Same doctrine as before: **declared (old → new) pairs through `genon/repair_c3.py`, applied
by assertion, never a hand edit.** Re-read §3 of the first brief for the two traps (empty
`old`, and purging derived plans). Run with `--declared-only`.

---

## 1. Fix these three first — they are not notes hygiene

**1 · vi ch 3, `teacher_notes` — a false statement.**

> "Problem 1 needs supercell reasoning (a cell is a supercell only if it exceeds every
> adjacent neighbour; **the largest number is always a supercell**)."

False. If the maximum value occupies two *adjacent* cells, neither exceeds its neighbour and
neither is a supercell. Problem 1 is the problem that plants exactly that case — the row is
41, 78, 65, 78, 52 and the stem asks "can both copies be supercells?". So the note
contradicts the problem it introduces, and the clause is unused by the solution, which
argues from the definition alone. **Strike the clause.** A teacher reading the notes before
class would otherwise assert it and then be contradicted by the answer.

**2 · vi ch 9, Problem 4 — a converse used as a proof.**

The solution concludes that a figure with smallest rotational-symmetry angle 20° is possible
because 360 ÷ 20 = 18 is a whole number. Divisibility is *necessary*, not *sufficient*; as
written the route only fails to rule the figure out. Fix by exhibiting the witness — a
regular 18-gon has exactly that symmetry — so the claim is established rather than merely
not refuted.

**3 · vii ch 9, Problem 4 — a figure that does not exist.**

The stem opens "In the figure, M is the midpoint…". No figure is supplied anywhere in the
unit, and this stage may not carry one (assessment Rule 7 bans SVG; the closers carry no
diagrams at all). Rewrite the stem so the configuration is fully determined by words and
numbers, as the other problems in these units are. The data does determine it — the two
right angles put A, M, B on the perpendicular at M — so this is a wording fix, not a
mathematical one. While there, tidy the muddled sentence "so the included angle between the
known angle and the equal side is 90° in both triangles"; the sentence after it states the
ASA condition correctly.

## 2. Then the notes-attribution defects

Each is the same shape: `teacher_notes` names, for some problem, a method that problem's own
solution does not use, or warns about an error that problem cannot produce. The closing
routine has the class **name the method aloud** and the teacher confirm it from these notes,
so a wrong attribution is taught out loud.

Known instances, from the audit of 8 chapters:

| file | defect |
|---|---|
| vi ch 3 | leftover drafting language "Pose all four problems at once by **reading each band aloud**" — the problems live in the Material table, not in bands |
| vi ch 3 | the Problem 3 warning ("forget to pad a four-digit result with a leading zero") names an error that cannot change the answer: 8640 − 468 and 8640 − 0468 are the same subtraction |
| vi ch 6 | "students finding area of only one **flower bed**" — Problem 2 is about *fountains*; the error named is right, the object is not |
| vii ch 3 | "students **multiplying instead of dividing** when converting mm to m" — Problem 1's own solution multiplies (× 0.1, × 0.01); the note flags its own method as the error |
| vii ch 3 | "left-to-right digit comparison **to locate a decimal on the number line**" — Problem 3 uses pure place-value ordering; no number line appears |
| vii ch 9 | "the isosceles base-angle result **proved via RHS congruence**" — Problem 3 cites the result; it proves nothing via RHS |
| vii ch 12 | "**division by a power of ten**" attributed to Problem 2, whose divisor is 8; powers of ten belong to Problem 3, which is separately and correctly attributed |
| viii ch 10 | "students who check **only one pair of ratios** and stop" — Problem 1 has exactly one pair, so one check is the whole method |

**Those eight are from eight chapters. The other 31 have not been audited.** Do not assume
they are clean — go through every chapter's `teacher_notes` against its own table and apply
the same two tests:

- for each problem named, is the method named the one that problem's solution uses?
- for each warning, can the error actually arise in that problem?

Report what you find; finding more than these eight is expected.

## 3. Also fix: the repair record overstates what it did

In vi ch 3 and vi ch 6, the `repair_c3` entries record the "Pose all four problems…" sentence
as **replaced**, but it is still present — the new "Refer to Prepared Table…" pointer was
*prepended*, not substituted. `genon_canonical.repairs[]` is what corpus statistics use to
separate generation quality from repair quality, so a record that overstates its edit
corrupts that measurement.

Two things: correct those records where you can, and check whether the same prepend-recorded-
as-replace pattern appears elsewhere in today's entries.

## 4. What must not change

- The **problems and solutions** in the tables are verified correct — 30 of 30 on audit. Do
  not rewrite a Solution cell in this pass unless you find an actual error, and if you do,
  report it as a new defect rather than folding it in silently.
- The notes' **first sentence** stays exactly:
  `Refer to Prepared Table (see material: '…') for the problems in full and their worked solutions.`
- **No text in these units** may state a quantity of minutes or point beyond the sitting.
  Minutes *inside* a problem, where they are the quantity being measured, are data and stay.
- `teacher_notes` is a few sentences. It must not regain the mathematics — the ceiling is
  1,600 characters and the median today is about 1,000.

## 5. Still open, and not yours to close

`ARV-D-220` and `ARV-D-221` — vii ch 11's Problem 3 needs `HCF × LCM = product` and vii
ch 14's Problem 3 needs the chessboard colouring argument, neither taught by the shorter
plans that borrow these closers. Those are content decisions for the founder. Leave them.

## 6. Finish

    python3 genon/repair_c3.py mathematics <grade> <chapter> --declared-only --dry-run
    python3 genon/repair_c3.py mathematics <grade> <chapter> --declared-only
    python3 genon/batch_build.py mathematics vi vii viii --certify-only --yes

Confirm 39 chapters ALL PASS and zero register ban hits, and record each defect on the
campaign register under combo `mathematics/middle`, step `F1`, with its evidence quoted.
