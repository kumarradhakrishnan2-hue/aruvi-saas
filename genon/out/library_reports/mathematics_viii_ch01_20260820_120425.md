# Library certification · mathematics VIII ch 1 · 20260820_120425

plan: counts [9, 7, 5] · basis authored_standard · registry 11 sections

PASS  library complete: ['ch_01_canonical.json', 'ch_01_canonical_p07.json', 'ch_01_canonical_p05.json'] vs plan [9, 7, 5]
serve granularity: unit  ·  section axis: True
PASS  ch_01_canonical.json: every section the chapter summary carries is anchored by some unit (11 summary section(s) vs 11 registry entr(ies))
PASS  ch_01_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_01_canonical.json: every anchor verbatim in the top registry
PASS  ch_01_canonical.json: first-visit order follows the registry
PASS  ch_01_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_01_canonical_p07.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_01_canonical_p07.json: every anchor verbatim in the top registry
PASS  ch_01_canonical_p07.json: first-visit order follows the registry
PASS  ch_01_canonical_p07.json: coverage reaches the final registry section
PASS  ch_01_canonical_p05.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_01_canonical_p05.json: every anchor verbatim in the top registry
PASS  ch_01_canonical_p05.json: first-visit order follows the registry
PASS  ch_01_canonical_p05.json: coverage reaches the final registry section
PASS  ch_01_canonical.json: register scan reached the band text (35 band(s) read: {'activity_title': 9, 'materials': 24, 'teacher_notes': 9, 'time_bands': 35, 'homework': 3, 'visual_aids': 1})
PASS  ch_01_canonical.json: register clean (0 ban hit(s))
PASS  ch_01_canonical_p07.json: register scan reached the band text (28 band(s) read: {'activity_title': 7, 'materials': 14, 'teacher_notes': 7, 'time_bands': 28, 'homework': 2})
PASS  ch_01_canonical_p07.json: register clean (0 ban hit(s))
PASS  ch_01_canonical_p05.json: register scan reached the band text (20 band(s) read: {'activity_title': 5, 'materials': 15, 'teacher_notes': 5, 'time_bands': 20, 'homework': 3})
PASS  ch_01_canonical_p05.json: register clean (0 ban hit(s))
PASS  ch_01_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_01_canonical_p07.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_01_canonical_p05.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_01_canonical.json: no stem points at a figure the item does not carry (0 does)
PASS  ch_01_canonical_p07.json: no stem points at a figure the item does not carry (0 does)
PASS  ch_01_canonical_p05.json: no stem points at a figure the item does not carry (0 does)
PASS  ch_01_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_01_canonical.json: ['ECR'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_01_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_01_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_01_canonical_p07.json: every question_type is a known assessment type (0 not)
PASS  ch_01_canonical_p07.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_01_canonical_p07.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_01_canonical_p05.json: every question_type is a known assessment type (0 not)
PASS  ch_01_canonical_p05.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_01_canonical_p05.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_01_canonical.json: MCQ options in arrangement order
PASS  ch_01_canonical_p07.json: MCQ options in arrangement order
PASS  ch_01_canonical_p05.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"(from handoff)": 0}
      ch_01_canonical.json: 0 items vs 0 expected
      ch_01_canonical_p07.json: 0 items vs 0 expected
      ch_01_canonical_p05.json: 0 items vs 0 expected
PASS  X=3: choice set non-empty (no defensive truncation)
PASS  X=4: choice set non-empty (no defensive truncation)
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)

serve sweep: {"3": "fill/single -5s", "4": "fill/forward -2s", "5": "identity", "6": "rescue/complete (from 7)", "7": "identity", "8": "fill/forward", "9": "identity", "10": "surrender", "11": "surrender"}

options arranged: 0 of 4 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_01_canonical.json: 0 of 2 item(s) re-ordered
      ch_01_canonical_p05.json: 0 of 1 item(s) re-ordered
      ch_01_canonical_p07.json: 0 of 1 item(s) re-ordered

DETERMINISTIC CHECKS ALL PASS.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
