# Library certification · social_sciences IX ch 3 · 20260803_144039

plan: counts [12, 10, 7] · basis authored_standard · registry 9 sections

PASS  library complete: ['ch_03_canonical.json', 'ch_03_canonical_p10.json', 'ch_03_canonical_p07.json'] vs plan [12, 10, 7]
PASS  ch_03_canonical.json: standard closes with the mandated `synthesis` unit (and carries the token nowhere else)
PASS  ch_03_canonical.json: every anchor verbatim in the top registry
PASS  ch_03_canonical.json: first-visit order follows the registry
PASS  ch_03_canonical.json: coverage reaches the final registry section before the synthesis unit
PASS  ch_03_canonical_p10.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_03_canonical_p10.json: every anchor verbatim in the top registry
FAIL  ch_03_canonical_p10.json: first-visit order follows the registry
PASS  ch_03_canonical_p10.json: coverage reaches the final registry section
PASS  ch_03_canonical_p07.json: the `synthesis` token is reserved to the standard canonical
PASS  ch_03_canonical_p07.json: every anchor verbatim in the top registry
PASS  ch_03_canonical_p07.json: first-visit order follows the registry
PASS  ch_03_canonical_p07.json: coverage reaches the final registry section
PASS  ch_03_canonical.json: register scan reached the band text (48 band(s) read: {'activity_title': 12, 'teacher_notes': 12, 'time_bands': 48, 'homework': 1})
FAIL  ch_03_canonical.json: register clean (3 ban hit(s))
      U4 time_bands[2] 30-44 [clock] …er occasions have strong winds caused problems?' — is posed for two minutes of paired oral sharing.
      U8 time_bands[0] 0-8 [clock] …s the monsoon a resource, a hazard, or both?' Pairs discuss for three minutes and take one response each side.
      U11 time_bands[2] 30-44 [clock] …r planning have reduced the damage?' Groups of four discuss for five minutes and prepare a two-sentence position. Then: what role can st…
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_03_canonical_p10.json: register scan reached the band text (40 band(s) read: {'activity_title': 10, 'teacher_notes': 10, 'time_bands': 40})
FAIL  ch_03_canonical_p10.json: register clean (1 ban hit(s))
      U2 time_bands[3] 40-50 [forward] …in the opening section of the chapter would be affected?' — previewing the climate change thread without naming a future topic.
      -> declare the fixes in genon/repair_register.py and re-run --certify-only; do NOT hand-edit the artefact
PASS  ch_03_canonical_p07.json: register scan reached the band text (28 band(s) read: {'activity_title': 7, 'teacher_notes': 7, 'time_bands': 28, 'homework': 1})
PASS  ch_03_canonical_p07.json: register clean (0 ban hit(s))

item counts per competency — ADVISORY, does not gate; basis: constitution
      expected {"Central": 5, "Present": 2, "Substantive": 3}
      ch_03_canonical.json: 18 items vs 18 expected
      ch_03_canonical_p10.json: 18 items vs 18 expected
      ch_03_canonical_p07.json: 18 items vs 18 expected
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

serve sweep: {"5": "fill/single -2s", "6": "fill/single -1s", "7": "identity", "8": "fill/single -1s", "9": "fill/single", "10": "identity", "11": "fill/single", "12": "identity", "13": "surrender", "14": "surrender"}
QUARANTINED  ch_03_canonical_p10.json -> backup/quarantine/social_sciences/ix/ch_03_canonical_p10_20260803_144039.json

DETERMINISTIC CHECKS HAVE FAILURES — do not certify Failed files are QUARANTINED under backup/quarantine/ (the fix worklist); regenerate them and re-run --certify-only..
The HUMAN GATE remains: read the borrowed seams and each closing synthesis in a Cowork session before calling this chapter certified.
