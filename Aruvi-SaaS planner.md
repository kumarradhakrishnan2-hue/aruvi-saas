# Aruvi Teacher Planning Layer – Design Summary

## Core Principle

Aruvi remains fundamentally an AI-powered lesson planning platform.

The AI-generated lesson plan is the canonical pedagogical plan and is not continuously rewritten based on classroom events.

Teachers adapt execution; Aruvi preserves planning integrity.

---

## Existing Workflow (Retained)

### 1. Allocate

Teacher selects:

- Subject
- Term
- Chapters

AI allocates available periods based on:

- Effort Index
- Competency Weightage
- Administrative inputs
- Teacher overrides

Output:

| Chapter   | Allocated Periods |
| --------- | ----------------- |
| Chapter 1 | 13                |
| Chapter 2 | 10                |
| Chapter 3 | 8                 |

---

### 2. Generate

AI generates the lesson plan.

Example:

- Period 1
- Period 2
- Period 3
- ...
- Period 13

No changes to this stage.

---

### 3. My Plan (Evolved)

The current static repository of lesson plans evolves into a teacher execution and planning workspace.

No new top-level tabs are introduced.

---

## Period as an Object

Each lesson period becomes an independent object.

Example: History Chapter 3

- Period 1
- Period 2
- Period 3
- ...
- Period 13

Each object contains:

- Objectives
- Activities
- Resources
- Assessments
- Homework

This objectification enables tracking and navigation.

---

## Teacher Weekly Schedule

The teacher enters a recurring weekly timetable.

Example:

| Day       | Period | Class      |
| --------- | ------ | ---------- |
| Monday    | 2      | 7A History |
| Monday    | 5      | 7B History |
| Tuesday   | 3      | 7C History |
| Wednesday | 1      | 8A History |

**Important:** This is NOT a school ERP calendar.

Aruvi does not manage:

- School holidays
- Leave calendars
- Timetable generation
- Attendance systems

It only stores the teacher's recurring teaching slots.

---

## Section-Level Progress

Progress is tracked independently for each section.

Example:

- 7A → Period 6
- 7B → Period 4
- 7C → Period 5

The same chapter can naturally progress at different speeds across sections.

This reflects real classroom behaviour.

---

## Key Design Shift: Lesson Pointer

> **Vocabulary note (standing rule).** "Pointer" is **internal/design vocabulary only** — it is
> how *we* describe the model in this doc and in code. It must **never appear in any teacher-facing
> UI string.** In the product, say it in plain language instead: "current period", "where you left
> off", "your place in the lesson", "resumes at Period N". Any new screen or copy is checked
> against this before it ships.

Instead of tracking detailed completion states, Aruvi tracks a single value:

### Current Lesson Pointer

Example: 7A History

**Current Lesson = Period 4**

Meaning: "When the teacher opens the next 7A History class, show Period 4."

This becomes the primary execution state.

---

## What Happens After a Class?

After completing a class, the teacher makes one simple decision:

### Where should this section continue next time?

Options:

- Continue with Period 4
- Move to Period 5

This updates the lesson pointer.

No detailed tracking of:

- Percentage completion
- Partial completion
- Activity completion

is required.

---

## Why This Works

Teachers routinely:

- Extend discussions
- Condense activities
- Assign homework
- Skip exercises
- Catch up later
- Blend adjacent lessons

Trying to model all of this creates unnecessary complexity.

The lesson pointer respects teacher autonomy.

---

## Handling Disruptions

Examples:

- Teacher absent
- Holiday
- Assembly
- Examination interruption

No special handling is required.

If a class does not happen:

**Current Lesson remains unchanged.**

Example:

- Current Lesson = Period 4
- Class missed
- Next class still opens: Period 4

No additional workflow required.

---

## Separation of Execution and Planning

A critical insight from the discussion:

**Execution state and planning visibility must be separated.**

### Execution

The lesson pointer determines: "What should I teach next?"

Example: Current Lesson = Period 4

### Planning

Teachers need visibility into upcoming lessons.

Example:

- Current Lesson: Period 4
- Upcoming: Period 5
- Following: Period 6

Teachers can preview future lessons without affecting progress.

This allows:

- Weekend planning
- Resource preparation
- Assessment preparation
- Activity preparation

without changing the lesson pointer.

---

## Weekly Planning Experience

On Saturday or Sunday, the teacher views:

### Next Week

#### Monday

7A History

- Current: Period 4
- Upcoming: Period 5, Period 6

#### Tuesday

7C History

- Current: Period 5
- Upcoming: Period 6, Period 7

