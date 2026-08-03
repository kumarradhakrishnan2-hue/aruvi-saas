# C2 — Cost the LIBRARY · social_sciences · IX · chapter 3 (Atmosphere and Climate)

**Stage:** social_sciences · secondary (pilot) · class IX at 50 min
**Library:** v2.0 re-author, 2026-08-03 · counts `{12, 10, 7}` · basis `authored_standard` · registry 9 sections
**Constitutions:** LP v1.10 / assessment v1.6 · **engine** `GENON_ENGINE_VERSION = 12` · **model** `claude-sonnet-4-6` (pinned)
**Certification report:** `genon/out/library_reports/social_sciences_ix_ch03_20260803_180705.md` — DETERMINISTIC CHECKS ALL PASS
**Sources of record:** `runtime_data/token_log.csv` (billing rows) · `genon/ledger.csv` (run rows) · `genon_canonical` block of each installed file

---

## 1. The library cost table (v2.0 authoring runs only)

| # | Artefact | Schedule | `ledger_ts` | Completed | Input tok | Output tok | Total tok | Cost ₹ | Wall s | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `ch_03_canonical.json` (standard) | 12 × 50 | `20260803_141938` | 14:26:58 | 15,325 | 26,649 | 41,974 | **41.01** | 439.5 | ok |
| 2 | `ch_03_canonical_p10.json` | 10 × 50 | `20260803_142658` | 14:34:26 | 15,580 | 26,484 | 42,064 | **40.85** | 448.2 | ok — auto-repaired 1 naked quote |
| 3 | `ch_03_canonical_p07.json` | 7 × 50 | `20260803_143426` | 14:40:39 | 15,580 | 21,959 | 37,539 | **34.60** | 372.4 | ok |
| | **LIBRARY TOTAL** | | | | **46,485** | **75,092** | **121,577** | **₹116.46** | **1,260.1 s ≈ 21.0 min** | 3/3 clean |

`call_type` in `token_log.csv`: row 1 `canonical_generation`, rows 2–3 `variant_generation`.
Rows reconcile to `ledger.csv` by start-time + wall-clock (e.g. 14:19:38 + 439.5 s = 14:26:57).
**No cell is missing.**

**Defect reruns in this library: ZERO.** Both defects found after authoring were repaired
**deterministically at ₹0** — no regeneration was bought:

| Repair pass | Tool | Files touched | Edits | API cost |
|---|---|---|---|---|
| 2026-08-03 17:41:40 | `genon/repair_anchors.py v1.0` | all three | 3 (V2 `;` → ` / ` section-anchor joiner) | ₹0 |
| 2026-08-03 18:07:01 | `genon/repair_register.py v1.1` | standard (3 clock), p10 (1 forward) | 4 (ban hits 3→0, 1→0) | ₹0 |

This is the C2 finding that matters most for the corpus bill: under v2.0 the two failure modes
the certifier caught were **declarable repairs, not reruns**. The 2026-08-01 pilot bought a
₹34.71 regeneration for its dropped-section defect; this one bought nothing.

---

## 2. Spend kept OUT of the library total (superseded R&D)

Recorded so the chapter is fully attributed, and excluded from any extrapolation — folding R&D
into a pre-warm figure inflates it.

| Date | What | Cost ₹ |
|---|---|---|
| 2026-07-29 | partition-era canonical (`canonical_generation`) | 46.01 |
| 2026-07-29 | `rule16_probe` × 2 | 2.41 |
| 2026-07-30 | `mcq_probe` | 5.93 |
| 2026-08-01 | pre-v2.0 library: top 39.43 + p09 36.51 + p07 35.05 + defect rerun 34.71 | 145.70 |
| | **Superseded subtotal** | **₹200.05** |
| | **Chapter total ever (superseded + v2.0 library)** | **₹316.50** |

The 2026-08-01 library is superseded in full by v2.0: `p09` is orphaned by the new counts, and
the old artefacts carry mandated closers (ARV-D-025).

---

## 3. Cost shape (what the numbers say about the bill)

