# Library certification · social_sciences VII ch 6 · 20260816_092042

plan: counts [18, 15, 11] · basis authored_standard · registry 11 sections

FAIL  library complete: ['ch_06_canonical.json'] vs plan [18, 15, 11]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_06_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_06_canonical.json: every anchor verbatim in the top registry
PASS  ch_06_canonical.json: first-visit order follows the registry
PASS  ch_06_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_06_canonical.json: register scan reached the band text (72 band(s) read: {'activity_title': 18, 'materials': 38, 'visual_aids': 15, 'teacher_notes': 18, 'time_bands': 72})
FAIL  ch_06_canonical.json: register clean (5 ban hit(s))
      U6 teacher_notes [forward] …l history. The mapping task fixes geographic positions that later units build on.
      U10 teacher_notes [ids] …pping identifies as primary carriers of cultural continuity (C-2.2), and it also carries the inclusion theme (C-7.3). A common…
      U10 teacher_notes [ids] …continuity (C-2.2), and it also carries the inclusion theme (C-7.3). A common confusion is reading the Indo-Greek period purely…
      U12 teacher_notes [forward] …le claim in a visual form that the art-school discussion in the next unit can then build on.
      U18 teacher_notes [meta-leak] …ared scaffold that makes the breadth of the chapter visible without requiring any particular prior activity to have happened.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_06_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_06_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_06_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_06_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_06_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_06_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_06_canonical.json: 14 items vs 14 expected
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

serve sweep: {"9": "fill/single -2s", "10": "fill/single -1s", "11": "fill/single", "12": "fill/single", "13": "synthesis", "14": "synthesis", "15": "synthesis", "16": "synthesis", "17": "synthesis", "18": "identity", "19": "surrender", "20": "surrender"}

options arranged: 10 of 10 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_06_canonical.json: 10 of 10 item(s) re-ordered
          #1 C-2.1 U1: A–D now hold CABD · correct A -> B
          #2 C-2.1 U7: A–D now hold BCDA · correct A -> D
          #6 C-2.2 U2: A–D now hold ADBC · correct A -> A
          #7 C-2.2 U11: A–D now hold DBCA · correct A -> D
          #9 C-3.1 U4: A–D now hold BCAD · correct A -> C
          #10 C-3.1 U14: A–D now hold ADBC · correct A -> A
          #11 C-7.3 U10: A–D now hold CABD · correct A -> B
          #12 C-7.3 U11: A–D now hold DCAB · correct A -> C
          #13 C-10.1 U4: A–D now hold CDAB · correct A -> C
          #14 C-10.1 U4: A–D now hold DACB · correct A -> B

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
