# Library certification · social_sciences VI ch 11 · 20260816_101633

plan: counts [19, 15, 11] · basis authored_standard · registry 5 sections

PASS  library complete: ['ch_11_canonical.json', 'ch_11_canonical_p15.json', 'ch_11_canonical_p11.json'] vs plan [19, 15, 11]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_11_canonical.json: 1 prose lead(s) in the summary match no registry entry (1 summary section(s) vs 5 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section
      ADVISORY ch_11_canonical.json: 5 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Panchayati Raj System; Gram Panchayat; Exemplary Sarpanchs; Child-Friendly Panchayat Initiative; Panchayat Samiti and Zila Parishad
PASS  ch_11_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_11_canonical.json: every anchor verbatim in the top registry
PASS  ch_11_canonical.json: first-visit order follows the registry
PASS  ch_11_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_11_canonical_p15.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_11_canonical_p15.json: every anchor verbatim in the top registry
PASS  ch_11_canonical_p15.json: first-visit order follows the registry
PASS  ch_11_canonical_p15.json: coverage reaches the final registry section
PASS  ch_11_canonical_p11.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_11_canonical_p11.json: every anchor verbatim in the top registry
PASS  ch_11_canonical_p11.json: first-visit order follows the registry
PASS  ch_11_canonical_p11.json: coverage reaches the final registry section
PASS  ch_11_canonical.json: register scan reached the band text (76 band(s) read: {'activity_title': 19, 'materials': 37, 'visual_aids': 3, 'teacher_notes': 19, 'time_bands': 76})
PASS  ch_11_canonical.json: register clean (0 ban hit(s))
PASS  ch_11_canonical_p15.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 33, 'visual_aids': 4, 'teacher_notes': 15, 'time_bands': 60})
FAIL  ch_11_canonical_p15.json: register clean (3 ban hit(s))
      U3 time_bands[3] 35-40 [forward] …e…' — teacher scans responses to gauge understanding before the next unit.
      U7 teacher_notes [forward] …tion. The pair task prepares students for the simulation in the following unit.
      U15 time_bands[0] 0-10 [clock] …ld you give on each side?' Students brainstorm individually for four minutes, listing evidence for and against, then share briefly in pa…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_11_canonical_p11.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 31, 'visual_aids': 5, 'teacher_notes': 11, 'time_bands': 44})
FAIL  ch_11_canonical_p11.json: register clean (2 ban hit(s))
      U2 time_bands[1] 10-22 [clock] …he past and the present?' Students first write individually for three minutes — possible answers include tracing changes in land ownershi…
      U10 time_bands[0] 0-10 [clock] …to the tier above and below it.' Students work individually for eight minutes. Teacher circulates to see what students recall fluently an…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_11_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_11_canonical_p15.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_11_canonical_p11.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_11_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_11_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_11_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_11_canonical_p15.json: every question_type is a known assessment type (0 not)
PASS  ch_11_canonical_p15.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_11_canonical_p15.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_11_canonical_p11.json: every question_type is a known assessment type (0 not)
PASS  ch_11_canonical_p11.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_11_canonical_p11.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_11_canonical.json: MCQ options in arrangement order
PASS  ch_11_canonical_p15.json: MCQ options in arrangement order
PASS  ch_11_canonical_p11.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_11_canonical.json: 16 items vs 16 expected
      ch_11_canonical_p15.json: 16 items vs 16 expected
      ch_11_canonical_p11.json: 16 items vs 16 expected
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

serve sweep: {"9": "synthesis", "10": "synthesis", "11": "identity", "12": "synthesis", "13": "synthesis", "14": "synthesis", "15": "identity", "16": "synthesis", "17": "synthesis", "18": "synthesis", "19": "identity", "20": "surrender", "21": "surrender"}

options arranged: 18 of 30 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_11_canonical.json: 0 of 10 item(s) re-ordered
      ch_11_canonical_p11.json: 9 of 10 item(s) re-ordered
          #1 C-8.3 U1: A–D now hold DABC · correct A -> B
          #2 C-8.3 U10: A–D now hold ADBC · correct A -> A
          #6 C-4.1 U2: A–D now hold CDBA · correct A -> D
          #7 C-4.1 U10: A–D now hold CABD · correct A -> B
          #9 C-4.2 U3: A–D now hold ACBD · correct A -> A
          #12 C-5.2 U3: A–D now hold BCDA · correct A -> D
          #13 C-5.2 U8: A–D now hold DBAC · correct A -> C
          #15 C-10.1 U9: A–D now hold ADBC · correct A -> A
          #16 C-10.1 U9: A–D now hold DBCA · correct A -> D
      ch_11_canonical_p15.json: 9 of 10 item(s) re-ordered
          #1 C-8.3 U1: A–D now hold ABDC · correct B -> B
          #2 C-8.3 U11: A–D now hold DABC · correct B -> C
          #7 C-4.1 U13: A–D now hold CBDA · correct C -> A
          #9 C-4.2 U5: A–D now hold ABDC · correct B -> B
          #10 C-4.2 U6: A–D now hold DBCA · correct D -> A
          #12 C-5.2 U7: A–D now hold CDBA · correct B -> C
          #13 C-5.2 U14: A–D now hold BADC · correct B -> A
          #15 C-10.1 U12: A–D now hold DCBA · correct B -> C
          #16 C-10.1 U12: A–D now hold DBCA · correct B -> B

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
