# Library certification · the_world_around_us V ch 7 · 20260812_141622

plan: counts [13, 11, 8] · basis authored_standard · registry 5 sections

FAIL  library complete: ['ch_07_canonical.json'] vs plan [13, 11, 8]
serve granularity: unit  ·  section axis: True
PASS  ch_07_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_07_canonical.json: every anchor verbatim in the top registry
PASS  ch_07_canonical.json: first-visit order follows the registry
PASS  ch_07_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_07_canonical.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 13 handoff group(s) for 13 unit(s) — at most 13 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_07_canonical.json: 12 unit(s) wear a section label the handoff does not route items through: U1=what is energy?, U2=what is energy?, U3=what is energy?, U4=what is energy?, U5=sources of energy, U6=sources of energy …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_07_canonical.json: register scan reached the band text (63 band(s) read: {'activity_title': 13, 'materials': 57, 'visual_aids': 10, 'teacher_facilitation_note': 13, 'time_bands': 63})
PASS  ch_07_canonical.json: register clean (0 ban hit(s))
PASS  ch_07_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_07_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_07_canonical.json: ['ECR'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_07_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_07_canonical.json: every OPEN_TASK carries question_text "" (0 not)
PASS  ch_07_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {}
      ch_07_canonical.json: 13 items vs 13 expected
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)
PASS  X=12: choice set non-empty (no defensive truncation)
PASS  X=13: choice set non-empty (no defensive truncation)
PASS  X=14: choice set non-empty (no defensive truncation)
PASS  X=15: choice set non-empty (no defensive truncation)

serve sweep: {"6": "fill/single -2s", "7": "fill/single -2s", "8": "fill/single -1s", "9": "fill/single", "10": "fill/single", "11": "fill/single", "12": "fill/single", "13": "identity", "14": "surrender", "15": "surrender"}

options arranged: 5 of 5 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_07_canonical.json: 5 of 5 item(s) re-ordered
          #1 C-7.1 U1: A–D now hold ABDC · correct B -> B
          #3 C-7.1 U3: A–D now hold DBCA · correct B -> B
          #5 C-2.1 U5: A–D now hold CABD · correct B -> C
          #7 C-2.1 U7: A–D now hold ADCB · correct C -> C
          #11 C-6.1 U11: A–D now hold DCBA · correct C -> B

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
