# Library certification · social_sciences VII ch 4 · 20260816_113721

plan: counts [19, 15, 11] · basis authored_standard · registry 9 sections

PASS  library complete: ['ch_04_canonical.json', 'ch_04_canonical_p15.json', 'ch_04_canonical_p11.json'] vs plan [19, 15, 11]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_04_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_04_canonical.json: every anchor verbatim in the top registry
PASS  ch_04_canonical.json: first-visit order follows the registry
PASS  ch_04_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_04_canonical_p15.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_04_canonical_p15.json: every anchor verbatim in the top registry
PASS  ch_04_canonical_p15.json: first-visit order follows the registry
PASS  ch_04_canonical_p15.json: coverage reaches the final registry section
PASS  ch_04_canonical_p11.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_04_canonical_p11.json: every anchor verbatim in the top registry
PASS  ch_04_canonical_p11.json: first-visit order follows the registry
PASS  ch_04_canonical_p11.json: coverage reaches the final registry section
PASS  ch_04_canonical.json: register scan reached the band text (76 band(s) read: {'activity_title': 19, 'materials': 45, 'visual_aids': 15, 'teacher_notes': 19, 'time_bands': 76})
PASS  ch_04_canonical.json: register clean (0 ban hit(s))
PASS  ch_04_canonical_p15.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 31, 'visual_aids': 12, 'teacher_notes': 15, 'time_bands': 60})
PASS  ch_04_canonical_p15.json: register clean (0 ban hit(s))
PASS  ch_04_canonical_p11.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 27, 'visual_aids': 8, 'teacher_notes': 11, 'time_bands': 44})
FAIL  ch_04_canonical_p11.json: register clean (3 ban hit(s))
      U6 time_bands[0] 0-10 [clock] …rper tools make to a farmer? To a soldier?' They brainstorm for three minutes and share. The teacher records key words (heavier harvests,…
      U8 time_bands[0] 0-8 [forward] …chapter's answer involves two interacting systems, and the unit will examine both.
      U11 teacher_notes [completion] Having worked through all substantive content of the chapter, this unit returns to th…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_04_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_04_canonical_p15.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_04_canonical_p11.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_04_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_04_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_04_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_04_canonical_p15.json: every question_type is a known assessment type (0 not)
PASS  ch_04_canonical_p15.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_04_canonical_p15.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_04_canonical_p11.json: every question_type is a known assessment type (0 not)
PASS  ch_04_canonical_p11.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_04_canonical_p11.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_04_canonical.json: MCQ options in arrangement order
PASS  ch_04_canonical_p15.json: MCQ options in arrangement order
PASS  ch_04_canonical_p11.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_04_canonical.json: 14 items vs 14 expected
      ch_04_canonical_p15.json: 14 items vs 14 expected
      ch_04_canonical_p11.json: 13 items vs 14 expected  <-- MISS
          C-5.1 (Present) has 1, its siblings carry 2
      -> 1 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
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

serve sweep: {"9": "fill/single", "10": "synthesis", "11": "identity", "12": "synthesis", "13": "synthesis", "14": "synthesis", "15": "identity", "16": "synthesis", "17": "synthesis", "18": "synthesis", "19": "identity", "20": "surrender", "21": "surrender"}

options arranged: 0 of 29 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_04_canonical.json: 0 of 10 item(s) re-ordered
          #6 SKIPPED — cross-references an option label — left untouched, needs a human
      ch_04_canonical_p11.json: 0 of 9 item(s) re-ordered
      ch_04_canonical_p15.json: 0 of 10 item(s) re-ordered

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
