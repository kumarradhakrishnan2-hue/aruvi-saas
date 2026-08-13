# C11 · Serve wall time — english · III · ch 11

**Exit: total < 5 s. Measured: 2.8–4.4 ms on a cache miss, worst single observation 27 ms.
Roughly three orders of magnitude inside the bound.**

Measured against a live API (`uvicorn api.main:app`) pointed at the sandbox content copy
(`ARUVI_DATA_DIR=/tmp/c10/content`), whose derived plans had been purged at C10.2(b) — so every
request below is a genuine **cache miss**, not a hit. `curl -w '%{time_total}'`, as the template
specifies.

---

## 1 · Cache-miss end-to-end, the C6 request set

| request | mode | **miss (s)** | hit (s) |
|---|---|---|---|
| 40m9 | `fill/single` | **0.0193** ¹ | 0.0028 |
| 40m8 | `complete_rescue` | **0.0040** | 0.0019 |
| 40m11 | `synthesis` | **0.0033** | 0.0016 |
| 40m6 | `fill/single` (below floor) | **0.0033** | 0.0017 |
| 40m13 | surrender | **0.0034** | 0.0018 |
| 50m12 | scaled whole | **0.0037** | 0.0017 |
| 40m7+50m5 | mixed, scaled | **0.0034** | 0.0016 |

¹ the first request of a cold process — it pays the library read. Every miss after it is 3.3–4.0 ms.

## 2 · Twelve consecutive misses on fresh matrices, one warm process

| matrix | total (s) | | matrix | total (s) |
|---|---|---|---|---|
| 45m9+40m2 | 0.0269 ¹ | | 45m15+40m2 | 0.0029 |
| 45m10+40m2 | 0.0044 | | 45m16+40m2 | 0.0034 |
| 45m11+40m2 | 0.0040 | | 45m17+40m2 | 0.0029 |
| 45m12+40m2 | 0.0034 | | 45m18+40m2 | 0.0028 |
| 45m13+40m2 | 0.0034 | | 45m19+40m2 | 0.0029 |
| 45m14+40m2 | 0.0029 | | 45m20+40m2 | 0.0028 |

All HTTP 200. **Median 0.0031 s; excluding the cold first, the range is 2.8 – 4.4 ms and it
drifts *downwards* as the process warms.** ¹ again the first request of the process.

**The cold-start cost is per PROCESS, not per chapter.** A second cold request against a
different matrix, issued after the process was warm, came back in 0.0030 s — the 19–27 ms is the
library read and import warm-up happening once, not a property of any request shape.

## 3 · Where the milliseconds actually go

Timed in-process, with no HTTP and no file write, to separate selection from I/O:

| operation | median | min – max |
|---|---|---|
| `compile_stream` × all three canonicals | **0.63 ms** | 0.58 – 9.28 |
| `serve_plan` — `identity` (40m13 / 50m12 / mixed) | **0.19 ms** | 0.17 – 0.28 |
| `serve_plan` — `synthesis` (40m11) | **0.21 ms** | 0.19 – 0.25 |
| `serve_plan` — `fill/single` below floor (40m6) | **0.20 ms** | 0.20 – 0.22 |
| `serve_plan` — `complete_rescue` (40m8) | **0.26 ms** | 0.20 – 1.17 |
| `serve_plan` — `fill/single` (40m9) | **0.58 ms** | 0.24 – 1.40 |

(50 iterations each, 20 for compile.)

**Serving is selection and it costs a fifth of a millisecond.** The end-to-end 3 ms is almost
entirely FastAPI, JSON serialisation and the plan write — the engine's own work is under 5% of
it. That is the architecture's central claim (`variant_canonical_architecture.md`: "served …
deterministically, free, in milliseconds, by selection alone") measured rather than asserted.

**The costliest mode is the cheapest kind of work.** `complete_rescue` — the Case-1b path that
tries the upward serve, detects the drop, and falls back to the lower canonical plus the
standard's synthesis — costs **0.26 ms**, barely more than an identity. The rescue is not
expensive; it is one more comparison.

---

## Verdict

**PASS, with enormous margin.** Worst observed total 0.027 s against a 5 s bound — **185× under
it** — and the steady-state figure is 0.003 s, **1,600× under**. No defect.

For the record against C10.2(b)'s claim that a purge is affordable because "the next request
rebuilds in ~11 ms": measured here, the rebuild is **2.8–4.4 ms**, so the purge-over-fingerprint
decision is if anything better-founded than the note that recorded it.
