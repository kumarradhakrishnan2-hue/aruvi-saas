# C11 — Serve wall time · science · secondary (IX) · ch 8

**Library** {12, 10, 7} · **floor** 7 · **authored duration** 50 min · **engine** e16
**Run** 2026-08-06 · **Runbook** `docs/testing_artefacts/c11_runbook_science_ix_ch08.sh` ·
**Responses** `docs/testing_artefacts/c11_responses/`

**Verdict: PASS. Worst cache-miss 21.7 ms against a 5 000 ms budget — 230× inside it.**
Measured end-to-end with `curl -w '%{time_total}'` against the live API, not in-process, so
this is the socket figure the step asks for and not an engine estimate.

---

## 11.1 · The measurement, and why it took this form

The step offers two ways to force a cache miss: delete the file first, or use a fresh matrix.
The sandbox cannot unlink on the mounted repo (C10.2b), so **fresh matrices** it is — and
rather than one, **six**, one per serve class, so the figure is not a single happy path. Each
is timed on the miss and then immediately re-requested to time the hit beside it. All six are
at 45 min, a duration the chapter had no served plan at, which makes every one a genuine miss.

## 11.2 · End-to-end timings — the answer

| Matrix | Serve class | **miss** | hit | file written |
|---|---|---|---|---|
| 45 × 12 | whole top, scaled (identity *shape*, not identity) | **21.7 ms** | 5.3 ms | `ch_08_45m12_e16_c…100029` |
| 45 × 11 | single fill off the top | **11.4 ms** | 4.8 ms | `ch_08_45m11_e16_c…100029` |
| 45 × 8 | Case 1b complete rescue (cross-plan borrow) | **10.7 ms** | 4.3 ms | `ch_08_45m8_e16_c…101157` |
| 45 × 6 | below floor, one unit dropped | **8.9 ms** | 4.5 ms | `ch_08_45m6_e16_c…101157` |
| 60 × 3 + 45 × 9 | mixed duration | **11.1 ms** | 4.4 ms | `ch_08_60m3-45m9_e16_c…100029` |
| 45 × 14 | surrender (above the top) | **11.2 ms** | 5.1 ms | `ch_08_45m14_e16_c…100029` |
| 50 × 12 | **identity** — no file written at all | — | 3.2 ms | (registers `ch_08_canonical.json`) |

Median miss **11.15 ms**, median hit **4.65 ms**. Nothing is close to the budget; the whole
distribution fits inside a fiftieth of it.

**The 21.7 ms outlier is process warm-up, not the 12-unit plan.** `serve_plan` is imported
inside the request handler and `api/data.py` keeps an **mtime-keyed `_stream_cache`**, so the
very first request of a process pays for importing the engine and compiling all three
canonicals. The five misses after it — including the two *largest* payloads, 45×14 and the
mixed matrix — land at 8.9–11.4 ms. Sorting the misses by unit count produces no ordering at
all, which is the point below.

## 11.3 · Where the time actually goes

In-process, warm, medians of 7–9 runs:

| Component | Cost | How often |
|---|---|---|
| `load_genon_streams` — **cold**, compiling all 3 canonicals | **10.1 ms** | once per process (or after a canonical changes) |
| `load_genon_streams` — warm `_stream_cache` hit | **0.34 ms** | every request |
| `serve_plan` — selection, X−1+1, scaling, assessment remap | **0.20–0.34 ms** | every request |
| `json.dumps` of the 96 KB payload | **0.81 ms** | every miss |

Per serve class, `serve_plan` alone:

| Matrix | median | min / max | payload |
|---|---|---|---|
| 45 × 12 | 0.29 ms | 0.28 / 0.36 | 82 KB |
| 45 × 11 | 0.33 ms | 0.31 / 0.34 | 78 KB |
| 45 × 8 (rescue) | 0.24 ms | 0.22 / 0.25 | 52 KB |
| 45 × 6 (below floor) | 0.20 ms | 0.20 / 0.21 | 48 KB |
| 60 × 3 + 45 × 9 | 0.30 ms | 0.29 / 0.31 | 82 KB |
| 45 × 14 (surrender) | 0.30 ms | 0.29 / 0.31 | 82 KB |

**Selection costs a third of a millisecond and does not care which class it is.** The
cross-plan borrow, the mixed matrix, the below-floor drop and the surrender all cost the same
as a plain prefix — within 0.14 ms of each other, and tracking payload size rather than serve
complexity. That is what *"serving is SELECTION, never composition"* is supposed to look like
in a timer: nothing in the Xth-unit choice set, the duration scaling or the assessment remap
is doing real work at request time, because the work was done at authoring time.

**So the ~11 ms miss is dominated by everything except serving.** HTTP framing,
`_current_identity`, the register write and one 96 KB file write account for roughly 10 of the
11 ms; `serve_plan` is 3% of it. The corollary is the useful one for later: **making the
engine faster would buy nothing.** If a serve ever approaches the budget, the cause will be
I/O or the register, and that is where to look — this figure says so in advance.

**One number worth carrying forward for the cloud move.** The 10.1 ms cold compile is paid per
*process*, not per teacher, and it is invalidated by mtime — so it re-fires after every repair,
exactly as it should. On a serverless deployment with cold starts per invocation that 10 ms
becomes per-request, which still leaves 500× of headroom. Not a risk; recorded so nobody
re-measures it in a panic later.

## 11.4 · A note on the mixed matrix, and the same trap C6 recorded

`60 × 3 + 45 × 9` totals **12**, which is the top canonical's own count — so the serve took the
top *whole* (`mode: full`, no `slot_fill`) rather than filling. It returns 200 and times fine,
which is all C11 needs, but it contains **no borrowed sitting**. This is the trap the C6
record flagged when its first mixed matrix came to 10 and silently became p10 whole. C11 is
indifferent to it; **C12 is not** — the plan C12 opens must be
`ch_08_60m4-50m7_e16_c20260806100029.json`, which does carry a borrowed sitting. Choose a
mixed total that is not a canonical count.

## 11.5 · Residue — six files this run created and cannot delete

Fresh matrices are the only way to force a miss here, and each one writes a plan the sandbox
cannot remove afterwards. Left on disk in
`data/content/saved_plans/science/ix/`, all registered to kumar1/kumar2/kumar3:

- `ch_08_45m12_e16_c20260806100029.json` — **keep this one.** It restores the scaled
  identity-shape row the C6 record lists (`45m12` at e14) and the C9-era purge took, so the
  stage's evidence set is more complete than before this run, not less.
- `ch_08_45m11_e16_c20260806100029.json`
- `ch_08_45m8_e16_c20260806101157.json`
- `ch_08_45m6_e16_c20260806101157.json`
- `ch_08_60m3-45m9_e16_c20260806100029.json`
- `ch_08_45m14_e16_c20260806100029.json`

Every one is a valid serve at a valid duration and none of them is wrong; they are simply C11
artefacts rather than stage evidence. Delete the last five at your convenience — or leave
them, since they cost nothing and a future engine bump re-keys around them anyway. They join
the two C10.5 quarantine leftovers already named in that artefact.

---

## Status

**C11 PASS**, actual figures recorded either way as the step requires: worst 21.7 ms, median
miss 11.15 ms, median hit 4.65 ms, identity 3.2 ms — against 5 000 ms. Remaining in the stage:
C12 (view + exports, on `ch_08_60m4-50m7_e16_c20260806100029.json`), C13 (failure paths), C14,
then the gate.
