# S2 · social_sciences · middle — stage preparation sign-off

**Date** 2026-08-04 · **Pilot class VIII** · **Pilot chapter 3, *The Rise of the Marathas***
(16 units × 45 min, 11 registry sections)

> ⚠️ **The recorded draw was VII, not VIII** (testing.md §1, seed
> `social_sciences|middle|2026-08-02` → `vii`). The founder is running **VIII**. That is allowed
> — but testing.md's own rule is that a pick nobody can reproduce is a preference, not a sample,
> so the **override needs a recorded reason** in the tracker beside the original draw. Two good
> ones are available if they are the actual reason: VIII is the only middle class on the **45-min**
> band (VI–VII are 40), and it is the class with the known content gap (14 mappings, 7 summaries).
> The constitutional work in P1–P4 is **stage-level and unaffected** — SS·middle covers VI/VII/VIII.

**Scope** P1–P4 + the [Claude] stage sign-off (done) · P5 (recorded below, **P5.4 open**) ·
C1 has already been RUN — and it **failed certification**; see "C1 status" below.
The stage is **not signed**.

**Reference pair read live, this session:** SS·secondary LP **v1.10** · assessment **v1.7**
(not v1.5 — see the P2 finding).

**Files amended (live, in place):**

| File | Before | After |
|---|---|---|
| `data/content/constitutions/lesson_plan/social_sciences/middle/lesson_plan_constitution.txt` | v2.7 | **v2.8** |
| `data/content/constitutions/assessment/social_sciences/middle/assessment_constitution.txt` | v2.3 | **v2.4** |

**Artefacts** (all in `genon/out/stage_prep_ss_middle/`): pre-amendment copies
`lesson_plan_constitution_v2.7_pre.txt` · `assessment_constitution_v2.3_pre.txt`; diffs
`lp_v2.7_to_v2.8.diff` (73 lines) · `assess_v2.3_to_v2.4.diff` (22 lines); changelog sidecars
written beside each constitution.

---

## Per-item verdict

| Item | Verdict | Evidence |
|---|---|---|
| **A1** — exactly ONE standard period row | **PRESENT** | INPUTS 4 ported verbatim from v1.10 (class-standard duration 40 ≤VII · 45 VIII · 50 IX × count); A1 preamble gains `period_schedule: exactly one row`; schema comment `integer — the class-standard duration`; INTEGRITY TIME restated as `duration × count` / `total unit count = count`, replacing the Σ-over-rows form. The old "one or more rows" is gone. |
| **A5 + A7** — the self-contained register, ONE block, v1.10 three-ban re-cut | **PRESENT** | Single block after VOCABULARY, headed `THE SELF-CONTAINED REGISTER (binds Rules 10 and 13)`, ported verbatim: clock quantity · forward reference/completion · calendar time, plus the "backward continuity is welcome" closing line. Not scattered: Rules 10 and 13 each reference it (`MUST NOT breach THE SELF-CONTAINED REGISTER`) rather than restating bans. Rule 13's is prohibition 4, added beside — not replacing — its existing padding ceiling. |
| **A6** — items carry their anchor unit | **PRESENT, no amendment needed** | `period_ref` is already an identity: Rule 6 mandate, integrity constraint 4, A1 schema (length-one array). `grep -c phase_ref` = **0** in both middle files — the reversed v1.2 band-level anchoring was never here and was not introduced. |
| **A9** — MCQ option order | **PORTED IN ITS CURRENT FORM, DEVIATES FROM THE TEMPLATE** — see finding 1 | Rule 7 mandate gains v1.7's "Option order carries no meaning and is not yours to set…"; prohibitions numbered, new prohibition 2 bans by-label references. The MEMORY-item-18 position prohibition is **struck**, as the template requires. |
| **P3** — Group B schema conversion | **N/A (Group A)** | `grep -c "phases\["` = 0; `grep -c '"description"'` = 0; the A1 schema emits `time_bands[{minutes, activity}]`. Nothing to convert. |
| **P4** — history to the sidecar | **DONE** | `CHANGELOG.md` created beside each amended file. Neither constitution carried an in-file history block, so nothing was lifted out; both keep their `VERSION` line. Pre-v2.8/v2.4 history is honestly marked as unrecorded (git only), with the known landmarks named. |
| **No cancelled amendment crept in** | **CLEAN** | `grep` for `band_id`, `band_refs`, `role_handoff`, `unit_handoff`, `Amendment A3`, `Amendment A4` across both files: **zero hits**. |
| **No V-rule in a constitution** | **CLEAN** | No mention of the variant brief, section registry, closing-synthesis mandate, per-variant assessment, or any precedence line. The V-series stays in `variant_plans.briefs_for`. |
| **No pedagogical rule changed** | **CONFIRMED** | The LP diff touches only: VERSION, VOCABULARY register line, the new register block, INPUTS 4, Rule 10's continuity phrasing + register reference, Rule 13's new prohibition 4, the TIME integrity line, and two A1 schema comments. Rules 1–9, 11, 12, the edge model, A2, and every field in A1 are byte-identical. The assessment diff touches only VERSION and Rule 7's order clause — counts (Rule 4), selection (Rule 5), guide layer (Rule 9), and the A1 schema are byte-identical. |

