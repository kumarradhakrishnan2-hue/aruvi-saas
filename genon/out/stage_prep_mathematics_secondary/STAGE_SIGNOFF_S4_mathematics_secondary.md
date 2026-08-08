# S4 · mathematics · secondary — stage preparation sign-off

**Date:** 2026-08-08 · **Template:** `docs/testing.md` v2.8 (bumped by this P-prep, §3 notes)
**Drawn class:** IX (seed `mathematics|secondary|2026-08-02`) · **standard duration:** 50 min
**Reference pair:** SS·secondary LP v1.10 · assessment v1.7
**Landed pair:** mathematics·secondary LP **v1.0 → v1.1** · assessment **v1.0 → v1.1**
**Pilot chapter:** IX · ch 4 · *Exploring Algebraic Identities* (founder pick, 2026-08-08)

Written by Claude. Status in the tracker is set by Kumar.

---

## 0. The headline — the constitutions are clean; C1 is gated on the CARRIER

P1–P5.3 are complete and this stage may be **signed provisionally**. But S4 cannot open
its C-cycle yet, and the blocker is not constitutional.

> **Scope note, corrected 2026-08-08 (founder challenge).** This is NOT "Aruvi cannot resolve
> mathematics assessment links". It can, and has all along: the app renders maths·secondary LPs
> and assessments correctly through `subjects/mathematics/subject.py::_secondary_assess`
> (line 263), which already runs the handoff-bridged join —
> `handoff_period_index(handoff, "section_number")` → `period_numbers`, platform stamp first —
> and is parity-tested. **The gap is one METHOD on one entry point.** The app reaches the plugin
> via `assessment_to_view`, which returns display objects; genon needs the RAW item dicts
> (options, `is_correct`, guide, `visual_stimulus` intact, for served files and exports), so it
> asks for `genon_assessment` instead — and only `science` has written one. `carriers.py`'s own
> docstring records this: *"The app never had this bug, because the app goes through the subject
> plugin… Genon skipped that layer."* Sizing therefore: the secondary half is ~6 lines, because
> `items_by_handoff` exists and maths·secondary needs the IDENTICAL arguments science·secondary
> passes. What makes the item serious is not its size — it is that the failure is paid for and
> misreported (below).

`aruvi_core/genon/carriers.py` carries an explicit `_NOT_YET` entry —

```python
"mathematics": "period-field join (middle/prep) + handoff-bridged (secondary) — owed by S4/S7/S8",
```

— and `assessment_items()` raises `CarrierNotImplemented` for it (`carriers.py:469` the test,
`:470` the raise). Every genon chapter to date has been Social Sciences (item-self-sufficient)
or Science (the one plugin with `genon_assessment`).

**`python3 genon/build_library.py mathematics ix 4` cannot certify — but it will spend the
money first, and it will report the wrong cause.** Corrected here after verification
(2026-08-08); an earlier draft of this note claimed the run "dies at compile before it spends a
rupee", which is false and matters, because that claim was the reason the gate looked cheap:

- `certify()` is called at `build_library.py:514`, **after** metered STEP 1 (`:482-484`) and
  metered STEP 4 (`:497-501`). The full ~₹110–150 for ch 4 is spent before the carrier is ever
  consulted.
- STEP 1 does not even fail. `generate_canonical.py:154-159` calls the carrier inside
  `try: … except Exception:` and falls back to `parsed.get("assessment_items")`. Maths·secondary
  emits its items under a **`questions`** wrapper (A1 schema), so that key is absent or a dict;
  either way the `isinstance(it, dict)` filter yields `[]` and the item-anchor validator becomes
  a **silent no-op**. A paid canonical installs looking clean, with every item anchored to
  nothing.
- The raise finally surfaces at `build_library.py:196-199`, inside `load_library`'s
  `except Exception`, which files it as `FAIL <file>: does not compile` for **every** library
  file. `lib` is then empty and `certify` exits at `:218-219` with
  `STOP: no library on disk to certify.` — so quarantine never runs and the message names
  neither the carrier nor mathematics.

So the gate holds in the sense that nothing can be certified, but it is a **post-payment,
misattributed** failure, not a pre-flight one. This is the S4 analogue of S6's engine gate.
Details and the second, subtler item in §3.

---

