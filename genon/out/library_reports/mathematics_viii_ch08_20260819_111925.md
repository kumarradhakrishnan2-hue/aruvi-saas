# Library certification · mathematics VIII ch 8 · 20260819_111925

plan: counts [14, 11, 8] · basis authored_standard · registry 3 sections

FAIL  library complete: ['ch_08_canonical.json'] vs plan [14, 11, 8]
serve granularity: unit  ·  section axis: True
PASS  ch_08_canonical.json: every section the chapter summary carries is anchored by some unit (3 summary section(s) vs 3 registry entr(ies))
PASS  ch_08_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_08_canonical.json: every anchor verbatim in the top registry
PASS  ch_08_canonical.json: first-visit order follows the registry
PASS  ch_08_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_08_canonical.json: register scan reached the band text (56 band(s) read: {'activity_title': 14, 'materials': 34, 'teacher_notes': 14, 'time_bands': 56, 'homework': 9})
FAIL  ch_08_canonical.json: register clean (2 ban hit(s))
      U9 time_bands[3] 38–45 [forward] …small loss or exact break-even depending on base) motivates the next unit's exploration of compounded percentage changes.
      U11 time_bands[3] 38–45 [forward] …ntence prediction, motivating the generalisation to come in the following unit.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_08_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_08_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_08_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_08_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_08_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"(from handoff)": 0}
      ch_08_canonical.json: 0 items vs 0 expected
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

serve sweep: {"6": "fill/single", "7": "fill/single", "8": "fill/single", "9": "synthesis", "10": "synthesis", "11": "synthesis", "12": "synthesis", "13": "synthesis", "14": "identity", "15": "surrender", "16": "surrender"}

options arranged: 0 of 2 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_08_canonical.json: 0 of 2 item(s) re-ordered

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
