# Library certification · social_sciences VII ch 12 · 20260816_092043

plan: counts [18, 15, 11] · basis authored_standard · registry 10 sections

FAIL  library complete: ['ch_12_canonical.json'] vs plan [18, 15, 11]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_12_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_12_canonical.json: every anchor verbatim in the top registry
PASS  ch_12_canonical.json: first-visit order follows the registry
PASS  ch_12_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_12_canonical.json: register scan reached the band text (72 band(s) read: {'activity_title': 18, 'materials': 67, 'teacher_notes': 18, 'time_bands': 72, 'visual_aids': 6})
FAIL  ch_12_canonical.json: register clean (3 ban hit(s))
      ADVISORY ch_12_canonical.json: 2 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U12 time_bands[1] 8-22: 'from the earlier unit' — …ling — connected to the government's maximum price controls from the earlier unit), name and address of manufacturer (accountability), nutrit…
        U13 time_bands[3] 34-40: 'from the previous unit' — …nt. Students add this insight to their three-item checklist from the previous unit.
      U1 time_bands[1] 8-20 [clock] …quire you to go further, or to go online?' Partners discuss for two minutes and report back.
      U2 time_bands[1] 6-20 [clock] …25 and want at least a dozen guavas.' Pairs negotiate aloud for two minutes and record the price they agreed on (or note if they could…
      U5 time_bands[0] 0-8 [clock] …a family in Chennai?' Students brainstorm in groups of four for three minutes and write the steps they imagine on strips of paper, one st…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_12_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_12_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_12_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_12_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_12_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_12_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_12_canonical.json: 14 items vs 14 expected
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

serve sweep: {"9": "fill/single -3s", "10": "fill/single -2s", "11": "fill/single -1s", "12": "fill/single", "13": "synthesis", "14": "synthesis", "15": "synthesis", "16": "synthesis", "17": "synthesis", "18": "identity", "19": "surrender", "20": "surrender"}

options arranged: 10 of 10 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_12_canonical.json: 10 of 10 item(s) re-ordered
          #1 C-9.1 U1: A–D now hold BCDA · correct B -> A
          #2 C-9.1 U6: A–D now hold BCAD · correct B -> A
          #6 C-4.1 U9: A–D now hold ACBD · correct C -> B
          #7 C-4.1 U11: A–D now hold DABC · correct C -> D
          #9 C-4.2 U9: A–D now hold BADC · correct B -> A
          #10 C-4.2 U11: A–D now hold BDCA · correct C -> C
          #11 C-6.2 U4: A–D now hold BADC · correct B -> A
          #12 C-6.2 U4: A–D now hold BADC · correct B -> A
          #13 C-10.1 U1: A–D now hold ACBD · correct B -> C
          #14 C-10.1 U11: A–D now hold BDAC · correct B -> A

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
