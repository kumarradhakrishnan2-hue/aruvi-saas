# Persona Test Checklist — front door + subscription model end-to-end (updated 2026-08-25)

Report against the numbers. Setup for every pass:
- API: `ARUVI_ENTITLEMENT_ENFORCED=1 python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000`
- Web: `npm --prefix web run dev -- -H 0.0.0.0`
- Reset any identity: `curl -X POST -H "X-Aruvi-User: <id-or-mobile>" -H "Content-Type: application/json" -d '{"confirm":"erase"}' localhost:8000/data-rights/erase`
- Grant/revoke: `python3 aruvi-scripts/entitlement.py grant|revoke|status|trial-reset <id>`
- **First-time device** = a browser that has never signed in: use a PRIVATE TAB, or
  clear the site's localStorage. Fresh identities = any unused 10-digit mobile number.

---

## Z · The front door (new — do this pass first)

1. **First-time device** → the CHOOSE page appears (not sign-in): pine bar with brand;
   headline + 4 tick benefits; "Choose what works for you"; Free-to-try card
   highlighted by default (pine outline, NO "Recommended" badge); Subscribe card
   (clay accents) with ONLY the honest bullets (no "priority support", no "export &
   more"); "🔒 upgrade or switch anytime"; CTA "Create sign in"; quiet "Already have
   an ID? Sign in" below.
2. Tap between the two cards → highlight moves; brand colors only (pine/clay — no
   orange gradient).
3. **OTP page**: +91 + 10-digit field (letters impossible); "Generate OTP" disabled
   until 10 digits; after Generate, the OTP field + "Preview build: enter 0000" note.
4. Wrong code (e.g. 1234) → error line; `0000` → verifies.
5. **Trial path** (Free-to-try chosen): lands straight on the slimmed WELCOME —
   "Welcome to Aruvi!", "Aruvi is free to try.", the trial CARD (tick circle, "Your
   free trial" terms, "To get started"), CTA — no benefits list here anymore, no
   theme toggle on the bar. Prepare bar visible without scrolling at 360×800.
6. **Subscribe path** (fresh number, Subscribe chosen): step rail Verify → About you →
   Subjects → Pay tracks correctly. About you: Save disabled until name+role+state
   filled; school optional.
7. **Subjects = the cart**: all 11 subject·stage combos listed (Science M/S · Social
   Science M/S · Maths P/M/S · English P/M/S · TWAU P); ticking updates the running
   total at ₹500 each; Continue disabled with empty cart.
8. **Pay**: line per combo + total; the honest stub note ("online payment opens
   soon — this activates right away"); "Pay ₹N & start" → lands in first run.
9. That first run is SCOPE-FILTERED: subject wheel = only what she bought (one item
   if one scope), class wheel = only her stage's classes; welcome was the CLEAN
   version (no trial card, no "free to try").
10. After onboarding once, reopening the app on the same tab → SIGN-IN screen
    (returning device): benefits block, "Who's planning today?" with NO sub-text,
    one field; legacy IDs (kumar1) still work; a mobile ID works; "New to Aruvi?
    Get started →" returns to the choose page.
11. Settings › Subscription for the new subscriber: ledger rows (Subject/Stage/
    Class/Validity dd-Mmm-yy), one trio per purchased scope.

## A · Fresh trial teacher (erase the trial mobile / kumar3 first; NO grant)

12. Confirm clean: `curl -H "X-Aruvi-User: <id>" localhost:8000/entitlement` →
    status trial, used 0.
13. Welcome shows the trial card (see Z5). Subject step: ALL subjects. Class step:
    all classes.
14. Chapter step: no trial line (welcome said it). Generate chapter 1 → My Lessons;
    tour offer appears below the lesson.
15. + Prepare Lesson → chapter step: "1 of 3 free chapters used. Regenerating same
    chapter allowed."
16. Re-generate the SAME chapter at different periods 2–3× → counter stays 1.
17. Chapters 2 and 3 (cross-subject on purpose) → counter 2, 3.
18. 4th chapter → POPUP (no card behind it): "FREE TRIAL ENDS", "…Your 3 chapters
    stay yours…", bold SUBSCRIBE, "Not now"; backdrop dismisses.
19. Trial-exhausted: all 3 chapters open/export/print; TRACKER STILL WORKS (attach,
    pointer, mark complete); "+" portal visible; Settings › Subscription: "Free
    trial — 3 of 3 chapters used".

## B · Convert: trial-exhausted → subscribed

20. `grant <id> --scopes social_sciences/middle` → within ~20s/on focus, SS-middle
    generation works, unlimited, counter line gone.
21. Settings › Subscription: SUBSCRIBED + ledger rows, Validity dd-Mmm-yy.
22. A Science chapter (trial-era subject) → popup "SEPARATE SUBSCRIPTION".
23. Profile edit pens: subject wheel = paid subject + any trial-era ENROLLED subjects
    only (so they can be removed), upsell line below; class wheel = classes 6–8 (+
    enrolled others).
24. "Keep it" in a removal warning re-ticks the item (subjects AND classes).
25. Removing her ONLY subject: allowed, warned, empties to "+ add a subject".

## C · Subscribed from the start

26. Covered by Z6–Z9. Additionally: no trial chrome anywhere in the session — no
    counter, no trial card, no trial line.

## D · Revocation / lapsed

27. `revoke <id>` while she is ON My Classes → within ~20s/on focus: moved to My
    Lessons; My Classes TAB GONE.
28. My Lessons: dropdowns work, plans open, plan export works; "Prepare a new
    lesson →" bar GONE.
29. Straggler generation attempt → popup "SUBSCRIPTION ENDED".
30. Settings: ENDED + "plans remain yours"; Profile read-only (no pen); "+" absent;
    tracking taps don't persist (server 402).
31. Data rights while lapsed: BOTH data downloads work; Delete my account works.

## E · Renewal

32. `grant` again → My Classes tab, prepare bar, pen, tracker all return; nothing lost.

## F · Settings suite (any signed-in user)

33. Gear → frozen "⚙ Settings ✕" bar (one title, no hairline); tabs + Ask mark gone
    inside; ✕ returns exactly where you were (test from My Classes AND My Lessons).
34. Cards in order: Profile · Subscription & billing · Your data & export · Help ·
    Support · About; no icons; one phone screen; Help opens Ask Aruvi;
    Support/About placeholders.
35. Appearance row toggles theme — and the toggle exists nowhere else (shell bar and
    first-run bar are clean).
36. Delete my account: type-"erase" → farewell → Done signs out; re-signin = new
    teacher.

## G · Tour eligibility

37. kumar1 (veteran): NO tour offer, either surface, any session.
38. Fresh post-first-run teacher: offer appears; take the 19 steps once — the profile
    step anchors the gear correctly.
39. After real teaching (pointer moved): offer never returns.

## H · Combinations

40. **Enterprise grant**: `grant <id> --plan enterprise_annual` (scopes "*") →
    unlimited everything; Subscription card: All subjects / All stages / 3 to 10;
    choosers unfiltered.
41. **Multi-scope checkout**: buy TWO combos in the cart (₹1000 total) → Subscription
    card shows two Subject/Stage/Class trios + one Validity; first run offers both
    subjects.
42. **Expired-by-date**: `grant <id> --until 2025-01-01` → same lapsed behavior as
    revoked.
43. **Notes while lapsed**: chapter notes still writable — CONFIRM this is the rule
    you want (her writing vs productivity tool); tell me if notes should lock too.
44. **Dark mode**: choose page, OTP, cart, welcome card, paywall popup, Settings —
    all legible.
45. **360×800 sweep**: every new screen (Z1–Z9) — no horizontal scroll, no clipped
    CTAs, step rail fits.
46. **Flag off sanity**: API without the flag → ALL trial/subscription chrome gone
    (choose page still shows both cards, but trial card/counters/popups never
    appear in-app); behaves like pre-Step-5 Aruvi.

Report failures by number.
