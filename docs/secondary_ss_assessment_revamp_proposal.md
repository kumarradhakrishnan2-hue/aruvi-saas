# Proposal — Secondary Social Sciences: Assessment Revamp + Lesson-Plan Constitution Adaptation

**Status:** draft for founder review
**Scope:** Class IX–X (secondary) Social Sciences only. Middle SS is finalised (LP v2.7, Assessment v2.2) and is the baseline this proposal adapts from.
**Evidence base:** the two IX chapters studied end-to-end — Chapter 5, *State and Society up to 1000 CE* (History), and Chapter 9, *The Price Puzzle: What Drives the Market* (Economics) — read against the finalised middle constitutions and the Opus/Sonnet generation runs of VI ch-6.

---

## 1. The one-line thesis

**Keep the machinery, raise the altitude.** The edge model, deterministic LO-to-slot selection, singular one-item→one-unit linkage, edge inheritance, and exact weight-driven counts are stage-agnostic and are the crown jewels — they carried perfectly across two different models on the middle run and must transfer to secondary unchanged. Secondary needs exactly two shifts, both driven by what the IX chapters actually are: **higher cognitive demand**, and **source/data interpretation as a first-class act, not an optional extra.**

Nothing below reopens the edge model. It changes only what secondary's content demands.

---

## 2. What the two IX chapters establish (evidence, not assumption)

Both chapters share a structure that differs from middle in three measurable ways:

**A. They are built to be interrogated, not recalled.** Each opens with **4 "Big Questions"** and closes with a "Questions and activities" set that is markedly higher-order: ch5 asks students to weigh what a primary source does and does not reveal ("What might be some limitations of relying only on such sources?") and includes a full **primary-source item** — the Nāśhik cave inscription (Q12) with structured sub-questions. ch9 asks "Defend or refute," multi-part causal chains ("if petrol prices double, what happens to diesel cars / EV / accessories / public transport"), and market-behaviour reasoning.

**B. The discipline *is* source and data work.** History (ch5) is explicitly about corroborating literary sources (the Rig Veda) against archaeology — source interpretation is the subject, not a side task. Economics (ch9) runs on **data**: demand/supply schedules (tables), price-quantity graphs (≈78 figures), equilibrium diagrams. A student who cannot read a schedule or a curve cannot do the chapter. Each sub-discipline carries its own characteristic stimulus — History a primary source, Economics a table/graph, Geography a map or climate figure, Civics a constitutional/legal text or case.

