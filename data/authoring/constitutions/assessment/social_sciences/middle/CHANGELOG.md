# Assessment constitution · Social Sciences · Middle — version history

Sidecar history per the P4 convention (`docs/testing.md` §3): amendment notes live here,
never in the constitution file; the `VERSION` line stays in the file.

Created 2026-08-04 at the S2 (social_sciences · middle) stage preparation. The file carried
no in-file version-history block to lift out.

| Version | Date | Change |
|---|---|---|
| v2.4 | 2026-08-04 | **P2 — the MCQ option-order carry-forward, ported from the SS·secondary reference at its CURRENT version (v1.7), and A6 confirmed.** Rule 7 loses the position prohibition ("The correct option MUST vary in position across the assessment — distribute is_correct across labels A–D … MUST NOT place the correct answer at the same label across consecutive items", the MEMORY-item-18 rule) and gains, in its mandate, the v1.7 statement that **option order carries no meaning and is not the model's to set**: emit the four options in whatever order they were authored; uneven letters across a chapter are coincidence, not a defect. The prohibitions are numbered and gain **prohibition 2** — no option may refer to another option by its label ("both A and B", "none of the above"), the one construction a downstream sort cannot reorder without rewriting. Arrangement is a pipeline stage, not a rule: `genon/normalize_options.py` (STEP 6 of `build_library.py`, subject-agnostic) sorts, relabels and remaps the guide keys deterministically and certification gates that it ran. **Note the divergence from the P2 checklist as written in `docs/testing.md` v2.4 §3**, which still specifies A9 in its 2026-07-30 alphabetical-convention form ("options arranged alphabetically from the first word at which they differ … correct answer never led with"): that sentence was REMOVED from the reference on 2026-08-03 (SS·secondary assessment v1.6 → v1.7, ARV-D-032) precisely because prose could not carry a sort — the v1.6 library came in 15 of 18 unarranged. Porting the struck text here would have put SS·middle in direct contradiction with STEP 6. The live reference file governs; the template text is stale. **Relaxing amendment** — nothing authored under v2.3 becomes non-compliant. **A6 is a CONFIRMATION and required no edit:** every item already carries its anchor unit as `period_ref` (Rule 6 "linkage is an identity", the integrity constraints, and the A1 schema's length-one array); the file has never carried the v1.2-era band-level `phase_ref`. **P3 is N/A:** this stage is already Group A — the LP schema emits `time_bands[{minutes, activity}]`, with no `phases[` and no `description` key anywhere. No selection, design, count or guide rule changed. |

## Before v2.4

v2.3 and earlier are not recorded here. The file arrived from the prototype at v2.3 with no
in-file history block; git history under
`data/content/constitutions/assessment/social_sciences/middle/` is the only record.
Known landmarks: the **`guide.{question_type}` nesting mandate** (Rule 9 + the A1 schema,
2026-07-10 — still owed a live SS·middle generation check at this stage's C4, MEMORY.md
"★ AMENDMENTS TO BE TESTED" item 1) and the **MEMORY item-18 position prohibition**
(2026-07-16), struck at v2.4 above.
