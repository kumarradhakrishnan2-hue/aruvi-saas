# Library certification · social_sciences VIII ch 7 · 20260816_120111

plan: counts [12, 10, 7] · basis authored_standard · registry 11 sections

PASS  library complete: ['ch_07_canonical.json', 'ch_07_canonical_p10.json', 'ch_07_canonical_p07.json'] vs plan [12, 10, 7]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_07_canonical.json: 5 prose lead(s) in the summary match no registry entry (6 summary section(s) vs 11 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: Education and training; Healthcare; Social and cultural influences; The section; This section
      ADVISORY ch_07_canonical.json: 10 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Introduction; Land (natural resources); Labour (human resources); Facilitators of human capital; Challenges to human capital; India's ancient skill heritage …
PASS  ch_07_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_07_canonical.json: every anchor verbatim in the top registry
PASS  ch_07_canonical.json: first-visit order follows the registry
PASS  ch_07_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_07_canonical_p10.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_07_canonical_p10.json: every anchor verbatim in the top registry
PASS  ch_07_canonical_p10.json: first-visit order follows the registry
PASS  ch_07_canonical_p10.json: coverage reaches the final registry section
PASS  ch_07_canonical_p07.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_07_canonical_p07.json: every anchor verbatim in the top registry
PASS  ch_07_canonical_p07.json: first-visit order follows the registry
PASS  ch_07_canonical_p07.json: coverage reaches the final registry section
PASS  ch_07_canonical.json: register scan reached the band text (48 band(s) read: {'activity_title': 12, 'materials': 21, 'visual_aids': 5, 'teacher_notes': 12, 'time_bands': 48})
PASS  ch_07_canonical.json: register clean (0 ban hit(s))
PASS  ch_07_canonical_p10.json: register scan reached the band text (40 band(s) read: {'activity_title': 10, 'materials': 32, 'teacher_notes': 10, 'time_bands': 40})
FAIL  ch_07_canonical_p10.json: register clean (6 ban hit(s))
      U1 teacher_notes [forward] …hold this tension rather than resolving it prematurely, as the next unit addresses it directly. Encourage students to name specific…
      U4 time_bands[1] 8-22 [clock] …alises its demographic dividend?' Students discuss in pairs for three minutes, then share two or three responses.
      U6 time_bands[3] 36-45 [forward] …less so for large companies?' — leaving this as a question the Entrepreneurship unit will deepen.
      U7 time_bands[2] 22-35 [clock] …otivations other than money?' Small groups of three discuss for four minutes and share one insight each.
      U7 time_bands[3] 35-45 [forward] …ction — the difference is scale and formality.' Link to the upcoming unit by noting that technology increasingly shapes how entrepren…
      U8 time_bands[3] 35-45 [forward] …ing digital and physical technologies. Close by noting that the next unit examines how all five factors — including technology — work…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_07_canonical_p07.json: register scan reached the band text (28 band(s) read: {'activity_title': 7, 'materials': 20, 'visual_aids': 5, 'teacher_notes': 7, 'time_bands': 28})
FAIL  ch_07_canonical_p07.json: register clean (3 ban hit(s))
      U5 teacher_notes [forward] …r creates labour previews the interconnection discussion in the next unit without requiring that unit to have occurred.
      U5 teacher_notes [meta-leak] …ur previews the interconnection discussion in the next unit without requiring that unit to have occurred.
      U6 time_bands[1] 10-22 [forward] …second-largest mobile phone manufacturer as of 2025 as the bridge to the case study.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_07_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_07_canonical_p10.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_07_canonical_p07.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_07_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_07_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_07_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_07_canonical_p10.json: every question_type is a known assessment type (0 not)
PASS  ch_07_canonical_p10.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_07_canonical_p10.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_07_canonical_p07.json: every question_type is a known assessment type (0 not)
PASS  ch_07_canonical_p07.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_07_canonical_p07.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_07_canonical.json: MCQ options in arrangement order
PASS  ch_07_canonical_p10.json: MCQ options in arrangement order
PASS  ch_07_canonical_p07.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_07_canonical.json: 15 items vs 15 expected
      ch_07_canonical_p10.json: 15 items vs 15 expected
      ch_07_canonical_p07.json: 15 items vs 15 expected
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

serve sweep: {"5": "fill/single -2s", "6": "fill/single -1s", "7": "identity", "8": "rescue/complete (from 10)", "9": "fill/single -1s", "10": "identity", "11": "fill/single", "12": "identity", "13": "surrender", "14": "surrender"}

options arranged: 0 of 30 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_07_canonical.json: 0 of 10 item(s) re-ordered
      ch_07_canonical_p07.json: 0 of 10 item(s) re-ordered
      ch_07_canonical_p10.json: 0 of 10 item(s) re-ordered

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
