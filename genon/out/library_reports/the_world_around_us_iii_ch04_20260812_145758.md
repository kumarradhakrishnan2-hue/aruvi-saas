# Library certification · the_world_around_us III ch 4 · 20260812_145758

plan: counts [13, 11, 8] · basis authored_standard · registry 6 sections

PASS  library complete: ['ch_04_canonical.json', 'ch_04_canonical_p11.json', 'ch_04_canonical_p08.json'] vs plan [13, 11, 8]
serve granularity: unit  ·  section axis: True
PASS  ch_04_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_04_canonical.json: every anchor verbatim in the top registry
PASS  ch_04_canonical.json: first-visit order follows the registry
PASS  ch_04_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_04_canonical_p11.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_04_canonical_p11.json: every anchor verbatim in the top registry
PASS  ch_04_canonical_p11.json: first-visit order follows the registry
PASS  ch_04_canonical_p11.json: coverage reaches the final registry section
PASS  ch_04_canonical_p08.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_04_canonical_p08.json: every anchor verbatim in the top registry
PASS  ch_04_canonical_p08.json: first-visit order follows the registry
PASS  ch_04_canonical_p08.json: coverage reaches the final registry section
PASS  ch_04_canonical.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 13 handoff group(s) for 13 unit(s) — at most 13 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_04_canonical.json: 12 unit(s) wear a section label the handoff does not route items through: U1=so many kinds of plants, U2=shrubs, U3=herbs and grasses, U4=climbers and creepers, U5=climbers and creepers, U6=parts of a plant …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_04_canonical_p11.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 11 handoff group(s) for 11 unit(s) — at most 11 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_04_canonical_p11.json: 11 unit(s) wear a section label the handoff does not route items through: U1=so many kinds of plants, U2=shrubs, U3=herbs and grasses, U4=climbers and creepers, U5=climbers and creepers, U6=parts of a plant …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_04_canonical_p08.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 8 handoff group(s) for 8 unit(s) — at most 8 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_04_canonical_p08.json: 8 unit(s) wear a section label the handoff does not route items through: U1=so many kinds of plants, U2=shrubs, U3=herbs and grasses, U4=climbers and creepers, U5=parts of a plant, U6=parts of a plant …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_04_canonical.json: register scan reached the band text (52 band(s) read: {'activity_title': 13, 'materials': 42, 'visual_aids': 7, 'teacher_facilitation_note': 13, 'time_bands': 52})
PASS  ch_04_canonical.json: register clean (0 ban hit(s))
PASS  ch_04_canonical_p11.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 37, 'visual_aids': 8, 'teacher_facilitation_note': 11, 'time_bands': 44})
PASS  ch_04_canonical_p11.json: register clean (0 ban hit(s))
PASS  ch_04_canonical_p08.json: register scan reached the band text (32 band(s) read: {'activity_title': 8, 'materials': 27, 'visual_aids': 8, 'teacher_facilitation_note': 8, 'time_bands': 32})
FAIL  ch_04_canonical_p08.json: register clean (1 ban hit(s))
      U3 teacher_facilitation_note [calendar] …-grain connection gently: ask which grains the children ate this week and let them discover that the grain is a grass seed. If ch…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_04_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_04_canonical_p11.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_04_canonical_p08.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_04_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_04_canonical.json: ['ECR'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_04_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_04_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_04_canonical_p11.json: every question_type is a known assessment type (0 not)
PASS  ch_04_canonical_p11.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_04_canonical_p11.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_04_canonical_p08.json: every question_type is a known assessment type (0 not)
PASS  ch_04_canonical_p08.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_04_canonical_p08.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_04_canonical.json: MCQ options in arrangement order
PASS  ch_04_canonical_p11.json: MCQ options in arrangement order
PASS  ch_04_canonical_p08.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {}
      ch_04_canonical.json: 13 items vs 13 expected
      ch_04_canonical_p11.json: 11 items vs 11 expected
      ch_04_canonical_p08.json: 8 items vs 8 expected
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

serve sweep: {"6": "fill/single", "7": "fill/single", "8": "identity", "9": "fill/single", "10": "fill/single", "11": "identity", "12": "synthesis", "13": "identity", "14": "surrender", "15": "surrender"}

options arranged: 6 of 10 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_04_canonical.json: 0 of 4 item(s) re-ordered
      ch_04_canonical_p08.json: 3 of 3 item(s) re-ordered
          #1 C-1.1 U1: A–D now hold CABD · correct B -> C
          #3 C-4.1 U3: A–D now hold DCAB · correct C -> B
          #5 C-1.1 U5: A–D now hold CBAD · correct B -> B
      ch_04_canonical_p11.json: 3 of 3 item(s) re-ordered
          #1 C-1.1 U1: A–D now hold CDAB · correct B -> D
          #3 C-4.3 U3: A–D now hold ACBD · correct B -> C
          #6 C-1.1 U6: A–D now hold ACBD · correct A -> A

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
