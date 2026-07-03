# Aruvi-SaaS — Accumulated Learnings & Carry-Forward Notes

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
