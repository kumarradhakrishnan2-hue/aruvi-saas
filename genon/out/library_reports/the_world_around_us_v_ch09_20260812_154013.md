# Library certification · the_world_around_us V ch 9 · 20260812_154013

plan: counts [12, 10, 7] · basis authored_standard · registry 4 sections

PASS  library complete: ['ch_09_canonical.json', 'ch_09_canonical_p10.json', 'ch_09_canonical_p07.json'] vs plan [12, 10, 7]
serve granularity: unit  ·  section axis: True
PASS  ch_09_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_09_canonical.json: every anchor verbatim in the top registry
PASS  ch_09_canonical.json: first-visit order follows the registry
PASS  ch_09_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_09_canonical_p10.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_09_canonical_p10.json: every anchor verbatim in the top registry
PASS  ch_09_canonical_p10.json: first-visit order follows the registry
PASS  ch_09_canonical_p10.json: coverage reaches the final registry section
PASS  ch_09_canonical_p07.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_09_canonical_p07.json: every anchor verbatim in the top registry
PASS  ch_09_canonical_p07.json: first-visit order follows the registry
PASS  ch_09_canonical_p07.json: coverage reaches the final registry section
PASS  ch_09_canonical.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 12 handoff group(s) for 12 unit(s) — at most 12 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_09_canonical.json: 11 unit(s) wear a section label the handoff does not route items through: U1=changes around us, U2=changes around us, U3=changes around us in a day (day and night), U4=changes around us in a day (day and night), U5=changes around us in a year (seasons), U6=changes around us in a year (seasons) …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_09_canonical_p10.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 10 handoff group(s) for 10 unit(s) — at most 10 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_09_canonical_p10.json: 10 unit(s) wear a section label the handoff does not route items through: U1=changes around us, U2=changes around us, U3=changes around us in a day (day and night), U4=changes around us in a day (day and night), U5=changes around us in a year (seasons), U6=changes around us in a year (seasons) …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_09_canonical_p07.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 7 handoff group(s) for 7 unit(s) — at most 7 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_09_canonical_p07.json: 7 unit(s) wear a section label the handoff does not route items through: U1=changes around us, U2=changes around us in a day (day and night), U3=changes around us in a year (seasons), U4=changes around us in a year (seasons), U5=changes around us in a year (seasons), U6=celebrating seasons …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_09_canonical.json: register scan reached the band text (48 band(s) read: {'activity_title': 12, 'materials': 51, 'teacher_facilitation_note': 12, 'time_bands': 48, 'visual_aids': 9})
PASS  ch_09_canonical.json: register clean (0 ban hit(s))
PASS  ch_09_canonical_p10.json: register scan reached the band text (40 band(s) read: {'activity_title': 10, 'materials': 36, 'teacher_facilitation_note': 10, 'time_bands': 40, 'visual_aids': 7})
PASS  ch_09_canonical_p10.json: register clean (0 ban hit(s))
PASS  ch_09_canonical_p07.json: register scan reached the band text (29 band(s) read: {'activity_title': 7, 'materials': 27, 'teacher_facilitation_note': 7, 'time_bands': 29, 'visual_aids': 4})
PASS  ch_09_canonical_p07.json: register clean (0 ban hit(s))
PASS  ch_09_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_09_canonical_p10.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_09_canonical_p07.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_09_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_09_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_09_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_09_canonical_p10.json: every question_type is a known assessment type (0 not)
PASS  ch_09_canonical_p10.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_09_canonical_p10.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_09_canonical_p07.json: every question_type is a known assessment type (0 not)
PASS  ch_09_canonical_p07.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_09_canonical_p07.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_09_canonical.json: MCQ options in arrangement order
PASS  ch_09_canonical_p10.json: MCQ options in arrangement order
PASS  ch_09_canonical_p07.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {}
      ch_09_canonical.json: 12 items vs 12 expected
      ch_09_canonical_p10.json: 9 items vs 9 expected
      ch_09_canonical_p07.json: 7 items vs 7 expected
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)
PASS  X=12: choice set non-empty (no defensive truncation)
PASS  X=13: choice set non-empty (no defensive truncation)
PASS  X=14: choice set non-empty (no defensive truncation)

serve sweep: {"5": "fill/single", "6": "fill/single", "7": "identity", "8": "fill/single", "9": "synthesis", "10": "identity", "11": "synthesis", "12": "identity", "13": "surrender", "14": "surrender"}

options arranged: 0 of 7 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_09_canonical.json: 0 of 2 item(s) re-ordered
      ch_09_canonical_p07.json: 0 of 2 item(s) re-ordered
      ch_09_canonical_p10.json: 0 of 3 item(s) re-ordered

DETERMINISTIC CHECKS ALL PASS.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
