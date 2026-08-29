# Naming & IP — the ARUVI blocker and the search for a replacement

**Status: CONVERGED, not closed** — sessions of 2026-08-28/29. ★★ **Leading candidate: MEYY**
(மெய், truth) — the only name of 95+ screened whose IPIndia register position is verified,
**by the founder's own searches: exact wordmark ZERO in classes 9, 41 and 42** (§4.12).
Remaining gates: the five-teacher test, and an attorney filing. **Second: AMAIYAL** (§4.9,
screened clean, register unsearched). Nothing here has yet been run past a trademark
attorney. §9 (Verification status) still governs what is and is not established.

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

## 4. Screening results — 95+ candidates. ★★ **Leading candidate: MEYY (§4.12)** — revived by
the founder's channel argument and cleared by the founder's own IPIndia searches (exact wordmark
ZERO in classes 9, 41 AND 42). **Second: AMAIYAL (§4.9)** — screened clean but register
unsearched. Neutral fallbacks §4.7

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

### 4.5 Round 4 — ★ pure phonetic coinage, no meaning (8 screened, **3 clear — best yield**)

Construction rules (§3.6 applied strictly): CV alternation · 2–3 syllables · **single vowels
only** · safe consonants only (b d g j k l m n p r s t v z) · **no initial cluster** (Tamil
breaks them) · no education derivation · no given name. Precedent: **Zoho** — a Tamil Nadu
company, a meaningless name, a global software brand.

