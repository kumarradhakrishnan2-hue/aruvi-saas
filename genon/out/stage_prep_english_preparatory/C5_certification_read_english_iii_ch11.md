# C5 · Certification report read — english · III · ch 11 *The Big Laddoo*

**Report:** `genon/out/library_reports/english_iii_ch11_20260813_124746.md`
**Verdict line:** `DETERMINISTIC CHECKS ALL PASS.`
**Implementation:** `genon/build_library.py::certify` (line 242) — checks cited below by their
line in that function, not re-specified.
**Quarantine:** `backup/quarantine/english/iii/` **does not exist / is empty**. The only english
entries in quarantine are `english/ix` (S11's ARV-D-136 re-author, 3 files) and they belong to a
different stage and chapter.

**Exit met: report says ALL PASS; quarantine empty for this chapter.**

An earlier report exists for the same chapter — `..._20260813_123939.md` — from the
`--top-only` pass. Its single `FAIL library complete` was the not-yet-authored compacts, and it
is superseded. Reading the newest, as C5 requires.

---

## The eleven checks

| # | Check | Result | What the report says, and what it means here |
|---|---|---|---|
| 1 | **library complete** (`:264`) | **PASS** | `['ch_11_canonical.json', 'ch_11_canonical_p10.json', 'ch_11_canonical_p07.json'] vs plan [12, 10, 7]`. Three files, three counts, in order. |
| 2 | **every file compiles** (`compile_stream` v0.5, `:236`) | **PASS, by absence** | This check reports only on failure — `FAIL <name>: does not compile — <e>` — so a clean report is the pass. Confirmed independently: all three files load through `compile_stream` in the sweep below, which could not run otherwise. Worth stating explicitly because a compile failure is the error mode that reports itself as "does not compile" on *every* file while naming nothing (the P5.5 carrier trap). |
| 3 | **anchors verbatim** (`:361`) | **PASS ×3** | `every anchor verbatim in the top registry`, on all three files. The registry is the five cells `B\|reading · B\|oracy · B\|writing · B\|word_work · B\|beyond_text`; every unit of every file draws its anchor from that list byte-for-byte. The reserved `synthesis` token is exempt by design — it is not a section. |
| 4 | **first-visit order** (`:371`) | **PASS ×3** | `first-visit order follows the registry`, on all three. First visits land at units 1 · 3 · 5 · 7 · 9 in the top; the revisit tails (u10 writing, u11 reading+oracy) are legal and the synthesis unit is skipped by the walk. **The three files agree**, which is the property the Xth-unit choice set depends on — a compact whose first-visit order differed would make a borrowed unit arrive out of sequence. |
| 5 | **coverage reaches the final registry section** (`:373`) | **PASS ×3** | The standard reaches `B\|beyond_text` at unit 9, comfortably before the A−1 bound of 11. Both compacts reach it too. |
| 6 | **synthesis-anchor gate** (`:350`, `:354`) | **PASS ×3** | `standard closes with the mandated synthesis unit (and carries the token nowhere else)`; `the synthesis token is reserved to the standard canonical` on both compacts. On this stage the carrier is the **`"synthesis": true` boolean**, not a `section_anchor` token, because `genon_anchor_field_present` is False for english — the brief asked for the boolean and the gate reads it. |
| 7 | **serve sweep** | **PASS — no exception at any X** | X from `floor−2` = 5 to `top+2` = 14. Full table in §2. |
| 8 | **no defensive truncation** (`:727`) | **PASS ×10** | `choice set non-empty` at every X from 5 to 14. Case 3 stays structurally impossible, as §0.4 requires. |
| 9 | **register clean** (`register_scan.py`, `:473`) | **PASS ×3, and the scan is proven to have REACHED the text** | `0 ban hit(s)` on all three, over **49 / 50 / 34 bands** plus `activity_title`, `materials`, `teacher_notes` and `homework`. The band-count line matters more than the zero: a scan that read nothing also reports zero. No advisories either. |
| 9a | **MCQ options in arrangement order** (`:636`) | **PASS ×3** | The gate proves STEP 6 ran. **Read the arrangement count from the FIRST pass, and it is the finding of this report**: `4 of 6 item(s) re-ordered` — p07 2 of 2, p10 2 of 2, the top 0 of 2 *because its two were already sorted by the earlier `--top-only` certify run*. Across the library the correct option was authored at **position B in five of five** MCQ/TRUE_FALSE items, scattered by the sort to C · D · B · C · B. |
| 10 | **item counts per competency — ADVISORY** (`:655`) | **reports 0 vs 0, and that is correct** | `expected {"(from handoff)": 0}` · `0 items vs 0 expected` on all three. **English has no competency axis** — Rule 7 of its LP constitution forbids C-codes anywhere, and its item count is structural (2 × `section_contributions`), so there is no per-competency slate for this check to compare against. It is reporting an empty grouping, not a miss. The real count check for english lives at C3/C4 (item 3), where 5 contributions → 10 items passed on all three files. |
| 11 | **registry ⟷ chapter summary** (`summary_sections.py`, `:293`) | **PASS — and it GATES for this stage** | `5 summary section(s) vs 5 registry entr(ies)`, every one anchored. English declares its sections in JSON `main_sections[]` and its registry entries are the SPINE CELLS, so this is one of the gating subjects rather than an SS-style advisory. Zero unmatched either way — no missing section, and no advisory extra. **This is the check that was added the same day and caught three real misses in its first 33-chapter sweep; here it is satisfied outright.** |

Also confirmed: no `ERROR:` row anywhere in the sweep, and no file was moved to quarantine
during either certification pass — the top's pre-compact report and this one both left all
three files live.

---

## 2 · The sweep table

Re-derived independently through `serve_plan` rather than read off the report, so the modes are
verified rather than transcribed. Floor 7 · top 12 · authored duration 40.

| X | units served | mode | drops | surrendered | note |
|---|---|---|---|---|---|
| 5 | 5 | `fill/single` | **1** | 0 | drops `B\|beyond_text` — **below floor** |
| 6 | 6 | `fill/single` | **1** | 0 | drops `B\|beyond_text` — **below floor** |
| 7 | 7 | `identity` | 0 | 0 | serves p07 whole |
| 8 | 8 | **`rescue/complete (from 10)`** | 0 | 0 | §3 |
| 9 | 9 | `fill/single` | 0 | 0 | prefix of 10 + one borrowed unit, nothing dropped |
| 10 | 10 | `identity` | 0 | 0 | serves p10 whole |
| 11 | 11 | `synthesis` | 0 | 0 | p10 complete + the standard's synthesis unit |
| 12 | 12 | `identity` | 0 | 0 | serves the standard whole |
| 13 | 12 | `identity` | 0 | **1** | 1 period (40 min) returned to the teacher's budget |
| 14 | 12 | `identity` | 0 | **2** | 2 periods returned |

**Everything inside the band [7, 12] serves complete — zero drops at every one of the six
period counts a teacher can actually land on.** That is the strongest possible reading of this
row, and it is what FULL SPINE COVERAGE bought: a library whose compacts are subsets of the
standard would have dropped somewhere in that range.

**The two drops sit at X=5 and X=6, both below the floor of 7**, which is specified behaviour —
below the lowest canonical there is no complete plan to serve. Both drop the *same* cell,
`B|beyond_text`, the last registry member, and both file it through the teacher-facing channel
rather than silently:

> *"Time budget short of the chapter's full span: `B|beyond_text` could not be scheduled — the
> material is included for you to share as guided self-study or homework."*

**Surrender above the top is declared, not swallowed:**

> *"1 period(s) (40 minutes) exceed this chapter's fullest plan and return to your budget."*

---

## 3 · X=8 is the row worth reading twice

`rescue/complete (from 10)` is Case 1b (e15). The ordinary upward serve at X=8 would take the
**prefix of the 10-unit compact** (8 units) plus a borrowed Xth unit — and that path *would have
dropped a section*, because a 10-unit plan's first 8 units have not yet reached `B|beyond_text`.
Instead the engine served the **7-unit canonical complete**, closed with the standard's synthesis
unit, and reached 8 units with **nothing dropped**.

`rescued_from: 10` names the count it rescued *from*, so the sweep shows what the trade cost:
the teacher gets the floor plan's richness rather than the 10-plan's, in exchange for complete
coverage. **That trade is the human gate's to read, not certification's** — the certifier only
proves no section was lost. Carried into C8, which inspects the X−1→X transition, and into the
gate.

It is also the sharpest confirmation available that this library is dense enough: the rescue
exists precisely so a gap between authored counts does not cost a section, and here it fires
once, at the one X that needed it.

---

## 4 · What C5 hands forward

- **No defect raised.** Nothing in the report fails, and nothing in the sweep is a defect
  requiring a repair or a re-author. The three drops-and-surrenders in the table are declared
  costs of their period counts, not faults.
- **C8 inherits X=8** (the rescue) and **X=11** (the synthesis borrow) as the two transitions
  worth reading in prose — the two rows where a served plan is not simply one authored file.
- **C6 inherits the band [7, 12] as clean**, so any coverage note it sees inside that range at
  40 minutes would be a regression, not an expected cost. Its mixed-duration requests (kumar3 at
  40/50) are the untested axis — this sweep is single-duration by construction.
- **Check 10 stays advisory and empty for english at every stage**; do not read a future
  `0 items vs 0 expected` as a miss.
