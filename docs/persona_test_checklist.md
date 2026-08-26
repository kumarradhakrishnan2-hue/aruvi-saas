# Persona Test Checklist — front door + subscription model end-to-end (updated 2026-08-26)

Report against the numbers. Setup for every pass:
- API: `ARUVI_ENTITLEMENT_ENFORCED=1 python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000`
  (the flag MUST be on the same command line; verify with `curl localhost:8000/entitlement
  -H "X-Aruvi-User: anything"` → `"enforced": true`)
- Web: `npm --prefix web run dev -- -H 0.0.0.0`
- Reset any identity: `curl -X POST -H "X-Aruvi-User: <id-or-mobile>" -H "Content-Type: application/json" -d '{"confirm":"erase"}' localhost:8000/data-rights/erase`
- Grant/revoke: `python3 aruvi-scripts/entitlement.py grant|revoke|status|trial-reset <id>`
- **First-time device** = a browser that has never signed in: use a PRIVATE TAB, or clear
  the site's localStorage. Fresh identities = any unused 10-digit mobile number.
- Dummy OTP is `0000` for everyone (dev stub, disclosed on screen).

## Notes for an automated (Claude in Chrome) run

- The browser agent can do everything in-app (localStorage clearing via JS, private-tab
  equivalents, form fills, viewport resize to 360×800, dark-mode toggle via the in-app
  Appearance row). It CANNOT run the terminal commands above — the founder must have both
  servers already running with enforcement ON, and must run the erase/grant/revoke/
  trial-reset CLI steps when a test calls for them (tests 15, 26, 33, 41, 48, 50, 52, 54).
  Alternative: erase is also an HTTP POST (see setup), which the agent CAN issue via fetch.
- Base URL: `http://localhost:3000`. Entitlement state ground truth:
  `GET localhost:8000/entitlement` with header `X-Aruvi-User: <mobile>`.
- Entitlement changes made server-side appear in the UI within ~20s or on tab focus —
  refocus/reload rather than declaring a failure instantly.
- If behavior looks stale (old copy, old layout), hard-reload first — Next dev serves
  cached bundles; a stale bundle is not a product failure.
- Use a FRESH unused mobile number per persona; do not reuse a number across personas
  unless the test says so.

---

## Z · The front door (do this pass first)

1. **First-time device** → the CHOOSE page appears (not sign-in): pine bar with the
   standard Aruvi brand chrome; headline "…in seconds"; the four benefits as ONE
   compact continuous paragraph (small font) with pine ✓ ticks — not a bulleted list;
   "Choose what works for you"; Free-to-try card highlighted by default (pine outline,
   NO "Recommended" badge); Subscribe card (clay accents) with ONLY the honest bullets
   ("Unlimited chapters · your full subject & stage, every class in it" — no "priority
   support", no "Everything in Free to try…" line); NO "upgrade or switch anytime"
   line; CTA "Create sign in"; quiet "Already have an ID? Sign in" below. All CTAs
   visible without scrolling at iPhone height (sticky footer).
2. Tap between the two cards → highlight moves; brand colors only (pine/clay — no
   orange gradient).
3. **OTP page**: +91 + 10-digit field (letters impossible); "Generate OTP" disabled
   until 10 digits. After Generate: **FOUR OTP boxes in a row** — typing a digit
   auto-advances to the next box; backspace moves back; "Preview build: enter 0000"
   note shown.
4. Wrong code (e.g. 1234) → error line; `0000` → verifies.
5. **Sign-in is registered-only, MOBILE or EMAIL only**: the field is labeled
   "Mobile number or email"; Enter stays disabled until the input is a 10-digit
   mobile OR a valid email shape (a free-form ID like "kumar1" never enables it).
   An unknown but well-formed number/email → "We don't recognise this mobile or
   email yet…" error, NOT a silent new account. A REGISTERED email signs in as its
   account's mobile (name/greeting/settings all hers). "New to Aruvi? Get
   started →" returns to choose. (Legacy dev IDs like kumar1 no longer pass this
   screen — test them via the `X-Aruvi-User` header/curl instead.)
6. **Trial path** (Free-to-try chosen): lands straight on the slimmed WELCOME —
   "Welcome to Aruvi!", the trial CARD (tick circle, "Your free trial" terms — the
   "Aruvi is free to try." line is GONE), CTA "Prepare my first lesson" high on the
   screen and visible without scrolling at 360×800; no benefits list; no theme toggle
   on the bar.
