# S6 · science · middle — stage preparation sign-off

**Date:** 2026-08-07 · **Template:** `docs/testing.md` v2.6 (→ v2.7 pending, §4 below)
**Drawn class:** VIII (seed `science|middle|2026-08-02`) · **standard duration:** 45 min
**Reference pair:** SS·secondary LP v1.10 · assessment v1.7
**Landed pair:** science·middle LP **v2.1 → v2.2** · assessment **v1.3 → v1.4**

Written by Claude. Status in the tracker is set by Kumar.

---

## 0. The headline — this stage is the campaign's structural exception

S6 is not a routine carry-forward. Science·middle is the only one of the eleven
subject·stages whose lesson plan is organised by the **cognitive progression arc** rather
than by textbook sections. That difference is deliberate (teaching and its testing are
aligned to the arc), and it has two consequences the template did not anticipate:

1. **The unit-granularity serve engine cannot serve this stage.** There are no section
   anchors to do the arithmetic on, and no prefix of a canonical is a valid plan, because a
   stage is taught whole or not at all. `compile.py`'s hard read of `p["section_anchor"]`
   would have killed the first build before any certification check ran.
2. **The self-contained register cannot be ported whole**, because its forward-reference ban
   exists to protect a property this stage does not have and does not need.

Both were surfaced before any file was touched and settled by founder ruling on 2026-08-07.
The serve model is specified in **`docs/science_middle_stage_serve.md`** (new); the register
decision is in the LP changelog. **The engine work in that spec is the gating item for C1** —
P1–P5 below are complete, but S6's C-cycle cannot open until items 1–8 of its §4 land.

---

## 1. Per-item verification (testing.md §3, the Claude sign-off)

| Item | Verdict | Evidence |
|---|---|---|
| **A1** — one standard row | **PRESENT** | INPUTS 4 now reads "exactly ONE row {duration_minutes, count}: the class-standard duration (40 min for classes VI–VII, 45 for VIII) × the period count … handled downstream at serve time". Rule 6's TIME statement restated as `duration × count` (was "sum of all (duration × count) products across all period rows"); A3 gains "period_schedule: exactly one row — the class-standard duration × count (INPUTS 4)". Class bands are the master-plan calibration, not NCF's flat 40. |
| **A5 + A7** — register as ONE block | **PRESENT, TWO-BAN CUT — declared deviation** | One block after VOCABULARY, bound at Rule 6 (band text) and Rule 10 (teacher notes) by reference, never as scattered bans. Ban 1 (clock quantity) and ban 3 (calendar time) verbatim in substance. **Ban 2 (forward reference / completion) deliberately not ported** — founder ruling 2026-08-07; the block states the omission and its reason in the file rather than leaving it silent. |
| **A6** — item anchoring | **CONFIRMED, not amended; one integrity block added** | Items already carry `progression_stage`; `coverage_handoff` maps each stage to `period_numbers`. New block records the anchor is DERIVED — stage → `period_numbers` → the LAST of them — and forbids `period_ref`/`phase_ref`/any unit number. Same doctrine as science·secondary's `section_number` line (v1.2). Carrier already implements it (`aruvi_core/genon/carriers.py`, handoff-bridged family). |
| **A9** — option order | **PRESENT as removal + two lines; no arrangement sentence** | REMOVED Rule 7's item-18 prohibition ("MUST NOT place the correct answer at the same label across consecutive items; is_correct MUST be distributed across A-D…"). ADDED the v1.7 mandate line and the by-label option-reference ban. The edit script asserts `alphabetically`, `never led with` and `first word at which they differ` are all absent. |
| **P3** — Group B conversion | **APPLIED** | `phases[{minutes, description}]` → `time_bands[{minutes, activity}]` in A3, Rule 6's prose following. No `band_id` in the target shape. Script asserts no `phases[` or `"phases"` survives. `roles[]` untouched (carried, ignored downstream). |
| **P4** — history to the sidecar | **DONE** | `CHANGELOG.md` created beside both constitutions. Neither file carried an in-document version-history block, so nothing was lifted out. |
| **Cancelled amendments A2/A3/A4, X3** | **ABSENT** | None introduced. (Note: this stage's own long-standing `AMENDMENT A3`/`A4` headings are its LP JSON schema and coverage-handoff schema — unrelated to the campaign's cancelled A3/A4, and untouched.) |
| **V-rules in a constitution** | **NONE** | No registry, no anchor mandate, no INPUTS acknowledgment, no precedence line. The synthesis unit's self-containment — the one residue of ban 2 — is left to the platform brief, per §3 of the template. |

---

## 2. P5 — stage inputs

