# C7 · register audit — the_world_around_us · V · ch 5

**Scanned:** the 3 library files **and all 7 C6 served plans** (10 files, 1,000+ teacher-facing
strings). `result.dropped_units` scanned too — there are none anywhere in this chapter's band.
**Date:** 2026-08-12 · **Template:** testing.md v2.9 C7 (a) gate · (b) advisories · (c) what
regex cannot see.

**PASS — with one minor defect, one scanner extension landed, and one cross-stage finding that
is not this stage's.**

---

## (a) The gate — `0 ban hit(s)`, on all ten files

| file | bans | advisory | fields reached |
|---|---|---|---|
| `ch_05_canonical.json` (16) | **0** | 3 | 16 titles · 16 notes · 63 bands |
| `ch_05_canonical_p13.json` | **0** | 1 | 13 · 13 · 52 |
| `ch_05_canonical_p10.json` | **0** | 2 | 10 · 10 · 40 |
| 7 served plans (40×8…40×15, 3×50+11×40) | **0** each | 1–2 each | titles · notes · bands, all present |

The `fields reached` column is the check that matters as much as the zero: a plan reporting
0 bans and 0 band fields has not been scanned, it has been skipped. Every file reports its full
complement, so the zeros are real.

## (b) Advisories — four distinct strings, ruled

| # | where | family | string | ruling |
|---|---|---|---|---|
| 1 | TOP U7, band 30–40 (and its 3 serves) | calendar | *"…this is an inquiry the class is opening, not closing **today**."* | **PASS, and it is the closest call in the chapter.** The literal token is present, but it means "in this sitting", not a calendar day, and the sentence's actual work is to **decline a completion claim** — the opposite of a ban-2 breach. Recorded rather than waved because ARV-D-100 is precedent that the scanner under-reports. |
| 2 | p10 U3 note (and 40×8, 40×9) | calendar | *"…how does that connect to the symbol we see on the note **today**?"* | **PASS.** Inside a quoted teacher question, meaning "in the present day" — the currency note now versus historically. Chapter content, self-consistent whenever taught. |
| 3 | p13 U7 note (and 40×11, 40×12) | calendar | *"'If your state had to choose a new symbol **today**, what would you suggest and why?'"* | **PASS.** Quoted hypothetical addressed to students. Not a scheduling claim. |
| 4 | p10 U3, band 20–32 (and 40×8, 40×9) | positional | *"…the Ashoka Chakra on the flag, already encountered in **the previous unit** of work on the tricolour…"* | **MINOR DEFECT — ARV-D-124.** See below. |

**On #4.** Backward reference is legal (v1.10 legalised it), so this is not a ban. But this
stage's own **VOCABULARY** clause — amended at P1 and standing in v1.5 — says *"Cross-reference
another unit by the CONTENT it built, **never by its position**"*, and the register's closing
sentence says the same as best practice. *"already encountered in the previous unit"* is
positional where content-naming was not merely available but easier: *"already encountered in
the tricolour work"* says it in fewer words. The claim is **true in every serve** (p10's U1–U2
teach the tricolour and the prefix is always preserved), so nothing is falsified and serving is
unaffected — which is why it is S4 and not higher. The scanner already surfaces it as
`positional`, so the machine did its job and this is the human ruling it asked for.

## (c) What regex cannot see — and the pattern that came back

Read all 10 files for the three shapes C7 names: paraphrased forward reference, a unit whose
opening move assumes another unit happened, a closing unit implying completion without saying so.

**Paraphrased forward reference: none.** The corpus reads as if the rule were understood rather
than dodged. Two strings are worth quoting as the positive form: TOP U15 closes *"it is an
inquiry that continues beyond this sitting, not something declared complete"* — a deliberate
refusal of the completion claim — and TOP U16's note instructs *"bring back specific content from
across the chapter by name … **Name the content, not any particular earlier activity**"*, which is
the register's own prescription quoted back at it.

**Closing unit implying completion: none.** The synthesis unit is licensed to assume the
chapter's CONTENT was taught, and it stays inside that licence — it names the flag's colours, the
currency note's symbols, the forest metaphor, the dance map, and assumes no particular activity.

