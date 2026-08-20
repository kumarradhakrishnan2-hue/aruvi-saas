# W1 pre-flight · S8 · mathematics · preparatory (iii, iv, v)

> **SUBMITTED 2026-08-19 13:37.** batch `msgbatch_01FA92FK9MoXAVJiuKNdWQsJ` · 42 requests ·
> manifest `genon/out/batches/mathematics_top_20260819_133718.json`.
> Kumar's dry run reproduced this file's worklist exactly (42 requests, ch 5 skipped, same
> period counts) before the metered call.
>
> **COLLECTED + CERTIFIED 2026-08-19 17:40.** ₹632.58 / 42 runs / ₹15.06 per run.
> 39 standards live, 4 chapters not library-ready.
>
> **CLEARED 2026-08-19 18:09 — W1 PASSES.** All repairs free; no rupee moved, nothing re-bought.
> 43 reports · 43 `authored_standard` rows · zero quarantines · zero register bans. The only
> remaining FAIL is `library complete`, which is between-waves arithmetic. **W2 is open.**
> One item needs the founder's eye: **ARV-D-187**, the authored replacement for iii ch 5's
> shell question (§"What was fixed" below).

Run 2026-08-19 in Cowork. Everything free is done here; the metered half is Terminal-only
(runbook §0, "place": the sandbox proxy blocks credentialed calls).

---

## §0 gates

