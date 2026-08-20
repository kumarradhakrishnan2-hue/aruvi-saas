# Library certification · mathematics VIII ch 12 · 20260820_121543

plan: counts [16, 13, 10] · basis authored_standard · registry 2 sections

PASS  library complete: ['ch_12_canonical.json', 'ch_12_canonical_p13.json', 'ch_12_canonical_p10.json'] vs plan [16, 13, 10]
serve granularity: unit  ·  section axis: True
PASS  ch_12_canonical.json: every section the chapter summary carries is anchored by some unit (2 summary section(s) vs 2 registry entr(ies))
PASS  ch_12_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_12_canonical.json: every anchor verbatim in the top registry
PASS  ch_12_canonical.json: first-visit order follows the registry
PASS  ch_12_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_12_canonical_p13.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_12_canonical_p13.json: every anchor verbatim in the top registry
PASS  ch_12_canonical_p13.json: first-visit order follows the registry
PASS  ch_12_canonical_p13.json: coverage reaches the final registry section
PASS  ch_12_canonical_p10.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_12_canonical_p10.json: every anchor verbatim in the top registry
PASS  ch_12_canonical_p10.json: first-visit order follows the registry
PASS  ch_12_canonical_p10.json: coverage reaches the final registry section
PASS  ch_12_canonical.json: register scan reached the band text (65 band(s) read: {'activity_title': 16, 'materials': 47, 'teacher_notes': 16, 'time_bands': 65, 'homework': 2, 'visual_aids': 1})
FAIL  ch_12_canonical.json: register clean (2 ban hit(s))
      U16 teacher_notes [clock] …r problems on the board at once. Students work individually for about 18 minutes, writing full working. They then compare in pairs or threes…
      U16 teacher_notes [clock] …writing full working. They then compare in pairs or threes for about 8 minutes — any disagreement must be reconstructed step by step, not…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_12_canonical_p13.json: register scan reached the band text (50 band(s) read: {'activity_title': 13, 'materials': 33, 'teacher_notes': 13, 'time_bands': 50, 'homework': 1})
PASS  ch_12_canonical_p13.json: register clean (0 ban hit(s))
PASS  ch_12_canonical_p10.json: register scan reached the band text (40 band(s) read: {'activity_title': 10, 'materials': 31, 'teacher_notes': 10, 'time_bands': 40})
PASS  ch_12_canonical_p10.json: register clean (0 ban hit(s))
PASS  ch_12_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_12_canonical_p13.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_12_canonical_p10.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_12_canonical.json: no stem points at a figure the item does not carry (0 does)
PASS  ch_12_canonical_p13.json: no stem points at a figure the item does not carry (0 does)
PASS  ch_12_canonical_p10.json: no stem points at a figure the item does not carry (0 does)
PASS  ch_12_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_12_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_12_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_12_canonical_p13.json: every question_type is a known assessment type (0 not)
PASS  ch_12_canonical_p13.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_12_canonical_p13.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_12_canonical_p10.json: every question_type is a known assessment type (0 not)
PASS  ch_12_canonical_p10.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_12_canonical_p10.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_12_canonical.json: MCQ options in arrangement order
PASS  ch_12_canonical_p13.json: MCQ options in arrangement order
PASS  ch_12_canonical_p10.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"(from handoff)": 0}
      ch_12_canonical.json: 0 items vs 0 expected
      ch_12_canonical_p13.json: 0 items vs 0 expected
      ch_12_canonical_p10.json: 0 items vs 0 expected
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
PASS  X=18: choice set non-empty (no defensive truncation)

serve sweep: {"8": "synthesis", "9": "synthesis", "10": "identity", "11": "synthesis", "12": "synthesis", "13": "identity", "14": "synthesis", "15": "synthesis", "16": "identity", "17": "surrender", "18": "surrender"}

options arranged: 0 of 9 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_12_canonical.json: 0 of 3 item(s) re-ordered
      ch_12_canonical_p10.json: 0 of 2 item(s) re-ordered
      ch_12_canonical_p13.json: 0 of 4 item(s) re-ordered

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
