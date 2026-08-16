# Library certification · social_sciences VII ch 8 · 20260816_113844

plan: counts [16, 13, 10] · basis authored_standard · registry 9 sections

PASS  library complete: ['ch_08_canonical.json', 'ch_08_canonical_p13.json', 'ch_08_canonical_p10.json'] vs plan [16, 13, 10]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_08_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_08_canonical.json: every anchor verbatim in the top registry
PASS  ch_08_canonical.json: first-visit order follows the registry
PASS  ch_08_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_08_canonical_p13.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_08_canonical_p13.json: every anchor verbatim in the top registry
FAIL  ch_08_canonical_p13.json: first-visit order follows the registry
PASS  ch_08_canonical_p13.json: coverage reaches the final registry section
PASS  ch_08_canonical_p10.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_08_canonical_p10.json: every anchor verbatim in the top registry
PASS  ch_08_canonical_p10.json: first-visit order follows the registry
PASS  ch_08_canonical_p10.json: coverage reaches the final registry section
PASS  ch_08_canonical.json: register scan reached the band text (64 band(s) read: {'activity_title': 16, 'materials': 36, 'teacher_notes': 16, 'time_bands': 64, 'visual_aids': 4})
PASS  ch_08_canonical.json: register clean (0 ban hit(s))
PASS  ch_08_canonical_p13.json: register scan reached the band text (52 band(s) read: {'activity_title': 13, 'materials': 38, 'teacher_notes': 13, 'time_bands': 52, 'visual_aids': 5})
PASS  ch_08_canonical_p13.json: register clean (0 ban hit(s))
PASS  ch_08_canonical_p10.json: register scan reached the band text (40 band(s) read: {'activity_title': 10, 'materials': 25, 'teacher_notes': 10, 'time_bands': 40, 'visual_aids': 3})
PASS  ch_08_canonical_p10.json: register clean (0 ban hit(s))
PASS  ch_08_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_08_canonical_p13.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_08_canonical_p10.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_08_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_08_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_08_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_08_canonical_p13.json: every question_type is a known assessment type (0 not)
PASS  ch_08_canonical_p13.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_08_canonical_p13.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_08_canonical_p10.json: every question_type is a known assessment type (0 not)
PASS  ch_08_canonical_p10.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_08_canonical_p10.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_08_canonical.json: MCQ options in arrangement order
PASS  ch_08_canonical_p13.json: MCQ options in arrangement order
PASS  ch_08_canonical_p10.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_08_canonical.json: 12 items vs 12 expected
      ch_08_canonical_p13.json: 10 items vs 12 expected  <-- MISS
          C-7.2 (Present) has 1, its siblings carry 2
          C-7.3 (Present) has 1, its siblings carry 2
      ch_08_canonical_p10.json: 12 items vs 12 expected
      -> 2 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
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

serve sweep: {"8": "fill/forward -1s", "9": "fill/single", "10": "identity", "11": "synthesis", "12": "synthesis", "13": "identity", "14": "synthesis", "15": "synthesis", "16": "identity", "17": "surrender", "18": "surrender"}

options arranged: 0 of 22 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_08_canonical.json: 0 of 8 item(s) re-ordered
      ch_08_canonical_p10.json: 0 of 8 item(s) re-ordered
      ch_08_canonical_p13.json: 0 of 6 item(s) re-ordered
QUARANTINED  ch_08_canonical_p13.json -> backup/quarantine/social_sciences/vii/ch_08_canonical_p13_20260816_113844.json

DETERMINISTIC CHECKS HAVE FAILURES — do not certify Failed files are QUARANTINED under backup/quarantine/ (the fix worklist); regenerate them and re-run --certify-only..
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
