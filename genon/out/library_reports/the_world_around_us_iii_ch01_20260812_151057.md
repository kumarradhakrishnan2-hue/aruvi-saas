# Library certification · the_world_around_us III ch 1 · 20260812_151057

plan: counts [10, 8, 6] · basis authored_standard · registry 5 sections

PASS  library complete: ['ch_01_canonical.json', 'ch_01_canonical_p08.json', 'ch_01_canonical_p06.json'] vs plan [10, 8, 6]
serve granularity: unit  ·  section axis: True
PASS  ch_01_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_01_canonical.json: every anchor verbatim in the top registry
PASS  ch_01_canonical.json: first-visit order follows the registry
PASS  ch_01_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_01_canonical_p08.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_01_canonical_p08.json: every anchor verbatim in the top registry
PASS  ch_01_canonical_p08.json: first-visit order follows the registry
PASS  ch_01_canonical_p08.json: coverage reaches the final registry section
PASS  ch_01_canonical_p06.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_01_canonical_p06.json: every anchor verbatim in the top registry
PASS  ch_01_canonical_p06.json: first-visit order follows the registry
PASS  ch_01_canonical_p06.json: coverage reaches the final registry section
PASS  ch_01_canonical.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 10 handoff group(s) for 10 unit(s) — at most 10 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_01_canonical.json: 9 unit(s) wear a section label the handoff does not route items through: U1=playing together, U2=singing together, U3=singing together, U4=laughing together, U5=laughing together, U6=helping each other …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_01_canonical_p08.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 8 handoff group(s) for 8 unit(s) — at most 8 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_01_canonical_p08.json: 8 unit(s) wear a section label the handoff does not route items through: U1=playing together, U2=singing together, U3=singing together, U4=laughing together, U5=helping each other, U6=helping each other …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_01_canonical_p06.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 6 handoff group(s) for 6 unit(s) — at most 6 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_01_canonical_p06.json: 6 unit(s) wear a section label the handoff does not route items through: U1=playing together, U2=singing together, U3=laughing together, U4=helping each other, U5=helping each other, U6=fun with family and friends  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_01_canonical.json: register scan reached the band text (41 band(s) read: {'activity_title': 10, 'materials': 21, 'teacher_facilitation_note': 10, 'time_bands': 41, 'visual_aids': 2})
PASS  ch_01_canonical.json: register clean (0 ban hit(s))
PASS  ch_01_canonical_p08.json: register scan reached the band text (32 band(s) read: {'activity_title': 8, 'materials': 26, 'teacher_facilitation_note': 8, 'time_bands': 32, 'visual_aids': 3})
PASS  ch_01_canonical_p08.json: register clean (0 ban hit(s))
PASS  ch_01_canonical_p06.json: register scan reached the band text (24 band(s) read: {'activity_title': 6, 'materials': 20, 'teacher_facilitation_note': 6, 'time_bands': 24, 'visual_aids': 3})
PASS  ch_01_canonical_p06.json: register clean (0 ban hit(s))
PASS  ch_01_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_01_canonical_p08.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_01_canonical_p06.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_01_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_01_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_01_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_01_canonical_p08.json: every question_type is a known assessment type (0 not)
PASS  ch_01_canonical_p08.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_01_canonical_p08.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_01_canonical_p06.json: every question_type is a known assessment type (0 not)
PASS  ch_01_canonical_p06.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_01_canonical_p06.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_01_canonical.json: MCQ options in arrangement order
PASS  ch_01_canonical_p08.json: MCQ options in arrangement order
PASS  ch_01_canonical_p06.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {}
      ch_01_canonical.json: 10 items vs 10 expected
      ch_01_canonical_p08.json: 8 items vs 8 expected
      ch_01_canonical_p06.json: 6 items vs 6 expected
PASS  X=4: choice set non-empty (no defensive truncation)
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)
PASS  X=12: choice set non-empty (no defensive truncation)

serve sweep: {"4": "fill/single -1s", "5": "fill/single", "6": "identity", "7": "fill/single", "8": "identity", "9": "fill/single", "10": "identity", "11": "surrender", "12": "surrender"}

options arranged: 0 of 7 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_01_canonical.json: 0 of 3 item(s) re-ordered
      ch_01_canonical_p06.json: 0 of 2 item(s) re-ordered
      ch_01_canonical_p08.json: 0 of 2 item(s) re-ordered

DETERMINISTIC CHECKS ALL PASS.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
