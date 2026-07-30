# Rolling the partition approach out to the remaining subjects & stages

**What this is.** SS·secondary is the only constitution that has been amended for the
partition engine (v1.1 → v1.5, 2026-07-24 → 07-28). This brief states what those
amendments actually bought, what the engine demands as a hard contract, where each of the
other ten LP constitutions stands against it, and what remains to be decided per subject.

Written 2026-07-28, after the weekly duration-ordering change (partition v0.4).
Revised the same day: A8 withdrawn on measurement, the container-text selector re-decided,
SS·secondary amended to v1.4 and consolidated to v1.5. Engine now at partition v0.5 /
`GENON_ENGINE_VERSION = "06"`.
Evidence: `aruvi_core/genon/compile.py`, `aruvi_core/genon/partition.py`, the eleven
`data/content/constitutions/lesson_plan/*/*/lesson_plan_constitution.txt`, the eleven
assessment constitutions, and the live SS·IX ch 5 canonical (21 units, 84 bands).

---

## 1. The hard contract

`compile.py` is the gate. It claims to be subject-agnostic and it is — which means every
subject must speak the same declaration language. A canonical that misses ANY of the
following raises `GenonDeclarationError` and the chapter simply cannot be prepared:

| # | Requirement | Read at |
|---|---|---|
| C1 | `result.lesson_plan.periods[]`, each with `period_number`, `period_duration_minutes`, `activity_title`, `section_anchor` | `compile_stream` |
| C2 | **`time_bands[]`** on every period — that exact key | `compile_stream` |
| C3 | Every band carries `band_id`, `minutes` (`"a-b"`, parseable), **`activity`** — that exact key | `_check_declarations`, `_parse_band` |
| C4 | Every band has a role in `{hook, development, consolidation}` — from `role_handoff[band_id]`, or inline `band.role` for pre-v1.2 canonicals | `_check_declarations` |
| C5 | Every `competency_edges[]` entry carries `band_refs` ⊆ its own unit's band_ids | `_check_declarations` |
| C6 | Every assessment item carries `phase_ref` | `_check_declarations` |

And one soft requirement, reported rather than enforced:

| C7 | `unit_handoff` — one `{title, teacher_notes}` per adjacent unit pair, N−1 entries | degrades to a mechanical join, logged in `genon.handoff_missing` |

C4 is not bookkeeping. The roles ARE the cut algorithm: `CUT_COST = {consolidation: 0,
development: 2, hook: 6}` decides where a sitting breaks, and the three compression regimes
protect development pacing while hooks and consolidations absorb the squeeze (and trailing
consolidations demote to homework below 0.35). A plan without roles cannot be cut well; a
plan with roles the author was *aiming at* is worse than one where they were read off
afterwards — which is exactly why v1.2 moved them out of the bands into `role_handoff`.

---

## 2. Where the eleven constitutions stand

| Subject · stage | Ver | band_id | band_refs | role_handoff | unit_handoff | band field | skill layer |
|---|---|---|---|---|---|---|---|
| **social_sciences · secondary** | **1.5** | **✓** | **✓** | **✓** | **✓** | `time_bands` | `competency_edges` |
| social_sciences · middle | 2.7 | — | — | — | — | `time_bands` | `competency_edges` |
| science · secondary | 1.0 | — | — | — | — | `time_bands` | `implied_lo`, no edges |
| mathematics · secondary | 1.0 | — | — | — | — | `time_bands` | `implied_lo`, no edges |
| the_world_around_us · preparatory | 1.2 | — | — | — | — | `time_bands` | `implied_lo`, no edges |
| science · middle | 2.1 | — | — | — | — | `phases{minutes, description}` | `implied_lo`, no edges |
| mathematics · middle | 3.3 | — | — | — | — | `phases{minutes, description}` | `core_/adjunct_competencies` |
| mathematics · preparatory | 1.1 | — | — | — | — | `phases{minutes, description}` | `core_/adjunct_competencies` |
| english · preparatory | 1.0 | — | — | — | — | `phases{minutes, description}` | `implied_lo`, no edges |
| english · middle | 1.5 | — | — | — | — | `phases{minutes, description}` | `implied_lo`, no edges |
| english · secondary | 1.0 | — | — | — | — | `phases{minutes, description}` | `implied_lo`, no edges |

Assessment side: only `social_sciences/secondary` (v1.2) carries `phase_ref` / `band_ref`.
The other ten carry neither, so C6 fails for every one of them.

Two groups fall out.

**Group A — `time_bands` already** (SS·middle, science·secondary, maths·secondary,
TWAU·preparatory). These need the declarations layer and nothing structural.

