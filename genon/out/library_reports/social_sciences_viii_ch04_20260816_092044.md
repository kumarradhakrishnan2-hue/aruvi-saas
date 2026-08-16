# Library certification · social_sciences VIII ch 4 · 20260816_092044

plan: counts [19, 15, 11] · basis authored_standard · registry 20 sections

FAIL  library complete: ['ch_04_canonical.json'] vs plan [19, 15, 11]
serve granularity: unit  ·  section axis: True
      registry <-> summary: no unmatched prose lead (1 summary section(s) vs 20 registry entr(ies))
      ADVISORY ch_04_canonical.json: 19 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): The Age of Colonialism; Europeans in India; The Portuguese: commerce and atrocities; The Dutch: commerce and competition; From traders to rulers; The strategy of 'divide and rule' …
PASS  ch_04_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_04_canonical.json: every anchor verbatim in the top registry
PASS  ch_04_canonical.json: first-visit order follows the registry
PASS  ch_04_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_04_canonical.json: register scan reached the band text (95 band(s) read: {'activity_title': 19, 'materials': 33, 'visual_aids': 8, 'teacher_notes': 19, 'time_bands': 95})
FAIL  ch_04_canonical.json: register clean (2 ban hit(s))
      U5 time_bands[0] 0-8 [clock] …s riches to Britannia' without commentary. Students observe for two minutes, then write: (1) Who is depicted and in what posture? (2) W…
      U14 time_bands[0] 0-10 [clock] …of the Santhal rebels without commentary. Students observe for two minutes and write: (1) How are the Santhal rebels depicted — postur…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_04_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_04_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_04_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_04_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_04_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_04_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_04_canonical.json: 22 items vs 22 expected
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

serve sweep: {"9": "fill/forward -9s", "10": "fill/single -8s", "11": "fill/single -7s", "12": "fill/single -6s", "13": "fill/single -5s", "14": "fill/single -4s", "15": "fill/single -3s", "16": "fill/single -2s", "17": "fill/single -1s", "18": "fill/single", "19": "identity", "20": "surrender", "21": "surrender"}

options arranged: 14 of 14 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_04_canonical.json: 14 of 14 item(s) re-ordered
          #1 C-2.1 U1: A–D now hold BDCA · correct A -> D
          #2 C-2.1 U7: A–D now hold DBAC · correct A -> C
          #6 C-1.1 U5: A–D now hold ABDC · correct A -> A
          #7 C-1.1 U8: A–D now hold BDCA · correct A -> D
          #9 C-3.2 U6: A–D now hold ABDC · correct A -> A
          #10 C-3.2 U14: A–D now hold ACDB · correct A -> A
          #12 C-4.2 U10: A–D now hold DBAC · correct A -> C
          #13 C-4.2 U12: A–D now hold BCDA · correct A -> D
          #15 C-5.1 U1: A–D now hold ACBD · correct A -> A
          #16 C-5.1 U14: A–D now hold CABD · correct A -> B
          #18 C-9.1 U3: A–D now hold ADBC · correct A -> A
          #19 C-9.1 U9: A–D now hold CADB · correct A -> B
          #21 C-10.1 U18: A–D now hold CBAD · correct A -> C
          #22 C-10.1 U18: A–D now hold BCAD · correct A -> C

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
