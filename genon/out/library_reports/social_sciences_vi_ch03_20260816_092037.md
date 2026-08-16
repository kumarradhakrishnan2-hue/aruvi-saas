# Library certification · social_sciences VI ch 3 · 20260816_092037

plan: counts [17, 14, 10] · basis authored_standard · registry 7 sections

FAIL  library complete: ['ch_03_canonical.json'] vs plan [17, 14, 10]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_03_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_03_canonical.json: every anchor verbatim in the top registry
PASS  ch_03_canonical.json: first-visit order follows the registry
PASS  ch_03_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_03_canonical.json: register scan reached the band text (68 band(s) read: {'activity_title': 17, 'materials': 36, 'visual_aids': 16, 'teacher_notes': 17, 'time_bands': 68})
FAIL  ch_03_canonical.json: register clean (2 ban hit(s))
      U6 teacher_notes [forward] …an is important groundwork for the livelihood discussion in the next unit.
      U12 time_bands[1] 8-20 [clock] …desert? What features would they need?' Students brainstorm for three minutes, then teacher confirms with textbook-level content: sparse,…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_03_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_03_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_03_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_03_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_03_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_03_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_03_canonical.json: 15 items vs 15 expected
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

serve sweep: {"8": "fill/single -1s", "9": "fill/single -1s", "10": "fill/single", "11": "synthesis", "12": "synthesis", "13": "synthesis", "14": "synthesis", "15": "synthesis", "16": "synthesis", "17": "identity", "18": "surrender", "19": "surrender"}

options arranged: 10 of 10 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_03_canonical.json: 10 of 10 item(s) re-ordered
          #1 C-6.4 U4: A–D now hold BDCA · correct A -> D
          #2 C-6.4 U11: A–D now hold BACD · correct A -> B
          #6 C-6.1 U3: A–D now hold CBAD · correct A -> C
          #7 C-6.1 U9: A–D now hold DABC · correct B -> C
          #9 C-7.2 U5: A–D now hold CDAB · correct A -> C
          #10 C-7.2 U10: A–D now hold CABD · correct A -> B
          #12 C-6.2 U7: A–D now hold BDAC · correct A -> C
          #13 C-6.2 U7: A–D now hold BADC · correct B -> A
          #14 C-7.1 U4: A–D now hold BCAD · correct B -> A
          #15 C-7.1 U16: A–D now hold ACDB · correct A -> A

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
