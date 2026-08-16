# Library certification · social_sciences VII ch 1 · 20260816_092040

plan: counts [19, 15, 11] · basis authored_standard · registry 14 sections

FAIL  library complete: ['ch_01_canonical.json'] vs plan [19, 15, 11]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_01_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_01_canonical.json: every anchor verbatim in the top registry
PASS  ch_01_canonical.json: first-visit order follows the registry
PASS  ch_01_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_01_canonical.json: register scan reached the band text (76 band(s) read: {'activity_title': 19, 'materials': 40, 'visual_aids': 17, 'teacher_notes': 19, 'time_bands': 76})
FAIL  ch_01_canonical.json: register clean (3 ban hit(s))
      U5 time_bands[2] 20-32 [clock] …st productive question from each cluster and discusses both for about six minutes total, with students offering reasoning rather than the tea…
      U7 time_bands[0] 0-8 [clock] …rming, for trade, for cities?' Students brainstorm in pairs for three minutes, then share.
      U16 time_bands[0] 0-8 [clock] …and from which direction.' Students study the map silently for three minutes and mark entry-possible and entry-blocked zones with symbol…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_01_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_01_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_01_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_01_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_01_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_01_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_01_canonical.json: 14 items vs 14 expected
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

serve sweep: {"9": "fill/single -5s", "10": "fill/single -4s", "11": "fill/single -3s", "12": "fill/single -3s", "13": "fill/single -2s", "14": "fill/single -1s", "15": "fill/single", "16": "synthesis", "17": "synthesis", "18": "synthesis", "19": "identity", "20": "surrender", "21": "surrender"}

options arranged: 10 of 10 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_01_canonical.json: 10 of 10 item(s) re-ordered
          #1 C-7.2 U1: A–D now hold CADB · correct A -> B
          #2 C-7.2 U12: A–D now hold BCAD · correct A -> C
          #6 C-6.4 U7: A–D now hold DBAC · correct A -> C
          #7 C-6.4 U11: A–D now hold DCBA · correct A -> D
          #9 C-6.1 U2: A–D now hold BADC · correct A -> B
          #10 C-6.1 U10: A–D now hold BCDA · correct A -> D
          #11 C-6.2 U9: A–D now hold DBAC · correct A -> C
          #12 C-6.2 U17: A–D now hold BCAD · correct A -> C
          #13 C-6.3 U8: A–D now hold CDBA · correct A -> D
          #14 C-6.3 U18: A–D now hold DACB · correct A -> B

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
