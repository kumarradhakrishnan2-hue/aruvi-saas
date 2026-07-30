# Assessment constitution · Social Sciences · Secondary — version history

Sidecar history per the P4 convention (docs/testing.md §3): amendment notes live here,
never in the constitution file; the `VERSION` line stays in the file. Created 2026-07-29
when the one inline v1.2 note was lifted out during the SS·secondary stage sign-off.

| Version | Date | Change |
|---|---|---|
| v1.0 | — | Rules 1–12 as first issued. |
| v1.1 | 2026-07-16 | Rule 7 · MCQ Design — new prohibition 3: the correct answer must vary in position across the assessment; distribute is_correct across labels A–D, never the same label across consecutive items (MEMORY.md amendment item 18, founder-reported audit). |
| v1.2 | 2026-07-24 | phase_ref — band-level anchoring copied verbatim from the source LO's band_refs (Rule 6, Amendment A1 schema, integrity constraints). Serialization only; no selection or design rule changed. |
| v1.3 | 2026-07-30 | MCQ position by convention — option order becomes an affirmative arrangement rule (alphabetical by text; ascending for numeric/chronological), with the correct answer taking whatever label falls out; the old prohibition ('never the same label across consecutive items') was ambiguous — MCQs are interleaved among other types — and asked the model for randomness it cannot produce (first live run: 5/6 correct answers on B). Position is now content-determined and signal-free; letter counts may still cluster by coincidence and that is compliant. Prohibition 3 softened to 'never adjust the arrangement'. |
| v1.4 | 2026-07-30 | ordering convention sharpened on probe evidence — the arrangement is named as the LAST step before emitting, explicitly includes the correct option ('never led with'), and the comparison key is 'the first word at which they differ'. Grounds: the Rs-6 MCQ probe under v1.3 arranged only 2 of 6, and 3 of the 4 failures were the same shape — DISTRACTORS correctly sorted, correct answer pulled to A (the old B-cluster simply moved to A). The remaining failures were options sharing a long stem ('Because…', 'The frigid zones lie…'), where the alphabetical key sits 30 characters in. |
