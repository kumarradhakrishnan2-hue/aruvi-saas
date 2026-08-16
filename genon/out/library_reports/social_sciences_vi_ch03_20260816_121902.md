# Library certification · social_sciences VI ch 3 · 20260816_121902

plan: counts [17, 14, 10] · basis authored_standard · registry 7 sections

PASS  library complete: ['ch_03_canonical.json', 'ch_03_canonical_p14.json', 'ch_03_canonical_p10.json'] vs plan [17, 14, 10]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_03_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_03_canonical.json: every anchor verbatim in the top registry
PASS  ch_03_canonical.json: first-visit order follows the registry
PASS  ch_03_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_03_canonical_p14.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_03_canonical_p14.json: every anchor verbatim in the top registry
PASS  ch_03_canonical_p14.json: first-visit order follows the registry
PASS  ch_03_canonical_p14.json: coverage reaches the final registry section
PASS  ch_03_canonical_p10.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_03_canonical_p10.json: every anchor verbatim in the top registry
PASS  ch_03_canonical_p10.json: first-visit order follows the registry
PASS  ch_03_canonical_p10.json: coverage reaches the final registry section
PASS  ch_03_canonical.json: register scan reached the band text (68 band(s) read: {'activity_title': 17, 'materials': 36, 'visual_aids': 16, 'teacher_notes': 17, 'time_bands': 68})
PASS  ch_03_canonical.json: register clean (0 ban hit(s))
PASS  ch_03_canonical_p14.json: register scan reached the band text (56 band(s) read: {'activity_title': 14, 'materials': 46, 'visual_aids': 9, 'teacher_notes': 14, 'time_bands': 56})
PASS  ch_03_canonical_p14.json: register clean (0 ban hit(s))
PASS  ch_03_canonical_p10.json: register scan reached the band text (40 band(s) read: {'activity_title': 10, 'materials': 26, 'visual_aids': 10, 'teacher_notes': 10, 'time_bands': 40})
PASS  ch_03_canonical_p10.json: register clean (0 ban hit(s))
PASS  ch_03_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_03_canonical_p14.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_03_canonical_p10.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_03_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_03_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_03_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_03_canonical_p14.json: every question_type is a known assessment type (0 not)
PASS  ch_03_canonical_p14.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_03_canonical_p14.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_03_canonical_p10.json: every question_type is a known assessment type (0 not)
PASS  ch_03_canonical_p10.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_03_canonical_p10.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_03_canonical.json: MCQ options in arrangement order
PASS  ch_03_canonical_p14.json: MCQ options in arrangement order
PASS  ch_03_canonical_p10.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_03_canonical.json: 15 items vs 15 expected
      ch_03_canonical_p14.json: 15 items vs 15 expected
      ch_03_canonical_p10.json: 13 items vs 14 expected  <-- MISS
          C-6.2 (Present) has 1, its siblings carry 2
      -> 1 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
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
PASS  X=18: choice set non-empty (no defensive truncation)
PASS  X=19: choice set non-empty (no defensive truncation)

serve sweep: {"8": "synthesis", "9": "synthesis", "10": "identity", "11": "synthesis", "12": "synthesis", "13": "synthesis", "14": "identity", "15": "synthesis", "16": "synthesis", "17": "identity", "18": "surrender", "19": "surrender"}

options arranged: 0 of 29 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_03_canonical.json: 0 of 10 item(s) re-ordered
      ch_03_canonical_p10.json: 0 of 9 item(s) re-ordered
      ch_03_canonical_p14.json: 0 of 10 item(s) re-ordered

DETERMINISTIC CHECKS ALL PASS.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
