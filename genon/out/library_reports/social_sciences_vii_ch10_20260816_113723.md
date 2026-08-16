# Library certification · social_sciences VII ch 10 · 20260816_113723

plan: counts [18, 15, 11] · basis authored_standard · registry 14 sections

PASS  library complete: ['ch_10_canonical.json', 'ch_10_canonical_p15.json', 'ch_10_canonical_p11.json'] vs plan [18, 15, 11]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_10_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_10_canonical.json: every anchor verbatim in the top registry
PASS  ch_10_canonical.json: first-visit order follows the registry
PASS  ch_10_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_10_canonical_p15.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_10_canonical_p15.json: every anchor verbatim in the top registry
PASS  ch_10_canonical_p15.json: first-visit order follows the registry
PASS  ch_10_canonical_p15.json: coverage reaches the final registry section
PASS  ch_10_canonical_p11.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_10_canonical_p11.json: every anchor verbatim in the top registry
PASS  ch_10_canonical_p11.json: first-visit order follows the registry
PASS  ch_10_canonical_p11.json: coverage reaches the final registry section
PASS  ch_10_canonical.json: register scan reached the band text (72 band(s) read: {'activity_title': 18, 'materials': 36, 'visual_aids': 7, 'teacher_notes': 18, 'time_bands': 72})
PASS  ch_10_canonical.json: register clean (0 ban hit(s))
PASS  ch_10_canonical_p15.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 35, 'visual_aids': 4, 'teacher_notes': 15, 'time_bands': 60})
FAIL  ch_10_canonical_p15.json: register clean (2 ban hit(s))
      U1 time_bands[2] 20-32 [forward] …: 'What is it?', 'Why do we need it?', 'How was it made?' — previewing the chapter's inquiry arc without closing any question.
      U15 time_bands[0] 0-10 [clock] …nciples, and Fundamental Duties. Students work individually for five minutes, then compare with a partner — gaps and disagreements show…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_10_canonical_p11.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 34, 'visual_aids': 5, 'teacher_notes': 11, 'time_bands': 44})
PASS  ch_10_canonical_p11.json: register clean (0 ban hit(s))
PASS  ch_10_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_10_canonical_p15.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_10_canonical_p11.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_10_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_10_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_10_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_10_canonical_p15.json: every question_type is a known assessment type (0 not)
PASS  ch_10_canonical_p15.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_10_canonical_p15.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_10_canonical_p11.json: every question_type is a known assessment type (0 not)
PASS  ch_10_canonical_p11.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_10_canonical_p11.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_10_canonical.json: MCQ options in arrangement order
PASS  ch_10_canonical_p15.json: MCQ options in arrangement order
PASS  ch_10_canonical_p11.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_10_canonical.json: 14 items vs 14 expected
      ch_10_canonical_p15.json: 14 items vs 14 expected
      ch_10_canonical_p11.json: 13 items vs 14 expected  <-- MISS
          C-5.2 (Present) has 1, its siblings carry 2
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

serve sweep: {"9": "fill/forward -1s", "10": "fill/single", "11": "identity", "12": "rescue/complete (from 15)", "13": "fill/single", "14": "synthesis", "15": "identity", "16": "synthesis", "17": "synthesis", "18": "identity", "19": "surrender", "20": "surrender"}

options arranged: 0 of 29 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_10_canonical.json: 0 of 10 item(s) re-ordered
      ch_10_canonical_p11.json: 0 of 9 item(s) re-ordered
      ch_10_canonical_p15.json: 0 of 10 item(s) re-ordered
          #6 SKIPPED — cross-references an option label — left untouched, needs a human

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
