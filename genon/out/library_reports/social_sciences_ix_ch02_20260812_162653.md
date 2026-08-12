# Library certification · social_sciences IX ch 2 · 20260812_162653

plan: counts [11, 9, 7] · basis authored_standard · registry 8 sections

FAIL  library complete: ['ch_02_canonical.json'] vs plan [11, 9, 7]
serve granularity: unit  ·  section axis: True
PASS  ch_02_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_02_canonical.json: every anchor verbatim in the top registry
PASS  ch_02_canonical.json: first-visit order follows the registry
PASS  ch_02_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_02_canonical.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 34, 'visual_aids': 9, 'teacher_notes': 11, 'time_bands': 44})
FAIL  ch_02_canonical.json: register clean (1 ban hit(s))
      U11 time_bands[1] 10-30 [clock] …ism, freshwater, disaster risk). Students work individually for fifteen minutes, then compare maps in pairs, adding any landform or human c…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_02_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_02_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_02_canonical.json: ['OPEN_TASK', 'SOURCE_INTERPRETATION'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_02_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_02_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_02_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: constitution
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_02_canonical.json: 17 items vs 17 expected
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)
PASS  X=12: choice set non-empty (no defensive truncation)
PASS  X=13: choice set non-empty (no defensive truncation)

serve sweep: {"5": "fill/single -5s", "6": "fill/single -4s", "7": "fill/single -3s", "8": "fill/single -2s", "9": "fill/single -1s", "10": "fill/single", "11": "identity", "12": "surrender", "13": "surrender"}

options arranged: 6 of 6 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_02_canonical.json: 6 of 6 item(s) re-ordered
          #1 C-4.2 U2: A–D now hold DABC · correct B -> C
          #6 C-4.4 U8: A–D now hold DACB · correct C -> C
          #9 C-4.5 U10: A–D now hold DBCA · correct B -> B
          #12 C-4.1 U2: A–D now hold CDAB · correct B -> D
          #14 C-4.6 U4: A–D now hold DBAC · correct B -> B
          #16 C-9.1 U2: A–D now hold DACB · correct B -> D

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
