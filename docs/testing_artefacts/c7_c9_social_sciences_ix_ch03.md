# C7 (register audit) + C9 (assessment anchoring) · social_sciences · secondary · ch 3

**Run** 2026-08-02, file-only, on the seven C6 `_e10_` plans + the three library canonicals.
**C7 verdict** — machine gate clean (0 bans / 10 files), advisories all ruled benign, **but the
manual read found what regex cannot see: ARV-D-023 (S2)**.
**C9 verdict** — **PASS on all four checks**, zero mis-anchored items.

Unit provenance was reconstructed by hashing each served unit against the library, so every claim
below is traceable to a specific authored unit:

| Plan | Mode | Units served (home variant : unit) |
|---|---|---|
| 50m×6 | suffix | P07 U1–U5 + **P09 U9** · dropped P07 U6 |
| 50m×8 | superset | P09 U1–U7 + **P07 U7** |
| 50m×10 | exact | TOP U1–U9 + **P09 U9** |
| 60m2-50m8 | exact | TOP U1–U9 + **P09 U9** |
| 50m×11 | synthesis | TOP U1–U10 + **P09 U9** (withheld U11, U12) |
| 50m×13 | surrender | TOP U1–U12 (no fill) |
| 45m×9 | full | P09 U1–U9 (no fill) |

---

# C7 · Register

## (a) The machine gate — PASS

`register_scan.py` over all ten files: **0 ban hits**, every file's band text reached
(`time_bands` counts match unit counts × 4). Matches the certification report.

## (b) Advisories — 18, all ruled benign

| Family | Count | Ruling |
|---|---|---|
| `calendar` — "today" | 17 | **Chapter content, not calendar time.** The chapter's whole subject is weather vs climate, and the textbook's own framing question is *"Will it rain today?"* versus *"What is the climate of Chennai?"*. Also *"today's change is driven primarily by human activities"* — "today" as epoch, not as a school day. This is the case the C5 spec anticipated: a gate that failed on "Will it rain today?" would be switched off in a week. |
| `positional` — "the previous unit" | 1 | TOP U11 band 42-50: *"The human-made causes identified in the previous unit … are the preventable half."* **Legal under v1.10** (backward references legalised; a defect only if it also names a clock quantity or calendar word — it does neither). Advisory upheld as *style*: it belongs in `teacher_notes`, not in band text a teacher reads aloud from. Not a defect. |

**`result.dropped_units` scanned separately** (C7 requires it — a teacher reads it on screen):
the one dropped unit in 50m×6 returns **0 bans, 0 advisories**.

## (c) What regex cannot see — **ARV-D-023, S2, NEW**

### A borrowed synthesis unit can assume content the prefix never taught

**P09 U9** ("Synthesis: Connecting Atmosphere, Climate Systems, and Human Vulnerability") is a
**synthesis-only** unit. In its home variant it follows P09 U7 (Climate Change) and P09 U8 (the
Punjab Floods case study), and its text depends on both having happened:

> *teacher_notes:* "Having traced the full arc from atmospheric composition through structure,
> weather elements, India's seasons and monsoon, **climate change, and the Punjab floods case
> study** … A common weakness is treating the floods as a self-contained story rather than
> connecting them to the monsoon mechanism and **climate-change intensification studied in
> earlier units**."
>
> *band 0-10:* "Students read the questions and **individually rank the factors from the case
> study** before discussion begins."
>
> *band 10-30:* "…drawing on evidence from the whole chapter: … the dhūsī bāndh failures and
> floodplain encroachment, **and NDMA guidelines**. Groups are told their position must name at
> least one concept from **each of three earlier sections**."
>
> *materials:* "**NDMA guidelines summary**"

The fill ladder borrows it into prefixes that never taught that content:

| Plan | Climate Change taught? | Floods case study taught? | NDMA taught? | Warned? |
|---|---|---|---|---|
| 50m×10 | ✅ TOP U9 | **❌** TOP U10 not served | **❌** | **NO coverage note at all** |
| 60m2-50m8 | ✅ | **❌** | **❌** | **NO coverage note at all** |
| 50m×6 | **❌ dropped** | **❌** | **❌** | note names Climate Change only |
| 50m×11 | ✅ | ✅ TOP U10 | **❌** withheld U11 | note mentions trimming |

**The sharpest case is 50m×10** — an ordinary, above-floor, full-coverage serve with no coverage
note. The teacher is told nothing, opens her closing sitting, and is instructed to have students
rank factors from a case study they have never read and cite NDMA guidelines they have never seen,
using a material the plan lists but the chapter never introduced.

**Why nothing caught it.** The certifier's section checks pass because the borrowed unit *anchors*
"Punjab Floods 2025: A Case Study" — so first-visit order, coverage-reaches-final-section and the
closing-span mandate are all satisfied. **Anchoring is not teaching.** A unit can be the first to
anchor a section while its text treats that section as revision. `register_scan` sees nothing:
there is no clock quantity, no calendar word, and backward references were deliberately legalised
in the v1.10 re-cut.

