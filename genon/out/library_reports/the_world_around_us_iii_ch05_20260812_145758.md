# Library certification · the_world_around_us III ch 5 · 20260812_145758

plan: counts [10, 8, 6] · basis authored_standard · registry 3 sections

PASS  library complete: ['ch_05_canonical.json', 'ch_05_canonical_p08.json', 'ch_05_canonical_p06.json'] vs plan [10, 8, 6]
serve granularity: unit  ·  section axis: True
PASS  ch_05_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_05_canonical.json: every anchor verbatim in the top registry
PASS  ch_05_canonical.json: first-visit order follows the registry
PASS  ch_05_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_05_canonical_p08.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_05_canonical_p08.json: every anchor verbatim in the top registry
PASS  ch_05_canonical_p08.json: first-visit order follows the registry
PASS  ch_05_canonical_p08.json: coverage reaches the final registry section
PASS  ch_05_canonical_p06.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_05_canonical_p06.json: every anchor verbatim in the top registry
PASS  ch_05_canonical_p06.json: first-visit order follows the registry
PASS  ch_05_canonical_p06.json: coverage reaches the final registry section
PASS  ch_05_canonical.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 10 handoff group(s) for 10 unit(s) — at most 10 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_05_canonical.json: 9 unit(s) wear a section label the handoff does not route items through: U1=plants and animals live together, U2=plants and animals live together, U3=life in the soil, U4=life in the soil, U5=life in the soil, U6=life in the soil …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_05_canonical_p08.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 8 handoff group(s) for 8 unit(s) — at most 8 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_05_canonical_p08.json: 8 unit(s) wear a section label the handoff does not route items through: U1=plants and animals live together, U2=plants and animals live together, U3=life in the soil, U4=life in the soil, U5=life in the soil, U6=life in the soil …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_05_canonical_p06.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 6 handoff group(s) for 6 unit(s) — at most 6 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_05_canonical_p06.json: 6 unit(s) wear a section label the handoff does not route items through: U1=plants and animals live together, U2=life in the soil, U3=life in the soil, U4=life in the soil, U5=let us reflect, U6=let us reflect  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_05_canonical.json: register scan reached the band text (41 band(s) read: {'activity_title': 10, 'materials': 32, 'visual_aids': 7, 'teacher_facilitation_note': 10, 'time_bands': 41})
PASS  ch_05_canonical.json: register clean (0 ban hit(s))
PASS  ch_05_canonical_p08.json: register scan reached the band text (32 band(s) read: {'activity_title': 8, 'materials': 26, 'visual_aids': 5, 'teacher_facilitation_note': 8, 'time_bands': 32})
FAIL  ch_05_canonical_p08.json: register clean (1 ban hit(s))
      U7 time_bands[0] 0-8 [clock] …irds, and insects did you notice? Students discuss in pairs for a few minutes, recalling what they have observed.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_05_canonical_p06.json: register scan reached the band text (24 band(s) read: {'activity_title': 6, 'materials': 20, 'visual_aids': 4, 'teacher_facilitation_note': 6, 'time_bands': 24})
PASS  ch_05_canonical_p06.json: register clean (0 ban hit(s))
PASS  ch_05_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_05_canonical_p08.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_05_canonical_p06.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_05_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_05_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_05_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_05_canonical_p08.json: every question_type is a known assessment type (0 not)
PASS  ch_05_canonical_p08.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_05_canonical_p08.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_05_canonical_p06.json: every question_type is a known assessment type (0 not)
PASS  ch_05_canonical_p06.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_05_canonical_p06.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_05_canonical.json: MCQ options in arrangement order
PASS  ch_05_canonical_p08.json: MCQ options in arrangement order
PASS  ch_05_canonical_p06.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {}
      ch_05_canonical.json: 10 items vs 10 expected
      ch_05_canonical_p08.json: 8 items vs 8 expected
      ch_05_canonical_p06.json: 6 items vs 6 expected
PASS  X=4: choice set non-empty (no defensive truncation)
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)
PASS  X=12: choice set non-empty (no defensive truncation)

serve sweep: {"4": "fill/single", "5": "fill/single", "6": "identity", "7": "fill/single", "8": "identity", "9": "synthesis", "10": "identity", "11": "surrender", "12": "surrender"}

options arranged: 5 of 9 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_05_canonical.json: 0 of 4 item(s) re-ordered
      ch_05_canonical_p06.json: 2 of 2 item(s) re-ordered
          #1 C-4.5 U1: A–D now hold BDCA · correct A -> D
          #3 C-1.1 U3: A–D now hold CABD · correct A -> B
      ch_05_canonical_p08.json: 3 of 3 item(s) re-ordered
          #1 C-1.1 U1: A–D now hold CADB · correct B -> D
          #3 C-6.1 U3: A–D now hold CBDA · correct B -> B
          #6 C-4.1 U6: A–D now hold CBAD · correct B -> B

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
