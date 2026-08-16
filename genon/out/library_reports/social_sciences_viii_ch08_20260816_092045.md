# Library certification · social_sciences VIII ch 8 · 20260816_092045

plan: counts [13, 11, 8] · basis authored_standard · registry 12 sections

FAIL  library complete: ['ch_08_canonical.json'] vs plan [13, 11, 8]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_08_canonical.json: 3 prose lead(s) in the summary match no registry entry (5 summary section(s) vs 12 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section; The final stop; The closing recap
      ADVISORY ch_08_canonical.json: 10 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Introduction; The Complexity of Mapping the Earth; The Blue of the Blue Planet, the Oceans; The oceans; The Great Barrier Reef; Asia …
PASS  ch_08_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_08_canonical.json: every anchor verbatim in the top registry
PASS  ch_08_canonical.json: first-visit order follows the registry
PASS  ch_08_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_08_canonical.json: register scan reached the band text (52 band(s) read: {'activity_title': 13, 'materials': 37, 'visual_aids': 13, 'teacher_notes': 13, 'time_bands': 52})
FAIL  ch_08_canonical.json: register clean (4 ban hit(s))
      U3 teacher_notes [forward] …here is the foundation for understanding ocean currents in the following unit — name the heat-release principle explicitly so students ca…
      U3 time_bands[1] 8-22 [forward] …ive in the deep?' Hold answers — these will be revisited in the next unit.
      U3 time_bands[2] 22-37 [clock] …nsequences they can reason out). Students work individually for five minutes, then share chains with a partner.
      U5 teacher_notes [meta-leak] …ing as a human-caused phenomenon keeps that thread explicit without requiring any earlier activity to have occurred. Students often confuse a gulf with a bay;…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_08_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_08_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_08_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_08_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_08_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_08_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_08_canonical.json: 16 items vs 16 expected
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

serve sweep: {"6": "fill/single -6s", "7": "fill/single -5s", "8": "fill/single -4s", "9": "fill/single -3s", "10": "fill/single -2s", "11": "fill/single -1s", "12": "fill/single", "13": "identity", "14": "surrender", "15": "surrender"}

options arranged: 10 of 10 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_08_canonical.json: 10 of 10 item(s) re-ordered
          #1 C-6.1 U4: A–D now hold DABC · correct A -> B
          #2 C-6.1 U12: A–D now hold CDBA · correct C -> A
          #6 C-1.2 U2: A–D now hold ADBC · correct B -> C
          #7 C-1.2 U5: A–D now hold DBAC · correct C -> D
          #9 C-6.3 U9: A–D now hold CDAB · correct C -> A
          #10 C-6.3 U12: A–D now hold DABC · correct A -> B
          #12 C-6.4 U8: A–D now hold CABD · correct A -> B
          #13 C-6.4 U11: A–D now hold ABDC · correct B -> B
          #15 C-6.2 U7: A–D now hold BCAD · correct A -> C
          #16 C-6.2 U9: A–D now hold CADB · correct A -> B

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
