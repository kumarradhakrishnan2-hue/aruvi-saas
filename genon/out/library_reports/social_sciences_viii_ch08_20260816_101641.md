# Library certification · social_sciences VIII ch 8 · 20260816_101641

plan: counts [13, 11, 8] · basis authored_standard · registry 12 sections

PASS  library complete: ['ch_08_canonical.json', 'ch_08_canonical_p11.json', 'ch_08_canonical_p08.json'] vs plan [13, 11, 8]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_08_canonical.json: 3 prose lead(s) in the summary match no registry entry (5 summary section(s) vs 12 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section; The final stop; The closing recap
      ADVISORY ch_08_canonical.json: 10 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Introduction; The Complexity of Mapping the Earth; The Blue of the Blue Planet, the Oceans; The oceans; The Great Barrier Reef; Asia …
PASS  ch_08_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_08_canonical.json: every anchor verbatim in the top registry
PASS  ch_08_canonical.json: first-visit order follows the registry
PASS  ch_08_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_08_canonical_p11.json: the `synthesis` token is reserved to the standard canonical
FAIL  ch_08_canonical_p11.json: every anchor verbatim in the top registry
FAIL  ch_08_canonical_p11.json: first-visit order follows the registry
PASS  ch_08_canonical_p11.json: coverage reaches the final registry section
PASS  ch_08_canonical_p08.json: the `synthesis` token is reserved to the standard canonical
FAIL  ch_08_canonical_p08.json: every anchor verbatim in the top registry
FAIL  ch_08_canonical_p08.json: first-visit order follows the registry
PASS  ch_08_canonical_p08.json: coverage reaches the final registry section
PASS  ch_08_canonical.json: register scan reached the band text (52 band(s) read: {'activity_title': 13, 'materials': 37, 'visual_aids': 13, 'teacher_notes': 13, 'time_bands': 52})
PASS  ch_08_canonical.json: register clean (0 ban hit(s))
PASS  ch_08_canonical_p11.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 32, 'visual_aids': 11, 'teacher_notes': 11, 'time_bands': 44})
PASS  ch_08_canonical_p11.json: register clean (0 ban hit(s))
PASS  ch_08_canonical_p08.json: register scan reached the band text (32 band(s) read: {'activity_title': 8, 'materials': 26, 'visual_aids': 8, 'teacher_notes': 8, 'time_bands': 32})
PASS  ch_08_canonical_p08.json: register clean (0 ban hit(s))
PASS  ch_08_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_08_canonical_p11.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_08_canonical_p08.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_08_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_08_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_08_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_08_canonical_p11.json: every question_type is a known assessment type (0 not)
PASS  ch_08_canonical_p11.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_08_canonical_p11.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_08_canonical_p08.json: every question_type is a known assessment type (0 not)
PASS  ch_08_canonical_p08.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_08_canonical_p08.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_08_canonical.json: MCQ options in arrangement order
PASS  ch_08_canonical_p11.json: MCQ options in arrangement order
PASS  ch_08_canonical_p08.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_08_canonical.json: 16 items vs 16 expected
      ch_08_canonical_p11.json: 16 items vs 16 expected
      ch_08_canonical_p08.json: 16 items vs 16 expected
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

serve sweep: {"6": "fill/single -2s", "7": "fill/single -1s", "8": "identity", "9": "rescue/complete (from 11)", "10": "fill/single", "11": "identity", "12": "fill/single", "13": "identity", "14": "surrender", "15": "surrender"}

options arranged: 20 of 30 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_08_canonical.json: 0 of 10 item(s) re-ordered
      ch_08_canonical_p08.json: 10 of 10 item(s) re-ordered
          #1 C-6.1 U1: A–D now hold DCAB · correct A -> C
          #2 C-6.1 U8: A–D now hold BDCA · correct A -> D
          #6 C-1.2 U1: A–D now hold CBAD · correct A -> C
          #7 C-1.2 U4: A–D now hold DCAB · correct A -> C
          #9 C-6.3 U2: A–D now hold BCAD · correct A -> C
          #10 C-6.3 U6: A–D now hold BADC · correct A -> B
          #12 C-6.4 U5: A–D now hold CBDA · correct A -> D
          #13 C-6.4 U7: A–D now hold BDAC · correct A -> C
          #15 C-6.2 U5: A–D now hold DCAB · correct A -> C
          #16 C-6.2 U7: A–D now hold DACB · correct A -> B
      ch_08_canonical_p11.json: 10 of 10 item(s) re-ordered
          #1 C-6.1 U1: A–D now hold ACDB · correct A -> A
          #2 C-6.1 U3: A–D now hold CDAB · correct A -> C
          #6 C-1.2 U1: A–D now hold DACB · correct A -> B
          #7 C-1.2 U5: A–D now hold ABDC · correct A -> A
          #9 C-6.3 U4: A–D now hold BDCA · correct A -> D
          #10 C-6.3 U8: A–D now hold ADBC · correct A -> A
          #12 C-6.4 U6: A–D now hold BADC · correct A -> B
          #13 C-6.4 U7: A–D now hold CBAD · correct A -> C
          #15 C-6.2 U6: A–D now hold CBDA · correct A -> D
          #16 C-6.2 U11: A–D now hold CABD · correct A -> B
QUARANTINED  ch_08_canonical_p08.json -> backup/quarantine/social_sciences/viii/ch_08_canonical_p08_20260816_101641.json
QUARANTINED  ch_08_canonical_p11.json -> backup/quarantine/social_sciences/viii/ch_08_canonical_p11_20260816_101641.json

DETERMINISTIC CHECKS HAVE FAILURES — do not certify Failed files are QUARANTINED under backup/quarantine/ (the fix worklist); regenerate them and re-run --certify-only..
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
