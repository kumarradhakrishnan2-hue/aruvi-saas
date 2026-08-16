# Library certification · social_sciences VIII ch 12 · 20260816_094443

plan: counts [13, 11, 8] · basis authored_standard · registry 12 sections

FAIL  library complete: ['ch_12_canonical.json'] vs plan [13, 11, 8]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_12_canonical.json: 4 prose lead(s) in the summary match no registry entry (9 summary section(s) vs 12 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section; This short section; A reference table; The closing recap
      ADVISORY ch_12_canonical.json: 7 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Who Is a Citizen?; Fundamental Rights in the Indian Constitution; Right to equality; Right to freedom; Right to freedom of religion; Key Constitutional Articles That Guide Our Rights …
PASS  ch_12_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_12_canonical.json: every anchor verbatim in the top registry
PASS  ch_12_canonical.json: first-visit order follows the registry
PASS  ch_12_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_12_canonical.json: register scan reached the band text (52 band(s) read: {'activity_title': 13, 'materials': 40, 'teacher_notes': 13, 'time_bands': 52, 'visual_aids': 6})
PASS  ch_12_canonical.json: register clean (0 ban hit(s))
PASS  ch_12_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_12_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_12_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_12_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_12_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_12_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_12_canonical.json: 17 items vs 17 expected
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

serve sweep: {"6": "fill/single -6s", "7": "fill/single -5s", "8": "fill/single -4s", "9": "fill/single -3s", "10": "fill/single -2s", "11": "fill/single -1s", "12": "fill/single", "13": "identity", "14": "surrender", "15": "surrender"}

options arranged: 0 of 12 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_12_canonical.json: 0 of 12 item(s) re-ordered

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
