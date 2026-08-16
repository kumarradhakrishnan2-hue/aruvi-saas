# Library certification · social_sciences VIII ch 4 · 20260816_121912

plan: counts [19, 15, 11] · basis authored_standard · registry 20 sections

PASS  library complete: ['ch_04_canonical.json', 'ch_04_canonical_p15.json', 'ch_04_canonical_p11.json'] vs plan [19, 15, 11]
serve granularity: unit  ·  section axis: True
      registry <-> summary: no unmatched prose lead (1 summary section(s) vs 20 registry entr(ies))
      ADVISORY ch_04_canonical.json: 19 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): The Age of Colonialism; Europeans in India; The Portuguese: commerce and atrocities; The Dutch: commerce and competition; From traders to rulers; The strategy of 'divide and rule' …
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
PASS  ch_04_canonical.json: register scan reached the band text (95 band(s) read: {'activity_title': 19, 'materials': 33, 'visual_aids': 8, 'teacher_notes': 19, 'time_bands': 95})
PASS  ch_04_canonical.json: register clean (0 ban hit(s))
PASS  ch_04_canonical_p15.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 47, 'visual_aids': 6, 'teacher_notes': 15, 'time_bands': 60})
PASS  ch_04_canonical_p15.json: register clean (0 ban hit(s))
PASS  ch_04_canonical_p11.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 33, 'visual_aids': 10, 'teacher_notes': 11, 'time_bands': 44})
PASS  ch_04_canonical_p11.json: register clean (0 ban hit(s))
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

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_04_canonical.json: 22 items vs 22 expected
      ch_04_canonical_p15.json: 19 items vs 22 expected  <-- MISS
          C-4.2 (Substantive) has 2, its siblings carry 3
          C-5.1 (Substantive) has 2, its siblings carry 3
          C-9.1 (Substantive) has 2, its siblings carry 3
      ch_04_canonical_p11.json: 22 items vs 22 expected
      -> 3 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
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

serve sweep: {"9": "fill/forward -2s", "10": "fill/single -1s", "11": "identity", "12": "rescue/complete (from 15)", "13": "fill/single -2s", "14": "fill/single -1s", "15": "identity", "16": "rescue/complete (from 19)", "17": "fill/single -1s", "18": "fill/single", "19": "identity", "20": "surrender", "21": "surrender"}

options arranged: 0 of 42 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_04_canonical.json: 0 of 14 item(s) re-ordered
      ch_04_canonical_p11.json: 0 of 14 item(s) re-ordered
      ch_04_canonical_p15.json: 0 of 14 item(s) re-ordered

DETERMINISTIC CHECKS ALL PASS.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
