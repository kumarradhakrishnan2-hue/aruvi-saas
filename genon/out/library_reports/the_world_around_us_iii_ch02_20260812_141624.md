# Library certification · the_world_around_us III ch 2 · 20260812_141624

plan: counts [11, 9, 7] · basis authored_standard · registry 4 sections

FAIL  library complete: ['ch_02_canonical.json'] vs plan [11, 9, 7]
serve granularity: unit  ·  section axis: True
PASS  ch_02_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_02_canonical.json: every anchor verbatim in the top registry
PASS  ch_02_canonical.json: first-visit order follows the registry
PASS  ch_02_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_02_canonical.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 11 handoff group(s) for 11 unit(s) — at most 11 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_02_canonical.json: 10 unit(s) wear a section label the handoff does not route items through: U1=preparing for the mela, U2=on the way to the mela, U3=on the way to the mela, U4=at the mela, U5=at the mela, U6=at the mela …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_02_canonical.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 39, 'teacher_facilitation_note': 11, 'time_bands': 44, 'visual_aids': 7})
PASS  ch_02_canonical.json: register clean (0 ban hit(s))
PASS  ch_02_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_02_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_02_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_02_canonical.json: every OPEN_TASK carries question_text "" (0 not)
PASS  ch_02_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {}
      ch_02_canonical.json: 11 items vs 11 expected
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)
PASS  X=12: choice set non-empty (no defensive truncation)
PASS  X=13: choice set non-empty (no defensive truncation)

serve sweep: {"5": "fill/single", "6": "fill/single", "7": "fill/single", "8": "fill/single", "9": "synthesis", "10": "synthesis", "11": "identity", "12": "surrender", "13": "surrender"}

options arranged: 4 of 4 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_02_canonical.json: 4 of 4 item(s) re-ordered
          #1 C-3.1 U1: A–D now hold CADB · correct B -> D
          #2 C-2.1 U2: A–D now hold DABC · correct B -> C
          #5 C-3.1 U5: A–D now hold BACD · correct B -> A
          #9 C-1.4 U9: A–D now hold ACDB · correct C -> B

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
