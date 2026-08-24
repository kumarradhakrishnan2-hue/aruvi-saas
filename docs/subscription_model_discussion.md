# Aruvi — Subscription Model Discussion (working record)

**Date:** 2026-08-22. **Status:** working hypotheses, deliberately not final. This record
exists so the next pricing conversation starts from here, not from zero. Read before any
work on entitlement UI, pricing pages, or the partner brief's billing sections. Companion:
`docs/administrative_architecture.md` §5 Step 5 (the entitlement seam this feeds).

---

## ★ 0. THE CURRENT MODEL (founder, 2026-08-22 second session) — supersedes §5's
## price-anchor hypothesis; §§1–4 and 6–7 below still stand as analysis

**Billing unit: one teacher × one SUBJECT-STAGE** (e.g. Social Science–Middle; 11 combos
exist, matching the library's structure), **unlimited serves within scope** — a quota
would create anxiety with no economic basis (serving is selection from a cached library,
marginal cost ≈ 0). Working figure ₹500/yr per subject-stage; the number stays empirical
(the §7 test) and lives in config, never code. A two-subject teacher buys two.

**Channel split IS the price fence: Individual = MOBILE APP ONLY · Enterprise = website.**
No individual web product. This protects the enterprise tier without inflating individual
price. Consequence, accepted deliberately: the Expo/mobile app moves up the roadmap —
individual monetization ships with it.

**Enterprise (T-teacher school):** near-equal per-teacher economics, on purpose. The
T>11 arbitrage (11 personal mobile subscriptions covering all subject-stages, plans
shared) is real and cannot be priced away — even at equal pricing 11×P beats T×P. The
pull that breaks it is FEATURES, not price: (1) website access (schools want the computer
centre — control + consistency), (2) whole-school curriculum alignment, (3) the admin
dashboard — tracker view per teacher/section, period allocation at CHAPTER granularity.
"A fair conversation for negotiations. Clear reason." The admin/monitoring layer is also
the enterprise renewal engine.

**Trial: all 11 subject-stages open · capped at ANY 3 CHAPTERS · unlimited re-serves per
chapter · NO time limit.** The cap counts chapters, never serves: her initial struggle is
period allocation — "can I teach this chapter in 10 periods rather than 15?" — and she
needs 3–4 attempts per chapter to learn the time-fitting, which is the product's core
value. (`already_yours` re-serves never decrement.) Breadth exposure happens HERE, in
trial — she sees everything Aruvi covers and can show colleagues.

**Two different after-states, deliberately asymmetric ("the unfairness is fair"):**
- **Trial exhausted (never paid):** keeps her 3 chapters — viewing, export, print,
  archive, AND the tracker on them. Locked: new generation. Rationale: she has 3 chapters
  in her pocket and 2 months of teaching ahead; the experience of actually applying the
  LP to track sections is the hook that brings her back to pay — LP quality alone is a
  weaker, non-collective hook.
- **Lapsed (paid, chose not to renew):** keeps what is hers — her plans: view, export,
  print, archive. Loses what is Aruvi's — the productivity/tracking tools, and
  generation. She has already experienced everything; if the productivity gain felt worth
  the money she renews for it; if not, she keeps her property and lets go what was never
  hers. **This AMENDS admin architecture §2.5** ("export and delete only") — see actions.

**Why renewal works despite stable textbooks:** cutover and subscription are independent
clocks. Teachers seldom decide, months ahead, the periods chapter 9 will get — an LP
generated in advance holds little correspondence to the time actually available when the
chapter arrives. A running subscription is peace of mind: generate anytime, iterating
periods against what is already allocated and what remains, no hurry to archive. The
renewal proposition is the LIVING fit to her time (plus the year's re-versioned library),
not access to old files.

**The "+" boundary (gating at ADD time, not generate time):** the paid teacher's choosers
show ONLY her scope — an SS-Middle teacher sees one subject (no dropdown) and three
classes; simple, unclogged. Attempting to expand the profile beyond scope is the ONE
upsell moment: an honest "this is a separate subscription" message at a moment she
initiated (pull, never push — the standing no-nudge rule). Never allow add-now-pay-at-
generate: "why did you let me add it if I had to pay?" is cognitive dissonance, and
unpaid subjects would clog every dropdown.

### Action points

> Progress 2026-08-24: **1 DONE** (§2.5 amended in place) · **2 DONE** (Step 5 built —
> ports, file adapter, ManualBillingProvider, CLI, gate in genon_make_plan, GET
> /entitlement, enforcement flag default OFF, test_entitlement.py green) · 3–6 open
> (3 = Step 6 surfaces + Expo promotion; 5 = the 20-teacher test).

1. **Amend `docs/administrative_architecture.md` §2.5**: lapsed = plans retained
   (view/export/print/archive) + generation and productivity tools locked; export and
   account-deletion remain always reachable. Trial-exhausted additionally keeps the
   tracker on her existing chapters. (Step 4's erase/export are unaffected.)
2. **Step 5 seam shape** (build when resumed): `Entitlement` gains `scopes:
   [subject/stage]`; trial is COUNTER-based (`chapters_used` of 3, `already_yours`
   re-serves free) with no expiry date; `require_entitlement(subject, grade)` resolves
   grade→stage and checks scope; gate sits ONLY in front of generation; `source`
   (ios/android/web) carries the channel fence. ManualBillingProvider + founder CLI
   unchanged in spirit.
3. **Roadmap consequence**: mobile app (Expo) is promoted — it is now the individual
   PRODUCT, not a port. Enterprise web = current app + future admin dashboard (tracker
   view + chapter-level allocation view) — that dashboard is the enterprise renewal
   engine and a Step-6-adjacent build.
4. **"+" / TeachingProfile**: scope-filtered choosers for paid users; the out-of-scope
   upsell screen designed once, used only at profile-expansion moments. Trial mode shows
   all 11.
5. **Pricing number**: ₹500/subject-stage/yr is the working figure; confirm via the §7
   20-teacher test (measure week-2 pointer return + the time-fitting reaction, then
   willingness-to-pay).
6. **Language**: cap and copy speak in CHAPTERS, never "generations" (§3 compression
   risk); public claims stay "NCF 2023 aligned" (§6).

---

## 1. What is settled (build-time facts, independent of price)

- **Subscription shape:** individual · annual · ROLLING (not academic-year aligned) —
  admin architecture §2.5, already decided. Oct 2026 purchase runs to Oct 2027, covering
  the next planning season. No monthly plan: teacher planning is seasonal (Mar–Jun), and
  monthly invites subscribe-plan-cancel around exactly that peak.
- **Lapsed = export and delete only.** No read-only tier. Data rights never gate (§2.5,
  built in Step 4).
- **Entitlement is per TENANT, resolved server-side, platform-tagged** (`source`:
  trial | manual | web | ios | android). A school later pays once for many teachers with
  no schema change. iOS must be priced/steered around Apple's 15–30% cut — this is why
  the seam exists before any gateway is chosen.
- **The seam is price-agnostic.** `plan_id` + `valid_until` are data; the ₹ figure lives
  in config, never in code. Step 5 can be built now regardless of where pricing lands.
- **Doctrine (founder, 2026-08-22): selection, never generation, at the teacher surface.**
  LLM transformation on top of a certified authored artifact is negative value-add — it
  debases the thing being sold. Adaptation offers ("Tamil-medium support", "activity-
  oriented") that mean re-generation are rejected. This also decided against a
  section-picker feature in-product (duplicates ChapterOrg, fights the pointer, no
  uniform section axis across subjects) — its valid form is a PRE-TRUST shop window /
  shareable single-section teaser, sequenced after the pricing test.

## 2. Market scan (2026-08, web)

Two price universes plus a free floor:

| Segment | Product | Price | ≈ INR/yr |
|---|---|---|---|
| Global AI teacher tools | MagicSchool Plus | $99.96/yr | ~8,800 |
| | Brisk Educator Pro | $99.99/yr | ~8,800 |
| | Diffit | $14.99/mo | ~15,800 |
| | Eduaide Pro | $49.99/yr | ~4,400 |
| | Khanmigo (teacher) | FREE (Microsoft-funded) | — |
| Pure planners (no AI) | Planbook / PlanbookEdu / Chalk | $20 / $30 / ~$99 /yr | — |
| India-priced | Twinkl India | ₹399/mo · ₹249/mo annual | 2,988 |
| | TeachBetter.ai | ₹149/mo | ~1,788 |
| | IndiaSchool.ai | ₹500/mo · ₹5,000/yr | 5,000 |
| | Teachmint (B2B ERP) | ~$5/user/yr, school pays | — |

Readings: the Indian self-paying teacher's demonstrated band is **₹1,500–5,000/yr**
(Twinkl's ₹2,988 the strongest signal — a mass Indian teacher audience pays it for
CONTENT). Organization-only planners command $20–30 — structure alone is nearly
worthless. Generic AI generation is commoditizing toward free (Khanmigo). Aruvi's serve
economics (cached certified libraries, near-zero marginal cost) support content-like
pricing without per-generation margin erosion.

## 3. The devil's-advocate critique, and where it landed

A strong outside critique was worked through in full. Its points and their dispositions:

- **"The market will compress Aruvi to 'a lesson planner', which is commoditized."**
  Accepted as the CENTRAL RISK — but diagnosed as a communication problem, not a product
  gap: the critique's own proposed fix (Plan → Teach → Check → Reflect as a workflow) is
  a description of what Aruvi already is (allocation · pointer/notes/phases ·
  unit-anchored assessments · completion state). The landing surface must demonstrate
  the YEAR, not the plan.
- **"High value × low frequency (June-only) is bad subscription economics."** Rejected
  as a description of the product — the calendar purge, cumulative pointer, "where did
  I stop?", mark-complete and after-class notes make Aruvi a period-by-period daily
  companion by design. BUT accepted as the thing to MEASURE: if the teach-loop doesn't
  land in practice, the objection becomes true.
- **"The real competitor is ₹0: ChatGPT + Google + WhatsApp groups + free NCERT-mapped
  PDFs."** Accepted fully. Confirmed concretely by the NCERT competitive scan (§4).
- **"The canonical library is invisible to the customer."** Accepted. Architecture is
  the cost story, never the buying story. Never market "certified" (see §6).
- **"Maybe the buyer is the school, not the teacher."** Half-accepted: the school's
  problem (consistency across 40 classrooms, curriculum execution) is a real and
  differently-shaped willingness to pay, and Step 0's tenant/user split keeps that tier
  structurally cheap. But individual-first stands: schools are a slow sales cycle and a
  different surface; individuals are how Aruvi learns fast. Every entitlement decision
  stays school-compatible (tenant-keyed).
- **"Full-year planning is not a moat — competitors can add curriculum maps."** The
  moat is not the feature claim; it is ~340 chapters of authored, calibrated,
  per-duration certified libraries across five subjects, re-versioned annually — content
  labor that compounds. It communicates only as EXPERIENCED coherence, never as claims.
- **Best line, adopted as the launch framing:** *"Aruvi — your complete academic-year
  teaching plan."* Never "AI lesson planner".

## 4. NCERT competitive field review (founder, first-hand)

Sites that map NCERT content exist — tickLinks (~9,500 free chapter-mapped LPs, Hindi,
state boards), Educart (free chapter PDFs), CBSE's own TERMs/sample plans, myCBSEguide
(student side), IndiaSchool.ai (learning-oriented). Founder reviewed each. Verdict:

> All clogged with content of all sorts. Not clear how a teacher lands there when she has
> the NCERT book. None aid her planning per se. None give her control over the time on
> her hand. None easily export a full plan to her time period. None have a hand-held app
> that is simple to use.

Flipped, these five negatives ARE the positioning, and each is an already-built decision:
land from the book (subject → class → chapter, first run's three steps) · state your time
and the plan fits it (period rows + calibrated defaults + budget) · export whole at her
matrix (PDF/DOCX) · one-handed phone app (mobile-first target). **Category: not a content
library, not an AI toolbox — THE PLAN FITTED TO HER TIME.**

Standing caution: "none aid planning" has two readings — whitespace (everyone missed the
job) or absent demand (the market drifted to content dumps because that is what got
used). Only the field test distinguishes them.

## 5. Working hypotheses — ★ SUPERSEDED by §0 (kept as history)

- **Price anchor: ₹1,999/yr** (`individual_annual`), framed ~₹165/mo, "less than one
  guidebook". Sits above TeachBetter (substance signal), below IndiaSchool.ai, beside
  Twinkl. Possible ₹1,499 founding/launch price.
- **Trial: 30 days, full product, auto on first account** — benefit-first demands she
  reach a real lesson before any wall. (Not yet founder-confirmed — was the open
  question when the Step 5 build paused for this discussion.)
- **School tier: later**, per-teacher discounted, enabled by the existing tenant split.
- **Landing line:** "Your complete academic-year teaching plan, fitted to the time you
  actually have."

## 6. Language rules (checked in-repo 2026-08-22)

- The ONLY public alignment claim is **"NCF 2023 aligned"** (topbar + both export
  headers). "Certified"/"NCF certified" appears NOWHERE teacher-facing and must not —
  no body certifies against NCF; "certified" is internal engine vocabulary (certified
  canonical libraries) and stays behind the curtain, like "canonical" (testing.md C13).
- Ask Aruvi's four "certification" mentions are the opposite sense (assessments are
  formative, NOT certification instruments) — correct, keep.
- Acceptable marketing forms: "NCF 2023 aligned" · "calibrated to NCF norms" · "built on
  the National Curriculum Framework".

## 7. The decisive experiment (before any price is public)

**The 20-teacher test.** Script: "Give me your class, subject and number of periods —
I'll give you your complete teaching plan for the year." Book → class → chapter → HER
periods → whole plan on her phone → export. Never mention architecture.

Measure, in order of importance:
1. **Return frequency in week 2+** — do they come back to tap the pointer? (Kills or
   confirms the frequency objection; first reactions do not count.)
2. **The time-fitting moment** — "I have 36 periods, not 42" → plan adjusts → reaction.
   (Tests whether time-control is the landing value, per §4.)
3. Willingness-to-pay asked ONLY after two weeks of use, never on day one.

If the reaction is "this saves me weeks" → ₹1,999 may be cheap. If it is "nice, but
ChatGPT can do this" → the price (or the demo) is wrong. The existing testing-campaign
infrastructure (`data/testing/`, docs/testing.md) is the vehicle.

## 8. Immediate consequences for the build

- **Step 5 proceeds price-agnostic** (it always was): `Entitlement` + repository
  (tenant-keyed) + `ManualBillingProvider` + one `require_entitlement` in front of
  generation only. Open founder decisions when the build resumes: auto-trial yes/no +
  length · enforcement flag default (off in dev?) · founder tooling (CLI script vs
  admin route).
- Step 6 (UI) later carries: subscription state, manage-subscription (deep-link rule on
  iOS), export/erase buttons, and the pricing page whose copy follows §4/§5.
- The single-section shareable teaser (§1 doctrine note) parks on the idea list until
  after the test.
