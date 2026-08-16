# Library certification · social_sciences VII ch 3 · 20260816_101635

plan: counts [21, 17, 13] · basis authored_standard · registry 13 sections

PASS  library complete: ['ch_03_canonical.json', 'ch_03_canonical_p17.json', 'ch_03_canonical_p13.json'] vs plan [21, 17, 13]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_03_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_03_canonical.json: every anchor verbatim in the top registry
PASS  ch_03_canonical.json: first-visit order follows the registry
PASS  ch_03_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_03_canonical_p17.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_03_canonical_p17.json: every anchor verbatim in the top registry
FAIL  ch_03_canonical_p17.json: first-visit order follows the registry
PASS  ch_03_canonical_p17.json: coverage reaches the final registry section
PASS  ch_03_canonical_p13.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_03_canonical_p13.json: every anchor verbatim in the top registry
FAIL  ch_03_canonical_p13.json: first-visit order follows the registry
PASS  ch_03_canonical_p13.json: coverage reaches the final registry section
PASS  ch_03_canonical.json: register scan reached the band text (84 band(s) read: {'activity_title': 21, 'materials': 50, 'teacher_notes': 21, 'time_bands': 84, 'visual_aids': 10})
PASS  ch_03_canonical.json: register clean (0 ban hit(s))
PASS  ch_03_canonical_p17.json: register scan reached the band text (68 band(s) read: {'activity_title': 17, 'materials': 38, 'visual_aids': 14, 'teacher_notes': 17, 'time_bands': 68})
FAIL  ch_03_canonical_p17.json: register clean (3 ban hit(s))
      U1 time_bands[0] 0-8 [calendar] Students brainstorm three weather events they noticed this week (rain, heat, wind) and write them on slips. Teacher sorts r…
      U2 teacher_notes [forward] …estern Ghats will be explained as a topographic factor in a later unit.
      U6 teacher_notes [forward] …are the mechanism linking wind to moisture and rainfall — a bridge to the monsoon unit ahead. The two-factor Rajasthan analysis invit…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_03_canonical_p13.json: register scan reached the band text (52 band(s) read: {'activity_title': 13, 'materials': 26, 'visual_aids': 9, 'teacher_notes': 13, 'time_bands': 52})
FAIL  ch_03_canonical_p13.json: register clean (1 ban hit(s))
      U1 time_bands[1] 8-20 [calendar] …he distinction: weather is day-to-day (rain today, sunshine tomorrow), climate is the decades-long pattern that gives a region i…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_03_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_03_canonical_p17.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_03_canonical_p13.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_03_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_03_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_03_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_03_canonical_p17.json: every question_type is a known assessment type (0 not)
PASS  ch_03_canonical_p17.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_03_canonical_p17.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_03_canonical_p13.json: every question_type is a known assessment type (0 not)
PASS  ch_03_canonical_p13.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_03_canonical_p13.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_03_canonical.json: MCQ options in arrangement order
PASS  ch_03_canonical_p17.json: MCQ options in arrangement order
PASS  ch_03_canonical_p13.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_03_canonical.json: 15 items vs 15 expected
      ch_03_canonical_p17.json: 15 items vs 15 expected
      ch_03_canonical_p13.json: 15 items vs 15 expected
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
PASS  X=22: choice set non-empty (no defensive truncation)
PASS  X=23: choice set non-empty (no defensive truncation)

serve sweep: {"11": "fill/single -1s", "12": "fill/single", "13": "identity", "14": "synthesis", "15": "synthesis", "16": "synthesis", "17": "identity", "18": "synthesis", "19": "synthesis", "20": "synthesis", "21": "identity", "22": "surrender", "23": "surrender"}

options arranged: 17 of 30 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_03_canonical.json: 0 of 10 item(s) re-ordered
      ch_03_canonical_p13.json: 9 of 10 item(s) re-ordered
          #1 C-6.1 U3: A–D now hold BCDA · correct A -> D
          #2 C-6.1 U7: A–D now hold CABD · correct A -> B
          #7 C-6.3 U13: A–D now hold DBCA · correct A -> D
          #9 C-6.4 U9: A–D now hold DACB · correct A -> B
          #10 C-6.4 U13: A–D now hold CBAD · correct A -> C
          #12 C-6.2 U2: A–D now hold DCBA · correct A -> D
          #13 C-6.2 U9: A–D now hold DBCA · correct A -> D
          #14 C-4.1 U10: A–D now hold CBAD · correct A -> C
          #15 C-4.1 U10: A–D now hold CDAB · correct A -> C
      ch_03_canonical_p17.json: 8 of 10 item(s) re-ordered
          #1 C-6.1 U1: A–D now hold CDAB · correct A -> C
          #2 C-6.1 U8: A–D now hold BACD · correct A -> B
          #7 C-6.3 U17: A–D now hold DABC · correct A -> B
          #9 C-6.4 U9: A–D now hold BADC · correct A -> B
          #10 C-6.4 U14: A–D now hold BADC · correct A -> B
          #12 C-6.2 U2: A–D now hold CABD · correct A -> B
          #13 C-6.2 U14: A–D now hold DBCA · correct A -> D
          #14 C-4.1 U10: A–D now hold CABD · correct A -> B
QUARANTINED  ch_03_canonical_p13.json -> backup/quarantine/social_sciences/vii/ch_03_canonical_p13_20260816_101635.json
QUARANTINED  ch_03_canonical_p17.json -> backup/quarantine/social_sciences/vii/ch_03_canonical_p17_20260816_101635.json

DETERMINISTIC CHECKS HAVE FAILURES — do not certify Failed files are QUARANTINED under backup/quarantine/ (the fix worklist); regenerate them and re-run --certify-only..
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
