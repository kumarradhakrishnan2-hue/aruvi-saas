# Library certification · social_sciences VIII ch 6 · 20260816_101640

plan: counts [12, 10, 7] · basis authored_standard · registry 11 sections

PASS  library complete: ['ch_06_canonical.json', 'ch_06_canonical_p10.json', 'ch_06_canonical_p07.json'] vs plan [12, 10, 7]
serve granularity: unit  ·  section axis: True
      registry <-> summary: no unmatched prose lead (1 summary section(s) vs 11 registry entr(ies))
      ADVISORY ch_06_canonical.json: 10 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Introduction; Composition of the Parliament of India; Legislative Functions of the Parliament — Constitutional function; Legislative Functions of the Parliament — Lawmaking; Legislative Functions of the Parliament — Executive accountability and Financial accountability; Executive Functions of Parliament …
PASS  ch_06_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_06_canonical.json: every anchor verbatim in the top registry
PASS  ch_06_canonical.json: first-visit order follows the registry
PASS  ch_06_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_06_canonical_p10.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_06_canonical_p10.json: every anchor verbatim in the top registry
PASS  ch_06_canonical_p10.json: first-visit order follows the registry
PASS  ch_06_canonical_p10.json: coverage reaches the final registry section
PASS  ch_06_canonical_p07.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_06_canonical_p07.json: every anchor verbatim in the top registry
PASS  ch_06_canonical_p07.json: first-visit order follows the registry
PASS  ch_06_canonical_p07.json: coverage reaches the final registry section
PASS  ch_06_canonical.json: register scan reached the band text (48 band(s) read: {'activity_title': 12, 'materials': 35, 'visual_aids': 11, 'teacher_notes': 12, 'time_bands': 48})
PASS  ch_06_canonical.json: register clean (0 ban hit(s))
PASS  ch_06_canonical_p10.json: register scan reached the band text (40 band(s) read: {'activity_title': 10, 'materials': 33, 'visual_aids': 10, 'teacher_notes': 10, 'time_bands': 40})
FAIL  ch_06_canonical_p10.json: register clean (4 ban hit(s))
      U1 time_bands[2] 20-32 [clock] …imately controls the government?' Students think-pair-share for two minutes, then teacher uses student responses to establish Parliamen…
      U4 time_bands[2] 24-36 [clock] …ution. How do these two ideas sit together?' Students think for two minutes individually, write a response, then discuss. Teacher clari…
      U5 teacher_notes [forward] …ich is the foundation for the accountability discussions in the following unit.
      U6 time_bands[0] 0-10 [clock] …you to demand answers?' Students brainstorm tools in pairs for two minutes, then share. Teacher uses responses to introduce the two ac…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_06_canonical_p07.json: register scan reached the band text (28 band(s) read: {'activity_title': 7, 'materials': 20, 'visual_aids': 4, 'teacher_notes': 7, 'time_bands': 28})
FAIL  ch_06_canonical_p07.json: register clean (2 ban hit(s))
      U3 time_bands[1] 8-25 [clock] …everyday life where this value can be felt. Groups discuss for about ten minutes, then write their three answers on the slip. Note: the chap…
      U7 time_bands[1] 10-25 [clock] …the role of citizens). Two speakers per group then present for two minutes each.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_06_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_06_canonical_p10.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_06_canonical_p07.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_06_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_06_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_06_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_06_canonical_p10.json: every question_type is a known assessment type (0 not)
PASS  ch_06_canonical_p10.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_06_canonical_p10.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_06_canonical_p07.json: every question_type is a known assessment type (0 not)
PASS  ch_06_canonical_p07.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_06_canonical_p07.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_06_canonical.json: MCQ options in arrangement order
PASS  ch_06_canonical_p10.json: MCQ options in arrangement order
PASS  ch_06_canonical_p07.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_06_canonical.json: 13 items vs 14 expected  <-- MISS
          C-8.1 (Present) has 1, its siblings carry 2
      ch_06_canonical_p10.json: 13 items vs 14 expected  <-- MISS
          C-8.1 (Present) has 1, its siblings carry 2
      ch_06_canonical_p07.json: 15 items vs 15 expected
      -> 2 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)
PASS  X=12: choice set non-empty (no defensive truncation)
PASS  X=13: choice set non-empty (no defensive truncation)
PASS  X=14: choice set non-empty (no defensive truncation)

serve sweep: {"5": "fill/forward -4s", "6": "fill/forward -1s", "7": "identity", "8": "rescue/complete (from 10)", "9": "fill/forward -1s", "10": "identity", "11": "fill/single", "12": "identity", "13": "surrender", "14": "surrender"}

options arranged: 18 of 28 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_06_canonical.json: 0 of 9 item(s) re-ordered
      ch_06_canonical_p07.json: 9 of 10 item(s) re-ordered
          #1 C-4.1 U1: A–D now hold BDAC · correct A -> C
          #2 C-4.1 U7: A–D now hold BCDA · correct B -> A
          #6 C-4.2 U4: A–D now hold ACBD · correct A -> A
          #7 C-4.2 U7: A–D now hold DBCA · correct B -> B
          #9 C-8.2 U3: A–D now hold ADCB · correct B -> D
          #12 C-8.1 U3: A–D now hold DBAC · correct A -> C
          #13 C-8.1 U3: A–D now hold BDAC · correct A -> C
          #14 C-10.1 U3: A–D now hold DBAC · correct B -> B
          #15 C-10.1 U3: A–D now hold DBAC · correct B -> B
      ch_06_canonical_p10.json: 9 of 9 item(s) re-ordered
          #1 C-4.1 U2: A–D now hold DBAC · correct B -> B
          #2 C-4.1 U8: A–D now hold DCAB · correct C -> B
          #6 C-4.2 U6: A–D now hold DACB · correct B -> D
          #7 C-4.2 U10: A–D now hold DBCA · correct B -> B
          #9 C-8.2 U4: A–D now hold CDBA · correct B -> C
          #10 C-8.2 U8: A–D now hold ADBC · correct B -> C
          #11 C-8.1 U4: A–D now hold DABC · correct B -> C
          #12 C-10.1 U4: A–D now hold BACD · correct B -> A
          #13 C-10.1 U4: A–D now hold DBAC · correct B -> B

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
