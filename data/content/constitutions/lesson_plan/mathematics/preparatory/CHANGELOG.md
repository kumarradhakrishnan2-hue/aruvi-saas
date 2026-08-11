# CHANGELOG — Lesson Plan Constitution · Mathematics · Preparatory Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).

---

## v1.3 — 2026-08-11 · Rules 1 and 2 aligned with SECONDARY and MIDDLE (S8 · P1, on challenge)

Landed at S8's P-prep, hours after v1.2 and still **before any canonical for this stage was
authored**. The first sign-off recommended leaving both numeric caps alone; the founder
challenged it — *"should we not align rule 1 and rule 2 with middle maths"* — and the data
does not support the recommendation. Three things settled it.

1. **The corpus already breaks the cap, with slack in hand.**
   `backup/saved_plans/mathematics/iv/ch_08_*.json` runs section S5 across periods 6, 7 **and
   8** — three periods against a cap of two — on a plan of 9 body units against a cap of 12.
   Arithmetic did not force it; the content did. So the cap does not only break when
   `body units > 2 × sections` (the 4-of-14 case the sign-off measured); it breaks whenever a
   heavy section warrants a third period, which is a property of the section and not of the
   budget. **The pilot dodging the arithmetic case buys nothing** — which is precisely what
   the first recommendation rested on.
2. **"Prep sections are small and task-dense" is half-wrong.** Across class III's 98 sections
   the median is 3 tasks and the mean 4.2 — but the maximum is 13 and **nine sections carry
   more than eight**. Those are exactly the sections a two-period cap mis-sizes. The claim was
   true of the median and irrelevant to the tail.
3. **Preparatory was the sole outlier left in the maths family.** Secondary never carried the
   cap; middle's went at v3.6. S7's changelog named the tell — *"the only one of the three that
   named a number"* — and after v3.6 that tell pointed here.

And Rule 1's other cap was not a risk but a **certainty**: the platform brief mandates a
closing whole-chapter synthesis unit, and *"one — or at most two adjacent — sections"* cannot
describe one. S7 met exactly this at C3 (ARV-D-094) and amended mid-cycle.

**What changed.**

- **Rule 1** loses the two-section cap (*"A period anchors to as many ADJACENT sections as its
  content warrants"*) and gains the contiguity sentence: a section's periods are CONTIGUOUS,
  and a later period MUST NOT re-anchor a section an earlier run completed. Consolidation
  belongs inside the section's own run. Adjacency is kept and is load-bearing — it stops a
  period naming S1 and S4 while skipping what lies between, which is what the serve engine's
  registry and first-visit arithmetic read off this field.
- **Rule 2** is renamed **FULL-SECTION COVERAGE**. The two-period cap is gone; a section may
  span as many ADJACENT periods as its content warrants, emphasis following the substance of
  the section and never the effort_index. Secondary's two prohibitions are ported in substance
  (no numerical allocation formula across sections; no front-loading). The coverage mandate
  **moves here from Rule 1**, where middle keeps it, so the two stages now read the same rule
  in the same place. The task-order rule is kept.

**Two things deliberately NOT ported, and both matter.**

- **v3.6's SURPLUS bullet.** Middle introduced it at v3.6 and **deleted it at v3.8** as the
  cause of the hoarding it was meant to cure — it framed placement as spending spare units,
  and a unit conceived as an add-on has no run to belong to (ARV-D-089). What ports is
  middle's **end state**, not its text at the moment the caps came out. `surplus`, `deepen`,
  `budget exceeds` and `more time available` are all asserted absent.
- **Middle's two `section_goal` split paragraphs.** Preparatory has **no per-period goal** —
  its cognitive axis is the per-TASK `intent` (Rule 4), and the handoff clusters on intent
  (Rule 8). Porting them would invent a field this stage does not have, which the founder
  ruling of 2026-08-10 forbids. `grep -c section_goal` = 0.

**Three residues, found by grepping the NUMBER rather than the rule.** A cap removed from one
rule and left standing in three other places is not removed. The DESIGN PRINCIPLE restated it
(*"each period anchors to one or two adjacent sections"*), Rule 2A still said *"Before
bin-packing"* after Rule 2 stopped being a bin-packing rule, and — the one that matters most —
the **schema comment carried the cap as a number**: `"section_refs": [...] // 1–2, e.g. ["S3"]`.
S7's v3.7 hit the identical thing in middle (`// 1–2 entries`). Rule 4's *"two adjacent reason
tasks"* (methods) and Rule 9's *"1–2 items"* (homework) are different subjects and are
untouched.

**§9: a constitution change in the FULL sense.** Both caps coming out are relaxations, but the
contiguity sentence and the two prohibitions are tightenings — **three new obligations**, which
the edit script asserts exactly (the first run asserted two and failed; the guard was corrected
rather than loosened). One tightening anywhere forfeits the relaxation-only carve-out. **It
costs nothing today because no library for this stage exists.** That is exactly what the §3
ordering rule buys, and it is the whole difference between this and S7, which paid ~₹106 and a
C1–C3 re-run to learn the same thing.

Artefacts: `genon/out/stage_prep_mathematics_preparatory/` —
`lesson_plan_constitution_v1.2_pre.txt` · `lp_v1.2_to_v1.3.diff` ·
`apply_s8_rules_1_2_alignment.py` (guards assert the cap is gone in every form including the
schema comment, the port arrived intact, the surplus framing never arrived, no `section_goal`
or `textbook_segments` leaked in, exactly three obligations were added, and A1, the register
and the P3 shape are all untouched).

---

## v1.2 — 2026-08-11 · the campaign carry-forward (S8 · P1 + P3)

Landed at S8's P-prep, before any canonical for this stage was authored (testing.md §3
ordering rule). Ported from the SS·secondary v1.10 reference via the mathematics·middle
v3.4 adaptation — same subject vocabulary, one stage up, and the same 8-rule FAMILY
(period-field), so the port is close to mechanical. No pedagogical rule changed: Rules 1–4
and 7–9 are untouched in force, and every edit below is either a platform fact the model
must know or a rename of a field the platform reads.

