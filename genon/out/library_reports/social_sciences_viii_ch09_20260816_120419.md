# Library certification · social_sciences VIII ch 9 · 20260816_120419

plan: counts [17, 14, 10] · basis authored_standard · registry 16 sections

PASS  library complete: ['ch_09_canonical.json', 'ch_09_canonical_p14.json', 'ch_09_canonical_p10.json'] vs plan [17, 14, 10]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_09_canonical.json: 5 prose lead(s) in the summary match no registry entry (5 summary section(s) vs 16 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This short section; Before turning to the political front, the chapter; This section; The section; The closing recap consolidates the chapter's argument
      ADVISORY ch_09_canonical.json: 16 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Introduction; A Royal Proclamation; Reform Movements; Other Influences; The Rise of the Indian National Congress; Growing Discontent …
PASS  ch_09_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_09_canonical.json: every anchor verbatim in the top registry
PASS  ch_09_canonical.json: first-visit order follows the registry
PASS  ch_09_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_09_canonical_p14.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_09_canonical_p14.json: every anchor verbatim in the top registry
PASS  ch_09_canonical_p14.json: first-visit order follows the registry
PASS  ch_09_canonical_p14.json: coverage reaches the final registry section
PASS  ch_09_canonical_p10.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_09_canonical_p10.json: every anchor verbatim in the top registry
PASS  ch_09_canonical_p10.json: first-visit order follows the registry
PASS  ch_09_canonical_p10.json: coverage reaches the final registry section
PASS  ch_09_canonical.json: register scan reached the band text (68 band(s) read: {'activity_title': 17, 'materials': 37, 'visual_aids': 6, 'teacher_notes': 17, 'time_bands': 68})
FAIL  ch_09_canonical.json: register clean (1 ban hit(s))
      U11 time_bands[0] 0-10 [clock] …r sealed the main exit and fired approximately 1,650 rounds for about ten minutes, deliberately aiming at the thickest parts of the crowd. Of…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_09_canonical_p14.json: register scan reached the band text (56 band(s) read: {'activity_title': 14, 'materials': 37, 'visual_aids': 8, 'teacher_notes': 14, 'time_bands': 56})
PASS  ch_09_canonical_p14.json: register clean (0 ban hit(s))
PASS  ch_09_canonical_p10.json: register scan reached the band text (40 band(s) read: {'activity_title': 10, 'materials': 21, 'visual_aids': 2, 'teacher_notes': 10, 'time_bands': 40})
PASS  ch_09_canonical_p10.json: register clean (0 ban hit(s))
PASS  ch_09_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_09_canonical_p14.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_09_canonical_p10.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_09_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_09_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_09_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_09_canonical_p14.json: every question_type is a known assessment type (0 not)
PASS  ch_09_canonical_p14.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_09_canonical_p14.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_09_canonical_p10.json: every question_type is a known assessment type (0 not)
PASS  ch_09_canonical_p10.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_09_canonical_p10.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_09_canonical.json: MCQ options in arrangement order
PASS  ch_09_canonical_p14.json: MCQ options in arrangement order
PASS  ch_09_canonical_p10.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_09_canonical.json: 21 items vs 22 expected  <-- MISS
          C-10.1 (Present) has 1, its siblings carry 2
      ch_09_canonical_p14.json: 20 items vs 22 expected  <-- MISS
          C-5.1 (Present) has 1, its siblings carry 2
          C-10.1 (Present) has 1, its siblings carry 2
      ch_09_canonical_p10.json: 22 items vs 22 expected
      -> 3 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
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

serve sweep: {"8": "fill/single -2s", "9": "fill/single -1s", "10": "identity", "11": "rescue/complete (from 14)", "12": "fill/single -1s", "13": "fill/single", "14": "identity", "15": "rescue/complete (from 17)", "16": "fill/single", "17": "identity", "18": "surrender", "19": "surrender"}

options arranged: 0 of 45 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_09_canonical.json: 0 of 15 item(s) re-ordered
      ch_09_canonical_p10.json: 0 of 16 item(s) re-ordered
      ch_09_canonical_p14.json: 0 of 14 item(s) re-ordered

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
