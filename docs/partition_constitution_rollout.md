# Constitution rollout — what ports to the remaining subjects & stages

**REWRITTEN 2026-07-31 for the variant-canonical pivot** (filename kept for standing
references from testing.md; "partition" in the name is historical). The previous version
of this brief rolled out the partition engine's declaration layer — band ids, roles,
unit handoffs. That engine is retired and its amendments are cancelled;
`docs/variant_canonical_architecture.md` records the whole story (§1 the failure
evidence, §6a the band-layer removal). This file now carries ONLY what still ports:
the amendments that survive and the one that shrank; the V-series is carried by the
variant brief, outside every constitution (§3). SS·secondary (LP v1.10 · assessment
v1.7) is the reference pair. **§3's A9 was rewritten 2026-08-04** — option order left the
constitution at assessment v1.7 and became a pipeline stage (`genon/normalize_options.py`);
A9 is now a removal, not an arrangement rule. Read §3 before amending any assessment
constitution.

---

## 1. The hard contract (serve-era)

`compile.py` v0.5 + `serve.py` v1.1 require of every canonical, subject-agnostically:

| # | Requirement | Why |
|---|---|---|
| S1 | `result.lesson_plan.periods[]`, each with `period_number`, `period_duration_minutes`, `activity_title`, `section_anchor` | the units ARE the served atoms |
| S2 | `time_bands[]` on every period — exactly that key, each band `{minutes "a-b", activity}` | proportional scaling parses these; band_id is DERIVED positionally, never demanded |
| S3 | `section_anchor` drawn VERBATIM from the chapter's section registry, contiguous in registry order; multi-section units join with " / " | the fill ladder is string arithmetic on the registry (V2) — spelling drift breaks serving |
| S4 | every assessment item resolves to a known unit — `period_ref` (the identity), legacy `phase_ref` accepted as fallback | anchoring is unit-level; compile normalizes to `unit_ref` |
| S5 | one standard period row (A1) | variants are partitions of the demand range, not of durations |

Nothing else is declared. Roles, band ids, band refs, unit handoffs: not read.

## 2. Where the eleven constitutions stand (2026-07-31)

| Subject · stage | LP ver | Band shape | A1 | Register (A5/A7) | A9 (assess option order) |
|---|---|---|---|---|---|
| **social_sciences · secondary** | **1.10 — reference** | time_bands | ✓ | ✓ | ✓ (v1.7 — arrangement struck) |
| social_sciences · middle | **2.8 ✓ (2026-08-04)** | time_bands | ✓ | ✓ | ✓ (v2.4 — item-18 struck) |
| science · secondary | **1.1 ✓ (2026-08-05)** | time_bands | ✓ | ✓ | ✓ (v1.2 — item-18 struck) |
| mathematics · secondary | 1.0 | time_bands | — | — | — |
| the_world_around_us · preparatory | 1.2 | time_bands | — | — | — |
| science · middle | **2.2 ✓ CERTIFIED (2026-08-07)** | time_bands ✓ | ✓ | ✓ **two-ban** | ✓ (v1.5 — item-18 struck; counts made binding at C3) |
| mathematics · middle | 3.3 | phases[] → P3 | — | — | — |
| mathematics · preparatory | **1.3 ✓ (2026-08-11)** | time_bands ✓ | ✓ | ✓ | ✓ (v1.3 — removal N/A) |
| english · preparatory | 1.0 | phases[] → P3 | — | — | — |
| english · middle | 1.5 | phases[] → P3 | — | — | — |
| english · secondary | 1.0 | phases[] → P3 | — | — | — |

(Table state is 2026-07-31 except the four amended rows. The remaining seven still carry
the item-18 position prohibition A9 strikes where they have one; see §3.)