## 1. Per-item verification (testing.md §3, the Claude sign-off)

| Item | Verdict | Evidence |
|---|---|---|
| **A1** — one standard row | **PRESENT** | INPUTS 4 was "one or more rows of {duration_minutes, count}"; now "exactly ONE row {duration_minutes, count}: the class-standard duration (40 min for classes up to VII, 45 for VIII, 50 for IX) × the period count … handled downstream at serve time". The TIME integrity constraint is restated `duration × count` (was "sum of (duration × count) per schedule row … sum of row counts"); the A3 schema comment names the standard duration and a new field constraint states the one-row rule where the schema is actually read. Class bands are the master-plan calibration, not NCF's flat 40. **Declared deviation:** the reference says "partition time"; this file says **serve time** — the partition engine was retired 2026-07-31. Same correction S3 made. |
| **A5 + A7** — register as ONE block | **PRESENT, verbatim in substance** | One block after VOCABULARY in the v1.10 three-ban re-cut, bound at **Rule 9** (prohibition 6 — teacher-facing text and band activity) and **Rule 10** (teacher notes) by reference, never as scattered bans. `grep -c "THE SELF-CONTAINED REGISTER"` = 3 (heading + two binds), asserted by the edit script. **Declared deviation:** the reference's illustrative strings are Social Sciences content; substituted with mathematics ones ("a quick individual calculation", "an extended derivation", "having covered all three identities", "Having established the expansion of a binomial product, …"). The three bans and the closing backward-continuity rule are verbatim in substance. **Consequential edits, both following the reference:** VOCABULARY dropped its positional cross-reference examples ("the previous unit", "this unit") and gained the "session" exclusion; Rule 10's continuity bullet ("a brief recap of what the previous unit covered") is now position-free, naming the content built on. |
| **A6** — item anchoring | **CONFIRMED, not amended; one integrity block added to each file** | Items already carry `section_number` matching the handoff; the LP's `coverage_handoff` (A4) maps it to `period_numbers`. Mathematics secondary's unique link is the **SECTION**, not the unit — LP Rule 7 lets a section span several periods — so the reference's `period_ref` field is **not** ported. Both files gain a line recording that the platform DERIVES the anchor from `section_number` through `period_numbers`, and forbidding `period_ref` or any unit number on an item. Identical shape to science·secondary v1.1/v1.2 (founder ruling 2026-08-05: derive the link, never demand it). `grep -c phase_ref` = 0 in both; the reversed band-level `phase_ref` was not reintroduced. Carrier family already named for it: handoff-bridged (`carriers.py` docstring) — but **not yet implemented**, see §0. |
| **A9** — option order | **PRESENT as two lines; the removal is N/A, and no arrangement sentence** | **REMOVAL — N/A.** This file never carried the MEMORY-item-18 position prohibition. testing.md P2 names four files that carry it (SS + Science, middle and secondary); mathematics·secondary is not one. Confirmed by grep: `is_correct MUST` · `consecutive items` · `same label` all 0. Nothing was struck. **ADDED**, v1.7 wording: the "option order carries no meaning and is not yours to set" mandate in Rule 7, and the by-label option-reference prohibition. The pre-existing "none of the above"/"all of the above" ban is **absorbed into** that prohibition rather than duplicated — same ban, now carrying its reason; Rule 7's prohibition renumbered 1/2 to hold both, no scope lost. **NOT re-added:** `alphabetically` · `never led with` · `first word at which they differ` all assert 0 in the edit script's guards. |
| **P3** — Group B conversion | **N/A** | Group A. The A3 schema already emits `time_bands[{minutes, activity}]`; `grep -c 'phases\['` = 0, `'"phases"'` = 0, `band_id` = 0, `time_bands` present. Matches the §3 stage table's "time_bands" entry for S4. |
| **P4** — history to the sidecar | **DONE** | `CHANGELOG.md` created beside both constitutions. Neither file carried an in-document version-history block, so nothing was lifted out. The assessment sidecar also carries the standing RENDERER WIRING debt (VS-2 SVG / VS-6 graph paper) as a note, flagged for the C-cycle rather than the constitution. |
| **Cancelled amendments A2/A3/A4, X3** | **ABSENT** | None introduced. Note this stage's own long-standing `AMENDMENT A3` (LP JSON schema) and `AMENDMENT A4` (coverage handoff schema) headings are its own numbering — unrelated to the campaign's cancelled A3/A4, and untouched apart from the two A1 schema comments. |
| **V-rules in a constitution** | **NONE** | No section registry, no verbatim-anchor mandate, no first-visit-order rule, no closing-synthesis mandate, no per-variant assessment rule, no INPUTS acknowledgment, no precedence line. All of it stays in the platform-composed brief (`variant_plans.top_brief_for` / `briefs_for`), per testing.md §3. Worth stating because the synthesis mandate sits in visible tension with LP Rule 1's "every period anchors to a named section" — the brief overrides, the constitution is deliberately left alone, and `carriers.is_synthesis` + certification check 3's token exemption are where that is handled. |

