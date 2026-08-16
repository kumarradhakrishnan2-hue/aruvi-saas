# Library certification · social_sciences VIII ch 5 · 20260816_092045

plan: counts [12, 10, 7] · basis authored_standard · registry 11 sections

FAIL  library complete: ['ch_05_canonical.json'] vs plan [12, 10, 7]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_05_canonical.json: 1 prose lead(s) in the summary match no registry entry (2 summary section(s) vs 11 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section
      ADVISORY ch_05_canonical.json: 10 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Universal Adult Franchise; The Role of the Election Commission of India (ECI); Election Commission of India — A brief introduction; Managing the electoral process; Model Code of Conduct (MCC); Election to the Lok Sabha and State Legislative Assemblies …
PASS  ch_05_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_05_canonical.json: every anchor verbatim in the top registry
PASS  ch_05_canonical.json: first-visit order follows the registry
PASS  ch_05_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_05_canonical.json: register scan reached the band text (60 band(s) read: {'activity_title': 12, 'materials': 24, 'visual_aids': 10, 'teacher_notes': 12, 'time_bands': 60})
PASS  ch_05_canonical.json: register clean (0 ban hit(s))
PASS  ch_05_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_05_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_05_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_05_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_05_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_05_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_05_canonical.json: 16 items vs 16 expected
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

options arranged: 12 of 12 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_05_canonical.json: 12 of 12 item(s) re-ordered
          #1 C-4.1 U1: A–D now hold CDAB · correct B -> D
          #2 C-4.1 U6: A–D now hold CDBA · correct A -> D
          #6 C-5.2 U2: A–D now hold DCBA · correct B -> C
          #7 C-5.2 U11: A–D now hold ACBD · correct B -> C
          #9 C-4.2 U11: A–D now hold BADC · correct B -> A
          #10 C-4.2 U7: A–D now hold BACD · correct B -> A
          #11 C-8.3 U3: A–D now hold CBAD · correct B -> B
          #12 C-8.3 U3: A–D now hold CBAD · correct B -> B
          #13 C-5.1 U2: A–D now hold BCDA · correct B -> A
          #14 C-5.1 U5: A–D now hold BDAC · correct B -> A
          #15 C-10.1 U4: A–D now hold DBAC · correct B -> B
          #16 C-10.1 U5: A–D now hold ACDB · correct B -> D

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
