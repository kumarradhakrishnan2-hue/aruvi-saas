# Seam read — the two non-self borrows · SS · IX · Ch 3

Human-gate prose inspection of the X−1 → X transition at the only two points in the band
where slot X comes from a plan other than the one being served. Repaired registry
(`; ` → ` / `). Companion to `…_FITNESS_20260803.md`.

| X | prefix served | last prefix unit | slot X borrowed | lender |
|---|---|---|---|---|
| 8 | p10 U1–U7 | **p10 U7** · Climate Change | **p07 U7** · Punjab Floods case study | p07 |
| 9 | p10 U1–U8 | **p10 U8** · Punjab Floods case study | **p12 U12** · whole-chapter synthesis | p12 |

**Verdict: no jumpiness at either seam — every prior either borrowed unit names is genuinely
taught in the prefix. But X=8 has a real flaw, and it is in the selector, not the prose.**

---

## Seam A · X=8 — p10 U7 → p07 U7

### What holds

p07 U7's teacher note opens: *"Having established the mechanisms of climate change as a
long-run planetary process, this unit grounds that understanding in a specific, recent,
geographically named event…"* In p07's home plan the preceding unit is U6 Climate Change; in
the served plan the preceding unit is p10 U7 Climate Change. **The back-reference lands
exactly.** Every other prior the unit draws on — monsoon rain and western disturbances (p10
U6), the river geography, the chapter text — is in the prefix. First-exposure for section 8
confirmed: p07 U7 is the first unit in p07 to deal the case study.

### ⚠ A1 — the chosen plan's OWN unit was available and lost the tie-break (the real flaw)

p10 has its own case-study unit, **U8 "Punjab Floods 2025: Separating Natural from Human
Causes"**, which is the identity candidate for slot 8 and equally first-exposure. It lost.
`fill_slot`'s sort key is:

```python
(overlap==0, overlap, -reach, abs(count - requested), -count)
```

Both candidates have `overlap=0` and `reach=8`, so the decision falls to
`abs(count − requested)`: p07 is |7−8| = 1, p10 is |10−8| = 2. **There is no self-preference
term.** The engine hands the teacher a stranger's lesson where the plan she is being served
has its own.

That matters because p10 U8 is written *for this exact prefix*:

> "The climate change mechanism examined in **the unit on greenhouse gases and fossil fuels**
> has a concrete, recent manifestation in the Punjab floods…"

— a precise back-reference to p10 U7, the sitting the class just had. p07 U7's reference is
generic by comparison. The two units teach substantially the same lesson (two-column
natural/human sort → cause-effect map → CLASSROOM DISCUSSION prompts → written evaluative
exit), so nothing pedagogical is *lost* — but the engine chose the version with the weaker
continuity when the better one was free, and "pacing context" is a thin reason to prefer a
foreign unit over the identity candidate.

It also causes A4 below.

**Recommendation:** add self-preference to the tie-break, above pacing distance —
`(overlap==0, overlap, -reach, not self_fill, abs(count-requested), -count)`. The identity
candidate should win every tie it enters. This is a one-line change and it strictly improves
X=8 with no effect anywhere else in the band (X=5, 6, 11 already self-fill; X=9 is Case 1).

### ⚠ A2 — the carbon-footprint pledge thread is left dangling

p10 U7 closes deliberately open: the class aggregates its audit scores and is asked *"whether
individual pledges are sufficient or whether collective and policy-level action is also
required."* That is a set-up — p10 pays it off in **U10**, which builds an explicit
individual / community / policy three-tier action plan and names "the pledge from carbon
footprint audit" as a live data source. At X=8, U10 is never served and the borrowed p07 U7
knows nothing about the thread, so the question is asked and never answered.

Note that p07's own sequence does *not* have this problem: p07 U6 closes its pledge thread
in-unit ("Students note one systemic measure alongside their personal pledge"). The dangle is
created by the borrow, not present in either home plan. Under the A1 fix it disappears
anyway — p10 U8 doesn't close the thread either, but the plan reads as p10's own arc, and the
teacher is not being handed a foreign unit that silently orphans a set-up.

### ⚠ A3 — the same organiser two sittings running

p10 U7's central task (band 2) is *"Map this chain on the board as a cause-consequence
diagram while students copy it."* p07 U7's central task (band 2) is *"Students build a
cause-effect map: from the two columns of causes, draw arrows to the chapter's listed
effects."* Two consecutive periods whose main activity is the same organiser.

Neither home plan does this — p07 U6's central task is written one-sentence causal chains,
not a board diagram. Pure borrow artefact. Low severity (a teacher will just vary it), and it
also resolves under the A1 fix: p10 U8's central task is a **two-column worksheet**, a
different instrument.

### ⚠ A4 — four case-study items in one assessment, two of them struck through

Direct consequence of A1. The served assessment at X=8 carries **20 items, 7 flagged
unscheduled** — and among them:

| item | anchor | state |
|---|---|---|
| SCR · Punjab Floods | p07 U7 | live |
| SCR · Punjab Floods | p07 U7 | live |
| SCR · Punjab Floods | **p10 U8** | **"anchor unit not scheduled in this plan (time budget)"** |
| SCR · Punjab Floods | **p10 U8** | **"anchor unit not scheduled in this plan (time budget)"** |

The teacher receives four questions on the same section, two of them marked as not covered —
while the coverage note tells her every section *is* covered. The unit-level anchoring (R5)
cannot see that the borrowed unit taught the very section its orphans test. Under the A1 fix
this specific case vanishes; the general defect (§3 of the fitness report) does not.

