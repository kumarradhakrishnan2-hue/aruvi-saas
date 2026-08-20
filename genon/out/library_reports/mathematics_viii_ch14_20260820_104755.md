# Library certification · mathematics VIII ch 14 · 20260820_104755

plan: counts [14, 11, 8] · basis authored_standard · registry 7 sections

PASS  library complete: ['ch_14_canonical.json', 'ch_14_canonical_p11.json', 'ch_14_canonical_p08.json'] vs plan [14, 11, 8]
serve granularity: unit  ·  section axis: True
PASS  ch_14_canonical.json: every section the chapter summary carries is anchored by some unit (7 summary section(s) vs 7 registry entr(ies))
PASS  ch_14_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_14_canonical.json: every anchor verbatim in the top registry
PASS  ch_14_canonical.json: first-visit order follows the registry
PASS  ch_14_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_14_canonical_p11.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_14_canonical_p11.json: every anchor verbatim in the top registry
PASS  ch_14_canonical_p11.json: first-visit order follows the registry
PASS  ch_14_canonical_p11.json: coverage reaches the final registry section
PASS  ch_14_canonical_p08.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_14_canonical_p08.json: every anchor verbatim in the top registry
PASS  ch_14_canonical_p08.json: first-visit order follows the registry
PASS  ch_14_canonical_p08.json: coverage reaches the final registry section
PASS  ch_14_canonical.json: register scan reached the band text (57 band(s) read: {'activity_title': 14, 'materials': 50, 'teacher_notes': 14, 'time_bands': 57, 'homework': 4, 'visual_aids': 1})
FAIL  ch_14_canonical.json: register clean (1 ban hit(s))
      U14 teacher_notes [clock] …once. Students work individually with full written working for the first fifteen minutes — no discussion during this phase. Then small groups of thr…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_14_canonical_p11.json: register scan reached the band text (43 band(s) read: {'activity_title': 11, 'materials': 35, 'teacher_notes': 11, 'time_bands': 43, 'homework': 9})
PASS  ch_14_canonical_p11.json: register clean (0 ban hit(s))
PASS  ch_14_canonical_p08.json: register scan reached the band text (32 band(s) read: {'activity_title': 8, 'materials': 27, 'teacher_notes': 8, 'time_bands': 32, 'homework': 7})
PASS  ch_14_canonical_p08.json: register clean (0 ban hit(s))
PASS  ch_14_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_14_canonical_p11.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_14_canonical_p08.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_14_canonical.json: no stem points at a figure the item does not carry (0 does)
PASS  ch_14_canonical_p11.json: no stem points at a figure the item does not carry (0 does)
PASS  ch_14_canonical_p08.json: no stem points at a figure the item does not carry (0 does)
PASS  ch_14_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_14_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_14_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_14_canonical_p11.json: every question_type is a known assessment type (0 not)
PASS  ch_14_canonical_p11.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_14_canonical_p11.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_14_canonical_p08.json: every question_type is a known assessment type (0 not)
PASS  ch_14_canonical_p08.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_14_canonical_p08.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_14_canonical.json: MCQ options in arrangement order
PASS  ch_14_canonical_p11.json: MCQ options in arrangement order
PASS  ch_14_canonical_p08.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"(from handoff)": 0}
      ch_14_canonical.json: 0 items vs 0 expected
      ch_14_canonical_p11.json: 0 items vs 0 expected
      ch_14_canonical_p08.json: 0 items vs 0 expected
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
PASS  X=16: choice set non-empty (no defensive truncation)

serve sweep: {"6": "fill/single -2s", "7": "fill/single -1s", "8": "identity", "9": "fill/single", "10": "fill/single", "11": "identity", "12": "fill/single", "13": "synthesis", "14": "identity", "15": "surrender", "16": "surrender"}

options arranged: 0 of 5 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_14_canonical.json: 0 of 3 item(s) re-ordered
      ch_14_canonical_p08.json: 0 of 1 item(s) re-ordered
      ch_14_canonical_p11.json: 0 of 1 item(s) re-ordered

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
