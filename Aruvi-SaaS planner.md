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
