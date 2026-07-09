# Aruvi-SaaS — Accumulated Learnings & Carry-Forward Notes

## 2026-07-09 (newest) — RENDERERS REBUILT to the standard anatomy (STATIC only — live pass pending)

The founder green-lit implementation; both LP renderers now speak the standard anatomy:

- **`LessonView.jsx` rebuilt.** (a) New `UnitBody` = teacher notes (clay margin-note, TOP) →
  materials (hairline box) → phases with **duration in the marginal rail** ("8 / min", from
  `Phase.start_min/end_min`; falls back to legacy `activities` lines when a view predates
  phases) → homework (tinted, full text) — **LO never rendered**. (b) New **`ChapterOrg`
  altitude** (the front door): section-card language — chapter tick rail (pine taught / ochre
  now / hairline ahead), one `co-card` per unit under quiet group-kicker dividers, collapsed
  "Chapter notes" control (placeholder). **Preview opens at chapter altitude** (org page →
  card tap → read-only unit doc → back to org); tracking defaults to the live unit with a
  "chapter organization →" link (navigation NEVER moves the pointer). (c) Header durline
  "**{dur} min · {approach}**". (d) 📝 "Add a note about this class" invoke (tracking only,
  honest coming-soon reply). (e) All copy says **Unit** (assess-sub, pvnav, aria labels,
  mark-complete cards; also fixed in MyPlans + SectionProgress aria/labels). PRESERVED
  contracts: `lu_pointer_/lu_done_` keys, pushSectionState sync, undo model, tour anchors
  (preview-root/preview-back moved WITH the landing to the org page; lesson-notes now on the
  top teacher-notes block).
- **`ViewModelView.jsx`** (Generate/PrepareLesson/Allocate preview doc): same anatomy in
  `PeriodCard` (durline·approach, notes top, materials box, phase rail, homework tint, no LO,
  Tags row dropped); group headers show description only (implied_lo stays data).
- **CSS:** `co-*` + `uv-*` blocks appended to globals.css (tokens only, dark-safe).
- **Verification: STATIC only** (acorn-jsx parse all components OK, CSS braces balanced,
  contract greps). ⚠️ Live render + mobile 360px pass on the founder's machine is the
  immediate must-do: org page (all 6 axes), unit doc, tour steps 4/7/8 anchors, dark mode.

## 2026-07-09 — LP display STANDARDIZED (founder rules) + audits

Founder rules, all implemented (details in CLAUDE.md §3 "Standard LP display rules"; suite now
14/14 incl. new `tests/test_lp_standard.py`): **LO never in LP** (assessment only; data kept);
**`Period.approach`** canonical field (TWAU dominant_mode spelled out via `_MODE_FULL`);
**Science secondary fixed** (section_anchor groups, handoff rejoin — API now passes the FULL
`result` to `lesson_plan_to_view`, both call sites); **English singleton-section collapse**
(spines = top axis for split chapters). Homework word-caps dropped; time-plan/lesson-view tabs
dropped; English inline task-refs kept.

**Audit findings (2026-07-09, 39 plans):**
- Approach coverage is NOT universal: Science ✓(approach) · Maths middle+secondary ✓(method) ·
  English ✓(methods dict) · TWAU ✓(dominant_mode) · **Maths PREPARATORY: none** · **SS: none**
  (SS periods carry competency instead). **FOUNDER DECISION (same day): NO constitutional
  change** — the field names are too diverse to flatten at source; `Period.approach` is the
  single normalization point and absorbs the diversity (empty where no source exists).
- English split confirmed: 14/16 plans were single-section; the 2 stragglers were then SPLIT
  in-repo (2026-07-09, same session) following the existing `_split_from` precedent (vi/vii/viii
  splits): Grade III old ch_01 → **ch_01 "Fun with Friends (Picture Reading)" (A, 3 periods) +
  ch_02 "Colours" (B, 4 periods)**; Grade IX old ch_06 → **ch_11 "Twin Melodies" (A, 7) +
  ch_12 "A Friend Found in Music" (B, 4)** — titles taken verbatim from the re-split summaries,
  periods renumbered 1..n, coverage_handoff spine dict + assessment spine groups filtered by
  section_id, period_rows_snapshot/schedule recomputed from actual durations, stale ix ch_06
  deleted (its content slot now belongs to "Canvas of Soil"). Library = **41 plans**, all
  prepared for Kumar1 (register updated); every English plan is now spine-top. Suite 14/14;
  287/287 phases tile. NOTE: ix ch_06 SUMMARY ("Canvas of Soil") has an empty
  main_sections_inventory — authoring-pipeline flag, not touched.
- dominant_mode ≠ free-form approach: it's TWAU's closed 5-mode taxonomy (O&R/HI/D&C/C&E/R&A),
  but it answers the same teacher question, so it maps into `approach` with full names.

## 2026-07-09 (later) — Prototype UI study: per-subject·stage element decisions (the display spec)

Founder asked how per-subject·stage display elements are decided → studied the prototype
(`../Project Aruvi`, mounted this session). The decisions live in TWO files:
**`app/aruvi_streamlit/app.py :: _normalise_lo_handoff`** (lines ~2368–2921 — detects each
subject·stage by DATA SHAPE, maps raw fields to a common render dict) and
**`app/lpa_page.html :: renderLPA`** (lines ~2364–2917 — per-subject render paths). Print
variants in `lp_pdf_generator.py`. The element matrix the prototype settled:

| | axis/grouping | header 4th col | competency/LO bars | materials | homework | notes |
|---|---|---|---|---|---|---|
| Science middle | collapsible Stage groups (first open) | pedagogical_approach | NONE (deliberate) | yes | — | Time-plan/Lesson-view TABS; roles in tab 2 |
| Science secondary | FLAT (section-anchored) | anchored section | LO at END (from coverage_handoff) | **deliberately NONE** | — (field exists, not rendered) | approach bar top; visual_aids row |
| English | collapsible Section A/B/C groups (+type pill) | TWO cols: spines + ped methods | none | yes | task_brief ≤12 words, after phases | phases substitute task refs inline |
| Maths (all stages) | flat | section title (secondary centre-aligned) | SUPPRESSED (Rule 8); ped method rides materials row | yes | book_ref+desc ≤15 words | escMath superscripts (x^2) |
| Social Sciences | flat | anchored section | competency bar TOP (c_code+weight+text); LO at end | yes | — | |
| TWAU | flat | section_ref | mode bar TOP (dominant_mode FULL name: Observe and Record…); LO at end | yes | — | teacher_facilitation_note → notes slot |

Universal: every header = Period # · duration · activity name · (subject-specific col);
time slots ("Time | description") universal; teacher notes near end for all. **How to decide
for a NEW subject·stage: the LP constitution defines what the generator emits; the prototype's
verdict per element is the mapping above — in the SaaS this translates to (a) the Group
type/label (the axis), (b) the kicker/4th-column choice, (c) which optional anatomy slots fill.**

**GAP FOUND in our normalizer:** Science SECONDARY plans misroute through the middle path —
groups come out as **"Stage None"** (progression_stage is absent; secondary is section-anchored
like Maths secondary), per-period LO/section_context (in coverage_handoff) never extracted, and
the prototype deliberately renders NO materials for sci-secondary. Fix when renderers adopt
phases: science normalizer needs a secondary branch (group by section_anchor, LO via handoff
rejoin — see prototype `_ho_by_period`/`_ho_by_label`). Also note prototype truncation rules
(homework 12/15 words) vs our full-text mockup, and English's phase-text task-ref substitution
(`renderEnglishTimeSlots`) — carry or drop deliberately when building the new renderer.

## 2026-07-09 — LP/Assessment layout principles DECIDED + all-plans Kumar1 profile

**Layout discussion with founder (LP first; assessment next session). Decisions, all final:**

- **Standard period anatomy (every subject, every period, same slots, same order):**
  rail number + axis kicker + title + duration → **Teacher notes** (top — prep reading; italic
  Newsreader, clay left rule) → **Materials** (hairline box, mono kicker) → **Phases** (the hero,
  unboxed, time in the marginal rail) → **Homework** (bottom, the one tinted block — ochre wash)
  → **Period note 📝** as an *invokable input affordance* (a control to tap, never an empty box
  taking space). Differentiation via typography + hairlines + a single tint — no colored cards.
- **Phase time display = duration, "5 min"** (not band "0–5") — fits the Learning-Unit concept
  (periods → LUs, absolute durations per arch-plan §F). Times live in the marginal numbering
  rail (same signature pattern as period `01` / `Q1`), giving a perfectly aligned time column
  at 360px with full width left for prose.
- **One timed spine per period:** phases only. Subject extras (English `tasks_in_class`, Maths
  textbook items, visual aids) render as *untimed* kicker'd supporting blocks — never a second
  timeline. **Science `roles` are IGNORED for now** (founder call).
- **View-model change required first (not yet done):** promote `Phase {start_min, end_min, text}`
  + `materials: List[str]` to first-class on `Period`; update the 5 normalizers (today
  `_phase_lines`/`band_lines` DISCARD the minutes into flat strings). Raw saved plans already
  carry per-phase minutes — parse en-dash "0–5" AND hyphen "0-10", keys `phases[].description`
  vs `time_bands[].activity` — so this is a normalizer change, NO plan regeneration. Validate
  phases tile 0 → period_duration_minutes.
- **Chapter Organization = the chapter's front door** (first open / previews); the recede rule
  stands — pointer live ⇒ opens at period, "see chapter organization" links back. Chapter Notes
  slot (collapsed control) reserved on Chapter Org; Period Note slot in the period footer.
- **Next deliverable:** VM + normalizer change, then static 360×800 mockups in `docs/mockups/`
  for the standard period view + Chapter Org page; then assessment layout (Q-rail exists).

**IMPLEMENTED same day (the VM/normalizer step + mockups; all decisions above are now code):**

- **`Phase` + `materials` are first-class on `Period`** (`aruvi_core/view_model.py`): Phase
  {text, start_min, end_min, label(raw band)}. ADDITIVE — `activities` still carries the legacy
  flat lines so the current UI renders unchanged; the renderers switch to `phases` when the new
  layout lands (then drop phase lines from activities).
- **`normalize.py` gains** `parse_minutes_band` (en/em-dash, hyphen, spaced, "to"; reversed →
  None), `phases_from` (handles the `description` vs `activity` key drift), and
  `phase_tiling_issues` (0-start, contiguity, ends-at-duration; never raises — feeds tests/QA).
- **All 5 normalizers populate phases + materials.** Gotcha found: **Science secondary saves
  carry `time_bands`, not `phases`** (like Maths secondary) — Science now reads
  `phases or time_bands`. English still ALSO concatenates tasks+phases into activities (legacy).
- **`tests/test_phases.py`** (stdlib, needs ARUVI_DATA_DIR): parser forms + phases_from +
  tiling units, then the whole library — **33 plans, 238 periods: 238 with phases, 238 parse,
  238 tile cleanly (100%)**. Full suite now 12/12 green. `test_link_resolver.py` corpus assert
  changed from hardcoded-5-subjects to subjects-on-disk (TWAU has no saved plans).
- **Mockup for founder review: `docs/mockups/lesson-period-layout.html` (v2, 2026-07-09)** — two
  360×800 frames with real Prime Time (Maths VI ch.5) content, REBUILT after founder feedback to
  speak the My Classes **section-card language**: (a) Chapter Organization = "the section card,
  opened up" — chapter head carries the SAME tick rail (pine taught / ochre now / hairline ahead)
  that the section card shows, and each unit is an sc-style card (11px radius, 4px left accent
  pine/ochre/edge, tint-cream current with NOW pill, paper-sunk upcoming, serif number); sections
  are quiet mono dividers, not boxed accordions. (b) Unit view opens with a header card that
  ECHOES the tapped org card (ochre accent, cream tint, serif 03, mini rail), then the document
  flows on plain paper: teacher notes → materials → collapsed extras → phases (8/14/11/7 in the
  rail) → homework → 📝 invoke. **NAMING DECIDED: user-facing copy says "Unit n of N" — never
  "LU" / "Learning Unit"** (founder: confusing, unnecessary acronym). Applies to app copy
  (LessonView "Learning Unit N", sc-rail aria, My Classes meta) when renderers adopt the new
  layout; internal identifiers/CSS may keep lu_/LU. Assessment layout is the NEXT discussion.

**Data/state work done same session:**

