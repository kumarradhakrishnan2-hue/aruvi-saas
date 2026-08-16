# Library certification · social_sciences VIII ch 11 · 20260816_121914

plan: counts [15, 12, 9] · basis authored_standard · registry 14 sections

PASS  library complete: ['ch_11_canonical.json', 'ch_11_canonical_p12.json', 'ch_11_canonical_p09.json'] vs plan [15, 12, 9]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_11_canonical.json: 2 prose lead(s) in the summary match no registry entry (2 summary section(s) vs 14 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This section; The closing recap
      ADVISORY ch_11_canonical.json: 14 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Introduction; The Connection Between Law and Justice; The Judicial System in India; The Supreme Court of India; Writ Jurisdiction of the Supreme Court and High Court; Public Interest Litigation (PIL) filed under Articles 32 and 226 …
PASS  ch_11_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_11_canonical.json: every anchor verbatim in the top registry
PASS  ch_11_canonical.json: first-visit order follows the registry
PASS  ch_11_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_11_canonical_p12.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_11_canonical_p12.json: every anchor verbatim in the top registry
PASS  ch_11_canonical_p12.json: first-visit order follows the registry
PASS  ch_11_canonical_p12.json: coverage reaches the final registry section
PASS  ch_11_canonical_p09.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_11_canonical_p09.json: every anchor verbatim in the top registry
PASS  ch_11_canonical_p09.json: first-visit order follows the registry
PASS  ch_11_canonical_p09.json: coverage reaches the final registry section
PASS  ch_11_canonical.json: register scan reached the band text (60 band(s) read: {'activity_title': 15, 'materials': 30, 'visual_aids': 9, 'teacher_notes': 15, 'time_bands': 60})
PASS  ch_11_canonical.json: register clean (0 ban hit(s))
      ADVISORY ch_11_canonical.json: 2 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U8 time_bands[2] 22-35: 'from the earlier unit' — …ointment process to the Supreme Court's appointment process from the earlier unit, noting similarities and differences.
        U10 teacher_notes: 'from the previous unit' — …ligation over the subordinate judiciary is a natural bridge from the previous unit and reinforces the coherence of the three-tier system.
PASS  ch_11_canonical_p12.json: register scan reached the band text (48 band(s) read: {'activity_title': 12, 'materials': 30, 'teacher_notes': 12, 'time_bands': 48, 'visual_aids': 3})
PASS  ch_11_canonical_p12.json: register clean (0 ban hit(s))
PASS  ch_11_canonical_p09.json: register scan reached the band text (36 band(s) read: {'activity_title': 9, 'materials': 19, 'visual_aids': 8, 'teacher_notes': 9, 'time_bands': 36})
PASS  ch_11_canonical_p09.json: register clean (0 ban hit(s))
PASS  ch_11_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_11_canonical_p12.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_11_canonical_p09.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_11_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_11_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_11_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_11_canonical_p12.json: every question_type is a known assessment type (0 not)
PASS  ch_11_canonical_p12.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_11_canonical_p12.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_11_canonical_p09.json: every question_type is a known assessment type (0 not)
PASS  ch_11_canonical_p09.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_11_canonical_p09.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_11_canonical.json: MCQ options in arrangement order
PASS  ch_11_canonical_p12.json: MCQ options in arrangement order
PASS  ch_11_canonical_p09.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_11_canonical.json: 18 items vs 18 expected
      ch_11_canonical_p12.json: 18 items vs 18 expected
      ch_11_canonical_p09.json: 18 items vs 18 expected
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

serve sweep: {"7": "fill/forward -2s", "8": "fill/forward", "9": "identity", "10": "rescue/complete (from 12)", "11": "fill/forward -2s", "12": "identity", "13": "fill/forward", "14": "fill/single", "15": "identity", "16": "surrender", "17": "surrender"}

options arranged: 0 of 36 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_11_canonical.json: 0 of 12 item(s) re-ordered
      ch_11_canonical_p09.json: 0 of 12 item(s) re-ordered
          #9 SKIPPED — cross-references an option label — left untouched, needs a human
      ch_11_canonical_p12.json: 0 of 12 item(s) re-ordered

DETERMINISTIC CHECKS ALL PASS.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
