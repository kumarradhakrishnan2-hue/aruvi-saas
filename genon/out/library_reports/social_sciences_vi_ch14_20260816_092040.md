# Library certification · social_sciences VI ch 14 · 20260816_092040

plan: counts [9, 7, 5] · basis authored_standard · registry 7 sections

FAIL  library complete: ['ch_14_canonical.json'] vs plan [9, 7, 5]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_14_canonical.json: 1 prose lead(s) in the summary match no registry entry (1 summary section(s) vs 7 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section
      ADVISORY ch_14_canonical.json: 7 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Introduction; The Classification of Economic Activities into Economic Sectors; A. Primary activities; B. Secondary activities; C. Tertiary activities; Interdependence Among Sectors …
PASS  ch_14_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_14_canonical.json: every anchor verbatim in the top registry
PASS  ch_14_canonical.json: first-visit order follows the registry
PASS  ch_14_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_14_canonical.json: register scan reached the band text (36 band(s) read: {'activity_title': 9, 'materials': 26, 'visual_aids': 8, 'teacher_notes': 9, 'time_bands': 36})
FAIL  ch_14_canonical.json: register clean (1 ban hit(s))
      U2 time_bands[0] 0-8 [clock] …the chapter's illustrated sector diagram. Students study it for two minutes in silence, noting every activity listed under each sector.…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_14_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_14_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_14_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_14_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_14_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_14_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Substantive": 3}
      ch_14_canonical.json: 8 items vs 8 expected
PASS  X=3: choice set non-empty (no defensive truncation)
PASS  X=4: choice set non-empty (no defensive truncation)
PASS  X=5: choice set non-empty (no defensive truncation)
PASS  X=6: choice set non-empty (no defensive truncation)
PASS  X=7: choice set non-empty (no defensive truncation)
PASS  X=8: choice set non-empty (no defensive truncation)
PASS  X=9: choice set non-empty (no defensive truncation)
PASS  X=10: choice set non-empty (no defensive truncation)
PASS  X=11: choice set non-empty (no defensive truncation)

serve sweep: {"3": "fill/single -4s", "4": "fill/single -3s", "5": "fill/single -2s", "6": "fill/single -1s", "7": "fill/single", "8": "synthesis", "9": "identity", "10": "surrender", "11": "surrender"}

options arranged: 4 of 4 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_14_canonical.json: 4 of 4 item(s) re-ordered
          #1 C-9.1 U1: A–D now hold ADBC · correct B -> C
          #2 C-9.1 U6: A–D now hold BDCA · correct C -> C
          #6 C-4.1 U7: A–D now hold DBAC · correct A -> C
          #7 C-4.1 U8: A–D now hold CABD · correct B -> C

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
