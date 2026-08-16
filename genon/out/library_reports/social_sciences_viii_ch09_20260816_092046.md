# Library certification · social_sciences VIII ch 9 · 20260816_092046

plan: counts [17, 14, 10] · basis authored_standard · registry 16 sections

FAIL  library complete: ['ch_09_canonical.json'] vs plan [17, 14, 10]
serve granularity: unit  ·  section axis: True
      ADVISORY ch_09_canonical.json: 5 prose lead(s) in the summary match no registry entry (5 summary section(s) vs 16 registry entr(ies)) — rule on each by eye, a sub-topic is not a section: This short section; Before turning to the political front, the chapter; This section; The section; The closing recap consolidates the chapter's argument
      ADVISORY ch_09_canonical.json: 16 registry entr(ies) the summary does not name (an unlabelled opening, a merge or a rename — never a failure): Introduction; A Royal Proclamation; Reform Movements; Other Influences; The Rise of the Indian National Congress; Growing Discontent …
PASS  ch_09_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_09_canonical.json: every anchor verbatim in the top registry
PASS  ch_09_canonical.json: first-visit order follows the registry
PASS  ch_09_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_09_canonical.json: register scan reached the band text (68 band(s) read: {'activity_title': 17, 'materials': 37, 'visual_aids': 6, 'teacher_notes': 17, 'time_bands': 68})
FAIL  ch_09_canonical.json: register clean (6 ban hit(s))
      U2 time_bands[0] 0-8 [clock] …ach arrangement have for the British?' Students think aloud for two minutes, then the teacher establishes the Crown's 1858 takeover fro…
      U3 time_bands[3] 34-45 [clock] …to a future independent India.' Students write individually for eight minutes; two volunteers read their responses for class comment.
      U8 time_bands[0] 0-12 [clock] …boxes on either side of the daily's title?' Students write for five minutes, then share. Teacher adds: the same 1906 Calcutta session d…
      U9 time_bands[3] 36-45 [forward] …Plot' as further expressions of this revolutionary energy, previewing the next content threads.
      U11 time_bands[0] 0-10 [clock] …r sealed the main exit and fired approximately 1,650 rounds for about ten minutes, deliberately aiming at the thickest parts of the crowd. Of…
      U12 time_bands[3] 38-45 [forward] …in the independence movement's demands.' Teacher closes by previewing the Civil Disobedience Movement's Salt March as the chosen…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_09_canonical.json: every declared stimulus type resolves (0 mis-tagged)
PASS  ch_09_canonical.json: every question_type is a known assessment type (0 not)
      ADVISORY ch_09_canonical.json: ['ECR', 'OPEN_TASK'] used by exactly one item in the whole library — check it against the constitution's type table
PASS  ch_09_canonical.json: every non-OPEN_TASK item carries a stem (0 without)
PASS  ch_09_canonical.json: every OPEN_TASK carries an empty stem (0 not)
PASS  ch_09_canonical.json: MCQ options in arrangement order

item counts per competency — ADVISORY, does not gate; basis: derived (modal count across this library — no constitution row yet)
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_09_canonical.json: 21 items vs 22 expected  <-- MISS
          C-10.1 (Present) has 1, its siblings carry 2
      -> 1 competenc(ies) off the mandated count. Generation variance, accepted by default (ARV-D-019); a hand back-fill is forbidden (testing.md §7) — the only fix is regeneration, and that is a founder call on cost, not a certification failure.
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
PASS  X=18: choice set non-empty (no defensive truncation)
PASS  X=19: choice set non-empty (no defensive truncation)

serve sweep: {"8": "fill/single -8s", "9": "fill/single -7s", "10": "fill/single -6s", "11": "fill/single -5s", "12": "fill/single -4s", "13": "fill/single -3s", "14": "fill/single -2s", "15": "fill/single -1s", "16": "fill/single", "17": "identity", "18": "surrender", "19": "surrender"}

options arranged: 14 of 15 item(s) re-ordered this run. Nothing is written to the artefact (founder ruling 2026-08-04), so a 0 here means only that nothing was left to move — on a re-run that is expected, and it is NOT evidence the model arranged them unaided. Read this number on the FIRST pass of a freshly generated library or not at all.
      ch_09_canonical.json: 14 of 15 item(s) re-ordered
          #1 C-2.1 U2: A–D now hold BDAC · correct B -> A
          #2 C-2.1 U15: A–D now hold BCAD · correct C -> B
          #6 C-1.1 U4: A–D now hold BACD · correct A -> B
          #7 C-1.1 U11: A–D now hold CADB · correct B -> D
          #9 C-3.2 U7: A–D now hold CABD · correct C -> A
          #10 C-3.2 U14: A–D now hold BACD · correct C -> C
          #12 C-4.2 U5: A–D now hold ACBD · correct B -> C
          #13 C-4.2 U15: A–D now hold CADB · correct C -> A
          #16 C-2.2 U8: A–D now hold BDAC · correct B -> A
          #17 C-5.1 U2: A–D now hold CBAD · correct C -> A
          #18 C-5.1 U13: A–D now hold BCAD · correct C -> B
          #19 C-9.1 U13: A–D now hold BDAC · correct B -> A
          #20 C-9.1 U7: A–D now hold BADC · correct B -> A
          #21 C-10.1 U4: A–D now hold ABDC · correct B -> B

DETERMINISTIC CHECKS HAVE FAILURES — do not certify.
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
