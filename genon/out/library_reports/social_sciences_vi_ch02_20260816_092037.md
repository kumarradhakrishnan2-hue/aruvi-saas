# Library certification · social_sciences VI ch 2 · 20260816_092037

plan: counts [15, 12, 9] · basis authored_standard · registry 6 sections

FAIL  library complete: ['ch_02_canonical.json'] vs plan [15, 12, 9]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_02_canonical.json: 1 prose lead(s) in the summary match no registry entry (1 summary section(s) vs 6 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: A continent is a large continuous landmass. The chapter
      ADVISORY ch_02_canonical.json: 6 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): The Distribution of Water and Land on the Earth; Oceans; Oceans and Disasters; Continents; Islands; Oceans and Life
PASS  ch_02_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_02_canonical.json: every anchor verbatim in the top registry
PASS  ch_02_canonical.json: first-visit order follows the registry
PASS  ch_02_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_02_canonical.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 39, 'visual_aids': 10, 'teacher_notes': 15, 'time_bands': 60})
FAIL  ch_02_canonical.json: register clean (3 ban hit(s))
      U4 teacher_notes [forward] …n. The causal-chain sentence at the close is the conceptual bridge to the water-cycle role oceans play in the 'Oceans and Life' secti…
      U8 teacher_notes [forward] …riding geology, and it sets up the size-ranking activity in the next unit.
      U13 time_bands[0] 0-10 [forward] …nsibility to solve? This primes the normative reasoning the unit will develop.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_02_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_02_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_02_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_02_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_02_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_02_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_02_canonical.json: 13 items vs 13 expected
PASS  X=7: choice set non-empty (no defensive truncation)
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

serve sweep: {"7": "fill/single -2s", "8": "fill/single -2s", "9": "fill/single -1s", "10": "fill/single -1s", "11": "fill/single", "12": "fill/single", "13": "synthesis", "14": "synthesis", "15": "identity", "16": "surrender", "17": "surrender"}

options arranged: 8 of 8 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_02_canonical.json: 8 of 8 item(s) re-ordered
          #1 C-6.1 U1: A–D now hold CADB · correct B -> D
          #2 C-6.1 U8: A–D now hold DACB · correct B -> D
          #6 C-6.3 U13: A–D now hold BDCA · correct B -> A
          #7 C-6.3 U14: A–D now hold CDAB · correct B -> D
          #9 C-6.4 U5: A–D now hold CADB · correct B -> D
          #10 C-6.4 U12: A–D now hold BADC · correct B -> A
          #12 C-7.2 U10: A–D now hold ABDC · correct B -> B
          #13 C-7.2 U11: A–D now hold BDAC · correct B -> A

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
