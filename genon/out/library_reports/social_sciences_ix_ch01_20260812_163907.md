# Library certification · social_sciences IX ch 1 · 20260812_163907

plan: counts [15, 12, 9] · basis authored_standard · registry 9 sections

FAIL  library complete: ['ch_01_canonical.json'] vs plan [15, 12, 9]
serve granularity: unit  ·  section axis: True
PASS  ch_01_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_01_canonical.json: every anchor verbatim in the top registry
PASS  ch_01_canonical.json: first-visit order follows the registry
PASS  ch_01_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_01_canonical.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 24, 'teacher_notes': 15, 'time_bands': 60, 'visual_aids': 4})
FAIL  ch_01_canonical.json: register clean (1 ban hit(s))
      U13 teacher_notes [completion] Having covered all four disciplines, this unit turns to the chapter's explicit…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_01_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_01_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_01_canonical.json: ['OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_01_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_01_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_01_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: constitution
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_01_canonical.json: 20 items vs 20 expected
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

serve sweep: {"7": "fill/single -4s", "8": "fill/single -4s", "9": "fill/single -3s", "10": "fill/single -3s", "11": "fill/single -2s", "12": "fill/single -1s", "13": "fill/single -1s", "14": "fill/single", "15": "identity", "16": "surrender", "17": "surrender"}

options arranged: 0 of 6 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_01_canonical.json: 0 of 6 item(s) re-ordered

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
