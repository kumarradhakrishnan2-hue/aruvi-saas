# Library certification · the_world_around_us III ch 11 · 20260812_142524

plan: counts [17, 14, 10] · basis authored_standard · registry 4 sections

FAIL  library complete: ['ch_11_canonical.json'] vs plan [17, 14, 10]
serve granularity: unit  ·  section axis: True
PASS  ch_11_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_11_canonical.json: every anchor verbatim in the top registry
PASS  ch_11_canonical.json: first-visit order follows the registry
PASS  ch_11_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_11_canonical.json: every handoff row routes to a unit that anchors its section
      handoff/anchor: 17 handoff group(s) for 17 unit(s) — at most 17 unit(s) can carry an item, so 0 without one is arithmetic, not a defect
      ADVISORY ch_11_canonical.json: 16 unit(s) wear a section label the handoff does not route items through: U1=a potter's family, U2=a potter's family, U3=a potter's family, U4=a potter's family, U5=patterns in nature, U6=patterns in nature …  (do NOT extend period_numbers to fix this — it moves the item to a later unit and loses it on short serves)
PASS  ch_11_canonical.json: register scan reached the band text (84 band(s) read: {'activity_title': 17, 'materials': 58, 'visual_aids': 14, 'teacher_facilitation_note': 17, 'time_bands': 84})
PASS  ch_11_canonical.json: register clean (0 ban hit(s))
PASS  ch_11_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_11_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_11_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_11_canonical.json: every OPEN_TASK carries question_text "" (0 not)
PASS  ch_11_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {}
      ch_11_canonical.json: 17 items vs 17 expected
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
PASS  X=19: choice set non-empty (no defensive truncation)

serve sweep: {"8": "fill/single -1s", "9": "fill/single", "10": "fill/single", "11": "fill/single", "12": "fill/single", "13": "fill/single", "14": "synthesis", "15": "synthesis", "16": "synthesis", "17": "identity", "18": "surrender", "19": "surrender"}

options arranged: 0 of 4 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_11_canonical.json: 0 of 4 item(s) re-ordered

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
