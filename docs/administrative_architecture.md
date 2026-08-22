# Aruvi — Administrative Architecture & the Ports a Partner Implements

**Status:** design settled, unbuilt. Written 2026-08-21.
**Read with:** `data/CLOUD_DATA_MODEL.md` (the Bucket A / Bucket B boundary), `CLAUDE.md §0`
(the mobile-first progressive-acquisition model), `aruvi_core/ports.py` (the existing seams),
and `docs/Aruvi_Technology_Partnership_and_Production_Roadmap.pdf` (the partner brief).

---

## 0. What this document is

Aruvi is a working product with no administrative half. Every API route today is
teaching-domain — `/readiness`, `/plans`, `/section-state`, `/genon/…` — and `Login.jsx` is a
bare user-ID box with no password. There is no account, no billing, no consent, no academic
year, no data-export path.

This document specifies that missing half: **what it must do, in what order, and — most
importantly — the exact ports an external technology partner implements.**

It is written to a constraint from the partnership roadmap (§4): *the providers should not be
selected simply because they are familiar to a freelancer.* So nothing here names a vendor.
Every step below defines a **Protocol** in `aruvi_core/ports.py` and a **file-backed reference
implementation** in `aruvi_core/adapters/`. The partner's job is to write a second
implementation of the same Protocol against whatever cloud they recommend. Nothing in the
engine, the API routes, or the React app changes when they do.

That is also the handover test the roadmap sets in §10: *another competent developer should be
able to take over the system without needing the original developer to explain how it works.*
A port with a docstring and a working file adapter beside it is that explanation.

---

## 1. Where the seams already are

The pattern is proven in this repo. `aruvi_core/ports.py` already declares:

| Port | State |
|---|---|
| `LLMClient`, `OutputCache`, `Storage`, `Repository`, `JobQueue` | declared |
| `AllocationRepository` | declared + file adapter + live |
| `ReadinessRepository` | declared + file adapter + live |
| `SectionStateRepository` | declared + file adapter + live |
| `PlanArchiveRepository` | declared + file adapter + live |
| `PreparedPlansRepository` | declared + file adapter + live |
| `AuthProvider` | **declared, one line, no implementation** |
| `BillingProvider` | **declared, two lines, no implementation** |

Five repositories already thread `(tenant_id, user_id)` through every method and are backed by
JSON on disk under `data/`. `api/config.py` keeps Bucket A (shared read-only content) and
Bucket B (per-tenant state) strictly apart. The holes for auth and billing are pre-cut and
empty.

**Identity today** is `_current_identity()` in `api/main.py`:

```python
def _current_identity(x_aruvi_user: Optional[str] = Header(default=None)) -> tuple[str, str]:
    uid = (x_aruvi_user or "").strip() or "local"
    return (uid, uid)          # tenant_id == user_id, asserted
```

That single function is the whole of Aruvi's identity model. Step 0 replaces its body.

---

## 2. The settled product decisions

These are founder decisions, already argued through. They constrain the steps below.

### 2.1 Cutover has two halves

- **(a) Aruvi's d-date.** Aruvi declares a date beyond which newly generated plans carry the
  next academic year's LP version. On that date the new authored canonicals go public and
  My Lessons restructures: current plans move into a year folder, the new year starts fresh.
- **(b) The teacher's declaration.** Offered from the day (a) lands, with a short explanation.
  When *she* declares it, My Classes performs cutover: section cards are cleared of attached
  LPs, and their pointers go with them.

These are genuinely different events — schools start at different times (CBSE runs April–March,
several state boards June–May) — and conflating them breaks one school or the other.

**Operational consequence:** (a) must precede peak planning. Teachers plan hardest March–June,
so the new canonicals must exist by roughly **January**, which makes the re-authoring batch run
a production schedule, not a preference.

### 2.2 LP versioning is by academic year — but the year is a LABEL, not the cache key

NCERT books are stable for years, but Aruvi's own constitutions, model and accumulated
corrections are not. So the library is re-versioned annually **regardless of whether the book
changed**. Canonicals and their generated variants live in a per-year folder; every canonical
and variant is stamped with its year, and both My Lessons and My Classes display that stamp so
versions can never be confused.

**But the cache key stays what it already is.** Derived plans are already named
`ch_NN_<matrix>_e<NN>_c<version>.json` — engine version and constitution version — and
`api/data.canonical_version` already reads it. `purge_derived.py` exists because stale-cache
bugs have already been met once.

