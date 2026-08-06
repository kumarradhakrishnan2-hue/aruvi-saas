# C10 — Storage conventions · science · secondary (IX) · ch 8

**Library** {12, 10, 7} · **floor** 7 · **authored duration** 50 min · **engine** e16
**Run** 2026-08-06, after C9's e16 re-serve · **Runbook**
`docs/testing_artefacts/c10_runbook_science_ix_ch08.sh` · **Responses**
`docs/testing_artefacts/c10_responses/`

**Verdict: PASS on all five.** Two checks were run in a substituted form because the Cowork
sandbox has no unlink permission on the mounted repo; both substitutes are stated below and
one of them (determinism) is *stronger* than the step asks. Two things came out of the run
that are not pass/fail: a new S3 provenance defect (ARV-D-065) and a re-confirmation that
ARV-D-050 is still open and is now more dangerous than when it was filed.

Ledger map: `…100029` = the standard, 12 units · `…100653` = p10 · `…101157` = p07.

---

## 10.1 · Filename conventions — PASS

Library on disk is `ch_08_canonical.json` + `ch_08_canonical_p10.json` +
`ch_08_canonical_p07.json`; the KK suffix matches the unit count in both compacts (10 → 10
units, 07 → 7). All **14** served files present at the start of the run match
`ch_08_<matrix>_e<ENGINE>_c<version>`, matrix duration-aggregated longest-first —
confirmed by `60m4-50m7`, not `50m7-60m4` — and every one of them keys on the **chosen
variant's** ledger timestamp, checked by re-reading `genon.variant_used` out of each file
rather than inferring it:

| Plan | X | Chosen variant | Keys on |
|---|---|---|---|
| `ch_08_50m11_e16_c20260806100029` · `60m4-50m7_e16_c…100029` | 11 | top (12) | top |
| `ch_08_50m9_e16_c20260806100653` | 9 | p10 | p10 |
| `ch_08_50m6_e16_c20260806101157` | 6 | p07 | p07 |
| `ch_08_50m8_e16_c20260806101157` | 8 | **p07** | **p07** |
| (e15) `50m13 · 50m16 · 50m19` | 13–19 | top | top |
| (e15) `50m5` | 5 | p07 | p07 |

**X=8 is the check that actually bites, and this chapter has the cleanest instance of it in
the campaign so far.** Under next-highest alone, 8 would take p10. It does not: e15's Case 1b
exact-fit complete rescue picks **p07** and borrows the standard's synthesis unit, so
`slot_fill.mode = complete_rescue`, `borrowed_from = 12`, `self_fill = false`. The filename
keys on **p07**, the plan's base — not on 12, the lender, and not on 10, the variant the
superseded rule would have named. This is the ARV-D-034 failure class the e15 comment in
`api/main.py` describes, tested rather than reasoned about: a cross-plan borrow whose key
follows the bytes.

Non-conforming filenames: **0**.

One absence, recorded so it does not read as a hole later: the C6 record lists
`ch_08_45m12_e14_…` (the scaled identity-shape row). No `45m*` file survives — the e14 set
was purged when the C9 repairs landed, and the e16 re-serve did not re-run that row. Nothing
turns on it here; C10 checks conventions, and the 50-min and mixed rows carry them.

## 10.2 · Cache hit, and the purge that keeps it honest — PASS (a) / verified-by-code-and-refusal (b)

**(a) The hit — PASS, live.** `ch_08_50m11_e16_c20260806100029.json` (built 18:55:40 by
kumar2 in the C9 re-serve) was requested again by **kumar2**, then by **kumar1**:

| Request | `cached` | `already_yours` | file mtime | file md5 |
|---|---|---|---|---|
| baseline | — | — | 18:55:40.448511947 | `004643b6…` |
| kumar2 (owner) | `true` | `true` | **unchanged** | **unchanged** |
| kumar1 (new to him) | `true` | `true`→`false` | **unchanged** | **unchanged** |

The internal `saved_at` still reads `2026-08-06T18:55:40`. Two teachers, one file, no copy —
per-teacher visibility comes from the register, exactly as CLOUD_DATA_MODEL §2.3 designs it,
and `already_yours` splits the two correctly (kumar2 has held it, kumar1 has not, though the
server did no work for either).

**One thing this stage's e15 code changes about how to read that.** Since 2026-08-06 the API
**serves first and keys the entry off `genon.variant_used`**, so a `cached: true` response has
still run the selection — the cache saves the *write*, not the serve. Consequence worth
writing down because it can mislead a reader of these files: the `serve.library` array in a
cached response is copied out of the **stored** plan, not read live. During 10.5 below, the
X=8 request returned `library: [12, 10, 7]` while p10 was physically quarantined, because it
was a cache hit. Not a defect; but a cached response is not evidence about the library's
current state, and no C-step should use it as such.

