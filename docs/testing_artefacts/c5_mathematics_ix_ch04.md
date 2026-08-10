# C5 — certification report read · mathematics · IX · chapter 4

**Report:** `genon/out/library_reports/mathematics_ix_ch04_20260809_154113.md` — closing line
**DETERMINISTIC CHECKS ALL PASS**.
**Library:** counts `[15, 12, 9]` · basis `authored_standard` · registry 8 sections ·
floor `9` · serve granularity `unit` · section axis `True`.
**Constitutions of record:** LP v1.3 · assessment v1.2. **Engine:** `GENON_ENGINE_VERSION = 17`.
**Checks implemented in** `genon/build_library.py::certify` — cited, not re-specified.

---

## The ten checks

| # | Check | Verdict | Evidence from the report |
|---|---|---|---|
| 1 | library complete | **PASS** | `['ch_04_canonical.json', 'ch_04_canonical_p12.json', 'ch_04_canonical_p09.json']` vs plan `[15, 12, 9]` |
| 2 | every file compiles (`compile_stream` v0.5) | **PASS** | re-run independently at C5: 15 / 12 / 9 units, no exception |
| 3 | anchors verbatim in the top registry | **PASS** | one line per file, all three |
| 4 | first-visit order follows the registry | **PASS** | one line per file, all three |
| 5 | coverage reaches the final registry section | **PASS** | standard qualified "before the synthesis unit"; compacts unqualified |
| 6 | synthesis-anchor gate | **PASS** | standard "closes with the mandated `synthesis` unit (and carries the token nowhere else)"; both compacts "the `synthesis` token is reserved to the standard canonical" |
| 7 | serve sweep, no exception | **PASS** | X = 7…17, eleven rows, table below |
| 8 | no defensive truncation | **PASS** | "choice set non-empty" at every X from 7 to 17; **no `truncation` mode appears at all** |
| 9 | register clean | **PASS** | 0 ban hits per file — but read the caveat below, it is the weakest PASS in this report |
| 9a | MCQ options in arrangement order | **PASS** | all three files; `0 of 5 re-ordered` on this run, which proves STEP 6 ran, not that the model arranged them |
| 10 | item counts per competency — ADVISORY | **reports, does not gate** | `expected {}` · basis "derived"; see below — inert at this stage by construction |

**Sweep range is correct.** The spec requires `floor − 2` to `top + 2`. `master_plan.json` gives
`floor_periods_at_standard = 9` and top = 15, so the required span is **7 → 17**, and the report
covers exactly 7 → 17. Nothing was sampled short.

**Quarantine:** `find backup/quarantine -name "*.json"` → **0 files**, campaign-wide, not merely
for this chapter.

## The serve sweep

| X | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mode | fill/single | fill/single | **identity** | fill/single | synthesis | **identity** | fill/single | synthesis | **identity** | surrender | surrender |

Three identities at 9, 12 and 15 — exactly the authored counts, so each canonical is reachable
as itself. Surrender only above the top, which is where the architecture says it belongs. **No
row carries a drop count** (`-Ns`), including the two below-floor requests at X = 7 and X = 8:
this chapter's compacts cover all eight sections, so a short serve loses units but never a
section. Confirmed independently at C3's post-repair sweep (`dropped_units` empty at every X).

## Three things the report says that need reading, not just ticking

**(a) The handoff/anchor ADVISORY is the *expected consequence* of the ARV-D-074 repair — do not
"fix" it.** The report flags:

> `ADVISORY ch_04_canonical.json: 2 unit(s) wear a section label the handoff does not route items
> through: U9=4.6, U12=4.7 (do NOT extend period_numbers to fix this — it moves the item to a
> later unit and loses it on short serves)`

Those are precisely the two units C3 removed from `period_numbers` because they consolidate a
section already taught rather than teach it (Rule 12). The advisory is the certifier observing
the intended end state, and its own parenthesis forbids the "repair" a future reader would
reach for. p12 and p09 carry one each, both on their multi-section closing units, same reason.
Recorded here so this is never mistaken for a regression.

**(b) Check 9 passes, and C3 proved that a pass here does not mean the register is clean.** When
C3 ran, `register_scan` reported *"register clean (0 ban hit(s))"* on files carrying **fourteen**
register breaches — "will recur", "once section 4.7 has been taught", "after section 4.7 is
covered", "a final unit", and a `today` classified ADVISORY by design. No pattern covered them.
The register is clean today because C3 repaired those strings by hand, **not because this gate
found them.** The scan's own coverage line (`60 band(s) read … activity_title 15, teacher_notes
15, time_bands 60, homework 6`) confirms it reached the text — the gap is in the patterns, not
the reach. Carried to §7 as the standing C5 tooling gap, alongside the self-correction regex
that would have caught both ARV-D-084 and ARV-D-085.

**(c) Check 10 is inert at this stage by construction, and should stay that way.**
`EXACT_ITEM_COUNTS` carries one row, `("social_sciences", "secondary")`, so maths falls to the
modal-count fallback and compares each file to its siblings: 14 vs 14, 13 vs 13, 9 vs 9 — self-
consistent and therefore uninformative. **This is not a missing constitution row to be filled.**
The check compares items to a fixed count per competency *weight label*, and maths·secondary has
no weight slate: Rule 5 sets the count as one item per `implied_lo`, which varies per chapter by
design. The real check exists and was run at C4 (item 3), where it passed per file **and per
section**. Adding a maths row to `EXACT_ITEM_COUNTS` would encode a slate the constitution does
not have.

---

## Verdict

**C5 = PASS.** All ten deterministic checks pass on the newest report, the sweep spans the full
required range with no exception and no drops, quarantine is empty, and check 2 was re-run
independently rather than taken on the report's word.

No defect filed. Two observations carried forward: the handoff/anchor advisory is correct and
must not be undone, and check 9's gate remains weaker than its PASS implies — which is the one
thing in this report that would mislead a reader who ticked it without reading C3.
