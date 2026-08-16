# Library certification · social_sciences VIII ch 1 · 20260816_092043

plan: counts [11, 9, 7] · basis authored_standard · registry 9 sections

FAIL  library complete: ['ch_01_canonical.json'] vs plan [11, 9, 7]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_01_canonical.json: 2 prose lead(s) in the summary match no registry entry (3 summary section(s) vs 9 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This category; A second axis of categorisation is based on renewability. The chapter
      ADVISORY ch_01_canonical.json: 8 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): When does Nature become a Resource?; Categories of Natural Resources; Renewable and non-renewable resources; Distribution of Natural Resources and its Implications; The 'Natural Resource Curse'; Overexploitation of groundwater: a caselet from Punjab …
PASS  ch_01_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_01_canonical.json: every anchor verbatim in the top registry
PASS  ch_01_canonical.json: first-visit order follows the registry
PASS  ch_01_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_01_canonical.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 33, 'teacher_notes': 11, 'time_bands': 44, 'visual_aids': 5})
FAIL  ch_01_canonical.json: register clean (1 ban hit(s))
      U11 time_bands[2] 28-38 [clock] Gallery: groups post maps and circulate for three minutes, reading other groups' work. Each student places a star on…
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
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)
PASS  X=12: choice set non-empty (no defensive truncation)
PASS  X=13: choice set non-empty (no defensive truncation)

serve sweep: {"5": "fill/single -4s", "6": "fill/single -3s", "7": "fill/single -2s", "8": "fill/single -1s", "9": "fill/single", "10": "synthesis", "11": "identity", "12": "surrender", "13": "surrender"}

options arranged: 9 of 10 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_01_canonical.json: 9 of 10 item(s) re-ordered
          #1 C-6.2 U4: A–D now hold DACB · correct B -> D
          #2 C-6.2 U10: A–D now hold CBDA · correct B -> B
          #7 C-6.3 U8: A–D now hold CABD · correct B -> C
          #9 C-6.4 U7: A–D now hold CBAD · correct B -> B
          #10 C-6.4 U7: A–D now hold ADBC · correct B -> C
          #11 C-10.1 U8: A–D now hold BCDA · correct B -> A
          #12 C-10.1 U9: A–D now hold ACBD · correct B -> C
          #13 C-9.1 U5: A–D now hold DCBA · correct B -> C
          #14 C-9.1 U11: A–D now hold ADBC · correct B -> C

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
