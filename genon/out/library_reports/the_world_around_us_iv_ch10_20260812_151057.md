# Library certification · the_world_around_us IV ch 10 · 20260812_151057

plan: counts [10, 8, 6] · basis authored_standard · registry 4 sections

PASS  library complete: ['ch_10_canonical.json', 'ch_10_canonical_p08.json', 'ch_10_canonical_p06.json'] vs plan [10, 8, 6]
serve granularity: unit  ·  section axis: True
PASS  ch_10_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_10_canonical.json: every anchor verbatim in the top registry
PASS  ch_10_canonical.json: first-visit order follows the registry
PASS  ch_10_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_10_canonical_p08.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_10_canonical_p08.json: every anchor verbatim in the top registry
PASS  ch_10_canonical_p08.json: first-visit order follows the registry
PASS  ch_10_canonical_p08.json: coverage reaches the final registry section
PASS  ch_10_canonical_p06.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_10_canonical_p06.json: every anchor verbatim in the top registry
PASS  ch_10_canonical_p06.json: first-visit order follows the registry
PASS  ch_10_canonical_p06.json: coverage reaches the final registry section
PASS  ch_10_canonical.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 10 handoff group(s) for 10 unit(s) — at most 10 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_10_canonical.json: 9 unit(s) wear a section label the handoff does not route items through: U1=pictures of the sky, U2=pictures of the sky, U3=pictures of the sky, U4=the shadows, U5=the shadows, U6=night sky …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_10_canonical_p08.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 8 handoff group(s) for 8 unit(s) — at most 8 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_10_canonical_p08.json: 8 unit(s) wear a section label the handoff does not route items through: U1=pictures of the sky, U2=pictures of the sky, U3=the shadows, U4=the shadows, U5=night sky, U6=night sky …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_10_canonical_p06.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 6 handoff group(s) for 6 unit(s) — at most 6 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_10_canonical_p06.json: 6 unit(s) wear a section label the handoff does not route items through: U1=pictures of the sky, U2=pictures of the sky, U3=the shadows, U4=night sky, U5=india's chandrayaan mission, U6=india's chandrayaan mission  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_10_canonical.json: register scan reached the band text (42 band(s) read: {'activity_title': 10, 'materials': 36, 'teacher_facilitation_note': 10, 'time_bands': 42, 'visual_aids': 6})
PASS  ch_10_canonical.json: register clean (0 ban hit(s))
PASS  ch_10_canonical_p08.json: register scan reached the band text (33 band(s) read: {'activity_title': 8, 'materials': 30, 'visual_aids': 5, 'teacher_facilitation_note': 8, 'time_bands': 33})
PASS  ch_10_canonical_p08.json: register clean (0 ban hit(s))
PASS  ch_10_canonical_p06.json: register scan reached the band text (24 band(s) read: {'activity_title': 6, 'materials': 18, 'visual_aids': 3, 'teacher_facilitation_note': 6, 'time_bands': 24})
PASS  ch_10_canonical_p06.json: register clean (0 ban hit(s))
PASS  ch_10_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_10_canonical_p08.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_10_canonical_p06.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_10_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_10_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_10_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_10_canonical_p08.json: every question_type is a known assessment type (0 not)
PASS  ch_10_canonical_p08.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_10_canonical_p08.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_10_canonical_p06.json: every question_type is a known assessment type (0 not)
PASS  ch_10_canonical_p06.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_10_canonical_p06.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_10_canonical.json: MCQ options in arrangement order
PASS  ch_10_canonical_p08.json: MCQ options in arrangement order
PASS  ch_10_canonical_p06.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {}
      ch_10_canonical.json: 10 items vs 10 expected
      ch_10_canonical_p08.json: 8 items vs 8 expected
      ch_10_canonical_p06.json: 6 items vs 6 expected
PASS  X=4: choice set non-empty (no defensive truncation)
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)
PASS  X=12: choice set non-empty (no defensive truncation)

serve sweep: {"4": "fill/single -1s", "5": "fill/single", "6": "identity", "7": "fill/single", "8": "identity", "9": "synthesis", "10": "identity", "11": "surrender", "12": "surrender"}

options arranged: 0 of 6 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_10_canonical.json: 0 of 3 item(s) re-ordered
      ch_10_canonical_p06.json: 0 of 1 item(s) re-ordered
      ch_10_canonical_p08.json: 0 of 2 item(s) re-ordered

DETERMINISTIC CHECKS ALL PASS.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
