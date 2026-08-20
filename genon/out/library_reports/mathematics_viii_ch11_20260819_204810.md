# Library certification · mathematics VIII ch 11 · 20260819_204810

plan: counts [17, 14, 10] · basis authored_standard · registry 13 sections

PASS  library complete: ['ch_11_canonical.json', 'ch_11_canonical_p14.json', 'ch_11_canonical_p10.json'] vs plan [17, 14, 10]
serve granularity: unit  ·  section axis: True
PASS  ch_11_canonical.json: every section the chapter summary carries is anchored by some unit (13 summary section(s) vs 13 registry entr(ies))
PASS  ch_11_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_11_canonical.json: every anchor verbatim in the top registry
PASS  ch_11_canonical.json: first-visit order follows the registry
PASS  ch_11_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_11_canonical_p14.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_11_canonical_p14.json: every anchor verbatim in the top registry
PASS  ch_11_canonical_p14.json: first-visit order follows the registry
PASS  ch_11_canonical_p14.json: coverage reaches the final registry section
PASS  ch_11_canonical_p10.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_11_canonical_p10.json: every anchor verbatim in the top registry
PASS  ch_11_canonical_p10.json: first-visit order follows the registry
PASS  ch_11_canonical_p10.json: coverage reaches the final registry section
PASS  ch_11_canonical.json: register scan reached the band text (67 band(s) read: {'activity_title': 17, 'materials': 61, 'teacher_notes': 17, 'time_bands': 67, 'homework': 3, 'visual_aids': 1})
FAIL  ch_11_canonical.json: register clean (1 ban hit(s))
      U17 teacher_notes [clock] …once. Students work individually with full written working for the first fifteen minutes — no group talk yet. Then groups of three compare: any disa…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_11_canonical_p14.json: register scan reached the band text (56 band(s) read: {'activity_title': 14, 'materials': 56, 'teacher_notes': 14, 'time_bands': 56})
PASS  ch_11_canonical_p14.json: register clean (0 ban hit(s))
PASS  ch_11_canonical_p10.json: register scan reached the band text (40 band(s) read: {'activity_title': 10, 'materials': 36, 'teacher_notes': 10, 'time_bands': 40})
PASS  ch_11_canonical_p10.json: register clean (0 ban hit(s))
PASS  ch_11_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_11_canonical_p14.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_11_canonical_p10.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_11_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_11_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_11_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_11_canonical_p14.json: every question_type is a known assessment type (0 not)
PASS  ch_11_canonical_p14.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_11_canonical_p14.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_11_canonical_p10.json: every question_type is a known assessment type (0 not)
PASS  ch_11_canonical_p10.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_11_canonical_p10.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_11_canonical.json: MCQ options in arrangement order
PASS  ch_11_canonical_p14.json: MCQ options in arrangement order
PASS  ch_11_canonical_p10.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"(from handoff)": 0}
      ch_11_canonical.json: 0 items vs 0 expected
      ch_11_canonical_p14.json: 0 items vs 0 expected
      ch_11_canonical_p10.json: 0 items vs 0 expected
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
PASS  X=19: choice set non-empty (no defensive truncation)

serve sweep: {"8": "fill/forward -2s", "9": "fill/forward", "10": "identity", "11": "rescue/complete (from 14)", "12": "fill/single -2s", "13": "fill/forward", "14": "identity", "15": "fill/forward", "16": "fill/forward", "17": "identity", "18": "surrender", "19": "surrender"}

options arranged: 0 of 9 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_11_canonical.json: 0 of 4 item(s) re-ordered
      ch_11_canonical_p10.json: 0 of 2 item(s) re-ordered
      ch_11_canonical_p14.json: 0 of 3 item(s) re-ordered

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
