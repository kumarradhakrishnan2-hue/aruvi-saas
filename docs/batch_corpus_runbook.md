# Batch corpus runbook — any subject · stage

Written from S5 (the_world_around_us · preparatory, 2026-08-12): 32 chapters, 93 canonicals,
₹1,212.90, ~25 minutes of processing, 28 declared repairs, **zero canonicals re-bought**.
Nothing below is TWAU-specific. Substitute `{subject}` and `{grades}` and run it.

---

## 0. Before any money moves

| gate | check |
|---|---|
| stage prep | P1–P5.5 signed off; constitutions amended and version-bumped |
| carrier | `require_carrier({subject}, {grade})` returns — the submit refuses without it |
| pilot | the stage's pilot chapter has been through the C-cycle |
| content | every chapter has a summary **and** a mapping; `master_plan.json` rows non-placeholder |
| credit | ~2× the estimate on the key (below); API credit, not a Claude subscription |
| place | **Terminal, not a Cowork sandbox** — the proxy blocks credentialed calls |

```bash
python3 genon/batch_api.py submit {subject} {grades} --wave top --dry
```

The dry run is the gate: it builds every prompt and prints the worklist. Read it. Confirm the
chapter count, the period counts against the master plan, and that any skip line says what you
expect. Then confirm the amended constitution actually reached the payload:

```bash
python3 -c "
import json,glob,os
f=max(glob.glob('genon/out/batches/DRY_{subject}_top_*.json'), key=os.path.getmtime)
print(f)
t=json.load(open(f))[0]['params']['system'][0]['text']
print([l for l in t.splitlines() if 'VERSION' in l][:2])"
```

**Scope the glob to `{subject}` and sort by mtime — both, always.** This check was written at S5
when TWAU was the only subject with dry files on disk. `sorted(glob('DRY_*top*'))[-1]` sorts
ALPHABETICALLY, so from S2·social_sciences onward it silently read
`DRY_the_world_around_us_top_*` and printed TWAU's versions against an SS submit (2026-08-15).
A gate that cannot fail loudly is not a gate: print the filename too, and confirm the SUBJECT
on the version lines before the version number.

## 1. Price it first

Runs = Σ `len(canonical_periods)` over non-placeholder chapters, minus anything already installed.
Cost per run tracks output, which tracks period count:

```
output_tokens ≈ 1.2k + 1.435k × periods        (fit on any stage's first three runs)
batch ₹/run   ≈ (input×$3 + output×$15)/1e6 × 92 × 0.5
```

S5 measured **₹12–15/run** at batch pricing with the system block cached, against ₹31 sync.
Budget ~2× the estimate: cache hits are best-effort (30–98%), and a systematic defect means
re-authoring a wave.

## 2. Two waves, never one

A compact's brief is built from its **standard's** section registry — `variant_plans.briefs_for`
reads the top off disk and refuses a provisional row. So:

```bash
# WAVE 1 — the standards
python3 genon/batch_api.py submit {subject} {grades} --wave top
python3 genon/batch_api.py status  <manifest>          # 'ended' is the signal
python3 genon/batch_api.py collect <manifest>          # installs + logs
python3 genon/batch_build.py {subject} {grades} --certify-only   # FREE, and REQUIRED

# WAVE 2 — the compacts (only after the certify pass annotates the rows)
python3 genon/batch_api.py submit {subject} {grades} --wave compact --dry
python3 genon/batch_api.py submit {subject} {grades} --wave compact
python3 genon/batch_api.py status  <manifest>
python3 genon/batch_api.py collect <manifest>
python3 genon/batch_build.py {subject} {grades} --certify-only
```

**Between the waves every chapter FAILS `library complete`** — its compacts do not exist yet.
That is arithmetic, not a defect. The certify pass is run for its *annotate* half.

Once two manifests exist, **pass the path explicitly**. `--latest` is by mtime now, but an
explicit path cannot read the wrong wave.

A batch is server-side: after submit you may shut the laptop. Results keep for 29 days.

## 3. Triage — the five defect families, and what each costs

Read the FAIL census first, not individual reports:

```bash
grep -h "^FAIL" genon/out/library_reports/{subject}_*_<stamp>*.md \
  | sed 's/ch_[0-9]*_canonical[^:]*: //' | sort | uniq -c | sort -rn
```

