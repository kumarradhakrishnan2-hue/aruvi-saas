# Library certification · social_sciences VIII ch 14 · 20260816_121915

plan: counts [15, 12, 9] · basis authored_standard · registry 10 sections

PASS  library complete: ['ch_14_canonical.json', 'ch_14_canonical_p12.json', 'ch_14_canonical_p09.json'] vs plan [15, 12, 9]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_14_canonical.json: 3 prose lead(s) in the summary match no registry entry (3 summary section(s) vs 10 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section; This case study; The closing recap
      ADVISORY ch_14_canonical.json: 10 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Introduction; Population Density in Cities; How do Cities Become Centres of Economic Activities?; What Leads to Urbanisation?; Cities as Cultural Hubs; Challenges Faced by Cities …
PASS  ch_14_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_14_canonical.json: every anchor verbatim in the top registry
PASS  ch_14_canonical.json: first-visit order follows the registry
PASS  ch_14_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_14_canonical_p12.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_14_canonical_p12.json: every anchor verbatim in the top registry
PASS  ch_14_canonical_p12.json: first-visit order follows the registry
PASS  ch_14_canonical_p12.json: coverage reaches the final registry section
PASS  ch_14_canonical_p09.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_14_canonical_p09.json: every anchor verbatim in the top registry
PASS  ch_14_canonical_p09.json: first-visit order follows the registry
PASS  ch_14_canonical_p09.json: coverage reaches the final registry section
PASS  ch_14_canonical.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 46, 'visual_aids': 12, 'teacher_notes': 15, 'time_bands': 60})
PASS  ch_14_canonical.json: register clean (0 ban hit(s))
PASS  ch_14_canonical_p12.json: register scan reached the band text (48 band(s) read: {'activity_title': 12, 'materials': 40, 'visual_aids': 10, 'teacher_notes': 12, 'time_bands': 48})
PASS  ch_14_canonical_p12.json: register clean (0 ban hit(s))
PASS  ch_14_canonical_p09.json: register scan reached the band text (36 band(s) read: {'activity_title': 9, 'materials': 22, 'visual_aids': 9, 'teacher_notes': 9, 'time_bands': 36})
PASS  ch_14_canonical_p09.json: register clean (0 ban hit(s))
      ADVISORY ch_14_canonical_p09.json: 1 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U7 teacher_notes: 'from the previous unit' — The urban challenge framing from the previous unit sets up the Bengaluru case as a specific, resolvable instan…
PASS  ch_14_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_14_canonical_p12.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_14_canonical_p09.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_14_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_14_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_14_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_14_canonical_p12.json: every question_type is a known assessment type (0 not)
PASS  ch_14_canonical_p12.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_14_canonical_p12.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_14_canonical_p09.json: every question_type is a known assessment type (0 not)
PASS  ch_14_canonical_p09.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_14_canonical_p09.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_14_canonical.json: MCQ options in arrangement order
PASS  ch_14_canonical_p12.json: MCQ options in arrangement order
PASS  ch_14_canonical_p09.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_14_canonical.json: 18 items vs 18 expected
      ch_14_canonical_p12.json: 18 items vs 18 expected
      ch_14_canonical_p09.json: 18 items vs 18 expected
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

serve sweep: {"7": "fill/single -3s", "8": "fill/forward -1s", "9": "identity", "10": "rescue/complete (from 12)", "11": "fill/single", "12": "identity", "13": "synthesis", "14": "synthesis", "15": "identity", "16": "surrender", "17": "surrender"}

options arranged: 0 of 36 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_14_canonical.json: 0 of 12 item(s) re-ordered
      ch_14_canonical_p09.json: 0 of 12 item(s) re-ordered
      ch_14_canonical_p12.json: 0 of 12 item(s) re-ordered

DETERMINISTIC CHECKS ALL PASS.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
