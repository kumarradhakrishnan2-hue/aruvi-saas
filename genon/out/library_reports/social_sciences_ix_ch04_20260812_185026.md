# Library certification · social_sciences IX ch 4 · 20260812_185026

plan: counts [19, 15, 11] · basis authored_standard · registry 16 sections

PASS  library complete: ['ch_04_canonical.json', 'ch_04_canonical_p15.json', 'ch_04_canonical_p11.json'] vs plan [19, 15, 11]
serve granularity: unit  ·  section axis: True
PASS  ch_04_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_04_canonical.json: every anchor verbatim in the top registry
PASS  ch_04_canonical.json: first-visit order follows the registry
PASS  ch_04_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_04_canonical_p15.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_04_canonical_p15.json: every anchor verbatim in the top registry
PASS  ch_04_canonical_p15.json: first-visit order follows the registry
PASS  ch_04_canonical_p15.json: coverage reaches the final registry section
PASS  ch_04_canonical_p11.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_04_canonical_p11.json: every anchor verbatim in the top registry
PASS  ch_04_canonical_p11.json: first-visit order follows the registry
PASS  ch_04_canonical_p11.json: coverage reaches the final registry section
PASS  ch_04_canonical.json: register scan reached the band text (76 band(s) read: {'activity_title': 19, 'materials': 38, 'visual_aids': 19, 'teacher_notes': 19, 'time_bands': 76})
PASS  ch_04_canonical.json: register clean (0 ban hit(s))
PASS  ch_04_canonical_p15.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 31, 'visual_aids': 7, 'teacher_notes': 15, 'time_bands': 60})
FAIL  ch_04_canonical_p15.json: register clean (2 ban hit(s))
      U2 time_bands[0] 0-8 [clock] …tudy early human history?' Students brainstorm individually for two minutes, then share aloud. Record responses on the board under two…
      U5 time_bands[0] 0-10 [clock] …ing and gathering communities?' Students predict in writing for two minutes, then share.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_04_canonical_p11.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 33, 'visual_aids': 11, 'teacher_notes': 11, 'time_bands': 44})
FAIL  ch_04_canonical_p11.json: register clean (1 ban hit(s))
      U7 time_bands[0] 0-10 [clock] …th of early civilisations? Students brainstorm individually for two minutes, then share. Record responses in two columns: geographical…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_04_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_04_canonical_p15.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_04_canonical_p11.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_04_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_04_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_04_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_04_canonical_p15.json: every question_type is a known assessment type (0 not)
PASS  ch_04_canonical_p15.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_04_canonical_p15.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_04_canonical_p11.json: every question_type is a known assessment type (0 not)
PASS  ch_04_canonical_p11.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_04_canonical_p11.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_04_canonical.json: MCQ options in arrangement order
PASS  ch_04_canonical_p15.json: MCQ options in arrangement order
PASS  ch_04_canonical_p11.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: constitution
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_04_canonical.json: 28 items vs 28 expected
      ch_04_canonical_p15.json: 28 items vs 28 expected
      ch_04_canonical_p11.json: 26 items vs 28 expected  <-- MISS
          C-2.4 (Substantive) has 2, constitution says 3
          C-4.4 (Substantive) has 2, constitution says 3
      -> 2 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
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

serve sweep: {"9": "fill/single -1s", "10": "fill/single -1s", "11": "identity", "12": "rescue/complete (from 15)", "13": "fill/single", "14": "synthesis", "15": "identity", "16": "fill/single", "17": "fill/single", "18": "synthesis", "19": "identity", "20": "surrender", "21": "surrender"}

options arranged: 20 of 30 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_04_canonical.json: 0 of 10 item(s) re-ordered
      ch_04_canonical_p11.json: 10 of 10 item(s) re-ordered
          #1 C-2.2 U5: A–D now hold ACDB · correct B -> D
          #6 C-1.2 U6: A–D now hold BCAD · correct B -> A
          #9 C-2.1 U8: A–D now hold ACBD · correct B -> C
          #12 C-2.3 U8: A–D now hold ADBC · correct A -> A
          #15 C-2.4 U8: A–D now hold ADCB · correct B -> D
          #17 C-4.4 U4: A–D now hold BCDA · correct B -> A
          #19 C-1.1 U1: A–D now hold CADB · correct B -> D
          #21 C-1.3 U6: A–D now hold CADB · correct B -> D
          #23 C-7.4 U8: A–D now hold DBAC · correct A -> C
          #25 C-9.1 U6: A–D now hold BCDA · correct B -> A
      ch_04_canonical_p15.json: 10 of 10 item(s) re-ordered
          #1 C-2.2 U6: A–D now hold DCAB · correct B -> D
          #6 C-1.2 U7: A–D now hold ACDB · correct B -> D
          #9 C-2.1 U14: A–D now hold ADBC · correct B -> C
          #12 C-2.3 U11: A–D now hold BADC · correct B -> A
          #15 C-2.4 U11: A–D now hold BCAD · correct B -> A
          #18 C-4.4 U9: A–D now hold BDCA · correct B -> A
          #21 C-1.1 U14: A–D now hold BDCA · correct B -> A
          #23 C-1.3 U8: A–D now hold DACB · correct B -> D
          #25 C-7.4 U10: A–D now hold CABD · correct B -> C
          #27 C-9.1 U8: A–D now hold BCAD · correct B -> A

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
