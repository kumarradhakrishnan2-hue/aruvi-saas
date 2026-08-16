# Library certification · social_sciences VI ch 4 · 20260816_092037

plan: counts [15, 12, 9] · basis authored_standard · registry 5 sections

FAIL  library complete: ['ch_04_canonical.json'] vs plan [15, 12, 9]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_04_canonical.json: 1 prose lead(s) in the summary match no registry entry (1 summary section(s) vs 5 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section
      ADVISORY ch_04_canonical.json: 5 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): How Do We Learn About the Past?; How Is Time Measured in History?; What Are the Sources of History?; The Beginnings of Human History; The First Crops
PASS  ch_04_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_04_canonical.json: every anchor verbatim in the top registry
PASS  ch_04_canonical.json: first-visit order follows the registry
PASS  ch_04_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_04_canonical.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 44, 'visual_aids': 11, 'teacher_notes': 15, 'time_bands': 60})
PASS  ch_04_canonical.json: register clean (0 ban hit(s))
PASS  ch_04_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_04_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_04_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_04_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_04_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_04_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_04_canonical.json: 13 items vs 13 expected
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

serve sweep: {"7": "fill/single -1s", "8": "fill/single -1s", "9": "fill/single", "10": "fill/single", "11": "synthesis", "12": "synthesis", "13": "synthesis", "14": "synthesis", "15": "identity", "16": "surrender", "17": "surrender"}

options arranged: 8 of 8 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_04_canonical.json: 8 of 8 item(s) re-ordered
          #1 C-1.1 U5: A–D now hold CDBA · correct A -> D
          #2 C-1.1 U6: A–D now hold CBDA · correct C -> A
          #6 C-1.2 U3: A–D now hold ABDC · correct B -> B
          #7 C-1.2 U4: A–D now hold ADCB · correct B -> D
          #9 C-3.1 U10: A–D now hold BACD · correct A -> B
          #10 C-3.1 U11: A–D now hold CBAD · correct A -> C
          #12 C-5.1 U12: A–D now hold CBDA · correct B -> B
          #13 C-5.1 U12: A–D now hold CDAB · correct B -> D

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
