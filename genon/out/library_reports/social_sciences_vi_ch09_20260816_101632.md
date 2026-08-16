# Library certification · social_sciences VI ch 9 · 20260816_101632

plan: counts [15, 12, 9] · basis authored_standard · registry 3 sections

PASS  library complete: ['ch_09_canonical.json', 'ch_09_canonical_p12.json', 'ch_09_canonical_p09.json'] vs plan [15, 12, 9]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_09_canonical.json: 1 prose lead(s) in the summary match no registry entry (1 summary section(s) vs 3 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section
      ADVISORY ch_09_canonical.json: 3 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Family; Roles and Responsibilities; Community
PASS  ch_09_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_09_canonical.json: every anchor verbatim in the top registry
PASS  ch_09_canonical.json: first-visit order follows the registry
PASS  ch_09_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_09_canonical_p12.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_09_canonical_p12.json: every anchor verbatim in the top registry
PASS  ch_09_canonical_p12.json: first-visit order follows the registry
PASS  ch_09_canonical_p12.json: coverage reaches the final registry section
PASS  ch_09_canonical_p09.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_09_canonical_p09.json: every anchor verbatim in the top registry
PASS  ch_09_canonical_p09.json: first-visit order follows the registry
PASS  ch_09_canonical_p09.json: coverage reaches the final registry section
PASS  ch_09_canonical.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 31, 'visual_aids': 8, 'teacher_notes': 15, 'time_bands': 60})
PASS  ch_09_canonical.json: register clean (0 ban hit(s))
PASS  ch_09_canonical_p12.json: register scan reached the band text (48 band(s) read: {'activity_title': 12, 'materials': 25, 'teacher_notes': 12, 'time_bands': 48, 'visual_aids': 1})
FAIL  ch_09_canonical_p12.json: register clean (2 ban hit(s))
      U4 teacher_notes [forward] …values and external obligation, which the Tenzing story in the next unit complicates.
      U12 teacher_notes [meta-leak] …graph brings the chapter's main analytical threads together without requiring students to have been through every prior unit.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_09_canonical_p09.json: register scan reached the band text (36 band(s) read: {'activity_title': 9, 'materials': 28, 'visual_aids': 6, 'teacher_notes': 9, 'time_bands': 36})
FAIL  ch_09_canonical_p09.json: register clean (3 ban hit(s))
      U3 time_bands[1] 10-22 [clock] …uations you have actually seen or experienced.' Groups work for eight minutes, then each group shares one example; the teacher maps examp…
      U6 teacher_notes [forward] …repares students for the halma and Kamal Parmar examples in the next unit.
      U9 time_bands[1] 8-28 [clock] …prepares his response. Each group role-plays their scenario for two minutes, then writes two sentences in their notebooks: the value en…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_09_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_09_canonical_p12.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_09_canonical_p09.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_09_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_09_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_09_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_09_canonical_p12.json: every question_type is a known assessment type (0 not)
PASS  ch_09_canonical_p12.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_09_canonical_p12.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_09_canonical_p09.json: every question_type is a known assessment type (0 not)
PASS  ch_09_canonical_p09.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_09_canonical_p09.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_09_canonical.json: MCQ options in arrangement order
PASS  ch_09_canonical_p12.json: MCQ options in arrangement order
PASS  ch_09_canonical_p09.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_09_canonical.json: 14 items vs 14 expected
      ch_09_canonical_p12.json: 14 items vs 14 expected
      ch_09_canonical_p09.json: 14 items vs 14 expected
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

serve sweep: {"7": "synthesis", "8": "synthesis", "9": "identity", "10": "synthesis", "11": "synthesis", "12": "identity", "13": "synthesis", "14": "synthesis", "15": "identity", "16": "surrender", "17": "surrender"}

options arranged: 20 of 30 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_09_canonical.json: 0 of 10 item(s) re-ordered
      ch_09_canonical_p09.json: 10 of 10 item(s) re-ordered
          #1 C-4.1 U1: A–D now hold ACBD · correct B -> C
          #2 C-4.1 U7: A–D now hold BACD · correct B -> A
          #6 C-7.1 U2: A–D now hold DCAB · correct B -> D
          #7 C-7.1 U7: A–D now hold CBAD · correct B -> B
          #9 C-3.2 U8: A–D now hold DCBA · correct B -> C
          #10 C-3.2 U8: A–D now hold CDAB · correct A -> C
          #11 C-5.1 U5: A–D now hold ACBD · correct A -> A
          #12 C-5.1 U8: A–D now hold CADB · correct B -> D
          #13 C-4.2 U3: A–D now hold DACB · correct B -> D
          #14 C-4.2 U5: A–D now hold BACD · correct B -> A
      ch_09_canonical_p12.json: 10 of 10 item(s) re-ordered
          #1 C-4.1 U1: A–D now hold BACD · correct B -> A
          #2 C-4.1 U7: A–D now hold DBAC · correct B -> B
          #6 C-7.1 U2: A–D now hold DBAC · correct B -> B
          #7 C-7.1 U8: A–D now hold CADB · correct C -> A
          #9 C-3.2 U9: A–D now hold CBDA · correct C -> A
          #10 C-3.2 U10: A–D now hold ADBC · correct B -> C
          #11 C-5.1 U5: A–D now hold ACDB · correct C -> B
          #12 C-5.1 U9: A–D now hold BCDA · correct C -> B
          #13 C-4.2 U3: A–D now hold BADC · correct B -> A
          #14 C-4.2 U9: A–D now hold BCAD · correct B -> A

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
