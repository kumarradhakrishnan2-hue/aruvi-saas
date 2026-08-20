# Repair brief — mathematics·middle closing-synthesis units (S7 · F1, 2026-08-20)

For a fresh reader with no context from the session that produced this. Everything you
need is here or named by path.

---

## 1. What these artefacts are

Each chapter of mathematics·middle has a LIBRARY of 2–3 lesson plans at different lengths
(`data/content/saved_plans/mathematics/{vi,vii,viii}/ch_NN_canonical*.json` — the bare name
is the longest, `_pNN` are shorter). A teacher whose timetable fits none of them is served
the first X−1 units of one plan plus ONE unit borrowed from another. The unit that gets
borrowed is almost always the longest plan's **closing synthesis** — the last period, the
one carrying `"synthesis": true`.

Those closing units were re-authored on 2026-08-20 (`genon/resynth.py`, wave `resynth`) so
that they pose the TEACHER'S OWN problems instead of running the textbook's end-of-chapter
exercises. Each now carries, in `visual_aids`, one table:

    No. | Problem | Solution

That table is teacher-facing. A teacher reads it at the board while the class works. It is
the only worked reference she has for problems that appear in no book.

## 2. What is wrong

The re-authoring fixed what it was aimed at. It also shipped mathematical defects that
certification cannot see: certification checks structure, anchors, register and coverage —
it never checks whether an answer is right.

**16 defects are listed in §5, each with its evidence.** They fall into four kinds:

- **wrong answer** — the Solution cell states something false (4 cases, the worst harm)
- **ill-posed problem** — the Problem cell's own conditions cannot produce the figure it
  names, so the question has no answer (2 cases)
- **invalid route, right answer** — the arithmetic lands correctly but the stated reasoning
  does not support it, and this unit's design has the class *name the method aloud*, so a
  wrong route is taught out loud (7 cases)
- **statement/solution disagreement** — the two cells describe different problems (3 cases)

Separately, **drafting scratch** survives in some tables (abandoned trials, editorial notes
to self, and in one case a fourth pipe column holding a second "corrected" solution).
Listed in §6. Not mathematics, but teacher-facing and indefensible.

## 3. THE ONE RULE: repair by declaration, never by editing the file

Hand-editing an artefact is forbidden in all cases. Every edit is a **stated (old → new)
pair in code**, applied by assertion — if `old` is not found verbatim the file is left
untouched and the run fails loudly — and recorded inside the artefact at
`genon_canonical.repairs[]`, so corpus statistics can still tell generation quality from
repair quality.

The tool is `genon/repair_c3.py`. Add entries to the `DECLARED` table, keyed
`("mathematics", "<grade>")` → `"<filename>"` → `"<defect-id>"` → a list of edits:

```python
{"unit": 17, "field": "visual_aids[0].table",
 "old": "…the exact text on disk…",
 "new": "…the replacement…"},
```

`field` reaches nested values as `name[index].leaf`. For an assessment item use
`{"item_where": {"id": "Q-C-10"}, "field": "prompt", …}` instead of `unit`.

Run:

    python3 genon/repair_c3.py mathematics viii 5 --declared-only --dry-run   # verify
    python3 genon/repair_c3.py mathematics viii 5 --declared-only             # apply

`--declared-only` matters: without it the generic passes run too, and they have never been
run on this stage.

**Two traps, both paid for already.**

1. **Never declare `"old": ""` on a string field.** `str.replace("", x)` inserts between
   every character. An entry declared that way re-fired during an unrelated sweep and
   exploded a 133-character prompt to 17,955. The tool now refuses it; use `"old": None`,
   which takes the safe set-with-drift-check branch.
2. **After any repair, purge derived plans and check the purge worked.** A repair does not
   move `canonical_version`, so the cache serves pre-repair bytes forever (ARV-D-034).
   `repair_c3` calls `purge_derived` itself; read its output. If it says "could not remove",
   delete by hand.

Then re-certify:

    python3 genon/batch_build.py mathematics vi vii viii --certify-only --yes

## 4. What "repaired" means for each kind

- **Wrong answer** — recompute from scratch, then correct the Solution cell. Keep the
  problem. State the corrected route in the same voice and length as its neighbours.
- **Ill-posed problem** — prefer changing the PROBLEM's numbers so its own conditions
  produce a whole answer, over changing the question. Then re-derive the solution against
  the new numbers. Do not do what the model did and answer a silently different question.
- **Invalid route** — keep the answer, replace the justification with one that holds. A
  justification must name the fact it rests on and must never assume what it is proving.
- **Statement/solution disagreement** — decide which is right, fix the other.

