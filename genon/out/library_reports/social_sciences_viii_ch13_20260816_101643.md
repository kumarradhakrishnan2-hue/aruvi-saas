# Library certification · social_sciences VIII ch 13 · 20260816_101643

plan: counts [11, 9, 7] · basis authored_standard · registry 8 sections

PASS  library complete: ['ch_13_canonical.json', 'ch_13_canonical_p09.json', 'ch_13_canonical_p07.json'] vs plan [11, 9, 7]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_13_canonical.json: 4 prose lead(s) in the summary match no registry entry (5 summary section(s) vs 8 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section; This subsection; This closing section; The closing recap
      ADVISORY ch_13_canonical.json: 6 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): What Is Demography?; Population at a Glance; What Determines the Population of a Country? — Birth and fertility rates; What Determines the Population of a Country? — Death or mortality rate; Migration; How Do Countries Experience Population Change?; India's Demographic Dividend — A Limited Window of Opportunity
PASS  ch_13_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_13_canonical.json: every anchor verbatim in the top registry
PASS  ch_13_canonical.json: first-visit order follows the registry
PASS  ch_13_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_13_canonical_p09.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_13_canonical_p09.json: every anchor verbatim in the top registry
PASS  ch_13_canonical_p09.json: first-visit order follows the registry
PASS  ch_13_canonical_p09.json: coverage reaches the final registry section
PASS  ch_13_canonical_p07.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_13_canonical_p07.json: every anchor verbatim in the top registry
PASS  ch_13_canonical_p07.json: first-visit order follows the registry
PASS  ch_13_canonical_p07.json: coverage reaches the final registry section
PASS  ch_13_canonical.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 28, 'teacher_notes': 11, 'time_bands': 44, 'visual_aids': 5})
PASS  ch_13_canonical.json: register clean (0 ban hit(s))
PASS  ch_13_canonical_p09.json: register scan reached the band text (45 band(s) read: {'activity_title': 9, 'materials': 21, 'visual_aids': 6, 'teacher_notes': 9, 'time_bands': 45})
PASS  ch_13_canonical_p09.json: register clean (0 ban hit(s))
PASS  ch_13_canonical_p07.json: register scan reached the band text (28 band(s) read: {'activity_title': 7, 'materials': 21, 'teacher_notes': 7, 'time_bands': 28, 'visual_aids': 4})
FAIL  ch_13_canonical_p07.json: register clean (1 ban hit(s))
      U5 teacher_notes [forward] …he visual representation of the demographic dividend, which the following unit will develop fully.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_13_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_13_canonical_p09.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_13_canonical_p07.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_13_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_13_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_13_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_13_canonical_p09.json: every question_type is a known assessment type (0 not)
PASS  ch_13_canonical_p09.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_13_canonical_p09.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_13_canonical_p07.json: every question_type is a known assessment type (0 not)
PASS  ch_13_canonical_p07.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_13_canonical_p07.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_13_canonical.json: MCQ options in arrangement order
PASS  ch_13_canonical_p09.json: MCQ options in arrangement order
PASS  ch_13_canonical_p07.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_13_canonical.json: 14 items vs 14 expected
      ch_13_canonical_p09.json: 14 items vs 14 expected
      ch_13_canonical_p07.json: 14 items vs 14 expected
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)
PASS  X=12: choice set non-empty (no defensive truncation)
PASS  X=13: choice set non-empty (no defensive truncation)

serve sweep: {"5": "fill/single -2s", "6": "fill/single -1s", "7": "identity", "8": "fill/single", "9": "identity", "10": "synthesis", "11": "identity", "12": "surrender", "13": "surrender"}

options arranged: 19 of 30 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_13_canonical.json: 0 of 10 item(s) re-ordered
      ch_13_canonical_p07.json: 10 of 10 item(s) re-ordered
          #1 C-9.1 U1: A–D now hold BACD · correct A -> B
          #2 C-9.1 U7: A–D now hold BDAC · correct B -> A
          #6 C-1.2 U2: A–D now hold ADBC · correct A -> A
          #7 C-1.2 U5: A–D now hold CDBA · correct B -> C
          #9 C-5.1 U6: A–D now hold CBDA · correct B -> B
          #10 C-5.1 U6: A–D now hold BDAC · correct B -> A
          #11 C-6.2 U1: A–D now hold BCAD · correct B -> A
          #12 C-6.2 U2: A–D now hold BDCA · correct B -> A
          #13 C-10.1 U7: A–D now hold ACBD · correct B -> C
          #14 C-10.1 U7: A–D now hold BCAD · correct B -> A
      ch_13_canonical_p09.json: 9 of 10 item(s) re-ordered
          #1 C-9.1 U1: A–D now hold CDAB · correct A -> C
          #2 C-9.1 U8: A–D now hold CBDA · correct A -> D
          #6 C-1.2 U2: A–D now hold BACD · correct A -> B
          #7 C-1.2 U5: A–D now hold BDCA · correct A -> D
          #9 C-5.1 U7: A–D now hold ACDB · correct A -> A
          #10 C-5.1 U9: A–D now hold ADBC · correct A -> A
          #12 C-6.2 U4: A–D now hold DACB · correct A -> B
          #13 C-10.1 U9: A–D now hold BCDA · correct A -> D
          #14 C-10.1 U9: A–D now hold CBAD · correct A -> C

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
