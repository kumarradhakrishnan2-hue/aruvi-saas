# Fitness across the range — SS · IX · Ch 3 "Atmosphere and Climate"

Cowork human-gate reading of the v2.0 library · 2026-08-03
Library: **p12 / p10 / p07** (`canonical_periods [12, 10, 7]`, basis `authored_standard`,
A = 12, C = 7, mid = ⌈19/2⌉ = 10 — equal dispersion per §0.2).
Deterministic run of record: `genon/out/library_reports/social_sciences_ix_ch03_20260803_144039.md`.

---

## Verdict in one line

**The three canonicals are pedagogically sound and the serve band [7..12] is fully covered
with zero drops and zero truncations — but the certification run that produced that verdict
was measuring against a CORRUPTED registry, and it quarantined a good plan for it.**

Do not certify yet. Three items below; only the first is structural.

---

## 1 · The blocker — one anchor, joined with `;` instead of `" / "` (V2 breach, all three files)

Every canonical in this library writes the same two-section unit as:

```
"section_anchor": "Weather and Climate; Elements of Weather and Climate"
```

V2 mandates multi-section anchors join with `" / "`, and `serve._ANCHOR_JOINER` is exactly
`" / "`. A semicolon is therefore **not split**: the string enters `section_registry` as ONE
opaque section. The registry the engine derived from the top canonical is:

| # | derived registry (WRONG) | chapter summary (TRUE) |
|---|---|---|
| 0 | Introduction to the Atmosphere | Introduction to the Atmosphere |
| 1 | Composition of the Atmosphere | Composition of the Atmosphere |
| 2 | Structure of the Atmosphere | Structure of the Atmosphere |
| 3 | **Weather and Climate; Elements of Weather and Climate** ← phantom composite | Weather and Climate |
| 4 | Seasons in India | **Elements of Weather and Climate** |
| 5 | **Elements of Weather and Climate** ← duplicate, mis-ordered | Seasons in India |
| 6 | Monsoon | Monsoon |
| 7 | Climate Change | Climate Change |
| 8 | Punjab Floods 2025: A Case Study | Punjab Floods 2025: A Case Study |

It still counts 9 entries, which is why `registry_sections: 9` passed by coincidence.
"Weather and Climate" as a standalone section **does not exist** in the derived registry, and
"Elements of Weather and Climate" is displaced two slots past its true position.

### What the corruption cost

**(a) It falsely quarantined p10.** The 14:40 report's only structural FAIL was
`ch_03_canonical_p10.json: first-visit order follows the registry`. Under the derived
registry p10's U6 (Monsoon) appears to skip phantom index 5, which p10 then "returns to" at
U9. Under the true registry p10's U9 is an ordinary **backward revisit** of Elements — legal
and welcome under §4 frontier arithmetic. Repair the joiner and **all three plans pass
first-visit order and reach the final section**:

```
p12: U1(0,0) U2(1,1) U3(2,2) U4(3,4) U5(5,5) U6(4,4) U7(6,6) U8(6,6) U9(7,7) U10(7,7) U11(8,8) U12[SYN]
p10: U1(0,0) U2(1,1) U3(2,2) U4(3,4) U5(5,5) U6(6,6) U7(7,7) U8(8,8) U9(4,4) U10(7,8)
p07: U1(0,1) U2(2,2) U3(3,4) U4(5,5) U5(6,6) U6(7,7) U7(8,8)
```

p10 is a good plan and should come back out of `backup/quarantine/`.

**(b) It corrupted the serve table at X = 8 and X = 9.** Side by side:

| X | as authored (certified table) | with the joiner repaired |
|---|---|---|
| 8 | fill from **p10 itself**, **drops "Elements of Weather and Climate"** | fill borrowed from **p07**, **no drops** |
| 9 | fill from p10, slot-X re-teaches "Elements of Weather and Climate" | **Case 1 — borrows p12's `synthesis` unit** |

The X=8 drop is a phantom: Elements was already taught in p10's U4. The X=9 fill was a
redundant re-teach standing where a whole-chapter synthesis belongs. Both are artefacts of
the joiner, not of the authoring.

**Fix:** a one-character serialization repair in all three artefacts (`; ` → ` / ` on that
anchor), then `--certify-only`. Worth a hardening pass too: `build_library.py` should
diff the derived registry against the chapter summary's section list, and the register
scanner should flag any `section_anchor` containing `;` — this class of slip is invisible to
every check we currently run.

---

## 2 · Fitness across the range (repaired registry, 50-min standard)

Floor C = 7, top A = 12. **Serve band = [7 .. 12].**

