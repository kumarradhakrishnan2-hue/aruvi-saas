# Library certification · social_sciences VI ch 1 · 20260816_092037

plan: counts [9, 7, 5] · basis authored_standard · registry 6 sections

FAIL  library complete: ['ch_01_canonical.json'] vs plan [9, 7, 5]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_01_canonical.json: 2 prose lead(s) in the summary match no registry entry (2 summary section(s) vs 6 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section; This subsection
      ADVISORY ch_01_canonical.json: 6 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): A Map and Its Components; Mapping the Earth; a) Understanding coordinates; b) Latitudes; c) Longitudes; Understanding Time Zones
PASS  ch_01_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_01_canonical.json: every anchor verbatim in the top registry
PASS  ch_01_canonical.json: first-visit order follows the registry
PASS  ch_01_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_01_canonical.json: register scan reached the band text (36 band(s) read: {'activity_title': 9, 'materials': 28, 'visual_aids': 9, 'teacher_notes': 9, 'time_bands': 36})
FAIL  ch_01_canonical.json: register clean (1 ban hit(s))
      U9 teacher_notes [meta-leak] …gned to be completed and checked within the sitting itself, requiring no prior draft or material.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_01_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_01_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_01_canonical.json: ['ECR', 'OPEN_TASK', 'SCR'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_01_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_01_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_01_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2}
      ch_01_canonical.json: 9 items vs 9 expected
PASS  X=3: choice set non-empty (no defensive truncation)
PASS  X=4: choice set non-empty (no defensive truncation)
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)

serve sweep: {"3": "fill/single -3s", "4": "fill/single -2s", "5": "fill/single -1s", "6": "fill/single", "7": "synthesis", "8": "synthesis", "9": "identity", "10": "surrender", "11": "surrender"}

options arranged: 4 of 6 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_01_canonical.json: 4 of 6 item(s) re-ordered
          #2 C-1.2 U7: A–D now hold ADCB · correct B -> D
          #7 C-6.1 U8: A–D now hold CABD · correct B -> C
          #8 C-10.1 U5: A–D now hold DABC · correct B -> C
          #9 C-10.1 U8: A–D now hold ACDB · correct A -> A

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