**(b) The purge — the wiring, the pattern and the refusal are verified; the deletion is not
runnable here.** `genon/purge_derived.py` is imported and called by `repair_register.py`,
`normalize_options.py` and `repair_chapter_cg.py` with `(subject, grade, ch)` threaded
through, and by `repair_anchors.py` with hardcoded arguments (see ARV-D-050 below). Run
against this chapter it resolves **16 derived plans** and, critically, `derived_pattern(8)`
matches **none** of `ch_08_canonical.json` / `_p07.json` / `_p10.json` — the library cannot be
caught by the purge.

The invocation was made for real. The sandbox cannot unlink on the mount, so the tool
printed its header, printed `COULD NOT REMOVE` for each of the 14 files, and **exited with
`STOP: derived plans could not be deleted, so a stale plan can still be served.`** That is
the property that matters most in a purge tool and it is now verified live on this stage: it
does not report a confident success it did not achieve. (The same limitation, and the same
observation, were recorded at SS·middle C10.)

**What is still owed on the founder's machine:** one real repair-then-purge cycle showing the
files gone and the next request rebuilding. Everything except the `unlink()` call itself has
been exercised.

**The stated cost, confirmed live.** kumar1's register carries two keys —
`ch_08_50m4_e15_c…101157` and `ch_08_50m21_e15_c…100029` — whose files no longer exist (they
were purged in an earlier repair). `GET /plans/science/ix` as kumar1 returned **HTTP 200**
and 19 ch-08 entries, and **neither dangling key appears**. The listing walks the directory
and marks what is prepared, so a dangling key is skipped, not an error, exactly as the
purge's docstring promises.

## 10.3 · No overwrite across engine versions — PASS

At the start of the run: **9 `_e15_` files** sitting beside **5 `_e16_` files** for this
chapter, the e15 set stamped 14:42–16:17 and the e16 set 18:55. An engine bump re-keys the
cache by construction, so nothing is ever rewritten in place; the older files remain readable
evidence of what e15 served.

**A note on order, because the runbook depends on it.** 10.2b's purge deletes *every* derived
plan for the chapter, e15 included — correctly, since a repaired canonical invalidates them
all. So 10.3 is recorded **before** the purge, the whole derived set is copied to `/tmp`
first, and the e15 half is restored from that copy afterwards. This run *simulated* a repair;
it did not perform one, so the older-engine evidence was not the purge's to take. Every
restored e15 file was md5-checked against the pre-run snapshot: **identical, 9/9.**

## 10.4 · Determinism — PASS, and stronger than the step asks

The step's form (delete one plan, re-request, diff) is not runnable here: `rm` returns
*Operation not permitted*, so the re-request was a cache hit and its empty diff proves
nothing. Substituted with the cross-process form:

| Plan | serve run 1 == run 2 | == the bytes on disk | filename re-derives |
|---|---|---|---|
| `50m11_e16_c…100029` | ✓ | ✓ | ✓ |
| `50m9_e16_c…100653` | ✓ | ✓ | ✓ |
| `50m8_e16_c…101157` (complete_rescue) | ✓ | ✓ | ✓ |
| `50m6_e16_c…101157` (below floor, 1 drop) | ✓ | ✓ | ✓ |
| `60m4-50m7_e16_c…100029` (mixed) | ✓ | ✓ | ✓ |

Two fresh in-process serves are byte-identical to each other **and** to the file the API
wrote in a different process three hours earlier (comparing everything but `saved_at` and
`filename`), and `genon_plan_filename` re-derives the exact name from the fresh serve. So
determinism holds across runs, across processes and across the API/engine boundary — which
is the property the delete-and-rebuild test is a proxy for, tested directly.

Independently, the five e16 plans were re-requested after the (attempted) purge and each came
back byte-identical to its pre-purge copy: **identical 5, differing 0.**

Why it matters, unchanged from the pilot: determinism is what makes served plans
*disposable*. They can vanish and return with nothing changing for anyone, which is why the
library canonicals need backing up and served plans do not, and why 10.2's file-sharing
between two teachers is safe — the plan is a function of the request, not an artefact of who
asked first.

## 10.5 · Quarantine is invisible to serving — PASS

`ch_08_canonical_p10.json` was **moved** (never deleted) to
`backup/quarantine/science_ix_ch08/` under an EXIT-trap restore, and the requests p10 feeds
were re-run.