| Name | Verdict | Reason |
|---|---|---|
| **Tomiro** | **CLEAR** | Cleanest across every check. Surname rank 4,649,889th worldwide, **zero India**; Behind the Name: no matches. No company, app or edtech found anywhere. **`tomiro.com` published at $3,300**; `tomiro.in` NXDOMAIN. ⚠️ Reads as **TOMATO** (Wiktionary auto-corrected the query) — compounded in India by Zomato; **Miro** is in-sector |
| **Zumira** | **CLEAR** | **Nothing in education anywhere.** ≤4 Indian name-bearers vs 1,369 Brazilian. `zumira.in` NXDOMAIN; `zumira.com` a broker lander, no published price. ⚠️ **Zumira-L**, a listed Indian prescription antacid (Healthmate Pharma, Lucknow), owns Indian search results; `-ira` reads pharmaceutical |
| **Nebori** | **CLEAR** | **1 name-bearer worldwide** — the cleanest name-check of the session. No company at scale, no exact-name app, nothing in education. `nebori.com` $4,395. ⚠️ **Nebo** (MyScript), a student note-taking app on Play/App Store/Indus, is Nebori minus two letters — same broad category |
| Milaro | CROWDED | `milaro.in` is a live Indian D2C womenswear brand (Delhi/Indore) using the exact wordmark; also parses as Hindi *milao* (mix/match) |
| Talora | CROWDED | **Talora Mecatronix** (Vadodara, 2016) holds `talora.in`; both app stores taken (50K+ installs on Play); Italian adverb "sometimes" — **not a coinage**; one consonant from **Zalora**, live in India via Myntra |
| **Sanivo** | **CROWDED** | ★ **"Sani-" is शनि, Saturn** — the malefic graha, root of *Shanivar*/*Śanivāram* (Saturday) in Telugu, Kannada, Marathi, Hindi. Reads **inauspicious** to an Indian ear. Both domains taken by pharma-shaped holders |
| **Kivo** | **FATAL** | **KiVO Learning International** is an AI **K-12 platform targeting CBSE**; **Kivo.ai** (Noida) sells "Kivo for Education"; a Kivo app is live in Play's **Education** category; `.com` and `.in` both delegated. One consonant from **Vivo** |
| **Belora** | **FATAL** | **Belora Cosmetics** — Indian, Gurgaon, **$3.86M from Sequoia Surge / DSG**; **Amravati (Belora) Airport** inaugurated April 2025; **three** exact-name apps across both stores |

★ **The lesson of this round: meaninglessness is a hypothesis, not a guarantee.** Five of
eight deliberately-invented words accidentally collided — with a religious morpheme, a CBSE
edtech, a funded cosmetics brand, an airport, a Hindi verb and an Italian adverb. The lane
produces the best yield of any tried (3/8 vs 3/12, 1/8, 1/8) **and produces the first
candidates clear on the deep checks simultaneously** — education sector, given name, and
Indian-language meaning. But it only works with the screening attached; **Sanivo would have
passed inspection by any English speaker.**

**Recommended next step: run volume in this exact shape.** At a 3-in-8 rate another 16
candidates yields ~6 more, giving a shortlist of nine to choose from rather than three to
compromise on.

### 4.6 Round 5 — phonetic coinage, volume run (16 screened, 3 clear)

Same construction rules as §4.5, with round-4's failure modes added as explicit checks
(Indic morphemes, Indian brand adjacency, Indian place names, Hindi verb stems, Romance
words, pharma-shaped endings).

| Name | Verdict | Reason |
|---|---|---|
| ★ **Zunabo** | **CLEAR — best of 57** | **Both `.com` and `.in` verified NXDOMAIN** — the only name all session with a free `.com`. Forebears has **no entry at all**. No company in any sector, no Play app, 0 results Apple India, nothing in education. Weak signals only: Arabic/Urdu *zunūb* (sins — different vowel and stress), *zuna-* ≈ Marathi/Gujarati *junā* (old). Zuno Insurance / ZunRoof share the onset, neither is a consonant away |
| **Nozibo** | **CLEAR** | `.com` and `.in` both NXDOMAIN (verified from gTLD SOA). No company any sector. ⚠️ One voicing feature from **nocebo** ("I will harm"); reads as an Nguni feminine given name (cf. Nozipho) |
| **Tobelu** | **CLEAR** | No company, no edtech, no Indic meaning. ⚠️ `.com` is a live German personal art site (won't sell). Note *-lu* is the Telugu plural suffix, so it sounds Dravidian-native while meaning nothing |
| **Venoli** | **FATAL** | ★ **Tamil வானொலி (*vānoli*) = RADIO** — a common noun in a core target language. Also a village in Palakkad, Kerala; sits between Ventolin and Ventorlin |
| **Ledumo** | **FATAL** | One letter from **EDUMO** — a live **teacher lesson-prep edtech** (edumo.io) on both app stores, *and* `edumo.in`, an Indian education brand. The embedded EDU is descriptive, so examiners would discount it, collapsing the difference to a bare leading "L" |
| **Zedimo** | **FATAL** | `zedimo.com` is a live, branded **study-abroad education business** |
| **Tebano** | **FATAL** | Ordinary dictionary adjective in Italian *and* Spanish ("Theban") + a *frazione* of Faenza — TALORA and BELORA failure modes stacked |
| Tuloma | CROWDED | ★ **EdTech Tulna** — IIT Bombay/IIT Madras, Central Square Foundation, same Sanskrit *tul-* root: the **government-adopted EdTech Evaluation Index Indian states use to score and procure learning software** (~₹1,700cr). Naming the product after its own examiner. Also the Tuloma River/settlement, Murmansk |
| Duvaro | CROWDED | **दुवारो is a live Hindi/Urdu inflection** of दुवार — "doors/gates", also "vertigo". The MILARO failure mode. `duvaro.io` was a scam CFD broker and owns page one |
| Torebi | CROWDED | **Kannada ತೊರೆ (*tore*) = "to abandon, forsake, give up"** — hostile reading for a planning tool. Bengali তোরে is the informal downward "you" |
| Kinabo | CROWDED | Exact-name app live on Google Play (5,000+ installs); Urdu *kīna* = **malice, grudge**; reads as truncated Kinabalu; `.com` $2,795 |
| Kemido | CROWDED | An **open-source Java/Spring framework** ships as `kemido` on GitHub; Gujarati hears *kem* ("how", as in *Kem cho?*); `.com` on BrandBucket |
| Nebito | CROWDED | `nebito.rs` is a live **software** company; "Nebi" ≈ Arabic *nabī* (prophet) |
| Bezoli | CROWDED | `.com` parked; Hindi/Urdu privative *be-* prefix invites a "without-something" parse (cf. *bezaar*, fed up); shares Bisleri's shape |
| Robeni | CROWDED | `.com` registered but dormant; English **"rob-"** onset — Play's own search resolves it to robbery games |
| Kubeni | CROWDED | **"Kube" reads Kubernetes** — wrong sector signal for software; plus an exact-name published board game |

### 4.7 ★ Shortlist — six viable candidates

| Rank | Name | Domain | Remaining cost |
|---|---|---|---|
| **1** | **Zunabo** | **`.com` + `.in` both free** | Nothing material found |
| 2 | Nozibo | both free | *nocebo* adjacency |
| 3 | Tomiro | `.com` $3,300 | reads as *tomato*; Miro in-sector |
| 4 | Nebori | `.com` $4,395 | **Nebo**, a student note-taking app |
| 5 | Zumira | broker, unpriced | **Zumira-L** antacid owns Indian search; `-ira` reads pharma |
| 6 | Tobelu | held by an active site | — |

**Zunabo led on every measurable axis** — and was then **rejected by the founder** (2026-08-29)
on the one axis no screen reaches: *"doesn't feel Indian enough"* and *"the sound is wrong."*
Both objections were correct and diagnosable — see §4.9, where the construction rules turn out
to have been accidentally Bantu rather than Indic. **This shortlist is superseded by AMAIYAL
(§4.9); it is retained because every name in it remains viable if the Tamil route is dropped.**

### 4.8 Round 6 — ★ four-letter Sangam / classical Tamil (8 screened, **0 clear**)

Premise: take the **poetics terminology** (akam, karu, iyal — scholars' terms from the
Tolkappiyam) rather than the imagery (aruvi = waterfall, nila = moon), on the theory that
technical terms don't become baby names. **The theory held — and it did not help.** Three of
four in batch A are not Tamil given names; they died of direct education-sector occupation
instead.

| Name | Verdict | Killed by |
|---|---|---|
| **Akam** (அகம்) | **FATAL** | Two **co-equal spellings**, both taken: **Agamverse Studios** is a live Indian K-12 edtech shipping Agam AR/Agam Games on both stores; **Agam EDU** (Pune) is a school ERP; **AKAM** is Akamai's NASDAQ ticker + a US trademark + an Indian software company. The Tamil Lexicon also files *akam* < Skt. *agha* = **sin/pollution** and *aham* = **ego** |
| **Karu** (கரு) | **FATAL** | Standing alone கரு reads **foetus** (dictionary neighbours are obstetric; கரு அகற்றல் = abortion). Last mass-media use in TN was a **Lyca-produced 2018 horror film titled *Karu*** about an aborted foetus. **Karu Learning** is an AI-for-schools platform live on the Indian App Store. Real given name: Karu Palaniappan, Karu Jain, Karu Jayasuriya. Kannada ಕರು = calf |
| **Neri** (நெறி) | **FATAL** | **NERI IAS Academy**, Perambur, Chennai — bilingual Tamil/English, TNPSC, with a "Junior IAS" track **from Class 11**. Plus St Philip Neri schools (Kerala) and the Syro-Malabar congregation at philipneri.in. All three domains parked. *Etymology was correct: path/method/right conduct, Thirukkural 356* |
| **Iyal** (இயல்) | **FATAL** | **Xam Guide Pvt Ltd (Salem, TN)** ships **"Iyal Math — grade-matched, curriculum-aligned"** (K–2) and "Iyal Exam Prep" on `iyal.app`. Plus Iyal Academy (Madurai) and Iyal Technologies (Erode). **இயல் is the Samacheer Kalvi word for a textbook UNIT** — naming lesson software "Unit". TN government spells it **EYAL** on its own portal |
| **Odai** (ஓடை) | **FATAL** | One transposition from **Odia** (language of Odisha, ~35M speakers); one letter from **Oda Class**, a Bengaluru K-12 edtech, $12.7M raised, ₹86.5cr FY25 revenue. `odai.com` is a live AI assistant; US Class 42 mark pending. Register is "drainage channel", not brook |
| **Amai** (அமை) | **FATAL** | **EUTM 018217316 "AMAI" WORD MARK, Classes 9/16/35/41/42** — specification reads like this product's spec sheet ("AI software… instructional and teaching materials… provision of instruction… SaaS"). Plus **Indian reg. 4626390, Class 42, filed at the CHENNAI IPO**. Plus AMAI Academy and Aamaai Academy (Indian K-12 coaching). **IAMAI** — one letter away — runs the India EdTech Consortium. Homograph ஆமை = turtle; அம்மை = smallpox |
| **Arum** (அரும்) | **FATAL** | One grapheme from **ARUN** — 1,343,634 Indians, the **63rd most common forename in India**, vs 316 Arums. A plain search returns **8 of 8 botanical results**. Grammatically a bound attributive awaiting its noun |
| **Uram** (உரம்) | **FATAL** | ★ **உரம் is the modern Tamil word for FERTILIZER.** Tamil Wikipedia's உரம் article *is* the fertilizer article, **with no disambiguation to "strength"**; TN newspapers use it for urea and subsidy raids; it is printed as "Uram" on Tamil Nadu manure sacks. The Sangam sense (fortitude, *Paripāṭal* 12,51) survives only inside compounds (மன உரம், நெஞ்சுரம்) |

★ **Three lessons worth carrying.**

**(a) Make the two-spelling test the FIRST gate for any Tamil word, not the last.** It killed
three of four in batch A before any market check was needed, and the evidence is decisive in
each case: **Wiktionary's own Tamil headword for அகம் romanises it *agam***; the **Government
of Tamil Nadu spells இயல் as "Eyal"** on its Art and Culture portal; Tamil's phonemic vowel
length cannot survive Roman script, so *karu* and *kāru* collapse into one string. Cost: ten
minutes. Decisiveness: total.

**(b) Every one failed as Aruvi failed, in a new costume.** Not bad luck. **A short, resonant
Sangam word is exactly what a Tamil founder naming an education business reaches for** — so
the competition is everyone who had the identical instinct. The well being drawn from is the
well Aruvi came from.

**(c) URAM is the instructive near-miss.** Zero education crowding, `uram.in` free, npm and
PyPI free, **clean on the Indian register in classes 9/41/42**, best transliteration
stability of the four, and the one name a Tamil teacher would spell right on first hearing.
It fails on a single unalterable fact about the language. When a candidate is clean on every
external axis and still fails, the failure is semantic — which is the whole argument for
meaningless coinage.

### 4.9 Round 7 — ★★ longer Tamil words + Tamil-rooted coinages (8 screened, **1 clear — AMAIYAL**)

**Why this round exists.** The founder rejected Zunabo (§4.7) on two grounds: *"doesn't feel
Indian enough"* and *"the sound is wrong"* — **not** on meaninglessness. ★ **Diagnosis of my
own error: the §3.6 construction rules were accidentally BANTU, not Indic.** CV alternation +
single vowels + no clusters + b/d/g/k/l/m/n/z + vowel endings describes Swahili and Nguni
phonotactics almost exactly — which is why the screeners kept flagging Zulu/Setswana adjacency
(Nozibo→Nozipho, Kinabo→Tanzanian surname, Ledumo→Setswana, Kubeni/Robeni→Nguni locative).
**Two specific faults: (a) /z/ is not an Indic phoneme** — absent from Sanskrit, absent from
Tamil, entered via Persian and still reads foreign; I reached for it because Zomato and Zepto
did, but those are deliberately modern-neutral, not Indian-sounding. **(b) "No initial
clusters" was over-strict** — Sanskrit is full of them (Krishna, Prakash, Shravan) and banning
them removed much of what makes a name sound Indian. **Corrected palette:** k g ch j t d n p
b m y r l v s sh h — **no z, f, w, q, x**; endings -a, -i, -am, -an, -ai, -ya; mid-word
gemination (-tt- -nn- -ll- -pp-) is characteristically Indic, not a defect; 6–8 letters per the
length finding.

| Name | Verdict | Reason |
|---|---|---|
| ★★ **Amaiyal** (அமையல்) | **CLEAR — best candidate of the session** | **Forebears: ZERO bearers worldwide**, forename or surname, any spelling — passes the Aruvi kill criterion outright. Zero Indian companies (MCA: 99 fuzzy, **0 exact**), zero education businesses, zero apps. **`amaiyal.com` AND `amaiyal.in` both NXDOMAIN.** Morphologically legitimate: அமை- ("to be arranged, settled, composed, suitable", 15 Lexicon senses) + the -அல் தொழிற்பெயர் suffix, patterning as செயல் / ஆடல் / பாடல் — a literate Tamil speaker parses "the arranging" unprompted. Transliterates cleanly **because it contains no intervocalic ப/த/க** (see the fault line below). Sonorants only — soft in the mouth |
| **Amaippu** | **FATAL** | ★ **அமைப்புகள் is the Settings app label on every Tamil-language Android phone** (verified against Google's own Tamil Android Help) — a mobile-first teacher app named after the menu she taps to change her ringtone. Also கல்வி அமைப்பு = "education system" (generic in-category), and `amaippu.com` is a live Indian AI SaaS (Dehradun), both domains on the same Route 53 account |
| **Ullurai** | **FATAL** | ★ **The first four letters — and first two spoken syllables — are ULLU**: a 10M-download Indian adult OTT platform the **Government of India ordered ISPs to block in July 2025** for obscenity. Also उल्लू = Hindi "owl", colloquially "fool". `ullurai.in` was the only free domain of the four, on the one name with a pornography-ban collision |
| **Thodar** | **FATAL** | In modern Tamil தொடர் means **TV serial**; **தொடர் கல்வி is the established Tamil term for "continuing education"** (Class 41 descriptiveness); `thodar.in` is a live Tamil financial-education brand using the identical wordmark in both scripts; Indraveen Technologies (TN) already ships software called "Thodar" |
| **Thodari** | **FATAL** | தொடரி = **train**; *Thodari* (2016, Dhanush/Keerthy Suresh) owns 10 of 10 first-page results and is still live on Prime/Play/IMDb. Lexicon's actual sense is a jujube shrub |
| **Marabu** | CROWDED→fatal | Meaning is genuinely excellent (Marapiyal is the Tolkāppiyam's ninth chapter) and the given-name screen passes (3 bearers in India) — but **every authority spells it MARAPU** (Wiktionary's headword: மரபு • *marapu*, IPA /mɐɾɐ**b**ɯ/), and **three Roman forms are in live commercial use** incl. a 10k-install Tamil app "MARABHU". `marabu.com` and `marabu.in` both sit with **Marabu GmbH** (German ink maker, est. 1859, ships "Marabu ColorManager" software). `themarabu.com` already markets itself as *"rooted in the Tamil word for heritage"* |
| **Muraiya** | CROWDED | Not a coinage — முறையா is the live colloquial clipping of முறையாக ("properly") **and** the interrogative "இது முறையா?" (*is this proper?*). Reads as an incomplete sentence. **Suraiya** is one grapheme away and a mass Indian female given name |
| **Nerali** | CROWDED | **Nirali Prakashan** — 40-year Indian academic/textbook publisher, 20,000+ titles, one vowel away, same sector. Kannada ನೆರಳು = shadow, ನೇರಳೆ = jamun/purple; Malayalam നീരാളി = octopus; நேரலை = "live broadcast" one vowel away. Recorded as a caste sept among the Holeyas |

★ **THE TRANSLITERATION FAULT LINE, stated as a pre-filter.** Any Tamil word containing an
intervocalic **ப / த / க** (written unvoiced, spoken voiced) WILL split in Roman script:
akam/agam · Iyal/Eyal · marapu/marabu/marabhu · toṭar/thodar. **Filter the candidate pool to
words built on sonorants — ல் ள் ர் ற் ம் ந் ண் வ் ய் — before spending any research.** That
single rule would have eliminated Marabu and Thodar in advance, and it is exactly why Amaiyal
transliterates cleanly.

★ **AND THE DEEPER LESSON: the Lexicon tells you what a word MEANT; it cannot tell you what it
MEANS.** Uram→fertilizer · Karu→foetus · Thodar→TV serial · Amaippu→the Settings menu. Every
one had an impeccable classical sense and a fatal living one. **Always check the modern
everyday register before the classical citation.**

⚠️ **Fourth wrong etymology of the session, recorded as a standing caution.** ULLURAI is NOT
*ul* + *urai* ("inner word/commentary") as I had it. It derives from **உள்ளுறு-**, second
element **உறை** (alveolar ṟ) = *to dwell, abide* — "that which dwells within". Prior errors:
*pathkram* is not a word (it is *pathyakram*); *sutradhar* in modern Hindi means "mastermind of
a conspiracy"; *kramya* is attested as "to be treated medically". **Verify every claimed
etymology against a dictionary before it reaches a decision.**

**Amaiyal — the three conditions.** (1) **Never spell it AMAIYAAL** — அமையாள் is attested in
**Kuruntokai 366** (`வேறு யான் கூறவும் அமையாள்`, "though I say otherwise, she is not
appeased"). (2) **Lock a Tamil-script mark, அமையல், beside the wordmark** — wisdomlib's Lexicon
mirror already resolves the Roman string "Amaiyal" to **ஆமையாழ்** (*tortoise-lute*); the script
kills that and the spelling scatter together. (3) **IPIndia classes 9/41/42 — still owed.**
Before any of it: **say it to five Tamil-medium teachers** and hear whether they land on
"arrangement", "tortoise", or nothing. No database can run that test.

### 4.10 Round 8 — ★ the மெய் (mey, "truth") family: CLOSED, eight forms, eight failures

The founder circled the root மெய் (truth/reality/authenticity) through eight forms across a
day. Each failed on **independent** grounds — the signature of an occupied semantic
territory, not bad luck. Ledger:

| Form | Died on |
|---|---|
| **Mey** | **Mey GmbH** — German lingerie maker, €123M, 1,100 staff, owns mey.com; `mey.in` parked on DaaZ; 3 letters |
| **Meyx** | **`meyx.com` is a live gambling/betting site** ("Meyx Bets"); Mexx International's registered marks one letter away; X has no Tamil phonology — the name cannot be written in the script of its own root |
| **Meyva** | A real word — Crimean Tatar/dialectal Turkish for **fruit**, one letter from Hindi मेवा (dry fruits); **MEYVA is a live French dried-fruits brand** (Palimex); MEVA (German formwork) and MEWA (German textiles) adjacent |
| **MeiX** | **Aurally identical to Meyx** — the hearer can't know which spelling was chosen, so a share of word-of-mouth is delivered to the betting site. `meix.com` = Shanghai fintech (¥100M Series B+) |
| **Mei** | Common East Asian **given name** (the Aruvi rule); sounds identical to "May"; mei.com = Chinese luxury flash-sales site; **MEI = Mathematics in Education and Industry** (UK maths-education body). `mei.in` free — the only clean square |
| **Meyy** | ★★ **VERDICT REVERSED — see §4.12.** Originally failed as spelling-invisible-in-speech; the founder's channel argument (link-mediated distribution in a closed teacher community) demoted that from kill to tax, and his own IPIndia searches then cleared the register |
| **Meyyal** | ★ **FIFTH ETYMOLOGY ERROR: -அல் is DEVERBAL** (செய்-→செயல், ஆடு-→ஆடல்) **and மெய் is a noun only — the coinage is ill-formed**, so a literate Tamil ear repairs it to **மையல் (maiyal) = infatuation/lust/madness** (Kural 838; a 2025 Tamil film; two hit film songs). `meyyal.com` broker-priced $1,500; **Meiyal Foods** (TN spices, meiyal.in) already pitches "Mei signifies truth" |
| **Meyyam** | Well-formed and beautifully corroborated — **Thirumayam** (Pudukkottai Divya Desam) is literally glossed "place of truth", Satya Kshetram — but **MAIYYAM Knowledge and Careers Pvt Ltd** (Coimbatore, inc. 2022, ACTIVE) is an **edtech with apps on both stores**, phonetically near-identical, same sector, same state; மையம் = "centre" crowds every near-romanisation (Maiyam.com Pvt Ltd, Makkal Needhi Maiam). `meyyam.com`/`.in` both free — and still not takeable |

★ **The morphology rule this round bought:** -அல் forms verbal nouns from VERB roots.
**Amaiyal works because அமை is a verb** (McAlpin: "become settled; be suitable; construct").
மெய் is a noun, so மெய்யல் violates the pattern — and an ill-formed coinage is repaired by
the native ear toward the nearest real word, which is where the damage lives. **Check the
root's part of speech before coining with any Tamil suffix.**

★ **Also bought: the mei/mey glide fork.** மெய் romanises as MEY *and* MEI in live use
(Meyyaram/Meyyanathan vs Meivazhi/Meiyappan, roughly co-equal) — a second transliteration
fault line alongside §4.9's voicing one: Tamil எய்/ஐ collapses unpredictably into Roman
ey/ei/ai. Amaiyal carries a milder version (AMAIYAL/AMAYAL); its mitigation is the
Tamil-script lockup + registering variant-spelling domains as redirects.

**Also screened from founder proposals, same period:** **LTG** (§4.11) · **TAVO** (right
shape, 7+ holders — see the length table) · **Stute** (German for "mare"; Stute
Nahrungsmittelwerke; initial cluster; truncation of "institute") · **Dingo** (dingo.com =
Australian predictive-maintenance software; DINGG = Indian salon SaaS one letter away;
Australian slang for coward/cheat) · **Nunuk** (★ **FATAL at maximum severity: "nunu"
(নুনু/नूनी) is child-slang for penis in Bengali and Hindi** — Wiktionary-attested, cognate
across Marathi/Odia — unsayable in a staff room; also a Javanese girls' pet name) ·
**MyLP revisited** (§4.11).

### 4.12 ★★ MEYY — the leading candidate (verdict reversed 2026-08-29, register-verified)

**The name.** MEYY, from Tamil **மெய்** — truth, reality, authenticity. Linguistic status,
stated precisely: the standard romanisation of மெய் is **MEY** (மெ = "me", ய் = "y" — nothing
is truncated; the doubled y in மெய்யம்/Meyyappan is sandhi, appearing only before vowel-initial
suffixes). **MEYY is therefore a brand stylisation, not the dictionary spelling** — but a
deliberate one: to a Tamil-literate eye the doubled y signals the ய்-final word unambiguously
(bare "Mey" could be misread மே), and the stylisation is precisely what makes the string
vacant. The Tamil-script mark **மெய்** should be locked beside the wordmark so the
stylisation resolves for Tamil readers.

**★ Why the original rejection was reversed — the founder's channel argument (2026-08-29),
conceded as correct.** The radio test (§3.3) was weighted for consumer apps discovered by
spoken referral + typed search. This product's buyers are **a dense, closed community —
teachers — and in India that community runs on WhatsApp.** The realistic transmission event is
a **forwarded Play Store link in a staff WhatsApp group** (or a QR at a training), which
carries its own spelling: zero transliteration loss. Under that weighting, spelling-invisible-
in-speech drops from first-order kill to second-order tax. What does NOT demote: trademark
collisions, app-store search hygiene, and meaning-collisions in the ear (மையல் was never a
spelling problem). §3.3's radio test stays first-order **for consumer-pattern products only**;
for closed-community products, register and store checks lead.

**★★ The register — searched by the FOUNDER HIMSELF on tmrsearch.ipindia.gov.in
(2026-08-29), the first candidate of 95+ to clear the check everything else still owes:**
- **Exact wordmark MEYY: ZERO hits — no registration, no abandonment — in classes 9, 41 AND
  42.** (Aruvi, for contrast: the identical word, registered, for identical services.)
- **Phonetic search: 324 rows across 41/42/multi-class + a class-9 set of the same shape —
  and not ONE mark contains MEY, MEIY or MAIY anywhere in it.** The volume is IPIndia's
  crude sound-code returning every M+vowel mark (MAYA, MAA, MAHA, MI, MW…) — algorithmic
  noise, not risk.
- **The honestly-citable set:** MYY (cl 42, reg., generic software services) — closest on
  paper, but "my" vs "mey" differs in vowel and length; **MAI (cl 41+42, ParentOf Solutions —
  parenting/child-development, the only education-adjacent citation, the one to name to the
  attorney)**; ME / MY / MEE / MEW / MEH (publications, BookMyShow ticketing, events —
  different services, weak short marks).
- ★ **The register's own coexistence precedent is the reply to any citation:** ME, MEE, MEH,
  MEW, MY, MYY, MAI and MAYA are all REGISTERED SIMULTANEOUSLY, side by side, in these very
  classes. The office has repeatedly allowed one-vowel-apart short marks to coexist. That
  history + the மெய் etymology (a dictionary word of an Indian language = inherently
  distinctive for software) is the examination story.

**Standing asset check (all verified 2026-08-29):** `meyy.in` **unregistered** (NXDOMAIN);
`meyy.com` broker-parked on Dan.com (price unknown — walk away if extortionate; meyy.in +
getmeyy.com suffices); **no company named Meyy anywhere, any sector**; **no Play app** named
Meyy (web-indexed check); Apple name unverifiable from outside — checkable only by creating
the app record. Mey GmbH (German lingerie, mey.com) is **class 25** — clothing vs software:
no allied-goods conflict expected, search-noise only.

**Known costs, accepted with eyes open:** (a) the **leak tax** — spoken "Meyy" = Mey/Mei/May,
so some unaided-search traffic lands on lingerie/a Chinese retail site/the month; mitigations:
link-first distribution, the Tamil-script lockup, owning meyy.in; (b) **MEI = Mathematics in
Education and Industry** (UK maths-education body) shares the sound in exam-adjacent contexts;
(c) four letters means the .com is squatted (the length rule held even here — the stylisation
is what created the vacancy).

**The claim sequence (urgency calibrated honestly, 2026-08-29: nothing is a two-week panic;
the real deadline is DISCLOSURE — the day the name is first said outside is the day these
should already be done):**
1. **Register `meyy.in`** — ₹500, ten minutes. Checks so far were DNS-over-HTTPS (leak-free);
   buy at a different registrar from any whose search box was used.
2. **Apple**: Developer Program ($99/yr, individual) → Bundle ID (pick ONCE — `in.meyy.app`
   or `com.meyy.app`, same root on both stores, unchangeable after first Play upload) → App
   Store Connect → New App → Name "Meyy". **Saving the record IS the reservation and the
   availability check.** ⚠️ Records with no build for ~180 days can be reclaimed — reserve
   within sight of a TestFlight build.
3. **Google Play**: names are NOT unique — no reservation exists. The permanent claim is the
   **package name**, taken by the first AAB upload to any track (internal testing suffices; a
   hello-world Expo shell works). $25 one-time; Indian ID verification; ⚠️ new personal
   accounts owe a closed test (~12 testers/14 days) before production — the five-teacher
   group is the right size.
4. **IPIndia filing in classes 9 + 41 + 42** via an attorney, மெய் etymology in the
   application as the distinctiveness story, ready for MYY/MAI citations with the coexistence
   precedent. File **before public launch**.

**Still owed before commitment:** the **five-teacher test** — say "Meyy" to five Tamil-medium
teachers; do they read மெய்? (Run it AFTER step 1 — the test is the first disclosure.) And
the attorney's read on MAI (ParentOf) specifically.

**Head-to-head with AMAIYAL, honestly:** Amaiyal is screened cleaner in the abstract (zero
bearers, zero leak tax, both domains free, morphologically impeccable) but its register search
was never run; Meyy carries a known leak tax but is now the only candidate with a
founder-verified clear register, and — the unscreenable input that §4.7 said would decide —
**it is the name the founder actually wants.** Eleven proposals and eight forms of one root
were data: founder conviction is a real asset, and Meyy has it.

### 4.13 Founder proposals (5 screened, 0 clear)

| Name | Verdict | Reason |
|---|---|---|
| Cademy | FATAL | `cademy.io` — live UK **platform for educators**: bookings, CRM, payments, AI course builder |
| Tutr | FATAL | TUTR, Tuscaloosa on-demand tutoring app, `tutr-app.com`. Vowel-drop fails the radio test; *tutor* names the wrong user |
| Skolar | FATAL | Taken 4+ times **including in India** — Skolar (Bengaluru, 2020, `facebook.com/skolar.in`), Skolar UK (2015), `skolar.online`, Skolar AI Flashcards on both stores |
| Kademi | FATAL | `kademi.co` — partner-management platform with an LMS; on G2 (24 reviews), Capterra, GetApp under **education software**. Also Turkish, not Indian, in sound (*kadem* = foot) |
| Socra | FATAL | `socra.com` AI goal platform **whose AI coach is named Socrates**, on both stores; `socra.org` = SOCRA, the CCRP certification body. *Best of the five* — suggestive, not descriptive, and failed only on availability |

★ **TAVO — CROWDED/FATAL, but the right shape.** Passes every §3.6 construction rule (2
syllables, CV-CV, single vowels, safe consonants, no initial cluster, one obvious spelling).
Failed only on occupancy: **seven-plus live holders, several in software** — Tavo
(tavoapp.co, business-management/POS), **Tavo — AI Roleplay Frontend** on *both* stores, TAVO
App (Tavo Sleep LLC, App Store), TAVO Tech (software development), TAVO Media Group, Tavo
Packaging, Tavo Adventure Gear. Also a given name twice: Spanish diminutive of *Gustavo*, and
a Lithuanian masculine name. ⚠️ Unverified but worth a native check: *tavo* may be the
Lithuanian possessive "your"; and Indian **tava/tawa (तवा)**, the kitchen griddle, is one
letter away and universally known.

★★ **THE FINDING THAT GENERALISES — LENGTH IS AVAILABILITY.** Measured across the 66 names
screened in this document:

| Length | Outcome |
|---|---|
| **3 letters** (LTG) | Dozens of holders incl. a listed company in-sector |
| **4 letters** (Akam · Karu · Neri · Iyal · Odai · Amai · Arum · Uram · Kivo · Tavo) | **10 of 10 taken** |
| **6–7 letters** (Zunabo · Nozibo · Tomiro · Nebori · Zumira · Tobelu) | **Free, or buyable for a few thousand dollars** |

Short names feel punchier, but the space is exhausted — a four-letter Latin string competes
against every founder in every industry on earth. **The habitable zone starts around six
letters**, which is precisely why Zunabo returned both domains unregistered while ten separate
four-letter candidates — Tamil words and coinages alike — came back taken. Do not spend
another round below six letters.

★ **LTG ("Learn. Teach. Grow.") — FATAL, and instructive.** **LTG is Learning Technologies
Group plc**: London Stock Exchange (AIM) listed, founded 1986, "market leader in workplace
digital learning and talent management", 30+ countries, owner of **Open LMS**, Bridge and
Watershed — a public company whose whole business is digital learning, on exactly those three
letters. Also **lamotrigine** (standard clinical shorthand for the antiepileptic), Lieutenant
General, Lithuanian Railways, Latgalian, Limits to Growth. **The structural point matters more
than the collision: an acronym has meaninglessness WITHOUT availability — the worst of both.**
Meaninglessness is only valuable because it buys an empty namespace (§5); three-letter strings
are the most contested namespace there is, so you pay emptiness and collect nothing. Acronyms
are also a retreat from fame, not a route to it — IBM, TCS, L&T and NIIT were all full names
for decades first. ⚠️ Fair counter, recorded because §3.2's "never" was too strong: **India
accepts acronyms more readily than the West** (TCS, HCL, ITC, and NIIT is education and well
known) — but each spent decades and large budgets earning the compression, which is the
opposite of a pre-launch solo founder's position. On the tagline: "Learn. Teach. Grow." leads
with **Learn**, which centres the *student* — the buyer is a qualified teacher, not a pupil —
and three generic category verbs describe every education product ever built.

Also reasoned about and rejected without screening: **MyAruvi** (§1.3) and **MyLP**
(descriptive + acronym + the "My X" IA collision; *LP* already means long-playing record, and
*limited partner* in any fundraising conversation; and it names the compliance artifact, not
the teaching — see §6.2).

---

## 5. ★ The structural finding

Across the **first three** lanes — 33 names, 3 weak survivors, none unambiguously good, and
one of those three (Folio) downgraded on a second look. The pattern did not vary:

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

## 8. Next actions — REWRITTEN 2026-08-29 after the MEYY register clearance (§4.12)

**Done since first drafted:** the phonetic-coinage rounds ran (§4.5–4.6); the Tamil lanes ran
to completion (§4.8–4.10); ★ **the founder ran the IPIndia searches himself for MEYY —
wordmark zero in classes 9, 41 and 42, phonetic field clear of the MEY family** — the first
and only candidate to clear the register.

**Now, in order:**
1. **Register `meyy.in`** (₹500) — before the name is spoken to anyone outside.
2. **Five-teacher test** on MEYY (and optionally AMAIYAL as control): say it aloud, ask what
   they hear. The one check no tool can run.
3. **Apple name reservation + Play package claim** per §4.12 steps 2–3.
4. **Attorney engagement** (~₹5–15k): file MEYY in 9 + 41 + 42; get a read on MAI (ParentOf,
   cl 41+42) and MYY (cl 42) as the likely citations; the coexistence precedent (§4.12) is
   the reply. While engaged, also pull the full record for **ARUVI 5933400** (proprietor
   address identifies which business Harikrishnan G runs) — closes §1.2's open inference.
5. **Answer §7.2** (paperwork vs teaching) — now decoupled from naming, but still owed for
   positioning and the sub-line under the logo.
6. Review **Almanack.ai** and **Staffroom.pro** as product competitors, independent of naming.
7. If MEYY fails the teacher test or the attorney's read: **AMAIYAL** (§4.9) is next — run its
   IPIndia search (incl. AMAYAL/AMMAIYAL phonetics) before attaching to it; then §4.7's
   neutral shortlist.

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
