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
newest, peek either in the read-only reader right there). My Plans keeps a "Make this active"
control, but it is the **library** (read / compare / see what exists), not the operating surface
— operating (choose version, start) happens where she already is. Switching version is only
possible **before start**; after start the version locks for that section's chapter.

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

- **Read-only, from My Plans (unstarted plan, no pointer).** Tapping a saved plan opens the
  chapter-org reader read-only — she can drill to and read any period in full, but there are
  **no pointer controls anywhere** (no stay/move), because the chapter hasn't started. This is
  the **only door to read an unstarted plan on screen** — including a freshly generated
  not-yet-active version she wants to review before committing. (Resolves the otherwise-missing
  "where does she view it?" gap: dashboard shows a plain row, the slot view doesn't exist yet,
  so My Plans → Preview is the entry point.)
- **Default on first start (pointer just created)** and **recede-to-link during execution
  (pointer live)** — the two altitudes below.

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
5. **Start declaration card** — what an unstarted slot shows: "Which chapter are you starting?"
   listing that grade/subject's saved plans; where a chapter has multiple versions, the version
   choice is offered **inline here** (default newest, peek in the read-only reader). The tap
   binds the chapter, creates the pointer, and locks the version.
6. **My Plans (the library)** — saved plans per grade/subject; marks the active version; never
   auto-deletes; no "stop tracking" here (that lives on the slot). **"Preview" opens the
   read-only chapter-org reader (§E), not any separate LP view.** "Make this active" is housekeeping
   only — the expected operating path is the slot start card (5), not this tab.

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