---

## 2. P5 — stage inputs

**P5.1 · The floor.** Accepted at the standing ratio, `round(0.6 × recommended_periods)`,
no override. For ch 4 that is `round(0.6 × 14) = round(8.4) = 8`, matching
`floor_periods_at_standard` on the row. Equal dispersion over [8, 14]: A−C = 6 ≥ 4, so
counts are `{A, ⌈(A+C)/2⌉, C}` = **[14, 11, 8]** — three canonicals, three authoring runs.

**P5.2 · The section registry.** Mathematics secondary's section model is **obvious, and
needs no definition** — the summary carries an explicit `sections[]` spine of `{ref, title}`,
and LP A3 already specifies `section_anchor` as the bare ref ("e.g. '2.5'"). For ch 4 the
registry is the eight refs in summary order:

```
4.1 Introduction · 4.2 Visualising Identities · 4.3 Factorisation of Algebraic
Expressions Using Identities · 4.4 More Identities · 4.5 Factorisation Using Algebra
Tiles · 4.6 Factorisation Without Using Algebra Tiles · 4.7 Finding New Identities ·
4.8 Simplifying Rational Expressions
```

Consistency across the library is guaranteed by construction, not by hope:
`standard_registry()` reads the registry off the AUTHORED standard canonical and
`briefs_for()` prints it verbatim into each compact's brief. Nothing about the registry
enters a constitution. **One open item rides on this — see §3.2.**

**P5.3 · The pilot chapter — mathematics · IX · ch 4, "Exploring Algebraic Identities".**
Founder pick from the eight eligible chapters (9–16 are `placeholder: true`, awaiting NCERT
release). Summary and mapping both on disk; `placeholder: false`; `canonical_plan` present
(`counts [14,11,8]`, `basis: "arithmetic"`, `provisional: true` until the standard is
authored — expected at this point in the cycle). Eight clean numbered sections, mid-book of
the covered half, 18 worked examples and 21 exercises for Rule 9's `book_ref` discipline to
bite on. `core_cg` CG-3, `co_central: false` (so Rule 5's OPEN_TASK arrives via Rule 6's
lift, not via the co-central path), `effort_index` 11.0. Shape is close to the certified
SS·IX ch 3 pilot, so the ~₹110–150 library benchmark should hold; 3 runs at ~₹37 is the
budget line, and C2 records clean-path and all-in separately.

**P5.5 · The carrier trace** (the P-step this stage caused to exist — testing.md v2.8 §3).
Genon does not invent linkage; the verified 8-rule table does, and `carriers.py` is that table
exposed to genon. Mathematics·secondary's row:

> **rule 6** · handoff-bridged · item `section_number` → handoff `section_number` →
> `period_numbers` (**never** `section_anchor` text) · LO from handoff `implied_lo`
> (item: `implied_lo_assessed`) · container `{…, questions: []}` dict ·
> app-side method **`_secondary_assess`** (`subjects/mathematics/subject.py:263`, parity-tested,
> already serving the app) · **`genon_assessment` ABSENT** · **still in `_NOT_YET`.**

**CLOSED 2026-08-08** — the door is open and the row is delegated, not re-implemented. What
landed (all free, no metered step involved; §5 has the verdict):

- **`genon_assessment` on the mathematics plugin** — secondary delegates to
  `carriers.items_by_handoff` with row 6's two keys; middle/preparatory RAISE with their own
  family named, so they cannot silently borrow a rule that is not theirs. The stage is told
  apart by **container shape**, not `stage_for(grade)`: this method receives only `result`,
  and the grade lives on the enclosing saved plan, so a grade read here is `None` on the very
  call the carrier makes. `tests/test_genon_carriers.py` caught that within a minute of the
  first draft and now pins it.