- **A1 — the period schedule is exactly ONE standard row.** INPUTS 4 was
  "Period schedule: {duration, count} rows; total = B", which licensed the mixed-duration
  plans the variant serve engine cannot use. It now names one row at the class-standard
  duration (40 min for classes up to VII, 45 for VIII, 50 for IX–X — the master-plan
  calibration bands, not NCF's flat 40) and says where timetable variation is handled
  instead: downstream, at serve time. Class III's standard is 40 min, which is what the
  master-plan row for `mathematics|III` already carries.

- **A5 + A7 — THE SELF-CONTAINED REGISTER, as ONE block beside VOCABULARY**, in the v1.10
  three-ban re-cut: no clock quantity, no forward reference or completion claim, no calendar
  time; backward continuity welcome, carried by naming the content built on. Bound by
  reference at Rule 6 (band narration) and at the `teacher_notes` schema comment — never as
  scattered prohibitions. This is the **three-ban** cut, not S6's two-ban exception: prep
  maths units anchor to textbook sections and travel between plans, so ban 2 binds in full.
  Illustrative strings are prep-maths ones ("a quick count round the class", "an unhurried
  making activity", "now that we have weighed everything", "The children have grouped in
  tens to count large collections, …").

- **Two consequential edits the register forced, both the same two S7 made.** VOCABULARY was
  *teaching* the forward reference ban 2 forbids — its cross-reference examples were
  literally `"the previous unit"`, `"this unit"` — so the examples are dropped and "session"
  is added to the excluded register. And the `teacher_notes` schema comment asked for
  positional continuity ("Recap prior unit"); it now asks for content-named continuity and
  cites ban 2.

- **P3 — `phases[{minutes, description}]` → `time_bands[{minutes, activity}]`.** Real here,
  not N/A: the array and the key are both renamed, with Rule 5, Rule 6's heading and prose,
  Rule 7 and the schema following. No `band_id` in the target shape — the band layer left the
  declaration surface when the partition engine was retired. `compile.py` reads exactly
  `time_bands` / `activity`: it rebuilds the timed spine from them (`:124`) and asserts an
  inventory invariant over the activity text (`:208-210`), which is why this one cannot be
  absorbed by a tolerant read the way the anchor is. `grep -c 'phases\['` = 0,
  `time_bands` = 2.

- **Rule 6's heading renamed** PHASE NARRATION → BAND NARRATION, and the register bound to
  every band in the same rule, matching middle's Rule 10.

- **Footer version corrected** — it read "Version 1.1" and now tracks the header.

**What this pass deliberately did NOT do — founder ruling, 2026-08-10, carried from S7.** No
field was invented to feed the serve engine. `section_anchor` was NOT added to the period
object. The unit anchor is already in the authored file under this stage's own name —
`section_refs[]` — and the plugin mediates the read
(`aruvi_core/subjects/mathematics/subject.py::genon_unit_anchor`, whose preparatory branch
S7 wrote and left unexercised pending this stage). That is P5.5's work, not this
constitution's. The edit script asserts the absence as a guard so a later pass cannot
reintroduce it by drift.

**One tension recorded, not resolved here.** Rule 1 says every section in the summary MUST
appear in at least one period's `section_refs` and that dropping a section is FORBIDDEN,
while the v2.0 serve architecture mandates a closing whole-chapter synthesis unit that
anchors to no section at all. The brief overrides, the constitution is deliberately left
alone (a V-rule may never enter a constitution — testing.md §3), and
`carriers.is_synthesis` plus the certifier's token exemption are where that is handled. This
is the same tension S7 recorded against middle's Rules 1 and 2, and it needs no amendment.

Artefacts: `genon/out/stage_prep_mathematics_preparatory/` —
`lesson_plan_constitution_v1.1_pre.txt` · `lp_v1.1_to_v1.2.diff` ·
`apply_s8_amendments.py` (the reproducible edit script; every edit asserts exactly one
occurrence, and the run closes on guards for the struck A9 arrangement strings, the retired
`phases` shape, `band_id`, `phase_ref`, `section_anchor`, `period_ref`, the cancelled
amendments' vocabulary and the V-rules).

**§9: this is a constitution change in the full sense** — bounds are tightened (one row, not
rows) and new obligations are created (the register's three bans), so the relaxation-only
carve-out does not apply. It costs nothing today because no library for this stage has been
authored yet; that is exactly what the §3 ordering rule buys.

---

## v1.1 and earlier

No sidecar was kept before this file existed, and the constitution carried no in-document
version-history block to lift out. Earlier history is in git.
