# Library certification · the_world_around_us IV ch 3 · 20260812_145756

plan: counts [16, 13, 10] · basis authored_standard · registry 5 sections

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
PASS  ch_03_canonical.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 16 handoff group(s) for 16 unit(s) — at most 16 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_03_canonical.json: 15 unit(s) wear a section label the handoff does not route items through: U1=the adventure begins, U2=animals in the forest, U3=animals in the forest, U4=animals in the forest, U5=animals in the forest, U6=animals in the forest …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_03_canonical_p13.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 13 handoff group(s) for 13 unit(s) — at most 13 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_03_canonical_p13.json: 13 unit(s) wear a section label the handoff does not route items through: U1=the adventure begins, U2=animals in the forest, U3=animals in the forest, U4=animals in the forest, U5=animals in the forest, U6=animals in the forest …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_03_canonical_p10.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 10 handoff group(s) for 10 unit(s) — at most 10 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_03_canonical_p10.json: 10 unit(s) wear a section label the handoff does not route items through: U1=the adventure begins, U2=animals in the forest, U3=animals in the forest, U4=animals in the forest, U5=animals in the forest, U6=animals in the forest …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_03_canonical.json: register scan reached the band text (64 band(s) read: {'activity_title': 16, 'materials': 64, 'teacher_facilitation_note': 16, 'time_bands': 64, 'visual_aids': 8})
PASS  ch_03_canonical.json: register clean (0 ban hit(s))
PASS  ch_03_canonical_p13.json: register scan reached the band text (52 band(s) read: {'activity_title': 13, 'materials': 56, 'visual_aids': 10, 'teacher_facilitation_note': 13, 'time_bands': 52})
FAIL  ch_03_canonical_p13.json: register clean (1 ban hit(s))
      U3 time_bands[3] 33-40 [forward] …, crabs, fish — making a short list in their notebooks as a bridge to the section's content on water-dwelling animals. The teacher as…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_03_canonical_p10.json: register scan reached the band text (40 band(s) read: {'activity_title': 10, 'materials': 46, 'visual_aids': 9, 'teacher_facilitation_note': 10, 'time_bands': 40})
FAIL  ch_03_canonical_p10.json: register clean (1 ban hit(s))
      U9 time_bands[0] 0-10 [clock] …teacher sets up the role-play activity from Textbook p. 56: half the class will be plants and animals, the other half will be forest v…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_03_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_03_canonical_p13.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_03_canonical_p10.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_03_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_03_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_03_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_03_canonical_p13.json: every question_type is a known assessment type (0 not)
PASS  ch_03_canonical_p13.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_03_canonical_p13.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_03_canonical_p10.json: every question_type is a known assessment type (0 not)
PASS  ch_03_canonical_p10.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_03_canonical_p10.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_03_canonical.json: MCQ options in arrangement order
PASS  ch_03_canonical_p13.json: MCQ options in arrangement order
PASS  ch_03_canonical_p10.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {}
      ch_03_canonical.json: 16 items vs 16 expected
      ch_03_canonical_p13.json: 13 items vs 13 expected
      ch_03_canonical_p10.json: 10 items vs 10 expected
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

serve sweep: {"8": "fill/single -1s", "9": "fill/single", "10": "identity", "11": "synthesis", "12": "synthesis", "13": "identity", "14": "synthesis", "15": "synthesis", "16": "identity", "17": "surrender", "18": "surrender"}

options arranged: 7 of 12 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_03_canonical.json: 0 of 5 item(s) re-ordered
      ch_03_canonical_p10.json: 3 of 3 item(s) re-ordered
          #1 C-3.1 U1: A–D now hold BADC · correct C -> D
          #4 C-6.1 U4: A–D now hold DACB · correct A -> B
          #7 C-1.1 U7: A–D now hold CADB · correct A -> B
      ch_03_canonical_p13.json: 4 of 4 item(s) re-ordered
          #1 C-3.1 U1: A–D now hold BDAC · correct B -> A
          #3 C-6.1 U3: A–D now hold ADCB · correct C -> C
          #5 C-1.1 U5: A–D now hold DCAB · correct B -> D
          #8 C-1.1 U8: A–D now hold DBAC · correct B -> B

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
