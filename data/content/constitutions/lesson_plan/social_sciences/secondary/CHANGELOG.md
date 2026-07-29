# Lesson-plan constitution · Social Sciences · Secondary — version history

Lifted out of the constitution on 2026-07-28. These notes are for people reading back
through why a rule exists. The constitution is a prompt: every word is paid for on each
generation call, and this block was 425 words (~573 tokens) the model was
asked to read and could not act on.

The live file keeps its `VERSION` line — certification records which version a canonical
was authored under, and `genon/make_amendments.py` matches on it.

| Version | Date | Change |
|---|---|---|
| v1.1 | 2026-07-24 | Rule 14 — band identity, role, and edge band anchoring; time input = single standard row. Serialization and input-shape only; no pedagogical rule changed. |
| v1.1.1 | 2026-07-25 | Rule 14 role guidance made definitional — arc framing removed, roles judged on a best-effort basis. Labeling only; band structure and all other rules unchanged. |
| v1.1.2 | 2026-07-25 | temporal self-containment — band text carries no calendar words and no cross-unit references; teacher notes' previous-unit link is the only cross-unit reference, always backward, never in calendar time. Register only; no pedagogical rule changed. |
| v1.2 | 2026-07-25 | roles leave the bands — Rule 14 carries identity and anchoring only; a new Rule 15 classifies every band's role in a single role_handoff emitted after the plan is complete, so authoring is never shaped by the role taxonomy. Serialization only; no pedagogical rule changed. |
| v1.2.1 | 2026-07-26 | teacher notes become position-free — the continuity link names the content it builds on, never a unit's position; positional orientation belongs exclusively to the platform, which alone knows where a timetable places each boundary. Register only; no pedagogical rule changed. |
| v1.3 | 2026-07-28 | a new Rule 16 emits unit_handoff — a title and a teacher note for every adjacent pair of units, authored after the plan is complete, so the platform can name and annotate a sitting that spans a unit boundary without an LLM in the request path. The title must refuse the conjunction AND name concrete content — abstraction is the other way to fail it. Companion output only; no pedagogical rule changed. |
| v1.4 | 2026-07-28 | duration independence — band text, teacher notes, and unit_handoff notes may no longer name a duration or clock quantity. The plan is authored at one standard duration and cut into sittings that may differ in length from it and from one another, and every band's minutes are rescaled to fit; text that states its own duration goes stale silently. Register only; no pedagogical rule changed. |
| v1.5 | 2026-07-28 | consolidation — the calendar / position / clock-quantity bans, until now restated in Rules 10, 13, and 16 with a different example list each time, are stated ONCE as THE SELF-CONTAINED REGISTER and referenced. Rule 13's padding gloss and apparatus-box prohibition fold into its mandate; Rule 16's two title failure modes become one prohibition and its anticipation ban cites Rule 15. Nothing is dropped: every prohibition survives, in one place instead of three. Rules 10, 13 and 16 fall from 175, 433 and 615 words to 85, 254 and 474; net of the new block, the three shed 16%. Structure only; no rule changed. |

## Before v1.1

Rules 1–13 as first issued (v1.0). `genon/make_amendments.py` builds the amended file from
`genon/amended/originals/lesson_plan_constitution_v1.0.txt` and hard-codes the header block
this file replaced — if that script is re-run, update it there too before its output is used
as the live constitution.
