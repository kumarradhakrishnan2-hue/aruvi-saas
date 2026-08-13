# Library certification · social_sciences IX ch 1 · 20260813_180156

plan: counts [15, 12, 9] · basis authored_standard · registry 9 sections

PASS  library complete: ['ch_01_canonical.json', 'ch_01_canonical_p12.json', 'ch_01_canonical_p09.json'] vs plan [15, 12, 9]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_01_canonical.json: 1 prose lead(s) in the summary match no registry entry (10 summary section(s) vs 9 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: Secondary-Stage Social Science
PASS  ch_01_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_01_canonical.json: every anchor verbatim in the top registry
PASS  ch_01_canonical.json: first-visit order follows the registry
PASS  ch_01_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_01_canonical_p12.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_01_canonical_p12.json: every anchor verbatim in the top registry
PASS  ch_01_canonical_p12.json: first-visit order follows the registry
PASS  ch_01_canonical_p12.json: coverage reaches the final registry section
PASS  ch_01_canonical_p09.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_01_canonical_p09.json: every anchor verbatim in the top registry
PASS  ch_01_canonical_p09.json: first-visit order follows the registry
PASS  ch_01_canonical_p09.json: coverage reaches the final registry section
PASS  ch_01_canonical.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 24, 'teacher_notes': 15, 'time_bands': 60, 'visual_aids': 4})
FAIL  ch_01_canonical.json: register clean (1 ban hit(s))
      U13 teacher_notes [completion] Having covered all four disciplines, this unit turns to the chapter's explicit…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_01_canonical_p12.json: register scan reached the band text (48 band(s) read: {'activity_title': 12, 'materials': 28, 'teacher_notes': 12, 'time_bands': 48, 'visual_aids': 4})
PASS  ch_01_canonical_p12.json: register clean (0 ban hit(s))
PASS  ch_01_canonical_p09.json: register scan reached the band text (36 band(s) read: {'activity_title': 9, 'materials': 19, 'teacher_notes': 9, 'time_bands': 36, 'visual_aids': 2})
PASS  ch_01_canonical_p09.json: register clean (0 ban hit(s))
PASS  ch_01_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_01_canonical_p12.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_01_canonical_p09.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_01_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_01_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_01_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_01_canonical_p12.json: every question_type is a known assessment type (0 not)
PASS  ch_01_canonical_p12.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_01_canonical_p12.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_01_canonical_p09.json: every question_type is a known assessment type (0 not)
PASS  ch_01_canonical_p09.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_01_canonical_p09.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_01_canonical.json: MCQ options in arrangement order
PASS  ch_01_canonical_p12.json: MCQ options in arrangement order
PASS  ch_01_canonical_p09.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: constitution
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_01_canonical.json: 20 items vs 20 expected
      ch_01_canonical_p12.json: 20 items vs 20 expected  <-- MISS
          C-1.4 (Substantive) has 2, constitution says 3
          C-4.4 (Substantive) has 4, constitution says 3
      ch_01_canonical_p09.json: 26 items vs 20 expected  <-- MISS
          C-4.4 (Substantive) has 5, constitution says 3
          C-5.4 (Substantive) has 5, constitution says 3
          C-7.1 (Substantive) has 5, constitution says 3
      -> 5 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)
PASS  X=12: choice set non-empty (no defensive truncation)
PASS  X=13: choice set non-empty (no defensive truncation)
PASS  X=14: choice set non-empty (no defensive truncation)
PASS  X=15: choice set non-empty (no defensive truncation)
PASS  X=16: choice set non-empty (no defensive truncation)
PASS  X=17: choice set non-empty (no defensive truncation)

serve sweep: {"7": "fill/single -2s", "8": "fill/single -1s", "9": "identity", "10": "rescue/complete (from 12)", "11": "fill/single -1s", "12": "identity", "13": "rescue/complete (from 15)", "14": "fill/single", "15": "identity", "16": "surrender", "17": "surrender"}

options arranged: 0 of 22 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_01_canonical.json: 0 of 6 item(s) re-ordered
      ch_01_canonical_p09.json: 0 of 9 item(s) re-ordered
      ch_01_canonical_p12.json: 0 of 7 item(s) re-ordered

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
