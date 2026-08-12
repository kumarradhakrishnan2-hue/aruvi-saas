# Library certification · social_sciences IX ch 6 · 20260812_162654

plan: counts [19, 15, 11] · basis authored_standard · registry 16 sections

FAIL  library complete: ['ch_06_canonical.json'] vs plan [19, 15, 11]
serve granularity: unit  ·  section axis: True
PASS  ch_06_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_06_canonical.json: every anchor verbatim in the top registry
PASS  ch_06_canonical.json: first-visit order follows the registry
PASS  ch_06_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_06_canonical.json: register scan reached the band text (76 band(s) read: {'activity_title': 19, 'materials': 40, 'visual_aids': 4, 'teacher_notes': 19, 'time_bands': 76})
FAIL  ch_06_canonical.json: register clean (3 ban hit(s))
      U3 time_bands[0] 0-12 [clock] …strengthen popular sovereignty?' Students discuss in pairs for three minutes, then share. Teacher introduces Universal Adult Franchise —…
      U7 time_bands[0] 0-12 [clock] …eir own state, town, or village. Students work individually for seven minutes, then share two examples with the class. Teacher notes that…
      U17 time_bands[0] 0-10 [clock] …ommunity issue you care about.' Students write individually for four minutes, then share one action and one community issue with the cla…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_06_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_06_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_06_canonical.json: ['OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_06_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_06_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_06_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: constitution
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_06_canonical.json: 25 items vs 27 expected  <-- MISS
          C-5.3 (Substantive) has 2, constitution says 3
          C-6.4 (Substantive) has 2, constitution says 3
      -> 2 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
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

serve sweep: {"9": "fill/single -8s", "10": "fill/single -7s", "11": "fill/single -7s", "12": "fill/single -6s", "13": "fill/single -5s", "14": "fill/single -4s", "15": "fill/single -3s", "16": "fill/single -2s", "17": "fill/single -1s", "18": "fill/single", "19": "identity", "20": "surrender", "21": "surrender"}

options arranged: 8 of 9 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_06_canonical.json: 8 of 9 item(s) re-ordered
          #6 C-5.1 U1: A–D now hold BDCA · correct B -> A
          #9 C-5.2 U4: A–D now hold DCBA · correct B -> C
          #12 C-5.3 U4: A–D now hold BDCA · correct B -> A
          #14 C-5.5 U8: A–D now hold DABC · correct B -> C
          #17 C-6.2 U7: A–D now hold ADCB · correct B -> D
          #20 C-6.4 U16: A–D now hold BDAC · correct B -> A
          #22 C-1.3 U16: A–D now hold BDCA · correct B -> A
          #24 C-2.5 U13: A–D now hold DABC · correct B -> C

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
