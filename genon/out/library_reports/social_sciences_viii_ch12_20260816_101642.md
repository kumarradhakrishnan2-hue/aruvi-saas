# Library certification · social_sciences VIII ch 12 · 20260816_101642

plan: counts [13, 11, 8] · basis authored_standard · registry 12 sections

PASS  library complete: ['ch_12_canonical.json', 'ch_12_canonical_p11.json', 'ch_12_canonical_p08.json'] vs plan [13, 11, 8]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_12_canonical.json: 4 prose lead(s) in the summary match no registry entry (9 summary section(s) vs 12 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section; This short section; A reference table; The closing recap
      ADVISORY ch_12_canonical.json: 7 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Who Is a Citizen?; Fundamental Rights in the Indian Constitution; Right to equality; Right to freedom; Right to freedom of religion; Key Constitutional Articles That Guide Our Rights …
PASS  ch_12_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_12_canonical.json: every anchor verbatim in the top registry
PASS  ch_12_canonical.json: first-visit order follows the registry
PASS  ch_12_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_12_canonical_p11.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_12_canonical_p11.json: every anchor verbatim in the top registry
PASS  ch_12_canonical_p11.json: first-visit order follows the registry
PASS  ch_12_canonical_p11.json: coverage reaches the final registry section
PASS  ch_12_canonical_p08.json: the `synthesis` token is reserved to the standard canonical
FAIL  ch_12_canonical_p08.json: every anchor verbatim in the top registry
FAIL  ch_12_canonical_p08.json: first-visit order follows the registry
FAIL  ch_12_canonical_p08.json: coverage reaches the final registry section
PASS  ch_12_canonical.json: register scan reached the band text (52 band(s) read: {'activity_title': 13, 'materials': 40, 'teacher_notes': 13, 'time_bands': 52, 'visual_aids': 6})
PASS  ch_12_canonical.json: register clean (0 ban hit(s))
PASS  ch_12_canonical_p11.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 33, 'teacher_notes': 11, 'time_bands': 44, 'visual_aids': 5})
FAIL  ch_12_canonical_p11.json: register clean (4 ban hit(s))
      ADVISORY ch_12_canonical_p11.json: 1 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U3 teacher_notes: 'from the previous unit' — …nsure groups physically read the text rather than recalling from the previous unit; the goal is to build the habit of returning to constitutio…
      U2 teacher_notes [forward] …es, which connects to the duties discussion that follows in later units.
      U5 time_bands[0] 0-12 [clock] …schools handle student opinions? Students discuss in pairs for three minutes, then share. Teacher records the principle: freedoms exist…
      U7 teacher_notes [forward] …ask (duty to right) is the key analytical move that sets up the next unit's 'two sides of the same coin' argument.
      U10 time_bands[3] 35-45 [forward] …e response? What is inclusion?' — opening the question that the next unit answers.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_12_canonical_p08.json: register scan reached the band text (32 band(s) read: {'activity_title': 8, 'materials': 22, 'teacher_notes': 8, 'time_bands': 32, 'visual_aids': 4})
FAIL  ch_12_canonical_p08.json: register clean (1 ban hit(s))
      U5 time_bands[3] 38-45 [forward] …nal idea of duty and the traditional concept, preparing for the next unit's rights-duties synthesis.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_12_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_12_canonical_p11.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_12_canonical_p08.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_12_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_12_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_12_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_12_canonical_p11.json: every question_type is a known assessment type (0 not)
PASS  ch_12_canonical_p11.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_12_canonical_p11.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_12_canonical_p08.json: every question_type is a known assessment type (0 not)
PASS  ch_12_canonical_p08.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_12_canonical_p08.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_12_canonical.json: MCQ options in arrangement order
PASS  ch_12_canonical_p11.json: MCQ options in arrangement order
PASS  ch_12_canonical_p08.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_12_canonical.json: 17 items vs 17 expected
      ch_12_canonical_p11.json: 17 items vs 17 expected
      ch_12_canonical_p08.json: 15 items vs 17 expected  <-- MISS
          C-5.2 (Substantive) has 2, its siblings carry 3
          C-7.1 (Present) has 1, its siblings carry 2
      -> 2 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
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

serve sweep: {"6": "fill/single -5s", "7": "fill/forward -1s", "8": "identity", "9": "rescue/complete (from 11)", "10": "fill/forward", "11": "identity", "12": "fill/single", "13": "identity", "14": "surrender", "15": "surrender"}

options arranged: 22 of 35 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_12_canonical.json: 0 of 12 item(s) re-ordered
      ch_12_canonical_p08.json: 11 of 11 item(s) re-ordered
          #1 C-8.1 U1: A–D now hold CDBA · correct A -> D
          #2 C-8.1 U4: A–D now hold BDCA · correct B -> A
          #6 C-5.1 U2: A–D now hold BDAC · correct A -> C
          #7 C-5.1 U7: A–D now hold BADC · correct B -> A
          #9 C-5.2 U3: A–D now hold CADB · correct B -> D
          #10 C-5.2 U8: A–D now hold ACBD · correct B -> C
          #11 C-4.2 U4: A–D now hold DCBA · correct B -> C
          #12 C-4.2 U4: A–D now hold DBCA · correct B -> B
          #13 C-7.1 U4: A–D now hold BCDA · correct B -> A
          #14 C-10.1 U5: A–D now hold DCBA · correct B -> C
          #15 C-10.1 U5: A–D now hold ADBC · correct B -> C
      ch_12_canonical_p11.json: 11 of 12 item(s) re-ordered
          #1 C-8.1 U1: A–D now hold CBAD · correct A -> C
          #2 C-8.1 U9: A–D now hold CBDA · correct A -> D
          #6 C-5.1 U10: A–D now hold CBDA · correct A -> D
          #7 C-5.1 U11: A–D now hold CBAD · correct A -> C
          #9 C-5.2 U4: A–D now hold CBAD · correct A -> C
          #10 C-5.2 U2: A–D now hold CABD · correct A -> B
          #12 C-4.2 U5: A–D now hold ACDB · correct A -> A
          #13 C-4.2 U5: A–D now hold ACBD · correct A -> A
          #14 C-7.1 U6: A–D now hold DCBA · correct A -> D
          #16 C-10.1 U8: A–D now hold ACBD · correct A -> A
          #17 C-10.1 U8: A–D now hold CDAB · correct A -> C
QUARANTINED  ch_12_canonical_p08.json -> backup/quarantine/social_sciences/viii/ch_12_canonical_p08_20260816_101642.json

DETERMINISTIC CHECKS HAVE FAILURES — do not certify Failed files are QUARANTINED under backup/quarantine/ (the fix worklist); regenerate them and re-run --certify-only..
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
