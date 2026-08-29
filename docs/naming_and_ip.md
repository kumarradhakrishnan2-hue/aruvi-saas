# Naming & IP — the ARUVI blocker and the search for a replacement

**Status: OPEN — decision not made.** Session of 2026-08-28/29. Nothing here has been run
past a trademark attorney, and **no candidate name has been checked against IPIndia**.
Read §7 (Verification status) before acting on anything.

---

## 0. The finding, in one paragraph — READ FIRST

**ARUVI is registered as a bare wordmark in Class 41 for EDUCATIONAL SERVICES** (appl.
5933400, Harikrishnan G, valid to 2033), alongside **ARUVI ONLINE** (5937004, same owner,
filed three days later). Class 41 is closed to us. Classes 9 and 42 are technically open —
no ARUVI exists in either — but educational *software* is routinely held allied and cognate
to educational *services* in Indian practice, so expect a s.11 citation and a live
opposition window. Worse than the single registration: **at least five separate Indian
education businesses trade as Aruvi**, so even a perfect deal with the registrant leaves us
the sixth Aruvi in Indian education. The diagnosis is that *aruvi* is a common Tamil given
name, and naming a business after a personal name is the dominant Indian SMB pattern — the
word was never distinctive, in the ordinary sense or the trademark sense.
**Recommendation: rebrand.** Rationale in §5, cost in §2, open questions in §6.

---

## 1. The blocker

### 1.1 The register (source: founder's IPIndia export, `Aruvi_Trademark_Search_Combined.xlsx`)

| Appl | Mark | Class | Filed | Proprietor | Used since | Status |
|---|---|---|---|---|---|---|
| **5933400** | **ARUVI** | **41** | 12/05/2023 | **Harikrishnan G** | — | **Registered → 12/05/2033** |
| **5937004** | **ARUVI ONLINE** | **41** | 15/05/2023 | **Harikrishnan G** | — | **Registered → 15/05/2033** |
| 5202892 | ARUVI MELODY'S | 9 | 09/11/2021 | K. Srinivasan / SRK Sounds | 08/10/2021 | Registered → 2031 |
| 5901171 | ARUVI SOLAR ENTERPRISES PVT LTD | 9 | 21/04/2023 | Aruvi Solar Enterprises Pvt Ltd | 04/10/2021 | Registered → 2033 |
| 5496328 | ARUVI SOLAR | 9 | 20/06/2022 | Pukazhendhi Devi | 20/11/2021 | **Abandoned** |
| 1991007 | ARUVIAN'S R' SEARCH WITH DEVICE | 42 | 08/07/2010 | Natasha Banerjee | 01/04/2007 | Registered, valid upto **08/07/2020** — lapsed unless renewed |

**Both class-41 marks show `Used since ---`** — filed proposed-to-be-used. s.47 non-use
rectification would therefore not mature until roughly **Aug/Sep 2028**, and only if the
mark is genuinely unused. See §1.2 — assume it is used.

**No plain ARUVI exists in Class 9 or Class 42.** The class-9 marks cover audio electronics
and solar/electrical apparatus; neither covers software.

### 1.2 The crowding — five live Indian education businesses

| Business | Where | What |
|---|---|---|
| **Aruvi TNPSC Academy** | TN | `aruvitnpsc.com` + LMS at `learn.aruvitnpsc.com`; "Aruvi and Soundar's Test Series" |
| **Aruvi Campus** | Padur OMR Chennai · Thirupporur · Coimbatore | Government-exam coaching, ₹5,000/course, 4.8 Google rating |
| **Aruvi TNPSC Coaching Centre** | Namakkal | Coaching |
| **Aruvi Institute of Learning** | Tenkasi (opp. RTO) | Python / full-stack / DS / ML training |
| **Aruvi Educational Services** | — | `aruvieducationalservices.education` |

Adjacent: **Aruvii Pte Ltd** (Singapore, AI software for manufacturing — phonetically
identical, class-42 territory); **Aruvi AI Studio** (`aruvi.co.in`, Coimbatore).

**Best inference on the registrant:** Harikrishnan G is most likely **Aruvi TNPSC Academy** —
an offline academy plus a separate online portal maps neatly onto ARUVI + ARUVI ONLINE filed
three days apart. **This is inference, not fact.** To settle it, pull the full detail record
for 5933400 on IPIndia public search; it carries the proprietor's **address** and the agent of
record. Match the address against the table above.

### 1.3 Why "MyAruvi" does not work

