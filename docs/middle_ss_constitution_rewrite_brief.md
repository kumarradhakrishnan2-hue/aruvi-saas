# Brief — Rewrite the Middle Social Sciences Constitutions (Lesson Plan + Assessment)

**For:** the model tasked with writing two fresh constitutions.
**Deliverables:** two files — a new **Lesson Plan Constitution** and a new **Assessment Constitution**, both for `social_sciences`, `middle` stage.
**Do NOT touch:** the Competency Mapping Constitution and the two authoring prompts (`step_1_chapter_summary.md`, `step_2_competency_mapping.md`). They are correct and stay exactly as they are. The mapping still emits a **flat, chapter-level** competency list — `[{cg, c_code, weight, justification}]` — and nothing upstream changes.

Write both constitutions **concise, plain-spoken, and minimalist** — shorter than the current versions — while preserving every load-bearing rule named below. Mirror the existing house style (numbered rules with a MANDATE / PROHIBITION split, a short Integrity Constraints block, and a final output-schema amendment), but trim wording ruthlessly. No rule should be longer than it needs to be to be unambiguous.

---

## 1. Why we are rewriting — the one idea to internalise

The current design forces **exactly one competency onto each teaching unit** and then requires that *every* mapped competency be spent on some unit ("coverage mandate"). Those two rules together manufacture false labels: a competency that has no genuine home gets dumped on whatever unit is still open. Real example — a "trade / interconnected subcontinent" unit was stamped with the *inequality* competency purely to satisfy coverage. That wrong label then flows into the assessment and becomes a graded question that misdescribes what it measures.

**The fix is structural, not a patch. Make the Learning Outcome the *edge* of a competency ↔ unit graph.**

- A unit teaches content (a textbook section).
- A competency is realised by *some* units and not others.
- Where a unit genuinely advances a competency, that pairing **produces one Learning Outcome** — the transferable skill that unit builds toward that competency.
- The LO therefore carries **both endpoints**: its competency and its unit. They cannot disagree, because they are two ends of the same edge.

Everything below follows from this. The relationship is **many-to-many and unforced**: a unit may realise zero, one, or several competencies; a competency reaches as many units as genuinely realise it. No unit is forced to carry a competency it does not develop; no competency is forced onto a unit that does not develop it.

Keep two layers cleanly separated:
- **Teaching layer** (properties of the *unit*): section content, materials, time, **teacher notes, homework, inclusivity**.
- **Skill layer** (the *edges*): one **implied LO + cognitive demand** per (unit × competency).

The teaching-layer fields never enter competency logic or assessment selection. The edges are the only thing the assessment consumes.

---

## 2. Lesson Plan Constitution — required content

Preserve these existing principles (keep their essence, shorten their prose):
- **Vocabulary:** "unit" in all teacher-facing text; "period" only in schema field names and scheduling.
- **Content-driven age calibration** from the chapter summary (not the pedagogy doc).
- **Cognitive floor:** every activity requires apply / analyse / connect / construct / evaluate — never recall-only.
- **Strict section anchoring:** every unit draws its content from one named section of the chapter summary; competency statements are never a content source.
- **Approach diversity** across units (SS carries no approach field today — keep the principle, do not invent a field).
- **Time integrity:** total minutes = Σ(duration × count); one activity per unit; teaching budget only, no assessment time.
- **LOs are outputs, never inputs;** no external LO document is consulted.

Change these — this is the edge model:

1. **Draw edges, do not force a single competency.** For each unit, attach every mapped competency that *teaching that unit genuinely realises* — zero, one, or many. An edge is valid only when the unit's activity actually executes that competency's cognitive operation. **Reject vocabulary-only matches** (shared topic words are not enough — this is the same guard the Mapping Constitution applies, and it must now also live here). The competency set and its weights are **settled by the mapping — do not add, drop, or re-weight competencies.** Placing them onto units is the LP's job; re-selecting them is not.

2. **One implied LO per edge** (not one per unit). Each LO states the transferable skill the unit builds toward *that* competency, skill-first, in the form "Students can [skill verb phrase]," with **no chapter-specific proper nouns** (those live in `section_context`). A unit with three competency edges yields three LOs, each competency-specific.

3. **Cognitive demand is an explicit field on every LO.** Position each LO on the Recall → Understanding → Application → Analysis → Evaluation spectrum and record it as its own value — do not leave it implicit in the verb. This is a deliberate output; the assessment inherits it and must not re-adjudicate it.

4. **`section_context` stays one per unit** — the compact 10–12 word content label (key artefacts / places / events) shared by all of that unit's LOs. Skill lives on the edge; content lives on the unit.

5. **No coverage mandate, no arithmetic.** Weights signal **emphasis** (more depth / time for heavier competencies), never a formula and never a requirement to place every competency. If a mapped competency finds **no genuine unit home**, record a short `competency_gap_note` rather than force-fitting it. A unit that genuinely realises **no** competency is allowed — it is taught (notes, homework, materials) but generates no LO.

6. **Teacher notes** — one per unit, 2–3 sentences of flowing prose: a link to the previous unit, one common confusion drawn only from the chapter summary, optionally a facilitation pointer. Never cite c-codes. (Unchanged in spirit.)

7. **Homework** — per unit, optional, `[]` by default; 1–2 items only when useful; same cognitive floor as class activities; **not consumed by the assessment generator.** It is a unit property, never an edge, never assessed.

8. **Inclusivity — NEW, per unit.** A short note on making *this lesson* reachable by a diverse classroom: language support, varied representation, and accommodations grounded in the unit's own activity. Plain and practical, not boilerplate; omit (leave empty) when the unit needs none. Teaching-side only — assessment inclusivity is handled in the other constitution.

