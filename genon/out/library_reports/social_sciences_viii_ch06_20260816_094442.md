# Library certification · social_sciences VIII ch 6 · 20260816_094442

plan: counts [12, 10, 7] · basis authored_standard · registry 11 sections

FAIL  library complete: ['ch_06_canonical.json'] vs plan [12, 10, 7]
serve granularity: unit  ·  section axis: True
      registry <-> summary: no unmatched prose lead (1 summary section(s) vs 11 registry entr(ies))
      ADVISORY ch_06_canonical.json: 10 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Introduction; Composition of the Parliament of India; Legislative Functions of the Parliament — Constitutional function; Legislative Functions of the Parliament — Lawmaking; Legislative Functions of the Parliament — Executive accountability and Financial accountability; Executive Functions of Parliament …
PASS  ch_06_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_06_canonical.json: every anchor verbatim in the top registry
PASS  ch_06_canonical.json: first-visit order follows the registry
PASS  ch_06_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_06_canonical.json: register scan reached the band text (48 band(s) read: {'activity_title': 12, 'materials': 35, 'visual_aids': 11, 'teacher_notes': 12, 'time_bands': 48})
PASS  ch_06_canonical.json: register clean (0 ban hit(s))
PASS  ch_06_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_06_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_06_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_06_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_06_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_06_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_06_canonical.json: 13 items vs 14 expected  <-- MISS
          C-8.1 (Present) has 1, its siblings carry 2
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

serve sweep: {"5": "fill/single -6s", "6": "fill/single -5s", "7": "fill/single -4s", "8": "fill/single -3s", "9": "fill/single -2s", "10": "fill/single -1s", "11": "fill/single", "12": "identity", "13": "surrender", "14": "surrender"}

options arranged: 0 of 9 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_06_canonical.json: 0 of 9 item(s) re-ordered

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
