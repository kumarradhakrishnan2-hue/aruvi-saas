# C4 + C5 — the_world_around_us · V · ch 5 *Our Vibrant Country*

**Library:** `[16, 13, 10]` at 40 min · engine 19 · LP v1.4 / assessment v1.4
**Report read:** `genon/out/library_reports/the_world_around_us_v_ch05_20260812_093902.md`
(the newest — post the ARV-D-119 unit permutation and the ARV-D-120 backfill)
**Date:** 2026-08-12 · **Template:** testing.md v2.9

**Both PASS.** C4 pays a debt that has been open since 2026-07-10; C5 is ALL PASS with one
advisory that is noise on this stage and one result worth reading as a finding rather than a tick.

---

# C4 · MEMORY.md "AMENDMENTS TO BE TESTED", live

Three items apply to TWAU·preparatory, two are recorded closures, and fourteen are N/A. The list
has grown to **19** items since the C4 table in testing.md was written (item 19, the curly-quote
narration format, landed 2026-08-11); it is included below and is N/A here.

| # | Item | Applies? | Verdict | Evidence from the live artefacts |
|---|---|---|---|---|
| **1** | `guide.{TYPE}` nesting (SS + **TWAU**) | **YES** | **PASS** | **The headline, and the debt this stage owed.** TWAU assessment v1.3 (2026-07-10) mandated `guide.{question_type}` nesting and was validated **synthetically only** — the saved plans were migrated in place and the constitution text had never been through a live run. Both SS stages have since had one (113 items); **TWAU was the last of the three still owed.** Measured across the whole library: **39 items · 39 nested under exactly their own `question_type` key · 0 FLAT placements · 0 key mismatches · 0 missing mandated fields.** MCQ `what_each_option_reveals` is keyed to **exactly the non-correct labels** on all 7 MCQs — never the correct one. The constitution text now has a live run behind it, and MEMORY item 1 can be closed for all three of its subjects. |
| **3** | Constitution exact item counts (all subjects) | **YES** | **PASS** | TWAU's count rule is not a per-competency slate but assessment Rule 2's 1:1: *"For each period … exactly one assessment item. Total items = total periods. No more, no less."* All three files satisfy it exactly — 16/16, 13/13, 10/10 — with `period_ref` covering `1..N` with no unit doubled and none skipped. C5's advisory block agrees (`16 vs 16`, `13 vs 13`, `10 vs 10`). **Note this is a different shape of check from S1's**, where counting passed but *slot type* resolution failed (ARV-D-028): TWAU mandates no per-competency slate, so there is no slot to mis-resolve, and the type mix is governed by Rule 3's indicative guidance rather than a mandate. |
| **6** | Time as a duration vector | closure | **CLOSED BY DESIGN** | Recorded, not tested. A1 fixes exactly ONE standard row and the serve engine owns every timetable variation (proportional per-unit scaling + weekly dispersion). There is nothing for a constitution to receive. Confirmed on the artefacts: `period_schedule` is `[{40,16}]`, `[{40,13}]`, `[{40,10}]`. Do not reopen. |
| **7** | `Period.approach` — empties acceptable | **YES**, as the positive half | **PASS** | The item's pre-warm check is *"maths-prep and SS empty is the question; confirm every other subject·stage carries one."* TWAU is squarely in the "every other". Measured on all three files through the port: **0 empty across all 39 units**, and every value is **SPELLED OUT** — Observe and Record · Hands-on Investigation · Discussion and Connection · Create and Express · Reflect and Act. **Zero acronyms leaked** (`O&R`, `HI`, `D&C`, `C&E`, `R&A` never reach `Period.approach`), and **zero off-taxonomy values** — so the ARV-D-043 caveat SS·middle added (*"populated ≠ valid — an approach no Pedagogy document contains"*) does not arise here: TWAU's five modes are a closed set fixed in LP Rule 3 with an NCF §7.4 citation each, so "populated" and "valid" are the same question. |
| **18** | MCQ correct-answer position spread | closure | **CLOSED BY THE PIPELINE** | Recorded, not tested. The position prohibition was N/A at this stage's P2 (this file never carried it) and ordering is deterministic in `normalize_options.py` (STEP 6). There is no spread to check and no convention to check either. The generation-quality signal is STEP 6's own line, read on the **first** pass of the fresh library: **`options arranged: 11 of 11 item(s) re-ordered`** — i.e. the model arranged none of them unaided, which is exactly what the design assumes. |
| 2, 4, 5, 8, 10, 11, 12, 13 | English items (keyed reveals · split chapters · task_density · FILL_IN/MATCH · named referenced word · homework `(p.NN)` · FILL_IN dedup · narrowed A/B ban) | no | **N/A** | English only; owed by S9–S11. |
| 9 | The Jul 12–13 constitution-edit wave | no | **N/A** | Checked against the item's own file list: it names english (all three assessment files) and the other stages in that batch. **No TWAU file appears in it** — `grep -i "world_around\|twau"` over the item returns nothing. |
| 14, 15, 16 | `number_line:` stimulus · homework `book_ref` · structured `inclusivity` | no | **N/A** | Mathematics only. Worth noting TWAU's LP has **no `homework` field at all**, so item 15's family of checks has no surface here. |
| 17 | SS·middle `teacher_notes` | no | **N/A** | Social Sciences middle only. |
| **19** | The curly-quote narration format (5 LP constitutions, 2026-08-11) | no | **N/A** | Added after the C4 table in testing.md was written. It names maths middle/prep and english prep/middle/secondary; **TWAU's LP is not one of the five** — it has no `book_ref ("brief")` construction and so never carried the JSON quote hazard. |

