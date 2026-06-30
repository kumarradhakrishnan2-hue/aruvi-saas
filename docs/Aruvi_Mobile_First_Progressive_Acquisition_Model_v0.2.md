# Aruvi Mobile-First Progressive Acquisition Model (Draft v0.2)

## Background

The earlier Aruvi design assumed that teachers would first create a reasonably complete teaching profile before deriving the full benefit of the platform.

Although architecturally sound, this places significant cognitive effort before the teacher experiences value. Conversations conducted using the "Frustrated Teacher" persona revealed that teachers are not opposed to providing information; they resist being asked for information before they understand why it is needed.

The redesign therefore does not simplify Aruvi's capabilities. Instead, it changes when information is requested.

The platform remains rich internally while appearing cognitively light externally.

Core Design Principle

Aruvi should reveal only what is needed to help the teacher succeed in her very next teaching moment. Every additional capability and every additional piece of information should emerge only when it immediately makes the teacher's work easier.

A consequence of this principle is that the teacher should almost never feel she is "building a profile."

Instead, the profile should emerge naturally as a by-product of useful work.

Strategic Shift

## Earlier philosophy

## Profile

##     ↓

## Allocation

##     ↓

## Generation

##     ↓

## Tracking

## Proposed philosophy

## Generate first lesson

##       ↓

## Teach the lesson to one or more sections

##       ↓

Weekly arrangement

##       ↓

## Begin teaching

##       ↓

## Remember progress

##       ↓

## Expand profile naturally

Exactly the same destination.

A fundamentally different journey.

Design Objectives

The redesign seeks to achieve four objectives simultaneously.

Allow first-time users to generate value almost immediately.

Progressively build a teacher profile without explicit onboarding burden.

Transition the teacher from "lesson generator" to "teacher workspace."

Reuse as much of the existing Aruvi architecture as possible.

No major re-engineering of the deterministic planning engine is envisaged.

The proposal primarily changes the interaction sequence.

Navigation & Information Architecture

Mobile-first Philosophy

The entire user experience will now be designed mobile-first, with the assumption that teachers interact with Aruvi primarily during the school day using a vertically held phone.

The desktop version remains important, but only as a larger rendering of the same mobile interaction model, not as the primary design target.

## In other words:

Mobile drives the product design.

Desktop adapts the mobile experience for larger screens.

Landscape interaction is not a design target.

Every workflow should comfortably operate with one-handed vertical mobile usage.

This is a deliberate reversal from traditional web-first applications.

Two Product Phases

Phase 1 – Guided First Experience

## Until the teacher has

## generated the first lesson,

## associated it with one or more sections,

## completed (or skipped) weekly arrangement,

there is no application shell.

No sidebar.

No navigation.

No tabs.

The teacher simply completes one meaningful task.

Phase 2 – Workspace

Once the first lesson enters the teacher's teaching workspace, the application opens into its normal navigation model.

This is considered Aruvi's activation moment.

Home Screen

There is no separate Home page.

The My Week screen becomes Home.

Every time the teacher opens Aruvi she lands directly here.

## Its purpose is to answer one question:

## What is immediately relevant to me?

Sidebar

Navigation is accessed through the hamburger menu.

## Suggested structure

☰

My Class

Calendar

Lesson Plans

## Settings

## Help & Support

"My Week" does not appear because it is already Home.

Closing the sidebar always returns to Home.

My Class

My Class becomes the teacher's progressively growing profile.

Rather than being completed upfront, it accumulates information naturally.

Examples include:

## Subject

## Grade

## Sections

## Duration

## Annual Budget

## Teaching Week

Completed information is prefilled.

Missing information can be completed or edited at any time.

Calendar

The Calendar is available from the beginning.

If insufficient information exists, it does not appear empty.

Instead it explains the benefit.

Example:

Arrange your teaching week once and Aruvi will automatically bring the right lessons before each class.

## Throughout the redesign the principle remains:

Benefit first. Data second.

Lesson Plans

Lesson Plans becomes the repository.

## It answers

## What lesson plans have I created?

It is no longer the teacher's daily execution screen.

Prepare Lesson

The Generate tab disappears.

Generation is no longer treated as a destination.

## Instead it becomes a universal action

## + Prepare Lesson

available wherever appropriate inside the application.

Internally the lesson generation engine remains unchanged.

First Launch

## (Login discussions excluded.)

Immediately after login Aruvi asks only one question.

## What would you like to teach?

## Not

## "What do you teach?"

The distinction is intentional.

The teacher is beginning a task rather than creating an identity.

Step 1 — Subject (Picture 1)

The teacher selects one subject only.

A three-step progress indicator appears at the top of the screen.

This reassures the teacher that only three basic pieces of information are required before the first lesson can be generated.

No attempt is made to gather every subject taught.

The objective is simply to complete one useful task.

