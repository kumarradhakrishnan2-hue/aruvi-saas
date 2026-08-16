# Library certification · social_sciences VII ch 7 · 20260816_101636

plan: counts [18, 15, 11] · basis authored_standard · registry 14 sections

PASS  library complete: ['ch_07_canonical.json', 'ch_07_canonical_p15.json', 'ch_07_canonical_p11.json'] vs plan [18, 15, 11]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_07_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_07_canonical.json: every anchor verbatim in the top registry
PASS  ch_07_canonical.json: first-visit order follows the registry
PASS  ch_07_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_07_canonical_p15.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_07_canonical_p15.json: every anchor verbatim in the top registry
PASS  ch_07_canonical_p15.json: first-visit order follows the registry
PASS  ch_07_canonical_p15.json: coverage reaches the final registry section
PASS  ch_07_canonical_p11.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_07_canonical_p11.json: every anchor verbatim in the top registry
PASS  ch_07_canonical_p11.json: first-visit order follows the registry
PASS  ch_07_canonical_p11.json: coverage reaches the final registry section
PASS  ch_07_canonical.json: register scan reached the band text (72 band(s) read: {'activity_title': 18, 'materials': 37, 'visual_aids': 11, 'teacher_notes': 18, 'time_bands': 72})
PASS  ch_07_canonical.json: register clean (0 ban hit(s))
PASS  ch_07_canonical_p15.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 45, 'visual_aids': 13, 'teacher_notes': 15, 'time_bands': 60})
PASS  ch_07_canonical_p15.json: register clean (0 ban hit(s))
PASS  ch_07_canonical_p11.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 34, 'visual_aids': 10, 'teacher_notes': 11, 'time_bands': 44})
FAIL  ch_07_canonical_p11.json: register clean (1 ban hit(s))
      U2 time_bands[1] 8-22 [clock] …text might not, and vice versa? Students work individually for eight minutes, then discuss in groups of three.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_07_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_07_canonical_p15.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_07_canonical_p11.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_07_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_07_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_07_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_07_canonical_p15.json: every question_type is a known assessment type (0 not)
PASS  ch_07_canonical_p15.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_07_canonical_p15.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_07_canonical_p11.json: every question_type is a known assessment type (0 not)
PASS  ch_07_canonical_p11.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_07_canonical_p11.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_07_canonical.json: MCQ options in arrangement order
PASS  ch_07_canonical_p15.json: MCQ options in arrangement order
PASS  ch_07_canonical_p11.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_07_canonical.json: 14 items vs 14 expected
      ch_07_canonical_p15.json: 13 items vs 14 expected  <-- MISS
          C-9.1 (Present) has 1, its siblings carry 2
      ch_07_canonical_p11.json: 14 items vs 14 expected
      -> 1 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
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

serve sweep: {"9": "fill/forward -2s", "10": "fill/forward", "11": "identity", "12": "fill/forward", "13": "fill/single", "14": "synthesis", "15": "identity", "16": "synthesis", "17": "synthesis", "18": "identity", "19": "surrender", "20": "surrender"}

options arranged: 18 of 29 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_07_canonical.json: 0 of 10 item(s) re-ordered
      ch_07_canonical_p11.json: 9 of 10 item(s) re-ordered
          #1 C-2.1 U1: A–D now hold CBDA · correct B -> B
          #2 C-2.1 U10: A–D now hold BDCA · correct B -> A
          #6 C-10.1 U8: A–D now hold ABDC · correct B -> B
          #7 C-10.1 U9: A–D now hold ADBC · correct B -> C
          #9 C-3.1 U5: A–D now hold BACD · correct C -> C
          #10 C-3.1 U6: A–D now hold BCDA · correct A -> D
          #11 C-9.1 U7: A–D now hold ACBD · correct B -> C
          #12 C-9.1 U7: A–D now hold CABD · correct B -> C
          #13 C-1.1 U5: A–D now hold CABD · correct B -> C
      ch_07_canonical_p15.json: 9 of 9 item(s) re-ordered
          #1 C-2.1 U1: A–D now hold CABD · correct A -> B
          #2 C-2.1 U12: A–D now hold BADC · correct A -> B
          #6 C-10.1 U9: A–D now hold BDAC · correct B -> A
          #7 C-10.1 U10: A–D now hold DABC · correct B -> C
          #9 C-3.1 U5: A–D now hold DABC · correct B -> C
          #10 C-3.1 U6: A–D now hold ACBD · correct B -> C
          #11 C-9.1 U7: A–D now hold ACBD · correct C -> B
          #12 C-1.1 U5: A–D now hold DCBA · correct B -> C
          #13 C-1.1 U2: A–D now hold DABC · correct B -> C

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
