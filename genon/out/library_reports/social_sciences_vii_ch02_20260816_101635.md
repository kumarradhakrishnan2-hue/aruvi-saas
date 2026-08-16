# Library certification · social_sciences VII ch 2 · 20260816_101635

plan: counts [9, 7, 5] · basis authored_standard · registry 4 sections

PASS  library complete: ['ch_02_canonical.json', 'ch_02_canonical_p07.json', 'ch_02_canonical_p05.json'] vs plan [9, 7, 5]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_02_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_02_canonical.json: every anchor verbatim in the top registry
PASS  ch_02_canonical.json: first-visit order follows the registry
PASS  ch_02_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_02_canonical_p07.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_02_canonical_p07.json: every anchor verbatim in the top registry
PASS  ch_02_canonical_p07.json: first-visit order follows the registry
PASS  ch_02_canonical_p07.json: coverage reaches the final registry section
PASS  ch_02_canonical_p05.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_02_canonical_p05.json: every anchor verbatim in the top registry
PASS  ch_02_canonical_p05.json: first-visit order follows the registry
PASS  ch_02_canonical_p05.json: coverage reaches the final registry section
PASS  ch_02_canonical.json: register scan reached the band text (36 band(s) read: {'activity_title': 9, 'materials': 31, 'visual_aids': 7, 'teacher_notes': 9, 'time_bands': 36})
PASS  ch_02_canonical.json: register clean (0 ban hit(s))
PASS  ch_02_canonical_p07.json: register scan reached the band text (28 band(s) read: {'activity_title': 7, 'materials': 22, 'visual_aids': 7, 'teacher_notes': 7, 'time_bands': 28})
FAIL  ch_02_canonical_p07.json: register clean (1 ban hit(s))
      U1 teacher_notes [forward] …agnostic of prior knowledge and sets up instrument study in later units.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_02_canonical_p05.json: register scan reached the band text (20 band(s) read: {'activity_title': 5, 'materials': 16, 'visual_aids': 5, 'teacher_notes': 5, 'time_bands': 20})
FAIL  ch_02_canonical_p05.json: register clean (1 ban hit(s))
      U5 time_bands[2] 22-32 [clock] …onger support from the text. Writers revise their paragraph for three minutes based on the partner's marks. Final paragraphs are handed t…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_02_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_02_canonical_p07.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_02_canonical_p05.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_02_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_02_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_02_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_02_canonical_p07.json: every question_type is a known assessment type (0 not)
PASS  ch_02_canonical_p07.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_02_canonical_p07.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_02_canonical_p05.json: every question_type is a known assessment type (0 not)
PASS  ch_02_canonical_p05.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_02_canonical_p05.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_02_canonical.json: MCQ options in arrangement order
PASS  ch_02_canonical_p07.json: MCQ options in arrangement order
PASS  ch_02_canonical_p05.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2}
      ch_02_canonical.json: 7 items vs 7 expected
      ch_02_canonical_p07.json: 7 items vs 7 expected
      ch_02_canonical_p05.json: 7 items vs 7 expected
PASS  X=3: choice set non-empty (no defensive truncation)
PASS  X=4: choice set non-empty (no defensive truncation)
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)

serve sweep: {"3": "fill/single -1s", "4": "fill/single -1s", "5": "identity", "6": "rescue/complete (from 7)", "7": "identity", "8": "synthesis", "9": "identity", "10": "surrender", "11": "surrender"}

options arranged: 6 of 12 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_02_canonical.json: 0 of 4 item(s) re-ordered
      ch_02_canonical_p05.json: 2 of 4 item(s) re-ordered
          #2 C-6.1 U2: A–D now hold CBDA · correct B -> B
          #6 C-1.2 U2: A–D now hold ABDC · correct B -> B
      ch_02_canonical_p07.json: 4 of 4 item(s) re-ordered
          #1 C-6.1 U1: A–D now hold DCAB · correct C -> B
          #2 C-6.1 U2: A–D now hold DABC · correct B -> C
          #6 C-1.2 U3: A–D now hold CABD · correct B -> C
          #7 C-1.2 U3: A–D now hold ADBC · correct A -> A

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
