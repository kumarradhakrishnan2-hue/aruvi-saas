# Library certification · the_world_around_us V ch 3 · 20260812_141622

plan: counts [8, 5] · basis authored_standard · registry 5 sections

FAIL  library complete: ['ch_03_canonical.json'] vs plan [8, 5]
serve granularity: unit  ·  section axis: True
PASS  ch_03_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_03_canonical.json: every anchor verbatim in the top registry
PASS  ch_03_canonical.json: first-visit order follows the registry
PASS  ch_03_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_03_canonical.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 8 handoff group(s) for 8 unit(s) — at most 8 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_03_canonical.json: 7 unit(s) wear a section label the handoff does not route items through: U1=food spoilage, U2=food preservation, U3=food preservation, U4=my food, my pride, U5=chew right!, U6=chew right! …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_03_canonical.json: register scan reached the band text (32 band(s) read: {'activity_title': 8, 'materials': 25, 'teacher_facilitation_note': 8, 'time_bands': 32, 'visual_aids': 3})
PASS  ch_03_canonical.json: register clean (0 ban hit(s))
PASS  ch_03_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_03_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_03_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_03_canonical.json: every OPEN_TASK carries question_text "" (0 not)
PASS  ch_03_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {}
      ch_03_canonical.json: 8 items vs 8 expected
PASS  X=3: choice set non-empty (no defensive truncation)
PASS  X=4: choice set non-empty (no defensive truncation)
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)

serve sweep: {"3": "fill/single -2s", "4": "fill/single -2s", "5": "fill/single -1s", "6": "fill/single", "7": "fill/single", "8": "identity", "9": "surrender", "10": "surrender"}

options arranged: 2 of 2 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_03_canonical.json: 2 of 2 item(s) re-ordered
          #1 C-7.2 U1: A–D now hold DACB · correct B -> D
          #4 C-2.1 U4: A–D now hold BACD · correct B -> A

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
