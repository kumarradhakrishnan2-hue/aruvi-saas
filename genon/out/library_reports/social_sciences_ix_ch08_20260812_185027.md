# Library certification · social_sciences IX ch 8 · 20260812_185027

plan: counts [7, 4] · basis authored_standard · registry 6 sections

PASS  library complete: ['ch_08_canonical.json', 'ch_08_canonical_p04.json'] vs plan [7, 4]
serve granularity: unit  ·  section axis: True
PASS  ch_08_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_08_canonical.json: every anchor verbatim in the top registry
PASS  ch_08_canonical.json: first-visit order follows the registry
PASS  ch_08_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_08_canonical_p04.json: the `synthesis` token is reserved to the standard canonical
FAIL  ch_08_canonical_p04.json: every anchor verbatim in the top registry
FAIL  ch_08_canonical_p04.json: first-visit order follows the registry
FAIL  ch_08_canonical_p04.json: coverage reaches the final registry section
PASS  ch_08_canonical.json: register scan reached the band text (28 band(s) read: {'activity_title': 7, 'materials': 27, 'visual_aids': 6, 'teacher_notes': 7, 'time_bands': 28})
PASS  ch_08_canonical.json: register clean (0 ban hit(s))
PASS  ch_08_canonical_p04.json: register scan reached the band text (16 band(s) read: {'activity_title': 4, 'materials': 12, 'visual_aids': 4, 'teacher_notes': 4, 'time_bands': 16, 'homework': 1})
FAIL  ch_08_canonical_p04.json: register clean (3 ban hit(s))
      U1 time_bands[0] 0-10 [calendar] …tudents individually list three things their parents bought this month, then classify each as a need (food, water, shelter) or a w…
      U2 time_bands[3] 38-50 [clock] …nomic Survey would it look for?' Students work individually for four minutes, then share in pairs. Draw out that producers depend on gov…
      U3 time_bands[1] 10-25 [clock] …and space exploration, and why?' Students discuss in pairs for three minutes, then two pairs share their reasoning. Second: shoes for di…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_08_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_08_canonical_p04.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_08_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_08_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_08_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_08_canonical_p04.json: every question_type is a known assessment type (0 not)
PASS  ch_08_canonical_p04.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_08_canonical_p04.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_08_canonical.json: MCQ options in arrangement order
PASS  ch_08_canonical_p04.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: constitution
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_08_canonical.json: 10 items vs 10 expected
      ch_08_canonical_p04.json: 10 items vs 10 expected
PASS  X=2: choice set non-empty (no defensive truncation)
PASS  X=3: choice set non-empty (no defensive truncation)
PASS  X=4: choice set non-empty (no defensive truncation)
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)

serve sweep: {"2": "fill/single -6s", "3": "fill/forward -3s", "4": "identity", "5": "rescue/complete (from 7)", "6": "fill/single", "7": "identity", "8": "surrender", "9": "surrender"}

options arranged: 3 of 6 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_08_canonical.json: 0 of 3 item(s) re-ordered
      ch_08_canonical_p04.json: 3 of 3 item(s) re-ordered
          #1 C-7.1 U1: A–D now hold ACBD · correct B -> C
          #6 C-8.2 U4: A–D now hold BACD · correct B -> A
          #9 C-8.5 U3: A–D now hold DCAB · correct B -> D
QUARANTINED  ch_08_canonical_p04.json -> backup/quarantine/social_sciences/ix/ch_08_canonical_p04_20260812_185027.json

DETERMINISTIC CHECKS HAVE FAILURES — do not certify Failed files are QUARANTINED under backup/quarantine/ (the fix worklist); regenerate them and re-run --certify-only..
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
