# C7 · Register audit — english · III · ch 11 *The Big Laddoo*

**Surface: 10 files, not 3.** The three library canonicals **plus the seven C6 served plans**
(X=9 · X=8 · X=11 · X=13 · X=6 · the mixed 40/50 matrix · X=12@50), **including
`result.dropped_units`**, which a teacher reads on screen. 1,019 teacher-facing surfaces in all.

**Exit: ZERO live-ban hits on any file.** Three advisories survive judgement as a real Rule 9
finding; everything else is dismissed with its reasoning below. One new pattern lands in
`register_scan.py` with a dated note, and was **narrowed before it was trusted**.

---

## (a) The gate's own lines

`0 ban hit(s)` on all three library files, over 49 / 50 / 34 bands plus `activity_title`,
`materials`, `teacher_notes` and `homework` (C5, `build_library.py::certify:473`). Re-run after
this step's pattern landed: **still ALL PASS** (`english_iii_ch11_20260813_134917.md`).

Extended here beyond what certification sees: `register_scan.py` run directly over all **ten**
files, including the served plans and the dropped units. **0 ban hits on every one.**

---

## (b) Ruling on the advisories

| Advisory | Count | Ruling |
|---|---|---|
| **`today`** | 8, across p10 · p07 · X=9 · X=8 · X=6's dropped unit | **DISMISSED — it means THIS SITTING, not a calendar day.** *"using the same format practised in class today"*, *"Teacher introduces today's hands-on task"*, *"based on what you observed today"*. Every instance refers to the sitting the teacher is in, which is self-consistent whenever it is taught. This is exactly the case the scanner header predicts ("a gate that fails on those would be switched off within a week"), and the template's C7 tells us to expect it. |
| **`first half`** | 1, top u1 band 3 | **DISMISSED, and it is the best illustration in this library of why the positional entries were retired.** *"teacher says the first half of each line and the class chimes in with the second half"* — the first half **of a line of the poem**. A positional word about CONTENT, not about time or units. |
| **`earlier`** (u11 notes) | 4 files | **LEGAL.** *"Having chanted and role-played the poem across earlier units, children can now discuss its structure explicitly…"* — a BACKWARD reference, legalised at v1.10, and it names the CONTENT built on ("chanted and role-played the poem") before the positional tail. The same note closes *"without requiring any prior activity to have been set"*, which is the register's own logic written back at us. |
| **`earlier`** (u12 notes) | 5 files | **NOT A HIT AT ALL — it is the disclaimer.** *"…without requiring any specific earlier activity to have taken place."* |
| **`(40 minutes)`** — clock quantity | 2, both X=13 | **DISMISSED, and worth an exclusion note.** *"1 period(s) (40 minutes) exceed this chapter's fullest plan and return to your budget."* This is **platform-generated**, not model prose, and the 40 is **the teacher's own declared duration**, echoed back from her request row. Ban 1 exists because *proportional scaling silently falsifies a stated number*; this number is never scaled — it is the input. A future scan should not chase it. |

---

## (c) What regex cannot see — the read

Three things were looked for specifically: paraphrased forward reference, a unit whose opening
move assumes another unit happened, and a closing unit that implies completion without saying so.

### The transition surface is ONE unit, and it is the best-written unit in the library

