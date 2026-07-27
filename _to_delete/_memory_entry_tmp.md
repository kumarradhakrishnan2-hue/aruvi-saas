## 2026-07-26 (newest) — THE CALIBRATED STANDARD IS NOW THE DEFAULT (first run was showing 12×40 for every chapter of every class)

**The report.** Founder: "the first time plan default was showing periods not in line with the
calibrated standard we created." Confirmed, and it was worse than a drift — first run was not
reading any period table at all.

**Two tables, silently disagreeing.** `data/content/allocation_norms/` holds both:

| | `ncf_period_norms.json` | `master_plan.json` (OUR calibration) |
|---|---|---|
| keyed by | subject · **stage** | subject · **class** |
| source | NCF adaptation (`NCF_adapted_for_Aruvi.xlsx`, 2026-07-01) | founder's `ncf_chapterwise_period_allocation.xlsx` → `genon/master_plan.py` (2026-07-24) |
| period length | **flat 40 min** everywhere (its own `_meta.unit`) | **class-banded: 40 ≤VII · 45 VIII · 50 IX** (`std_duration`) |
| per chapter | annual total ÷ effort weight, computed in the API | `recommended_periods`, precomputed by largest remainder |

They disagree, both ways: SS IX **245** calibrated vs **150** NCF (1.63×); TWAU preparatory **140**
vs **300** (0.47×). And they are not even in the same unit at secondary — 245×50 min against
150×40 min. The bands ARE the basis the certified canonicals were authored at: SS IX ch 5 is the
21×50 canonical, i.e. 1050 min.

**What first run actually did (the bug).** `FirstRun.jsx` shipped `DEFAULT_DURATION = 40` and
`DEFAULT_PERIODS = 12` as flat constants. `estimateFor()` existed, read `ncf_estimated_periods`
— and was **never called**: the 2026-07-08 "neutral flat default" decision had `pickChapter` and
its sibling effect both hard-set `DEFAULT_PERIODS`. So every chapter of every class opened at
12 periods × 40 min = **480 minutes**, against SS IX ch 5's canonical **1050**. The teacher was
being handed a default that contradicted the plan the very next tap would generate.

**The fix — master plan first, NCF norms only as fallback.** Founder call, all four choices:
switch everywhere (not just first run) · show BOTH figures on the budget screen · extend the
50-min band to class X.

- `api/data.py` — new `standard_duration_minutes(grade, subject=None)` (prefers the combo's own
  `standard_duration_minutes` so the JSON stays authoritative over the band table; falls back to
  the band, then 40), `master_annual_budget(subject, grade)`, `master_recommended_periods(subject,
  grade) → {chapter: periods}`. **Class X gets the 50-min band** (same secondary band as IX) even
  though it has no master-plan row — its period counts still fall through to the NCF norms until
  the workbook carries X's chapters.
- `api/main.py` `/chapters` — new `recommended_periods` + `recommended_source`
  (`"master_plan" | "ncf" | null`) per chapter, plus top-level `standard_duration_minutes` and
  `annual_budget_periods`. **`ncf_estimated_periods` is retained, computed exactly as before** —
  it is a published norm, not a bug; it just no longer drives anything.
- `api/main.py` `/ncf-periods` — now returns `recommended_total_periods` (calibrated budget,
  NCF as fallback), `recommended_source` and `standard_duration_minutes` alongside the unchanged
  `ncf_total_periods`. Endpoint name kept so nothing else had to move.
- `FirstRun.jsx` — `estimateFor` reads `recommended_periods` and **is wired in** (this reverses
  2026-07-08); duration seeds from `standard_duration_minutes` into new `stdDuration` state (the
  "recommended" tag can no longer compare against a constant); tag copy **"NCF recommended" →
  "Aruvi recommended"**, and the periods field gains the same live tag. The soft 5–25 sanity band
  is **suppressed while she sits ON the recommendation** — five calibrated chapters are genuinely
  below 5 periods (English III ch 5/10/14, English VI ch 16, Science VI ch 1) and warning her
  about a number Aruvi just proposed reads as a bug.
- `YearPlan.jsx` — budget fallback and per-chapter suggestion moved to `recommended_periods`.
- `TeachingProfile.jsx` — budget estimator reads both totals; the two duplicated sub-lines
  collapse into one `estimateSubLine()` helper, shared wording with FirstRun:
  *"(based on a 30-week year. Aruvi recommends 245 periods a year for this class (NCF norm: 150).)"*

**New test — `tests/test_calibrated_defaults.py`** (stdlib, passes on the real repo). Pins the
duration bands incl. X→50 and the unknown-grade fallback; pins **SS IX ch 5 = 21 periods × 50 min
= 1050**, matching the canonical; asserts per-chapter figures sum EXACTLY to the annual budget
(largest remainder, no drift); pins the science·preparatory double-empty fallback; and asserts the
two tables still differ — if they ever converge, the test says the fix is moot, not broken.

**STATIC + unit-verified only.** Python compiles, the new suite passes against real data, all
three JSX files babel-parse clean with default exports intact. Per §11 the sandbox can't
`next dev` — **live render + mobile (360×800 first) pass on the chapter step and both budget
screens is the immediate must-do.** Watch specifically: the "Aruvi recommended" tag on both
fields at 360px (two tags now, one per field), and the longer both-figures budget sub-line
wrapping.

**Open.** Class X has no chapter weights in the workbook, so X still falls back to NCF norms for
counts (duration is right). `Allocate.jsx`'s G4 "periods in total" input is still teacher-entered
and untouched by this — the 2026-07-01 follow-on is still open.

---