Additional subjects naturally become part of the profile through future usage.

Step 2 — Grade (Picture 2)

Teacher selects one grade only.

## Current wording under consideration:

## Which grade do you want to teach Science to?

Only one grade is requested.

Additional grades naturally emerge through future lesson generation.

Step 3 — Chapter Selection (Picture 3)

Teacher selects the chapter.

At this stage Aruvi introduces sensible starting points.

## 40-minute classes

## 12 teaching periods

These are presented as starting points, not authoritative assumptions.

Teacher may continue immediately.

## Or choose

## Want to change?

Optional Customization

## If "Want to change?" is selected

## (existing duration screen reused)

## Teacher may

## modify class duration

## modify estimated teaching periods

## or

provide annual teaching budget to receive Aruvi recommendations.

This captures richer information only from teachers wishing to customize.

Lesson Generation

Generation proceeds exactly as in the current architecture.

No major changes.

## Profile now quietly contains

## Subject

## Grade

## Duration (default or modified)

## Annual Budget (if supplied)

No explicit profile workflow has occurred.

Associate Lesson with Classes (Picture 4)

The existing lesson preview opens.

## Immediately afterwards Aruvi displays

✓ Your lesson plan is ready.

Teach the lesson to your class.

A default section appears.

## VI A

## Alongside it is

## Change section

Selecting this opens a multiple-selection section picker containing all available sections.

The teacher simply ticks the sections that will use this lesson.

Example

## ☑ VI A

## ☑ VI B

## ☑ VI C

Once confirmed, Aruvi creates an independent lesson card for each selected section.

Section information is quietly added to the teacher's profile.

## The teacher is never explicitly asked to "create tracking."

Instead she simply tells Aruvi which classes will use the lesson.

Transition into Workspace

Once section cards have been created, the teacher enters Aruvi's workspace for the first time.

This is considered the activation moment of the product.

Instead of remaining inside generation, the teacher now sees independent section cards.

Example

## VI A

## Exploring Magnets

## Ready to teach

------------------

## VI B

## Exploring Magnets

## Ready to teach

------------------

## VI C

## Exploring Magnets

## Ready to teach

Section names become the primary visual identity.

First-Time Guidance

Opening a lesson card for the first time may display lightweight guided overlays introducing

Lesson Pointer

## Continue / Move Next

## Resources

## Assessment

## Notes

Existing functionality is reused.

Only the entry point changes.

Weekly Arrangement

Immediately after section cards have been created, Aruvi introduces weekly organization.

## Prompt

Would you like Aruvi to show the lesson cards on the right day?

## Supporting text

It will help you see only what is relevant immediately.

## Buttons

## Arrange my week

## Later

## Week Arrangement Screen (Picture 5)

Simple recurring weekday model.

No dates.

No timetable.

## Teacher taps

## Monday

## ↓

## Chooses sections

## ☑ VI A

## ☑ VI C

## Tuesday

## ↓

## Chooses sections

and so on.

The objective is not calendar management.

It is attention management.

Home Screen Behaviour

## Once weekday mapping exists,

Aruvi automatically opens to the current weekday.

Example

## Monday

## Today's Lessons

## VI A

## Exploring Magnets

## Learning Unit 3

## Ready

----------------

## VI C

## Matter

## Learning Unit 2

Tuesday automatically surfaces Tuesday's lessons.

Remaining weekdays remain collapsed.

No dates are required.

The existing lesson pointer architecture remains unchanged.

Calendar

Calendar remains available from the sidebar.

## If insufficient information exists,

## instead of an empty screen,

## Aruvi explains

## what additional information is required, and

what benefit the teacher receives.

## The principle remains

Benefit before data.

Lesson Plans

"My Lesson Plans" continues using the existing functionality.

The only difference is that lesson plans naturally arrive there after first becoming part of the teacher's section workspace.

The repository therefore feels like a consequence of teaching rather than the starting point.

Development Philosophy

This redesign deliberately avoids rewriting Aruvi.

Instead it reorders existing capabilities.

## Existing functionality expected to be reused includes

Lesson generation pipeline

Lesson preview

Lesson cards

Lesson pointer

## Tracking

## Assessment

My Lesson Plans

## Duration editor

## Profile management

## Deterministic planning engine

## The primary redesign effort lies in

## onboarding,

## progressive profile acquisition,

## navigation,

first-time workspace transition.

Overall Vision

The destination remains unchanged.

## Aruvi ultimately becomes

## a complete teacher profile,

## section-wise lesson tracking,

## lesson repository,

## weekly teaching workspace,

planning system.

The difference is that teachers arrive there through successive moments of value rather than through an initial configuration exercise.

Rather than asking teachers to configure Aruvi before using it, Aruvi gradually learns about their teaching through useful interactions.

The end state is therefore identical.

Only the journey changes.