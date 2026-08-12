# Library certification · the_world_around_us IV ch 3 · 20260812_141623

plan: counts [16, 13, 10] · basis authored_standard · registry 5 sections

FAIL  library complete: ['ch_03_canonical.json'] vs plan [16, 13, 10]
serve granularity: unit  ·  section axis: True
PASS  ch_03_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_03_canonical.json: every anchor verbatim in the top registry
PASS  ch_03_canonical.json: first-visit order follows the registry
PASS  ch_03_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_03_canonical.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 16 handoff group(s) for 16 unit(s) — at most 16 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_03_canonical.json: 15 unit(s) wear a section label the handoff does not route items through: U1=the adventure begins, U2=animals in the forest, U3=animals in the forest, U4=animals in the forest, U5=animals in the forest, U6=animals in the forest …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_03_canonical.json: register scan reached the band text (64 band(s) read: {'activity_title': 16, 'materials': 64, 'teacher_facilitation_note': 16, 'time_bands': 64, 'visual_aids': 8})
PASS  ch_03_canonical.json: register clean (0 ban hit(s))
PASS  ch_03_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_03_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_03_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_03_canonical.json: every OPEN_TASK carries question_text "" (0 not)
PASS  ch_03_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {}
      ch_03_canonical.json: 16 items vs 16 expected
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

serve sweep: {"8": "fill/single -2s", "9": "fill/single -1s", "10": "fill/single -1s", "11": "fill/single -1s", "12": "fill/single", "13": "synthesis", "14": "synthesis", "15": "synthesis", "16": "identity", "17": "surrender", "18": "surrender"}

options arranged: 5 of 5 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_03_canonical.json: 5 of 5 item(s) re-ordered
          #1 C-3.1 U1: A–D now hold ADBC · correct B -> C
          #2 C-4.1 U2: A–D now hold CDBA · correct B -> C
          #7 C-4.1 U7: A–D now hold DCAB · correct C -> B
          #8 C-1.1 U8: A–D now hold CDBA · correct B -> C
          #13 C-1.1 U13: A–D now hold ACDB · correct B -> D

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
