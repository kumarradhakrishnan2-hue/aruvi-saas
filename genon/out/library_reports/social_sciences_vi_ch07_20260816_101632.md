# Library certification · social_sciences VI ch 7 · 20260816_101632

plan: counts [22, 18, 13] · basis authored_standard · registry 21 sections

PASS  library complete: ['ch_07_canonical.json', 'ch_07_canonical_p18.json', 'ch_07_canonical_p13.json'] vs plan [22, 18, 13]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_07_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_07_canonical.json: every anchor verbatim in the top registry
PASS  ch_07_canonical.json: first-visit order follows the registry
PASS  ch_07_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_07_canonical_p18.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_07_canonical_p18.json: every anchor verbatim in the top registry
PASS  ch_07_canonical_p18.json: first-visit order follows the registry
PASS  ch_07_canonical_p18.json: coverage reaches the final registry section
PASS  ch_07_canonical_p13.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_07_canonical_p13.json: every anchor verbatim in the top registry
PASS  ch_07_canonical_p13.json: first-visit order follows the registry
FAIL  ch_07_canonical_p13.json: coverage reaches the final registry section
      OMITS 4 cell(s) the standard teaches — ch_07_canonical_p13.json: Buddhism — ahimsa; Jainism — ahimsa extended to all living beings; The Vedas — UNESCO recognition; Buddhism — spread across Asia; Jainism — anekāntavāda as intellectual contribution; Buddhism — enduring influence; Jainism — rock-cut caves and monasteries; Folk and Tribal Roots — continued tribal worship practices; Buddhism — ahimsa and the Sangha; Jainism — anekāntavāda; Folk and Tribal Roots — mutual exchange; Vedic schools — brahman and ātman  (reported, not gated — rule at the human gate)
PASS  ch_07_canonical.json: register scan reached the band text (88 band(s) read: {'activity_title': 22, 'materials': 44, 'visual_aids': 16, 'teacher_notes': 22, 'time_bands': 88})
PASS  ch_07_canonical.json: register clean (0 ban hit(s))
PASS  ch_07_canonical_p18.json: register scan reached the band text (72 band(s) read: {'activity_title': 18, 'materials': 36, 'visual_aids': 14, 'teacher_notes': 18, 'time_bands': 72})
FAIL  ch_07_canonical_p18.json: register clean (5 ban hit(s))
      ADVISORY ch_07_canonical_p18.json: 1 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U11 time_bands[1] 12-24: 'from the previous unit' — …yse the story in groups of three, using three Jain concepts from the previous unit: 'Where in Rohineya's story can you see right action, right…
      U4 teacher_notes [forward] …r itself uses stories to make these ideas accessible, which the next unit will exploit.
      U6 time_bands[0] 0-10 [clock] …uted to the foundations of Hinduism. They work individually for five minutes, then compare with a neighbour.
      U9 teacher_notes [forward] …lytical question about diversity of intellectual traditions foreshadows the chapter's broader argument about India's cultural roots…
      U9 time_bands[1] 10-25 [clock] …specific framework of brahman-ātman). Working individually for eight minutes, they then compare with a partner and reconcile differences…
      U10 time_bands[1] 10-22 [clock] …on might apply it in daily life. Students work individually for seven minutes, then compare examples with a partner.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_07_canonical_p13.json: register scan reached the band text (52 band(s) read: {'activity_title': 13, 'materials': 44, 'visual_aids': 10, 'teacher_notes': 13, 'time_bands': 52})
PASS  ch_07_canonical_p13.json: register clean (0 ban hit(s))
PASS  ch_07_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_07_canonical_p18.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_07_canonical_p13.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_07_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_07_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_07_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_07_canonical_p18.json: every question_type is a known assessment type (0 not)
PASS  ch_07_canonical_p18.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_07_canonical_p18.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_07_canonical_p13.json: every question_type is a known assessment type (0 not)
PASS  ch_07_canonical_p13.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_07_canonical_p13.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_07_canonical.json: MCQ options in arrangement order
PASS  ch_07_canonical_p18.json: MCQ options in arrangement order
PASS  ch_07_canonical_p13.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_07_canonical.json: 20 items vs 20 expected
      ch_07_canonical_p18.json: 20 items vs 20 expected
      ch_07_canonical_p13.json: 19 items vs 20 expected  <-- MISS
          C-7.1 (Substantive) has 2, its siblings carry 3
      -> 1 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
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
PASS  X=24: choice set non-empty (no defensive truncation)

serve sweep: {"11": "fill/single -6s", "12": "fill/single -5s", "13": "identity", "14": "rescue/complete (from 18)", "15": "fill/single -6s", "16": "fill/single -5s", "17": "fill/single -4s", "18": "identity", "19": "rescue/complete (from 22)", "20": "fill/single -1s", "21": "fill/single", "22": "identity", "23": "surrender", "24": "surrender"}

options arranged: 26 of 42 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_07_canonical.json: 0 of 14 item(s) re-ordered
      ch_07_canonical_p13.json: 14 of 14 item(s) re-ordered
          #1 C-3.1 U4: A–D now hold BADC · correct B -> A
          #2 C-3.1 U9: A–D now hold BACD · correct B -> A
          #6 C-2.1 U3: A–D now hold DABC · correct B -> C
          #7 C-2.1 U12: A–D now hold BADC · correct B -> A
          #9 C-2.2 U6: A–D now hold BACD · correct B -> A
          #10 C-2.2 U8: A–D now hold BACD · correct B -> A
          #12 C-7.1 U1: A–D now hold BCAD · correct B -> A
          #13 C-7.1 U9: A–D now hold DCBA · correct B -> C
          #14 C-1.1 U2: A–D now hold CDBA · correct B -> C
          #15 C-1.1 U2: A–D now hold DACB · correct B -> D
          #16 C-7.3 U12: A–D now hold ABDC · correct B -> B
          #17 C-7.3 U13: A–D now hold ABDC · correct B -> B
          #18 C-10.1 U2: A–D now hold DBAC · correct B -> B
          #19 C-10.1 U10: A–D now hold DBAC · correct B -> B
      ch_07_canonical_p18.json: 12 of 14 item(s) re-ordered
          #1 C-3.1 U4: A–D now hold ADBC · correct A -> A
          #2 C-3.1 U9: A–D now hold BDAC · correct A -> C
          #7 C-2.1 U7: A–D now hold DCAB · correct A -> C
          #9 C-2.2 U8: A–D now hold CADB · correct A -> B
          #10 C-2.2 U14: A–D now hold DCAB · correct A -> C
          #12 C-7.1 U9: A–D now hold DABC · correct A -> B
          #13 C-7.1 U15: A–D now hold DCBA · correct A -> D
          #15 C-1.1 U2: A–D now hold DCBA · correct A -> D
          #16 C-1.1 U2: A–D now hold DBAC · correct A -> C
          #17 C-7.3 U13: A–D now hold DABC · correct A -> B
          #18 C-7.3 U18: A–D now hold BADC · correct A -> B
          #19 C-10.1 U2: A–D now hold CADB · correct A -> B
          #6 SKIPPED — cross-references an option label — left untouched, needs a human
QUARANTINED  ch_07_canonical_p13.json -> backup/quarantine/social_sciences/vi/ch_07_canonical_p13_20260816_101632.json

DETERMINISTIC CHECKS HAVE FAILURES — do not certify Failed files are QUARANTINED under backup/quarantine/ (the fix worklist); regenerate them and re-run --certify-only..
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
