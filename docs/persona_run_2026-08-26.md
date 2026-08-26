# Persona Run — 26 August 2026 · What was found, what changed, where we are

The first time `docs/persona_test_checklist.md` was actually **driven** rather than read:
Claude in Chrome against the live API + web pair, `ARUVI_ENTITLEMENT_ENFORCED=1`, throwaway
mobiles `1234567890`–`98`, each identity erased before use.

**Headline:** **10 bugs found, 10 fixed.** 5 product decisions taken and built. 2 new
features (subscription confirmation email; academic-year cutover). All 13 suites green.
Every fix verified live, not statically.

**Read in this order if you are short of time:** PART A (the five bugs the persona run
found) → PART H (cutover, built and walked through a simulated June) → PART E (what is
still open).

**The lesson worth keeping:** almost every bug in this document was a **race, stale state,
or a wrong assumption about what the calendar would do** — the exact class of defect that
`babel-parse`, unit tests and even careful phone testing cannot reach. Several were
invisible on the happy path a developer walks. Two more specific rules earned the hard way
today: **a parse check is not a render check** (a TDZ error white-screened the whole app
while every static check passed), and **the founder's Mac runs Python 3.9 while the dev
sandbox runs 3.10** (a `X | None` annotation shipped green and refused to boot).
§11's "verified statically only" caveat is not a formality.

---

## PART A — BUGS FOUND (all fixed)

### A1. First run bounced back to the welcome screen after the first successful generation
**Severity: critical — it broke the product's single most important moment.**

- **Symptom.** Trial teacher completed first run, the plan generated fine (on disk, section
  bound, trial chapter counted) — and the screen went **back to "Welcome to Aruvi! … Prepare my
  first lesson"**. Only a page reload escaped it.
- **Cause.** `firstGenNeeded` in `page.jsx` asks the server *"has she ever generated?"*.
  Completing first run flips `ready` false→true, which **re-runs that check while the serve
  fired by `prepareAndHandOff` is still in flight**. The server truthfully answered "nothing
  prepared, nothing bound", so the heuristic **re-armed first run**. The plan landed ~0.3 s
  later; nothing re-triggered the check.
- **Fix.** A one-shot latch, `everGeneratedRef`. The question is "has she EVER generated?" —
  once this session has watched her do it, the answer can never revert.
- **File.** `web/app/page.jsx`
- **Verified.** Re-ran end to end on `1234567892`: handoff now lands on **My Lessons** with the
  real preparing card ("Preparing your 6 periods lesson plan…"), replaced in place by "Teaching
  now 3A", tour offer below.

### A2. That latch then leaked ACROSS TEACHERS
**This is your "direct subscriber went straight to My Lessons" — it was real, not your environment.**

- **Symptom.** A fresh subscriber paid and landed **straight in the shell**, skipping the guided
  first generation entirely.
- **Cause.** Signing out does **not** remount `page.jsx`, so the *previous* teacher's latch was
  still set and suppressed the *next* teacher's first run.
- **Fix.** `latchUserRef` — the latch belongs to one teacher and clears on identity change.
- **File.** `web/app/page.jsx`
- **Verified.** Clean re-test on `1234567893` (bought Science · Middle): lands on the **clean
  welcome** (no trial card), first run scope-filtered to **Science only**, **classes 6/7/8 only**,
  "We'll start you with Section 6A".
- **Standing rule now recorded in MEMORY.md:** *any ref caching a per-teacher answer must be
  keyed to the teacher, because sign-out is not a remount.*

### A3. A subscription that ran out BY DATE kept its productivity tools
**Severity: high — this is how every real lapse will happen once payments are live.**

| Gate | Revoked (`status: expired`) | Ran out by date (`status: active`, `valid_until` past) |
|---|---|---|
| Generation | 402 ✅ | 402 ✅ |
| Profile / tracking writes | 402 ✅ | **200 — allowed** ❌ |
| UI (My Classes tab, "+", edit pen) | hidden ✅ | **still shown** ❌ |
| Settings panel | ENDED ✅ | **"SUBSCRIBED"** ❌ |