**Input is flat and unavoidable — 15.3–15.6k tokens every run.** The constitution, chapter
summary, competency mapping and brief are paid for in full on each authoring run; nothing is
amortised across a library. Input rose only ~3% from the 2026-08-01 runs (14.9–15.4k), the
brief having grown.

**Output no longer tracks period count the way it did.** v2.0 free authoring:

| Units | Output tok | vs standard | Cost ₹ | vs standard |
|---|---|---|---|---|
| 12 (standard) | 26,649 | — | 41.01 | — |
| 10 | 26,484 | −0.6% | 40.85 | **−0.4%** |
| 7 | 21,959 | −17.6% | 34.60 | −15.6% |

**A 10-unit compact costs essentially the same as the 12-unit standard.** Under the retired
partition-era briefs a 9-unit variant came in 7.4% under the top; freed of the closing-span
mandate the model writes each compact at full richness, so compaction stops buying discount
until the count drops sharply. The old guidance ("a compact costs ~11% less than the top")
is superseded: **assume a compact costs what the standard costs unless it is ≥ 40% shorter.**

**Budget per RUN, never per unit** — the rule holds and is now stronger, not weaker.

---

## 4. Rate and corpus extrapolation (updated)

- **Measured rate this library: ₹38.82 per authoring run** (116.46 / 3). The testing.md
  benchmark of ₹37/run was measured pre-v2.0 and is ~5% low.
- Corpus: 315 non-placeholder chapters carrying plans of size 3 (296) or 2 (19) = **926
  authoring runs** (unchanged — v2.0's equal dispersion produces the same set sizes).

| Basis | Rate | Corpus | Note |
|---|---|---|---|
| Synchronous, no allowance | ₹38.82 | **≈ ₹35.9k** | SS·secondary is the heaviest corner — treat as upper-middle |
| + 15% defect-rerun allowance | — | ≈ ₹41.3k | conservative; see below |
| Batch pricing (50%), deferred to mass pre-warm | — | ≈ ₹18–21k | |

**On the 15% allowance:** the observed v2.0 rerun rate on this chapter is **0/3**, because both
defects were deterministically repairable. Keep the 15% until a second stage is measured — one
chapter is not a rate — but the mechanism that would justify lowering it (declared repairs in
`repair_anchors.py` / `repair_register.py` instead of regeneration) is now built and proven.

---

## 5. Provenance panel (§6 fields, for the tracker)

| Field | Value |
|---|---|
| Subject · stage · class drawn | social_sciences · secondary · **IX** (pilot) |
| Pilot chapter | 3 — Atmosphere and Climate |
| LP constitution | v1.10 |
| Assessment constitution | v1.6 |
| `GENON_ENGINE_VERSION` | 12 |
| Canonical plan row | `{counts: [12,10,7], provisional: false, basis: "authored_standard", registry_sections: 9, authored: [12,10,7]}` |
| Brief identity | `genon/out/briefs/ch_03_top.txt`, `ch_03_p10.txt`, `ch_03_p07.txt` (written 2026-08-03 18:07 by `variant_plans.py` — record its git commit) |
| `ledger_ts` | `20260803_141938` · `20260803_142658` · `20260803_143426` |
| Certification report | `genon/out/library_reports/social_sciences_ix_ch03_20260803_180705.md` |
| Repairs applied | `repair_anchors.py v1.0` (3 edits) · `repair_register.py v1.1` (4 edits, ban hits 4→0) |
| Model | `claude-sonnet-4-6` |
| Date · wall time | 2026-08-03 · 1,260.1 s authoring |
| Tokens in / out · cost ₹ | 46,485 / 75,092 · **₹116.46 library total** |

---

## 6. Exit

- [x] Every `token_log.csv` row for this chapter is attributed to an artefact or to superseded R&D.
- [x] Library total recorded (₹116.46) and carried into the provenance panel.
- [x] Failed/redone runs accounted for — there were none in v2.0; the two repairs cost ₹0.
- [x] No cell missing; nothing recorded blank.

**C2 PASSES.** Next: C3 (canonical + one compact vs the stage constitution, rule by rule) —
note the existing `c3_social_sciences_ix_ch03.md` was written against the **pre-v2.0** library
and must be re-run against the 2026-08-03 files.
