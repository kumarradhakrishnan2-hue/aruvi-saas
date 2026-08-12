# Library certification · the_world_around_us IV ch 6 · 20260812_145757

plan: counts [19, 15, 11] · basis authored_standard · registry 7 sections

PASS  library complete: ['ch_06_canonical.json', 'ch_06_canonical_p15.json', 'ch_06_canonical_p11.json'] vs plan [19, 15, 11]
serve granularity: unit  ·  section axis: True
PASS  ch_06_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_06_canonical.json: every anchor verbatim in the top registry
PASS  ch_06_canonical.json: first-visit order follows the registry
PASS  ch_06_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_06_canonical_p15.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_06_canonical_p15.json: every anchor verbatim in the top registry
PASS  ch_06_canonical_p15.json: first-visit order follows the registry
PASS  ch_06_canonical_p15.json: coverage reaches the final registry section
PASS  ch_06_canonical_p11.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_06_canonical_p11.json: every anchor verbatim in the top registry
PASS  ch_06_canonical_p11.json: first-visit order follows the registry
PASS  ch_06_canonical_p11.json: coverage reaches the final registry section
PASS  ch_06_canonical.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 19 handoff group(s) for 19 unit(s) — at most 19 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_06_canonical.json: 18 unit(s) wear a section label the handoff does not route items through: U1=journey of the grains, U2=journey of the grains, U3=journey of the grains, U4=journey of the grains, U5=mindful eating, U6=mindful eating …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_06_canonical_p15.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 15 handoff group(s) for 15 unit(s) — at most 15 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_06_canonical_p15.json: 15 unit(s) wear a section label the handoff does not route items through: U1=journey of the grains, U2=journey of the grains, U3=journey of the grains, U4=mindful eating, U5=valuing food, U6=valuing food …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_06_canonical_p11.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 11 handoff group(s) for 11 unit(s) — at most 11 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_06_canonical_p11.json: 11 unit(s) wear a section label the handoff does not route items through: U1=journey of the grains, U2=journey of the grains, U3=mindful eating, U4=valuing food, U5=enjoy sports, U6=enjoy sports …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_06_canonical.json: register scan reached the band text (76 band(s) read: {'activity_title': 19, 'materials': 55, 'visual_aids': 6, 'teacher_facilitation_note': 19, 'time_bands': 76})
PASS  ch_06_canonical.json: register clean (0 ban hit(s))
PASS  ch_06_canonical_p15.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 47, 'visual_aids': 7, 'teacher_facilitation_note': 15, 'time_bands': 60})
FAIL  ch_06_canonical_p15.json: register clean (2 ban hit(s))
      U2 time_bands[0] 0-6 [completion] …n's journey that students have already examined — and asks: Now that we have seen who helps the grain, let's think about the farmer specifica…
      U6 time_bands[3] 33-40 [calendar] …cific change they will make in how they handle food at home this week, and why it matters. A few students share their commitment…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_06_canonical_p11.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 37, 'visual_aids': 6, 'teacher_facilitation_note': 11, 'time_bands': 44})
FAIL  ch_06_canonical_p11.json: register clean (1 ban hit(s))
      U5 time_bands[0] 0-7 [clock] …ents open Textbook p. 94 and observe the park scene picture for a quiet two minutes without talking. Teacher then asks: 'How many different phy…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_06_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_06_canonical_p15.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_06_canonical_p11.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_06_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_06_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_06_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_06_canonical_p15.json: every question_type is a known assessment type (0 not)
PASS  ch_06_canonical_p15.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_06_canonical_p15.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_06_canonical_p11.json: every question_type is a known assessment type (0 not)
PASS  ch_06_canonical_p11.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_06_canonical_p11.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_06_canonical.json: MCQ options in arrangement order
PASS  ch_06_canonical_p15.json: MCQ options in arrangement order
PASS  ch_06_canonical_p11.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {}
      ch_06_canonical.json: 19 items vs 19 expected
      ch_06_canonical_p15.json: 15 items vs 15 expected
      ch_06_canonical_p11.json: 11 items vs 11 expected
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
PASS  X=20: choice set non-empty (no defensive truncation)
PASS  X=21: choice set non-empty (no defensive truncation)

serve sweep: {"9": "fill/single", "10": "synthesis", "11": "identity", "12": "fill/single", "13": "fill/single", "14": "synthesis", "15": "identity", "16": "fill/single", "17": "fill/single", "18": "synthesis", "19": "identity", "20": "surrender", "21": "surrender"}

options arranged: 9 of 14 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_06_canonical.json: 0 of 5 item(s) re-ordered
      ch_06_canonical_p11.json: 3 of 3 item(s) re-ordered
          #1 C-2.1 U1: A–D now hold DABC · correct A -> B
          #5 C-2.1 U5: A–D now hold DABC · correct A -> B
          #9 C-2.1 U9: A–D now hold BDCA · correct A -> D
      ch_06_canonical_p15.json: 6 of 6 item(s) re-ordered
          #1 C-2.1 U1: A–D now hold DCAB · correct C -> B
          #3 C-2.2 U3: A–D now hold DBAC · correct B -> B
          #5 C-6.1 U5: A–D now hold CBAD · correct B -> B
          #7 C-3.1 U7: A–D now hold BADC · correct B -> A
          #9 C-6.1 U9: A–D now hold DCBA · correct B -> C
          #11 C-3.1 U11: A–D now hold BADC · correct B -> A

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