| family | looks like | tool | cost |
|---|---|---|---|
| register ban hit | "for two minutes", "this week", "in the next unit" | `repair_register.py` | free |
| anchor joiner | `A; B` or `A, B` instead of `A / B` | `repair_anchors.py` | free |
| section missing from registry | a compact anchors a real section the top never named | `repair_anchors.py` + judgement | free |
| first-visit order | a compact teaches a late section early | `repair_unit_order.py` | free |
| wrong-column `question_type` | a mode/tier code where a type belongs | `repair_item_type.py` | free |
| **section the summary carries and no unit anchors** | C5 check 11 FAILs, naming the section | **none — re-author the top + its compacts, or rule the omission accepted** | **~₹37/run × the chapter's plan size** |

**Regenerating is a lottery (founder, 2026-08-02).** Repair unless the fix is a real teaching
change. Every repair is a STATED (old → new) pair with its evidence in the declaration, applied
by assertion — never a normalizer that computes at apply time, never a hand edit.

Rates to expect, from S5: ~1 register breach per 3 files, ~1 wrong-column item per 90 runs,
a handful of joiner slips. All were free. Budget effort, not money.

## 4. The traps that cost time (all learned the hard way)

1. **A quarantined file skips every later repair sweep.** Re-scan anything you restore — twice
   at S5 a restored file carried an unrepaired hit its siblings had lost.
2. **Purge derived plans after any in-place repair, and check it worked.** `canonical_version`
   is the generation timestamp; a repair does not move it, so the cache serves pre-repair bytes
   forever (ARV-D-034). If the purge prints "could not remove", delete by hand before serving.
3. **`--max-fails` is a money brake.** It is off under `--certify-only`; do not re-arm it there.
4. **A false positive is fixed at the scanner, not in the text.** If a pattern flags correct
   pedagogy ("half the class will be…"), make it advisory in `register_scan.py` and say why.
   Striking good teaching to satisfy a regex is the wrong direction.
5. **CLOSED 2026-08-13 — the registry is derived from the top, so a top-level omission used to
   be invisible** to certification: the check cannot see what it is built from. It is now
   **C5 check 11** (`genon/summary_sections.py`), which reconciles the registry against the
   chapter summary and fails on any section no unit anchors — it caught science·ix ch 8 omitting
   `8.5 Atomic Number` on a library already certified ALL PASS. A section reached only through
   the standard's closing SYNTHESIS unit is taught (that unit is outside the registry by design
   but anchors a real section on every mediated-anchor stage) and is reported, not failed.
   Read it as a defect family
   (below), not a trap. It gates on mathematics · english · TWAU · science and returns an
   ADVISORY shortlist on social_sciences, whose summaries carry no structural section marker.
6. **Field names differ by stage.** `section_anchor`/`section_ref`, `teacher_notes`/
   `teacher_facilitation_note`. Every tool reads through a carrier seam; if a repair refuses
   with "declared text not found", suspect the field before the text.
7. **Restart uvicorn after any plugin/carrier change**, or the first serve check reproduces a
   `KeyError` that looks like a data defect.

## 5. Closing checklist — what "released" means

```bash
# 1. every canonical the master plan expects is on disk
# 2. no quarantined file lacks a live counterpart
# 3. zero register ban hits library-wide
# 4. every chapter ALL PASS — including C5 check 11, and on a prose subject
#    (social_sciences) its advisory shortlist has been ruled on rather than skimmed
# 5. every chapter serves at top / middle / floor / below-floor
# 6. no derived plans left on disk
# 7. spend reconciled from runtime_data/token_log.csv
```

Then, and only then, the **human gate**: the serve-sweep table, the synthesis unit read in
full, each compact's ending, and any register judgement calls. Deterministic ALL PASS is a
precondition, never the verdict — and in a batch the founder samples at a rate they choose.

**Recorded in the tracker's BATCH RELEASE tab** (added 2026-08-13; `docs/testing_tracker.html`,
scope `batch`, keyed subject·stage): **W1** = this document's wave 1, **W2** = wave 2 plus the
closing checklist above, **F1** = C8 across the batch, **F2** = C14 across the batch. F1 and F2
are the batch analogue of the human gate, and **the sample size and stratification go in the
step's comment before the reading starts** — "a rate they choose" only means anything once it is
written down. Stratify by period-count band (floor compacts and the borrow slot concentrate the
defects, not the top) and include 100% of any chapter that took a repair: a chapter with one
register breach is the likeliest place a paraphrased one survived.

Record the stage in `MEMORY.md`: spend, defect families and rates, every repair declared, and
anything the campaign should meet earlier next time.
