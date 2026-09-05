# Meyy → Expo: reuse assessment and migration path

*Measured against the repo on 2026-09-04. Numbers are from the code, not estimates, unless marked.*

## 0. The one-line answer

**Yes, there is a clean HTTP seam.** Next.js is a static host and nothing more: zero `next/*`
imports in the app (only `globals.css`), all 33 source files are `"use client"`, no `app/api`
routes, no server actions, no SSR data. The backend is FastAPI with **57 REST endpoints**, CORS
`*`, identity via the `X-Aruvi-User` header. **The backend, engine and data need zero changes
for a mobile beta.** The work is the presentation layer — and it is smaller than usual, because
the web app has **no third-party UI dependencies at all** (`react`, `react-dom`, `next`; that is
the whole `package.json`), so there is nothing to find a native replacement for.

## 1. What is there

| Layer | Size | Carries to Expo |
|---|---|---|
| `api/` + `aruvi_core/` + `data/cloud/` | 57 routes | **100%, untouched.** |
| `web/app/lib/` + `ask-aruvi/*.js` (format, sectionState, sectionHistory, verify, legalmd, bank, search) | 1,030 LOC | **~90% as-is** behind a storage shim (§3). |
| Live components — logic (state, effects, handlers, data shaping) | ~6,900 LOC | **Ports with edits**, not rewrites: same React, same hooks. |
| Live components — JSX markup | ~3,500 LOC | **Rebuilt** as RN primitives. |
| `globals.css` | 5,228 LOC · 2,068 selectors · 93 tokens · 54 `@media` | **Rebuilt** as StyleSheet + a token module. The 93 tokens and three fonts are the design system; they move first. |
| Dead files (Allocate, MyClasses, MyCalendar, SidebarNav, Generate, AccountPanel, PeriodRows, StatePill, SectionProgress…) | 13 files · 2,509 LOC | **Not ported.** |

Live surface: 31 files, 15,926 LOC. In the live components roughly two lines in three are
not markup, which is why "rewrite the frontend" overstates it — the component *behaviour*
carries; the *rendering* does not.

## 2. The beta's core flows (from the code, in the order a teacher meets them)

1. **Login** — OTP (mobile IS the identity; stub `0000`) → `/onboarding/known` · `/verified`.
2. **FirstRun** — Subject · Class · Chapter → `prepareAndHandOff` → `POST /genon/…/plan`.
3. **My Lessons** — prepared cards, preview, attach, Year Plan.
4. **My Classes** — section cards, LU progress rail, "+" portal, mark complete.
5. **LessonView** — unit tabs (Overview · Material · Lesson · Assess), bookmark, phases.
   **2,300 LOC — the product. Build this first; everything else is scaffolding around it.**
6. **Settings** — Teaching profile, Support, Legal, Subscription status.
7. **Ask Meyy** — bank fetched once, cached, searched on device.

Defer from beta: **GuidedTour** (the most DOM-bound file, §3), **SubscribeFlow** (§5B),
allocation report exports.

## 3. Browser-specific code that needs a native equivalent (the complete list)