**C4 verdict: PASS.** No item fails; no defect opens. **MEMORY item 1 is now fully discharged** —
SS·secondary (2026-08-03), SS·middle (2026-08-04) and TWAU (today) each have a live run behind the
`guide.{TYPE}` mandate, and the item's own text ("**Still owed: TWAU** (v1.3) alone") can be closed.

---

# C5 · the certification report

**ALL PASS.** Each check as implemented in `genon/build_library.py::certify` — cited, not
re-specified.

| # | check | result |
|---|---|---|
| 1 | library complete vs `canonical_plan.counts` | **PASS** — `[ch_05_canonical, _p13, _p10]` vs `[16, 13, 10]`; `basis authored_standard`, registry 6 sections |
| 2 | every file compiles (`compile_stream` v0.5) | **PASS** — implicit in the run reaching certification; `serve granularity: unit · section axis: True`, which is this stage's declaration and confirms the P5.5 mediation is being read |
| 3 | anchors verbatim in the top registry | **PASS ×3** — the check that matters most here, since TWAU's registry token is **prose** |
| 4 | first-visit order follows the registry | **PASS ×3** |
| 5 | coverage reaches the final registry section | **PASS ×3** (standard: before the synthesis unit) |
| 6 | synthesis-anchor gate | **PASS ×3** — the standard closes with it and carries the marker nowhere else; **neither compact uses it** |
| 7 | serve sweep, floor−2 → top+2 | **PASS** — 11 rows, X = 8…18, every one producing a mode with no exception raised |
| 8 | no defensive truncation | **PASS ×11** — choice set non-empty at every X |
| 9 | register clean (`register_scan.py`) | **PASS ×3** — **0 ban hits**, and the scan is proven to have *reached* the text: 63 / 52 / 40 bands read plus every `activity_title` and `teacher_facilitation_note` |
| 9a | MCQ options in arrangement order | **PASS ×3** — proves STEP 6 ran. First-pass count `11 of 11 re-ordered` (the `0 of 11` on this re-run means only that nothing was left to move) |
| 10 | item counts per competency — **ADVISORY** | reports 16/16, 13/13, 10/10 against a **derived** basis (`expected {}` — no constitution row, since TWAU mandates no per-competency slate). No miss to carry into C4. |
| — | quarantine empty for this chapter | **PASS** — `find backup/quarantine -name "*.json"` returns nothing at all; the three directories present (`mathematics`, `science_ix_ch08`, `social_sciences`) hold no files |

## The sweep, read rather than transcribed

```
X     8     9    10    11    12    13    14    15    16    17    18
mode  f/s   f/s  ID    f/s   f/s   ID    SYN   SYN   ID    SUR   SUR
```
`ID` identity · `f/s` fill/single · `SYN` synthesis borrow · `SUR` surrender
(floor 10 · counts 16, 13, 10)

**Two things in this sweep are worth more than a tick.**

**(a) Coverage is 6/6 at EVERY X in the band — including below the floor — with zero declared
drops.** Not one row carries a `-Ns` drop count, a `dropped_units` entry, or a missing section.
This is the direct answer to the pilot lesson C5 quotes (*"the first 7-period variant of ch 3
silently DROPPED a section with no coverage note; the first-visit check caught it, the serve sweep
did not"*). Here neither check has anything to catch, and the reason is structural rather than
lucky: 6 sections against a lowest canonical of 10 units means a prefix of p10 reaches five
sections on its own, and the first-exposure choice set (§0.4) fills slot X with the unit that
FIRST deals the sixth. **X = 8 and 9 sit below the floor and still teach the whole chapter.**

**(b) Assessment does not thin anywhere in the band.** Items track units 1:1 at every X — 8 items
at X=8, 11 at X=11, 15 at X=15. Contrast **ARV-D-116** at maths·preparatory, where X=12/13 gave 20
items against X=11's 33 and two taught sections carried none. TWAU's Rule 2 1:1 mandate makes that
failure mode arithmetically unreachable, which is a real property of this stage and not an accident
of this chapter.

The two `SYN` rows carry the expected note (*"Every section is covered; the closing sitting draws
the chapter together"*) and the two `SUR` rows return the surplus honestly (*"1 period(s) (40
minutes) exceed this chapter's fullest plan"*). Above the top the engine serves 16 and declares the
remainder — a real answer, not a refusal.

## The one advisory, and why it is noise here

> `ADVISORY: 15 unit(s) wear a section label the handoff does not route items through`

**Read it as noise on this stage, and do not act on it.** It is a HANDOFF-FAMILY check — written
for stages where an item reaches its unit through `coverage_handoff.period_numbers` — firing on an
**item-self-sufficient** stage (8-rule row 8), where routing is by `period_ref` off the item and the
handoff is not in the path at all. Every unit does carry an item: `period_ref` covers `1..N` with
**zero orphans** on all three files. The advisory's own warning (*"do NOT extend `period_numbers`
to fix this"*) is the right instinct pointed at the wrong stage. Worth a small gate-side fix
eventually — suppress it where `carriers.item_anchor_family() == "item"` — but it gates nothing and
costs nothing today.

**C5 verdict: PASS.** Report says ALL PASS; quarantine empty.
