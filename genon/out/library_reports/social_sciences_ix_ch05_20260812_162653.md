# Library certification · social_sciences IX ch 5 · 20260812_162653

plan: counts [21, 17, 13] · basis authored_standard · registry 20 sections

FAIL  library complete: ['ch_05_canonical.json'] vs plan [21, 17, 13]
serve granularity: unit  ·  section axis: True
PASS  ch_05_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_05_canonical.json: every anchor verbatim in the top registry
PASS  ch_05_canonical.json: first-visit order follows the registry
PASS  ch_05_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_05_canonical.json: register scan reached the band text (84 band(s) read: {'activity_title': 21, 'materials': 47, 'visual_aids': 7, 'teacher_notes': 21, 'time_bands': 84})
FAIL  ch_05_canonical.json: register clean (2 ban hit(s))
      ADVISORY ch_05_canonical.json: 1 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U11 time_bands[2] 27-42: 'from the previous unit' — …ṇa. Students compare this Sangam model with the varṇa model from the previous unit by completing a two-column table: VARṆA MODEL / SANGAM OCCU…
      U2 time_bands[0] 0-10 [clock] …to date when it was composed?' Students think independently for two minutes, then share. Teacher records the core problem — oral transm…
      U21 time_bands[0] 0-12 [clock] …rigation, trade routes, guilds. Students work independently for five minutes, then share their labels. Teacher does not evaluate — colle…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_05_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_05_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_05_canonical.json: ['OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_05_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_05_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_05_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: constitution
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_05_canonical.json: 31 items vs 31 expected
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

serve sweep: {"11": "fill/single -9s", "12": "fill/single -8s", "13": "fill/single -7s", "14": "fill/single -6s", "15": "fill/single -5s", "16": "fill/single -4s", "17": "fill/single -3s", "18": "fill/single -2s", "19": "fill/single -1s", "20": "fill/single", "21": "identity", "22": "surrender", "23": "surrender"}

options arranged: 11 of 11 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_05_canonical.json: 11 of 11 item(s) re-ordered
          #1 C-1.3 U5: A–D now hold DBCA · correct B -> B
          #6 C-1.1 U10: A–D now hold BADC · correct B -> A
          #9 C-1.2 U5: A–D now hold BACD · correct A -> B
          #12 C-1.4 U15: A–D now hold CABD · correct B -> C
          #15 C-5.1 U4: A–D now hold DACB · correct B -> D
          #18 C-8.3 U18: A–D now hold CADB · correct B -> D
          #21 C-6.1 U9: A–D now hold BCAD · correct B -> A
          #24 C-5.4 U4: A–D now hold ADCB · correct B -> D
          #26 C-7.4 U18: A–D now hold BADC · correct B -> A
          #28 C-6.2 U10: A–D now hold BCDA · correct B -> A
          #30 C-9.1 U15: A–D now hold ABDC · correct B -> B

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