### LP output schema (per unit)

```json
{
  "period_number": 0,
  "period_duration_minutes": 0,
  "activity_title": "string",
  "section_anchor": "string — named chapter section this unit teaches",
  "materials": ["string"],
  "visual_aids": "string | null",
  "time_bands": [{ "minutes": "0-8", "activity": "string" }],
  "section_context": "string — 10–12 word content label for this unit",
  "teacher_notes": "string — 2–3 sentences, required, teacher-facing",
  "inclusivity": "string — inclusive-teaching note; empty if none",
  "homework": ["string"],
  "competency_edges": [
    {
      "c_code": "string",
      "cg": "string",
      "weight": 3,
      "competency_text": "string",
      "implied_lo": "string — skill this unit builds toward this competency; no proper nouns",
      "cognitive_demand": "Recall | Understanding | Application | Analysis | Evaluation"
    }
  ]
}
```

Also emit a chapter-level `competency_gap_note` (string, empty when none).

---

## 3. Assessment Constitution — required content

Preserve these existing principles (shorten their prose):
- **Governing purpose:** every question tests a mapped competency through an *observable* demonstration; no "did the student understand/appreciate" items.
- **Weight-driven architecture with EXACT counts** (keep as-is): Central = 2 MCQ + 1 SCR + 1 ECR + 1 Open Task; Substantive = 2 MCQ + 1 SCR; Present = 2 MCQ; Incidental = not assessed. Exactly one Open Task per assessment (assign to the Central competency with the most LOs; other Central competencies get a second ECR in its place). Weight integers never appear in output — use Central / Substantive / Present.
- **Demand spectrum** inherited from the handoff, never re-adjudicated.
- **Distractor design:** every MCQ has exactly three diagnostically intentional distractors, each a nameable engagement failure, explained in the guide block.
- **Guide block** for every item.

Change / add these:

1. **Input is the edge set.** The handoff is the LP's `competency_edges`, grouped by competency: each competency owns a set of LOs, and every LO already carries its **unit (period), cognitive demand, and `section_context`.** Plus the chapter summary for content grounding. Nothing else is retrieved.

2. **Coherence is now automatic.** An item is generated *from an LO*, and the LO carries its competency — so the item's competency always matches its source. State this as a one-line inheritance rule; the old multi-clause coherence constraint is no longer needed.

3. **Selection is a deterministic step that runs BEFORE authoring.** For each competency, assign its LOs to its weight-prescribed item slots by fixed rules, not by free choice:
   - **Saturate:** if slots ≥ LOs, use every LO once.
   - **Spread:** if LOs > slots, choose LOs distributed across the chapter's units — never first-LOs-first (that starves later units).
   - **Demand-match:** route the highest-demand LOs to the highest-demand slots (Open Task, ECR); MCQ / SCR take the rest. An item's demand must be **at or below** its LO's demand — never above (never assess deeper than the unit taught).
   - **Surplus (slots > LOs):** fill extra slots by **reusing a single LO at a lower demand rung** — never by synthesising across multiple LOs. (Synthesis would give an item two units and break linkage; see rule 4.)
   - **Coverage preference:** where the rules leave a choice, prefer the assignment that leaves the fewest units un-probed.

4. **One item ← one LO → one unit. Linkage is an identity.** Each item's `period_ref` is the **single** unit of its LO, and that is its display anchor. No item spans multiple units for the purpose of anchoring. (If a question legitimately draws *content* from other sections, name them in the guide block — never in `period_ref`.) This makes 100% unit linkage true by construction, with no tie-break needed.

5. **`implied_lo` is single and verbatim** — copied from the chosen edge, not paraphrased. `cognitive_demand` is inherited from that edge.

6. **Inclusivity — NEW, per item.** A short note on making *this question* fair and reachable: alternative response modes, unbiased stimulus, language scaffolding. Omit when not needed. Assessment-side only.

### Assessment output schema (per item)

```json
{
  "question_type": "MCQ | SCR | ECR | OPEN_TASK",
  "weight_label": "Central | Substantive | Present",
  "competency": { "c_code": "string", "cg": "string", "competency_text": "string" },
  "implied_lo": "string — verbatim from the source edge",
  "cognitive_demand": "Recall | Understanding | Application | Analysis | Evaluation",
  "period_ref": [0],
  "chapter_section": "string",
  "question_text": "string",
  "options": ["string"],
  "expected_elements": ["string"],
  "look_for": ["string"],
  "task": "string",
  "scaffold": "string",
  "format_of_output": "string",
  "visual_stimulus": "string | null",
  "inclusivity": "string — inclusive-assessment note; empty if none",
  "guide": { }
}
```

`period_ref` is an array of length one for schema stability, but must contain exactly the LO's single unit.

---

## 4. Writing instructions (style)

- **Concise and minimalist.** Aim shorter than the current constitutions. Prefer one crisp sentence over three careful ones. Cut restatement.
- **Plain language.** Simple words; no jargon the essence doesn't require.
- **Keep the house structure** — numbered MANDATE / PROHIBITION rules, an Integrity Constraints block, a final output-schema amendment — but only as many rules as the content genuinely needs.
- **Lose nothing essential.** Every preserved principle listed above must survive, and every changed/new rule must be stated unambiguously. Brevity is the goal; omission of substance is not.
- **Do not reference or alter** the Mapping Constitution or the two prompts. Assume the flat chapter-level competency list as the given input.

---

## 5. One-line test of success

After the rewrite, it should be **impossible** to produce an assessment item whose competency the anchoring unit does not genuinely develop — because the LO that generated the item is the edge that binds the two together. If a reviewer can still construct that mismatch on paper, the edge model has not been captured.
