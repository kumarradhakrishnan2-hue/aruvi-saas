# Library certification · social_sciences VII ch 5 · 20260816_092041

plan: counts [19, 15, 11] · basis authored_standard · registry 12 sections

FAIL  library complete: ['ch_05_canonical.json'] vs plan [19, 15, 11]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_05_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_05_canonical.json: every anchor verbatim in the top registry
PASS  ch_05_canonical.json: first-visit order follows the registry
PASS  ch_05_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_05_canonical.json: register scan reached the band text (76 band(s) read: {'activity_title': 19, 'materials': 30, 'teacher_notes': 19, 'time_bands': 76, 'visual_aids': 6})
FAIL  ch_05_canonical.json: register clean (2 ban hit(s))
      U4 time_bands[0] 0-8 [clock] …t you more than working alone?' Students think individually for two minutes, then share.
      U18 time_bands[0] 0-8 [clock] …r in how they built and held their empires?' Students think for two minutes.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_05_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_05_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_05_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_05_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_05_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_05_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_05_canonical.json: 14 items vs 14 expected
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

serve sweep: {"9": "fill/single -4s", "10": "fill/single -3s", "11": "fill/single -2s", "12": "fill/single -1s", "13": "fill/single -1s", "14": "fill/single", "15": "fill/single", "16": "synthesis", "17": "synthesis", "18": "synthesis", "19": "identity", "20": "surrender", "21": "surrender"}

options arranged: 10 of 10 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_05_canonical.json: 10 of 10 item(s) re-ordered
          #1 C-2.1 U1: A–D now hold ACDB · correct B -> D
          #2 C-2.1 U15: A–D now hold BCAD · correct C -> B
          #6 C-3.1 U4: A–D now hold BCAD · correct B -> A
          #7 C-3.1 U14: A–D now hold CABD · correct B -> C
          #9 C-3.2 U7: A–D now hold DACB · correct C -> C
          #10 C-3.2 U11: A–D now hold ACBD · correct B -> C
          #11 C-4.1 U4: A–D now hold BCAD · correct B -> A
          #12 C-4.1 U10: A–D now hold BDCA · correct B -> A
          #13 C-10.1 U12: A–D now hold DCBA · correct B -> C
          #14 C-10.1 U16: A–D now hold DBCA · correct B -> B

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
