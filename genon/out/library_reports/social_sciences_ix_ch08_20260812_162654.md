# Library certification · social_sciences IX ch 8 · 20260812_162654

plan: counts [7, 4] · basis authored_standard · registry 6 sections

FAIL  library complete: ['ch_08_canonical.json'] vs plan [7, 4]
serve granularity: unit  ·  section axis: True
PASS  ch_08_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_08_canonical.json: every anchor verbatim in the top registry
PASS  ch_08_canonical.json: first-visit order follows the registry
PASS  ch_08_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_08_canonical.json: register scan reached the band text (28 band(s) read: {'activity_title': 7, 'materials': 27, 'visual_aids': 6, 'teacher_notes': 7, 'time_bands': 28})
FAIL  ch_08_canonical.json: register clean (4 ban hit(s))
      U1 time_bands[0] 0-10 [calendar] …ividually and quickly, one choice they or their family made this week where they could not have both options. Take three examples…
      U1 time_bands[2] 22-38 [calendar] …is section: students list three things their parents bought this month and classify each as a need or a want, then answer — could…
      U5 time_bands[3] 40-50 [clock] …and innovation; real-world examples. They work individually for five minutes, then compare with a neighbour to catch gaps. Consolidate b…
      U7 time_bands[1] 12-28 [clock] …1 anchor the three system cells. Students work individually for ten minutes, then compare with a neighbour to check that all three ques…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_08_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_08_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_08_canonical.json: ['OPEN_TASK', 'SOURCE_INTERPRETATION'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_08_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_08_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_08_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: constitution
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_08_canonical.json: 10 items vs 10 expected
PASS  X=2: choice set non-empty (no defensive truncation)
PASS  X=3: choice set non-empty (no defensive truncation)
PASS  X=4: choice set non-empty (no defensive truncation)
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)

serve sweep: {"2": "fill/single -4s", "3": "fill/single -3s", "4": "fill/single -2s", "5": "fill/single -1s", "6": "fill/single", "7": "identity", "8": "surrender", "9": "surrender"}

options arranged: 3 of 3 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_08_canonical.json: 3 of 3 item(s) re-ordered
          #1 C-7.1 U4: A–D now hold CADB · correct B -> D
          #6 C-8.2 U5: A–D now hold ACDB · correct B -> D
          #9 C-8.5 U4: A–D now hold DCAB · correct B -> D

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