Considered and rejected. "My" is a possessive/laudatory prefix that carries no weight under
the dominant-feature test — the memorable element remains ARUVI. **The registrant already
owns ARUVI ONLINE**, i.e. the registry has already treated "Aruvi + generic word" as one
family belonging to him. Getting past examination (Indian examination is inconsistent enough
that it might) would not survive his four-month opposition window, and registration under
s.28 has never been a defence to passing off. It also collides with our own IA vocabulary,
where "My X" means *a section of the app* (My Classes, My Lessons, MyPlans.jsx).

### 1.4 Options

1. **Assignment or letter of consent** from Harikrishnan G, carving out K-12 teacher
   lesson-planning software in classes 9/42 and leaving him class 41 whole. A consent letter
   overcomes a s.11 citation. His customers (adult government-exam aspirants) and ours
   (K-12 teachers) are genuinely different, which is the fact pattern coexistence is for.
   **Do not approach him directly or reveal that we are already built on the name** — that
   prices the deal. ⚠️ **This clears one of six.** The other four have common-law rights
   from actual use, and passing off does not require registration.
2. **Rebrand.** See §2 for cost, §3–5 for the search.
3. **File 9 + 42 and proceed.** Not advisable for a name about to be baked into a signed
   user agreement, invoices, and email templates.

---

## 2. What a rename would cost — audited 2026-08-28

**The name is not load-bearing.** Verified by grep across `api/`, `aruvi_core/`, `web/`.

### 2.1 What does NOT move (no migration, no regeneration)

- **Plan cache key** is `_e{GENON_ENGINE_VERSION}_c{canonical_version}` — no brand token.
  **The 990-file certified library and its derived cache are untouched. Nothing regenerates.**
- Library paths: `saved_plans/{subject}/{grade}/{year}/…`
- All 14 Bucket-B state stores: `{kind}/{tenant}/{user}/{year}/…` (accounts, consents,
  invoices, readiness, section_state, prepared_plans, plan_archive, plan_notes, entitlements,
  academic_years, allocations, support, outbox, erasure_log)
- **All 51 API routes**
- localStorage teaching state (`lu_pointer_*`, `lu_done_*`, `current_chapter_*`)
- `consent_and_disclaimer_v0.1.md` — no brand token in the filename, so **a rename does not
  force re-consent**
- **No conditional anywhere branches on the string "aruvi."** The only literal matches are
  env-var names being read.

### 2.2 Where it actually lives — all mechanical

| Category | Scale | Nature |
|---|---|---|
| `aruvi_core` package + imports | ~250 refs | Directory rename + sed |
| `ARUVI_*` env vars | 28 distinct, ~130 refs | All `os.environ.get(NAME, default)` — behaviour unchanged; update launch config |
| `X-Aruvi-User` header | 20 refs | Private contract between our own two servers |
| Display strings (mail_templates, `render/html.py`, FastAPI title, package.json) | ~75 | Pure copy |
| `.aruvi` CSS wrapper in `render/html.py` | ~28 | Self-contained — style block and `<div>` in one file |

The 33 `globals.css` hits are **all prose comments**. No CSS variable or class is named
`--aruvi-*` or `.aruvi`.

### 2.3 The two items touching data already written

1. **`ARV-` / `ARV-S` reference prefixes** — already parameterised as
   `config.INVOICE_PREFIX` / `config.SUPPORT_PREFIX`, env-overridable, passed to adapters as
   constructor args. A config edit, not a code change. One support record (`ARV-S-742`) and
   three outbox emails carry it, and that reference was mailed to a real address. **`ARV` is
   an abbreviation, not the word — it can reasonably survive a rename.**
2. **`aruvi-theme`** localStorage key — rename it and each user's theme resets to default.

### 2.4 ⚠️ The one trap

**`X-Aruvi-User` must change on both sides in the same commit**, or `_current_identity()`
falls back and every teacher silently becomes the fallback tenant. Same class of defect as
the three-seeding-paths ppw bug of 2026-08-27: *count the places before declaring it done.*

### 2.5 Not a code question

The consent document body and mail templates name Aruvi as the **contracting party**, and
signatures in `consents/_ledger/` reference it. Whether those carry through a rename is for
the attorney. The mechanism if not is publishing v0.2 of the agreement — **add a file, never
edit** (the versioning rule of 2026-08-27).

---

## 3. What should drive a name

### 3.1 Honest empirical picture