> **Rule: year is the label, `(engine, constitution)` is the key.** At cutover, mark each
> chapter's canonical as *carried* or *new*. A carried canonical keeps its variant cache. Get
> this wrong and every June you re-pay to regenerate content that did not change, at peak load,
> in your busiest season. `CLAUDE.md §3` names output caching as the #1 economic lever at
> seasonal scale.

### 2.3 Mid-year changes are software updates, not versioning events

If generation logic changes mid-year, past plans must not move and new plans reflect the change
smoothly. This needs one hard companion rule:

> **A plan attached to a section is IMMUTABLE for the life of that attachment.**

This matters more in Aruvi than in most products: canonical unit counts vary, so re-deriving a
plan under a teacher can leave her pointer at "unit 7 of 17" pointing at nothing.

### 2.4 Chapter notes belong to a specific LP, and do not carry forward

Notes are tenanted and privacy-sensitive. They are keyed to **a particular LP** — which, since
canonicals carry a year stamp, means the year is captured too. At cutover they stay with the
previous year's plan, which she can still open from the year folder. New generation starts with
an empty note.

Consequences, all deliberate:

- **Editing a note IS deleting it.** No separate per-note delete flow. The thing she does every
  day is the mechanism.
- **No version history, ever.** This is what makes "she deleted it" simply true. Someone will
  later propose note history as a helpful feature; it would silently break the promise.
- **Last-write-wins needs a timestamp, not history.** Without versioning, a stale phone
  overwriting a fresh laptop edit is unrecoverable. Store `updated_at` and refuse to overwrite a
  newer server copy with an older local one. That is not history, it is not clobbering.
- One consequence to confirm in use: keying by LP means preparing two plans for the same chapter
  at different period counts yields two notes, where today there is one.

### 2.5 Subscription: annual, rolling, not academic-year aligned

Forcing renewal at year-end bunches revenue risk and mixes money with planning at the worst
moment. A subscription taken in Oct 2026 runs to Oct 2027, so it covers the next year's
planning season.

**Lapsed state: export and delete only.** No read-only tier, no "dummy access". But the floor
below is not a product tier — it is a legal and store requirement:

- She can always sign in to **download her data** and **delete her account**. DPDP erasure and
  access rights do not lapse with payment, and Apple guideline 5.1.1(v) requires in-app account
  deletion for any app that supports account creation.
- The export must carry **her notes with their plans** — otherwise she exports her lesson plans
  and silently leaves her own writing behind.

### 2.6 "No remnants" must be precise, not absolute

Three exceptions to state plainly rather than over-promise:

1. **Disaster-recovery backups are unavoidable** (roadmap §7, §10). The honest form is *deleted
   immediately from the live system, purged from backups within 30 days.*
2. **Tax records outlive the account.** GST invoices carry a statutory retention period. Her
   account, profile and notes can genuinely vanish; the invoice for what she paid cannot.
3. **Shared content is not hers.** A lesson plan is a *reference* to the shared library, never a
   per-tenant copy (`CLOUD_DATA_MODEL.md §2.3`). Deleting her account removes the reference.

### 2.7 The class list carries silently at cutover

She keeps the same classes into the new year and changes them herself if wrong — she will have
spent months in the product by then. This matches the profile's existing philosophy: warned,
never blocked; edited at a point, never redone wholesale.

**Re-offering the guided tour at cutover is DEFERRED** — revisit after a year of real use.

### 2.8 India's DPDP is on a clock

Rules notified **13–14 Nov 2025**. Soft enforcement through 2026; **hard enforcement ~13 May
2027** at the end of the 18-month transition. Aruvi launches into that window, so §§2.5–2.6 are
build-time requirements, not later polish.

One decision not yet made: chapter notes are free text and voice. If a teacher names a student
in one, Aruvi is processing children's personal data, which DPDP treats far more strictly
(verifiable parental consent). Either constrain that surface or accept the obligation
deliberately.

---

## 3. The two sequencing principles

**Do the re-filing first.** Some work changes *where* data is stored; some changes *what the
software does*. Re-filing is nearly free today — seven test accounts on one machine, all
disposable — and brutal after launch, when it means rewriting thousands of live folders without
losing a bookmark. Building a feature costs the same whenever. So the addressing changes go
first, even though they show nothing on screen.

