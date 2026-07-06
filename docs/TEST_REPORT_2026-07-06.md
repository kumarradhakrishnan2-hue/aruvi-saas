# Aruvi SaaS — Autonomous Test Report

**Date:** 2026-07-06 · **Method:** Claude in Chrome driving the live local app
(`localhost:3000` + API `:8000`), plus direct API probes. **Effective viewport:** ~304px CSS
width throughout (below the 360 target — a stricter mobile stress test), window nominally
360×800. **Test users:** `test_fr1` (left intact for review), `test_fr2`, `test_alloc`,
`test_iso_a/b` (cleaned up). No real user data (`Kumar1`, `kumar23`, `kumar3`) was modified.

**Bottom line:** The core product loops — guided first run, activation, the 12-step tour, attach
→ teach → complete, pointer persistence & cross-device reconcile, My Lessons + archive, teaching
profile edits, and tenant isolation — all work correctly. Two findings deserve attention: the
entire multi-step **Allocate UI is dead/unreachable code**, and the **"+" profile portal exits to
the wrong screen** vs. the CLAUDE.md §0 spec. No blockers or crashes were found.

---

## A. Confirmed defects / divergences

### A1 — Multi-step Allocate flow is dead code (Major – product-scope)
`web/app/components/Allocate.jsx` (991 lines: periods → select → adjust → final → generate spoke,
Δ-balance editing, PDF/DOCX export buttons) is **never imported or rendered anywhere**
(`grep "import Allocate"` → no matches; `GenerateTab` renders only `PrepareLesson`). Consequences:
- The top-down annual allocator and its **PDF/DOCX allocation-report export have no UI entry
  point**, even though CLAUDE.md §9 lists the allocation-report export under "Done."
- The engine + API still work: `POST /subjects/science/viii/allocate` returned a correct
  effort-weighted split (ch1 = 8×40+3×60 = 11; ch5 = 22×40+7×60 = 29; totals reconcile), and
  `export-pdf` / `export-docx` returned 200 with valid files (PDF 6.3 KB, DOCX 39 KB).
- **Suspected defect #1 is therefore latent only:** the `grids[]`-based `annualBudgetPeriods()` /
  `weeklyRatioFromReadiness()` in Allocate.jsx still read the all-`-1` grids (calendar purge) and
  never read `periods_per_week`/`ppw_by_duration`, so budgets/ratios would misbehave — **but no
  user can reach that code today.** If Allocate is ever re-wired, fix these first.
- Recommendation: either delete Allocate.jsx (like the other retired components) or, if the
  allocation report is still wanted, give it a real entry point and fix the grids reads.

### A2 — "+" profile portal exits to the profile accordion, not My Classes (Minor – spec divergence)
CLAUDE.md §0 states: *"A portal visit always exits to My Classes, never the profile accordion."*
Observed: from My Classes → standing **"+"** → chooser → **Section** → "Edit sections of Class 8"
(enrolled sections pre-ticked, manage mode ✓), then Back/Save both land on the **TeachingProfile
accordion** (`.tp` present, no `.sc-list`, neither centre tab active), not My Classes. The manage
flows end in `setScreen("view")` with `editFlow` still `"profile"`. Functional, but one screen off
from the documented "gliding path." Fix: after a portal-initiated action resolves, route back to
My Classes (`onBack`/`goClasses`) rather than the accordion.