This provides a genuine planning experience while preserving execution simplicity.

---

## What Aruvi Deliberately Avoids

Aruvi should not become:

- School ERP
- Timetable generator
- Leave management system
- Attendance tracker
- Annual calendar manager

These concerns dilute the core product.

---

## Final Product Vision

Aruvi consists of two integrated layers:

### Layer 1 – Curriculum Planning

**Allocate → Generate**

Creates pedagogically sound lesson plans.

### Layer 2 – Teacher Execution & Planning

**My Plan**

Provides:

- Weekly teaching schedule
- Section-wise lesson pointers
- Upcoming lesson visibility
- Weekend planning support
- Lightweight progress tracking

without modifying the AI-generated lesson plan.

---

## Guiding Principle

The AI owns the lesson plan.

The teacher owns execution.

Aruvi's role is to connect the two through a simple lesson-pointer model that supports real classroom variability without compromising pedagogical integrity.

---

**One final observation:** this direction subtly changes Aruvi from being merely a "lesson plan generator" into a **teacher operating workspace**. The AI plan remains the asset, but the weekly planner becomes the reason teachers return to the platform every week rather than only when generating a lesson plan.

---

# Planning Layer — Build Spec (settled 2026-06-23)

This is the spec the planning layer is built against. Where it refines the draft above, it
governs. Live generation is wired **last**; everything here is built and tested on existing
saved plans as fixtures.

## A. Principles (non-negotiable)

1. **The weld is the product.** A tracker alone is worthless (teachers already use a diary);
   a lesson plan alone is inert. The value is the pointer resolving to authored content. All
   of this exists **only where a saved lesson plan exists** — a slot with no plan is a plain
   schedule row, nothing to follow.
2. **ERP test (use to refuse scope-creep):** if a feature works equally well whether or not the
   teacher reads the lesson, it is an ERP feature — do not build it. No completion %, no
   delayed/done states, no holidays, no attendance, no dates.
3. **Pointer = instruction, not progress.** It records "where do I resume," never "how far
   along." It moves **only by explicit teacher action**; the system never advances, infers, or
   auto-completes it. A stationary pointer is valid and honest, not an error. A teacher can
   ignore it with no penalty beyond getting less help.
4. **Dateless trigger.** The schedule is days, not dates; the system cannot detect that a class
   happened. The only trigger is **the teacher opening the slot**. No notifications, no "class
   over" events. On open, the slot offers the content and a one-tap advance.
5. **Navigation is universal; manipulation is local.** A teacher can view any period by any
   route; pointer controls (stay / move-next) appear **only on the current period**. Every
   other period is read-only.
6. **No branching on subject, ever.** Differences live in plugin data, not in shared code.

## B. State model (per slot, e.g. "6A Science")

The system stores per slot: one **active-plan reference** + one **pointer**. States:

```
empty ──(teacher picks chapter)──▶ in-progress[chapter, pointer] ──(teacher ends)──▶ empty
```

- **Start = declaration.** Empty slot shows that grade/subject's saved plans and asks "Which
  chapter are you starting?" The tap binds the chapter and creates the pointer (period 1, or
  wherever she says). Until the tap, the slot is a plain schedule row.
