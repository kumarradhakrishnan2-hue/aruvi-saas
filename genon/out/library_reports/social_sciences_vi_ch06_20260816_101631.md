# Library certification · social_sciences VI ch 6 · 20260816_101631

plan: counts [24, 19, 14] · basis authored_standard · registry 9 sections

PASS  library complete: ['ch_06_canonical.json', 'ch_06_canonical_p19.json', 'ch_06_canonical_p14.json'] vs plan [24, 19, 14]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_06_canonical.json: 1 prose lead(s) in the summary match no registry entry (1 summary section(s) vs 9 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section
      ADVISORY ch_06_canonical.json: 9 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): What Is a Civilisation?; From Village to City; The Sarasvatī River; Town-Planning; Water Management; What Did the Harappans Eat? …
PASS  ch_06_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_06_canonical.json: every anchor verbatim in the top registry
PASS  ch_06_canonical.json: first-visit order follows the registry
PASS  ch_06_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_06_canonical_p19.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_06_canonical_p19.json: every anchor verbatim in the top registry
PASS  ch_06_canonical_p19.json: first-visit order follows the registry
PASS  ch_06_canonical_p19.json: coverage reaches the final registry section
PASS  ch_06_canonical_p14.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_06_canonical_p14.json: every anchor verbatim in the top registry
PASS  ch_06_canonical_p14.json: first-visit order follows the registry
PASS  ch_06_canonical_p14.json: coverage reaches the final registry section
PASS  ch_06_canonical.json: register scan reached the band text (96 band(s) read: {'activity_title': 24, 'materials': 52, 'teacher_notes': 24, 'time_bands': 96, 'visual_aids': 15})
PASS  ch_06_canonical.json: register clean (0 ban hit(s))
      ADVISORY ch_06_canonical.json: 1 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U8 time_bands[3] 35-40: 'from the previous unit' — …e activities. Students add this to their trade-flow diagram from the previous unit, noting seals as a record-keeping and identification tool.…
PASS  ch_06_canonical_p19.json: register scan reached the band text (76 band(s) read: {'activity_title': 19, 'materials': 49, 'teacher_notes': 19, 'time_bands': 76, 'visual_aids': 12})
FAIL  ch_06_canonical_p19.json: register clean (3 ban hit(s))
      U8 teacher_notes [forward] This unit focuses on everyday objects; the next unit will take up the cultural and symbolic objects from the sam…
      U8 teacher_notes [forward] This unit focuses on everyday objects; the next unit will take up the cultural and symbolic objects from the same section, so…
      U9 time_bands[3] 36-40 [forward] …in South Asian life today, raising the question the chapter will take up: when a civilisation 'ends,' does its culture truly disappe…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_06_canonical_p14.json: register scan reached the band text (56 band(s) read: {'activity_title': 14, 'materials': 37, 'teacher_notes': 14, 'time_bands': 56, 'visual_aids': 10})
FAIL  ch_06_canonical_p14.json: register clean (2 ban hit(s))
      ADVISORY ch_06_canonical_p14.json: 1 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U10 time_bands[2] 22-34: 'from the previous unit' — …ghts to the gamesboard, whistle, and other everyday objects from the previous unit: the range of objects tells us the Harappans had time beyon…
      U9 time_bands[0] 0-8 [clock] …e cultural or symbolic meaning.' Students sort individually for three minutes, then compare their groupings with a neighbour. Teacher not…
      U14 teacher_notes [completion] Having worked through all the chapter's content sections, this unit consolidates the…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_06_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_06_canonical_p19.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_06_canonical_p14.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_06_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_06_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_06_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_06_canonical_p19.json: every question_type is a known assessment type (0 not)
PASS  ch_06_canonical_p19.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_06_canonical_p19.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_06_canonical_p14.json: every question_type is a known assessment type (0 not)
PASS  ch_06_canonical_p14.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_06_canonical_p14.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_06_canonical.json: MCQ options in arrangement order
PASS  ch_06_canonical_p19.json: MCQ options in arrangement order
PASS  ch_06_canonical_p14.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_06_canonical.json: 22 items vs 22 expected
      ch_06_canonical_p19.json: 20 items vs 20 expected
      ch_06_canonical_p14.json: 19 items vs 20 expected  <-- MISS
          C-6.2 (Present) has 1, its siblings carry 2
      -> 1 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
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
PASS  X=22: choice set non-empty (no defensive truncation)
PASS  X=23: choice set non-empty (no defensive truncation)
PASS  X=24: choice set non-empty (no defensive truncation)
PASS  X=25: choice set non-empty (no defensive truncation)
PASS  X=26: choice set non-empty (no defensive truncation)

serve sweep: {"12": "fill/single", "13": "synthesis", "14": "identity", "15": "synthesis", "16": "synthesis", "17": "synthesis", "18": "synthesis", "19": "identity", "20": "synthesis", "21": "synthesis", "22": "synthesis", "23": "synthesis", "24": "identity", "25": "surrender", "26": "surrender"}

options arranged: 25 of 43 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_06_canonical.json: 0 of 16 item(s) re-ordered
          #6 SKIPPED — cross-references an option label — left untouched, needs a human
      ch_06_canonical_p14.json: 11 of 13 item(s) re-ordered
          #1 C-3.1 U1: A–D now hold BDCA · correct B -> A
          #2 C-3.1 U8: A–D now hold ADBC · correct B -> C
          #6 C-1.1 U3: A–D now hold BADC · correct C -> D
          #7 C-1.1 U9: A–D now hold ADBC · correct B -> C
          #10 C-2.1 U12: A–D now hold BCDA · correct B -> A
          #12 C-9.1 U7: A–D now hold DABC · correct B -> C
          #15 C-6.1 U3: A–D now hold DCAB · correct B -> D
          #16 C-6.1 U12: A–D now hold CBAD · correct A -> C
          #17 C-6.2 U7: A–D now hold DCAB · correct B -> D
          #18 C-7.1 U9: A–D now hold BADC · correct B -> A
          #19 C-7.1 U12: A–D now hold CBAD · correct B -> B
      ch_06_canonical_p19.json: 14 of 14 item(s) re-ordered
          #1 C-3.1 U1: A–D now hold BCAD · correct B -> A
          #2 C-3.1 U4: A–D now hold BCDA · correct B -> A
          #6 C-1.1 U3: A–D now hold CBAD · correct B -> B
          #7 C-1.1 U9: A–D now hold CBDA · correct B -> B
          #9 C-2.1 U2: A–D now hold BDAC · correct B -> A
          #10 C-2.1 U10: A–D now hold CBAD · correct B -> B
          #12 C-9.1 U7: A–D now hold CABD · correct B -> C
          #13 C-9.1 U17: A–D now hold DBAC · correct B -> B
          #15 C-6.1 U3: A–D now hold ACDB · correct B -> D
          #16 C-6.1 U10: A–D now hold ABDC · correct B -> B
          #17 C-6.2 U7: A–D now hold ADBC · correct B -> C
          #18 C-6.2 U5: A–D now hold DACB · correct B -> D
          #19 C-7.1 U9: A–D now hold CADB · correct B -> D
          #20 C-7.1 U19: A–D now hold DBCA · correct B -> B

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
