# Library certification · the_world_around_us III ch 3 · 20260812_141624

plan: counts [10, 8, 6] · basis authored_standard · registry 2 sections

FAIL  library complete: ['ch_03_canonical.json'] vs plan [10, 8, 6]
serve granularity: unit  ·  section axis: True
PASS  ch_03_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_03_canonical.json: every anchor verbatim in the top registry
PASS  ch_03_canonical.json: first-visit order follows the registry
PASS  ch_03_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_03_canonical.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 10 handoff group(s) for 10 unit(s) — at most 10 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_03_canonical.json: 9 unit(s) wear a section label the handoff does not route items through: U1=festival of flowers, U2=festival of flowers, U3=festival of flowers, U4=festival of flowers, U5=festival of flowers, U6=festival of flowers …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_03_canonical.json: register scan reached the band text (40 band(s) read: {'activity_title': 10, 'materials': 36, 'teacher_facilitation_note': 10, 'time_bands': 40, 'visual_aids': 4})
PASS  ch_03_canonical.json: register clean (0 ban hit(s))
PASS  ch_03_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_03_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_03_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_03_canonical.json: every OPEN_TASK carries question_text "" (0 not)
PASS  ch_03_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {}
      ch_03_canonical.json: 10 items vs 10 expected
PASS  X=4: choice set non-empty (no defensive truncation)
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)
PASS  X=12: choice set non-empty (no defensive truncation)

serve sweep: {"4": "fill/single", "5": "fill/single", "6": "fill/single", "7": "fill/single", "8": "fill/single", "9": "synthesis", "10": "identity", "11": "surrender", "12": "surrender"}

options arranged: 4 of 4 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_03_canonical.json: 4 of 4 item(s) re-ordered
          #1 C-4.1 U1: A–D now hold CDBA · correct C -> A
          #3 C-4.1 U3: A–D now hold BCDA · correct D -> C
          #6 C-4.2 U6: A–D now hold ADBC · correct C -> D
          #8 C-1.3 U8: A–D now hold BCDA · correct A -> D

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
