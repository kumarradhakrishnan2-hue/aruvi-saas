# C10 — Storage conventions · social_sciences · secondary · ch 3

**Library** {12, 9, 7} · **floor** 7 · **authored duration** 50 min · **engine** e10
**Run** 2026-08-02, alongside C6 · **Verdict** **all five checks PASS**

Ledger map: `…143756` = top (12) · `…144458` = p09 · `…150218` = p07.

---

## 10.1 · Filename conventions — PASS

Library files are `ch_NN_canonical.json` + `ch_NN_canonical_pKK.json`. Served plans are
`ch_NN_<matrix>_e10_c<chosen-variant ledger_ts>.json`, matrix duration-aggregated longest-first.

The **chosen-variant** rule (not the top's timestamp) is visible across the seven C6 files:

| Plan | X | Chosen variant | Key carries |
|---|---|---|---|
| `ch_03_50m8_e10_c20260801144458` | 8 | p09 | p09's ts |
| `ch_03_50m6_e10_c20260801150218` | 6 | p07 | p07's ts |
| `ch_03_50m10 / 50m11 / 50m13 / 60m2-50m8` | 10–13 | top | top's ts |
| `ch_03_45m9_e10_c20260801144458` | 9 @ 45 min | p09 | p09's ts |

Aggregation order confirmed by `60m2-50m8` (longest first), not `50m8-60m2`.

## 10.2 · Cache hit — PASS

kumar2 built `ch_03_50m10_e10_c20260801143756.json` at 06:59:08. kumar1 requested the identical
matrix at **07:11:33** and got `"cached": true` — the file's mtime stayed `12:29:08` and its
internal `saved_at` still read kumar2's timestamp. The register gained kumar1's key; the file was
not rewritten.

Two teachers, one file, no copy. Per-teacher visibility lives in the prepared register
(CLOUD_DATA_MODEL §2.3), exactly as designed. The same property holds for identity serves:
`ch_03_canonical.json` is registered by **all three** identities and exists once.

## 10.3 · No overwrite across engine versions — PASS

**Six** pre-campaign files (`_e08_`, `_e09_`) sit untouched beside the new `_e10_` set. An engine
bump re-keys the cache, so prior plans are stale by construction and are never overwritten —
they remain readable evidence of what an earlier engine served.

## 10.4 · Determinism — PASS

`ch_03_50m10_e10_c20260801143756.json` was copied aside, deleted, and re-requested by kumar1.
Response `"cached": false` (correctly — it genuinely rebuilt), same filename returned, and

```
diff <(jq 'del(.saved_at)' before) <(jq 'del(.saved_at)' after)   →  empty
```

Byte-identical apart from the top-level `saved_at`. Same `exact` mode, same `variant_used: 12`.

**Why it matters, since a teacher can never delete a plan:** deletion is only the instrument. The
rebuilds that happen in production are engine bumps (three in two days), canonical re-authoring
(new `ledger_ts` → re-key), storage migration or cache eviction, and — later — two API instances
racing to build the same plan. Determinism is what makes served plans *disposable*: they can
vanish and return with nothing changing for anyone, which is why they need no backup while the
library canonicals do. It is also what makes 10.2's file-sharing safe — the plan must be a
function of the request, not an artefact of whoever asked first.

## 10.5 · Quarantine is invisible to serving — PASS

Procedure: `docs/testing_artefacts/c10_5_quarantine.sh` (EXIT-trap restore; p09 is moved, never
deleted). Request under test: 50m × 8, whose closing unit p09 supplies.

| Phase | Library seen | Chosen | Mode | Filename | Names p09? |
|---|---|---|---|---|---|
| baseline | `[12, 9, 7]` | 9 | `superset` (borrowed from 7) | `…c20260801144458` | **False** |
| p09 quarantined | `[12, 7]` | 12 | `exact` (borrowed from 7) | `…c20260801143756` | **False** |
| p09 restored | `[12, 9, 7]` | 9 | `superset` (borrowed from 7) | `…c20260801144458` | **False** |

Nothing 500'd, the library glob simply stopped seeing the quarantined file, and no response
named it in any field at any phase (checked against the raw JSON, not just the summary keys).
Serving fell through to the next surviving variant and returned to normal on restore.

**The re-key is structural, not incidental.** Because the filename carries the *chosen variant's*
`ledger_ts`, removing p09 changes which variant is chosen and therefore changes the address — so
a quarantined variant's plans can never be served from cache by accident. The fall-through cannot
collide with the pre-quarantine file.

**Clean-up verified:** quarantine directory empty, p09 back and intact (ledger `20260801_144458`,
9 units, 18 items), the temporary top-keyed plan removed along with its dangling register key, and
the library byte-for-byte the 16 files it was at baseline.

**One observation for the human gate, not a defect.** With p09 present, X=8 serves `superset` and
carries a coverage note ("briefly re-crosses Climate Change as runway"); without p09 it serves
`exact` and carries none. Both are full-coverage, but the *smaller* library produced the cleaner
note here. That is the next-highest doctrine working as intended — it prefers the richest
authored source over the tidiest note — but it is worth the founder reading both closing sittings
side by side at the gate, since it is a case where the rule's output is arguably less elegant than
the alternative it rejected.

---

## Status

C10 is complete ahead of its place in the template (run opportunistically during C6). Remaining
before the human gate: C7 (register audit — file-only), C8 (LLM-need flags), C9 (assessment
anchoring across the serve — file-only), C11 (serve wall time), C12 (view + exports),
C13 (failure paths).