| Phase | Request | Library seen | Chosen | Mode | Filename | Names p10? |
|---|---|---|---|---|---|---|
| baseline | X=9 | `[12, 10, 7]` | 10 | fill (self) | `…50m9_e16_c20260806100653` | **no** |
| withheld | X=9 | `[12, 7]` | **12** | fill (self) | `…50m9_e16_c20260806100029` | **no** |
| withheld | X=10 | `[12, 7]` | **12** | fill (self) | `…50m10_e16_c20260806100029` | **no** |
| withheld | X=8 | (cached) | 7 | complete_rescue | `…50m8_e16_c20260806101157` | **no** |
| restored | X=9 | `[12, 10, 7]` | 10 | fill (self) | `…50m9_e16_c20260806100653` | **no** |

Nothing 500'd. The library glob simply stopped seeing the quarantined file; serving fell
through to the next surviving variant and returned to normal on restore. The string `p10`
appears nowhere in any withheld-phase payload, and neither does `quarantine` — checked
against the raw JSON, not the summary keys.

**Two things this chapter shows that the pilot could not.**

1. **X=10 stops being an identity serve.** With p10 present, a 10 × 50 min ask *is* p10 and
   returns the canonical itself with no file written. With p10 withheld the same ask becomes
   an ordinary fill off the standard and writes a served plan. The identity rule is a property
   of the library, not of the number — quarantining a variant does not orphan the teachers who
   ask for its shape, it demotes them to a derived plan.
2. **The re-key is structural, not incidental.** Because the filename carries the *chosen*
   variant's `ledger_ts`, withholding p10 changed which variant was chosen and therefore
   changed the address — `…c20260806100029` instead of `…c20260806100653`. A quarantined
   variant's plans can never be served from cache by accident, and the fall-through cannot
   collide with the pre-quarantine file. The p10-keyed file sat untouched throughout and was
   served again, unchanged, the moment p10 came back.

**Clean-up: partial, and the residue is named.** The quarantine directory is empty, p10 is
back, and all three library canonicals are byte-for-byte their pre-run selves
(`_lib_before.md5` vs `_lib_after.md5`). But the pilot's last clean-up step — removing the
temporary top-keyed plans and their dangling register keys — **could not be done here** (no
unlink). Left on disk for the founder to delete:

- `data/content/saved_plans/science/ix/ch_08_50m9_e16_c20260806100029.json`
- `data/content/saved_plans/science/ix/ch_08_50m10_e16_c20260806100029.json`

and the matching two keys in `data/prepared_plans/kumar1/kumar1/prepared.json`
(`science/ix/ch_08_50m9_e16_c20260806100029.json`, `…50m10_e16_c20260806100029.json`,
both stamped `2026-08-06T14:32:17`). Neither file is wrong — each is a valid serve of the
withheld library — but they are quarantine-experiment artefacts, not stage evidence, and a
later reader would otherwise find two plans for X=9 keyed to different variants with no note
saying why.

---

## Defects

**ARV-D-065 (new, S3) — the engine version stamped into every served plan has drifted from
the one that keys its filename, again.** `aruvi_core/genon/serve.py:765` writes
`"engine": "serve v2.2 / e15 (…)"` while `api/data.py:370` sets `GENON_ENGINE_VERSION = "16"`.
Every plan in this stage's e16 set therefore has `e16` in its name and `e15` in its
provenance field — the e16 change is described in the trailing clause of that same string, so
the text is complete and only the leading token is stale. The comment sitting directly above
that line predicts this exact failure and says why it matters: *"the tracker's amber rule
reads provenance, so a stale string here reads as 'no engine change' on a plan that is one."*
It drifted at e14, was fixed, and has drifted again at e16 — which is the argument for
deriving the label from `GENON_ENGINE_VERSION` rather than re-typing it. **Owner: Claude.
Fix: one line, plus a test asserting the two strings agree.** No served bytes are wrong; the
attribution is.

**ARV-D-050 (open, S3) — re-confirmed here, and this stage raises the stakes.**
`genon/repair_anchors.py:197` still calls `purge("social_sciences", "ix", 3, …)` with the
arguments hardcoded, while the other three repair tools thread `(subject, grade, ch)`. When
it was filed, science·secondary was not yet certified. It is now: pointing that tool at
science IX ch 8 would repair science and **purge social_sciences ch 3's derived plans**,
leaving the chapter it just repaired serving pre-repair bytes — and the purge would print a
confident success while doing it. Either parameterise it like the other three, or make it
refuse to run outside SS·IX ch 3.

---

## Status

C10 is complete for science·secondary. Two live confirmations are outstanding on the
founder's machine, neither expected to differ: **(10.2b)** a real repair-then-purge showing
the files gone and the rebuild, and **(10.5)** deleting the two residue files and their
register keys. Remaining in the stage: C11 (serve wall time — the C6/C10 responses already
show 4–12 ms per request against a 5 s budget), C12 (view + exports), C13 (failure paths),
C14, then the gate.
