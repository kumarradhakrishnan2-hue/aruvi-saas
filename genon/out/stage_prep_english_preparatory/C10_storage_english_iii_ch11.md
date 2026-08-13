# C10 · Storage conventions — english · III · ch 11

**Verdict: 1, 2, 4 and 5 PASS. 3 is VACUOUS here and its corpus evidence no longer exists —
recorded, not failed. One defect raised, found while running check 2.**

> **Where the destructive checks ran.** Checks 2(b), 4 and 5 delete or move files, and the
> Cowork mount refuses `unlink` (`[Errno 1] Operation not permitted`). They were run against a
> **copy of the content tree at `/tmp/c10/content`**, served by a second API on port 8001/8002
> with `ARUVI_DATA_DIR` pointed at it. Identical code, isolated data. **The real corpus is
> untouched — 11 files still in `data/content/saved_plans/english/iii/`, 3 canonicals + 8
> derived.**

---

## 1 · Filename conventions — **PASS**, and this is the campaign's clearest proof of the chosen-variant rule

Library files: `ch_11_canonical.json` · `ch_11_canonical_p10.json` · `ch_11_canonical_p07.json`
— `pKK` zero-padded to the variant's period count.

Served plans, every one `ch_11_<matrix>_e19_c<version>.json`. The version token must be **the
chosen variant's** ledger timestamp, not the top's. This library's three canonicals have three
different ledger timestamps, so the rule is falsifiable here — and it holds on all seven:

| served filename | `variant_used` | version token | the chosen variant's ledger_ts? |
|---|---|---|---|
| `ch_11_40m9_e19_c20260813124142.json` | 10 | `…124142` | **p10** ✓ |
| `ch_11_40m8_e19_c20260813124508.json` | 7 | `…124508` | **p07** ✓ |
| `ch_11_40m6_e19_c20260813124508.json` | 7 | `…124508` | **p07** ✓ |
| `ch_11_40m11_e19_c20260813123304.json` | 12 | `…123304` | **top** ✓ |
| `ch_11_40m13_e19_c20260813123304.json` | 12 | `…123304` | **top** ✓ |
| `ch_11_50m5-40m7_e19_c20260813123304.json` | 12 | `…123304` | **top** ✓ |
| `ch_11_50m12_e19_c20260813123304.json` | 12 | `…123304` | **top** ✓ |

Ledger timestamps: top `20260813123304` · p10 `20260813124142` · p07 `20260813124508`.

**Three distinct tokens across one serve set.** Note X=8 in particular: `complete_rescue` serves
from **p07** while borrowing the *top's* synthesis unit, and the filename keys on **p07** — which
is exactly the e15 correction the route's own comment records (the old code recomputed the
next-highest here and would have stamped `…123304`, "the version of a file its bytes do not come
from").

**Matrix duration-aggregated longest-first:** `50m5-40m7` — 50 before 40. ✓

## 2 · Cache hit, and the purge that keeps it honest

**(a) Cache hit — PASS.** Repeating the X=9 request returns `cached: true` and the file's mtime
is unchanged.

**(b) Purge — PASS.** `purge_derived.purge('english','iii',11)` against the sandbox tree:

```
== derived plans invalidated by C10.2(b) verification ==
   removed  ch_11_40m11_e19_c20260813123304.json
   removed  ch_11_40m13_e19_c20260813123304.json
   removed  ch_11_40m6_e19_c20260813124508.json
   removed  ch_11_40m8_e19_c20260813124508.json
   removed  ch_11_40m9_e19_c20260813124142.json
   removed  ch_11_50m12_e19_c20260813123304.json
   removed  ch_11_50m4-40m7_e19_c20260813123304.json
   removed  ch_11_50m5-40m7_e19_c20260813123304.json
   (the next request for each rebuilds from the repaired canonical, ~11 ms)
```

