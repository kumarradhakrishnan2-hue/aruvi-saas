# C5 — read the certification report · english · IX · ch 7 *Vitamin-M*

**Date:** 2026-08-12 · **Report:** `genon/out/library_reports/english_ix_ch07_20260812_143511.md`
· **Library:** `ch_07_canonical.json` (17) · `_p14.json` (14) · `_p10.json` (10) · LP v1.2 ·
assessment v1.4 · engine 19

**Verdict: the report says DETERMINISTIC CHECKS ALL PASS, and every check is confirmed
independently below.** One exit condition is satisfied in substance but not yet in fact — the
quarantine directory still holds three stale copies from the false-fail run, and the sandbox
cannot unlink them (§Quarantine).

Each check is `genon/build_library.py::certify`'s, cited not re-specified; where I could
re-derive the answer without the certifier I did, so the report is corroborated rather than
quoted back.

| # | Check | Report | Independently confirmed |
|---|---|---|---|
| **1** | library complete vs `canonical_plan.counts` | PASS | `[17, 14, 10]` on disk = the row's counts, `basis: authored_standard`, `registry 6 sections`. |
| **2** | every file compiles (`compile_stream` v0.5) | PASS (implicit — a failure reads "does not compile") | Re-run: all three compile. 17 units / 54 phases, 14 / 57, 10 / 26; 6 items each; `stream_format: aruvi-phase-stream v0.5 (unit-anchored)`. |
| **3** | anchors verbatim in the top registry | PASS ×3 | Every anchor on all 41 units resolves in the top registry; **zero** anchors outside it. The registry is the six composite cells `A|reading_for_comprehension · A|vocabulary_grammar · A|listening · A|speaking · A|writing · A|beyond_text` — this stage's token is built by the platform from `section_id` + `spines_taught[]`, so "verbatim" here is really asking whether those two fields came out clean on 41 units. They did. |
| **4** | first-visit order follows the registry | PASS ×3 | All three files' first-visit sequence is the registry **in full and in order** — identical across the standard and both compacts, which is the property the Xth-unit choice set runs on. |
| **5** | coverage reaches the final registry section | PASS ×3 | All six cells reached in every file; on the standard, before the synthesis unit (U17). This is S11's coverage amendment holding at every count, including the floor. |
| **6** | synthesis-anchor gate | PASS ×3 | Standard: synthesis on U17 and nowhere else. p14 and p10: **no synthesis unit at all**. Note this stage carries the fact as the `"synthesis": true` BOOLEAN, not the reserved token — `genon_anchor_field_present` is False for english, so `is_synthesis` reads the boolean carrier. |
| **7** | serve sweep, floor−2 … top+2 | PASS, no exception | Re-run independently — the table below reproduces the report exactly, X = 8 … 19. |
| **8** | no defensive truncation | PASS ×12 | No `truncation` mode appears anywhere in the sweep. The only rows carrying drops are X = 8 and 9, **below the floor of 10**, where drops are the declared cost rather than a failure. |
| **9** | register clean | PASS ×3, 0 ban hits | Re-run `register_scan` myself: **0 BAN hits** across all three files over `activity_title` · `materials` · `teacher_notes` · `time_bands[].activity` · `homework[]` (54 / 57 / 26 bands read). Two ADVISORY hits, both correctly non-gating (§Advisories). |
| **9a** | MCQ options in arrangement order | PASS ×3 | Read on the FIRST pass, as the template requires: `options arranged: 1 of 1 item(s) re-ordered`. The library has exactly one options-bearing item — the TRUE_FALSE — and STEP 6 moved it. On the re-certify run it reads `0 of 1`, which means only that nothing was left to move. |
| **10** | item counts per competency — ADVISORY | reports 0 vs 0 ×3 | **N/A in substance, and it should be.** English performs no per-chapter competency mapping and C-codes are forbidden in its LP and assessment (LP Rule 7), so there are no competencies to group by. The advisory's `expected {"(from handoff)": 0}` is the honest reading of a handoff that carries none. Carried into the C4 record. |

## The serve sweep — re-derived, not copied

