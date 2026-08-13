# Library certification · social_sciences IX ch 8 · 20260813_175729

plan: counts [7, 4] · basis authored_standard · registry 10 sections

PASS  library complete: ['ch_08_canonical.json', 'ch_08_canonical_p04.json'] vs plan [7, 4]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_08_canonical.json: 1 prose lead(s) in the summary match no registry entry (11 summary section(s) vs 10 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: Economic Survey
PASS  ch_08_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_08_canonical.json: every anchor verbatim in the top registry
PASS  ch_08_canonical.json: first-visit order follows the registry
PASS  ch_08_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_08_canonical_p04.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_08_canonical_p04.json: every anchor verbatim in the top registry
PASS  ch_08_canonical_p04.json: first-visit order follows the registry
PASS  ch_08_canonical_p04.json: coverage reaches the final registry section
PASS  ch_08_canonical.json: register scan reached the band text (28 band(s) read: {'activity_title': 7, 'materials': 27, 'visual_aids': 6, 'teacher_notes': 7, 'time_bands': 28})
PASS  ch_08_canonical.json: register clean (0 ban hit(s))
PASS  ch_08_canonical_p04.json: register scan reached the band text (16 band(s) read: {'activity_title': 4, 'materials': 12, 'visual_aids': 4, 'teacher_notes': 4, 'time_bands': 16, 'homework': 1})
PASS  ch_08_canonical_p04.json: register clean (0 ban hit(s))
PASS  ch_08_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_08_canonical_p04.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_08_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_08_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_08_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_08_canonical_p04.json: every question_type is a known assessment type (0 not)
PASS  ch_08_canonical_p04.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_08_canonical_p04.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_08_canonical.json: MCQ options in arrangement order
PASS  ch_08_canonical_p04.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: constitution
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_08_canonical.json: 10 items vs 10 expected
      ch_08_canonical_p04.json: 10 items vs 10 expected
PASS  X=2: choice set non-empty (no defensive truncation)
PASS  X=3: choice set non-empty (no defensive truncation)
PASS  X=4: choice set non-empty (no defensive truncation)
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)

serve sweep: {"2": "fill/single -7s", "3": "fill/forward -4s", "4": "identity", "5": "fill/forward", "6": "fill/single", "7": "identity", "8": "surrender", "9": "surrender"}

options arranged: 0 of 6 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_08_canonical.json: 0 of 3 item(s) re-ordered
      ch_08_canonical_p04.json: 0 of 3 item(s) re-ordered

DETERMINISTIC CHECKS ALL PASS.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
