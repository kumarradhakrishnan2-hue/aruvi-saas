# Library certification · social_sciences VIII ch 3 · 20260809_100221

plan: counts [16, 13, 10] · basis authored_standard · registry 11 sections

PASS  library complete: ['ch_03_canonical.json', 'ch_03_canonical_p13.json', 'ch_03_canonical_p10.json'] vs plan [16, 13, 10]
serve granularity: unit  ·  section axis: True
PASS  ch_03_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_03_canonical.json: every anchor verbatim in the top registry
PASS  ch_03_canonical.json: first-visit order follows the registry
PASS  ch_03_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_03_canonical_p13.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_03_canonical_p13.json: every anchor verbatim in the top registry
PASS  ch_03_canonical_p13.json: first-visit order follows the registry
PASS  ch_03_canonical_p13.json: coverage reaches the final registry section
PASS  ch_03_canonical_p10.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_03_canonical_p10.json: every anchor verbatim in the top registry
PASS  ch_03_canonical_p10.json: first-visit order follows the registry
PASS  ch_03_canonical_p10.json: coverage reaches the final registry section
PASS  ch_03_canonical.json: register scan reached the band text (64 band(s) read: {'activity_title': 16, 'teacher_notes': 16, 'time_bands': 64, 'homework': 1})
PASS  ch_03_canonical.json: register clean (0 ban hit(s))
PASS  ch_03_canonical_p13.json: register scan reached the band text (52 band(s) read: {'activity_title': 13, 'teacher_notes': 13, 'time_bands': 52, 'homework': 2})
PASS  ch_03_canonical_p13.json: register clean (0 ban hit(s))
PASS  ch_03_canonical_p10.json: register scan reached the band text (40 band(s) read: {'activity_title': 10, 'teacher_notes': 10, 'time_bands': 40, 'homework': 4})
PASS  ch_03_canonical_p10.json: register clean (0 ban hit(s))
PASS  ch_03_canonical.json: MCQ options in arrangement order
PASS  ch_03_canonical_p13.json: MCQ options in arrangement order
PASS  ch_03_canonical_p10.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_03_canonical.json: 20 items vs 20 expected
      ch_03_canonical_p13.json: 19 items vs 20 expected  <-- MISS
          C-9.1 (Present) has 1, its siblings carry 2
      ch_03_canonical_p10.json: 20 items vs 20 expected
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

serve sweep: {"8": "fill/single -2s", "9": "fill/single -1s", "10": "identity", "11": "fill/single", "12": "synthesis", "13": "identity", "14": "fill/single", "15": "synthesis", "16": "identity", "17": "surrender", "18": "surrender"}

options arranged: 0 of 41 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_03_canonical.json: 0 of 14 item(s) re-ordered
      ch_03_canonical_p10.json: 0 of 14 item(s) re-ordered
      ch_03_canonical_p13.json: 0 of 13 item(s) re-ordered

DETERMINISTIC CHECKS ALL PASS.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