- **End = declaration**, identical in shape. Reaching the last period only *prompts* ("Finished?
  Start the next chapter") — it never auto-ends. She may sit at 10/10 for revision; the offer
  recurs each open until she acts.
- **Truncation is first-class.** "Done with this chapter" at 12/13 is one unburied tap.
- **One off-ramp = "Stop tracking."** Same action and outcome as "done": no trail, returns to
  empty, plan stays safe in My Plans. Lives **on the slot view**, not in a settings menu.
- **Chapter-end offers Chapter Notes (§I-bis).** On the chapter-end transition — either "I'm done"
  or "Stop tracking" — a single declinable offer: "Add any notes on this chapter for next time?"
  Yes opens the Chapter Notes window; No moves on to the empty slot. The one active note-prompt.
- **No mid-chapter plan switch.** Once a chapter begins, its active plan is **locked** for the
  chapter's duration.

## C. Active-plan rule (regeneration)

The calendar points at a **slot**, never a plan. "Active" is a property of the
**(section, chapter)** pair, not a global flag on the plan — so two sections teaching the same
chapter can run different versions in parallel (6A on Optics-12, 6B on Optics-10), each with its
own pointer. The **lock is per section**: 6A starting on 12 does not lock 6B out of 10.

- New generation auto-activates **only while the chapter is untouched** (pointer not advanced).
- Once teaching has begun, a regenerate **lands in My Plans and does not steal the slot**.
- Old versions are **never auto-deleted** — she regenerates to compare.

**Version choice happens in the flow, at the slot — she never steps out to operate.** When she
opens an unstarted slot, that is the start declaration ("Which chapter are you starting?"); if a
chapter has more than one saved version, the **start card surfaces the choice inline** (default =
newest, with a full read-only **Preview** of each version right there). There is **no separate
library and no "Make this active" control** (old Screen 6, removed 2026-06-25) — reading, comparing
and choosing all happen on the start card, the one place she already is, because reading is always
mid-decision. Switching version is only possible **before start**; after start the version locks
for that section's chapter.

**Generation outcome.** When generation completes, the plan is **auto-saved** and **opens
directly in the read-only chapter-org reader** (§E) — no "do you wish to save?" prompt, no
separate HTML LP popup (the reader *is* the view). The just-generated version becomes the
**active-in-waiting** version for that chapter per the rule above (newest auto-active while
unstarted). How she *returns* to a generated plan later, and the smooth Generate ↔ My Plan
hand-off, is **deferred to the Generate-tab navigation milestone** (taken up last, with live
generation) — not patched with a dashboard indicator now.

## D. Time model — content spine (the "(c)" decision)

- The plan is **content + duration-needs**, not a fixed time sequence. The teacher inputs a
  **gross budget** (e.g. 8×45 min + 3×60 min); the AI fills it, ordering periods by **pedagogy**,
  not by the teacher's serial guess. Period/duration **counts and totals are hard constraints**;
  ordering is the AI's.
- At execution the **pointer indexes content position, not slots**. A 60-min Period 1 may span
  two real classes; the pointer simply stays on Period 1 until its content is done. Cancelled
  class → pointer unchanged. Block period → advance two. Surprise extra period → teach the next
  period's content, advance. **One primitive (pointer-into-plan, not into-calendar) absorbs all
  schedule slips with zero special-casing.**
- **Phases render as absolute durations** (e.g. `5 min · 15 min · 20 min`) summing to the period
  total — **not** time ranges. Phases flow freely; absolute durations are position-independent.

## E. Plan view — two altitudes (replaces the old standalone HTML LP view)

The navigable plan view (chapter-org page + period views) is the **single on-screen plan
reader** — the old standalone HTML LP view is retired for good and not reintroduced. The
**PDF stays** as the consolidated class-use / print artifact. The same reader serves three
access modes, differing only in whether a pointer exists:

- **Read-only, from the start card (unstarted plan, no live place-marker).** Reading a plan is
  never an independent want — it always happens because she is mid-decision (about to teach a
  class). So previewing lives **inside the start flow**, not on a separate library she navigates
  to: the dashboard's "pick a chapter to begin" row opens the **start card (§G item 5)**, which
  lists the chapter's saved versions; tapping **Preview** on any version opens the chapter-org
  reader read-only — she can drill to and read any period in full **and its assessment**, but
  there are **no place-controls anywhere** (no stay/move), because the chapter hasn't started —
  then she returns to the start card to choose. Reading and choosing are the same motivated act
  in the same place. (Resolves the earlier "where does she view it?" gap **without** a standalone
  library: the start card is both the preview surface and the commit surface.)

  > **Read-without-commitment — resolved (2026-06-25).** The genuine need stands: a teacher may
  > want to *read* a plan without committing it to a grade & section. But the earlier resolution —
  > a standalone "My Plans" library (old Screen 6) reached independently of any section — was
  > **dropped**, because in Aruvi every screen is reached *because* of a prior motivator; there is
  > no free-floating "browse my plans" want. Reading is always mid-decision. So the read-without-
  > commitment path is served **in the flow**, two ways, with **no separate library**:
  > (1) *before start* — the **start card** lists the chapter's versions and offers a full
  > read-only **Preview** (the §E reader, including the assessment suite) on each, then returns her
  > to the card to choose; reading happens any number of times before — or without ever —
  > committing, and committing (binding to a section, starting tracking) is a separate deliberate
  > tap. (2) *after start* — re-reading for prep is the period view's **← previous / next → peek
  > (§F)**, equally motivated and in-flow. Consequences: standalone Screen 6 removed; the
  > "Make this active" housekeeping control removed (version choice is the commit act on the start
  > card); the per-version contextual note (e.g. "6A is already teaching the 12-period version")
  > **stays** because it prevents accidental mismatched picks, but its mechanism tail ("that's
  > locked / own pointer") is dropped from teacher copy.
- **Default on first start (place-marker just created)** and **recede-to-link during execution
  (place-marker live)** — the two altitudes below.

Two altitudes within the reader:

- **Chapter altitude — Chapter Organization page.** The default the **first** time a chapter is
  opened. Renders the plugin's Group tree uniformly as collapsible bars that drill to period
  links: label → … → period (tap jumps to the period). Depth comes from the data (English nests
  section → spine → period; others are one level → period). **Uniform for all subjects — no
  branch.** If a subject's axis mirrors the textbook sequence (e.g. Maths sections), its org
  page simply looks like a contents list; that is correct, not a special case. The **Group label
  carries the meaning** (e.g. "C-2.3 — Analyses cause and effect", "Progression Stage 2 —
  Building the model") so the page is self-explanatory without notes. Every drill is
  **navigation, never pointer movement**.
- **Period altitude — Slot / Period view.** Once the pointer is live, opening the slot defaults
  here; a "see chapter organization" link returns to chapter altitude. The axis recedes to a
  mono kicker on the period (e.g. "PROGRESSION STAGE 2", "SPINE · CHARACTER").

## F. Slot / Period view — contents

One window:

- **Current period as hero** — title, axis kicker, phases as absolute-duration items.
- **Pointer-safe peek: ← previous / next →** — read-only preview for prep (weekend resource
  prep). Previewing the next period **must not** move the pointer and must look visibly distinct
  from the advance control.
- **Pointer controls on the current period only** — "Move to Period N+1" / "Stay on Period N",
  a deliberate two-choice act (never inferred). No phase-marker UI — the full phase list is the
  recall cue; there is no separate "tap the phase you stopped at" screen.
- **Non-current periods are read-only**, labelled passed / current / upcoming for orientation.
- **"Stop tracking" off-ramp** seated here (not on My Plans).

## G. Screens (deliverables)

1. **Schedule input** — dead simple. Fields only: day of week, grade, section, period duration.
   No dates, no holidays, no period-of-day numbers. Recurring rows. This is the one piece of
   real setup friction — keep it frictionless.
2. **Weekly dashboard** — the cross-axis Sunday glance: each section's next class, each row
   resolving to named content ("6A Science · Optics — Reflection in plane mirrors · Current:
   Period 4 · 5 phases · tap to see"). Rows with no chapter started show as plain schedule rows.
   **Not a progress comparison** — "6A 10/12 vs 6B 11/12" is irrelevant and never framed as a
   burn-down.
3. **Chapter Organization page** — section E, chapter altitude (uniform collapsible drill to
   period links).
4. **Slot / Period view** — section F.
5. **Start declaration card** — what an unstarted slot shows, reached straight from the
   dashboard's "pick a chapter to begin" row: "Which chapter are you starting?" listing that
   grade/subject's saved plans; where a chapter has multiple versions, the version choice is
   offered **inline here**, default newest. **This is also the read-without-commitment surface**
   (§E): each version carries a full read-only **Preview** that opens the §E chapter reader —
   including its assessment suite — and returns her here to choose, so she can read freely before
   committing. The tap binds the chapter to the section, starts tracking, and locks the version.
   A per-version contextual note where useful (e.g. "6A is already teaching the 12-period
   version") prevents accidental mismatched picks — kept in plain language, no mechanism-speak.

   _(There is **no** standalone "My Plans" library screen — removed 2026-06-25. Reading is always
   mid-decision, so it lives in-flow: before start via this card's Preview, after start via the
   §F period-view peek. There is no separate "Make this active" control; version choice is the
   commit act here.)_

## H. Design language

Warm-paper scholarly planner (Fraunces display, Newsreader body, IBM Plex Mono kickers; paper /
ink / pine / clay / ochre; marginal numbering rail; mono uppercase kickers; ledger hairlines).
**Mobile is first-class** — verify every screen at ~390px. Tone is supportive, never judging.

## I. Objects (identity + state slot)

`Period` is already a dataclass; every object carries `meta`. Objectify additively via `meta`,
contingent on a **stable identity** that survives regeneration (the open identity/re-anchor
problem — solve before pinning state). Worth objectifying: **phases** (intra-period time, model
the pointer as `(period, phase)` from day one, surface phase-resolution only after period-level
is proven), **materials** (aggregate into a weekly prep checklist), **assessment items** (a
per-chapter item bank), **competencies/outcomes** (school-ICP coverage dashboard later).

## I-bis. Period Notes & Chapter Notes (the teacher's overlay)

**Purpose / why it matters.** Teachers are creatures of habit — they reuse the same plan across
sections and year after year to do less work. Period/Chapter Notes are the mechanism that makes
that reuse *compound*: the AI plan is the canonical starting point; the notes are **the teacher's
accrued personal improvement layer on top of it**, built over time. This is a primary retention
hook — it's the thing she'd lose by leaving. Notes are **overlay, never edit**: the canonical AI
plan renders identically with or without them; strip the overlay and the plan is untouched.

Two tiers, plainly named (the name is the spec):

**Period Notes** — pinned to a period.
- **Where/when:** written from the **period view (slot, Screen 3), after class** — the one moment
  she's reflecting on what just happened. A deliberately invoked field, **never always-open**.
- **Viewing:** **collapsed by default.** A period that *has* a note shows a small mark
  ("📝"); tapping expands it. A period with no note shows **nothing** — no empty-and-waiting
  field (that's the chore trap we avoid). Invisible when empty, a mark when present, full text on
  invoke. Past notes are reached via a drop-down / invoke, never persistently on screen.
- **Five purposes (all execution insight, none is "edit the plan"):** (1) time — did this,
  couldn't do that; (2) materials — keep this too / discard that; (3) student(s); (4) what to do
  next class in relation to this one; (5) next-year — don't do this, do it that way.
- **Contiguous context:** purpose (4) needs the previous/next periods' notes while writing — this
  rides on the **existing ← previous / next → peek (§F)**, now also surfacing those periods' notes
  read-only. No new mechanism.

**Chapter Notes** — per (section, chapter), unpinned to any period.
- **Where:** on the **Chapter Organization page (§E), chapter altitude** — *not* the everyday slot
  view. This altitude placement **is the intrusiveness control**: the everyday teacher who only
  opens the slot to teach never lands here and never sees Chapter Notes; the reflective teacher who
  goes here finds them where her head is already at chapter level. Opt-in by location, not by nag.
- **How invoked:** a **single collapsed "Chapter Notes" affordance on that page** — a small mark if
  notes exist, nothing insistent if they don't — expanding to the field on tap. Never an always-open
  box competing with the chapter structure (the page's primary job is the section→period drill).
  Pull, not push.
- **When (three convergent moments, all on the same page):** (1) *mid-chapter reflection* — she
  steps up from a class via the slot's "see chapter organization" link and jots a thought; (2)
  *chapter-end* — on the chapter-end transition (§B), i.e. **either "I'm done with this chapter" or
  "Stop tracking"** (one transition, both labels), **one gentle, declinable offer**: "Add any notes
  on this chapter for next time?" — **Yes** opens the Chapter Notes window; **No** moves straight on
  to the empty slot. This is the single active prompt, fired at the moment she's leaving the chapter
  and next-year reflection is naturally top of mind; (3) *next-year planning* — she opens last year's
  record from My Plans (the read-only reader **is** this page), reads last year's Chapter Notes, and
  adds to this year's as she plans. One place to invoke, reached three ways; **only the chapter-end
  offer is a nudge — the one and only push for Chapter Notes — everywhere else it's pull.**
- **Purposes:** general activities where students struggled; materials used outside the book;
  next-year precautions / better planning. Reflective, long-horizon — futuristic; valued by the
  committed teacher, never in the everyday teacher's way.

**The writing surface (both tiers).** Typed, **voice-supported, multilingual**; ~250-word soft
cap; **mobile-first**. **No rich text, color, tables, or attachments** — a plain note field. The
constraints *are* the feature (a mini-editor becomes a thing to fuss over → a chore). Voice and
multilingual mostly ride the device keyboard/dictation (so "support" = not breaking Unicode / IME
/ dictation). **Maths/Science subject symbols are deferred** — v1 is plain Unicode text; a
symbol palette / shorthand is a known later enhancement (the one non-trivial input build).

**The two tiers key to two different things — and the key follows the altitude.** A generated
plan is the teacher's **owned, kept asset**, shared across sections that use it (one Optics
generation may serve 6A and 6B).

- **Period Notes → the (section, plan) instance.** A Period Note is about *what happened in a
  specific class* ("7A got stuck on the mirror angles," "6B ran short today") — irreducibly
  per-section. So Period Notes are keyed to the section instance, alongside its own pointer and
  version-lock (same per-section principle, now extended to notes — they ride the existing
  *instance* concept, not a new key). 6A's Period Notes never pool into 6B's; she keeps each class
  separate, exactly as wanted.
- **Chapter Notes → the plan asset itself (not the instance).** A Chapter Note is reflective and
  *lesson-shaped*, not class-shaped ("this investigation always overruns," "next year reorder
  these") — true regardless of which section she has in mind. Keying it per-instance would force her
  to write the same insight under 6A and 6B and let them drift — the redundancy we avoid. So she
  **writes a Chapter Note once, against the plan asset**, and it surfaces wherever that plan is used,
  for every section. Invokes the **main asset, not the section instance.**

This makes the keying **follow the altitude**: write from the class/period view → about this class →
section instance; write from the Chapter Organization page → about this chapter/plan → the asset.
The surface tells you what it attaches to. (This also *is* the class-vs-lesson distinction — a
genuinely 6A-specific thought is a class observation and belongs in 6A's Period Notes; the chapter
tier is deliberately the shared, cross-section reflection. No separate "promote to plan-level"
mechanism is needed.)

**Persistence — notes live with their record; they never migrate.** Both tiers stay with the
record they were written against (Period Notes with the section-instance, Chapter Notes with the
plan-asset record).
- **Reuse of the *same* record** (unchanged plan next year): notes persist and compound — the
  accrued edge.
- **Regeneration** (book/chapters changed → a new plan asset record): **last year's asset, its
  Chapter Notes, and each section instance's Period Notes all persist untouched as their own dated
  record.** She **opens last year's record to read them** alongside this year's fresh plan. Notes
  are **never migrated onto the regenerated plan** — a note about last year's Period 4 may not fit
  this year's (possibly different) Period 4. So the year-over-year case has **nothing to re-anchor**
  — notes don't move, can't orphan.
Records are **dated** so years stay legible.

**Privacy / safety.** Schedule + durations + these notes are the **only** teacher-authored data
in the system, and the notes are the sensitive part (candid reflections, possible student refs).
They are **private, per-teacher, tenant-isolated** — never pooled, never shown to admins — joining
the user-data-isolation set (saved_plans / feedback → per-user DB in the cloud move). The product
should **gently steer toward non-identifying phrasing** for student references (steer, not forbid)
so we don't accumulate identifiable minor data in free text. **Export** of one's own notes is a
**planned, low-priority** trust gesture ("your notes are yours") — not v1.

**Dependencies (record honestly).** (a) **Period Notes need stable period identity *within a
single plan record*** — periods must be stably identified so a note re-finds its period when that
same plan is reopened/reused. This is bounded by the "notes never migrate across plan records"
model above, which removes the cross-year orphaning risk (regeneration makes a new record, not a
re-anchor). So the identity requirement is the simpler intra-plan one, not a cross-version
re-anchor. (b) The subject-symbol input is the one non-trivial build in an otherwise plain field —
deferred per above.

## I-ter. Assessment — objectification & period linkage

Assessment is an **add-on aligned to the lesson plan**, primarily formative. Aruvi's
differentiator: unlike textbook end-of-chapter Q&A (which breaks the cognitive chain), every
Aruvi item traces to an **implied LO** that is the same LO its lesson unit was built on. The
chain is intact in the data, and that LO is the join key that lets us objectify items and link
them to the plan. Teachers use it on-the-go (per unit, deferring the pointer) or end-of-chapter;
the PDF remains the printable summary.

### The governing principle — assessment is an appendage to the LP, linked by the LO

Chapter structure (stages / sections / cells / competencies) belongs to **Chapter Organization**;
the **LP enacts** it; **assessment is an appendage to the LP**. The teacher is **never shown the
structure** to justify an item's placement — no "stage-4 assessment," no "shown at period 10,"
no forward markers. That is internal plumbing and means nothing to her. We do **not** prove to the
teacher that an item has stage/section links.

What is visible and meaningful is the **learning outcome**: wherever an assessment item exists, it
carries the LO it tests, and that LO is the honest link to the lesson ("does the class now transfer
what this period built?"). The group→period-set→anchor machinery (below) stays **entirely under the
hood in the normalizer** — it decides *which period an item surfaces at*, but never appears as
teacher-facing copy.

**The item arrives in full richness — that is the differentiator.** Each item carries what the
constitution packs into it: MCQ **distractors with what-each-reveals**, expected elements, scaffold,
look-fors, teacher guide, cognitive demand, visual stimulus. The assessment surface **opens the item
up fully**; it never reduces it to a thin "check" line. (Internally, items still resolve to a period
set and anchor at the group's closing period — see resolver table — but this is silent.)

### Link resolution — verified 8-rule table (all confirmed on real saved files)

Each item resolves to a **period set** (never "latest only" as the stored value — that is lossy;
the closing period is flagged as the display *anchor*, the set is retained). Join key, LO source,
and item-container shape are **subject-specific** and were each corrected against saved data
(constitution prose diverged from reality on all but SS):

| # | Subject / Stage | Join method | LO source | Item container |
|---|---|---|---|---|
| 1 | Science middle | item `progression_stage` → handoff `stage_number` → `period_numbers` | handoff `implied_lo` (item: `implied_lo_assessed`) | flat list |
| 2 | Science secondary | item `section_number` → handoff `section_number` → `period_numbers` | handoff `implied_lo` | `{…,questions:[]}` dict |
| 3 | Social Sciences middle | item `period_ref[]` (direct) | item `implied_lo` (inline) | flat list |
| 4 | Maths middle | item `section_ref` ("section 5.2") → period `textbook_segments[].ref` | none | flat list |
| 5 | Maths preparatory | item `section_ref` ("S2") → period `section_refs[]` | none | grouped by `section_code` A/B/C |
| 6 | Maths secondary | item `section_number` → handoff `section_number` → `period_numbers` (**NOT** `section_anchor`) | handoff `implied_lo` (item: `implied_lo_assessed`) | `{…,questions:[]}` dict |
| 7 | English (prep/mid/sec) | item (`source_section_id` + `source_spine`) → period (`section_id` + `spines_taught[]`) | handoff cell `implied_lo` (item: `source_lo`) | spine-grouped list |
| 8 | TWAU preparatory | item `period_ref[]` (direct) | item `implied_lo` (inline) | flat list (1:1) |

**Three carrier families** (the only real variation): **item-self-sufficient** (SS, TWAU — read
`period_ref` + `implied_lo` off the item) · **handoff-bridged** (Science both, Maths-secondary —
join the integer section/stage number through the handoff; **never** match `section_anchor` text
— it is messy/granular and orphans items) · **period-field join** (Maths middle/prep, English —
match the item's section/spine code to the period's own field).

**Hard-won corrections (locked by data):** never join on `section_anchor` (failed in both
secondary stages); "unique section per item" is **false** everywhere (A/B/C and intent tiers
re-test a section) — resolvers must accept many-items→one-group and one-group→many-periods;
**store the period set**, flag the closing period as anchor; **five distinct container shapes**
exist (flat list · spine-grouped · `questions` dict · `section_code` groups · per-competency) —
each resolver declares its own, none inferable; **no LO for Maths middle & prep** (structural link
only — LO/coverage views don't apply there).

### Architecture — sanctioned subject gating, not forbidden runtime branching

The per-subject link logic is **real subject gating**, but it lives in the one place the
convention sanctions it: **each subject plugin's normalizer**, run **once at normalize-time**
(not generative, not runtime). Every resolver outputs the **same uniform contract** —
`item.meta.linked_periods = [period set]`, `item.meta.anchor_period = closing period`,
`item.meta.linked_lo = LO | null` — so the renderer/engine stay subject-agnostic. This is the
assessment-side mirror of the view-model axis difference already handled in normalizers.

**Guardrails:** (a) each resolver is **parity-tested** — a per-subject "every item resolves to
≥1 period, 0 orphans" assertion run against a real saved plan (the existing parity-test pattern);
(b) resolvers are **derived from saved-file inspection, never constitution prose** (prose diverged
on 7 of 8). All 8 rows are currently **verified on real saved files**.

### Where assessment surfaces — the lesson/period viewer (Screen 3 / §F), nowhere else

Assessment lives at the **period viewer (Screen 3)** — *not* the dashboard (Screen 2, a teaching
glance) and *not* Chapter Organization (Screen 4, structure). The reason is pedagogical: at the end
of the period's phases there is a fresh, rich grasp of the LO, and the *transferability* of that
understanding is exactly what wants testing — right there, in the moment the lesson concludes.
(Because **Preview** shows future periods' content, future assessment comes along for free — it is
part of the period view.)

**Surfacing — a dedicated assessment view, not inline.** Inline expansion clogs the period viewer
(a full-richness item with distractors + look-fors is too tall, especially on a phone). Instead, a
**quiet "Assessment here" affordance** on Screen 3 opens a **dedicated assessment view (Screen 3b)**
in a **distinct green colour scheme** — set apart from the LP's warm paper so she always knows she
is in assessment, not the lesson. That view holds the period's linked item(s) in **full richness**
(the item's **learning outcome aired above its stem** — see next subsection — then stem, options
with what-each-distractor-reveals, expected elements, scaffold, look-fors, cognitive demand, visual
stimulus), and provides a clear **"← Back to lesson"** return that lands her exactly where she was.
No structural labels anywhere.

### Airing the LO on 3b — the bridge from phases to item (per item, not per view)

The teacher reaches 3b **from the phases** — the part of the period that imparts the transferable
skill. The **LO is the bridge** between that skill and the item that tests its transfer, so she must
read the LO **first**, immediately before the item. 3b is therefore the right and only place to air
it. Placement rules (locked against the audit):

- **Per item, above the stem — never one LO in the header.** The audit confirms the LO lives at the
  level of the **assessment item** for every subject except Maths middle/prep, and the normalizer
  contract is per-item (`item.meta.linked_lo`). A single 3b view can hold **multiple items resolving
  to one period**, and those items may test **different LOs** (A/B/C and intent tiers re-test a
  section). So the LO is aired as a labelled `LEARNING OUTCOME` line at the **top of each item card,
  directly above that item's stem** — reading order LO → item, per item. A single header LO line
  would mislabel any view whose items differ.
- **Header carries only a unit framer**, e.g. "Checks whether the class can transfer what this period
  built" — context, not a per-item LO claim.
- **Maths middle & preparatory have no LO** (resolver rows 4–5: structural link only; `linked_lo =
  null`). There the LO line is **absent, not blank** — no empty "LEARNING OUTCOME" label, no
  placeholder. Renderer branch is **intended**, not a bug. Maths **secondary** does carry an LO
  (row 6) and shows the line like every other subject. English airs the LO from the handoff cell
  (`source_lo`, row 7) — still per item.

(Mockup: `planning-layer-mockups/index.html` Screen 3b shows both cases — the Science view with a
per-item LO above each stem, the items deliberately carrying two different LOs to prove the per-item
placement; and a Maths middle/prep view with the line absent.)

**Rationalized Screen-3 controls** (clutter removed): the move button drops the section name —
"**Move to Period N+1**" (she knows she's in 6A; naming it is redundant), alongside "**Stay on
Period N**", a quiet "**Assessment here**" affordance (opens Screen 3b), and "**Stop tracking**".

### Tracking (when assessment tracking is taken up)

If tracked at all: **competency/LO coverage only** ("which LOs/competencies have been assessed"
— feeds NCF/school-ICP compliance evidence), **never student marks or grades** (gradebook = ERP
line, permanently out of scope). Most of v1 can surface items read-only (view/pull-up at the
anchor period + full set on the chapter-org page); item-bank *assembly* is a deferred enhancement.

### Constitution fix already applied + owed

- **SS middle assessment (done this session):** Rule 4 changed from "minimum / uncapped" to
  **exact** per-weight counts (Central = exactly 2 MCQ + 1 SCR + 1 ECR + 1 Open Task, etc.),
  removing the loophole that produced 6 MCQs on one Central competency. Runtime mirror only.
- **Owed at generation:** audit the *other* subjects' assessment constitutions for the same
  minimum/uncapped loophole and apply exact counts where intended (see §J).

## J. Owed at the generation milestone (nothing owed now)

For now, building/testing on fixtures needs **no constitution change** — only a by-hand,
arithmetic-only amendment of saved-plan phases from ranges to absolute minutes (`end − start`;
flag anything that won't convert, change no content, no re-ordering). Owed only when generation
is wired — and **both apply across the board, to every subject's LP constitution + prompt
(Science, English, Social Sciences, Mathematics, TWAU; all stages)**, not to one subject:

1. **Phase notation** — every LP constitution's phase/time-band output changes from time *ranges*
   to *absolute minutes per phase* (summing to the period total). Across all subjects.
2. **Input contract / prompt wording** — every LP constitution/prompt changes the teacher input
   from an *ordered* period schedule to a **gross budget** ({duration, count} totals as hard
   constraints), and the AI orders periods by pedagogy. Strip any "in that order" / serial-order
   phrasing from every prompt wrapper. The time change is a **pure relaxation** (one fewer
   constraint) — it touches **no binding rule** in any constitution; only duration *ordering* is
   freed, while content order (textbook sequence, competency coverage) is untouched. SS already
   budgets time as a quantity, so for it this is mostly prompt wording; subjects whose wrappers
   carry explicit order language (e.g. English) need that phrasing removed.
3. **Assessment exact-counts audit** (§I-ter) — SS-middle was fixed this session (min/uncapped →
   exact per-weight counts). Audit every *other* subject's assessment constitution for the same
   "minimum / uncapped" loophole and apply exact counts where a fixed item set is intended, so
   re-generation does not reproduce the over-generation (e.g. 6 MCQs on one Central competency).