- **Cause.** `_check_entitlement` tested `valid_until`; `_check_productivity` and the entire web
  half tested only the literal string `status == "expired"`. **Manual revocation is the rare
  founder-only case; date expiry is the normal one** — so the lockout would have missed nearly
  every teacher it was designed for, while generation was already refusing her.
- **Fix.** `GET /entitlement` now **derives** a `lapsed` flag (revoked **OR** date passed).
  `_check_productivity` uses the same rule; `page.jsx` and `Settings.jsx` consume the server's
  answer instead of re-deriving it. `active` explicitly excludes lapsed.
  **The duplication was the bug — one rule, one place.**
- **Files.** `api/main.py`, `web/app/page.jsx`, `web/app/components/Settings.jsx`
- **Verified.** `1234567895` (`--until 2025-01-01`) → `lapsed: true`, readiness write 402,
  identical behaviour to a revoke.

### A4. Renaming yourself did not change the name on screen
- **Symptom.** Saved a new name in Settings › Personal profile; server stored it, but the top-right
  and greeting kept the **old** first name until a reload.
- **Cause.** The account is fetched on `[user, entSyncTick]`; a profile save bumped neither.
- **Fix.** Settings bumps the tick on save (`onAccountSaved`).
- **Files.** `web/app/page.jsx`, `web/app/components/Settings.jsx`
- **Verified.** Live: **Priya → Anjali** the instant Save lands.

### A5. A shared email signed you into the WRONG account
**Found while verifying that sign-in accepts email as well as mobile.**

- **Symptom.** Two test personas happened to share `sita@example.com`. Signing in with that
  address resolved to **whichever account file sorted first on disk** — an arbitrary winner.
- **Why it matters.** Email became a **credential** the moment sign-in started accepting it, and
  a credential pointing at two accounts points at neither. Two real paths to it: two teachers at
  a school sharing an address, or — far likelier — **one teacher registering a second mobile with
  the same email**, quietly splitting herself into two accounts and then landing in whichever one
  wins the sort.
- **Fix, at both ends:**
  1. **Prevention** — `_guard_email_not_taken` refuses an address already held by a *different*
     account, on **both** checkout and Personal-profile save (409, plain wording). Re-saving your
     own address is always fine.
  2. **Safety net** — `find_by_email` returns `None` on ambiguity instead of guessing, and
     sign-in says *"More than one Aruvi account uses this email. Please sign in with your mobile
     number."* The mobile is always unambiguous.
- **Files.** `aruvi_core/adapters/account_repository_file.py` (new `find_all_by_email`),
  `aruvi_core/ports.py`, `api/main.py`, `web/app/components/Login.jsx`,
  `tests/test_account.py`
- **Verified live.** Mobile ✅ · unique email ✅ · `SITA@Example.Com` ✅ (case-insensitive) ·
  unknown email correctly refused ✅ · shared email → `ambiguous_email`, sign-in blocked ✅ ·
  attempting to take another account's address → **409** ✅.
- **Note for the field.** The file store cannot enforce uniqueness; the partner's DB adapter
  should add a **UNIQUE constraint on email** when Supabase lands. Prevention here makes new
  duplicates impossible; the ambiguity guard covers records that already exist.

---

## PART B — DECISIONS YOU TOOK, NOW BUILT

