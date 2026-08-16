# Library certification · social_sciences VI ch 7 · 20260816_121904

plan: counts [22, 18, 13] · basis authored_standard · registry 17 sections

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
PASS  ch_07_canonical_p13.json: coverage reaches the final registry section
PASS  ch_07_canonical.json: register scan reached the band text (88 band(s) read: {'activity_title': 22, 'materials': 44, 'visual_aids': 16, 'teacher_notes': 22, 'time_bands': 88})
PASS  ch_07_canonical.json: register clean (0 ban hit(s))
PASS  ch_07_canonical_p18.json: register scan reached the band text (72 band(s) read: {'activity_title': 18, 'materials': 36, 'visual_aids': 14, 'teacher_notes': 18, 'time_bands': 72})
PASS  ch_07_canonical_p18.json: register clean (0 ban hit(s))
      ADVISORY ch_07_canonical_p18.json: 1 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U11 time_bands[1] 12-24: 'from the previous unit' — …yse the story in groups of three, using three Jain concepts from the previous unit: 'Where in Rohineya's story can you see right action, right…
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

serve sweep: {"11": "fill/single -6s", "12": "fill/single -5s", "13": "identity", "14": "rescue/complete (from 18)", "15": "fill/single -2s", "16": "fill/single -1s", "17": "fill/single", "18": "identity", "19": "synthesis", "20": "synthesis", "21": "synthesis", "22": "identity", "23": "surrender", "24": "surrender"}

options arranged: 0 of 42 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_07_canonical.json: 0 of 14 item(s) re-ordered
      ch_07_canonical_p13.json: 0 of 14 item(s) re-ordered
      ch_07_canonical_p18.json: 0 of 14 item(s) re-ordered
          #6 SKIPPED — cross-references an option label — left untouched, needs a human

DETERMINISTIC CHECKS ALL PASS.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