**Do not pick the plumbing.** Build the half that holds true whichever cloud, database and
gateway the partner recommends: the domain records, the Protocols, the route contracts, the UI.
Leave a correctly shaped, empty socket for everything else.

---

## 4. The dependency chain

```
0. Account + tenant record  ──┬──→ 1. Year-scoped addressing ──→ 2. Cutover / rollover
   (the spine)                │         (cheap ONLY now)
                              │
                              ├──→ 3. PlanNoteRepository ─────┬──→ 4. Export / erase
                              │      (last data gap)          │      traversal
                              │                               │
                              └──→ 5. Entitlement seam ───────┴──→ 6. UI surfaces
                                     (the payment-shaped hole)
```

Nothing starts before **0** — every other step attaches something to that record. After it, two
chains run independently and can be done in either order. **6** is last: designing settings
screens around data that does not exist is how junk drawers form.

The only hard rules are **0 first**, **6 last**, **1 before 2**, **3 before 4**.

---

## 5. The steps

Each step below lists the port, its methods, the reference adapter, and what "done" means.

### Step 0 — Account + tenant record

**Why first:** billing, privacy, notifications and institutions all hang off it, and it is the
one place where `tenant` stops being an alias for `user`.

**New port — `AccountRepository`:**

```python
@dataclass
class Account:
    account_id: str            # stable internal id, never the email
    tenant_id: str             # today == account_id; a school later owns many accounts
    display_name: str
    email: str = ""
    phone: str = ""
    locale: str = "en-IN"
    school_name: str = ""
    status: str = "active"     # active | suspended | pending_deletion
    created_at: str = ""
    consent: Dict[str, Any] = field(default_factory=dict)   # {policy_version, accepted_at, channels}
    notify: Dict[str, Any] = field(default_factory=dict)    # {email: bool, push: bool, whatsapp: bool}

@runtime_checkable
class AccountRepository(Protocol):
    def load(self, tenant_id: str, user_id: str) -> Optional["Account"]: ...
    def save(self, account: "Account") -> None: ...
    def find_by_email(self, email: str) -> Optional["Account"]: ...
    def delete(self, tenant_id: str, user_id: str) -> None: ...   # §2.6 semantics
```

**Also in this step:** flesh out the existing one-line `AuthProvider` so a real identity
provider can sit behind it, and change `_current_identity()` to read the account rather than
assert `(uid, uid)`. That one function is the entire migration.

**Reference adapter:** `adapters/account_repository_file.py`, JSON under
`data/accounts/{tenant}/{user}/account.json`.

**Done when:** a teacher has a durable account record; `tenant_id` and `user_id` are separate
values that merely happen to be equal; nothing anywhere else re-derives identity.

---

### Step 1 — Year-scoped addressing

**Why now:** this is the single most time-sensitive item in the document. Half a day today; a
live data migration in two years.

Teaching state moves from `{kind}/{tenant}/{user}/…` to `{kind}/{tenant}/{user}/{year}/…`.

**Year-scoped:** section state (pointers, done, bookmarks) · allocations · prepared register ·
plan archive · chapter notes (via their year-stamped LP).
**Not year-scoped:** the account and subscription (rolling, §2.5) · her teaching profile — the
class list carries (§2.7).

**New port — `AcademicYearRepository`:**

```python
@dataclass
class AcademicYear:
    year_id: str               # "2026-27"
    starts_on: str             # ISO date — varies by board (CBSE Apr, several state boards Jun)
    ends_on: str
    is_current: bool

@runtime_checkable
class AcademicYearRepository(Protocol):
    def current(self, tenant_id: str, user_id: str) -> Optional["AcademicYear"]: ...
    def list_years(self, tenant_id: str, user_id: str) -> List["AcademicYear"]: ...
    def open_year(self, tenant_id: str, user_id: str, year: "AcademicYear") -> None: ...
    def set_current(self, tenant_id: str, user_id: str, year_id: str) -> None: ...
```

Every existing repository method gains a `year_id` parameter. Their Protocols change; their
callers change; the engine does not.

**Done when:** no Bucket-B teaching write can land without a year in its address.

---

### Step 2 — Cutover / rollover

Implements §2.1–§2.2. Two operations, not one:

- **Aruvi-side (a):** publish the new year's library; mark each chapter *carried* or *new*;
  carried canonicals keep their variant cache (§2.2); My Lessons folds the prior year into its
  archive folder.