7. **Subscribe path** (fresh number): step rail Verify → About you → Subjects → Pay
   tracks correctly. **About you** uses labels ABOVE each field ("Your name", "Email",
   "Re-enter your email", "Role", "State", "City", "School name (optional)"), fields on
   a lighter (white) background than the card; **email is double-blind**: type it, it
   hides, re-enter to confirm, mismatch → error; Continue disabled until
   name+email-confirmed+role+state; school optional. Role/State dropdowns are
   Aruvi-styled (paper background + chevron, no dark native menu button).
8. **Subjects = the CART OF DROPDOWN ROWS** (not a tick list): each row = Subject ▾ ·
   Stage ▾ · ✕, with "+ Add another subject" below and the running total at the bottom
   (₹500 per combo, NO per-row price). Unset dropdowns show bold grey **Subject** /
   **Stage** placeholders. Picking a stage shows its classes below the row; secondary
   shows "Class 9 (Class 10 coming soon)". **Duplicate combos cannot be ENTERED at all**
   (2026-08-26 — see 22c; they used to be silently de-duped at the total, which showed
   two rows and charged for one). Continue disabled with an empty/incomplete cart.
9. **Pay**: line per combo + total; the honest stub note ("online payment opens
   soon — this activates right away"); "Pay ₹N & start".
10. **Checkout creates the default teaching profile** per purchased scope: lowest
    class of the stage, section A ("6A" etc.), standard duration, 6 periods/week,
    calibrated annual budget. Verify BOTH purchased subjects then appear (e.g. SS +
    English → both in every chooser, not just one).
11. A direct subscriber still walks the FIRST RUN, scope-filtered: subject wheel =
    only what she bought, class wheel = only her stage's classes; welcome is the CLEAN
    variant (no trial card, no "free to try").
12. After onboarding once, reopening on the same tab → SIGN-IN screen (returning
    device); her mobile works; her CONFIRMED EMAIL also works (resolves to the same
    account); the greeting screen and the top-right (above Log out) show her FIRST
    NAME ONLY, first letter capitalized — until a name exists, plain
    "Good morning/evening!".
13. Settings › Subscription for the new subscriber: ledger rows (Subject/Stage/Class/
    Validity dd-Mmm-yy), one trio per purchased scope.

## A · Fresh trial teacher (erase the trial mobile first; NO grant)

14. Confirm clean: `curl -H "X-Aruvi-User: <id>" localhost:8000/entitlement` →
    status trial, used 0.
15. Welcome shows the trial card (see Z6). Subject step: ALL subjects. Class step:
    all classes.
16. Chapter step: no trial line (welcome said it). Generate chapter 1 → My Lessons;
    tour offer appears below the lesson.
17. + Prepare Lesson → chapter step: "1 of 3 free chapters used. Regenerating same
    chapter allowed."
18. Re-generate the SAME chapter at different periods 2–3× → counter stays 1.
19. Chapters 2 and 3 (cross-subject on purpose) → counter 2, 3.
20. 4th chapter → POPUP (no card behind it): "FREE TRIAL ENDS", "…Subscribe to keep
    preparing — the chapters you made in a subject you subscribe to come with you."
    (reworded 2026-08-26 evening: the old "Your 3 chapters stay yours" became false
    once the trial purge landed — see 22f), bold SUBSCRIBE, "Not now"; backdrop
    dismisses.
21. **Paywall SUBSCRIBE opens the subscribe wizard IN-APP** (with the Aruvi bar/logo
    on top): starts at About you; if her personal profile is already complete it skips
    straight to Subjects. Completing Pay activates without sign-out; scoped choosers
    update.
22. Trial-exhausted (Not now): all 3 chapters open/export/print; TRACKER STILL WORKS
    (attach, pointer, mark complete); "+" portal visible; Settings › Subscription:
    "Free trial — 3 of 3 chapters used" + a **Subscribe** button below (button appears
    whenever on-trial or lapsed).
22a. **Trial Settings are narrower** (founder, 2026-08-26): the cards show **Teaching
    profile · Subscription & billing · Help · Support · About** — **no Personal
    profile, no Your data & export** — with no gap or flash where they were (the flag
    comes from the shell, not from Settings' own fetch). Deleting the account still
    works and its last window still offers **"Download my data first"** — on trial that
    is her only export door. `POST /account` and `GET /data-rights/export` still answer
    200 by curl: this is what Settings shows, not a gate. Subscribe → both cards return.

22b. **"Already in use", said at the field** (2026-08-26): on Create sign in, a
    registered mobile is refused **before the OTP** — "This mobile number is already in
    use. Create using a different number." and nothing else (no Sign in link: this
    screen creates a sign-in, so its refusal stays inside that job); in
    checkout About-you and Settings › Personal profile, confirming an email held by
    another account (or shared by two) shows the same sentence at the **email field**,
    not at Pay/Save. Her OWN address always re-saves fine. Force the late path by
    curl-taking an address between Verify and Pay: the Pay error must now be the
    server's sentence, never "try again in a moment".
22c. **The cart cannot hold the same subject & stage twice**: pick SS · Middle, add
    another row — Middle reads "· already added" and is unselectable; once every stage
    of a subject is taken the subject itself greys ("— all stages added"); with the
    whole catalogue in the cart "+ Add another" is dead. Changing a row's own value
    still works.
22d. **Adding a subject does not overwrite the ones she has** (2026-08-26 — it did):
    buy Science·Middle + Science·Secondary, then add English·Middle from Settings ›
    Subscription › **Add subjects & stages**. All THREE must remain, each with its own
    "Validity … until dd-Mmm-yy" INSIDE its block, and her teaching profile must keep
    all three subjects. The chooser must not offer a subject-stage she already holds
    ("· you have this", unselectable); forcing it by curl → **409** naming the date it
    runs to. The confirmation mail must show what she just added AND
    "Everything you have with Aruvi now" with a date per line.
22e. **One subscription ending does not lock the others**: set one scope's date in the
    past (edit `scope_valid_until` in `entitlements/{id}/entitlement.json`). That
    subject's generation → **402 naming that subject and its end date**; every other
    subject still generates; the tracker, "+", edit pen and My Classes all stay; the
    Settings ledger shows that one as "ended dd-Mmm-yy" in clay. Expire them ALL →
    only then the full lapsed lockout (tab gone, writes 402, plans still readable).

22f. **The trial purge** (2026-08-26 evening — reverses that morning's "trial plans
    stay reachable"): trial in English AND Science, then subscribe to **Science only**.
    The Pay screen must warn, by name, that the English trial lessons will be cleared.
    After activation: English is gone from My Lessons, from the choosers and from the
    profile, with its pointers and chapter notes gone too; **Science keeps every
    chapter, pointer and note**. Adding a subject LATER must purge nothing
    (`"purged": {}` in the checkout response). The saved plan FILES under
    `data/cloud/content/saved_plans/` must still be there — the purge removes her
    records, never shared library content.
22g. **The subscription page is one box per subscription, latest first**: buy two, add
    a third later → three separate cards, the newest on top, each with its own
    Subject / Stage / Class / Validity. An expired one still shows, in clay, as
    "ended dd-Mmm-yy".

22h. **Invoicing** (2026-08-26): every purchase issues `ARV/{FY}/NNNN`, gapless and
    April-anchored. Check: the number appears in the confirmation mail body AND the PDF
    is attached (in the outbox, the PDF is written beside the .txt); the file lands in
    `state/invoices/{tenant}/{user}/`; Settings shows it on the card of the subscription
    it paid for and the download works; a second purchase gets its OWN invoice for that
    purchase only (not the whole holding); another teacher's `GET /invoices/{number}`
    → 404. The PDF must show no GSTIN and the words "No tax charged" — never a ₹0 tax
    row. Deleting the account keeps invoices (tax records, §2.6) but she loses access:
    the last delete window must say so.
## B · Convert: trial-exhausted → subscribed

23. `grant <id> --scopes social_sciences/middle` → within ~20s/on focus, SS-middle
    generation works, unlimited, counter line gone.
24. Settings › Subscription: SUBSCRIBED + ledger rows, Validity dd-Mmm-yy; Subscribe
    button gone.
25. A Science chapter (trial-era subject) → popup "SEPARATE SUBSCRIPTION".
26. Profile edit pens: subject wheel = paid subject + any trial-era ENROLLED subjects
    only (so they can be removed), upsell line below; class wheel = classes 6–8 (+
    enrolled others).
27. "Keep it" in a removal warning re-ticks the item (subjects AND classes).
28. Removing her ONLY subject: allowed, warned, empties to "+ add a subject".

## C · Subscribed from the start

29. Covered by Z7–Z11. Additionally: no trial chrome anywhere in the session — no
    counter, no trial card, no trial line.

## D · Revocation / lapsed

30. `revoke <id>` while she is ON My Classes → within ~20s/on focus: moved to My
    Lessons; My Classes TAB GONE.
31. My Lessons: dropdowns work, plans open, plan export works; "Prepare a new
    lesson →" bar GONE.
32. Straggler generation attempt → popup "SUBSCRIPTION ENDED"; its Subscribe opens
    the same in-app wizard (Z21 behavior).
33. Settings: ENDED + "plans remain yours" + Subscribe button; Teaching profile
    read-only (no pen); "+" absent; tracking taps don't persist (server 402).
34. Data rights while lapsed: BOTH data downloads work (Word + PDF); Delete my
    account works.

## E · Renewal

35. `grant` again (or re-subscribe via Settings → wizard skips known About-you) → My
    Classes tab, prepare bar, pen, tracker all return; nothing lost.

## F · Settings suite (any signed-in user)

36. Gear → frozen "⚙ Settings ✕" bar (one title, no hairline); tabs + Ask mark gone
    inside; ✕ returns exactly where you were (test from My Classes AND My Lessons).
37. Cards in order: **Personal profile** ("Your name, email, role and school
    details") · **Teaching profile** ("Subjects, classes, sections and periods you
    teach") · Subscription & billing · Your data & export · Help · Support · About;
    no icons; one phone screen; Help opens Ask Aruvi; Support/About placeholders.
    **Subscribed or lapsed teacher — on trial see 22a** (two of these cards are absent).
38. **Personal profile editor**: labels above fields, lighter field background;
    mobile number shown below the name (no "your sign-in" text); email shows masked
    with a "Change" path → double-blind re-entry ONLY when changing email — editing
    any other field never re-demands email; quiet note that email isn't saved until
    confirmed; **Save returns to the Settings cards** on success.
39. Name saved in Personal profile updates the top-right first name + greeting
    immediately (capitalized first name only).
40. Appearance row toggles theme — and the toggle exists nowhere else (shell bar and
    first-run bar are clean).
41. Delete my account: type-"erase" → farewell → Done signs out; re-signin = new
    teacher.

## G · Tour eligibility + content

42. A veteran teacher (e.g. kumar1 via header, or any long-used mobile): NO tour
    offer, either surface, any session.
43. Fresh post-first-run teacher: offer appears; take the **20 steps** once — the
    profile step anchors the gear correctly.
44. **Step 12 = the bookmark**: title "Bookmark where you left a particular section",
    box sits ABOVE the bookmark (does not cover it), no hand symbol. Hands are also
    absent from steps 4, 5, 6, 16 and 18.
45. After real teaching (pointer moved): offer never returns.

## H · Combinations

46. **Enterprise grant**: `grant <id> --plan enterprise_annual` (scopes "*") →
    unlimited everything; Subscription card: All subjects / All stages / 3 to 10;
    choosers unfiltered.
47. **Multi-scope checkout**: buy TWO combos in the cart (₹1000 total) → Subscription
    card shows two Subject/Stage/Class trios + one Validity; first run offers both
    subjects; after first run BOTH subjects' default profiles exist (Z10).
48. **Expired-by-date**: `grant <id> --until 2025-01-01` → same lapsed behavior as
    revoked.
49. **Notes while lapsed**: the notes modal opens READ-ONLY — her existing notes are
    all still readable (and still export), the textarea is not editable, the footer
    reads "Renew to write notes — what you wrote stays yours." and the only button
    is Close. Server refuses the write too (402). Founder ruled 2026-08-26: notes
    belong to Aruvi's working half, alongside the tracker and profile.
50. **Dark mode**: choose page, OTP boxes, About-you fields (lighter field tone still
    reads lighter than the card), cart dropdowns, welcome card, paywall popup,
    Settings — all legible.
51. **360×800 sweep**: every front-door screen (Z1–Z11) — no horizontal scroll, no
    clipped CTAs, sticky footers keep CTAs on screen, step rail fits.
52. **Flag off sanity**: API without the flag → ALL trial/subscription chrome gone
    (choose page still shows both cards, but trial card/counters/popups never appear
    in-app); behaves like pre-Step-5 Aruvi.

Report failures by number.
