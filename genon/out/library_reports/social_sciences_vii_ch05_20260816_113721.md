# Library certification · social_sciences VII ch 5 · 20260816_113721

plan: counts [19, 15, 11] · basis authored_standard · registry 12 sections

PASS  library complete: ['ch_05_canonical.json', 'ch_05_canonical_p15.json', 'ch_05_canonical_p11.json'] vs plan [19, 15, 11]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_05_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_05_canonical.json: every anchor verbatim in the top registry
PASS  ch_05_canonical.json: first-visit order follows the registry
PASS  ch_05_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_05_canonical_p15.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_05_canonical_p15.json: every anchor verbatim in the top registry
PASS  ch_05_canonical_p15.json: first-visit order follows the registry
PASS  ch_05_canonical_p15.json: coverage reaches the final registry section
PASS  ch_05_canonical_p11.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_05_canonical_p11.json: every anchor verbatim in the top registry
PASS  ch_05_canonical_p11.json: first-visit order follows the registry
PASS  ch_05_canonical_p11.json: coverage reaches the final registry section
PASS  ch_05_canonical.json: register scan reached the band text (76 band(s) read: {'activity_title': 19, 'materials': 30, 'teacher_notes': 19, 'time_bands': 76, 'visual_aids': 6})
PASS  ch_05_canonical.json: register clean (0 ban hit(s))
PASS  ch_05_canonical_p15.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 34, 'teacher_notes': 15, 'time_bands': 60, 'visual_aids': 4})
FAIL  ch_05_canonical_p15.json: register clean (4 ban hit(s))
      U1 time_bands[0] 0-8 [clock] …olds power and how they hold it?' Students discuss in pairs for two minutes, then share observations aloud.
      U8 teacher_notes [forward] …ral, not tactical, and his Arthaśhāstra will be examined in the next unit. The written comparison must use Dhana Nanda and Chandragup…
      U8 time_bands[2] 20-32 [clock] …e historians use to reconstruct the past?' Students discuss for four minutes, then the teacher draws out the distinction between indigen…
      U9 time_bands[0] 0-8 [clock] …tial parts, what would you include?' Students suggest ideas for two minutes. The teacher then has students read the Kauṭilya section to…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_05_canonical_p11.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 31, 'visual_aids': 8, 'teacher_notes': 11, 'time_bands': 44})
FAIL  ch_05_canonical_p11.json: register clean (2 ban hit(s))
      U2 time_bands[0] 0-7 [clock] …that trade actually happens?' Students brainstorm in pairs for two minutes, then share. Teacher accepts responses and introduces the w…
      U6 time_bands[3] 32-40 [forward] …better supported. This closes the founding narrative before the next unit examines the governance philosophy that sustained it.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_05_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_05_canonical_p15.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_05_canonical_p11.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_05_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_05_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_05_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_05_canonical_p15.json: every question_type is a known assessment type (0 not)
PASS  ch_05_canonical_p15.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_05_canonical_p15.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_05_canonical_p11.json: every question_type is a known assessment type (0 not)
PASS  ch_05_canonical_p11.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_05_canonical_p11.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_05_canonical.json: MCQ options in arrangement order
PASS  ch_05_canonical_p15.json: MCQ options in arrangement order
PASS  ch_05_canonical_p11.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_05_canonical.json: 14 items vs 14 expected
      ch_05_canonical_p15.json: 14 items vs 14 expected
      ch_05_canonical_p11.json: 14 items vs 14 expected
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

serve sweep: {"9": "fill/single -1s", "10": "fill/single", "11": "identity", "12": "fill/single", "13": "synthesis", "14": "synthesis", "15": "identity", "16": "synthesis", "17": "synthesis", "18": "synthesis", "19": "identity", "20": "surrender", "21": "surrender"}

options arranged: 0 of 30 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_05_canonical.json: 0 of 10 item(s) re-ordered
      ch_05_canonical_p11.json: 0 of 10 item(s) re-ordered
      ch_05_canonical_p15.json: 0 of 10 item(s) re-ordered

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
