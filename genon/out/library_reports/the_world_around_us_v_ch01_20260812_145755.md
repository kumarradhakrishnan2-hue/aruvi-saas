# Library certification · the_world_around_us V ch 1 · 20260812_145755

plan: counts [14, 11, 8] · basis authored_standard · registry 7 sections

PASS  library complete: ['ch_01_canonical.json', 'ch_01_canonical_p11.json', 'ch_01_canonical_p08.json'] vs plan [14, 11, 8]
serve granularity: unit  ·  section axis: True
PASS  ch_01_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_01_canonical.json: every anchor verbatim in the top registry
PASS  ch_01_canonical.json: first-visit order follows the registry
PASS  ch_01_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_01_canonical_p11.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_01_canonical_p11.json: every anchor verbatim in the top registry
PASS  ch_01_canonical_p11.json: first-visit order follows the registry
PASS  ch_01_canonical_p11.json: coverage reaches the final registry section
PASS  ch_01_canonical_p08.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_01_canonical_p08.json: every anchor verbatim in the top registry
PASS  ch_01_canonical_p08.json: first-visit order follows the registry
PASS  ch_01_canonical_p08.json: coverage reaches the final registry section
PASS  ch_01_canonical.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 14 handoff group(s) for 14 unit(s) — at most 14 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_01_canonical.json: 13 unit(s) wear a section label the handoff does not route items through: U1=water on earth, U2=water has different forms, U3=water cycle, U4=groundwater, U5=surface water, U6=surface water …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_01_canonical_p11.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 11 handoff group(s) for 11 unit(s) — at most 11 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_01_canonical_p11.json: 11 unit(s) wear a section label the handoff does not route items through: U1=water on earth, U2=water has different forms, U3=water cycle, U4=groundwater, U5=surface water, U6=surface water …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_01_canonical_p08.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 8 handoff group(s) for 8 unit(s) — at most 8 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_01_canonical_p08.json: 8 unit(s) wear a section label the handoff does not route items through: U1=water on earth, U2=water has different forms, U3=water cycle, U4=groundwater, U5=surface water, U6=surface water …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_01_canonical.json: register scan reached the band text (70 band(s) read: {'activity_title': 14, 'materials': 60, 'visual_aids': 9, 'teacher_facilitation_note': 14, 'time_bands': 70})
PASS  ch_01_canonical.json: register clean (0 ban hit(s))
PASS  ch_01_canonical_p11.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 50, 'visual_aids': 8, 'teacher_facilitation_note': 11, 'time_bands': 44})
FAIL  ch_01_canonical_p11.json: register clean (1 ban hit(s))
      U10 time_bands[2] 20-33 [clock] …to rainwater in a forest compared to a city?' Pairs discuss for a few minutes, then share. Teacher scribes key contrasting ideas on the b…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_01_canonical_p08.json: register scan reached the band text (32 band(s) read: {'activity_title': 8, 'materials': 40, 'visual_aids': 7, 'teacher_facilitation_note': 8, 'time_bands': 32})
FAIL  ch_01_canonical_p08.json: register clean (1 ban hit(s))
      U3 time_bands[1] 7-22 [clock] …them to a sunny spot. Students watch the inside of the bag for a few minutes and begin filling the 'I Observe' column of their table, no…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_01_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_01_canonical_p11.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_01_canonical_p08.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_01_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_01_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_01_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_01_canonical_p11.json: every question_type is a known assessment type (0 not)
PASS  ch_01_canonical_p11.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_01_canonical_p11.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_01_canonical_p08.json: every question_type is a known assessment type (0 not)
PASS  ch_01_canonical_p08.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_01_canonical_p08.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_01_canonical.json: MCQ options in arrangement order
PASS  ch_01_canonical_p11.json: MCQ options in arrangement order
PASS  ch_01_canonical_p08.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {}
      ch_01_canonical.json: 14 items vs 14 expected
      ch_01_canonical_p11.json: 11 items vs 11 expected
      ch_01_canonical_p08.json: 8 items vs 8 expected
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)
PASS  X=12: choice set non-empty (no defensive truncation)
PASS  X=13: choice set non-empty (no defensive truncation)
PASS  X=14: choice set non-empty (no defensive truncation)
PASS  X=15: choice set non-empty (no defensive truncation)
PASS  X=16: choice set non-empty (no defensive truncation)

serve sweep: {"6": "fill/single -1s", "7": "fill/single -1s", "8": "identity", "9": "fill/single", "10": "fill/single", "11": "identity", "12": "synthesis", "13": "synthesis", "14": "identity", "15": "surrender", "16": "surrender"}

options arranged: 6 of 10 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_01_canonical.json: 0 of 4 item(s) re-ordered
      ch_01_canonical_p08.json: 3 of 3 item(s) re-ordered
          #1 C-4.4 U1: A–D now hold DCBA · correct B -> C
          #4 C-6.1 U4: A–D now hold BDAC · correct C -> D
          #6 C-5.3 U6: A–D now hold BDAC · correct B -> A
      ch_01_canonical_p11.json: 3 of 3 item(s) re-ordered
          #1 C-2.1 U1: A–D now hold DBAC · correct B -> B
          #4 C-4.4 U4: A–D now hold ACDB · correct C -> B
          #6 C-5.3 U6: A–D now hold CADB · correct C -> A

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
