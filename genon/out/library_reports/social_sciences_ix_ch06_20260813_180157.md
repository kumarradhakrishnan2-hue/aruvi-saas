# Library certification · social_sciences IX ch 6 · 20260813_180157

plan: counts [19, 15, 11] · basis authored_standard · registry 17 sections

PASS  library complete: ['ch_06_canonical.json', 'ch_06_canonical_p15.json', 'ch_06_canonical_p11.json'] vs plan [19, 15, 11]
serve granularity: unit  ·  section axis: True
      registry <-> summary: no unmatched prose lead (18 summary section(s) vs 17 registry entr(ies))
PASS  ch_06_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_06_canonical.json: every anchor verbatim in the top registry
PASS  ch_06_canonical.json: first-visit order follows the registry
PASS  ch_06_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_06_canonical_p15.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_06_canonical_p15.json: every anchor verbatim in the top registry
PASS  ch_06_canonical_p15.json: first-visit order follows the registry
PASS  ch_06_canonical_p15.json: coverage reaches the final registry section
PASS  ch_06_canonical_p11.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_06_canonical_p11.json: every anchor verbatim in the top registry
PASS  ch_06_canonical_p11.json: first-visit order follows the registry
PASS  ch_06_canonical_p11.json: coverage reaches the final registry section
PASS  ch_06_canonical.json: register scan reached the band text (76 band(s) read: {'activity_title': 19, 'materials': 40, 'visual_aids': 4, 'teacher_notes': 19, 'time_bands': 76})
PASS  ch_06_canonical.json: register clean (0 ban hit(s))
PASS  ch_06_canonical_p15.json: register scan reached the band text (75 band(s) read: {'activity_title': 15, 'materials': 45, 'visual_aids': 4, 'teacher_notes': 15, 'time_bands': 75})
PASS  ch_06_canonical_p15.json: register clean (0 ban hit(s))
      ADVISORY ch_06_canonical_p15.json: 1 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U4 teacher_notes: 'from the previous unit' — …uss PIL, connect it to the Right to Constitutional Remedies from the previous unit as another route to enforcing rights.
PASS  ch_06_canonical_p11.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 33, 'visual_aids': 4, 'teacher_notes': 11, 'time_bands': 44})
PASS  ch_06_canonical_p11.json: register clean (0 ban hit(s))
PASS  ch_06_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_06_canonical_p15.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_06_canonical_p11.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_06_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_06_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_06_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_06_canonical_p15.json: every question_type is a known assessment type (0 not)
PASS  ch_06_canonical_p15.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_06_canonical_p15.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_06_canonical_p11.json: every question_type is a known assessment type (0 not)
PASS  ch_06_canonical_p11.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_06_canonical_p11.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_06_canonical.json: MCQ options in arrangement order
PASS  ch_06_canonical_p15.json: MCQ options in arrangement order
PASS  ch_06_canonical_p11.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: constitution
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_06_canonical.json: 25 items vs 27 expected  <-- MISS
          C-5.3 (Substantive) has 2, constitution says 3
          C-6.4 (Substantive) has 2, constitution says 3
      ch_06_canonical_p15.json: 25 items vs 27 expected  <-- MISS
          C-5.3 (Substantive) has 2, constitution says 3
          C-6.4 (Substantive) has 2, constitution says 3
      ch_06_canonical_p11.json: 25 items vs 27 expected  <-- MISS
          C-5.3 (Substantive) has 2, constitution says 3
          C-6.4 (Substantive) has 2, constitution says 3
      -> 6 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
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

serve sweep: {"9": "fill/forward -3s", "10": "fill/forward -1s", "11": "identity", "12": "rescue/complete (from 15)", "13": "fill/single -1s", "14": "fill/single", "15": "identity", "16": "rescue/complete (from 19)", "17": "fill/single", "18": "synthesis", "19": "identity", "20": "surrender", "21": "surrender"}

options arranged: 0 of 27 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_06_canonical.json: 0 of 9 item(s) re-ordered
      ch_06_canonical_p11.json: 0 of 9 item(s) re-ordered
      ch_06_canonical_p15.json: 0 of 9 item(s) re-ordered

DETERMINISTIC CHECKS ALL PASS.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
