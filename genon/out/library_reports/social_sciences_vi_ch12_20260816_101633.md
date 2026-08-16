# Library certification · social_sciences VI ch 12 · 20260816_101633

plan: counts [13, 11, 8] · basis authored_standard · registry 2 sections

PASS  library complete: ['ch_12_canonical.json', 'ch_12_canonical_p11.json', 'ch_12_canonical_p08.json'] vs plan [13, 11, 8]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_12_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_12_canonical.json: every anchor verbatim in the top registry
PASS  ch_12_canonical.json: first-visit order follows the registry
PASS  ch_12_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_12_canonical_p11.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_12_canonical_p11.json: every anchor verbatim in the top registry
PASS  ch_12_canonical_p11.json: first-visit order follows the registry
PASS  ch_12_canonical_p11.json: coverage reaches the final registry section
PASS  ch_12_canonical_p08.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_12_canonical_p08.json: every anchor verbatim in the top registry
PASS  ch_12_canonical_p08.json: first-visit order follows the registry
PASS  ch_12_canonical_p08.json: coverage reaches the final registry section
PASS  ch_12_canonical.json: register scan reached the band text (52 band(s) read: {'activity_title': 13, 'materials': 39, 'visual_aids': 10, 'teacher_notes': 13, 'time_bands': 52})
PASS  ch_12_canonical.json: register clean (0 ban hit(s))
PASS  ch_12_canonical_p11.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 28, 'visual_aids': 4, 'teacher_notes': 11, 'time_bands': 44})
FAIL  ch_12_canonical_p11.json: register clean (1 ban hit(s))
      U7 teacher_notes [meta-leak] …tudents see the systematic logic of Indian local governance without requiring those units to have been covered in this class. A common confusion is t…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_12_canonical_p08.json: register scan reached the band text (32 band(s) read: {'activity_title': 8, 'materials': 16, 'visual_aids': 4, 'teacher_notes': 8, 'time_bands': 32})
PASS  ch_12_canonical_p08.json: register clean (0 ban hit(s))
PASS  ch_12_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_12_canonical_p11.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_12_canonical_p08.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_12_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_12_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_12_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_12_canonical_p11.json: every question_type is a known assessment type (0 not)
PASS  ch_12_canonical_p11.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_12_canonical_p11.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_12_canonical_p08.json: every question_type is a known assessment type (0 not)
PASS  ch_12_canonical_p08.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_12_canonical_p08.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_12_canonical.json: MCQ options in arrangement order
PASS  ch_12_canonical_p11.json: MCQ options in arrangement order
PASS  ch_12_canonical_p08.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_12_canonical.json: 10 items vs 10 expected
      ch_12_canonical_p11.json: 11 items vs 11 expected
      ch_12_canonical_p08.json: 10 items vs 10 expected
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)
PASS  X=12: choice set non-empty (no defensive truncation)
PASS  X=13: choice set non-empty (no defensive truncation)
PASS  X=14: choice set non-empty (no defensive truncation)
PASS  X=15: choice set non-empty (no defensive truncation)

serve sweep: {"6": "synthesis", "7": "synthesis", "8": "identity", "9": "synthesis", "10": "synthesis", "11": "identity", "12": "synthesis", "13": "identity", "14": "surrender", "15": "surrender"}

options arranged: 11 of 18 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_12_canonical.json: 0 of 6 item(s) re-ordered
      ch_12_canonical_p08.json: 6 of 6 item(s) re-ordered
          #1 C-4.1 U1: A–D now hold ADCB · correct A -> A
          #2 C-4.1 U6: A–D now hold BDAC · correct A -> C
          #6 C-4.2 U4: A–D now hold DBAC · correct A -> C
          #7 C-4.2 U8: A–D now hold BCDA · correct A -> D
          #9 C-8.3 U1: A–D now hold BDCA · correct A -> D
          #10 C-8.3 U2: A–D now hold ACBD · correct A -> A
      ch_12_canonical_p11.json: 5 of 6 item(s) re-ordered
          #1 C-4.1 U2: A–D now hold ABDC · correct A -> A
          #2 C-4.1 U7: A–D now hold ADCB · correct A -> A
          #6 C-4.2 U4: A–D now hold DACB · correct A -> B
          #7 C-4.2 U10: A–D now hold CABD · correct A -> B
          #10 C-8.3 U5: A–D now hold ADBC · correct A -> A

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
