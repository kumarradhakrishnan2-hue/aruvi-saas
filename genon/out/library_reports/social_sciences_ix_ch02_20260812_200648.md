# Library certification · social_sciences IX ch 2 · 20260812_200648

plan: counts [11, 9, 7] · basis authored_standard · registry 9 sections

PASS  library complete: ['ch_02_canonical.json', 'ch_02_canonical_p09.json', 'ch_02_canonical_p07.json'] vs plan [11, 9, 7]
serve granularity: unit  ·  section axis: True
PASS  ch_02_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_02_canonical.json: every anchor verbatim in the top registry
PASS  ch_02_canonical.json: first-visit order follows the registry
PASS  ch_02_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_02_canonical_p09.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_02_canonical_p09.json: every anchor verbatim in the top registry
PASS  ch_02_canonical_p09.json: first-visit order follows the registry
PASS  ch_02_canonical_p09.json: coverage reaches the final registry section
PASS  ch_02_canonical_p07.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_02_canonical_p07.json: every anchor verbatim in the top registry
PASS  ch_02_canonical_p07.json: first-visit order follows the registry
PASS  ch_02_canonical_p07.json: coverage reaches the final registry section
PASS  ch_02_canonical.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 34, 'visual_aids': 9, 'teacher_notes': 11, 'time_bands': 44})
PASS  ch_02_canonical.json: register clean (0 ban hit(s))
PASS  ch_02_canonical_p09.json: register scan reached the band text (36 band(s) read: {'activity_title': 9, 'materials': 27, 'visual_aids': 8, 'teacher_notes': 9, 'time_bands': 36})
PASS  ch_02_canonical_p09.json: register clean (0 ban hit(s))
      ADVISORY ch_02_canonical_p09.json: 3 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U5 teacher_notes: 'from the previous unit' — …ilds the same analytical habit as the coastal-glacial table from the previous unit: shape encodes process.
        U5 time_bands[3] 40-50: 'from the previous unit' — …agent (running water, wind, underground water, and glacier from the previous unit) — filling in: one erosion landform, one depositional landf…
        U8 time_bands[0] 0-12: 'built earlier' — Reactivate the plate boundary framework built earlier — convergent, divergent, transform — and pose the spatial q…
PASS  ch_02_canonical_p07.json: register scan reached the band text (28 band(s) read: {'activity_title': 7, 'materials': 16, 'visual_aids': 6, 'teacher_notes': 7, 'time_bands': 28})
PASS  ch_02_canonical_p07.json: register clean (0 ban hit(s))
PASS  ch_02_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_02_canonical_p09.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_02_canonical_p07.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_02_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_02_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_02_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_02_canonical_p09.json: every question_type is a known assessment type (0 not)
PASS  ch_02_canonical_p09.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_02_canonical_p09.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_02_canonical_p07.json: every question_type is a known assessment type (0 not)
PASS  ch_02_canonical_p07.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_02_canonical_p07.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_02_canonical.json: MCQ options in arrangement order
PASS  ch_02_canonical_p09.json: MCQ options in arrangement order
PASS  ch_02_canonical_p07.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: constitution
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_02_canonical.json: 17 items vs 17 expected
      ch_02_canonical_p09.json: 17 items vs 17 expected
      ch_02_canonical_p07.json: 16 items vs 17 expected  <-- MISS
          C-4.5 (Substantive) has 2, constitution says 3
      -> 1 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)
PASS  X=12: choice set non-empty (no defensive truncation)
PASS  X=13: choice set non-empty (no defensive truncation)

serve sweep: {"5": "fill/forward -2s", "6": "fill/single -1s", "7": "identity", "8": "synthesis", "9": "identity", "10": "fill/single", "11": "identity", "12": "surrender", "13": "surrender"}

options arranged: 0 of 18 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_02_canonical.json: 0 of 6 item(s) re-ordered
      ch_02_canonical_p07.json: 0 of 6 item(s) re-ordered
      ch_02_canonical_p09.json: 0 of 6 item(s) re-ordered

DETERMINISTIC CHECKS ALL PASS.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
