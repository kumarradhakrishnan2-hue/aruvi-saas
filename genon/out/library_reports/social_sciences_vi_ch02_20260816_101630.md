# Library certification · social_sciences VI ch 2 · 20260816_101630

plan: counts [15, 12, 9] · basis authored_standard · registry 6 sections

PASS  library complete: ['ch_02_canonical.json', 'ch_02_canonical_p12.json', 'ch_02_canonical_p09.json'] vs plan [15, 12, 9]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_02_canonical.json: 1 prose lead(s) in the summary match no registry entry (1 summary section(s) vs 6 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: A continent is a large continuous landmass. The chapter
      ADVISORY ch_02_canonical.json: 6 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): The Distribution of Water and Land on the Earth; Oceans; Oceans and Disasters; Continents; Islands; Oceans and Life
PASS  ch_02_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_02_canonical.json: every anchor verbatim in the top registry
PASS  ch_02_canonical.json: first-visit order follows the registry
PASS  ch_02_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_02_canonical_p12.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_02_canonical_p12.json: every anchor verbatim in the top registry
PASS  ch_02_canonical_p12.json: first-visit order follows the registry
PASS  ch_02_canonical_p12.json: coverage reaches the final registry section
PASS  ch_02_canonical_p09.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_02_canonical_p09.json: every anchor verbatim in the top registry
PASS  ch_02_canonical_p09.json: first-visit order follows the registry
PASS  ch_02_canonical_p09.json: coverage reaches the final registry section
PASS  ch_02_canonical.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 39, 'visual_aids': 10, 'teacher_notes': 15, 'time_bands': 60})
PASS  ch_02_canonical.json: register clean (0 ban hit(s))
PASS  ch_02_canonical_p12.json: register scan reached the band text (48 band(s) read: {'activity_title': 12, 'materials': 31, 'visual_aids': 11, 'teacher_notes': 12, 'time_bands': 48})
FAIL  ch_02_canonical_p12.json: register clean (1 ban hit(s))
      U9 time_bands[0] 0-10 [clock] …people?' Students write their initial thoughts individually for five minutes, then share one idea each in a brief whole-class round.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_02_canonical_p09.json: register scan reached the band text (36 band(s) read: {'activity_title': 9, 'materials': 29, 'visual_aids': 6, 'teacher_notes': 9, 'time_bands': 36})
FAIL  ch_02_canonical_p09.json: register clean (2 ban hit(s))
      U6 teacher_notes [forward] …deliberately left open: it plants the environmental concern the next unit develops.
      U8 time_bands[1] 8-22 [clock] …oes it help? What kind of action is needed?' Groups discuss for about eight minutes, then each group nominates a spokesperson to share one key…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_02_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_02_canonical_p12.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_02_canonical_p09.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_02_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_02_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_02_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_02_canonical_p12.json: every question_type is a known assessment type (0 not)
PASS  ch_02_canonical_p12.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_02_canonical_p12.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_02_canonical_p09.json: every question_type is a known assessment type (0 not)
PASS  ch_02_canonical_p09.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_02_canonical_p09.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_02_canonical.json: MCQ options in arrangement order
PASS  ch_02_canonical_p12.json: MCQ options in arrangement order
PASS  ch_02_canonical_p09.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_02_canonical.json: 13 items vs 13 expected
      ch_02_canonical_p12.json: 13 items vs 13 expected
      ch_02_canonical_p09.json: 13 items vs 13 expected
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

serve sweep: {"7": "synthesis", "8": "synthesis", "9": "identity", "10": "synthesis", "11": "synthesis", "12": "identity", "13": "synthesis", "14": "synthesis", "15": "identity", "16": "surrender", "17": "surrender"}

options arranged: 16 of 24 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_02_canonical.json: 0 of 8 item(s) re-ordered
      ch_02_canonical_p09.json: 8 of 8 item(s) re-ordered
          #1 C-6.1 U1: A–D now hold CDAB · correct A -> C
          #2 C-6.1 U4: A–D now hold BACD · correct B -> A
          #6 C-6.3 U6: A–D now hold BDAC · correct A -> C
          #7 C-6.3 U8: A–D now hold CADB · correct B -> D
          #9 C-6.4 U3: A–D now hold DCAB · correct B -> D
          #10 C-6.4 U6: A–D now hold CABD · correct B -> C
          #12 C-7.2 U5: A–D now hold ABDC · correct B -> B
          #13 C-7.2 U5: A–D now hold ABDC · correct B -> B
      ch_02_canonical_p12.json: 8 of 8 item(s) re-ordered
          #1 C-6.1 U1: A–D now hold DCAB · correct B -> D
          #2 C-6.1 U5: A–D now hold BADC · correct B -> A
          #6 C-6.3 U8: A–D now hold ABDC · correct B -> B
          #7 C-6.3 U12: A–D now hold DCAB · correct B -> D
          #9 C-6.4 U7: A–D now hold ABDC · correct D -> C
          #10 C-6.4 U11: A–D now hold CADB · correct B -> D
          #12 C-7.2 U6: A–D now hold BCAD · correct B -> A
          #13 C-7.2 U6: A–D now hold DABC · correct B -> C

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