Startup naming lore is largely **survivorship bias** — we never see the companies that failed
with excellent names. The one effect that survives scrutiny is **processing fluency**
(easier-to-pronounce names rate more favourably; Alter & Oppenheimer found it even in
post-IPO ticker performance). Real, replicated, small. Distribution, product and timing dwarf
the name. Note the asymmetry: **a good name is worth little; a bad name charges rent
forever.** The goal is not a great name — it is avoiding the taxes.

### 3.2 The six types, and which are out for us

| Type | Examples | Verdict |
|---|---|---|
| **Descriptive** | PayPal, Salesforce | **OUT** — near-unregistrable in 9/41/42 without acquired distinctiveness; its payoff is SEO and our distribution is word-of-mouth; boxes us in (assessment is already in the product) |
| **Suggestive** | Amazon, Stripe, Slack | **IN** — legally strong, evocative, room to grow |
| **Arbitrary** | Apple, Blackberry | **IN** — strong; pay in marketing to build the association |
| **Coined** | Kodak, Google, Spotify | **IN** — strongest legally, domains available, meaning must be filled |
| **Eponymous** | Ford, Bloomberg | **OUT** — carries no credibility in Indian edtech; ties company value to a person |
| **Acronym** | IBM, HP | **OUT** — always a retreat from fame, never a start |

### 3.3 The governing constraint

The buyer is a K-12 teacher in India, likely not English-first, on a phone, who will most
often **hear the name spoken by a colleague in a staff room.** Word of mouth is the primary
channel. Governing test: **can she hear it once and type it correctly?**

### 3.4 Hard screens (cheapest first — 1–3 kill most candidates in seconds)

1. Google `<name> + education / school / India` — a crowd appears → kill
2. Google Play and Apple App Store, exact name
3. Domain: exact-match `.com` or `.in` available or cheaply acquirable
4. IPIndia public search, classes 9/41/42, wordmark, "Start With" **and** Phonetic
5. Meaning check: Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Marathi
6. **Not a common Indian given name** — see §3.5
7. Fit: sits in "scholarly planner on warm paper"; no collision with My X / units / rail /
   ledger / margin / chapter / period
8. Only then: attorney clearance on the final two or three

### 3.5 ★ The highest-yield screen — the given-name rule