Only two of the seven served plans contain a **foreign** unit. X=9 and X=6 turned out to be pure
PREFIXES — every served unit came from its own base in order (`borrowed_from` 10 and 7, i.e. the
base itself). The genuine cross-plan borrows are **X=8** (p07 complete + the standard's synthesis
at position 8) and **X=11** (p10 complete + the standard's synthesis at position 11) — and both
borrow *the same unit*.

Read in full, that unit holds:

> *"This synthesis draws on everything the chapter explored — the poem's cumulative structure,
> describing words, animal name pairs, the blend words, and the float-or-sink curiosity —
> **without requiring any specific earlier activity to have taken place. Children who encounter
> this as their first sitting can still participate fully in every band.**"*

And the bands earn it: recitation *"from memory **or with books open**"*, a word round on
content the summary names, a free writing frame, an invented stanza on the poem's own pattern, a
closing chorus. Nothing reaches for a prior unit's artefact, discussion or homework. **It survives
the borrow into position 8 verbatim** — byte-identical band text — and is still true there.

The model wrote the serve contract into the teacher notes. That is the brief landing.

### Opening moves: the backward references are content-named, as the register asks

Every unit's opening band was read. The recurring shape is `"Having chanted the poem together, …"`
(top u2, p07 u2) and `"Having heard the poem recited together, …"` — backward, content-named,
and legal. No opening move anywhere requires an artefact another unit produced; the artefact
family reports 0.

**One borderline, recorded not filed:** p10 u2 opens *"Having chanted the poem together **in its
first full encounter**, …"*. "First full encounter" is a unit's POSITION, which the VOCABULARY
re-cut asks prose to avoid in favour of content. It is legal (backward, and it names the content
too) and has **no live consequence** — p10 u2 is never a borrowed unit, since the choice set
borrows only first-exposure units and the standard's synthesis. Worth naming as the shape to
watch if a future chapter's u2 becomes borrowable.

### THE FINDING — planner vocabulary in teacher prose, 3 hits, all in the TOP

| unit | field | leak |
|---|---|---|
| u6 | `teacher_notes` | *"…connect to the **word-work spine** content…"* |
| u11 | `teacher_notes` | *"The invented stanzas in **the final band** reward creativity…"* |
| u12 | `teacher_notes` | *"…can still participate fully in **every band**."* |

`spines_taught` / `source_spine` / `time_bands` are schema keys, and LP **Rule 9** bans "schema
keys or planner identifiers" from teacher-facing prose. A teacher reading her own plan should
never meet one. C3 found the `spine` instance; reading the whole surface finds three.

**The asymmetry is the interesting part: 3 in the top, 0 in either compact.** Same model, same
prompt, same chapter, three runs. And **the leak travels with the borrowed unit** — X=8's u8
carries *"every band"* because it *is* the standard's u12.

### The near-miss, reported because it nearly became a defect

u11's *"The invented stanzas in the final band"* reads like a forward reference to u12's
invented-stanza band, and I had it drafted as a ban-2 breach the gate could not see. It is not:
**u11's own closing band (30–40) is an invented-stanza band** — *"invites children to suggest
their own 'giant' stanza aloud, completing the frame together"*. A keyword search for "invent"
missed it because u11 says "suggest their own". A gate that fired here would have failed a
correct plan. This is why C7(c) is a read.

---

## The new pattern, and the narrowing it needed the same day

`register_scan.py` gains a **`planner-vocab`** family, **ADVISORY**, with the dated note the
file's header promises. Two disciplines from the file's own history were applied:

**1 · Field-scoped.** The first run reported 7 advisories on the top, because `homework[i]` and
`tasks_in_class[i]` are scanned as their *serialized dicts*, which legitimately contain the keys
`spine` and `task_index`. Rule 9 is about prose a teacher READS, so the pattern is scoped via
`_FIELD_SCOPED` to `activity_title` · `teacher_notes` · `teacher_facilitation_note` · the band
arrays.

**2 · Narrowed before it was trusted, and it needed it.** The first cut matched bare `spine` and
`canonical` and scored **3 true positives in 14 corpus-wide**:

- *"the structural **spine** of this unit"*, *"'Monsoon' at the **spine**"* of a cause-effect
  diagram, *"the chapter's chronological **spine**"* — SS·IX, metaphorical English;
- *"the angle-sum property is the **canonical** check"*, *"a **canonical** three-step
  procedure"* — maths·VII, ordinary mathematics;
- and the one that settles it: *"shell, fins, branching shape, **spines**"* — TWAU·IV, **a sea
  creature's spines.**

So `canonical` is dropped outright and `spine` matches **only when preceded by one of Aruvi's
actual spine names** — which is the shape of the real hit, *"the word-work spine content"*.

**Re-verified after narrowing, across all 143 canonical files on disk: 3 planner-vocab hits,
all three real, all in the one file that produced them.** Corpus ban hits unchanged at 11 (all
pre-existing, none in this stage's ten files), and `english iii 11 --certify-only` still reports
ALL PASS.

> This is the S6 note doing its job one stage later: *"I first added all seven as BANS. Six were
> wrong, and the certified corpus said so immediately."* Six of seven then; eleven of fourteen
> now, caught before the pattern was believed rather than after.

---

## Verdict and what is filed

**Zero live-ban hits across ten files — the C7 exit is met.** The three planner-vocabulary hits
are a **Rule 9** matter, not a register ban, and they extend C3's single-instance subjective fail
(**ARV-D-148** covers the `spine` one) rather than opening a new row: same rule, same file, same
field, two more instances. ARV-D-148's evidence is amended to name all three and to record the
top-vs-compact asymmetry.

**No new defect.** The pattern that would have made these mechanical now exists.
