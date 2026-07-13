# period → unit — change log

Two levers, same goal (the teacher reads "unit", never "period"):

- **Lever A** — rename in the **generation source** (constitutions + prompts) so *new / pre-warmed*
  plans are born saying "unit". Documented below.
- **Lever B** — a **display-time cleaner** that rescues the **historic** saved plans without
  backfilling storage. Documented in the next section.

---

## Lever B — display-time cleaner (`aruvi_core/unitize.py`)

**What it does.** Rewrites the *teaching-chunk* sense of "period" to "unit" at the two display
sinks only — `ViewModel.to_dict()` (the JSON the API serves to the React app) and
`render/html.py` (PDF/export). The saved plans on disk and the engine's normalized view model
stay **literally "period"**; only what reaches the teacher's eyes says "unit". No backfill, fully
reversible (delete two call sites + the module).

**Why pattern-scoped, not a find-replace.** "period" is overloaded. The cleaner converts ONLY
when context marks a teaching chunk — a chunk determiner immediately before
(this/that/the/each/previous/next/first/last/closing/subsequent/consecutive/… period), a number
immediately after ("Period 1", "Periods 1–2"), or a duration immediately before ("40-minute
period"). It deliberately does **not** touch:

- domain science — "periodic table", "the period of a pendulum", "period of rigidification"
- punctuation — "end the sentence with a period"
- scheduling — "35 minutes × 3 periods" (and it never sees `period_schedule_display` anyway)
- ambiguous — bare "a period of time"; and it errs toward *leaving* "first period of the chapter"
  (the "period of X" guard) rather than risk corrupting "period of oscillation".

Capitalisation and plurals are preserved ("Period"→"Unit", "periods"→"units").

**Fields cleaned** (teacher-facing narrative only): period `title`, `activities`,
`teacher_notes`, `materials`, `homework`, and each phase's `text`. **Never** touched: schema keys,
group labels, `meta` (carried-not-interpreted extras), scheduling fields.

**Verification (2026-07-13).**

- `tests/test_unitize.py` — 10 convert cases + 11 keep/trap cases, idempotency, walker-scope
  (confirms keys/meta/labels untouched), and a corpus corruption scan.
- Dry-run over all **41 saved plans**: 343 narrative strings changed, **0 corruption**
  (no "unit of …", "unitic", "time unit").
- End-to-end on a real historic plan (science vii ch_02): the served view model turned 9
  "Period N" references into "Unit N" (teacher_notes, materials, activity/phase text) while the
  file on disk stayed literal. 6 "Period N" remain only in `period.meta` duplicates, which the
  renderers never display (they read first-class `p.materials`; roles are ignored).
- Full existing suite: **17/17 green** (incl. `test_api`, which exercises the `to_dict` path).

**Known conservative miss:** "the first/final period of the chapter" (means the first/final unit)
is left as "period", because it is structurally identical to the time-sense "period of X" the
guard protects. A missed swap is mild; a wrong swap corrupts science prose — the asymmetry is
intentional.

---

## Lever A — generation source (constitutions + prompts)

**What this is.** Lever A renames the teaching chunk from "period" to "unit" **in the
generation source** (constitutions + authoring prompts), so that *newly generated / pre-warmed*
lesson plans are born saying "unit" in the prose the teacher reads. Historic saved plans are
handled by Lever B (above).

**Scope: narrative-only (agreed 2026-07-13).** Only teacher-facing prose is swapped. Two things
are deliberately **kept** as "period":

1. **Schema field names** — `period_number`, `period_duration_minutes`, `period_numbers`,
   `periods[]`. Changing these makes the model emit a different key and silently breaks every
   normalizer (`p.get("period_number")` → nothing). Non-negotiable freeze.
2. **Scheduling / allocation vocabulary** — "period schedule", "period budget", "period count",
   "period assignment". The teacher never reads these instructions; they are the internal
   time-slot budget.

Each edited file also gains **one additive `VOCABULARY` line** near the top that tells the model:
write "unit" in all teacher-facing prose, keep "period" only for schema + scheduling. This is what
makes the remaining mixed usage coherent rather than accidental.

**Reversal.** Every swap is an exact-string replacement, so this log *is* the reversal script.
Full revert = replay each `swap` as after→before and delete each `insert` block. Partial revert =
filter `changes.json` by file, by `op`, or by `id`. `git diff` / `git revert` is the second,
independent trail.

---

## Status: COMPLETE across the board (conservative)

**10 LP constitutions edited** (+45 / −15). Verified via `git diff`: no schema or scheduling
token was removed; every removed→added pair is a clean narrative period→unit swap.

Each file received the **vocabulary anchor** (TWAU's variant names `teacher_facilitation_note`).
Narrative swaps by file:

| file | narrative swaps | notes |
|---|---|---|
| science/middle | 3 | RULE 10 (pilot) |
| science/secondary | 3 | RULE 10: run-the-unit-well, connect/first, grounding + no-restate |
| mathematics/secondary | 1 | RULE 10: previous unit + first unit |
| mathematics/middle | 1 | teacher_notes schema comment: "the previous unit" |
| mathematics/preparatory | 1 | teacher_notes schema comment: "Recap prior unit" |
| english/middle | 1 | teacher_notes schema comment: "prior … unit; preview into next" |
| english/preparatory | 1 | teacher_notes schema comment: "transition from prior unit" |
| english/secondary | 0 | guidance says "prior / next" with no period token; anchor governs |
| social_sciences/middle | 0 | no teacher_notes cross-ref; anchor governs |
| the_world_around_us/prep | 0 | facilitation note has no cross-ref; anchor governs |

### Deliberately NOT changed (inspected)

- **Assessment constitutions** (twau/ss/science ×2/maths-sec): every "period" is a schema key
  (`period_number`, `period_ref`, `period_numbers`) or scheduling ("stage period allocation",
  "period budget", "one item per period"). No teacher-facing lesson prose → no change, no anchor.
- **Chapter-summary prompts** (science-sec, english ×3, maths ×2): "period" only as scheduling /
  authoring-meta ("allocate periods across sections", "in-period task", "beyond-period",
  "period budgeting"). Not teacher-facing → no change.
- **TWAU competency-mapping constitution:** "periods that teach those sections" / "period-level
  CG assignment" — scheduling/structural → no change.

Say the word if you want anchors added to the assessment constitutions too (belt-and-suspenders),
but they carry no chunk cross-references, so it isn't needed for the teacher_notes problem.

---

## Pilot detail — Science / middle

`data/content/constitutions/lesson_plan/science/middle/lesson_plan_constitution.txt`

| metric | value |
|---|---|
| "period" substrings before | 49 |
| "period" substrings after | 52 |
| narrative swaps | 3 (touching 5 period-words) |
| additive lines | 1 (VOCABULARY anchor) |
| kept (schema + scheduling) | 44 |

Reconciliation: 49 − 5 (narrative words removed) + 8 (period-tokens *inside* the new VOCABULARY
line, all naming schema/scheduling keys on purpose) = 52. ✓ Verified via `git diff`: exactly the
4 intended changes, nothing else.

### The 4 changes

1. **Insert — VOCABULARY anchor** after the OUTPUTS block (line 15).
2. **Swap** (RULE 10) — "helping them run the **period** well" → "…run the **unit** well".
3. **Swap** (RULE 10 cross-reference — the direct source of *"in the previous period"*) —
   "connect this **period** to the previous one … how this **period** builds on it. The first
   **period** instead orients…" → **unit** ×3.
4. **Swap** (RULE 10 constraint) — "Grounded in this **period's** activity" →
   "…this **unit's** activity".

### Borderline cases kept (flagged for your call on widening)

- L11 "Period-by-period lesson plan (one activity per period)" — output-format spec language.
- L63 "not per period … multiple periods … each individual period" — LO-to-chunk mapping.
- L88 "same approach in more than two consecutive periods" — approach-diversity constraint.
- L104 "homework … is a bridge between periods" — conceptual framing to the model.
- L116/118 "PER-PERIOD TEACHING GUIDANCE / Every period MUST carry…" — refers to the schema object.

None of these emit "period" into teacher-visible output, so under narrative-only scope they stay.
Say the word if you want any of them folded in.

---

## Open decision before scaling

**Constitution versioning.** Each LP constitution carries a version (Science-middle is
`VERSION 2.1`) and `CLAUDE.md §3` notes output caching is keyed by `constitution_version`. If
we change a constitution without bumping its version, a future cache could serve stale
pre-rename content. Recommend bumping each edited file's version (e.g. 2.1 → 2.2) as part of
this change set — **not yet done** (it is not a word-swap). Confirm and I will include version
bumps in the roll-out.
