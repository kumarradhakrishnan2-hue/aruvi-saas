# Library certification · social_sciences VII ch 10 · 20260816_092043

plan: counts [18, 15, 11] · basis authored_standard · registry 14 sections

FAIL  library complete: ['ch_10_canonical.json'] vs plan [18, 15, 11]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_10_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_10_canonical.json: every anchor verbatim in the top registry
PASS  ch_10_canonical.json: first-visit order follows the registry
PASS  ch_10_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_10_canonical.json: register scan reached the band text (72 band(s) read: {'activity_title': 18, 'materials': 36, 'visual_aids': 7, 'teacher_notes': 18, 'time_bands': 72})
FAIL  ch_10_canonical.json: register clean (5 ban hit(s))
      U10 teacher_notes [forward] …tal Rights, setting up a conceptual contrast with DPSP that the following unit will complete. A common confusion: students often think all…
      U10 time_bands[3] 33-40 [forward] …nse. Teacher closes by noting the contrast with DPSP, which the next unit will examine.
      U14 teacher_notes [meta-leak] …d in 1976 connects this unit to the living document concept without requiring that unit to have been taught.
      U17 teacher_notes [meta-leak] …and consolidation exercise that sets up the synthesis unit without requiring any specific prior activity to have occurred.
      U18 teacher_notes [meta-leak] …closing statement restates the constitutional design logic without requiring students to have heard any particular unit's framing before.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_10_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_10_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_10_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_10_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_10_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_10_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_10_canonical.json: 14 items vs 14 expected
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

serve sweep: {"9": "fill/single -5s", "10": "fill/single -4s", "11": "fill/single -3s", "12": "fill/single -2s", "13": "fill/single -1s", "14": "fill/single", "15": "synthesis", "16": "synthesis", "17": "synthesis", "18": "identity", "19": "surrender", "20": "surrender"}

options arranged: 10 of 10 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_10_canonical.json: 10 of 10 item(s) re-ordered
          #1 C-8.2 U4: A–D now hold CDBA · correct A -> D
          #2 C-8.2 U8: A–D now hold DABC · correct A -> B
          #6 C-8.1 U3: A–D now hold CADB · correct A -> B
          #7 C-8.1 U16: A–D now hold ACBD · correct A -> A
          #9 C-4.1 U10: A–D now hold CBDA · correct A -> D
          #10 C-4.1 U11: A–D now hold ACDB · correct A -> A
          #11 C-5.2 U10: A–D now hold CDAB · correct A -> C
          #12 C-5.2 U11: A–D now hold ADBC · correct A -> A
          #13 C-7.1 U7: A–D now hold DBAC · correct A -> C
          #14 C-7.1 U7: A–D now hold BCDA · correct A -> D

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
