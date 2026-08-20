# C5 check 12 — the ENGLISH advisory shortlist

Written 2026-08-19 with the check (ARV-D-188). Mathematics is at ZERO after the Tier-1
generic pass; every hit below is english, and english does NOT gate — `stem_deixis._GATES`
carries why. These are for a reader at C7, not for a repair tool.

Three kinds are mixed in here and only the first is a defect:

1. **A real dangling pointer** — *"Choose any one action word from the list below"* on an
   ORAL_PROMPT with no options and no list. The item cannot be answered.
2. **The poem or story is doing the pointing** — *"the child imagines people below staring
   up"*. The word belongs to the text, not to the plan.
3. **The referent lives in a spine-specific field** the detector does not read — the
   teacher's own reading on an ORAL_PROMPT, a `task_brief` on a WRITING_TASK.

29 item(s):

```
  english/iii/ch_02_canonical_p04.json Q-WW-B-2     figure    ref=—                             Choose any one action word from the list below. Say it aloud clearly,
  english/iii/ch_04_canonical_p09.json Q-WRITE-A-1  figure    ref=—                             Complete the sentence below about your best friend.
  english/iii/ch_09_canonical_p05.json Q-WORD-A-2   figure    ref=—                             Read the two sentences below. Replace the underlined name in the secon
  english/iv/ch_08_canonical_p09.json Q-WORD-A-2   figure    ref=—                             The scrambled letters below spell a word used in the story. Use the me
  english/iv/ch_09_canonical.json    Q-WRIT-A-1   figure    ref=—                             Read the sentence below and add one detail to complete it as a clear g
  english/iv/ch_09_canonical_p08.json Q-WRITE-A-2  figure    ref=—                             Just as the people of Nagaland created Hekko with its own name, teams,
  english/iv/ch_11_canonical.json    Q-BEXT-A-2   figure    ref=—                             Choose any one Himalayan animal from the list below and speak for abou
  english/ix/ch_09_canonical_p07.json Q-VGR-A-2    figure    ref=—                             The sentences below are in direct speech from Dr. Deepa Malik's interv
  english/v/ch_01_canonical.json     Q-WORD-A-2   figure    ref=—                             The poem is about 'a pair of spectacles'. Choose TWO other objects fro
  english/vi/ch_03_canonical_p06.json Q-BTX-C-2    figure    ref=—                             Design a small 'Emergency Contacts Chart' that a family could keep at
  english/vi/ch_04_canonical_p09.json Q-SPK-A-1    figure    ref=—                             Tell your classmates about a real friend of yours. Use the cues below
  english/vi/ch_05_canonical_p09.json Q-VG-B-2     figure    ref=—                             The poem says "With special friends I feel I'm blessed." The word 'ble
  english/vi/ch_05_canonical_p09.json Q-BT-B-1     figure    ref=—                             Read the two friendship quotations below and answer the questions that
  english/vi/ch_07_canonical.json    Q-VG-A-2     figure    ref=—                             The sentence below is from the neem dialogue, written in the present t
  english/vi/ch_14_canonical.json    Q-RFC-B-2    figure    ref=—                             In the final stanza of the poem, the child imagines looking down while
  english/vi/ch_14_canonical.json    Q-WRT-B-2    figure    ref=—                             Write a paragraph of about 80–100 words in the first person, imagining
  english/vi/ch_14_canonical.json    Q-VGR-B-2    figure    ref=—                             The poem uses the word ‘drift’ to describe how the child moves on the
  english/vi/ch_14_canonical_p05.json Q-RFC-B-2    figure    ref=—                             In the final stanza of the poem, the speaker imagines people below sta
  english/vi/ch_14_canonical_p05.json Q-WRT-B-1    figure    ref=—                             Using the hints below as a guide, write a short paragraph of about 80–
  english/vi/ch_14_canonical_p07.json Q-SPK-B-2    figure    ref=—                             The child in the poem wishes they could ride a kite and look down at p
  english/vi/ch_14_canonical_p07.json Q-WRT-B-2    figure    ref=—                             The poem ends with the child imagining people on the ground staring up
  english/vi/ch_14_canonical_p07.json Q-VGR-B-2    figure    ref=—                             The poem uses the word “drift” to describe how the child would move on
  english/vii/ch_09_canonical_p08.json Q-VG-C-2     figure    ref=—                             Four sentences below describe scenes from Shaana's journey across Indi
  english/vii/ch_09_canonical_p08.json Q-BT-C-1     figure    ref=—                             Shaana's journey takes her to many regions of India, each known for a
  english/viii/ch_02_canonical.json  Q-VG-B-2     figure    ref=—                             The poem describes Mrs. Jones’s sundial as a ‘device’. Choose ONE of t
  english/viii/ch_02_canonical_p05.json Q-VG-B-2     figure    ref=—                             The poem uses the word ‘soil’ as part of the garden world Mrs. Jones i
  english/viii/ch_05_canonical.json  Q-BTX-B-2    figure    ref=—                             Create a gratitude card for your mother or grandmother. The card must:
  english/viii/ch_06_canonical_p05.json Q-BT-C-2     figure    ref=—                             India's three major agricultural revolutions — White (dairy), Green (f
  english/viii/ch_13_canonical_p09.json Q-WRT-A-1    figure    ref=—                             A school magazine has invited students to contribute a short article.
```

## What to do with it

Nothing automatically. A generic repair cannot tell kind 1 from kind 2, and repointing a
pointer with nowhere to point replaces a visible defect with an invisible one. Read the list
at english's C7; the kind-1 items are declared stem repairs, one at a time.