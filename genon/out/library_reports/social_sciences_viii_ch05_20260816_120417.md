# Library certification · social_sciences VIII ch 5 · 20260816_120417

plan: counts [12, 10, 7] · basis authored_standard · registry 11 sections

PASS  library complete: ['ch_05_canonical.json', 'ch_05_canonical_p10.json', 'ch_05_canonical_p07.json'] vs plan [12, 10, 7]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_05_canonical.json: 1 prose lead(s) in the summary match no registry entry (2 summary section(s) vs 11 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section
      ADVISORY ch_05_canonical.json: 10 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Universal Adult Franchise; The Role of the Election Commission of India (ECI); Election Commission of India — A brief introduction; Managing the electoral process; Model Code of Conduct (MCC); Election to the Lok Sabha and State Legislative Assemblies …
PASS  ch_05_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_05_canonical.json: every anchor verbatim in the top registry
PASS  ch_05_canonical.json: first-visit order follows the registry
PASS  ch_05_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_05_canonical_p10.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_05_canonical_p10.json: every anchor verbatim in the top registry
PASS  ch_05_canonical_p10.json: first-visit order follows the registry
PASS  ch_05_canonical_p10.json: coverage reaches the final registry section
PASS  ch_05_canonical_p07.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_05_canonical_p07.json: every anchor verbatim in the top registry
PASS  ch_05_canonical_p07.json: first-visit order follows the registry
PASS  ch_05_canonical_p07.json: coverage reaches the final registry section
PASS  ch_05_canonical.json: register scan reached the band text (60 band(s) read: {'activity_title': 12, 'materials': 24, 'visual_aids': 10, 'teacher_notes': 12, 'time_bands': 60})
PASS  ch_05_canonical.json: register clean (0 ban hit(s))
PASS  ch_05_canonical_p10.json: register scan reached the band text (40 band(s) read: {'activity_title': 10, 'materials': 28, 'visual_aids': 10, 'teacher_notes': 10, 'time_bands': 40})
PASS  ch_05_canonical_p10.json: register clean (0 ban hit(s))
PASS  ch_05_canonical_p07.json: register scan reached the band text (35 band(s) read: {'activity_title': 7, 'materials': 21, 'visual_aids': 6, 'teacher_notes': 7, 'time_bands': 35})
PASS  ch_05_canonical_p07.json: register clean (0 ban hit(s))
PASS  ch_05_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_05_canonical_p10.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_05_canonical_p07.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_05_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_05_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_05_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_05_canonical_p10.json: every question_type is a known assessment type (0 not)
PASS  ch_05_canonical_p10.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_05_canonical_p10.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_05_canonical_p07.json: every question_type is a known assessment type (0 not)
PASS  ch_05_canonical_p07.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_05_canonical_p07.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_05_canonical.json: MCQ options in arrangement order
PASS  ch_05_canonical_p10.json: MCQ options in arrangement order
PASS  ch_05_canonical_p07.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_05_canonical.json: 16 items vs 16 expected
      ch_05_canonical_p10.json: 15 items vs 16 expected  <-- MISS
          C-8.3 (Present) has 1, its siblings carry 2
      ch_05_canonical_p07.json: 16 items vs 16 expected
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

serve sweep: {"5": "fill/single -4s", "6": "fill/forward -1s", "7": "identity", "8": "rescue/complete (from 10)", "9": "fill/single", "10": "identity", "11": "fill/single", "12": "identity", "13": "surrender", "14": "surrender"}

options arranged: 0 of 35 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_05_canonical.json: 0 of 12 item(s) re-ordered
      ch_05_canonical_p07.json: 0 of 12 item(s) re-ordered
      ch_05_canonical_p10.json: 0 of 11 item(s) re-ordered
          #10 SKIPPED — cross-references an option label — left untouched, needs a human

DETERMINISTIC CHECKS ALL PASS.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
