# Library certification · social_sciences VI ch 9 · 20260816_092039

plan: counts [15, 12, 9] · basis authored_standard · registry 3 sections

FAIL  library complete: ['ch_09_canonical.json'] vs plan [15, 12, 9]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_09_canonical.json: 1 prose lead(s) in the summary match no registry entry (1 summary section(s) vs 3 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section
      ADVISORY ch_09_canonical.json: 3 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Family; Roles and Responsibilities; Community
PASS  ch_09_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_09_canonical.json: every anchor verbatim in the top registry
PASS  ch_09_canonical.json: first-visit order follows the registry
PASS  ch_09_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_09_canonical.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 31, 'visual_aids': 8, 'teacher_notes': 15, 'time_bands': 60})
FAIL  ch_09_canonical.json: register clean (2 ban hit(s))
      U3 teacher_notes [forward] …mily experience before moving to the narrative vignettes in the next unit. A common confusion is treating dharma as a religious term…
      U5 teacher_notes [meta-leak] …ssigned. The drama-outline task lets students own the model without requiring a fully performed roleplay within the sitting.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_09_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_09_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_09_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_09_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_09_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_09_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_09_canonical.json: 14 items vs 14 expected
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

serve sweep: {"7": "fill/single", "8": "synthesis", "9": "synthesis", "10": "synthesis", "11": "synthesis", "12": "synthesis", "13": "synthesis", "14": "synthesis", "15": "identity", "16": "surrender", "17": "surrender"}

options arranged: 10 of 10 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_09_canonical.json: 10 of 10 item(s) re-ordered
          #1 C-4.1 U1: A–D now hold CADB · correct B -> D
          #2 C-4.1 U12: A–D now hold BADC · correct B -> A
          #6 C-7.1 U2: A–D now hold CABD · correct B -> C
          #7 C-7.1 U9: A–D now hold BCDA · correct B -> A
          #9 C-3.2 U10: A–D now hold BCAD · correct B -> A
          #10 C-3.2 U14: A–D now hold DBCA · correct B -> B
          #11 C-5.1 U13: A–D now hold BADC · correct B -> A
          #12 C-5.1 U10: A–D now hold BDAC · correct A -> C
          #13 C-4.2 U3: A–D now hold BDAC · correct B -> A
          #14 C-4.2 U10: A–D now hold ACDB · correct B -> D

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
