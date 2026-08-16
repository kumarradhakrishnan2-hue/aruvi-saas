# Library certification · social_sciences VI ch 8 · 20260816_092038

plan: counts [13, 11, 8] · basis authored_standard · registry 5 sections

FAIL  library complete: ['ch_08_canonical.json'] vs plan [13, 11, 8]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_08_canonical.json: 1 prose lead(s) in the summary match no registry entry (1 summary section(s) vs 5 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: The section
      ADVISORY ch_08_canonical.json: 5 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): A Rich Diversity; Food for All; Textiles and Clothing; Festivals Galore; An Epic Spread
PASS  ch_08_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_08_canonical.json: every anchor verbatim in the top registry
PASS  ch_08_canonical.json: first-visit order follows the registry
PASS  ch_08_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_08_canonical.json: register scan reached the band text (52 band(s) read: {'activity_title': 13, 'materials': 41, 'visual_aids': 8, 'teacher_notes': 13, 'time_bands': 52})
FAIL  ch_08_canonical.json: register clean (2 ban hit(s))
      U3 time_bands[1] 8-22 [clock] …, weave, dye, print, draping style). They work individually for five minutes, then share with a neighbour.
      U10 time_bands[0] 0-10 [clock] …festival. The teacher explains that each student will speak for two minutes as that person, describing one thing about their life that…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_08_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_08_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_08_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_08_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_08_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_08_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_08_canonical.json: 12 items vs 12 expected
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

serve sweep: {"6": "fill/single", "7": "synthesis", "8": "synthesis", "9": "synthesis", "10": "synthesis", "11": "synthesis", "12": "synthesis", "13": "identity", "14": "surrender", "15": "surrender"}

options arranged: 7 of 8 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_08_canonical.json: 7 of 8 item(s) re-ordered
          #1 C-7.1 U2: A–D now hold ABDC · correct B -> B
          #2 C-7.1 U5: A–D now hold BADC · correct B -> A
          #6 C-7.3 U6: A–D now hold BDAC · correct B -> A
          #7 C-7.3 U8: A–D now hold DBAC · correct C -> D
          #9 C-2.2 U3: A–D now hold CBDA · correct B -> B
          #10 C-2.2 U11: A–D now hold ABDC · correct C -> D
          #12 C-10.1 U12: A–D now hold BADC · correct C -> D

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