---

## Findings the founder should rule on

**1. The template's A9 text is stale; the reference struck it yesterday.** `docs/testing.md` v2.4
§3 and `partition_constitution_rollout.md` §3 both still specify A9 as the alphabetical
arrangement convention ("arranged alphabetically from the first word at which they differ …
correct answer never led with"), and both name the reference pair as **assessment v1.5**. The
live SS·secondary assessment is **v1.7**: v1.6 (2026-08-02) removed "never led with", and v1.7
(2026-08-03, ARV-D-032) **struck the arrangement sentence entirely** — the sort moved into
`genon/normalize_options.py`, STEP 6 of `build_library.py`, which is subject-agnostic and gated
at certification. Porting the template's wording into SS·middle would have put the constitution
in direct contradiction with the pipeline stage that enforces it. **I ported v1.7's form.** Two
consequences to accept or reverse: (a) SS·middle v2.4 is what SS·secondary v1.7 is, not what
testing.md described; (b) testing.md §3 and the rollout brief §3 needed the same correction
before S3 (science·secondary) is prepared — otherwise the next nine stages inherit the struck
sentence.

> **RESOLVED, same session (founder instruction: "remove stale A9 as sorting now handled at
> normalize_options.py").** The docs are corrected: `docs/testing.md` → **template v2.5**
> (P2's A9 rewritten as one removal + two lines with an explicit ban on re-adding any
> arrangement rule; reference pair now LP v1.10 · assessment v1.7; C13's item 18 reads "closed
> by STEP 6"; §3 stage table and §11 execution order carry S2's landed versions; the [Claude]
> sign-off checklist now tests that no arrangement sentence came back). `partition_constitution_rollout.md`
> → §3's A9 block rewritten the same way, header reference pair corrected, §2 table and §5
> sequencing updated, corpus-repair debt marked discharged by STEP 6.
> `variant_canonical_architecture.md` §7's carry-forward list, `CLAUDE.md` §3's version line, and
> the MEMORY.md item-18 instruction ("must receive A9 in this v1.6 form") are all annotated or
> struck. §9 does not fire: no stage is certified, so nothing re-opens.

**2. "handled downstream at partition time" — ported verbatim, and it names a retired engine.**
A1 was to port verbatim, so INPUTS 4 in SS·middle now carries v1.10's closing clause, which
still says *partition time*. The deterministic partition engine was retired 2026-07-31; the
sentence should read *at serve time*. I did not unilaterally reword a verbatim port. It is
harmless to generation (the clause is descriptive) but it is wrong, and it will propagate to all
ten remaining constitutions. Suggest a coordinated one-word fix across SS·secondary v1.10 and
SS·middle v2.8 in the same edit, both as a patch version.

**3. Rule 9's `pedagogical_approaches` is live at v2.7 but has never been generated at this
stage.** MEMORY.md line 115 expects it to populate at SS·middle's own C4. Not a prep item —
flagged so C4 checks the Overview "Pedagogy" row actually fills for VII.

---

## P5 — stage inputs (class VIII, ch 3)

**P5.1 Floor — ACCEPTED at the standing ratio, unchanged.** `round(0.6 × 16) = 10`; the row
carries `floor_minutes: 432.0`, `floor_periods_at_standard: 10`. Equal dispersion over [10, 16]
gives A−C = 6 ≥ 4 → `{16, ⌈26/2⌉=13, 10}`, and the row's `canonical_periods` is exactly
`[16, 13, 10]`. No per-chapter override; §0.7's open-dial flag stands.

**P5.2 Section registry — no non-obvious decision; SS is section-anchored from the summary.**
The authored registry is **11 sections**, in first-visit order, plus the reserved token:

1. Who are the Marathas? · 2. Foundation of Maratha Power and the Rise of Chhatrapati Shivaji ·
3. The Marathas after Chhatrapati Shivaji · 4. Maratha Administration — Civilian administration ·
5. — Military administration · 6. — Maritime supremacy · 7. — Judicial system and Trade networks ·
8. Cultural Revival · 9. The mighty Maratha women · 10. In focus: Thanjavur · 11. The Maratha
legacy · **+ `synthesis`** (reserved; on the standard canonical only).

Note the four-way split of "Maratha Administration" into its own sub-anchors — that is a
registry *choice*, and it is the reason the sweep has room to fill at X = 11/14. It certified
clean (anchors verbatim, first-visit order, coverage complete before synthesis), so it stands;
recorded here because §7's brief-composed registry is where such choices live.

**P5.3 Pilot chapter — CONFIRMED.** `data/content/chapters/social_sciences/viii/` has both
`ch_03_summary.txt` and `ch_03_mapping.json`. The `master_plan.json` row is
`placeholder: false`, `recommended_periods: 16`, `standard_duration_minutes: 45`, and the
`canonical_plan` is **finalized** — `provisional: false`, `basis: "authored_standard"`,
`registry_sections: 11`, `authored: [16, 13, 10]`.

**P5.4 Three test identities — OPEN (amber).** All three still carry S1's leftover profile:
`kumar1` SS **IX** A/B · `kumar2` SS **IX** C/E · `kumar3` SS **IX** A/Y. They must be rebuilt
for **VIII**, through the app's own first-run / profile flow (the setup doubles as a live check
of that flow), with different sections per identity and one longer duration alongside the 45-min
standard so C6's mixed-duration matrix has something real. Provisional sign-off is permitted with
only P5.4 open (founder ruling 2026-08-02); **C6 is the hard stop.**

---

## C1 status — the library was BUILT, and it did NOT certify

`genon/out/library_reports/social_sciences_viii_ch03_20260804_163741.md`, run 16:37 today.
Three canonicals installed at `[16, 13, 10]`; **₹149.28** across the three calls
(₹54.73 + ₹49.97 + ₹44.58, `runtime_data/token_log.csv`). Quarantine is empty.

**What passed:** library complete · the standard closes with the mandated `synthesis` unit and
the token appears nowhere else · every anchor verbatim in the registry, first-visit order, full
coverage before synthesis, in all three files · MCQ arrangement gate on all three · the serve
sweep X = 8…18 with no defensive truncation (`{8: fill −2s, 9: fill −1s, 10: identity, 11: fill,
12: synthesis, 13: identity, 14: fill, 15: synthesis, 16: identity, 17–18: surrender}`) · STEP 6
moved **41 of 41** items.

**What failed — 7 register ban hits, and the cause is an ordering breach:**

| File | Hits |
|---|---|
| `ch_03_canonical.json` | 3 × forward reference (U2 "a preview of the next unit's content", U6 "setting up … in later units", U7 "navy addressed in the next unit") + 3 × clock quantity (U7 "for four minutes", U9 "for five minutes", U16 "circulates for three minutes") |
| `ch_03_canonical_p10.json` | 1 × clock quantity (U4 "discuss in pairs for two minutes") |
| `ch_03_canonical_p13.json` | clean |

**The artefact records `"constitution": "LP v2.7 / assessment v2.3"`** — the library was authored
at 16:10–16:37, and the P1–P4 amendments landed at 17:39. So it was generated **before** the
stage's constitutional work, against a constitution that **did not contain the register at all**.
That is precisely the ordering rule §3 exists to prevent, and the failure mode is the predicted
one: the model was never told the three bans, so it broke two of them.

**Also advisory (does not gate):** `ch_03_canonical_p13.json` carries 19 items vs 20 — C-9.1
(Present) has 1 where its siblings have 2. ARV-D-019 says generation variance is accepted by
default and a hand back-fill is forbidden; the only fix is regeneration, and that is a cost call.

**The choice is yours, and it is not the 2026-08-02 lottery case.** That ruling ("regenerating is
a lottery — repair in place") was made when SS·IX ch 3 breached a register the constitution
**stated in terms**. Here the constitution was silent, so a run under v2.8 is not a re-roll of the
same distribution — it is the first roll with the rule present, and it is the only thing that
would actually prove the ported register block works for SS·middle.

- **Regenerate under v2.8 · v2.4** — ordering-rule-correct, exercises the amendment live, also
  re-rolls the p13 count miss. ~₹150 and ~10 minutes.
- **Repair in place** — `genon/repair_register.py` with 7 declared (old → new) pairs, then
  `build_library.py --certify-only`. ₹0. All 7 are trailing-clause deletions or a number-to-kind
  swap, exactly the shape the tool was built for. But the library stays authored under the
  superseded pair, which needs a recorded founder waiver, and the v2.8 register block goes into
  the campaign never having been generated against.

**Then:** record the class-override reason and the stage row in `docs/testing_tracker.html`, and
the C-cycle proper opens at C2.
