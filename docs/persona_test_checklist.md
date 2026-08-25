# Persona Test Checklist — subscription model end-to-end (2026-08-24)

Report against the numbers. Every test assumes the API is running WITH the flag:
`ARUVI_ENTITLEMENT_ENFORCED=1 python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000`
and the web dev server as usual. Reset kumar3 between personas:
`curl -X POST -H "X-Aruvi-User: kumar3" -H "Content-Type: application/json" -d '{"confirm":"erase"}' localhost:8000/data-rights/erase`
Grant/revoke: `python3 aruvi-scripts/entitlement.py grant|revoke|status|trial-reset kumar3 [--scopes social_sciences/middle]`

---

## A · Fresh trial teacher (erase kumar3 first)

1. Sign in → welcome page: trial terms line in PINE above "Let's get started"; prepare
   bar visible WITHOUT scrolling (360×800 esp.); "Lesson plan in seconds, not hours";
   bar shows brand + kumar3 only (no theme toggle).
2. Subject step: ALL subjects offered (trial breadth). Class step: all classes.
3. Chapter step: NO trial line here (welcome said it). Generate chapter 1 → lands in
   My Lessons; tour offer appears below the lesson (fresh teacher = eligible).
4. + Prepare Lesson → chapter step shows "1 of 3 free chapters used. Regenerating same
   chapter allowed."
5. Re-generate the SAME chapter at different periods 2–3× → counter stays at 1.
6. Generate chapters 2 and 3 (any subjects — cross-subject on purpose) → counter 2, 3.
7. Ask for a 4th chapter → POPUP (no section card behind it): kicker "FREE TRIAL ENDS",
   message "…Your 3 chapters stay yours…", bold SUBSCRIBE, "Not now"; backdrop tap
   dismisses.
8. TRIAL-EXHAUSTED state: all 3 chapters still open/export/print; TRACKER STILL WORKS
   (attach to section, move pointer, mark complete) — exhausted keeps the tracker,
   unlike lapsed. "+" portal still visible. Settings › Subscription: "Free trial — 3 of
   3 chapters used".

## B · Convert: trial-exhausted → subscribed

9. `grant kumar3 --scopes social_sciences/middle` → within ~20s or on next app focus,
   generation works again for SS middle chapters — unlimited, counter line GONE from
   the chapter step.
10. Settings › Subscription & billing: pill SUBSCRIBED + ledger rows — Subject: Social
    Science / Stage: Middle / Class: 6, 7 & 8 / Validity: until dd-Mmm-yy.
11. Ask for a SCIENCE chapter (trial-era subject still in her profile) → popup, kicker
    "SEPARATE SUBSCRIPTION", "…covers a different subject…".
12. Profile (Settings › Profile) → edit pen → SUBJECT pen: wheel shows her paid subject
    PLUS any trial-era enrolled subjects (so they can be removed), but NO other
    catalogue subjects; upsell line below the wheel. CLASS pen: only classes 6–8
    offered (+ any enrolled others); same upsell line.
13. "Keep it" in a removal warning re-ticks the item (subjects AND classes).
14. Removing her ONLY subject: allowed, warned, profile empties → "+ add a subject".
    (Then rebuild or re-erase.)

## C · Subscribed from the start (erase, grant, THEN first sign-in)

15. Welcome: CLEAN — no trial terms line. Subject step: ONE-item wheel (Social
    Science). Class step: only 6, 7, 8.
16. Generate freely; no counter anywhere; chapter step clean.

## D · Revocation / lapsed (from state B or C)

17. `revoke kumar3` while she is ON My Classes in the app → within ~20s or on focus:
    moved to My Lessons; My Classes TAB GONE.
18. My Lessons: dropdowns work, plans open, EXPORT works (plan PDF/DOCX); "Prepare a
    new lesson →" bar GONE.
19. Any straggler generation attempt → popup kicker "SUBSCRIPTION ENDED".
20. Settings: Subscription shows ENDED + "plans remain yours"; Profile opens READ-ONLY
    (no pen); "+" portal absent everywhere; tracking taps don't persist (server 402).
21. Data rights while lapsed: BOTH downloads work; Delete my account works. (Rights
    never lapse.)

## E · Renewal (from D)

22. `grant kumar3 --scopes social_sciences/middle` again → My Classes tab returns,
    prepare bar returns, pen returns, tracker works. Nothing lost from before.

## F · Settings screen suite (any signed-in user)

23. Gear → frozen bar "⚙ Settings ✕" (one title only, larger, no hairline below); tabs +
    Ask mark gone while inside; ✕ from home/subview/profile returns EXACTLY where you
    were (test from My Classes AND from My Lessons).
24. Cards: Profile → Subscription & billing → Your data & export → Help → Support →
    About; no icons; all fit one phone screen; Help opens Ask Aruvi; Support/About show
    their placeholder texts.
25. Appearance row: theme toggles (and the toggle exists NOWHERE else — first-run bar
    and shell bar are clean).
26. Delete my account: type-"erase" flow → farewell → Done signs out; re-signin =
    brand-new teacher.

## G · Tour eligibility

27. kumar1 (veteran): NO tour offer on either surface, any session.
28. Fresh post-first-run teacher (state A step 3): offer appears; take it once through
    all 19 steps — step 15/17 opens the PROFILE correctly through the new gear anchor.
29. After she really teaches (pointer moved): offer never returns.

## H · Combinations we haven't touched (worth one pass each)

30. **Enterprise-style grant**: `grant kumar3 --plan enterprise_annual` (scopes default
    "*") → everything unlimited; Subscription card reads All subjects / All stages /
    3 to 10; profile choosers unfiltered.
31. **Multi-scope**: `grant kumar3 --scopes social_sciences/middle,science/secondary` →
    Subscription card shows TWO Subject/Stage/Class trios + one Validity; choosers
    offer both.
32. **Expired-by-date** (vs revoked): `grant kumar3 --until 2025-01-01` → same lapsed
    behavior everywhere (the date, not the founder's hand, ended it).
33. **Notes while lapsed**: open a plan's chapter notes — writing should still work
    (notes are hers, not a productivity lock — CONFIRM this is the behavior you want;
    if notes should lock too, tell me).
34. **Dark mode**: paywall popup, Settings cards, trial lines — all legible in dark.
35. **360×800 sweep**: welcome, chapter step + counter, popup, Settings, subscription
    ledger — no horizontal scroll, no clipped buttons.
36. **Flag off sanity**: restart API WITHOUT the flag → all trial/subscription chrome
    vanishes everywhere; app behaves exactly as before Step 5 existed.

Report failures by number.