| gate | result |
|---|---|
| stage prep P1–P5.5 | **PASS** — tracker `mathematics/preparatory` P1–P5 + SIGN all green (2026-08-11) |
| carrier | **PASS** — `require_carrier("mathematics", iii/iv/v)` returns; `carrier_gap` = None (row 5, landed at S8's P5.5) |
| pilot C-cycle | **PASS** — C1–C14 all pass in the tracker (iii ch 5) — but see the open defects below |
| content | **PASS** — iii 14/14 · iv 14/14 · v 15/15 summaries + mappings = 43 chapters; zero placeholder rows; every row carries `canonical_plan` |
| quarantine | **CAUTION** — 9 files under `backup/quarantine/mathematics/iii/`, all ch 5, all restored counterparts (see below) |
| credit | Kumar's to confirm on the key |
| place | Terminal |

## Dry run — 42 requests, 1 skip

```
python3 genon/batch_api.py submit mathematics iii iv v --wave top --dry
→ genon/out/batches/DRY_mathematics_top_20260819_133420.json
  requests 42 · ~769k input tokens (uncached worst case) · cache ON (1h) · price 50%
  skip iii ch 5 — standard already installed
```

43 chapters, 42 tops to author. Period counts read the master plan: mean **11.1**, range
**6–16**, all at **40 min** (the calibrated preparatory band). Σ periods = 466.
W2 will be **76 compacts** (Σ 620 periods).

## Constitution reached the payload

Glob scoped to `mathematics`, sorted by mtime, filename printed (runbook §0's own trap):

```
FILE: genon/out/batches/DRY_mathematics_top_20260819_133152.json
  ARUVI — MATHEMATICS LESSON PLAN CONSTITUTION (PREPARATORY) · VERSION 1.4
  ARUVI — MATHEMATICS ASSESSMENT CONSTITUTION (PREPARATORY) · VERSION 1.4
```

Subject and stage confirmed on the version lines before the number. Both are the live pair.

**Doc drift, cosmetic:** `docs/testing.md` §3's S8 row still reads "assess v1.3 (2026-08-11)".
The live assessment constitution is **v1.4** (the `number_line:` tick-line ruling, same day).
The LP row (1.4) is correct.

## Price

`output ≈ 1.2k + 1.435k × periods`, batch ₹/run `= (in×$3 + out×$15)/1e6 × 92 × 0.5`,
input ≈ 18.3k/run from the dry note:

| cache hit | total | ₹/run |
|---|---|---|
| 0% | ₹602 | 14.34 |
| 30% | ₹574 | 13.66 |
| 90% | ₹516 | 12.29 |
| 98% | ₹509 | 12.11 |

Est. output ≈ 719k tokens. Inside the runbook's ₹12–15/run band. **Budget ~₹1,200 (2×).**
Cheaper per run than S7·middle (₹18.23) — prep chapters are shorter.

---

## OPEN — read before submitting

`build_library.py mathematics iii 5 --certify-only` (free, run today) **FAILS** and
quarantines the whole ch 5 library. Report:
`genon/out/library_reports/mathematics_iii_ch05_20260819_133353.md`.
The three files were restored to `data/content/saved_plans/mathematics/iii/` immediately —
had they been left in quarantine, the next `submit --wave top` would have **re-bought ch 5's
standard** instead of skipping it.

This is why the quarantine folder holds 9 ch-5 files: three prior certify runs on 2026-08-13
(17:57, 17:59, 18:00) did the same thing and were restored the same way. The defects have
never been repaired.

**Defect 1 — register `[completion]`, 3 of 3 files.** Ban 2 (forward reference / completion).

- `ch_05_canonical.json` U11 `teacher_notes`: "…built across the chapter…"
- `ch_05_canonical_p11.json` U11 `teacher_notes`: "…developed across the chapter…"
- `ch_05_canonical_p08.json` U8 `teacher_notes`: "…that has been built across the chapter."

Plus one ADVISORY artefact-dependency hit (`U7 materials[3]: 'from the previous unit'`).
Free to repair (`repair_register.py` — there is **no `("mathematics","iii")` key in it yet**),
but note the **rate**: 1 hit per file on n=3, against S5's ~1 per 3 files. If it holds across
the batch, expect ~40 declarations at W1's certify pass rather than ~14. Budget effort, not money.

**Defect 2 — empty MCQ stem.** `ch_05_canonical.json` `Q-C-2`: "MCQ has prompt '' — there is
nothing to ask". Structural, gates, quarantines, and is **not** one of the five repair families —
the remedy is a re-author of the top (and therefore its compacts) or an accepted-omission ruling
at the human gate. ~₹37/run × 33 periods if re-authored.

Neither blocks W1 — W1 authors the other 42 chapters' standards and never touches ch 5 — but
**both will re-quarantine ch 5 at the W1 certify pass**, and the closing checklist cannot be met
until they are resolved. Also on disk: 8 derived `ch_05_40m*_e19_*.json` plans in the same
folder (closing checklist item 6).

---

## The Terminal sequence

```bash
cd ~/main/kumar/AI/aruvi-saas

# 1. re-read the dry worklist on your machine (cheap, and proves the key/env)
python3 genon/batch_api.py submit mathematics iii iv v --wave top --dry

# 2. THE METERED CALL — 42 requests
python3 genon/batch_api.py submit mathematics iii iv v --wave top

# 3. poll; 'ended' is the signal (laptop may be shut in between)
python3 genon/batch_api.py status  genon/out/batches/<manifest>.json

# 4. install + log
python3 genon/batch_api.py collect genon/out/batches/<manifest>.json

# 5. FREE and REQUIRED — annotates the rows W2's briefs are built from
python3 genon/batch_build.py mathematics iii iv v --certify-only
```

Pass the manifest path explicitly, never `--latest` (two waves now exist for other stages).

Expect every chapter to FAIL `library complete` at step 5 — its compacts do not exist yet.
That is arithmetic, not a defect; the pass is run for its annotate half.

Then the FAIL census:

```bash
grep -h "^FAIL" genon/out/library_reports/mathematics_*_<stamp>*.md \
  | sed 's/ch_[0-9]*_canonical[^:]*: //' | sort | uniq -c | sort -rn
```

---

# W1 RESULT · collected + certified 2026-08-19 17:40

**₹632.58 over 42 runs = ₹15.06/run** (estimate ₹602 at 0% cache; output 828k vs 719k projected).
**Cache never engaged** — `cache_write` and `cache_read` are both 0 in `token_log.csv` despite
`cache ON (1h)`. The batch discount alone carried it. Worth diagnosing before W2, where 76
requests share the same system block and the 0.1x read would actually pay.

**39 standards live · 4 chapters not library-ready.** Certify wrote **42 reports for 43 chapters**
— the missing report is the tell. Master-plan annotation: iv 14/14 `authored_standard`,
iii 12/14, v 13/15.

Every report's `library complete` FAIL is between-waves arithmetic, not a defect.

## The four chapters that cannot enter W2

`variant_plans.briefs_for` refuses a provisional row, so each of these blocks its own compacts.

| chapter | what | cost |
|---|---|---|
| **iii ch 4** Vacation with My Nani Maa | Q-A-2 tagged `number_line:` with 2 tick cells (≥3 required) — quarantined | free |
| **v ch 3** Angles as Turns | Q-B-7 tagged `number_line:` with a 17-char label `"3 o'clock (right)"` (≤16) — quarantined | free |
| **v ch 6** The Dairy Farm | JSON parse failure. 95,619-byte raw on disk, never installed, **billed**. `recover_from_raw.py` | free |
| **iii ch 5** (the pilot) | Q-C-2: MCQ with an empty prompt. Carried from this morning, unchanged — quarantined again on schedule | re-author or accepted-omission ruling |

**The two `number_line:` catches are the DECLARED-TYPE GATE working.** It landed at this stage's
own C4 with assessment v1.4 (ARV-D-113) and this is its first batch. Both would previously have
degraded silently to TABLE and printed the literal token to a teacher.

## Register — 23 hits across 16 of 42 chapters

`14 [forward] · 4 [completion] · 4 [clock] · 1 advisory artefact-dependency`

Affected: iii 1, 5, 7, 8, 11, 13 · iv 3, 4, 9, 11, 12 · v 3, 7, 9, 10, 11.
`repair_register.py` carries no `("mathematics", "iii"/"iv"/"v")` key yet — the pilot's own three
hits were never declared either.

**The four `[clock]` hits need a founder ruling, not a repair, and this is the first stage where
that is true.** Preparatory mathematics *teaches clock time*, so ban 1's regex collides with
correct content:

- `'What did you put for 5 minutes? For 60?'` — content
- `'We put the minute hand at 9 for 45 minutes past'` — content
- `'moves clockwise for 15 minutes. What type of angle has it traced?'` — content
- `'first individually in silence for a few minutes'` — **real breach**
- `'Students sketch independently for several minutes'` — **real breach**

Runbook trap 4 applies in terms: fix the false positives at the scanner and say why; never strike
good teaching to satisfy a regex.

---

# What was fixed · 2026-08-19 18:09 · all free

Re-certify at 18:09: **43 reports · 43 `authored_standard` rows · zero quarantines · zero
register ban hits.** Only `library complete` fails, on the 42 chapters whose compacts don't
exist yet. **W2 is open.**

## 1. v ch 6 — and a third parse-repair family

The raw would not recover: 413 quote "repairs" thrashed past the real defect and turned a
structural newline into an in-string one; `_structural_escape` then stopped at the same place.
The whole 94 KB file had **exactly one defect — a trailing comma before a closing brace**, which
neither existing family can see.

`_trailing_comma_fix` added to `generate_canonical.py` beside `_bracket_fix`, tried **before**
the quote loop for the same reason the bracket fix is (the quote heuristic corrupts on a
structural typo). Same guarantee as its two siblings: one character removed, at a position a
string-aware walk proves is a comma followed only by whitespace and a closer — where JSON has no
legal construct, so it cannot be content. Unit-checked on object/array/newline forms, on a comma
inside a string, and on a bracket typo (falls through).

With it: 39 quote repairs instead of 413, 13 × 40 min, validate ok, installed. The money was
already logged by the run that earned it.

## 2. The two `number_line:` tags — opposite fixes

One rule for "number_line failures" would have got one of them wrong.

- **ARV-D-185** (iii ch 4 Q-A-2) — the stimulus was two **tens frames**, and a tens frame is a
  grid. Rule 7 forbids a tick line from being one and prohibits SVG here, so no permitted format
  can carry it; padding to three cells would satisfy the regex and still be the wrong picture.
  Field dropped to `""`, Rule 7's stated default. The prompt already says "Draw dots on the two
  tens frames below" and the exercise block carries p.30.
- **ARV-D-186** (v ch 3 Q-B-7) — a **good** tick line: four ordered clock positions, exactly the
  picture the question needs and exactly what assessment v1.4 was amended to permit. It failed
  only the ≤16-char bound, at 17 and 18. Labels shortened (`3 o'clock (right)` → `3 (right)`),
  each keeping both facts it carries; "o'clock" is in the prompt anyway.

## 3. Register: 21 → 0. Nineteen repaired, two fixed at the scanner

Both false positives share a root, and it is the stage's own subject matter: **this is the first
stage that teaches the thing the register bans talking about.**

- **Clock inside quotation marks.** iii ch 13 is *Time Goes On*, v ch 3 is *Angles as Turns*, and
  their bands quote the lesson. Ban 1 exists because proportional scaling falsifies a stated
  duration — and nothing inside quotation marks is scaled. `clock` now takes the quoted-span
  exemption `calendar` already had. **Measured first:** only four quoted clock hits exist in the
  whole corpus, all four are maths·preparatory, all four are content, and **both unquoted hits
  still fail**. No other stage moves. The pre-existing `_instructional` test can't do this job —
  a quoted question is routinely followed by "The class checks…", so an actor is named and it
  bans on a sentence that isn't about pacing.
- **`from the next` + a calendar noun.** iii ch 13 U2: "did they count July 22 itself, or start
  from the next day?" is day-counting on a grid. Narrowed by lookahead; still fires on
  science·vi ch 10 p11, the only other corpus occurrence.

**Nothing material to delivering a lesson was removed.** Every one of the 19 is a deletion of a
positional pointer or a rewording that names content instead of position, and each declaration
carries a `survives:` clause quoting what remains. The clearest case is the clock pair: "first
individually in silence *for a few minutes*, then discussing with a partner" — the pedagogy is
the **sequence**, and the sequence is untouched. The band carries its own minutes, which is why
the prose must not restate them.

Three are rewordings rather than deletions, where deleting would have cost the teacher a reason:
iv ch 9's bridge is real mathematics ("the bridge to 3-digit multiplication"), iv ch 12's preview
is a **list** every item of which survives, v ch 7 U8 keeps its rationale ("held back to give the
spatial reasoning tasks space").

## 4. ★ iii ch 5 Q-C-2 — authored, not repaired. Read this one.

The pre-flight called this the stage's one non-repairable defect, and it is why the pilot library
re-quarantined on every certify run since 2026-08-13. Declared MCQ, `verified: false`,
prompt/options/answer/method all empty, `inclusivity` carrying the generator's own failure
marker. The only filled field is the exercise companion: *Let us Do Q1, p.55 · Mark the square
corners in these shapes.*

**Authored under the ARV-D-180 precedent** (founder ruling 2026-08-19, one day old, identical
shape: "generate an equivalent question" rather than re-buying a 14-period standard and the two
compacts built from its registry).

**ARV-D-187.** The p.55 figures can't be carried at this stage, so the item asks about the
**testing procedure the section teaches** — the notebook-corner test, the section's own method —
making it answerable from the stem alone. The three distractors are the three ways a Class III
child misreads that test: accepting a gap, accepting an overlap, testing along a side instead of
at the meeting point. Each carries its own repair in `what_each_option_reveals`. No letter
appears in the guide prose (ARV-D-180's rule). **`verified` is deliberately left false.**

This is the one place in the stage where text was written rather than repaired.

## 5. A chapter summary was not valid JSON — and check 11 was silently off

`chapters/mathematics/v/summaries/ch_03_summary.json` carried naked inner quotes
(`"banner": "Let us play "Statue""`). `summary_sections` returns `([], NONE)` rather than raising
— correct, it must not fail a chapter for a reason that isn't about the chapter — so the 17:40
report reads **"ADVISORY: no section list readable … registry ↔ summary NOT reconciled"** where
every sibling reads PASS. The check `testing.md` v2.10 exists for had never run on that chapter.

Escaped (decoded text byte-identical). Check 11 now reads 7 sections, and **all 43 chapters pass
it.**

A corpus sweep found exactly one other invalid summary: **`mathematics/viii/summaries/
ch_05_summary.json`** — S7's territory, on a stage whose W1 has already passed, and it fails
`_structural_escape`, so it's a different glitch. **Filed for S7, not fixed here.**

## Hygiene and verification

All 8 derived `ch_05_40m*_e19_*` plans purged (ARV-D-034). The sandbox's first purge attempt
printed "could not remove" exactly as runbook trap 2 warns; deleted by hand. Every restored file
was re-scanned after restoring (trap 1).

Green: `test_genon_serve` · `test_genon_duration_order` · `test_genon_carriers` ·
`test_summary_sections`.

`test_genon_plan_key` fails one assertion — **pre-existing**, verified by re-running with this
session's changes stashed. It asserts a served filename contains `_e10_` while
`GENON_ENGINE_VERSION` is `"19"`. One-line fix for whoever touches that file next.

## W2 — SUBMITTED 2026-08-19 20:20

batch `msgbatch_01FVQLZnqvoxFuVD79eTYXUE` · **74 requests** (76 compacts minus ch 5's two,
already installed) · manifest `genon/out/batches/mathematics_compact_20260819_202033.json`.

Σ 601 periods · mean 8.1 · range 4–13. Payload confirmed carrying MATHEMATICS · PREPARATORY
**LP v1.4 / assessment v1.4**, filename printed, glob scoped by subject and mtime. Kumar's dry
run reproduced the worklist exactly before the metered call.

Estimate **₹692–843** (₹9–11/run — compacts are shorter than the standards).

```bash
python3 genon/batch_api.py status  genon/out/batches/mathematics_compact_20260819_202033.json
python3 genon/batch_api.py collect genon/out/batches/mathematics_compact_20260819_202033.json
python3 genon/batch_build.py mathematics iii iv v --certify-only
```

At this certify pass `library complete` should PASS for the first time on all 43 chapters.

Two things to watch:

- **The cache.** W1 logged `cache_write` and `cache_read` both at zero despite `cache ON (1h)`.
  74 requests sharing one system block is where the 0.1x read pays — check the ledger after the
  first results land, not at the end.
- **`completion` hits.** At S7·middle the compacts came in *better* behaved than their standards
  (0.16 hits/file vs 0.54) — the opposite of S2·middle. But a compact asserting "having covered
  every section" on a plan carrying fewer of them is the predicted failure, and `completion` is
  the family that caught all three of ch 5's files at W1.