**C. They are longer and denser.** ch5 ≈ 11.6k words versus ~7-unit middle chapters, and richer embedded apparatus (ch5: 5× THINK ABOUT IT, 6× DON'T MISS OUT, 3× LET'S EXPLORE, LET'S ANALYSE; ch9 similar plus tables and graphs). More sections → more units → a bigger edge graph. But the higher demand means more LOs qualify for the high-value assessment slots, so the "concentrated-central" feasibility worry *eases* at secondary.

The middle template is MCQ-forward (Present competency = 2 MCQ only; Substantive = 2 MCQ + 1 SCR). Applied to these chapters, that under-assesses the analytical work the text itself models.

---

## 3. Current state — what exists, what is missing

- **Reusable as-is:** the competency-mapping constitution already declares "Middle Stage – Secondary Stage" (stage-agnostic weight rules 3/2/1 = Central/Substantive/Present).
- **Missing (prerequisites — see §6):** there is **no secondary CG document, no secondary pedagogy document, no secondary LP or assessment constitution, and no processed IX chapters** in the repo. Secondary SS is greenfield. The framework docs are the gating dependency: mapping and LP both need the secondary CG and pedagogy text as inputs.

The upside of greenfield: we design secondary *right from the start* — the edge model, deterministic selection, and the two shifts below are built in, never retrofitted.

---

## PART A — Assessment revamp for secondary

### A1. Recalibrate the type mix, keep the counts

Hold the item **counts per weight identical to middle** (Central 5, Substantive 3, Present 2) so the deterministic selection, total-length logic, and Open-Task assignment are untouched — but shift the **type mix** up the constructed/source ladder:

| Weight | Middle (current) | Secondary (proposed) |
|---|---|---|
| Central (3) | 2 MCQ + 1 SCR + 1 ECR + 1 Open Task | **1 MCQ + 1 SCR + 1 Source + 1 ECR + 1 Open Task** |
| Substantive (2) | 2 MCQ + 1 SCR | **1 MCQ + 1 (Source or ECR) + 1 SCR** |
| Present (1) | 2 MCQ | **1 MCQ + 1 SCR** |

Rationale: no competency at secondary is assessed by recognition alone (Present loses its second MCQ to an SCR); every Central competency carries at least one source/data act; MCQ drops from the dominant format to one calibration anchor per competency. Counts are unchanged, so **Rule 4/5/6 of the middle constitution port verbatim** — only the slot *labels* change. (The exact mix is a founder knob — §7.)

### A2. Make SOURCE_INTERPRETATION a first-class item type

Middle offers "source analysis" only as one option inside the single Open Task. Secondary needs it as its own type, appearing in the Central and Substantive tiers:

- **Stimulus + 2–4 structured sub-questions of ascending demand** (read → infer → evaluate).
- **Sub-discipline-aware stimulus**, chosen from the LO's own section: History → a short primary source (inscription, account, document); Economics → a data table/schedule or a graph; Geography → a map or climate/distribution figure; Civics → a constitutional/legal excerpt or case vignette.
- It still obeys every crown-jewel rule: generated FROM one LO, inheriting its competency/unit/demand; singular `period_ref`; demand ≤ LO demand.

This is the single genuinely new type. (Alternative, if you prefer minimal surface area: don't add a type — instead elevate the existing Open-Task "source analysis" option and add a *stimulus-bearing* SCR/ECR variant. Trade-off in §7.)

### A3. Broaden the stimulus schema

Middle's `visual_stimulus` carries only pipe-delimited tables. Secondary must carry the sub-discipline stimuli above. Extend it to a typed stimulus: `{ type: source_text | table | figure | map, payload }` — where `figure` supplies the underlying data points a student reads (not a prose description), aligning with the engine's existing typed-stimulus renderer (svg / table / prose). History source excerpts travel as `source_text`; Economics schedules as `table`, curves as `figure`.

### A4. Raise the cognitive-demand floor

Every competency's item set must include **at least one Analysis-or-higher item**, and **no MCQ below Understanding**. This is feasible precisely because secondary LOs skew high (the LP's demand field, §B1). The middle ceiling rule (item demand ≤ LO demand) is retained unchanged — we are raising the floor, not the ceiling.

### A5. Carry over the crown jewels verbatim

Edge inheritance (Rule 2), deterministic LO-to-slot selection with saturate/spread/demand-match/surplus-reuse (Rule 5), singular linkage as identity (Rule 6), MCQ distractor design (Rule 7), the guide layer (Rule 9), inclusivity (Rule 10). **No change.** These are what made the middle output model-independent; they must not be reopened.

### A6. Add a deterministic count validator (bake in now)

The VI ch-6 comparison proved a strong model (Sonnet) will silently under-deliver an *explicitly stated* exact-count rule (18 items vs 22; three competencies short), while another (Opus) hit it exactly. The lesson: countable constraints belong enforced in code, not trusted to the model. Secondary should ship with a post-generation validator that checks each competency's item counts and type mix against its weight template and regenerates/flags any shortfall — before the plan is ever saved. (This equally benefits middle; propose it as shared infrastructure.)

### A7. Big Questions — synthesis framing, not structure

Per the founder's decision, Big Questions are **not** a spine. But at secondary they are the chapter's declared inquiry outcomes, so use them in exactly one bounded place: as optional framing for the single **Open Task**, whose LO already lives at the culminating unit. The Open Task may be phrased to synthesise toward a Big Question, while still anchoring (singular) to its source LO's unit, with any content breadth recorded in the guide block — never in `period_ref`. No structural role; framing only.

### A8. Scope stays formative

Retain the middle scope boundary (Rule 11): chapter-scoped formative assessment only — no summative/board/HPC/portfolio generation. The source-interpretation type builds board-readiness as a by-product without crossing into summative territory.

---

## PART B — Lesson-Plan constitution changes for secondary

The middle LP v2.7 is strong and mostly ports as-is (edge model, section anchoring, full-section coverage, coverage handoff, time-band substance Rule 13, teacher notes, homework, approach diversity). Five adaptations:

### B1. Raise the cognitive floor

Rule 2 currently allows "apply, analyse, connect, construct, evaluate, or produce." At secondary, tilt the norm toward **analyse / evaluate / construct**, and let each unit's edge demand reflect it. This is what feeds the assessment's higher floor (A4): the LP's `cognitive_demand` field is the supply of high-value LOs the source/ECR/Open-Task slots draw on.

### B2. Integrate the section's own pedagogical apparatus

The IX chapters carry rich embedded prompts (THINK ABOUT IT, LET'S EXPLORE, LET'S ANALYSE, DON'T MISS OUT). The best middle-run time-bands already leaned on these ("using the Think About It question from the section as the organising prompt"). Make it explicit in the time-band-substance rule: **where a section carries its own apparatus box, the unit should use it as the activity's scaffold or prompt rather than inventing a parallel one.** This raises executability and anchors the lesson to the book the teacher actually holds.

### B3. Surface source/data/map exposure

Because secondary assessment leans on source and data interpretation, the LP must ensure the units that expose students to a **primary source, data table, graph, or map** are identifiable — so those source-item LOs have a genuine home. Lightest touch: require `section_context` to name the source/data/map when the section contains one (no schema change; it already names "key artefacts, places, events"). This connects the teaching layer to the assessment's new stimulus need without adding a field.

### B4. Big Questions as orientation only

Mirror A7 on the teaching side: the opening unit may orient to the chapter's Big Questions and the culminating unit may synthesise them, expressed in `teacher_notes` — never as a grouping axis or a required structure. Orientation, not scaffolding.

### B5. Budget realism for longer chapters

Secondary chapters routinely need 11–15+ units. Rule 4 (full-section coverage, no front-loading, `section_coverage_note` on shortfall) already handles this correctly — but the guidance should acknowledge the larger arc so the model spreads evenly across a longer chapter rather than pacing to a middle-length one.

Everything else in LP v2.7 — the edge model, one-LO-per-edge, section anchoring, coverage handoff, homework, inclusivity's absence from the LP (kept in assessment only) — **carries over unchanged.**

---

## PART C — Prerequisites & sequencing

Because secondary is greenfield, the constitutions cannot be tested until their inputs exist. Recommended order:

1. **Extract the secondary framework docs** — the NCF secondary SS **CG document** and **pedagogy document** into `data/content/framework/social_sciences/secondary/` (mirrors the middle layout). *Gating dependency for everything below.*
2. **Process 2–3 IX chapters** through Steps 1–2 (chapter summary + competency mapping) — the mapping constitution already covers secondary; ch5 (History) and ch9 (Economics) are the natural first pair (maximally different sub-disciplines).
3. **Write the secondary LP + assessment constitutions** from this proposal (a Fable brief, as with middle).
4. **Test-generate ch5 and ch9** on Opus 4.8, then run the same compliance + thinness audit used on VI ch-6, plus a new source-item check.
5. **Only then tune** the type-mix numbers (A1) against real output.

---

## PART D — Open decisions for the founder

1. **Item type mix (A1).** Adopt the proposed 5/3/2 relabelling, or a different balance? (Counts stay 5/3/2 regardless — only the mix is in question.)
2. **New type vs. elevated Open Task (A2).** Add `SOURCE_INTERPRETATION` as a first-class fifth type (cleaner pedagogy, more schema/selection surface), or fold source work into an elevated Open Task + a stimulus-bearing SCR/ECR (smaller surface, less explicit)?
3. **How high to raise the MCQ floor (A4).** "No MCQ below Understanding" — comfortable, or hold some Recall MCQs for foundational facts at secondary?
4. **Validator scope (A6).** Ship the deterministic count validator for secondary only, or retrofit middle at the same time (recommended)?

---

## Success test

After the secondary build, it should be **impossible** to produce an assessment for an IX chapter that (a) tests a competency the anchoring unit does not develop — the edge-model guarantee — or (b) assesses a source-heavy chapter (ch5, ch9) entirely through recognition-level MCQs. The first is inherited from the middle design; the second is the whole point of this revamp.
