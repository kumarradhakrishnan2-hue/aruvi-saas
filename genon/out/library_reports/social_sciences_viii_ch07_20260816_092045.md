# Library certification · social_sciences VIII ch 7 · 20260816_092045

plan: counts [12, 10, 7] · basis authored_standard · registry 11 sections

FAIL  library complete: ['ch_07_canonical.json'] vs plan [12, 10, 7]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_07_canonical.json: 5 prose lead(s) in the summary match no registry entry (6 summary section(s) vs 11 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: Education and training; Healthcare; Social and cultural influences; The section; This section
      ADVISORY ch_07_canonical.json: 10 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Introduction; Land (natural resources); Labour (human resources); Facilitators of human capital; Challenges to human capital; India's ancient skill heritage …
PASS  ch_07_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_07_canonical.json: every anchor verbatim in the top registry
PASS  ch_07_canonical.json: first-visit order follows the registry
PASS  ch_07_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_07_canonical.json: register scan reached the band text (48 band(s) read: {'activity_title': 12, 'materials': 21, 'visual_aids': 5, 'teacher_notes': 12, 'time_bands': 48})
FAIL  ch_07_canonical.json: register clean (1 ban hit(s))
      U9 time_bands[3] 35-45 [forward] …ents write one final sentence answering this, which sets up the next unit's focus on how factors interact.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_07_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_07_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_07_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_07_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_07_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_07_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_07_canonical.json: 15 items vs 15 expected
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)
PASS  X=12: choice set non-empty (no defensive truncation)
PASS  X=13: choice set non-empty (no defensive truncation)
PASS  X=14: choice set non-empty (no defensive truncation)

serve sweep: {"5": "fill/single -6s", "6": "fill/single -5s", "7": "fill/single -4s", "8": "fill/single -3s", "9": "fill/single -2s", "10": "fill/single -1s", "11": "fill/single", "12": "identity", "13": "surrender", "14": "surrender"}

options arranged: 10 of 10 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_07_canonical.json: 10 of 10 item(s) re-ordered
          #1 C-9.1 U1: A–D now hold BCAD · correct B -> A
          #2 C-9.1 U5: A–D now hold ABDC · correct C -> D
          #6 C-6.3 U11: A–D now hold ADBC · correct C -> D
          #7 C-6.3 U12: A–D now hold DABC · correct C -> D
          #9 C-4.1 U1: A–D now hold BCDA · correct A -> D
          #10 C-4.1 U8: A–D now hold BDAC · correct B -> A
          #12 C-6.2 U2: A–D now hold BDAC · correct B -> A
          #13 C-6.2 U10: A–D now hold BCDA · correct A -> D
          #14 C-10.1 U6: A–D now hold BDAC · correct B -> A
          #15 C-10.1 U6: A–D now hold BDCA · correct C -> C

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