- **Teacher-side (b):** clear section attachments and pointers for the closing year; carry the
  class list forward unchanged; leave notes with their old plans.

**Port — extends `AcademicYearRepository`:**

```python
@dataclass
class CutoverResult:
    closed_year: str
    opened_year: str
    sections_cleared: int
    carried_chapters: List[str] = field(default_factory=list)   # canonical unchanged → keep its cache
    new_chapters: List[str] = field(default_factory=list)       # re-authored → fresh cache

@runtime_checkable
class YearCutover(Protocol):
    def close_year(self, tenant_id: str, user_id: str, year_id: str) -> "CutoverResult":
        """Archive the closing year's execution state and open the next.
        IDEMPOTENT: a second call on an already-closed year is a no-op — a teacher WILL tap
        twice, and on a phone she will tap twice by accident."""
        ...
```

**Staleness:** a live subscriber teaching the new year on last year's cards is not forced to
cut over — forced erasure invites disputes. Soft email reminders, gated on
*subscription active AND academic year new AND section view old*. Better still, put the prompt
at the moment of intent: when she prepares a lesson that would be stamped a later year than her
sections, ask there.

**Done when:** June works. Bookmarks reset, plans and notes survive in their year folders, the
class list is untouched, and no regeneration bill arrives for unchanged chapters.

---

### Step 3 — `PlanNoteRepository` (the last data gap)

Chapter notes currently live **only in the browser** — no API route has ever seen one.
`CLOUD_DATA_MODEL.md §2.8` records this as the single known exception to Aruvi's own rule that
no teacher data exists without an owner, and §5 lists it as an invariant violation.

Browser-only is not "more private", it is *unaccounted for*: plain text on a shared school
machine, lost silently on a cache clear, and invisible to the export and erase rights in Step 4.

```python
@dataclass
class PlanNote:
    plan_key: str              # "{subject}/{grade}/{filename}" — the LP, year-stamped (§2.4)
    text: str
    updated_at: str            # the anti-clobber field (§2.4). NOT a version history.

@runtime_checkable
class PlanNoteRepository(Protocol):
    def load(self, tenant_id: str, user_id: str, plan_key: str) -> Optional["PlanNote"]: ...
    def save(self, tenant_id: str, user_id: str, note: "PlanNote") -> None: ...
    def load_all(self, tenant_id: str, user_id: str) -> Dict[str, "PlanNote"]: ...
    def delete(self, tenant_id: str, user_id: str, plan_key: str) -> None: ...
```

**Note for the implementer:** `save` must reject a write whose `updated_at` is older than the
stored one, and tell the caller — that is the whole of the multi-device protection, and it must
not grow into version history (§2.4).

**Done when:** her notes follow her across devices, **and she is told that they do.** Disclosure
is what makes holding them legitimate.

---

### Step 4 — Export and erase

One traversal, three obligations: DPDP data portability, DPDP erasure, Apple 5.1.1(v).

```python
@runtime_checkable
class DataRightsService(Protocol):
    def export(self, tenant_id: str, user_id: str) -> bytes: ...
    def erase(self, tenant_id: str, user_id: str) -> "ErasureReceipt": ...
```

**Export contains:** her account record, her teaching profile, and every chapter note across
every year — each note beside the plan it belongs to (§2.5). **Not** the lesson plan library:
that is shared content she already has as PDFs, and copying it per-tenant breaks the cache
economics and the IP model.

Word is the better format than PDF here — these are notes to her future self, and she will want
to extend them rather than only read them.

**Erase** walks the same path destructively and returns a receipt naming what was kept and why
(§2.6: backups for 30 days, tax records by statute).

> The export traversal is also the best tenant-isolation test you will ever write. If it can
> reach another tenant's row, RLS was never real.

**Done when:** both actions are reachable **while lapsed** (§2.5), and the erase receipt's
wording matches what the privacy policy actually promises.

---

### Step 5 — The entitlement seam (the payment-shaped hole)

This is the structure the thing you cannot build fits into.

```python
@dataclass
class Entitlement:
    plan_id: str               # "individual_annual"
    status: str                # trial | active | grace | expired
    valid_until: str
    source: str                # trial | manual | web | ios | android   ← the whole trick

@runtime_checkable
class EntitlementRepository(Protocol):
    def load(self, tenant_id: str) -> Optional["Entitlement"]: ...
    def save(self, tenant_id: str, ent: "Entitlement") -> None: ...
```