**A unit whose opening move assumes another unit happened: YES — and it is ARV-D-119, which this
step should have been the one to find.** The scanner reported 0 bans on the top canonical, and
the top canonical's closing unit could not be run as served:

```
materials:    ["Group posters and charts PREPARED PREVIOUSLY"]
visual_aids:  "Group-created posters and charts from all states represented"
band 0–5:     "Groups SET UP THEIR POSTERS or displays around the classroom."
```

**Why the scanner missed it, precisely.** Two independent reasons, and both are now fixed:

1. **It was not reading the field.** `_fields()` yielded `activity_title`, the note keys, the
   band array and `homework[]` — **not `materials[]` and not `visual_aids`**. The dependency
   arrived through the *props*, so a scanner reading only prose reported clean on a plan whose
   shopping list required a sitting that may not have happened. A materials list is the first
   thing a teacher reads when deciding whether she can run the sitting; it is teacher-facing on
   exactly the same ground as `homework[]`, which has always been scanned.
2. **The phrasing was not in the pattern set.** The `artefact` family added at S6 looks for a
   possessive in prose (*"their earlier chart"*). TWAU's breach used neither shape — it was
   **passive, ownerless, and named no unit**: *"prepared previously"*.

**Landed (the C7 feedback loop, with dated notes in the file):** `_fields()` now reads
`materials[]` and `visual_aids`, and three `artefact` patterns are added —
`(prepared|made|built|drawn|created|collected|written) (previously|earlier|beforehand|in
advance|last time)`, `(set up|bring out|hand back|redistribute|display) their
(posters|charts|models|displays|drafts|collections)`, and `from the (earlier|previous|last)
(sitting|unit|session|lesson)`. Kept **advisory**, like the S6 pair and for the same reason: on a
plan-granularity stage every unit is served with every other, so the dependency is legal there
and a human decides. The place it is now **forbidden** is the platform brief (landed the same
day), which is where a rule about *serving* belongs — this is the detector, not the rule.

**Verified both ways, to S6's discipline** (six of its seven new patterns were wrong and the
certified corpus said so immediately):

- **It fires on the real thing.** Both ARV-D-119 strings are now caught, on the exact unit:
  `U16 materials[0] [artefact] "Group posters and charts prepared previously"` and
  `U16 time_bands[0] 0-5 [artefact] "Groups set up their posters…"`.
- **It breaks nothing.** Re-run over **every certified library in the corpus** (25 files, now
  including 1,040 newly-scanned `materials`/`visual_aids` strings): **BANS 5 → 5, delta +0.**
  Advisories 72 → 77, which is exactly the intended new surface — 2 on TWAU's top, 3 elsewhere.

---

## The cross-stage finding — not this stage's, and it should not wait for one

The corpus-wide re-run surfaced **5 live BAN hits on already-certified libraries**, none of them
mine and none of them TWAU's:

| file | unit | family | string | recorded? |
|---|---|---|---|---|
| maths/iii ch 5 canonical, p08, p11 | U11, U8, U11 | completion | *"built/developed across the chapter"* ×3 | **ARV-D-112, accepted** |
| maths/vii ch 7 canonical | U11 | completion | *"the geometric intuition built throughout the chapter"* | **ARV-D-100, open** |
| maths/vii ch 7 **p10** | **U4** | **forward** | ***"…foreshadows the angle-sum property that follows in this section."*** | **NOT RECORDED — new** |

The last one appears in no defect row. It is caught by the `foreshadow` pattern added at
S6/S7 — i.e. **after that library certified** — which is the general shape of the problem: the
gate keeps getting smarter and the already-certified corpus is never re-run against it. Four of
the five are attributable to a defect row; the fifth is only visible because C7 happened to sweep
the whole corpus today.

**Recorded as ARV-D-125**, owner founder, with the cheap general fix: `--certify-only` is free
and idempotent, so a corpus-wide re-certify after any `register_scan` pattern addition would turn
this from an accident of one stage's C7 into a standing check. At 25 files it costs seconds.

---

**C7 verdict: PASS.** Zero live-ban hits on all ten files; every advisory ruled; one minor defect
(ARV-D-124) and one scanner extension landed with corpus-wide proof that it adds no false
positives.
