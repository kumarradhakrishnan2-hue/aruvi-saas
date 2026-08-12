# Library certification · social_sciences IX ch 1 · 20260812_185026

plan: counts [15, 12, 9] · basis authored_standard · registry 9 sections

PASS  library complete: ['ch_01_canonical.json', 'ch_01_canonical_p12.json', 'ch_01_canonical_p09.json'] vs plan [15, 12, 9]
serve granularity: unit  ·  section axis: True
PASS  ch_01_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_01_canonical.json: every anchor verbatim in the top registry
PASS  ch_01_canonical.json: first-visit order follows the registry
PASS  ch_01_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_01_canonical_p12.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_01_canonical_p12.json: every anchor verbatim in the top registry
PASS  ch_01_canonical_p12.json: first-visit order follows the registry
PASS  ch_01_canonical_p12.json: coverage reaches the final registry section
PASS  ch_01_canonical_p09.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_01_canonical_p09.json: every anchor verbatim in the top registry
PASS  ch_01_canonical_p09.json: first-visit order follows the registry
PASS  ch_01_canonical_p09.json: coverage reaches the final registry section
PASS  ch_01_canonical.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 24, 'teacher_notes': 15, 'time_bands': 60, 'visual_aids': 4})
FAIL  ch_01_canonical.json: register clean (1 ban hit(s))
      U13 teacher_notes [completion] Having covered all four disciplines, this unit turns to the chapter's explicit…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_01_canonical_p12.json: register scan reached the band text (48 band(s) read: {'activity_title': 12, 'materials': 28, 'teacher_notes': 12, 'time_bands': 48, 'visual_aids': 4})
FAIL  ch_01_canonical_p12.json: register clean (2 ban hit(s))
      U5 time_bands[0] 0-8 [clock] …ment density, and trade patterns. Why?' Students brainstorm for two minutes in pairs before any explanation.
      U8 time_bands[0] 0-10 [clock] …pens if someone breaks the rule?' Students discuss in pairs for three minutes. Teacher collects responses and writes on the board the clu…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_01_canonical_p09.json: register scan reached the band text (36 band(s) read: {'activity_title': 9, 'materials': 19, 'teacher_notes': 9, 'time_bands': 36, 'visual_aids': 2})
FAIL  ch_01_canonical_p09.json: register clean (1 ban hit(s))
      U8 time_bands[0] 0-10 [clock] …help you in your daily life?' Students brainstorm silently for two minutes, then share. The teacher lists their reasons on the board w…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_01_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_01_canonical_p12.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_01_canonical_p09.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_01_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_01_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_01_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_01_canonical_p12.json: every question_type is a known assessment type (0 not)
PASS  ch_01_canonical_p12.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_01_canonical_p12.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_01_canonical_p09.json: every question_type is a known assessment type (0 not)
PASS  ch_01_canonical_p09.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_01_canonical_p09.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_01_canonical.json: MCQ options in arrangement order
PASS  ch_01_canonical_p12.json: MCQ options in arrangement order
PASS  ch_01_canonical_p09.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: constitution
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_01_canonical.json: 20 items vs 20 expected
      ch_01_canonical_p12.json: 20 items vs 20 expected  <-- MISS
          C-1.4 (Substantive) has 2, constitution says 3
          C-4.4 (Substantive) has 4, constitution says 3
      ch_01_canonical_p09.json: 26 items vs 20 expected  <-- MISS
          C-4.4 (Substantive) has 5, constitution says 3
          C-5.4 (Substantive) has 5, constitution says 3
          C-7.1 (Substantive) has 5, constitution says 3
      -> 5 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
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

serve sweep: {"7": "fill/single -2s", "8": "fill/single -1s", "9": "identity", "10": "rescue/complete (from 12)", "11": "fill/single -1s", "12": "identity", "13": "rescue/complete (from 15)", "14": "fill/single", "15": "identity", "16": "surrender", "17": "surrender"}

options arranged: 16 of 22 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_01_canonical.json: 0 of 6 item(s) re-ordered
      ch_01_canonical_p09.json: 9 of 9 item(s) re-ordered
          #1 C-9.1 U3: A–D now hold ABDC · correct C -> D
          #6 C-1.1 U5: A–D now hold CADB · correct A -> B
          #9 C-1.4 U2: A–D now hold DBCA · correct B -> B
          #12 C-4.4 U4: A–D now hold BDCA · correct B -> A
          #15 C-5.4 U6: A–D now hold CADB · correct A -> B
          #18 C-7.1 U7: A–D now hold DCAB · correct B -> D
          #21 C-4.4 U4: A–D now hold DCBA · correct B -> C
          #23 C-5.4 U6: A–D now hold DBAC · correct B -> B
          #25 C-7.1 U7: A–D now hold DBAC · correct B -> B
      ch_01_canonical_p12.json: 7 of 7 item(s) re-ordered
          #1 C-9.1 U3: A–D now hold DACB · correct B -> D
          #6 C-1.1 U6: A–D now hold DCAB · correct B -> D
          #9 C-1.4 U2: A–D now hold DABC · correct C -> D
          #11 C-4.4 U4: A–D now hold BADC · correct A -> B
          #13 C-5.4 U9: A–D now hold ADBC · correct B -> C
          #16 C-7.1 U10: A–D now hold CDAB · correct B -> D
          #19 C-4.4 U5: A–D now hold CDAB · correct B -> D

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