### B1. Trial plans stay reachable after subscribing to a different subject
> ★★ **REVERSED THE SAME EVENING (founder, on seeing it live).** *"The {x,y} stands there
> in My Lessons with no use, clogging the space for a trial reason that is no longer
> valid."* A subject she trialled and did not buy cannot be prepared in, tracked or given
> sections — every card of it is a door that no longer opens. On her FIRST purchase, the
> records those subjects left (prepared marks, section state, notes) are now purged; the
> shared plan files are never touched, and a subject she trialled and BOUGHT keeps
> everything. The paywall promise below was withdrawn with it — it now reads *"the
> chapters you made in a subject you subscribe to come with you"*, which is true on both
> paths. Kept here as written, because the reasoning was sound and only the screen
> outvoted it. See MEMORY.md 2026-08-26 (evening).
- **The problem.** The paywall promises *"Your 3 chapters stay yours"* — but
  `_apply_subscription_profile` dropped the out-of-scope subject, leaving those plans on disk
  with **no chooser entry able to reach them**. The promise was not kept.
- **Now.** An out-of-scope subject she has **prepared plans in** survives untouched, so she can
  open, export and print them. A subject with **no** plans is still a pure trial artifact and is
  still dropped. **Not** a licence to prepare more there.
- **File.** `api/main.py` (`_apply_subscription_profile`)
- **Verified.** Trial English teacher subscribes to Social Sciences → profile keeps **both**
  `Social Sciences:VI/6A` and `English:III/3A`. Preparing new English → **402 "covers a different
  subject"**; Social Sciences → **200**.

### B2. No guided tour when lapsed
The tour walks her through attaching, tracking and preparing — every one of which her lapse just
removed. Offering it would teach her the shape of a locked door.
`tourOnOffer` now requires `!entLapsed`. **File.** `web/app/page.jsx`

### B3. First run greets her by first name
She types her name at checkout and used to meet her **raw mobile** on the very next screen. Same
rule as the shell's bar: first name, capitalised; a numeric JIT default still shows the id.
**File.** `web/app/components/FirstRun.jsx`

### B4. Notes LOCK when lapsed
Previously left writable on the argument that a note is her own writing; you placed them in
Aruvi's **working half**, alongside the tracker and profile.
- `_check_productivity` now guards `POST /plan-notes`. **`GET` stays ungated** — every note she
  wrote is still readable and still exports with her plans.
- The modal opens **read-only**, footer reads *"Renew to write notes — what you wrote stays
  yours."*, only button is Close.
- **Files.** `api/main.py`, `web/app/components/LessonView.jsx`
- **Verified.** Lapsed write → 402 with her existing note untouched; lapsed read → works; active
  teacher → 200.

### B5. Sign-in accepts MOBILE or EMAIL only
No free-form user IDs at the front door. Enter stays disabled until the input is a 10-digit mobile
or a valid email shape; a registered email resolves server-side (`find_by_email`) to its account's
mobile, which is what the session runs under.
- **Files.** `api/main.py` (`/onboarding/known`), `web/app/components/Login.jsx`
- **Note.** Dev IDs like `kumar1` no longer pass this screen — test those with
  `curl -H "X-Aruvi-User: kumar1"`.

### B6. Trial Settings show neither Personal profile nor Your data & export
Taken after the run, on the same reasoning as B4: the trial is a look at the **teaching**
product, and the account around it — her details, her export — belongs to a teacher who has
one. Both cards are hidden and both subviews unreachable while `status: trial`; both return
whole on subscribing.

Two boundaries deliberately **not** crossed:
- **UI only — the routes stay open.** `POST /account` and `/data-rights/*` are ungated.
  Checkout itself writes the account record, so a trial-time `/account` refusal would break
  the path *out* of the trial; and §2.5's "data rights are never gated" is a promise about
  the routes. A3's lesson is that a rule must not be **derived** in two places — not that
  every UI hide needs a 402 behind it.
- **Delete my account keeps its download.** G3's last window still offers "Download my data
  first" on trial, where it is now her only export door. Hiding the card must never mean
  destroying her work with no copy.

The flag rides down from `page.jsx`'s entitlement sync (`entTrial` → `trial` prop) rather than
Settings' own fetch, so the cards are never drawn and then withdrawn; Settings' `ent` stays as
the fallback for a state change landing while it is open.
- **Files.** `web/app/page.jsx`, `web/app/components/Settings.jsx`
- **STATIC ONLY** — live pass on a trial identity owed (E1's split of labour; H4.4's rule).

