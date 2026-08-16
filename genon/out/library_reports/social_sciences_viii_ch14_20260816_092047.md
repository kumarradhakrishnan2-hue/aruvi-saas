# Library certification · social_sciences VIII ch 14 · 20260816_092047

plan: counts [15, 12, 9] · basis authored_standard · registry 10 sections

FAIL  library complete: ['ch_14_canonical.json'] vs plan [15, 12, 9]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_14_canonical.json: 3 prose lead(s) in the summary match no registry entry (3 summary section(s) vs 10 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section; This case study; The closing recap
      ADVISORY ch_14_canonical.json: 10 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Introduction; Population Density in Cities; How do Cities Become Centres of Economic Activities?; What Leads to Urbanisation?; Cities as Cultural Hubs; Challenges Faced by Cities …
PASS  ch_14_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_14_canonical.json: every anchor verbatim in the top registry
PASS  ch_14_canonical.json: first-visit order follows the registry
PASS  ch_14_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_14_canonical.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 46, 'visual_aids': 12, 'teacher_notes': 15, 'time_bands': 60})
FAIL  ch_14_canonical.json: register clean (1 ban hit(s))
      U10 time_bands[0] 0-8 [calendar] …sks: 'If you were appointed urban planner for your own town tomorrow, what is the first question you would ask?' Students offer…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_14_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_14_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_14_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_14_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_14_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_14_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_14_canonical.json: 18 items vs 18 expected
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

serve sweep: {"7": "fill/single -5s", "8": "fill/single -4s", "9": "fill/single -3s", "10": "fill/single -2s", "11": "fill/single -1s", "12": "fill/single", "13": "synthesis", "14": "synthesis", "15": "identity", "16": "surrender", "17": "surrender"}

options arranged: 12 of 12 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_14_canonical.json: 12 of 12 item(s) re-ordered
          #1 C-9.1 U3: A–D now hold DABC · correct A -> B
          #2 C-9.1 U5: A–D now hold CBAD · correct A -> C
          #6 C-6.4 U4: A–D now hold ADBC · correct A -> A
          #7 C-6.4 U11: A–D now hold DABC · correct A -> B
          #9 C-6.3 U9: A–D now hold BADC · correct A -> B
          #10 C-6.3 U10: A–D now hold ADCB · correct A -> A
          #12 C-7.1 U7: A–D now hold BDAC · correct A -> C
          #13 C-7.1 U14: A–D now hold CBDA · correct A -> D
          #15 C-1.2 U2: A–D now hold DBAC · correct A -> C
          #16 C-1.2 U13: A–D now hold ADCB · correct A -> A
          #17 C-5.1 U8: A–D now hold CABD · correct A -> B
          #18 C-5.1 U10: A–D now hold BADC · correct A -> B

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