> ★ **science · middle is the structural exception — read `docs/science_middle_stage_serve.md`
> before touching it** (added 2026-08-07 at S6's prep). It anchors learning units to the
> COGNITIVE PROGRESSION ARC, not to textbook sections: no `section_anchor`, no section
> registry, no cross-canonical registry of any kind, and no prefix of a canonical is a valid
> plan (a stage is taught whole or not at all). Two consequences recorded here because they
> break the table's assumptions. (a) Its register is a **two-ban** cut — the forward-reference /
> completion ban is deliberately NOT ported, because every unit of a canonical is served with
> every other unit of that canonical, so forward reference is never wrong for anyone. Bans 1
> and 3 (clock quantity, calendar time) stand in full: duration scaling and the Calendar Purge
> are orthogonal to the serve model. (b) It serves at **plan granularity**, not unit
> granularity, which is engine work gating its C1 — do not assume the standard serve law here.

## 3. The surviving amendment set

**A1 · Period schedule = exactly ONE standard row.** Ports verbatim (40 ≤VII · 45 VIII ·
50 IX–X — the master-plan calibration bands, not NCF's flat 40). Unchanged in force;
now doubly load-bearing because every VARIANT is authored at the standard duration and
the serve engine handles all timetable variation. Ten constitutions still say "one or
more rows" (or subject-specific equivalents) and must be corrected.

**A5 + A7 · THE SELF-CONTAINED REGISTER, one block — port the v1.10 re-cut.** Re-cut
2026-07-31 on a founder challenge (with X−1 units served in canonical order, the
backward-position ban's engine justification died with the partition): every surviving
clause traces to a live mechanism. Three bans — (1) clock quantity (rule-4 proportional
scaling falsifies stated numbers silently); (2) forward reference / completion language
(X varies per teacher, so ANY unit may be terminal or precede a companion variant's
unit); (3) calendar time (Aruvi keeps no calendar — Calendar Purge doctrine, older than
the engine). Backward references are no longer forbidden; content-named continuity is
the stated best practice (the notes rule's continuity link). Port as ONE block
referenced by the notes rule and band rule; never as scattered prohibitions. Known
direct contradiction to strike: english·middle's schema comment "Transition from prior
unit; preview into next" (forward direction — still banned).

**A6 · REDUCED to a confirmation.** Items must carry their anchor unit — `period_ref`
or that subject's equivalent, copied from the LO row consumed. Verify at each stage's
prep; amend only where absent. (The v1.2-era band-level `phase_ref` is reversed —
the reversal landed at SS·secondary assessment v1.5 and stands in the live v1.7.)

**A9 · MCQ option order is NOT the model's to set.** *Rewritten 2026-08-04. The
alphabetical arrangement convention this item carried from v1.3 to v1.6 is STRUCK: it was
removed from the reference at SS·secondary assessment **v1.7** (2026-08-03, ARV-D-032)
because prose could not carry a sort — the v1.6 library came in 15 of 18 unarranged, the
correct option at A or B on 16 of 18 and never at D. Ordering is now a deterministic
pipeline stage,* `genon/normalize_options.py` *(STEP 6 of* `build_library.py`*,
subject-agnostic), gated at certification.* Scope is unchanged — all eleven assessment
constitutions — but what ports is **one removal and two lines**:

- **REMOVE** the MEMORY-item-18 position prohibition in the four files that carry it
  (SS + Science, middle and secondary). Nothing replaces it in kind.
- **ADD** the v1.7 mandate line (option order carries no meaning and is not yours to set;
  emit the four as authored; uneven letters across a chapter are coincidence, not a
  defect) and the prohibition on an option that references another **by its label**
  ("both A and B", "none of the above") — the one construction a downstream sort cannot
  reorder without rewriting.
- **NEVER re-add** the arrangement sentence, "never led with", or any rule naming a label
  position: naming arrangement at all keeps position salient to a model that should not be
  reasoning about position (founder, v1.6 and v1.7).

**Corpus-repair debt — now discharged by the pipeline:** STEP 6 normalises already-saved
SS and Science plans in place at ₹0, never shuffles, and writes the moved-item count into
`genon_canonical.repairs[]`. That count is the only remaining generation-quality signal for
this item; if it falls to zero across a stage, say so rather than assume it.

**P3 · Group B schema conversion.** Unchanged: the six `phases[{minutes, description}]`
constitutions convert to `time_bands[{minutes, activity}]` (note: no band_id in the
target shape any more — the conversion got smaller). The compiler reads exactly
`time_bands` and `activity`; the decision stands to amend constitutions, not to teach
`compile.py` an adapter.

**P4 · History to the sidecar.** Unchanged convention: amendment notes go to
`CHANGELOG.md` beside the constitution; the `VERSION` line stays in the file.

**V-series · NOT CONSTITUTIONAL (founder ruling, 2026-08-01).** The variant
requirements — V1 the variant brief (count + mandated closing span), V2 the shared
section registry (verbatim anchors, first-visit order), V3 the closing-synthesis
mandate, V4 per-variant assessment — are carried ENTIRELY by the platform-computed
VARIANT BRIEF (`genon/variant_plans.py briefs_for`, prepended to the generation
prompt) and enforced by the deterministic certifier (`genon/build_library.py`). The
brief is post-constitution and invisible to it; no constitution carries a V-rule, an
INPUTS acknowledgment, or any reference to briefs (the founder rejected even a
precedence line). This is deliberate economics: brief wording iterates at the speed
generation failures teach (the ch 3 pilot hardened it twice in one day at Rs 35 and no
cascade), while a constitutional amendment reopens every certified combo under §9.
Full text and rationale: variant_canonical_architecture.md §7.
One decision still lands at prep, in the PIPELINE not the constitution: what the
registry lists where the section model is non-obvious — English's split-chapter/spine
model needs its registry defined before its variants are authored.

## 4. Cancelled, and where the reasoning lives

A2 (band identity/anchoring), A3 (role_handoff), A4 (unit_handoff) are cancelled for
all ten un-amended constitutions; X3 (generalising `_check_declarations`) is void with
them. A8 was withdrawn on measurement before the pivot. The container-text pair-selection
finding and the wide-span analysis were partition-era engineering; they are recorded in
the architecture brief and the git history, not carried forward. Do not reintroduce any
of it: the failure evidence is variant_canonical_architecture.md §1.

## 5. Suggested sequencing

1. **A1 everywhere.** Still the cheapest, highest-leverage edit; stops new canonicals
   being authored in shapes the library cannot use.
2. **Per stage, in the campaign's combo order: A5/A7 → A6-confirm** (P3 first where
   Group B). That is the WHOLE constitutional carry-forward per stage — the V-series
   rides in the brief and never touches the files. One stage fully signed off before
   the next begins — the testing.md P-prep slot, with A2/A3/A4 struck from its
   checklist.
3. **A9 into the ten remaining assessment constitutions** — the strike-plus-two-lines form
   above, never an arrangement rule; the four item-18 files first, since their prohibition is
   known not to hold. No corpus repair to schedule: STEP 6 does it.
4. **Floor + σ per subject·stage** (founder inputs the solver needs) — set at each
   stage's prep, from the master-plan calibration.
