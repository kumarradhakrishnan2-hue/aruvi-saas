# Library certification · social_sciences IX ch 4 · 20260812_162653

plan: counts [19, 15, 11] · basis authored_standard · registry 16 sections

FAIL  library complete: ['ch_04_canonical.json'] vs plan [19, 15, 11]
serve granularity: unit  ·  section axis: True
PASS  ch_04_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_04_canonical.json: every anchor verbatim in the top registry
PASS  ch_04_canonical.json: first-visit order follows the registry
PASS  ch_04_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_04_canonical.json: register scan reached the band text (76 band(s) read: {'activity_title': 19, 'materials': 38, 'visual_aids': 19, 'teacher_notes': 19, 'time_bands': 76})
FAIL  ch_04_canonical.json: register clean (1 ban hit(s))
      U8 teacher_notes [forward] …for understanding 'cultural continuity' in the civilisation sections that follow.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_04_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_04_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_04_canonical.json: ['OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_04_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_04_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_04_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: constitution
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_04_canonical.json: 28 items vs 28 expected
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
PASS  X=20: choice set non-empty (no defensive truncation)
PASS  X=21: choice set non-empty (no defensive truncation)

serve sweep: {"9": "fill/single -7s", "10": "fill/single -6s", "11": "fill/single -5s", "12": "fill/single -4s", "13": "fill/single -3s", "14": "fill/single -2s", "15": "fill/single -1s", "16": "fill/single", "17": "fill/single", "18": "synthesis", "19": "identity", "20": "surrender", "21": "surrender"}

options arranged: 10 of 10 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_04_canonical.json: 10 of 10 item(s) re-ordered
          #1 C-2.2 U4: A–D now hold ABDC · correct A -> A
          #6 C-1.2 U8: A–D now hold BDAC · correct A -> C
          #9 C-2.1 U15: A–D now hold ADCB · correct A -> A
          #12 C-2.3 U7: A–D now hold BDCA · correct A -> D
          #15 C-2.4 U13: A–D now hold DBAC · correct A -> C
          #18 C-4.4 U6: A–D now hold DCBA · correct A -> D
          #21 C-1.1 U16: A–D now hold DBAC · correct A -> C
          #23 C-1.3 U9: A–D now hold CBAD · correct A -> C
          #25 C-7.4 U14: A–D now hold CBAD · correct A -> C
          #27 C-9.1 U10: A–D now hold CABD · correct A -> B

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