- **Deleted 7 saved plans — 4 later RESTORED (the audit was WRONG, see below):** ss/vi ch_06 ×3,
  ss/viii ch_04_20260520, twau iii/iv/v one each.
  > **CORRECTION (same day):** the "old-schema / no time bands" flag was a FALSE POSITIVE — the
  > audit script counted `coverage_handoff[]` rows (which carry `period_number` but rightly no
  > `time_bands`; they're the LP→assessment link table) as periods. The files' REAL periods all
  > had clean bands. Lesson: **a dict with `period_number` is not necessarily a period — only
  > `lesson_plan.periods[]` entries are.** Founder re-uploaded the 3 TWAU files (restored to
  > data/content/saved_plans), ss/vi ch_06_20260520_161946 was restored from
  > tests/fixtures/ss_vi_ch06_saved.json, and founder later restored ss/vi ch_06_20260520_190601
  > + ss/viii ch_04_20260520_195842 from his own copies (both validated clean). Only
  > ss/vi ch_06_20260520_172638 (a 3rd version of the same chapter) remains lost — immaterial.
  > **Library = 39 plans, all 5 subjects, every subject·stage covered**; all 39 marked prepared
  > for Kumar1 (verified via TestClient, 39/39); test_phases: 287/287 periods parse + tile
  > cleanly; link_resolver: 382 items, 0 orphans, 5 subjects.
- **Kumar1 profile REPLACED with full-coverage profile** (founder request: see every LP in one
  place): all 24 subject·grade combos with chapter content — English III–IX, Maths III–IX,
  Science VI–IX, SS VI–VIII, TWAU III–V — one section each ("{n}A"/sec A, preserving old "A"
  section tags), durations [40], ppw 6, budget = NCF totals via `ncf_total_periods` (fallback
  180). Written directly to `data/readiness/Kumar1/Kumar1/profile.json`.
- **All 33 plans marked prepared for Kumar1** in `data/prepared_plans/Kumar1/Kumar1/prepared.json`
  ({at, periods} records; the 2 pre-existing timestamps preserved) — My Lessons filters to
  `prepared || attached`, so this is what makes the shared library visible.
- **Verified via FastAPI TestClient** (pip-installed fastapi/httpx in sandbox): /readiness
  returns all 5 subjects · 24 grades; /plans lists 33/33 prepared; 4 spot-check /view calls
  200 with lesson_plan present. Live browser + mobile pass still pending as ever (§11).

## 2026-07-06 — The standing "+" profile portal: the gliding path to acquisition (STATIC only)

**The problem (founder):** class expansion inside the first subject worked because acquisition
left HOOKS on screen (unbound section cards, the per-subject expand window). A second subject had
NO artifact anywhere — My Classes only renders enrolled cards, the My Lessons wheels are
restricted to the enrolled set, and the only door was the settings gear (data-first). Founder
rejected a "ghost card" as a back-door ask; instead: **once comfort is established (first gen →
tour → attach → the expand window has been seen), a permanent, prominent "+" opens** — the
standing portal for ALL profile change (new subject, new class, new/dropped section). Nudge
campaigns end; furniture begins.

- **Trigger (founder-precise, REVISED same day):** the expand window ("Do you teach {subject} to
  other classes?") appears **ONCE, EVER** — after the first generation, once the tour resolves
  (completed or skipped), pinned to the first one-class subject (`expand_shown_{user}` +
  `expand_subject_{user}` in localStorage; `expand_session`/`expand_dismiss` keep it up across
  tab-hops within its one session). The founder's earlier per-subject 3-appearance budget is
  **superseded**: after this single window, reminding about adding ANYTHING is an irritation —
  all growth is pull via the +, never push. The + unlocks on any of the window's three endings:
  (1) she used it (add-class completed; derived: any subject >1 class), (2) she clicked ✕,
  (3) she ignored it (spent in a past session, never returns). Persistent forever after
  (per-user `plus_portal_{user}`, sticky even if the profile shrinks back); never competes with
  the tour (`tourResolved` gate).
- **Placement (founder-precise, refined same day):** on the REPEAT view (anything bound) the +
  sits IN the greeting row ("Good evening, {user}!"), right side — no row of its own ("we cannot
  lose so much real estate"), and it rides the sticky `.dash-hd` so it stays reachable while the
  cards scroll. On the FIRST-TIME view it keeps its own row BELOW "Your classes are ready" and
  ABOVE the section cards — classes encompass new subjects too, so the portal governs the whole
  card list, never sits above the welcome. `.sc-growrow`/`.sc-grow` in globals.css —
  founder-specified glyph + finish (same day): a plus RINGED BY A CIRCLE with FOUR DOTS outside
  the ring ("grow in every direction", `GrowIcon` in MyPlans.jsx, pine) on a 46px RAISED TILE with real depth — paper
  gradient face, inset top-edge highlight, layered contact + ambient shadows, hover lifts,
  :active flips the light inward (pressed-key feel). Not a flat circle.
- **Chooser:** tapping + opens an ap-modal ("What would you like to change?") with three rows —
  Subject · Class · Section. Each routes via page.jsx's one-shot `profilePortal` intent
  (`onProfilePortal(kind)`, consumed like `profileAutoAdd`) into TeachingProfile, which launches
  the matching screen ("shared flows, two doors" — same wheels + warnings as the gear; no drift).
- **Manage modes (NEW in TeachingProfile):** `pickMode`/`classMode` "add" | "manage". Manage =
  enrolled options PRE-TICKED; unticking = removal behind ONE scoped confirm in the dustbins'
  voice (names what goes, "your lessons stay in the library") — **warned, never blocked**
  (founder: mid-year reassignment is real). Subject → manage-pickSubjects (keep ≥1 enforced by
  the disabled CTA — whole-profile delete stays impossible by design); Class → manage-classes on
  the same classes screen (removing the last class takes the subject, said in the warning);
  Section → the existing editSections screen (already add+remove+warn). Class/Section goals pass
  through light portalSubject/portalClass pick screens, skipped when only one option. Adds after
  removals queue the normal per-class question flow (`continueWithGrades` extracted so add +
  manage share it). All removals run `clearSectionState` per section, and `persist` already
  sends `cascade:true`.
- **A portal visit ALWAYS ends in My Classes (founder, same day)** — never on the profile
  accordion. Implemented as ONE seam: every flow ending (completion, cancel, all seven back
  links) funnels through `setScreen("view")`, and a `fromPortal` bounce effect forwards that to
  `onBack()` (= page.jsx's goClasses). The back links relabel to "← Back to My Classes" on
  portal visits (`backLabel`) so they say where she'll actually land; gear visits unchanged.
- **VERIFIED STATICALLY ONLY** (babel-parse clean ×3, CSS balance 0, prop/hook-order greps; the
  sandbox can't `next dev`). Live must-do next session: resolve an expand window as a test user →
  + appears → all three chooser paths, incl. a subject removal WITH attached sections, portal
  exits landing in My Classes, and the mobile 360×800 pass.

## 2026-07-06 — Tour revised to 12 STEPS + transparent hand + popup-always attach (LIVE-verified)

Second revision pass, same day. All 12 steps + Back boundaries re-verified live as kumar23.

- **APP change:** the section card's "+" now ALWAYS opens the "Track a chapter" picker — the
  first-run direct-attach shortcut is RETIRED (the card still names the ready chapter). One true
  way to attach, so the tour teaches the real flow.
- **NEW step 6:** after the "+" step, the tour OPENS the track-a-chapter popup with the hand on
  the just-generated lesson row (`data-tour="attach-pop-row"` on listPlans[0]); title "Select a
  lesson plan to track for Section {tag}". Next from 6 performs the real attach. So: popup at
  steps 6 AND 11 (at 6 nothing bound → lesson in list; at 11 bound excluded). MyPlans boundaries
  moved: bind ≥7 / unbind ≤6, lesson open 8–9, demoDone 10–11; page.jsx: 11→12 goProfile.
- **Hand is now a TRANSPARENT outline SVG** (translucent white fill + ink stroke, custom
  index-up path in GuidedTour.jsx) — not the filled emoji. Also appears on step 3 (lesson row).
- **Placement fixes:** step 8's box uses `tipAnchor:["lesson-notes","mark-complete"]` + place
  "above" + `scrollAnchor:"mark-complete"` so the teacher notes AND Mark-complete stay visible
  below the box (lv-tnote carries data-tour="lesson-notes"). Step 10's box is pinned to the
  viewport bottom ("over") so the progress rail and the SECOND section card stay visible; its
  copy renders the circled + (.gt-plus, a mini .sc-add). Step 12 rings the header SETTINGS GEAR
  (data-tour="settings-gear") with the profile open behind — "here's where profile lives".
- **Auto-scroll is INSTANT with ≤5 retries/step** (scrollRef) — smooth scrollIntoView silently
  no-oped on some layouts and made mid-scroll screenshots look broken. Carry-forward: never use
  behavior:"smooth" for tour scrolls.
- **Nudge reworded + new glyph:** title "Allow me to show you how to track sections and handle
  Lesson plans", sub "It only takes a few steps — I'll walk you through it."; the 👋 emoji is
  replaced by a stroke-only ROUTE icon (start dot → dashed path → destination, pine, transparent).
- Chrome `resize_window` stopped constraining the viewport mid-session (stuck ~1120px) — the
  12-step pass ran at desktop width; round-1's 390px pass validated the mobile geometry (all
  tour positioning is viewport-clamped). A manual DevTools 360×800 pass remains worthwhile.
- **Round-3 refinements (same day, live-verified):** step 4 = scrollTop + box LIFTED 130px above
  the sticky attach bar + hand moved to the "← back to lesson plans" button
  (data-tour="preview-back") + copy now directs "go back … and attach this plan to section
  {tag}"; steps 6/7 hands CENTRED on the row/card (cfg.handPos:"center"); step 8 = scrollTop +
  box hangs below phase 1 (data-tour="lesson-phase-1" on UnitBody's first phaserow) so header →
  progress bar → phase 1 stay visible; step 10 subtext = "Once all units of the chapter are
  marked complete by you…" + box lifted 10% of vh (cfg.lift: fraction<1 = vh-fraction, number =
  px) — 10% balances "well above the bottom" against keeping the second card visible (22%
  covered card 3B). Default anchor-scroll CENTRES a taller-than-viewport target — full-view
  steps must set scrollTop:true or the top of the view (back button etc.) scrolls away.
- **Round-7 — first-run stand-in made LOUD (founder chose "deposit stand-in, say so clearly").**
  kumar23 picked Maths VIII ch 5; only saved test plan is ch 9 → FirstRun substituted ch 9 AND
  deposited it (unlike PrepareLesson, which only marks the EXACT chapter). Root causes: the
  teaser screen SET previewNote but never rendered it, and showed the CHOSEN chapter's title
  over the stand-in's numbers. Fix: `.fr-standin` ochre notice box on the teaser (names the
  stand-in and says it's what lands in My Lessons), and the teaser title now names the plan
  actually deposited. Behavior stays deposit-the-stand-in (keeps activation + tour testable
  until live gen); PrepareLesson's exact-only rule unchanged. Once live generation lands,
  the substitution path dies naturally.
- **Round-6 BUG FIX — "guide switched to a chapter I never generated" (kumar23, 2026-07-06).**
  `/plans/{subject}/{grade}` returns the WHOLE shared library with per-tenant `prepared`/
  `prepared_at` flags; My Lessons filtered client-side but **MyPlans consumed the raw list**.
  Four spots fixed to prepared-only: (1) the tour target plan is now the MOST RECENTLY PREPARED
  lesson (`latestPrepared`, prepared_at desc) — was `gp[0]`, an arbitrary library entry (kumar23
  generated Science IX ch 2; the guide walked ch 8 "Journey Inside the Atom", prepared:false);
  (2) the "+" track-a-chapter popup list; (3) the card's `readyOne` ("Chapter N ready");
  (4) `anyPlans` (nudge/welcome gate — a raw library entry must never trigger the nudge).
  MyLessonPlans steps 3–4 now key off the same `tourPlanOf()` (most recent prepared), so the
  row spotlight and the auto-opened preview can never diverge from the tour's target. RULE:
  any client list fed to teachers must filter `p.prepared || attached` — never trust the raw
  /plans order.
- **Round-5 (same day):** "below"-placed tour boxes are now CLAMPED to the viewport
  (top ≤ vh−260) — on phones a long chapter title pushed phase 1's underside past the fold and
  step 8's box rendered off-screen; it now settles onto the plan body. scrollTop pins capped at
  2 tries so the guide never snap-scrolls against the teacher's own reading. ALSO FOUND (not
  fixed, plan-DATA issue, out of tour scope): the saved Science IX ch_02 plan renders LU1 with
  "No phases recorded for this unit" and a "STAGE NONE" kicker — the plan's first unit carries
  no activities and no stage label through normalization; this is the "garbled" look kumar
  reported on step 8. Investigate the science secondary saved plan / normalizer next session.
- **Round-4 (same day):** the My Lessons preview's "Attach to a class" CTA + section chooser are
  RETIRED app-wide (LessonView attach bar removed, MyLessonPlans attachPick/attachToSection/
  onAttached deleted) — attaching happens ONLY via the section card's "+" → track-a-chapter
  window, so tour step 4 no longer shows a button that "does not exist in reality". Step 9
  subtext → "Track chapter progress of {chapter} with section {tag} unit by unit…"; step 11 →
  "…the same window shown in step 6…". Live-verified; the tour proved profile-agnostic when
  kumar23's profile changed to Science IX mid-test (targets/copy followed the new first class).

## 2026-07-06 (later) — Guided tour RESTRUCTURED to 11 guide-driven steps (verified LIVE, mobile Chrome)

Kumar respecified the tour top-to-bottom. The 4-step wait-for-real-taps walk is GONE; the tour is
now **11 steps, fully guide-driven** — every step has Back · Skip · Next, a "N of 11" counter, and
Next itself performs the move (nav, open preview, the attach, popup, profile) with a bobbing 👆
hand showing where the real tap would land. All 11 steps + Back across every view boundary
verified live at localhost:3000 as kumar23 at 390px.

- **Steps:** 1 My Classes tab → 2 My Lessons tab → 3 the lesson row (guide navigates) → 4 preview
  auto-opens → 5 hand on the section card's "+" → 6 REAL attach (the activation; Back from 6
  unbinds) → 7 tracking view opens → 8 hand on Mark-complete (never really clicked) → 9 card
  DEMOED as Complete + hand on its "+" (render-only — `tourDemoDone` forces the completed look;
  her real pointer/done untouched) → 10 the "Track a chapter" popup (opened by the tour) →
  11 the teaching profile, Done.
- **Architecture:** GuidedTour.jsx is presentational (numeric step, one anchor per step, poll +
  scrollIntoView, `place: below/above/over` — "over" pins the box to the viewport bottom for
  full-view targets). page.jsx owns shell transitions (2→3 goLessons, 4→5 goClasses, 10→11
  goProfile); **MyPlans owns steps 5–10 via IDEMPOTENT state-keyed effects** (bind/unbind at the
  6/5 boundary, open/close lesson at 7–8, popup at 10, prev-ref cleanup on Skip) — hooks sit ABOVE
  the !ready early-return (rules of hooks). MyLessonPlans owns 3–4 (auto-open first prepared plan).
  MyPlans reports `{tag, chapter}` up (onTourInfo) so step copy names them. The old "success"
  banner step is gone. Anchors: nav-classes/nav-lessons (tabs), lesson-first, preview-root/
  lesson-root + mark-complete (LessonView), section-add/section-card-target (target card = first
  class WITH a prepared plan), attach-pop (ap-modal), profile-root (page.jsx editflow div).
- **Tooltip is the thematic box:** .gt-tip restyled to the SAME sage-pine window as .dash-nudge
  (#eef4f0, 1.5px pine border, r14) — one visual voice for the whole first-run journey. Dots
  replaced by a mono "N of 11" counter. .gt-root z-index 70 (ABOVE ap-overlay's 60) so step 10
  annotates the popup; scrim blocks taps on every step (guide-driven).
- **Live-verify gotchas:** screenshots taken during the smooth scrollIntoView LOOK broken (blank
  paper, header mid-screen) — always re-shoot after the scroll settles; the ring transition
  (.18s) can also lag a capture. `resize_window` 390×844 DID constrain the viewport this time
  (~304 CSS px content width) — footer needed white-space:nowrap on the three buttons to stay on
  one line. Test state restored after the run (section-state DELETE + localStorage clear), so
  kumar23's nudge re-offers the tour on reload.

## 2026-07-06 — Tour refinements + "lesson not in My Lessons" bug (all verified LIVE in Chrome)

Kumar reviewed the tour and asked for changes; also hit a real bug. Verified live at localhost:3000
as kumar23 (Chrome), steps 1→4 + Back all confirmed on screen.

- **BUG FIX — "I ran a lesson but it's not in My Lessons" (kumar23).** NOT a deposit failure — the
  plan WAS marked prepared on disk (`data/prepared_plans/kumar23/.../english/iii/ch_01…`). The bug
  was My Lessons' DEFAULT CLASS: `mylessons_class` localStorage is neither user-namespaced nor
  validated, so a stale class (from another user in the browser, or from before a profile delete)
  made the tab open on a class where her prepared lesson doesn't live → "no lessons prepared". Fix
  (MyLessonPlans.jsx `activeGrade` initializer): default to a class she actually TEACHES for the
  initial subject, derived from the current server profile — trust the taught-grades list, not the
  persisted value. Same server-derived principle as the tour-flag fix. Confirmed live: My Lessons
  now opens English·Class 3 and shows "Fun with Friends — Ready to teach".
- **Tour changes (all live-verified):** (1) removed the confusing "Tap any class… your place only
  moves…" `dash-foot`. (2) Nudge is now a distinct sage-pine WINDOW (`.dash-nudge`, speech-bubble
  tail, pine border — clearly not paper) with a CONVERSATIONAL italic-serif "Show me how →" link,
  not a solid button. (3) Step 1 CYCLES the spotlight through every section card (`data-tour=
  "section-card"` on each unbound card; GuidedTour rotates cycleIdx every 1.1s, tooltip anchored to
  the first card, stable). (4) Step-2 copy = "To attach a lesson plan to a section, you tap the +
  symbol on its card. But first, let's see where your lesson plans sit." (5) Steps 1–2 have Next;
  after step 2 there is NO Next — steps 3–4 are real-tap with Back+Skip only. Step-2 Next
  AUTO-navigates to My Lessons. (6) BACK on every step (except 1) returns to the previous step's
  animation; back from preview closes the open preview (MyLessonPlans effect on `tourStep==="lesson"`)
  and re-highlights the lesson. page.jsx `tourNext`/`tourBack` own the transitions.
- **Also:** the preview "Attach to a class" CTA is now STICKY to the viewport bottom (`.lv-attachbar`
  position:sticky) so it's always reachable on a long plan and the step-4 spotlight is never below
  the fold. Verified live.
- NOTE: `resize_window` to 390 didn't actually constrain the content viewport in this Chrome (still
  rendered desktop-width), so the true 360×800 phone pass is still worth a manual DevTools device-mode
  check — but the flow, copy, spotlight, and back-nav are all confirmed working.
- **BUG FIX — "+ works late" (kumar23, live-confirmed).** Tapping "+" on the first-run ready card
  wrote the binding (server confirmed) but the card didn't refresh until the next incidental render
  (20s sync / tab focus) — because the DIRECT-attach path calls `setAttachFor(null)` while attachFor
  is ALREADY null, so React skips the re-render. Fix (MyPlans `attachChapter`): also
  `setSyncTick((t)=>t+1)` to force an immediate re-render. Verified live: card now flips to "Fun with
  Friends" instantly on tap.
- **Removed the nudge speech-bubble tail** (`.dash-nudge::before`). Kumar flagged it as an "uninvited
  arrow" on desktop — it was an unrequested flourish I'd added; the nudge is now just the clean
  rounded sage window. (Reminder for future: don't add decorative flourishes beyond what's asked.)

## 2026-07-06 — First-run GUIDED TOUR: the helping hand from blank cards → first attach

**The blank-landing problem (founder).** After the 2026-07-05 full-profile first run, she lands in
My Classes on empty section cards (3A, 3B) with the promised lesson one un-obvious tap away (via +
on a card, or My Lessons → preview). She's blank, doesn't know what to do. Ask Aruvi is the wrong
tool here — it's PULL (she must know what to ask); the first-run moment needs PUSH. Solution: a
one-time, skippable coach-mark tour, launched from a "Show me how" nudge, that walks her My Classes
→ My Lessons → preview → attach. Founder decisions this session: **full 6-step walk** (nudge + 4
coach-marks + success, not a compressed 3-beat); **+ attaches the ready lesson directly** (first-run
card copy reconciled from "Pick a chapter to begin" → "Chapter N ready · tap + to add"; picker still
used when >1 prepared); **wait-for-real-taps** (the tour does NOT auto-drive — she performs the real
taps, page.jsx advances); Ask Aruvi placement parked for now.

**Built (all STATIC-verified only — esbuild parses clean, CSS balanced; live + 360×800 pass is
Kumar's must-do next):**
- `GuidedTour.jsx` (NEW) — presentational coach-mark overlay. Positions by `data-tour` attribute +
  getBoundingClientRect on a 200ms poll (survives tab switches / late-loading targets). Spotlight =
  a transparent ring with `box-shadow:0 0 0 9999px rgba(...)` cutout. Scrim is pointer-transparent
  on action steps (real tap reaches the app), blocking on the one informational step. Steps:
  card (Next) → lessons (tap My Lessons) → lesson (tap the lesson) → preview (tap Attach). Success
  is NOT an overlay step — it's a banner in My Classes.
- `page.jsx` — tour controller (crosses `editFlow`, so it must live here). State `tour`
  (card|lessons|lesson|preview|success), `tourTag` (attached section, for success copy),
  `tourDismissed` (SESSION-ONLY, never persisted — see the fix note below). Advances on REAL events:
  goLessons → lesson; MyLessonPlans onPreviewOpen → preview; onAttached → success (+ goClasses).
  Success auto-dismisses after 7s. `data-tour="nav-lessons"` on the My Lessons tab.

  ⚠️ **FIX 2026-07-06 (kumar23): the tour offer must be SERVER-DERIVED, not a persisted client
  flag.** First cut stored "tour done" in localStorage (`aruvi_tour_done_{user}`). Kumar skipped for
  kumar23, deleted profile+allocations server-side, logged in again → the fresh first run never
  re-offered the guide, because the stale browser flag survived the server-side delete. This is the
  identical desync the top-of-page activation-flag note already warns about. Fixed: dropped the
  persisted flag entirely. The nudge is gated purely by server-derived first-run state (MyPlans:
  `!anyBound && anyPlans`), which self-closes forever once she attaches; `tourDismissed` is
  in-memory only (skipping hides it for the session; a fresh login re-derives from the server). The
  old `aruvi_tour_done_*` localStorage keys are now dead/ignored — no migration needed. Carry-forward:
  do NOT reintroduce a client-side "onboarded/seen" flag; if skip must persist across sessions, put
  it on the server profile record so a profile delete clears it too.
- `MyPlans.jsx` — first-run card copy "Chapter N ready · tap + to add" + direct attach when exactly
  one prepared plan; `data-tour="add-first"` on the first unbound card's +; "Show me how" nudge
  card; success banner (step 6). attachChapter/clearBinding now call the shared writers.
- `MyLessonPlans.jsx` — `data-tour="lesson-first"` on first card (tour only); `onPreviewOpen`
  callback; "Attach to a class" from the preview opens a section chooser → `bindSectionChapter` →
  `onAttached(tag)`. Preview attach is a NEW capability (was read-only); gated behind an `onAttach`
  prop so the in-view "View full lesson plan" preview stays read-only.
- `LessonView.jsx` — optional `onAttach` renders the "Attach to a class" CTA (`data-tour="attach-cta"`)
  in My-Lessons preview only.
- `lib/sectionState.js` — NEW shared `bindSectionChapter` / `unbindSection` writers, so My Classes'
  "+" and the preview attach can never drift.
- CSS: `.gt-*` (overlay, z-index 55 — above sticky chrome, below `.ap-overlay` z60 so the section
  picker layers over the tour), `.dash-nudge*`, `.dash-success*`, `.lv-attachbar/.lv-attach-btn`.

**Open / to confirm with Kumar:** the 'card' step is informational (Next), NOT an action, so she
isn't nudged into a direct attach that skips the My-Lessons half of the walk — reworded away from
"tap +". Whether preview-attach should stay general (current) or be gated to first run only. Ask
Aruvi's post-first-run home (header vs permanent footer) still parked.

## 2026-07-06 — PickWheel shows a running "chosen so far" line under the button

**The stray-tick problem (founder).** `PickWheel` (wheels.jsx) shows only 4 rows at a time; a
teacher picking durations/sections from a later batch can't see her earlier picks and may leave a
stray tick behind she never meant to keep. Fix: PickWheel now renders a running confirmation UNDER
the Continue/Done button — `Chosen (N): …` listing the FULL current selection in option order
(independent of scroll position), or an italic "Nothing chosen yet" empty state. Built once in the
shared component, so EVERY multi-select flow inherits it (FirstRun acqSections/acqDurations + the
SectionPicker modal; TeachingProfile add-subject/classes/sections/durations). Uses each caller's
existing `labelFor` (subjects list is already pretty-mapped, so no labelFor needed there). Opt out
with `summaryLabel={false}`. CSS: `.fr-pick-summary` / `.fr-pick-summary-empty` in globals.css
(added under `.fr-sec-wheel-col`), `aria-live="polite"`. Statically verified (esbuild parses
wheels.jsx clean; CSS braces balanced); live/mobile render still pending per §11.

## 2026-07-05 — First-gen now acquires the FULL profile (reveal-on-attach, unattached cards)

**The orphaned-first-class problem (founder).** The old first-run tail generated a lesson then just
asked her to NAME a section, auto-attaching a single-duration LP to the fanned-out sections. That
left the first class looking "done" while its profile was never acquired (defaulted duration, no
periods/week, no budget) — and once "complete" cards exist, nothing ever pulls her back to finish
it; she moves on to other classes/subjects and the first class stays orphaned. The one moment she's
motivated is right after generation (desperate to see the lesson), so we now acquire the WHOLE
profile there. Founder decisions this session: **reveal-on-attach** (she does NOT see the full LP
before the profile questions; she sees it after landing in My Classes and tapping "+"), and
**full profile incl. annual budget** (not a lighter subset).

**New FirstRun tail:** welcome → subject → grade → chapter(+default duration) → preview (facts
teaser, "your lesson is ready") → **acqSections → acqDurations → acqPpw → acqBudget** (the full
per-class profile for this subject·grade) → creatingCards → lands in My Classes. The old preview
section-picker fan-out + `SectionPicker` modal usage are gone (the component is left defined but
unused). `buildActivationPayload` now emits the full canonical grade record: sections, durations
(multi), `ppw_by_duration`, derived `periods_per_week`, and `budget: { 0: … }`.

**UNATTACHED cards (the key mechanism).** `finishActivation` deposits the lesson in My Lessons
(`markPrepared`) but NO LONGER binds it to any section (removed the `current_chapter_*` writes +
`pushSectionState` import). Cards land in the "pick a chapter" state; MyPlans already renders those
with a "+" that opens the attach picker listing the deposited lesson. So the reveal path is: acquire
profile → land → tap "+" → attach → tap card → see LP. MyPlans' `!anyBound` welcome banner now
guides to "+": "Your lesson is waiting in My Lessons — tap + on a class to start teaching it" (falls
back to "tap + … to prepare its first lesson" when `anyPlans` is false, e.g. a later subject added
with nothing generated).

**Reuse:** `PpwCapture` + `normPpw` + `ppwMapSum` + the duration/ppw constants were EXPORTED from
`wheels.jsx` and FirstRun imports them; the annual-budget estimator (METHODS/defaultValueFor/
budgetPeriods + NCF `/ncf-periods` fetch) is duplicated into FirstRun (self-contained). **Cleanup
TODO:** `TeachingProfile.jsx` still carries its OWN identical copies of `PpwCapture`/`normPpw`/
`ppwMapSum` + those constants — left untouched on purpose to avoid destabilising the working editor;
migrate it to import from `wheels.jsx` when next in there.

**Stale-binding bug (found via `kumar23`, fixed 2026-07-05).** After the unattached-cards change,
`kumar23`'s first-gen still showed 3A already attached to "Fun with friends". Cause: the section
teaching-state (`current_chapter` etc.) is SERVER-backed + localStorage-cached and survives profile
deletion, so a reused section key (`english_iii_3A`) resurrected its old chapter via
`pullSectionState` — the new code never binds, but old rows persisted. Three-part fix: (1)
`finishActivation` now explicitly CLEARS each created section's binding — localStorage keys removed
+ `pushSectionState` (which DELETEs the server row when no chapter is cached) — guaranteeing fresh
cards regardless of stale state (safe because first-gen only runs for an empty profile); (2)
**`DELETE /readiness` now also `section_state_repo.clear_all(...)`** (new repo method — unlink the
state.json, fallback empty-write) so "start setup over" truly resets teaching state; (3) wiped
`kumar23`'s stale `state.json` → `{}`. **Caveats for the local test:** restart uvicorn (Python
change) and note that the `serverEmpty` guard in `pullSectionState` KEEPS local cache on a
wholesale-empty pull — so a device that already cached the 3A binding only clears it by re-running
first-gen (which now self-clears) or clearing site storage; wiping the server alone won't update
that device's view.

**Copy/layout refinements (founder, 2026-07-05):** the four acquisition screens now carry a
4-step **progress rail** (`ACQ_STEPS` = Sections · Durations · Periods · Budget, via the generalised
`Progress` component) so she sees the run ends soon. Preview lead-in is "Your lesson plan needs a
home. Help us set up your class to receive the plan." + bold "Now let's set up your class"; CTA is
**"Set up my class"** (singular, both the preview and the final button). Sections hint: "Pick all
the sections you teach." Periods question is grade+subject-specific ("How many periods a week does
Class N get for English[ for each duration]?") with NCF-framed sub-copy. **Budget step restyled:**
each method carries its OWN result (stepper/estimate + "≈ N periods…") DIRECTLY below it, not one
shared block at the end — so the number sits where she chose; and once she picks a method the other
three **dim** (`.fr-dim`, siblings wrapped in `.fr-bud-row` with `.fr-bud-detail`). No method is
pre-selected (budget starts null); the finish button is disabled until she picks one.

**Verified (static only — sandbox can't `next dev`):** acorn-jsx parse clean on wheels/FirstRun/
MyPlans/TeachingProfile; globals.css balanced; FirstRun no longer references `pushSectionState`/
`durOptions`; "Set up my class" is singular everywhere; 4 acquisition progress rails present. Local
+ mobile pass owed (§11): run first-gen end to end (single AND 2-duration), confirm the 4 screens +
progress rail render, the profile persists, cards land UNATTACHED, the "+" picker lists the deposited
lesson, and the budget number appears under the chosen method with the others dimmed.

## 2026-07-05 — Period durations & the LLM's time budget: order is dead, counts survive (Issues 1 & 2 resolved)

A design conversation settling how the constitution should receive TIME once the calendar was
purged. Two problems were on the table and are now resolved; a third (collection UX) is decided
in principle but deliberately NOT built into first run yet.

**The root diagnosis.** Both problems come from trying to hand the LLM time as a SCALAR — either
"N periods" (durations unknown) or a single "total time Tm = ΣD·T" (mix and order unknown). A sum
throws away exactly the structure the problems are about. The fix is to hand the LLM an **ordered
vector of per-period durations** (e.g. `[40,60,40,40,60,…]`), NOT a scalar. This keeps the proven
ordered-period constitution instead of migrating it to a gross-time model. **Carry-forward for the
pending "wire time into the constitutions" task: do NOT wire a scalar total-time Tm — wire a
per-period duration field/vector. Tm becomes a derived checksum (Σ of the vector), never an input.**
This supersedes the earlier "give the LLM total time to gross up" drift (which was never wired).

**ISSUE 1 (the mix) — where does T1/T2 come from once the weekly grid is gone?** With a single
duration D and total T, Tm = D·T trivially. With two durations we know D1,D2 but not the counts
T1,T2. We must NOT let the LLM pick them (it would go to an extreme — all-short or all-long — i.e.
iterate on time itself). So the counts must be COLLECTED. Resolution: collect the per-week duration
split as COUNTS (e.g. 6 periods/week = 4×40 + 2×60); the counts give the ratio.

**ISSUE 2 (clumping / un-teachable layout) — and why ORDER cannot save us.** Even given the counts,
the LLM could clump all longs together, or place an indivisible 60-min activity where the teacher
only has a 40-min period. The tempting fix was to collect the ORDERED weekly rhythm per section and
stamp period *i* → rhythm[i mod k]. **This idea is DEAD, killed by a per-section objection that is
fatal, not cosmetic:** order is the ONE time-fact that genuinely varies across sections of a grade
(7A has the subject Mon-P1, 7B Tue-P3, …). Periods/week and the duration split are set by curriculum
+ the school bell schedule → grade-UNIFORM and factually answerable; only the slotting (order)
differs per section. Since we generate ONE plan per GRADE (per-section generation is too expensive
and breaks the shared-asset model), a per-grade plan cannot carry a per-section order, and asking
"what's the order?" is unanswerable when her three sections differ. **The old design's latent sin:
it collected section-wise day order and then the gross-time constitution grossed it away — paying
to collect the one fact the model can't consume. Dropping order is what makes the per-grade plan
CONSISTENT for the first time.** Everything the plan needs (total periods, duration split) is
grade-level; only the unanswerable thing leaves.

**How Issue 2 is actually handled WITHOUT order:** hand the LLM the **count multiset** ("14 periods:
11×40, 3×60"). Counts are GIVEN (no free iteration); the LLM only decides WHICH pedagogical moments
are the long ones — a pedagogical judgment (the sessions that need sustained time: experiment,
project, extended write), which is arguably BETTER than honoring any one section's calendar accident.
Feasibility is guaranteed globally (she has exactly 3 long slots over the chapter; the plan has
exactly 3 long sessions). The only residue is LOCAL (a long session may surface in the plan before
her next long slot) — handled by the flow pointer + trivial teacher agency, and made cheap by
**MARKING** the long sessions in the view ("longer session — best in a full period"). Marking is the
whole mitigation; she never has to split an indivisible activity because it's flagged to wait for a
slot that fits, and she's guaranteed to have one. Generation assumes each chapter **starts at cycle
position 0** (no cross-chapter phase tracking — keeps chapters independent, matches "notes never
migrate across regenerated plans").

**At generation:** allocation stays in period COUNTS (NCF norms → allocator, unchanged). The split
enters one layer downstream: total periods → split by the grade ratio via **`splitByRatio`
(largest-remainder, already in Allocate.jsx, already unit-tested, sums exactly)**. The calendar
purge only removed `splitByRatio`'s INPUT (it used to derive the ratio from the weekly grid via
`weeklyRatioFromReadiness`); we restore the input as a **direct two-number question** (the duration
split), not a grid. Small restoration, existing engine.

**Approach A (default) vs B (override).** A = store the grade duration split once, derive the
per-chapter split by rounding at generation (low friction, reused across section cards + My Lessons).
B = ask the split at every generation. B's "exactness" is mostly illusory — the split she'd type is
her weekly ratio × the total, i.e. the arithmetic A already does. **Decision: A is the default;**
expose B only as an optional per-chapter **"Modify split"** override, reusing the existing Allocate
**Accept / Modify** idiom (§3).

**Collection UX (decided in principle):** wherever a duration is captured (first gen, direct edit in
My Profile, or indirect acquisition as she navigates), if she picks >1 duration type, ask the
per-week COUNT per type RIGHT THERE (40→4, 60→2) — do NOT introduce periods/week as a separate
number and then ask the split; periods/week = Σ of the per-type counts. This will feed a schema
where the grade record carries the per-duration weekly counts (ratio) + derived `periods_per_week`.

**BUT — first-run scope decision (founder, this session): do NOT build multi-duration into first
generation.** It would force a `durations` schema change (today `durations` is a flat number array,
consumed by Allocate/MyCalendar/MyClasses/TeachingProfile/format.projectReadiness) and add friction
to a deliberately minimal, benefit-first flow. **Interim shipped:** in `FirstRun.jsx`, when she taps
"Change" on Class duration, a small `fr-hint fr-dur-note` line now reassures her — "Some classes run
longer than others. Let’s keep to one duration for now — you can add more later." First run still
collects a SINGLE duration. The mixed-duration capture (per-week count per type → count multiset at
generation) + the actual `splitByRatio` wiring land LATER, in gradual profile acquisition, together
with live generation (the preview currently serves a canned saved plan, so a split can't affect it
yet anyway).

**Implemented in My Profile (`TeachingProfile.jsx`) this session — the per-duration periods/week
capture (founder scoped it to My Profile now; first run stays single-duration).** The single
"periods per week" question is REPLACED by per-duration capture wherever duration is captured
(the add-a-subject / add-a-class conversational flow AND the spot-edit pencils):
- **Schema (additive, server-safe):** the grade record gains `ppw_by_duration: { [minutes]: count }`
  (e.g. `{"40":4,"60":2}`). `periods_per_week` is KEPT as the DERIVED sum, so every existing
  consumer is untouched (budget estimator, the view totals `stats.ppw`/`subPpw`, the per-class
  column, `format.projectReadiness`). Confirmed end-to-end: POST /readiness stores `subjects`
  verbatim and the file adapter's `_PROJECTION_KEYS` strip is TOP-LEVEL only, so a grade-level field
  rides through save→reload; `projectReadiness` returns `subjects` intact. NO api/adapter/other-
  component changes were needed — the whole change is `TeachingProfile.jsx` + a `.tp-ppw-*` CSS block.
- **Two helpers + one component:** `ppwMapSum`, `normPpw(durations, map, fallbackPpw)` (reconciles
  the map to the CURRENT durations — keep surviving counts, new duration defaults to the total when
  single / to 1 when multi), and `<PpwCapture>` — the ONE idiom, two shapes: single duration → the
  same large periods/week wheel as before (no visible change); >1 duration → a two-column table
  (Duration · a −/number/+ stepper per row, reusing `.tp-val-btn/.tp-val-input`) with a live
  weekly total. **Total is never asked directly — it's the sum.** Handles up to 3 duration types.
- **Flow:** the durations step now CHAINS into the per-duration question (add flow: durations→ppw
  reconciles the map on Continue; spot-edit "duration" screen shows **Continue** when >1 duration —
  routing to the per-duration ppw screen — and **Save** when only one). Save paths (`finalizeSubject`,
  `saveEditNums`, the new-grade seed, `gradeDraftFrom`) all write `ppw_by_duration` + the derived
  `periods_per_week` via `normPpw`/`ppwMapSum`.
- **View (2026-07-05, final — "Option C" total-forward, empty-row fixed):** the accordion class
  card's **Periods / week** column shows the weekly TOTAL as the big number, with the per-duration
  split as a caption directly below it ("6×40 · 1×50") when >1 duration; single-duration shows just
  the number. **The caption (`.tp-cc-col-cap`) is `position:absolute; top:100%`** so it lives in the
  card's bottom padding and does NOT stretch the centre column — that height difference (centre 3
  lines vs Duration/Budget 2 lines) was what left an empty row hanging under the card. `.tp-classcard`
  padding-bottom bumped 13→16px to hold the caption. (History, so no one re-breaks it: tried
  positional "4/2" — ambiguous; then the caption in normal flow — caused the empty row; then folding
  the split into the value line inline — founder wanted the total-forward look back; landed on the
  absolute-caption version, which keeps total-forward AND removes the empty row.) The weekly total
  also still shows in the subject header.
- **Legacy caveat:** a pre-existing MULTI-duration record with no `ppw_by_duration` can't have its
  old total re-split (we never had the per-type data — that's the whole point), so `normPpw` seeds
  each type at 1; she re-enters the split once. Single-duration legacy records migrate exactly
  (`{[dur]: periods_per_week}`).

**Verified (static only — sandbox can't `next dev`):** acorn-jsx parse clean on TeachingProfile.jsx
+ FirstRun.jsx; globals.css brace-balanced (1261/1261). Live render + mobile (360×800 first) owed
locally per §11: confirm the FirstRun note appears under the duration wheel only in edit mode; and
in My Profile that picking a 2nd/3rd duration shows the two-column table, the running total is
right, Save persists across refresh, and the class card reads "40/60 min ↔ 4/2".

## 2026-07-04 — Archive (not delete) for lesson plans in My Lessons

**Founder decision: there is NO hard delete of a lesson plan — only Archive.** Two reasons that
compound: (1) a generated plan is the most expensive artifact the teacher owns (prototype ~Rs 23/
chapter), and the planned output cache means even a "deleted" plan is cheaply regenerable — but
(2) the cache does NOT hold the teacher-specific state wrapped around the plan (section
attachments, the LU pointer = where she stopped, period/chapter notes). THAT is irreplaceable, and
it's the real reason to preserve rather than destroy. So a hard delete was rejected; archive is the
only removal affordance.

**Archive is a FLAG, not a place.** The plan asset itself is shared read-only CONTENT under
DATA_DIR (Bucket A) — archiving can't and doesn't relocate it. Instead a per-tenant Bucket-B store
records the plan's key `{subjectSlug}/{gradeSlug}/{filename}`. My Lessons lists un-archived plans;
an **Archived** view lists the rest; **Restore** just drops the key. Frozen identity + all
back-references untouched ⇒ restore is lossless. To the teacher it *looks* like it moved to
"Archive"; architecturally nothing moved — "Archive" is a second filtered view over one list.

**Attached ⇒ NO archive affordance at all (founder, 2026-07-04 — refined from "block+warn").**
"Attached" = any section is currently teaching or has completed the chapter (the same signal that
colours the card; `isAttached()` in MyLessonPlans). The earlier design showed the archive control
and blocked it with a warning toast; the founder's point was that showing-then-blocking is
inconsistent — so the archive icon is simply **not rendered** on an attached card. No warning path
exists. `archivePlan()` keeps a silent `isAttached` guard purely as defensive dead-code. So
archived plans are only ever detached ones — no orphaned pointers to reason about on restore.

Implementation (all behind existing seams, Supabase-swap-ready at Phase 4):
- **Port** `PlanArchiveRepository` (ports.py) + **file adapter**
  `aruvi_core/adapters/plan_archive_repository_file.py` — atomic write, tenant-keyed, stored at
  `STATE_DIR/plan_archive/{tenant}/{user}/archive.json` as `{plan_key: archived_at_iso}`. Mirrors
  the section_state repo pattern. `archive()` is idempotent; `restore()` a no-op if absent.
- **API** (main.py): `GET /plan-archive` (all keys), `POST /plan-archive`, `DELETE /plan-archive`
  (both take `{subject, grade, filename}`); `GET /plans/{subject}/{grade}` now takes identity and
  annotates each listing with `archived` + `archived_at`. Phase-4 swap = an `archived_at` column /
  small `plan_archive` table behind the same port; routes + components unchanged.
- **UI** (MyLessonPlans.jsx + globals.css) — NO pills (founder). Archive is a "folder" you open and
  close via ONE symmetric control: an **archive-box icon + count to the right of the title**. In
  your lessons it's a **closed box** (tap to open the archive); inside, the title switches to
  **"Archive"** and the same control becomes an **OPEN box** (lid lifted = you're in it) — tapping
  it closes the box and drops you back to your lessons. This replaced an earlier "‹ Your lessons"
  back link the founder found confusing. Each *un-attached* active card carries a small
  **closed-box archive icon at its top-right corner** (absolutely placed; card reserves right
  padding; the old `›` chevron was dropped); attached cards show NO archive icon. Archived cards
  carry an explicit **green "Restore" text button** (founder: the undo-arrow glyph was unclear;
  the word on a solid pine fill is direct). Icons are inline SVG (`ArchiveIcon`/`OpenArchiveIcon`,
  currentColor). Pressing archive optimistically drops the card from the active list and STAYS on
  the active page (no view switch) with a brief bottom toast; restore optimistically removes it
  from the folder and, when the folder empties, `effView` auto-falls-back to active.
  Revert-on-failure on both.
- **Scope:** archive affects ONLY the My Lessons library view. Other `/plans` consumers (Generate,
  PrepareLesson, MyPlans dashboard, SectionProgress) select a plan by chapter/filename and are
  intentionally left seeing the plan — you can still preview/regenerate an archived chapter; it's
  just decluttered from the library list. Since attached plans can't be archived, the MyPlans
  weekly dashboard (driven by section pointers) never surfaces an archived plan anyway.
- **No purge / no auto-expiry** (superseding the earlier junk-basket-for-1-week idea): the economic
  argument says keep it. A future explicit, gated "empty archive" would be the only place a true
  hard delete could ever live — noted, not built.
- **Verified:** adapter unit test (archive/restore/idempotent/tenant-isolation) green; `api.main`
  imports + route registered; globals.css brace-balanced; MyLessonPlans.jsx babel-parses. Live
  render + mobile (~390px) pass still owed per §11 (sandbox can't `next dev`).

## 2026-07-04 — Section history + the long-chapter-title standard + My Lessons wheel tweaks

> **Naming (founder, 2026-07-04):** the feature is **"Section history"** (UI title + glyph label),
> NOT "Chapter history". Vocabulary: **Class = grade** (7), **Section = the letter within** (7A).
> The history belongs to a SECTION and lists the CHAPTERS it has taught. "Chapter history" is
> deliberately RESERVED for a future per-chapter concept — the LP version trail across repeat
> regenerations of one chapter. The data module stays `sectionHistory.js` (correctly section-scoped).
> Also swept the class/section slips this exposed: the "+" picker + section-card aria-labels now say
> "section", not "class".

**Section history — a per-section teaching ledger (the natural completion of "where did I
stop?").** Before this, a section only held its CURRENT chapter binding + pointer + done flag
(`sectionState.js`); the moment a chapter left the current slot (untrack, or move-on from a
completed chapter) that record was DELETED, so the trail of what a section had taught lived
nowhere. Built:
- **`web/app/lib/sectionHistory.js`** — a per-section MAP keyed by chapter FILE (so exactly ONE
  row per chapter and the latest action wins automatically). Value:
  `{ file, chapter_number, chapter_title, status, units_done, total_units, ts }`,
  `status ∈ {completed, untracked}` (renamed from "set_aside" 2026-07-04 to match the app's
  track/untrack vocabulary). `units_done`/`total_units` stamp progress so each row can draw a
  completion bar.
  `readHistory` / `recordHistory` / `hasHistory`. **localStorage only for now** (matches the
  lesson pointer's status, CLAUDE.md §9) — gains a server mirror like `sectionState.js` in Phase 4
  so history follows the teacher across devices. Deliberately NOT cleared by `clearBinding` —
  untracking must not erase the record that a chapter was once taught.
- **The anti-noise gate (founder's rule):** a chapter enters history only when it earned its place
  — **≥1 learning unit marked complete** before it left. Completed chapters always qualify (all
  units done); an untracked chapter qualifies only if the pointer advanced ≥1. Casual attach→untrack
  with no progress logs NOTHING. The gate lives in `MyPlans.jsx` where the pointer is known
  (`unitsDoneFor()` = raw pointer index): `untrackChapter(sectionKey, plan)` logs `untracked` only
  if `unitsDoneFor≥1`; `moveOnFromCompleted(c, sectionKey, plan)` always logs `completed`.
- **UI:** a small history glyph (clock + counter-clockwise arrow SVG, `HistoryIcon`) stacked BELOW
  the card's action button in a `.sc-right` column, shown ONLY when `hasHistory` is true (the
  current still-bound chapter is not "history"). Kept **conditional, not always-visible** (founder
  confirmed "ok now"). Tapping it opens `historyModal` — an instant popup (reuses `.ap-overlay`/
  `.ap-modal`) listing one row per chapter, newest first, with the current bound chapter overlaid
  LIVE as "Ongoing"/"Completed" only if it has progress. Statuses carry the section-card palette
  plus a NEW **slate** code for "Untracked" (`.ch-untracked` #e7ebee/#566169) — a chapter untracked
  before finishing, distinct from warm completed-clay and cream not-started grey. Each row also
  shows a completion bar under the name — the section card's `.sc-rail`/`.sc-tick` reused (pine =
  completed units, ochre = current unit when ongoing), so history and cards read as one surface.

**The long-chapter-title standard (applies everywhere a title renders — cross-cutting).** Long
NCERT titles were breaking layouts. The fix + its rules:
- **Root cause = the flexbox trap:** a title in a flex row won't shrink below its own text width
  unless the parent has `min-width:0`, so it overflowed / shoved action buttons out. `.sc-body`
  already had `min-width:0`; the `.sc-title` clamp now actually engages.
- **Anchor on the NUMBER, clamp the title.** The chapter number is the stable identity, so it's
  folded into the kicker (`Science · Ch 12`) where it never truncates, and the bare title clamps.
  Section cards + My Lessons share `.sc-title` → **2-line clamp** applied once covers both.
- **Two title FORMS (founder's standardization):** (1) **popup lists** (the "+" track picker and
  the history popup — untrack is a single-chapter confirm, exempt) use a **stacked row**: a meta
  line on top (**just `Ch NN`** now — subject/grade REMOVED 2026-07-04 since the modal header
  already shows subject·grade·section) with the Track action / status pill pinned to its right end,
  and the chapter NAME below spanning full width across up to 2 lines, truncated beyond. Shared
  classes `.ch-row/.ch-meta/.ch-meta-tx/.ch-name/.ch-act/.ch-pill` in `globals.css`; `.ap-row`
  restructured from the old horizontal `[CH | name | Track]` strip. (2) **screen bodies** (My
  Lessons) keep their structure, just cap the title at 2 lines.
- **Never truncate the reading surface** (LessonView shows the full title). Hover `title=""` is a
  desktop-only extra — NOT relied on (phones have no hover); full text comes from the picker's
  2-line wrap and from opening the lesson.

**My Lessons wheel tweaks (founder, `.mlp2` scoped):** the **Class number left-aligned** (was
centred) with a 28px inset — centre-aligned, the number sits under the rolling finger and vanishes;
inset-left keeps it visible beside the thumb. **▲▼ cue arrows tightened** (`.mlp2 .fr-wheel-cue
{gap:0}` + `.fr-wheel-cue-btn{height:21px}`) — the button BOX height, not the gap, is what spaces
the glyphs apart.

All of the above is **static-verified only** (Babel-parse clean via a temp `@babel/parser`, CSS
braces balanced, class/prop greps) — the sandbox still can't `next dev`. Live render + mobile pass
(360×800 first) is the founder's local must-do: confirm the history glyph appears after a
taught-then-untracked chapter, slate reads distinctly, and long titles clamp without shoving.

## 2026-07-03 — My Lessons rebuilt to the My Classes idiom + section-state corruption bug fixed

**My Lessons (`MyLessonPlans.jsx`) redesigned, scoped to ONE class at a time.** The founder's
insight: a teacher opens this tab with one class in mind ("what's left to prepare for VI
Science"), so showing all grades/subjects at once is cognitive overload — scope to a single
subject·grade and give the whole body to that list. What shipped:
- Header **"Your lessons"** at the `dash-title` size (mirrors My Classes' greeting), then
  **Subject + Grade as the first-run `RollWheel`s** (from `wheels.jsx`) side by side — only the
  subjects/grades she teaches; a single-option axis shows a static box, not a pointless wheel.
  Both default to the first entry. Header is a **frozen (sticky) band**; the lesson list scrolls
  beneath. No scope-repeat header, no "N of M prepared" meta (removed at founder's request).
- Cards **reuse `.sc-card`** verbatim so size/shape match the "pick a chapter" section cards.
- **Card colour = teaching lifecycle lifted from section to lesson** (the chosen basis): sage
  rail = ready to teach (on the shelf, distinct from My Classes' grey "not started" — a prepared
  lesson isn't unstarted), green (`st-going`) = any section teaching it now, clay (`st-done`) =
  all engaged sections done and none live. Precedence: teaching-now wins over completed.
- **Status line is EXHAUSTIVE and single-colour** (founder: don't colour completed differently —
  looked odd): "Completed 6A, 6C · Teaching now 6B, 6D", completed first; fully done reads all
  sections. Read from the same server-backed section cache My Classes writes (`readLocalSection`),
  so the two tabs always agree. Section tags are already stored as "6A" in readiness.
- **Tap a card = read-only `LessonView` (preview)**; PDF attachment later. NO per-section
  drill-down (that's the section card's job) and the old **Track button is removed** — attaching
  a lesson to a section now happens only via the "+" on My Classes cards. `SectionProgress.jsx`
  is now dead code (like `SidebarNav`/`MyCalendar`). `onOpenSection` prop is unused but still
  passed by `page.jsx` (harmless). Empty state: "There are no lesson plans prepared for {subject}
  · {grade} yet." with the Prepare CTA ALWAYS present below, in every state.
- New CSS lives under `.mlp2-*` in `globals.css` (frozen header, wheel row, static box, sage
  shelf accent, single-colour status). Verified statically only (sandbox can't `next dev`).

**Founder tweaks to My Lessons — DONE 2026-07-03 (items 1 & 2; item 3 was blank/dropped):**
1. **"Your lessons" header aligned to My Classes' greeting.** It sat 8px low because My Lessons
   renders inside `.editflow` (`padding-top:8px`) while My Classes doesn't — cancelled with
   `.mlp2 { margin-top:-8px }`. Title was already `.dash-title` spec (Fraunces 500 / 23px); added
   the mobile `.mlp2-title{font-size:20px}` under the 600px breakpoint to match `.dash-title`.
2. **Compact Subject/Class wheels.** The `RollWheel` height is hard-tied to `WHEEL_ROW=64` (row
   height === scroll-snap step, or snapping lands between rows), so shrinking the CSS alone would
   break it. Added a backward-compatible **`rowPx` prop** to `RollWheel` (`wheels.jsx`) that sets
   both the container + row height AND the scroll math; first-run passes nothing → stays 64. My
   Lessons passes `rowPx={48}`; `.mlp2-static` reduced to 48 to match. Arrows sit naturally closer
   at the shorter height.
3. Founder's list cut off at "3." with no content — nothing to do.

**NAMING CONVENTION (cross-cutting, honour everywhere user-facing) — "Class", plain numbers:**
The teacher's word is **"Class"**, never "Grade", and the number is **Arabic, never Roman**
("Class 6", not "Grade VI"). Readiness still STORES the grade as Roman ("VI") — convert to the
display number only at the UI boundary (`classNum()` map in `MyLessonPlans.jsx`: iii→3 … x→10).
Wheel layout (refined 2026-07-03): **Class** wheel = short number, **centred**; **Subject** wheel
= **left-aligned + auto-fit font** (new opt-in `fit` prop on `RollWheel` measures the longest
option via an offscreen canvas at the base/bold size and shrinks the label so a long word like
"Mathematics" never clips on a narrow phone column — first-run passes no `fit`, unchanged). The
settled/chosen value renders **bold** (`.fr-wheel-row[aria-selected] .fr-wheel-label`).

**SCOPE RULE — Subject restricted to hers, Class is NOT (2026-07-03).** In My Lessons the Subject
wheel offers only `readiness.subjects[]` (what she teaches), but the **Class wheel offers every
class Aruvi has CONTENT for** in that subject (`useSupportedGrades(subject)` — a superset of her
taught classes), so she can browse/prepare for a class she doesn't currently teach. Picking a
class with no prepared LPs falls through to the empty message + always-present Prepare CTA. The
per-section status line only has sections when the chosen class IS one she teaches
(`taughtGradeObj`); a non-taught class shows every lesson as "Ready to teach" (no sections).

Apply the Class/plain-number rule to any NEW surface too — the older screens (Allocate, first-run,
TeachingProfile) still say "Grade"/Roman and are candidates for the same cleanup when next touched.

**Section-state corruption bug (data-loss) — root-caused and fixed.** Symptom: after marking a
chapter complete, all My Classes cards flashed correct status then reverted to "pick a chapter".
Cause chain: `markComplete` fires two rapid fire-and-forget POSTs (pointer, then done); the file
repo did a **non-atomic** read-modify-write of one shared `state.json`, the two writes interleaved
and left a stray `}` → invalid JSON → server `_read` silently falls back to `{}` → GET returns
empty → the client reconcile treated "server empty" as "untrack everything" and **deleted every
local binding**. Fixes (all shipped):
- **Server writes now atomic** — temp file + `os.replace` (+ fsync) in
  `section_state_repository_file.py`; concurrent writers can't tear the file. Verified under
  40×15 concurrent writes.
- **Process-level `threading.Lock`** around the read-modify-write — atomicity alone still let
  writes to DIFFERENT sections lose each other's rows (stress: 40→13 survived; with the lock,
  40→40). One module-level repo instance → the lock is process-wide. Multi-instance deployment
  moves this to a DB row-lock (Supabase, CLOUD_DATA_MODEL §2.4).
- **Client reconcile hardened** (`sectionState.js` `pullSectionState`): a WHOLESALE-empty server
  response now deletes NOTHING (keeps local optimistic state) — only a NON-empty payload clears
  the keys it omits (genuine cross-device untrack). Guard var `serverEmpty`.
- Repaired the live corrupt `data/section_state/Kumar1/Kumar1/state.json` (both sections restored
  via `raw_decode`). **Carry-forward:** the section-state POST is fire-and-forget + full-snapshot;
  never assume ordering between the pointer and done pushes — the last write wins, so keep
  `setDone` firing after `writePointer` on the completion path. Restart uvicorn to load the repo
  change (Python).

**Follow-up 2026-07-03 (same bug, second episode) — RESTART-REQUIRED gotcha + self-heal read.**
The file corrupted AGAIN after the first repair, and one device (the phone) never recovered while
the Mac did. Root cause: **a Python server-code change is NOT live until uvicorn is restarted** —
the running process was still the OLD non-atomic writer, so normal use re-corrupted the file, and
the OLD `_read` still returned `{}` on the corrupt file. Two lessons, both now permanent:
- **Always restart the API after editing anything under `api/` or `aruvi_core/`** (no auto-reload
  in the run recipe). A repaired data file + un-restarted server = it just corrupts again. The web
  side is different — Next dev hot-reloads, but a fix only reaches a device after that device
  RELOADS the page (localStorage is per-device; a server repair doesn't heal a client — the client
  must re-pull the good state into its own cache). A device that can't reach the API (wrong LAN IP,
  server down) or is signed in under a different **case-sensitive** user id (`Kumar1` ≠ `kumar1`,
  a different tenant) will look "not recovered".
- **Self-heal read added** (`section_state_repository_file._read`): on `JSONDecodeError` it now
  `raw_decode`s the valid leading object instead of returning `{}`, so the classic stray-brace
  corruption can no longer wipe a device even before the atomic-write fix is deployed. (Note the
  2nd corruption truncated INSIDE the file, so only 1 of 2 sections survived salvage — the other
  was restored by hand from the known-good values. Salvage recovers the valid prefix, not
  necessarily every row.)

**My Lessons remembers its Subject + Class across tab switches (2026-07-03).** The tab reset to
the first subject/class every time she toggled to My Classes and back, because the component
unmounts on tab switch and re-initialised to defaults. Fixed by persisting `activeSubject` +
`activeGrade` to localStorage (`mylessons_subject` / `mylessons_class`), restored on mount (falls
back to first taught subject/class on first visit; a stale saved class is harmless — the RollWheel
self-corrects). She flips between the two tabs to pick chapters, so the selection must be sticky.

## 2026-07-02 — THE CALENDAR PURGE: day-organization is a category error; nav = two centre tabs

A design conversation with the founder overturned the day/week framing that had crept into the
product, and the first slice of the restructure is now implemented. The reasoning, so no future
session re-invents the calendar:

- **The core insight: the timetable is cyclic, the pointer is cumulative.** A teacher's calendar
  repeats identically every week; her curriculum progress never repeats. Housing cumulative
  state (the section pointer) inside a cyclic container (weekday buckets) constantly asserts
  something the content doesn't — if 6A's card sits under "Monday" and she didn't advance the
  pointer, the app displays a falsehood that reads as an accusation. Tuesday's content for a
  section is CONTINGENT on Monday's outcome, so a forward-looking week view can only ever render
  one truthful day. Aruvi's organizing question is **"where did I stop?"**, never "what is due".
  An app that makes no claims about her schedule can never be wrong about it (substitutions,
  exam weeks, sports day — no reconciliation class of bugs exists at all).
- **How the calendar crept in (genealogy, for vigilance):** time entered legitimately ONCE, as
  allocation arithmetic (weekly grid → period supply → effort-index distribution). The input
  then mission-crept into an interface (grid on screen → week view → "My Week is Home" →
  day-bucketed cards). Watch for this pattern; the only time-facts Aruvi keeps are NUMBERS
  (periods/week, durations, annual budget), never a grid of days.
- **Aruvi's product story, restated:** a lesson-plan artifact tool (constitutions = the IP). The
  section card is her working copy of the plan; the pointer is her pen mark; five cards replace
  five PDF printouts. The profile accretes as a by-product (progressive acquisition unchanged).

**Implemented this session (deliberately scoped by the founder — no more, no less):**
1. **FirstRun.jsx** — arrange-week step REMOVED (WeekGrid/DurationEditor/DateBadge/BenefitIcon
   components deleted; sectionCards is now the final screen, CTA "Go to my classes →"). The
   canonical payload still ships `grids[]` all -1 for readiness-shape compat; DAYS survives
   only to shape that.
2. **page.jsx** — sidebar/hamburger/drawer/My Week/Calendar ALL GONE. Nav = **two centre tabs,
   all viewports** (`.bottom-tabs` no longer mobile-only): **My Classes** (home, editFlow null)
   and **My Lessons** (renamed from "Lesson Plans"; = MyLessonPlans). Teaching profile
   (MyClasses.jsx) parked behind a header **settings gear** (`goProfile`); Generate is reached
   only via "+ Prepare Lesson" (a verb — never a tab). SidebarNav.jsx + MyCalendar.jsx are now
   DEAD CODE on disk (unimported), like Generate.jsx.
3. **MyPlans.jsx (home)** — day buckets/`daylabel`/"today floats first" logic deleted; FLAT
   list of section cards (`.sc-card` in globals.css): serif section tag · subject kicker ·
   "Ch N — title" · **LU progress rail** (done=pine, current=ochre, remaining=hairline) ·
   "LU n of N" meta. NO dates, NO pace pills. Phase-level (within-LU) marking is specced in
   the conversation but deliberately NOT built yet.
4. **api/main.py** — `GET /plans/{subject}/{grade}` now enriches each listing with
   `total_units` (recursive LU count via `_count_units`, same flatten as LessonView.jsx) so
   the card rail doesn't fetch every view. Verified against real data (science vii ch_02 → 7,
   english vii ch_01 → 5 incl. nested groups).

**Verified:** acorn-jsx parse clean on all touched JSX (use `web/node_modules/acorn`+`acorn-jsx`
— no @babel/parser in the sandbox), CSS braces balanced, `py_compile` + tests pass
(test_api needed `pip install fastapi httpx2 --break-system-packages` in the sandbox; the
failure was environmental, not ours). Live render + mobile pass still pending locally (§11).

**Approved-but-not-built (from the same conversation, in order):** phase-level pointer ("mark
the last phase you covered" — needs stable phase IDs at generation time, same requirement as
Period Notes), pace-against-allocation on the card (periods consumed vs allocated).
Mockups of all of this live in the Cowork conversation (2026-07-02).

**Same day, second slice — TeachingProfile (Settings) built; MyClasses editor retired:**
- **Copy:** first run now asks "What do you teach?" / "Which class do you teach {Subject} to?"
  (statements of fact, not intent). The redo flow uses the plurals ("What subjects…", "Which
  classes…").
- **wheels.jsx** (new) — RollWheel + PickWheel extracted from FirstRun.jsx, imported by both
  FirstRun and TeachingProfile. ONE selection UI everywhere (founder rule: no multiple UI
  types). CSS class names unchanged (.fr-wheel*/.fr-sec-*), so the extraction is CSS-invisible.
- **TeachingProfile.jsx** (new, behind the settings gear) — VIEW (read-only cards per subject·
  class: sections · durations · ppw · ≈periods/yr) + REDO (conversational: subjects multi →
  per subject: classes multi → per class: sections → durations → periods/week → annual budget
  4-method estimator; existing answers PRE-TICKED; unticking a subject at Q1 removes it
  immediately) + DELETE (DELETE /readiness + clears `lu_pointer_*`/`current_chapter_*` from
  localStorage; lessons stay; page.jsx onDeleted flips ready=false → back through FirstRun).
- **Checkpoint semantics (founder spec):** each finished subject POSTs the merged canonical
  subjects[] to /readiness at the "subject saved ✓" interstitial → "Continue to {next} /
  Finish for now". She can leave AFTER any subject, never mid-subject (mid-subject state is
  component-local and simply evaporates).
- **Budget estimator without a grid:** Readiness.jsx's 4 methods derived periods/week from
  the weekly grid; grids are gone, so the loop asks the number directly and stores it as
  `periods_per_week` on the grade record (ADDITIVE schema field — older records lack it, all
  consumers tolerate that). weeks→ppw×w · periods→direct · days→ppw×d/6 · auto→ppw×30.
- **MyClasses.jsx is now dead code** (retired per founder decision — Settings shows view +
  Redo + Delete only). page.jsx imports TeachingProfile instead.
- Verified: acorn-jsx parse clean (page, FirstRun, wheels, TeachingProfile, MyPlans), CSS
  balanced, DELETE /readiness endpoint confirmed present. Live render still pending locally.

**Same day, third slice — brand + tab placement (founder polish):**
- **One logo everywhere:** the brand dot is now upright and RED (#c0392b) in every surface
  (shared `.brand-row em` rule), matching the first-run welcome page; the shell header stacks
  "Aruvi." over the mono LESSON STUDIO tag exactly like first run.
- **Tabs moved from bottom to TOP** (under the header), centred (`.tabs.main-tabs`), reusing
  the ORIGINAL `.tab.active` treatment — clay-red underline — that the old My Plans/Generate
  tab row used. `.bottom-tabs`/`.bt-item` CSS removed; body no longer pads for a fixed bar.
- **No tab-name echoes:** the "My Classes" / "My lessons" kickers inside the two tab bodies
  are removed — the active tab already says where she is.

**Same day, fourth slice — TeachingProfile REBUILT as accordion + granular editing (founder
iterated past the redo/delete design within hours; the "second slice" description below is
historical):**
- **Accordion:** one subject (and its classes) open at a time; collapsed rows show just the
  name + class count. **Master Edit toggle** (top right) reveals ALL mutation controls at
  once; view mode is clean data only, no prose.
- **Granular ops:** red dustbin (inline SVG, #c0392b) per subject / class / section chip;
  each behind ONE scoped confirm naming exactly what goes + "lessons stay in the library".
  Removals cascade upward (last section takes its class; last class takes its subject),
  clear the removed sections' lu_pointer_*/current_chapter_* keys, and RE-KEY the per-index
  budget map (rekeyBudget — budget is keyed by grade index, so any structural change must
  re-key or budgets silently attach to the wrong class).
- **Structure vs values rule:** tree things (subject/class/section) are added/removed in
  place — green .tp-add buttons (+ section · + add a class · + add a subject, pine bg);
  numbers (duration · ppw · budget) open the SAME single-question wheel screens, prefilled,
  as a 3-step edit → Save. Add-a-class asks questions ONLY for the new classes (pendingIdxs
  mechanism); add-a-subject runs the full per-subject loop with the "saved ✓ — continue /
  finish for now" checkpoint between multiple additions.
- **REMOVED: "Delete profile" and "Redo whole profile"** (and the delete→redo flow from the
  second slice). The profile is only ever edited at a point. Emptying it entirely (deleting
  the last subject) leaves the "+ add a subject" button; server profile empties via the same
  POST /readiness full-replace.
- **Delete profile → straight into rebuild:** after the warning + deletion, she lands
  DIRECTLY in the same conversational flow "Redo profile" opens (nothing pre-ticked). The
  shell stays open — `ready` untouched, onDeleted prop removed from TeachingProfile/page.jsx;
  a signed-out return without rebuilding still hits first run naturally (server profile gone).
- **First-run handoff is now DIRECT** (founder: a "Go to my classes →" button is meaningless
  to someone who has never seen the shell). creatingCards beat → finishActivation, landing
  straight on the My Classes home; the interstitial sectionCards screen + LessonCard component
  are deleted. **Bug fixed en route:** nothing ever wrote `current_chapter_{sub}_{grade}_{tag}`
  (MyPlans reads it to bind a chapter to a card), so post-first-run cards showed empty
  "pick a chapter" states — finishActivation now binds the previewed plan's filename to every
  fan-out section, so she lands on cards already carrying her lesson.

## 2026-07-01 — English Grade VIII Unit→true-chapter split (audit found + replaced a stale prior attempt)

Repeated the VI/VII true-chapter split for Grade VIII. Unlike VI/VII, this one started from a
**discovered, undocumented, stale prior attempt** — worth reading in full before trusting any
similar staging folder found in future sessions.

- **What was found before any new work started:** `data/content/chapters/english/viii/
  {summaries_split,mappings_split}/` already existed (15 files each, all timestamped earlier the
  same day, before this conversation's own edits). Live `summaries/`/`mappings/` still held the
  original 5 unsplit Unit files — so a split had been staged but never cut over, and neither
  MEMORY.md nor CLAUDE.md had any record of it (`data/` is git-ignored, so no commit trail
  either). Auditing the staged files' `effort_signals` showed fractional values (e.g.
  `spine_load: 1.0, task_density: 0.3, writing_demand: 0.3, project_load: 1.0, effort_index:
  4.0`) — NOT the integer 1–3/0–2/0–3 tiers the current Step 7d methodology produces. Structurally
  it matched (`_source_unit`, `page_share_of_unit`, etc.) but the effort-index formula was clearly
  an earlier/different one, quite possibly the page-count-weighted proration the script's own
  docstring flags as explicitly rejected for VI. **Deleted both stale staging folders and redid
  the split from scratch** rather than trust or repair the old output.
- **Tier-cutoff audit:** VIII's raw `task_density` distribution (2.67–4.33 across 15 sections) is
  narrower and shifted higher than VI (1.67–3.83) or VII (1.83–4.17). Reusing VI/VII's cutoffs
  (≤2.0/2.1–2.9/≥3.0) never reaches tier 1 at all for VIII — pins 11/15 chapters at tier 3,
  collapsing task_density to an effectively binary (2-or-3) signal. A recalibrated cutoff
  (≤3.0→1, 3.1–3.4→2, ≥3.5→3) would restore real 3-tier use (5/6/4 split), though both options
  land on 7 distinct `effort_index` values overall (11.5–16.5). Presented both to the user —
  **decision: reuse VI/VII's cutoffs unchanged anyway**, accepting the weaker task_density
  discrimination for a single shared config across all three grades. `split_english_chapters.py`
  needed NO changes (already in its VI/VII single-cutoff form). `spine_load` is degenerate for
  VIII too (all 15 sections use all 6 spines).
- **Split + verify:** ran `python3 aruvi-scripts/split_english_chapters.py viii` into staging;
  verified valid JSON, sequential 1–15 numbering, title format, and NCF allocation
  (`ncf_total_periods('english','middle')` = 157) sums exactly to 157 with a compressed but real
  spread (9–12 periods per chapter — narrower than VI/VII's spread, consistent with VIII's own
  compressed effort_index range).
- **Cutover:** done — old 5 Unit-level files deleted, staged files moved into live
  `summaries/`/`mappings/`, each mapping's `summary_path` corrected `summaries_split/` →
  `summaries/`, staging folders removed.
- **Saved-plans — a NEW wrinkle vs. VI/VII:** `data/content/saved_plans/english/viii/` had **two**
  separate whole-Unit saved plans, both for Unit 2 "Values and Dispositions" (true chapters
  4/5/6) — `ch_02_20260519_122152.json` (12 periods) and `ch_02_20260609_101904.json` (11
  periods) — two independent generation runs of the same Unit, not two different chapters (a
  first pass at reading period counts alone could mistake this for a genuine duplicate-chapter
  bug; a full section_id walk on both confirmed they cover identical sections A/B/C). Asked the
  user how to resolve the duplicate before touching anything: **decision — keep only the newer
  2026-06-09 run, discard the 2026-05-19 one entirely.** Split the kept file into `ch_04`/`ch_05`/
  `ch_06` (periods renumbered per chapter, `coverage_handoff`/`assessment_items` filtered by
  section_id, homogeneity-checked same as VI/VII); period counts reconcile (5+4+2=11 orig). Both
  original whole-Unit files (kept-then-split, and discarded) deleted.
- **Process note for future grades:** when a `summaries_split`/`mappings_split` staging folder is
  found already on disk, don't assume it's this session's own leftover or safe to cut over as-is
  — check `effort_signals` for the right *shape* (integer tiers, not fractions) before trusting
  it, since the workspace folder persists across sessions and past undocumented attempts can
  linger silently.
- **Doc gap flagged (not yet fixed):** `cowork prompts/english/middle/step_1_chapter_summary_and_
  mapping.md` Step 7d's "Verified 2026-07-01" note still only cites the Grade VI calibration
  (16 chapters, 4.5–16.5) — it hasn't been updated to note that `task_density` is the one signal
  requiring a per-grade raw-distribution audit before reuse (VII reused VI's numbers after
  checking; VIII reused them too despite a weaker fit). Worth a doc update next time this file is
  touched, so a future read doesn't assume the VI numbers are grade-invariant by default.

## 2026-07-01 — English Grade VII Unit→true-chapter split (repeat of the VI process)

Repeated the VI true-chapter split (§CLAUDE.md, `aruvi-scripts/split_english_chapters.py`) for
Grade VII, per the standing handoff. Live now: `data/content/chapters/english/vii/{summaries,
mappings}/` hold **15 true chapters** (5 Units × 3 sections each), numbered/titled the same way
as VI (`"<section title> (<unit title>)"`).

- **Tier-cutoff audit (Step 1):** extracted VII's raw per-section signals and compared applying
  VI's existing chapter-scale Step 7d tiers unchanged vs. a VII-recalibrated `task_density`
  (VII's raw avg range 1.83–4.17 vs. VI's 1.67–3.83, so VI's cutoffs left 8/15 chapters tied at
  the top tier vs. a possible even 5/5/5 split). Presented both to the user with a full table —
  **decision: reuse VI's cutoffs unchanged, no VII-specific retiering.** `spine_load` is fully
  degenerate for VII (every chapter uses all 6 spines, tiers to 3 for all 15 — more so than VI,
  which had one 2-cell outlier); `writing_demand`/`project_load` already sat on VII's natural
  data breaks. Result: `effort_index` spans 7.5–16.5 across 8 distinct values, no collapse.
  `split_english_chapters.py`'s tier functions are therefore UNCHANGED from the VI version — the
  only edit kept was making `ROOT` derive from the script's own location instead of a hardcoded
  stale sandbox path (portability fix, unrelated to the tiering decision).
- **Split + verify (Step 2):** ran `python3 aruvi-scripts/split_english_chapters.py vii` into
  staging (`summaries_split/`/`mappings_split/`); verified valid JSON, sequential 1–15 numbering,
  title format, and that NCF period allocation (`allocate_for_subject` + `ncf_total_periods
  ('english','middle')` = 157) sums exactly to 157 with a real per-chapter spread (6–14 periods).
- **Cutover (Step 3):** done — old 5 Unit-level files deleted, staged files moved into the live
  `summaries/`/`mappings/` folders, each mapping's `summary_path` corrected from
  `summaries_split/` → `summaries/`, staging folders removed. (Files under the connected
  `aruvi-saas` workspace folder can't be `rm`'d without first calling
  `mcp__cowork__allow_cowork_file_delete` on a path inside the folder — needed once per session.)
- **Saved-plans loose end — RESOLVED for both VI and VII.**
  `data/content/saved_plans/english/vii/` held 2 pre-split test plans
  (`ch_01_20260510_175736.json`, `ch_02_20260512_122542.json`); `.../vi/` held 1
  (`ch_02_20260518_104012.json`). All three turned out to be **whole-Unit** plans (every true
  chapter's periods/coverage_handoff/assessment_items bundled into one file) — on first read
  VI's looked like it covered only one true chapter ("The Unlikely Best Friends"), but a full
  section_id walk showed it actually spans all 3 sections of the "Friendship" Unit (A/B/C =
  true chapters 4/5/6), same shape as VII's two. Sliced each by `section_id` (confirmed to align
  with new true-chapter order — VII: 1-2-3 and 4-5-6; VI: 4-5-6) into separate per-chapter saved-
  plan files: periods renumbered from 1 within each, `coverage_handoff` and `assessment_items`
  filtered to that section's entries only (empty spine/group keys dropped), `chapter_number`/
  `chapter_title` set to match the new mapping JSON exactly, filename keeps the original save
  timestamp with the new chapter number prefix. Period counts reconcile exactly in all 3 source
  files (VII Unit 1: 5+4+2=11 orig; VII Unit 2: 6+4+1=11 orig; VI "Friendship": 5+3+2=10 orig).
  Old whole-Unit files deleted in both grades. **No open saved-plans loose end remains for
  English VI or VII** — worth re-running this same section_id-walk check (don't trust content
  from a partial read) on any grade/subject that gets a Unit→true-chapter split in future.

## 2026-07-01 — Strategic pivot: mobile-first, progressive-acquisition model (Phase 0)

### What changed (direction, not code yet)
- Adopted the **mobile-first progressive-acquisition model** (`docs/Aruvi_Mobile_First_
  Progressive_Acquisition_Model_v0.2.md` + `docs/mobile pics/`) as the standing direction.
  Recorded in **CLAUDE.md §0** (new, read-first banner) with pointers added to §9 and §11.
- **Core reframe:** OLD Profile→Allocate→Generate→Track becomes NEW Generate-first-lesson →
  attach-to-sections → (optional) arrange-week → teach → profile accretes as a by-product.
  Principle: **benefit first, data second.** Engine/plugins/view-model/ports UNCHANGED — this is
  interaction re-sequencing + a mobile-first reflow only.
- **Two phases:** Phase 1 = shell-less "Guided First Experience" (no sidebar/tabs/nav until a
  lesson is generated + attached to ≥1 section + week arranged-or-skipped). Phase 2 = workspace
  shell opens (activation moment): hamburger sidebar, **My Week = Home** (auto-opens to today),
  Generate tab replaced by universal **+ Prepare Lesson**.
- **Dev workflow decision:** development moves to **Chrome + mobile DevTools device mode**,
  mobile-first then desktop. Stress-test **360×800** (Indian budget Android; custom preset, UA
  type = Mobile), then 375 (iPhone SE) / 390 (iPhone 14) / 412 (Pixel 7). Final iPhone pass in
  real iOS Safari for safe-area/`100vh`/sticky-header quirks Blink won't reproduce. `next dev`
  still can't run in the Cowork sandbox → live render + mobile checks are local.

### Component audit — reuse map (existing `web/app/components/` vs new IA)
- **Reuse ~as-is:** `LessonView.jsx` (before/after-complete matches the LP-view mockups),
  `ViewModelView.jsx`, `PeriodRows.jsx`, `StatePill.jsx`, `AllocationReportView.jsx`,
  `SectionProgress.jsx`, `Login.jsx`.
- **Reuse, re-sequenced / re-skinned:** `MyPlans.jsx` → **My Week / Home** (already the weekly
  dashboard grouped by day; needs mobile reflow + "auto-open today"); `MyLessonPlans.jsx` →
  **repository** (already subject→grade→chapter); `MyClasses.jsx` → **progressively-filled
  profile** (already the editable subject→grade→section drill-down); `MyCalendar.jsx` → Calendar
  (add the benefit-first empty state); `Allocate.jsx` → keep its generate path, but surfaced via
  **+ Prepare Lesson** not a tab; `SidebarNav.jsx` → hamburger sidebar (already has My Class /
  Calendar / My Week / Lesson Plans + Settings/Help — close to the mockup).
- **Harvest pieces, retire as a gate:** `Readiness.jsx` (the upfront 6-step wizard) is **retired
  as the entry point**; its duration editor / section multi-picker / weekly grid are lifted into
  the progressive first-run + My Class.
- **Net-new (the real work):**
  1. **Shell-less Phase-1 wrapper + activation gate** — `page.jsx` currently renders the shell
     (header + tabs + rail) immediately after Login; the new flow must suppress ALL shell until an
     activation flag (lesson generated + attached to a section) flips. That gate is the single
     biggest structural change.
  2. **Section-card fan-out** — "Add to Class" → multi-select section picker → one independent
     lesson card per section. Does NOT exist today: sections are currently implicit from the
     readiness profile, and MyPlans derives cards by day. This is the activation mechanism.
  3. **+ Prepare Lesson** universal action (replaces the Generate tab as a destination).
  4. **Mobile bottom-tab bar** (My Week / My Class / Calendar / Lesson Plans) per the mockups —
     distinct from the current desktop left rail.
  5. **Benefit-first Calendar empty state** ("your calendar is waiting for a little more info").
- **Deferred but specced (note now):** Period Notes (section plan-instance, pull-based, 📝) and
  Chapter Notes (shared plan asset, Chapter Organization page, chapter-end prompt). Needs stable
  per-plan period identifiers; notes never migrate across regenerated plans.

### Carry-forwards
- `page.jsx` is the pivot's center of gravity: the `tab` state + `TABS` array + the `navOpen`
  rail all assume the two-tab shell. The activation gate replaces `ready`-gates-Generate with
  `activated`-gates-the-whole-shell. Don't delete the reused components — re-wire the router.
- Keep the §4 "scholarly planner on warm paper" system (Fraunces / Newsreader / IBM Plex Mono,
  warm palette) intact — the mockups already use it; warmth comes from words + pacing, not a new
  visual language. This is a reflow, not a rebrand.

## 2026-06-28 — Persistence + tenanting + self-contained `data/` + repo cleanup

### What changed (big session — see CLAUDE.md §5/§7/§9/§11)
- **User-ID login portal** (`web/app/components/Login.jsx`) now gates the app. No password
  yet: the ID is stored in localStorage and sent as the **`X-Aruvi-User`** header on every
  API call (`format.js` `withUser()` wraps fetch). Server `_current_identity()` reads it;
  `tenant_id == user_id` (one teacher = one individual tenant). Phase-4 swaps for Supabase Auth.
- **Readiness is now server-persisted** (was front-end only — that gap is closed). New
  `ReadinessRepository` port + file adapter; `/readiness` GET/POST/DELETE. Profile survives
  refresh/restart/new browser. Stores ONLY canonical `subjects[]`; the denormalized projection
  is stripped on save and regenerated on read via `projectReadiness()` (format.js).
- **Allocation register made tenant-keyed** (it was NOT — a real multi-tenancy hole: all
  teachers shared one register per subject·grade). Threaded `tenant_id/user_id` through the
  `AllocationRepository` port → file adapter → engine fns → API routes. Path is now
  `allocations/{tenant}/{user}/{subject}/{grade}/allocation.json`.
- **Self-contained `data/` root.** Content copied prototype-mirror → `data/content/`
  (`ARUVI_DATA_DIR` default); state at `data/` (`ARUVI_STATE_DIR` default). Both repo-derived,
  no machine hardcoding. **App no longer reads the prototype mirror at runtime.** Two seams in
  `api/config.py`: `DATA_DIR` (Bucket A content) vs `STATE_DIR` (Bucket B state).
- **Repo cleanup/reorg.** Purged junk (`out/`, `web/.next/`, caches, `.DS_Store`, `others/`);
  consolidated design docs under `docs/` (incl. `docs/mockups/`, `docs/architecture-plan.md`).
  All moved-file references were comment/doc-only (no code paths) — rewritten to new paths.
- **Tests:** added `test_readiness.py` + rewrote `test_allocation.py` (tenant isolation, new
  signatures, redraw-ready record schema); fixed stale `/health` assert in `test_api.py`.
  **Full suite 11/11 green.**

### Key decisions / carry-forwards
- **`tenant_id == user_id` is the deliberate stub** until Supabase Auth. Every Bucket-B record
  already carries both keys, so Phase-4 is a value swap in `_current_identity()`, not a schema
  change. Grep invariant (CLOUD_DATA_MODEL §5): no teacher data without a tenant key.
- **Never persist the readiness active-subject projection** (subject/grades/grids/durations/
  budget top-level keys) — derived sugar, regenerated on read. The file adapter strips it
  defensively even if the frontend sends it.
- **Sandbox cannot DELETE files in the mounted repo** (`Operation not permitted`) — only
  create/overwrite. So destructive cleanup must be a script the USER runs on their Mac
  (`tidy_repo.sh` was the vehicle this session). `clear_*` adapter methods fall back to
  overwriting-empty when unlink is blocked, so resets never 500.
- Current dev data is under user **`Kumar1`** (`data/readiness/Kumar1/…`, `data/allocations/Kumar1/…`).

### Verification limitation (unchanged, still important)
- Web/React changes are verified **statically only** (sandbox can't run `next dev`). The full
  login→readiness→allocate→teach loop must be smoke-tested locally at desktop + mobile widths.
  Local run is now `python3 -m uvicorn api.main:app --port 8000; npm --prefix web run dev`
  with **no `ARUVI_DATA_DIR` needed** (defaults to `data/content/`).

## 2026-06-27 — Planning-layer rebuild (web app restructured to the finalized flow)

### What changed
- Web app went from **3 sibling tabs** (Allocate / Generate / My Plans) to the finalized
  **two-tab, readiness-gated, hub-and-spoke** flow. Spec: `docs/mockups/index.html`
  + `docs/aruvi_saas_full_lifecycle_flow.png`. Full architecture documented in **CLAUDE.md §11**.
- New components: `Readiness.jsx` (ported from `readiness-grid-flow.html`), `GenerateTab.jsx`
  (readiness gate + folds in Allocate), `LessonView.jsx` (Learning-Unit lesson view +
  assessment artifact). Rebuilt: `MyPlans.jsx` (weekly dashboard). Reshaped: `Allocate.jsx`
  (added G2 hub `final` step, G7 `generate` spoke, G4 total-periods model, G5 howbox).
- `Generate.jsx` (old thin component) is now **dead code** — not imported; safe to delete later.

### Key decisions / carry-forwards
- ~~**Readiness state is front-end only**~~ **(SUPERSEDED 2026-06-28: now server-persisted +
  tenant-keyed via `/readiness`; see top entry.)** Original note: lived in `page.jsx`, threaded
  to GenerateTab/MyPlans. Still front-end-only: the **LU pointer** (`localStorage` key
  `lu_pointer_{sectionKey}`) — next to migrate.
- **G4 weekly ratio** comes from the readiness grid (`weeklyRatioFromReadiness`) and splits the
  single total-periods input via `splitByRatio` (largest-remainder — unit-tested, always sums
  exactly). Falls back to period-rows when readiness data absent. Internally still writes into
  `rows` so the engine allocate call + persist + export path is unchanged.
- **Status belongs in My Plans, not Generate** (deliberate): started/in-progress/locked is
  execution state (the LU pointer); Generate only knows allocated vs. plan-made.
- **G7 generate spoke serves saved-plan previews** — live generation still deferred.

### Verification limitation (important, recurring)
- **The Cowork sandbox cannot run `next dev`/`next build`** — Next.js's arm64 SWC native
  binary fails to load, and the Google-Fonts `@import` stalls the build. So all web work this
  session was verified **statically only** (brace/export/prop-contract greps, CSS brace
  balance, unit-testing pure helpers). **None of Phases 1/2/3/5 has been live-rendered.**
  A local smoke test of the whole loop at desktop + mobile is the must-do before more UI work:
  `python3 -m uvicorn api.main:app --port 8000; npm --prefix web run dev`. (Stale as of
  2026-06-28: no `ARUVI_DATA_DIR` env var or sibling Project Aruvi folder needed anymore — the
  app defaults to the self-contained `data/content/` copy, per CLAUDE.md §7.)

### Deferred / parked
- **G6 selective-reset screen** not yet aligned to the mockup (still the old modal, not the
  G2-styled select-to-clear danger-zone screen).
- **Sample-plans pre-readiness surface** parked — it exposes only an LP, not the execution/
  My-Plans value; needs a better approach (mockups Screen S note).

## 2026-06-22  *(allocations note below SUPERSEDED 2026-06-28 — register is now file-persisted AND tenant-keyed; only the Supabase swap remains)*

### Allocations persistence (accumulation model)
- **What was built:** The Allocate tab now accumulates allocations — when a teacher allocates a second set of chapters, both sets persist in the Final view, not just the latest one.
- **Current scope:** In-memory during the session (state-based). Survives page navigation but resets on browser refresh.
- **Portability note:** When moving to Supabase, allocations must be persisted to the DB keyed by (subject, grade, user/teacher_id). Each allocation set should be a row with (chapter_numbers[], period_rows[], final_allocation_data). The UI `allAllocations` array becomes a DB query + cache in the API layer.
- **Migration path:** Add a `POST /subjects/{subject}/{grade}/save-allocation` endpoint in the FastAPI layer (api/main.py) that writes to Supabase. The web component calls it instead of just updating local state. Keep the in-memory `allAllocations` as a display cache during the session.

### Text updates (2026-06-22)
- Changed "AI Suggested Allocation" → "Suggested allocation" (line 248, Allocate.jsx)
- Changed period-definition subtitle to "To begin, set the total number of periods available and how long each period type lasts below." (line 370, Allocate.jsx)