**Group B — `phases[]`** (science·middle, maths·middle, maths·preparatory, english ×3).
These need a rename *and* a key rename: their phase objects are `{minutes, description}`,
and the compiler reads `activity`. Two options, and it is a real decision:

- amend the six constitutions to emit `time_bands[{band_id, minutes, activity}]`; or
- teach `compile.py` an adapter (`phases`→`time_bands`, `description`→`activity`).

Recommend the first. The compiler's one virtue is that it never branches, and an adapter is
a branch wearing a disguise. Six constitutions is a bigger edit but leaves one shape.

---

## 3. The amendment set

In dependency order. A1–A4 are the SS·secondary template; A5 is register; A6 is the
assessment side; A7 is new (§4). **A7 is done for SS·secondary (v1.4); everything below is
outstanding for the other ten.**

### A1 · Period schedule = exactly ONE standard row

> INPUTS 4 — Period schedule: exactly ONE row `{duration_minutes, count}`: the
> class-standard duration (40 min for classes up to VII, 45 for VIII, 50 for IX)
> × the period count. Teacher timetable variation never reaches generation; it is
> handled downstream at partition time.

Plus the matching TIME integrity constraint and the `period_schedule` schema line.

This is the amendment that makes everything else coherent: the canonical is authored ONCE
per chapter at one duration, and every teacher's variant is a partition of it. Ten
constitutions currently say "one or more rows" (science ×2, SS·middle, TWAU,
maths·secondary), `{period_duration_minutes, period_count}` (english ×3), or
"{duration, count} rows; total = B" (maths·middle/preparatory) — all of which invite the
model to author a mixed-duration plan that the partitioner then has to undo.

The band sentence ports verbatim to every stage, including preparatory (III–V → 40) and
middle (VI–VII → 40, VIII → 45). The bands are the master-plan calibration the certified
canonicals were authored at (CLAUDE.md, 2026-07-26) — do not restate them as NCF's flat 40.

### A2 · Rule 14 — band identity and edge band anchoring

`band_id` = `"P<period_number>.<ordinal>"`; every skill-layer object names the band_id(s)
of its own unit that actually execute it; the coverage handoff copies them verbatim.
Serialization only — authored content is untouched.

**This is the one that does not copy-paste.** Rule 14 hangs `band_refs` off
`competency_edges`, which only Social Sciences has. For the other eight the skill layer is
`implied_lo` rows (science ×2, maths·secondary, TWAU, english ×3) or
`core_/adjunct_competencies` (maths·middle/preparatory), and each needs its own decision
about which object carries the reference.

Worth knowing before you start: `_check_declarations` iterates `competency_edges` only, so
for those eight subjects the C5 gate is **currently vacuous** — they would pass it while
carrying no band anchoring whatsoever, and only the assessment `phase_ref` (C6) would fail.
The compiler is subject-shaped despite the docstring. Either generalise the check alongside
A2, or the gate will keep quiet about exactly the subjects that need it most.

### A3 · Rule 15 — `role_handoff` companion output

Flat `band_id → hook | development | consolidation`, covering every band in plan order,
emitted AFTER the plan is complete, with the standing prohibition that no band may be
shaped, sized, ordered, or counted in anticipation of it.

Science·middle already says "no role embedding" in its phase schema — the doctrine is
aligned, it just has nothing to carry the roles. That one is a pure addition.

### A4 · Rule 16 — `unit_handoff` companion output

N−1 adjacent-pair entries, each a `title` + a `teacher_notes` ≤90 words, authored where
both units are fully in view. The three prohibitions that matter: no splice (conjunctions
and joiners banned outright), no retreat into abstraction (the title must name a concrete
element the two units actually teach), and no completion language, since the platform may
place only part of either unit.

Soft in the compiler, hard in certification. Without it the partitioner falls back to a
mechanical join and `genon.container_text` reports PARTIAL — a degraded plan that still
serves, which is precisely why certification has to catch it instead.

### A5 · Register — temporal, positional and duration self-containment

**Port this as ONE block, not as three prohibitions.** SS·secondary accumulated the same
ban in Rules 10, 13 and 16, with a different example list each time; v1.5 factored it into
a named block sitting beside VOCABULARY, which the three rules reference in a single line
each. That cut those rules by 392 words before the block's own 196, and it states the
principle the bans all descend from:

> THE SELF-CONTAINED REGISTER — every teacher-facing string is authored without knowing
> which sitting will carry it, where in that sitting it falls, or how long that sitting
> runs. So none may name calendar time, position in any direction, or clock quantity.

Copy the block verbatim into each subject as it is amended, then reference it from that
subject's notes rule, band rule and (once A4 lands) handoff rule. Adding the three
prohibitions separately is how SS·secondary got into the state v1.5 had to undo.

