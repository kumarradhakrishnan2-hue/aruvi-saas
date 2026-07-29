# Rolling the partition approach out to the remaining subjects & stages

**What this is.** SS·secondary is the only constitution that has been amended for the
partition engine (v1.1 → v1.3, 2026-07-24 → 07-28). This brief states what those
amendments actually bought, what the engine demands as a hard contract, where each of the
other ten LP constitutions stands against it, and what remains to be decided per subject.

Written 2026-07-28, after the weekly duration-ordering change (partition v0.4).
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
| **social_sciences · secondary** | **1.3** | **✓** | **✓** | **✓** | **✓** | `time_bands` | `competency_edges` |
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
assessment side; A7 is new (§4).

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

### A5 · Register — temporal and positional self-containment

Two prohibitions, from v1.1.2 and v1.2.1:

- **Bands** (Rule 13): no calendar words, no cross-unit references. Each band speaks in the
  present of its own activity.
- **Teacher notes** (Rule 10): continuity is expressed by naming the content it builds on,
  never by pointing at a unit's position. Only the platform knows where a timetable places
  a boundary.

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

---

## 4. What the duration-ordering change adds — including to SS·secondary

Partition v0.4 sequences a mixed matrix as a repeating week with the longer periods at
maximum dispersion, so **sittings inside a single plan now differ in length**, not just in
where they start. Two consequences no constitution currently covers.

### A7 · Duration-independent band text

Band minutes are not preserved. Compression rescales them through three regimes; the live
SS·IX ch 5 plan at 16×50 against a 21×50 canonical ran role-weighted at 0.762, so a band
can lose a quarter of its authored time. Band text that names its own duration goes stale
silently — and there is already one instance in the certified canonical:

> P6.1 — "Students write individually for **three minutes**, then …"

Proposed, as a Rule 13 prohibition alongside the calendar-words one:

> MUST NOT name any duration, clock quantity, or share of the sitting in band text —
> no "for three minutes", "in the last ten minutes", "for the remaining time", "the whole
> period", "half the session". The rail carries the minutes and the platform sets them;
> band text carries the teaching move alone. Where a task is genuinely brief, say so in
> kind ("a quick individual list") and not in number.

Same prohibition belongs in Rule 16's `teacher_notes` and in Rule 10.

### A8 · Sittings of unequal length within one plan

Rule 16's prohibition 3 already forbids assuming a unit runs to completion. With v0.4 a
stronger statement is warranted, because a single plan's sittings now genuinely vary:

> A sitting's length is not fixed within a plan. Container text MUST NOT assume how much
> of either unit the sitting holds, nor that consecutive sittings are of equal length.

This one applies to SS·secondary too — it is the first amendment the template itself needs.

---

## 5. Suggested sequencing

1. **A1 everywhere.** Cheapest, highest leverage, no dependency. Ten one-paragraph edits;
   it stops new canonicals being authored in a shape the partitioner has to undo.
2. **A7 + A8 into SS·secondary** (→ v1.4), and re-certify ch 5. Small, and it closes a
   known defect in the only certified chapter.
3. **Group A, one subject at a time: A2 → A3 → A5 → A4 → A6.** Take SS·middle first —
   it shares the edge model, so A2 really is a copy-paste there and the rest follows the
   template exactly. It is the cheapest possible proof that the template ports.
4. **Decide the Group B band shape** (rename in six constitutions vs. adapter in
   `compile.py`) before touching any of them.
5. **Generalise `_check_declarations`** beyond `competency_edges` at the same time as the
   first non-SS A2, so the gate stops passing subjects it never inspected.

One caution on A1: it changes the authored duration for chapters whose canonicals already
exist, so `canonical_version` moves and every derived plan re-keys. That is correct
behaviour — a teacher mid-chapter is offered the new plan, never substituted into it — but
it means the re-certification cost is real and should be spent subject by subject, not in
one sweep.
