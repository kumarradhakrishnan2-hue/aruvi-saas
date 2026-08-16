# Library certification · social_sciences VI ch 11 · 20260816_092039

plan: counts [19, 15, 11] · basis authored_standard · registry 5 sections

FAIL  library complete: ['ch_11_canonical.json'] vs plan [19, 15, 11]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_11_canonical.json: 1 prose lead(s) in the summary match no registry entry (1 summary section(s) vs 5 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section
      ADVISORY ch_11_canonical.json: 5 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Panchayati Raj System; Gram Panchayat; Exemplary Sarpanchs; Child-Friendly Panchayat Initiative; Panchayat Samiti and Zila Parishad
PASS  ch_11_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_11_canonical.json: every anchor verbatim in the top registry
PASS  ch_11_canonical.json: first-visit order follows the registry
PASS  ch_11_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_11_canonical.json: register scan reached the band text (76 band(s) read: {'activity_title': 19, 'materials': 37, 'visual_aids': 3, 'teacher_notes': 19, 'time_bands': 76})
FAIL  ch_11_canonical.json: register clean (7 ban hit(s))
      U1 teacher_notes [forward] …ich scale of problem, giving you diagnostic information for later units.
      U3 time_bands[2] 22-33 [forward] …ions. This bridges toward the Exemplary Sarpanch cases in a later unit.
      U3 time_bands[2] 22-33 [forward] …means when it includes women in collective decisions. This bridges toward the Exemplary Sarpanch cases in a later unit.
      U6 time_bands[0] 0-8 [clock] …ement within a Gram Panchayat's power?' Students brainstorm for two minutes and share ideas. Then introduce Popatrao Baguji Pawar and H…
      U8 time_bands[1] 8-20 [clock] …they need and adults responding?' Students discuss in pairs for three minutes, then share the key distinction they arrived at — ownership…
      U10 time_bands[0] 0-8 [clock] …ou think they would choose to address?' Students brainstorm for two minutes and share four or five ideas. Then introduce the Children's…
      U15 time_bands[2] 20-33 [clock] …acceptable variation?' Students discuss in groups of three for five minutes, then one spokesperson per group shares the group's positio…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_11_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_11_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_11_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_11_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_11_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_11_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_11_canonical.json: 16 items vs 16 expected
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

serve sweep: {"9": "fill/single", "10": "fill/single", "11": "fill/single", "12": "fill/single", "13": "synthesis", "14": "synthesis", "15": "synthesis", "16": "synthesis", "17": "synthesis", "18": "synthesis", "19": "identity", "20": "surrender", "21": "surrender"}

options arranged: 10 of 10 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_11_canonical.json: 10 of 10 item(s) re-ordered
          #1 C-8.3 U1: A–D now hold CADB · correct B -> D
          #2 C-8.3 U13: A–D now hold BCAD · correct B -> A
          #6 C-4.1 U3: A–D now hold ADCB · correct C -> C
          #7 C-4.1 U12: A–D now hold BCDA · correct B -> A
          #9 C-4.2 U5: A–D now hold DCBA · correct B -> C
          #10 C-4.2 U9: A–D now hold BACD · correct B -> A
          #12 C-5.2 U4: A–D now hold BADC · correct B -> A
          #13 C-5.2 U10: A–D now hold ADBC · correct B -> C
          #15 C-10.1 U14: A–D now hold BDAC · correct B -> A
          #16 C-10.1 U14: A–D now hold CDAB · correct B -> D

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
