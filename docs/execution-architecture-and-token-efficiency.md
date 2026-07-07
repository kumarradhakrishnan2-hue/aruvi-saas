# Aruvi SaaS — Execution Architecture & Token/Process Efficiency

Written 2026-07-07, revised same day after founder review. Documents the two-part
execution architecture, then the agreed efficiency decisions for scale. Companion to
`docs/architecture-plan.md` and `CLOUD_DATA_MODEL.md`.

---

## Part 1 — The architecture

Execution splits into two halves with different economics:

| | **A. Authoring pipeline** (offline) | **B. Runtime generation** (online) |
|---|---|---|
| Who runs it | Founder, in Cowork sessions | Teacher, via the web UI |
| Frequency | Once per chapter, ever | Per teacher · chapter · period profile |
| Cost model | Amortized across all future users | Marginal, per request |
| Output | Bucket A content (`data/content/`) | Bucket B state (plans, per tenant) |

### A. Authoring pipeline — the cowork prompts

Location: `cowork prompts/{subject}/{stage}/`. Per subject·stage:
`step_1_chapter_summary.md` reads a chapter PDF and writes the summary;
`step_2_competency_mapping.md` (or `effort_index.md`) reads summary + CG framework + the
mapping constitution and writes the mapping JSON carrying the chapter's allocation
weight. English combines both steps in one prompt.

Two properties matter. These sessions run inside Cowork's own context — no API call —
with the founder as human QA on every artifact. And the outputs are write-once,
read-forever: they become shared read-only content for every tenant. The expensive
cognition (reading a 30-page PDF, applying a constitution) happens exactly once per
chapter, ever.

### B. Runtime generation — UI → engine → LLM

```
teacher → Next.js (web/) → X-Aruvi-User → FastAPI (api/) → aruvi_core.engine.generate()
```

The engine is tiny and subject-agnostic:

1. Resolve the subject plugin from the registry.
2. The plugin builds the lesson-plan prompt: **system** = role framing + the LP
   constitution (~60–70 KB ≈ 15–18 K tokens, includes the output JSON schemas A3/A4),
   flagged cacheable; **user** = pedagogy document (~2 K tokens) + chapter summary +
   competency mapping + teacher's period profile.
3. LLM call (Sonnet) → JSON parse → validate → normalize to the canonical view model.
4. Same again for the assessment (system = assessment constitution; user = summary +
   lesson-plan handoff), with the link resolver tying items back to periods.
5. One `ViewModel` out; the React and export renderers consume it.

Allocate is LLM-free: it reads each chapter's pre-authored weight and distributes
periods deterministically. The `OutputCache` port is specced but not yet wired; live
generation is deferred (the API serves saved-plan previews today). Prototype baseline:
~₹23/chapter (vs ₹8 target), ~5 minutes for LP + assessment.

The essential shape: everything static is pre-computed offline by Part A; the runtime
call only pays for the per-request combination (this teacher's profile × this chapter)
plus the two model outputs.

---

## Part 2 — Efficiency decisions for scale

The two-part split is the right shape and stays. The decisions below extract its value.

### 2.1 Cache the static prompt prefix

Restructure prompts so everything static per subject·stage — constitution + pedagogy —
sits in one cached block. Today only the constitution is flagged; the pedagogy document
sits at the top of the user block and is re-billed at full rate every call. (The output
JSON schemas already live inside the constitution, so pedagogy is the only gap.)

Pricing: a 1-hour cache write costs 2× base input on the cached prefix; reads cost 0.1×
— break-even after one reuse, then ~90 % off. The ~20 K static tokens drop to ~2 K
effective on every hit, and this prefix is shared by every generation in that
subject·stage.

A second, per-chapter cache block (summary + mapping) is **deferred**: teacher pacing is
unsynchronized, so same-chapter repeats within the 1-hour TTL will be rare and every miss
pays the 2× write. Log would-have-hits via token telemetry and revisit with ~6 months of
usage data.

### 2.2 Pre-warm the output cache for the default profile

First-run defaults to 40 min / NCF-estimated periods — the majority profile by
construction. The full catalogue is ~400 chapter-plans. Generate them all once, offline,
and seed the output cache: the modal first-time teacher gets an instant plan, and the
₹23 is paid once per chapter instead of once per teacher. This converts runtime cost
from per-teacher to per-chapter for the common path — the same amortization Part A
already made for summaries and mappings.

Execution: run the one-time build as scripted Claude Code sessions under the founder's
Max subscription (zero marginal cost; sessions must reproduce the engine's exact prompt
and certified model, and outputs must pass the same validate/normalize path; subscription
rate limits spread the build over days). Use the Batch API (50 % price) for later re-runs.
Never proxy the subscription token as an API key.

**Cache key rules.** Normalize the key, never the teacher's input: round durations to
5-min bands, sort period types, ignore names. Profiles can carry several duration types —
the key is the full set of rounded durations with per-type counts, and a cached plan is
usable only when **every** rounded duration matches; partial overlap is a miss. On a
cross-duration hit (42-min teacher, 40-min cached plan), phase minutes are **rescaled
deterministically** to her actual duration (proportional split, largest-remainder so they
sum exactly) — pure post-processing, no regeneration. A miss generates with her real
values.

**Cached plans are served whole.** Assessment generation is deferred by default only on
first-time live generation (the teacher gets the LP fast and opts in to the assessment) —
that deferment exists to hide latency, and a cache hit has none. Any cached plan is
served complete, LP + assessment, no opt-in step. So the pre-warm build generates both
artifacts, and an opted-in assessment is written back to the cache for the next teacher.

### 2.3 Reduce output tokens (the latency lever)

Latency and most of the cost sit in output tokens, which input caching does not touch.
Audit saved plans for echoed input — restated competency descriptions, repeated chapter
context — and have the constitution forbid it; every echoed token costs money and
seconds. Together with assessment deferment (2.2), this is the whole latency plan for
the live path; the cache serves the rest instantly.

### 2.4 Content changes — two kinds, two treatments

**Structural changes** (the JSON contract: summary/mapping shape or the LP/assessment
schema — e.g. phase timing format, or adding a `short_summary` field): significant
downstream impact including UI, but handled by **edition works** — a migration/enrichment
script edits saved plans and cache entries in place. No dump, no regeneration.

**Qualitative changes** (pedagogical rules in the cowork prompts or constitutions): these
cannot be edited into existing plans — the affected cache slice is **dumped and
regenerated**. Amendments land per subject·stage, so the ring-fence is scoped and managed
manually. Hard rule: from day 1 of an amendment, every new serving in the scoped part of
the curriculum reflects it.

**Edition tag.** Stamp every cached and saved plan with a plain edition label at write
time (e.g. `"edition": "science-middle-2026-07"`). It makes the day-1 rule auditable
(finding stragglers is a query) and tells edition works which shape each saved plan is in.

### 2.5 No vector store in the generation path

Every runtime read is a deterministic keyed lookup (subject/grade/chapter → summary +
mapping) — object storage or Postgres is cheaper, simpler, and exactly correct. Semantic
retrieval earns its keep only in Ask Aruvi (free-form Q&A); scope any vector store there.

---

## Summary

Part A amortizes comprehension cost to zero per user; these decisions make Part B do the
same for generation. With the static prefix cached (2.1), the default-profile catalogue
pre-warmed and served whole (2.2), and output tightened (2.3), the marginal cost of the
modal teacher's first plan approaches a cache read, and ₹23/chapter should fall below the
₹8 target for the common path. Edition-tagged content handling (2.4) and keeping vectors
out of the generation path (2.5) keep it that way as content and tenancy grow.