Length discipline: the Solution cell is "the answer and the few steps that reach it, in
plain words and figures … no longer than the problem it answers". `teacher_notes` is a few
sentences and must not regain the mathematics; its first sentence is the fixed pointer
`Refer to Prepared Table (see material: '…') …` and stays.

Register: no text in these units may state a quantity of minutes ("for the first fifteen
minutes") or point beyond the sitting. Minutes INSIDE a problem, where they are the
quantity being measured, are data and stay.

## 5. The 16 mathematical defects

Grade · chapter · the problem number in the table. The unit is always the plan's LAST
period, in `ch_NN_canonical.json` (not the `_pNN` files).

### Wrong answers — fix these first

1. **vii ch 14, Problem 3** — "the four corner squares of a 4 × 4 grid are all the same
   colour" is false: with colour = (i+j) mod 2, (1,1) and (4,4) are one colour, (1,4) and
   (4,1) the other. So removing them leaves **6 and 6**, not "4 black and 8 white", and the
   conclusion "the region cannot be tiled" is **false** — a tiling exists (row 1 cols 2–3;
   row 4 cols 2–3; rows 2 and 3 full). All-corners-same-colour holds on odd×odd boards.
   *Note: this problem also presumes a method the shorter plan never teaches — see §7.*

2. **viii ch 5, Problem 4** — "No solution exists for AB × 7 = CBA with all digits
   distinct" is false: **97 × 7 = 679**. Algebraically 7(10A+B) = 100C+10B+A ⇒ 3(23A−B) =
   100C ⇒ C ∈ {3,6,9}; C = 6 gives 23A−B = 200 ⇒ A = 9, B = 7. The enumeration missed it
   via a bogus exclusion, "B = 7: repeated digit" — B = 7 forces A = 9 and repeats nothing.

3. **viii ch 8, Problem 3** — statement and solution contradict. The stem says the price
   "fell by 15% in the second year **compared with the start of the first year**", which
   gives 100 + 8 − 15 = 93, i.e. **−7%**. The solution computes 1.08 × 0.85 = 0.918 →
   −8.2%, which requires the fall to be against the END of year 1. Fix the stem (drop
   "compared with the start of the first year") or the solution — the notes currently brand
   the statement-consistent reading as the student error, so fix them together.

4. **viii ch 12, Problem 4(i)** — "City B has the higher mean" is not derivable from the
   three points the problem gives (14 °C Jan, 38 °C May, 16 °C Dec). The justification
   imports "May–September above 30 °C", which appears nowhere in the statement; on a plain
   monotone reading B's mean (≈ 25.7) is BELOW A's (≈ 26). Either give the data the
   argument needs, or change the question to one the given points settle.

### Ill-posed problems

5. **vii ch 10, Problem 3** — +3 for right, −2 for wrong, all 20 attempted ⇒ score = 5c − 40,
   so every attainable score is a multiple of 5. The stated score of **11 is impossible**
   (5c = 51). The cell knows, and silently answers for a score of 10 while the stem still
   reads 11. Change the stem's score to one the rule can produce, then re-derive.

6. **viii ch 5, Problem 2** — 3A5B72 divisible by both 9 and 11 requires A+B ∈ {1,10} and
   A+B ∈ {2,13}; the intersection is empty, so "find all pairs" has no answer. The cell
   ships an editorial note proposing 3A5B18 instead. Make that (or another working choice)
   the actual problem and delete the note.

### Invalid route, right answer

7. **vi ch 9, Problem 1** — "The figure has exactly 1 line of symmetry" does not follow.
   An equilateral triangle folds along its vertical axis, fails the horizontal fold, and has
   three axes. Ruling out one perpendicular fold only excludes even-order dihedral symmetry.
   The stem is also incoherent: a HORIZONTAL fold maps top onto bottom, not "the left half
   onto the right half".

8. **vi ch 6, Problem 4** — as stated (two 5×4 pieces joined along their 4 cm edges) the
   configuration simply rebuilds the original 10×4 rectangle, so nothing changes and the
   named method is never exercised; the solution then answers a second, unasked
   configuration and ends with two answers.

9. **vii ch 3, Problem 3** — the justification places 36.089 among "those with tenths digit
   8"; its tenths digit is 0. The step that actually orders 36.08 < 36.089 is never given.
   The stem also says four students record "the same temperature" when only two readings
   are equal.

10. **vii ch 8, Problem 4** — "Since 4/7 < 1, the product is also less than 1" is a
    non-sequitur (8/5 × 4/5 > 1). The valid reason is 8 × 4 = 32 < 35 = 5 × 7.

11. **vii ch 9, Problem 1** — the offered alternative statement "△QPR ≅ △TUS" is wrong.
    With P↔S, Q↔T, R↔U, reordering the first triangle as Q,P,R forces **△TSU**. As printed
    it asserts PQ = TU and PR = TS, both false. (The other alternative given, △RQP ≅ △UTS,
    is correct.) The notes correctly warn the teacher to check vertex order — against a
    solution that gets it wrong.

12. **vii ch 12, Problem 2** — "Regroup: 40 tenths ÷ 8 = 5 tenths". The remainder is 4
    TENTHS, regrouped to 40 HUNDREDTHS, giving 5 hundredths. As written the quotient reads
    6.3, contradicting the cell's own correct answer 5.85. The decimal point is also placed
    a step late — it belongs before the tenths digit is written.

13. **vii ch 7, Problem 3** — the construction contradicts the data. Given AB = 8, BC = 6,
    CA = 5, the solution says "draw base BC = 8 cm" and swings arcs of 5 from B and 6 from
    C. The triangle it builds has AB = 5 and AC = 6. Knock-on: with the CORRECT triangle
    ∠C ≈ 92.9°, so the altitude foot falls outside BC — which is what the notes warn about,
    and which does not happen in the figure the solution draws.

14. **vii ch 14, Problem 4** — "grouping the 6 columns in pairs of adjacent columns gives
    six 5 × 2 blocks": it gives **three**. The surrounding text is also an abandoned trial
    (see §6).

15. **viii ch 10, closing band [42-45]** — "every problem in this chapter … was solved by
    the same idea: when two quantities share a fixed ratio, knowing one tells you the
    other." False for Problem 4, which is INVERSE proportion — constant product, not fixed
    ratio — and it reverses the distinction the immediately preceding sitting is built on.

16. **viii ch 11, Problem 3** — the notes and the band both name the Baudhāyana–Pythagoras
    theorem, but both endpoints are face centres so the horizontal offset is zero and the
    solution's own line is √(0 + 64) = 8: a plain sum, not a hypotenuse. The described net
    ("unrolling the four side faces in a strip") also isn't the net the coordinates use,
    which crosses one side face. Either name the method honestly or move the endpoints off
    the centres so the theorem is actually needed.

## 6. Drafting scratch to remove (teacher-facing, not mathematics)

Pure deletions. The answer already present stays; only the working around it goes.

- **viii ch 5** — the worst. Rows 2 and 4 carry a **fourth pipe-delimited column** holding
  a second "corrected" solution, including *"(Teacher note: if the problem is to have a
  solution, replace 72 with 18 … Use the number 3A5B18 in class.)"* and five abandoned
  cryptarithm searches. The table must be three columns.
