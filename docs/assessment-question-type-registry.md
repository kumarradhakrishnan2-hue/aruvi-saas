# Assessment — Question-Type Registry & Normalized Item Contract

**Status:** spec (2026-07-10). The standardization artifact the LP-attach work builds on.
**Companion:** `docs/architecture-plan.md §I-ter` (governing principle + verified 8-rule link table).
**Scope:** how a saved assessment item is normalized into ONE renderer-facing shape, and how each
question type renders on the Screen 3b assessment view.

---

## 0. The two-axis decision (why this is type-driven, not grade-driven)

Two consumers want two different axes, so the standard has two parts:

1. **Question type — the PRIMARY axis (this registry).** The 3b renderer is subject-agnostic by
   design ("one renderer, uniform contract"). It switches on **`question_type`**, because each type
   has a distinct card anatomy. There are **11 types total**; define each once.
2. **Subject × stage — the COMPANION axis (§5 allow-matrix).** Which types are permitted, with
   counts/weights. This is the constitution/normalizer's concern (gating + generation), never the
   renderer's.

**Grade drops out.** The allowed set is a subject × **stage** property (prep / middle / secondary);
grade only shifts counts/weights, which the allocator/constitution already own. Listing grade-wise
would duplicate the same 4-type core ~15 times and bury the real variation.

---

## 1. The core complication — one type name, three source shapes

