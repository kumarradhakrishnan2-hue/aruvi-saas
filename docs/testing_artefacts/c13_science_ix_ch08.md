# C13 — Failure paths · science · secondary (IX) · ch 8

**Library** {12, 10, 7} · **floor** 7 · **engine** e16 · **Run** 2026-08-06
**Runbook** `docs/testing_artefacts/c13_runbook_science_ix_ch08.sh` ·
**Responses** `docs/testing_artefacts/c13_responses/`

**Verdict: PASS on all four. Twelve broken requests, twelve readable answers, zero
tracebacks in any body.** Every check runs against the live API; case 3 runs against a
throwaway content root so nothing broken is ever written into the repo.

---

## 13.1 · No canonical — PASS

| Request | Code | Detail |
|---|---|---|
| `POST /genon/science/ix/**3**/plan` (a real chapter, no library) | **404** | `No underlying chapter yet.` |
| `POST /genon/science/ix/**99**/plan` (no such chapter at all) | **404** | `No underlying chapter yet.` |

The 2026-08-04 founder wording holds on both paths, and it holds for the right reason — the
message talks about the **chapter**, in her language. Nothing in it says "canonical",
"library", "variant" or "stream". Worth noting that a teacher will hit this constantly during
the pilot: science IX has **one** authored chapter out of thirteen
(`chapters: [8]`), so twelve of her thirteen chapters answer with this sentence. It is the
most-seen error message in the product, and it reads like a status, not a failure.

## 13.2 · Implausible and empty matrices — PASS, and the boundary is on the total

| Request | Code | Detail |
|---|---|---|
| one row, 50 × **61** | **400** | `Period count implausibly large.` |
| **two rows**, 50 × 40 + 60 × 40 = 80 | **400** | `Period count implausibly large.` |
| `rows: []` | **400** | `At least one duration row is required.` |
| one row, 50 × **0** | **400** | `At least one duration row is required.` |

The split row is the one worth having: the guard is on the **aggregate**, not per row, so it
cannot be walked past by spreading the ask across durations. And a row with `count: 0` is
filtered out *before* the emptiness test, so it lands on the "give me a row" message rather
than a confusing "too large" — the two messages divide the space cleanly with no gap between
them.

## 13.3 · Unresolvable item anchor — PASS, and it names the item

**How this was isolated.** The step says to copy the canonical to a scratch chapter number and
remove the scratch file afterwards. The sandbox cannot unlink on the mounted repo (C10.2b), and
a permanent broken `ch_90_canonical.json` in `data/content/` would be worse than clutter —
`genon_chapters()` lists any `ch_NN_canonical.json` it finds, so the scratch chapter would
advertise itself as certified content forever. So the whole check ran against a **throwaway
content root** at `/tmp/c13_content` (symlinks to the real content, a private `saved_plans/`
holding copies), served by a second API on `:8001` through `ARUVI_DATA_DIR`. Nothing was
written into the repo; the scratch tree was deleted at the end, where deletion works.

**How the break was made.** Science·secondary is the **handoff-bridged** family — `carriers.py`
resolves an item's unit through the `coverage_handoff` row matching its section **label**, not
through a `period_ref`. So an item is made unresolvable by naming a section the chapter does not
teach: question #1's `section_number → 99`, `section_label → "8.99 A Section This Chapter Does
Not Teach"`. (A subject in the item-self-sufficient family would need its `period_ref` broken
instead — the break is family-specific, and a runbook copied to another stage must change here.)

**Result — `POST /genon/science/ix/90/plan`, 11 × 50:**

```
HTTP 500
Canonical cannot be compiled: canonical plan is not v1.1-declared (1 problem):
assessment item #1 MCQ / C-1.1: no resolvable anchor unit (period_ref/phase_ref)
 — it names nothing
```

It names the item three ways — **position (#1), type (MCQ) and competency (C-1.1)** — which is
the 2026-08-04 improvement working: "assessment item ?" would tell a reader nothing about which
question is broken in a 12-item file. Not a bare 500, no traceback, and the count ("1 problem")
tells you whether to expect more.

**Control.** An unmodified copy at chapter **91** in the same scratch root returned **200** and
served `ch_91_50m11_e16_c20260806100029.json`. So the 500 is the broken item, not the scratch
root.

**One observation for the gate, filed as a note rather than a defect.** The detail string
contains `"canonical plan is not v1.1-declared"` — engine vocabulary, of the same family as the
"canonical" the founder struck from the 404. It is defensible: this is a 500, it can only fire
on an **uncertified** library (C1's certifier gates exactly this), and the words need to be
diagnostic for us rather than gentle for her. But if it ever does reach a teacher it will read
as machine noise, and the C13 promise is "a message a teacher can read". Worth a founder ruling
at the gate: leave it as an operator string, or wrap it the way the 404 was wrapped.

## 13.4 · Quarantined variant absent from serving — PASS

The C10.5 transcript re-read as a failure path, which is what the step asks for:

| Request during quarantine | status | library seen | chosen | `detail` in body | names `p10` |
|---|---|---|---|---|---|
| X = 9 | `prepared` | `[12, 7]` | 12 | no | **no** |
| X = 8 | `prepared` | `[12, 10, 7]` (cached) | 7 | no | **no** |
| X = 10 | `prepared` | `[12, 7]` | 12 | no | **no** |

Nothing 500'd, no response carries a `detail` key at all, and no response names the withheld
file. A missing library file is not an error path in this system — it is simply a smaller
library, and the serve falls through. That is the property C10.5 proved and this step
re-reads: **the failure mode of a vanished variant is a quieter plan, not an exception.**

## 13.5 · Beyond the step — three neighbouring bad inputs

Not required by C13, cheap to run, and they make the same promise:

| Request | Code | Detail |
|---|---|---|
| `POST /genon/**astrology**/ix/8/plan` | **404** | `Unknown subject: astrology` |
| `GET /plans/science/ix/**ch_08_50m99_e16_cdeadbeef.json**/view` | **404** | `Saved plan not found.` |
| `POST /plans-prepared` with `filename: "../../etc/passwd"` | **400** | `Invalid plan filename.` |

**A correction to my own first reading, worth recording.** Path traversal in the *URL*
(`/plans/science/ix/..%2F..%2Fetc%2Fpasswd/view`, tried four ways including
`curl --path-as-is`) returns **404 `Not Found`**, not the app's 400 — which first looked like
the `_plan_key` guard failing. It is not: Starlette's router rejects those paths before any
handler runs, so the guard is never reached. The guard exists for filenames arriving in a
**request body**, and tested there it fires correctly with `400 Invalid plan filename.` Two
layers, both closed; the 404 is the outer one doing its job.

## 13.6 · The traceback sweep

Every response body this run produced was scanned for `Traceback (most recent`, `File "/`,
`, line N, in`, and `.py", line`:

```
bodies scanned: 12
bodies containing anything traceback-shaped: NONE
```

Including the two 500s. The `_export_plan` handler prints the traceback to the **server log**
and returns only `{message} [{last aruvi/api frame}]` to the client — the frame reference is a
file-and-line hint, not a stack, and it is what made C12's `xhtml2pdf` gap diagnosable in one
read without leaking anything.

---

## Status

**C13 PASS** — all four paths surface a code and a readable sentence; nothing resembling a
traceback in any body. One founder call is parked for the gate: whether
`"canonical plan is not v1.1-declared"` should stay operator vocabulary (§13.3). Remaining in
the stage: **C14** (copyright review), then the gate — plus the browser work owed from C12
(§12.5) and the two residue clean-ups from C10.5 and C11.
