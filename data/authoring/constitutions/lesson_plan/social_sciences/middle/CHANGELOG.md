# Lesson-plan constitution · Social Sciences · Middle — version history

Sidecar history per the P4 convention (`docs/testing.md` §3): amendment notes live here,
never in the constitution file; the `VERSION` line stays in the file — certification records
which version a canonical was authored under.

Created 2026-08-04 at the S2 (social_sciences · middle) stage preparation. The file carried
no in-file version-history block to lift out, so nothing was removed from the constitution to
make this sidecar.

| Version | Date | Change |
|---|---|---|
| v2.8 | 2026-08-04 | **The variant-canonical carry-forward (P1), ported from the SS·secondary v1.10 reference.** Two amendments and their dependent references, nothing else. **A1** — INPUTS 4 becomes exactly ONE standard period row (the class-standard duration × count; 40 min ≤VII, 45 VIII, 50 IX), replacing "one or more rows"; the A1 schema preamble and `period_schedule` comment say so; the INTEGRITY TIME constraint restates it as a single row (`total minutes = duration × count`, `total unit count = count`) in place of the Σ-over-rows form. Every variant is authored at the class-standard duration and the serve engine handles all timetable variation, so a second row now has no meaning. **A5 + A7** — THE SELF-CONTAINED REGISTER arrives as ONE block after VOCABULARY, in the v1.10 three-ban re-cut: (1) no clock quantity, (2) no forward reference or completion language, (3) no calendar time. Backward continuity is welcome and is best carried by naming the content built on. The block binds Rules 10 and 13, each of which gains `MUST NOT breach THE SELF-CONTAINED REGISTER` (Rule 13's as prohibition 4, beside its existing padding ceiling). Rule 10's continuity link is restated as the register's companion — a link to the content already taught, named by that content itself, never by its position — and VOCABULARY drops its now-contradicted example `cross-references such as "the previous unit"` and adds `"session" is outside the register too`. Register and input-shape only; **no pedagogical rule changed** — Rules 1–9, 11, 12, the edge model, A1's field set and A2 are untouched. Amendments A2, A3 and A4 are cancelled for this file and were not ported; no V-rule (variant brief, section registry, synthesis mandate, per-variant assessment) is in the constitution — the V-series is carried entirely by the platform-composed brief. |

## Before v2.8

v2.7 and earlier are not recorded here. The file arrived from the prototype at v2.7 with no
in-file history block; the git history under
`data/content/constitutions/lesson_plan/social_sciences/middle/` is the only record.
Known landmark: **v2.7 (2026-07-15)** added `pedagogical_approaches` — a list of 1-to-few
approaches named verbatim from the NCF Pedagogy document, which the SS port joins with "; "
into `Period.approach` (CLAUDE.md §3).