---

## PART C — NEW FEATURE: subscription confirmation email

### C1. The seam
A `Notifier` port (`EmailMessage` + `Notifier` in `aruvi_core/ports.py`) with two adapters, chosen
**once at startup** by whether credentials exist:

| Adapter | When | What it does |
|---|---|---|
| `FileNotifier` | no credentials (**today**) | writes each message to `data/cloud/state/outbox/` |
| `SmtpNotifier` | all three env vars set | really sends, from your address |

`FileNotifier` is the notification twin of `ManualBillingProvider`: the whole flow runs with **no
vendor and no credential in the repo**.

### C2. To switch on real sending
```
export ARUVI_SMTP_HOST=smtp.gmail.com
export ARUVI_SMTP_USER=kumar.radhakrishnan2@gmail.com
export ARUVI_SMTP_PASSWORD=<Google APP password>
```
Gmail needs an **app password** (Google Account → Security → 2-Step Verification → App passwords);
the normal account password is refused. **Stop-gap only** — personal Gmail has daily caps and weak
deliverability; a transactional provider (SES / Postmark / Resend) belongs behind this same port
before real volume.

### C3. What she receives
Confirms **what** she bought, **when** it runs to, and the **mobile her account is keyed to** (that
number is her sign-in, so it belongs in writing). No upsell, no feature tour.

```
Hello Meera,

Your Aruvi subscriptions are active. Here is what you have:

  • Social Sciences · Middle — Classes 6, 7 and 8
  • English · Middle — Classes 6, 7 and 8

  Amount    ₹1,000 for the year
  Valid to  26-Aug-2027
  Sign in   1234567896
  …
```

### C4. Two guarantees, enforced by tests
1. **Mail failure can never fail a subscription** — the notifier returns a status, never raises.
   `checkout` returns `email_status` so the UI can be honest instead of promising unsent mail.
2. **The copy never says "certified"** — only NCF-aligned.

You also get a **BCC of every sale** (`ARUVI_MAIL_BCC_FOUNDER`, default on) — your sales log until
invoicing exists.

- **Files.** `aruvi_core/ports.py`, `aruvi_core/adapters/file_notifier.py`,
  `aruvi_core/adapters/smtp_notifier.py`, `api/mail_templates.py`, `api/config.py`, `api/main.py`,
  `tests/test_notifier.py` (7 tests)

---

## PART D — WHAT PASSED

| Area | Tests | Result |
|---|---|---|
| Front door | Z1–Z13 | ✅ choose page · four-box OTP with real auto-advance · registered-only sign-in · double-blind email · cart of dropdown rows · honest Pay · default profile per scope · scope-filtered first run · first-name display · ledger |
| Trial mechanics | 14–22 | ✅ counter, re-serve free, 4th chapter → popup with **no ghost card**, paywall Subscribe opens the in-app wizard |
| Convert | 23–28 | ✅ scoped choosers, "Keep it" re-ticks, only-subject removal allowed |
| Lapsed | 30–34 | ✅ tab/+/pen/prepare-bar all gone, server 402s, **both Word and PDF exports still work** |
| Renewal | 35 | ✅ everything returns, nothing lost |
| Settings | 36–39 | ✅ frozen bar, card order, labels-above, Save exits to cards, live name update |
| Tour | 43–44 | ✅ exactly **20 steps**, step 12 = bookmark placed **above**, hands absent from 4/5/6/12/16/18 |
| Combinations | 46–49 | ✅ enterprise unfiltered · multi-scope ₹1000 with both profiles · date-expiry · notes lock |

---

## PART E — STILL OPEN

### E1. Layout verification is yours (tests 51, and the visual halves of 1 and 6)
The browser surface driven by the automation reports `outerWidth: 0`, `visibilityState: "hidden"`
and a **fixed 222 × 629** rendering area — it is an off-screen, extension-managed tab, not a
resizable window. Every resize call succeeds and changes nothing. Narrower than any real phone, so
any layout verdict from it would be false.

