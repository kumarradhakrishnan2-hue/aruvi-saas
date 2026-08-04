# Library certification · social_sciences VIII ch 3 · 20260804_163741

plan: counts [16, 13, 10] · basis authored_standard · registry 11 sections

PASS  library complete: ['ch_03_canonical.json', 'ch_03_canonical_p13.json', 'ch_03_canonical_p10.json'] vs plan [16, 13, 10]
PASS  ch_03_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_03_canonical.json: every anchor verbatim in the top registry
PASS  ch_03_canonical.json: first-visit order follows the registry
PASS  ch_03_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_03_canonical_p13.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_03_canonical_p13.json: every anchor verbatim in the top registry
PASS  ch_03_canonical_p13.json: first-visit order follows the registry
PASS  ch_03_canonical_p13.json: coverage reaches the final registry section
PASS  ch_03_canonical_p10.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_03_canonical_p10.json: every anchor verbatim in the top registry
PASS  ch_03_canonical_p10.json: first-visit order follows the registry
PASS  ch_03_canonical_p10.json: coverage reaches the final registry section
PASS  ch_03_canonical.json: register scan reached the band text (64 band(s) read: {'activity_title': 16, 'teacher_notes': 16, 'time_bands': 64, 'homework': 1})
FAIL  ch_03_canonical.json: register clean (6 ban hit(s))
      U2 time_bands[3] 37-45 [forward] …n their timelines as 'coronation at Raigad' as a preview of the next unit's content.
      U6 time_bands[3] 35-45 [forward] …achiv) — setting up the military and conflict discussion in later units.
      U7 time_bands[0] 0-8 [forward] …te-equipped) + shiledars (self-equipped); navy addressed in the next unit.
      U7 time_bands[0] 0-8 [clock] …the military administration section of the chapter summary for four minutes, then fill in what each branch comprised. Teacher checks an…
      U9 time_bands[0] 0-10 [clock] …and begin reading the two sections from the chapter summary for five minutes.
      U16 time_bands[0] 0-10 [clock] …a' and 'Serfoji II's Dhanwantari Mahal.' Teacher circulates for three minutes, then students share one item per spoke with a partner.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_03_canonical_p13.json: register scan reached the band text (52 band(s) read: {'activity_title': 13, 'teacher_notes': 13, 'time_bands': 52, 'homework': 2})
PASS  ch_03_canonical_p13.json: register clean (0 ban hit(s))
PASS  ch_03_canonical_p10.json: register scan reached the band text (40 band(s) read: {'activity_title': 10, 'teacher_notes': 10, 'time_bands': 40, 'homework': 4})
FAIL  ch_03_canonical_p10.json: register clean (1 ban hit(s))
      U4 time_bands[0] 0-10 [clock] …t new problem might this create?' Students discuss in pairs for two minutes, then share. Teacher records responses and holds them for r…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_03_canonical.json: MCQ options in arrangement order
PASS  ch_03_canonical_p13.json: MCQ options in arrangement order
PASS  ch_03_canonical_p10.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_03_canonical.json: 20 items vs 20 expected
      ch_03_canonical_p13.json: 19 items vs 20 expected  <-- MISS
          C-9.1 (Present) has 1, its siblings carry 2
      ch_03_canonical_p10.json: 20 items vs 20 expected
      -> 1 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
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
PASS  X=18: choice set non-empty (no defensive truncation)

serve sweep: {"8": "fill/single -2s", "9": "fill/single -1s", "10": "identity", "11": "fill/single", "12": "synthesis", "13": "identity", "14": "fill/single", "15": "synthesis", "16": "identity", "17": "surrender", "18": "surrender"}

options arranged: 41 of 41 item(s) re-ordered this run — the generation-quality rate for Rule 7 (ARV-D-032). A 0 with no earlier run behind it means the model arranged them unaided.
      ch_03_canonical.json: 14 of 14 item(s) re-ordered
          #1 C-2.1 U1: A–D now hold ACBD · correct A -> A
          #2 C-2.1 U5: A–D now hold CABD · correct A -> B
          #6 C-3.2 U2: A–D now hold BCAD · correct A -> C
          #7 C-3.2 U13: A–D now hold ADCB · correct A -> A
          #9 C-4.1 U6: A–D now hold BDAC · correct A -> C
          #10 C-4.1 U8: A–D now hold ADCB · correct A -> A
          #12 C-7.1 U10: A–D now hold DCBA · correct A -> D
          #13 C-7.1 U12: A–D now hold ACBD · correct A -> A
          #15 C-7.3 U1: A–D now hold BADC · correct A -> B
          #16 C-7.3 U15: A–D now hold BCAD · correct A -> C
          #17 C-9.1 U9: A–D now hold CADB · correct A -> B
          #18 C-9.1 U9: A–D now hold CBDA · correct A -> D
          #19 C-10.1 U14: A–D now hold DBCA · correct A -> D
          #20 C-10.1 U16: A–D now hold ADCB · correct A -> A
      ch_03_canonical_p10.json: 14 of 14 item(s) re-ordered
          #1 C-2.1 U1: A–D now hold BADC · correct A -> B
          #2 C-2.1 U3: A–D now hold BDCA · correct B -> A
          #6 C-3.2 U2: A–D now hold BACD · correct B -> A
          #7 C-3.2 U4: A–D now hold ABDC · correct B -> B
          #9 C-4.1 U4: A–D now hold DABC · correct A -> B
          #10 C-4.1 U5: A–D now hold CADB · correct C -> A
          #12 C-7.1 U7: A–D now hold BDAC · correct B -> A
          #13 C-7.1 U9: A–D now hold CDBA · correct B -> C
          #15 C-7.3 U1: A–D now hold CADB · correct B -> D
          #16 C-7.3 U9: A–D now hold ACDB · correct B -> D
          #17 C-9.1 U6: A–D now hold BDAC · correct B -> A
          #18 C-9.1 U6: A–D now hold BACD · correct B -> A
          #19 C-10.1 U10: A–D now hold CADB · correct B -> D
          #20 C-10.1 U10: A–D now hold CABD · correct A -> B
      ch_03_canonical_p13.json: 13 of 13 item(s) re-ordered
          #1 C-2.1 U1: A–D now hold BDCA · correct B -> A
          #2 C-2.1 U4: A–D now hold ADCB · correct C -> C
          #6 C-3.2 U3: A–D now hold BCAD · correct B -> A
          #7 C-3.2 U11: A–D now hold DBCA · correct C -> C
          #9 C-4.1 U5: A–D now hold CABD · correct B -> C
          #10 C-4.1 U6: A–D now hold DBAC · correct B -> B
          #12 C-7.1 U8: A–D now hold ACDB · correct B -> D
          #13 C-7.1 U9: A–D now hold CBAD · correct A -> C
          #15 C-7.3 U1: A–D now hold DACB · correct B -> D
          #16 C-7.3 U10: A–D now hold DBAC · correct B -> B
          #17 C-9.1 U7: A–D now hold DBAC · correct B -> B
          #18 C-10.1 U11: A–D now hold ACDB · correct B -> D
          #19 C-10.1 U13: A–D now hold BADC · correct B -> A

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
