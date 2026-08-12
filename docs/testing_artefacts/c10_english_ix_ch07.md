# C10 — storage conventions · english · IX · ch 7 *Vitamin-M*

**Date:** 2026-08-12 · 3 library files + 7 served plans on disk · engine 19

**Four checks pass. Check 2 fails, and it fails on exactly the thing this stage spent ₹28.74
fixing: two of the seven served plans would still be handed to a teacher carrying the withdrawn
synthesis, from cache.** ARV-D-137, S2.

---

## 1 · Filenames — PASS, and the chosen-variant rule is proven live

Library: `ch_07_canonical.json` · `ch_07_canonical_p14.json` · `ch_07_canonical_p10.json` —
`pKK` zero-padded, no collision with the served pattern.

Served: `ch_NN_<matrix>_e<ENGINE>_c<chosen-variant-version>.json`, matrix duration-aggregated
longest-first. **Every one keys on the variant that actually served it, not on the top:**

| file | `variant_used` | c-token | that token is |
|---|---|---|---|
| `ch_07_50m9_…_c20260812142824` | 10 | 142824 | **p10's** ledger ts |
| `ch_07_50m11_…_c20260812142824` | 10 | 142824 | p10 |
| `ch_07_50m12_…_c20260812142352` | 14 | 142352 | **p14's** |
| `ch_07_50m13_…_c20260812142352` | 14 | 142352 | p14 |
| `ch_07_50m15_…_c20260812142352` | 14 | 142352 | p14 |
| `ch_07_60m2-50m13_…_c20260812142352` | 14 | 142352 | p14 · **longest-first** ✓ |
| `ch_07_50m16_…_c20260812141916` | 17 | 141916 | the top's (pre-re-author) |

## 2 · Cache hit and purge — **FAIL** (ARV-D-137)

**(a) the hit itself** is correct by construction and by code: `api/main.py` computes the
filename, and `if hit is not None` returns `cached: true` with the file untouched, discarding the
freshly served plan. The HTTP half (response flag + unchanged mtime) is owed to a run with
uvicorn up.

**(b) the purge is where it breaks — and the re-author is the case nobody wired.**
`purge_derived` is called from `normalize_options`, `repair_register`, `repair_anchors`,
`repair_leaked_deliberation` and `repair_item_type` — **every repair tool, and no generator.**
So an in-place *repair* invalidates the chapter's derived plans; a *re-author* does not.

`canonical_version()`'s docstring says regenerating "therefore produces a NEW key". **That is
true only of the chosen variant.** A served plan can contain a unit BORROWED from another
canonical, and the key does not name the lender. Re-author the lender and the content changes
while the key stands still. Measured, with the library as it now stands:

| request | chosen variant | key | on disk? | that file still says *"complete the draft article"* |
|---|---|---|---|---|
| **X = 11** | p10 | `…50m11_e19_c20260812142824` | **yes** | **YES** |
| **X = 15** | p14 | `…50m15_e19_c20260812142352` | **yes** | **YES** |
| X = 16 | the top | `…50m16_e19_c20260812154258` | no — key moved | — |

So the two serves ARV-D-136 was raised about, and re-authored to fix, are the two that would be
served **from cache, unfixed**. X = 16 is safe only because its chosen variant *is* the
re-authored file.

This is ARV-D-034's family — the key did not move, stale bytes served — on the one path the
2026-08-04 fix did not cover: that fix moved invalidation into the repair tools, and a
regeneration is not a repair.

**Remedy (founder call), and the first is the obvious one:**

1. **Purge on re-author** — call `purge_derived` from `generate_canonical`'s install path, as
   every repair tool already does. Consistent with the doctrine, and the accepted cost is
   already written down: "a teacher holding a purged plan loses that file and re-prepares".
2. Or **name the lender in the key** (`c<chosen>` + `b<lender>` when a borrow occurred) — more
   surgical, only borrow-bearing plans re-key, but it hangs a second token off the filename and
   a version tail was explicitly reverted on 2026-08-04 for exactly that reason.

**Immediately, for this chapter**, the three plans built from the old top should go:

```bash
rm data/content/saved_plans/english/ix/ch_07_50m11_e19_c20260812142824.json \
   data/content/saved_plans/english/ix/ch_07_50m15_e19_c20260812142352.json \
   data/content/saved_plans/english/ix/ch_07_50m16_e19_c20260812141916.json
```

(The other four — X = 9, 12, 13 and the mixed week — contain no borrowed unit from the top and
are unaffected; I checked rather than assumed.)

## 3 · No overwrite across engine versions — **N/A here, with the reason**

This is the first english chapter ever built, so no earlier-engine file exists to preserve; all
seven served plans are `e19`. What the re-author *does* demonstrate is the same property from
the other side: it rewrote `ch_07_canonical.json` in place (library files are not
version-keyed) and **left every served file untouched** — which is precisely why check 2 fails.
The two rules are in tension, and the resolution is that stale derived plans must be *deleted*,
never overwritten.

## 4 · Determinism — PASS

Same request served twice in-process: byte-identical except `saved_at`.

## 5 · Quarantine invisible to serving — PASS

Withholding `p14` from the library and re-serving:

| X | variant with the full library | variant with p14 quarantined |
|---|---|---|
| 12 | 14 | **17** |
| 13 | 14 | **17** |
| 15 | 14 | **17** |

The serve falls to the next surviving variant, the key changes to that variant's version
(`c20260812154258`), and no response names the withheld file.

---

## Exit

Checks 1, 4 and 5 pass; 3 is N/A with reason; **2 fails as ARV-D-137 (S2)**. One HTTP-level
assertion is owed (the `cached: true` flag and unchanged mtime) at the next run with uvicorn up.