**Split of labour:** automation drives behaviour, state and flows; you judge appearance at
360×800 and on your iPhone. Chrome DevTools device mode — the workflow in CLAUDE.md §0 — cannot be
driven programmatically and will always be a human step.

### E2. Cosmetic nit, not fixed
English chapter titles read *"Fun with Friends (Fun with Friends)"* — the section name repeats when
it matches the chapter title.

### E3. Watch this when payments go live
A3 is the one to remember: **manual revocation — the only lapse ever tested before today — takes a
different code path from a subscription that runs out on its own.** Real lapses will all be the
latter.

---

## PART G — THE FOUR FOUNDER ITEMS RAISED AT THE END OF THE SESSION

Asked: *"have you tested these?"* — none of the four had been built, so none had been
tested. Status after this session:

### G1. Cutover (Aruvi-side and teacher-side) — **BUILT + TESTED LIVE**
Founder's decision: **offered, never automatic.** Full write-up in **PART H** below.

### G2. Tenant vs user (school buying under its own name) — **DEFERRED, DECIDED**
**`tenant_id == user_id` stands. One teacher = one tenant. No bulk purchase until the
website exists.** Full reasoning in `docs/subscription_model_discussion.md` §0-bis, added
this session: the arbitrage cannot be priced away, the phone (not the price) is the fence,
the billing unit must stay subject-stage × teacher on every channel, and the bulk flow has
no natural home on a phone. Schema remains ready (separate `tenant_id`/`account_id`,
tenant-keyed entitlement, erase already refuses to destroy a school's subscription when
one teacher leaves) — nothing built here has to be undone later.

### G3. Account deletion — download-confirmation gate — **BUILT + TESTED**
Deletion is now **two windows**: type `erase` → **Continue →** (intent), then a modal
*"Have you downloaded your Aruvi data?"* with a download-first button, a checkbox
*"I confirm I have downloaded my Aruvi data"*, and the note *"Your confirmation is
recorded against your account."* Delete stays disabled until ticked.
Server enforces both — `{"confirm":"erase"}` alone now returns **400**.
**The confirmation is written BEFORE anything is destroyed**, into
`STATE_DIR/erasure_log/{tenant}.json`, which sits **outside the erase walk** so it
survives the erasure it records. Keyed tenant/user wise; carries identifiers and
timestamps ONLY — a test asserts no name, email or note text can leak into it, since that
would reintroduce exactly what she asked to have destroyed. Append-only (a second
deletion appends). Never raises: a logging failure must not block a right-to-be-forgotten.
*Note:* "only the tenant may delete" is currently trivially satisfied — tenant == user
(G2). It becomes a real restriction the day multi-user tenants exist.
**Files.** `aruvi_core/adapters/erasure_log_file.py` (new), `api/main.py`,
`web/app/components/Settings.jsx`, `web/app/globals.css`, `tests/test_data_rights.py`

### G4. Chapter-notes child-privacy line — **BUILT**
Below the two existing scope lines, in clay with a hairline above so it reads as a rule
rather than more scope text: *"Private data like name, age of child must not be recorded.
Aruvi reserves right to delete if entered."* Stated where she types, because notes are
free text written right after class — exactly the moment a child might be named.
**Files.** `web/app/components/LessonView.jsx`, `web/app/globals.css`

---

## PART H — ACADEMIC-YEAR CUTOVER (built and walked through a simulated 1 June 2027)

Founder's spec, verbatim in intent: *June 1st is the cutover date; old plans move into a
2026-27 folder and new generations sit outside it; a teacher adding a plan sees the old
folder below the latest generation if she wants; existing linkages to sections remain
unaffected. On the same date she gets a message on My Classes every login explaining what
cutover is, and on her confirmation it is effected for her.*