`BillingProvider` (already declared) gains the rest of its surface — `create_subscription`,
`verify_webhook`, `cancel`, `fetch_status` — and ships with a **`ManualBillingProvider`** where
the founder grants access by hand. Real behaviour, no gateway.

**`source` is why this must exist before any gateway is chosen.** Web takes Razorpay/UPI;
Android takes Play Billing; iOS takes Apple IAP at 15–30%, and on iOS "Manage subscription" must
deep-link into Apple's own settings rather than into Aruvi's UI. A subscription bought on her
phone has to be honoured on a school laptop. Entitlement resolved **server-side and
platform-tagged** makes that work; entitlement inferred on the device never will.

Put one `require_entitlement(account)` check in front of generation. That is the only place it
belongs — generation is what costs money.

**Done when:** the founder can grant, expire and revoke access without a gateway, and the
partner's work is to implement `BillingProvider` and populate `source`.

---

### Step 6 — The UI surfaces

Last, deliberately. Account, subscription, privacy, notifications, support, and the year-plan
budget control.

The design tension is real and worth stating: `CLAUDE.md §0` strips the shell to two tabs and a
gear on a benefit-first principle, and everything in this document is, by definition, *not*
benefit-first — it is obligation. So the question is not "where do these go" but **which of
these a teacher should ever have to look at at all**, versus which should stay invisible until
the one moment they matter.

Two rules that follow from the rest of this document:

- **Put each control where its number is used.** The annual budget belongs in Year Plan, beside
  the sentence that reads "a budget of N periods" — the only place she has the context to judge
  it. It is currently read-only prose there.
- **Disclose the assumptions.** First run asks three things and assumes the section, the
  periods/week and the calibrated annual budget. That is a feature — two taps to a real lesson
  plan is the product's pitch. The defect is never saying so.

---

## 6. Ports index

| Step | Port | Status | Reference adapter |
|---|---|---|---|
| 0 | `AccountRepository` | **new** | `account_repository_file.py` |
| 0 | `AuthProvider` | declared, expand | header stub → partner's IdP |
| 1 | `AcademicYearRepository` | **new** | `academic_year_repository_file.py` |
| 1 | all five existing repositories | **signature change** (`year_id`) | existing files |
| 2 | `AcademicYearRepository.close_year` | **new** | same adapter |
| 3 | `PlanNoteRepository` | **new** | `plan_note_repository_file.py` |
| 4 | `DataRightsService` | **new** | walks every Bucket-B repo |
| 5 | `EntitlementRepository` | **new** | `entitlement_repository_file.py` |
| 5 | `BillingProvider` | declared, expand | `ManualBillingProvider` |

Every one ships with a working file-backed implementation. The partner writes the second
implementation and nothing above the port changes.

---

## 7. Open items

- **Backup retention** — confirm 30 days is achievable before the privacy policy promises it.
- **GST retention period** — confirm the statutory figure with an accountant (§2.6).
- **Children's data** — decide whether to constrain notes or accept the DPDP obligation (§2.8).
- **Notes split per plan** — confirm two plans for one chapter yielding two notes is intended
  (§2.4); it reverses a deliberate 2026-07-23 "one surface" decision.
- **Periods/week** — nothing reads it while the budget is stored as `{method: "periods"}`, but
  it becomes load-bearing the moment she switches to the weeks method in her profile. Derive it
  (`round(budget / 30)`) rather than seeding a flat guess.
- **Institutional tier** — not built, but Step 0's tenant/user split is what keeps it cheap.

---

## 8. Invariants (grep-able, do not regress)

- No teacher data without `tenant_id` (+ `user_id` where row-owned). After Step 1, no teaching
  data without `year_id`.
- No shared content carrying a tenant key — it would break both cache economics and the IP model.
- A teacher's plan is a **reference** to the shared library, never a per-tenant copy of bytes.
- A plan attached to a section is **immutable** for the life of that attachment (§2.3).
- Notes carry **no version history** (§2.4).
- Year is a **label**; `(engine, constitution)` is the cache key (§2.2).
- Entitlement is resolved **server-side** and carries its **platform of purchase** (§2.5).
- Export and erase remain reachable **while lapsed** (§2.5).
- Core/engine never talks to a vendor directly — only through `aruvi_core/ports.py`.
