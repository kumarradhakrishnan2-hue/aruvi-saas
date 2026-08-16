# Library certification · social_sciences VIII ch 10 · 20260816_101642

plan: counts [12, 10, 7] · basis authored_standard · registry 11 sections

PASS  library complete: ['ch_10_canonical.json', 'ch_10_canonical_p10.json', 'ch_10_canonical_p07.json'] vs plan [12, 10, 7]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_10_canonical.json: 3 prose lead(s) in the summary match no registry entry (3 summary section(s) vs 11 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section; The final descriptive section; The closing recap consolidates the chapter's argument
      ADVISORY ch_10_canonical.json: 11 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Introduction; The Beginnings …; Structural Stupa Architecture; Rock-Cut Architecture; Water Structures; Classical Temple Architecture …
PASS  ch_10_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_10_canonical.json: every anchor verbatim in the top registry
PASS  ch_10_canonical.json: first-visit order follows the registry
PASS  ch_10_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_10_canonical_p10.json: the `synthesis` token is reserved to the standard canonical
FAIL  ch_10_canonical_p10.json: every anchor verbatim in the top registry
FAIL  ch_10_canonical_p10.json: first-visit order follows the registry
PASS  ch_10_canonical_p10.json: coverage reaches the final registry section
PASS  ch_10_canonical_p07.json: the `synthesis` token is reserved to the standard canonical
FAIL  ch_10_canonical_p07.json: every anchor verbatim in the top registry
FAIL  ch_10_canonical_p07.json: first-visit order follows the registry
FAIL  ch_10_canonical_p07.json: coverage reaches the final registry section
PASS  ch_10_canonical.json: register scan reached the band text (48 band(s) read: {'activity_title': 12, 'materials': 36, 'visual_aids': 10, 'teacher_notes': 12, 'time_bands': 48})
PASS  ch_10_canonical.json: register clean (0 ban hit(s))
PASS  ch_10_canonical_p10.json: register scan reached the band text (40 band(s) read: {'activity_title': 10, 'materials': 22, 'visual_aids': 10, 'teacher_notes': 10, 'time_bands': 40})
PASS  ch_10_canonical_p10.json: register clean (0 ban hit(s))
      ADVISORY ch_10_canonical_p10.json: 1 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U2 time_bands[2] 20-33: 'from the previous unit' — …eyond — students add 'Sanchi, Madhya Pradesh' to their maps from the previous unit.
PASS  ch_10_canonical_p07.json: register scan reached the band text (28 band(s) read: {'activity_title': 7, 'materials': 21, 'visual_aids': 7, 'teacher_notes': 7, 'time_bands': 28})
FAIL  ch_10_canonical_p07.json: register clean (1 ban hit(s))
      U3 teacher_notes [forward] …present civic responsibility, making this section a natural bridge to the chapter's closing argument.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_10_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_10_canonical_p10.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_10_canonical_p07.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_10_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_10_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_10_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_10_canonical_p10.json: every question_type is a known assessment type (0 not)
PASS  ch_10_canonical_p10.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_10_canonical_p10.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_10_canonical_p07.json: every question_type is a known assessment type (0 not)
PASS  ch_10_canonical_p07.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_10_canonical_p07.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_10_canonical.json: MCQ options in arrangement order
PASS  ch_10_canonical_p10.json: MCQ options in arrangement order
PASS  ch_10_canonical_p07.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_10_canonical.json: 15 items vs 15 expected
      ch_10_canonical_p10.json: 15 items vs 15 expected
      ch_10_canonical_p07.json: 15 items vs 15 expected
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

serve sweep: {"5": "fill/forward -5s", "6": "fill/single -4s", "7": "identity", "8": "rescue/complete (from 10)", "9": "fill/forward -1s", "10": "identity", "11": "fill/single", "12": "identity", "13": "surrender", "14": "surrender"}

options arranged: 19 of 30 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_10_canonical.json: 0 of 10 item(s) re-ordered
      ch_10_canonical_p07.json: 9 of 10 item(s) re-ordered
          #1 C-7.1 U1: A–D now hold CBAD · correct B -> B
          #2 C-7.1 U5: A–D now hold CBDA · correct A -> D
          #6 C-2.2 U2: A–D now hold ACDB · correct A -> A
          #7 C-2.2 U6: A–D now hold CDBA · correct A -> D
          #10 C-10.1 U4: A–D now hold CABD · correct B -> C
          #12 C-1.2 U1: A–D now hold CBAD · correct B -> B
          #13 C-1.2 U5: A–D now hold BACD · correct A -> B
          #14 C-4.2 U4: A–D now hold BADC · correct B -> A
          #15 C-4.2 U5: A–D now hold DCAB · correct B -> D
          #9 SKIPPED — cross-references an option label — left untouched, needs a human
      ch_10_canonical_p10.json: 10 of 10 item(s) re-ordered
          #1 C-7.1 U2: A–D now hold DABC · correct B -> C
          #2 C-7.1 U6: A–D now hold CDBA · correct B -> C
          #6 C-2.2 U3: A–D now hold BCDA · correct B -> A
          #7 C-2.2 U4: A–D now hold CADB · correct B -> D
          #9 C-10.1 U1: A–D now hold ABDC · correct B -> B
          #10 C-10.1 U4: A–D now hold DBCA · correct B -> B
          #12 C-1.2 U1: A–D now hold DABC · correct B -> C
          #13 C-1.2 U7: A–D now hold CABD · correct B -> C
          #14 C-4.2 U2: A–D now hold CDBA · correct B -> C
          #15 C-4.2 U6: A–D now hold DCAB · correct B -> D
QUARANTINED  ch_10_canonical_p07.json -> backup/quarantine/social_sciences/viii/ch_10_canonical_p07_20260816_101642.json
QUARANTINED  ch_10_canonical_p10.json -> backup/quarantine/social_sciences/viii/ch_10_canonical_p10_20260816_101642.json

DETERMINISTIC CHECKS HAVE FAILURES — do not certify Failed files are QUARANTINED under backup/quarantine/ (the fix worklist); regenerate them and re-run --certify-only..
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