| X | serves | sittings | slot X | lender | first-exposure | drops |
|---|---|---|---|---|---|---|
| 5 | p07 | 5 | fill · Monsoon | p07 (self) | ✓ U5 first-deals s6 | 2 — Climate Change, Punjab Floods |
| 6 | p07 | 6 | fill · Climate Change | p07 (self) | ✓ U6 first-deals s7 | 1 — Punjab Floods |
| **7** | **p07** | **7** | identity | — | — | **0** |
| **8** | **p10** | **8** | fill · Punjab Floods | **p07 U7** | ✓ U7 first-deals s8 | **0** |
| **9** | **p10** | **9** | **Case 1 · synthesis** | **p12 U12** | n/a (full coverage) | **0** |
| **10** | **p10** | **10** | identity | — | — | **0** |
| **11** | **p12** | **11** | fill · Punjab Floods | p12 U11 (self) | ✓ U11 first-deals s8 | **0** |
| **12** | **p12** | **12** | identity | — | — | **0** |
| 13 | p12 | 12 | identity · surrender 1 period (50 min) returned | — | — | 0 |
| 14 | p12 | 12 | identity · surrender 2 periods (100 min) returned | — | — | 0 |

**Across the whole serve band [7..12]: complete coverage, no dropped sections, no
truncation, no defensive Case 3.** X = 5 and X = 6 sit *below* the floor — the drops there
are the honest below-floor behaviour, sourced from the lender's subsequent units exactly as
§0.4 requires, with the coverage note naming what moved to self-study.

**No jumpiness (the ARV-D-025 guarantee holds).** Every Case-2 borrow was verified to be a
**first-exposure** unit for the next-due section M in its own home plan: X=5→p07 U5, X=6→p07
U6, X=8→p07 U7, X=11→p12 U11. Each borrowed unit's only backward dependency is "the sections
before mine have been taught", which the deterministic prefix guarantees. The one cross-plan
borrow that matters — **X=8 lending p07's case-study unit into p10's 7-unit prefix** — is
clean: p07 U7 introduces the Punjab Floods case study from scratch.

The X=9 Case-1 borrow is the architecture working as designed: p10's 8-unit prefix covers the
entire registry, so slot 9 takes p12's mandated `synthesis` unit — the only prior a
whole-chapter synthesis needs is full coverage, and Case 1 guarantees it.

**Equal dispersion is validated by the table.** {12, 10, 7} produces an identity serve at
three of six band positions and a single-unit fill at the other three. No gap in the band
needs a fourth canonical.

---

## 3 · Assessment composition under mixed serves — worth a founder decision

Not a gate, but the mixed plans read oddly:

| X | items served | flagged unscheduled | coverage |
|---|---|---|---|
| 7 | 18 | 0 | complete |
| **8** | **20** | **7 (35%)** | **complete — 0 drops** |
| **9** | **19** | **5** | **complete — 0 drops** |
| 10 | 18 | 0 | complete |
| 11 | 18 | 1 | complete |
| 12 | 18 | 0 | complete |

At X=8 the teacher gets a plan that says *every section is covered* alongside an assessment
where 7 of 20 items carry a scheduling note. The cause is that anchoring is **unit-level**
(R5), so when p07's U7 substitutes for p10's U8, the items anchored to p10's U8/U9/U10 are
orphaned even though **the section they test was taught** by the borrowed unit. Complete
coverage and 35% unschedulable items is a contradictory artefact to hand a teacher.

A section-level fallback for re-anchoring — when a borrowed unit covers the same section as
the orphaned item's anchor unit, re-anchor rather than flag — would resolve it without
touching the selection engine. Founder call; recorded here, not fixed.

---

## 4 · Register breaches — real, outstanding, unrelated to §1

Four hits, all `time_bands` prose, none in p07:

- **p12 U4** `30-44` [clock] — "…posed for **two minutes** of paired oral sharing."
- **p12 U8** `0-8` [clock] — "Pairs discuss for **three minutes** and take one response each side."
- **p12 U11** `30-44` [clock] — "Groups of four discuss for **five minutes** and prepare a two-sentence position."
- **p10 U2** `40-50` [forward] — "…**previewing the climate change thread** without naming a future topic."

These make serving *wrong*, not impossible, and are repairable in place (§ certification
doctrine, 2026-08-02). **`genon/repair_register.py`'s declared edits are stale** — its
`ch_03_canonical.json` U1 entry now fails its own assertion ("declared text not found — the
artefact has changed since this repair was written"), because these canonicals were
regenerated at 14:19/14:26/14:34. The declarations need rewriting against the new artefacts.
Do not hand-edit.

**Item counts: clean.** All three carry 18 items and match the SS·secondary assessment v1.6
mandate exactly (Central 5 / Substantive 3 / Present 2) — no repeat of the p07/ARV-D-019
short-count.

---

## 5 · What to do, in order

1. Repair the `; ` → ` / ` anchor join in all three artefacts (serialization fix, declared not hand-edited).
2. Restore `ch_03_canonical_p10.json` from quarantine — it was failed by the bug in §1.
3. Rewrite `repair_register.py`'s ch 3 declarations against the current artefacts; apply the four fixes.
4. Re-run `python3 genon/build_library.py social_sciences ix 3 --certify-only`; expect a clean sheet and the §2 table as the adaptation table of record.
5. Harden: registry-vs-summary diff in certification, and a `;`-in-anchor check in the scanner.
6. Founder call on §3 (section-level re-anchoring for orphaned items in mixed serves).

The human gate stays open on the borrowed seams themselves — this report certifies the
*arithmetic* of the choice set, not the prose of the four borrowed slot-X units. Those still
want a read.
