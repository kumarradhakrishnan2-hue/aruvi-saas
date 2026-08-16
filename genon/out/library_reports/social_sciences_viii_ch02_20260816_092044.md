# Library certification · social_sciences VIII ch 2 · 20260816_092044

plan: counts [15, 12, 9] · basis authored_standard · registry 12 sections

FAIL  library complete: ['ch_02_canonical.json'] vs plan [15, 12, 9]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_02_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_02_canonical.json: every anchor verbatim in the top registry
PASS  ch_02_canonical.json: first-visit order follows the registry
PASS  ch_02_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_02_canonical.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 45, 'visual_aids': 15, 'teacher_notes': 15, 'time_bands': 60})
FAIL  ch_02_canonical.json: register clean (5 ban hit(s))
      ADVISORY ch_02_canonical.json: 1 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U4 time_bands[3] 35-45: 'from the previous unit' — …a fragmentation mirrors the Bahmani→five Sultanates pattern from the previous unit, pointing to a recurring structure in Deccan political hist…
      U3 time_bands[3] 35-45 [forward] …rce' — and that its cultural peak under one ruler will form the next unit's focus.
      U7 time_bands[3] 35-45 [forward] …nd eventual British entry — content beyond this chapter but foreshadowed here.
      U8 time_bands[2] 22-36 [clock] Groups of four discuss for eight minutes using the prompt card. Each group must identify: one shared…
      U11 teacher_notes [forward] …alism and from the Mughal mansabdari in important ways that the next unit will develop. Students often treat 'tax burden on peasantry…
      U15 time_bands[3] 40-45 [clock] …specific example to support your position.' Students write for the remaining minutes — this is a take-away prompt, not assessed in this sitting.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_02_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_02_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_02_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_02_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_02_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_02_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_02_canonical.json: 19 items vs 19 expected
PASS  X=7: choice set non-empty (no defensive truncation)
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

serve sweep: {"7": "fill/single -5s", "8": "fill/single -4s", "9": "fill/single -3s", "10": "fill/single -2s", "11": "fill/single -1s", "12": "fill/single", "13": "fill/single", "14": "synthesis", "15": "identity", "16": "surrender", "17": "surrender"}

options arranged: 13 of 14 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_02_canonical.json: 13 of 14 item(s) re-ordered
          #1 C-2.1 U1: A–D now hold CBDA · correct A -> D
          #2 C-2.1 U6: A–D now hold BADC · correct A -> B
          #6 C-3.2 U2: A–D now hold BDAC · correct A -> C
          #7 C-3.2 U9: A–D now hold CADB · correct A -> B
          #9 C-4.2 U11: A–D now hold CABD · correct A -> B
          #10 C-4.2 U12: A–D now hold BCDA · correct A -> D
          #13 C-1.1 U5: A–D now hold ACDB · correct A -> A
          #14 C-2.2 U13: A–D now hold DABC · correct A -> B
          #15 C-2.2 U14: A–D now hold BCDA · correct A -> D
          #16 C-7.3 U6: A–D now hold BACD · correct A -> B
          #17 C-7.3 U10: A–D now hold ACDB · correct A -> A
          #18 C-9.1 U13: A–D now hold ACBD · correct A -> A
          #19 C-9.1 U13: A–D now hold DBAC · correct A -> C

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
