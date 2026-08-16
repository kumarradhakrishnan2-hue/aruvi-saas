# Library certification · social_sciences VIII ch 5 · 20260816_101640

plan: counts [12, 10, 7] · basis authored_standard · registry 11 sections

PASS  library complete: ['ch_05_canonical.json', 'ch_05_canonical_p10.json', 'ch_05_canonical_p07.json'] vs plan [12, 10, 7]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_05_canonical.json: 1 prose lead(s) in the summary match no registry entry (2 summary section(s) vs 11 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section
      ADVISORY ch_05_canonical.json: 10 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Universal Adult Franchise; The Role of the Election Commission of India (ECI); Election Commission of India — A brief introduction; Managing the electoral process; Model Code of Conduct (MCC); Election to the Lok Sabha and State Legislative Assemblies …
PASS  ch_05_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_05_canonical.json: every anchor verbatim in the top registry
PASS  ch_05_canonical.json: first-visit order follows the registry
PASS  ch_05_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_05_canonical_p10.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_05_canonical_p10.json: every anchor verbatim in the top registry
PASS  ch_05_canonical_p10.json: first-visit order follows the registry
PASS  ch_05_canonical_p10.json: coverage reaches the final registry section
PASS  ch_05_canonical_p07.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_05_canonical_p07.json: every anchor verbatim in the top registry
PASS  ch_05_canonical_p07.json: first-visit order follows the registry
PASS  ch_05_canonical_p07.json: coverage reaches the final registry section
PASS  ch_05_canonical.json: register scan reached the band text (60 band(s) read: {'activity_title': 12, 'materials': 24, 'visual_aids': 10, 'teacher_notes': 12, 'time_bands': 60})
PASS  ch_05_canonical.json: register clean (0 ban hit(s))
PASS  ch_05_canonical_p10.json: register scan reached the band text (40 band(s) read: {'activity_title': 10, 'materials': 28, 'visual_aids': 10, 'teacher_notes': 10, 'time_bands': 40})
FAIL  ch_05_canonical_p10.json: register clean (6 ban hit(s))
      U3 time_bands[1] 8-22 [forward] …the Model Code of Conduct — hold this for elaboration in a later unit; note only that it governs campaign behaviour. (4) Overseei…
      U6 time_bands[3] 34-45 [clock] …the logic of how FPTP is designed to work.' Students write for five minutes; three or four read aloud. The teacher synthesises: FPTP pr…
      U7 time_bands[3] 35-45 [clock] …Sabha, or differently democratic?' Students argue in pairs for two minutes, then share. The teacher draws out that democratic legitima…
      U9 time_bands[2] 25-38 [clock] …only looked at the post-1947 Constitution.' Students write for eight minutes; this requires them to reason historically, not just report…
      U10 time_bands[2] 22-35 [clock] …ven the institutional constraints?' Students argue in pairs for three minutes, then share. The teacher ensures both perspectives are hear…
      U10 time_bands[3] 35-45 [clock] …ut the electoral system, how do you decide?' Students write for five minutes; two or three share aloud. The teacher closes without presc…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_05_canonical_p07.json: register scan reached the band text (35 band(s) read: {'activity_title': 7, 'materials': 21, 'visual_aids': 6, 'teacher_notes': 7, 'time_bands': 35})
FAIL  ch_05_canonical_p07.json: register clean (2 ban hit(s))
      U5 teacher_notes [forward] …he unit's closing note on 'direct election' is a conceptual bridge to the indirect election logic of Rajya Sabha, presidential, and v…
      U7 time_bands[2] 20-32 [clock] …mechanism that would be needed.' Students work individually for eight minutes.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_05_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_05_canonical_p10.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_05_canonical_p07.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_05_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_05_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_05_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_05_canonical_p10.json: every question_type is a known assessment type (0 not)
PASS  ch_05_canonical_p10.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_05_canonical_p10.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_05_canonical_p07.json: every question_type is a known assessment type (0 not)
PASS  ch_05_canonical_p07.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_05_canonical_p07.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_05_canonical.json: MCQ options in arrangement order
PASS  ch_05_canonical_p10.json: MCQ options in arrangement order
PASS  ch_05_canonical_p07.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_05_canonical.json: 16 items vs 16 expected
      ch_05_canonical_p10.json: 15 items vs 16 expected  <-- MISS
          C-8.3 (Present) has 1, its siblings carry 2
      ch_05_canonical_p07.json: 16 items vs 16 expected
      -> 1 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
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

serve sweep: {"5": "fill/single -4s", "6": "fill/forward -1s", "7": "identity", "8": "rescue/complete (from 10)", "9": "fill/single", "10": "identity", "11": "fill/single", "12": "identity", "13": "surrender", "14": "surrender"}

options arranged: 22 of 35 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_05_canonical.json: 0 of 12 item(s) re-ordered
      ch_05_canonical_p07.json: 12 of 12 item(s) re-ordered
          #1 C-4.1 U1: A–D now hold ADBC · correct A -> A
          #2 C-4.1 U6: A–D now hold BACD · correct A -> B
          #6 C-5.2 U2: A–D now hold BDCA · correct A -> D
          #7 C-5.2 U2: A–D now hold DABC · correct A -> B
          #9 C-4.2 U4: A–D now hold BDAC · correct A -> C
          #10 C-4.2 U7: A–D now hold BDCA · correct A -> D
          #11 C-8.3 U3: A–D now hold DBAC · correct A -> C
          #12 C-8.3 U3: A–D now hold DCAB · correct A -> C
          #13 C-5.1 U1: A–D now hold ACDB · correct A -> A
          #14 C-5.1 U2: A–D now hold ACBD · correct A -> A
          #15 C-10.1 U4: A–D now hold BACD · correct A -> B
          #16 C-10.1 U7: A–D now hold BDCA · correct A -> D
      ch_05_canonical_p10.json: 10 of 11 item(s) re-ordered
          #1 C-4.1 U1: A–D now hold DABC · correct A -> B
          #2 C-4.1 U4: A–D now hold BCAD · correct B -> A
          #6 C-5.2 U2: A–D now hold CBAD · correct B -> B
          #7 C-5.2 U10: A–D now hold ADCB · correct B -> D
          #9 C-4.2 U1: A–D now hold CABD · correct B -> C
          #11 C-8.3 U3: A–D now hold DCBA · correct C -> B
          #12 C-5.1 U2: A–D now hold CABD · correct B -> C
          #13 C-5.1 U4: A–D now hold CABD · correct B -> C
          #14 C-10.1 U4: A–D now hold DBCA · correct B -> B
          #15 C-10.1 U9: A–D now hold CADB · correct B -> D
          #10 SKIPPED — cross-references an option label — left untouched, needs a human

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