**And keep the amendment note out of the file.** SS·secondary had accumulated an eight-line
version block above VOCABULARY — 425 words, ~573 tokens, read by the model on every
generation call and actionable by none of it. It now lives in `CHANGELOG.md` beside the
constitution; the `VERSION` line stays in the file, since certification records which
version a canonical was authored under. Checked across all twenty-two constitutions: only
SS·secondary had grown one, so this is a habit to avoid rather than a sweep to run.

Zero of the other ten constitutions carry either. Several actively contradict them —
english·middle's schema comment instructs "Transition from prior unit; preview into next",
which is a position reference in both directions and would survive into a plan whose
boundaries have since moved.

### A6 · Assessment constitutions — `phase_ref`

C6 is a hard gate and ten of eleven assessment constitutions fail it. An item anchored to a
period number goes stale the moment the plan is re-cut; anchored to a phase it survives,
and `build_plan` re-derives `period_ref` from `phase_to_period` (and marks an item whose
anchor unit was dropped under the coverage floor rather than silently mis-anchoring it).

Depends on A2 — the band ids have to exist before an item can name one.

### A9 · MCQ option order — a convention, not a choice

> Option ORDER is a convention, never a choice. Author the four options first; then, as the
> LAST step before emitting the item, arrange all four — the correct one included, never led
> with — alphabetically from the first word at which they differ, ascending where they are
> numeric, and label them A–D in that order. Uneven letters across a chapter are coincidence,
> not a defect.

Plus the matching prohibition, which replaces the 2026-07-16 one outright: *MUST NOT depart
from the arrangement to move the correct answer toward or away from any label.*

**Why this exists.** MEMORY item 18 added a prohibition to four assessment constitutions
(SS + Science, middle and secondary) telling the model to spread `is_correct` across A–D and
never repeat a label across consecutive items. The first live generation under it — SS·IX ch 3,
2026-07-29 — put **5 of 6 correct answers on B, four of them consecutively**. The prohibition
asks the model to randomise, which a language model cannot do; and its wording was ambiguous
anyway, since MCQs are interleaved among other item types, so "consecutive items" names
nothing definite. The convention removes the decision instead of restating the ban: position
becomes a function of the option text, blind to correctness, so there is nothing to cluster.
Letter counts may still come out uneven by coincidence of content — the amended clause says so
explicitly, because a model that "corrects" a coincidental cluster is choosing positions again.

This is the same failure family as Rule 16's spliced titles (§4 below, and LP v1.6/v1.7): a
negative prohibition aimed at a generation artefact does not steer. The fix is always an
affirmative mechanism the model can execute — derive, or arrange — never a stronger ban.

**Scope: all eleven assessment constitutions.** Every one mandates MCQs, so every one needs
the clause. It has **no dependency on A2 or A6** — it touches neither band ids nor anchoring —
so it can land in the same pass as A6 or on its own, whichever is cheaper. Mathematics is the
healthy counter-example in the corpus audit (genuinely mixed positions), which is an argument
for the convention rather than against it: the property becomes structural instead of
incidental. Note also the standing corpus-repair debt from MEMORY item 18 — the already-saved
SS and Science plans still carry clustered answers, and the repair pass should now reorder them
into convention order rather than shuffling them at random.

**How it is checked.** Not by counting letters. The audit is mechanical: are the four options
in arrangement order? A chapter whose correct answers happen to fall B, B, B, C, D, B is
compliant if the arrangement was followed, and non-compliant if it was not, whatever the
spread looks like.

