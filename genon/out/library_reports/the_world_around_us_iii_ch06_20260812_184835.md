# Library certification · the_world_around_us III ch 6 · 20260812_184835

plan: counts [17, 14, 10] · basis authored_standard · registry 5 sections

PASS  library complete: ['ch_06_canonical.json', 'ch_06_canonical_p14.json', 'ch_06_canonical_p10.json'] vs plan [17, 14, 10]
serve granularity: unit  ·  section axis: True
PASS  ch_06_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_06_canonical.json: every anchor verbatim in the top registry
PASS  ch_06_canonical.json: first-visit order follows the registry
PASS  ch_06_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_06_canonical_p14.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_06_canonical_p14.json: every anchor verbatim in the top registry
PASS  ch_06_canonical_p14.json: first-visit order follows the registry
PASS  ch_06_canonical_p14.json: coverage reaches the final registry section
PASS  ch_06_canonical_p10.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_06_canonical_p10.json: every anchor verbatim in the top registry
PASS  ch_06_canonical_p10.json: first-visit order follows the registry
PASS  ch_06_canonical_p10.json: coverage reaches the final registry section
PASS  ch_06_canonical.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 17 handoff group(s) for 17 unit(s) — at most 17 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_06_canonical.json: 16 unit(s) wear a section label the handoff does not route items through: U1=living in harmony, U2=living in harmony, U3=the mango tree, U4=the mango tree, U5=we need each other, U6=we need each other …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_06_canonical_p14.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 14 handoff group(s) for 14 unit(s) — at most 14 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_06_canonical_p14.json: 14 unit(s) wear a section label the handoff does not route items through: U1=living in harmony, U2=living in harmony, U3=living in harmony, U4=the mango tree, U5=the mango tree, U6=we need each other …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_06_canonical_p10.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 10 handoff group(s) for 10 unit(s) — at most 10 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_06_canonical_p10.json: 10 unit(s) wear a section label the handoff does not route items through: U1=living in harmony, U2=living in harmony, U3=the mango tree, U4=we need each other, U5=we need each other, U6=we need each other …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_06_canonical.json: register scan reached the band text (68 band(s) read: {'activity_title': 17, 'materials': 59, 'visual_aids': 5, 'teacher_facilitation_note': 17, 'time_bands': 68})
PASS  ch_06_canonical.json: register clean (0 ban hit(s))
PASS  ch_06_canonical_p14.json: register scan reached the band text (56 band(s) read: {'activity_title': 14, 'materials': 42, 'visual_aids': 5, 'teacher_facilitation_note': 14, 'time_bands': 56})
PASS  ch_06_canonical_p14.json: register clean (0 ban hit(s))
      ADVISORY ch_06_canonical_p14.json: 1 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U5 time_bands[0] 0-8: 'from the previous unit' — …its the radial diagram on Textbook p. 77 and the discussion from the previous unit's content about how humans, plants, and animals are connect…
PASS  ch_06_canonical_p10.json: register scan reached the band text (40 band(s) read: {'activity_title': 10, 'materials': 21, 'visual_aids': 2, 'teacher_facilitation_note': 10, 'time_bands': 40})
PASS  ch_06_canonical_p10.json: register clean (0 ban hit(s))
PASS  ch_06_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_06_canonical_p14.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_06_canonical_p10.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_06_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_06_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_06_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_06_canonical_p14.json: every question_type is a known assessment type (0 not)
PASS  ch_06_canonical_p14.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_06_canonical_p14.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_06_canonical_p10.json: every question_type is a known assessment type (0 not)
PASS  ch_06_canonical_p10.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_06_canonical_p10.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_06_canonical.json: MCQ options in arrangement order
PASS  ch_06_canonical_p14.json: MCQ options in arrangement order
PASS  ch_06_canonical_p10.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {}
      ch_06_canonical.json: 17 items vs 17 expected
      ch_06_canonical_p14.json: 14 items vs 14 expected
      ch_06_canonical_p10.json: 10 items vs 10 expected
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

serve sweep: {"8": "fill/single", "9": "synthesis", "10": "identity", "11": "fill/single", "12": "fill/single", "13": "synthesis", "14": "identity", "15": "synthesis", "16": "synthesis", "17": "identity", "18": "surrender", "19": "surrender"}

options arranged: 0 of 12 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_06_canonical.json: 0 of 5 item(s) re-ordered
      ch_06_canonical_p10.json: 0 of 3 item(s) re-ordered
      ch_06_canonical_p14.json: 0 of 4 item(s) re-ordered

DETERMINISTIC CHECKS ALL PASS.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