It **printed what it removed**, 8 of 8 derived plans went, and **the library is untouched** —
all three `ch_11_canonical*.json` survive. The regex was checked directly rather than inferred:
it matches `ch_11_40m9_e19_c….json`, and refuses `ch_11_canonical.json`,
`ch_11_canonical_p07.json` and another chapter's `ch_12_40m9_e19_c1.json`.

**Credit where it is due, from the failed first attempt.** Run against the read-only mount, the
tool did not half-purge and exit quietly: it printed `COULD NOT REMOVE` for each file and
stopped with *"STOP: derived plans could not be deleted, so a stale plan can still be served.
Delete them by hand and re-run, or run this on a machine with write access."* That is the right
behaviour for a tool whose whole job is invalidation.

## 3 · No overwrite across engine versions — **VACUOUS, and the evidence the template cites is gone**

Ch 11 was first authored at **e19**, so there are no earlier-engine files for it to sit beside.
Recorded as vacuous rather than passed.

**More than that: the corpus-wide evidence testing.md points at no longer exists.** A sweep of
every served plan on disk finds **17 files, and ZERO chapters carrying more than one engine
version** — the e08–e13 files the template calls "the C10.3 no-overwrite evidence" have been
removed, almost certainly by the very mechanism check 2(b) mandates (`purge_derived` runs on
every repair and takes all engine versions of a chapter's derived plans with it).

**The two checks pull against each other**, and 2(b) wins: 3 wants earlier-engine files retained
as evidence, 2(b) requires derived plans to be gone after any repair. **The property itself still
holds by construction** — the engine version is a filename component, so a bump re-keys the cache
and cannot collide with an existing file. It is guaranteed structurally rather than observed.
Worth a template note at the next §9 revision; not a defect in this stage.

## 4 · Determinism — **PASS**

Deleted `ch_11_40m9_e19_c20260813124142.json`, re-issued the identical request:

- served fresh (`cached: false`), the file reappears;
- **byte-identical except the top-level `saved_at`** (`2026-08-13T13:12:34` →
  `2026-08-13T14:04:46`). Compared as normalised JSON with `saved_at` removed from both; no other
  key differs.

## 5 · Quarantine is invisible to serving — **PASS**

Moved `ch_11_canonical_p10.json` into `quarantine/english/iii/` and re-issued the requests p10
had been serving:

| request | before | after quarantine |
|---|---|---|
| **X=9** (was served by p10) | `variant_used: 10`, file `…c20260813124142` | **`variant_used: 12`**, `mode: fill`, file `ch_11_40m9_e19_c20260813123304.json`, **0 drops** |
| **X=10** (p10's own count) | `identity: true`, `ch_11_canonical_p10.json` | **not an identity serve**, `variant_used: 12`, `ch_11_40m10_e19_c20260813123304.json` |

The library glob no longer sees it, the serve falls to the next-highest surviving variant (the
top), coverage still completes with zero drops, and **no response names the quarantined file
anywhere** — `'p10'` appears nowhere in either payload. Restored afterwards; the sandbox library
is back to three canonicals.

---

## The defect this step found

**The genon repair toolchain does not honour `ARUVI_DATA_DIR`.** `purge_derived.py`,
`build_library.py` and `normalize_options.py` each compose
`REPO / "data" / "content" / "saved_plans"` directly, while `api/config.py` exposes `DATA_DIR`
(env `ARUVI_DATA_DIR`) as the seam §7 calls "the single root that migrates to the cloud". So the
API and the repair tools can address **different trees**.

Found the ordinary way: `purge_derived.py` was pointed at the sandbox copy via the env var and
purged the repo tree instead — visible in its own error paths. The mechanism had to be verified
by redirecting `purge_derived.CONTENT` in-process, which is precisely what the env var should
have done.

Filed **S4**: no live consequence today (nothing overrides `ARUVI_DATA_DIR` outside tests, and
the tests point at the same tree). But the failure mode it opens is **ARV-D-034 exactly** — a
repair lands, the purge cleans a tree nobody is serving from, and the stale plan keeps being
served — reached by a different route, and §7's seam is load-bearing for the Phase-4 migration.
