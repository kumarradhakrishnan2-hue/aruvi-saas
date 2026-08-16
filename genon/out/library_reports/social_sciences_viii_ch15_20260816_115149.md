# Library certification · social_sciences VIII ch 15 · 20260816_115149

plan: counts [17, 14, 10] · basis authored_standard · registry 16 sections

PASS  library complete: ['ch_15_canonical.json', 'ch_15_canonical_p14.json', 'ch_15_canonical_p10.json'] vs plan [17, 14, 10]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_15_canonical.json: 3 prose lead(s) in the summary match no registry entry (3 summary section(s) vs 16 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This subsection; This section; The closing recap
      ADVISORY ch_15_canonical.json: 16 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Introduction; The power of the bhakti tradition; Regional saints and their messages; Sufism; Musical Traditions — Continuation and Evolution; From Walls to Paper — Miniature Paintings …
PASS  ch_15_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_15_canonical.json: every anchor verbatim in the top registry
PASS  ch_15_canonical.json: first-visit order follows the registry
PASS  ch_15_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_15_canonical_p14.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_15_canonical_p14.json: every anchor verbatim in the top registry
FAIL  ch_15_canonical_p14.json: first-visit order follows the registry
PASS  ch_15_canonical_p14.json: coverage reaches the final registry section
PASS  ch_15_canonical_p10.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_15_canonical_p10.json: every anchor verbatim in the top registry
PASS  ch_15_canonical_p10.json: first-visit order follows the registry
PASS  ch_15_canonical_p10.json: coverage reaches the final registry section
PASS  ch_15_canonical.json: register scan reached the band text (68 band(s) read: {'activity_title': 17, 'materials': 30, 'visual_aids': 16, 'teacher_notes': 17, 'time_bands': 68})
PASS  ch_15_canonical.json: register clean (0 ban hit(s))
PASS  ch_15_canonical_p14.json: register scan reached the band text (56 band(s) read: {'activity_title': 14, 'materials': 30, 'visual_aids': 8, 'teacher_notes': 14, 'time_bands': 56})
FAIL  ch_15_canonical_p14.json: register clean (3 ban hit(s))
      U1 time_bands[0] 0-8 [clock] …s in without being blown off your feet? Students pair-share for two minutes, then two or three share with the class. Teacher charts the…
      U3 teacher_notes [forward] …le of integration. The closing analytical question directly bridges to the Sufism unit that follows.
      U12 time_bands[2] 24-36 [clock] …her than just a construction act? Students discuss in pairs for three minutes, then share.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_15_canonical_p10.json: register scan reached the band text (40 band(s) read: {'activity_title': 10, 'materials': 30, 'visual_aids': 8, 'teacher_notes': 10, 'time_bands': 40})
FAIL  ch_15_canonical_p10.json: register clean (2 ban hit(s))
      U3 time_bands[1] 8-22 [clock] …ritual, and (d) one shared idea. Students work individually for six minutes, then compare with a neighbour.
      U7 time_bands[2] 22-33 [clock] …he production of new knowledge? Students think individually for two minutes, then discuss in pairs, then share whole class. Teacher rec…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_15_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_15_canonical_p14.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_15_canonical_p10.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_15_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_15_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_15_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_15_canonical_p14.json: every question_type is a known assessment type (0 not)
PASS  ch_15_canonical_p14.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_15_canonical_p14.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_15_canonical_p10.json: every question_type is a known assessment type (0 not)
PASS  ch_15_canonical_p10.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_15_canonical_p10.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_15_canonical.json: MCQ options in arrangement order
PASS  ch_15_canonical_p14.json: MCQ options in arrangement order
PASS  ch_15_canonical_p10.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_15_canonical.json: 21 items vs 21 expected
      ch_15_canonical_p14.json: 21 items vs 21 expected
      ch_15_canonical_p10.json: 21 items vs 21 expected
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

serve sweep: {"8": "fill/forward -4s", "9": "fill/forward -2s", "10": "identity", "11": "rescue/complete (from 14)", "12": "fill/single -2s", "13": "fill/forward", "14": "identity", "15": "rescue/complete (from 17)", "16": "fill/single", "17": "identity", "18": "surrender", "19": "surrender"}

options arranged: 14 of 42 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_15_canonical.json: 0 of 14 item(s) re-ordered
      ch_15_canonical_p10.json: 0 of 14 item(s) re-ordered
      ch_15_canonical_p14.json: 14 of 14 item(s) re-ordered
          #1 C-7.1 U6: A–D now hold DCAB · correct B -> D
          #2 C-7.1 U13: A–D now hold BCDA · correct C -> B
          #6 C-2.2 U2: A–D now hold DACB · correct B -> D
          #7 C-2.2 U9: A–D now hold BCDA · correct B -> A
          #9 C-3.2 U3: A–D now hold BACD · correct B -> A
          #10 C-3.2 U10: A–D now hold CBDA · correct B -> B
          #12 C-5.1 U8: A–D now hold CBAD · correct B -> B
          #13 C-5.1 U3: A–D now hold CBAD · correct B -> B
          #15 C-10.1 U11: A–D now hold CBDA · correct B -> B
          #16 C-10.1 U14: A–D now hold ADBC · correct B -> C
          #18 C-1.1 U6: A–D now hold ACDB · correct B -> D
          #19 C-1.1 U8: A–D now hold BDAC · correct B -> A
          #20 C-2.1 U9: A–D now hold BACD · correct B -> A
          #21 C-2.1 U13: A–D now hold CBAD · correct A -> C
QUARANTINED  ch_15_canonical_p14.json -> backup/quarantine/social_sciences/viii/ch_15_canonical_p14_20260816_115149.json

DETERMINISTIC CHECKS HAVE FAILURES — do not certify Failed files are QUARANTINED under backup/quarantine/ (the fix worklist); regenerate them and re-run --certify-only..
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