- **vii ch 10, Problem 3** — five abandoned trials and an explicit bracketed working note
  that rewrites the question.
- **vii ch 14, Problem 4** — "in fact … but …" restart after a complete route.
- **viii ch 7, Problem 2** — a wrong trial ("? = 960 ÷ 15 = 64") stated before being
  retracted, and a retraction sentence that contradicts itself.
- **vi ch 3** — duplicated fragments: "the number 4-digit number 3,5,2,1"; "smallest = 0468
  = 0468, treated as 0468".
- **vi ch 6, Problem 4** — an unrequested second configuration left in.
- **vii ch 3, Problem 3** — "36.08_" shorthand and a dangling "— look further:".

## 7. NOT repairable by declaration — leave, and report

Two closers demand a method the shorter plan never taught. That is a content decision, not
a text repair; do not paper over it.

- **vii ch 11, Problem 3** needs `HCF × LCM = product`. The shorter plan teaches HCF and
  LCM separately and never the product relation.
- **vii ch 14, Problem 3** needs the chessboard two-colouring argument. The shorter plan
  teaches only total-count parity.

Both are recorded under ARV-D-181's family. Flag them; the founder rules.

## 8. Verify before you believe this list

**This list is a floor, not a total.** Every file was read once, by one reader. Files
previously declared clean have twice regressed on later reads. So:

- Recompute every problem in any chapter you touch, not only the one named here.
- When you correct a cell, work the problem yourself first and only then write the route.
- If you find a defect not on this list, add it and say so — that is expected, not a
  contradiction.
- After applying, re-run certification and confirm 39 chapters ALL PASS and zero register
  ban hits:

      python3 genon/batch_build.py mathematics vi vii viii --certify-only --yes

Record each defect on the campaign register (`data/testing/campaign_state.json`, the
`defects` list) with its evidence quoted, under combo `mathematics/middle`, step `F1`.
