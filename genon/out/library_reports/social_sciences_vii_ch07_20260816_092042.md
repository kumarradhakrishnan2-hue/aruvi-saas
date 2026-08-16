# Library certification · social_sciences VII ch 7 · 20260816_092042

plan: counts [18, 15, 11] · basis authored_standard · registry 14 sections

FAIL  library complete: ['ch_07_canonical.json'] vs plan [18, 15, 11]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_07_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_07_canonical.json: every anchor verbatim in the top registry
PASS  ch_07_canonical.json: first-visit order follows the registry
PASS  ch_07_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_07_canonical.json: register scan reached the band text (72 band(s) read: {'activity_title': 18, 'materials': 37, 'visual_aids': 11, 'teacher_notes': 18, 'time_bands': 72})
FAIL  ch_07_canonical.json: register clean (2 ban hit(s))
      U7 teacher_notes [forward] …re will resurface when they examine Nālandā and the arts in later units. A common confusion is imagining the Indian Ocean as a peri…
      U12 time_bands[0] 0-12 [clock] …y all four images simultaneously. Students observe silently for two minutes, then write: 'These four works come from different places a…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_07_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_07_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_07_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_07_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_07_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_07_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_07_canonical.json: 14 items vs 14 expected
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

serve sweep: {"9": "fill/single -5s", "10": "fill/single -4s", "11": "fill/single -3s", "12": "fill/single -2s", "13": "fill/single -1s", "14": "fill/single", "15": "synthesis", "16": "synthesis", "17": "synthesis", "18": "identity", "19": "surrender", "20": "surrender"}

options arranged: 10 of 10 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_07_canonical.json: 10 of 10 item(s) re-ordered
          #1 C-2.1 U2: A–D now hold BCAD · correct B -> A
          #2 C-2.1 U13: A–D now hold CADB · correct B -> D
          #6 C-10.1 U9: A–D now hold CDBA · correct B -> C
          #7 C-10.1 U11: A–D now hold BCAD · correct B -> A
          #9 C-3.1 U16: A–D now hold ADCB · correct B -> D
          #10 C-3.1 U5: A–D now hold BCDA · correct B -> A
          #11 C-9.1 U7: A–D now hold BADC · correct B -> A
          #12 C-9.1 U7: A–D now hold CDAB · correct B -> D
          #13 C-1.1 U3: A–D now hold CDAB · correct B -> D
          #14 C-1.1 U5: A–D now hold CADB · correct B -> D

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