---

## Seam B · X=9 — p10 U8 → p12 U12 (synthesis)

### What holds — checked prior by prior

p12 U12's note states its priors explicitly: *"assumes all chapter sections have been taught
… from the gas proportions in Fig. 3.2 through the layered structure, the five weather
elements, the seasonal and monsoon mechanisms, the greenhouse effect, and the Punjab floods
case study."* Against the served prefix:

| prior named by the synthesis | served by | status |
|---|---|---|
| gas proportions, Fig. 3.2 | p10 U2 | ✓ |
| layered structure | p10 U3 | ✓ |
| five weather elements (insolation, temperature, humidity, pressure, wind) | p10 U4 | ✓ |
| seasons (IMD four, six ṛtu) | p10 U5 | ✓ |
| monsoon mechanisms, land–sea differential | p10 U6 | ✓ |
| greenhouse effect | p10 U7 | ✓ |
| Punjab floods case study | p10 U8 | ✓ |

**The ARV-D-023 trap does not bite here.** I checked specifically whether p10 U4 merely
*anchors* "Elements of Weather and Climate" or actually teaches it — its band 8–28 teaches all
five elements systematically with Figs. 3.6/3.7/3.8 and Table 3.1. The anchor is honest.

The opening also transitions cleanly: p10 U8 closes on a case-study evaluative question
("Is describing an event as a 'natural disaster' ever fully accurate?"), p12 U12 opens on a
whole-chapter thread question. Different register, no collision, natural escalation. **Case 1
is doing exactly what §0.3 promises.**

### ⚠ B1 — the synthesis is pitched at a class with one more rehearsal than this one

The concept map's critical task is *labelled cross-node arrows*, and the note's exemplar is a
demanding one ("ozone in stratosphere filters the UV that, if unfiltered, would raise surface
temperatures beyond the torrid zone's current range").

In p12's home plan that inter-linkage reasoning is built over **two** elements units — U4
(Weather/Elements) and U6 (a second pass at Elements). The served class had **U4 only**.
p10's own inter-linkage drill is **U9, "Interlinked Physical Systems: Insolation, Relief, and
Regional Climate Variation"** — whose entire purpose is to make students state inter-linkages
rather than parallel facts — **and X=9 withholds it.**

This is not a false prior (the elements *were* taught, so the unit assumes nothing untrue).
It is a **cognitive-demand mismatch**: the hardest task in the synthesis presumes a rehearsal
this prefix skipped. Softer than jumpiness, and only visible on a read. Cheap to mitigate —
a difficulty note to the teacher, not a restructure. Worth noting that it is structural to
Case 1: a synthesis authored at the top count will always assume the top plan's depth of
rehearsal, and Case 1 lends it into shorter prefixes by design.

### ⚠ B2 — two authored units vanish, and the coverage note says everything is covered

X=9 withholds **p10 U9** (the inter-linkage analysis above) and **p10 U10** ("From Greenhouse
Gas to Flood Plain" — the three-tier individual/community/policy action plan). The coverage
note reads:

> "Every section is covered; the closing sitting draws the chapter together in one…"

True at section granularity, and `uncovered_sections` is correctly empty. But the teacher
loses two substantial authored sittings and is told nothing at all. Compare X=8, which names
what moved to self-study. The asymmetry is that drops are reported per *section* and these
losses are per *unit*.

This also drives the item orphaning at X=9: 5 of 19 items are struck, and three of them are
**Climate Change** items anchored to U10 — a section that *was* taught, in U7. Same defect
family as A4.

**Recommendation:** when `withheld_units` is non-empty, say so — "two authored sittings
(inter-linkage analysis; human-environment action plan) were not scheduled at this budget;
their material is available." Refusal-with-access is already the doctrine (§6); this is the
same principle applied one granularity down.

---

## Cross-cutting · the live-item dip lands exactly on the two mixed serves

| X | 7 | **8** | **9** | 10 | 11 | 12 |
|---|---|---|---|---|---|---|
| items in artefact | 18 | 20 | 19 | 18 | 18 | 18 |
| **live (schedulable)** | **18** | **13** | **14** | **18** | **17** | **18** |

A teacher who moves from 7 periods to 8 **gains a period and loses five live assessment
items.** The dip is non-monotonic and sits precisely at the two non-self borrows — which is
the tell that it is caused by cross-plan substitution, not by time budget. Both mixed serves
report complete section coverage while delivering the *thinnest* assessments in the band.

A1 lifts X=8 from 13 live to 18. B2's re-anchoring (§3 of the fitness report — re-anchor an
orphaned item when a served unit covers its section, rather than flagging it) lifts X=9 from
14 to 17. Together they flatten the dip.

---

## Summary of what to change

| # | flaw | severity | fix |
|---|---|---|---|
| A1 | identity candidate loses the tie-break to a foreign plan | **high** | add `not self_fill` to `fill_slot`'s sort key, above pacing distance |
| A4 | four case-study items, two struck | high | resolved by A1 |
| B2 | withheld authored units unreported | medium | name `withheld_units` in the coverage note |
| — | live-item dip at the mixed serves | medium | A1 + section-level re-anchoring |
| A2 | dangling pledge thread | low | resolved by A1 |
| B1 | synthesis pitched above the prefix's rehearsal | low | teacher-facing difficulty note; structural to Case 1 |
| A3 | same organiser two sittings running | low | resolved by A1 |

**The prose at both seams is sound.** Five of the seven items above trace to one missing term
in one sort key.
