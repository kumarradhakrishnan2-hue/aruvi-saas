# Library certification · mathematics VIII ch 13 · 20260820_133215

plan: counts [6, 4] · basis authored_standard · registry 6 sections

PASS  library complete: ['ch_13_canonical.json', 'ch_13_canonical_p04.json'] vs plan [6, 4]
serve granularity: unit  ·  section axis: True
PASS  ch_13_canonical.json: every section the chapter summary carries is anchored by some unit (6 summary section(s) vs 6 registry entr(ies))
PASS  ch_13_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_13_canonical.json: every anchor verbatim in the top registry
PASS  ch_13_canonical.json: first-visit order follows the registry
PASS  ch_13_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_13_canonical_p04.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_13_canonical_p04.json: every anchor verbatim in the top registry
PASS  ch_13_canonical_p04.json: first-visit order follows the registry
PASS  ch_13_canonical_p04.json: coverage reaches the final registry section
PASS  ch_13_canonical.json: register scan reached the band text (25 band(s) read: {'activity_title': 6, 'materials': 13, 'teacher_notes': 6, 'time_bands': 25, 'homework': 4, 'visual_aids': 1})
PASS  ch_13_canonical.json: register clean (0 ban hit(s))
PASS  ch_13_canonical_p04.json: register scan reached the band text (17 band(s) read: {'activity_title': 4, 'materials': 10, 'teacher_notes': 4, 'time_bands': 17, 'homework': 4})
PASS  ch_13_canonical_p04.json: register clean (0 ban hit(s))
PASS  ch_13_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_13_canonical_p04.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_13_canonical.json: no stem points at a figure the item does not carry (0 does)
PASS  ch_13_canonical_p04.json: no stem points at a figure the item does not carry (0 does)
PASS  ch_13_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_13_canonical.json: ['MCQ'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_13_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_13_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_13_canonical_p04.json: every question_type is a known assessment type (0 not)
PASS  ch_13_canonical_p04.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_13_canonical_p04.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_13_canonical.json: MCQ options in arrangement order
PASS  ch_13_canonical_p04.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"(from handoff)": 0}
      ch_13_canonical.json: 0 items vs 0 expected
      ch_13_canonical_p04.json: 0 items vs 0 expected
PASS  X=2: choice set non-empty (no defensive truncation)
PASS  X=3: choice set non-empty (no defensive truncation)
PASS  X=4: choice set non-empty (no defensive truncation)
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)

serve sweep: {"2": "fill/single -3s", "3": "fill/forward -1s", "4": "identity", "5": "fill/forward", "6": "identity", "7": "surrender", "8": "surrender"}

options arranged: 0 of 1 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_13_canonical.json: 0 of 1 item(s) re-ordered
      ch_13_canonical_p04.json: 0 of 0 item(s) re-ordered

DETERMINISTIC CHECKS ALL PASS.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