### A3 — Un-namespaced localStorage leaks across users in a shared browser (Minor)
Several client keys are **not scoped by user ID**, so they carry over when a different teacher
signs in on the same browser. Observed live: while signed in as `test_fr1` (teaches Science VIII
only), `localStorage` held `mylessons_subject = English`, `mylessons_class = III` (left by
`test_fr2`), plus `allocations_english_*` and `expand_prompt_count_kumar23_*` /
`_kumar3_*` from prior real-user sessions.
- **My Lessons** is protected in practice: its derivation guard snapped the view to the enrolled
  Science profile (didn't strand on the stale English/III). Good defensive code — but the keys
  themselves still leak.
- **Allocation cache** (`allocations_{subject}_{grade}`, suspected defect #2): not user-scoped; the
  server register overrides on load, but a brief paint of another user's cached numbers is possible
  before the server responds. Low impact today (Allocate UI is unreachable, A1), but the pattern is
  the concern. Recommend namespacing all these keys by user ID (as `plus_portal_{user}` and the
  section keys already are).

### A4 — `/plans/{subject}/{grade}/{filename}/view` lacks the traversal guard its siblings have (Minor – hardening)
`plan-archive` / `plans-prepared` route filenames through `_plan_key()`, which rejects `/`, `\`,
`..` with **400**. The plan-view endpoint has no such guard; a `../../../etc/passwd` filename
returned **404** (safe in practice — file-not-found / JSON-parse failure, not a leak) but should
validate defensively and return 400 for consistency.

---

## B. UX frictions / minor observations

- **B1 (Minor, verify on-device):** the RollWheel ▲▼ arrow buttons use
  `scrollBy({behavior:"smooth"})`, which is suppressed while the tab renders in the background —
  the arrows then no-op. Drag/scroll always works. Because the arrows are the documented
  tap-friendly/phone affordance, confirm they respond on a real phone (and under reduced-motion),
  where smooth-scroll throttling can occur.
- **B2 (Minor):** on the first-run chapter step, the "Estimated periods" figure trails the chapter
  wheel by one settle cycle during fast scrolling (briefly showed ch3's 12 before settling on
  ch5's 24). It always converges to the correct value; a flash of the prior estimate is possible.
- **B3 (Minor):** the annual-budget number input accepts **0** (and clamps negatives to 0) with no
  lower-bound warning, so a 0-period teaching year can be saved. Probably acceptable (fill later),
  but a soft validation would prevent an empty budget.
- **B4 (Cosmetic):** FirstRun's subject wheel defaults to **English** (alphabetical first) while
  `page.jsx` elsewhere prefers Science — harmless inconsistency in the default landing item.
- **B5 (Latent, not user-facing):** the FirstRun preview "no saved plan at all" dead-end
  (disabled CTA, no Back) is **unreachable** with current data — every subject·grade has ≥1 saved
  plan, so a stand-in is always available. Keep in mind if content is ever pruned.
- **B6 (Known, out of scope):** re-confirmed the pre-existing Science IX ch_02 plan-data issue is
  not in scope here (MEMORY 2026-07-06 round-5); did not re-test.

---

## C. Works as designed (verified)

**First run (Pass 1–2):** login gate → FirstRun; subject/grade/chapter wheels; NCF period
defaults match the API per chapter (ch1=8, ch5=24 for Science VIII; full table cross-checked) and
the "NCF recommended" tag tracks the value; exact-match teaser (no stand-in) **and** stand-in
teaser (round-7 fix: names the actual deposited plan, `.fr-standin` notice shown); acquisition
rail Sections→Durations→Periods→Budget; multi-section fan-out → one card per section;
single- vs multi-duration ppw (wheel vs live table, inputs clamp ≥1); budget auto = 180 (6×30)
with NCF note "requires 240", other methods dim, CTA gated until a method is chosen; activation
persists the exact canonical payload (grids all `-1`, `ppw_by_duration {40:6}`, budget keyed by
grade index, sections 8A/8B), section-state cleared, plan flagged prepared; **refresh keeps the
shell** (server `ready` is the sole signal). Back-navigation preserves state; refresh mid-flow
returns to welcome with nothing persisted.

**Tour + teach loop (Pass 3):** nudge gate (shows unattached+prepared; retires on attach); full
**12-step tour** with real tab nav, preview at 4, popup at 6, **real attach at 6→7 (persists to
server)**, Back 7→6 unbinds cleanly, lesson open 8–9, **demo-complete 10–11 never touches the real
pointer/done**, gear ring at 12; attach via "+" (prepared-only, excludes bound); mark-complete
advances the pointer (local + server); **pointer persists across refresh** and is **restored from
the server after a cleared cache** (cross-device); untrack confirm; **history anti-noise gate both
ways** (1 unit → logged "untracked 1/10"; 0 units → no row); final unit → "Mark chapter complete"
→ done flag (local + server) → gold `st-done` card; sections independent (8B untouched throughout).

**My Lessons + archive (Pass 4):** prepared-only filter; exhaustive status line ("Completed 8A");
single-subject static label; attached plan has **no** archive icon; archive → toast + chip +
empty active view + server key; archive view + **restore** round-trips; **PrepareLesson stand-in
does NOT deposit** (vs FirstRun which does — intentional divergence, both directions verified).

**Teaching profile (Pass 5):** clean view mode (no controls); master Edit reveals bins + add
buttons + 4 edit pencils; stats (1/1/2/6); budget derives to 180; **scoped removal warning** names
"8A, 8B", "last class — Science goes with it", "lessons stay in the library"; expand window
("Do you teach Science to other classes?") gated behind tour resolution; ✕ unlocks the persistent
**"+" portal** (`plus_portal_test_fr1=1`); portal chooser Subject/Class/Section → manage mode with
enrolled options pre-ticked.

**Tenancy + API (Pass 7):** per-user isolation (iso_a state invisible to iso_b); missing header →
`local` tenant (no leak); unknown subject → 404; allocate empty-chapters / no-body → 422; profile
removal without `cascade` → **409 `destructive_edit`** + impact list; `/readiness/impact` dry-run
correct; archive traversal → 400; 5 concurrent section-state writes → all 200, last-write-wins, no
5xx/corruption; wholesale-empty `pullSectionState` guard preserves local bindings (seen in Pass 3).

**Mobile (Pass 8):** at ~304px effective width, **zero horizontal overflow** on My Classes,
LessonView, Assessment, Profile, and the profile's dense 3-column class card; tap targets and the
warm-paper layout render cleanly.

---

## D. Not testable in this environment

- Live LLM generation (deferred by design — `/generate` returns 501; saved plans stand in).
- Real iOS Safari safe-area / `100vh` / sticky quirks (Blink-only here; on-device pass still
  recommended per CLAUDE.md §4).
- Supabase auth / RLS (Phase 4 not built).
- True multi-instance concurrency / task-queue behavior (single file-backed instance today).
- On-device confirmation of B1 (arrow-tap under real mobile/reduced-motion conditions).

---

## E. Suggested priority

1. **A1** — decide Allocate's fate (delete, or re-wire + fix the grids reads). Biggest surprise;
   affects whether the allocation PDF/DOCX is a shipped feature.
2. **A2** — one-line-ish fix to match the documented portal exit behavior.
3. **A3** — namespace the leaking localStorage keys by user (small, prevents cross-user bleed).
4. **A4 / B1 / B3** — hardening + on-device verification when convenient.
