# CHANGELOG — Lesson Plan Constitution · Mathematics · Secondary Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).
Nothing in this file is read at generation time.

---

## v1.2 — 2026-08-08 · Rule 12 · `period_numbers` = the units that TEACH the section

**Founder ruling, from the maths·IX ch 4 pilot.** Not a carry-forward item and not part of the
P-step set — a defect found at C1 and fixed at its cause. **No pedagogical rule changed:** the
diff touches the VERSION line, Rule 12's mandate sentence, A4's `period_numbers` comment, one
integrity constraint, and the footer.

Rule 12 said *"a section spanning several periods is ONE entry whose period_numbers lists them
all."* `carriers.items_by_handoff` anchors an item at the **LAST** unit in that list, on the
2026-08-05 rationale that "an item tests its section's whole implied_lo, so it becomes available
only when the section COMPLETES: if the class was not taught all of it, it cannot be tasked on
any of it." Applied to a **revisit** — a unit that anchors a section but adds nothing to its
outcome — the old wording goes past that rationale and costs questions:

- **p11, sec#1 (4.1):** taught at U1, "revisited" at U10/U11 — which are whole-chapter
  consolidation and deliver nothing of the row's single LO ("verify the consecutive-square
  invariant … express the general pattern with n−1, n, n+1"). `[1, 10, 11]` → the Introduction
  item anchors at U11 and vanishes at X=9 and X=10. **This is the case the amendment is for.**
- **top, sec#1:** lists `[1]` alone and its item survives at every X where U1 is served. The
  same model produced both behaviours on one chapter, so this was variance, not policy — which
  is why it needed a rule rather than a repair.

**One case explicitly NOT covered, corrected after checking the LOs.** The top's `sec#6 (4.6) =
[6, 13]` looks like the same defect and is not. The row carries **two** LOs and each unit
delivers one — U6 "Splitting the Middle Term" delivers the factorising LO, U13 "Proving and
Justifying" delivers the proof-construction LO. Both are teaching units, so `[6, 13]` is
**correct under v1.2 and stays**. Its two 4.6 items do still vanish at X=12/13, but the cause is
different: **anchoring is per-SECTION while outcomes are per-LO**, so LO1's item anchors at U13
as well, even though U6 taught it. v1.2 does not address that and must not be read as doing so;
it is recorded as an open item in the S4 sign-off.

So the field is narrowed to what the anchoring rule actually needs. A section introduced early
and **completed** later still lists both units: the later one is a teaching unit and the item
rightly waits for it. Only units that add nothing to the outcome are excluded.

**Deliberately NOT changed:** the anchoring rule itself (last listed unit), Rule 6's one-or-two
LOs, Rule 1's section anchoring, and the renderer. Display groups by `section_anchor` and looks
the title up with an **anchor fallback** (`ho_by_period.get(pn) or ho_by_ref.get(key)`), so a
narrower `period_numbers` cannot blank a group label — proven by the top canonical, whose
U10/11/12 are already absent from every list and still render as a group.

**Consequence for the existing library — one row, not two.** ch 4 was authored under v1.1, so
this is the ordering breach testing.md §3 warns about (amending after authoring). Audited against
the LOs rather than by position:

| file | multi-unit rows | verdict under v1.2 |
|---|---|---|
| `ch_04_canonical.json` | `sec#6 [6,13]`, `sec#7 [7,8]` | **compliant** — 2 LOs each, one per unit |
| `ch_04_canonical_p11.json` | `sec#1 [1,10,11]`, `sec#7 [7,8]` | `sec#7` compliant; **`sec#1` NON-COMPLIANT** |
| `ch_04_canonical_p08.json` | none | **compliant** |

So the exposure is a single row: p11's `sec#1` should read `[1]`. Founder call on the remedy —
re-author (~₹106), a declared repair, or a recorded waiver as S2 took on 2026-08-04. Recorded in
the S4 sign-off, not decided here.

Artefacts: `genon/out/stage_prep_mathematics_secondary/` —
`lesson_plan_constitution_v1.1_pre.txt`, `lp_v1.1_to_v1.2.diff`,
`apply_s4_rule12_teaching_units.py` (asserts exactly-one on every edit and fails if the
superseded wording survives).

---

## v1.1 — 2026-08-08 · S4 stage preparation (P1)