- **`_NOT_YET` re-keyed by subject·STAGE.** It was per subject, which made `mathematics` one
  entry spanning two families — deleting it would have declared middle and preparatory ready
  too. Now maths·secondary is simply absent while `("mathematics","middle")` and
  `("mathematics","preparatory")` remain, each naming its 8-rule row and owing stage.
- **`carrier_gap()` / `require_carrier()`, and a STEP 0 pre-flight in `build_library.py`.**
  P5.5 asked for a read; this makes it a gate, because a gate cannot be forgotten. An owed
  stage now stops with `STOP before spending — …` before any metered step.
- **`generate_canonical.validate` no longer swallows `CarrierNotImplemented`.** It sat inside
  a bare `except Exception` whose fallback read a key the wrapper subjects lack, so the
  item-anchor check silently saw zero items and passed.
- **`genon_item_anchor_family` declared** on base/science/mathematics — the 8-rule table's
  family column as a first-class fact rather than something inferred, which is what the
  synthesis-row brief line reads.

**P5.4 · The three test identities' profiles for class IX. DONE 2026-08-08** — set up by Kumar
through the app's own first-run / profile flow, which doubles as the live check of that flow.
Verified against the store (`data/readiness/{u}/{u}/profile.json`); every P5.4 requirement is met:

| Identity | Mathematics IX sections | Durations | Periods/week | Role in C6 |
|---|---|---|---|---|
| kumar1 | **B, D** (9B, 9D) | [50] | 7 @ 50 | identity requests |
| kumar2 | **F** (9F) | [50] | 7 @ 50 | between-variant + below-floor |
| kumar3 | **H, I** (9H, 9I) | **[50, 60]** | 5 @ 50 + 2 @ 60, anchor 50 | **mixed-duration matrix** |

Sections are **disjoint** — no section appears on two identities — so X1's tenancy evidence is
unambiguous. The longer duration landed on **kumar3**, which is the identity §4 assigns the
mixed-duration weekly matrix to, so C6's matrix has real material against the 50-min class
standard rather than a contrived one. Leftovers from S1–S3 and S6 (Social Sciences VIII+IX,
Science VIII+IX) remain and are accepted per the founder ruling of 2026-08-07 — they touch no
mathematics-IX key. `grids[]` are all `-1`, which is correct post-Calendar-Purge, not an omission.

*Method note: verified by reading the store, not by calling `GET /readiness` — the Cowork sandbox
cannot reach the local API. The profiles were created through the app, so the API read is implied.*

---

## 3. What was found along the way — two items, both pre-C1, neither constitutional

### 3.1 The mathematics carrier is not wired to the GENON entry point (hard gate on C1)

**What is NOT wrong:** the join itself. `subjects/mathematics/subject.py::_secondary_assess`
(line 263) implements the handoff-bridged rule already, and the app has been rendering
maths·secondary lesson plans and assessments correctly on it. `link_resolver.py`'s docstring
names "Maths-secondary" in the handoff-bridged family, and the plugin follows it. Nothing about
the *resolution logic* needs designing.

**What IS wrong:** genon asks a different method for it.

`carriers.py`'s `_NOT_YET` lists `mathematics` and `assessment_items()` raises
`CarrierNotImplemented` (`:469` the test, `:470` the raise). Only `science` implements
`genon_assessment`; social_sciences and TWAU ride the item-self-sufficient default. So
`build_library.py` cannot certify mathematics today — after paying for it, and reporting
"does not compile" for the whole library rather than naming the carrier (§0). What S4 needs:

