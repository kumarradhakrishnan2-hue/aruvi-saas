# Library certification · social_sciences VII ch 9 · 20260816_092042

plan: counts [21, 17, 13] · basis authored_standard · registry 15 sections

FAIL  library complete: ['ch_09_canonical.json'] vs plan [21, 17, 13]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_09_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_09_canonical.json: every anchor verbatim in the top registry
PASS  ch_09_canonical.json: first-visit order follows the registry
PASS  ch_09_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_09_canonical.json: register scan reached the band text (84 band(s) read: {'activity_title': 21, 'materials': 63, 'teacher_notes': 21, 'time_bands': 84, 'visual_aids': 7})
FAIL  ch_09_canonical.json: register clean (5 ban hit(s))
      U1 time_bands[1] 8-20 [clock] …enforce them, what would happen?' Students discuss in pairs for three minutes, then share briefly. The teacher uses this to anchor the ch…
      U6 time_bands[3] 36-40 [forward] …ystem and will be contrasted with the presidential model in the next unit of study.
      U9 time_bands[3] 36-40 [forward] …early example of merit-based, elected leadership — and that the next unit will examine Uttaramerur as a second, more detailed case.
      U17 teacher_notes [forward] …ndency previews the challenges section without naming it as the next unit.
      U18 teacher_notes [completion] …students to draw on evidence from all the government types covered across the chapter. Having examined monarchy, theocracy, dictatorship, and oli…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_09_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_09_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_09_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_09_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_09_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_09_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"(from handoff)": 0, "Central": 5, "Present": 2, "Substantive": 3}
      ch_09_canonical.json: 12 items vs 12 expected
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

serve sweep: {"11": "fill/single -5s", "12": "fill/single -5s", "13": "fill/single -4s", "14": "fill/single -3s", "15": "fill/single -2s", "16": "fill/single -1s", "17": "fill/single -1s", "18": "fill/single", "19": "synthesis", "20": "synthesis", "21": "identity", "22": "surrender", "23": "surrender"}

options arranged: 7 of 8 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_09_canonical.json: 7 of 8 item(s) re-ordered
          #1 C-4.1 U1: A–D now hold CBAD · correct B -> B
          #2 C-4.1 U3: A–D now hold CADB · correct B -> D
          #6 C-8.1 U9: A–D now hold DACB · correct B -> D
          #9 C-5.1 U4: A–D now hold BACD · correct B -> A
          #10 C-5.1 U15: A–D now hold CDAB · correct B -> D
          #11 C-10.1 U9: A–D now hold CBAD · correct B -> B
          #12 C-10.1 U11: A–D now hold CABD · correct B -> C

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