| X | mode | sittings | drops | variant | borrowed from |
|---|---|---|---|---|---|
| 8 | fill/forward −2s | 8 | 2 | 10 | 10 |
| 9 | fill/single −1s | 9 | 1 | 10 | 10 |
| **10** | **identity** | 10 | 0 | 10 | — |
| 11 | rescue/complete (from 14) | 11 | 0 | 10 | **17** |
| 12 | fill/single | 12 | 0 | 14 | 14 |
| 13 | fill/single | 13 | 0 | 14 | 14 |
| **14** | **identity** | 14 | 0 | 14 | — |
| 15 | rescue/complete (from 17) | 15 | 0 | 14 | **17** |
| 16 | fill/single | 16 | 0 | 17 | 17 |
| **17** | **identity** | 17 | 0 | 17 | — |
| 18 | surrender | 17 | 0 | 17 | — |
| 19 | surrender | 17 | 0 | 17 | — |

Three identities at the three authored counts; **no drops anywhere inside [10, 17]**; drops only
below the floor, with a coverage note attached (*"Time budget short of the chapter's full…"*);
surrender above the top, declared in minutes (*"1 period (50 minutes) exceed this chapter…"*).
The two `rescue/complete` rows at X = 11 and 15 are the Case-1 borrow — a shorter canonical
served complete and closed with **the standard's synthesis unit**, which is exactly the joint
C8 inspects and where C3's ARV-D-132 lands.

## Advisories — both non-gating, and one is worth keeping

- **p14 U9, band 1, family `calendar`:** *"…today's podcast on meditation explores a discipline
  that cultivates exactly that quality."* Advisory by design — the template's own example is
  "Will it rain today?", and this is the same construction: "today's podcast" names the lesson's
  own material, not a calendar date. Correctly not a ban hit.
- **p10 U10, `teacher_notes`, family `positional`:** *"…The photograph slide-show task is set as
  homework and **does not require any classroom artefact from an earlier unit**."* The scanner
  flagged the phrase "earlier unit"; what the sentence actually does is **declare artefact
  independence out loud**. Worth recording because the standard canonical failed at precisely
  this (ARV-D-132: U17 lists U15's draft article in `materials`). **The compact states the rule
  the standard broke** — same chapter, same run, same constitution. That is evidence the model
  understands the constraint and applies it unevenly, which is a generation-variance finding
  rather than a comprehension one.

## Quarantine — the one exit condition not yet met in fact

`backup/quarantine/english/ix/` holds three files:

```
ch_07_canonical_20260812_143130.json
ch_07_canonical_p10_20260812_143130.json
ch_07_canonical_p14_20260812_143130.json
```

They are **stale copies from the false-fail certification run** (ARV-D-127, closed): the
item-shape gate read `question_text` where english's constitution names the field `item_stem`,
failed all 18 items, and quarantined the library. The gate is fixed, the files were restored,
and the library re-certified ALL PASS — so there is no fix worklist behind these three, and
nothing in them is servable (quarantine is outside every read path).

The sandbox cannot unlink them (`PermissionError: Operation not permitted` on both `rm` and
`os.remove`), so this needs one command on the founder's machine:

```bash
rm backup/quarantine/english/ix/ch_07_canonical*_20260812_143130.json
```

**Recorded rather than waived:** step 0.8's doctrine is that a non-empty quarantine reads as an
open worklist, and the whole point of that rule is that nobody has to ask whether an entry is
stale. Until the `rm` runs, this chapter's quarantine line is satisfied in substance and not in
fact. (Unrelated and not mine to touch: `backup/quarantine/the_world_around_us/iv/ch_06_…` from
14:16 today.)

## What C6 inherits

- **The three identity counts are 10, 14, 17** — the natural requests for kumar1's identity runs.
- **X = 11 and X = 15 are the borrow rows**, and kumar2 owns the between-variant requests.
- **X = 8 and 9 are the below-floor rows** with declared drops (2 and 1), also kumar2's.
- **kumar3's mixed-duration week is real**: the profile carries `[50, 60]` with
  `ppw_by_duration {50: 5, 60: 1}`, so the mixed matrix has something to draw on rather than a
  synthetic row.