1. **`genon_assessment` on the mathematics plugin** (`aruvi_core/subjects/mathematics/subject.py`).
   For **secondary** this is a ~6-line delegation, not new logic — `items_by_handoff` already
   exists in `carriers.py` and maths·secondary needs the **identical arguments**
   science·secondary passes, because both wrap items under `questions` and both join
   `section_number` → `section_number`:

   ```python
   def genon_assessment(self, result):
       from ...genon.carriers import items_by_handoff
       raw = result.get("assessment_items")
       if isinstance(raw, dict) and "questions" in raw:        # secondary
           return items_by_handoff(result, items=raw.get("questions") or [],
                                   join_key="section_number",
                                   handoff_key="section_number")
       raise CarrierNotImplemented("maths middle/prep: period-field join, owed by S7/S8")
   ```

   `items_by_handoff` already anchors at the **LAST** unit of the group, per the founder's
   2026-08-05 rule (an item tests the section's whole `implied_lo`, so it becomes available only
   when the section completes) — so that ruling is inherited, not re-implemented. The only care
   needed is that the middle/preparatory branch must NOT silently fall through to a wrong join;
   it belongs to a different family and is owed by S7/S8.
2. **The `questions` wrapper is worse than a container note — it disarms STEP 1's only
   anchor check.** Maths·secondary wraps its items under `questions`, exactly like
   science·secondary. `raw_item_list`'s shape-based lookup should find them, but
   `generate_canonical.validate` never gets that far: its carrier call is inside a bare
   `except Exception` whose fallback reads the flat `assessment_items` key, which this shape
   does not have. Result `[]`, validator silent (§0). So the fix is two-part — implement the
   carrier, **and** stop `validate` from swallowing `CarrierNotImplemented` into a pass. A
   subject with no carrier should refuse to generate, not generate unvalidated. This is
   precisely the failure mode S3's `questions`-wrapper bug created the seam to prevent, now
   recurring one layer up.
3. **Deleting `_NOT_YET["mathematics"]` opens middle AND preparatory too**, and those are a
   *different* family (period-field join, owed by S7/S8). Two clean options, founder's call:
   implement both halves now branching on `stage_for(grade)`, or make `_NOT_YET`
   stage-aware so S4 can open without silently unlocking S7/S8. Recommend the latter — it
   keeps the campaign's stage-at-a-time discipline and is a smaller change.
4. **Optional, and downgraded after verification:** declaring `genon_serve_granularity` /
   `genon_has_section_axis` on the mathematics plugin is cosmetic. Checked live —
   `serve_granularity("mathematics","ix")` returns `"unit"` and `has_section_axis(...)`
   returns `True`, reached through `carriers._ask`'s **documented default**, not through a
   swallowed exception. An earlier draft of this note claimed the right answer arrived "by
   luck"; that was wrong. Declaring them explicitly is still worth doing for legibility, but
   it is not a correctness item and does not gate C1.

### 3.2 The synthesis unit has no home in a derived-anchor handoff (brief item, cheap now)