The genon constitutional carry-forward from the SS·secondary v1.10 reference. **No
pedagogical rule changed** — the diff touches the VERSION line, the vocabulary register,
the new register block, INPUTS 4, Rule 9's prohibition list, Rule 10's continuity phrasing,
Rule 10's prohibition, two integrity lines and two A3 schema comments. Rules 1–8, 11, 12,
Amendment A4 and every period field are byte-identical.

- **A1 — the period schedule is exactly ONE standard row.** INPUTS 4 was "one or more rows
  of {duration_minutes, count}"; it is now one row at the class-standard duration — **50 min
  at this stage** — × the period count. Every canonical is authored at the standard duration and
  the serve engine handles all timetable variation, so a multi-row input has no meaning any
  more. The TIME integrity constraint is restated as `duration × count` rather than a sum
  over rows; the A3 schema comment names the standard duration and a new field constraint
  states the one-row rule where the schema is read.
  - Deviation from the verbatim port, declared: the reference's closing clause reads
    "handled downstream at **partition time**". The deterministic partition engine was
    retired 2026-07-31, so this file says **serve time** — the same correction S3 made.

- **A5 + A7 — THE SELF-CONTAINED REGISTER, as ONE block.** Added after VOCABULARY in the
  v1.10 three-ban re-cut: (1) no clock quantity, (2) no forward reference or completion
  claim, (3) no calendar time — plus the closing line that backward continuity is welcome
  when carried by naming the content rather than a unit's position. Bound at Rule 9
  (prohibition 6, teacher-facing text and band activity) and Rule 10 (teacher notes) by
  reference, never restated as scattered bans.
  - Deviation from the verbatim port, declared: the reference's illustrative strings are
    Social Sciences content (a Vedic continuity link, "having covered all four"). Those are
    substituted with mathematics ones — "a quick individual calculation", "an extended
    derivation", "having covered all three identities", "Having established the expansion
    of a binomial product, …". The three bans and the closing rule are verbatim in
    substance.
  - Consequential edits: VOCABULARY dropped its positional cross-reference examples
    ("the previous unit", "this unit") and gained the "session" exclusion; Rule 10's
    continuity bullet is now position-free, naming the content built on; and A3's
    `teacher_notes` schema comment, which echoed the OLD framing verbatim
    ("recap-and-connect"), now reads "continuity by content not position" — pointing at the
    rule rather than restating a framing that no longer exists, as science·secondary's A3
    comment does. All three follow the reference; the old wording instructed exactly what the
    position doctrine now discourages.

- **A6 — item anchoring, stated as DERIVED.** Mathematics secondary's assessment is
  anchored per SECTION, not per unit: Rule 7 lets a section span several periods, and the
  handoff (A4) carries `section_number` alongside `period_numbers`, so there is no single
  unit for the model to name. A new integrity line records that the platform resolves an
  item's anchor unit from its `section_number` through the handoff's `period_numbers`, and
  forbids the model emitting `period_ref`. This is the subject's equivalent of the
  reference's A6, not an adoption of the reference's field — the same shape science·secondary
  landed at v1.1 (founder ruling 2026-08-05: derive the link, never demand it).

- **P3 — N/A.** Group A: the schema already emits `time_bands[{minutes, activity}]`; no
  `phases[`, `"phases"` or `band_id` anywhere in the file.

- **Two residues disclosed, deliberately NOT fixed.** Both are inert, and both are shared with
  science·secondary v1.1 and science·middle v2.2 — patching mathematics alone would put four
  signed stages out of step for no gain. (a) A4's `period_duration_minutes` comment still reads
  "if mixed across this section's periods, the most common"; under one standard row nothing can
  be mixed. (b) INPUTS 4 names the bands "40 ≤VII · 45 VIII · 50 IX" verbatim from the
  reference, in a constitution whose grades are `ix · x`, where testing.md P1 writes the band as
  "50 IX–X". Practically inert — step 0.6 records that class X has no content in any subject —
  but if the wording is to change it should change in the REFERENCE and be ported, not be
  patched per stage.

Artefacts: `genon/out/stage_prep_mathematics_secondary/` —
`lesson_plan_constitution_v1.0_pre.txt`, `lp_v1.0_to_v1.1.diff`,
`apply_s4_amendments.py` (the reproducible edit script; every edit asserts exactly-one
occurrence, and the run ends on guard assertions for the struck arrangement strings).

---

## v1.0 — pre-2026-08-08

The stage's original constitution. Its history before v1.1 was never kept in a sidecar and
is not reconstructed here; git is the record. The file carried no in-document version-history
block, so nothing was lifted out of it by P4.