The same `question_type` string is emitted in **three incompatible field shapes**, by subject family.
This is the divergence the normalizer exists to erase (mirrors the 8-rule table's per-subject gating).

| Family | Subjects | Stem key | Answer/guide keys | Options | LO key |
|---|---|---|---|---|---|
| **Constitution** | Science, Social Sciences, TWAU | `question_text` | `expected_elements[]` · `look_for[]` · `scaffold` · `task` · `format_of_output[]` · `guide{TYPE:{what_each_option_reveals, inclusivity, …}}` | `[{label,text,is_correct}]` | `implied_lo_assessed` (item) / handoff |
| **Maths** | Mathematics (all stages) | `prompt` | `teacher_guide{expected_answer, method_one_line, what_each_option_reveals, inclusivity}` · `exercise{book_ref,description}` | `[]` (MCQ has `options`) | none (mid/prep); handoff (sec) |
| **English** | English (all stages) | `item_stem` (+ mirrored `question_text`) | `teacher_guide{suggested_answer, expected_elements[], note}` · `transcript_ref` · `is_english` | `[{label,text,is_correct}]` (MCQ, TRUE_FALSE only) | `source_lo` (item) |

Consequence: `MCQ`-in-Science ≠ `MCQ`-in-Maths ≠ `MCQ`-in-English at the field level. The renderer
must never see these differences.

---

## 2. The uniform normalized item contract (the target shape)

Every resolver, in each subject plugin's normalizer, emits this ONE shape. The renderer reads only
this — never a raw source key. Fields absent for a type/subject are **omitted, not blanked** (see the
Maths-no-LO and no-options rules).

```
NormalizedItem {
  # ── identity & discriminator ──
  question_type      : enum(11)         # the render switch (see §3)
  id                 : str | null

  # ── the question ──
  stem               : str              # ← question_text | prompt | item_stem
  visual_stimulus    : Typed | null     # typed table/prose/svg (SAME typing as LP visuals — never raw markup)
  passage            : Typed | null     # EXTRACT_ANALYSIS reading extract (← visual_stimulus when it is the text)
  options            : [Option]         # [{label, text, is_correct}] — selected-response only; else []
  audio_ref          : str | null       # ← English transcript_ref when source_spine=listening. A page
                                        #   ref to the listening passage the teacher reads aloud; renders
                                        #   as a "Listening passage · p.NN" cue, NOT a textbook citation.
                                        #   Distinct from exercise_ref — never merge the two.

  # ── the answer / marking surface (exactly one of the first two is populated per type) ──
  model_answer       : str | null       # ← expected_answer | suggested_answer  (a worked/model answer)
  expected_elements  : [str]            # rubric bullets (constructed / performance / oral / writing)
  option_reveals     : { label: str }   # ← what_each_option_reveals (all families; legacy English: note prose)
  look_fors          : [str]            # ← look_for[]  (ECR marking cues)
  scaffold           : str | null       # ← scaffold
  method_one_line    : str | null       # ← Maths teacher_guide.method_one_line  (one-line solution path)
  format_of_output   : [str]            # ← format_of_output[]  (OPEN_TASK / performance deliverables)
  open_task_guide    : OTGuide | null   # ← guide.OPEN_TASK.{format_type, format_rationale,
                                        #    what_this_demonstrates, reading_the_scaffold, strong_vs_weak_markers}
  exercise_ref       : str | null       # ← Maths exercise.book_ref (+ description)
  inclusivity        : str | null       # ← guide.TYPE.inclusivity | teacher_guide.inclusivity

  # ── context (shown as quiet meta, never as structural labels) ──
  cognitive_demand   : str | null       # ← cognitive_demand. Present only for Science mid/sec, SS middle,
                                        #   TWAU prep, Maths secondary. Absent key OR "" → null (same state).
  competency         : {code, text} | null   # ← competency  (content subjects)

  # ── the LP link (from §I-ter 8-rule resolver; renderer treats as opaque) ──
  linked_lo          : str | null       # airs as LEARNING OUTCOME above the stem, PER ITEM (null → line absent)
  linked_periods     : [int]            # the resolved period set
  anchor_period      : int              # closing period of the set (display anchor)
}
```

**Locked rules carried from §I-ter:** `linked_lo` is per item (a 3b view can hold items testing
different LOs) → the LEARNING OUTCOME line sits above **each** item's stem, and is **absent, not
blank** when null (Maths middle/prep). The header carries only a unit framer, never a per-item LO.

---

## 3. The question-type registry (11 types → 6 render templates)

The 11 types collapse into 6 card templates. The template decides layout; the type decides which
normalized fields are populated. Order of a 3b card is always: **LEARNING OUTCOME (if any) → stem →
stimulus → answer/marking surface → inclusivity**, with the marking surface differing per template.

### T1 · Selected-response — `MCQ`, `TRUE_FALSE`
Populated: `stem`, `options[]` (correct flagged), `option_reveals{}`, `inclusivity`.
**Card:** stem → option list (each option on its own line; the correct one quietly marked) →
a **"What each choice reveals"** block mapping every distractor label to its misconception →
inclusivity note. `TRUE_FALSE` is the same template with True/False (or numbered statement) options.

### T2 · Short constructed response — `SCR`
Populated: `stem`, `visual_stimulus?`, and EITHER `model_answer` (Maths/English) OR
`expected_elements[]` (Science) — whichever the source carried → `inclusivity`.
**Card:** stem → stimulus (table/prose) → **"Suggested answer"** (model_answer) or
**"Look for"** (expected_elements as ticks) → inclusivity. Compact; single-part.

### T3 · Extended constructed response — `ECR`
Populated: `stem`, `visual_stimulus?`, `expected_elements[]` and/or `look_fors[]`, `scaffold?`,
`inclusivity`.
**Card:** stem (often multi-part a/b) → stimulus → **"Look for"** (look_fors, the richer per-part
marking cues) → **"Expected elements"** if present → scaffold → inclusivity. Taller than SCR.

### T4 · Open / performance task — `OPEN_TASK`, `PROJECT`, `WRITING_TASK`
Populated: `stem`/`task`, `format_of_output[]`, `expected_elements[]`, `scaffold?`,
`open_task_guide?` (OPEN_TASK only), `visual_stimulus?` (PROJECT often a blank table to fill),
`inclusivity`.
**Card:** task statement → **"What to produce"** (format_of_output) → **"Expected elements"** (rubric)
→ for OPEN_TASK the rich guide accordion (**what this demonstrates**, **reading the scaffold**,
**strong vs weak markers**) → scaffold → inclusivity. The richest card; keep the OPEN_TASK guide
collapsible so the card isn't a wall on a phone.

### T5 · Cloze / matching — `FILL_IN`, `MATCH`
Populated: `stem`, `model_answer` (the answer key), `inclusivity`. (English family; `options[]` empty.)
**Card:** stem (the cloze passage or the two lists to pair) → **"Answer key"** (model_answer) →
inclusivity. `MATCH` renders the key as an ordered pairing.

### T6 · Oral / numeric / passage — `ORAL_PROMPT`, `NUM`, `EXTRACT_ANALYSIS`
Three single-type variants that don't share a body with the above:
- **`ORAL_PROMPT`** (spoken output): prompt → `audio_ref?` (if listening-based) →
  **"Speaking rubric"** (expected_elements) → inclusivity. No written options/answer key.
- **`NUM`** (numeric, Maths): prompt → **"Worked answer"** (model_answer) → **"Method"**
  (method_one_line) → **"Textbook"** (exercise_ref) → inclusivity.
- **`EXTRACT_ANALYSIS`** (English secondary, close-reading): **passage** block (set off, literary
  extract) → multi-part stem (Q1/Q2/Q3) → **"Expected elements"** keyed per part → inclusivity.

> The 6 templates, not 11 types, are what the renderer actually implements. Adding a future type =
> map it to a template + declare its populated fields; zero new layout code if it fits a template.

---

## 4. Master field-mapping table (source → normalized)

The normalizer's job, exhaustively. `∅` = field is genuinely absent for that family (omit downstream).

| Normalized field | Constitution (Sci/SS/TWAU) | Maths | English |
|---|---|---|---|
| `stem` | `question_text` | `prompt` | `item_stem` |
| `options[]` | `options` | `options` (MCQ) / ∅ | `options` (MCQ,TRUE_FALSE) / ∅ |
| `option_reveals` | `guide.{TYPE}.what_each_option_reveals` | `teacher_guide.what_each_option_reveals` | `teacher_guide.what_each_option_reveals` (legacy plans: prose `note`) |
| `model_answer` | ∅ (uses elements) | `teacher_guide.expected_answer` | `teacher_guide.suggested_answer` |
| `expected_elements[]` | `expected_elements` | ∅ | `teacher_guide.expected_elements` |
| `look_fors[]` | `look_for` | ∅ | ∅ |
| `scaffold` | `scaffold` | ∅ | ∅ |
| `task` → `stem` (OPEN_TASK) | `task` | — | — |
| `format_of_output[]` | `format_of_output` | ∅ | ∅ |
| `open_task_guide` | `guide.OPEN_TASK.*` | ∅ | ∅ |
| `method_one_line` | ∅ | `teacher_guide.method_one_line` | ∅ |
| `exercise_ref` | ∅ | `exercise.book_ref` (+`description`) | ∅ |
| `audio_ref` | ∅ | ∅ | `transcript_ref` when `source_spine=listening` (else ∅) |
| `inclusivity` | `guide.{TYPE}.inclusivity` | `teacher_guide.inclusivity` | ∅ (in `note`, if any) |
| `visual_stimulus` | `visual_stimulus` (type it) | `visual_stimulus` | `visual_stimulus` |
| `cognitive_demand` | `cognitive_demand` | `cognitive_demand` (sec only; else absent → null) | absent/`""` → null |
| `competency` | `competency` | ∅ | ∅ |
| `linked_lo` | handoff `implied_lo` / item `implied_lo` | ∅ (sec: handoff) | `source_lo` |

`option_reveals` note: all three subject families now give a `{label: text}` map directly. English's
assessment constitutions (prep/middle/secondary) were rewritten (2026-07-10) so MCQ emits
`teacher_guide.what_each_option_reveals` like Science/Maths; `note` reverted to verification-fallback
only. **Legacy saved English plans predating the rewrite carried the diagnosis as prose in
`teacher_guide.note`** — those were migrated in place to the keyed map (fallback items kept their
`note`). The normalizer should still tolerate a prose `note` on any un-migrated MCQ as a fallback.

---

## 5. Companion — subject × stage allow-matrix (gating & counts, not rendering)

Deduped from grade (the taxonomy is stage-level; grade only changes counts). `—` = not offered.

| Subject | Preparatory (III–V) | Middle (VI–VIII) | Secondary (IX) |
|---|---|---|---|
| Science | — | MCQ · SCR · ECR · OPEN_TASK | MCQ · SCR · ECR · OPEN_TASK |
| Social Sciences | — | MCQ · SCR · ECR · OPEN_TASK | — |
| The World Around Us | MCQ · SCR · ECR · OPEN_TASK | — | — |
| Mathematics | MCQ · SCR · NUM (· ECR) | MCQ · SCR · ECR · NUM | MCQ · SCR · ECR · NUM · OPEN_TASK |
| English | MCQ · SCR · FILL_IN · MATCH · TRUE_FALSE · ORAL_PROMPT · WRITING_TASK · PROJECT | + ECR | + EXTRACT_ANALYSIS |

Four subjects share the clean 4-type core (MCQ/SCR/ECR/OPEN_TASK); Maths swaps in NUM (and adds
OPEN_TASK only at secondary); English is the outlier language palette. Counts/weights per type live
in each `assessment_constitution.txt` (the SS-middle exact-counts fix is the current precedent; §J.3
owes the same audit to the other subjects).

---

## 6. Resolver & LP-link (defer to the 8-rule table)

Rendering is type-driven; **linking is subject×stage-driven** and already specified — do not re-derive
it here. Each subject plugin's normalizer runs its row from the §I-ter verified 8-rule table to fill
`linked_periods`, `anchor_period`, `linked_lo`. Three carrier families: item-self-sufficient (SS,
TWAU), handoff-bridged (both Sciences, Maths-secondary — never join `section_anchor`), period-field
join (Maths mid/prep, English). Guardrail: each resolver is parity-tested "every item resolves to ≥1
period, 0 orphans" against a real saved plan.

---

## 7. Build order this unlocks

1. ✅ **Contract + enum** (2026-07-10) — `NormalizedItem` (§2) + the `QuestionType` enum in
   `aruvi_core/view_model.py` (+ `RENDER_TEMPLATE`, the §3 type→template map). NOTE: the enum
   holds **12** types — this doc's "11" is a miscount of its own §3/§5 lists (all 12 occur in
   the saved corpus).