### H1. The design that made it small
**Cutover moves nothing and deletes nothing.** Step 1 had already year-scoped every
TEACHING store by path (`{kind}/{tenant}/{user}/{year}/…`) while leaving readiness
un-scoped, so opening the next year and pointing her at it produces all four promises for
free:

| Store | Year-scoped? | Effect of cutover |
|---|---|---|
| prepared plans | yes | new year's folder empty → My Lessons starts clean |
| section state | yes | new year's folder empty → **attachments and pointers cleared** |
| plan notes | yes | stay in the closed year → **notes travel with their plans** |
| readiness (profile) | **no** | **class list, sections, periods carry forward untouched** |

The old year's folders are never touched, which is exactly why last year stays readable.

### H2. What she sees
- **From 1 June, on every visit to My Classes** until she acts: *"Start the 2027-28
  school year?"* — what carries, what starts fresh, and plainly that **nothing is
  deleted**. Ochre left edge. **Two ways to defer, both real controls** — an **✕
  top-right** and a **NOT YET beside START**, the latter styled as the quiet twin of the
  start button so it reads as a genuine option without competing with it. (The first build
  shipped a "Not now" that was a plain `<span>`: it looked like a choice and did nothing.
  The founder found it on sight.) **Dismissal is session-only and never persisted** — a
  stored "don't ask again" would quietly strand a teacher in last year, and the rule is
  that she sees the offer every login until she acts. Deferring changes nothing: her year,
  her bindings and her bookmarks are untouched, so a teacher still finishing a chapter in
  early June simply carries on.
- **On confirmation**, a panel states facts, not promises: *"2027-28 has begun. 2 sections
  carried over. Your 3 2026-27 lesson plans are in My Lessons under 2026-27."*
- **In My Lessons**, a collapsed **"2026-27 · lessons you prepared last year"** folder
  sits below the current list and below the prepare bar. Expanding it shows last year's
  lessons as **the same cards this year's list uses** — number tag, title, period matrix —
  differing only in the status line, which reads *"Taught in 2026-27"* because tracking
  belongs to the year she is in now. Tapping one opens it in full, exactly as before.
  Four points the founder settled on seeing it (all built and verified live):
  **(a) cards, not lines** — last year's lessons are the same kind of thing as this year's
  and should look it; **(b) the same sentence on both surfaces**, so the folder reads
  identically wherever she meets it; **(c) always closed by default** — never persisted,
  and re-closed whenever she changes subject or class, because an open folder carried over
  from another class would put last year's work in front of her before this year's;
  **(d) no duplicates** — a chapter she has brought back into this year is excluded from
  the folder (his screenshot caught Ch 01 showing twice on one screen, "Teaching now 9A"
  above and "Taught in 2026-27" below — both true, and confusing). The folder answers only
  *"what ELSE do I have from last year?"*
- **In the "+" attach picker too** (founder caught this omission the same day — his
  original spec said *"a teacher trying to add a plan now will see the old folder"*, and
  the first build only put it in My Lessons). A collapsed **"2026-27 · lessons you
  prepared last year"** folder sits below this year's list and above "prepare a new one".
  **She taught Ch 5 last June and wants it again this June — asking her to regenerate a
  plan she already has would be absurd.** Attaching one **marks it prepared in the CURRENT
  year** before binding: teaching it again makes it this year's work, so it moves into
  this year's My Lessons rather than being tracked from a folder the tracker cannot show.
  Verified live: Ch 01 attached from 2026-27 → bound to 9A in 2027-28's section state,
  listed under 2027-28's prepared plans, and showing as "Teaching now 9A".

### H3. Mechanics
- `GET /academic-year` → `current_year`, `next_year`, `prior_years`, **`cutover_due`**,
  `cutover_date`. `cutover_due` is computed **server-side** — never from the browser
  clock, which a teacher can change and a phone in another timezone gets wrong.
