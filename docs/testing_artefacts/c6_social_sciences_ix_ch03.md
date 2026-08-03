# C6 — API serve checks · social_sciences · secondary

**Stage** S1 · **class** ix · **chapter** 3 · **library** {12, 9, 7} · **floor** 7 ·
**authored duration** 50 min · **engine** e10 · LP v1.10 / assessment v1.6
**Run** 2026-08-02, through the app (not the curl runbook) · **Verdict** **PASS on all seven
rows**, one S3 provenance defect (ARV-D-022), one register oddity to rule on, and **the adapted
cache is NOT yet exercised** — one more request closes it.

Read from the seven `_e10_` files on disk plus the three prepared-plan registers. Filenames key on
the **chosen variant's** `ledger_ts`: `…143756` = top (12) · `…144458` = p09 · `…150218` = p07.

---

## 1. The C6 table, row by row

| # | Request | Identity | Expected | Result |
|---|---|---|---|---|
| 1 | 50m × 12 / 9 / 7 | kumar1 | identity, own filename, **no file written** | **PASS** — no `_e10_` file exists for 12, 9 or 7; all three registered against `ch_03_canonical.json` / `_p09` / `_p07` |
| 2 | 50m × 8 | kumar2 | `superset`, note names re-crossed sections | **PASS** — `borrowed_from: 7`, `overlap_sections: ["Climate Change"]`, note quoted below |
| 3 | 50m × 10 | kumar2 | `exact`, no coverage note needed | **PASS** — `borrowed_from: 9`, `coverage_note: null` |
| 4 | 50m × 11 | kumar2 | (recorded, not required) | **PASS** — `synthesis`, `withheld_units: [11, 12]` |
| 5 | 50m × 13 | kumar2 | surrender ≥1, sentence in `coverage_note`, **served schedule prints 12** | **PASS** — see §2 |
| 6 | 50m × 6 | kumar2 | `suffix`/`truncation`, note names what was dropped, `dropped_units` flagged | **PASS** — see §3 |
| 7 | 60m × 2 + 50m × 8 | kumar3 | 200, mixed dispersion | **PASS** — see §4 |
| 8 | 45m × 9 | kumar3 | **not** identity; scaled, file written, exact tiling | **PASS** — see §5 |