**The gap is in the register's design, not its enforcement.** v1.10 banned *forward* reference on
exactly the right reasoning — "X varies per teacher, so ANY unit may be terminal or may precede a
companion variant's unit" — but treated backward reference as safe, because the chapter is always
taught in registry order. That holds for section *coverage* and fails for what each unit *taught*:
a fill serve replaces the prefix, and a suffix serve drops units, so a backward content reference
can become false.

**The contrast that proves it is fixable, not inherent.** The same ladder borrows **P07 U7**
("Closing Synthesis: Climate Change and the Punjab Floods 2025") into 50m×8, and that one is
correct — its opening band *"Introduce the Punjab Floods 2025 case study as a real event…"*
**introduces** the section it anchors, and its one backward reference (to climate change) is true,
because P09 U7 was served at sitting 7. A closing unit that teaches what it anchors is safe to
borrow anywhere; one that only synthesises is not.

**Options for the founder** (this belongs at the human gate, which already asks "is the closing
synthesis a real unit-arc or a summary lecture wearing a unit's clothes?"):

1. **Brief rule — a closing unit must TEACH the sections it anchors**, introducing them rather
   than assuming them, and may reference earlier content only by concept, never as completed
   activity ("the monsoon mechanism" ✅ / "the case study you read" ❌). Cheapest, brief-level, not
   constitutional — iterates at failure speed.
2. **Register addition — ban backward references to *activities and materials*, keep them for
   *concepts*.** Detectable: "the case study you read", "the guidelines we saw", a `materials`
   entry naming content from a section the unit does not anchor.
3. **Solver constraint** — never borrow a unit whose anchored sections are not also anchored by
   the prefix… which would forbid most fills. Probably too strong.
4. **Accept and declare** — extend the coverage note to name what the closing sitting assumes.
   Honest, but it puts the repair in the teacher's lap.

My reading: (1) plus the detectable half of (2). The defect is in the *authoring* of P09 U9, and
the brief is where authoring rules live.

---

# C9 · Assessment anchoring across the serve — PASS

All four checks, on every fill plan:

**1. Prefix remap — PASS.** Every scheduled item's `period_ref` equals the **sitting** number of
its home unit, not its home unit number. Verified by mapping each item back to its authoring
variant and unit: 50m×6 13/13 · 50m×8 16/16 · 50m×10 15/15 correct, **zero mismatches**. E.g. in
50m×10 an item authored against TOP U9 carries `period_ref: [9]`; in 50m×6 an item authored
against P07 U5 carries `[5]`.

**2. Borrowed unit brings its own items — PASS.** The fill sitting's items come from the borrowed
unit's **home** variant and anchor to the last sitting:

| Plan | Fill sitting | Items anchored there | Their home |
|---|---|---|---|
| 50m×6 | 6 | C-4.4 ECR, C-4.5 ECR | **P09 U9** |
| 50m×8 | 8 | C-4.4 SCR, C-4.5 MCQ | **P07 U7** |
| 50m×10 | 10 | C-4.4 ECR, C-4.5 ECR | **P09 U9** |

No chosen-variant item is ever anchored to the fill sitting, and no borrowed item is anchored to a
chosen-variant unit.

**3. Unserved anchors — PASS.** Items whose anchor unit was not scheduled carry
`scheduling_note: "anchor unit not scheduled in this plan (time budget)"` with an **empty**
`period_ref` — never mis-anchored onto a surviving unit. Counts: 50m×6 **6** · 50m×8 **4** ·
50m×10 / 60m2-50m8 **5** · 50m×11 **3** · 50m×13 and 45m×9 **0** (full serves, nothing unserved).
Every one verified to carry no `period_ref`.

**4. No cross-variant references — PASS.** Every `period_ref` is a single in-range sitting; no item
references a unit number from another variant, and no item carries more than one anchor.

Note for the record: **item totals rise on fill serves** (20 on 50m×8/10/11, 19 on 50m×6) because
the borrowed unit contributes its home variant's items on top of the chosen variant's — the
per-variant assessment composition working as designed, not a count defect (contrast ARV-D-019,
which is a count *shortfall* inside a single authored file).

---

## Defects opened

| id | sev | step | title |
|---|---|---|---|
| ARV-D-023 | **S2** | C7 | Borrowed synthesis unit (P09 U9) assumes content the prefix never taught — affects 50m×10, 60m2-50m8, 50m×6, partly 50m×11; **50m×10 carries no coverage note at all**. Certifier cannot see it (anchoring ≠ teaching); `register_scan` cannot see it (backward references are legal). Fix belongs in the variant brief, not a constitution. |

Advisory `positional` hit in TOP U11 recorded as style, not a defect.