- `POST /academic-year/cutover {confirm:true}` → `CutoverResult`. Idempotent.
- **`ARUVI_CUTOVER_MONTH_DAY`** (default `06-01`) — config, never code; boards differ.
- **`ARUVI_TODAY`** (ISO date) — ★ testing only. Every date decision in `api/main.py` goes
  through one `_today()` seam, so a simulated date makes the WHOLE service agree what day
  it is (entitlement expiry included) instead of only the piece under test.
  **Remove it from the command line before ordinary testing.**
- Files: `aruvi_core/ports.py` (`CutoverResult`, `YearCutover`),
  `aruvi_core/adapters/year_cutover_file.py`, `api/config.py`, `api/main.py`,
  `web/app/page.jsx`, `web/app/components/MyPlans.jsx`,
  `web/app/components/MyLessonPlans.jsx`, `web/app/lib/sectionState.js`,
  `web/app/globals.css`, `tests/test_cutover.py` (5 tests).

### H4. Four bugs the live June walk caught — all fixed
None of these were visible to unit tests or to `babel-parse`.

1. **Tapping twice gave the wrong answer.** After cutting over, the second tap hit the
   date guard and returned *"the 2028-29 year opens on 2028-06-01"* instead of "already
   done" — the spec's own warning is that "a teacher WILL tap twice". Now distinguished by
   whether she has a prior year at all.
2. **Section cards still read "Teaching now Ch 5" after cutover.** `pullSectionState`
   deliberately deletes NOTHING on a wholesale-empty server response — an anti-corruption
   guard added after a corrupt `state.json` flashed every card back to "pick a chapter".
   Cutover is the one moment when empty genuinely means empty. Fixed with an explicit
   `clearLocalSectionCache()` at cutover rather than by weakening the guard.
3. **A ten-year veteran was thrown into the guided FIRST RUN.** `firstGenNeeded` reads
   year-scoped stores, so the morning after cutover they truthfully answer "nothing
   prepared, nothing bound" — indistinguishable from a brand-new teacher. It now also
   reads her year history: **a prior year is proof she has been here before.**
4. **A TDZ ReferenceError white-screened the entire app.** The earlier "no tour when
   lapsed" fix put `entLapsed` in `tourOnOffer` *above* its own `useState` declaration.
   `babel-parse` accepts this happily; the browser throws
   `Cannot access 'entLapsed' before initialization` and renders nothing.
   **Lesson: a parse check is not a render check — load the page.**

### H5. Verified live (simulated 1 June 2027, teacher seeded mid-2026-27)
Offer appears on My Classes ✅ · nothing changes until she confirms ✅ · after confirming:
`current_year` 2027-28 with `2026-27` in `prior_years` and the offer gone ✅ · section
state empty, cards read "Pick a chapter to begin" ✅ · **both sections still there** ✅ ·
profile intact (SS · IX · 9A+9B · 6 ppw) ✅ · 3 plans readable under 2026-27 ✅ · note
still in 2026-27, absent from the new year ✅ · prior-year plan opens in full ✅ ·
`test_cutover.py` 5/5 and all 12 suites green ✅.

### H6. Latent hazard noticed, not fixed
**Prepared-plan keys are case-sensitive** — `social_sciences/IX/…` and
`social_sciences/ix/…` are different keys. The app always writes lowercase, so nothing is
broken today, but a future caller that passes a Roman grade uppercase would silently
create a parallel set of invisible records. Worth normalising in `_plan_key` when
convenient.

---

## PART F — DOCS UPDATED

1. `MEMORY.md` — full dated entry, newest-first, including the races-and-stale-state lesson and a
   tooling note for the next driven run.
2. `docs/persona_test_checklist.md` — rewritten to **52 tests**, with a preamble on what an
   automated run can and cannot do.
3. `docs/subscription_model_discussion.md` — **new §0-bis**: bulk/school purchase deferred, with
   the full arbitrage reasoning and the ideas worth keeping when it is picked up.
4. `docs/persona_run_2026-08-26.md` — this document.