**P5.1 · The floor.** Accepted at the standing ratio, `round(0.6 × recommended_periods)`, no
override. For the pilot chapter that is `round(0.6 × 12) = 7`, matching
`floor_periods_at_standard` on the row.

**P5.2 · The registry, where the section model is non-obvious.** This is the stage the
template's P5.2 was written for, and the answer is a negative one: **science·middle has no
section registry and no cross-canonical registry of any kind.** Stage count, labels and
structure are derived freshly per generation and may legitimately differ between a chapter's
own canonicals (founder, 2026-08-07); stages therefore may never be borrowed between
canonicals. The one shared fact is the arc's terminus — Rule 1 binds every arc to the
operation named in the dissolution test sentence — and that is the only thing a borrowed
synthesis unit may assume. Recorded in full in `docs/science_middle_stage_serve.md` §1.

**P5.3 · The pilot chapter — science · VIII · ch 6, "Pressure, Winds, Storms, and Cyclones".**
Mid-book, five clean numbered sections (6.1–6.5), summary and mapping both on disk,
`placeholder: false`, `canonical_plan` present. `recommended_periods` 12, floor 7, counts
**`[12, 10, 8, 7]`** — the density rule LANDED 2026-08-07 (spec §4 item 5), so the row is final,
not provisional against a pending change. Science·middle now stands at 154 authoring runs across
its 37 chapters (was 107 under equal dispersion): +47 runs, ≈ ₹1,739.
Chose ch 6 over ch 5 (18 periods, 8 sections) on cost: it is the closest shape to the
certified SS·IX ch 3 pilot at ~₹110–145 for the library.

**P5.4 · The three test identities' profiles for class VIII.** **DONE 2026-08-07** — set up
through the app's own first-run / profile flow, which doubles as the live check of that flow.
kumar1 sections F + G at 45 min · kumar2 section M at 45 min · kumar3 section O at **60 min**.
Sections are disjoint, so X1's tenancy evidence is unambiguous; kumar3's 60 min against the
45-min class standard gives C6's mixed-duration matrix real material, and kumar3 is the
identity §4 assigns that matrix to. The profiles also still carry Social Sciences VIII/IX and
Science IX from S1–S3 — **leftover accepted by founder ruling**: it touches no science-VIII key
and clearing it would buy nothing. **P5 is green; the provisional rule is no longer needed.**

---

## 3. What was found and settled along the way

- **The `section_anchor` gap** — `compile.py` line 115 reads `p["section_anchor"]` with no
  fallback, and science·middle emits no such field. Found before any generation spend.
  Resolution: the field is not added to the constitution; the read becomes carrier-mediated
  and the stage serves at plan granularity (spec §4, items 1–3).
- **The synthesis-items question** — the founder's working assumption was that synthesis
  units carry no assessment items on SS and science·secondary. An audit of the installed
  libraries found the **opposite**: SS·VIII ch 3 anchors items to synthesis unit 12, SS·IX
  ch 3 to unit 16, and C9.2 mandates a borrowed unit bring its own items. Ruling 2026-08-07:
  keep it, and let science·middle's synthesis carry and travel with its items — consistency
  over exception. No constitution text was written.
- **Dropped-unit exports** — confirmed unchanged: dropped units and their items are rendered
  online only and omitted from exports (ARV-D-037 / e13), for this stage as for every other.

---

## 4. Template consequence (testing.md → v2.7, pending)

The S6 row's C-steps read differently and the template must say so before the C-cycle opens:
C5's checks 3/4/5 N/A, 6 adapted, 8 redefined (truncation legal only below the floor), 7's
sweep modes reduced to four; C6's request matrix loses the fill rows and gains the `K+1`
synthesis row; C7 unchanged in bans 1 and 3, with ban 2 struck for this stage; C8 has exactly
one joint to inspect; C9's remap cases collapse. §9 applies and costs nothing: **no stage
carries a signed human GATE**, so nothing re-opens.

---

## 5. Verdict

**P1, P2, P3, P4 — complete and verified. P5 — recorded, P5.4 open by design.**

The constitutional gate is clear: the stage may be **signed provisionally**. It may **not**
enter its C-cycle until the engine work in `docs/science_middle_stage_serve.md` §4 lands,
which is a new gating condition specific to S6 and has no precedent in S1–S3.

Artefacts, all in `genon/out/stage_prep_science_middle/`:
`lesson_plan_constitution_v2.1_pre.txt` · `assessment_constitution_v1.3_pre.txt` ·
`lp_v2.1_to_v2.2.diff` · `assess_v1.3_to_v1.4.diff` · `apply_s6_amendments.py`.
Plus `docs/science_middle_stage_serve.md` and the two `CHANGELOG.md` sidecars.
