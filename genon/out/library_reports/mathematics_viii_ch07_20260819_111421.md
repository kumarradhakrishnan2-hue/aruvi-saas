# Library certification · mathematics VIII ch 7 · 20260819_111421

plan: counts [17, 14, 10] · basis authored_standard · registry 6 sections

FAIL  library complete: ['ch_07_canonical.json'] vs plan [17, 14, 10]
serve granularity: unit  ·  section axis: True
PASS  ch_07_canonical.json: every section the chapter summary carries is anchored by some unit (6 summary section(s) vs 6 registry entr(ies))
PASS  ch_07_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_07_canonical.json: every anchor verbatim in the top registry
PASS  ch_07_canonical.json: first-visit order follows the registry
PASS  ch_07_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_07_canonical.json: register scan reached the band text (68 band(s) read: {'activity_title': 17, 'materials': 52, 'teacher_notes': 17, 'time_bands': 68})
FAIL  ch_07_canonical.json: register clean (1 ban hit(s))
      U12 teacher_notes [forward] …the reasoning to multi-step contexts and is the subject of the next unit.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_07_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_07_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_07_canonical.json: ['ECR'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_07_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_07_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_07_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"(from handoff)": 0}
      ch_07_canonical.json: 0 items vs 0 expected
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
PASS  X=19: choice set non-empty (no defensive truncation)

serve sweep: {"8": "fill/single -1s", "9": "fill/single -1s", "10": "fill/single -1s", "11": "fill/single -1s", "12": "fill/single -1s", "13": "fill/single", "14": "fill/single", "15": "fill/single", "16": "synthesis", "17": "identity", "18": "surrender", "19": "surrender"}

options arranged: 1 of 2 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_07_canonical.json: 1 of 2 item(s) re-ordered
          #1 None #1: A–D now hold DBAC · correct B -> B

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
