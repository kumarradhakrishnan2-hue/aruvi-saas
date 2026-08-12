# Library certification · the_world_around_us V ch 10 · 20260812_141622

plan: counts [16, 13, 10] · basis authored_standard · registry 9 sections

FAIL  library complete: ['ch_10_canonical.json'] vs plan [16, 13, 10]
serve granularity: unit  ·  section axis: True
PASS  ch_10_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_10_canonical.json: every anchor verbatim in the top registry
PASS  ch_10_canonical.json: first-visit order follows the registry
PASS  ch_10_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_10_canonical.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 16 handoff group(s) for 16 unit(s) — at most 16 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_10_canonical.json: 15 unit(s) wear a section label the handoff does not route items through: U1=the blue planet, U2=story 1: the travelling birds!, U3=story 1: the travelling birds!, U4=story 1: the travelling birds!, U5=story 2: yoga—india's gift to the world!, U6=story 3: chilli—a spice that changed our lives! …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_10_canonical.json: register scan reached the band text (64 band(s) read: {'activity_title': 16, 'materials': 57, 'visual_aids': 11, 'teacher_facilitation_note': 16, 'time_bands': 64})
FAIL  ch_10_canonical.json: register clean (1 ban hit(s))
      U7 time_bands[1] 10-22 [clock] …ith the world, what would it be?' Students discuss in pairs for a few minutes, then share with the class. Teacher asks: 'Why that food? W…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_10_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_10_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_10_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_10_canonical.json: every OPEN_TASK carries question_text "" (0 not)
PASS  ch_10_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {}
      ch_10_canonical.json: 16 items vs 16 expected
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

serve sweep: {"8": "fill/single -3s", "9": "fill/single -2s", "10": "fill/single -1s", "11": "fill/single -1s", "12": "fill/single", "13": "fill/single", "14": "synthesis", "15": "synthesis", "16": "identity", "17": "surrender", "18": "surrender"}

options arranged: 2 of 3 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_10_canonical.json: 2 of 3 item(s) re-ordered
          #5 C-2.2 U5: A–D now hold ABDC · correct B -> B
          #10 C-4.2 U10: A–D now hold CABD · correct B -> C

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
