# Library certification · social_sciences IX ch 5 · 20260812_185027

plan: counts [21, 17, 13] · basis authored_standard · registry 20 sections

PASS  library complete: ['ch_05_canonical.json', 'ch_05_canonical_p17.json', 'ch_05_canonical_p13.json'] vs plan [21, 17, 13]
serve granularity: unit  ·  section axis: True
PASS  ch_05_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_05_canonical.json: every anchor verbatim in the top registry
PASS  ch_05_canonical.json: first-visit order follows the registry
PASS  ch_05_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_05_canonical_p17.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_05_canonical_p17.json: every anchor verbatim in the top registry
PASS  ch_05_canonical_p17.json: first-visit order follows the registry
PASS  ch_05_canonical_p17.json: coverage reaches the final registry section
PASS  ch_05_canonical_p13.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_05_canonical_p13.json: every anchor verbatim in the top registry
PASS  ch_05_canonical_p13.json: first-visit order follows the registry
PASS  ch_05_canonical_p13.json: coverage reaches the final registry section
PASS  ch_05_canonical.json: register scan reached the band text (84 band(s) read: {'activity_title': 21, 'materials': 47, 'visual_aids': 7, 'teacher_notes': 21, 'time_bands': 84})
PASS  ch_05_canonical.json: register clean (0 ban hit(s))
      ADVISORY ch_05_canonical.json: 1 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U11 time_bands[2] 27-42: 'from the previous unit' — …ṇa. Students compare this Sangam model with the varṇa model from the previous unit by completing a two-column table: VARṆA MODEL / SANGAM OCCU…
PASS  ch_05_canonical_p17.json: register scan reached the band text (68 band(s) read: {'activity_title': 17, 'materials': 38, 'visual_aids': 7, 'teacher_notes': 17, 'time_bands': 68})
PASS  ch_05_canonical_p17.json: register clean (0 ban hit(s))
PASS  ch_05_canonical_p13.json: register scan reached the band text (52 band(s) read: {'activity_title': 13, 'materials': 42, 'teacher_notes': 13, 'time_bands': 52, 'visual_aids': 4})
FAIL  ch_05_canonical_p13.json: register clean (2 ban hit(s))
      ADVISORY ch_05_canonical_p13.json: 1 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U9 time_bands[3] 38-50: 'built earlier' — …t in one written paragraph, using evidence from the columns built earlier.
      U4 time_bands[2] 25-40 [clock] …hā approves; the samiti is divided.' Each group deliberates for five minutes and presents its position. The vidhata (the whole class tog…
      U13 time_bands[3] 38-50 [completion] …estion that surveys the chapter's full arc without claiming the chapter is complete: 'The Nāśhik inscription records a transaction involving a…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_05_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_05_canonical_p17.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_05_canonical_p13.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_05_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_05_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_05_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_05_canonical_p17.json: every question_type is a known assessment type (0 not)
PASS  ch_05_canonical_p17.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_05_canonical_p17.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_05_canonical_p13.json: every question_type is a known assessment type (0 not)
PASS  ch_05_canonical_p13.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_05_canonical_p13.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_05_canonical.json: MCQ options in arrangement order
PASS  ch_05_canonical_p17.json: MCQ options in arrangement order
PASS  ch_05_canonical_p13.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: constitution
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_05_canonical.json: 31 items vs 31 expected
      ch_05_canonical_p17.json: 31 items vs 31 expected
      ch_05_canonical_p13.json: 27 items vs 31 expected  <-- MISS
          C-1.2 (Substantive) has 2, constitution says 3
          C-1.4 (Substantive) has 2, constitution says 3
          C-8.3 (Substantive) has 2, constitution says 3
          C-6.1 (Substantive) has 2, constitution says 3
      -> 4 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
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
PASS  X=22: choice set non-empty (no defensive truncation)
PASS  X=23: choice set non-empty (no defensive truncation)

serve sweep: {"11": "fill/forward -2s", "12": "fill/single -1s", "13": "identity", "14": "rescue/complete (from 17)", "15": "fill/single -1s", "16": "fill/single", "17": "identity", "18": "rescue/complete (from 21)", "19": "fill/single -1s", "20": "fill/single", "21": "identity", "22": "surrender", "23": "surrender"}

options arranged: 21 of 33 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_05_canonical.json: 0 of 11 item(s) re-ordered
      ch_05_canonical_p13.json: 10 of 11 item(s) re-ordered
          #1 C-1.3 U5: A–D now hold CADB · correct B -> D
          #6 C-1.1 U2: A–D now hold DBAC · correct C -> D
          #9 C-1.2 U5: A–D now hold BADC · correct D -> C
          #11 C-1.4 U3: A–D now hold CBAD · correct B -> B
          #13 C-5.1 U4: A–D now hold CDBA · correct A -> D
          #16 C-8.3 U12: A–D now hold DBCA · correct B -> B
          #20 C-5.4 U4: A–D now hold ABDC · correct B -> B
          #22 C-7.4 U12: A–D now hold ADBC · correct C -> D
          #24 C-6.2 U8: A–D now hold CBDA · correct B -> B
          #26 C-9.1 U10: A–D now hold ACBD · correct B -> C
      ch_05_canonical_p17.json: 11 of 11 item(s) re-ordered
          #1 C-1.3 U4: A–D now hold BACD · correct A -> B
          #6 C-1.1 U8: A–D now hold DACB · correct A -> B
          #9 C-1.2 U4: A–D now hold ADCB · correct A -> A
          #12 C-1.4 U11: A–D now hold ADBC · correct A -> A
          #15 C-5.1 U3: A–D now hold CBAD · correct A -> C
          #18 C-8.3 U14: A–D now hold DCAB · correct A -> C
          #21 C-6.1 U10: A–D now hold ACDB · correct A -> A
          #24 C-5.4 U3: A–D now hold CADB · correct A -> B
          #26 C-7.4 U14: A–D now hold BADC · correct A -> B
          #28 C-6.2 U8: A–D now hold ADCB · correct A -> A
          #30 C-9.1 U11: A–D now hold DBAC · correct A -> C

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
