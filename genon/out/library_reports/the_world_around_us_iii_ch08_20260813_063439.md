# Library certification · the_world_around_us III ch 8 · 20260813_063439

plan: counts [7, 4] · basis authored_standard · registry 5 sections

PASS  library complete: ['ch_08_canonical.json', 'ch_08_canonical_p04.json'] vs plan [7, 4]
serve granularity: unit  ·  section axis: True
PASS  ch_08_canonical.json: every section the chapter summary carries is anchored by some unit (5 summary section(s) vs 5 registry entr(ies))
PASS  ch_08_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_08_canonical.json: every anchor verbatim in the top registry
PASS  ch_08_canonical.json: first-visit order follows the registry
PASS  ch_08_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_08_canonical_p04.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_08_canonical_p04.json: every anchor verbatim in the top registry
PASS  ch_08_canonical_p04.json: first-visit order follows the registry
PASS  ch_08_canonical_p04.json: coverage reaches the final registry section
PASS  ch_08_canonical.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 7 handoff group(s) for 7 unit(s) — at most 7 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_08_canonical.json: 6 unit(s) wear a section label the handoff does not route items through: U1=my favourite food, U2=story of shirin — the runner, U3=we eat different things, U4=where does food come from?, U5=where does food come from?, U6=let us reflect  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_08_canonical_p04.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 4 handoff group(s) for 4 unit(s) — at most 4 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_08_canonical_p04.json: 4 unit(s) wear a section label the handoff does not route items through: U1=my favourite food, U2=story of shirin — the runner, U3=we eat different things/where does food come from?, U4=let us reflect  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_08_canonical.json: register scan reached the band text (28 band(s) read: {'activity_title': 7, 'materials': 19, 'teacher_facilitation_note': 7, 'time_bands': 28, 'visual_aids': 4})
PASS  ch_08_canonical.json: register clean (0 ban hit(s))
PASS  ch_08_canonical_p04.json: register scan reached the band text (16 band(s) read: {'activity_title': 4, 'materials': 12, 'teacher_facilitation_note': 4, 'time_bands': 16, 'visual_aids': 2})
PASS  ch_08_canonical_p04.json: register clean (0 ban hit(s))
PASS  ch_08_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_08_canonical_p04.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_08_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_08_canonical.json: ['ECR'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_08_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_08_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_08_canonical_p04.json: every question_type is a known assessment type (0 not)
PASS  ch_08_canonical_p04.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_08_canonical_p04.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_08_canonical.json: MCQ options in arrangement order
PASS  ch_08_canonical_p04.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {}
      ch_08_canonical.json: 7 items vs 7 expected
      ch_08_canonical_p04.json: 4 items vs 4 expected
PASS  X=2: choice set non-empty (no defensive truncation)
PASS  X=3: choice set non-empty (no defensive truncation)
PASS  X=4: choice set non-empty (no defensive truncation)
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)

serve sweep: {"2": "fill/single -3s", "3": "fill/forward -1s", "4": "identity", "5": "fill/single", "6": "fill/single", "7": "identity", "8": "surrender", "9": "surrender"}

options arranged: 0 of 3 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_08_canonical.json: 0 of 2 item(s) re-ordered
      ch_08_canonical_p04.json: 0 of 1 item(s) re-ordered

DETERMINISTIC CHECKS ALL PASS.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
