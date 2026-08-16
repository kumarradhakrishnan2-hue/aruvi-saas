# Library certification · social_sciences VII ch 3 · 20260816_092041

plan: counts [21, 17, 13] · basis authored_standard · registry 13 sections

FAIL  library complete: ['ch_03_canonical.json'] vs plan [21, 17, 13]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_03_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_03_canonical.json: every anchor verbatim in the top registry
PASS  ch_03_canonical.json: first-visit order follows the registry
PASS  ch_03_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_03_canonical.json: register scan reached the band text (84 band(s) read: {'activity_title': 21, 'materials': 50, 'teacher_notes': 21, 'time_bands': 84, 'visual_aids': 10})
FAIL  ch_03_canonical.json: register clean (4 ban hit(s))
      U3 teacher_notes [forward] …tinguish them clearly here since altitude is the subject of the next unit.
      U3 time_bands[2] 20-32 [clock] …ut the role of latitude relative to seasons?' Pairs discuss for five minutes, then share answers aloud.
      U7 time_bands[3] 33-40 [forward] …This grounds the mechanism in cultural significance before the next unit explores climate and livelihoods.
      U13 time_bands[3] 32-40 [forward] …owth goals. This question is not resolved here — it sets up the next unit's deeper engagement with mitigation.
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
PASS  X=22: choice set non-empty (no defensive truncation)
PASS  X=23: choice set non-empty (no defensive truncation)

serve sweep: {"11": "fill/single -3s", "12": "fill/single -2s", "13": "fill/single -1s", "14": "fill/single", "15": "fill/single", "16": "fill/single", "17": "synthesis", "18": "synthesis", "19": "synthesis", "20": "synthesis", "21": "identity", "22": "surrender", "23": "surrender"}

options arranged: 9 of 10 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_03_canonical.json: 9 of 10 item(s) re-ordered
          #1 C-6.1 U1: A–D now hold DCAB · correct A -> C
          #2 C-6.1 U7: A–D now hold DBAC · correct A -> C
          #6 C-6.3 U13: A–D now hold DBCA · correct A -> D
          #7 C-6.3 U14: A–D now hold ABDC · correct A -> A
          #9 C-6.4 U8: A–D now hold DABC · correct A -> B
          #12 C-6.2 U2: A–D now hold DCAB · correct A -> C
          #13 C-6.2 U20: A–D now hold CBDA · correct A -> D
          #14 C-4.1 U10: A–D now hold CBAD · correct A -> C
          #15 C-4.1 U17: A–D now hold BCAD · correct A -> C

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
