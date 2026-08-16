# Library certification · social_sciences VII ch 12 · 20260816_101638

plan: counts [18, 15, 11] · basis authored_standard · registry 10 sections

PASS  library complete: ['ch_12_canonical.json', 'ch_12_canonical_p15.json', 'ch_12_canonical_p11.json'] vs plan [18, 15, 11]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_12_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_12_canonical.json: every anchor verbatim in the top registry
PASS  ch_12_canonical.json: first-visit order follows the registry
PASS  ch_12_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_12_canonical_p15.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_12_canonical_p15.json: every anchor verbatim in the top registry
PASS  ch_12_canonical_p15.json: first-visit order follows the registry
PASS  ch_12_canonical_p15.json: coverage reaches the final registry section
PASS  ch_12_canonical_p11.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_12_canonical_p11.json: every anchor verbatim in the top registry
PASS  ch_12_canonical_p11.json: first-visit order follows the registry
PASS  ch_12_canonical_p11.json: coverage reaches the final registry section
PASS  ch_12_canonical.json: register scan reached the band text (72 band(s) read: {'activity_title': 18, 'materials': 67, 'teacher_notes': 18, 'time_bands': 72, 'visual_aids': 6})
PASS  ch_12_canonical.json: register clean (0 ban hit(s))
      ADVISORY ch_12_canonical.json: 2 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U12 time_bands[1] 8-22: 'from the earlier unit' — …ling — connected to the government's maximum price controls from the earlier unit), name and address of manufacturer (accountability), nutrit…
        U13 time_bands[3] 34-40: 'from the previous unit' — …nt. Students add this insight to their three-item checklist from the previous unit.
PASS  ch_12_canonical_p15.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 35, 'teacher_notes': 15, 'time_bands': 60, 'visual_aids': 5})
FAIL  ch_12_canonical_p15.json: register clean (2 ban hit(s))
      U10 teacher_notes [forward] …ls) and the environment — a preview of the external effects the next unit addresses. Weights-and-measures monitoring is a small but c…
      U15 teacher_notes [completion] …ents to deploy the full consumer quality-assessment toolkit developed across the chapter's closing sections — not introduce new content but apply ac…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_12_canonical_p11.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 23, 'visual_aids': 7, 'teacher_notes': 11, 'time_bands': 44})
PASS  ch_12_canonical_p11.json: register clean (0 ban hit(s))
PASS  ch_12_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_12_canonical_p15.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_12_canonical_p11.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_12_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_12_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_12_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_12_canonical_p15.json: every question_type is a known assessment type (0 not)
PASS  ch_12_canonical_p15.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_12_canonical_p15.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_12_canonical_p11.json: every question_type is a known assessment type (0 not)
PASS  ch_12_canonical_p11.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_12_canonical_p11.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_12_canonical.json: MCQ options in arrangement order
PASS  ch_12_canonical_p15.json: MCQ options in arrangement order
PASS  ch_12_canonical_p11.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_12_canonical.json: 14 items vs 14 expected
      ch_12_canonical_p15.json: 14 items vs 14 expected
      ch_12_canonical_p11.json: 14 items vs 14 expected
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

serve sweep: {"9": "fill/single -1s", "10": "fill/single", "11": "identity", "12": "fill/single", "13": "fill/single", "14": "synthesis", "15": "identity", "16": "synthesis", "17": "synthesis", "18": "identity", "19": "surrender", "20": "surrender"}

options arranged: 20 of 30 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_12_canonical.json: 0 of 10 item(s) re-ordered
      ch_12_canonical_p11.json: 10 of 10 item(s) re-ordered
          #1 C-9.1 U1: A–D now hold CBAD · correct A -> C
          #2 C-9.1 U3: A–D now hold DABC · correct A -> B
          #6 C-4.1 U8: A–D now hold CADB · correct A -> B
          #7 C-4.1 U9: A–D now hold DACB · correct A -> B
          #9 C-4.2 U7: A–D now hold BADC · correct A -> B
          #10 C-4.2 U9: A–D now hold BADC · correct A -> B
          #11 C-6.2 U4: A–D now hold BADC · correct A -> B
          #12 C-6.2 U4: A–D now hold ABDC · correct A -> A
          #13 C-10.1 U1: A–D now hold CBAD · correct A -> C
          #14 C-10.1 U8: A–D now hold DABC · correct A -> B
      ch_12_canonical_p15.json: 10 of 10 item(s) re-ordered
          #1 C-9.1 U1: A–D now hold ACDB · correct A -> A
          #2 C-9.1 U7: A–D now hold BCDA · correct B -> A
          #6 C-4.1 U9: A–D now hold DABC · correct B -> C
          #7 C-4.1 U11: A–D now hold CABD · correct B -> C
          #9 C-4.2 U9: A–D now hold DBAC · correct B -> B
          #10 C-4.2 U11: A–D now hold DBAC · correct B -> B
          #11 C-6.2 U5: A–D now hold BACD · correct B -> A
          #12 C-6.2 U5: A–D now hold CDAB · correct B -> D
          #13 C-10.1 U2: A–D now hold DBAC · correct B -> B
          #14 C-10.1 U12: A–D now hold DCBA · correct B -> C

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