**Aruvi failed because it is a common Tamil given name.** Naming a business after a personal
name is the dominant Indian SMB pattern, which is why five education outfits landed on it
independently. **Reject any word that is a common given name in any major Indian language.**
Sanskrit is dense with them (Usha, Arun, Prabhat, Nitya, Setu are all order/dawn words *and*
people's names), so this screen matters most in exactly the lane that feels most resonant.

### 3.6 Form constraints

- 2–3 syllables, 5–9 letters
- **One obvious spelling.** Test: say it to five people, count spellings. >1 → reject
- Avoid Indian-English orthographic traps: v/w · t/th and d/dh (Vidya/Vidhya/Vithya) ·
  doubled vowels (Aruvi/Aruvii) · i/ee · s/sh
- **No numerals, hyphens, or deliberate misspellings.** The Flickr/Toppr device fails the
  radio test hardest and is downstream of 2010-era domain scarcity, not insight
- Must survive **"Ask ___"** — that is a shipped feature name

---

## 4. Screening results — 33 candidates, 3 weak survivors

⚠️ **What the verdicts mean.** **CLEAR = "no Indian education business found using this
name"** — the screen that Aruvi failed, and the one that matters most. **It does NOT mean
available.** Every survivor still needs domains, app stores, global-sector collisions and
IPIndia checked independently. Folio was originally logged CLEAR on that basis and is
revised to CROWDED below; the general heuristic is that **a short, common English word with
a pleasant meaning is essentially never free — if it looks available, the screen was too
shallow.** Only **Docera** has a confirmed-acquirable domain (`docera.com`, $5,000);
`sheaf.com` is taken, and Folio's and Kramik's are undetermined.

### 4.1 Round 1 — real English school/paper words (12 screened, 3 clear)

| Name | Verdict | Reason |
|---|---|---|
| **Sheaf** | **CLEAR** | No education collision found, Indian or global. Same-name holders: a Sheffield forklift dealer, a finance SaaS, a UK consultancy. ⚠️ Uncommon noun — comprehension by Indian teachers untested |
| **Folio** | **CROWDED** ⚠️ *revised 2026-08-29* | Passed the Indian-education screen and **nothing else**. **FOLIO** (EBSCO / Index Data) is an established open-source **library-services platform** — education software; **Folio Collaborative** is a US non-profit running **teacher professional development** across ~145 schools; Folio (Japan) raised $158M; the Folio Society is a known publisher; multiple Folio apps on Play, one marketing to students, one India-facing; `folio.com` / `folio.in` **undetermined — assume taken**; `-folio` is a diluted suffix |
| **Docent** | **CLEAR → dropped** | Zero Indian education businesses. **Dropped: near-homophone of "decent," a very high-frequency Indian English word.** Also carries no meaning for an Indian teacher (US = museum guide; Europe = academic rank) |
| Satchel | CROWDED | **Satchel One**, $20M, 4,500 schools, **live in Indian App Store and Play** |
| Vellum | CROWDED | `vellum.ai` $20M YC company publishing edtech content; `vellum.in` held by an Indian party |
| Lark | CROWDED | ByteDance's Lark deployed in Indian education (Narayana Group, 400k students); Lark Health owns `lark.com` |
| Lantern | CROWDED | Three Indian education entities; 150M-download VPN of the same name |
| Overture | CROWDED | Overture Maps Foundation (Amazon/Meta/Microsoft); Overture Learning (US K-12) |
| Gather | NEAR-FATAL | `gather.town`, $77M, **runs an education use-case page**; generic verb |
| **Slate** | **FATAL** | Five-plus Indian education businesses — exact repeat of the Aruvi failure. Plus Slate Magazine, Slate by Technolutions (2,000+ colleges) |
| **Chalk** | **FATAL** | `chalk.com` is **PowerSchool's K-12 lesson-planning product** (Planboard, 250k teachers) — our exact category. Six Indian Chalk- edtech brands |
| **Almanac** | **FATAL** | **Almanack.ai** sells AI lesson planning to Indian CBSE/ICSE teachers; "almanac" is the generic Indian word for a school diary |

### 4.2 Round 2 — coined from English roots (8 screened, 1 clear)

| Name | Verdict | Reason |
|---|---|---|
| **Docera** | **CLEAR** | From Latin *docere*, to teach. No Indian education presence, no app listing, **`docera.com` purchasable at $5,000**. ⚠️ Caveat: **Doceree**, a $65M-funded Noida healthtech, is indistinguishable spoken |
| Folia | CROWDED | `folia.com` = Folia Inc (iAnnotate), names teachers as users, apps on both stores. **Means "folly / revelry" in Portuguese and Spanish** |
| Lessonry | CROWDED | `lessonry.com` live US literacy business; dense cluster with Lessonly, Lessonary, LessonApp |
| Bindery | CROWDED | Not a coinage — a working trade noun, current in the Indian print industry. `bindery.com` live |
| Alongside | CROWDED | `alongside.care` established US K-12 platform, now shipping a teacher product; owns the exact Play listing |
| Wellread | CROWDED | Live in AU/NZ school libraries; exact name taken on both stores; misdescribes a lesson planner |
| **Teachly** | **FATAL** | **Teachly Edutech Pvt Ltd**, Lucknow, **incorporated Oct 2025**; `teachly.in` live |
| **Staffroom** | **FATAL** | `staffroom.pro` is **a UK primary-school lesson-planning app**; `thestaffroom.in` incorporated Jan 2025 |

### 4.3 Round 3 — Sanskrit-rooted coinage (8 screened, 1 weak clear)

| Name | Verdict | Reason |
|---|---|---|
| **Kramik** | **CLEAR (weak)** | क्रमिक = gradual/sequential. Nothing found as name, business or app. ⚠️ It is an **adjective** (names a property, not a thing); "Karmik"/karma pull; and see the KRAM- problem below |
| Kramya | CROWDED | Not a given name, `.in` appears free — but `.com` owned and renewed to 2028. क्रम्य is attested Sanskrit meaning "to be treated medically," not "sequenced" |
| Anukram | CROWDED | **Anukram Analytics LLP**, Mumbai, active since Dec 2023 — Indian *software* company, same TM classes. `.in` a live business, `.com` $6,750 |
| Upakram | CROWDED | **In Marathi it is the ordinary word for "school activity"** — सहशालेय उपक्रम is the Maharashtra department's own term. `upakram.com` a live Salesforce consultancy. Confusable with *Upakarma* (Brahmin ritual) |
| Tantu | CROWDED | `.com` and `.in` both resolve; "Tantu AI" live on Play; unresolved **Vedantu** adjacency (*veda* + *tantu*) |
| Pathkram | CROWDED | **Not a real spelling** — the word is *pathyakram*. And it means "syllabus," i.e. descriptive of the category |
| **Pathya** | **FATAL** | पथ्य = **the diet prescribed to a sick person** — everyday vocabulary in Hindi, Marathi, Bengali (পথ্য) and Tamil (பத்தியம்). Every live Pathya property is a diet/Ayurveda business. Govt "e-Pathya" exists |
| **Sutradhar** | **FATAL** | **Caste surname** — WB 49%, Assam 37%, Tripura 13%. `sutradhar.com` is a Bangalore non-profit *equipping teachers with resources*. Modern Hindi = **"mastermind of a conspiracy"** |

### 4.4 ★ The KRAM- family problem (systemic)

**In English, KRAM- reads as a stylised spelling of "cram."** C→K is a standard branding swap
(Kwik, Kool, Kar), so an English-medium reader does not see a different word. *Cram* is the
most loaded negative word in Indian schooling and precisely the pedagogy NCF 2023 exists to
displace — and NCF alignment is our core claim. It softens for a Devanagari reader who parses
क्रम instantly; **it does not soften in English, which is the language our marketing is read
in.** This takes out Anukram, Kramya and most of Kramik as a family.

### 4.5 Founder proposals (5 screened, 0 clear)

| Name | Verdict | Reason |
|---|---|---|
| Cademy | FATAL | `cademy.io` — live UK **platform for educators**: bookings, CRM, payments, AI course builder |
| Tutr | FATAL | TUTR, Tuscaloosa on-demand tutoring app, `tutr-app.com`. Vowel-drop fails the radio test; *tutor* names the wrong user |
| Skolar | FATAL | Taken 4+ times **including in India** — Skolar (Bengaluru, 2020, `facebook.com/skolar.in`), Skolar UK (2015), `skolar.online`, Skolar AI Flashcards on both stores |
| Kademi | FATAL | `kademi.co` — partner-management platform with an LMS; on G2 (24 reviews), Capterra, GetApp under **education software**. Also Turkish, not Indian, in sound (*kadem* = foot) |
| Socra | FATAL | `socra.com` AI goal platform **whose AI coach is named Socrates**, on both stores; `socra.org` = SOCRA, the CCRP certification body. *Best of the five* — suggestive, not descriptive, and failed only on availability |

Also reasoned about and rejected without screening: **MyAruvi** (§1.3) and **MyLP**
(descriptive + acronym + the "My X" IA collision; *LP* already means long-playing record, and
*limited partner* in any fundraising conversation; and it names the compliance artifact, not
the teaching — see §6.2).

---

## 5. ★ The structural finding

**33 names, 3 weak survivors, none unambiguously good** — and one of those three (Folio) had
to be downgraded on a second look, which is itself evidence for the finding below. The
pattern did not vary across three independently-designed lanes:

> **A name derived from your category's vocabulary is already taken, because the derivation is
> obvious to everyone else in the category too. Distance from the category word IS the
> availability.**

Academy, tutor, scholar, lesson, teach, chalk, slate, staffroom, *krama*, *pāṭha* — every one
produced collisions. **The names that were available were available because they were wrong**
(Docent: clear *and* meaningless to our buyer; Sheaf: clear *and* an uncommon noun).

The three screens are in tension by construction: **availability correlates with obscurity,
warmth correlates with familiarity, familiarity correlates with crowding.** "Warm, familiar,
available English word" is close to an empty set.

**Resolution — relocate the warmth.** Stripe, Notion, Figma, Linear are not warm words; the
warmth in those products lives in the writing and the design. Ours already does: *"Good
morning. Today you teach three classes"* is warmer than any noun. Fraunces on warm paper is
warm. **Drop warm as a naming requirement; keep it as a product requirement.** That opens
arbitrary coinage, which is also the strongest trademark position and the cheapest domain.

**The lane not yet tried — phonetic coinage.** Sound carries the lineage, meaning stays empty.
Two syllables, open vowels, -a/-i ending, no consonant cluster a Tamil or Bengali mouth must
break, one obvious spelling, **no derivation from any education word**, screened hard against
Indian given names. This is what actually won here: **Swiggy** is not derived from food,
**Zomato** not from restaurant, **Nykaa**'s Sanskrit root is invisible, **Vedantu**'s *tantu*
is invisible, **Zerodha** means "zero barrier" and no customer knows it. Etymology is
decorative backstory for the About page, not communication. It also sidesteps the
Tamil/Sanskrit political question entirely — an invented word takes no side.

---

## 6. Competitors discovered (byproduct — arguably worth more than the names)

| Competitor | What | Why it matters |
|---|---|---|
| **Almanack.ai** | AI lesson planning with a **dedicated Indian-teachers page**, `en-IN` locale, CBSE/ICSE/state-board plans for Classes 1–12, 15+ boards, report cards | **Our product, our customer, our market.** Highest-priority review |
| **PowerSchool** (Chalk / Planboard) | K-12 lesson planner, 250k teachers. **~1,450 India staff** (1,300 Bengaluru, 175 Chennai), Chennai CoE opened Oct 2025, acquired **Neverskip** (2024) reaching **900+ Indian schools, 1.2M students** | Not a distant foreign incumbent — an actively expanding Indian operator |
| **Staffroom.pro** | UK primary lesson-planning app, £5/mo, curriculum objectives dragged into a weekly timetable, AI assistant, PDF/Word export | Closest analogue to our UX model |
| **Lessonary.org** | AI lesson-planning platform | Same category |
| **Satchel One** | $20M, 4,500 schools across 20+ countries, **live in Indian app stores** | Teacher-facing K-12, present in our stores |
| **Sutradhar** (Bangalore) | Non-profit "equipping teachers with materials, methods and knowledge" | Indian, teacher-facing, non-commercial |

---

## 7. Open decisions (founder)

1. **Consent letter vs rebrand.** Evidence favours rebrand: a deal with Harikrishnan G clears
   one of six, and the commercial problem — a teacher searching "Aruvi" meets a crowd — is
   untouched by any legal instrument.
2. ★ **What is the product selling — relief from paperwork, or better teaching?** This
   determines whether a descriptive name is right. In Indian schools the lesson plan is
   largely *the record the HM inspects*; if removing that burden is the job to be done, then
   naming the artifact is correct positioning and §3.2's rejection of descriptive names is
   wrong. Everything in CLAUDE.md points to the second (the calendar purge, benefit-first,
   the Monday-morning north star) — but the first is what most Indian teachers would name as
   their problem. **Note the channel split:** a descriptive name likely serves the Enterprise
   (school) buyer better and the Individual (teacher) buyer worse.
3. **Tamil beachhead vs pan-India neutral.** A Tamil-rooted name buys warmth and a TN
   beachhead; it reads regionally on a pan-India NCF product. Founder chose **neutral
   English/coined + warm** on 2026-08-28; §5 argues for relaxing "warm."
4. **Whether to relocate warmth to the product voice** (§5). Recommended.

---

## 8. Next actions

1. **IPIndia manual search** — pull the full detail record for **5933400** (proprietor address
   + agent) to identify which business Harikrishnan G runs. Captcha'd portal; cannot be
   automated.
2. **Attorney clearance opinion** on the allied-and-cognate exposure of filing ARUVI (or any
   successor) in classes 9/42 against a class-41 registration. ~₹5–15k. Do this before any
   branding spend.
3. **Answer §7.2** — it determines the whole brief.
4. **Run the phonetic-coinage round** (§5), then screens §3.4 1–3, then IPIndia on survivors.
5. **Registrar lookups** on every domain marked undetermined below.
6. Review **Almanack.ai** and **Staffroom.pro** as product competitors, independent of naming.

---

## 9. ⚠️ Verification status — what is and is not established

- **Trademark data in §1.1 is authoritative** — the founder's own IPIndia export.
- **The registrant's identity (§1.2) is inference, not fact.**
- **No candidate name in §4 has been checked against IPIndia.** All "no Indian presence"
  findings are search-derived **absence of evidence, not evidence of absence.** The registry
  is a session-based captcha'd portal and cannot be queried programmatically.
- **"Domain undetermined" ≠ available.** `web_fetch` returns an empty body for
  bot-blocked, JS-only and non-existent hosts alike, and DNS/whois were blocked in the
  session sandbox. Every domain claim needs a registrar check before it is relied on.
- **§2's rename audit is grep-verified against the working tree** and is solid.
- ★ **Three Sanskrit meanings asserted in round 3 were wrong** and were corrected only
  because they were checked: *pathkram* is not a word (it is *pathyakram*); *sutradhar* in
  modern Hindi means "mastermind of a conspiracy," not the classical thread-holder;
  *kramya* is attested as "to be treated medically," not "sequenced." **Verify every claimed
  etymology against a dictionary before it reaches a decision.**
- Nothing in this document is legal advice.
