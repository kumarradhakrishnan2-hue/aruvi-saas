# Library certification · social_sciences VIII ch 2 · 20260816_120416

plan: counts [15, 12, 9] · basis authored_standard · registry 12 sections

PASS  library complete: ['ch_02_canonical.json', 'ch_02_canonical_p12.json', 'ch_02_canonical_p09.json'] vs plan [15, 12, 9]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_02_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_02_canonical.json: every anchor verbatim in the top registry
PASS  ch_02_canonical.json: first-visit order follows the registry
PASS  ch_02_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_02_canonical_p12.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_02_canonical_p12.json: every anchor verbatim in the top registry
PASS  ch_02_canonical_p12.json: first-visit order follows the registry
PASS  ch_02_canonical_p12.json: coverage reaches the final registry section
PASS  ch_02_canonical_p09.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_02_canonical_p09.json: every anchor verbatim in the top registry
PASS  ch_02_canonical_p09.json: first-visit order follows the registry
PASS  ch_02_canonical_p09.json: coverage reaches the final registry section
PASS  ch_02_canonical.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 45, 'visual_aids': 15, 'teacher_notes': 15, 'time_bands': 60})
PASS  ch_02_canonical.json: register clean (0 ban hit(s))
      ADVISORY ch_02_canonical.json: 1 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U4 time_bands[3] 35-45: 'from the previous unit' — …a fragmentation mirrors the Bahmani→five Sultanates pattern from the previous unit, pointing to a recurring structure in Deccan political hist…
PASS  ch_02_canonical_p12.json: register scan reached the band text (48 band(s) read: {'activity_title': 12, 'materials': 36, 'visual_aids': 7, 'teacher_notes': 12, 'time_bands': 48})
PASS  ch_02_canonical_p12.json: register clean (0 ban hit(s))
      ADVISORY ch_02_canonical_p12.json: 1 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U12 time_bands[2] 25-38: 'revise their essay' — …rtners give written feedback in two sentences. Writers then revise their essay's closing argument (final two sentences only) based on the…
PASS  ch_02_canonical_p09.json: register scan reached the band text (36 band(s) read: {'activity_title': 9, 'materials': 24, 'visual_aids': 9, 'teacher_notes': 9, 'time_bands': 36})
PASS  ch_02_canonical_p09.json: register clean (0 ban hit(s))
PASS  ch_02_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_02_canonical_p12.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_02_canonical_p09.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_02_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_02_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_02_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_02_canonical_p12.json: every question_type is a known assessment type (0 not)
PASS  ch_02_canonical_p12.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_02_canonical_p12.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_02_canonical_p09.json: every question_type is a known assessment type (0 not)
PASS  ch_02_canonical_p09.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_02_canonical_p09.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_02_canonical.json: MCQ options in arrangement order
PASS  ch_02_canonical_p12.json: MCQ options in arrangement order
PASS  ch_02_canonical_p09.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_02_canonical.json: 19 items vs 19 expected
      ch_02_canonical_p12.json: 19 items vs 19 expected
      ch_02_canonical_p09.json: 16 items vs 19 expected  <-- MISS
          C-2.2 (Present) has 1, its siblings carry 2
          C-7.3 (Present) has 1, its siblings carry 2
          C-9.1 (Present) has 1, its siblings carry 2
      -> 3 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
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
PASS  X=17: choice set non-empty (no defensive truncation)

serve sweep: {"7": "fill/single -1s", "8": "fill/single -1s", "9": "identity", "10": "rescue/complete (from 12)", "11": "fill/single", "12": "identity", "13": "fill/single", "14": "synthesis", "15": "identity", "16": "surrender", "17": "surrender"}

options arranged: 0 of 39 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_02_canonical.json: 0 of 14 item(s) re-ordered
      ch_02_canonical_p09.json: 0 of 11 item(s) re-ordered
      ch_02_canonical_p12.json: 0 of 14 item(s) re-ordered
          #6 SKIPPED — cross-references an option label — left untouched, needs a human

DETERMINISTIC CHECKS ALL PASS.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
