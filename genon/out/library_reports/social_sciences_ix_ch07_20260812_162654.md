# Library certification · social_sciences IX ch 7 · 20260812_162654

plan: counts [9, 7, 5] · basis authored_standard · registry 8 sections

FAIL  library complete: ['ch_07_canonical.json'] vs plan [9, 7, 5]
serve granularity: unit  ·  section axis: True
PASS  ch_07_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_07_canonical.json: every anchor verbatim in the top registry
PASS  ch_07_canonical.json: first-visit order follows the registry
PASS  ch_07_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_07_canonical.json: register scan reached the band text (36 band(s) read: {'activity_title': 9, 'materials': 27, 'visual_aids': 6, 'teacher_notes': 9, 'time_bands': 36})
FAIL  ch_07_canonical.json: register clean (1 ban hit(s))
      U4 time_bands[0] 0-10 [clock] …s that equal representation?' Let students discuss in pairs for two minutes, then take responses. Establish that unequal constituency s…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_07_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_07_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_07_canonical.json: ['OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_07_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_07_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_07_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: constitution
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_07_canonical.json: 13 items vs 13 expected
PASS  X=3: choice set non-empty (no defensive truncation)
PASS  X=4: choice set non-empty (no defensive truncation)
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)

serve sweep: {"3": "fill/single -5s", "4": "fill/single -4s", "5": "fill/single -3s", "6": "fill/single -2s", "7": "fill/single -1s", "8": "fill/single", "9": "identity", "10": "surrender", "11": "surrender"}

options arranged: 4 of 4 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_07_canonical.json: 4 of 4 item(s) re-ordered
          #1 C-5.4 U2: A–D now hold CDAB · correct B -> D
          #6 C-5.5 U7: A–D now hold DCBA · correct B -> C
          #9 C-6.4 U8: A–D now hold CDAB · correct B -> D
          #12 C-5.3 U1: A–D now hold CBAD · correct B -> B

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
