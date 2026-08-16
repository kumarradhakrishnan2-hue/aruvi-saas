# Library certification · social_sciences VII ch 11 · 20260816_113723

plan: counts [14, 11, 8] · basis authored_standard · registry 8 sections

PASS  library complete: ['ch_11_canonical.json', 'ch_11_canonical_p11.json', 'ch_11_canonical_p08.json'] vs plan [14, 11, 8]
serve granularity: unit  ·  section axis: True
      ADVISORY: no section list readable from the chapter summary — registry <-> summary NOT reconciled for this chapter
PASS  ch_11_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_11_canonical.json: every anchor verbatim in the top registry
PASS  ch_11_canonical.json: first-visit order follows the registry
PASS  ch_11_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_11_canonical_p11.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_11_canonical_p11.json: every anchor verbatim in the top registry
PASS  ch_11_canonical_p11.json: first-visit order follows the registry
PASS  ch_11_canonical_p11.json: coverage reaches the final registry section
PASS  ch_11_canonical_p08.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_11_canonical_p08.json: every anchor verbatim in the top registry
PASS  ch_11_canonical_p08.json: first-visit order follows the registry
PASS  ch_11_canonical_p08.json: coverage reaches the final registry section
PASS  ch_11_canonical.json: register scan reached the band text (56 band(s) read: {'activity_title': 14, 'materials': 43, 'teacher_notes': 14, 'time_bands': 56, 'visual_aids': 5})
FAIL  ch_11_canonical.json: register clean (1 ban hit(s))
      U4 time_bands[2] 22-33 [calendar] …worth ₹800 but pays only ₹500 today and agrees to pay ₹300 next week — which function is in use? (c) A shopkeeper needs to compa…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_11_canonical_p11.json: register scan reached the band text (44 band(s) read: {'activity_title': 11, 'materials': 31, 'visual_aids': 7, 'teacher_notes': 11, 'time_bands': 44})
FAIL  ch_11_canonical_p11.json: register clean (5 ban hit(s))
      ADVISORY ch_11_canonical_p11.json: 1 artefact-dependency hit(s) — a unit reaching for something a PREVIOUS sitting produced. Read them: the brief forbids it, certification cannot.
        U10 teacher_notes: 'prepared beforehand' — …e and write the recommendation within this sitting; nothing prepared beforehand is needed.
      U1 time_bands[3] 30-40 [forward] …se one idea each; teacher notes responses on the board as a bridge to the problems the barter system creates, which the chapter will…
      U2 time_bands[0] 0-6 [clock] …tems through barter.' Individuals write their list silently for three minutes, then share with a neighbour.
      U7 time_bands[0] 0-7 [clock] …stop relying on coins alone?' Students brainstorm in pairs for two minutes, then share. Teacher lists responses on the board; expected…
      U8 time_bands[0] 0-7 [clock] …still complete the sale.' Students brainstorm individually for two minutes. Collect responses: expected answers include digital paymen…
      U10 teacher_notes [completion] …covers, asking students to apply the analytical vocabulary built across the chapter to a structured evaluative task — the comparison table form…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_11_canonical_p08.json: register scan reached the band text (32 band(s) read: {'activity_title': 8, 'materials': 24, 'visual_aids': 7, 'teacher_notes': 8, 'time_bands': 32})
FAIL  ch_11_canonical_p08.json: register clean (1 ban hit(s))
      U6 time_bands[0] 0-8 [clock] …mage tell us about the issuer? Students write independently for four minutes, then share one observation each in a quick round.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_11_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_11_canonical_p11.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_11_canonical_p08.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_11_canonical.json: every question_type is a known assessment type (0 not)
PASS  ch_11_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_11_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_11_canonical_p11.json: every question_type is a known assessment type (0 not)
PASS  ch_11_canonical_p11.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_11_canonical_p11.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_11_canonical_p08.json: every question_type is a known assessment type (0 not)
PASS  ch_11_canonical_p08.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_11_canonical_p08.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_11_canonical.json: MCQ options in arrangement order
PASS  ch_11_canonical_p11.json: MCQ options in arrangement order
PASS  ch_11_canonical_p08.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_11_canonical.json: 10 items vs 10 expected
      ch_11_canonical_p11.json: 10 items vs 10 expected
      ch_11_canonical_p08.json: 10 items vs 10 expected
PASS  X=6: choice set non-empty (no defensive truncation)
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

serve sweep: {"6": "fill/single -2s", "7": "fill/single -1s", "8": "identity", "9": "synthesis", "10": "synthesis", "11": "identity", "12": "synthesis", "13": "synthesis", "14": "identity", "15": "surrender", "16": "surrender"}

options arranged: 0 of 18 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_11_canonical.json: 0 of 6 item(s) re-ordered
      ch_11_canonical_p08.json: 0 of 6 item(s) re-ordered
      ch_11_canonical_p11.json: 0 of 6 item(s) re-ordered

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