| What | Where | Native answer |
|---|---|---|
| `localStorage` — 131 uses in 20 files | `sectionState.js` (37), `LessonView` (17), `MyPlans` (12), `page.jsx` (9)… | One **storage shim** (`getItem/setItem/removeItem`, sync) → **MMKV**. Sync matters: `sectionState.js` is designed as a *synchronous* optimistic cache in front of the server; AsyncStorage would break that contract. |
| API host derived from `window.location` | `lib/format.js` | `EXPO_PUBLIC_API_URL` constant. |
| `document.querySelector('[data-tour]')` + `getBoundingClientRect` + scroll math | `GuidedTour.jsx` (295 LOC) | Rewrite on `ref.measureInWindow`. Or defer. |
| `URL.createObjectURL` downloads (PDF/DOCX) — 6 sites | YearPlan, MyLessonPlans, Settings ×2, (2 dead) | `expo-file-system` + `expo-sharing` share sheet. |
| `dangerouslySetInnerHTML` for SVG visual stimuli in plans — 2 sites | LessonView, ViewModelView | `react-native-svg` `SvgXml`. |
| Inline `<svg>` icons — ~20 | 13 files | `react-native-svg`. `MeyyMark` is already path data with `currentColor`. |
| `position: fixed/sticky` (40 rules), measured `--nav-h`/`--fr-bar-h`, `ResizeObserver`, `matchMedia` | globals.css, page.jsx, FirstRun | **Disappear.** Native headers, SafeAreaView and `useColorScheme` do this without measurement. Simplifications, not ports. |
| `Dropdown.jsx` (built to escape macOS's unthemeable `<select>`) | 8 uses in 3 files | Native picker / bottom sheet. Its reason to exist is gone. |
| Google Fonts `@import` | globals.css | `expo-font`, bundled. (Self-hosting was already owed on web — CLAUDE.md §9.) |
| No-flash theme script | layout.jsx | `useColorScheme` + stored preference. |
| `legalmd.js` builds React nodes from markdown | Agreement, PrivacyNotice | Same code, element factories swapped (`p` → `Text`). |

Nothing else. No camera, mic, geolocation, clipboard, print, or web workers are used.

## 4. State that is localStorage-ONLY today (per-device unless mirrored)

Server-backed with a local cache already — fine: section state (chapter, pointer, done,
bookmark), chapter notes, readiness, prepared plans, archive, consent, tour-offered.

**localStorage only:** `section_history_*` (the "what has this section taught" ledger — its own
header says a server mirror is owed), `plus_portal_*` / portal queue, theme, the Ask Meyy bank +
ETag (a cache — fine). **Mirror `section_history` server-side before the beta**, or a teacher on
phone + laptop gets the exact two-device disagreement `sectionState.js` was built to end.

## 5. Two things the generic advice missed — both bigger than any UI item

**A. There is no deployed API.** `next dev` + local uvicorn is the whole runtime today. A beta
on other people's phones needs FastAPI on a public HTTPS host with persistent storage.
`data/cloud/` was designed as the byte-for-byte migration unit for exactly this, and the file
adapters work on a persistent volume — so for a beta, one container + one volume is enough;
Supabase (Phase 4) can follow. This is the first task, not the last.

**B. SubscribeFlow cannot be ported as-is.** The repo already knows this
(`administrative_architecture.md` Step 5: "Android takes Play Billing; iOS takes Apple IAP at
15–30%"; advisor questions 21–24 of 2026-09-04) — what the generic advice missed is that it is a
*build-order* fact: the one screen that takes money is the one screen that must NOT be a
straight port, because a Razorpay checkout inside the app is a store rejection. The clean beta
answer is the repo's own Q21: **free beta on `ManualBillingProvider` grants, no purchase screen
in the app at all.** The store-billing adapter behind the existing `BillingProvider` port (Q22–24
decide its shape) is post-beta work. This removes 686 LOC from the beta scope.

## 6. Recommendation

**Expo (managed workflow, Expo Router), not Capacitor.** The usual Capacitor argument — "the web
app is already built, wrap it" — is weak here: the design doc names the app as the individual
product and the price fence, so it has to be a first-class native product, and Apple's 4.2
"just a website" rejection risk is real for a wrapper with no native behaviour. The counter-
argument — "RN means a full rewrite" — is also weak here, for the reasons in §1: no UI libraries
to replace, a logic-heavy component layer that ports, and a design system that is 93 tokens.

**Do not adopt react-native-web for the beta.** `web/` is the enterprise channel and works;
replacing it is a separate decision. But **structure for it**: move `web/app/lib/` into an npm
workspace package (`packages/shared`, plain JS, no bundler) consumed by both apps, so the helpers
the repo already guards against drift (`ppwFromAnnual`, `stageOfGrade`, `normalizeBudget`…)
have one copy. That is the same "one seam" rule CLAUDE.md applies to `ppw_from_annual` across
Python/JS, applied across web/mobile.

## 7. Phasing (estimate, AI-assisted, one founder)

| Step | Work | Est. |
|---|---|---|
| 0 | Deploy the API (container + volume, HTTPS); `EXPO_PUBLIC_API_URL`; storage shim in `lib/`; mirror `section_history` server-side | 1 wk |
| 1 | Expo scaffold, Router, fonts, tokens, dark theme, `MeyyMark`, Login/OTP | 1 wk |
| 2 | **LessonView** + My Classes + My Lessons (the teaching loop) | 2 wk |
| 3 | FirstRun → PrepareLesson → ProfilePortal → Teaching profile | 1 wk |
| 4 | Settings (Support, Legal, Privacy, subscription status), Ask Meyy, exports via share sheet | 1 wk |
| 5 | TestFlight + Play internal testing; real OTP provider replaces `0000` | ½ wk |

**≈ 6–7 weeks to a testable beta**, with the teaching loop usable on a phone by the end of week 4.
GuidedTour, store billing (§5B) and Year Plan export come after the beta.

## 8. What to ask Claude for, in order

Not "convert the Next.js app". Instead: (1) extract `lib/` into `packages/shared` with the storage
shim, keep web green; (2) scaffold Expo with the token module and fonts; (3) port `LessonView`
against the real `/plans/…/view` JSON; (4) the two list screens; (5) FirstRun; (6) the rest.
Each step ships a screen against the live API, so reuse is proven, not assumed.
