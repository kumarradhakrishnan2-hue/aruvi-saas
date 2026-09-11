# Meyy — the phone app (Track D)

Expo managed + Expo Router. Presentation only: client logic is `@aruvi/shared`
(`../packages/shared`), facts come from the API. Teacher-facing name **Meyy**; identifiers stay Aruvi.

## Run (first time, on the Mac)

```
cd <repo root>
npm install                      # workspace: web + packages/shared + mobile
cd mobile
cp .env.example .env.local       # already written on the founder's Mac — Supabase + Render values
npx expo install --fix           # aligns every native package to the installed Expo SDK
npx expo-doctor                  # should be clean
npx expo start                   # scan the QR with Expo Go (same WiFi as the Mac)
```

Test numbers `919000000001–3` sign in with OTP `123456` until DLT lands.

## Layout

```
app/_layout.jsx      boot → fonts → theme → stack
app/index.jsx        gate: signed in? → (app) : login
app/login.jsx        the front door (choose · OTP · sign-in) — the web's Login.jsx
app/privacy.jsx      Privacy Notice, no account needed
app/(app)/           the signed-in shell (step 2: proof screen; step 3: LessonView)
lib/boot.js          installs storage (expo-sqlite/kv-store, sync), API base, Supabase client
theme/tokens.js      GENERATED from web/app/globals.css — python3 theme/gen-tokens.py
theme/fonts.js       Fraunces · Newsreader · IBM Plex Mono, bundled
components/          MeyyMark (svg), Bar, OtpBoxes, Markdown (shared parser → Text), ui
```

Stress width 360×800 first, then 375 / 390 / 412 (CLAUDE.md §4).
