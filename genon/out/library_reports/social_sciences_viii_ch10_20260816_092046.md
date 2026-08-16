# Library certification · social_sciences VIII ch 10 · 20260816_092046

plan: counts [12, 10, 7] · basis authored_standard · registry 11 sections

FAIL  library complete: ['ch_10_canonical.json'] vs plan [12, 10, 7]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_10_canonical.json: 3 prose lead(s) in the summary match no registry entry (3 summary section(s) vs 11 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section; The final descriptive section; The closing recap consolidates the chapter's argument
      ADVISORY ch_10_canonical.json: 11 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Introduction; The Beginnings …; Structural Stupa Architecture; Rock-Cut Architecture; Water Structures; Classical Temple Architecture …
PASS  ch_10_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_10_canonical.json: every anchor verbatim in the top registry
PASS  ch_10_canonical.json: first-visit order follows the registry
PASS  ch_10_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_10_canonical.json: register scan reached the band text (48 band(s) read: {'activity_title': 12, 'materials': 36, 'visual_aids': 10, 'teacher_notes': 12, 'time_bands': 48})
FAIL  ch_10_canonical.json: register clean (3 ban hit(s))
      U3 time_bands[2] 22-35 [clock] …tice and architectural form?' Small groups of three discuss for four minutes, then one member reports. Teacher records key points on the…
      U4 time_bands[0] 0-10 [clock] …sing only hammers and chisels?' Students individually write for three minutes, listing the sequence of steps, the challenges, and what wo…
      U10 time_bands[0] 0-8 [clock] …l management and cooling?' Students brainstorm individually for three minutes, listing at least one advantage per category, then share wi…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_10_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_10_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_10_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_10_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_10_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_10_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_10_canonical.json: 15 items vs 15 expected
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)
PASS  X=12: choice set non-empty (no defensive truncation)
PASS  X=13: choice set non-empty (no defensive truncation)
PASS  X=14: choice set non-empty (no defensive truncation)

serve sweep: {"5": "fill/single -6s", "6": "fill/single -5s", "7": "fill/single -4s", "8": "fill/single -3s", "9": "fill/single -2s", "10": "fill/single -1s", "11": "fill/single", "12": "identity", "13": "surrender", "14": "surrender"}

options arranged: 10 of 10 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_10_canonical.json: 10 of 10 item(s) re-ordered
          #1 C-7.1 U7: A–D now hold BCAD · correct A -> C
          #2 C-7.1 U9: A–D now hold BACD · correct A -> B
          #6 C-2.2 U5: A–D now hold BADC · correct A -> B
          #7 C-2.2 U12: A–D now hold DCAB · correct A -> C
          #9 C-10.1 U2: A–D now hold CBAD · correct A -> C
          #10 C-10.1 U5: A–D now hold CBAD · correct A -> C
          #12 C-1.2 U1: A–D now hold ADBC · correct A -> A
          #13 C-1.2 U8: A–D now hold DBCA · correct A -> D
          #14 C-4.2 U3: A–D now hold CADB · correct A -> B
          #15 C-4.2 U8: A–D now hold CDAB · correct A -> C

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