**What the probe found — read this before porting.** `genon/test_mcq_convention.py` (Rs 6 a
run) authored the six SS·IX ch 3 MCQs under the first draft of the clause. Only 2 of 6 came
out arranged, but the failures were highly informative and are why the wording above says what
it says. Three of the four failures had the SAME shape: the three distractors were correctly
sorted among themselves and the correct option was pulled to A — the model sorts what it
regards as the list and leads with the answer it thought of first. The B-cluster of the old
prohibition had simply become an A-cluster (labels A,B,B,A,C,A against the certified run's
B,B,B,B,C,B). Hence "the correct one included, never led with", and hence naming the
arrangement as the last step before emission rather than a property of the authored list. The
fourth failure was different: every option opened with the same long stem ("Because…", "The
frigid zones lie…"), putting the alphabetical key thirty characters in — hence "from the first
word at which they differ". Expect both failure modes in every subject; parallel option
construction is a quality feature, so the shared-stem case will be common.

---

## 4. What the duration-ordering change adds — including to SS·secondary

Partition v0.4 sequences a mixed matrix as a repeating week with the longer periods at
maximum dispersion, so **sittings inside a single plan now differ in length**, not just in
where they start.

### A7 · Duration-independent band text — DONE for SS·secondary (v1.4, 2026-07-28)

Band minutes are not preserved. Compression rescales them through three regimes; the live
SS·IX ch 5 plan at 16×50 against a 21×50 canonical ran role-weighted at 0.762, so a band
can lose a quarter of its authored time. Band text that names its own duration goes stale
silently — and there is one instance in the certified canonical:

> P6.1 — "Students write individually for **three minutes**, then …"

SS·secondary v1.4 adds Rule 13 prohibition 6 (no duration, clock quantity, or share of the
sitting in band text; say "a quick individual list", never a number), mirrors it into
Rule 10's teacher-notes prohibition and Rule 16 prohibition 4, and corrects Rule 16's
rationale paragraph — the plan is authored at one standard duration and cut into sittings
that may differ in length from it and from one another.

**Outstanding for SS·secondary:** ch 5 carries the P6.1 violation and needs re-certifying
against v1.4. Nothing in the engine catches it; the prohibition binds the author, not the
partitioner.

### A8 · WITHDRAWN

A8 proposed a separate prohibition on assuming equal-length sittings. Measurement withdrew
it. Rule 16 prohibition 3 already forbids assuming either unit runs to completion, and
prohibition 4 bans positional references outright — no sentence violates A8 while passing
those. The duration effect is real but small: across 25 matrices on ch 5, 60-minute
sittings straddle a unit boundary 68% of the time against 59–61% at 40/45/50 min. Not
enough to carry a rule. What survives of A8 is the Rule 16 rationale wording, folded into
A7 above.

### The finding that replaced it — container-text pair selection

Testing A8 surfaced something worth more. The hypothesis was that mixing durations would
produce more 3+-unit sittings; it does not. **Wide spans are driven by the compression
ratio, not the mix** — uniform 12×50 produced four of them, more than any mixed matrix.

And in a 3+-unit sitting, `select_container_text` took the LAST adjacent pair, justified in
the code by "the opening unit contributes only its tail, so (b,c) names where the
substance is." That premise fails:

```
P3 (50m) spans units 4, 5, 6 — minutes {4: 14, 5: 32, 6: 4}
   entry used : 5-6   →  names a four-minute scrap
   unit 4 contributes 14 minutes and goes unnamed
```

Two of that plan's four wide spans went the same way, and none of it was reported —
`handoff_missing` was empty and `container_text` logged a clean Rule-16 hit.

**Fixed in partition v0.5** (engine, not constitution): the selector now takes the adjacent
pair carrying the most of the sitting's minutes, ties to the later pair. It changes P3 and
P9 (each to a pair covering 46–47 of 50 minutes) and agrees with the old rule on P2 and P8,
so nothing that was already right moved. Wide spans are now reported in `genon.wide_spans`
with the minutes per unit and which units the container text does not name.

Carry this forward as a *review* item rather than an amendment: when each subject reaches
A4, check its wide-span behaviour at a tight period budget before certifying — a title
naming a three-minute scrap is not a Rule 16 failure the validator can see.

## 5. Suggested sequencing

Constitution by constitution, not in sweeps.

0. ~~**A7 into SS·secondary** (→ v1.4).~~ Done 2026-07-28. **Re-certify ch 5 against it** —
   the P6.1 duration phrase is still in the certified canonical.
1. **A1 everywhere.** Cheapest, highest leverage, no dependency. Ten one-paragraph edits;
   it stops new canonicals being authored in a shape the partitioner has to undo.
2. **Group A, one subject at a time: A2 → A3 → A5 → A4 → A6.** Take SS·middle first —
   it shares the edge model, so A2 really is a copy-paste there and the rest follows the
   template exactly. It is the cheapest possible proof that the template ports.
3. **Decide the Group B band shape** (rename in six constitutions vs. adapter in
   `compile.py`) before touching any of them.
4. **Generalise `_check_declarations`** beyond `competency_edges` at the same time as the
   first non-SS A2, so the gate stops passing subjects it never inspected.
5. **A9 into all eleven assessment constitutions.** No dependency, one short clause each,
   and it repairs a rule that is currently failing live in four of them. Fold it into each
   subject's A6 pass; do the four MEMORY-item-18 files first, since those are the ones whose
   prohibition is known not to hold.

One caution on A1: it changes the authored duration for chapters whose canonicals already
exist, so `canonical_version` moves and every derived plan re-keys. That is correct
behaviour — a teacher mid-chapter is offered the new plan, never substituted into it — but
it means the re-certification cost is real and should be spent subject by subject, not in
one sweep.

Carry A7 into every subject as it is amended — it is register, it costs one prohibition, and
it is cheapest to add beside A5, which it sits next to.
