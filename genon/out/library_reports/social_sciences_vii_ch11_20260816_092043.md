# Library certification · social_sciences VII ch 11 · 20260816_092043

plan: counts [14, 11, 8] · basis authored_standard · registry 8 sections

FAIL  library complete: ['ch_11_canonical.json'] vs plan [14, 11, 8]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_11_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_11_canonical.json: every anchor verbatim in the top registry
PASS  ch_11_canonical.json: first-visit order follows the registry
PASS  ch_11_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_11_canonical.json: register scan reached the band text (56 band(s) read: {'activity_title': 14, 'materials': 43, 'teacher_notes': 14, 'time_bands': 56, 'visual_aids': 5})
FAIL  ch_11_canonical.json: register clean (2 ban hit(s))
      U4 time_bands[2] 22-33 [calendar] …worth ₹800 but pays only ₹500 today and agrees to pay ₹300 next week — which function is in use? (c) A shopkeeper needs to compa…
      U6 time_bands[2] 22-32 [clock] …coin-based exchange became in India?' Small groups discuss for three minutes and share one-sentence conclusions.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_11_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_11_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_11_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_11_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_11_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_11_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_11_canonical.json: 10 items vs 10 expected
PASS  X=6: choice set non-empty (no defensive truncation)
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

serve sweep: {"6": "fill/single -2s", "7": "fill/single -1s", "8": "fill/single -1s", "9": "fill/single", "10": "synthesis", "11": "synthesis", "12": "synthesis", "13": "synthesis", "14": "identity", "15": "surrender", "16": "surrender"}

options arranged: 6 of 6 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_11_canonical.json: 6 of 6 item(s) re-ordered
          #1 C-9.1 U2: A–D now hold ACDB · correct A -> A
          #2 C-9.1 U13: A–D now hold DBAC · correct A -> C
          #6 C-2.1 U6: A–D now hold CABD · correct A -> B
          #7 C-2.1 U11: A–D now hold BCDA · correct A -> D
          #9 C-10.1 U6: A–D now hold BCAD · correct A -> C
          #10 C-10.1 U3: A–D now hold ACDB · correct A -> A

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
