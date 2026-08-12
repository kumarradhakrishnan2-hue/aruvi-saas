# Library certification · the_world_around_us III ch 12 · 20260812_184836

plan: counts [16, 13, 10] · basis authored_standard · registry 7 sections

PASS  library complete: ['ch_12_canonical.json', 'ch_12_canonical_p13.json', 'ch_12_canonical_p10.json'] vs plan [16, 13, 10]
serve granularity: unit  ·  section axis: True
PASS  ch_12_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_12_canonical.json: every anchor verbatim in the top registry
PASS  ch_12_canonical.json: first-visit order follows the registry
PASS  ch_12_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_12_canonical_p13.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_12_canonical_p13.json: every anchor verbatim in the top registry
PASS  ch_12_canonical_p13.json: first-visit order follows the registry
PASS  ch_12_canonical_p13.json: coverage reaches the final registry section
PASS  ch_12_canonical_p10.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_12_canonical_p10.json: every anchor verbatim in the top registry
PASS  ch_12_canonical_p10.json: first-visit order follows the registry
PASS  ch_12_canonical_p10.json: coverage reaches the final registry section
PASS  ch_12_canonical.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 16 handoff group(s) for 16 unit(s) — at most 16 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_12_canonical.json: 15 unit(s) wear a section label the handoff does not route items through: U1=how is waste created?, U2=how is waste created?, U3=ways to manage waste, U4=ways to manage waste, U5=reduce, U6=reduce …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_12_canonical_p13.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 13 handoff group(s) for 13 unit(s) — at most 13 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_12_canonical_p13.json: 13 unit(s) wear a section label the handoff does not route items through: U1=how is waste created?, U2=how is waste created?, U3=ways to manage waste, U4=ways to manage waste, U5=reduce, U6=reduce …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_12_canonical_p10.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 10 handoff group(s) for 10 unit(s) — at most 10 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_12_canonical_p10.json: 10 unit(s) wear a section label the handoff does not route items through: U1=how is waste created?, U2=ways to manage waste, U3=reduce, U4=reduce, U5=reuse, U6=reuse …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_12_canonical.json: register scan reached the band text (64 band(s) read: {'activity_title': 16, 'materials': 51, 'visual_aids': 8, 'teacher_facilitation_note': 16, 'time_bands': 64})
PASS  ch_12_canonical.json: register clean (0 ban hit(s))
      ADVISORY ch_12_canonical.json: 1 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U16 time_bands[2] 30-38: 'display their posters' — Children display their posters on their desks. A gallery walk: children move around readin…
PASS  ch_12_canonical_p13.json: register scan reached the band text (52 band(s) read: {'activity_title': 13, 'materials': 44, 'visual_aids': 6, 'teacher_facilitation_note': 13, 'time_bands': 52})
PASS  ch_12_canonical_p13.json: register clean (0 ban hit(s))
      ADVISORY ch_12_canonical_p13.json: 1 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U2 time_bands[0] 0-6: 'built previously' — Teacher recaps the class list of waste types built previously (from memory, retelling the ideas — not a named earlier uni…
PASS  ch_12_canonical_p10.json: register scan reached the band text (40 band(s) read: {'activity_title': 10, 'materials': 38, 'visual_aids': 7, 'teacher_facilitation_note': 10, 'time_bands': 40})
PASS  ch_12_canonical_p10.json: register clean (0 ban hit(s))
PASS  ch_12_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_12_canonical_p13.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_12_canonical_p10.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_12_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_12_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_12_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_12_canonical_p13.json: every question_type is a known assessment type (0 not)
PASS  ch_12_canonical_p13.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_12_canonical_p13.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_12_canonical_p10.json: every question_type is a known assessment type (0 not)
PASS  ch_12_canonical_p10.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_12_canonical_p10.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_12_canonical.json: MCQ options in arrangement order
PASS  ch_12_canonical_p13.json: MCQ options in arrangement order
PASS  ch_12_canonical_p10.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {}
      ch_12_canonical.json: 16 items vs 16 expected
      ch_12_canonical_p13.json: 13 items vs 13 expected
      ch_12_canonical_p10.json: 10 items vs 10 expected
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

serve sweep: {"8": "fill/single -1s", "9": "fill/single", "10": "identity", "11": "rescue/complete (from 13)", "12": "fill/single", "13": "identity", "14": "synthesis", "15": "synthesis", "16": "identity", "17": "surrender", "18": "surrender"}

options arranged: 0 of 9 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_12_canonical.json: 0 of 4 item(s) re-ordered
      ch_12_canonical_p10.json: 0 of 2 item(s) re-ordered
      ch_12_canonical_p13.json: 0 of 3 item(s) re-ordered

DETERMINISTIC CHECKS ALL PASS.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