2. ✅ **Per-subject normalizers** (2026-07-10) — `aruvi_core/assessment_norm.py` family builders
   (from_constitution / from_maths / from_english) wired into all 5 plugins after `stamp()`;
   parity-tested by `tests/test_normalized_item.py` (382 items, 12/12 types, omitted-not-blanked
   serialization). Corpus findings locked there: Maths secondary is a guide{TYPE}+top-level
   hybrid. SS/TWAU originally wrote the guide FLAT (by their constitutions' own design) —
   **standardized at source 2026-07-10** per the English-fix playbook: SS assessment
   constitution v1.7 + TWAU v1.3 now mandate `guide.{TYPE}` nesting (the §1 table's
   `guide{TYPE:{…}}` shape holds for the whole family again), and all SS/TWAU saved plans
   were migrated in place (pure relocation, strict diff-verified). The builder keeps a
   corpus-unused flat fallback + the prose-`annotation`→"note" last resort. The third
   English prose-note MCQ (missed by the earlier English migration) was also converted;
   the only note-only MCQ remaining is the genuine `[Verification failed]` item.
3. ✅ **3b renderer** (2026-07-10) — `LessonView.jsx` `AssessCard`, switching on `template` only
   (green scheme, per-item LO absent-not-blank, pre-split tables, collapsible OPEN_TASK guide).
   Live + mobile pass pending (MEMORY.md 2026-07-10).
4. **Constitution counts audit** (§5 / §J.3) — deferred to the generation milestone.

## Open items / flags
- ~~**English `option_reveals`** is prose in `note`, not a `{label:…}` map — decide split-vs-keep.~~
  **RESOLVED 2026-07-10:** constitutions rewritten to emit `teacher_guide.what_each_option_reveals`
  (keyed, like Science/Maths); existing saved English plans migrated in place. TRUE_FALSE `note`
  (verdict + justification) deliberately left as-is → maps to `model_answer`, not reveals.
- **`visual_stimulus` typing** — raw table/prose strings must be typed like LP visuals (never dumped
  as text); EXTRACT_ANALYSIS's extract routes to `passage`, not a generic stimulus.
- **`cognitive_demand`** — optional meta; present only for Science mid/sec, SS middle, TWAU prep,
  Maths secondary. Absent for all English and Maths prep/middle (key missing OR `""` — both → null,
  no real difference). Renderer shows the chip only when non-null; no placeholder otherwise.
- ~~**Listening types** carry an audio `transcript_ref` — surface as an audio-source note.~~
  **RESOLVED 2026-07-10:** `transcript_ref` gets its own normalized field `audio_ref` (English,
  `source_spine=listening` only), kept separate from `exercise_ref`; renders as a "Listening passage ·
  p.NN (read aloud)" cue. It is an input the item can't run without, not a source citation.