Under architecture v2.0 the STANDARD canonical must close with a whole-chapter synthesis
unit whose `section_anchor` is the reserved token `synthesis`, and it is excluded from the
registry. On a stage where items anchor by `period_ref` that is harmless. On a **derived**
anchor stage — science·secondary and now mathematics·secondary — the item's only route to a
unit is `section_number → coverage_handoff → period_numbers`. **If the synthesis unit gets
no handoff entry, nothing can anchor to it**, and C9.2 ("a borrowed unit brings its own
items") is unsatisfiable on exactly the Case-1 synthesis borrow that C8 exists to inspect.

What the installed science·IX ch 8 library actually does: the model emitted an **11th
handoff entry with `section_label: "synthesis"`**, `period_numbers: [12]`, and
`total_sections: 11` — i.e. it invented a section slot for the synthesis unit, and
`total_sections` counts it. Nothing asked for it, and the maths A4 schema is stricter:
`section_ref` and `section_title` are specified as **copied verbatim from the summary**, and
there is no summary section to copy. The model will either omit the entry or contradict A4.

**And the invented entry does not actually rescue it.** Verified on the installed library
(2026-08-08): the entry provides a *route*, but **no item uses it** — ch 8's item
`section_number`s run 1–10, and `assessment_items()` stamps `unit_ref` 1,2,4,5,6,7,8,9,10,11,
never 12. So **C9.2 is already unsatisfiable on the certified reference library**, not merely
at risk on mathematics. The compacts (p07, p10) carry no synthesis unit and no such entry, as
v2.0 requires. This is a live defect against a CERTIFIED stage, so it wants raising as one
(§7) rather than only as an S4 pre-C1 item — but the remedy is the same single brief line, and
it costs nothing to make it before ch 4 is authored.

`top_brief_for` mandates the synthesis unit and says nothing about its handoff row. One
line in the brief closes this for every derived-anchor stage. It is a **V-series / brief
matter and MUST NOT go into a constitution** (§3: brief wording iterates freely; a
constitution change triggers the §9 cascade). Founder call on the values — the
science-compatible reading is `section_number` = the entry's ordinal, `section_ref` /
`section_title` = the token `synthesis`, `total_sections` = the entry count. Worth settling
before ₹110 of ch 4 is authored against a guess.

---

### 3.3 The handoff↔anchor question — FOUNDER RULING 2026-08-08, and a new certification check

Found at C1 on the authored library, and worth recording carefully because the obvious fix was
the wrong one and I initially recommended it.

**What was observed.** The top canonical's units 10, 11 and 12 carry `section_anchor: "4.1"`
(Introduction) while section 1's handoff row lists `period_numbers: [1]`. Their titles are
whole-chapter consolidation — "Mixed Expansion and Products Using All Identities So Far",
"Factorising a Wide Range of Expressions Using All Chapter Identities", "Geometric and
Contextual Problems". They are not teaching Introduction.

**What was NOT a defect, corrected.** I first reported "5 of 14 units hold no assessment item"
as a finding. It is arithmetic, not a fault: items are one-per-LO, LOs are per-SECTION, and the
chapter has 8 sections + synthesis = 9 handoff groups, so at most 9 of 14 units can ever anchor
an item. The founder's challenge was right. Item counts are exactly as Rule 5 mandates in all
three canonicals — top 14 items / 14 LOs, p11 11/11, p08 11/11.

**Why the obvious repair was rejected — measured, not argued.** Extending `sec#1` to
`[1, 10, 11, 12]` moves the Introduction item to unit 12, because an item anchors at its
section's LAST unit. Served both ways across X = 6…14:

| X | mode | `sec#1=[1]` (as authored) | `sec#1=[1,10,11,12]` |
|---|---|---|---|
| 12 | synthesis | 12 items, **Introduction present** | 11 items, **Introduction ABSENT** |

Every other X is identical. So the "fix" costs one question and buys nothing. `[1]` is the
truthful list: section 4.1 completes at unit 1, and a consolidation unit revisiting it does not
re-open it. **p11 is the proof from the other side** — it *does* list them
(`sec#1 = [1, 10, 11]`), and that is precisely why p11 loses its Introduction item at X=9 and
X=10. The canonical that complies with Rule 12 here is the one that drops questions.

**FOUNDER RULING, 2026-08-08: leave the item linkage severed.** `sec#1` stays `[1]`; units
10/11/12 are not routed. Nothing was edited — the linkage was already absent and stays absent.
The residual wrong-section *label* on those units is NOT repaired: `repair_register.py` excludes
"an anchor that names the wrong section" by name, and `repair_anchors.py` is serialization-only
("the anchors name the RIGHT sections… only the DELIMITER is wrong"). Neither tool covers it,
which is correct — it would be authoring content judgements as text hygiene. It goes to the
human gate.

**Root cause, for the founder's list — architectural, not a model failure.** There is **no legal
anchor token for a CONSOLIDATION unit.** The registry is the chapter's sections and `synthesis`
is reserved to exactly one closing unit, so a chapter with many more units than sections has no
honest label for the remainder and the model picks the least-wrong registry entry. Confirmed not
to be a maths quirk: the same advisory fires on the **certified** science·IX ch 8 p10, whose U10
wears a four-section composite label the handoff does not route through. Options, all founder
calls: allow a `consolidation` token beside `synthesis`; cap canonical counts nearer the section
count; or accept the label as cosmetic and let the advisory carry it.

**New certification check (`build_library.py::certify`).** Nothing had ever compared the two
objects that between them decide where an item lands — checks 3–5 test `section_anchor` against
the REGISTRY, and nothing tested it against the `coverage_handoff`. The check is deliberately
asymmetric, because the evidence above says the two directions are not equivalent:

- **GATE** — a handoff row routing to a unit that does not anchor its section. The item would
  land on a sitting that never taught it; there is no reading on which that is correct.
  Negative-tested: injecting `sec#1 → [1, 5]` (U5 anchors 4.5) produces
  `FAIL … 1 mis-route(s): U5 anchors ['4.5'] but is routed as '4.1'`.
- **ADVISORY, never a gate** — a unit wearing a section label the handoff does not route items
  through. Carries an explicit "do NOT extend period_numbers to fix this" warning, so the next
  reader does not repeat my mistake.
- An informational line stating how many units *can* carry an item, so nobody reads
  "N units without an item" as a defect again.

Verified no regression: SS·IX ch 3, SS·VIII ch 3, science·IX ch 8 and science·VIII ch 6 all
still report **ALL PASS**. SS's dict-shaped (competency-keyed) handoff and science·middle's
plan-granularity stage are both skipped correctly.

## 4. Verdict — **ALL P-STEPS CLOSED; S4 IS CLEAR TO ENTER C1**

**P1, P2, P4 — complete and verified. P3 — N/A with evidence. P5.1–P5.3 — recorded.
P5.4 — DONE (profiles verified). P5.5 — DONE (carrier landed, tested).** Both §3 findings are
fixed, not merely declared.

**Test state:** `tests/test_genon_carriers.py` **25 → 36 tests, all green**, including the row-6
join at the section's LAST unit, the synthesis row being reachable, an unserved anchor resolving
to `[]` rather than a guess, raw item fields surviving, the no-grade regression, the pre-flight
gate, and the family declarations against all eight rows. Full suite **20 passed / 5 failed**;
all five failures were confirmed pre-existing on a tree with these changes reverted
(`test_api` needs `fastapi`, `test_link_resolver` + `test_normalized_item` want a missing
English saved plan, `test_lp_standard` a missing TWAU view, `test_stimulus` a fixture count).

**Before C1, one thing is still worth a founder eye:** the synthesis-row brief line is new, so
ch 4's top canonical is the first artefact ever generated against it. Read that one row in the
output before STEP 4 buys the two compacts — it is the cheapest possible place to catch a
wording problem, and STEP 1's output is resumable, so checking costs nothing.

### The C1 command

```bash
python3 genon/build_library.py mathematics ix 4
```

It will no longer stop at the carrier. It *will* still stop at STEP 2 with "Row is provisional"
until the standard canonical exists — that is the normal path for a fresh chapter, not a fault.

The constitutional gate is clear: **no cancelled amendment, no V-rule, no arrangement
sentence, no pedagogical rule changed in either file.** The stage may be **signed
provisionally**.

It may **not** enter its C-cycle until §3.1 lands — the mathematics genon carrier — and
§3.2 should be settled in the same pass, before C1 spends anything. Note the gate is
post-payment, not pre-flight (§0), so "the build will stop us" is not a safety net here.

### Disclosed residues (declared, not fixed)

Two statements in the LP survive the A1 amendment and are now vestigial. Both are left
untouched deliberately, because science·secondary v1.1 and science·middle v2.2 carry the same
residue and changing them here alone would put four signed stages out of step for no gain:

1. **A4's `period_duration_minutes` comment** — "if mixed across this section's periods, the
   most common". Under one standard row nothing can be mixed. Harmless; inert.
2. **The class-X duration band.** INPUTS 4 names "40 ≤VII · 45 VIII · 50 IX" verbatim from the
   reference, in a constitution whose grades are `ix · x`. testing.md P1 writes the band as
   "50 IX–X". Practically inert — step 0.6 records that class X has no content in any subject —
   but if the founder wants the wording aligned, it should be aligned in the reference and
   ported, not patched per stage.

A third was **fixed** as a directly consequential edit rather than disclosed: A3's
`teacher_notes` comment read "recap-and-connect", the exact framing Rule 10's bullet was
rewritten away from. It now reads "continuity by content not position", matching
science·secondary's practice of pointing at the rule instead of restating it.

Artefacts, all in `genon/out/stage_prep_mathematics_secondary/`:
`lesson_plan_constitution_v1.0_pre.txt` · `assessment_constitution_v1.0_pre.txt` ·
`lp_v1.0_to_v1.1.diff` · `assess_v1.0_to_v1.1.diff` · `apply_s4_amendments.py` (the
reproducible edit script — every edit asserts exactly-one occurrence, and the run closes on
guard assertions for the struck arrangement strings and the P3 target shape).
Plus the two `CHANGELOG.md` sidecars.
