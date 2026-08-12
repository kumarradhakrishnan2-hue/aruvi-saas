# Library certification · the_world_around_us IV ch 6 · 20260812_141623

plan: counts [19, 15, 11] · basis authored_standard · registry 7 sections

FAIL  library complete: ['ch_06_canonical.json'] vs plan [19, 15, 11]
serve granularity: unit  ·  section axis: True
PASS  ch_06_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_06_canonical.json: every anchor verbatim in the top registry
PASS  ch_06_canonical.json: first-visit order follows the registry
PASS  ch_06_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_06_canonical.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 19 handoff group(s) for 19 unit(s) — at most 19 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_06_canonical.json: 18 unit(s) wear a section label the handoff does not route items through: U1=journey of the grains, U2=journey of the grains, U3=journey of the grains, U4=journey of the grains, U5=mindful eating, U6=mindful eating …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_06_canonical.json: register scan reached the band text (76 band(s) read: {'activity_title': 19, 'materials': 55, 'visual_aids': 6, 'teacher_facilitation_note': 19, 'time_bands': 76})
PASS  ch_06_canonical.json: register clean (0 ban hit(s))
PASS  ch_06_canonical.json: every declared stimulus type resolves (0 mis-tagged)
FAIL  ch_06_canonical.json: every question_type is a known assessment type (1 not)
      unit [13]: question_type 'HI' is not an assessment type at all
      -> check the assessment constitution's type-selection TABLE: its left column is another enumeration (dominant_mode, weight tier, CG theme) and this is usually a value copied from the wrong column
      ADVISORY ch_06_canonical.json: ['HI'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_06_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_06_canonical.json: every OPEN_TASK carries question_text "" (0 not)
PASS  ch_06_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {}
      ch_06_canonical.json: 19 items vs 19 expected
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

serve sweep: {"9": "fill/single -3s", "10": "fill/single -2s", "11": "fill/single -2s", "12": "fill/single -2s", "13": "fill/single -2s", "14": "fill/single -1s", "15": "fill/single -1s", "16": "fill/single", "17": "fill/single", "18": "synthesis", "19": "identity", "20": "surrender", "21": "surrender"}

options arranged: 5 of 5 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_06_canonical.json: 5 of 5 item(s) re-ordered
          #1 C-2.1 U1: A–D now hold DCBA · correct A -> D
          #4 C-2.1 U4: A–D now hold DBCA · correct A -> D
          #9 C-3.1 U9: A–D now hold CBAD · correct A -> C
          #14 C-6.1 U14: A–D now hold CDAB · correct A -> C
          #15 C-3.1 U15: A–D now hold CDAB · correct A -> C
NOTE  top canonical failed — the entire library is quarantined with it (variants have no registry ground without the top)
QUARANTINED  ch_06_canonical.json -> backup/quarantine/the_world_around_us/iv/ch_06_canonical_20260812_141623.json

DETERMINISTIC CHECKS HAVE FAILURES — do not certify Failed files are QUARANTINED under backup/quarantine/ (the fix worklist); regenerate them and re-run --certify-only..
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
