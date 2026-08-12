# C2 — cost the library · english · IX · ch 7 *Vitamin-M*

**Date:** 2026-08-12 · **Model:** claude-sonnet-4-6 · **Constitutions:** LP v1.2 / assessment v1.4
· **Engine:** 19 · **Source:** `runtime_data/token_log.csv` (costs) + `genon/ledger.csv` (wall time)

## The library cost — 3 metered runs, each producing an LP AND its assessment in one call

| time | call | schedule | in | out | ₹ | wall |
|---|---|---|---|---|---|---|
| 14:19:16 → 14:23:52 | `canonical_generation` | 17 × 50 (top) | 25,412 | 16,041 | **29.15** | 275.1 s |
| 14:23:52 → 14:28:24 | `variant_generation` | 14 × 50 | 25,467 | 15,466 | **28.37** | 271.5 s |
| 14:28:24 → 14:31:30 | `variant_generation` | 10 × 50 | 25,467 | 11,405 | **22.77** | 186.0 s |
| | **LIBRARY TOTAL** | | **76,346** | **42,912** | **₹80.29** | **732.6 s (12.2 min)** |

**Defect re-runs: ZERO.** Every metered call returned `status: ok` with no `problems`, no
auto-repair, and no regeneration. The one failure this stage had — the certifier's false
quarantine (ARV-D-127) — was diagnosed and fixed on the FREE `--certify-only` path, so it cost
nothing. The prompt-builder refusal that stopped the first C1 attempt raised in `prepare_job`,
before the API call, and also cost nothing.

## This is the cheapest library of the campaign so far, and the reason is worth recording

| stage | chapter | counts | in | out | ₹ | ₹/canonical |
|---|---|---|---|---|---|---|
| S1 · SS·secondary | IX ch 3 | 12, 10, 7 | 46,485 | 75,092 | 116.46 | 38.82 |
| **S11 · english·secondary** | **IX ch 7** | **17, 14, 10** | **76,346** | **42,912** | **80.29** | **26.76** |

**English costs less per canonical while authoring MORE units** (41 units across the library
against SS's 29). Two causes, in order of size:

1. **Output is what you pay for, and english emits little of it.** Output bills at 5× input
   ($15/M vs $3/M), and english's assessment is **one item per (section × spine) cell — six
   items per canonical, fixed**, where SS emits 18–29 per canonical against a per-competency
   slate. Eighteen items of stem + options + guide cost far more than eleven extra lesson
   units. English's whole library emitted 42,912 output tokens; SS's single top canonical
   emitted 26,649.
2. **Input is bigger and it barely matters.** English's prompt is the largest in the campaign
   — 53,771 system + 48,689 user chars, ≈25.4k tokens, against SS's ≈15.3k — because both
   english constitutions are long and the whole two-axis summary goes in. That 10k-token
   excess costs about ₹2.8 per call.

**I estimated ₹200–250 for this library before it ran and it came in at ₹80.** The estimate was
sized off prompt CHARACTERS, which is the input side; the bill is dominated by output. Recorded
because the same mistake would misprice the whole pre-warm: **project a corpus from output
tokens per unit and per item, never from prompt size.**

## Portfolio implication

At ₹80.29 for a 3-canonical library, english IX's 16 chapters project to **≈ ₹1,285**, and the
English family (101 chapters across three stages) to **≈ ₹8,100** — the cheapest subject in the
portfolio per chapter, on the largest chapter count. Preparatory and middle carry fewer spines
(prep has five) and shorter texts, so the per-chapter figure should fall, not rise.

## Data-hygiene note, carried from the last C2

`genon/ledger.csv` rows are **column-shifted by one** from their header (an extra empty field
around `tag`/`subject`): read as CSV, `subject` comes back empty and `grade` holds the subject.
The numeric tail (`input_tokens`, `output_tokens`, `cost_inr`, `seconds`) still lands correctly
for these rows, and `runtime_data/token_log.csv` — which C2 costs from — is intact. Anyone
aggregating the ledger by subject will get nonsense until the writer is fixed; anyone reading
wall time from it is fine.
