# Library certification · social_sciences VI ch 10 · 20260816_092039

plan: counts [15, 12, 9] · basis authored_standard · registry 4 sections

FAIL  library complete: ['ch_10_canonical.json'] vs plan [15, 12, 9]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_10_canonical.json: 1 prose lead(s) in the summary match no registry entry (1 summary section(s) vs 4 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section
      ADVISORY ch_10_canonical.json: 4 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Introduction; Three Organs of Government; Three Levels of Government; Democracy
PASS  ch_10_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_10_canonical.json: every anchor verbatim in the top registry
PASS  ch_10_canonical.json: first-visit order follows the registry
PASS  ch_10_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_10_canonical.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 44, 'visual_aids': 8, 'teacher_notes': 15, 'time_bands': 60})
FAIL  ch_10_canonical.json: register clean (3 ban hit(s))
      U1 time_bands[2] 18-30 [clock] …n students do anything about it?' Students discuss in pairs for three to four minutes, then share. Draw out the idea that citizens — like student…
      U15 teacher_notes [meta-leak] …ative and grassroots democracy from the Democracy section — without requiring any particular prior activity to have occurred. A common risk in synthesis work is that s…
      U15 time_bands[3] 33-40 [clock] …one element I think could be made clearer.' Partners revise for two minutes. Class closes with one final question: 'If you had to expla…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_10_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_10_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_10_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_10_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_10_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_10_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_10_canonical.json: 14 items vs 14 expected
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

serve sweep: {"7": "fill/single", "8": "fill/single", "9": "synthesis", "10": "synthesis", "11": "synthesis", "12": "synthesis", "13": "synthesis", "14": "synthesis", "15": "identity", "16": "surrender", "17": "surrender"}

options arranged: 10 of 10 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_10_canonical.json: 10 of 10 item(s) re-ordered
          #1 C-4.1 U2: A–D now hold BCAD · correct A -> C
          #2 C-4.1 U3: A–D now hold BACD · correct A -> B
          #6 C-8.3 U4: A–D now hold DBAC · correct A -> C
          #7 C-8.3 U14: A–D now hold CADB · correct A -> B
          #9 C-4.2 U8: A–D now hold BDAC · correct A -> C
          #10 C-4.2 U9: A–D now hold DABC · correct A -> B
          #11 C-8.1 U1: A–D now hold CDBA · correct A -> D
          #12 C-8.1 U1: A–D now hold ADBC · correct A -> A
          #13 C-10.1 U6: A–D now hold CDAB · correct A -> C
          #14 C-10.1 U7: A–D now hold ADBC · correct A -> A

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