Row 7 was run as **60m × 2 + 50m × 8** (founder's choice between the two ten-period shapes). It
still lands on a fill mode, so C12's requirement — a plan containing a **borrowed closing sitting**
— is satisfied: `mode: exact`, `borrowed_from: 9`.

**Coverage notes as a teacher reads them:**

- 50m×8 — *"The closing sitting briefly re-crosses Climate Change as runway before completing the
  chapter."*
- 50m×11 — *"Every section is covered; the time budget trims the chapter's closing synthesis to one
  sitting."*
- 50m×6 — *"Time budget short of the chapter's full span: Climate Change could not be scheduled —
  share this material for guided self-study or homework. The closing sitting completes the
  chapter."*

Each names the consequence in teacher language, without naming a rule or a mode. The 8 and 11
cases are the two that could have read as failures and do not.

---

## 2. Row 5 — surrender, and the e10 assertion

`requested_periods: 13` · `served_matrix: [{50, 12}]` · `surrendered_periods: 1` · 12 units on the
plan. The sentence appears in **both** channels, which is the e09 fold working as specified:
`section_coverage_note` (the teacher-facing channel, shared with drops) and `genon.surrender_note`
(provenance).

> "1 period(s) (50 minutes) exceed this chapter's fullest plan and return to your budget."

**e10 holds where it matters:** `period_schedule_display` reads *"50 minutes × 12 periods = 600
minutes / Total: 12 periods · 10h 00min"* — the served count, not the 13 asked. The request
survives in `genon.matrix` and `period_rows_snapshot`. The card's small print reads "50 min × 12".

**ARV-D-022 (S3, new).** `genon.duration_sequence` carries **13 entries against 12 sittings**.
`serve.py:338` splits `sit_durations = durations[:len(served)]` for the plan itself but line 497
emits the full pre-surrender `durations` as `duration_sequence`. Nothing teacher-facing reads it
(no UI consumer; `scale` correctly zips over the served list), so this is provenance drift, not
wrongness — **but C6's own mixed-duration assertion is made from this field**, so a request that
combined surrender with mixed durations would have its dispersion checked against a sitting that
was never served. **Recommend NOT fixing now:** the one-line change alters served bytes, which
bumps `GENON_ENGINE_VERSION` and re-keys every `_e10_` file for a field nobody reads. Ride it into
the next engine bump.

---

## 3. Row 6 — below the floor

`mode: suffix` · `variant_used: 7` (p07) · 6 sittings · `uncovered_sections: ["Climate Change"]`.
`result.dropped_units` carries **1 unit — p07's unit 7 — flagged `unscheduled: true`**, verbatim
with its authored minutes, exactly as e09 specifies. The coverage note names the section, not the
unit number, which is the right register for a teacher.

This is the row C12 inspects: `/view` must carry `dropped_lp` and `LessonView` must page it after
the served units; the exports must omit it.

---

## 4. Row 7 — mixed-duration dispersion

`duration_sequence: [50, 50, 60, 50, 50, 50, 50, 60, 50, 50]`

| Assertion | Result |
|---|---|
| shortest sitting opens the week | **PASS** — opens on 50 |
| long sittings interior | **PASS** — the 60s sit at positions 3 and 8 of 10 |
| long sittings never adjacent | **PASS** — four sittings apart |

Per-unit minutes match the sequence one-for-one, and both 60-minute units tile exactly to 60.

---

## 5. Row 8 — the ordinary teacher case

45 × 9 is the same X as a variant's own count but **not** at the authored duration, so identity
correctly does **not** fire: a file was written (`ch_03_45m9_e10_c20260801144458.json`, keyed on
p09), `mode` is a full serve with proportional scaling, and every unit carries
`period_duration_minutes: 45`.

**Exact tiling verified on every unit of every scaled plan** — 45m×9 (9 units), 60m2-50m8 (10
units, mixed), 50m×6 (6 units): bands start at 0, are contiguous end-to-start, and close exactly on
the unit's duration. **0 units fail** across all three files.

---

## 6. Storage conventions seen in passing (C10 evidence, recorded early)

- Filenames follow `ch_NN_<matrix>_e10_c<chosen-variant ledger_ts>`, duration-aggregated
  longest-first: `60m2-50m8`, not `50m8-60m2`. ✅
- The chosen-variant rule holds: 50m×8 keys on **p09**'s timestamp, 50m×6 on **p07**'s, the
  10/11/13 requests on the **top**'s. ✅
- **No matrix has two `_e10_` files** — the cache key is behaving as an address. ✅
- **Six `_e08_`/`_e09_` files still on disk untouched** beside the new ones — C10.3's no-overwrite
  evidence, stale by construction. ✅

---

## 7. Cache — what is proven, and the one request still owed

**Proven: the identity share.** `ch_03_canonical.json` is registered by **all three teachers**
(kumar1, kumar2 06:58:07, kumar3 07:00:53) and exists **once** on disk. Three teachers, one file,
no copies — the register carries the per-teacher visibility, exactly as CLOUD_DATA_MODEL §2.3
intends. kumar1 additionally holds `_p09` and `_p07`.

**NOT proven: the adapted cache hit.** kumar2's matrices (8, 10, 11, 13, 6) and kumar3's (60m2-50m8,
45m9) are **disjoint** — no adapted request was ever repeated, by the same teacher or another. So
`cached: true` has not been exercised once. Run exactly one more request to close it:

```bash
# 50m x 10 already exists (kumar2 made it). Ask as kumar1 and it must be SERVED, not rebuilt.
F=data/content/saved_plans/social_sciences/ix/ch_03_50m10_e10_c20260801143756.json
stat -f '%Sm %N' "$F"                      # note the mtime
curl -s -X POST http://localhost:8000/genon/social_sciences/ix/3/plan \
     -H 'Content-Type: application/json' -H 'X-Aruvi-User: kumar1' \
     -d '{"rows":[{"duration":50,"count":10}]}' | python3 -m json.tool | head -20
stat -f '%Sm %N' "$F"                      # must be UNCHANGED
```

Expect: `"cached": true`, the **same filename**, the mtime **identical**, and kumar1's
`prepared.json` gaining that key while the file itself is not rewritten. That is C10.2, and doing
it now also finishes C6's cache question.

---

## 8. One register oddity for the founder

kumar1's `prepared.json` carries `ch_03_canonical.json` with **`"periods": null`** (registered
05:05:46, well before the C6 run), while kumar2 and kumar3 both carry it with `"periods": 12`. A
null slipped in from an earlier path that marked the plan prepared without a period count — most
likely the first-run/attach route rather than a `/plan` request, since every `/plan` call passes
`total_periods`.

It matters because `PrepareLesson`'s committed-budget arithmetic sums `prepared_periods`: a null
row contributes nothing, so kumar1's year budget under-counts this chapter by 12 periods. Worth
deciding whether to (a) backfill the null from the plan's own `period_rows_snapshot` on read, or
(b) treat it as a legacy shape and leave it. Not a C6 failure — the C6 requests all registered
correctly — but it will resurface at X2 (Year Plan values) and X1.8 (the two screens that already
disagree about archived plans).
