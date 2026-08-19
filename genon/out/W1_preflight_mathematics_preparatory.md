# W1 pre-flight · S8 · mathematics · preparatory (iii, iv, v)

> **SUBMITTED 2026-08-19 13:37.** batch `msgbatch_01FA92FK9MoXAVJiuKNdWQsJ` · 42 requests ·
> manifest `genon/out/batches/mathematics_top_20260819_133718.json`.
> Kumar's dry run reproduced this file's worklist exactly (42 requests, ch 5 skipped, same
> period counts) before the metered call.

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
