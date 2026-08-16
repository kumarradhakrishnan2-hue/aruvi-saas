# Library certification · social_sciences VII ch 9 · 20260816_120415

plan: counts [21, 17, 13] · basis authored_standard · registry 15 sections

PASS  library complete: ['ch_09_canonical.json', 'ch_09_canonical_p17.json', 'ch_09_canonical_p13.json'] vs plan [21, 17, 13]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_09_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_09_canonical.json: every anchor verbatim in the top registry
PASS  ch_09_canonical.json: first-visit order follows the registry
PASS  ch_09_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_09_canonical_p17.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_09_canonical_p17.json: every anchor verbatim in the top registry
PASS  ch_09_canonical_p17.json: first-visit order follows the registry
PASS  ch_09_canonical_p17.json: coverage reaches the final registry section
PASS  ch_09_canonical_p13.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_09_canonical_p13.json: every anchor verbatim in the top registry
PASS  ch_09_canonical_p13.json: first-visit order follows the registry
PASS  ch_09_canonical_p13.json: coverage reaches the final registry section
PASS  ch_09_canonical.json: register scan reached the band text (84 band(s) read: {'activity_title': 21, 'materials': 63, 'teacher_notes': 21, 'time_bands': 84, 'visual_aids': 7})
PASS  ch_09_canonical.json: register clean (0 ban hit(s))
PASS  ch_09_canonical_p17.json: register scan reached the band text (68 band(s) read: {'activity_title': 17, 'materials': 59, 'teacher_notes': 17, 'time_bands': 68, 'visual_aids': 9})
PASS  ch_09_canonical_p17.json: register clean (0 ban hit(s))
      ADVISORY ch_09_canonical_p17.json: 1 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U12 time_bands[2] 22-34: 'from the earlier unit' — …— and asks students to apply the four-dimensions framework from the earlier unit: '1. Who grants authority? 2. How is the Supreme Leader for…
PASS  ch_09_canonical_p13.json: register scan reached the band text (52 band(s) read: {'activity_title': 13, 'materials': 33, 'teacher_notes': 13, 'time_bands': 52, 'visual_aids': 4})
PASS  ch_09_canonical_p13.json: register clean (0 ban hit(s))
PASS  ch_09_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_09_canonical_p17.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_09_canonical_p13.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_09_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_09_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_09_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_09_canonical_p17.json: every question_type is a known assessment type (0 not)
PASS  ch_09_canonical_p17.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_09_canonical_p17.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_09_canonical_p13.json: every question_type is a known assessment type (0 not)
PASS  ch_09_canonical_p13.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_09_canonical_p13.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_09_canonical.json: MCQ options in arrangement order
PASS  ch_09_canonical_p17.json: MCQ options in arrangement order
PASS  ch_09_canonical_p13.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"(from handoff)": 0, "Central": 5, "Present": 2, "Substantive": 3}
      ch_09_canonical.json: 12 items vs 12 expected
      ch_09_canonical_p17.json: 12 items vs 12 expected
      ch_09_canonical_p13.json: 13 items vs 15 expected  <-- MISS
          C-5.1 (Present) has 1, its siblings carry 2
          C-10.1 (Present) has 1, its siblings carry 2
      -> 2 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
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

serve sweep: {"11": "fill/single -1s", "12": "fill/single", "13": "identity", "14": "rescue/complete (from 17)", "15": "fill/single", "16": "synthesis", "17": "identity", "18": "fill/single", "19": "synthesis", "20": "synthesis", "21": "identity", "22": "surrender", "23": "surrender"}

options arranged: 0 of 24 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_09_canonical.json: 0 of 8 item(s) re-ordered
      ch_09_canonical_p13.json: 0 of 8 item(s) re-ordered
      ch_09_canonical_p17.json: 0 of 8 item(s) re-ordered

DETERMINISTIC CHECKS ALL PASS.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
